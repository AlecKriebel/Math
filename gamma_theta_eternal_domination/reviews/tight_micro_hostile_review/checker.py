#!/usr/bin/env python3
"""Clean-room audit of the order-13 neutral-port obstruction.

This file deliberately imports neither discovery generator.  It reconstructs
the graph/family CNF from its mathematical semantics, checks the local closure
gadget by a complete truth table, and replays the retained proof through both
strict RUP-only DRAT checking and a fresh LRAT conversion/check.

The production certificate has four neutral vertices, only positive response
incidences, and no redundant alpha block.
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
PORTS = (
    (3, frozenset((0, 2))),
    (5, frozenset((0, 1))),
)

SOURCE_INSTANCE_SHA256 = (
    "3d1a1379eb2a90ffd399e5a830b1a81881ed527c6e9db06574a390085cb5c1e0"
)
SOURCE_PROOF_SHA256 = (
    "c4f1989ac80474a86b75ba939e494bde5928b2727fd61297eb695f3937222eee"
)
DRAT_TRIM_SHA256 = (
    "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
)
LRAT_CHECK_SHA256 = (
    "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2"
)
CADICAL_SHA256 = (
    "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes())


def run(
    command: list[str],
    *,
    timeout: int = 120,
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
    """Formula plus its clean-room variable maps and clause categories."""

    def __init__(
        self,
        neutral_count: int,
        *,
        include_k4_block: bool = False,
        exact_port_lists: bool = False,
    ) -> None:
        if not 0 <= neutral_count <= 5:
            raise ValueError("neutral_count must be between zero and five")
        self.neutral_count = neutral_count
        self.include_k4_block = include_k4_block
        self.exact_port_lists = exact_port_lists
        self.vertices = tuple(range(N))
        self.pairs = tuple(itertools.combinations(self.vertices, 2))
        self.triples = tuple(itertools.combinations(self.vertices, 3))
        self.next_variable = 1
        self.edge = self._allocate(self.pairs)
        self.family = self._allocate(self.triples)
        witness_keys = (
            (u, v, w)
            for u, v in self.pairs
            for w in self.vertices
            if w not in (u, v)
        )
        self.witness = self._allocate(witness_keys)
        self.clauses: list[tuple[int, ...]] = []
        self.categories: dict[str, int] = {}
        self._build()

    def _allocate(self, keys: Iterable[object]) -> dict[object, int]:
        result: dict[object, int] = {}
        for key in keys:
            result[key] = self.next_variable
            self.next_variable += 1
        return result

    def e(self, u: int, v: int) -> int:
        return self.edge[(u, v) if u < v else (v, u)]

    def add(self, category: str, *literals: int) -> None:
        if not literals or 0 in literals:
            raise AssertionError("malformed clean-room clause")
        self.clauses.append(tuple(literals))
        self.categories[category] = self.categories.get(category, 0) + 1

    def _build(self) -> None:
        # Optional redundant alpha(G) <= 3 block.  Production omits it:
        # an eternal triple-family already implies alpha(G) <= 3.
        if self.include_k4_block:
            for four in itertools.combinations(self.vertices, 4):
                self.add(
                    "no_H_K4",
                    *(
                        -self.e(u, v)
                        for u, v in itertools.combinations(four, 2)
                    ),
                )

        # gamma(G) >= 3: every pair misses a common vertex in G, equivalently
        # every pair has an open common neighbor in H.  Selectors are only
        # one-way witnesses; their at-least-one clause makes the encoding exact.
        for u, v in self.pairs:
            outside = tuple(w for w in self.vertices if w not in (u, v))
            self.add(
                "pair_witness_choice",
                *(self.witness[(u, v, w)] for w in outside),
            )
            for w in outside:
                selector = self.witness[(u, v, w)]
                self.add("pair_witness_edge", -selector, self.e(u, w))
                self.add("pair_witness_edge", -selector, self.e(v, w))

        # F-state closure.  If D is selected and r is unoccupied, at least one
        # guard g must simultaneously have gr in G and have D-g+r selected.
        # Distributing the OR of three two-literal conjunctions yields exactly
        # eight clauses.
        for state in self.triples:
            selected = self.family[state]
            for attacked in self.vertices:
                if attacked in state:
                    continue
                response_pairs: list[tuple[int, int]] = []
                for guard in state:
                    successor = tuple(
                        sorted((set(state) - {guard}) | {attacked})
                    )
                    response_pairs.append(
                        (-self.e(guard, attacked), self.family[successor])
                    )
                for choices in itertools.product(*response_pairs):
                    self.add("one_guard_closure", -selected, *choices)

        # S is an independent retained state.
        for u, v in itertools.combinations(ANCHORS, 2):
            self.add("anchor_independence", self.e(u, v))
        self.add("anchor_retained", self.family[ANCHORS])

        # Neutral means no H edge to an anchor, i.e. G-complete to S.
        for q in range(8, 8 + self.neutral_count):
            for anchor in ANCHORS:
                self.add("neutral_signature", -self.e(anchor, q))

        # Production requires only the two positive responses at each port.
        # The independent restrictive control also fixes the third response
        # absent, thereby making each list exact.
        for vertex, response in PORTS:
            for anchor in ANCHORS:
                if not self.exact_port_lists and anchor not in response:
                    continue
                successor = tuple(
                    sorted((set(ANCHORS) - {anchor}) | {vertex})
                )
                literal = self.family[successor]
                self.add(
                    (
                        "exact_port_list"
                        if self.exact_port_lists
                        else "positive_port_response"
                    ),
                    literal if anchor in response else -literal,
                )

    @property
    def variable_count(self) -> int:
        return self.next_variable - 1

    def dimacs(self) -> bytes:
        header = f"p cnf {self.variable_count} {len(self.clauses)}\n"
        body = "".join(
            " ".join(map(str, clause)) + " 0\n" for clause in self.clauses
        )
        return (header + body).encode("ascii")


def closure_truth_table() -> dict[str, int | bool]:
    """Check the eight-clause gadget against the intended Boolean formula."""

    tested = 0
    failures = 0
    for bits in itertools.product((False, True), repeat=7):
        selected = bits[0]
        edge_h = bits[1:4]
        successor = bits[4:7]
        intended = (not selected) or any(
            (not edge_h[index]) and successor[index] for index in range(3)
        )
        encoded = True
        pairs = tuple(
            ((not edge_h[index]), successor[index]) for index in range(3)
        )
        for choices in itertools.product((0, 1), repeat=3):
            clause = (not selected) or any(
                pairs[index][choices[index]] for index in range(3)
            )
            encoded = encoded and clause
        tested += 1
        if encoded != intended:
            failures += 1
    return {
        "assignments_tested": tested,
        "failures": failures,
        "exact": failures == 0,
    }


def parse_dimacs(data: bytes) -> tuple[int, list[tuple[int, ...]]]:
    lines = data.decode("ascii").splitlines()
    if not lines or not lines[0].startswith("p cnf "):
        raise AssertionError("missing DIMACS header")
    fields = lines[0].split()
    variables = int(fields[2])
    expected_clauses = int(fields[3])
    clauses: list[tuple[int, ...]] = []
    for line in lines[1:]:
        values = tuple(map(int, line.split()))
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise AssertionError("malformed DIMACS clause")
        clauses.append(values[:-1])
    if len(clauses) != expected_clauses:
        raise AssertionError("DIMACS clause count mismatch")
    return variables, clauses


def proof_is_addition_only(data: bytes) -> tuple[bool, int, bool]:
    lines = data.decode("ascii").splitlines()
    return (
        all(line and not line.startswith("d ") for line in lines),
        len(lines),
        bool(lines) and lines[-1] == "0",
    )


def validate_model(clauses: list[tuple[int, ...]], stdout: str) -> bool:
    assignments: dict[int, bool] = {}
    for line in stdout.splitlines():
        if not line.startswith("v "):
            continue
        for literal in map(int, line.split()[1:]):
            if literal == 0:
                continue
            assignments[abs(literal)] = literal > 0
    if not assignments:
        return False
    return all(
        any(assignments.get(abs(literal), False) == (literal > 0) for literal in clause)
        for clause in clauses
    )


def strict_replay(
    *,
    instance: Path,
    proof: Path,
    drat_trim: Path,
    lrat_check: Path,
    negative_instance_data: bytes,
) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="tight-micro-review-") as raw:
        temporary = Path(raw)
        lrat = temporary / "fresh.lrat"
        negative_instance = temporary / "satisfiable-ablation.cnf"
        negative_instance.write_bytes(negative_instance_data)
        forward = run(
            [
                str(drat_trim),
                str(instance),
                str(proof),
                "-I",
                "-f",
                "-W",
                "-U",
                "-t",
                "120",
            ]
        )
        convert = run(
            [
                str(drat_trim),
                str(instance),
                str(proof),
                "-I",
                "-W",
                "-U",
                "-L",
                str(lrat),
                "-t",
                "120",
            ]
        )
        lrat_result = run(
            [str(lrat_check), str(instance), str(lrat)],
            timeout=120,
        )

        # The proof must fail on the satisfiable three-neutral ablation.
        mutation = run(
            [
                str(drat_trim),
                str(negative_instance),
                str(proof),
                "-I",
                "-f",
                "-W",
                "-U",
                "-t",
                "120",
            ]
        )

        return {
            "forward_rup_exit": forward.returncode,
            "forward_rup_verified": forward.stdout.count("s VERIFIED") == 1,
            "forward_rup_zero_rat": "0 RAT lemmas in core" in forward.stdout,
            "drat_to_lrat_exit": convert.returncode,
            "drat_to_lrat_verified": convert.stdout.count("s VERIFIED") == 1,
            "drat_to_lrat_zero_rat": "0 RAT lemmas in core" in convert.stdout,
            "fresh_lrat_bytes": lrat.stat().st_size if lrat.exists() else 0,
            "fresh_lrat_sha256": file_sha256(lrat) if lrat.exists() else None,
            "lrat_check_exit": lrat_result.returncode,
            "lrat_check_verified": lrat_result.stdout.count("c VERIFIED") == 1,
            "lrat_check_stderr_empty": not lrat_result.stderr,
            "sat_ablation_rejects_unsat_proof": (
                mutation.returncode != 0
                or mutation.stdout.count("s VERIFIED") != 1
            ),
            "forward_stdout_tail": forward.stdout.splitlines()[-8:],
            "converter_stdout_tail": convert.stdout.splitlines()[-8:],
            "lrat_stdout": lrat_result.stdout.splitlines(),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()

    review = Path(__file__).resolve().parent
    campaign = review.parents[1]
    source = campaign / "math/working/order13_no_full_tight_five_five"
    tools = campaign / "tools"
    drat_trim = tools / "drat_trim_2023_05_22/drat-trim"
    lrat_check = tools / "drat_trim_2023_05_22/lrat-check"
    cadical = tools / "cadical_3_0_1/build/cadical"

    pinned_tools = {
        "drat_trim": file_sha256(drat_trim) == DRAT_TRIM_SHA256,
        "lrat_check": file_sha256(lrat_check) == LRAT_CHECK_SHA256,
        "cadical": file_sha256(cadical) == CADICAL_SHA256,
    }
    if not all(pinned_tools.values()):
        raise AssertionError("a proof tool does not match its pinned hash")

    production = Formula(neutral_count=4)
    reconstructed = production.dimacs()
    source_instance = source / "micro-instance.cnf"
    source_proof = source / "micro-proof.additions.drat"
    source_bytes = source_instance.read_bytes()
    proof_bytes = source_proof.read_bytes()
    variables, parsed_clauses = parse_dimacs(source_bytes)
    additions, proof_lines, terminal_empty = proof_is_addition_only(proof_bytes)

    source_checks = {
        "byte_identical_clean_room_reconstruction": source_bytes == reconstructed,
        "instance_hash_pinned": file_sha256(source_instance)
        == SOURCE_INSTANCE_SHA256,
        "proof_hash_pinned": file_sha256(source_proof) == SOURCE_PROOF_SHA256,
        "variables": variables == 1222 == production.variable_count,
        "clauses": len(parsed_clauses) == 24694 == len(production.clauses),
        "no_duplicate_clauses": len(set(parsed_clauses)) == len(parsed_clauses),
        "no_tautologies": all(
            not any(-literal in clause for literal in clause)
            for clause in parsed_clauses
        ),
        "all_variables_in_range": all(
            1 <= abs(literal) <= variables
            for clause in parsed_clauses
            for literal in clause
        ),
        "addition_only_proof": additions,
        "proof_line_count": proof_lines == 78697,
        "proof_terminal_empty_clause": terminal_empty,
    }
    source_replay = strict_replay(
        instance=source_instance,
        proof=source_proof,
        drat_trim=drat_trim,
        lrat_check=lrat_check,
        negative_instance_data=Formula(neutral_count=3).dimacs(),
    )

    # Boundary control: with the same two ports but only three named
    # neutral vertices, the independently generated formula is satisfiable.
    q3 = Formula(neutral_count=3)
    with tempfile.TemporaryDirectory(prefix="tight-micro-q3-") as raw:
        q3_path = Path(raw) / "q3.cnf"
        q3_path.write_bytes(q3.dimacs())
        q3_solver = run([str(cadical), "--quiet", str(q3_path)], timeout=120)
        _, q3_clauses = parse_dimacs(q3.dimacs())
        q3_control = {
            "solver_exit": q3_solver.returncode,
            "reported_sat": "s SATISFIABLE" in q3_solver.stdout,
            "model_satisfies_every_clause": validate_model(
                q3_clauses, q3_solver.stdout
            ),
        }

    truth_table = closure_truth_table()
    source_replay_ok = all(
        (
            source_replay["drat_to_lrat_exit"] == 0,
            source_replay["forward_rup_exit"] == 0,
            source_replay["forward_rup_verified"],
            source_replay["forward_rup_zero_rat"],
            source_replay["drat_to_lrat_verified"],
            source_replay["drat_to_lrat_zero_rat"],
            source_replay["lrat_check_exit"] == 0,
            source_replay["lrat_check_verified"],
            source_replay["lrat_check_stderr_empty"],
            source_replay["sat_ablation_rejects_unsat_proof"],
        )
    )
    verdict = (
        "PASS"
        if all(source_checks.values())
        and source_replay_ok
        and truth_table["exact"]
        and all(q3_control.values())
        else "FAIL"
    )

    result = {
        "verdict": verdict,
        "source_four_neutral_positive_ports": {
            "checks": source_checks,
            "instance_sha256": file_sha256(source_instance),
            "proof_sha256": file_sha256(source_proof),
            "formula_categories": production.categories,
            "replay": source_replay,
        },
        "three_neutral_positive_control": q3_control,
        "closure_gadget_truth_table": truth_table,
        "tool_hashes_pinned": pinned_tools,
        "scope": {
            "proved_by_q4_certificate": (
                "No 13-vertex graph G with gamma=alpha=gamma_infinity=3, "
                "an independent retained triple S, four distinct vertices "
                "G-complete to S, and two further distinct vertices with "
                "response lists containing {h,j} and {h,i}, respectively."
            ),
            "not_imposed": [
                "theta(G)>3",
                "connectedness",
                "no-full response lists",
                "anchor signatures of the two ports",
                "greatest-family status",
            ],
        },
    }
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.result:
        args.result.write_text(output, encoding="utf-8")
    print(output, end="")
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
