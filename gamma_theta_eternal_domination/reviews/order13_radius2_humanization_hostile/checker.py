#!/usr/bin/env python3
"""Clean-room hostile audit of the order-13 anchored-radius-two result.

This checker imports no campaign generator, transition core, model verifier,
or prior hostile checker.  It independently reconstructs the full C097
formula and its radius-two relaxations from the mathematical definitions,
compares exact DIMACS bytes, replays the addition-only proof with RAT
forbidden, and directly audits the three two-slice SAT controls.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
from typing import Iterable


N = 13
VERTICES = tuple(range(N))
S = frozenset((0, 1, 2))
ANCHORS = tuple(sorted(S))
OUTSIDE = tuple(range(3, N))
RESIDUAL = tuple(range(7, N))
PAIRS = tuple(itertools.combinations(VERTICES, 2))
TRIPLES = tuple(itertools.combinations(VERTICES, 3))
ALL_MASK = (1 << N) - 1

EXPECTED = {
    "full_c097": {
        "sha256": "76ff2768c7afd95ee535f8684515b0b15319b1f5ca69085447a1f7eba66393e1",
        "bytes": 4_784_714,
        "clauses": 84_614,
    },
    "radius2": {
        "sha256": "8bd4ae50e2ac06deb6560c4ff482eb19d7b64a4769029284da4660ccbefd1b55",
        "bytes": 4_667_702,
        "clauses": 76_214,
    },
    "proof": {
        "sha256": "f5fcbe26885ab229636d511d2b1ee47203478002fb22ce34407f1182d1c1eeea",
        "bytes": 9_367_094,
        "lines": 168_880,
    },
    "models": {
        "01": "6cb2f5951c4c1526d0162d4df156e9cf023196567070f0827034ce485a5cffd9",
        "02": "d9472ab2debd3d52367e155ce5fd62540646c111f232c212f469b01e280efb05",
        "12": "ac1e61b65661ef8a60094ebf93eae629993805113ceb227e60d9157b89792c57",
    },
    "two_slice_formulas": {
        "01": "14bfba6998ef348a1884a88a2b092325d08beb81f5b64b600bba8e44c10d1e72",
        "02": "90604d16600b51f0ae9a178300b0e17b44eaea6d0f428d1ee2549ad5ea624c87",
        "12": "bb2720da0ab48e2279c30ce3661a711009d9ee114f01ad8bcd8a49d7e02bf328",
    },
    "graph6": {
        "01": r"LBZ]ditl\jtoq}",
        "02": r"LBZMbqjntjJp`}",
        "12": r"LBZ]b|j\rpufme",
    },
    "source_note": "34c9ce6c2756e7ee5b791cf2ff7dc7edb9272307ced43e729b4d68edcbea8a28",
    "drat_trim": "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


class Formula:
    """Independent exact formula emitter with the production variable order."""

    def __init__(self, retained_anchors: frozenset[int] | None) -> None:
        if retained_anchors is not None:
            if not retained_anchors or not retained_anchors <= S:
                raise ValueError("retained anchors must be a nonempty subset of S")
        self.retained_anchors = retained_anchors
        self.next_variable = 1
        self.edge = self.allocate(PAIRS)
        self.witness = self.allocate(
            (u, v, w)
            for u, v in PAIRS
            for w in VERTICES
            if w not in (u, v)
        )
        self.family = self.allocate(TRIPLES)
        self.move = self.allocate(
            (state, attacked, guard)
            for state in TRIPLES
            for attacked in VERTICES
            if attacked not in state
            for guard in state
        )
        self.clauses: list[tuple[int, ...]] = []
        self.categories: dict[str, int] = {}
        self.closure_states: set[tuple[int, int, int]] = set()
        self.build()

    def allocate(self, keys: Iterable[object]) -> dict[object, int]:
        allocated: dict[object, int] = {}
        for key in keys:
            allocated[key] = self.next_variable
            self.next_variable += 1
        return allocated

    @property
    def variables(self) -> int:
        return self.next_variable - 1

    def e(self, u: int, v: int) -> int:
        return self.edge[pair(u, v)]

    def f(self, vertices: Iterable[int]) -> int:
        return self.family[tuple(sorted(vertices))]

    def direct(self, target: int, omitted: int) -> int:
        return self.f((S - {omitted}) | {target})

    def add(self, category: str, *literals: int) -> None:
        if not literals or any(literal == 0 for literal in literals):
            raise AssertionError("malformed clause")
        self.clauses.append(tuple(literals))
        self.categories[category] = self.categories.get(category, 0) + 1

    def closure_required(self, state: tuple[int, int, int]) -> bool:
        if self.retained_anchors is None:
            return True
        return bool(set(state) & self.retained_anchors)

    def build(self) -> None:
        # Edge variables are edges of H=complement(G).  No H-K4 says alpha<=3.
        for four in itertools.combinations(VERTICES, 4):
            self.add(
                "no_H_K4",
                *(-self.e(u, v) for u, v in itertools.combinations(four, 2)),
            )

        # No pair dominates G iff each pair has an outside vertex adjacent
        # in H to both members.
        for u, v in PAIRS:
            candidates = tuple(w for w in VERTICES if w not in (u, v))
            self.add(
                "pair_common_H_neighbor_choice",
                *(self.witness[(u, v, w)] for w in candidates),
            )
            for w in candidates:
                selector = self.witness[(u, v, w)]
                self.add("pair_common_H_neighbor_edge", -selector, self.e(u, w))
                self.add("pair_common_H_neighbor_edge", -selector, self.e(v, w))

        # Every selected triple dominates G.
        for state in TRIPLES:
            selected = self.family[state]
            for target in VERTICES:
                if target not in state:
                    self.add(
                        "selected_state_dominates",
                        -selected,
                        *(-self.e(target, guard) for guard in state),
                    )
        self.add("family_nonempty", *(self.family[state] for state in TRIPLES))

        # Full closure, radius two, or a two-anchor radius-two slice.
        # A retained-anchor set R imposes closure precisely on states D with
        # D intersect R nonempty.  For R=S this is the closed Johnson ball of
        # radius two around S.
        for state in TRIPLES:
            if not self.closure_required(state):
                continue
            self.closure_states.add(state)
            selected = self.family[state]
            for attacked in VERTICES:
                if attacked in state:
                    continue
                replies: list[int] = []
                for guard in state:
                    move = self.move[(state, attacked, guard)]
                    successor = tuple(
                        sorted((set(state) - {guard}) | {attacked})
                    )
                    replies.append(move)
                    self.add(
                        "move_uses_G_edge",
                        -move,
                        -self.e(guard, attacked),
                    )
                    self.add(
                        "move_reaches_selected_successor",
                        -move,
                        self.family[successor],
                    )
                self.add("selected_state_has_response", -selected, *replies)

        # Distinguished maximum independent state.
        for u, v in itertools.combinations(ANCHORS, 2):
            self.add("anchor_H_triangle", self.e(u, v))
        self.add("anchor_state_selected", self.family[ANCHORS])

        # H is not 3-colorable.  S fixes the three colors up to permutation.
        for tail in itertools.product(range(3), repeat=N - len(ANCHORS)):
            colors = ANCHORS + tail
            self.add(
                "anchored_non_3_coloring",
                *(
                    self.e(u, v)
                    for u, v in PAIRS
                    if colors[u] == colors[v]
                ),
            )

        # Exact no-full branch at S.
        for target in OUTSIDE:
            self.add(
                "no_full_direct_response",
                *(-self.direct(target, anchor) for anchor in ANCHORS),
            )

        def fixed_signature(vertex: int, signature: frozenset[int]) -> None:
            for anchor in ANCHORS:
                self.add(
                    "named_signature",
                    self.e(anchor, vertex)
                    if anchor in signature
                    else -self.e(anchor, vertex),
                )

        def fixed_list(vertex: int, response: frozenset[int]) -> None:
            for anchor in ANCHORS:
                direct = self.direct(vertex, anchor)
                self.add(
                    "named_response_list",
                    direct if anchor in response else -direct,
                )

        fixed_signature(3, frozenset((0,)))
        fixed_signature(4, frozenset((0,)))
        fixed_list(3, frozenset((1, 2)))
        self.add("named_pure_pair_H_edge", self.e(3, 4))

        fixed_signature(5, frozenset((2,)))
        fixed_signature(6, frozenset((2,)))
        fixed_list(5, frozenset((0, 1)))
        self.add("named_pure_pair_H_edge", self.e(5, 6))

        # Sort the six otherwise unnamed three-bit anchor signatures.
        for left, right in zip(RESIDUAL[:-1], RESIDUAL[1:], strict=True):
            for left_value in range(8):
                for right_value in range(left_value):
                    mismatch: list[int] = []
                    for bit, anchor in enumerate(ANCHORS):
                        left_bit = (left_value >> bit) & 1
                        right_bit = (right_value >> bit) & 1
                        mismatch.append(
                            -self.e(left, anchor)
                            if left_bit
                            else self.e(left, anchor)
                        )
                        mismatch.append(
                            -self.e(right, anchor)
                            if right_bit
                            else self.e(right, anchor)
                        )
                    self.add("residual_signature_sort", *mismatch)

        # Under sorting, label 10 nonneutral is exactly at most three neutral
        # residual vertices.
        self.add(
            "label10_nonneutral",
            *(self.e(anchor, 10) for anchor in ANCHORS),
        )

    def dimacs(self) -> bytes:
        header = f"p cnf {self.variables} {len(self.clauses)}\n"
        body = "".join(
            " ".join(map(str, clause)) + " 0\n" for clause in self.clauses
        )
        return (header + body).encode("ascii")


def parse_dimacs(data: bytes) -> tuple[int, list[tuple[int, ...]]]:
    lines = data.decode("ascii").splitlines()
    marker, kind, variables_text, clauses_text = lines[0].split()
    if (marker, kind) != ("p", "cnf"):
        raise AssertionError("bad DIMACS header")
    variables = int(variables_text)
    expected = int(clauses_text)
    clauses: list[tuple[int, ...]] = []
    for line in lines[1:]:
        literals = tuple(map(int, line.split()))
        if not literals or literals[-1] != 0 or 0 in literals[:-1]:
            raise AssertionError("malformed DIMACS clause")
        clauses.append(literals[:-1])
    if len(clauses) != expected:
        raise AssertionError("DIMACS clause-count mismatch")
    return variables, clauses


def parse_total_model(data: bytes, variables: int) -> dict[int, bool]:
    assignment: dict[int, bool] = {}
    status: str | None = None
    for raw in data.decode("ascii").splitlines():
        fields = raw.split()
        if not fields:
            continue
        if fields[0] == "s":
            status = " ".join(fields[1:])
        elif fields[0] == "v":
            for field in fields[1:]:
                literal = int(field)
                if literal == 0:
                    continue
                variable = abs(literal)
                if variable in assignment:
                    raise AssertionError(f"duplicate model variable {variable}")
                assignment[variable] = literal > 0
    if status != "SATISFIABLE":
        raise AssertionError(f"unexpected model status {status!r}")
    if set(assignment) != set(range(1, variables + 1)):
        raise AssertionError("model is not a total assignment")
    return assignment


def assignment_satisfies(
    clauses: Iterable[tuple[int, ...]], assignment: dict[int, bool]
) -> bool:
    return all(
        any(assignment[abs(literal)] == (literal > 0) for literal in clause)
        for clause in clauses
    )


def adjacency_from_assignment(
    formula: Formula, assignment: dict[int, bool]
) -> tuple[int, ...]:
    adjacency = [0] * N
    for u, v in PAIRS:
        # Formula edge=true is an H-edge; false is a G-edge.
        if not assignment[formula.edge[(u, v)]]:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    return tuple(adjacency)


def selected_family(
    formula: Formula, assignment: dict[int, bool]
) -> frozenset[frozenset[int]]:
    return frozenset(
        frozenset(state)
        for state in TRIPLES
        if assignment[formula.family[state]]
    )


def dominates(adjacency: tuple[int, ...], state: frozenset[int]) -> bool:
    covered = sum(1 << vertex for vertex in state)
    for vertex in state:
        covered |= adjacency[vertex]
    return covered == ALL_MASK


def independent(adjacency: tuple[int, ...], state: frozenset[int]) -> bool:
    return all(
        not adjacency[u] & (1 << v)
        for u, v in itertools.combinations(state, 2)
    )


def domination_number(adjacency: tuple[int, ...]) -> int:
    for size in range(N + 1):
        for state in itertools.combinations(VERTICES, size):
            if dominates(adjacency, frozenset(state)):
                return size
    raise AssertionError("domination search exhausted")


def independence_number(adjacency: tuple[int, ...]) -> int:
    for size in range(N, -1, -1):
        if any(
            independent(adjacency, frozenset(state))
            for state in itertools.combinations(VERTICES, size)
        ):
            return size
    raise AssertionError("independence search exhausted")


def independent_domination_number(adjacency: tuple[int, ...]) -> int:
    for size in range(N + 1):
        for state in itertools.combinations(VERTICES, size):
            frozen = frozenset(state)
            if independent(adjacency, frozen) and dominates(adjacency, frozen):
                return size
    raise AssertionError("independent domination search exhausted")


def complement_coloring(
    adjacency_g: tuple[int, ...], colors: int
) -> tuple[int, ...] | None:
    adjacency_h = tuple(
        (ALL_MASK ^ (1 << vertex)) & ~adjacency_g[vertex]
        for vertex in VERTICES
    )
    assigned = [-1] * N

    def search(remaining: int) -> bool:
        if remaining == 0:
            return True
        candidates = [vertex for vertex in VERTICES if assigned[vertex] < 0]
        vertex = max(
            candidates,
            key=lambda item: (
                len(
                    {
                        assigned[neighbor]
                        for neighbor in VERTICES
                        if adjacency_h[item] & (1 << neighbor)
                        and assigned[neighbor] >= 0
                    }
                ),
                (adjacency_h[item] & sum(
                    1 << neighbor for neighbor in candidates
                )).bit_count(),
            ),
        )
        forbidden = {
            assigned[neighbor]
            for neighbor in VERTICES
            if adjacency_h[vertex] & (1 << neighbor)
            and assigned[neighbor] >= 0
        }
        for color in range(colors):
            if color in forbidden:
                continue
            assigned[vertex] = color
            if search(remaining - 1):
                return True
            assigned[vertex] = -1
        return False

    return tuple(assigned) if search(N) else None


def clique_cover_number(adjacency_g: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    for colors in range(1, N + 1):
        coloring = complement_coloring(adjacency_g, colors)
        if coloring is not None:
            return colors, coloring
    raise AssertionError("coloring search exhausted")


def greatest_eternal_kernel(
    adjacency: tuple[int, ...], size: int
) -> frozenset[frozenset[int]]:
    active = {
        frozenset(state)
        for state in itertools.combinations(VERTICES, size)
        if dominates(adjacency, frozenset(state))
    }
    while True:
        next_active: set[frozenset[int]] = set()
        for state in active:
            valid = True
            for attacked in VERTICES:
                if attacked in state:
                    continue
                if not any(
                    adjacency[guard] & (1 << attacked)
                    and frozenset((state - {guard}) | {attacked}) in active
                    for guard in state
                ):
                    valid = False
                    break
            if valid:
                next_active.add(state)
        if next_active == active:
            return frozenset(active)
        active = next_active


def eternal_number(
    adjacency: tuple[int, ...],
) -> tuple[int, dict[int, int]]:
    kernel_sizes: dict[int, int] = {}
    for size in range(domination_number(adjacency), N + 1):
        kernel = greatest_eternal_kernel(adjacency, size)
        kernel_sizes[size] = len(kernel)
        if kernel:
            return size, kernel_sizes
    raise AssertionError("eternal search exhausted")


def graph6(adjacency: tuple[int, ...]) -> str:
    if not 0 <= N <= 62:
        raise AssertionError("only short graph6 header implemented")
    bits = [
        1 if adjacency[u] & (1 << v) else 0
        for v in range(1, N)
        for u in range(v)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(N + 63) + "".join(payload)


def response_list(
    family: frozenset[frozenset[int]], target: int
) -> frozenset[int]:
    return frozenset(
        omitted
        for omitted in ANCHORS
        if frozenset((S - {omitted}) | {target}) in family
    )


def anchor_signature(
    adjacency_g: tuple[int, ...], target: int
) -> frozenset[int]:
    return frozenset(
        anchor
        for anchor in ANCHORS
        if not adjacency_g[target] & (1 << anchor)
    )


def audit_control(
    tag: str,
    retained: frozenset[int],
    formula: Formula,
    model_path: Path,
) -> dict[str, object]:
    model_bytes = model_path.read_bytes()
    assignment = parse_total_model(model_bytes, formula.variables)
    formula_satisfied = assignment_satisfies(formula.clauses, assignment)
    adjacency = adjacency_from_assignment(formula, assignment)
    family = selected_family(formula, assignment)
    if not formula_satisfied:
        raise AssertionError(f"{tag}: assignment does not satisfy formula")
    if S not in family:
        raise AssertionError(f"{tag}: anchor state absent")
    if not all(dominates(adjacency, state) for state in family):
        raise AssertionError(f"{tag}: selected nondominating state")

    required_checks = 0
    failures: list[tuple[tuple[int, ...], int]] = []
    for state in family:
        for attacked in VERTICES:
            if attacked in state:
                continue
            replies = [
                guard
                for guard in state
                if adjacency[guard] & (1 << attacked)
                and frozenset((state - {guard}) | {attacked}) in family
            ]
            if state & retained:
                required_checks += 1
                if not replies:
                    raise AssertionError(
                        f"{tag}: retained closure failure {sorted(state)}, {attacked}"
                    )
            elif not replies:
                failures.append((tuple(sorted(state)), attacked))
    if not failures:
        raise AssertionError(f"{tag}: unexpectedly full closure")
    if any(frozenset(state) & retained for state, _ in failures):
        raise AssertionError(f"{tag}: failure in retained slice")
    omitted = next(iter(S - retained))
    omitted_slice_failures = [
        (state, attacked)
        for state, attacked in failures
        if omitted in state and not (frozenset(state) & retained)
    ]
    if not omitted_slice_failures:
        raise AssertionError(f"{tag}: no omitted single-anchor failure")

    signatures = {
        target: anchor_signature(adjacency, target) for target in OUTSIDE
    }
    lists = {target: response_list(family, target) for target in OUTSIDE}
    signature_values = [
        sum(1 << anchor for anchor in signatures[target])
        for target in RESIDUAL
    ]
    named_ok = (
        signatures[3] == signatures[4] == frozenset((0,))
        and signatures[5] == signatures[6] == frozenset((2,))
        and lists[3] == frozenset((1, 2))
        and lists[5] == frozenset((0, 1))
        and not adjacency[3] & (1 << 4)
        and not adjacency[5] & (1 << 6)
    )
    structural_ok = (
        named_ok
        and all(0 < len(values) < 3 for values in lists.values())
        and signature_values == sorted(signature_values)
        and signature_values[3] != 0
    )

    gamma = domination_number(adjacency)
    independent_gamma = independent_domination_number(adjacency)
    alpha = independence_number(adjacency)
    gamma_infinity, kernel_sizes = eternal_number(adjacency)
    theta, coloring = clique_cover_number(adjacency)
    parameters = {
        "gamma": gamma,
        "i": independent_gamma,
        "alpha": alpha,
        "gamma_infinity": gamma_infinity,
        "theta": theta,
    }
    expected_parameters = {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 4,
        "theta": 4,
    }
    encoded_graph6 = graph6(adjacency)
    return {
        "tag": tag,
        "model_sha256": sha256_bytes(model_bytes),
        "model_hash_pinned": (
            sha256_bytes(model_bytes) == EXPECTED["models"][tag]
        ),
        "formula_assignment_satisfies_all_clauses": formula_satisfied,
        "structural_normalization_exact": structural_ok,
        "graph6": encoded_graph6,
        "graph6_matches_report": encoded_graph6 == EXPECTED["graph6"][tag],
        "parameters": parameters,
        "parameters_match_report": parameters == expected_parameters,
        "theta_4_coloring": list(coloring),
        "eternal_kernel_sizes_until_first_nonempty": {
            str(size): count for size, count in kernel_sizes.items()
        },
        "selected_family_size": len(family),
        "required_partial_closure_checks": required_checks,
        "full_closure_failures": len(failures),
        "omitted_anchor": omitted,
        "omitted_anchor_slice_failures": len(omitted_slice_failures),
        "all_failures_outside_retained_slices": all(
            not (frozenset(state) & retained) for state, _ in failures
        ),
        "first_failures": [
            {"state": list(state), "attack": attacked}
            for state, attacked in sorted(failures)[:5]
        ],
    }


def closure_gadget_truth_table() -> dict[str, object]:
    failures = 0
    for bits in itertools.product((False, True), repeat=7):
        selected = bits[0]
        h_edges = bits[1:4]
        successors = bits[4:7]
        intended = (not selected) or any(
            not h_edges[index] and successors[index] for index in range(3)
        )
        encoded = any(
            all(
                (not moves[index] or not h_edges[index])
                and (not moves[index] or successors[index])
                for index in range(3)
            )
            and ((not selected) or any(moves))
            for moves in itertools.product((False, True), repeat=3)
        )
        failures += intended != encoded
    return {
        "assignments": 128,
        "failures": failures,
        "exact": failures == 0,
    }


def proof_shape(data: bytes) -> dict[str, object]:
    lines = data.decode("ascii").splitlines()
    deletion_lines = sum(line.startswith("d ") for line in lines)
    malformed = sum(
        not line
        or (
            not line.startswith("d ")
            and not all(field.lstrip("-").isdigit() for field in line.split())
        )
        for line in lines
    )
    return {
        "lines": len(lines),
        "bytes": len(data),
        "sha256": sha256_bytes(data),
        "deletion_lines": deletion_lines,
        "addition_only": deletion_lines == 0,
        "terminal_empty_clause": bool(lines) and lines[-1] == "0",
        "malformed_lines": malformed,
    }


def strict_rup_replay(
    checker: Path, instance: Path, proof: Path
) -> dict[str, object]:
    command = [
        str(checker),
        str(instance),
        str(proof),
        "-I",
        "-f",
        "-W",
        "-U",
        "-t",
        "180",
    ]
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=240,
        check=False,
    )
    output = completed.stdout
    stable_output = [
        " ".join(line.split())
        for line in output.splitlines()
        if line.strip() and not line.strip().startswith("c verification time:")
    ]
    return {
        "command_flags": ["ASCII", "forward", "warnings-fatal", "RUP-only"],
        "exit": completed.returncode,
        "verified_once": output.count("s VERIFIED") == 1,
        "zero_RAT_lemmas": "0 RAT lemmas in core" in output,
        "warning_count": output.upper().count("WARNING"),
        "stable_output_without_wall_time": stable_output,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()

    review = Path(__file__).resolve().parent
    campaign = review.parents[1]
    source = campaign / "math/working/order13_no_full_a7_humanization"
    c097_source = campaign / "math/working/order13_no_full_a7_structured"
    drat_trim = campaign / "tools/drat_trim_2023_05_22/drat-trim"
    note_bytes = (source / "NOTE.md").read_bytes()
    note_text = note_bytes.decode("utf-8")
    status_phrases = (
        "a proof-log-backed **certified finite strengthening**",
        (
            "An independent generator and hostile coverage audit have "
            "reconstructed the\nradius reduction and accepted the UNSAT proof."
        ),
        "## 2. Certified finite strengthening",
    )
    retired_phrases = (
        "a proof-log-backed **finite strengthening candidate**",
        "The UNSAT statement remains a **certificate candidate**",
        "## 2. Finite strengthening candidate",
    )
    source_note_checks = {
        "sha256": sha256_bytes(note_bytes),
        "current_hash_pinned": (
            sha256_bytes(note_bytes) == EXPECTED["source_note"]
        ),
        "three_post_audit_status_phrases_each_once": all(
            note_text.count(phrase) == 1 for phrase in status_phrases
        ),
        "pre_audit_pending_phrases_absent": all(
            phrase not in note_text for phrase in retired_phrases
        ),
        "decisive_CNF_hash_unchanged": (
            EXPECTED["radius2"]["sha256"] in note_text
        ),
        "decisive_proof_hash_unchanged": (
            EXPECTED["proof"]["sha256"] in note_text
        ),
        "exact_census_unchanged": all(
            marker in note_text
            for marker in (
                "variables:  9,802",
                "clauses:   76,214",
                "addition-only DRAT lines: 168,880",
                "addition-only DRAT bytes: 9,367,094",
            )
        ),
        "all_control_graph6_strings_unchanged": all(
            graph6_value in note_text
            for graph6_value in EXPECTED["graph6"].values()
        ),
        "unresolved_scope_caveat_retained": (
            "This lane did **not** produce a universal proof" in note_text
            and "counterexamples to the gamma--theta conjecture" in note_text
        ),
    }

    full = Formula(None)
    radius2 = Formula(S)
    full_bytes = full.dimacs()
    radius2_bytes = radius2.dimacs()
    source_radius2 = (source / "closure-radius-2.cnf").read_bytes()
    source_full = (c097_source / "instance.cnf").read_bytes()
    radius_variables, radius_clauses = parse_dimacs(source_radius2)

    omitted_states = set(TRIPLES) - radius2.closure_states
    full_clause_set = set(full.clauses)
    radius_clause_set = set(radius2.clauses)
    omitted_clauses = full_clause_set - radius_clause_set
    formula_checks = {
        "full_reconstruction_matches_C097_bytes": full_bytes == source_full,
        "full_hash_pinned": sha256_bytes(full_bytes)
        == EXPECTED["full_c097"]["sha256"],
        "full_bytes": len(full_bytes),
        "full_clauses": len(full.clauses),
        "radius2_reconstruction_byte_identical": radius2_bytes == source_radius2,
        "radius2_hash_pinned": sha256_bytes(radius2_bytes)
        == EXPECTED["radius2"]["sha256"],
        "radius2_bytes": len(radius2_bytes),
        "radius2_variables": radius_variables,
        "radius2_clauses": len(radius_clauses),
        "radius2_no_duplicate_clauses": len(set(radius_clauses))
        == len(radius_clauses),
        "radius2_no_tautologies": all(
            not any(-literal in clause for literal in clause)
            for clause in radius_clauses
        ),
        "radius2_is_clause_subset_of_C097": radius_clause_set < full_clause_set,
        "exact_omitted_clause_count_8400": len(omitted_clauses) == 8_400,
        "exact_omitted_state_count_120": len(omitted_states) == 120,
        "all_omitted_states_disjoint_from_S": all(
            not (set(state) & S) for state in omitted_states
        ),
        "every_disjoint_triple_omitted": omitted_states
        == {
            state for state in TRIPLES if not (set(state) & S)
        },
        "retained_closure_states_166": len(radius2.closure_states) == 166,
        "retained_closure_obligations_1660": (
            len(radius2.closure_states) * 10 == 1660
        ),
        "unused_variables_expected": len(
            set(range(1, radius2.variables + 1))
            - {
                abs(literal)
                for clause in radius2.clauses
                for literal in clause
            }
        )
        == 3_600,
        "closure_category_counts": {
            category: radius2.categories.get(category, 0)
            for category in (
                "move_uses_G_edge",
                "move_reaches_selected_successor",
                "selected_state_has_response",
            )
        },
    }

    proof_path = source / "closure-radius-2-proof.additions.drat"
    proof_bytes = proof_path.read_bytes()
    shape = proof_shape(proof_bytes)
    proof_checks = {
        "shape": shape,
        "hash_pinned": shape["sha256"] == EXPECTED["proof"]["sha256"],
        "bytes_pinned": shape["bytes"] == EXPECTED["proof"]["bytes"],
        "lines_pinned": shape["lines"] == EXPECTED["proof"]["lines"],
        "checker_hash": sha256_file(drat_trim),
        "checker_hash_pinned": sha256_file(drat_trim)
        == EXPECTED["drat_trim"],
        "strict_replay": strict_rup_replay(
            drat_trim, source / "closure-radius-2.cnf", proof_path
        ),
    }

    controls: list[dict[str, object]] = []
    for tag, retained_tuple in (
        ("01", (0, 1)),
        ("02", (0, 2)),
        ("12", (1, 2)),
    ):
        retained = frozenset(retained_tuple)
        formula = Formula(retained)
        formula_bytes = formula.dimacs()
        formula_hash = sha256_bytes(formula_bytes)
        control = audit_control(
            tag,
            retained,
            formula,
            source / f"closure-radius-2-anchors-{tag}.model",
        )
        control["formula"] = {
            "variables": formula.variables,
            "clauses": len(formula.clauses),
            "sha256": formula_hash,
            "reported_hash_pinned": (
                formula_hash == EXPECTED["two_slice_formulas"][tag]
            ),
            "closure_states": len(formula.closure_states),
            "closure_obligations": len(formula.closure_states) * 10,
        }
        controls.append(control)

    expected_control_counts = {
        "01": (142, 640, 47, 13),
        "02": (160, 600, 22, 5),
        "12": (153, 570, 30, 6),
    }
    control_checks = []
    for control in controls:
        expected_counts = expected_control_counts[str(control["tag"])]
        observed_counts = (
            control["selected_family_size"],
            control["required_partial_closure_checks"],
            control["full_closure_failures"],
            control["omitted_anchor_slice_failures"],
        )
        control_checks.append(
            control["model_hash_pinned"]
            and control["formula_assignment_satisfies_all_clauses"]
            and control["structural_normalization_exact"]
            and control["graph6_matches_report"]
            and control["parameters_match_report"]
            and control["all_failures_outside_retained_slices"]
            and control["formula"]["reported_hash_pinned"]
            and control["formula"]["variables"] == 9802
            and control["formula"]["clauses"] == 73064
            and control["formula"]["closure_states"] == 121
            and control["formula"]["closure_obligations"] == 1210
            and observed_counts == expected_counts
        )

    truth_table = closure_gadget_truth_table()
    strict = proof_checks["strict_replay"]
    scalar_formula_checks = [
        value
        for value in formula_checks.values()
        if isinstance(value, bool)
    ]
    verdict = (
        "PASS"
        if all(scalar_formula_checks)
        and formula_checks["full_bytes"] == EXPECTED["full_c097"]["bytes"]
        and formula_checks["full_clauses"] == EXPECTED["full_c097"]["clauses"]
        and formula_checks["radius2_bytes"] == EXPECTED["radius2"]["bytes"]
        and formula_checks["radius2_variables"] == 9802
        and formula_checks["radius2_clauses"] == EXPECTED["radius2"]["clauses"]
        and formula_checks["closure_category_counts"]
        == {
            "move_uses_G_edge": 4980,
            "move_reaches_selected_successor": 4980,
            "selected_state_has_response": 1660,
        }
        and shape["addition_only"]
        and shape["terminal_empty_clause"]
        and shape["malformed_lines"] == 0
        and proof_checks["hash_pinned"]
        and proof_checks["bytes_pinned"]
        and proof_checks["lines_pinned"]
        and proof_checks["checker_hash_pinned"]
        and strict["exit"] == 0
        and strict["verified_once"]
        and strict["zero_RAT_lemmas"]
        and strict["warning_count"] == 0
        and all(
            value
            for key, value in source_note_checks.items()
            if key != "sha256"
        )
        and truth_table["exact"]
        and all(control_checks)
        else "FAIL"
    )

    result = {
        "verdict": verdict,
        "formula": formula_checks,
        "proof": proof_checks,
        "source_note": source_note_checks,
        "closure_gadget_truth_table": truth_table,
        "controls": controls,
        "scope": {
            "certified_statement": (
                "Within the exact normalized no-full residual branch used by "
                "C097, no order-13 assignment exists even when closure is "
                "required only for selected triples D with D intersect "
                "S nonempty."
            ),
            "relation_to_C097": (
                "This is a strict 8,400-clause relaxation of the already "
                "certified C097 residual CNF.  It strengthens the finite "
                "mechanism but does not enlarge C097's graph universe."
            ),
            "two_slice_refutation": (
                "Each relaxation retaining only two of the three anchor "
                "slices is SAT and has an independently checked graph with "
                "(gamma,i,alpha,gamma_infinity,theta)=(3,3,3,4,4)."
            ),
            "prerequisites_for_graph_level_use": [
                "C090 full-response branch exclusion",
                "C093 two-type and pure-pair reduction",
                "C096 four-neutral obstruction giving at most three neutrals",
            ],
            "not_claimed": [
                "a new order frontier beyond C097",
                "the arbitrary-order parameter-three theorem",
                "the universal gamma-theta conjecture",
                "that any SAT control has gamma=gamma_infinity",
            ],
        },
    }
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.result is not None:
        args.result.parent.mkdir(parents=True, exist_ok=True)
        args.result.write_text(output, encoding="utf-8")
    print(output, end="")
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
