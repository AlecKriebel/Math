#!/usr/bin/env python3
"""Clean-room differential and mutation probes for the k=4 candidate verifier.

The reference routines below use integer masks, recursive coloring, and an
independent graph6 construction.  They import no campaign evaluator.  Only
the implementation under review is imported for comparison.
"""

from __future__ import annotations

from contextlib import redirect_stdout
from hashlib import sha256
from io import StringIO
from itertools import combinations
from pathlib import Path
from random import Random
import subprocess
import sys
import tempfile
from unittest.mock import patch


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from verifier_k4_candidate import checker as target  # noqa: E402
from verifier_k4_candidate import cli as target_cli  # noqa: E402


SEED = 20_260_726


def masks_from_edges(order: int, edges: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    rows = [0] * order
    for left, right in edges:
        rows[left] |= 1 << right
        rows[right] |= 1 << left
    return tuple(rows)


def reference_graph6(order: int, edges: tuple[tuple[int, int], ...]) -> str:
    assert 0 <= order <= 62
    bit_count = order * (order - 1) // 2
    payload = [0] * bit_count
    for left, right in edges:
        lower, higher = sorted((left, right))
        payload[higher * (higher - 1) // 2 + lower] = 1
    payload.extend([0] * ((-len(payload)) % 6))
    characters = [chr(order + 63)]
    for start in range(0, len(payload), 6):
        value = sum(payload[start + offset] << (5 - offset) for offset in range(6))
        characters.append(chr(value + 63))
    return "".join(characters)


def reference_dominates(rows: tuple[int, ...], selected: int) -> bool:
    covered = selected
    remaining = selected
    while remaining:
        bit = remaining & -remaining
        remaining ^= bit
        covered |= rows[bit.bit_length() - 1]
    return covered == (1 << len(rows)) - 1


def reference_independent(rows: tuple[int, ...], selected: int) -> bool:
    remaining = selected
    while remaining:
        bit = remaining & -remaining
        remaining ^= bit
        if rows[bit.bit_length() - 1] & remaining:
            return False
    return True


def reference_parameters(rows: tuple[int, ...]) -> tuple[int, int, tuple[int, ...], int]:
    order = len(rows)
    subsets = range(1 << order)
    gamma = min(
        selected.bit_count()
        for selected in subsets
        if reference_dominates(rows, selected)
    )
    independent = [
        selected for selected in subsets if reference_independent(rows, selected)
    ]
    alpha = max(selected.bit_count() for selected in independent)
    maximal_sizes: list[int] = []
    for selected in independent:
        outside = ((1 << order) - 1) ^ selected
        maximal = True
        remaining = outside
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            vertex = bit.bit_length() - 1
            if not (rows[vertex] & selected):
                maximal = False
                break
        if maximal:
            maximal_sizes.append(selected.bit_count())
    return gamma, alpha, tuple(sorted(set(maximal_sizes))), len(maximal_sizes)


def state_mask(state: tuple[int, ...]) -> int:
    return sum(1 << vertex for vertex in state)


def reference_eternal_family(
    rows: tuple[int, ...],
    family: tuple[tuple[int, int, int, int], ...],
) -> bool:
    if not family:
        return False
    family_masks = {state_mask(state) for state in family}
    if len(family_masks) != len(family):
        return False
    order = len(rows)
    for selected in family_masks:
        if selected.bit_count() != 4 or not reference_dominates(rows, selected):
            return False
        for attacked in range(order):
            attacked_bit = 1 << attacked
            if selected & attacked_bit:
                continue
            responders = selected & rows[attacked]
            if not any(
                ((selected ^ guard_bit) | attacked_bit) in family_masks
                for guard_bit in (
                    1 << vertex for vertex in range(order) if responders & (1 << vertex)
                )
            ):
                return False
    return True


def reference_anchor_colorings(
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[int, tuple[int, ...] | None]:
    edge_set = set(edges)
    complement_rows = [0] * order
    for left, right in combinations(range(order), 2):
        if (left, right) not in edge_set:
            complement_rows[left] |= 1 << right
            complement_rows[right] |= 1 << left
    colors = [0, 1, 2, 3] + [-1] * (order - 4)
    proper = 0
    first: tuple[int, ...] | None = None

    def visit(vertex: int) -> None:
        nonlocal proper, first
        if vertex == order:
            proper += 1
            if first is None:
                first = tuple(colors)
            return
        earlier = complement_rows[vertex] & ((1 << vertex) - 1)
        for color in range(4):
            if any(
                earlier & (1 << other) and colors[other] == color
                for other in range(vertex)
            ):
                continue
            colors[vertex] = color
            visit(vertex + 1)
        colors[vertex] = -1

    visit(4)
    return proper, first


def digits_for_row(index: int) -> tuple[int, ...]:
    return tuple((index // (4 ** power)) % 4 for power in range(7, -1, -1))


def validate_trace(
    trace: Path,
    edges: tuple[tuple[int, int], ...],
    *,
    expected_proper: int,
) -> None:
    raw = trace.read_bytes()
    lines = raw.decode("ascii").splitlines()
    assert lines[:5] == [
        "GT4TRACE 1",
        f"graph6 {reference_graph6(12, edges)}",
        "anchor 0:0 1:1 2:2 3:3",
        "outer 4 5 6 7 8 9 10 11",
        "rows 65536",
    ]
    complement_edges = tuple(
        pair for pair in combinations(range(12), 2) if pair not in set(edges)
    )
    proper_count = 0
    for index in range(4**8):
        fields = lines[5 + index].split()
        digits = digits_for_row(index)
        assert fields[:3] == ["r", f"{index:05d}", "".join(map(str, digits))]
        coloring = (0, 1, 2, 3) + digits
        conflicts = tuple(
            pair
            for pair in complement_edges
            if coloring[pair[0]] == coloring[pair[1]]
        )
        if fields[3] == "proper":
            assert len(fields) == 4
            assert not conflicts
            proper_count += 1
        else:
            assert fields[3] == "conflict" and len(fields) == 6
            assert conflicts
            assert tuple(map(int, fields[4:])) == conflicts[0]
    assert proper_count == expected_proper
    assert lines[-1] == f"summary rows 65536 proper {expected_proper}"
    assert len(lines) == 5 + 4**8 + 1


def graph6_and_parameter_differential() -> None:
    rng = Random(SEED)
    all_edges = tuple(combinations(range(12), 2))
    for case in range(2_048):
        threshold = rng.randrange(101)
        edges = tuple(edge for edge in all_edges if rng.randrange(100) < threshold)
        graph = target.Graph.from_edges(12, edges)
        assert graph.to_graph6() == reference_graph6(12, edges), case
        if case < 256:
            rows = masks_from_edges(12, edges)
            gamma, alpha, maximal_sizes, maximal_count = reference_parameters(rows)
            assert target._first_dominating_set(graph)[0] == gamma, case
            assert target._first_maximum_independent_set(graph)[0] == alpha, case
            assert target._maximal_independent_profile(graph) == (
                maximal_sizes,
                maximal_count,
            ), case
    print("GRAPH6_DIFFERENTIAL cases=2048 PASS")
    print("STATIC_PARAMETER_DIFFERENTIAL cases=256 PASS")


def eternal_differential() -> None:
    rng = Random(SEED ^ 0xE7E2)
    all_edges = tuple(combinations(range(6), 2))
    all_states = tuple(combinations(range(6), 4))
    for case in range(4_096):
        edges = tuple(edge for edge in all_edges if rng.getrandbits(1))
        graph = target.Graph.from_edges(6, edges)
        rows = masks_from_edges(6, edges)
        family = tuple(state for state in all_states if rng.randrange(4) == 0)
        expected = reference_eternal_family(rows, family)
        observed = target.check_eternal_family(graph, family).passed
        assert observed == expected, (case, edges, family, expected, observed)

    complete5 = target.Graph.from_edges(5, combinations(range(5), 2))
    all_four_sets = tuple(combinations(range(5), 4))
    assert target.check_eternal_family(complete5, all_four_sets).passed

    missing_move_edge = target.Graph.from_edges(
        5,
        (
            edge
            for edge in combinations(range(5), 2)
            if edge != (0, 4)
        ),
    )
    two_states = ((0, 1, 2, 3), (1, 2, 3, 4))
    assert not target.check_eternal_family(missing_move_edge, two_states).passed

    complete6 = target.Graph.from_edges(6, combinations(range(6), 2))
    all_guards_only = ((0, 1, 2, 3), (2, 3, 4, 5))
    assert not target.check_eternal_family(complete6, all_guards_only).passed
    print("ONE_GUARD_DIFFERENTIAL cases=4096 PASS")
    print("ONE_GUARD_MUTATIONS nonedge_move=KILLED all_guards_move=KILLED")


def coloring_differential_and_trace() -> None:
    rng = Random(SEED ^ 0xC0102)
    anchor_pairs = set(combinations(range(4), 2))
    eligible = tuple(
        pair for pair in combinations(range(12), 2) if pair not in anchor_pairs
    )
    graphs: list[tuple[tuple[int, int], ...]] = [
        tuple(eligible),
        tuple(
            pair
            for pair in combinations(range(12), 2)
            if pair not in set(combinations(range(5), 2))
        ),
    ]
    for _ in range(62):
        graphs.append(tuple(edge for edge in eligible if rng.getrandbits(1)))

    for case, edges in enumerate(graphs):
        graph = target.Graph.from_edges(12, edges)
        expected_proper, expected_first = reference_anchor_colorings(12, edges)
        observed = target.anchored_four_color_search(graph)
        assert observed.rows_checked == 4**8, case
        assert observed.proper_rows == expected_proper, case
        assert observed.first_proper_coloring == expected_first, case

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        for label, edges in (
            ("complement_k4", graphs[0]),
            ("complement_k5", graphs[1]),
        ):
            graph = target.Graph.from_edges(12, edges)
            expected_proper, _ = reference_anchor_colorings(12, edges)
            trace = root / f"{label}.gt4trace"
            result = target.anchored_four_color_search(graph, trace_path=trace)
            validate_trace(trace, edges, expected_proper=expected_proper)
            assert sha256(trace.read_bytes()).hexdigest() == result.trace_sha256
    print("COLORING_DIFFERENTIAL cases=64 PASS")
    print("TRACE_INDEPENDENT_ROWS traces=2 rows=131072 PASS")


def classifier_and_cli_checks() -> None:
    names = target.DEFINITION_LEVEL_CHECKS
    assert names == (
        "graph_identity",
        "gamma_equals_4",
        "one_guard_eternal_family",
        "theta_at_least_5",
    )
    for mask in range(16):
        for ancillary in (False, True):
            checks = {
                name: {"passed": bool(mask & (1 << index))}
                for index, name in enumerate(names)
            }
            checks["connected"] = {"passed": ancillary}
            mathematical, complete, status, consistency = target._classify_checks(
                checks
            )
            expected_math = mask == 15
            assert mathematical == expected_math
            assert complete == (expected_math and ancillary)
            assert consistency == ("connected",)
            assert status == (
                "VERIFIED_COUNTEREXAMPLE_CANDIDATE"
                if expected_math and ancillary
                else (
                    "VERIFIED_COUNTEREXAMPLE_WITH_CONSISTENCY_ALERTS"
                    if expected_math
                    else "REJECTED_NO_COUNTEREXAMPLE_VERIFIED"
                )
            )

    with tempfile.TemporaryDirectory() as temporary:
        candidate = Path(temporary) / "placeholder.json"
        candidate.write_text("{}")
        with patch.object(
            target_cli,
            "load_candidate",
            return_value=(object(), "source-hash"),
        ):
            for accepted, expected_exit in ((True, 0), (False, 1)):
                synthetic = {
                    "accepted": accepted,
                    "status": (
                        "VERIFIED_COUNTEREXAMPLE_WITH_CONSISTENCY_ALERTS"
                        if accepted
                        else "REJECTED_NO_COUNTEREXAMPLE_VERIFIED"
                    ),
                }
                with patch.object(
                    target_cli,
                    "verify_candidate",
                    return_value=synthetic,
                ):
                    sink = StringIO()
                    with redirect_stdout(sink):
                        observed_exit = target_cli.main([str(candidate)])
                    assert observed_exit == expected_exit
    print("ACCEPTANCE_CLASSIFIER truth_rows=32 PASS")
    print("CLI_DOCUMENTED_BRANCHES accepted=0 rejected=1 PASS")


def malformed_nesting_cli_regression() -> None:
    """Confirm that deeply nested JSON fails through the documented boundary."""

    with tempfile.TemporaryDirectory() as temporary:
        malformed = Path(temporary) / "deep.json"
        depth = 500_000
        malformed.write_text("[" * depth + "0" + "]" * depth)
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "verifier_k4_candidate",
                str(malformed),
            ],
            cwd=CAMPAIGN,
            env={
                "PYTHONPATH": str(CAMPAIGN / "src"),
                "PATH": "/usr/bin:/bin",
            },
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20,
            check=False,
        )
        assert result.returncode == 2
        assert not result.stderr
        assert b'"accepted": false' in result.stdout
        assert b'"status": "MALFORMED_OR_IO_ERROR"' in result.stdout
        assert b"candidate JSON nesting is too deep" in result.stdout
    print(
        "CLI_DEEP_JSON_REGRESSION bytes=1000001 exit=2 "
        "json_report=true PASS"
    )


def main() -> None:
    graph6_and_parameter_differential()
    eternal_differential()
    coloring_differential_and_trace()
    classifier_and_cli_checks()
    malformed_nesting_cli_regression()
    print("CORE_SOUNDNESS_PROBES PASS")
    print("RELEASE_ROBUSTNESS_PROBES PASS")


if __name__ == "__main__":
    main()
