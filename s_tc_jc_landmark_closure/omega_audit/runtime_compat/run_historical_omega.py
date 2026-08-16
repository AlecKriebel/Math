#!/usr/bin/env python3
"""Execute the untouched historical Omega proof with its verified orbit shim."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

import probe_four_leaf_jc_atlas as orbit_shim


HERE = Path(__file__).resolve().parent
HISTORICAL = HERE.parent / "frozen_input" / "historical" / "src"
SCRIPT = HISTORICAL / "verify_jc_omega_move.py"


def main() -> None:
    # The historical verifier imports this name only for
    # JC_REPRESENTATIVES.  Installing the already verified shim explicitly is
    # stronger than relying on PYTHONPATH order, because Python otherwise
    # places the executed script's directory first.
    sys.modules["probe_four_leaf_jc_atlas"] = orbit_shim
    sys.path.insert(1, str(HISTORICAL))
    runpy.run_path(str(SCRIPT), run_name="__main__")


if __name__ == "__main__":
    main()
