#!/usr/bin/env python3
"""Independent exact and numerical attack on the PARTITION reduction."""
from __future__ import annotations

import itertools
import json
import random
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import differential_evolution

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "independent_verifier"))
from partition_reduction import (  # noqa: E402
    X_matrix,
    conjugator,
    hurwitz_determinants,
    interior_q,
    is_hurwitz_exact,
    lifted_matrix,
    make_family,
    make_lift,
    minimum_partition_square,
    open_cube_matrix,
    partition_witness,
    triangular_form,
)


def exact_small_census() -> dict[str, int]:
    instances = 0
    yes = 0
    no = 0
    exact_interior_checks = 0
    for length in range(2, 7):
        for numbers in itertools.combinations_with_replacement(range(1, 7), length):
            family = make_family(numbers)
            signs = partition_witness(numbers)
            minimum_square = minimum_partition_square(numbers)
            cube_max = sp.Rational(family.m) - sp.Rational(minimum_square, 1 + family.gamma)
            threshold = family.m * family.beta
            if (signs is not None) != (minimum_square == 0):
                raise AssertionError("sign enumeration and exact minimum disagree")
            if signs is None:
                if not cube_max < threshold:
                    raise AssertionError({"numbers": numbers, "cube_max": cube_max, "threshold": threshold})
                no += 1
            else:
                if not cube_max > threshold:
                    raise AssertionError("YES instance did not clear the open-cube threshold")
                q = interior_q(family, signs)
                r = (sp.Integer(1) + family.beta) / 2
                if not all(-1 < value < 1 for value in q):
                    raise AssertionError("interior witness left the open cube")
                if not (family.beta < 1 and r**2 - family.beta > 0):
                    raise AssertionError("exact 2x2 Hurwitz block inequalities failed")
                # Directly verify the explicit invariant vectors for a bounded sample.
                if exact_interior_checks < 80:
                    B = open_cube_matrix(family, q)
                    padded = sp.Matrix(tuple(signs) + (1,) * (family.m - len(signs)))
                    if (family.a.T * padded)[0] != 0:
                        raise AssertionError("padded sign vector is not orthogonal to a")
                    u = padded / family.k
                    top_u = sp.Matrix.vstack(u, sp.Matrix([0]))
                    bottom = sp.Matrix([0] * family.m + [1])
                    expected1 = -family.k * top_u + r * family.k * bottom
                    expected2 = -r * family.k * top_u + family.k * family.beta * bottom
                    if sp.simplify(B * top_u - expected1) != sp.zeros(family.m + 1, 1):
                        raise AssertionError("first invariant-vector identity failed")
                    if sp.simplify(B * bottom - expected2) != sp.zeros(family.m + 1, 1):
                        raise AssertionError("second invariant-vector identity failed")
                    exact_interior_checks += 1
                yes += 1
            instances += 1
    return {"instances": instances, "yes": yes, "no": no, "exact_interior_checks": exact_interior_checks}

def similarity_tests() -> int:
    rng = random.Random(20260813)
    checks = 0
    for numbers in ((1, 1), (1, 2), (2, 3, 5), (1, 1, 2, 2)):
        family = make_family(numbers)
        lift = make_lift(family, alpha=sp.Rational(3, 2))
        n0 = family.base_dimension
        d = family.parameter_dimension
        for trial in range(8):
            q = tuple(sp.Rational(rng.randint(-8, 8), 9) for _ in range(d))
            L = lifted_matrix(lift, q)
            X = X_matrix(lift, q)
            P = sp.Matrix.vstack(
                sp.eye(n0).row_join(sp.zeros(n0, d)),
                (-X).row_join(sp.eye(d)),
            )
            Pinv = sp.Matrix.vstack(
                sp.eye(n0).row_join(sp.zeros(n0, d)),
                X.row_join(sp.eye(d)),
            )
            target = triangular_form(lift, q)
            if sp.simplify(P * L * Pinv - target) != sp.zeros(n0 + d):
                raise AssertionError("row-splitting similarity failed")
            if checks < 4:
                lam = sp.symbols("lambda")
                if sp.factor(L.charpoly(lam).as_expr() - target.charpoly(lam).as_expr()) != 0:
                    raise AssertionError("characteristic polynomials differ")
            checks += 1
    return checks


def numeric_lift_arrays(lift):
    return (
        np.array(lift.B0.evalf(30).tolist(), dtype=float),
        np.array(lift.U.evalf(30).tolist(), dtype=float),
        np.array(lift.W.evalf(30).tolist(), dtype=float),
        float(lift.alpha),
    )


def fast_lifted_matrix(arrays, q: np.ndarray) -> np.ndarray:
    B0, U, W, alpha = arrays
    X = np.diag(q) @ W
    top = np.hstack((B0, U))
    bottom = np.hstack((X @ (B0 + alpha * np.eye(B0.shape[0])), X @ U - alpha * np.eye(W.shape[0])))
    return np.vstack((top, bottom))

def spectral_abscissa_scaled(variables: np.ndarray, arrays, parameter_dimension: int) -> float:
    q = variables[:parameter_dimension]
    logs = variables[parameter_dimension:]
    logs = logs - np.mean(logs)
    diagonal = np.exp(logs)
    L = fast_lifted_matrix(arrays, q)
    eig = np.linalg.eigvals(L @ np.diag(diagonal))
    return float(np.max(eig.real))

def numerical_no_search() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for numbers in ((1, 2), (1, 1, 1), (1, 2, 4)):
        if partition_witness(numbers) is not None:
            raise AssertionError("selected numerical attack instance is not NO")
        family = make_family(numbers)
        lift = make_lift(family)
        dimension = family.parameter_dimension + lift.dimension
        arrays = numeric_lift_arrays(lift)
        bounds = [(-0.999, 0.999)] * family.parameter_dimension + [(-4.0, 4.0)] * lift.dimension
        result = differential_evolution(
            lambda z: spectral_abscissa_scaled(z, arrays, family.parameter_dimension),
            bounds,
            seed=20260813 + len(numbers),
            popsize=5,
            maxiter=24,
            polish=True,
            workers=1,
            updating="immediate",
            tol=1e-7,
        )
        best = float(result.fun)
        if best < -1e-7:
            raise AssertionError({"false_Hurwitz_candidate": numbers, "spectral_abscissa": best, "point": result.x.tolist()})
        results.append({
            "numbers": list(numbers),
            "variables": dimension,
            "best_spectral_abscissa": best,
            "optimizer_success": bool(result.success),
            "evaluations": int(result.nfev),
        })
    return results


def main() -> int:
    census = exact_small_census()
    similarity = similarity_tests()
    numerical = numerical_no_search()
    print(json.dumps({
        "status": "PASS",
        "small_partition_census": census,
        "exact_similarity_checks": similarity,
        "numerical_NO_searches": numerical,
        "false_yes_found": False,
        "false_no_found": False,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
