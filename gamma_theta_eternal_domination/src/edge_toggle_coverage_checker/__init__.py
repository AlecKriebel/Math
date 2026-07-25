"""Independent coverage checker for the one-edge-toggle production ledger.

This package intentionally imports neither the edge-toggle search engine nor
either mathematical evaluator used by that engine.
"""

from .audit import AuditError, AuditOutcome, AuditPaths, run_audit

__all__ = (
    "AuditError",
    "AuditOutcome",
    "AuditPaths",
    "run_audit",
)
