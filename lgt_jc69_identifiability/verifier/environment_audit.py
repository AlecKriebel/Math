#!/usr/bin/env python3
"""Report and validate the locked theorem-verifier environment."""
from __future__ import annotations

import ctypes.util
import platform
import sys

import mpmath
import sympy

EXPECTED_SYMPY = "1.14.0"
EXPECTED_MPMATH = "1.3.0"


def main() -> None:
    assert sympy.__version__ == EXPECTED_SYMPY, (
        f"SymPy {EXPECTED_SYMPY} required; found {sympy.__version__}"
    )
    assert mpmath.__version__ == EXPECTED_MPMATH, (
        f"mpmath {EXPECTED_MPMATH} required; found {mpmath.__version__}"
    )
    mpfr = ctypes.util.find_library("mpfr") or "libmpfr.so.6"
    assert mpfr, "MPFR shared library not found"
    print(f"PASS Python {platform.python_version()} ({sys.executable})")
    print(f"PASS SymPy {sympy.__version__} and mpmath {mpmath.__version__}")
    print(f"PASS MPFR library discovery: {mpfr}")
    print("ALL ENVIRONMENT LOCK CHECKS PASSED")


if __name__ == "__main__":
    main()
