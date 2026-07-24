#!/usr/bin/env python3
"""Exact local-excess root cover for an order-43 Ramsey(5,5) candidate.

For a vertex v let A=N(v), B=V\\(A union {v}), and

    c(v) = e(B) - e(A) - d(v)(43 - 2d(v))/2.

The sum of c(v) over all vertices is zero, and c(v) is invariant under graph
complementation.  Hence a hypothetical order-43 Ramsey(5,5) graph can be
complemented and relabelled so that vertex 0 has degree d in {18,19,20,21}
and c(0)<=0.  With H=complement(G[B]), this last condition is exactly one
cardinality lower bound on e(A)+e(H).

This module constructs a deterministic exact cover plan.  It also describes
an optional useful refinement by the complement-invariant parameter

    mu = min(delta(G), 42 - Delta(G)).

Unlike a mere interval label, every refined mu branch enforces mu exactly:
the global interval [mu,42-mu] is paired with a selector cover requiring some
vertex to have degree mu or 42-mu.

No SAT solve or nonexistence claim is made here.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

from direct_ramsey_cnf import (
    SequentialCounter,
    allocate_sequential_counter,
    build_direct_instance,
    variable_for_edge,
)
from global_minmax_degree_cover import additional_degree_units


ORDER = 43
ROOT = Path(__file__).resolve().parents[1]
BASE_VARIABLE_COUNT = 65_403
BASE_CLAUSE_COUNT = 2_052_132
BASE_CNF_SHA256 = (
    "141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1"
)
BASE_METADATA_SHA256 = (
    "88906686b2554cf1b5b9051eae4a200b878944278ed91682b78d9f40d43cf70c"
)
DEGREE_BOUNDS = (18, 24)
CROOT_DEGREES = (18, 19, 20, 21)
MU_VALUES = (18, 19, 20)
SCHEMA = "ramsey55.global_croot_cover.v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def clause_stream_sha256(clauses: Iterable[Sequence[int]]) -> str:
    digest = hashlib.sha256()
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return digest.hexdigest()


def graph_degrees(adjacency: Sequence[int]) -> tuple[int, ...]:
    return tuple(neighbors.bit_count() for neighbors in adjacency)


def complement(adjacency: Sequence[int]) -> list[int]:
    order = len(adjacency)
    mask = (1 << order) - 1
    return [
        mask & ~(neighbors | (1 << vertex))
        for vertex, neighbors in enumerate(adjacency)
    ]


def relabel(adjacency: Sequence[int], old_order: Sequence[int]) -> list[int]:
    order = len(adjacency)
    if sorted(old_order) != list(range(order)):
        raise ValueError("old_order is not a permutation")
    result = [0] * order
    for new_left, old_left in enumerate(old_order):
        for new_right in range(new_left + 1, order):
            old_right = old_order[new_right]
            if (adjacency[old_left] >> old_right) & 1:
                result[new_left] |= 1 << new_right
                result[new_right] |= 1 << new_left
    return result


def induced_edge_count(adjacency: Sequence[int], vertices: Sequence[int]) -> int:
    return sum(
        (adjacency[left] >> right) & 1
        for left, right in itertools.combinations(vertices, 2)
    )


def local_excess_twice(adjacency: Sequence[int], vertex: int) -> int:
    """Return 2*c(v), avoiding half-integral arithmetic."""

    order = len(adjacency)
    if not 0 <= vertex < order:
        raise ValueError("vertex is outside graph")
    neighbors = tuple(
        other
        for other in range(order)
        if other != vertex and (adjacency[vertex] >> other) & 1
    )
    nonneighbors = tuple(
        other
        for other in range(order)
        if other != vertex and not (adjacency[vertex] >> other) & 1
    )
    degree = len(neighbors)
    return (
        2
        * (
            induced_edge_count(adjacency, nonneighbors)
            - induced_edge_count(adjacency, neighbors)
        )
        - degree * (order - 2 * degree)
    )


def normalize_croot(adjacency: Sequence[int]) -> tuple[list[int], bool, int, int]:
    """Choose c(v)<=0, orient it to degree at most 21, and relabel it to 0."""

    if len(adjacency) != ORDER:
        raise ValueError(f"expected a graph of order {ORDER}")
    degrees = graph_degrees(adjacency)
    if any(not DEGREE_BOUNDS[0] <= degree <= DEGREE_BOUNDS[1] for degree in degrees):
        raise ValueError("graph does not satisfy the certified degree bounds")
    candidates = [
        vertex
        for vertex in range(ORDER)
        if local_excess_twice(adjacency, vertex) <= 0
    ]
    if not candidates:
        raise AssertionError("zero-sum local excess has no nonpositive vertex")
    root = candidates[0]
    graph = list(adjacency)
    complemented = degrees[root] > (ORDER - 1) // 2
    if complemented:
        graph = complement(graph)
    degree = graph[root].bit_count()
    if degree not in CROOT_DEGREES:
        raise AssertionError("oriented c-root degree is outside 18 through 21")
    neighbors = [
        vertex
        for vertex in range(ORDER)
        if vertex != root and (graph[root] >> vertex) & 1
    ]
    nonneighbors = [
        vertex
        for vertex in range(ORDER)
        if vertex != root and not (graph[root] >> vertex) & 1
    ]
    normalized = relabel(graph, (root, *neighbors, *nonneighbors))
    excess_twice = local_excess_twice(normalized, 0)
    if excess_twice > 0:
        raise AssertionError("complement or relabelling changed c-root sign")
    return normalized, complemented, degree, excess_twice


def croot_threshold(degree: int) -> int:
    """Minimum integer value of e(A)+e(complement(G[B]))."""

    if degree not in CROOT_DEGREES:
        raise ValueError("unsupported c-root degree")
    b_size = ORDER - 1 - degree
    rational = Fraction(math.comb(b_size, 2), 1) - Fraction(
        degree * (ORDER - 2 * degree), 2
    )
    return math.ceil(rational)


def croot_star_units(degree: int) -> tuple[int, ...]:
    if degree not in CROOT_DEGREES:
        raise ValueError("unsupported c-root degree")
    return tuple(
        (
            variable_for_edge(ORDER, 0, other)
            if other <= degree
            else -variable_for_edge(ORDER, 0, other)
        )
        for other in range(1, ORDER)
    )


def croot_good_literals(degree: int) -> tuple[int, ...]:
    """Literals counted by e(A)+e(complement(G[B]))."""

    if degree not in CROOT_DEGREES:
        raise ValueError("unsupported c-root degree")
    side_a = tuple(range(1, degree + 1))
    side_b = tuple(range(degree + 1, ORDER))
    return tuple(
        variable_for_edge(ORDER, left, right)
        for left, right in itertools.combinations(side_a, 2)
    ) + tuple(
        -variable_for_edge(ORDER, left, right)
        for left, right in itertools.combinations(side_b, 2)
    )


def croot_bad_literals(degree: int) -> tuple[int, ...]:
    return tuple(-literal for literal in croot_good_literals(degree))


def croot_counter(
    degree: int, first_auxiliary: int = BASE_VARIABLE_COUNT + 1
) -> tuple[SequentialCounter, int]:
    good = croot_good_literals(degree)
    bad_bound = len(good) - croot_threshold(degree)
    return allocate_sequential_counter(
        croot_bad_literals(degree),
        bad_bound,
        first_auxiliary,
        f"croot_d{degree}_bad_internal_literals_at_most_{bad_bound}",
    )


def basic_appended_clauses(degree: int) -> tuple[tuple[int, ...], ...]:
    counter, _next_variable = croot_counter(degree)
    return tuple((literal,) for literal in croot_star_units(degree)) + tuple(
        counter.clauses()
    )


def exact_mu_selector_clauses(
    degree: int, mu: int, first_selector: int
) -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...], int]:
    """Encode an extremal degree witness under global interval [mu,42-mu].

    Base counter variables use forward threshold semantics.  Under the global
    interval, selecting ``-E[v,mu+1]`` forces degree(v)=mu, while selecting
    ``-N[v,mu+1]`` forces nondegree(v)=mu, i.e. degree(v)=42-mu.
    """

    if degree not in CROOT_DEGREES or mu not in MU_VALUES or mu > degree:
        raise ValueError("invalid (degree, mu) refined branch")
    instance = build_direct_instance(ORDER)
    if instance.variable_count != BASE_VARIABLE_COUNT:
        raise AssertionError("base direct counter layout changed")
    selectors = tuple(range(first_selector, first_selector + 2 * ORDER))
    clauses: list[tuple[int, ...]] = [selectors]
    trigger_variables: list[int] = []
    for vertex in range(ORDER):
        low_selector = selectors[2 * vertex]
        high_selector = selectors[2 * vertex + 1]
        edge_final = instance.counters[2 * vertex].rows[-1]
        nonedge_final = instance.counters[2 * vertex + 1].rows[-1]
        edge_at_least_mu_plus_one = edge_final[mu]
        nonedge_at_least_mu_plus_one = nonedge_final[mu]
        clauses.append((-low_selector, -edge_at_least_mu_plus_one))
        clauses.append((-high_selector, -nonedge_at_least_mu_plus_one))
        trigger_variables.extend(
            (edge_at_least_mu_plus_one, nonedge_at_least_mu_plus_one)
        )
    return tuple(clauses), tuple(trigger_variables), first_selector + 2 * ORDER


def refined_appended_clauses(
    degree: int, mu: int
) -> tuple[tuple[tuple[int, ...], ...], int, tuple[int, ...]]:
    counter, next_variable = croot_counter(degree)
    interval_units = additional_degree_units(mu)
    selector_clauses, triggers, after_selectors = exact_mu_selector_clauses(
        degree, mu, next_variable
    )
    clauses = (
        tuple((literal,) for literal in croot_star_units(degree))
        + tuple(counter.clauses())
        + tuple((literal,) for literal in interval_units)
        + selector_clauses
    )
    return clauses, after_selectors, triggers


def basic_branch_record(degree: int) -> dict[str, object]:
    good = croot_good_literals(degree)
    counter, next_variable = croot_counter(degree)
    additions = basic_appended_clauses(degree)
    threshold = croot_threshold(degree)
    b_size = ORDER - 1 - degree
    raw_bound = Fraction(math.comb(b_size, 2), 1) - Fraction(
        degree * (ORDER - 2 * degree), 2
    )
    return {
        "degree": degree,
        "A_size": degree,
        "B_size": b_size,
        "croot_threshold_rational": (
            str(raw_bound.numerator)
            if raw_bound.denominator == 1
            else f"{raw_bound.numerator}/{raw_bound.denominator}"
        ),
        "good_literal_count": len(good),
        "good_literal_stream_sha256": clause_stream_sha256(
            (literal,) for literal in good
        ),
        "required_good_literal_count": threshold,
        "bad_literal_at_most_bound": len(good) - threshold,
        "star_unit_count": len(croot_star_units(degree)),
        "star_units_sha256": clause_stream_sha256(
            (literal,) for literal in croot_star_units(degree)
        ),
        "counter_first_auxiliary": BASE_VARIABLE_COUNT + 1,
        "counter_auxiliary_count": counter.auxiliary_count,
        "counter_clause_count": counter.clause_count,
        "appended_clause_count": len(additions),
        "appended_clause_stream_sha256": clause_stream_sha256(additions),
        "variable_count": next_variable - 1,
        "clause_count": BASE_CLAUSE_COUNT + len(additions),
    }


def refined_branch_record(degree: int, mu: int) -> dict[str, object]:
    clauses, after_selectors, triggers = refined_appended_clauses(degree, mu)
    counter, next_variable = croot_counter(degree)
    interval_units = additional_degree_units(mu)
    selector_first = next_variable
    selectors = tuple(range(selector_first, selector_first + 2 * ORDER))
    return {
        "branch_id": f"mu{mu}_d{degree}",
        "mu": mu,
        "degree": degree,
        "global_degree_interval": [mu, ORDER - 1 - mu],
        "global_interval_unit_count": len(interval_units),
        "global_interval_units_sha256": clause_stream_sha256(
            (literal,) for literal in interval_units
        ),
        "exact_mu_condition": (
            "at least one selected vertex has degree mu or degree 42-mu"
        ),
        "selector_variable_first": selector_first,
        "selector_count": len(selectors),
        "selector_order": (
            "vertex 0 low, vertex 0 high, vertex 1 low, vertex 1 high, ..."
        ),
        "selector_cover_clause_sha256": clause_stream_sha256((selectors,)),
        "selector_implication_clause_count": 2 * ORDER,
        "base_counter_trigger_variable_count": len(triggers),
        "base_counter_trigger_variables_sha256": clause_stream_sha256(
            (variable,) for variable in triggers
        ),
        "counter_auxiliary_count": counter.auxiliary_count,
        "appended_clause_count": len(clauses),
        "appended_clause_stream_sha256": clause_stream_sha256(clauses),
        "variable_count": after_selectors - 1,
        "clause_count": BASE_CLAUSE_COUNT + len(clauses),
    }


def build_plan() -> dict[str, object]:
    basic = [basic_branch_record(degree) for degree in CROOT_DEGREES]
    refined = [
        refined_branch_record(degree, mu)
        for mu in MU_VALUES
        for degree in CROOT_DEGREES
        if mu <= degree
    ]
    if len(refined) != 9:
        raise AssertionError("unexpected exact-mu refinement count")
    return {
        "schema": SCHEMA,
        "status": "EXACT_COVER_PLAN_NO_SOLVE_CLAIM",
        "order": ORDER,
        "base_cnf_sha256": BASE_CNF_SHA256,
        "base_metadata_sha256": BASE_METADATA_SHA256,
        "base_variable_count": BASE_VARIABLE_COUNT,
        "base_clause_count": BASE_CLAUSE_COUNT,
        "certified_base_degree_interval": list(DEGREE_BOUNDS),
        "local_excess_definition": (
            "c(v)=e(G[V minus (N(v) union {v})])-e(G[N(v)])"
            "-d(v)(43-2d(v))/2"
        ),
        "zero_sum_identity": (
            "sum_v(e(B_v)-e(A_v))=sum_{xy in E}(43-d(x)-d(y))"
            "=43|E|-sum_v d(v)^2"
            "=sum_v d(v)(43-2d(v))/2"
        ),
        "complement_invariance": "c_complement(v)=c_G(v)",
        "normalization": (
            "choose any c(v)<=0, complement if d(v)>21, relabel it to 0, "
            "and relabel its neighbours before its nonneighbours"
        ),
        "basic_cover": {
            "degrees": list(CROOT_DEGREES),
            "branch_count": len(basic),
            "branches": basic,
            "cover_reason": (
                "zero-sum gives c(v)<=0; complement invariance and the "
                "certified degree interval [18,24] orient its degree to "
                "18, 19, 20, or 21"
            ),
            "cardinality_semantics": (
                "good literals are edges inside A and nonedges inside B; "
                "their count is e(A)+e(complement(G[B])), and its lower "
                "bound is equivalent to c(0)<=0"
            ),
        },
        "optional_exact_mu_refinement": {
            "parameter": "mu=min(delta(G),42-Delta(G))",
            "mu_values": list(MU_VALUES),
            "parity_elimination": (
                "mu=21 forces a 21-regular graph on 43 vertices, impossible "
                "because its degree sum is odd"
            ),
            "branch_count": len(refined),
            "branch_order": (
                "mu increasing, then c-root degree increasing"
            ),
            "branches": refined,
            "exactness": (
                "The symmetric global interval alone would only be an "
                "overlapping label. Each branch additionally has an "
                "86-selector cover: selected low forces degree<=mu and "
                "selected high forces nondegree<=mu using the existing "
                "forward threshold counters. Combined with the interval, "
                "this forces degree exactly mu or 42-mu, hence invariant "
                "mu exactly."
            ),
            "cover_reason": (
                "mu is complement-invariant. In actual invariant branch mu, "
                "all degrees lie in [mu,42-mu], an extremal vertex has degree "
                "mu or 42-mu, and the oriented c-root degree lies in [mu,21]."
            ),
        },
        "source": "src/global_croot_cover.py",
        "source_sha256": sha256_file(Path(__file__)),
        "checker_source": "verify/global_croot_cover_check.py",
        "checker_source_sha256": sha256_file(
            ROOT / "verify/global_croot_cover_check.py"
        ),
        "test_source": "tests/global_croot_cover_tests.py",
        "test_source_sha256": sha256_file(
            ROOT / "tests/global_croot_cover_tests.py"
        ),
        "claim_limit": (
            "This artifact specifies exact CNF additions and an exhaustive "
            "symmetry cover only. It contains no SAT model, solver run, "
            "UNSAT certificate, or Ramsey-bound improvement."
        ),
    }


def main() -> int:
    print(json.dumps(build_plan(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
