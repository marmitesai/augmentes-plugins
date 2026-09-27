#!/usr/bin/env python3
"""Construit le ZIP d'une recette maison servie par learn, depuis ce dépôt, à un tag.

Usage : python3 scripts/build_learn_zip.py <slug> <tag> <version>
Ex    : python3 scripts/build_learn_zip.py kit-plaud v1.0.0-rc.7 1.1   -> dist/kit-plaud-v1.1.zip

Les fichiers sont lus au tag (git archive), jamais dans la copie de travail. La racine
de l'archive et le `name:` du SKILL.md gardent le slug de learn : c'est le dossier que
les clients ont installé dans ~/.claude/skills/, une mise à jour doit le remplacer.
Exclus : tests/, apercu/, __pycache__/, .DS_Store, config.json.
Jamais `zip` en ligne de commande : drapeau UTF-8 (bit 11) et NFC, sinon les accents
cassent sous Windows. Dates fixées : le même tag donne la même empreinte.
"""
import hashlib
import io
import re
import subprocess
import sys
import tarfile
import unicodedata
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
RECETTES_LEARN = {
    "kit-plaud": "plugins/augmentes-meetings/skills/plaud",
    "le-point": "plugins/augmentes-pilotage/skills/le-point",
}
DOSSIERS_EXCLUS = {"tests", "apercu", "__pycache__"}
FICHIERS_EXCLUS = {".DS_Store", "config.json"}
DATE_FIXE = (2026, 1, 1, 0, 0, 0)


def fichiers_au_tag(source, tag):
    """(chemin relatif à la skill, octets) pour chaque fichier de `source` au tag."""
    tar = subprocess.run(["git", "-C", str(RACINE), "archive", "--format=tar", tag, source],
                         capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as archive:
        for membre in archive.getmembers():
            if membre.isfile():
                yield membre.name[len(source) + 1:], archive.extractfile(membre).read()


def construire(slug, tag, version, dist=RACINE / "dist"):
    if slug not in RECETTES_LEARN:
        raise ValueError(f"recette inconnue : {slug} (connues : {', '.join(RECETTES_LEARN)})")
    source = RECETTES_LEARN[slug]
    dist.mkdir(parents=True, exist_ok=True)
    chemin = dist / f"{slug}-v{version}.zip"
    with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED) as zf:
        for relatif, contenu in sorted(fichiers_au_tag(source, tag)):
            parties = relatif.split("/")
            if DOSSIERS_EXCLUS & set(parties[:-1]) or parties[-1] in FICHIERS_EXCLUS:
                continue
            if relatif == "SKILL.md":
                texte = re.sub(r"(?m)^name: .*$", f"name: {slug}", contenu.decode("utf-8"), count=1)
                contenu = texte.encode("utf-8")
            info = zipfile.ZipInfo(unicodedata.normalize("NFC", f"{slug}/{relatif}"), DATE_FIXE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, contenu)
    return chemin, hashlib.sha256(chemin.read_bytes()).hexdigest()


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    chemin, empreinte = construire(*sys.argv[1:])
    print(f"{empreinte}  {chemin.name}")


if __name__ == "__main__":
    main()
