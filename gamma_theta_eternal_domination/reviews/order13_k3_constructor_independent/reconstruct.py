#!/usr/bin/env python3
"""Clean-room order-13, k=3 CNF reconstructor and semantic auditor.

This module is intentionally standard-library-only.  It imports no campaign
search, synthesis, coloring, or verifier implementation.  The graph encoded
by edge variables is H = complement(G).

The implementation is a finite transcription of the definitions:

* H has no K4 and every pair has an external common neighbor;
* a nonempty family of dominating triples is closed under one-guard moves;
* every maximum independent triple of G (triangle of H) is selected;
* G is connected;
* one of four named, hub-free induced odd-hole templates is fixed; and
* every first-use-canonical proper coloring of the forced positive template
  graph is obstructed.

The program can emit a deterministic DIMACS formula, parse it independently,
or run the complete clean-room audit and mutation suite.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence


N = 13
K = 3
HOLE_LENGTHS = (5, 7, 9, 11)

EXPECTED = {
    5: {
        "variables": 9802,
        "base_clauses": 29791,
        "base_literals": 227006,
        "color_rows": 10935,
        "full_clauses": 40726,
        "full_literals": 493820,
        "size_bytes": 1805539,
        "sha256": "8df56270f1abf3a9a8e5d088a78680dcde0198292eaa51da78a7fce9179d2fb5",
    },
    7: {
        "variables": 9802,
        "base_clauses": 29800,
        "base_literals": 227019,
        "color_rows": 5103,
        "full_clauses": 34903,
        "full_literals": 349248,
        "size_bytes": 1372338,
        "sha256": "3e1c86ccbcfc1e04b3ec4de29ec5b7d342cf909553655f959b1c35de0a36c340",
    },
    9: {
        "variables": 9802,
        "base_clauses": 29813,
        "base_literals": 227028,
        "color_rows": 2295,
        "full_clauses": 32108,
        "full_literals": 281028,
        "size_bytes": 1168197,
        "sha256": "3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea",
    },
    11: {
        "variables": 9802,
        "base_clauses": 29830,
        "base_literals": 227033,
        "color_rows": 1023,
        "full_clauses": 30853,
        "full_literals": 250664,
        "size_bytes": 1076723,
        "sha256": "1ab880e6d2cf9014e70362437b530c8d534fe57db7620029d06bc3ed9afee901",
    },
}


def pairs(vertices: Iterable[int]) -> Iterator[tuple[int, int]]:
    yield from itertools.combinations(vertices, 2)


def triples(vertices: Iterable[int]) -> Iterator[tuple[int, int, int]]:
    yield from itertools.combinations(vertices, 3)


def edge_key(a: int, b: int) -> tuple[int, int]:
    if a == b:
        raise ValueError("a loop is not an edge")
    return (a, b) if a < b else (b, a)


@dataclass(frozen=True)
class VariableMap:
    edge: Mapping[tuple[int, int], int]
    witness: Mapping[tuple[int, int, int], int]
    family: Mapping[tuple[int, int, int], int]
    move: Mapping[tuple[tuple[int, int, int], int, int], int]
    count: int

    @classmethod
    def derive(cls, *, occupied_attack_mutant: bool = False) -> "VariableMap":
        """Allocate variables in independent, explicitly specified blocks."""
        nxt = 1
        edge: dict[tuple[int, int], int] = {}
        for uv in pairs(range(N)):
            edge[uv] = nxt
            nxt += 1

        witness: dict[tuple[int, int, int], int] = {}
        for a, b in pairs(range(N)):
            for c in range(N):
                if c not in (a, b):
                    witness[(a, b, c)] = nxt
                    nxt += 1

        family: dict[tuple[int, int, int], int] = {}
        states = list(triples(range(N)))
        for state in states:
            family[state] = nxt
            nxt += 1

        move: dict[tuple[tuple[int, int, int], int, int], int] = {}
        for state in states:
            attacks = range(N) if occupied_attack_mutant else (
                r for r in range(N) if r not in state
            )
            for r in attacks:
                for u in state:
                    move[(state, r, u)] = nxt
                    nxt += 1

        return cls(edge=edge, witness=witness, family=family, move=move, count=nxt - 1)

    def e(self, a: int, b: int) -> int:
        return self.edge[edge_key(a, b)]


@dataclass(frozen=True)
class TaggedClause:
    family: str
    literals: tuple[int, ...]


def _add(
    clauses: list[TaggedClause],
    family: str,
    literals: Iterable[int],
) -> None:
    clause = tuple(literals)
    if not clause:
        raise AssertionError(f"empty clause in {family}")
    if 0 in clause:
        raise AssertionError(f"literal zero inside {family}")
    clauses.append(TaggedClause(family, clause))


def forced_template_edges(hole: int) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    """Return exactly the positive and negative H-edge units of the template."""
    if hole not in HOLE_LENGTHS:
        raise ValueError(f"unsupported hole length {hole}")
    rim = tuple(range(hole))
    positive = {
        edge_key(v, (v + 1) % hole)
        for v in rim
    }
    negative = set(pairs(rim)) - positive
    z = hole
    positive.update((edge_key(0, z), edge_key(1, z)))
    return positive, negative


def derive_base(
    hole: int,
    vm: VariableMap,
    *,
    mutation: str | None = None,
) -> list[TaggedClause]:
    """Derive the base clauses directly from their quantified predicates."""
    if mutation not in {
        None,
        "all_guards",
        "omit_result_domination",
        "complement_reversal",
        "omit_alpha",
        "omit_gamma",
        "unsafe_anchor",
    }:
        raise ValueError(f"unknown mutation {mutation!r}")
    clauses: list[TaggedClause] = []

    # alpha(G) <= 3, equivalently omega(H) <= 3.
    if mutation != "omit_alpha":
        for four in itertools.combinations(range(N), 4):
            _add(clauses, "no_k4", (-vm.e(a, b) for a, b in pairs(four)))

    # gamma(G) >= 3: each pair has an external common H-neighbor.
    if mutation != "omit_gamma":
        for a, b in pairs(range(N)):
            witnesses = [
                vm.witness[(a, b, c)]
                for c in range(N)
                if c not in (a, b)
            ]
            _add(clauses, "pair_has_witness", witnesses)
            for c, w in (
                (c, vm.witness[(a, b, c)])
                for c in range(N)
                if c not in (a, b)
            ):
                _add(clauses, "pair_witness_edge", (-w, vm.e(a, c)))
                _add(clauses, "pair_witness_edge", (-w, vm.e(b, c)))

    positive, negative = forced_template_edges(hole)
    rim_cycle = {
        edge_key(v, (v + 1) % hole)
        for v in range(hole)
    }
    for uv in pairs(range(hole)):
        if uv in rim_cycle:
            _add(clauses, "template_rim_positive", (vm.edge[uv],))
        else:
            _add(clauses, "template_rim_negative", (-vm.edge[uv],))
    for x in range(hole, N):
        _add(
            clauses,
            "template_hub_free",
            (-vm.e(x, v) for v in range(hole)),
        )
    _add(clauses, "template_named_common_neighbor", (vm.e(0, hole),))
    _add(clauses, "template_named_common_neighbor", (vm.e(1, hole),))

    if mutation == "unsafe_anchor":
        # The fixed hole already fixes its justified triangle {0,1,hole}.
        # Simultaneously fixing this unrelated triangle has no proved orbit
        # incidence with the selected hole and is intentionally unsafe.
        for a, b in ((0, N - 2), (0, N - 1), (N - 2, N - 1)):
            _add(clauses, "unsafe_unrelated_anchor", (vm.e(a, b),))

    # G is connected: for each unordered cut, represented by the side with 0,
    # at least one crossing pair is a nonedge of H.
    for mask in range(0, 1 << (N - 1)):
        side = {0}
        side.update(v for v in range(1, N) if mask & (1 << (v - 1)))
        if len(side) == N:
            continue
        _add(
            clauses,
            "g_connected_cut",
            (
                -vm.e(u, v)
                for u in sorted(side)
                for v in range(N)
                if v not in side
            ),
        )

    states = tuple(triples(range(N)))

    # A selected triple dominates G.  In H it has no external common neighbor.
    if mutation != "omit_result_domination":
        for state in states:
            f = vm.family[state]
            for x in range(N):
                if x not in state:
                    _add(
                        clauses,
                        "selected_state_dominates",
                        (-f, *(-vm.e(x, v) for v in state)),
                    )
    _add(clauses, "family_nonempty", (vm.family[state] for state in states))

    # Exact one-guard response, for attacks only at unoccupied vertices.
    for state in states:
        f = vm.family[state]
        for r in range(N):
            if r in state:
                continue
            response: list[int] = [-f]
            for u in state:
                m = vm.move[(state, r, u)]
                response.append(m)
                edge_lit = (
                    vm.e(u, r)
                    if mutation == "complement_reversal"
                    else -vm.e(u, r)
                )
                _add(clauses, "move_traverses_g_edge", (-m, edge_lit))
                if mutation == "all_guards":
                    # Deliberately wrong: preserve the attacked vertex but
                    # also replace another guard, emulating a multi-guard step.
                    others = [v for v in state if v != u]
                    replacement = next(
                        v for v in range(N) if v not in state and v != r
                    )
                    successor = tuple(sorted((r, others[0], replacement)))
                else:
                    successor = tuple(sorted((set(state) - {u}) | {r}))
                _add(
                    clauses,
                    "move_successor_selected",
                    (-m, vm.family[successor]),
                )
            _add(clauses, "attack_has_response", response)

    # Every H-triangle is a maximum independent triple of G and is selected.
    for state in states:
        a, b, c = state
        _add(
            clauses,
            "triangle_selected",
            (-vm.e(a, b), -vm.e(a, c), -vm.e(b, c), vm.family[state]),
        )

    return clauses


def canonical_template_colorings(hole: int) -> list[tuple[int, ...]]:
    """All first-use-canonical proper 3-colorings of forced positive edges."""
    positive, _ = forced_template_edges(hole)
    neighbors_before: list[list[int]] = [[] for _ in range(N)]
    for a, b in positive:
        neighbors_before[max(a, b)].append(min(a, b))
    for values in neighbors_before:
        values.sort()

    result: list[tuple[int, ...]] = []
    row = [-1] * N

    def visit(v: int, maximum: int) -> None:
        if v == N:
            result.append(tuple(row))
            return
        upper = min(K - 1, maximum + 1)
        for color in range(upper + 1):
            if any(row[u] == color for u in neighbors_before[v]):
                continue
            row[v] = color
            visit(v + 1, max(maximum, color))
            row[v] = -1

    visit(0, -1)
    return result


def derive_coloring_clauses(
    rows: Sequence[Sequence[int]],
    vm: VariableMap,
) -> list[TaggedClause]:
    clauses: list[TaggedClause] = []
    for row in rows:
        if len(row) != N:
            raise ValueError("wrong coloring length")
        _add(
            clauses,
            "complete_coloring_obstruction",
            (
                vm.e(a, b)
                for a, b in pairs(range(N))
                if row[a] == row[b]
            ),
        )
    return clauses


def serialize_dimacs(variable_count: int, clauses: Sequence[TaggedClause]) -> bytes:
    out = [f"p cnf {variable_count} {len(clauses)}\n"]
    out.extend(
        " ".join(str(lit) for lit in tagged.literals) + " 0\n"
        for tagged in clauses
    )
    return "".join(out).encode("ascii")


@dataclass(frozen=True)
class ParsedDimacs:
    variables: int
    clauses: tuple[tuple[int, ...], ...]


def parse_dimacs(payload: bytes) -> ParsedDimacs:
    """Strict independent DIMACS parser for the generated certificate input."""
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ValueError("DIMACS is not ASCII") from exc
    if not text.endswith("\n"):
        raise ValueError("DIMACS must end in LF")
    lines = text.splitlines()
    if not lines or not lines[0].startswith("p cnf "):
        raise ValueError("missing canonical header")
    header = lines[0].split()
    if len(header) != 4 or header[:2] != ["p", "cnf"]:
        raise ValueError("malformed header")
    try:
        variables, promised = int(header[2]), int(header[3])
    except ValueError as exc:
        raise ValueError("noninteger header") from exc
    if variables <= 0 or promised < 0:
        raise ValueError("invalid header count")
    clauses: list[tuple[int, ...]] = []
    for line_no, line in enumerate(lines[1:], 2):
        fields = line.split()
        if not fields or fields[-1] != "0" or "0" in fields[:-1]:
            raise ValueError(f"noncanonical clause termination at line {line_no}")
        try:
            clause = tuple(int(field) for field in fields[:-1])
        except ValueError as exc:
            raise ValueError(f"noninteger literal at line {line_no}") from exc
        if not clause:
            raise ValueError(f"empty clause at line {line_no}")
        if any(abs(lit) > variables for lit in clause):
            raise ValueError(f"out-of-range literal at line {line_no}")
        clauses.append(clause)
    if len(clauses) != promised:
        raise ValueError("clause count differs from header")
    return ParsedDimacs(variables, tuple(clauses))


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def census(clauses: Sequence[TaggedClause]) -> dict[str, object]:
    family_counts = Counter(tagged.family for tagged in clauses)
    family_literals = Counter()
    for tagged in clauses:
        family_literals[tagged.family] += len(tagged.literals)
    return {
        "clauses": len(clauses),
        "literals": sum(len(tagged.literals) for tagged in clauses),
        "family_clause_counts": dict(sorted(family_counts.items())),
        "family_literal_counts": dict(sorted(family_literals.items())),
    }


def audit_variable_map(vm: VariableMap) -> dict[str, object]:
    expected_blocks = {
        "edge": 78,
        "witness": 858,
        "family": 286,
        "move": 8580,
    }
    actual = {
        "edge": len(vm.edge),
        "witness": len(vm.witness),
        "family": len(vm.family),
        "move": len(vm.move),
    }
    all_ids = (
        list(vm.edge.values())
        + list(vm.witness.values())
        + list(vm.family.values())
        + list(vm.move.values())
    )
    if actual != expected_blocks:
        raise AssertionError((actual, expected_blocks))
    if sorted(all_ids) != list(range(1, vm.count + 1)):
        raise AssertionError("variable ids are not a unique contiguous partition")
    for (state, r, u), _ in vm.move.items():
        if r in state or u not in state:
            raise AssertionError("move domain admits an occupied attack or absent guard")
    return {
        "block_counts": actual,
        "contiguous_unique_ids": True,
        "unoccupied_attack_domain_only": True,
        "total": vm.count,
    }


def audit_coloring_bank(
    hole: int,
    rows: Sequence[tuple[int, ...]],
) -> dict[str, object]:
    positive, _ = forced_template_edges(hole)
    if len(set(rows)) != len(rows):
        raise AssertionError("duplicate coloring row")
    for row in rows:
        if row[0] != 0:
            raise AssertionError("not first-use canonical")
        seen_max = -1
        for color in row:
            if color < 0 or color >= K or color > seen_max + 1:
                raise AssertionError("not a restricted-growth string")
            seen_max = max(seen_max, color)
        if any(row[a] == row[b] for a, b in positive):
            raise AssertionError("row violates forced positive edge")

    # Independent completeness count: enumerate all 3^13 named rows proper on
    # the small forced-positive graph, then divide by the free S3 action.
    labeled_count = 0
    for row in itertools.product(range(K), repeat=N):
        if all(row[a] != row[b] for a, b in positive):
            labeled_count += 1
    if labeled_count % 6:
        raise AssertionError("color-name action is not free")
    if len(rows) != labeled_count // 6:
        raise AssertionError("incomplete canonical coloring bank")
    return {
        "canonical_rows": len(rows),
        "labeled_rows": labeled_count,
        "color_permutation_orbit_size": 6,
        "complete": True,
        "no_duplicate_rows": True,
    }


def audit_clause_semantics(
    hole: int,
    vm: VariableMap,
    base: Sequence[TaggedClause],
) -> dict[str, object]:
    """Check every quantified index domain and exact family multiplicity."""
    observed = Counter(tagged.family for tagged in base)
    expected = {
        "no_k4": 715,
        "pair_witness_edge": 1716,
        "pair_has_witness": 78,
        "family_nonempty": 1,
        "selected_state_dominates": 2860,
        "move_traverses_g_edge": 8580,
        "move_successor_selected": 8580,
        "attack_has_response": 2860,
        "triangle_selected": 286,
        "g_connected_cut": 4095,
        "template_rim_positive": hole,
        "template_rim_negative": hole * (hole - 1) // 2 - hole,
        "template_hub_free": N - hole,
        "template_named_common_neighbor": 2,
    }
    if observed != Counter(expected):
        raise AssertionError({"observed": observed, "expected": expected})

    # Build a second, checker-side family specification.  This deliberately
    # does not call derive_base: generation and validation have separate
    # transition/clause paths even within this clean-room module.
    expected_by_family: dict[str, Counter[tuple[int, ...]]] = {}
    actual_by_family: dict[str, Counter[tuple[int, ...]]] = {}

    def expect(family: str, literals: Iterable[int]) -> None:
        expected_by_family.setdefault(family, Counter())[tuple(literals)] += 1

    for tagged in base:
        actual_by_family.setdefault(tagged.family, Counter())[tagged.literals] += 1

    for four in itertools.combinations(range(N), 4):
        expect("no_k4", (-vm.e(a, b) for a, b in pairs(four)))

    for a, b in pairs(range(N)):
        candidate_vertices = tuple(c for c in range(N) if c not in (a, b))
        expect(
            "pair_has_witness",
            (vm.witness[(a, b, c)] for c in candidate_vertices),
        )
        for c in candidate_vertices:
            w = vm.witness[(a, b, c)]
            expect("pair_witness_edge", (-w, vm.e(a, c)))
            expect("pair_witness_edge", (-w, vm.e(b, c)))

    rim_cycle = {
        edge_key(v, (v + 1) % hole)
        for v in range(hole)
    }
    for uv in pairs(range(hole)):
        if uv in rim_cycle:
            expect("template_rim_positive", (vm.edge[uv],))
        else:
            expect("template_rim_negative", (-vm.edge[uv],))
    for x in range(hole, N):
        expect("template_hub_free", (-vm.e(x, v) for v in range(hole)))
    expect("template_named_common_neighbor", (vm.e(0, hole),))
    expect("template_named_common_neighbor", (vm.e(1, hole),))

    # Independent cut enumeration uses direct subset tuples rather than the
    # generator's integer-mask-to-set representation.
    outer = tuple(range(1, N))
    for subset_size in range(len(outer) + 1):
        for subset in itertools.combinations(outer, subset_size):
            side = (0, *subset)
            if len(side) == N:
                continue
            side_set = frozenset(side)
            expect(
                "g_connected_cut",
                (
                    -vm.e(u, v)
                    for u in side
                    for v in range(N)
                    if v not in side_set
                ),
            )

    states = tuple(triples(range(N)))
    for state in states:
        f = vm.family[state]
        outside = tuple(x for x in range(N) if x not in state)
        for x in outside:
            expect(
                "selected_state_dominates",
                (-f, *(-vm.e(x, v) for v in state)),
            )
    expect("family_nonempty", (vm.family[state] for state in states))

    for state in states:
        f = vm.family[state]
        for r in (x for x in range(N) if x not in state):
            response = [-f]
            for u in state:
                move = vm.move[(state, r, u)]
                response.append(move)
                expect("move_traverses_g_edge", (-move, -vm.e(u, r)))
                successor = tuple(sorted(v for v in (*state, r) if v != u))
                expect(
                    "move_successor_selected",
                    (-move, vm.family[successor]),
                )
            expect("attack_has_response", response)

    for a, b, c in states:
        state = (a, b, c)
        expect(
            "triangle_selected",
            (-vm.e(a, b), -vm.e(a, c), -vm.e(b, c), vm.family[state]),
        )

    if actual_by_family != expected_by_family:
        raise AssertionError("tagged clause multiset differs from semantic reconstruction")

    positive, negative = forced_template_edges(hole)
    if positive & negative:
        raise AssertionError("template forces an edge both ways")
    if edge_key(0, hole) not in positive or edge_key(1, hole) not in positive:
        raise AssertionError("named common-neighbor triangle absent")
    if set(pairs(range(hole))) != (positive & set(pairs(range(hole)))) | negative:
        raise AssertionError("rim is not completely specified")
    if any(name.startswith(("row_", "column_", "signature_", "reflection_"))
           or name == "unsafe_unrelated_anchor" for name in observed):
        raise AssertionError("unproved symmetry breaker present")

    return {
        "exact_family_clause_counts": dict(sorted(expected.items())),
        "tagged_multisets_exact": True,
        "template_positive_negative_disjoint": True,
        "template_rim_fully_induced": True,
        "only_justified_template_relabeling": True,
        "no_doublelex_signature_reflection_or_extra_anchor": True,
    }


def run_mutation_suite(hole: int, vm: VariableMap, reference: bytes) -> dict[str, object]:
    """Require independent checks to reject seven deliberate model errors."""
    results: dict[str, object] = {}

    occupied_vm = VariableMap.derive(occupied_attack_mutant=True)
    results["occupied_attacks"] = {
        "detected": occupied_vm.count != vm.count
        and len(occupied_vm.move) != len(vm.move),
        "mutant_variables": occupied_vm.count,
        "reason": "move-variable domain includes r in T",
    }

    for name in (
        "all_guards",
        "omit_result_domination",
        "complement_reversal",
        "omit_alpha",
        "omit_gamma",
        "unsafe_anchor",
    ):
        try:
            mutant_base = derive_base(hole, vm, mutation=name)
        except (KeyError, AssertionError, ValueError) as exc:
            # An invalid all-guards successor can be rejected during derivation;
            # this is still fail-closed detection.
            results[name] = {
                "detected": True,
                "stage": "construction",
                "reason": type(exc).__name__,
            }
            continue
        rows = canonical_template_colorings(hole)
        mutant = serialize_dimacs(
            vm.count,
            mutant_base + derive_coloring_clauses(rows, vm),
        )
        detected = mutant != reference
        try:
            audit_clause_semantics(hole, vm, mutant_base)
        except AssertionError:
            semantic_rejection = True
        else:
            semantic_rejection = False
        results[name] = {
            "detected": detected and semantic_rejection,
            "byte_sha256": sha256(mutant),
            "semantic_rejection": semantic_rejection,
        }

    rows = canonical_template_colorings(hole)
    incomplete = rows[:-1]
    coloring_audit_rejected = False
    try:
        audit_coloring_bank(hole, incomplete)
    except AssertionError:
        coloring_audit_rejected = True
    mutant = serialize_dimacs(
        vm.count,
        derive_base(hole, vm) + derive_coloring_clauses(incomplete, vm),
    )
    results["incomplete_coloring_obstruction"] = {
        "detected": mutant != reference and coloring_audit_rejected,
        "mutant_rows": len(incomplete),
        "semantic_rejection": coloring_audit_rejected,
        "byte_sha256": sha256(mutant),
    }

    if not all(bool(record["detected"]) for record in results.values()):
        raise AssertionError({"undetected_mutations": results})
    return results


def reconstruct(hole: int) -> tuple[VariableMap, list[TaggedClause], list[tuple[int, ...]], bytes]:
    vm = VariableMap.derive()
    base = derive_base(hole, vm)
    rows = canonical_template_colorings(hole)
    clauses = base + derive_coloring_clauses(rows, vm)
    payload = serialize_dimacs(vm.count, clauses)
    return vm, base, rows, payload


def run_audit(*, include_mutations: bool = True) -> dict[str, object]:
    formulas: list[dict[str, object]] = []
    mutations: dict[str, object] = {}
    for hole in HOLE_LENGTHS:
        vm, base, rows, payload = reconstruct(hole)
        parsed = parse_dimacs(payload)
        if parsed.variables != vm.count:
            raise AssertionError("parsed variable count mismatch")
        all_clauses = base + derive_coloring_clauses(rows, vm)
        if parsed.clauses != tuple(tagged.literals for tagged in all_clauses):
            raise AssertionError("parser/reconstructor clause mismatch")

        variable_audit = audit_variable_map(vm)
        semantic_audit = audit_clause_semantics(hole, vm, base)
        bank_audit = audit_coloring_bank(hole, rows)
        base_census = census(base)
        full_census = census(all_clauses)
        actual = {
            "variables": vm.count,
            "base_clauses": base_census["clauses"],
            "base_literals": base_census["literals"],
            "color_rows": len(rows),
            "full_clauses": full_census["clauses"],
            "full_literals": full_census["literals"],
            "size_bytes": len(payload),
            "sha256": sha256(payload),
        }
        agreement = {
            key: actual[key] == EXPECTED[hole][key]
            for key in EXPECTED[hole]
        }
        if not all(agreement.values()):
            raise AssertionError(
                {"hole": hole, "actual": actual, "expected": EXPECTED[hole]}
            )
        formulas.append(
            {
                "template": f"hole{hole}",
                **actual,
                "expected_agreement": agreement,
                "dimacs_strict_round_trip": True,
                "variable_audit": variable_audit,
                "semantic_audit": semantic_audit,
                "coloring_bank_audit": bank_audit,
                "base_family_census": base_census,
            }
        )
        if include_mutations:
            mutations[f"hole{hole}"] = run_mutation_suite(hole, vm, payload)

    return {
        "schema": "gamma-theta-order13-k3-independent-constructor-audit-v1",
        "schema_version": 1,
        "implementation_boundary": {
            "standard_library_only": True,
            "imports_production_or_legacy_clause_core": False,
            "solver_run": False,
            "sat_or_unsat_claim": False,
            "graph_semantics": "edge variables encode H=complement(G)",
            "attack_model": "unoccupied attacks; exactly one adjacent guard moves",
            "symmetry": (
                "template relabeling plus color-name quotient only; no unrelated "
                "anchor, DoubleLex, signature, or reflection breaker"
            ),
        },
        "formulas": formulas,
        "mutation_suite": mutations,
        "verdict": "ACCEPT_EXACT_CLEAN_ROOM_RECONSTRUCTION" if include_mutations else
        "ACCEPT_EXACT_CLEAN_ROOM_RECONSTRUCTION_WITHOUT_MUTATION_RUN",
        "limitations": [
            "This audit reconstructs and parses formulas; it does not solve them.",
            "Byte agreement is with the frozen exploratory hashes, not an UNSAT certificate.",
            "A negative order-13 result still requires checked proofs for all four templates.",
        ],
    }


def canonical_json(data: object) -> bytes:
    return (
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=True)
        + "\n"
    ).encode("utf-8")


def compact_evidence(full: Mapping[str, object]) -> dict[str, object]:
    """Publication-sized replay record derived from the complete audit."""
    source_path = Path(__file__).resolve()
    formulas = []
    for raw in full["formulas"]:
        if not isinstance(raw, Mapping):
            raise AssertionError("nonmapping formula audit")
        semantic = raw["semantic_audit"]
        bank = raw["coloring_bank_audit"]
        variables = raw["variable_audit"]
        if not all(isinstance(value, Mapping) for value in (semantic, bank, variables)):
            raise AssertionError("malformed audit component")
        formulas.append(
            {
                key: raw[key]
                for key in (
                    "template",
                    "variables",
                    "base_clauses",
                    "base_literals",
                    "color_rows",
                    "full_clauses",
                    "full_literals",
                    "size_bytes",
                    "sha256",
                )
            }
            | {
                "all_frozen_fields_agree": all(raw["expected_agreement"].values()),
                "strict_dimacs_round_trip": raw["dimacs_strict_round_trip"],
                "semantic_clause_multisets_exact": semantic[
                    "tagged_multisets_exact"
                ],
                "only_justified_template_relabeling": semantic[
                    "only_justified_template_relabeling"
                ],
                "no_unproved_symmetry_breaker": semantic[
                    "no_doublelex_signature_reflection_or_extra_anchor"
                ],
                "coloring_bank_complete": bank["complete"],
                "labeled_coloring_rows": bank["labeled_rows"],
                "color_orbit_size": bank["color_permutation_orbit_size"],
                "variable_blocks": variables["block_counts"],
                "unoccupied_attack_domain_only": variables[
                    "unoccupied_attack_domain_only"
                ],
            }
        )

    mutation_summary = {
        template: {
            name: record["detected"]
            for name, record in sorted(records.items())
        }
        for template, records in sorted(full["mutation_suite"].items())
    }
    if not all(
        detected
        for records in mutation_summary.values()
        for detected in records.values()
    ):
        raise AssertionError("compact evidence cannot accept an undetected mutation")

    source_payload = source_path.read_bytes()
    return {
        "schema": "gamma-theta-order13-k3-independent-constructor-evidence-v1",
        "schema_version": 1,
        "source": {
            "path": (
                "reviews/order13_k3_constructor_independent/reconstruct.py"
            ),
            "sha256": sha256(source_payload),
            "size_bytes": len(source_payload),
        },
        "implementation_boundary": full["implementation_boundary"],
        "formulas": formulas,
        "mutation_detection": mutation_summary,
        "all_mutations_detected": True,
        "verdict": full["verdict"],
        "limitations": full["limitations"],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    audit_parser = sub.add_parser("audit")
    audit_parser.add_argument(
        "--without-mutations",
        action="store_true",
        help="skip the deliberate model-error suite",
    )
    sub.add_parser(
        "evidence",
        help="emit compact deterministic evidence from the complete audit",
    )
    emit_parser = sub.add_parser("emit")
    emit_parser.add_argument("--hole", type=int, choices=HOLE_LENGTHS, required=True)
    emit_parser.add_argument("--output", type=Path, required=True)
    parse_parser = sub.add_parser("parse")
    parse_parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)

    if args.command == "audit":
        sys.stdout.buffer.write(
            canonical_json(run_audit(include_mutations=not args.without_mutations))
        )
        return 0
    if args.command == "evidence":
        sys.stdout.buffer.write(canonical_json(compact_evidence(run_audit())))
        return 0
    if args.command == "emit":
        _, _, _, payload = reconstruct(args.hole)
        args.output.write_bytes(payload)
        return 0
    if args.command == "parse":
        parsed = parse_dimacs(args.path.read_bytes())
        result = {
            "path": str(args.path),
            "variables": parsed.variables,
            "clauses": len(parsed.clauses),
            "literals": sum(map(len, parsed.clauses)),
            "sha256": sha256(args.path.read_bytes()),
        }
        sys.stdout.buffer.write(canonical_json(result))
        return 0
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
