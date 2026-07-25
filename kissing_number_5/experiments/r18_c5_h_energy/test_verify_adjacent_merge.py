#!/usr/bin/env python3
"""Normal, optimized-mode, and digest-tamper tests for the merge verifier."""

from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
VERIFIER = HERE / "verify_adjacent_merge.py"
SUCCESS = "verified: adjacent merge D >= 2*x*y*(a+c)"
DIGEST = "5153dc70e2db1f215f2c8e60c39f55e1a5a41960f849bfb315edd2fb6a47b21b"


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
        require(SUCCESS in result.stdout, "success marker missing")
        require(DIGEST in result.stdout, "certificate digest missing")

    source = VERIFIER.read_text()
    require(DIGEST in source, "digest tamper anchor missing")
    tampered = source.replace(DIGEST, "0" + DIGEST[1:], 1)
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "tampered_verifier.py"
        path.write_text(tampered)
        for optimized in (False, True):
            result = run(path, optimized)
            require(result.returncode != 0, "tampered certificate unexpectedly passed")

    print("tests passed: normal, -O, and Bernstein-digest tamper")


if __name__ == "__main__":
    main()
