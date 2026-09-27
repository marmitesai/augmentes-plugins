import importlib.util
import subprocess
import tempfile
import unittest
import unicodedata
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
SCRIPT = RACINE / "scripts" / "build_learn_zip.py"
SCRUB = RACINE / "scripts" / "scrub-check.sh"


def charger():
    spec = importlib.util.spec_from_file_location("build_learn_zip", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ZipDeLearn(unittest.TestCase):
    """Les ZIP de learn se construisent ici, au tag, sous le slug que les clients ont installé."""

    def construire(self, slug):
        dossier = Path(tempfile.mkdtemp())
        chemin, empreinte = charger().construire(slug, "HEAD", "9.9", dossier)
        return chemin, empreinte

    def test_la_racine_et_le_nom_restent_le_slug_de_learn(self):
        chemin, _ = self.construire("kit-plaud")
        self.assertEqual(chemin.name, "kit-plaud-v9.9.zip")
        with zipfile.ZipFile(chemin) as archive:
            noms = archive.namelist()
            self.assertTrue(noms and all(n.startswith("kit-plaud/") for n in noms))
            skill = archive.read("kit-plaud/SKILL.md").decode("utf-8")
        self.assertRegex(skill, r"(?m)^name: kit-plaud$")

    def test_ni_tests_ni_apercu_ni_configuration_du_client(self):
        for slug in ("kit-plaud", "le-point"):
            chemin, _ = self.construire(slug)
            with zipfile.ZipFile(chemin) as archive:
                for nom in archive.namelist():
                    with self.subTest(slug=slug, nom=nom):
                        parties = nom.split("/")
                        self.assertFalse({"tests", "apercu", "__pycache__"} & set(parties))
                        self.assertNotEqual(parties[-1], "config.json")

    def test_noms_en_utf8_et_nfc(self):
        chemin, _ = self.construire("le-point")
        with zipfile.ZipFile(chemin) as archive:
            for info in archive.infolist():
                self.assertEqual(info.filename, unicodedata.normalize("NFC", info.filename))
                if not info.filename.isascii():
                    self.assertTrue(info.flag_bits & 0x800)

    def test_meme_tag_meme_empreinte(self):
        _, premiere = self.construire("le-point")
        _, seconde = self.construire("le-point")
        self.assertEqual(premiere, seconde)

    def test_un_slug_inconnu_est_refuse(self):
        with self.assertRaises(ValueError):
            charger().construire("inconnu", "HEAD", "1.0", Path(tempfile.mkdtemp()))


class Scrub(unittest.TestCase):
    def scrub(self, texte):
        with tempfile.TemporaryDirectory() as dossier:
            (Path(dossier) / "SKILL.md").write_text(texte, encoding="utf-8")
            return subprocess.run(["bash", str(SCRUB), dossier], capture_output=True, text=True).returncode

    def test_la_signature_publique_passe(self):
        self.assertEqual(self.scrub("Le Point, une recette M:armites.ai\nUne recette Marmites.ai\n"), 0)

    def test_une_donnee_interne_bloque(self):
        self.assertEqual(self.scrub("voir le cockpit\n"), 1)
        self.assertEqual(self.scrub("écrire à osman@marmites.com\n"), 1)


if __name__ == "__main__":
    unittest.main()
