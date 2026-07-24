#!/usr/bin/env python3
"""Capacity certificate for the regular degree-18, (85,128) endpoint.

Let ``v`` be a vertex of a hypothetical 18-regular Ramsey(5,5;43) graph,
write ``A=N_G(v)``, and let

    H = complement(G[V(G) - (A union {v})]).

At the endpoint ``e(A)=85`` and ``e(H)=128``, the published complete
``R(4,5;18)`` and ``R(4,5;24)`` catalogs give 74 and 843 fixed-side
isomorphism types.  This producer classifies their 62,382 Cartesian-product
pairs without constructing a CNF or invoking a solver.

For ``b in V(H)``, put ``X_b=N_G(b) intersect A``.  Regularity gives
``|X_b|=degree_H(b)-5``.  Each ``X_b`` must hit every independent four-set
of ``A``.  If ``Q`` is an independent three-set of ``A``, then

    Z_Q = {b : X_b is disjoint from Q}

must be independent in ``H``.  Since ``H`` has no independent five-set,
``|Z_Q| <= 4``.  For a fixed ``A`` define

    q_s(A) = min_X #{independent triples Q of A disjoint from X},

where the minimum is over exact-size-``s`` subsets hitting every independent
four-set.  Double counting ``(b,Q)`` yields the necessary capacity inequality

    sum_b q_{degree_H(b)-5}(A) <= 4 i_3(A).

Exactly 61,939 endpoint pairs violate this inequality.  The other 443 all
use one exceptional A record and H degree sequence ``10^8 11^16``.  Equality
in the capacity inequality then forces all sixteen size-six columns to use
the exceptional A record's unique minimizing size-six set.  Every degree-11
H vertex has at least three neighbors among those sixteen vertices, so an
H-edge has two identical cross neighborhoods.  Their union misses an
independent triple of A, contradicting the necessary two-column condition.

The producer emits:

* a compact, catalog-conditional manifest; and
* one explicit classification/witness line for each of the 62,382 pairs.

Catalog completeness, pairwise nonisomorphism, and the endpoint cover remain
publisher inputs.  Local code binds the exact bytes and verifies every
retained record.  This excludes only ``e(A)=85,e(H)=128`` inside the regular
degree-18 branch; it does not exclude the other regular degree-18 layers, any
other global branch, or all order-43 Ramsey graphs.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence


SCHEMA = "ramsey55.branch18_regular_endpoint_capacity_cover.v1"
CLASSIFICATION_SCHEMA = (
    "ramsey55.branch18_regular_endpoint_capacity_classifications.v1"
)

A_ORDER = 18
H_ORDER = 24
A_EDGE_COUNT = 85
H_EDGE_COUNT = 128
A_RECORD_COUNT = 74
H_FULL_RECORD_COUNT = 352_366
H_SELECTED_RECORD_COUNT = 843
PAIR_COUNT = A_RECORD_COUNT * H_SELECTED_RECORD_COUNT

A_CATALOG_RELATIVE = "data/r45extreme/r4518.85.g6"
A_CATALOG_BYTES = 2_072
A_CATALOG_SHA256 = (
    "46abaee2572d06bba1e594554809d784be60f8f60b9b0d3345b8bf3dd800810a"
)
H_CATALOG_RELATIVE = "data/r45_24.g6"
H_CATALOG_BYTES = 16_913_568
H_CATALOG_SHA256 = (
    "83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0"
)
H_SELECTED_RECORD_STREAM_SHA256 = (
    "2fe5a0505c0b6b252caaeee1c35d866a538567c0731aa9616734a444a880db5d"
)
H_SELECTED_LINE_STREAM_SHA256 = (
    "344eadae59880c8c3a815add0e1ac4861236c5de9eb3949446262b539c940524"
)
EXPECTED_H_EDGE_HISTOGRAM = {
    116: 9,
    117: 90,
    118: 806,
    119: 4_358,
    120: 16_346,
    121: 43_457,
    122: 79_678,
    123: 92_504,
    124: 67_209,
    125: 31_996,
    126: 11_485,
    127: 3_401,
    128: 843,
    129: 147,
    130: 32,
    131: 3,
    132: 2,
}

SIZE_MIN = 3
SIZE_MAX = 7
CAPACITY_EXCLUSION_COUNT = 61_939
TERMINAL_EXCLUSION_COUNT = 443
RETAINED_PAIR_COUNT = 0

EXCEPTIONAL_A_INDEX = 50
EXCEPTIONAL_A_LINE = 51
EXCEPTIONAL_A_GRAPH6 = b"QznZZYVk{mHZuJuD@\\XfQOs}_lo"
EXCEPTIONAL_A_LINE_SHA256 = (
    "4f72e799b87cb665a114fb56f8e9fadd1cee9615ad5f58b26c1d866a1d416e7e"
)
EXCEPTIONAL_I3_COUNT = 74
EXCEPTIONAL_I4_COUNT = 23
EXCEPTIONAL_Q5 = 17
EXCEPTIONAL_Q6 = 10
EXCEPTIONAL_Q5_CANDIDATE_COUNT = 30
EXCEPTIONAL_Q6_CANDIDATE_COUNT = 569
EXCEPTIONAL_Q5_MINIMIZER_SHA256 = (
    "99cf8c6d83a46b8b68e67df2b592a5d5ab5118bad84764fa6bdaafef3bc684cb"
)
EXCEPTIONAL_Q6_MINIMIZER_SHA256 = (
    "0fac5312b98a3fef21dc66e22e8daeb8833fef3a922abe286ee5bfcbb228a797"
)
EXCEPTIONAL_Q5_MINIMIZERS = (
    (2, 3, 4, 12, 14),
    (2, 3, 4, 12, 15),
    (2, 4, 6, 9, 11),
    (2, 4, 7, 9, 11),
    (3, 8, 9, 11, 12),
    (3, 9, 10, 11, 12),
    (5, 6, 8, 9, 11),
    (5, 6, 9, 10, 11),
    (5, 7, 8, 9, 11),
    (5, 7, 9, 10, 11),
)
EXCEPTIONAL_Q6_MINIMIZERS = ((2, 3, 4, 9, 11, 12),)
EXCEPTIONAL_MISSED_I3 = (
    (0, 6, 7),
    (0, 14, 15),
    (1, 8, 10),
    (1, 14, 15),
    (5, 14, 15),
    (5, 16, 17),
    (6, 7, 13),
    (6, 7, 17),
    (8, 10, 13),
    (8, 10, 16),
)
EXCEPTIONAL_H_DEGREE_HISTOGRAM = {10: 8, 11: 16}

SOURCE_BINDING_PATHS = (
    "src/branch18_regular_endpoint_capacity_cover.py",
    "verify/branch18_regular_endpoint_capacity_cover_check.py",
    "tests/branch18_regular_endpoint_capacity_cover_tests.py",
)


@dataclass(frozen=True)
class MinimumProfile:
    """Exact minimum for one cross-neighborhood size."""

    size: int
    value: int | None
    candidate_count: int
    minimizer_count: int
    first_minimizer: int | None
    minimizer_stream_sha256: str | None


@dataclass(frozen=True)
class AProfile:
    """Capacity data for one labeled order-18 catalog representative."""

    index: int
    line_sha256: str
    graph6: bytes
    degrees: tuple[int, ...]
    independent3: tuple[int, ...]
    independent4: tuple[int, ...]
    minima: tuple[MinimumProfile, ...]

    def minimum(self, size: int) -> MinimumProfile:
        if not SIZE_MIN <= size <= SIZE_MAX:
            raise ValueError("cross-neighborhood size outside profile")
        return self.minima[size - SIZE_MIN]


@dataclass(frozen=True)
class HProfile:
    """Minimal retained order-24 data needed by the certificate."""

    index: int
    source_line: int
    line_sha256: str
    adjacency: tuple[int, ...]
    degrees: tuple[int, ...]
    size_histogram: tuple[tuple[int, int], ...]


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, separators=(",", ": "))
        + "\n"
    ).encode("utf-8")


def streaming_file_binding(
    path: Path, *, relative: str, expected_bytes: int, expected_sha256: str
) -> dict[str, object]:
    """Hash a file without retaining it and enforce its frozen binding."""

    hasher = hashlib.sha256()
    byte_count = 0
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1 << 20)
            if not chunk:
                break
            byte_count += len(chunk)
            hasher.update(chunk)
    actual_sha256 = hasher.hexdigest()
    if byte_count != expected_bytes or actual_sha256 != expected_sha256:
        raise ValueError(f"frozen file binding failed: {relative}")
    return {
        "path": relative,
        "bytes": byte_count,
        "sha256": actual_sha256,
    }


def local_file_binding(root: Path, relative: str) -> dict[str, object]:
    """Bind a required local derivation file, failing if it is absent."""

    path = root / relative
    payload = path.read_bytes()
    return {
        "path": relative,
        "bytes": len(payload),
        "sha256": digest(payload),
    }


def decode_graph6(record: bytes, expected_order: int) -> tuple[int, ...]:
    """Decode one canonical short graph6 record into adjacency bitsets."""

    if not record or record[0] != expected_order + 63:
        raise ValueError("graph6 order mismatch")
    pair_count = expected_order * (expected_order - 1) // 2
    payload_length = (pair_count + 5) // 6
    if len(record) != payload_length + 1:
        raise ValueError("noncanonical short graph6 length")
    values = tuple(character - 63 for character in record[1:])
    if any(value < 0 or value >= 64 for value in values):
        raise ValueError("invalid graph6 payload")
    padding = payload_length * 6 - pair_count
    if padding and values[-1] & ((1 << padding) - 1):
        raise ValueError("nonzero graph6 padding")

    adjacency = [0] * expected_order
    cursor = 0
    for right in range(1, expected_order):
        for left in range(right):
            if (values[cursor // 6] >> (5 - cursor % 6)) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1
    if cursor != pair_count:
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
        full & ~(neighbors | (1 << vertex))
        for vertex, neighbors in enumerate(adjacency)
    )


def contains_clique(adjacency: Sequence[int], size: int) -> bool:
    """Return whether the graph contains a clique of the requested size."""

    if size < 0:
        raise ValueError("negative clique size")
    if size == 0:
        return True

    def search(candidates: int, remaining: int) -> bool:
        while candidates.bit_count() >= remaining:
            chosen = candidates & -candidates
            candidates ^= chosen
            vertex = chosen.bit_length() - 1
            if remaining == 1 or search(
                candidates & adjacency[vertex], remaining - 1
            ):
                return True
        return False

    return search((1 << len(adjacency)) - 1, size)


def independent_masks(
    adjacency: Sequence[int], size: int
) -> tuple[int, ...]:
    """Enumerate independent sets in lexicographic combination order."""

    retained: list[int] = []
    for chosen in itertools.combinations(range(len(adjacency)), size):
        mask = sum(1 << vertex for vertex in chosen)
        if all(
            not (adjacency[vertex] & (mask ^ (1 << vertex)))
            for vertex in chosen
        ):
            retained.append(mask)
    return tuple(retained)


def mask_vertices(mask: int, order: int) -> tuple[int, ...]:
    return tuple(vertex for vertex in range(order) if (mask >> vertex) & 1)


def minimizer_line(size: int, mask: int) -> bytes:
    vertices = ",".join(
        f"{vertex:02d}" for vertex in mask_vertices(mask, A_ORDER)
    )
    return f"s={size} X={vertices}\n".encode("ascii")


def exact_minimum_profile(
    *,
    size: int,
    independent3: Sequence[int],
    independent4: Sequence[int],
) -> MinimumProfile:
    """Exhaust one exact subset size and retain only minimum metadata."""

    best: int | None = None
    candidate_count = 0
    minimizers: list[int] = []
    for chosen in itertools.combinations(range(A_ORDER), size):
        mask = sum(1 << vertex for vertex in chosen)
        if any(not (mask & subset) for subset in independent4):
            continue
        candidate_count += 1
        missed = sum(not (mask & subset) for subset in independent3)
        if best is None or missed < best:
            best = missed
            minimizers = [mask]
        elif missed == best:
            minimizers.append(mask)

    if best is None:
        if candidate_count or minimizers:
            raise AssertionError("empty minimum has retained candidates")
        return MinimumProfile(
            size=size,
            value=None,
            candidate_count=0,
            minimizer_count=0,
            first_minimizer=None,
            minimizer_stream_sha256=None,
        )

    if not minimizers or candidate_count < len(minimizers):
        raise AssertionError("minimum bookkeeping failed")
    minimizer_payload = b"".join(
        minimizer_line(size, mask) for mask in minimizers
    )
    return MinimumProfile(
        size=size,
        value=best,
        candidate_count=candidate_count,
        minimizer_count=len(minimizers),
        first_minimizer=minimizers[0],
        minimizer_stream_sha256=digest(minimizer_payload),
    )


def read_a_profiles(root: Path) -> tuple[list[AProfile], dict[str, object]]:
    """Read, validate, and exhaust all 74 endpoint A representatives."""

    path = root / A_CATALOG_RELATIVE
    binding = streaming_file_binding(
        path,
        relative=A_CATALOG_RELATIVE,
        expected_bytes=A_CATALOG_BYTES,
        expected_sha256=A_CATALOG_SHA256,
    )
    with path.open("rb") as handle:
        raw_lines = list(handle)
    if len(raw_lines) != A_RECORD_COUNT:
        raise ValueError("A catalog record count mismatch")

    profiles: list[AProfile] = []
    for index, raw_line in enumerate(raw_lines):
        if not raw_line.endswith(b"\n") or raw_line.endswith(b"\r\n"):
            raise ValueError("A catalog line ending is not canonical LF")
        record = raw_line[:-1]
        adjacency = decode_graph6(record, A_ORDER)
        if edge_count(adjacency) != A_EDGE_COUNT:
            raise ValueError("A endpoint record has the wrong edge count")
        if contains_clique(adjacency, 4) or contains_clique(
            complement(adjacency), 5
        ):
            raise ValueError("A endpoint record is not in R(4,5)")
        independent3 = independent_masks(adjacency, 3)
        independent4 = independent_masks(adjacency, 4)
        minima = tuple(
            exact_minimum_profile(
                size=size,
                independent3=independent3,
                independent4=independent4,
            )
            for size in range(SIZE_MIN, SIZE_MAX + 1)
        )
        profiles.append(
            AProfile(
                index=index,
                line_sha256=digest(raw_line),
                graph6=record,
                degrees=tuple(
                    neighbors.bit_count() for neighbors in adjacency
                ),
                independent3=independent3,
                independent4=independent4,
                minima=minima,
            )
        )

    if len({profile.graph6 for profile in profiles}) != A_RECORD_COUNT:
        raise ValueError("A endpoint catalog contains duplicate records")
    binding["record_count"] = len(profiles)
    binding["selection_rule"] = "all records, each with 85 edges"
    return profiles, binding


def read_h_profiles(root: Path) -> tuple[list[HProfile], dict[str, object]]:
    """Stream the order-24 catalog and retain only the 843 edge-128 records."""

    path = root / H_CATALOG_RELATIVE
    binding = streaming_file_binding(
        path,
        relative=H_CATALOG_RELATIVE,
        expected_bytes=H_CATALOG_BYTES,
        expected_sha256=H_CATALOG_SHA256,
    )
    selected_record_hasher = hashlib.sha256()
    selected_line_hasher = hashlib.sha256()
    full_edge_histogram: Counter[int] = Counter()
    profiles: list[HProfile] = []
    line_count = 0
    with path.open("rb") as handle:
        for source_line, raw_line in enumerate(handle, 1):
            line_count = source_line
            if not raw_line.endswith(b"\n") or raw_line.endswith(b"\r\n"):
                raise ValueError("H catalog line ending is not canonical LF")
            record = raw_line[:-1]
            adjacency = decode_graph6(record, H_ORDER)
            edges = edge_count(adjacency)
            full_edge_histogram[edges] += 1
            if edges != H_EDGE_COUNT:
                continue
            if contains_clique(adjacency, 4) or contains_clique(
                complement(adjacency), 5
            ):
                raise ValueError("selected H record is not in R(4,5)")
            degrees = tuple(
                neighbors.bit_count() for neighbors in adjacency
            )
            sizes = tuple(degree - 5 for degree in degrees)
            if min(sizes) < SIZE_MIN or max(sizes) > SIZE_MAX:
                raise ValueError("selected H cross size is outside 3..7")
            selected_record_hasher.update(raw_line)
            selected_line_hasher.update(f"{source_line}\n".encode("ascii"))
            profiles.append(
                HProfile(
                    index=len(profiles),
                    source_line=source_line,
                    line_sha256=digest(raw_line),
                    adjacency=adjacency,
                    degrees=degrees,
                    size_histogram=tuple(sorted(Counter(sizes).items())),
                )
            )

    if line_count != H_FULL_RECORD_COUNT:
        raise ValueError("H full catalog record count mismatch")
    if dict(sorted(full_edge_histogram.items())) != EXPECTED_H_EDGE_HISTOGRAM:
        raise ValueError("H full edge-count histogram changed")
    if len(profiles) != H_SELECTED_RECORD_COUNT:
        raise ValueError("H edge-128 selection does not have 843 records")
    if len({profile.adjacency for profile in profiles}) != (
        H_SELECTED_RECORD_COUNT
    ):
        raise ValueError("H edge-128 selection contains duplicate records")
    if selected_record_hasher.hexdigest() != (
        H_SELECTED_RECORD_STREAM_SHA256
    ):
        raise ValueError("H selected-record stream binding failed")
    if selected_line_hasher.hexdigest() != H_SELECTED_LINE_STREAM_SHA256:
        raise ValueError("H selected-line stream binding failed")

    binding.update(
        {
            "full_record_count": line_count,
            "full_edge_count_histogram": {
                str(edges): full_edge_histogram[edges]
                for edges in sorted(full_edge_histogram)
            },
            "selection_rule": "edge_count==128",
            "selected_record_count": len(profiles),
            "selected_record_stream_sha256": (
                selected_record_hasher.hexdigest()
            ),
            "selected_line_index_stream_sha256": (
                selected_line_hasher.hexdigest()
            ),
        }
    )
    return profiles, binding


def profile_value_text(profile: MinimumProfile) -> str:
    return "INF" if profile.value is None else f"{profile.value:03d}"


def a_profile_line(profile: AProfile) -> bytes:
    """Canonical compact stream line binding all capacity minima."""

    fields = [
        f"A={profile.index:02d}",
        f"I3={len(profile.independent3):03d}",
        f"I4={len(profile.independent4):03d}",
    ]
    for minimum in profile.minima:
        fields.append(
            "S"
            f"{minimum.size}={profile_value_text(minimum)}/"
            f"{minimum.candidate_count:05d}/"
            f"{minimum.minimizer_count:05d}/"
            f"{minimum.minimizer_stream_sha256 or '-'}"
        )
    return (" ".join(fields) + "\n").encode("ascii")


def degree_histogram_key(histogram: Mapping[int, int]) -> str:
    return ",".join(
        f"{degree}^{histogram[degree]}" for degree in sorted(histogram)
    )


def first_high_edge(
    profile: HProfile, *, degree: int
) -> tuple[tuple[int, int], int]:
    """Return the lex-first same-degree edge and induced minimum degree."""

    high = tuple(
        vertex
        for vertex, actual_degree in enumerate(profile.degrees)
        if actual_degree == degree
    )
    high_mask = sum(1 << vertex for vertex in high)
    if not high:
        raise ValueError("terminal H record has no high-degree vertices")
    internal_degrees = tuple(
        (profile.adjacency[vertex] & high_mask).bit_count()
        for vertex in high
    )
    for left in high:
        candidates = profile.adjacency[left] & high_mask
        candidates &= ~((1 << (left + 1)) - 1)
        if candidates:
            right = (candidates & -candidates).bit_length() - 1
            return (left, right), min(internal_degrees)
    raise ValueError("terminal H record has no high-high edge")


def capacity_lower_bound(
    a_profile: AProfile, h_profile: HProfile
) -> tuple[int | None, int | None]:
    """Return the summed lower bound and first impossible exact size."""

    total = 0
    for size, multiplicity in h_profile.size_histogram:
        minimum = a_profile.minimum(size)
        if minimum.value is None:
            return None, size
        total += multiplicity * minimum.value
    return total, None


def capacity_line(
    *,
    a_index: int,
    h_profile: HProfile,
    lower: int | None,
    upper: int,
    impossible_size: int | None,
) -> bytes:
    prefix = (
        f"A={a_index:02d} H={h_profile.index:03d} "
        f"L={h_profile.source_line:06d} C=CAP "
    )
    if lower is None:
        if impossible_size is None:
            raise AssertionError("infinite capacity has no impossible size")
        return (
            prefix
            + f"LB=INF UB={upper:03d} S={impossible_size}\n"
        ).encode("ascii")
    if lower <= upper or impossible_size is not None:
        raise AssertionError("finite capacity line is not an exclusion")
    return (
        prefix
        + f"LB={lower:04d} UB={upper:03d} D={lower - upper:04d}\n"
    ).encode("ascii")


def terminal_line(
    *,
    h_profile: HProfile,
    lower: int,
    upper: int,
    edge: tuple[int, int],
    missed_triple: tuple[int, int, int],
) -> bytes:
    return (
        f"A={EXCEPTIONAL_A_INDEX:02d} H={h_profile.index:03d} "
        f"L={h_profile.source_line:06d} C=TERM "
        f"LB={lower:04d} UB={upper:03d} "
        f"E={edge[0]:02d},{edge[1]:02d} "
        f"Q={missed_triple[0]:02d},{missed_triple[1]:02d},"
        f"{missed_triple[2]:02d}\n"
    ).encode("ascii")


def verify_exceptional_profile(profile: AProfile) -> dict[str, object]:
    """Fail closed unless the unique terminal A data match exactly."""

    if (
        profile.index != EXCEPTIONAL_A_INDEX
        or profile.graph6 != EXCEPTIONAL_A_GRAPH6
        or profile.line_sha256 != EXCEPTIONAL_A_LINE_SHA256
        or len(profile.independent3) != EXCEPTIONAL_I3_COUNT
        or len(profile.independent4) != EXCEPTIONAL_I4_COUNT
    ):
        raise ValueError("exceptional A record binding changed")

    q5 = profile.minimum(5)
    q6 = profile.minimum(6)
    if (
        q5.value != EXCEPTIONAL_Q5
        or q5.candidate_count != EXCEPTIONAL_Q5_CANDIDATE_COUNT
        or q5.minimizer_count != len(EXCEPTIONAL_Q5_MINIMIZERS)
        or q5.minimizer_stream_sha256
        != EXCEPTIONAL_Q5_MINIMIZER_SHA256
        or q6.value != EXCEPTIONAL_Q6
        or q6.candidate_count != EXCEPTIONAL_Q6_CANDIDATE_COUNT
        or q6.minimizer_count != len(EXCEPTIONAL_Q6_MINIMIZERS)
        or q6.minimizer_stream_sha256
        != EXCEPTIONAL_Q6_MINIMIZER_SHA256
    ):
        raise ValueError("exceptional A capacity profile changed")

    q5_masks = tuple(
        sum(1 << vertex for vertex in vertices)
        for vertices in EXCEPTIONAL_Q5_MINIMIZERS
    )
    q6_masks = tuple(
        sum(1 << vertex for vertex in vertices)
        for vertices in EXCEPTIONAL_Q6_MINIMIZERS
    )
    q5_payload = b"".join(minimizer_line(5, mask) for mask in q5_masks)
    q6_payload = b"".join(minimizer_line(6, mask) for mask in q6_masks)
    if (
        digest(q5_payload) != EXCEPTIONAL_Q5_MINIMIZER_SHA256
        or digest(q6_payload) != EXCEPTIONAL_Q6_MINIMIZER_SHA256
        or q5.first_minimizer != q5_masks[0]
        or q6.first_minimizer != q6_masks[0]
    ):
        raise ValueError("exceptional minimizer constants are inconsistent")

    unique_q6_mask = q6_masks[0]
    missed = tuple(
        mask_vertices(subset, A_ORDER)
        for subset in profile.independent3
        if not (subset & unique_q6_mask)
    )
    if missed != EXCEPTIONAL_MISSED_I3:
        raise ValueError("exceptional size-six missed triples changed")

    return {
        "A_index_zero_based": profile.index,
        "catalog_line_one_based": EXCEPTIONAL_A_LINE,
        "graph6": profile.graph6.decode("ascii"),
        "graph6_line_sha256": profile.line_sha256,
        "degrees_labeled": list(profile.degrees),
        "independent_3_count": len(profile.independent3),
        "independent_4_count": len(profile.independent4),
        "size_5": {
            "q": q5.value,
            "transversal_count": q5.candidate_count,
            "minimizer_count": q5.minimizer_count,
            "minimizer_stream_encoding": (
                "s={size} X={comma-separated zero-based vertices:02d}\\n"
            ),
            "minimizer_stream_sha256": q5.minimizer_stream_sha256,
            "minimizers_zero_based": [
                list(vertices) for vertices in EXCEPTIONAL_Q5_MINIMIZERS
            ],
        },
        "size_6": {
            "q": q6.value,
            "transversal_count": q6.candidate_count,
            "minimizer_count": q6.minimizer_count,
            "minimizer_stream_encoding": (
                "s={size} X={comma-separated zero-based vertices:02d}\\n"
            ),
            "minimizer_stream_sha256": q6.minimizer_stream_sha256,
            "unique_minimizer_zero_based": list(
                EXCEPTIONAL_Q6_MINIMIZERS[0]
            ),
            "missed_independent_triples_zero_based": [
                list(vertices) for vertices in EXCEPTIONAL_MISSED_I3
            ],
        },
    }


def write_classification_temp(
    *,
    path: Path,
    a_profiles: Sequence[AProfile],
    h_profiles: Sequence[HProfile],
) -> tuple[Path, dict[str, object], dict[str, object]]:
    """Build and fsync the pair stream, but do not publish it yet."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)
    stream_hasher = hashlib.sha256()
    terminal_hasher = hashlib.sha256()
    record_count = 0
    byte_count = 0
    capacity_count = 0
    terminal_count = 0
    finite_margin_histogram: Counter[int] = Counter()
    impossible_size_histogram: Counter[int] = Counter()
    terminal_high_minimum_histogram: Counter[int] = Counter()
    terminal_h_indices: list[int] = []
    surviving_a_indices: set[int] = set()
    surviving_h_indices: set[int] = set()
    missed_triple = EXCEPTIONAL_MISSED_I3[0]

    try:
        with os.fdopen(descriptor, "wb") as handle:
            for a_profile in a_profiles:
                upper = 4 * len(a_profile.independent3)
                for h_profile in h_profiles:
                    lower, impossible_size = capacity_lower_bound(
                        a_profile, h_profile
                    )
                    if lower is None or lower > upper:
                        line = capacity_line(
                            a_index=a_profile.index,
                            h_profile=h_profile,
                            lower=lower,
                            upper=upper,
                            impossible_size=impossible_size,
                        )
                        capacity_count += 1
                        if lower is None:
                            assert impossible_size is not None
                            impossible_size_histogram[impossible_size] += 1
                        else:
                            finite_margin_histogram[lower - upper] += 1
                    else:
                        surviving_a_indices.add(a_profile.index)
                        surviving_h_indices.add(h_profile.index)
                        if (
                            a_profile.index != EXCEPTIONAL_A_INDEX
                            or dict(h_profile.size_histogram) != {5: 8, 6: 16}
                            or lower != 296
                            or upper != 296
                        ):
                            raise ValueError(
                                "unexpected capacity survivor escaped"
                            )
                        degree_histogram = Counter(h_profile.degrees)
                        if dict(sorted(degree_histogram.items())) != (
                            EXCEPTIONAL_H_DEGREE_HISTOGRAM
                        ):
                            raise ValueError(
                                "terminal H degree sequence changed"
                            )
                        edge, high_minimum = first_high_edge(
                            h_profile, degree=11
                        )
                        if high_minimum < 3:
                            raise ValueError(
                                "terminal high-degree counting bound failed"
                            )
                        line = terminal_line(
                            h_profile=h_profile,
                            lower=lower,
                            upper=upper,
                            edge=edge,
                            missed_triple=missed_triple,
                        )
                        terminal_hasher.update(line)
                        terminal_count += 1
                        terminal_h_indices.append(h_profile.index)
                        terminal_high_minimum_histogram[high_minimum] += 1

                    handle.write(line)
                    stream_hasher.update(line)
                    byte_count += len(line)
                    record_count += 1
            handle.flush()
            os.fsync(handle.fileno())

        if (
            record_count != PAIR_COUNT
            or capacity_count != CAPACITY_EXCLUSION_COUNT
            or terminal_count != TERMINAL_EXCLUSION_COUNT
            or capacity_count + terminal_count != PAIR_COUNT
            or surviving_a_indices != {EXCEPTIONAL_A_INDEX}
            or len(surviving_h_indices) != TERMINAL_EXCLUSION_COUNT
            or terminal_h_indices != sorted(terminal_h_indices)
        ):
            raise ValueError("endpoint classification census changed")

        stream_summary = {
            "schema": CLASSIFICATION_SCHEMA,
            "path": str(path),
            "bytes": byte_count,
            "sha256": stream_hasher.hexdigest(),
            "record_count": record_count,
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
            "retained_pair_count": RETAINED_PAIR_COUNT,
            "finite_capacity_margin_histogram": {
                str(margin): finite_margin_histogram[margin]
                for margin in sorted(finite_margin_histogram)
            },
            "infinite_capacity_impossible_size_histogram": {
                str(size): impossible_size_histogram[size]
                for size in sorted(impossible_size_histogram)
            },
        }
        terminal_summary = {
            "terminal_line_stream_sha256": terminal_hasher.hexdigest(),
            "terminal_H_record_count": terminal_count,
            "terminal_H_cover_index_stream_sha256": digest(
                b"".join(
                    f"{index}\n".encode("ascii")
                    for index in terminal_h_indices
                )
            ),
            "minimum_degree_inside_degree_11_set_histogram": {
                str(value): terminal_high_minimum_histogram[value]
                for value in sorted(terminal_high_minimum_histogram)
            },
        }
        return temporary, stream_summary, terminal_summary
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def within_root(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


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


def build_and_write(
    *,
    root: Path,
    manifest_path: Path,
    classification_path: Path,
) -> tuple[dict[str, object], bytes]:
    """Build both artifacts and publish stream first, manifest last."""

    source_bindings = [
        local_file_binding(root, relative)
        for relative in SOURCE_BINDING_PATHS
    ]
    a_profiles, a_binding = read_a_profiles(root)
    h_profiles, h_binding = read_h_profiles(root)

    profile_payload = b"".join(
        a_profile_line(profile) for profile in a_profiles
    )
    exceptional = verify_exceptional_profile(
        a_profiles[EXCEPTIONAL_A_INDEX]
    )
    h_degree_histogram = Counter(
        degree_histogram_key(Counter(profile.degrees))
        for profile in h_profiles
    )

    temporary, stream_summary, terminal_summary = write_classification_temp(
        path=classification_path,
        a_profiles=a_profiles,
        h_profiles=h_profiles,
    )
    try:
        stream_summary["path"] = str(
            classification_path.resolve().relative_to(root)
        )
        manifest: dict[str, object] = {
            "schema": SCHEMA,
            "status": (
                "EXACT_EXCLUSION_OF_REGULAR_D18_E85_E128_ENDPOINT_"
                "CONDITIONAL_ON_PUBLISHED_CATALOG_COMPLETENESS"
            ),
            "theorem": {
                "ambient_order": 43,
                "global_regular_degree": 18,
                "root_degree": 18,
                "A_definition": "root neighborhood",
                "A_order": A_ORDER,
                "A_edge_count": A_EDGE_COUNT,
                "H_definition": (
                    "complement of the root antineighborhood"
                ),
                "H_order": H_ORDER,
                "H_edge_count": H_EDGE_COUNT,
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
            },
            "catalogs": {
                "A": a_binding,
                "H": h_binding,
                "publisher_page": (
                    "https://users.cecs.anu.edu.au/~bdm/data/ramsey.html"
                ),
            },
            "capacity_profiles": {
                "A_profile_stream_encoding": (
                    "A={index:02d} I3={count:03d} I4={count:03d} "
                    "S{s}={q|INF}/{transversals:05d}/"
                    "{minimizers:05d}/{minimizer_stream_sha256|-}\\n"
                ),
                "A_profile_stream_bytes": len(profile_payload),
                "A_profile_stream_sha256": digest(profile_payload),
                "H_degree_sequence_histogram": {
                    key: h_degree_histogram[key]
                    for key in sorted(h_degree_histogram)
                },
            },
            "classification": stream_summary,
            "terminal_obstruction": {
                "exceptional_A": exceptional,
                "capacity_equality": (
                    "8*q_5+16*q_6=8*17+16*10=296=4*74"
                ),
                "terminal_H_degree_histogram": {
                    "10": 8,
                    "11": 16,
                },
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
            },
            "claim_boundary": (
                "This locally excludes all 62,382 fixed-side pairs only at "
                "the regular degree-18 endpoint e(A)=85,e(H)=128. Catalog "
                "completeness and pairwise nonisomorphism are inherited "
                "from the publisher. It does not exclude e(A)=81 through "
                "84, the remainder of the regular degree-18 branch, any "
                "other one of the six global branches, or arbitrary "
                "order-43 graphs. No Ramsey-bound change follows by itself."
            ),
            "execution": {
                "solver_calls": 0,
                "proof_jobs": 0,
                "formulas_materialized": 0,
                "classification_records_materialized": PAIR_COUNT,
            },
            "local_derivation_bindings": source_bindings,
        }
        manifest_payload = canonical_json(manifest)
        os.replace(temporary, classification_path)
        atomic_write(manifest_path, manifest_payload)
        return manifest, manifest_payload
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(
            "results/benchmark_plans/"
            "branch18_regular_endpoint_capacity_cover_v1.json"
        ),
    )
    parser.add_argument(
        "--classifications",
        type=Path,
        default=Path(
            "certificates/"
            "branch18_regular_endpoint_capacity_cover_v1.pairs"
        ),
    )
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    manifest_path = (
        arguments.manifest
        if arguments.manifest.is_absolute()
        else root / arguments.manifest
    )
    classification_path = (
        arguments.classifications
        if arguments.classifications.is_absolute()
        else root / arguments.classifications
    )
    protected_paths = {
        (root / A_CATALOG_RELATIVE).resolve(),
        (root / H_CATALOG_RELATIVE).resolve(),
    }
    protected_paths.update(
        (root / relative).resolve() for relative in SOURCE_BINDING_PATHS
    )
    if (
        not within_root(root, manifest_path)
        or not within_root(root, classification_path)
        or manifest_path.resolve() == classification_path.resolve()
        or manifest_path.resolve() in protected_paths
        or classification_path.resolve() in protected_paths
    ):
        raise SystemExit(
            "refusing outputs outside root, overlapping each other, or "
            "overlapping frozen inputs"
        )

    _, manifest_payload = build_and_write(
        root=root,
        manifest_path=manifest_path,
        classification_path=classification_path,
    )
    print(
        json.dumps(
            {
                "manifest": str(manifest_path),
                "manifest_sha256": digest(manifest_payload),
                "classifications": str(classification_path),
                "pair_count": PAIR_COUNT,
                "capacity_exclusions": CAPACITY_EXCLUSION_COUNT,
                "terminal_exclusions": TERMINAL_EXCLUSION_COUNT,
                "retained_pairs": RETAINED_PAIR_COUNT,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
