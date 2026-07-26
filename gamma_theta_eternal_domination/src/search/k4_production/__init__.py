"""Resumable proof-production workflow for the exact order-12, k=4 CNF.

Importing this package never starts a solver.  Use
``python -m search.k4_production`` for the explicit command-line gates.
"""

from .runner import (
    DEFAULT_CUBE_VARIABLES,
    EXPECTED_PARENT_CNF_SHA256,
    audit_run,
    initialize_run,
    run_next_case,
)

__all__ = [
    "DEFAULT_CUBE_VARIABLES",
    "EXPECTED_PARENT_CNF_SHA256",
    "audit_run",
    "initialize_run",
    "run_next_case",
]
