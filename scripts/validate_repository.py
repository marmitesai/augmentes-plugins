#!/usr/bin/env python3

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECRET_PATTERNS = {
    "clé privée": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "jeton connu": re.compile(
        r"ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|"
        r"xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{30,}"
    ),
    "chemin personnel": re.compile(r"/Users/[^ /]+|Dropbox-Marmites"),
    "IP privée": re.compile(
        r"(?<!\d)(?:(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
        r"192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?!\d)"
    ),
    "marqueur d'accès interne": re.compile(
        r"CF_ACCESS_CLIENT_SECRET|COCKPIT_API_TOKEN|client[_-]?secret|access[_-]?token",
        re.IGNORECASE,
    ),
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def frontmatter(path: Path, errors: list[str]) -> dict:
    content = path.read_text()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        fail(errors, f"{path.relative_to(ROOT)} : frontmatter absent")
        return {}
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        fail(errors, f"{path.relative_to(ROOT)} : YAML invalide ({exc})")
        return {}
    if not isinstance(data, dict):
        fail(errors, f"{path.relative_to(ROOT)} : frontmatter non objet")
        return {}
    return data


def validate() -> list[str]:
    errors: list[str] = []
    catalog = yaml.safe_load((ROOT / "catalog.yaml").read_text())
    plugins = catalog.get("plugins", [])
    plugin_names = [plugin.get("name") for plugin in plugins]
    if len(plugin_names) != len(set(plugin_names)):
        fail(errors, "catalog.yaml : noms de plugins dupliqués")
    declared_skills: set[str] = set()
    for plugin in plugins:
        plugin_name = plugin.get("name", "")
        if not NAME.fullmatch(plugin_name):
            fail(errors, f"nom de plugin invalide : {plugin_name}")
            continue
        plugin_root = ROOT / "plugins" / plugin_name
        actual = {path.name for path in (plugin_root / "skills").iterdir() if path.is_dir()}
        expected = set(plugin.get("skills", []))
        if actual != expected:
            fail(errors, f"{plugin_name} : skills réels {sorted(actual)} != catalogue {sorted(expected)}")
        for skill_name in sorted(actual):
            skill_file = plugin_root / "skills" / skill_name / "SKILL.md"
            if not skill_file.exists():
                fail(errors, f"{skill_file.relative_to(ROOT)} absent")
                continue
            data = frontmatter(skill_file, errors)
            if data.get("name") != skill_name:
                fail(errors, f"{skill_file.relative_to(ROOT)} : name différent du dossier")
            if skill_name in declared_skills:
                fail(errors, f"skill dupliqué dans le dépôt : {skill_name}")
            declared_skills.add(skill_name)
            description = data.get("description")
            if not isinstance(description, str) or not description.strip():
                fail(errors, f"{skill_file.relative_to(ROOT)} : description absente")
        for manifest in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
            if not (plugin_root / manifest).exists():
                fail(errors, f"{plugin_name}/{manifest} absent")
    if catalog.get("public"):
        for path in (ROOT / "plugins").rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            try:
                content = path.read_text()
            except UnicodeDecodeError:
                continue
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(content):
                    fail(errors, f"{path.relative_to(ROOT)} : {label} détecté")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(f"ERREUR : {problem}" for problem in problems), file=sys.stderr)
        raise SystemExit(1)
    print("Dépôt valide")
