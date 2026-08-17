"""Regression tests for release-manifest and archive path safety."""

from __future__ import annotations

import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from supplement import build_release_archive
from supplement import verify_manifest


class ReleaseToolSafetyTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
