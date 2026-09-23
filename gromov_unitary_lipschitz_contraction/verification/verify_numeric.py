#!/usr/bin/env python3
"""Deterministic floating-point stress checks; NOT a proof of the theorem.

Requires NumPy. Tests selected matrices in dimensions 1,2,3,5,8, including
noncommuting exact boundary examples. Exit status is nonzero on any failure.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import sys

try:
    import numpy as np
except ImportError:
    sys.exit("NumPy is required for this optional numerical check. Run verify_exact.py for the dependency-free checks.")


SEED = 660025
TOLERANCE = 5e-12


def opnorm(matrix):
    return float(np.linalg.norm(matrix, ord=2))


def hsnorm(matrix):
    return float(np.linalg.norm(matrix, ord="fro"))


def F(matrix, t):
    identity = np.eye(matrix.shape[0], dtype=complex)
    # Right multiplication by the inverse, implemented as a linear solve.
    return np.linalg.solve((identity + t * matrix).T, (matrix + t * identity).T).T


def random_unitary(rng, n, boundary=False):
    Q, _ = np.linalg.qr(rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)))
    if boundary:
        angles = rng.choice([-np.pi / 2, np.pi / 2], size=n)
    else:
        angles = rng.uniform(-np.pi / 2, np.pi / 2, size=n)
    return (Q * np.exp(1j * angles)) @ Q.conj().T


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("results_numeric.json"))
    args = parser.parse_args()
    rng = np.random.default_rng(SEED)
    failures = []
    counts = {}
    maxima = {"unitarity_residual": 0.0, "difference_identity_residual": 0.0,
              "resolvent_bound_excess": 0.0, "difference_bound_excess_HS": 0.0,
              "difference_bound_excess_op": 0.0, "derivative_bound_excess_HS": 0.0,
              "derivative_bound_excess_op": 0.0, "derivative_identity_residual": 0.0}

    def check(name, value, limit, context):
        counts[name] = counts.get(name, 0) + 1
        if not np.isfinite(value) or value > limit:
            failures.append({"check": name, "value": float(value), "limit": float(limit), **context})

    # Re U = Re V = 0 exactly and UV != VU. These cover the closed boundary
    # without relying only on pseudorandomly generated cases.
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    boundary_U, boundary_V = 1j * sigma_z, 1j * sigma_x
    check("explicit_boundary_noncommuting", 1.0 / opnorm(boundary_U @ boundary_V - boundary_V @ boundary_U), 1.0, {})
    pairs = [(boundary_U, boundary_V, "explicit_noncommuting_boundary")]
    for n in [1, 2, 3, 5, 8]:
        for k in range(20):
            pairs.append((random_unitary(rng, n, boundary=k % 4 == 0),
                          random_unitary(rng, n, boundary=k % 4 == 0),
                          f"dimension_{n}_sample_{k}"))

    for U, V, label in pairs:
        n = U.shape[0]
        identity = np.eye(n, dtype=complex)
        context = {"case": label, "dimension": n}
        for W in [U, V]:
            check("input_is_unitary", opnorm(W.conj().T @ W - identity), TOLERANCE, context)
            check("input_in_closed_semicircle", -float(np.linalg.eigvalsh((W + W.conj().T) / 2).min()), TOLERANCE, context)
        for t in [0.0, 0.01, 0.25, 0.5, 0.9, 0.999999, 1.0]:
            context_t = {**context, "t": t}
            q = (1 - t * t) / (1 + t * t)
            RU = np.linalg.solve(identity + t * U, identity)
            RV = np.linalg.solve(identity + t * V, identity)
            FU, FV = F(U, t), F(V, t)
            residual = opnorm(FU.conj().T @ FU - identity)
            maxima["unitarity_residual"] = max(maxima["unitarity_residual"], residual)
            check("output_is_unitary", residual, TOLERANCE, context_t)
            for inverse in [RU, RV]:
                excess = opnorm(inverse) - 1 / np.sqrt(1 + t * t)
                maxima["resolvent_bound_excess"] = max(maxima["resolvent_bound_excess"], excess)
                check("resolvent_bound", excess, TOLERANCE, context_t)
            residual = opnorm(FU - FV - (1 - t * t) * RU @ (U - V) @ RV)
            maxima["difference_identity_residual"] = max(maxima["difference_identity_residual"], residual)
            check("difference_identity", residual, TOLERANCE, context_t)
            # E=U K is a tangent vector to U(N). Differentiate the original
            # rational expression independently via the product rule.
            raw = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
            K = (raw - raw.conj().T) / 2
            E = U @ K
            derivative_direct = E @ RU - (U + t * identity) @ RU @ (t * E) @ RU
            derivative_factored = (1 - t * t) * RU @ E @ RU
            residual = opnorm(derivative_direct - derivative_factored)
            maxima["derivative_identity_residual"] = max(maxima["derivative_identity_residual"], residual)
            check("derivative_identity", residual, TOLERANCE * max(1.0, opnorm(E)), context_t)
            for name, norm in [("HS", hsnorm), ("op", opnorm)]:
                excess = norm(FU - FV) - q * norm(U - V)
                maxima[f"difference_bound_excess_{name}"] = max(maxima[f"difference_bound_excess_{name}"], excess)
                check(f"difference_bound_{name}", excess, TOLERANCE * max(1.0, norm(U - V)), context_t)
                excess = norm(derivative_direct) - q * norm(E)
                maxima[f"derivative_bound_excess_{name}"] = max(maxima[f"derivative_bound_excess_{name}"], excess)
                check(f"derivative_bound_{name}", excess, TOLERANCE * max(1.0, norm(E)), context_t)
            if t == 0:
                check("initial_endpoint", opnorm(FU - U), TOLERANCE, context_t)
            if t == 1:
                check("terminal_endpoint", opnorm(FU - identity), TOLERANCE, context_t)
            check("identity_fixed", opnorm(F(identity, t) - identity), TOLERANCE, context_t)

    # Outside the semicircle: at -1 the derivative expands by 3 when t=1/2.
    t = 0.5
    outside = np.array([[-1.0 + 0j]])
    near_outside = np.array([[np.exp(1j * (np.pi - 1e-3))]])
    outside_ratio = opnorm(F(outside, t) - F(near_outside, t)) / opnorm(outside - near_outside)
    check("outside_semicircle_expansion_detected", 1.0 / outside_ratio, 1.0, {})
    endpoint_smallest_singular = float(np.linalg.svd(np.eye(1) + outside, compute_uv=False).min())
    check("outside_semicircle_endpoint_singular", endpoint_smallest_singular, 0.0, {})

    result = {
        "scope": "Finite deterministic floating-point stress checks; not a proof of the theorem or of an all-dimensions assertion.",
        "limitations": ["Ordinary double precision, without interval error certification.",
                        "These checks do not establish curve-length inequalities or mapping-space continuity."],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(), "numpy_version": np.__version__,
        "seed": SEED, "absolute_base_tolerance": TOLERANCE,
        "dimensions": [1, 2, 3, 5, 8], "matrix_pairs": len(pairs),
        "time_parameters": [0.0, 0.01, 0.25, 0.5, 0.9, 0.999999, 1.0],
        "passed": not failures, "check_count": sum(counts.values()),
        "checks_by_type": counts, "maxima": maxima,
        "outside_semicircle_chordal_expansion_ratio": outside_ratio,
        "failures": failures,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Numerical checks: {result['check_count']} checks, {len(failures)} failures; {args.output}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
