#!/usr/bin/env python3
"""Génère une page de correction à partir du template + d'une fixture + d'une config.

Usage : generer_page.py <fixture.json> <config.json> <out.html>

Remplace /*__KIT_CONFIG__*/ et /*__PLAUD_DATA__*/ dans correction-template.html
(le sibling de ce script) par du JSON brut, via str.replace (pas de regex :
le template contient des accolades/parenthèses qu'une regex abîmerait).
Si config.entreprise.logo pointe vers un fichier (chemin relatif au config.json),
il est inliné en data URI avant l'injection.
"""
import base64
import json
import mimetypes
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "correction-template.html"


def inline_logo(config: dict, config_path: Path) -> dict:
    entreprise = config.get("entreprise") or {}
    logo = entreprise.get("logo") or ""
    if not logo:
        return config
    logo_path = Path(logo)
    if not logo_path.is_absolute():
        logo_path = (config_path.parent / logo_path).resolve()
    if not logo_path.is_file():
        raise FileNotFoundError(f"logo introuvable : {logo_path}")
    mime, _ = mimetypes.guess_type(logo_path.name)
    mime = mime or "application/octet-stream"
    data = base64.b64encode(logo_path.read_bytes()).decode("ascii")
    entreprise = {**entreprise, "logo": f"data:{mime};base64,{data}"}
    return {**config, "entreprise": entreprise}


def main() -> None:
    if len(sys.argv) != 4:
        sys.exit(f"usage: {sys.argv[0]} <fixture.json> <config.json> <out.html>")
    fixture_path, config_path, out_path = (Path(a) for a in sys.argv[1:4])

    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config = inline_logo(config, config_path.resolve())

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("/*__KIT_CONFIG__*/", json.dumps(config, ensure_ascii=False))
    html = html.replace("/*__PLAUD_DATA__*/", json.dumps(fixture, ensure_ascii=False))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"écrit → {out_path}")


if __name__ == "__main__":
    main()
