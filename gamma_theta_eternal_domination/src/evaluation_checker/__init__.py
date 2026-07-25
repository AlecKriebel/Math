"""Independent mathematical checker for the completed extension artifact."""

from .audit import (
    EvaluationAuditError,
    EvaluationPaths,
    EvaluationPolicy,
    PRODUCTION_POLICY,
    run_evaluation_audit,
    verify_certificate,
)
from .math_core import (
    FixedPointResult,
    greatest_fixed_point,
    verify_empty_fixed_point_trace,
)

__all__ = [
    "EvaluationAuditError",
    "EvaluationPaths",
    "EvaluationPolicy",
    "FixedPointResult",
    "PRODUCTION_POLICY",
    "greatest_fixed_point",
    "run_evaluation_audit",
    "verify_certificate",
    "verify_empty_fixed_point_trace",
]
