"""Exact order-13, parameter-three synthesis constructor.

This package is intentionally separate from the frozen order-12 synthesis
code.  It contains no SAT-solver invocation.
"""

from .encoding import (
    EXPECTED_FORMULAS,
    N,
    TEMPLATES,
    K3Encoding,
    build_base_encoding,
    build_full_encoding,
    enumerate_coloring_bank,
    validate_decoded_candidate,
)

__all__ = [
    "EXPECTED_FORMULAS",
    "N",
    "TEMPLATES",
    "K3Encoding",
    "build_base_encoding",
    "build_full_encoding",
    "enumerate_coloring_bank",
    "validate_decoded_candidate",
]
