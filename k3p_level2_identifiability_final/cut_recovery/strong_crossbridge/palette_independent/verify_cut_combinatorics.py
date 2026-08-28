#!/usr/bin/env python3
"""Replay and byte-bind the two independent noncut-word enumerations."""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(script: str, certificate: str) -> tuple[str, str]:
    expected = HERE / certificate
    require(expected.is_file(), ("missing certificate", certificate))
    with tempfile.TemporaryDirectory(prefix="k3p-cut-palette-") as directory:
        output = Path(directory) / certificate
        result = subprocess.run(
            [sys.executable, str(HERE / script), "--output", str(output)],
            cwd=HERE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
            timeout=600,
        )
        require(result.returncode == 0, (script, result.stdout[-4000:]))
        require(output.read_bytes() == expected.read_bytes(),
                ("fresh certificate mismatch", certificate,
                 sha256(output), sha256(expected)))
        return sha256(output), result.stdout.strip()


def main() -> int:
    try:
        reduction, _ = replay(
            "enumerate_balanced_word_reduction.py",
            "BALANCED_WORD_REDUCTION_CERTIFICATE.json",
        )
        palette, _ = replay(
            "verify_reduced_palette_cleanroom.py",
            "REDUCED_PALETTE_CLEANROOM_CERTIFICATE.json",
        )
        print(
            "K3P_CUT_COMBINATORICS_PASS "
            f"balanced_words=808642 palette_presentations=379742 survivors=0 "
            f"reduction_sha256={reduction} palette_sha256={palette}"
        )
        return 0
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"K3P_CUT_COMBINATORICS_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
