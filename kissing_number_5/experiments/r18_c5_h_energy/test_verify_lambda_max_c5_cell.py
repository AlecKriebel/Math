#!/usr/bin/env python3
"""Normal, optimized-mode, and tamper tests for the exact frame checker."""

from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
VERIFIER = HERE / "verify_lambda_max_c5_cell.py"
EXPECTED = "verified: exact C5-cell frame bound lambda_max <= 3"


class TestFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise TestFailure(message)


def run(path, optimized=False):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.append(str(path))
    return subprocess.run(command, text=True, capture_output=True, check=False)


def main():
    for optimized in (False, True):
        result = run(VERIFIER, optimized)
        require(result.returncode == 0, result.stderr)
        require(EXPECTED in result.stdout, "success marker missing")

    source = VERIFIER.read_text()
    require(
        'cos_2L = Fraction(-1, 2)' in source,
        "tamper anchor missing",
    )
    tampered = source.replace(
        'cos_2L = Fraction(-1, 2)',
        'cos_2L = Fraction(-2, 3)',
        1,
    )
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "tampered_verifier.py"
        path.write_text(tampered)
        for optimized in (False, True):
            result = run(path, optimized)
            require(result.returncode != 0, "tampered verifier unexpectedly passed")

    print("tests passed: normal, -O, and exact-constant tamper")


if __name__ == "__main__":
    main()
