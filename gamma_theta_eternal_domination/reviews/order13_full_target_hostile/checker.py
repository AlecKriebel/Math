#!/usr/bin/env python3
"""Clean-room audit for the order-13, k=3 full-response exclusion.

This program intentionally does not import the discovery generator.  It
reconstructs the SAT instance directly from the mathematical definition,
checks its binding to the frozen DIMACS and DRAT artifacts, truth-tables the
signature sorter, and independently checks the retained positive control.
"""

from __future__ import annotations

import collections
import hashlib
import itertools
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable


ORDER = 13
ANCHORS = (0, 1, 2)
FULL_TARGET = 3
VERTICES = tuple(range(ORDER))
TRIPLES = tuple(itertools.combinations(VERTICES, 3))

HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
SOURCE = CAMPAIGN / "math" / "working" / "order13_single_full_squeeze"
DRAT_TRIM = CAMPAIGN / "tools" / "drat_trim_2023_05_22" / "drat-trim"
CADICAL = CAMPAIGN / "tools" / "cadical_3_0_1" / "build" / "cadical"

EXPECTED_HASHES = {
    "minimal-instance.cnf":
        "d5a2f17ad6e61cb7ca5cb9d2930b6a0738fec32ee1d9956207dc67bb297dcb13",
    "minimal-proof.drat":
        "653b01e904b97c01bfa25fbbea29fbadee603918dbaff0ea41b7ad09460fb910",
    "minimal-core.cnf":
        "dcba47ea9d60afc1cc86672498af39681c3acf02606c728f66cb84f47ee557e7",
    "minimal-core.drat":
        "83f73ee2c2a82ab0a228099f0354abf46e23f3e807561a6d665a43b86b1e273f",
    "positive-model.out":
        "91ed17277bfd4405f7e1dfdecc199bed2f9cdc788f1c59a15e7d3a55e8f79d8d",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canon_pair(a: int, b: int) -> tuple[int, int]:
    assert a != b
    return (a, b) if a < b else (b, a)


class CleanEncoding:
    """Declarative reconstruction with an explicit, audited variable map."""

    def __init__(self) -> None:
        self.next_variable = 1
        self.edge: dict[tuple[int, int], int] = {}
        self.pair_witness: dict[tuple[int, int, int], int] = {}
        self.retained: dict[tuple[int, int, int], int] = {}
        self.response: dict[
            tuple[tuple[int, int, int], int, int], int
        ] = {}
        self.clauses: list[tuple[int, ...]] = []
        self.tags: list[str] = []
        self._allocate_variables()

    def _fresh(self) -> int:
        answer = self.next_variable
        self.next_variable += 1
        return answer

    def _allocate_variables(self) -> None:
        # Natural lexicographic allocation is stated here independently so a
        # byte-for-byte comparison also audits the frozen proof's variable map.
        for u, v in itertools.combinations(VERTICES, 2):
            self.edge[(u, v)] = self._fresh()
        for u, v in itertools.combinations(VERTICES, 2):
            for witness in VERTICES:
                if witness not in (u, v):
                    self.pair_witness[(u, v, witness)] = self._fresh()
        for state in TRIPLES:
            self.retained[state] = self._fresh()
        for state in TRIPLES:
            for attacked in VERTICES:
                if attacked in state:
                    continue
                for moving_guard in state:
                    self.response[(state, attacked, moving_guard)] = self._fresh()
        assert self.next_variable - 1 == 9802
        assert min(self.edge.values()) == 1
        assert max(self.edge.values()) == 78
        assert min(self.pair_witness.values()) == 79
        assert max(self.pair_witness.values()) == 936
        assert min(self.retained.values()) == 937
        assert max(self.retained.values()) == 1222
        assert min(self.response.values()) == 1223
        assert max(self.response.values()) == 9802

    @property
    def variable_count(self) -> int:
        return self.next_variable - 1

    def h_edge(self, u: int, v: int) -> int:
        return self.edge[canon_pair(u, v)]

    def add(self, tag: str, literals: Iterable[int]) -> None:
        clause = tuple(literals)
        assert clause
        assert all(literal and abs(literal) <= self.variable_count
                   for literal in clause)
        assert not ({*clause} & {-literal for literal in clause})
        self.tags.append(tag)
        self.clauses.append(clause)

    def build(
        self,
        *,
        include_closure: bool = True,
        include_theta_gap: bool = True,
        include_sorter: bool = True,
    ) -> None:
        # alpha(G) <= 3, equivalently H has no K4.
        for four_set in itertools.combinations(VERTICES, 4):
            self.add(
                "no_h_k4",
                (-self.h_edge(u, v)
                 for u, v in itertools.combinations(four_set, 2)),
            )

        # gamma(G) >= 3.  Every pair {u,v} has an outside vertex adjacent
        # to both in H, so no pair dominates G.
        for u, v in itertools.combinations(VERTICES, 2):
            candidates = tuple(w for w in VERTICES if w not in (u, v))
            self.add(
                "pair_witness_choice",
                (self.pair_witness[(u, v, w)] for w in candidates),
            )
            for w in candidates:
                choice = self.pair_witness[(u, v, w)]
                self.add("pair_witness_edge", (-choice, self.h_edge(u, w)))
                self.add("pair_witness_edge", (-choice, self.h_edge(v, w)))

        # Every retained triple dominates G.
        for state in TRIPLES:
            selected = self.retained[state]
            for outside in VERTICES:
                if outside in state:
                    continue
                self.add(
                    "retained_dominates",
                    (
                        -selected,
                        -self.h_edge(outside, state[0]),
                        -self.h_edge(outside, state[1]),
                        -self.h_edge(outside, state[2]),
                    ),
                )

        # Redundant nonemptiness is retained in the frozen instance.  The
        # distinguished anchor state is fixed below.
        self.add("family_nonempty", self.retained.values())

        # Literal one-guard-moves closure.  Attacks are only outside the
        # occupied state.  A response variable can be true only when its one
        # chosen guard traverses a G edge and the resulting triple is retained.
        if include_closure:
            for state in TRIPLES:
                selected = self.retained[state]
                for attacked in VERTICES:
                    if attacked in state:
                        continue
                    possible: list[int] = []
                    for guard in state:
                        response = self.response[(state, attacked, guard)]
                        possible.append(response)
                        successor = tuple(
                            sorted((set(state) - {guard}) | {attacked})
                        )
                        assert len(successor) == 3
                        self.add(
                            "response_traverses_g_edge",
                            (-response, -self.h_edge(guard, attacked)),
                        )
                        self.add(
                            "response_successor_retained",
                            (-response, self.retained[successor]),
                        )
                    self.add(
                        "retained_state_has_response",
                        (-selected, *possible),
                    )

        # S is an independent triple in G, belongs to the family, and x is a
        # full family-response target: all three graph edges and all three
        # one-guard successor states are present.
        for u, v in itertools.combinations(ANCHORS, 2):
            self.add("anchor_h_triangle", (self.h_edge(u, v),))
        self.add("anchor_retained", (self.retained[ANCHORS],))
        for removed_anchor in ANCHORS:
            self.add(
                "full_target_g_edge",
                (-self.h_edge(removed_anchor, FULL_TARGET),),
            )
            successor = tuple(
                sorted(
                    (set(ANCHORS) - {removed_anchor}) | {FULL_TARGET}
                )
            )
            self.add(
                "full_target_successor",
                (self.retained[successor],),
            )

        # theta(G)>3, equivalently H is not 3-colorable.  The H-triangle S
        # can be assigned colors 0,1,2 after permuting color names.  For each
        # of the 3^10 extensions, demand a monochromatic H edge.
        if include_theta_gap:
            for tail in itertools.product(range(3), repeat=ORDER - 3):
                colors = ANCHORS + tail
                self.add(
                    "anchored_noncoloring",
                    (
                        self.h_edge(u, v)
                        for u, v in itertools.combinations(VERTICES, 2)
                        if colors[u] == colors[v]
                    ),
                )

        # Symmetry breaking under S9 on vertices 4,...,12.  Each clause is
        # the negation of one adjacent inversion of the four H-adjacency bits
        # to 0,1,2,3.
        if include_sorter:
            core = (0, 1, 2, 3)
            for left in range(4, ORDER - 1):
                right = left + 1
                for left_signature in range(16):
                    for right_signature in range(left_signature):
                        literals: list[int] = []
                        for bit, core_vertex in enumerate(core):
                            left_bit = (left_signature >> bit) & 1
                            right_bit = (right_signature >> bit) & 1
                            left_edge = self.h_edge(left, core_vertex)
                            right_edge = self.h_edge(right, core_vertex)
                            literals.append(-left_edge if left_bit else left_edge)
                            literals.append(
                                -right_edge if right_bit else right_edge
                            )
                        self.add("signature_sorter", literals)

    def dimacs_bytes(self) -> bytes:
        lines = [
            f"p cnf {self.variable_count} {len(self.clauses)}",
            *(" ".join(map(str, clause)) + " 0" for clause in self.clauses),
        ]
        return ("\n".join(lines) + "\n").encode("ascii")


def parse_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variable_count = -1
    promised_clauses = -1
    clauses: list[tuple[int, ...]] = []
    pending: list[int] = []
    with path.open("rt", encoding="ascii") as stream:
        for line_number, raw in enumerate(stream, 1):
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p "):
                assert variable_count < 0, f"duplicate header at {line_number}"
                words = line.split()
                assert words[:2] == ["p", "cnf"] and len(words) == 4
                variable_count = int(words[2])
                promised_clauses = int(words[3])
                continue
            assert variable_count >= 0, f"clause before header at {line_number}"
            for token in map(int, line.split()):
                if token:
                    assert abs(token) <= variable_count
                    pending.append(token)
                else:
                    assert pending
                    clauses.append(tuple(pending))
                    pending = []
    assert not pending
    assert len(clauses) == promised_clauses
    return variable_count, clauses


def normalized_clause(clause: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(clause, key=lambda literal: (abs(literal), literal < 0)))


def evaluate_clause(clause: tuple[int, ...], assignment: dict[int, bool]) -> bool:
    return any(assignment[abs(lit)] == (lit > 0) for lit in clause)


def parse_model(path: Path, variable_count: int) -> dict[int, bool]:
    signed: list[int] = []
    status = None
    with path.open("rt", encoding="ascii") as stream:
        for raw in stream:
            words = raw.split()
            if not words:
                continue
            if words[:2] == ["s", "SATISFIABLE"]:
                status = "SATISFIABLE"
            elif words[0] == "v":
                signed.extend(int(word) for word in words[1:] if word != "0")
    assert status == "SATISFIABLE"
    assert len(signed) == variable_count
    assert {abs(value) for value in signed} == set(range(1, variable_count + 1))
    return {abs(value): value > 0 for value in signed}


def sorter_truth_table(encoding: CleanEncoding) -> dict[str, int]:
    clauses = [
        clause for tag, clause in zip(encoding.tags, encoding.clauses)
        if tag == "signature_sorter"
    ]
    assert len(clauses) == 960
    edge = encoding.h_edge
    tested = 0
    for adjacent_index, left in enumerate(range(4, ORDER - 1)):
        right = left + 1
        block = clauses[120 * adjacent_index:120 * (adjacent_index + 1)]
        assert len(block) == 120
        for left_signature in range(16):
            for right_signature in range(16):
                assignment: dict[int, bool] = {}
                for bit, core_vertex in enumerate((0, 1, 2, 3)):
                    assignment[edge(left, core_vertex)] = bool(
                        (left_signature >> bit) & 1
                    )
                    assignment[edge(right, core_vertex)] = bool(
                        (right_signature >> bit) & 1
                    )
                allowed = all(evaluate_clause(clause, assignment)
                              for clause in block)
                assert allowed == (left_signature <= right_signature)
                tested += 1
    return {"clauses": len(clauses), "signature_pairs_tested": tested}


def adjacency_from_model(
    encoding: CleanEncoding, assignment: dict[int, bool]
) -> tuple[list[int], list[int]]:
    h_adjacency = [0] * ORDER
    g_adjacency = [0] * ORDER
    for (u, v), variable in encoding.edge.items():
        target = h_adjacency if assignment[variable] else g_adjacency
        target[u] |= 1 << v
        target[v] |= 1 << u
    return g_adjacency, h_adjacency


def dominates(adjacency: list[int], state: tuple[int, ...]) -> bool:
    covered = 0
    for vertex in state:
        covered |= adjacency[vertex] | (1 << vertex)
    return covered == (1 << ORDER) - 1


def exact_domination_number(adjacency: list[int]) -> int:
    for size in range(1, ORDER + 1):
        for state in itertools.combinations(VERTICES, size):
            if dominates(adjacency, state):
                return size
    raise AssertionError("finite graph has no dominating set")


def exact_independence_number(adjacency: list[int]) -> int:
    best = 0
    for mask in range(1 << ORDER):
        size = mask.bit_count()
        if size <= best:
            continue
        independent = True
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            vertex = bit.bit_length() - 1
            remaining ^= bit
            if adjacency[vertex] & remaining:
                independent = False
                break
        if independent:
            best = size
    return best


def three_coloring(adjacency: list[int]) -> list[int] | None:
    """Independent DSATUR-style exact coloring search."""

    colors = [-1] * ORDER
    degrees = [mask.bit_count() for mask in adjacency]

    def recurse(colored: int) -> bool:
        if colored == ORDER:
            return True
        best_vertex = -1
        best_key = (-1, -1)
        for vertex in VERTICES:
            if colors[vertex] >= 0:
                continue
            neighbor_colors = {
                colors[neighbor]
                for neighbor in VERTICES
                if (adjacency[vertex] >> neighbor) & 1
                and colors[neighbor] >= 0
            }
            key = (len(neighbor_colors), degrees[vertex])
            if key > best_key:
                best_key = key
                best_vertex = vertex
        forbidden = {
            colors[neighbor]
            for neighbor in VERTICES
            if (adjacency[best_vertex] >> neighbor) & 1
            and colors[neighbor] >= 0
        }
        for color in range(3):
            if color in forbidden:
                continue
            colors[best_vertex] = color
            if recurse(colored + 1):
                return True
            colors[best_vertex] = -1
        return False

    return colors.copy() if recurse(0) else None


def greatest_eternal_triple_family(adjacency: list[int]) -> set[tuple[int, ...]]:
    family = {state for state in TRIPLES if dominates(adjacency, state)}
    changed = True
    while changed:
        changed = False
        survivors: set[tuple[int, ...]] = set()
        for state in family:
            closed = True
            for attacked in VERTICES:
                if attacked in state:
                    continue
                legal = False
                for guard in state:
                    if not ((adjacency[guard] >> attacked) & 1):
                        continue
                    successor = tuple(
                        sorted((set(state) - {guard}) | {attacked})
                    )
                    if successor in family:
                        legal = True
                        break
                if not legal:
                    closed = False
                    break
            if closed:
                survivors.add(state)
        if survivors != family:
            family = survivors
            changed = True
    return family


def graph6(adjacency: list[int]) -> str:
    assert ORDER <= 62
    bits: list[int] = []
    for column in range(1, ORDER):
        for row in range(column):
            bits.append((adjacency[row] >> column) & 1)
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = sum(bits[start + offset] << (5 - offset)
                    for offset in range(6))
        payload.append(chr(63 + value))
    return chr(63 + ORDER) + "".join(payload)


def audit_positive_control(
    encoding_without_theta: CleanEncoding,
) -> dict[str, object]:
    assignment = parse_model(
        SOURCE / "positive-model.out",
        encoding_without_theta.variable_count,
    )
    failed = [
        index for index, clause in enumerate(
            encoding_without_theta.clauses, start=1
        )
        if not evaluate_clause(clause, assignment)
    ]
    assert not failed

    g_adjacency, h_adjacency = adjacency_from_model(
        encoding_without_theta, assignment
    )
    gamma = exact_domination_number(g_adjacency)
    alpha = exact_independence_number(g_adjacency)
    assert gamma == alpha == 3

    coloring = three_coloring(h_adjacency)
    assert coloring is not None
    # The fixed H triangle proves that two colors do not suffice.
    assert all(
        (h_adjacency[u] >> v) & 1
        for u, v in itertools.combinations(ANCHORS, 2)
    )
    theta = 3

    greatest_family = greatest_eternal_triple_family(g_adjacency)
    assert greatest_family
    dominating_triples = {
        state for state in TRIPLES if dominates(g_adjacency, state)
    }
    assert greatest_family == dominating_triples

    selected_family = {
        state for state, variable in encoding_without_theta.retained.items()
        if assignment[variable]
    }
    assert selected_family
    assert selected_family <= greatest_family

    full_targets = []
    for target in VERTICES:
        if target in ANCHORS:
            continue
        successors = [
            tuple(sorted((set(ANCHORS) - {guard}) | {target}))
            for guard in ANCHORS
        ]
        if (
            all((g_adjacency[guard] >> target) & 1 for guard in ANCHORS)
            and all(successor in greatest_family for successor in successors)
        ):
            full_targets.append(target)
    assert full_targets == [FULL_TARGET]

    return {
        "model_satisfies_clean_theta_ablation_clauses": True,
        "theta_ablation_clause_count": len(encoding_without_theta.clauses),
        "graph6_G": graph6(g_adjacency),
        "gamma": gamma,
        "alpha": alpha,
        "gamma_infinity": 3,
        "theta": theta,
        "proper_H_3_coloring": coloring,
        "dominating_triples": len(dominating_triples),
        "greatest_eternal_family_states": len(greatest_family),
        "model_selected_family_states": len(selected_family),
        "full_targets_in_greatest_family_at_S": full_targets,
    }


def run_process(command: list[str], *, timeout: int) -> dict[str, object]:
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout,
        check=False,
        env={**os.environ, "LC_ALL": "C"},
    )
    return {
        "returncode": completed.returncode,
        "output": completed.stdout,
    }


def normalized_drat_log(display_command: list[str], output: str) -> str:
    lines = ["$ " + " ".join(display_command)]
    for raw in output.splitlines():
        line = raw.rstrip()
        if line.startswith("c verification time:"):
            lines.append("c verification time: <volatile timing omitted>")
        else:
            lines.append(line)
    return "\n".join(lines).rstrip() + "\n"


def complete_model_from_output(
    output: str, variable_count: int
) -> dict[int, bool]:
    signed: list[int] = []
    assert "s SATISFIABLE" in output
    for raw in output.splitlines():
        words = raw.split()
        if words and words[0] == "v":
            signed.extend(int(word) for word in words[1:] if word != "0")
    assert len(signed) == variable_count
    assert {abs(value) for value in signed} == set(range(1, variable_count + 1))
    return {abs(value): value > 0 for value in signed}


def stable_run_metadata(
    *,
    display_command: list[str],
    returncode: int,
    log_name: str,
    log_text: str,
) -> dict[str, object]:
    return {
        "command": display_command,
        "returncode": returncode,
        "log": f"reviews/order13_full_target_hostile/{log_name}",
        "log_sha256": sha256_bytes(log_text.encode("utf-8")),
    }


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    for name, expected in EXPECTED_HASHES.items():
        actual = sha256(SOURCE / name)
        assert actual == expected, (name, actual, expected)

    clean = CleanEncoding()
    clean.build()
    assert clean.variable_count == 9802
    assert len(clean.clauses) == 85409
    expected_tag_counts = {
        "no_h_k4": 715,
        "pair_witness_choice": 78,
        "pair_witness_edge": 1716,
        "retained_dominates": 2860,
        "family_nonempty": 1,
        "response_traverses_g_edge": 8580,
        "response_successor_retained": 8580,
        "retained_state_has_response": 2860,
        "anchor_h_triangle": 3,
        "anchor_retained": 1,
        "full_target_g_edge": 3,
        "full_target_successor": 3,
        "anchored_noncoloring": 59049,
        "signature_sorter": 960,
    }
    assert collections.Counter(clean.tags) == expected_tag_counts

    generated_bytes = clean.dimacs_bytes()
    generated_hash = hashlib.sha256(generated_bytes).hexdigest()
    frozen_bytes = (SOURCE / "minimal-instance.cnf").read_bytes()
    byte_identical = generated_bytes == frozen_bytes
    assert byte_identical
    assert generated_hash == EXPECTED_HASHES["minimal-instance.cnf"]

    frozen_variables, frozen_clauses = parse_dimacs(
        SOURCE / "minimal-instance.cnf"
    )
    assert frozen_variables == clean.variable_count
    assert frozen_clauses == clean.clauses
    assert all(
        len(clause) == len(set(clause))
        and not ({*clause} & {-lit for lit in clause})
        for clause in frozen_clauses
    )

    core_variables, core_clauses = parse_dimacs(SOURCE / "minimal-core.cnf")
    assert core_variables == clean.variable_count
    full_counter = collections.Counter(map(normalized_clause, clean.clauses))
    core_counter = collections.Counter(map(normalized_clause, core_clauses))
    assert not (core_counter - full_counter)

    sorter_result = sorter_truth_table(clean)

    clean_without_theta = CleanEncoding()
    clean_without_theta.build(include_theta_gap=False)
    assert len(clean_without_theta.clauses) == 26360
    positive = audit_positive_control(clean_without_theta)
    assert positive["graph6_G"] == "LF\\|ul\\XzVsaqJ"
    assert positive["greatest_eternal_family_states"] == 157

    assert DRAT_TRIM.is_file() and os.access(DRAT_TRIM, os.X_OK)
    assert CADICAL.is_file() and os.access(CADICAL, os.X_OK)

    # Independent ablation: removing literal one-guard closure makes the
    # otherwise minimal formula satisfiable.  This confirms that the
    # dynamics, not only the static parameter constraints, are active.
    clean_without_closure = CleanEncoding()
    clean_without_closure.build(include_closure=False)
    assert len(clean_without_closure.clauses) == 65389
    no_closure_bytes = clean_without_closure.dimacs_bytes()

    full_display = [
        "tools/drat_trim_2023_05_22/drat-trim",
        "<clean-room-byte-identical-minimal-instance.cnf>",
        "math/working/order13_single_full_squeeze/minimal-proof.drat",
        "-U",
    ]
    core_display = [
        "tools/drat_trim_2023_05_22/drat-trim",
        "math/working/order13_single_full_squeeze/minimal-core.cnf",
        "math/working/order13_single_full_squeeze/minimal-core.drat",
        "-U",
    ]
    closure_display = [
        "tools/cadical_3_0_1/build/cadical",
        "--quiet",
        "--binary=false",
        "<clean-room-minimal-without-closure.cnf>",
    ]

    def external_round() -> dict[str, object]:
        with tempfile.TemporaryDirectory(
            prefix="order13-full-hostile-"
        ) as raw:
            temporary = Path(raw)
            regenerated = temporary / "clean-room.cnf"
            regenerated.write_bytes(generated_bytes)
            no_closure_path = temporary / "without-closure.cnf"
            no_closure_path.write_bytes(no_closure_bytes)

            full_raw = run_process(
                [
                    str(DRAT_TRIM),
                    str(regenerated),
                    str(SOURCE / "minimal-proof.drat"),
                    "-U",
                ],
                timeout=60,
            )
            assert full_raw["returncode"] == 0
            assert "s VERIFIED" in full_raw["output"]
            assert "0 RAT lemmas" in full_raw["output"]
            full_log = normalized_drat_log(full_display, full_raw["output"])

            core_raw = run_process(
                [
                    str(DRAT_TRIM),
                    str(SOURCE / "minimal-core.cnf"),
                    str(SOURCE / "minimal-core.drat"),
                    "-U",
                ],
                timeout=60,
            )
            assert core_raw["returncode"] == 0
            assert "s VERIFIED" in core_raw["output"]
            assert "0 RAT lemmas" in core_raw["output"]
            core_log = normalized_drat_log(core_display, core_raw["output"])

            closure_raw = run_process(
                [
                    str(CADICAL),
                    "--quiet",
                    "--binary=false",
                    str(no_closure_path),
                ],
                timeout=60,
            )
            assert closure_raw["returncode"] == 10
            closure_assignment = complete_model_from_output(
                closure_raw["output"],
                clean_without_closure.variable_count,
            )
            assert all(
                evaluate_clause(clause, closure_assignment)
                for clause in clean_without_closure.clauses
            )
            closure_log = (
                "$ " + " ".join(closure_display) + "\n"
                "s SATISFIABLE\n"
                "c complete 9802-variable model independently checked "
                "against 65389 clean-room clauses\n"
            )

        logs = {
            "proof_replay_full.log": full_log,
            "proof_replay_core.log": core_log,
            "ablation_omit_closure.log": closure_log,
        }
        return {
            "logs": logs,
            "full_replay": stable_run_metadata(
                display_command=full_display,
                returncode=0,
                log_name="proof_replay_full.log",
                log_text=full_log,
            ),
            "core_replay": stable_run_metadata(
                display_command=core_display,
                returncode=0,
                log_name="proof_replay_core.log",
                log_text=core_log,
            ),
            "closure_ablation": stable_run_metadata(
                display_command=closure_display,
                returncode=10,
                log_name="ablation_omit_closure.log",
                log_text=closure_log,
            ),
        }

    # Run all external checks twice.  Random temporary paths and wall-clock
    # measurements are intentionally absent from the serialized evidence.
    first_round = external_round()
    second_round = external_round()
    assert first_round == second_round
    for log_name, log_text in first_round["logs"].items():
        (HERE / log_name).write_text(log_text, encoding="utf-8")
    full_replay = first_round["full_replay"]
    core_replay = first_round["core_replay"]
    closure_ablation = first_round["closure_ablation"]

    result = {
        "schema": "order13-full-target-hostile-audit-v1",
        "date": "2026-07-27",
        "verdict": "PASS",
        "determinism_regression": {
            "external_audit_rounds": 2,
            "normalized_outputs_byte_identical": True,
            "volatile_timing_and_temporary_paths_serialized": False,
        },
        "review_sources": {
            "checker.py": sha256(Path(__file__).resolve()),
            "REVIEW.md": sha256(HERE / "REVIEW.md"),
            "order13_single_full_squeeze/NOTE.md": sha256(
                SOURCE / "NOTE.md"
            ),
            "full_response_disjoint_witnesses/NOTE.md": sha256(
                CAMPAIGN
                / "math"
                / "working"
                / "full_response_disjoint_witnesses"
                / "NOTE.md"
            ),
            "full_response_witness_bound/NOTE.md": sha256(
                CAMPAIGN
                / "math"
                / "working"
                / "full_response_witness_bound"
                / "NOTE.md"
            ),
        },
        "finite_theorem_certified":
            "No order-13 k=3 equality counterexample with theta>3 has a "
            "full family-response target at a maximum independent triple.",
        "boundary":
            "This is only the full-response branch; the no-full-list "
            "order-13 branch and the universal conjecture remain open.",
        "clean_room_formula": {
            "variables": clean.variable_count,
            "clauses": len(clean.clauses),
            "tag_counts": expected_tag_counts,
            "sha256": generated_hash,
            "byte_identical_to_frozen": byte_identical,
            "normalized_core_is_submultiset": True,
            "omitted_conditions": [
                "connectivity",
                "uniqueness of the full target",
                "the five- or six-witness bound",
                "forcing every H-triangle into the family",
                "odd-hole/odd-antihole templates",
            ],
        },
        "sorter_truth_table": sorter_result,
        "artifacts": {
            name: {
                "sha256": sha256(SOURCE / name),
                "bytes": (SOURCE / name).stat().st_size,
            }
            for name in EXPECTED_HASHES
        },
        "tools": {
            "drat_trim": {
                "path": str(DRAT_TRIM.relative_to(CAMPAIGN)),
                "sha256": sha256(DRAT_TRIM),
            },
            "cadical": {
                "path": str(CADICAL.relative_to(CAMPAIGN)),
                "sha256": sha256(CADICAL),
            },
        },
        "proof_replays": {
            "full_clean_room_instance": full_replay,
            "reduced_core": core_replay,
        },
        "positive_control": positive,
        "ablations": {
            "omit_theta_gap": {
                "status": "SAT_MODEL_CHECKED",
                "clauses": len(clean_without_theta.clauses),
            },
            "omit_closure": {
                "status": "SAT",
                "clauses": 65389,
                "complete_model_independently_checked": True,
                **closure_ablation,
            },
            "no_sorter": "TIMEOUT in discovery run; treated as a nonclaim",
            "uniqueness_connectivity_witness_and_all_triangle_forcing":
                "absent from the decisive clean-room formula",
        },
        "human_theorem_review": {
            "anchor_pure_external_witnesses": "PASS",
            "pairwise_disjoint_external_witness_layers": "PASS",
            "six_non_neutral_vertices": "PASS",
            "cross_response_lemma": "PASS",
            "exact_separated_port_floor": 15,
        },
    }
    result_path = HERE / "result.json"
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
