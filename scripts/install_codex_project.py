#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(message)


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        fail(result.stderr.strip() or f"git {' '.join(args)} a échoué")
    return result.stdout.strip()


def directory_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: str(item.relative_to(root))):
        if path.is_symlink():
            fail(f"Lien symbolique interdit dans un skill géré : {path}")
        if not path.is_file():
            continue
        digest.update(str(path.relative_to(root)).encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def safe_target(value: str, source_root: Path) -> Path:
    target = Path(value).expanduser().resolve()
    forbidden = {Path("/").resolve(), Path.home().resolve(), source_root.resolve()}
    if target in forbidden:
        fail(f"Cible dangereuse refusée : {target}")
    if not target.is_dir():
        fail(f"Le projet cible n'existe pas : {target}")
    return target


def source_revision(source_root: Path, ref: str) -> str:
    if run_git(source_root, "status", "--porcelain"):
        fail("Le dépôt source doit être propre")
    head = run_git(source_root, "rev-parse", "HEAD")
    wanted = run_git(source_root, "rev-list", "-n", "1", ref)
    if head != wanted:
        fail(f"Le dépôt source n'est pas positionné sur {ref}")
    return head


def marketplace_plugins(source_root: Path, selected: list[str]) -> tuple[str, list[dict], dict[str, Path]]:
    marketplace_path = source_root / ".agents" / "plugins" / "marketplace.json"
    marketplace = json.loads(marketplace_path.read_text())
    available = {plugin["name"]: plugin for plugin in marketplace["plugins"]}
    unknown = sorted(set(selected) - set(available))
    if unknown:
        fail(f"Plugins inconnus : {', '.join(unknown)}")

    plugins = []
    skills = {}
    repositories = set()
    for name in selected:
        relative = available[name]["source"]["path"]
        plugin_root = (source_root / relative).resolve()
        if source_root.resolve() not in plugin_root.parents:
            fail(f"Source hors dépôt refusée pour {name}")
        manifest = json.loads((plugin_root / ".codex-plugin" / "plugin.json").read_text())
        repositories.add(manifest["repository"])
        plugins.append({"name": name, "version": manifest["version"]})
        for skill_root in sorted((plugin_root / "skills").iterdir()):
            if not skill_root.is_dir() or not (skill_root / "SKILL.md").is_file():
                continue
            if skill_root.name in skills:
                fail(f"Skill dupliqué dans la sélection : {skill_root.name}")
            directory_hash(skill_root)
            skills[skill_root.name] = skill_root
    if len(repositories) != 1:
        fail("Les plugins sélectionnés doivent partager le même dépôt")
    return marketplace["name"], plugins, skills


def lock_path(target: Path, marketplace: str) -> Path:
    return target / ".agents" / "plugins" / f"{marketplace}.lock.json"


def read_lock(path: Path) -> dict | None:
    if not path.is_file():
        return None
    data = json.loads(path.read_text())
    if data.get("schema_version") != 1 or not isinstance(data.get("skills"), dict):
        fail(f"Lock invalide : {path}")
    return data


def verify_managed(skills_root: Path, lock: dict) -> list[str]:
    drift = []
    for name, expected in lock["skills"].items():
        skill_root = skills_root / name
        if not skill_root.is_dir() or directory_hash(skill_root) != expected:
            drift.append(name)
    return drift


def write_json_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def replace_installation(stage: Path, destination: Path, backup: Path, lock_file: Path, new_lock: dict) -> None:
    moved = False
    try:
        if destination.exists():
            os.replace(destination, backup)
            moved = True
        os.replace(stage, destination)
        write_json_atomic(lock_file, new_lock)
    except Exception:
        if destination.exists():
            shutil.rmtree(destination)
        if moved and backup.exists():
            os.replace(backup, destination)
        raise
    if backup.exists():
        shutil.rmtree(backup)


def install(args: argparse.Namespace) -> None:
    source_root = Path(args.source_root).expanduser().resolve()
    target = safe_target(args.target, source_root)
    revision = source_revision(source_root, args.ref)
    marketplace, plugins, sources = marketplace_plugins(source_root, args.plugins)
    destination = target / ".agents" / "skills"
    lock_file = lock_path(target, marketplace)
    previous = read_lock(lock_file)
    if previous:
        drift = verify_managed(destination, previous)
        if drift:
            fail(f"Copies gérées modifiées localement : {', '.join(drift)}")

    agents_root = target / ".agents"
    agents_root.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".skills-stage-", dir=agents_root))
    backup = agents_root / f".skills-backup-{os.getpid()}"
    try:
        if destination.is_dir():
            shutil.copytree(destination, stage, dirs_exist_ok=True, symlinks=True)
        previous_names = set(previous["skills"]) if previous else set()
        for name in sorted(previous_names | set(sources)):
            staged_skill = stage / name
            if staged_skill.exists() or staged_skill.is_symlink():
                if name not in previous_names:
                    fail(f"Collision avec un skill non géré : {name}")
                if staged_skill.is_dir() and not staged_skill.is_symlink():
                    shutil.rmtree(staged_skill)
                else:
                    staged_skill.unlink()
        for name, source in sources.items():
            shutil.copytree(source, stage / name)

        hashes = {name: directory_hash(stage / name) for name in sorted(sources)}
        repository = json.loads(
            (next(iter(sources.values())).parents[1] / ".codex-plugin" / "plugin.json").read_text()
        )["repository"]
        new_lock = {
            "schema_version": 1,
            "marketplace": marketplace,
            "repository": repository,
            "ref": args.ref,
            "commit": revision,
            "installed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "plugins": plugins,
            "skills": hashes,
        }

        replace_installation(stage, destination, backup, lock_file, new_lock)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    print(f"{len(sources)} skills installés depuis {marketplace}@{args.ref}")


def check(args: argparse.Namespace) -> None:
    target = Path(args.target).expanduser().resolve()
    current = read_lock(lock_path(target, args.marketplace))
    if not current:
        fail(f"Installation absente : {args.marketplace}")
    drift = verify_managed(target / ".agents" / "skills", current)
    if drift:
        fail(f"Dérive détectée : {', '.join(drift)}")
    print(f"Installation {args.marketplace}@{current['ref']} conforme")


def main() -> None:
    parser = argparse.ArgumentParser(description="Installe des plugins dans .agents/skills à portée projet.")
    commands = parser.add_subparsers(dest="command", required=True)
    install_parser = commands.add_parser("install")
    install_parser.add_argument("--source-root", default=str(ROOT))
    install_parser.add_argument("--target", required=True)
    install_parser.add_argument("--ref", required=True)
    install_parser.add_argument("--plugins", nargs="+", required=True)
    install_parser.set_defaults(func=install)
    check_parser = commands.add_parser("check")
    check_parser.add_argument("--target", required=True)
    check_parser.add_argument("--marketplace", required=True)
    check_parser.set_defaults(func=check)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
