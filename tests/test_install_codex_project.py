import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "install_codex_project.py"


class ProjectInstallerTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        root = Path(self.temporary.name)
        self.source = root / "source"
        self.target = root / "project"
        skill = self.source / "plugins" / "sample-plugin" / "skills" / "alpha"
        manifest = self.source / "plugins" / "sample-plugin" / ".codex-plugin"
        marketplace = self.source / ".agents" / "plugins"
        skill.mkdir(parents=True)
        manifest.mkdir(parents=True)
        marketplace.mkdir(parents=True)
        self.target.mkdir()
        (skill / "SKILL.md").write_text("---\nname: alpha\ndescription: Test\n---\n")
        (manifest / "plugin.json").write_text(json.dumps({
            "name": "sample-plugin",
            "version": "1.0.0-rc.1",
            "repository": "https://example.com/sample.git",
        }))
        (marketplace / "marketplace.json").write_text(json.dumps({
            "name": "sample",
            "plugins": [{
                "name": "sample-plugin",
                "source": {"source": "local", "path": "./plugins/sample-plugin"},
            }],
        }))
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        self.git("tag", "v1.0.0-rc.1")

    def tearDown(self):
        self.temporary.cleanup()

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.source), *args], check=True)

    def command(self, *args):
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def install(self):
        return self.command(
            "install",
            "--source-root", str(self.source),
            "--target", str(self.target),
            "--ref", "v1.0.0-rc.1",
            "--plugins", "sample-plugin",
        )

    def test_install_is_idempotent_and_preserves_unmanaged_skills(self):
        unmanaged = self.target / ".agents" / "skills" / "third-party"
        unmanaged.mkdir(parents=True)
        (unmanaged / "SKILL.md").write_text("third party")
        self.assertEqual(self.install().returncode, 0)
        self.assertEqual(self.install().returncode, 0)
        self.assertTrue((self.target / ".agents" / "skills" / "alpha" / "SKILL.md").is_file())
        self.assertTrue((unmanaged / "SKILL.md").is_file())
        check = self.command("check", "--target", str(self.target), "--marketplace", "sample")
        self.assertEqual(check.returncode, 0, check.stderr)

    def test_local_change_blocks_update(self):
        self.assertEqual(self.install().returncode, 0)
        managed = self.target / ".agents" / "skills" / "alpha" / "SKILL.md"
        managed.write_text("modification locale")
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("modifiées localement", result.stderr)
        self.assertEqual(managed.read_text(), "modification locale")

    def test_wrong_ref_is_rejected(self):
        result = self.command(
            "install",
            "--source-root", str(self.source),
            "--target", str(self.target),
            "--ref", "v9.9.9",
            "--plugins", "sample-plugin",
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
