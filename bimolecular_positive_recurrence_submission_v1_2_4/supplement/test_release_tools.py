"""Regression tests for release-manifest and archive path safety."""

from __future__ import annotations

import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from supplement import build_release_archive
from supplement import verify_manifest


class ReleaseToolSafetyTests(unittest.TestCase):
    EXPECTED_TAG = "bimolecular-positive-recurrence-v1.2.4"

    def make_replay_repository(self, directory: str) -> tuple[Path, Path]:
        root = Path(directory)
        validation = (
            root
            / "bimolecular_positive_recurrence_submission_v1_2_4"
            / "validation"
        )
        validation.mkdir(parents=True)
        source = Path(__file__).resolve().parents[1] / "validation" / "replay_release.sh"
        script = validation / "replay_release.sh"
        shutil.copy2(source, script)
        self.git(root, "init", "--quiet")
        self.git(root, "config", "user.name", "Release Test")
        self.git(root, "config", "user.email", "release-test@example.invalid")
        self.git(root, "add", ".")
        self.git(root, "commit", "--quiet", "-m", "test release")
        return root, script

    def git(self, root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ("git", *arguments),
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )

    def run_replay(self, root: Path, script: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ("bash", str(script)),
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_manifest_parser_rejects_windows_separator(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "MANIFEST.sha256"
            manifest.write_text(f"{'0' * 64}  ..\\escape.txt\n", encoding="utf-8")
            with patch.object(verify_manifest, "MANIFEST", manifest):
                with self.assertRaisesRegex(ValueError, "unsafe"):
                    verify_manifest.parse_manifest()

    def test_archive_parser_rejects_windows_separator(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            unsafe_name = "bad\\name.txt"
            payload = root / unsafe_name
            payload.write_bytes(b"unsafe cross-platform member name\n")
            digest = hashlib.sha256(payload.read_bytes()).hexdigest()
            manifest = root / "MANIFEST.sha256"
            manifest.write_text(f"{digest}  {unsafe_name}\n", encoding="utf-8")
            with (
                patch.object(build_release_archive, "PROJECT", root),
                patch.object(build_release_archive, "MANIFEST", manifest),
            ):
                with self.assertRaisesRegex(ValueError, "unsafe"):
                    build_release_archive.manifest_paths()

    def test_manifest_walk_rejects_broken_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            link = root / "broken-link"
            try:
                link.symlink_to("missing-target")
            except (NotImplementedError, OSError):
                self.skipTest("symbolic links are unavailable on this platform")
            with patch.object(verify_manifest, "PROJECT", root):
                with self.assertRaisesRegex(ValueError, "symbolic links are forbidden"):
                    verify_manifest.actual_entries()

    def test_manifest_walk_ignores_virtual_environment_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bin_directory = root / "code" / ".venv" / "bin"
            bin_directory.mkdir(parents=True)
            link = bin_directory / "python"
            try:
                link.symlink_to("missing-interpreter")
            except (NotImplementedError, OSError):
                self.skipTest("symbolic links are unavailable on this platform")
            with patch.object(verify_manifest, "PROJECT", root):
                self.assertEqual(verify_manifest.actual_entries(), {})

    def test_release_replay_rejects_untagged_head_before_other_checks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, script = self.make_replay_repository(directory)
            result = self.run_replay(root, script)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("is untagged", result.stderr)
            self.assertNotIn("Python:", result.stdout)

    def test_release_replay_rejects_wrong_exact_tag_before_other_checks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, script = self.make_replay_repository(directory)
            self.git(root, "tag", "--annotate", "wrong-release-tag", "-m", "wrong")
            result = self.run_replay(root, script)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                f"expected exact tag {self.EXPECTED_TAG}, found wrong-release-tag",
                result.stderr,
            )
            self.assertNotIn("Python:", result.stdout)

    def test_release_replay_rejects_lightweight_expected_tag(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, script = self.make_replay_repository(directory)
            self.git(root, "tag", self.EXPECTED_TAG)
            result = self.run_replay(root, script)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must be an annotated tag", result.stderr)
            self.assertNotIn("Python:", result.stdout)


if __name__ == "__main__":
    unittest.main()
