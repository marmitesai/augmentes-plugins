#!/usr/bin/env python3

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-rc\.\d+)?$")
VALID_SCOPES = {"user", "project"}
VALID_CHANNELS = {"pilot", "stable"}
VALID_CLASSIFICATIONS = {"personal", "internal", "restricted", "public"}
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
SKILL_TOKEN = r"(?:m-[a-z0-9]+(?:-[a-z0-9]+)*|daily-brief|done-dev|point-dev|update-mes-sessions)"
SKILL_REFERENCE = re.compile(
    rf"(?:\[\[(?P<wiki>{SKILL_TOKEN})(?:[|#][^\]]*)?\]\]|"
    rf"`(?P<code>{SKILL_TOKEN})`|(?<![\w-])[$/](?P<sigil>{SKILL_TOKEN})(?![a-z0-9*/-]))"
)
MCP_REFERENCE = re.compile(r"\bmcp__[A-Za-z0-9_-]+__[A-Za-z0-9_-]+\b")
LOCAL_RESOURCE = re.compile(
    r"\$(?:SK|SKILL|SKILL_DIR)/(?P<path>[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\.(?:py|sh|js|mjs|html|json|yaml|yml))"
)
FORBIDDEN_REFERENCES = {
    "atelier Dropbox obsolète": re.compile(r"(?:\$DEXTER|_DEXTER)/Devs(?:/|\b)"),
    "ancien dossier Claude": re.compile(r"(?:~|\$HOME)/\.claude/(?:skills|scripts)/"),
    "ancien outil Plaud": re.compile(r"\bmcp__plaud__plaud_get_recent\b"),
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


def declared_reference_set(catalog: dict, key: str, errors: list[str]) -> set[str]:
    references = catalog.get("references", {})
    values = references.get(key, []) if isinstance(references, dict) else []
    if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
        fail(errors, f"catalog.yaml : references.{key} doit être une liste de chaînes")
        return set()
    if len(values) != len(set(values)):
        fail(errors, f"catalog.yaml : references.{key} contient des doublons")
    return set(values)


def validate_references(
    skill_files: list[Path], declared_skills: set[str], catalog: dict, errors: list[str], root: Path = ROOT
) -> None:
    external_skills = declared_reference_set(catalog, "skills", errors)
    allowed_mcp_tools = declared_reference_set(catalog, "mcp_tools", errors)
    collisions = external_skills & declared_skills
    if collisions:
        fail(errors, f"catalog.yaml : skills externes aussi locaux {sorted(collisions)}")
    used_external_skills: set[str] = set()
    used_mcp_tools: set[str] = set()
    for skill_file in skill_files:
        content = skill_file.read_text()
        relative = skill_file.relative_to(root)
        for label, pattern in FORBIDDEN_REFERENCES.items():
            if pattern.search(content):
                fail(errors, f"{relative} : {label} détecté")
        referenced_skills = {
            next(value for value in match.groups() if value)
            for match in SKILL_REFERENCE.finditer(content)
        }
        unknown_skills = referenced_skills - declared_skills - external_skills
        if unknown_skills:
            fail(errors, f"{relative} : skills référencés inconnus {sorted(unknown_skills)}")
        used_external_skills.update(referenced_skills & external_skills)
        referenced_mcp_tools = set(MCP_REFERENCE.findall(content))
        unknown_mcp_tools = referenced_mcp_tools - allowed_mcp_tools
        if unknown_mcp_tools:
            fail(errors, f"{relative} : outils MCP non déclarés {sorted(unknown_mcp_tools)}")
        used_mcp_tools.update(referenced_mcp_tools)
        for match in LOCAL_RESOURCE.finditer(content):
            resource = skill_file.parent / match.group("path")
            if not resource.is_file():
                fail(errors, f"{relative} : ressource locale absente {match.group('path')}")
    unused_skills = external_skills - used_external_skills
    if unused_skills:
        fail(errors, f"catalog.yaml : skills externes non référencés {sorted(unused_skills)}")
    unused_mcp_tools = allowed_mcp_tools - used_mcp_tools
    if unused_mcp_tools:
        fail(errors, f"catalog.yaml : outils MCP non référencés {sorted(unused_mcp_tools)}")


def validate() -> list[str]:
    errors: list[str] = []
    catalog = yaml.safe_load((ROOT / "catalog.yaml").read_text())
    for filename in ("CHANGELOG.md", "GOVERNANCE.md"):
        if not (ROOT / filename).is_file():
            fail(errors, f"{filename} absent")
    distribution = catalog.get("distribution", {})
    if not isinstance(distribution.get("audience"), str) or not distribution["audience"].strip():
        fail(errors, "catalog.yaml : audience absente")
    if distribution.get("default_scope") not in VALID_SCOPES:
        fail(errors, "catalog.yaml : default_scope doit valoir user ou project")
    channel = distribution.get("release_channel")
    if channel not in VALID_CHANNELS:
        fail(errors, "catalog.yaml : release_channel doit valoir pilot ou stable")
    if distribution.get("data_classification") not in VALID_CLASSIFICATIONS:
        fail(errors, "catalog.yaml : data_classification invalide")
    if distribution.get("secrets") != "forbidden":
        fail(errors, "catalog.yaml : secrets doit valoir forbidden")
    if distribution.get("runtime_data") != "local-only":
        fail(errors, "catalog.yaml : runtime_data doit valoir local-only")
    plugins = catalog.get("plugins", [])
    plugin_names = [plugin.get("name") for plugin in plugins]
    if len(plugin_names) != len(set(plugin_names)):
        fail(errors, "catalog.yaml : noms de plugins dupliqués")
    declared_skills: set[str] = set()
    skill_files: list[Path] = []
    for plugin in plugins:
        plugin_name = plugin.get("name", "")
        version = plugin.get("version", "")
        if not SEMVER.fullmatch(version):
            fail(errors, f"{plugin_name} : version SemVer invalide ({version})")
        elif channel == "pilot" and "-rc." not in version:
            fail(errors, f"{plugin_name} : le canal pilot exige une version -rc.N")
        elif channel == "stable" and "-rc." in version:
            fail(errors, f"{plugin_name} : le canal stable refuse une version de test")
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
            skill_files.append(skill_file)
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
    validate_references(skill_files, declared_skills, catalog, errors)
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
