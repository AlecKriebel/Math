#!/usr/bin/env python3
"""Exact CP-SAT diagnostic for the 78-trit Eliahou fold+causal system.

The model uses two Boolean endpoint variables per ternary coordinate:

    lower_j, upper_j in {0,1},  lower_j + upper_j <= 1,
    u_j = lower_j + upper_j,    t_j = lower_j - upper_j.

Every distinct Boolean product is defined once and reused across the shell,
four exact root equations, twenty anti-fold equations, twenty-one plus-fold
equations, and forty-one causal high-lag equations.  A reported SAT model is
reconstructed in the original four physical sequences and checked at every
aperiodic lag.  UNKNOWN and solver UNSAT are diagnostics only; this script
does not emit a proof certificate.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from functools import reduce
from math import gcd
import json
from pathlib import Path
import random
import resource
import sys
import time
from typing import Iterable

import numpy as np
from ortools.sat.python import cp_model


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
REDTEAM = SEARCH / "eliahou_long_orientation_redteam"
CHAR3 = SEARCH / "eliahou_char3_jet"
sys.path[:0] = [str(REDTEAM), str(CHAR3), str(SEARCH)]

import audit_exact_ternary_model as ternary  # noqa: E402
import audit_orientation_redteam as orientation  # noqa: E402
import search_char3_local as local  # noqa: E402


EndpointMonomial = tuple[int, ...]
EndpointPolynomial = dict[EndpointMonomial, int]


@dataclass(frozen=True)
class ExactSystem:
    case_number: int
    case: object
    keys: tuple[tuple[str, int], ...]
    correlations: tuple[ternary.Polynomial, ...]
    anti: tuple[ternary.Polynomial, ...]
    plus: tuple[ternary.Polynomial, ...]
    causal: tuple[ternary.Polynomial, ...]
    root_coefficients: np.ndarray


def exact_system(case_number: int) -> ExactSystem:
    """Derive the exact fold+causal equations from the physical seed."""

    case, keys, _, _, _, _ = local.arrays(case_number)
    rows = ternary.symbolic_rows(case, keys)
    correlations = tuple(
        ternary.correlation_polynomial(rows, lag) for lag in range(84)
    )

    expected_c42: ternary.Polynomial = {(): -156}
    for variable in range(len(keys)):
        expected_c42[((variable, 0),)] = 4
    if correlations[42] != expected_c42:
        raise AssertionError("the exact shell/lag-42 identity changed")

    anti = tuple(
        ternary.add_polynomials(
            (1, correlations[k]),
            (-1, correlations[42 - k]),
            (-1, correlations[42 + k]),
            (1, correlations[84 - k]),
        )
        for k in range(1, 21)
    )
    plus_list = [
        ternary.add_polynomials(
            (1, correlations[k]),
            (1, correlations[42 - k]),
            (1, correlations[42 + k]),
            (1, correlations[84 - k]),
        )
        for k in range(1, 21)
    ]
    plus_list.append(
        ternary.add_polynomials(
            (2, correlations[21]), (2, correlations[63])
        )
    )
    causal = tuple(correlations[lag] for lag in range(43, 84))
    coefficients = orientation.root_coefficients(
        keys, tuple(range(len(keys)))
    )
    if len(keys) != 78:
        raise AssertionError(
            f"case {case_number} has {len(keys)} rather than 78 trits"
        )
    if len(getattr(case, "profiles")) != 2:
        raise AssertionError("the authoritative case lost its two profiles")
    return ExactSystem(
        case_number=case_number,
        case=case,
        keys=keys,
        correlations=correlations,
        anti=anti,
        plus=tuple(plus_list),
        causal=causal,
        root_coefficients=coefficients,
    )


def formal_expansion(formal: ternary.Formal) -> tuple[tuple[int, int], ...]:
    """Expand u or t into signed lower/upper Boolean endpoints."""

    variable, kind = formal
    lower, upper = 2 * variable, 2 * variable + 1
    if kind == 0:
        return ((lower, 1), (upper, 1))
    if kind == 1:
        return ((lower, 1), (upper, -1))
    raise AssertionError("unknown formal-variable kind")


def expand_polynomial(polynomial: ternary.Polynomial) -> EndpointPolynomial:
    """Substitute u=l+r and t=l-r in a reduced ternary polynomial."""

    result: EndpointPolynomial = {}
    for monomial, coefficient in polynomial.items():
        if not monomial:
            result[()] = result.get((), 0) + coefficient
            continue
        factors = [formal_expansion(formal) for formal in monomial]
        terms: list[tuple[EndpointMonomial, int]] = [((), coefficient)]
        for factor in factors:
            next_terms: list[tuple[EndpointMonomial, int]] = []
            for prior_monomial, prior_coefficient in terms:
                for endpoint, endpoint_coefficient in factor:
                    product = tuple(sorted(prior_monomial + (endpoint,)))
                    # The source has already reduced products on one ternary
                    # coordinate.  This guard catches an accidental violation.
                    if len(product) != len(set(product)):
                        raise AssertionError(
                            "unexpected repeated Boolean endpoint"
                        )
                    next_terms.append(
                        (
                            product,
                            prior_coefficient * endpoint_coefficient,
                        )
                    )
            terms = next_terms
        for endpoint_monomial, value in terms:
            result[endpoint_monomial] = (
                result.get(endpoint_monomial, 0) + value
            )
    return {
        monomial: coefficient
        for monomial, coefficient in result.items()
        if coefficient
    }


def divide_content(polynomial: EndpointPolynomial) -> EndpointPolynomial:
    """Divide an exact equality by the gcd of all nonzero coefficients."""

    content = reduce(gcd, (abs(value) for value in polynomial.values()), 0)
    if content <= 1:
        return polynomial
    return {
        monomial: coefficient // content
        for monomial, coefficient in polynomial.items()
    }


def endpoint_assignment(ternary_point: Iterable[int]) -> list[int]:
    result: list[int] = []
    for value in ternary_point:
        if value not in (-1, 0, 1):
            raise ValueError("ternary value out of range")
        result.extend((int(value == 1), int(value == -1)))
    return result


def evaluate_endpoint(
    polynomial: EndpointPolynomial, assignment: list[int]
) -> int:
    return sum(
        coefficient
        * (
            1
            if not monomial
            else int(np.prod([assignment[index] for index in monomial]))
        )
        for monomial, coefficient in polynomial.items()
    )


def random_algebra_audit(
    system: ExactSystem, samples: int, seed: int
) -> dict[str, int]:
    """Cross-check every expanded equation against exact and physical replay."""

    labelled = [
        *[(f"anti_{index}", polynomial) for index, polynomial in enumerate(system.anti, 1)],
        *[(f"plus_{index}", polynomial) for index, polynomial in enumerate(system.plus, 1)],
        *[
            (f"causal_{lag}", polynomial)
            for lag, polynomial in zip(range(43, 84), system.causal)
        ],
    ]
    expanded = {
        label: expand_polynomial(polynomial)
        for label, polynomial in labelled
    }
    generator = random.Random(seed)
    checks = 0
    for _ in range(samples):
        point = [generator.randrange(-1, 2) for _ in system.keys]
        endpoint = endpoint_assignment(point)
        rows = ternary.physical_rows(system.case, system.keys, point)
        direct = [
            ternary.direct_correlation(rows, lag) for lag in range(84)
        ]
        for lag, polynomial in enumerate(system.correlations):
            if ternary.evaluate_polynomial(polynomial, point) != direct[lag]:
                raise AssertionError(
                    f"source polynomial failed physical replay at lag {lag}"
                )
            checks += 1
        for label, polynomial in labelled:
            source = ternary.evaluate_polynomial(polynomial, point)
            observed = evaluate_endpoint(expanded[label], endpoint)
            if source != observed:
                raise AssertionError(
                    f"Boolean expansion disagreed for {label}: "
                    f"{observed} != {source}"
                )
            checks += 1
        general_roots = system.root_coefficients.T @ np.asarray(
            point, dtype=np.int16
        )
        for root_index in range(4):
            root_polynomial: EndpointPolynomial = {}
            for variable, coefficient in enumerate(
                system.root_coefficients[:, root_index]
            ):
                root_polynomial[(2 * variable,)] = int(coefficient)
                root_polynomial[(2 * variable + 1,)] = -int(coefficient)
            observed_root = evaluate_endpoint(root_polynomial, endpoint)
            if observed_root != int(general_roots[root_index]):
                raise AssertionError("root endpoint expansion failed")
        checks += 4
    return {"random_assignments": samples, "scalar_checks": checks}


class ModelBuilder:
    def __init__(self, system: ExactSystem, profile_index: int):
        self.system = system
        self.profile_index = profile_index
        self.model = cp_model.CpModel()
        self.endpoints = [
            self.model.NewBoolVar(
                f"{'lower' if endpoint % 2 == 0 else 'upper'}_"
                f"{endpoint // 2}"
            )
            for endpoint in range(2 * len(system.keys))
        ]
        self.products: dict[tuple[int, int], cp_model.IntVar] = {}
        self.equation_contents: dict[str, int] = {}
        self.equation_term_counts: dict[str, int] = {}

        for variable in range(len(system.keys)):
            lower = self.endpoints[2 * variable]
            upper = self.endpoints[2 * variable + 1]
            self.model.AddBoolOr([lower.Not(), upper.Not()])

        self.model.Add(sum(self.endpoints) == 39)
        self._add_roots()
        for index, polynomial in enumerate(system.anti, 1):
            self.add_polynomial(f"anti_{index}", polynomial)
        for index, polynomial in enumerate(system.plus, 1):
            self.add_polynomial(f"plus_{index}", polynomial)
        for lag, polynomial in zip(range(43, 84), system.causal):
            self.add_polynomial(f"causal_{lag}", polynomial)

    def product(self, left: int, right: int) -> cp_model.IntVar:
        if left == right:
            return self.endpoints[left]
        key = tuple(sorted((left, right)))
        if key not in self.products:
            product = self.model.NewBoolVar(f"product_{key[0]}_{key[1]}")
            x, y = self.endpoints[key[0]], self.endpoints[key[1]]
            # Exact Boolean conjunction, expressed as three clauses.
            self.model.AddImplication(product, x)
            self.model.AddImplication(product, y)
            self.model.AddBoolOr([x.Not(), y.Not(), product])
            self.products[key] = product
        return self.products[key]

    def add_endpoint_polynomial(
        self, label: str, endpoint_polynomial: EndpointPolynomial
    ) -> None:
        original = endpoint_polynomial
        reduced = divide_content(original)
        original_content = reduce(
            gcd, (abs(value) for value in original.values()), 0
        )
        self.equation_contents[label] = max(1, original_content)
        self.equation_term_counts[label] = len(reduced) - int(() in reduced)
        constant = reduced.get((), 0)
        terms = []
        for monomial, coefficient in reduced.items():
            if not monomial:
                continue
            if len(monomial) == 1:
                variable = self.endpoints[monomial[0]]
            elif len(monomial) == 2:
                variable = self.product(*monomial)
            else:
                raise AssertionError("degree exceeded two")
            terms.append(coefficient * variable)
        self.model.Add(sum(terms) == -constant)

    def add_polynomial(
        self, label: str, polynomial: ternary.Polynomial
    ) -> None:
        self.add_endpoint_polynomial(label, expand_polynomial(polynomial))

    def _add_roots(self) -> None:
        profile = self.system.case.profiles[self.profile_index]
        targets = orientation.profile_targets(profile)
        for root_index, target in enumerate(targets):
            terms = []
            for variable, coefficient in enumerate(
                self.system.root_coefficients[:, root_index]
            ):
                coefficient = int(coefficient)
                terms.append(coefficient * self.endpoints[2 * variable])
                terms.append(-coefficient * self.endpoints[2 * variable + 1])
            self.model.Add(sum(terms) == int(target))

    def statistics(self) -> dict[str, object]:
        proto = self.model.Proto()
        constraint_types = Counter(
            constraint.WhichOneof("constraint") for constraint in proto.constraints
        )
        return {
            "ternary_variables": len(self.system.keys),
            "endpoint_boolean_variables": len(self.endpoints),
            "reused_boolean_product_variables": len(self.products),
            "total_proto_variables": len(proto.variables),
            "total_proto_constraints": len(proto.constraints),
            "constraint_type_histogram": dict(sorted(constraint_types.items())),
            "fold_causal_equations": 82,
            "root_equations": 4,
            "shell_equations": 1,
            "equation_content_histogram": dict(
                sorted(Counter(self.equation_contents.values()).items())
            ),
            "equation_term_count_min": min(self.equation_term_counts.values()),
            "equation_term_count_max": max(self.equation_term_counts.values()),
            "equation_term_count_sum": sum(
                self.equation_term_counts.values()
            ),
        }


def peak_rss_megabytes() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # macOS reports bytes; Linux reports KiB.
    divisor = 1024 * 1024 if sys.platform == "darwin" else 1024
    return float(value) / divisor


def replay_solution(
    system: ExactSystem,
    profile_index: int,
    solver: cp_model.CpSolver,
    builder: ModelBuilder,
) -> dict[str, object]:
    point = []
    for variable in range(len(system.keys)):
        lower = solver.Value(builder.endpoints[2 * variable])
        upper = solver.Value(builder.endpoints[2 * variable + 1])
        if lower and upper:
            raise AssertionError("SAT model selected both endpoints")
        point.append(lower - upper)
    if sum(value != 0 for value in point) != 39:
        raise AssertionError("SAT model failed the shell on replay")

    rows = ternary.physical_rows(system.case, system.keys, point)
    correlations = [
        ternary.direct_correlation(rows, lag) for lag in range(84)
    ]
    if correlations[0] != 334:
        raise AssertionError("SAT model changed zero-lag energy")
    nonzero = {
        lag: value
        for lag, value in enumerate(correlations[1:], 1)
        if value
    }
    if nonzero:
        raise AssertionError(
            f"SAT model failed original-sequence replay: {nonzero}"
        )

    targets = orientation.profile_targets(
        system.case.profiles[profile_index]
    )
    roots = system.root_coefficients.T @ np.asarray(point, dtype=np.int16)
    if not np.array_equal(roots, targets):
        raise AssertionError(
            f"SAT model failed root replay: {roots} != {targets}"
        )
    for family in (system.anti, system.plus, system.causal):
        if any(
            ternary.evaluate_polynomial(polynomial, point)
            for polynomial in family
        ):
            raise AssertionError("SAT model failed symbolic equation replay")
    return {
        "ternary": point,
        "selected_endpoints": [
            [system.keys[index][0], system.keys[index][1], value]
            for index, value in enumerate(point)
            if value
        ],
        "root_values": roots.astype(int).tolist(),
        "aperiodic_correlations_1_through_83": correlations[1:],
        "status": (
            "SAT candidate passed direct original-sequence replay at all "
            "83 nonzero aperiodic lags"
        ),
    }


def solve_profile(
    system: ExactSystem,
    profile_index: int,
    seconds: float,
    workers: int,
    seed: int,
    log_progress: bool,
    fixed_endpoint_search: bool,
) -> dict[str, object]:
    builder = ModelBuilder(system, profile_index)
    model_stats = builder.statistics()
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    solver.parameters.cp_model_presolve = True
    solver.parameters.cp_model_probing_level = 2
    solver.parameters.linearization_level = 2
    solver.parameters.symmetry_level = 3
    solver.parameters.log_search_progress = log_progress
    if fixed_endpoint_search:
        builder.model.AddDecisionStrategy(
            builder.endpoints,
            cp_model.CHOOSE_FIRST,
            cp_model.SELECT_MAX_VALUE,
        )
        solver.parameters.search_branching = cp_model.FIXED_SEARCH
    started = time.monotonic()
    status = solver.Solve(builder.model)
    elapsed = time.monotonic() - started
    status_name = solver.StatusName(status)

    solution = None
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        solution = replay_solution(
            system, profile_index, solver, builder
        )
    response = solver.ResponseProto()
    return {
        "case": system.case_number,
        "q_block": system.case.block,
        "q_index": system.case.index,
        "profile_index": profile_index,
        "profile": [
            list(system.case.profiles[profile_index][0]),
            list(system.case.profiles[profile_index][1]),
        ],
        "model": model_stats,
        "solver": {
            "status": status_name,
            "wall_seconds_measured": elapsed,
            "wall_seconds_reported": solver.WallTime(),
            "user_seconds_reported": solver.UserTime(),
            "branches": int(response.num_branches),
            "conflicts": int(response.num_conflicts),
            "deterministic_time": float(response.deterministic_time),
            "best_objective_bound": solver.BestObjectiveBound(),
            "workers": workers,
            "fixed_endpoint_search": fixed_endpoint_search,
            "time_limit_seconds": seconds,
            "peak_process_rss_megabytes": peak_rss_megabytes(),
        },
        "solution": solution,
        "scope": (
            "SAT is trusted only after exact physical replay; UNKNOWN and "
            "CP-SAT UNSAT are diagnostics, not proof certificates"
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=int, default=1)
    parser.add_argument(
        "--profiles",
        default="0,1",
        help="comma-separated authoritative root-profile indices",
    )
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=668_780_041)
    parser.add_argument("--random-audit-samples", type=int, default=24)
    parser.add_argument("--log-progress", action="store_true")
    parser.add_argument(
        "--fixed-endpoint-search",
        action="store_true",
        help="branch on the 156 endpoint decisions before shared products",
    )
    parser.add_argument(
        "--audit-only",
        action="store_true",
        help="build and validate algebra/model statistics without solving",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not 0 < args.case <= 20:
        raise ValueError("this diagnostic is scoped to open cases 1,...,20")
    if not 1 <= args.workers <= 4:
        raise ValueError("workers must lie in 1,...,4")
    if not 0 < args.seconds <= 300:
        raise ValueError("seconds must lie in (0,300]")
    profile_indices = tuple(
        int(value) for value in args.profiles.split(",") if value
    )
    if not profile_indices or any(index not in (0, 1) for index in profile_indices):
        raise ValueError("profiles must select from 0,1")

    system = exact_system(args.case)
    audit = random_algebra_audit(
        system, args.random_audit_samples, args.seed ^ 0x668
    )
    if args.audit_only:
        results = []
        for profile_index in profile_indices:
            builder = ModelBuilder(system, profile_index)
            results.append(
                {
                    "profile_index": profile_index,
                    "profile": system.case.profiles[profile_index],
                    "model": builder.statistics(),
                }
            )
    else:
        results = [
            solve_profile(
                system,
                profile_index,
                args.seconds,
                args.workers,
                args.seed + profile_index,
                args.log_progress,
                args.fixed_endpoint_search,
            )
            for profile_index in profile_indices
        ]
    print(
        json.dumps(
            {
                "status": (
                    "exact algebra/model audit passed; bounded solver "
                    "results follow"
                ),
                "random_algebra_audit": audit,
                "results": results,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
