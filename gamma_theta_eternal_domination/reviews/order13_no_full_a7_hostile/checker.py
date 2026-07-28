#!/usr/bin/env python3
"""Hostile clean-room audit of the structured order-13 no-full formula.

This checker deliberately imports no campaign search generator, decomposition
script, or transition implementation.  It reconstructs the exact DIMACS from
the mathematical definition, checks the local Boolean gadgets, verifies the
retained artifact hashes and syntax, and replays both retained proof streams
with RAT additions forbidden.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Iterable


N = 13
ANCHORS = (0, 1, 2)
OUTSIDE = tuple(range(3, N))
RESIDUAL = tuple(range(7, N))
SOURCE_SEARCH_SHA256 = (
    "15684fd87cdea18daa30f3506a72aa5e81a57bf4e5af94aef214f9d151f4d755"
)
SOURCE_INSTANCE_SHA256 = (
    "76ff2768c7afd95ee535f8684515b0b15319b1f5ca69085447a1f7eba66393e1"
)
SOURCE_RAW_PROOF_SHA256 = (
    "c5807a20b263bce64f40b1e998db2a947f221a0cdf71d734c5514ea4c10f96be"
)
SOURCE_ADDITION_PROOF_SHA256 = (
    "c985ce0a602a91a0d323594e3aeecf210fa5131027ef4b6c9b6e4d4b628f1848"
)
DRAT_TRIM_SHA256 = (
    "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
)
CADICAL_SHA256 = (
    "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run(
    command: list[str],
    *,
    timeout: int = 600,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
        check=False,
    )


class Formula:
    """Independent exact reconstruction, including production variable order."""

    def __init__(
        self,
        *,
        include_theta_gap: bool = True,
        include_label10_cut: bool = True,
    ) -> None:
        self.vertices = tuple(range(N))
        self.pairs = tuple(itertools.combinations(self.vertices, 2))
        self.triples = tuple(itertools.combinations(self.vertices, 3))
        self.next_variable = 1
        self.edge = self.allocate(self.pairs)
        self.witness = self.allocate(
            (u, v, w)
            for u, v in self.pairs
            for w in self.vertices
            if w not in (u, v)
        )
        self.family = self.allocate(self.triples)
        self.move = self.allocate(
            (state, attacked, guard)
            for state in self.triples
            for attacked in self.vertices
            if attacked not in state
            for guard in state
        )
        self.clauses: list[tuple[int, ...]] = []
        self.categories: dict[str, int] = {}
        self.include_theta_gap = include_theta_gap
        self.include_label10_cut = include_label10_cut
        self.build()

    def allocate(self, keys: Iterable[object]) -> dict[object, int]:
        result: dict[object, int] = {}
        for key in keys:
            result[key] = self.next_variable
            self.next_variable += 1
        return result

    @property
    def variable_count(self) -> int:
        return self.next_variable - 1

    def e(self, u: int, v: int) -> int:
        return self.edge[(u, v) if u < v else (v, u)]

    def f(self, state: Iterable[int]) -> int:
        return self.family[tuple(sorted(state))]

    def add(self, category: str, *literals: int) -> None:
        if not literals or 0 in literals:
            raise AssertionError("malformed clean-room clause")
        self.clauses.append(tuple(literals))
        self.categories[category] = self.categories.get(category, 0) + 1

    def direct(self, target: int, omitted_anchor: int) -> int:
        return self.f(
            (set(ANCHORS) - {omitted_anchor}) | {target}
        )

    def build(self) -> None:
        # edge=true means adjacency in H=complement(G).
        # alpha(G)<=3 is the assertion that H has no K4.
        for four in itertools.combinations(self.vertices, 4):
            self.add(
                "no_H_K4",
                *(
                    -self.e(u, v)
                    for u, v in itertools.combinations(four, 2)
                ),
            )

        # gamma(G)>=3: every pair has an outside common neighbor in H.
        for u, v in self.pairs:
            choices = tuple(w for w in self.vertices if w not in (u, v))
            self.add(
                "pair_witness_choice",
                *(self.witness[(u, v, w)] for w in choices),
            )
            for w in choices:
                selector = self.witness[(u, v, w)]
                self.add(
                    "pair_witness_edge",
                    -selector,
                    self.e(u, w),
                )
                self.add(
                    "pair_witness_edge",
                    -selector,
                    self.e(v, w),
                )

        # Every retained triple dominates G.
        for state in self.triples:
            selected = self.family[state]
            for target in self.vertices:
                if target not in state:
                    self.add(
                        "selected_state_dominates",
                        -selected,
                        *(-self.e(target, guard) for guard in state),
                    )

        # Nonemptiness is redundant after the anchor-state unit but retained
        # to reproduce the production bytes.
        self.add(
            "family_nonempty",
            *(self.family[state] for state in self.triples),
        )

        # Literal one-guard closure.  Auxiliary move variables witness one
        # guard moving along a G-edge to the unoccupied attacked vertex.
        for state in self.triples:
            selected = self.family[state]
            for attacked in self.vertices:
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
                        "move_reaches_retained_state",
                        -move,
                        self.family[successor],
                    )
                self.add(
                    "selected_state_has_response",
                    -selected,
                    *replies,
                )

        # S is an independent retained triple.
        for u, v in itertools.combinations(ANCHORS, 2):
            self.add("anchor_H_triangle", self.e(u, v))
        self.add("anchor_state_retained", self.family[ANCHORS])

        # H is not 3-colorable.  Since S is an H-triangle, every proper
        # 3-coloring can be color-permuted so anchors 0,1,2 have those colors.
        if self.include_theta_gap:
            for tail in itertools.product(range(3), repeat=N - 3):
                colors = ANCHORS + tail
                self.add(
                    "anchored_non_3_coloring",
                    *(
                        self.e(u, v)
                        for u, v in self.pairs
                        if colors[u] == colors[v]
                    ),
                )

        # No outside target has all three direct successor states retained.
        for target in OUTSIDE:
            self.add(
                "no_full_target",
                *(-self.direct(target, anchor) for anchor in ANCHORS),
            )

        def fix_signature(vertex: int, signature: frozenset[int]) -> None:
            for anchor in ANCHORS:
                self.add(
                    "named_signature",
                    (
                        self.e(anchor, vertex)
                        if anchor in signature
                        else -self.e(anchor, vertex)
                    ),
                )

        def fix_list(vertex: int, response: frozenset[int]) -> None:
            for anchor in ANCHORS:
                state = self.direct(vertex, anchor)
                self.add(
                    "named_exact_response_list",
                    state if anchor in response else -state,
                )

        # Two distinct response types, normalized by the anchor S_3 action.
        # Each exact representative has a same-signature H-neighbor.
        fix_signature(3, frozenset((0,)))
        fix_signature(4, frozenset((0,)))
        fix_list(3, frozenset((1, 2)))
        self.add("named_pure_pair_edge", self.e(3, 4))

        fix_signature(5, frozenset((2,)))
        fix_signature(6, frozenset((2,)))
        fix_list(5, frozenset((0, 1)))
        self.add("named_pure_pair_edge", self.e(5, 6))

        # The six unnamed vertices are freely relabelable.  Forbid every
        # adjacent descent of their three-bit anchor signatures.
        for left, right in zip(RESIDUAL[:-1], RESIDUAL[1:], strict=True):
            for left_signature in range(8):
                for right_signature in range(left_signature):
                    forbidden_assignment_clause: list[int] = []
                    for bit, anchor in enumerate(ANCHORS):
                        left_bit = (left_signature >> bit) & 1
                        right_bit = (right_signature >> bit) & 1
                        forbidden_assignment_clause.append(
                            -self.e(left, anchor)
                            if left_bit
                            else self.e(left, anchor)
                        )
                        forbidden_assignment_clause.append(
                            -self.e(right, anchor)
                            if right_bit
                            else self.e(right, anchor)
                        )
                    self.add(
                        "residual_signature_sort",
                        *forbidden_assignment_clause,
                    )

        # With nondecreasing signatures, at most three zero signatures are
        # equivalent to the fourth residual vertex having nonzero signature.
        if self.include_label10_cut:
            self.add(
                "at_most_three_neutral_residual",
                *(self.e(anchor, 10) for anchor in ANCHORS),
            )

    def dimacs(self) -> bytes:
        header = f"p cnf {self.variable_count} {len(self.clauses)}\n"
        body = "".join(
            " ".join(map(str, clause)) + " 0\n" for clause in self.clauses
        )
        return (header + body).encode("ascii")


def parse_dimacs(data: bytes) -> tuple[int, list[tuple[int, ...]]]:
    lines = data.decode("ascii").splitlines()
    if not lines or len(lines[0].split()) != 4:
        raise AssertionError("malformed DIMACS header")
    marker, kind, variable_text, clause_text = lines[0].split()
    if (marker, kind) != ("p", "cnf"):
        raise AssertionError("wrong DIMACS header")
    variables = int(variable_text)
    expected_clauses = int(clause_text)
    clauses: list[tuple[int, ...]] = []
    for line in lines[1:]:
        fields = tuple(map(int, line.split()))
        if not fields or fields[-1] != 0 or 0 in fields[:-1]:
            raise AssertionError("malformed clause")
        clauses.append(fields[:-1])
    if len(clauses) != expected_clauses:
        raise AssertionError("clause-count mismatch")
    return variables, clauses


def proof_shape(data: bytes) -> dict[str, object]:
    lines = data.decode("ascii").splitlines()
    deletion_lines = sum(line.startswith("d ") for line in lines)
    return {
        "line_count": len(lines),
        "deletion_lines": deletion_lines,
        "addition_only": deletion_lines == 0,
        "terminal_empty_clause": bool(lines) and lines[-1] == "0",
    }


def closure_auxiliary_truth_table() -> dict[str, object]:
    """Existentially eliminate move bits and compare with intended closure."""

    failures: list[dict[str, object]] = []
    tested = 0
    for values in itertools.product((False, True), repeat=7):
        selected = values[0]
        h_edges = values[1:4]
        successors = values[4:7]
        intended = (not selected) or any(
            (not h_edges[index]) and successors[index]
            for index in range(3)
        )
        encoded_exists = False
        for moves in itertools.product((False, True), repeat=3):
            clauses_hold = all(
                (not moves[index] or not h_edges[index])
                and (not moves[index] or successors[index])
                for index in range(3)
            )
            clauses_hold = clauses_hold and (
                (not selected) or any(moves)
            )
            if clauses_hold:
                encoded_exists = True
                break
        tested += 1
        if intended != encoded_exists:
            failures.append(
                {
                    "selected": selected,
                    "h_edges": h_edges,
                    "successors": successors,
                }
            )
    return {
        "assignments_tested": tested,
        "failure_count": len(failures),
        "exact": not failures,
        "first_failure": failures[0] if failures else None,
    }


def signature_sort_truth_table() -> dict[str, object]:
    failures = 0
    for left in range(8):
        for right in range(8):
            clauses_hold = True
            for forbidden_left in range(8):
                for forbidden_right in range(forbidden_left):
                    clause_hold = not (
                        left == forbidden_left
                        and right == forbidden_right
                    )
                    clauses_hold = clauses_hold and clause_hold
            if clauses_hold != (left <= right):
                failures += 1
    return {
        "signature_pairs_tested": 64,
        "failure_count": failures,
        "exact_nondecreasing": failures == 0,
    }


def coverage_truth_tables() -> dict[str, object]:
    permutations = tuple(itertools.permutations(ANCHORS))
    ordered_type_pairs = tuple(
        (left, right)
        for left in ANCHORS
        for right in ANCHORS
        if left != right
    )
    pair_normalization = all(
        any(
            permutation[left] == 0 and permutation[right] == 2
            for permutation in permutations
        )
        for left, right in ordered_type_pairs
    )

    sorted_signature_sequences = tuple(
        itertools.combinations_with_replacement(range(8), len(RESIDUAL))
    )
    neutral_cut_exact = all(
        ((sequence[3] != 0) == (sequence.count(0) <= 3))
        for sequence in sorted_signature_sequences
    )
    return {
        "ordered_distinct_type_pairs": len(ordered_type_pairs),
        "anchor_permutations": len(permutations),
        "every_type_pair_normalizes_to_0_and_2": pair_normalization,
        "sorted_residual_signature_sequences": len(
            sorted_signature_sequences
        ),
        "label10_nonzero_exactly_at_most_three_neutral": neutral_cut_exact,
    }


def strict_replay(
    instance: Path,
    proof: Path,
    drat_trim: Path,
    *,
    warnings_fatal: bool,
    plain_mode: bool = False,
) -> dict[str, object]:
    command = [
        str(drat_trim),
        str(instance),
        str(proof),
        "-I",
        "-f",
    ]
    if warnings_fatal:
        command.append("-W")
    if plain_mode:
        command.append("-p")
    command.extend(["-U", "-t", "600"])
    completed = run(
        command,
        timeout=660,
    )
    combined = completed.stdout + completed.stderr
    return {
        "exit": completed.returncode,
        "verified_exactly_once": combined.count("s VERIFIED") == 1,
        "zero_RAT_lemmas": "0 RAT lemmas in core" in combined,
        "warning_count": combined.upper().count("WARNING"),
        "warnings_fatal": warnings_fatal,
        "plain_mode": plain_mode,
        "tail": combined.splitlines()[-12:],
    }


def model_from_solver(stdout: str) -> dict[int, bool]:
    assignment: dict[int, bool] = {}
    for line in stdout.splitlines():
        if not line.startswith("v "):
            continue
        for literal in map(int, line.split()[1:]):
            if literal:
                assignment[abs(literal)] = literal > 0
    return assignment


def model_satisfies(
    clauses: list[tuple[int, ...]],
    assignment: dict[int, bool],
) -> bool:
    return bool(assignment) and all(
        any(
            assignment.get(abs(literal), False) == (literal > 0)
            for literal in clause
        )
        for clause in clauses
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()

    review = Path(__file__).resolve().parent
    campaign = review.parents[1]
    source = campaign / "math/working/order13_no_full_a7_structured"
    tools = campaign / "tools"
    drat_trim = tools / "drat_trim_2023_05_22/drat-trim"
    cadical = tools / "cadical_3_0_1/build/cadical"
    tool_checks = {
        "drat_trim_hash_pinned": sha256_file(drat_trim)
        == DRAT_TRIM_SHA256,
        "cadical_hash_pinned": sha256_file(cadical) == CADICAL_SHA256,
    }

    formula = Formula()
    reconstructed = formula.dimacs()
    instance = source / "instance.cnf"
    duplicate_instance = source / "instance-proof.cnf"
    raw_proof = source / "proof.drat"
    addition_proof = source / "proof.additions.drat"
    source_bytes = instance.read_bytes()
    variables, clauses = parse_dimacs(source_bytes)

    used = {
        abs(literal)
        for clause in clauses
        for literal in clause
    }
    source_checks = {
        "search_hash_pinned": sha256_file(source / "search.py")
        == SOURCE_SEARCH_SHA256,
        "instance_hash_pinned": sha256_file(instance)
        == SOURCE_INSTANCE_SHA256,
        "byte_identical_clean_room_reconstruction": source_bytes
        == reconstructed,
        "duplicate_instance_byte_identical": source_bytes
        == duplicate_instance.read_bytes(),
        "variables_9802": variables == formula.variable_count == 9802,
        "clauses_84614": len(clauses) == len(formula.clauses) == 84614,
        "no_duplicate_clauses": len(set(clauses)) == len(clauses),
        "no_tautologies": all(
            not any(-literal in clause for literal in clause)
            for clause in clauses
        ),
        "all_variables_in_range": all(
            1 <= abs(literal) <= variables
            for clause in clauses
            for literal in clause
        ),
        "all_variables_used": used == set(range(1, variables + 1)),
    }

    raw_shape = proof_shape(raw_proof.read_bytes())
    addition_shape = proof_shape(addition_proof.read_bytes())
    raw_without_deletions = b"".join(
        line
        for line in raw_proof.read_bytes().splitlines(keepends=True)
        if not line.startswith(b"d ")
    )
    proof_checks = {
        "raw": {
            "sha256": sha256_file(raw_proof),
            "bytes": raw_proof.stat().st_size,
            "hash_pinned": sha256_file(raw_proof)
            == SOURCE_RAW_PROOF_SHA256,
            "shape": raw_shape,
            "replay_honoring_deletions": strict_replay(
                instance,
                raw_proof,
                drat_trim,
                warnings_fatal=False,
            ),
            "replay_plain_warning_fatal": strict_replay(
                instance,
                raw_proof,
                drat_trim,
                warnings_fatal=True,
                plain_mode=True,
            ),
        },
        "addition_only": {
            "sha256": sha256_file(addition_proof),
            "bytes": addition_proof.stat().st_size,
            "hash_pinned": sha256_file(addition_proof)
            == SOURCE_ADDITION_PROOF_SHA256,
            "shape": addition_shape,
            "exactly_raw_trace_with_deletions_removed": (
                raw_without_deletions == addition_proof.read_bytes()
            ),
            "replay": strict_replay(
                instance,
                addition_proof,
                drat_trim,
                warnings_fatal=True,
            ),
        },
    }

    # Positive ablation: dropping theta>3 should admit many equality graphs.
    # This checks that UNSAT is not caused solely by an accidental
    # contradiction in the structural normalization.
    theta_ablation = Formula(include_theta_gap=False)
    with tempfile.TemporaryDirectory(prefix="a7-hostile-control-") as raw:
        control_path = Path(raw) / "control.cnf"
        control_path.write_bytes(theta_ablation.dimacs())
        control_run = run(
            [str(cadical), "--quiet", str(control_path)],
            timeout=300,
        )
        _, control_clauses = parse_dimacs(theta_ablation.dimacs())
        assignment = model_from_solver(control_run.stdout)
        control = {
            "solver_exit": control_run.returncode,
            "reported_SAT": "s SATISFIABLE" in control_run.stdout,
            "model_satisfies_every_clause": model_satisfies(
                control_clauses, assignment
            ),
            "instance_sha256": sha256_bytes(theta_ablation.dimacs()),
            "variables": theta_ablation.variable_count,
            "clauses": len(theta_ablation.clauses),
        }

    local_checks = {
        "closure": closure_auxiliary_truth_table(),
        "signature_sort": signature_sort_truth_table(),
        "coverage": coverage_truth_tables(),
    }

    raw_replay_ok = all(
        replay["exit"] == 0
        and replay["verified_exactly_once"]
        and replay["zero_RAT_lemmas"]
        for replay in (
            proof_checks["raw"]["replay_honoring_deletions"],
            proof_checks["raw"]["replay_plain_warning_fatal"],
        )
    )
    addition_replay = proof_checks["addition_only"]["replay"]
    replay_ok = (
        raw_replay_ok
        and addition_replay["exit"] == 0
        and addition_replay["verified_exactly_once"]
        and addition_replay["zero_RAT_lemmas"]
        and proof_checks["raw"]["hash_pinned"]
        and proof_checks["addition_only"]["hash_pinned"]
    ) and proof_checks["addition_only"][
        "exactly_raw_trace_with_deletions_removed"
    ]
    verdict = (
        "PASS"
        if all(source_checks.values())
        and all(tool_checks.values())
        and addition_shape["addition_only"]
        and raw_shape["terminal_empty_clause"]
        and addition_shape["terminal_empty_clause"]
        and proof_checks["addition_only"]["replay"]["warning_count"] == 0
        and replay_ok
        and local_checks["closure"]["exact"]
        and local_checks["signature_sort"]["exact_nondecreasing"]
        and all(local_checks["coverage"].values())
        and control["reported_SAT"]
        and control["model_satisfies_every_clause"]
        else "FAIL"
    )

    result = {
        "verdict": verdict,
        "source": {
            "instance_sha256": sha256_file(instance),
            "instance_bytes": instance.stat().st_size,
            "checks": source_checks,
            "formula_categories": formula.categories,
        },
        "tools": tool_checks,
        "proofs": proof_checks,
        "local_semantics": local_checks,
        "theta_gap_ablation_control": control,
        "claim_scope": {
            "conditional_inputs": [
                "C-090 excludes the complementary full-family-response branch",
                "C-093 gives at least two exact two-list types when theta(G)>3",
                "C-093/C-091 give a pure-signature representative and a "
                "same-signature H-neighbor for each occurring type",
                "the separately certified four-neutral/two-port obstruction "
                "implies at most three neutral vertices",
            ],
            "certified_conclusion_if_inputs_accepted": (
                "No 13-vertex graph satisfies "
                "gamma(G)=alpha(G)=gamma_infinity(G)=3<theta(G)."
            ),
            "not_claimed": [
                "the universal gamma-theta conjecture",
                "the complete k=3 case at arbitrary order",
                "any k=4 or larger order-13 slice",
            ],
        },
    }
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.result is not None:
        args.result.write_text(output, encoding="utf-8")
    print(output, end="")
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
