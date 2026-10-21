import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class StoragePackagingTest(unittest.TestCase):
    def test_every_catalogued_skill_embeds_the_same_contract(self):
        generator = module('generate_catalog')
        catalog = generator.load_catalog()
        files = generator.expected_files(catalog)
        expected = (ROOT / 'references/storage-contract.md').read_text()
        count = 0
        for plugin in catalog['plugins']:
            for name in plugin['skills']:
                skill = ROOT / 'plugins' / plugin['name'] / 'skills' / name
                self.assertEqual(files[skill / 'references/storage-contract.md'], expected)
                self.assertEqual((skill / 'references/storage-contract.md').read_text(), expected)
                count += 1
        self.assertEqual(count, 18)

    def test_standalone_zip_contains_the_contract_without_repo_dependency(self):
        builder = module('build_learn_zip')
        skill = ROOT / 'plugins/augmentes-meetings/skills/plaud'
        entries = [('SKILL.md', (skill / 'SKILL.md').read_bytes()),
                   ('references/storage-contract.md', (skill / 'references/storage-contract.md').read_bytes())]
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(builder, 'fichiers_au_tag', return_value=entries):
                archive, _ = builder.construire('kit-plaud', 'fixture', '1.0.0-test', Path(folder))
            with zipfile.ZipFile(archive) as package:
                contract = package.read('kit-plaud/references/storage-contract.md')
                self.assertEqual(contract, entries[1][1])
                self.assertIn(b'(references/storage-contract.md)', package.read('kit-plaud/SKILL.md'))

    def test_validator_rejects_a_missing_or_modified_packaged_contract(self):
        validator = module('validate_repository')
        target = ROOT / 'plugins/augmentes-foundation/skills/done/references/storage-contract.md'
        original_is_file, original_read = Path.is_file, Path.read_bytes
        with patch.object(Path, 'is_file', lambda path: False if path == target else original_is_file(path)):
            self.assertTrue(any('contrat de stockage absent' in error for error in validator.validate()))
        with patch.object(Path, 'read_bytes', lambda path: b'stale' if path == target else original_read(path)):
            self.assertTrue(any('contrat de stockage absent ou périmé' in error for error in validator.validate()))
