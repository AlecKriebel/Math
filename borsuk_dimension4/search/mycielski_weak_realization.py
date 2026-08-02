#!/usr/bin/env python3
"""Exact combinatorial screens for weak diameter realizations of M^3(C5).

The exact-realization obstruction in ``mycielski_tower_screen.py`` uses the
top Mycielski original--shadow slack matrix.  A weak realization may turn
some of its formerly positive entries into zero.  This program enumerates
small sets of those new cross-layer zeros and applies two kinds of exact
certificates:

* monotone forbidden-subgraph/local diameter-graph tests; and
* the rank-five slack minor plus the four-polytope face-lattice certificate,
  recomputed after the new zeros are inserted.

No floating-point arithmetic is used.
"""

from __future__ import annotations

import argparse
import itertools
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Iterator, Sequence

from mycielski_tower_screen import Graph, common_mask, edge, tower


T0, T1, T2, T3 = tower()
N2 = T2.n
ALL2 = (1 << N2) - 1
NB2 = T2.neighbor_masks()


def popcount(mask: int) -> int:
    return mask.bit_count()


def bits(mask: int) -> Iterator[int]:
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def top_cross_edge(i: int, j: int) -> tuple[int, int]:
    """The T3 edge joining top original i to top shadow j."""

    return edge(i, N2 + j)


def cross_nonedges() -> tuple[tuple[int, int], ...]:
    """Directed T2 nonedges, identified with top original--shadow pairs."""

    return tuple(
        (i, j)
        for i in range(N2)
        for j in range(N2)
        if not T2.adjacent(i, j)
    )


CROSS_NONEDGES = cross_nonedges()


def augmented_graph(cross_additions: Iterable[tuple[int, int]],
                    other_additions: Iterable[tuple[int, int]] = ()) -> Graph:
    edges = list(T3.edges)
    edges.extend(top_cross_edge(i, j) for i, j in cross_additions)
    edges.extend(edge(u, v) for u, v in other_additions)
    return Graph.make(T3.n, edges, T3.labels)


def augmented_zero_masks(cross_additions: Iterable[tuple[int, int]]) -> tuple[int, ...]:
    """Zero pattern of B_ij=1-||x_i-y_j||^2 at the top level."""

    zeros = list(NB2)
    for i, j in cross_additions:
        zeros[i] |= 1 << j
    return tuple(zeros)


def d5_permutations(level: int = 2) -> tuple[tuple[int, ...], ...]:
    """The natural dihedral action inherited from the base 5-cycle."""

    answer: list[tuple[int, ...]] = []
    for sign in (1, -1):
        for shift in range(5):
            perm = tuple((sign * i + shift) % 5 for i in range(5))
            n = 5
            for _ in range(level):
                perm = perm + tuple(n + perm[i] for i in range(n)) + (2 * n,)
                n = 2 * n + 1
            answer.append(perm)
    return tuple(dict.fromkeys(answer))


D5_T2 = d5_permutations(2)


def canonical_cross_pattern(pattern: Iterable[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    pattern = tuple(pattern)
    images = []
    for perm in D5_T2:
        images.append(tuple(sorted((perm[i], perm[j]) for i, j in pattern)))
    return min(images)


def cross_orbits(patterns: Iterable[tuple[tuple[int, int], ...]]) -> dict[
        tuple[tuple[int, int], ...], list[tuple[tuple[int, int], ...]]]:
    result: dict[tuple[tuple[int, int], ...], list[tuple[tuple[int, int], ...]]] = defaultdict(list)
    for pattern in patterns:
        result[canonical_cross_pattern(pattern)].append(pattern)
    return dict(result)


# A known triangular rank-five minor from the exact-realization certificate.
_T2_INDEX = T2.label_index()
BASE_MINOR_ROWS = tuple(_T2_INDEX[label] for label in (
    "O2(O1(c0))",
    "O2(O1(c2))",
    "O2(S1(c0))",
    "S2(O1(c0))",
    "O2(O1(c1))",
))
BASE_MINOR_COLS = tuple(_T2_INDEX[label] for label in (
    "O2(O1(c0))",
    "O2(O1(c4))",
    "O2(S1(c1))",
    "S2(O1(c1))",
    "O2(O1(c1))",
))


def seed_triangular_minors() -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    minors = []
    for perm in D5_T2:
        rows = tuple(perm[i] for i in BASE_MINOR_ROWS)
        cols = tuple(perm[j] for j in BASE_MINOR_COLS)
        minors.append((rows, cols))
    return tuple(dict.fromkeys(minors))


SEED_MINORS = seed_triangular_minors()


def is_triangular_minor(
    zero_masks: Sequence[int], rows: Sequence[int], cols: Sequence[int]
) -> bool:
    """Check positive diagonal and forced-zero strict upper triangle."""

    if len(set(rows)) != len(rows) or len(set(cols)) != len(cols):
        return False
    for a, r in enumerate(rows):
        if zero_masks[r] & (1 << cols[a]):
            return False
        for b in range(a + 1, len(cols)):
            if not (zero_masks[r] & (1 << cols[b])):
                return False
    return True


def find_seed_rank_five_minor(
    zero_masks: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    for rows, cols in SEED_MINORS:
        if is_triangular_minor(zero_masks, rows, cols):
            return rows, cols
    return None


def find_triangular_minor(
    zero_masks: Sequence[int], size: int,
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    """Find a forced nonsingular triangular support minor exactly.

    Rows and columns are constructed from upper-left to lower-right.  Every
    new diagonal column must be zero in all earlier rows and positive in its
    own row.  Memoization is valid because future feasibility depends only on
    the common zero columns of the chosen rows and on the used row/column
    sets, not on their order.
    """

    all_columns = (1 << len(zero_masks)) - 1
    positive_masks = tuple(all_columns ^ z for z in zero_masks)
    failed: set[tuple[int, int, int, int]] = set()

    def search(
        depth: int,
        common_zeros: int,
        used_rows: int,
        used_cols: int,
        rows: tuple[int, ...],
        cols: tuple[int, ...],
    ) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
        if depth == size:
            return rows, cols
        state = (depth, common_zeros, used_rows, used_cols)
        if state in failed:
            return None
        remaining_after = size - depth - 1
        row_candidates = all_columns & ~used_rows
        while row_candidates:
            rbit = row_candidates & -row_candidates
            row_candidates ^= rbit
            r = rbit.bit_length() - 1
            diagonal_columns = common_zeros & positive_masks[r] & ~used_cols
            new_common = common_zeros & zero_masks[r]
            while diagonal_columns:
                cbit = diagonal_columns & -diagonal_columns
                diagonal_columns ^= cbit
                new_used_cols = used_cols | cbit
                if popcount(new_common & ~new_used_cols) < remaining_after:
                    continue
                answer = search(
                    depth + 1,
                    new_common,
                    used_rows | rbit,
                    new_used_cols,
                    rows + (r,),
                    cols + (cbit.bit_length() - 1,),
                )
                if answer is not None:
                    return answer
        failed.add(state)
        return None

    return search(0, all_columns, 0, 0, (), ())


@dataclass(frozen=True)
class PolytopeCertificate:
    excluded: bool
    stage: str
    detail: str
    facets: int = 0
    ridges: int = 0
    edges: int = 0
    vertices: int = N2


def augmented_polytope_certificate(
    cross_additions: Iterable[tuple[int, int]],
) -> PolytopeCertificate:
    """Re-run the exact 4-polytope contradiction for an augmented zero pattern.

    ``excluded`` means the zero/nonzero support alone proves that no weak
    realization can have exactly this top cross-layer diameter pattern.
    """

    additions = tuple(cross_additions)
    zeros = augmented_zero_masks(additions)
    rank_six = find_triangular_minor(zeros, 6)
    if rank_six is not None:
        return PolytopeCertificate(
            True,
            "rank-six",
            f"forced triangular minor rows={rank_six[0]}, columns={rank_six[1]}",
        )
    minor = find_seed_rank_five_minor(zeros)
    if minor is None:
        minor = find_triangular_minor(zeros, 5)
    if minor is None:
        return PolytopeCertificate(False, "rank", "no triangular rank-five minor was found")

    face_masks = tuple(zeros)
    if any(mask == ALL2 for mask in face_masks):
        return PolytopeCertificate(False, "facet", "a displayed face contains every shadow")
    if len(set(face_masks)) != N2:
        return PolytopeCertificate(False, "facet", "two displayed face vertex sets coincide")

    # A proper intersection with at least three vertices is a 2-face or
    # higher.  Since F_i is a proper face of a 4-polytope and x_i != 0,
    # this forces dim(F_i)=3, so F_i is a facet.
    witnesses: list[int] = []
    for i, fi in enumerate(face_masks):
        witness = None
        for j, fj in enumerate(face_masks):
            if i == j:
                continue
            inter = fi & fj
            if 3 <= popcount(inter) < popcount(fi):
                witness = j
                break
        if witness is None:
            return PolytopeCertificate(False, "facet", f"no facet witness for row {i}")
        witnesses.append(witness)

    ridges: dict[int, tuple[int, int]] = {}
    duplicate_ridge = None
    for i in range(N2):
        for j in range(i + 1, N2):
            inter = face_masks[i] & face_masks[j]
            if popcount(inter) < 3:
                continue
            if inter in ridges:
                duplicate_ridge = (inter, ridges[inter], (i, j))
                break
            ridges[inter] = (i, j)
        if duplicate_ridge is not None:
            break
    if duplicate_ridge is not None:
        mask, pair1, pair2 = duplicate_ridge
        # A ridge of a convex 4-polytope lies in exactly two facets.  The
        # same >=3-vertex intersection displayed by two different facet
        # pairs is therefore already an exact contradiction.
        return PolytopeCertificate(
            True,
            "duplicate-ridge",
            f"vertices {tuple(bits(mask))} arise from facet pairs {pair1} and {pair2}",
            facets=N2,
        )

    edge_masks: set[int] = set()
    for i in range(N2):
        for j in range(i + 1, N2):
            for k in range(j + 1, N2):
                inter = face_masks[i] & face_masks[j] & face_masks[k]
                if popcount(inter) == 2:
                    edge_masks.add(inter)

    # Each displayed ridge must have exactly the captured edges of one
    # polygon: a connected 2-regular graph on all its vertices.
    for ridge_mask, pair in ridges.items():
        local_edges = [m for m in edge_masks if (m & ridge_mask) == m]
        degree = {v: 0 for v in bits(ridge_mask)}
        adjacency = {v: set() for v in bits(ridge_mask)}
        for emask in local_edges:
            u, v = tuple(bits(emask))
            degree[u] += 1
            degree[v] += 1
            adjacency[u].add(v)
            adjacency[v].add(u)
        if any(degree[v] > 2 for v in degree):
            return PolytopeCertificate(
                True,
                "ridge-overdegree",
                f"ridge {pair} has a vertex incident with more than two forced polygon edges",
                facets=N2,
                ridges=len(ridges),
                edges=len(edge_masks),
            )

        # A captured cycle on only part of the ridge is also impossible: its
        # vertices have already used both polygon edges, so the remaining
        # ridge vertices cannot be spliced into the unique boundary cycle.
        unseen = set(degree)
        while unseen:
            start = next(iter(unseen))
            component = {start}
            queue = deque([start])
            unseen.remove(start)
            while queue:
                u = queue.popleft()
                for v in adjacency[u]:
                    if v in unseen:
                        unseen.remove(v)
                        component.add(v)
                        queue.append(v)
            if component != set(degree) and all(degree[v] == 2 for v in component):
                return PolytopeCertificate(
                    True,
                    "ridge-premature-cycle",
                    f"ridge {pair} contains a closed captured cycle omitting other ridge vertices",
                    facets=N2,
                    ridges=len(ridges),
                    edges=len(edge_masks),
                )

        if any(degree[v] != 2 for v in degree):
            return PolytopeCertificate(
                False,
                "ridge",
                f"ridge {pair} is not certified as a polygonal cycle",
                facets=N2,
                ridges=len(ridges),
                edges=len(edge_masks),
            )
        start = next(iter(degree))
        seen = {start}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
        if len(seen) != len(degree):
            return PolytopeCertificate(
                False,
                "ridge",
                f"ridge {pair} has a disconnected captured edge graph",
                facets=N2,
                ridges=len(ridges),
                edges=len(edge_masks),
            )

    # In every displayed facet, check the elementary completion lemma used in
    # the exact certificate: each listed edge is incident with two listed
    # polygonal ridges, and V-E+F=2.  Hence its listed boundary is already a
    # complete polyhedral 2-sphere; the facet has no undisplayed ridge.
    for i, facet_mask in enumerate(face_masks):
        facet_edges = [e for e in edge_masks if (e & facet_mask) == e]
        facet_ridges = [
            ridge_mask
            for ridge_mask, pair in ridges.items()
            if i in pair
        ]
        for emask in facet_edges:
            incidence = sum((emask & ridge_mask) == emask for ridge_mask in facet_ridges)
            if incidence != 2:
                return PolytopeCertificate(
                    False,
                    "local-completion",
                    f"facet {i} has an edge in {incidence} displayed ridges",
                    facets=N2,
                    ridges=len(ridges),
                    edges=len(edge_masks),
                )
        euler = popcount(facet_mask) - len(facet_edges) + len(facet_ridges)
        if euler != 2:
            # Every displayed ridge has its complete polygon boundary, and
            # every displayed edge is saturated by two displayed ridges.
            # Hence these ridges form a closed component of the ridge-dual
            # graph of this 3-polytope facet.  That dual graph is connected,
            # so the displayed component is the whole boundary and must have
            # Euler characteristic 2.  A different value is a contradiction,
            # not merely a failure of the completion certificate.
            return PolytopeCertificate(
                True,
                "local-euler",
                f"facet {i} has local Euler value {euler}",
                facets=N2,
                ridges=len(ridges),
                edges=len(edge_masks),
            )

    # The displayed facet-ridge dual graph must be connected.  The local
    # completion lemma then leaves no place for an undisplayed facet.
    dual = [set() for _ in range(N2)]
    for i, j in ridges.values():
        dual[i].add(j)
        dual[j].add(i)
    reached = {0}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j in dual[i] - reached:
            reached.add(j)
            queue.append(j)
    if len(reached) != N2:
        return PolytopeCertificate(
            False,
            "dual-connectivity",
            f"only {len(reached)} of {N2} displayed facets are connected",
            facets=N2,
            ridges=len(ridges),
            edges=len(edge_masks),
        )

    # All facets have supporting inequalities x_i.y >= ||x_i||^2/2 > 0.
    # Their intersection contains every outward ray through a point of P,
    # contradicting boundedness.  Thus the zero pattern is impossible.
    return PolytopeCertificate(
        True,
        "positive-facet-completion",
        "the displayed positive-offset facets are complete, forcing an unbounded polytope",
        facets=N2,
        ridges=len(ridges),
        edges=len(edge_masks),
    )


def colorable(graph: Graph, vertices_mask: int, colors: int) -> bool:
    """Exact DSATUR-style backtracking on an induced subgraph."""

    vertices = tuple(bits(vertices_mask))
    if len(vertices) <= colors:
        return True
    assigned = [-1] * graph.n
    uncolored = set(vertices)
    nb = graph.neighbor_masks()

    def search() -> bool:
        if not uncolored:
            return True
        v = max(
            uncolored,
            key=lambda x: (
                len({assigned[y] for y in bits(nb[x] & vertices_mask)
                     if assigned[y] >= 0}),
                popcount(nb[x] & vertices_mask),
                -x,
            ),
        )
        forbidden = {
            assigned[y]
            for y in bits(nb[v] & vertices_mask)
            if assigned[y] >= 0
        }
        uncolored.remove(v)
        for c in range(colors):
            if c in forbidden:
                continue
            assigned[v] = c
            if search():
                assigned[v] = -1
                uncolored.add(v)
                return True
        assigned[v] = -1
        uncolored.add(v)
        return False

    return search()


def clique_of_size(graph: Graph, size: int) -> tuple[int, ...] | None:
    """Return an exact clique witness, if one exists."""

    nb = graph.neighbor_masks()

    def extend(chosen: tuple[int, ...], candidates: int) -> tuple[int, ...] | None:
        need = size - len(chosen)
        if need == 0:
            return chosen
        if popcount(candidates) < need:
            return None
        while candidates:
            vbit = candidates & -candidates
            v = vbit.bit_length() - 1
            candidates ^= vbit
            result = extend(chosen + (v,), candidates & nb[v])
            if result is not None:
                return result
            if popcount(candidates) < need:
                return None
        return None

    return extend((), (1 << graph.n) - 1)


def k6_minus_edge(graph: Graph) -> tuple[int, ...] | None:
    """Find six vertices spanning at least 14 edges."""

    # A 5-clique plus a vertex adjacent to at least four clique vertices is
    # equivalent to containment of K6-e (with K6 included).
    nb = graph.neighbor_masks()

    def five_cliques() -> Iterator[tuple[int, ...]]:
        def extend(chosen: tuple[int, ...], candidates: int) -> Iterator[tuple[int, ...]]:
            if len(chosen) == 5:
                yield chosen
                return
            need = 5 - len(chosen)
            while candidates and popcount(candidates) >= need:
                bit = candidates & -candidates
                candidates ^= bit
                v = bit.bit_length() - 1
                yield from extend(chosen + (v,), candidates & nb[v])
        yield from extend((), (1 << graph.n) - 1)

    for clique in five_cliques():
        cmask = (1 << graph.n) - 1
        for v in clique:
            cmask &= nb[v]
        # K6 case.
        if cmask:
            return clique + (next(bits(cmask)),)
        for omitted in clique:
            mask = (1 << graph.n) - 1
            for v in clique:
                if v != omitted:
                    mask &= nb[v]
            mask &= ~sum(1 << v for v in clique)
            if mask:
                return clique + (next(bits(mask)),)
    return None


def bad_common_neighborhood(graph: Graph) -> tuple[tuple[int, int], tuple[int, ...]] | None:
    nb = graph.neighbor_masks()
    for u, v in graph.edges:
        mask = nb[u] & nb[v]
        if not colorable(graph, mask, 3):
            return (u, v), tuple(bits(mask))
    return None


def edge_count_at_least(graph: Graph, mask: int, threshold: int) -> bool:
    count = 0
    for u, v in graph.edges:
        if mask & (1 << u) and mask & (1 << v):
            count += 1
            if count >= threshold:
                return True
    return False


def crossed_two_edge_blocks(graph: Graph) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    """Find completely cross-joined blocks, each containing two edges."""

    nb = graph.neighbor_masks()
    all_vertices = (1 << graph.n) - 1
    support_masks = sorted({
        (1 << a) | (1 << b) | (1 << c) | (1 << d)
        for (a, b), (c, d) in itertools.combinations(graph.edges, 2)
    })
    for left in support_masks:
        common = common_mask(nb, bits(left), all_vertices) & ~left
        if popcount(common) < 3:
            continue
        if edge_count_at_least(graph, common, 2):
            # Extract a small witness block containing its first two edges.
            selected = []
            for u, v in graph.edges:
                if common & (1 << u) and common & (1 << v):
                    selected.extend((u, v))
                    if len({*selected}) >= 3 and sum(
                        1 for a, b in graph.edges
                        if a in set(selected) and b in set(selected)
                    ) >= 2:
                        return tuple(bits(left)), tuple(sorted(set(selected)))
    return None


@dataclass(frozen=True)
class GraphScreen:
    excluded: bool
    reason: str
    witness: object | None = None


def screen_graph(graph: Graph) -> GraphScreen:
    k6e = k6_minus_edge(graph)
    if k6e is not None:
        return GraphScreen(True, "K6-e", k6e)
    k5 = clique_of_size(graph, 5)
    if k5 is not None:
        # A diameter K5 yields a five-cell simplex/Voronoi partition, contrary
        # to the inherited six-chromatic T3 subgraph.
        return GraphScreen(True, "K5", k5)
    bad_common = bad_common_neighborhood(graph)
    if bad_common is not None:
        return GraphScreen(True, "common-neighborhood-not-3-colorable", bad_common)
    crossed = crossed_two_edge_blocks(graph)
    if crossed is not None:
        return GraphScreen(True, "crossed-two-edge-blocks", crossed)
    return GraphScreen(False, "survives")


def monotone_graph_screen(cross_additions: Iterable[tuple[int, int]]) -> GraphScreen:
    return screen_graph(augmented_graph(cross_additions))


def all_t3_nonedges() -> tuple[tuple[int, int], ...]:
    return tuple(
        (u, v)
        for u in range(T3.n)
        for v in range(u + 1, T3.n)
        if not T3.adjacent(u, v)
    )


def analyze_all_single_edge_supergraphs() -> Counter[str]:
    reasons: Counter[str] = Counter()
    for uv in all_t3_nonedges():
        reasons[screen_graph(augmented_graph((), (uv,))).reason] += 1
    return reasons


def analyze_single_cross_additions(run_graph_screens: bool = True) -> dict[str, object]:
    records = []
    for addition in CROSS_NONEDGES:
        pattern = (addition,)
        poly = augmented_polytope_certificate(pattern)
        graph = monotone_graph_screen(pattern) if run_graph_screens else None
        records.append((addition, poly, graph))
    orbit_records = defaultdict(list)
    for record in records:
        orbit_records[canonical_cross_pattern((record[0],))].append(record)
    return {
        "records": records,
        "orbits": dict(orbit_records),
        "poly_stages": Counter(poly.stage for _, poly, _ in records),
        "poly_excluded": sum(poly.excluded for _, poly, _ in records),
        "graph_reasons": Counter(graph.reason for _, _, graph in records if graph is not None),
    }


def print_single_summary(run_graph_screens: bool = True) -> None:
    result = analyze_single_cross_additions(run_graph_screens)
    total_nonedges = len(all_t3_nonedges())
    noncross = total_nonedges - len(CROSS_NONEDGES)
    cross_survivors = len(CROSS_NONEDGES) - int(result["poly_excluded"])
    surviving_orbits = [
        (representative, records)
        for representative, records in sorted(result["orbits"].items())
        if not records[0][1].excluded
    ]
    print(f"T2 vertices: {N2}")
    print(f"T3 vertices/edges: {T3.n}/{len(T3.edges)}")
    print(f"all one-edge supergraphs: {total_nonedges}")
    print(f"directed top cross nonedges: {len(CROSS_NONEDGES)}")
    print(f"noncross additions excluded by the unchanged certificate: {noncross}")
    print(f"D5 single-addition orbits: {len(result['orbits'])}")
    print(f"polytope exclusions: {result['poly_excluded']}/{len(CROSS_NONEDGES)}")
    print(
        "complete one-edge census: "
        f"excluded={noncross + int(result['poly_excluded'])}, "
        f"surviving={cross_survivors} in {len(surviving_orbits)} D5 orbits"
    )
    print(f"polytope terminal stages: {dict(result['poly_stages'])}")
    if run_graph_screens:
        print(f"graph-screen reasons: {dict(result['graph_reasons'])}")
    print("orbit representatives:")
    for representative, records in sorted(result["orbits"].items()):
        _, poly, graph = records[0]
        graph_reason = graph.reason if graph is not None else "not-run"
        invariant = {(r[1].excluded, r[1].stage, r[2].reason if r[2] else None) for r in records}
        print(
            f"  {representative}: orbit={len(records)}, "
            f"poly={poly.excluded}:{poly.stage}, graph={graph_reason}, "
            f"constant={len(invariant) == 1}"
        )
    print("surviving orbit representatives (T2 row label -> T2 column label):")
    nb3 = T3.neighbor_masks()
    common_histogram: Counter[int] = Counter()
    for representative, records in surviving_orbits:
        (i, j), = representative
        u, v = top_cross_edge(i, j)
        common = popcount(nb3[u] & nb3[v])
        common_histogram[common] += len(records)
        print(
            f"  {T2.labels[i]} -> {T2.labels[j]}: "
            f"indices=({i},{j}), orbit={len(records)}, "
            f"old-common-neighbors={common}, break-stage={records[0][1].stage}"
        )
    print(f"surviving common-neighbor histogram: {dict(sorted(common_histogram.items()))}")


def print_all_single_graph_summary() -> None:
    print(f"all T3 nonedges: {len(all_t3_nonedges())}")
    print(f"single-edge graph-screen reasons: {dict(analyze_all_single_edge_supergraphs())}")


def dihedral_cross_orbit_patterns() -> list[
        tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]]:
    orbits = cross_orbits(((addition,) for addition in CROSS_NONEDGES))
    return [
        (representative, tuple(member[0] for member in members))
        for representative, members in sorted(orbits.items())
    ]


def print_symmetric_orbit_summary(run_pairs: bool = False) -> None:
    records = []
    for representative, pattern in dihedral_cross_orbit_patterns():
        poly = augmented_polytope_certificate(pattern)
        graph = monotone_graph_screen(pattern)
        records.append((representative, pattern, poly, graph))
    print(f"single D5-orbit augmentations: {len(records)}")
    print("polytope stages:", dict(Counter((p.excluded, p.stage) for _, _, p, _ in records)))
    print("graph stages:", dict(Counter((g.excluded, g.reason) for _, _, _, g in records)))
    survivors = [record for record in records if not record[2].excluded and not record[3].excluded]
    print(f"jointly surviving single-orbit augmentations: {len(survivors)}")
    for representative, pattern, poly, graph in survivors:
        (i, j), = representative
        print(
            f"  {T2.labels[i]} -> {T2.labels[j]}: "
            f"representative=({i},{j}), added={len(pattern)}, break-stage={poly.stage}"
        )

    diagonal = tuple((i, i) for i in range(N2))
    diagonal_poly = augmented_polytope_certificate(diagonal)
    diagonal_graph = monotone_graph_screen(diagonal)
    print(
        "full 23-edge diagonal matching: "
        f"poly={diagonal_poly.excluded}:{diagonal_poly.stage}, "
        f"graph={diagonal_graph.excluded}:{diagonal_graph.reason}"
    )

    if run_pairs:
        pair_counts: Counter[str] = Counter()
        pair_stages: Counter[tuple[bool, str]] = Counter()
        for first, second in itertools.combinations(survivors, 2):
            pattern = first[1] + second[1]
            poly = augmented_polytope_certificate(pattern)
            graph = monotone_graph_screen(pattern)
            pair_stages[(poly.excluded, poly.stage)] += 1
            if poly.excluded and graph.excluded:
                pair_counts["both"] += 1
            elif poly.excluded:
                pair_counts["polytope"] += 1
            elif graph.excluded:
                pair_counts["graph"] += 1
            else:
                pair_counts["survives"] += 1
        print(f"pairs of surviving orbit augmentations: {sum(pair_counts.values())}")
        print(f"pair outcome counts: {dict(pair_counts)}")
        print(f"pair polytope stages: {dict(pair_stages)}")


def print_diagonal_orbit_union_summary() -> None:
    diagonal_orbits = [
        (representative, pattern)
        for representative, pattern in dihedral_cross_orbit_patterns()
        if representative[0][0] == representative[0][1]
    ]
    outcomes: Counter[str] = Counter()
    poly_stages: Counter[tuple[bool, str]] = Counter()
    graph_stages: Counter[tuple[bool, str]] = Counter()
    for choice in range(1, 1 << len(diagonal_orbits)):
        pattern = tuple(
            addition
            for k, (_, orbit) in enumerate(diagonal_orbits)
            if choice & (1 << k)
            for addition in orbit
        )
        poly = augmented_polytope_certificate(pattern)
        graph = monotone_graph_screen(pattern)
        poly_stages[(poly.excluded, poly.stage)] += 1
        graph_stages[(graph.excluded, graph.reason)] += 1
        if poly.excluded and graph.excluded:
            outcomes["both"] += 1
        elif poly.excluded:
            outcomes["polytope"] += 1
        elif graph.excluded:
            outcomes["graph"] += 1
        else:
            outcomes["survives"] += 1
    print(f"diagonal D5 orbits: {len(diagonal_orbits)}")
    print(f"nonempty diagonal-orbit unions: {(1 << len(diagonal_orbits)) - 1}")
    print(f"diagonal-union outcomes: {dict(outcomes)}")
    print(f"diagonal-union polytope stages: {dict(poly_stages)}")
    print(f"diagonal-union graph stages: {dict(graph_stages)}")


def verify_hom_c5_antipodal_cycle() -> tuple[tuple[int, int], ...]:
    """Verify the explicit equivariant decagon S^1 -> Hom(K2,C5)."""

    cycle = (
        (0, 1),
        (0, 4),
        (3, 4),
        (3, 2),
        (1, 2),
        (1, 0),
        (4, 0),
        (4, 3),
        (2, 3),
        (2, 1),
    )
    assert len(set(cycle)) == 10
    assert set(cycle) == {
        (u, v)
        for u, v in itertools.permutations(range(T0.n), 2)
        if T0.adjacent(u, v)
    }
    for k, ((a, b), (c, d)) in enumerate(zip(cycle, cycle[1:] + cycle[:1])):
        # Consecutive oriented edges span a product-cell edge in Hom(K2,C5):
        # either the left shore is fixed and the two right vertices are its
        # neighbors, or conversely.
        valid = (
            a == c and T0.adjacent(a, b) and T0.adjacent(a, d)
        ) or (
            b == d and T0.adjacent(a, b) and T0.adjacent(c, b)
        )
        assert valid, (k, cycle[k], cycle[(k + 1) % 10])
        assert cycle[(k + 5) % 10] == (b, a)
    return cycle


def verify_mycielski_hom_suspension(g: Graph, mg: Graph) -> None:
    """Check the edge identities behind Sigma Hom(K2,G) -> Hom(K2,M(G))."""

    n = g.n
    assert mg.n == 2 * n + 1
    apex = 2 * n
    for a, b in g.edges:
        for u, v in ((a, b), (b, a)):
            # Stage 1: (O alpha,O beta) -> (O alpha,S beta).
            assert mg.adjacent(u, v)
            assert mg.adjacent(u, n + v)
            # Stage 2: (O alpha,S beta) -> (w,S beta).
            assert mg.adjacent(apex, n + v)
    # Stage 3 contracts the shadow-side distribution to one fixed
    # distribution on all shadows while the other shore is the apex.
    assert all(mg.adjacent(apex, n + v) for v in range(n))


def verify_topological_obstruction() -> None:
    """Verify the finite skeleton of the global weak-realization obstruction."""

    cycle = verify_hom_c5_antipodal_cycle()
    verify_mycielski_hom_suspension(T0, T1)
    verify_mycielski_hom_suspension(T1, T2)
    verify_mycielski_hom_suspension(T2, T3)
    # Three equivariant suspensions of the antipodal S^1 decagon give an
    # equivariant S^4 -> Hom(K2,T3).  The analytic center-vector theorem gives
    # edge products <= -1/4, strictly negative as required by the Hom-to-sphere
    # normalization map.
    assert Fraction(-1, 4) < 0
    assert len(cycle) == 10
    print("topological obstruction skeleton: PASS")
    print("equivariant chain: S^1 -> Hom(K2,T0), then three suspensions -> S^4 -> Hom(K2,T3)")
    print("rank-4 obtuse vectors would give an impossible antipodal map S^4 -> S^3")


def self_test() -> None:
    assert N2 == 23 and T3.n == 47
    assert len(T2.edges) == 71 and len(T3.edges) == 236
    assert len(CROSS_NONEDGES) == N2 * N2 - 2 * len(T2.edges) == 387
    base_zeros = augmented_zero_masks(())
    assert find_seed_rank_five_minor(base_zeros) is not None
    base_cert = augmented_polytope_certificate(())
    assert base_cert.excluded and base_cert.stage == "positive-facet-completion"
    assert (base_cert.vertices, base_cert.edges, base_cert.ridges, base_cert.facets) == (23, 62, 62, 23)
    # T3 is maximal triangle-free: every missing edge has a common neighbor.
    for u in range(T3.n):
        for v in range(u + 1, T3.n):
            if not T3.adjacent(u, v):
                nb3 = T3.neighbor_masks()
                assert nb3[u] & nb3[v]
    print("self-test: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--single", action="store_true", help="screen all one-cross-edge augmentations")
    parser.add_argument("--all-single-graph", action="store_true",
                        help="run monotone graph screens on all one-edge supergraphs")
    parser.add_argument("--symmetric-orbits", action="store_true",
                        help="screen augmentations consisting of complete D5 edge orbits")
    parser.add_argument("--orbit-pairs", action="store_true",
                        help="also screen pairs of the surviving D5 edge orbits")
    parser.add_argument("--diagonal-unions", action="store_true",
                        help="screen all unions of the seven diagonal D5 edge orbits")
    parser.add_argument("--topological", action="store_true",
                        help="verify the Hom-complex/Mycielski obstruction skeleton")
    parser.add_argument("--skip-graph", action="store_true", help="skip slower monotone graph screens")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test or not args.single:
        self_test()
    if args.single:
        print_single_summary(not args.skip_graph)
    if args.all_single_graph:
        print_all_single_graph_summary()
    if args.symmetric_orbits or args.orbit_pairs:
        print_symmetric_orbit_summary(args.orbit_pairs)
    if args.diagonal_unions:
        print_diagonal_orbit_union_summary()
    if args.topological:
        verify_topological_obstruction()


if __name__ == "__main__":
    main()
