#!/usr/bin/env python3
"""Standalone exact adversarial audit of the K3P cut-transfer shortcut.

This program imports no project module and uses only the Python standard
library.  It treats both JC certificates as untrusted JSON, reconstructs the
literal type-48 endpoint from descendant masks, and compiles the CFN and full
K3P Fourier flattenings in exact ``fractions.Fraction`` arithmetic.

Default execution performs the complete deterministic endpoint/single-blob
scan and the mutation suite.  ``--quick`` skips only the 31,329 endpoint-pair
and 453 single-blob scan.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict, deque
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys
import time


HERE = Path(__file__).resolve().parent
CUT_ROOT = HERE.parent

FROZEN = CUT_ROOT / "upstream_frozen" / "pointwise_cut_certificate.json"
WITHDRAWN = CUT_ROOT / "upstream_frozen" / "WITHDRAWN.md"
CORRECTED = CUT_ROOT / "upstream_frozen" / "corrected_jc_cut_certificate.json"
PROVENANCE = CUT_ROOT / "UPSTREAM_PROVENANCE.json"

FROZEN_SHA256 = "b627df5b2dc8cf1eb21c2e08c974f9e54f5a0399043e4dd96ea95dc73c2c3350"
FROZEN_BYTES = 3_077_509
CORRECTED_SHA256 = "edbd4afe566ed0ed5d1c518ffe5b21f8f224d547b9c351cb4e1a8c1c613ac086"
WITHDRAWN_SHA256 = "92cbc225aa3a65962a149fc833cbd118be83ad54dd0052c84e88a2ac1d8b8111"

ZERO = 0
C = 1
G = 2
T = 3
GROUP = (ZERO, C, G, T)

TYPE48 = (
    (0, 0, 0, 4),
    (0, 0, 4, 0),
    (0, 0, 4, 4),
    (1, 1, 1, 1),
    (1, 1, 1, 5),
    (1, 1, 5, 5),
    (2, 2, 2, 2),
    (4, 4, 0, 0),
    (4, 4, 4, 4),
    (5, 5, 5, 5),
)
TYPE48_INDEX = 48  # Python zero-based: the 49th frozen endpoint record.
CENTRAL_ROW = 8

CFN_C = tuple(
    map(
        Fraction,
        (
            "3/4",
            "9/10",
            "2/3",
            "1/3",
            "3/4",
            "1/10",
            "1/2",
            "5/6",
            "1",
            "1/2",
        ),
    )
)
CFN_DELTAS = (Fraction(1, 6), Fraction(1, 2))
CFN_A = Fraction(1, 160)
CFN_B = Fraction(25, 288)
CFN_C_COORD = Fraction(427, 3840)
CFN_GAMMA = Fraction(-3763, 1_105_920)
CFN_EFFECTIVE_Z = Fraction(6912, 10675)

# A strict continuous-time extension of the type-48 CFN witness.  Every
# noncentral reduced endpoint row has eigenvalue triple (c,1/4,1/4).
CT_AUX = Fraction(1, 4)
CT_ENDPOINT_CENTRAL = (Fraction(9, 10), CT_AUX, CT_AUX)
CT_PHYSICAL_BRIDGE = (Fraction(1024, 1281), CT_AUX, CT_AUX)
CT_EFFECTIVE_BRIDGE = (
    Fraction(1),
    CFN_EFFECTIVE_Z,
    Fraction(1, 64),
    Fraction(1, 64),
)

# Exact rational point at which all three order-two projections drop to the
# binary cut threshold simultaneously.  The full K3P flattening remains rank
# 16.  Row 8 is the normalized central incidence and is therefore identity.
JOINT_EDGE_TRIPLES_RAW = (
    (559, 301, 349),
    (270, 363, 430),
    (890, 953, 896),
    (87, 283, 680),
    (89, 69, 764),
    (59, 52, 38),
    (514, 671, 822),
    (635, 627, 685),
    None,
    (379, 380, 991),
)
JOINT_DELTAS = (Fraction(117, 1000), Fraction(563, 1000))


def ftext(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def sha256_bytes(payload: bytes) -> str:
    return sha256(payload).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def fraction_digest(value: Fraction) -> str:
    return sha256(ftext(value).encode("ascii")).hexdigest()


def switching_weights(deltas: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    """Frozen type-key convention: index = bit0 + 2*bit1."""

    answer = []
    for switching in range(1 << len(deltas)):
        weight = Fraction(1)
        for bit, delta in enumerate(deltas):
            weight *= delta if switching & (1 << bit) else 1 - delta
        answer.append(weight)
    assert sum(answer) == 1
    return tuple(answer)


def xor_on_mask(assignment: tuple[int, ...], mask: int) -> int:
    answer = 0
    for position, character in enumerate(assignment):
        if mask & (1 << position):
            answer ^= character
    return answer


def endpoint_coordinate(
    tensor: tuple[tuple[int, ...], ...],
    edge_fourier: tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...],
    deltas: tuple[Fraction, ...],
    assignment: tuple[int, int, int],
) -> Fraction:
    assert len(tensor) == len(edge_fourier)
    weights = switching_weights(deltas)
    assert all(len(row) == len(weights) for row in tensor)
    total = Fraction(0)
    for switching, weight in enumerate(weights):
        term = weight
        for row, eigenvalues in zip(tensor, edge_fourier):
            term *= eigenvalues[xor_on_mask(assignment, row[switching])]
        total += term
    return total


def endpoint_matrix(
    tensor: tuple[tuple[int, ...], ...],
    edge_fourier: tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...],
    deltas: tuple[Fraction, ...],
) -> list[list[Fraction]]:
    return [
        [endpoint_coordinate(tensor, edge_fourier, deltas, (i, j, i ^ j)) for j in GROUP]
        for i in GROUP
    ]


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    result = 0
    for column in range(columns):
        pivot = next((row for row in range(result, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[result], work[pivot] = work[pivot], work[result]
        pivot_value = work[result][column]
        for row in range(result + 1, rows):
            if not work[row][column]:
                continue
            multiplier = work[row][column] / pivot_value
            work[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(work[row], work[result])
            ]
        result += 1
        if result == rows:
            break
    return result


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    assert matrix and len(matrix) == len(matrix[0])
    work = [row[:] for row in matrix]
    result = Fraction(1)
    sign = 1
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        result *= pivot_value
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            multiplier = work[row][column] / pivot_value
            work[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(work[row], work[column])
            ]
    return sign * result


def crossing_blocks(
    left: list[list[Fraction]],
    right: list[list[Fraction]],
    bridge: tuple[Fraction, Fraction, Fraction, Fraction],
) -> tuple[list[list[Fraction]], ...]:
    blocks = []
    # Wrong split 13|24: row is (g1,g3), column is (g2,g4).
    # In block s, g3=s^g1 and g4=s^g2.
    for total in GROUP:
        blocks.append(
            [
                [
                    left[g1][g2]
                    * bridge[g1 ^ g2]
                    * right[total ^ g1][total ^ g2]
                    for g2 in GROUP
                ]
                for g1 in GROUP
            ]
        )
    return tuple(blocks)


def principal_projection_rank(blocks: tuple[list[list[Fraction]], ...], character: int) -> int:
    assert character in (C, G, T)
    return sum(
        rank([[blocks[total][i][j] for j in (ZERO, character)] for i in (ZERO, character)])
        for total in (ZERO, character)
    )


def d3_margins(triple: tuple[Fraction, Fraction, Fraction]) -> tuple[Fraction, Fraction, Fraction]:
    c, g, t = triple
    return (1 + c - g - t, 1 - c + g - t, 1 - c - g + t)


def ct_margins(triple: tuple[Fraction, Fraction, Fraction]) -> tuple[Fraction, Fraction, Fraction]:
    c, g, t = triple
    return (c - g * t, g - c * t, t - c * g)


def assert_d3_plus(triple: tuple[Fraction, Fraction, Fraction]) -> None:
    assert all(0 < value < 1 for value in triple)
    assert all(value > 0 for value in d3_margins(triple))


def assert_ct(triple: tuple[Fraction, Fraction, Fraction]) -> None:
    assert_d3_plus(triple)
    assert all(value > 0 for value in ct_margins(triple))


def multiply_triples(
    triples: list[tuple[Fraction, Fraction, Fraction]] | tuple[tuple[Fraction, Fraction, Fraction], ...]
) -> tuple[Fraction, Fraction, Fraction]:
    result = [Fraction(1), Fraction(1), Fraction(1)]
    for triple in triples:
        result = [left * right for left, right in zip(result, triple)]
    return tuple(result)  # type: ignore[return-value]


def normalize_mask(mask: int, width: int) -> int:
    all_mask = (1 << width) - 1
    if mask in (0, all_mask):
        return 0
    return min(mask, all_mask ^ mask)


def normalize_tensor(tensor: tuple[tuple[int, ...], ...], boundary_width: int) -> tuple[tuple[int, ...], ...]:
    rows = {
        tuple(normalize_mask(mask, boundary_width) for mask in row)
        for row in tensor
    }
    return tuple(sorted(row for row in rows if any(row)))


def relabel_mask(mask: int, old_positions_in_new_order: tuple[int, ...]) -> int:
    result = 0
    for new_position, old_position in enumerate(old_positions_in_new_order):
        if mask & (1 << old_position):
            result |= 1 << new_position
    return result


def verify_rooted_graph_and_masks(record: dict) -> dict:
    graph = record["witness_graph"]
    arcs = tuple(tuple(edge) for edge in graph["arcs"])
    root = graph["root"]
    selected = {str(key): int(value) for key, value in graph["selected"].items()}
    full_labels = {str(key): int(value) for key, value in graph["full_labels"].items()}
    assert len(arcs) == len(set(arcs))

    vertices = {vertex for edge in arcs for vertex in edge}
    indegree = Counter(head for _tail, head in arcs)
    outdegree = Counter(tail for tail, _head in arcs)
    children: dict[str, list[str]] = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    assert (indegree[root], outdegree[root]) == (0, 2)
    for vertex in vertices:
        degree = (indegree[vertex], outdegree[vertex])
        if vertex in full_labels:
            assert degree == (1, 0)
        elif vertex != root:
            assert degree in ((1, 2), (2, 1))

    # DAG and reachability.
    pending = {vertex: indegree[vertex] for vertex in vertices}
    queue = deque(vertex for vertex in vertices if pending[vertex] == 0)
    visited = []
    while queue:
        vertex = queue.popleft()
        visited.append(vertex)
        for child in children[vertex]:
            pending[child] -= 1
            if pending[child] == 0:
                queue.append(child)
    assert len(visited) == len(vertices)
    reachable = set()
    stack = [root]
    while stack:
        vertex = stack.pop()
        if vertex in reachable:
            continue
        reachable.add(vertex)
        stack.extend(children[vertex])
    assert reachable == vertices

    # The displayed rooted presentation is tree-child.
    for vertex in vertices - set(full_labels):
        assert any(child in full_labels or indegree[child] == 1 for child in children[vertex])

    reticulations = tuple(sorted(vertex for vertex in vertices if (indegree[vertex], outdegree[vertex]) == (2, 1)))
    assert reticulations == tuple(graph["reticulations"])
    assert len(reticulations) == 2

    incoming = {
        reticulation: tuple(index for index, (_tail, head) in enumerate(arcs) if head == reticulation)
        for reticulation in reticulations
    }
    raw_rows = [[] for _edge in arcs]
    normalized_rows = [[] for _edge in arcs]
    all_mask = (1 << len(selected)) - 1
    active_choices = tuple(product((0, 1), repeat=len(reticulations)))
    for choice in active_choices:
        excluded = {
            incoming[reticulation][1 - bit]
            for reticulation, bit in zip(reticulations, choice)
        }
        kept_children: dict[str, list[str]] = defaultdict(list)
        for edge_index, (tail, head) in enumerate(arcs):
            if edge_index not in excluded:
                kept_children[tail].append(head)
        memo: dict[str, int] = {}

        def descendants(vertex: str) -> int:
            if vertex not in memo:
                mask = (1 << selected[vertex]) if vertex in selected else 0
                for child in kept_children[vertex]:
                    mask |= descendants(child)
                memo[vertex] = mask
            return memo[vertex]

        for edge_index, (_tail, head) in enumerate(arcs):
            raw = 0 if edge_index in excluded else descendants(head)
            raw_rows[edge_index].append(raw)
            normalized_rows[edge_index].append(normalize_mask(raw, len(selected)))

    compilation = graph["displayed_tree_compilation"]
    assert [list(choice) for choice in active_choices] == compilation["switching_choices"]
    for edge_index, stored in enumerate(compilation["edge_rows"]):
        assert stored["edge_index"] == edge_index
        assert stored["arc"] == list(arcs[edge_index])
        assert stored["raw_descendant_masks"] == raw_rows[edge_index]
        assert stored["zero_sum_normalized_masks"] == normalized_rows[edge_index]

    raw_effective = tuple(sorted({tuple(row) for row in normalized_rows if any(row)}))
    transport = graph["transport"]
    order = tuple(transport["leaf_permutation"])
    action = tuple(transport["choice_action"])
    transformed = tuple(
        sorted(
            tuple(relabel_mask(row[index], order) for index in action)
            for row in raw_effective
        )
    )
    stored_signatures = tuple(tuple(row) for row in record["signatures"])
    assert transformed == stored_signatures

    # Locked standard-strong mixed-graph criterion after one root suppression.
    reticulation_set = set(reticulations)
    retained = []
    incident = []
    for tail, head in arcs:
        mixed = (frozenset((tail, head)), frozenset((head,)) if head in reticulation_set else frozenset())
        (incident if root in mixed[0] else retained).append(mixed)
    assert len(incident) == 2
    left = next(iter(incident[0][0] - {root}))
    right = next(iter(incident[1][0] - {root}))
    assert left != right
    inherited = (incident[0][1] & {left}) | (incident[1][1] & {right})
    retained.append((frozenset((left, right)), inherited))
    assert len({edge[0] for edge in retained}) == len(retained)
    incidence: dict[str, list[tuple[frozenset[str], frozenset[str]]]] = defaultdict(list)
    incoming_count = Counter()
    undirected_count = Counter()
    tails = set()
    for endpoints, arrowheads in retained:
        assert len(arrowheads) <= 1
        for vertex in endpoints:
            incidence[vertex].append((endpoints, arrowheads))
        if arrowheads:
            head = next(iter(arrowheads))
            incoming_count[head] += 1
            tails.update(endpoints - {head})
        else:
            for vertex in endpoints:
                undirected_count[vertex] += 1
    for vertex, adjacent in incidence.items():
        if vertex in full_labels:
            assert len(adjacent) == 1
        else:
            assert len(adjacent) == 3 and incoming_count[vertex] in (0, 2)
    assert all(undirected_count[tail] == 2 for tail in tails)

    return {
        "corrected_record_id": record["id"],
        "core": graph["core"],
        "role": graph["role"],
        "vertices": len(vertices),
        "arcs": len(arcs),
        "reticulations": list(reticulations),
        "raw_descendant_rows_recomputed": len(raw_rows),
        "effective_rows_recomputed": len(raw_effective),
        "rooted_binary_DAG": True,
        "tree_child_rooting": True,
        "locked_standard_strong_mixed_criterion": True,
    }


def bind_provenance() -> tuple[dict, dict, dict]:
    frozen_bytes = FROZEN.read_bytes()
    corrected_bytes = CORRECTED.read_bytes()
    provenance = json.loads(PROVENANCE.read_text())
    assert len(frozen_bytes) == FROZEN_BYTES
    assert sha256_bytes(frozen_bytes) == FROZEN_SHA256
    assert sha256_bytes(corrected_bytes) == CORRECTED_SHA256
    assert sha256_path(WITHDRAWN) == WITHDRAWN_SHA256
    assert provenance["dependency"]["destination_sha256"] == FROZEN_SHA256
    assert provenance["dependency"]["source_sha256"] == FROZEN_SHA256
    assert provenance["dependency"]["status"] == "BYTE_IDENTICAL_COPY"
    withdrawn_text = WITHDRAWN.read_text()
    assert "WITHDRAWN" in withdrawn_text and "DO NOT SUBMIT OR CITE AS ESTABLISHED" in withdrawn_text
    frozen = json.loads(frozen_bytes)
    corrected = json.loads(corrected_bytes)
    assert frozen["status"] == "PROVED"
    assert len(frozen["endpoint_records"]) == 177
    assert len(frozen["single_blob_records"]) == 453
    assert corrected["status"] == "EXACTLY COMPUTED"
    assert corrected["three_port_endpoint_dichotomy"]["status"] == "EXACTLY COMPUTED"
    return frozen, corrected, {
        "recovered_sha256": FROZEN_SHA256,
        "recovered_bytes": FROZEN_BYTES,
        "historical_byte_identity": provenance["dependency"]["status"] == "BYTE_IDENTICAL_COPY",
        "historical_location": provenance["dependency"]["source"],
        "historical_release_marked_withdrawn": True,
        "historical_git_commit": "a9a377d5e5d1af773ae161baf836cce37c5578b0",
        "historical_git_blob": "cbfe1d486e3cc59e1839098149735714a0819797",
        "corrected_JC_certificate_sha256": CORRECTED_SHA256,
        "corrected_JC_certificate_bytes": len(corrected_bytes),
        "corrected_JC_git_commits": [
            "85413ad5680db6b6c6d82211d901e8c4ee7862e1",
            "9c6c9c5f2878671b5b32ceee254bab96da854b73",
        ],
        "corrected_JC_git_blob": "f24769f4a451b83dcee001a6048e8c815819b7a7",
    }


def verify_type48_binding(frozen: dict, corrected: dict) -> tuple[dict, dict]:
    row = frozen["endpoint_records"][TYPE48_INDEX]
    assert ast.literal_eval(row["type_key"]) == TYPE48
    assert row["origins"] == ["theta_incoming_active"]
    assert row["certificate"]["branch"] == "F_positive"

    # Corrected record 26 is the same central-designated structural tensor
    # after exact zero-sum complement normalization and duplicate-row grouping.
    corrected_row = corrected["three_port_endpoint_dichotomy"]["records"][26]
    assert corrected_row["id"] == 26
    corrected_signatures = tuple(tuple(signature) for signature in corrected_row["signatures"])
    assert normalize_tensor(TYPE48, 3) == normalize_tensor(corrected_signatures, 3)
    assert corrected_row["dichotomy"]["normalization"]["central_effective_edge_index"] == 7
    assert corrected_signatures[7] == (4, 4, 4, 4)
    graph_report = verify_rooted_graph_and_masks(corrected_row)

    old_groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for index, signature in enumerate(TYPE48):
        old_groups[tuple(normalize_mask(mask, 3) for mask in signature)].append(index)
    corrected_to_old = []
    for signature in corrected_signatures:
        normalized = tuple(normalize_mask(mask, 3) for mask in signature)
        corrected_to_old.append(old_groups[normalized])
    assert corrected_to_old == [[0], [1], [2], [3], [4], [5], [7], [8], [6, 9]]

    return {
        "frozen_record_index_zero_based": TYPE48_INDEX,
        "frozen_record_ordinal": TYPE48_INDEX + 1,
        "origin": row["origins"][0],
        "JC_branch": row["certificate"]["branch"],
        "literal_reduced_descendant_masks": [list(signature) for signature in TYPE48],
        "corrected_graph_record_id": 26,
        "zero_sum_normalized_tensor_matches_corrected_graph": True,
        "corrected_effective_row_to_old_row_indices": corrected_to_old,
    }, graph_report


def cfn_counterexample() -> tuple[dict, list[list[Fraction]], tuple[list[list[Fraction]], ...]]:
    edge = tuple((Fraction(1), value, Fraction(1), Fraction(1)) for value in CFN_C)
    endpoint = endpoint_matrix(TYPE48, edge, CFN_DELTAS)
    a = endpoint[C][C]
    b = endpoint[C][ZERO]
    c = endpoint[ZERO][C]
    assert (a, b, c) == (CFN_A, CFN_B, CFN_C_COORD)
    assert a - b * c == CFN_GAMMA < 0
    z = a / (b * c)
    assert z == CFN_EFFECTIVE_Z and 0 < z < 1
    blocks = crossing_blocks(endpoint, endpoint, (Fraction(1), z, Fraction(1), Fraction(1)))
    cfn_determinants = []
    for total in (ZERO, C):
        minor = [[blocks[total][i][j] for j in (ZERO, C)] for i in (ZERO, C)]
        cfn_determinants.append(determinant(minor))
    assert cfn_determinants == [0, 0]
    assert principal_projection_rank(blocks, C) == 2

    physical_central_c = Fraction(9, 10)
    physical_bridge_c = z / physical_central_c**2
    assert physical_bridge_c == Fraction(1024, 1281)
    assert 0 < physical_bridge_c < 1
    return {
        "status": "EXACT_COUNTEREXAMPLE_TO_ONE_CHARACTER_TRANSFER",
        "edge_c_parameters_type_key_order": [ftext(value) for value in CFN_C],
        "inheritance_deltas": [ftext(value) for value in CFN_DELTAS],
        "endpoint_coordinates": {"a=q011": ftext(a), "b=q101": ftext(b), "c=q110": ftext(c)},
        "Gamma=a-bc": ftext(CFN_GAMMA),
        "effective_z": ftext(z),
        "endpoint_central_c_each_side": ftext(physical_central_c),
        "physical_bridge_c": ftext(physical_bridge_c),
        "wrong_split": "13|24",
        "binary_character_block_determinants": [ftext(value) for value in cfn_determinants],
        "binary_flattening_rank": 2,
        "binary_cut_threshold": 2,
    }, endpoint, blocks


def ct_edge_fourier() -> tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...]:
    result = []
    for index, c in enumerate(CFN_C):
        if index == CENTRAL_ROW:
            result.append((Fraction(1), Fraction(1), Fraction(1), Fraction(1)))
        else:
            result.append((Fraction(1), c, CT_AUX, CT_AUX))
    return tuple(result)


def physical_graph_realization(
    corrected: dict,
    normalized_old_triples: tuple[tuple[Fraction, Fraction, Fraction], ...],
    central_triple: tuple[Fraction, Fraction, Fraction],
    split_rho: Fraction,
    require_ct: bool,
) -> dict:
    """Put exact physical triples on every arc of corrected graph record 26."""

    record = corrected["three_port_endpoint_dichotomy"]["records"][26]
    graph = record["witness_graph"]
    compilation = graph["displayed_tree_compilation"]
    corrected_signatures = tuple(tuple(row) for row in record["signatures"])
    old_groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for index, signature in enumerate(TYPE48):
        old_groups[tuple(normalize_mask(mask, 3) for mask in signature)].append(index)

    desired_by_stored: dict[tuple[int, ...], tuple[Fraction, Fraction, Fraction]] = {}
    for stored in corrected_signatures:
        normalized = tuple(normalize_mask(mask, 3) for mask in stored)
        indices = old_groups[normalized]
        desired = multiply_triples([normalized_old_triples[index] for index in indices])
        if stored == (4, 4, 4, 4):
            assert indices == [CENTRAL_ROW]
            desired = central_triple
        desired_by_stored[stored] = desired

    order = tuple(graph["transport"]["leaf_permutation"])
    action = tuple(graph["transport"]["choice_action"])
    arc_triples: list[tuple[Fraction, Fraction, Fraction] | None] = [None] * len(graph["arcs"])
    physical_rows = compilation["effective_row_groups"]
    for group in physical_rows:
        raw_signature = tuple(group["signature"])
        stored_signature = tuple(relabel_mask(raw_signature[index], order) for index in action)
        desired = desired_by_stored[stored_signature]
        indices = list(group["edge_indices"])
        if len(indices) == 1:
            factors = [desired]
        else:
            assert len(indices) == 2
            isotropic = (split_rho, split_rho, split_rho)
            quotient = tuple(value / split_rho for value in desired)
            factors = [isotropic, quotient]
            assert multiply_triples(factors) == desired
        for edge_index, triple in zip(indices, factors):
            arc_triples[edge_index] = triple

    # The dummy-leaf row is identically zero on retained coordinates.
    for index, triple in enumerate(arc_triples):
        if triple is None:
            stored = compilation["edge_rows"][index]
            assert not any(stored["zero_sum_normalized_masks"])
            arc_triples[index] = (Fraction(1, 2),) * 3

    for triple in arc_triples:
        assert triple is not None
        (assert_ct if require_ct else assert_d3_plus)(triple)

    # Active graph switching weights equal frozen weights after reticulation
    # axis swap and choice-complement convention.
    d0, d1 = CFN_DELTAS if require_ct else JOINT_DELTAS
    active_inheritance = (1 - d1, 1 - d0)
    active_weights = tuple(
        (active_inheritance[0] if b0 == 0 else 1 - active_inheritance[0])
        * (active_inheritance[1] if b1 == 0 else 1 - active_inheritance[1])
        for b0, b1 in product((0, 1), repeat=2)
    )
    assert active_weights == switching_weights((d0, d1))

    # Compile all 16 endpoint coordinates once from the literal physical arc
    # descendant masks, not from the reduced tensor, and compare them with
    # the old reduced tensor plus the restored central-incidence multiplier.
    old_fourier = tuple((Fraction(1),) + triple for triple in normalized_old_triples)
    old_endpoint = endpoint_matrix(TYPE48, old_fourier, (d0, d1))
    raw_rows = tuple(
        tuple(row["raw_descendant_masks"])
        for row in compilation["edge_rows"]
    )
    arc_fourier = tuple((Fraction(1),) + triple for triple in arc_triples)  # type: ignore[operator]
    coordinate_checks = 0
    for first in GROUP:
        for second in GROUP:
            central = first ^ second
            stored_assignment = (first, second, central)
            original_assignment = [0, 0, 0]
            for new_position, old_position in enumerate(order):
                original_assignment[old_position] = stored_assignment[new_position]
            graph_value = Fraction(0)
            for switching, weight in enumerate(active_weights):
                term = weight
                for row, eigenvalues in zip(raw_rows, arc_fourier):
                    term *= eigenvalues[xor_on_mask(tuple(original_assignment), row[switching])]
                graph_value += term
            expected = (
                old_endpoint[first][second] * central_triple[central - 1]
                if central
                else old_endpoint[first][second]
            )
            assert graph_value == expected
            coordinate_checks += 1

    return {
        "physical_arc_count": len(arc_triples),
        "physical_arc_triples": [[ftext(value) for value in triple] for triple in arc_triples],
        "active_inheritance_parameters": [ftext(value) for value in active_inheritance],
        "all_arcs_strict_CT" if require_ct else "all_arcs_strict_D3_plus": True,
        "serial_effective_products_checked": True,
        "literal_arc_coordinate_checks": coordinate_checks,
    }


def verify_full_k3p_type48(corrected: dict) -> tuple[dict, tuple[list[list[Fraction]], ...]]:
    edges = ct_edge_fourier()
    for index, eigenvalues in enumerate(edges):
        if index != CENTRAL_ROW:
            assert_ct(eigenvalues[1:])
    assert_ct(CT_ENDPOINT_CENTRAL)
    assert_ct(CT_PHYSICAL_BRIDGE)
    effective = tuple(
        CT_ENDPOINT_CENTRAL[index] ** 2 * CT_PHYSICAL_BRIDGE[index]
        for index in range(3)
    )
    assert effective == CT_EFFECTIVE_BRIDGE[1:]

    endpoint = endpoint_matrix(TYPE48, edges, CFN_DELTAS)
    blocks = crossing_blocks(endpoint, endpoint, CT_EFFECTIVE_BRIDGE)
    block_ranks = [rank(block) for block in blocks]
    assert block_ranks == [4, 3, 4, 4]
    assert sum(block_ranks) == 15
    assert principal_projection_rank(blocks, C) == 2
    assert principal_projection_rank(blocks, G) == 4
    assert principal_projection_rank(blocks, T) == 4

    block_determinants = [determinant(block) for block in blocks]
    assert block_determinants[0] and not block_determinants[1]
    assert block_determinants[2] and block_determinants[3]
    block1_minor = determinant([[blocks[1][i][j] for j in (0, 2, 3)] for i in (0, 2, 3)])
    assert block1_minor == Fraction(109444956179346849, 21525608961378488554199449600000)

    # Explicit nonzero 5x5 block-diagonal minor: all of block 0 and the
    # (0,0) entry of block 1.
    five_minor = block_determinants[0] * blocks[1][0][0]
    assert five_minor

    normalized_old = tuple(eigenvalues[1:] for eigenvalues in edges)
    graph_physical = physical_graph_realization(
        corrected,
        normalized_old,
        CT_ENDPOINT_CENTRAL,
        Fraction(19, 20),
        require_ct=True,
    )

    return {
        "status": "FULL_K3P_WITNESS_SEPARATES_NONCUT",
        "extension": "noncentral rows (c,1/4,1/4); normalized central row identity",
        "physical_endpoint_central_triple_each_side": [ftext(value) for value in CT_ENDPOINT_CENTRAL],
        "physical_bridge_triple": [ftext(value) for value in CT_PHYSICAL_BRIDGE],
        "effective_bridge_triple": [ftext(value) for value in CT_EFFECTIVE_BRIDGE[1:]],
        "all_physical_edges_strict_D3_plus": True,
        "all_physical_edges_strict_CT": True,
        "character_block_ranks": block_ranks,
        "full_fourier_flattening_rank": sum(block_ranks),
        "block_determinant_sha256": [fraction_digest(value) for value in block_determinants],
        "block_1_nonzero_3x3_minor": ftext(block1_minor),
        "nonzero_5x5_minor": ftext(five_minor),
        "nonzero_5x5_minor_sha256": fraction_digest(five_minor),
        "nonzero_5x5_minor_numerator_bits": five_minor.numerator.bit_length(),
        "nonzero_5x5_minor_denominator_bits": five_minor.denominator.bit_length(),
        "order_two_projection_ranks": {
            "{0,C}": principal_projection_rank(blocks, C),
            "{0,G}": principal_projection_rank(blocks, G),
            "{0,T}": principal_projection_rank(blocks, T),
        },
        "literal_graph_physicalization": graph_physical,
    }, blocks


def joint_projection_counterexample(corrected: dict) -> dict:
    edge_fourier = []
    normalized_triples = []
    for raw in JOINT_EDGE_TRIPLES_RAW:
        if raw is None:
            triple = (Fraction(1), Fraction(1), Fraction(1))
            edge_fourier.append((Fraction(1),) * 4)
        else:
            triple = tuple(Fraction(value, 1000) for value in raw)
            assert_d3_plus(triple)
            edge_fourier.append((Fraction(1),) + triple)
        normalized_triples.append(triple)
    endpoint = endpoint_matrix(TYPE48, tuple(edge_fourier), JOINT_DELTAS)
    ratios = []
    for character in (C, G, T):
        a = endpoint[character][character]
        b = endpoint[character][ZERO]
        c = endpoint[ZERO][character]
        ratio = a / (b * c)
        assert 0 < ratio < 1
        ratios.append(ratio)
    bridge = (Fraction(1),) + tuple(ratios)
    assert_d3_plus(tuple(ratios))
    blocks = crossing_blocks(endpoint, endpoint, bridge)
    projection_ranks = {character: principal_projection_rank(blocks, character) for character in (C, G, T)}
    assert projection_ranks == {C: 2, G: 2, T: 2}
    block_ranks = [rank(block) for block in blocks]
    assert block_ranks == [4, 4, 4, 4]

    endpoint_central = (Fraction(9, 10),) * 3
    physical_bridge = tuple(value / Fraction(81, 100) for value in ratios)
    assert_d3_plus(endpoint_central)
    assert_d3_plus(physical_bridge)
    graph_physical = physical_graph_realization(
        corrected,
        tuple(normalized_triples),
        endpoint_central,
        Fraction(999, 1000),
        require_ct=False,
    )

    return {
        "status": "ALL_THREE_ORDER_TWO_PROJECTIONS_DROP_BUT_FULL_K3P_DOES_NOT",
        "inheritance_deltas": [ftext(value) for value in JOINT_DELTAS],
        "effective_bridge_triple": [ftext(value) for value in ratios],
        "effective_bridge_D3_plus_margins": [ftext(value) for value in d3_margins(tuple(ratios))],
        "physical_endpoint_central_triple_each_side": [ftext(value) for value in endpoint_central],
        "physical_bridge_triple": [ftext(value) for value in physical_bridge],
        "all_physical_edges_strict_D3_plus": True,
        "projection_ranks": {"{0,C}": 2, "{0,G}": 2, "{0,T}": 2},
        "full_character_block_ranks": block_ranks,
        "full_fourier_flattening_rank": sum(block_ranks),
        "literal_graph_physicalization": graph_physical,
    }


SCAN_C_VALUES = (
    Fraction(1, 5),
    Fraction(1, 4),
    Fraction(1, 3),
    Fraction(2, 5),
    Fraction(1, 2),
    Fraction(3, 5),
    Fraction(2, 3),
    Fraction(3, 4),
    Fraction(4, 5),
)
SCAN_AUX = Fraction(1, 5)
SCAN_BRIDGE = (Fraction(1), Fraction(2, 3), SCAN_AUX, SCAN_AUX)


def scan_edge_fourier(type_id: int, tensor: tuple[tuple[int, ...], ...], central: int | None) -> tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...]:
    width = len(tensor[0])
    answer = []
    for edge_index, row in enumerate(tensor):
        if central is not None and row == (central,) * width:
            answer.append((Fraction(1),) * 4)
            continue
        c = SCAN_C_VALUES[(type_id + 2 * edge_index) % len(SCAN_C_VALUES)]
        triple = (c, SCAN_AUX, SCAN_AUX)
        assert_ct(triple)
        answer.append((Fraction(1),) + triple)
    return tuple(answer)


def scan_deltas(width: int) -> tuple[Fraction, ...]:
    assert width in (2, 4)
    return (Fraction(1, 3),) if width == 2 else (Fraction(1, 3), Fraction(2, 5))


def four_port_coordinate(
    tensor: tuple[tuple[int, ...], ...],
    edge_fourier: tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...],
    deltas: tuple[Fraction, ...],
    assignment: tuple[int, int, int, int],
) -> Fraction:
    weights = switching_weights(deltas)
    total = Fraction(0)
    for switching, weight in enumerate(weights):
        term = weight
        for row, eigenvalues in zip(tensor, edge_fourier):
            term *= eigenvalues[xor_on_mask(assignment, row[switching])]
        total += term
    return total


def deterministic_universe_scan(frozen: dict) -> dict:
    started = time.monotonic()
    endpoint_matrices = []
    for type_id, record in enumerate(frozen["endpoint_records"]):
        tensor = ast.literal_eval(record["type_key"])
        width = len(tensor[0])
        assert sum(row == (4,) * width for row in tensor) == 1
        edges = scan_edge_fourier(type_id, tensor, central=4)
        endpoint_matrices.append(endpoint_matrix(tensor, edges, scan_deltas(width)))

    pair_ranks = Counter()
    low_pair = []
    for left_id, left in enumerate(endpoint_matrices):
        for right_id, right in enumerate(endpoint_matrices):
            total_rank = sum(rank(block) for block in crossing_blocks(left, right, SCAN_BRIDGE))
            pair_ranks[total_rank] += 1
            if total_rank <= 4:
                low_pair.append((left_id, right_id, total_rank))
    assert not low_pair
    assert pair_ranks == {16: 31_329}

    single_blob_ranks = Counter()
    low_noncut = []
    for type_id, record in enumerate(frozen["single_blob_records"]):
        tensor = ast.literal_eval(record["type_key"])
        width = len(tensor[0])
        edges = scan_edge_fourier(type_id, tensor, central=None)
        deltas = scan_deltas(width)
        total_rank = 0
        for total in GROUP:
            pairs = tuple((left, right) for left in GROUP for right in GROUP if left ^ right == total)
            block = [
                [four_port_coordinate(tensor, edges, deltas, left + right) for right in pairs]
                for left in pairs
            ]
            total_rank += rank(block)
        classification = record["certificate"]["classification"]
        single_blob_ranks[(classification, total_rank)] += 1
        if classification == "wrong_split_strict" and total_rank <= 4:
            low_noncut.append((type_id, total_rank))
    assert not low_noncut
    assert single_blob_ranks == {
        ("rank_one_all_blocks", 4): 32,
        ("wrong_split_strict", 16): 421,
    }

    return {
        "status": "EXACT_DETERMINISTIC_NO_COUNTEREXAMPLE_SCAN",
        "point_kind": "strict continuous-time rational",
        "endpoint_types": len(endpoint_matrices),
        "ordered_endpoint_pairs": 31_329,
        "endpoint_pair_rank_distribution": {str(key): value for key, value in sorted(pair_ranks.items())},
        "single_blob_types": 453,
        "single_blob_rank_distribution": {
            f"{classification}:rank{value_rank}": count
            for (classification, value_rank), count in sorted(single_blob_ranks.items())
        },
        "noncut_rank_at_most_four_found": 0,
        "seconds": round(time.monotonic() - started, 3),
        "scope": "one deterministic exact point per frozen type/pair; falsification evidence, not pointwise proof",
    }


def boundary_checks() -> dict:
    strict = endpoint_matrix(TYPE48, ct_edge_fourier(), CFN_DELTAS)
    identity_edges = tuple((Fraction(1),) * 4 for _row in TYPE48)
    identity_endpoint = endpoint_matrix(TYPE48, identity_edges, CFN_DELTAS)
    identity_blocks = crossing_blocks(identity_endpoint, identity_endpoint, (Fraction(1),) * 4)
    strict_inheritance_zero = endpoint_matrix(TYPE48, ct_edge_fourier(), (Fraction(0), Fraction(1, 2)))
    inheritance_zero_blocks = crossing_blocks(strict_inheritance_zero, strict_inheritance_zero, CT_EFFECTIVE_BRIDGE)
    identity_bridge_blocks = crossing_blocks(strict, strict, (Fraction(1),) * 4)
    results = {
        "all_edge_identity_boundary": [rank(block) for block in identity_blocks],
        "inheritance_delta0_zero_boundary": [rank(block) for block in inheritance_zero_blocks],
        "effective_bridge_identity_boundary": [rank(block) for block in identity_bridge_blocks],
    }
    assert results == {
        "all_edge_identity_boundary": [1, 1, 1, 1],
        "inheritance_delta0_zero_boundary": [4, 4, 4, 4],
        "effective_bridge_identity_boundary": [4, 4, 4, 4],
    }
    return {
        "status": "BOUNDARY_CASES_CHECKED",
        "character_block_ranks": results,
        "interpretation": "rank four occurs at the excluded all-identity edge boundary; two other sampled boundary faces remain full rank",
    }


def mutation_suite(frozen: dict, corrected: dict) -> dict:
    detected = []

    def reject(name: str, callback) -> None:
        try:
            callback()
        except (AssertionError, KeyError, ValueError, TypeError, IndexError):
            detected.append(name)
            return
        raise AssertionError(f"mutation survived: {name}")

    reject("frozen_byte_flip", lambda: (_ for _ in ()).throw(AssertionError()) if sha256_bytes(FROZEN.read_bytes()[:-1] + b"X") != FROZEN_SHA256 else None)

    def bad_type_mask() -> None:
        changed = [list(row) for row in TYPE48]
        changed[0][0] = 1
        assert tuple(tuple(row) for row in changed) == TYPE48

    reject("type48_descendant_mask", bad_type_mask)

    def bad_record_index() -> None:
        assert ast.literal_eval(frozen["endpoint_records"][47]["type_key"]) == TYPE48

    reject("type48_record_index", bad_record_index)

    def bad_c_parameter() -> None:
        changed = list(CFN_C)
        changed[0] = Fraction(2, 3)
        edge = tuple((Fraction(1), value, Fraction(1), Fraction(1)) for value in changed)
        matrix = endpoint_matrix(TYPE48, edge, CFN_DELTAS)
        assert (matrix[C][C], matrix[C][ZERO], matrix[ZERO][C]) == (CFN_A, CFN_B, CFN_C_COORD)

    reject("CFN_edge_parameter", bad_c_parameter)

    def bad_inheritance() -> None:
        edge = tuple((Fraction(1), value, Fraction(1), Fraction(1)) for value in CFN_C)
        matrix = endpoint_matrix(TYPE48, edge, (Fraction(1, 5), Fraction(2, 5)))
        assert (matrix[C][C], matrix[C][ZERO], matrix[ZERO][C]) == (CFN_A, CFN_B, CFN_C_COORD)

    reject("CFN_inheritance", bad_inheritance)

    def bad_z() -> None:
        edge = tuple((Fraction(1), value, Fraction(1), Fraction(1)) for value in CFN_C)
        matrix = endpoint_matrix(TYPE48, edge, CFN_DELTAS)
        blocks = crossing_blocks(matrix, matrix, (Fraction(1), CFN_EFFECTIVE_Z + Fraction(1, 1000), Fraction(1), Fraction(1)))
        assert determinant([[blocks[0][i][j] for j in (0, 1)] for i in (0, 1)]) == 0

    reject("CFN_effective_bridge", bad_z)

    def bad_central_normalization() -> None:
        edge = list(tuple((Fraction(1), value, Fraction(1), Fraction(1)) for value in CFN_C))
        edge[CENTRAL_ROW] = (Fraction(1), Fraction(9, 10), Fraction(1), Fraction(1))
        matrix = endpoint_matrix(TYPE48, tuple(edge), CFN_DELTAS)
        assert matrix[C][ZERO] == CFN_B

    reject("central_normalization", bad_central_normalization)

    def bad_corrected_record() -> None:
        candidate = corrected["three_port_endpoint_dichotomy"]["records"][25]
        assert normalize_tensor(tuple(tuple(row) for row in candidate["signatures"]), 3) == normalize_tensor(TYPE48, 3)

    reject("corrected_graph_record_binding", bad_corrected_record)

    def bad_graph_arc() -> None:
        candidate = json.loads(json.dumps(corrected["three_port_endpoint_dichotomy"]["records"][26]))
        candidate["witness_graph"]["arcs"][0] = ["V", "U"]
        verify_rooted_graph_and_masks(candidate)

    reject("literal_graph_arc", bad_graph_arc)

    def bad_physical_bridge() -> None:
        changed = (CT_PHYSICAL_BRIDGE[0] + Fraction(1, 1000), CT_AUX, CT_AUX)
        effective = tuple(CT_ENDPOINT_CENTRAL[index] ** 2 * changed[index] for index in range(3))
        assert effective == CT_EFFECTIVE_BRIDGE[1:]

    reject("K3P_physical_bridge", bad_physical_bridge)

    def nonphysical_edge() -> None:
        assert_d3_plus((Fraction(9, 10), Fraction(9, 10), Fraction(1, 10)))

    reject("D3_plus_inequality", nonphysical_edge)

    def bad_full_entry() -> None:
        endpoint = endpoint_matrix(TYPE48, ct_edge_fourier(), CFN_DELTAS)
        blocks = list(crossing_blocks(endpoint, endpoint, CT_EFFECTIVE_BRIDGE))
        blocks[0][0][0] += Fraction(1, 10_000)
        assert [rank(block) for block in blocks] == [4, 3, 4, 4]
        # Rank happens to remain unchanged; require the sealed determinant too.
        assert fraction_digest(determinant(blocks[0])) == "98fa7de82716bae2db991008d6ee195c46d93863fc178602c9aa087ae2414637"

    reject("full_K3P_flattening_entry", bad_full_entry)

    def joint_bridge_mutation() -> None:
        report = joint_projection_counterexample(corrected)
        changed = Fraction(report["effective_bridge_triple"][0]) + Fraction(1, 1000)
        assert changed == Fraction(report["effective_bridge_triple"][0])

    reject("joint_projection_bridge", joint_bridge_mutation)

    assert len(detected) == 13
    return {"status": "ALL_MUTATIONS_DETECTED", "count": len(detected), "detected": detected}


def generic_repair_statement() -> dict:
    return {
        "status": "RIGOROUS_GENERIC_REPAIR_ONLY",
        "argument": [
            "For a fixed topology and split, every 5x5 Fourier-flattening minor is a polynomial in K3P Fourier edge parameters and inheritance parameters.",
            "If the split is a cut, all such minors vanish identically by the four character-sector rank-one factorization.",
            "If the split is noncut, restrict to the isotropic slice (c_e,g_e,t_e)=(r_e,r_e,r_e), 0<r_e<1. This slice lies in strict D3_plus and strict CT and is exactly the JC model.",
            "The corrected JC pointwise cut theorem supplies a nonzero 5x5 minor at every strict isotropic point; hence at least one K3P minor polynomial is not identically zero.",
            "Therefore rank<=4 characterizes cuts outside a proper algebraic exceptional set for each fixed K3P topology.",
        ],
        "does_not_prove": "the pointwise noncut rank lower bound at every strict K3P parameter point",
        "containment_scope_warning": "generic nonvanishing immediately gives target-cut implies source-cut under source-open containment; the reverse cut inclusion still needs a pointwise target obstruction or a separate dimension/positivity argument",
    }


def build_report(full_scan: bool) -> dict:
    frozen, corrected, provenance = bind_provenance()
    binding, graph = verify_type48_binding(frozen, corrected)
    cfn, _cfn_endpoint, _cfn_blocks = cfn_counterexample()
    full_k3p, _full_blocks = verify_full_k3p_type48(corrected)
    joint = joint_projection_counterexample(corrected)
    report = {
        "schema": "k3p-cut-transfer-adversarial-audit-v1",
        "status": "SHORTCUT_INVALID_ONLY",
        "verdict": "shortcut invalid only",
        "qualification": "No strict full-K3P cut-recovery counterexample was found. The available evidence repairs generic cut recovery, but does not certify the claimed pointwise theorem throughout D3_plus.",
        "provenance": provenance,
        "type48_binding": binding,
        "literal_graph_reconstruction": graph,
        "one_character_counterexample": cfn,
        "full_K3P_same_literal_witness": full_k3p,
        "all_three_projection_counterexample": joint,
        "boundary_checks": boundary_checks(),
        "generic_repair": generic_repair_statement(),
    }
    if full_scan:
        report["deterministic_universe_scan"] = deterministic_universe_scan(frozen)
    else:
        report["deterministic_universe_scan"] = {"status": "SKIPPED_BY_QUICK_FLAG"}
    report["mutations"] = mutation_suite(frozen, corrected)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="skip the deterministic 31,329-pair/453-type scan")
    parser.add_argument("--check-audit-json", action="store_true", help="compare substantive fields with the sealed audit JSON")
    arguments = parser.parse_args()
    report = build_report(full_scan=not arguments.quick)
    if arguments.check_audit_json:
        sealed = json.loads((HERE / "CUT_TRANSFER_ADVERSARIAL_AUDIT.json").read_text())

        def assert_subset(expected, observed, location="$") -> None:
            if isinstance(expected, dict):
                assert isinstance(observed, dict), location
                for key, value in expected.items():
                    assert key in observed, f"{location}.{key}"
                    assert_subset(value, observed[key], f"{location}.{key}")
            elif isinstance(expected, list):
                assert expected == observed, location
            else:
                assert expected == observed, location

        assert_subset(sealed, report)
    json.dump(report, sys.stdout, indent=2, sort_keys=True)
    print()


if __name__ == "__main__":
    main()
