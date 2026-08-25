#!/usr/bin/env python3
"""Small mutation suite for the fail-closed readiness state machine."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location(
    "submission_validator", HERE / "validate_submission_packages.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def main() -> int:
    cases = [
        ([], [], ("READY", 0)),
        ([], ["unresolved token"], ("NOT_READY", 2)),
        (["bad manifest"], [], ("INVALID", 1)),
        (["bad manifest"], ["unresolved token"], ("INVALID", 1)),
    ]
    for errors, blockers, expected in cases:
        actual = MODULE.package_status(errors, blockers)
        if actual != expected:
            raise SystemExit(f"state-machine mutation failed: {errors}, {blockers}: {actual}")

    text = "@@REAL_RELEASE_FIELD@@ @@TOKEN@@ @@UPPER_CASE_TOKEN@@"
    tokens = [
        token for token in MODULE.TOKEN_RE.findall(text)
        if token not in MODULE.DOCUMENTATION_TOKENS
    ]
    if tokens != ["REAL_RELEASE_FIELD"]:
        raise SystemExit(f"placeholder grammar mutation failed: {tokens}")

    if MODULE.latex_word_count(r"One two \(x\) three-four") != 4:
        raise SystemExit("LaTeX word-count mutation failed")

    print("PASS: 6 fail-closed validator mutations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
