#!/usr/bin/env python3
"""Replay and positively identify the untouched historical H21-01 failure."""
from __future__ import annotations

import builtins
import hashlib
import pathlib
import traceback


HERE = pathlib.Path(__file__).resolve().parent
ARTIFACTS = HERE.parent / "input_frozen" / "k3p_cloud_artifacts"
HISTORICAL = HERE / "HISTORICAL_cleanroom_verify_fourteen_orbits.py"
FROZEN = ARTIFACTS / "cleanroom_verify_fourteen_orbits.py"
EXPECTED_HASH = "ee5e29a2cd795d9389e8e1257ebdb9eeaa4256fb5d03e07f230bf82ba555ef91"
EXPECTED = (
    "source automorphism",
    "H21-01",
    {
        "permutation": [2, 1, 3, 0],
        "source_automorphism": [2, 1, 0, 3],
        "target_automorphism": [0, 1, 2, 3],
    },
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    assert digest(HISTORICAL) == digest(FROZEN) == EXPECTED_HASH

    # The cloud export flattened inputs that originally lived at project root
    # and software/certificates.  This adapter changes only read resolution;
    # the executed verifier bytes are untouched.
    real_open = builtins.open

    def mapped_open(file, *args, **kwargs):
        candidate_path = (pathlib.Path(file)
                          if isinstance(file, (str, bytes, pathlib.Path)) else None)
        if candidate_path is not None and not candidate_path.exists():
            flattened = ARTIFACTS / candidate_path.name
            if flattened.exists():
                file = flattened
        return real_open(file, *args, **kwargs)

    builtins.open = mapped_open
    globals_for_historical = {
        "__name__": "__main__",
        # Makes the historical ROOT expression point to ARTIFACTS while leaving
        # the historical file itself byte-for-byte unchanged.
        "__file__": str(ARTIFACTS / "software" /
                        "cleanroom_verify_fourteen_orbits.py"),
    }
    try:
        code = compile(HISTORICAL.read_bytes(), str(HISTORICAL), "exec")
        exec(code, globals_for_historical)
    except AssertionError as error:
        traceback.print_exc()
        assert error.args == (EXPECTED,), (error.args, EXPECTED)
        print("HISTORICAL_H21_01_FAILURE_REPRODUCED_EXACTLY")
        return
    finally:
        builtins.open = real_open
    raise AssertionError("historical verifier unexpectedly passed")


if __name__ == "__main__":
    run()
