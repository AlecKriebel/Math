#!/usr/bin/env python3
"""Independent audit of the regular-d18 endpoint capacity obstruction.

The mathematical reconstruction in this module is deliberately self-contained
and does not import the certificate producer.  At the regular degree-18
endpoint, let A be the root neighborhood and let H be the complement of the
root antineighborhood.  For an H vertex h, regularity fixes the size of its
cross-neighborhood X_h in A to

    |X_h| = degree_H(h) - 5.

Every X_h must hit every independent four-set of A.  For an exact size s,
define q_s(A) as the minimum number of independent triples of A missed by such
a transversal.  Double-counting pairs (h,Q), where Q is an independent triple
missed by X_h, gives the necessary inequality

    sum_h q_{degree_H(h)-5}(A) <= 4 * i_3(A).

The factor four is local and exact: vertices of H missing a fixed independent
triple Q must form an independent set in H, while H has independence number at
most four.

The checker exhaustively reconstructs q_s(A) for every published A record and
the degree data for every selected H record.  Equality survivors are closed by
the unique size-six minimizer for the exceptional A record together with an
H-edge whose endpoints both have cross-neighborhood size six.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import re
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence


CHECKER_SCHEMA = (
    "ramsey55.branch18_regular_endpoint_capacity_cover_checker.v1"
)
DEFAULT_ROOT = Path(__file__).resolve().parents[1]

A_RELATIVE = "data/r45extreme/r4518.85.g6"
H_RELATIVE = "data/r45_24.g6"
A_SHA256 = "46abaee2572d06bba1e594554809d784be60f8f60b9b0d3345b8bf3dd800810a"
H_SHA256 = "83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0"
A_BYTES = 2_072
H_BYTES = 16_913_568
A_RECORDS = 74
H_RECORDS = 352_366
H_SELECTED = 843
A_ORDER = 18
H_ORDER = 24
A_EDGES = 85
H_EDGES = 128
SIZE_MIN = 3
SIZE_MAX = 7
PAIR_COUNT = A_RECORDS * H_SELECTED
EXPECTED_CAPACITY_EXCLUSIONS = 61_939
EXPECTED_EQUALITY_SURVIVORS = 443
EXPECTED_TERMINAL_EXCLUSIONS = 443
EXPECTED_EXCEPTIONAL_A = 50

MANIFEST_SCHEMA = (
    "ramsey55.branch18_regular_endpoint_capacity_cover.v1"
)
CLASSIFICATION_SCHEMA = (
    "ramsey55.branch18_regular_endpoint_capacity_classifications.v1"
)
EXPECTED_STATUS = (
    "EXACT_EXCLUSION_OF_REGULAR_D18_E85_E128_ENDPOINT_"
    "CONDITIONAL_ON_PUBLISHED_CATALOG_COMPLETENESS"
)
EXPECTED_H_SELECTED_LINE_SHA256 = (
    "344eadae59880c8c3a815add0e1ac4861236c5de9eb3949446262b539c940524"
)
EXPECTED_THEOREM = {
    "ambient_order": 43,
    "global_regular_degree": 18,
    "root_degree": 18,
    "A_definition": "root neighborhood",
    "A_order": 18,
    "A_edge_count": 85,
    "H_definition": "complement of the root antineighborhood",
    "H_order": 24,
    "H_edge_count": 128,
    "cross_size_identity": (
        "|X_b|=|N_G(b) intersect A|=degree_H(b)-5"
    ),
    "single_column_condition": (
        "Every X_b hits every independent four-set of A."
    ),
    "capacity_definition": (
        "q_s(A) is the minimum number of independent triples "
        "of A disjoint from an exact-size-s independent-four-"
        "set transversal X."
    ),
    "capacity_bound": (
        "For every independent triple Q of A, the H vertices "
        "whose X_b misses Q form an H-independent set of size "
        "at most four; hence sum_b q_{degree_H(b)-5}(A) "
        "<= 4*i_3(A)."
    ),
    "two_column_condition": (
        "For every H-edge uv, X_u union X_v hits every "
        "independent triple of A."
    ),
}
EXPECTED_CLAIM_BOUNDARY = (
    "This locally excludes all 62,382 fixed-side pairs only at "
    "the regular degree-18 endpoint e(A)=85,e(H)=128. Catalog "
    "completeness and pairwise nonisomorphism are inherited "
    "from the publisher. It does not exclude e(A)=81 through "
    "84, the remainder of the regular degree-18 branch, any "
    "other one of the six global branches, or arbitrary "
    "order-43 graphs. No Ramsey-bound change follows by itself."
)
EXPECTED_EXECUTION = {
    "solver_calls": 0,
    "proof_jobs": 0,
    "formulas_materialized": 0,
    "classification_records_materialized": PAIR_COUNT,
}
CAPACITY_INF_RE = re.compile(
    rb"A=(\d{2}) H=(\d{3}) L=(\d{6}) C=CAP "
    rb"LB=INF UB=(\d{3}) S=(\d)\n"
)
CAPACITY_FINITE_RE = re.compile(
    rb"A=(\d{2}) H=(\d{3}) L=(\d{6}) C=CAP "
    rb"LB=(\d{4}) UB=(\d{3}) D=(\d{4})\n"
)
TERMINAL_RE = re.compile(
    rb"A=(\d{2}) H=(\d{3}) L=(\d{6}) C=TERM "
    rb"LB=(\d{4}) UB=(\d{3}) E=(\d{2}),(\d{2}) "
    rb"Q=(\d{2}),(\d{2}),(\d{2})\n"
)


@dataclass(frozen=True)
class Minimum:
    size: int
    candidate_count: int
    value: int | None
    minimizers: tuple[int, ...]


@dataclass(frozen=True)
class AProfile:
    index: int
    record: bytes
    adjacency: tuple[int, ...]
    independent3: tuple[int, ...]
    independent4: tuple[int, ...]
    minima: tuple[Minimum, ...]

    def minimum(self, size: int) -> Minimum:
        if not SIZE_MIN <= size <= SIZE_MAX:
            raise ValueError("capacity size outside 3..7")
        return self.minima[size - SIZE_MIN]


@dataclass(frozen=True)
class HProfile:
    index: int
    source_line: int
    record: bytes
    adjacency: tuple[int, ...]
    degrees: tuple[int, ...]
    size_histogram: tuple[int, ...]

    def size_count(self, size: int) -> int:
        if not SIZE_MIN <= size <= SIZE_MAX:
            raise ValueError("cross-neighborhood size outside 3..7")
        return self.size_histogram[size - SIZE_MIN]


@dataclass(frozen=True)
class CapacityDecision:
    kind: str
    lower_bound: int | None
    capacity: int
    margin: int | None
    impossible_size: int | None


@dataclass(frozen=True)
class TerminalWitness:
    high_edge: tuple[int, int]
    forced_minimizer: int
    missed_independent_triple: int


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, separators=(",", ": "))
        + "\n"
    ).encode("utf-8")


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_canonical_json(payload: bytes) -> object:
    value = json.loads(
        payload.decode("utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    if canonical_json(value) != payload:
        raise ValueError("JSON is not in the canonical encoding")
    return value


def confined_path(root: Path, value: str | Path) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        resolved = candidate.resolve()
    else:
        if any(part == ".." for part in candidate.parts):
            raise ValueError("path traversal is forbidden")
        resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("path resolves outside the research root") from exc
    return resolved


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def decode_graph6(record: bytes, expected_order: int) -> tuple[int, ...]:
    """Decode canonical short graph6 using an explicit bit string."""
    if not record or record[0] - 63 != expected_order:
        raise ValueError("graph6 order mismatch")
    needed = expected_order * (expected_order - 1) // 2
    payload_length = (needed + 5) // 6
    if len(record) != payload_length + 1:
        raise ValueError("noncanonical graph6 length")
    values = [character - 63 for character in record[1:]]
    if any(value < 0 or value > 63 for value in values):
        raise ValueError("invalid graph6 byte")
    bits = "".join(f"{value:06b}" for value in values)
    if "1" in bits[needed:]:
        raise ValueError("nonzero graph6 padding")
    adjacency = [0] * expected_order
    cursor = 0
    for right in range(1, expected_order):
        for left in range(right):
            if bits[cursor] == "1":
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1
    if cursor != needed:
        raise AssertionError("graph6 traversal mismatch")
    return tuple(adjacency)


def edge_count(adjacency: Sequence[int]) -> int:
    degree_sum = sum(neighbors.bit_count() for neighbors in adjacency)
    if degree_sum % 2:
        raise ValueError("odd degree sum")
    return degree_sum // 2


def complement(adjacency: Sequence[int]) -> tuple[int, ...]:
    full = (1 << len(adjacency)) - 1
    return tuple(
        full ^ neighbors ^ (1 << vertex)
        for vertex, neighbors in enumerate(adjacency)
    )


def has_clique(adjacency: Sequence[int], target: int) -> bool:
    if target < 0:
        raise ValueError("negative clique target")
    if target == 0:
        return True
    stack: list[tuple[int, int]] = [
        ((1 << len(adjacency)) - 1, target)
    ]
    while stack:
        candidates, remaining = stack.pop()
        while candidates.bit_count() >= remaining:
            chosen = candidates & -candidates
            candidates ^= chosen
            vertex = chosen.bit_length() - 1
            if remaining == 1:
                return True
            stack.append(
                (candidates & adjacency[vertex], remaining - 1)
            )
    return False


def validate_r45(
    adjacency: Sequence[int], expected_edges: int, label: str
) -> None:
    if edge_count(adjacency) != expected_edges:
        raise ValueError(f"{label} edge count mismatch")
    if has_clique(adjacency, 4):
        raise ValueError(f"{label} contains K4")
    if has_clique(complement(adjacency), 5):
        raise ValueError(f"{label} contains I5")


def independent_masks(
    adjacency: Sequence[int], size: int
) -> tuple[int, ...]:
    result: list[int] = []
    for vertices in itertools.combinations(range(len(adjacency)), size):
        mask = sum(1 << vertex for vertex in vertices)
        if all(adjacency[vertex] & mask == 0 for vertex in vertices):
            result.append(mask)
    return tuple(result)


def vertices(mask: int, order: int) -> list[int]:
    return [vertex for vertex in range(order) if mask & (1 << vertex)]


def hits_every(mask: int, family: Sequence[int]) -> bool:
    return all(mask & member for member in family)


def minimizer_line(size: int, mask: int) -> bytes:
    encoded = ",".join(
        f"{vertex:02d}" for vertex in vertices(mask, A_ORDER)
    )
    return f"s={size} X={encoded}\n".encode("ascii")


def minimizer_stream_sha256(minimum: Minimum) -> str | None:
    if minimum.value is None:
        if minimum.minimizers:
            raise AssertionError("infinite minimum has minimizers")
        return None
    return sha256(
        b"".join(
            minimizer_line(minimum.size, mask)
            for mask in minimum.minimizers
        )
    )


def a_profile_line(profile: AProfile) -> bytes:
    fields = [
        f"A={profile.index:02d}",
        f"I3={len(profile.independent3):03d}",
        f"I4={len(profile.independent4):03d}",
    ]
    for minimum in profile.minima:
        value = (
            "INF"
            if minimum.value is None
            else f"{minimum.value:03d}"
        )
        fields.append(
            f"S{minimum.size}={value}/"
            f"{minimum.candidate_count:05d}/"
            f"{len(minimum.minimizers):05d}/"
            f"{minimizer_stream_sha256(minimum) or '-'}"
        )
    return (" ".join(fields) + "\n").encode("ascii")


def degree_histogram_key(degrees: Sequence[int]) -> str:
    histogram = Counter(degrees)
    return ",".join(
        f"{degree}^{histogram[degree]}" for degree in sorted(histogram)
    )


def reconstruct_minimum(
    independent3: Sequence[int],
    independent4: Sequence[int],
    size: int,
) -> Minimum:
    candidate_count = 0
    minimum: int | None = None
    minimizers: list[int] = []
    for chosen in itertools.combinations(range(A_ORDER), size):
        mask = sum(1 << vertex for vertex in chosen)
        if not hits_every(mask, independent4):
            continue
        candidate_count += 1
        missed = sum(1 for triple in independent3 if mask & triple == 0)
        if minimum is None or missed < minimum:
            minimum = missed
            minimizers = [mask]
        elif missed == minimum:
            minimizers.append(mask)
    if (minimum is None) != (not minimizers):
        raise AssertionError("minimum/minimizer consistency failure")
    return Minimum(
        size=size,
        candidate_count=candidate_count,
        value=minimum,
        minimizers=tuple(minimizers),
    )


def reconstruct_a_record(record: bytes, index: int) -> AProfile:
    adjacency = decode_graph6(record, A_ORDER)
    validate_r45(adjacency, A_EDGES, f"A[{index}]")
    independent3 = independent_masks(adjacency, 3)
    independent4 = independent_masks(adjacency, 4)
    minima = tuple(
        reconstruct_minimum(independent3, independent4, size)
        for size in range(SIZE_MIN, SIZE_MAX + 1)
    )
    return AProfile(
        index=index,
        record=record,
        adjacency=adjacency,
        independent3=independent3,
        independent4=independent4,
        minima=minima,
    )


def reconstruct_h_record(
    record: bytes, index: int, source_line: int
) -> HProfile:
    adjacency = decode_graph6(record, H_ORDER)
    validate_r45(adjacency, H_EDGES, f"H[{index}]")
    degrees = tuple(neighbors.bit_count() for neighbors in adjacency)
    sizes = tuple(degree - 5 for degree in degrees)
    if min(sizes) < SIZE_MIN or max(sizes) > SIZE_MAX:
        raise ValueError("selected H has cross size outside 3..7")
    histogram = Counter(sizes)
    return HProfile(
        index=index,
        source_line=source_line,
        record=record,
        adjacency=adjacency,
        degrees=degrees,
        size_histogram=tuple(
            histogram[size] for size in range(SIZE_MIN, SIZE_MAX + 1)
        ),
    )


def read_catalog(
    path: Path,
    expected_bytes: int,
    expected_hash: str,
    expected_records: int,
) -> tuple[bytes, list[bytes]]:
    payload = path.read_bytes()
    if len(payload) != expected_bytes:
        raise ValueError(f"catalog byte count mismatch: {path}")
    if sha256(payload) != expected_hash:
        raise ValueError(f"catalog digest mismatch: {path}")
    if not payload.endswith(b"\n"):
        raise ValueError(f"catalog lacks final newline: {path}")
    lines = payload.splitlines()
    if len(lines) != expected_records or any(not line for line in lines):
        raise ValueError(f"catalog framing mismatch: {path}")
    if len(set(lines)) != len(lines):
        raise ValueError(f"duplicate graph6 record in catalog: {path}")
    return payload, lines


def reconstruct_catalogs(
    root: Path,
) -> tuple[
    bytes,
    bytes,
    list[AProfile],
    list[HProfile],
    Counter[int],
    str,
]:
    a_payload, a_records = read_catalog(
        confined_path(root, A_RELATIVE),
        A_BYTES,
        A_SHA256,
        A_RECORDS,
    )
    h_payload, h_records = read_catalog(
        confined_path(root, H_RELATIVE),
        H_BYTES,
        H_SHA256,
        H_RECORDS,
    )
    a_profiles = [
        reconstruct_a_record(record, index)
        for index, record in enumerate(a_records)
    ]
    h_profiles: list[HProfile] = []
    full_edge_histogram: Counter[int] = Counter()
    selected_digest = hashlib.sha256()
    for source_line, record in enumerate(h_records, 1):
        adjacency = decode_graph6(record, H_ORDER)
        edges = edge_count(adjacency)
        full_edge_histogram[edges] += 1
        if edges != H_EDGES:
            continue
        selected_digest.update(record + b"\n")
        h_profiles.append(
            reconstruct_h_record(
                record, len(h_profiles), source_line
            )
        )
    if len(h_profiles) != H_SELECTED:
        raise ValueError("edge-128 H selection is not 843 records")
    return (
        a_payload,
        h_payload,
        a_profiles,
        h_profiles,
        full_edge_histogram,
        selected_digest.hexdigest(),
    )


def capacity_decision(a_profile: AProfile, h_profile: HProfile) -> CapacityDecision:
    capacity = 4 * len(a_profile.independent3)
    for size in range(SIZE_MIN, SIZE_MAX + 1):
        minimum = a_profile.minimum(size)
        if h_profile.size_count(size) and minimum.value is None:
            return CapacityDecision(
                kind="STRICT_INFINITE",
                lower_bound=None,
                capacity=capacity,
                margin=None,
                impossible_size=size,
            )
    lower = sum(
        h_profile.size_count(size)
        * int(a_profile.minimum(size).value)
        for size in range(SIZE_MIN, SIZE_MAX + 1)
        if h_profile.size_count(size)
    )
    if lower > capacity:
        return CapacityDecision(
            kind="STRICT_FINITE",
            lower_bound=lower,
            capacity=capacity,
            margin=lower - capacity,
            impossible_size=None,
        )
    if lower == capacity:
        return CapacityDecision(
            kind="EQUALITY",
            lower_bound=lower,
            capacity=capacity,
            margin=0,
            impossible_size=None,
        )
    return CapacityDecision(
        kind="SLACK",
        lower_bound=lower,
        capacity=capacity,
        margin=lower - capacity,
        impossible_size=None,
    )


def first_high_edge(
    h_profile: HProfile, minimum_size: int = 6
) -> tuple[int, int] | None:
    for left in range(H_ORDER):
        if h_profile.degrees[left] - 5 < minimum_size:
            continue
        for right in range(left + 1, H_ORDER):
            if h_profile.degrees[right] - 5 < minimum_size:
                continue
            if h_profile.adjacency[left] & (1 << right):
                return left, right
    return None


def first_same_degree_edge_and_internal_minimum(
    h_profile: HProfile, degree: int
) -> tuple[tuple[int, int], int]:
    high = tuple(
        vertex
        for vertex, actual_degree in enumerate(h_profile.degrees)
        if actual_degree == degree
    )
    if not high:
        raise ValueError("H profile has no requested high-degree vertices")
    high_mask = sum(1 << vertex for vertex in high)
    internal_degrees = tuple(
        (h_profile.adjacency[vertex] & high_mask).bit_count()
        for vertex in high
    )
    for left in high:
        candidates = h_profile.adjacency[left] & high_mask
        candidates &= ~((1 << (left + 1)) - 1)
        if candidates:
            right_bit = candidates & -candidates
            return (
                (left, right_bit.bit_length() - 1),
                min(internal_degrees),
            )
    raise ValueError("H profile has no same-degree high edge")


def terminal_witness(
    a_profile: AProfile, h_profile: HProfile
) -> TerminalWitness:
    decision = capacity_decision(a_profile, h_profile)
    if decision.kind != "EQUALITY":
        raise ValueError("terminal witness requires capacity equality")
    q6 = a_profile.minimum(6)
    if q6.value is None or q6.value <= 0:
        raise ValueError("size-six minimum is not positive")
    if len(q6.minimizers) != 1:
        raise ValueError("size-six capacity minimizer is not unique")
    edge = first_high_edge(h_profile, 6)
    if edge is None:
        raise ValueError("equality H record has no high-high edge")
    left, right = edge
    if (
        h_profile.degrees[left] - 5 != 6
        or h_profile.degrees[right] - 5 != 6
    ):
        raise ValueError("terminal high-high edge is not size 6--6")
    minimizer = q6.minimizers[0]
    missed = next(
        (
            triple
            for triple in a_profile.independent3
            if minimizer & triple == 0
        ),
        None,
    )
    if missed is None:
        raise ValueError("positive q6 has no missed independent triple")
    return TerminalWitness(
        high_edge=edge,
        forced_minimizer=minimizer,
        missed_independent_triple=missed,
    )


def reconstruct_classification(
    a_profiles: Sequence[AProfile],
    h_profiles: Sequence[HProfile],
) -> dict[str, object]:
    kind_histogram: Counter[str] = Counter()
    finite_margin_histogram: Counter[int] = Counter()
    infinite_size_histogram: Counter[int] = Counter()
    capacity_by_a: Counter[int] = Counter()
    capacity_by_h: Counter[int] = Counter()
    equality_pairs: list[tuple[int, int, CapacityDecision]] = []
    terminal_witnesses: list[
        tuple[int, int, TerminalWitness]
    ] = []
    for h_profile in h_profiles:
        for a_profile in a_profiles:
            decision = capacity_decision(a_profile, h_profile)
            kind_histogram[decision.kind] += 1
            if decision.kind == "STRICT_INFINITE":
                assert decision.impossible_size is not None
                infinite_size_histogram[decision.impossible_size] += 1
                capacity_by_a[a_profile.index] += 1
                capacity_by_h[h_profile.index] += 1
            elif decision.kind == "STRICT_FINITE":
                assert decision.margin is not None
                finite_margin_histogram[decision.margin] += 1
                capacity_by_a[a_profile.index] += 1
                capacity_by_h[h_profile.index] += 1
            elif decision.kind == "EQUALITY":
                equality_pairs.append(
                    (a_profile.index, h_profile.index, decision)
                )
                terminal_witnesses.append(
                    (
                        a_profile.index,
                        h_profile.index,
                        terminal_witness(a_profile, h_profile),
                    )
                )
            else:
                equality_pairs.append(
                    (a_profile.index, h_profile.index, decision)
                )
    strict_count = (
        kind_histogram["STRICT_INFINITE"]
        + kind_histogram["STRICT_FINITE"]
    )
    terminal_count = len(terminal_witnesses)
    return {
        "kind_histogram": kind_histogram,
        "finite_margin_histogram": finite_margin_histogram,
        "infinite_size_histogram": infinite_size_histogram,
        "capacity_by_a": capacity_by_a,
        "capacity_by_h": capacity_by_h,
        "strict_count": strict_count,
        "equality_pairs": equality_pairs,
        "terminal_witnesses": terminal_witnesses,
        "terminal_count": terminal_count,
    }


def capacity_line(
    a_profile: AProfile,
    h_profile: HProfile,
    decision: CapacityDecision,
) -> bytes:
    prefix = (
        f"A={a_profile.index:02d} H={h_profile.index:03d} "
        f"L={h_profile.source_line:06d} C=CAP "
    )
    if decision.kind == "STRICT_INFINITE":
        if decision.impossible_size is None:
            raise AssertionError("infinite decision lacks impossible size")
        return (
            prefix
            + f"LB=INF UB={decision.capacity:03d} "
            + f"S={decision.impossible_size}\n"
        ).encode("ascii")
    if (
        decision.kind != "STRICT_FINITE"
        or decision.lower_bound is None
        or decision.margin is None
        or decision.margin <= 0
    ):
        raise ValueError("capacity line requires a strict exclusion")
    return (
        prefix
        + f"LB={decision.lower_bound:04d} "
        + f"UB={decision.capacity:03d} "
        + f"D={decision.margin:04d}\n"
    ).encode("ascii")


def terminal_line(
    a_profile: AProfile,
    h_profile: HProfile,
    decision: CapacityDecision,
    edge: tuple[int, int],
    triple: tuple[int, int, int],
) -> bytes:
    if decision.kind != "EQUALITY" or decision.lower_bound is None:
        raise ValueError("terminal line requires capacity equality")
    return (
        f"A={a_profile.index:02d} H={h_profile.index:03d} "
        f"L={h_profile.source_line:06d} C=TERM "
        f"LB={decision.lower_bound:04d} UB={decision.capacity:03d} "
        f"E={edge[0]:02d},{edge[1]:02d} "
        f"Q={triple[0]:02d},{triple[1]:02d},{triple[2]:02d}\n"
    ).encode("ascii")


def reconstruct_classification_stream(
    a_profiles: Sequence[AProfile],
    h_profiles: Sequence[HProfile],
    stream_path: str,
) -> tuple[bytes, dict[str, object], dict[str, object]]:
    """Independently reconstruct the canonical A-major pair stream."""
    chunks: list[bytes] = []
    terminal_hasher = hashlib.sha256()
    capacity_count = 0
    terminal_count = 0
    finite_margins: Counter[int] = Counter()
    infinite_sizes: Counter[int] = Counter()
    terminal_internal_minima: Counter[int] = Counter()
    terminal_h_indices: list[int] = []
    surviving_a: set[int] = set()
    surviving_h: set[int] = set()

    for a_profile in a_profiles:
        for h_profile in h_profiles:
            decision = capacity_decision(a_profile, h_profile)
            if decision.kind in {"STRICT_INFINITE", "STRICT_FINITE"}:
                line = capacity_line(a_profile, h_profile, decision)
                capacity_count += 1
                if decision.kind == "STRICT_INFINITE":
                    assert decision.impossible_size is not None
                    infinite_sizes[decision.impossible_size] += 1
                else:
                    assert decision.margin is not None
                    finite_margins[decision.margin] += 1
            elif decision.kind == "EQUALITY":
                surviving_a.add(a_profile.index)
                surviving_h.add(h_profile.index)
                witness = terminal_witness(a_profile, h_profile)
                edge, internal_minimum = (
                    first_same_degree_edge_and_internal_minimum(
                        h_profile, 11
                    )
                )
                if edge != witness.high_edge:
                    raise ValueError(
                        "independent terminal edge reconstructions disagree"
                    )
                missed_vertices = vertices(
                    witness.missed_independent_triple, A_ORDER
                )
                if len(missed_vertices) != 3:
                    raise AssertionError("missed triple mask is malformed")
                triple = tuple(missed_vertices)
                line = terminal_line(
                    a_profile,
                    h_profile,
                    decision,
                    edge,
                    triple,
                )
                terminal_hasher.update(line)
                terminal_count += 1
                terminal_h_indices.append(h_profile.index)
                terminal_internal_minima[internal_minimum] += 1
            else:
                raise ValueError(
                    "capacity reconstruction has an unexpected slack pair"
                )
            chunks.append(line)

    payload = b"".join(chunks)
    if (
        len(chunks) != PAIR_COUNT
        or capacity_count != EXPECTED_CAPACITY_EXCLUSIONS
        or terminal_count != EXPECTED_TERMINAL_EXCLUSIONS
        or surviving_a != {EXPECTED_EXCEPTIONAL_A}
        or len(surviving_h) != EXPECTED_EQUALITY_SURVIVORS
        or terminal_h_indices != sorted(terminal_h_indices)
    ):
        raise ValueError("independent endpoint classification census changed")
    classification_summary = {
        "schema": CLASSIFICATION_SCHEMA,
        "path": stream_path,
        "bytes": len(payload),
        "sha256": sha256(payload),
        "record_count": len(chunks),
        "order": "A index major, then H cover index",
        "capacity_line_encoding": (
            "A={a:02d} H={h:03d} L={H_source_line:06d} C=CAP "
            "LB={lower:04d|INF} UB={4*i3:03d} "
            "D={positive_difference:04d}|S={impossible_size}\\n"
        ),
        "terminal_line_encoding": (
            "A=50 H={h:03d} L={H_source_line:06d} C=TERM "
            "LB=0296 UB=296 E={H_edge:02d,02d} "
            "Q={missed_A_I3:02d,02d,02d}\\n"
        ),
        "capacity_exclusion_count": capacity_count,
        "terminal_exclusion_count": terminal_count,
        "retained_pair_count": 0,
        "finite_capacity_margin_histogram": {
            str(margin): finite_margins[margin]
            for margin in sorted(finite_margins)
        },
        "infinite_capacity_impossible_size_histogram": {
            str(size): infinite_sizes[size]
            for size in sorted(infinite_sizes)
        },
    }
    terminal_summary = {
        "terminal_line_stream_sha256": terminal_hasher.hexdigest(),
        "terminal_H_record_count": terminal_count,
        "terminal_H_cover_index_stream_sha256": sha256(
            b"".join(
                f"{index}\n".encode("ascii")
                for index in terminal_h_indices
            )
        ),
        "minimum_degree_inside_degree_11_set_histogram": {
            str(value): terminal_internal_minima[value]
            for value in sorted(terminal_internal_minima)
        },
    }
    return payload, classification_summary, terminal_summary


def exceptional_manifest(profile: AProfile) -> dict[str, object]:
    if profile.index != EXPECTED_EXCEPTIONAL_A:
        raise ValueError("wrong exceptional A index")
    q5 = profile.minimum(5)
    q6 = profile.minimum(6)
    if q5.value != 17 or q6.value != 10:
        raise ValueError("exceptional q5/q6 values changed")
    if len(q5.minimizers) != 10 or len(q6.minimizers) != 1:
        raise ValueError("exceptional minimizer multiplicities changed")
    unique = q6.minimizers[0]
    missed = [
        vertices(triple, A_ORDER)
        for triple in profile.independent3
        if triple & unique == 0
    ]
    if len(missed) != q6.value:
        raise ValueError("unique q6 minimizer miss count changed")
    return {
        "A_index_zero_based": profile.index,
        "catalog_line_one_based": profile.index + 1,
        "graph6": profile.record.decode("ascii"),
        "graph6_line_sha256": sha256(profile.record + b"\n"),
        "degrees_labeled": [
            neighbors.bit_count() for neighbors in profile.adjacency
        ],
        "independent_3_count": len(profile.independent3),
        "independent_4_count": len(profile.independent4),
        "size_5": {
            "q": q5.value,
            "transversal_count": q5.candidate_count,
            "minimizer_count": len(q5.minimizers),
            "minimizer_stream_encoding": (
                "s={size} X={comma-separated zero-based vertices:02d}\\n"
            ),
            "minimizer_stream_sha256": minimizer_stream_sha256(q5),
            "minimizers_zero_based": [
                vertices(mask, A_ORDER) for mask in q5.minimizers
            ],
        },
        "size_6": {
            "q": q6.value,
            "transversal_count": q6.candidate_count,
            "minimizer_count": len(q6.minimizers),
            "minimizer_stream_encoding": (
                "s={size} X={comma-separated zero-based vertices:02d}\\n"
            ),
            "minimizer_stream_sha256": minimizer_stream_sha256(q6),
            "unique_minimizer_zero_based": vertices(unique, A_ORDER),
            "missed_independent_triples_zero_based": missed,
        },
    }


def file_binding(root: Path, relative: str) -> dict[str, object]:
    payload = confined_path(root, relative).read_bytes()
    return {
        "path": relative,
        "bytes": len(payload),
        "sha256": sha256(payload),
    }


def validate_classification_lines(
    errors: list[str],
    payload: bytes,
    a_profiles: Sequence[AProfile],
    h_profiles: Sequence[HProfile],
) -> None:
    if not payload.endswith(b"\n"):
        errors.append("classification stream lacks final newline")
        return
    lines = payload.splitlines()
    if len(lines) != PAIR_COUNT:
        errors.append("classification stream record count mismatch")
        return
    for ordinal, raw in enumerate(lines):
        line = raw + b"\n"
        a_index = ordinal // H_SELECTED
        h_index = ordinal % H_SELECTED
        a_profile = a_profiles[a_index]
        h_profile = h_profiles[h_index]
        decision = capacity_decision(a_profile, h_profile)
        if decision.kind == "STRICT_INFINITE":
            match = CAPACITY_INF_RE.fullmatch(line)
            if match is None:
                errors.append(
                    f"classification line {ordinal + 1} malformed infinite"
                )
                continue
            actual = tuple(int(group) for group in match.groups())
            expected = (
                a_index,
                h_index,
                h_profile.source_line,
                decision.capacity,
                int(decision.impossible_size),
            )
        elif decision.kind == "STRICT_FINITE":
            match = CAPACITY_FINITE_RE.fullmatch(line)
            if match is None:
                errors.append(
                    f"classification line {ordinal + 1} malformed finite"
                )
                continue
            actual = tuple(int(group) for group in match.groups())
            expected = (
                a_index,
                h_index,
                h_profile.source_line,
                int(decision.lower_bound),
                decision.capacity,
                int(decision.margin),
            )
        elif decision.kind == "EQUALITY":
            match = TERMINAL_RE.fullmatch(line)
            if match is None:
                errors.append(
                    f"classification line {ordinal + 1} malformed terminal"
                )
                continue
            witness = terminal_witness(a_profile, h_profile)
            triple = vertices(
                witness.missed_independent_triple, A_ORDER
            )
            actual = tuple(int(group) for group in match.groups())
            expected = (
                a_index,
                h_index,
                h_profile.source_line,
                int(decision.lower_bound),
                decision.capacity,
                witness.high_edge[0],
                witness.high_edge[1],
                triple[0],
                triple[1],
                triple[2],
            )
        else:
            errors.append(
                f"classification line {ordinal + 1} has slack decision"
            )
            continue
        if actual != expected:
            errors.append(
                f"classification line {ordinal + 1} semantic mismatch"
            )


def preartifact_reconstruction(root: Path) -> dict[str, object]:
    (
        _a_payload,
        _h_payload,
        a_profiles,
        h_profiles,
        full_edge_histogram,
        selected_digest,
    ) = reconstruct_catalogs(root)
    classification = reconstruct_classification(a_profiles, h_profiles)
    exceptional = a_profiles[EXPECTED_EXCEPTIONAL_A]
    q5 = exceptional.minimum(5)
    q6 = exceptional.minimum(6)
    q7 = exceptional.minimum(7)
    equality_pairs = classification["equality_pairs"]
    terminal_witnesses = classification["terminal_witnesses"]
    assert isinstance(equality_pairs, list)
    assert isinstance(terminal_witnesses, list)
    equality_a_indices = sorted(
        {int(pair[0]) for pair in equality_pairs}
    )
    equality_h_histogram: Counter[tuple[int, ...]] = Counter(
        h_profiles[int(pair[1])].size_histogram
        for pair in equality_pairs
    )
    return {
        "catalogs": {
            "A_record_count": len(a_profiles),
            "H_full_record_count": H_RECORDS,
            "H_selected_record_count": len(h_profiles),
            "H_selected_stream_sha256": selected_digest,
            "H_full_edge_histogram": {
                str(edges): full_edge_histogram[edges]
                for edges in sorted(full_edge_histogram)
            },
        },
        "capacity": {
            "pair_count": PAIR_COUNT,
            "strict_exclusion_count": classification["strict_count"],
            "equality_survivor_count": len(equality_pairs),
            "kind_histogram": dict(
                sorted(classification["kind_histogram"].items())
            ),
            "finite_margin_histogram": {
                str(margin): count
                for margin, count in sorted(
                    classification["finite_margin_histogram"].items()
                )
            },
            "infinite_impossible_size_histogram": {
                str(size): count
                for size, count in sorted(
                    classification["infinite_size_histogram"].items()
                )
            },
        },
        "exceptional_A": {
            "index_zero_based": exceptional.index,
            "graph6": exceptional.record.decode("ascii"),
            "graph6_line_sha256": sha256(exceptional.record + b"\n"),
            "independent_3_count": len(exceptional.independent3),
            "independent_4_count": len(exceptional.independent4),
            "q5": q5.value,
            "q5_candidate_count": q5.candidate_count,
            "q5_minimizer_count": len(q5.minimizers),
            "q5_minimizers_zero_based": [
                vertices(mask, A_ORDER) for mask in q5.minimizers
            ],
            "q6": q6.value,
            "q6_candidate_count": q6.candidate_count,
            "q6_minimizer_count": len(q6.minimizers),
            "q6_unique_minimizer_zero_based": (
                vertices(q6.minimizers[0], A_ORDER)
                if len(q6.minimizers) == 1
                else None
            ),
            "q7": q7.value,
            "q7_candidate_count": q7.candidate_count,
            "q7_minimizer_count": len(q7.minimizers),
        },
        "terminal": {
            "terminal_exclusion_count": len(terminal_witnesses),
            "equality_A_indices_zero_based": equality_a_indices,
            "equality_H_size_histogram": {
                ",".join(
                    f"{size}:{histogram[size - SIZE_MIN]}"
                    for size in range(SIZE_MIN, SIZE_MAX + 1)
                ): count
                for histogram, count in sorted(
                    equality_h_histogram.items()
                )
            },
            "all_terminal_edges_are_size_6_6": all(
                h_profiles[h_index].degrees[witness.high_edge[0]] - 5
                == 6
                and h_profiles[h_index].degrees[witness.high_edge[1]] - 5
                == 6
                for _, h_index, witness in terminal_witnesses
            ),
            "all_terminal_witnesses_use_unique_q6_minimizer": all(
                witness.forced_minimizer == q6.minimizers[0]
                for _, _, witness in terminal_witnesses
            ),
        },
    }


def audit(root: Path, manifest_path: Path) -> dict[str, object]:
    """Reconstruct all mathematics and compare the complete artifact."""
    root = root.resolve()
    manifest_path = confined_path(root, manifest_path)
    manifest_payload = manifest_path.read_bytes()
    loaded = load_canonical_json(manifest_payload)
    if not isinstance(loaded, dict):
        raise ValueError("manifest root is not an object")
    manifest = loaded
    errors: list[str] = []

    (
        a_payload,
        h_payload,
        a_profiles,
        h_profiles,
        full_h_edge_histogram,
        selected_h_digest,
    ) = reconstruct_catalogs(root)
    selected_line_digest = sha256(
        b"".join(
            f"{profile.source_line}\n".encode("ascii")
            for profile in h_profiles
        )
    )
    if selected_line_digest != EXPECTED_H_SELECTED_LINE_SHA256:
        errors.append("selected H line-index digest changed")

    classification = manifest.get("classification")
    stream_relative = ""
    if not isinstance(classification, dict):
        errors.append("manifest classification is not an object")
    else:
        raw_path = classification.get("path")
        if not isinstance(raw_path, str):
            errors.append("classification path is not a string")
        else:
            stream_relative = raw_path

    actual_stream = b""
    if stream_relative:
        try:
            stream_path = confined_path(root, stream_relative)
            if stream_path.resolve() == manifest_path.resolve():
                raise ValueError("classification overlaps manifest")
            actual_stream = stream_path.read_bytes()
        except Exception as exc:
            errors.append(f"classification stream read failure: {exc}")

    (
        expected_stream,
        classification_summary,
        terminal_summary,
    ) = reconstruct_classification_stream(
        a_profiles, h_profiles, stream_relative
    )
    validate_classification_lines(
        errors, actual_stream, a_profiles, h_profiles
    )
    if actual_stream != expected_stream:
        errors.append(
            "classification stream differs from independent reconstruction"
        )

    profile_payload = b"".join(
        a_profile_line(profile) for profile in a_profiles
    )
    h_degree_histogram = Counter(
        degree_histogram_key(profile.degrees)
        for profile in h_profiles
    )
    expected_catalogs = {
        "A": {
            "path": A_RELATIVE,
            "bytes": len(a_payload),
            "sha256": sha256(a_payload),
            "record_count": len(a_profiles),
            "selection_rule": "all records, each with 85 edges",
        },
        "H": {
            "path": H_RELATIVE,
            "bytes": len(h_payload),
            "sha256": sha256(h_payload),
            "full_record_count": H_RECORDS,
            "full_edge_count_histogram": {
                str(edges): full_h_edge_histogram[edges]
                for edges in sorted(full_h_edge_histogram)
            },
            "selection_rule": "edge_count==128",
            "selected_record_count": len(h_profiles),
            "selected_record_stream_sha256": selected_h_digest,
            "selected_line_index_stream_sha256": selected_line_digest,
        },
        "publisher_page": (
            "https://users.cecs.anu.edu.au/~bdm/data/ramsey.html"
        ),
    }
    expected_capacity_profiles = {
        "A_profile_stream_encoding": (
            "A={index:02d} I3={count:03d} I4={count:03d} "
            "S{s}={q|INF}/{transversals:05d}/"
            "{minimizers:05d}/{minimizer_stream_sha256|-}\\n"
        ),
        "A_profile_stream_bytes": len(profile_payload),
        "A_profile_stream_sha256": sha256(profile_payload),
        "H_degree_sequence_histogram": {
            key: h_degree_histogram[key]
            for key in sorted(h_degree_histogram)
        },
    }
    expected_terminal = {
        "exceptional_A": exceptional_manifest(
            a_profiles[EXPECTED_EXCEPTIONAL_A]
        ),
        "capacity_equality": (
            "8*q_5+16*q_6=8*17+16*10=296=4*74"
        ),
        "terminal_H_degree_histogram": {"10": 8, "11": 16},
        "equality_consequence": (
            "Every one of the sixteen degree-11 H vertices has a "
            "size-six cross neighborhood attaining q_6. The q_6 "
            "minimizer is unique, so all sixteen neighborhoods are "
            "the same set X*."
        ),
        "high_edge_reason": (
            "A degree-11 H vertex has only eight degree-10 vertices "
            "available, hence at least three neighbors among the "
            "sixteen degree-11 vertices. Therefore a degree-11--"
            "degree-11 H-edge exists."
        ),
        "contradiction": (
            "The endpoints of the recorded H-edge both have X*. "
            "Their union equals X* and misses the recorded "
            "independent triple of A, contradicting the exact "
            "two-column condition."
        ),
        **terminal_summary,
    }
    expected_bindings = [
        file_binding(
            root, "src/branch18_regular_endpoint_capacity_cover.py"
        ),
        file_binding(
            root,
            "verify/branch18_regular_endpoint_capacity_cover_check.py",
        ),
        file_binding(
            root,
            "tests/branch18_regular_endpoint_capacity_cover_tests.py",
        ),
    ]
    expected_manifest = {
        "schema": MANIFEST_SCHEMA,
        "status": EXPECTED_STATUS,
        "theorem": EXPECTED_THEOREM,
        "catalogs": expected_catalogs,
        "capacity_profiles": expected_capacity_profiles,
        "classification": classification_summary,
        "terminal_obstruction": expected_terminal,
        "claim_boundary": EXPECTED_CLAIM_BOUNDARY,
        "execution": EXPECTED_EXECUTION,
        "local_derivation_bindings": expected_bindings,
    }
    for key, expected in expected_manifest.items():
        if manifest.get(key) != expected:
            errors.append(
                f"manifest {key} differs from independent reconstruction"
            )
    if set(manifest) != set(expected_manifest):
        errors.append("manifest top-level key set mismatch")

    strict_count = int(
        classification_summary["capacity_exclusion_count"]
    )
    terminal_count = int(
        classification_summary["terminal_exclusion_count"]
    )
    return {
        "checker": CHECKER_SCHEMA,
        "valid": not errors,
        "errors": errors,
        "manifest": str(manifest_path.relative_to(root)),
        "manifest_bytes": len(manifest_payload),
        "manifest_sha256": sha256(manifest_payload),
        "checker_source_sha256": sha256(Path(__file__).read_bytes()),
        "catalog_reconstruction": {
            "A_record_count": len(a_profiles),
            "H_full_record_count": H_RECORDS,
            "H_selected_record_count": len(h_profiles),
            "H_selected_record_stream_sha256": selected_h_digest,
            "H_selected_line_index_stream_sha256": selected_line_digest,
        },
        "capacity_reconstruction": {
            "pair_count": PAIR_COUNT,
            "strict_capacity_exclusion_count": strict_count,
            "capacity_equality_survivor_count": terminal_count,
            "terminal_exclusion_count": terminal_count,
            "retained_pair_count": PAIR_COUNT
            - strict_count
            - terminal_count,
            "A_profile_stream_sha256": sha256(profile_payload),
            "classification_stream_sha256": sha256(expected_stream),
            "terminal_line_stream_sha256": terminal_summary[
                "terminal_line_stream_sha256"
            ],
            "exceptional_A_index_zero_based": EXPECTED_EXCEPTIONAL_A,
            "exceptional_q6_unique_minimizer_zero_based": vertices(
                a_profiles[EXPECTED_EXCEPTIONAL_A]
                .minimum(6)
                .minimizers[0],
                A_ORDER,
            ),
        },
        "semantic_audit": {
            "cross_size_identity_rederived": True,
            "single_column_transversals_exhausted": True,
            "capacity_double_count_rederived": True,
            "all_capacity_survivors_are_equalities": True,
            "unique_q6_minimizer_reconstructed": True,
            "all_terminal_H_records_have_high_high_edge": True,
            "catalog_completeness_checked_locally": False,
            "catalog_completeness_inherited_from_publisher": True,
        },
        "execution": {
            "solver_calls": 0,
            "proof_jobs": 0,
            "formulas_materialized": 0,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(
            "results/benchmark_plans/"
            "branch18_regular_endpoint_capacity_cover_v1.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "results/verification/"
            "branch18_regular_endpoint_capacity_cover_v1.check.json"
        ),
    )
    parser.add_argument(
        "--reconstruct-only",
        action="store_true",
        help="print the independent mathematical reconstruction only",
    )
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    if arguments.reconstruct_only:
        report = {
            "checker": CHECKER_SCHEMA,
            "valid": True,
            "preartifact_reconstruction": preartifact_reconstruction(root),
            "execution": {
                "solver_calls": 0,
                "proof_jobs": 0,
                "formulas_materialized": 0,
            },
        }
        print(json.dumps(report, sort_keys=True))
        return 0

    manifest_path = confined_path(root, arguments.manifest)
    output_path = confined_path(root, arguments.output)
    if manifest_path.resolve() == output_path.resolve():
        raise SystemExit("refusing checker output overlapping manifest")
    try:
        report = audit(root, manifest_path)
    except Exception as exc:
        report = {
            "checker": CHECKER_SCHEMA,
            "valid": False,
            "errors": [
                f"checker failed closed: {type(exc).__name__}: {exc}"
            ],
            "manifest": str(manifest_path.relative_to(root)),
            "checker_source_sha256": sha256(Path(__file__).read_bytes()),
            "execution": {
                "solver_calls": 0,
                "proof_jobs": 0,
                "formulas_materialized": 0,
            },
        }
    atomic_write(output_path, canonical_json(report))
    print(json.dumps(report, sort_keys=True))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
