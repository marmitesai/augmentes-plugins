#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_catalog() -> dict:
    data = yaml.safe_load((ROOT / "catalog.yaml").read_text())
    if not isinstance(data, dict) or not isinstance(data.get("plugins"), list):
        raise SystemExit("catalog.yaml invalide")
    return data


def json_text(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def author(data: dict) -> dict:
    result = {"name": data["name"]}
    for key in ("email", "url"):
        if data.get(key):
            result[key] = data[key]
    return result


def plugin_manifests(catalog: dict, plugin: dict) -> dict[Path, str]:
    publisher = author(catalog["owner"])
    common = {
        "name": plugin["name"],
        "version": plugin["version"],
        "description": plugin["description"],
        "author": publisher,
        "homepage": catalog["homepage"],
        "repository": catalog["repository"],
        "license": catalog["license"],
        "keywords": plugin.get("keywords", []),
    }
    claude = dict(common)
    codex = {
        **common,
        "skills": "./skills/",
        "interface": {
            "displayName": plugin["display_name"],
            "shortDescription": plugin["short_description"],
            "longDescription": plugin["description"],
            "developerName": catalog["owner"]["name"],
            "category": plugin.get("category", "Productivity"),
            "capabilities": plugin.get("capabilities", ["Skills"]),
            "defaultPrompt": plugin.get("default_prompts", [])[:3],
        },
    }
    for source, target in (
        ("website_url", "websiteURL"),
        ("privacy_policy_url", "privacyPolicyURL"),
        ("terms_url", "termsOfServiceURL"),
    ):
        if catalog.get(source):
            codex["interface"][target] = catalog[source]
    base = ROOT / "plugins" / plugin["name"]
    return {
        base / ".claude-plugin" / "plugin.json": json_text(claude),
        base / ".codex-plugin" / "plugin.json": json_text(codex),
    }


def marketplace_manifests(catalog: dict) -> dict[Path, str]:
    codex_plugins = []
    claude_plugins = []
    for plugin in catalog["plugins"]:
        codex_plugins.append(
            {
                "name": plugin["name"],
                "source": {"source": "local", "path": f"./plugins/{plugin['name']}"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": plugin.get("category", "Productivity"),
            }
        )
        claude_plugins.append(
            {
                "name": plugin["name"],
                "version": plugin["version"],
                "source": f"./plugins/{plugin['name']}",
                "description": plugin["description"],
                "author": author(catalog["owner"]),
                "category": plugin.get("category", "Productivity").lower(),
                "homepage": catalog["homepage"],
                "repository": catalog["repository"],
                "license": catalog["license"],
            }
        )
    codex = {
        "name": catalog["marketplace"]["name"],
        "interface": {"displayName": catalog["marketplace"]["display_name"]},
        "plugins": codex_plugins,
    }
    claude = {
        "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
        "name": catalog["marketplace"]["name"],
        "description": catalog["marketplace"]["description"],
        "owner": author(catalog["owner"]),
        "plugins": claude_plugins,
    }
    return {
        ROOT / ".agents" / "plugins" / "marketplace.json": json_text(codex),
        ROOT / ".claude-plugin" / "marketplace.json": json_text(claude),
    }


def expected_files(catalog: dict) -> dict[Path, str]:
    files = marketplace_manifests(catalog)
    for plugin in catalog["plugins"]:
        files.update(plugin_manifests(catalog, plugin))
    return files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files = expected_files(load_catalog())
    stale = []
    for path, content in files.items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(path.relative_to(ROOT))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    if stale:
        names = "\n".join(f"- {path}" for path in stale)
        raise SystemExit(f"Fichiers générés absents ou périmés :\n{names}")
    print(f"{len(files)} fichiers {'vérifiés' if args.check else 'générés'}")


if __name__ == "__main__":
    main()
