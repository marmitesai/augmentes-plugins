import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_repository.py"
SPEC = importlib.util.spec_from_file_location("validate_repository", MODULE_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ReferenceValidationTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.skill = self.root / "plugins" / "sample" / "skills" / "m-local"
        self.skill.mkdir(parents=True)
        self.skill_file = self.skill / "SKILL.md"

    def tearDown(self):
        self.temporary.cleanup()

    def validate(self, content, skills=None, mcp_tools=None):
        self.skill_file.write_text(content)
        errors = []
        VALIDATOR.validate_references(
            [self.skill_file],
            {"m-local"},
            {"references": {"skills": skills or [], "mcp_tools": mcp_tools or []}},
            errors,
            root=self.root,
        )
        return errors

    def test_declared_external_references_are_accepted(self):
        errors = self.validate(
            "Utiliser `m-external` et mcp__service__read.",
            skills=["m-external"],
            mcp_tools=["mcp__service__read"],
        )
        self.assertEqual(errors, [])

    def test_unknown_skill_is_rejected(self):
        errors = self.validate("Utiliser /m-missing.")
        self.assertTrue(any("skills référencés inconnus" in error for error in errors))

    def test_unknown_mcp_tool_is_rejected(self):
        errors = self.validate("Utiliser mcp__service__missing.")
        self.assertTrue(any("outils MCP non déclarés" in error for error in errors))

    def test_legacy_path_is_rejected(self):
        errors = self.validate('PY="$DEXTER/Devs/app/venv/bin/python"')
        self.assertTrue(any("atelier Dropbox obsolète" in error for error in errors))

    def test_missing_local_resource_is_rejected(self):
        errors = self.validate('python "$SK/scripts/run.py"')
        self.assertTrue(any("ressource locale absente" in error for error in errors))
        scripts = self.skill / "scripts"
        scripts.mkdir()
        (scripts / "run.py").write_text("")
        self.assertEqual(self.validate('python "$SK/scripts/run.py"'), [])


if __name__ == "__main__":
    unittest.main()

