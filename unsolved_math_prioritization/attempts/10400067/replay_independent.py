#!/usr/bin/env python3
"""Replay the unchanged independent checker in its expected portable layout.

The original checker expects sibling `packet` and audit directories.
Copy only the 18 frozen author files and that unchanged checker to a
temporary directory, run it, and compare its output with the audit receipt.
No mathematical checker code or proof bytes are modified.
"""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "AUTHOR_MANIFEST.json").read_text())
    names = ["AUTHOR_MANIFEST.json", *manifest["files"]]
    assert len(names) == 18 and len(set(names)) == 18
    review = root / "independent_review"
    with tempfile.TemporaryDirectory(prefix="two-loop-independent-") as tmp:
        base = Path(tmp)
        packet = base / "packet"
        audit = base / "audit-independent"
        packet.mkdir()
        audit.mkdir()
        for name in names:
            assert Path(name).name == name
            shutil.copy2(root / name, packet / name)
        script = audit / "independent_controls.py"
        shutil.copy2(review / script.name, script)
        result = subprocess.run([sys.executable, str(script)],
                                check=True, capture_output=True)
    expected = (review / "INDEPENDENT_CHECK.json").read_bytes()
    assert result.stdout == expected, "Independent receipt differs"
    sys.stdout.buffer.write(result.stdout)


if __name__ == "__main__":
    main()
