#!/usr/bin/env python3
"""Exact screen for the triangle-free six-chromatic Mycielski tower.

This file uses only the Python standard library.  It constructs

    T_0 = C_5,   T_{r+1} = M(T_r),

and proves, by a finite combinatorial certificate, that T_3 cannot be the
*exact* diameter graph of a set of distinct points in R^4.

The obstruction is recursive.  If T_3=M(T_2) had such a realization, put
the top apex at zero, call its shadows y_j, and call the originals x_i.  The
matrix

    B[i,j] = 1 - ||x_i-y_j||^2

has rank at most five, is zero on the edges of T_2, and is strictly positive
elsewhere.  A lower-triangular 5-by-5 support minor forces rank(B)=5, so the
y_j affinely span R^4.  They are distinct points on the unit sphere and are
therefore all vertices of their convex hull P.  Each neighborhood of T_2 is
the exact vertex set of an exposed face of P.

The certificate below checks that these 23 faces must be all 23 facets of P:
there are 62 specified polygonal ridges and 62 specified edges; on every one
of the seven C_5-orbit types of facets the data already form a complete
polyhedral 2-sphere.  But the supporting inequality for every one of these
facets is

    x_i . y >= ||x_i||^2 / 2 > 0.

Thus any q in P would bring the whole ray {tq:t>=1} into all facet
halfspaces, contradicting boundedness.

Strict positivity on graph nonedges is used.  Consequently this certificate
does not rule out a weak unit-diameter realization in which extra nonedges of
T_3 accidentally also attain the diameter.
"""

from __future__ import annotations

import itertools
from collections import Counter, deque
from dataclasses import dataclass
from typing import Iterable, Sequence


Edge = tuple[int, int]


def edge(i: int, j: int) -> Edge:
    if i == j:
        raise ValueError("loops are not allowed")
    return (i, j) if i < j else (j, i)


@dataclass(frozen=True)
class Graph:
    n: int
    edges: frozenset[Edge]
    labels: tuple[str, ...]

    @staticmethod
    def make(n: int, edges: Iterable[Edge], labels: Sequence[str]) -> "Graph":
        answer = Graph(n, frozenset(edge(i, j) for i, j in edges),
                       tuple(labels))
        if len(answer.labels) != n:
            raise ValueError("wrong label count")
        if any(not (0 <= i < j < n) for i, j in answer.edges):
            raise ValueError("edge endpoint out of range")
        return answer

    def neighbor_masks(self) -> tuple[int, ...]:
        masks = [0] * self.n
        for i, j in self.edges:
            masks[i] |= 1 << j
            masks[j] |= 1 << i
        return tuple(masks)

    def adjacent(self, i: int, j: int) -> bool:
        return i != j and edge(i, j) in self.edges

    def label_index(self) -> dict[str, int]:
        result = {label: i for i, label in enumerate(self.labels)}
        if len(result) != self.n:
            raise ValueError("labels are not unique")
        return result


def cycle_five() -> Graph:
    return Graph.make(
        5,
        ((i, (i + 1) % 5) for i in range(5)),
        [f"c{i}" for i in range(5)],
    )


def mycielski(g: Graph, level: int) -> Graph:
    """Return M(g): originals O, shadows S, and a new apex w."""
    n = g.n
    edges = set(g.edges)
    for i, j in g.edges:
        edges.add(edge(i, n + j))
        edges.add(edge(j, n + i))
    edges.update((n + i, 2 * n) for i in range(n))
    labels = [f"O{level}({label})" for label in g.labels]
    labels += [f"S{level}({label})" for label in g.labels]
    labels += [f"w{level}"]
    return Graph.make(2 * n + 1, edges, labels)


def tower() -> tuple[Graph, Graph, Graph, Graph]:
    graphs = [cycle_five()]
    for level in range(1, 4):
        graphs.append(mycielski(graphs[-1], level))
    return tuple(graphs)  # type: ignore[return-value]


def verify_coloring(g: Graph, colors: Sequence[int], deleted: int | None = None) -> None:
    if len(colors) != g.n:
        raise AssertionError("wrong coloring length")
    for i, j in g.edges:
        if i == deleted or j == deleted:
            continue
        if colors[i] < 0 or colors[j] < 0 or colors[i] == colors[j]:
            raise AssertionError((g.labels[i], g.labels[j], colors[i], colors[j]))


@dataclass(frozen=True)
class CriticalColorCertificate:
    chromatic: int
    coloring: tuple[int, ...]
    deletion_colorings: tuple[tuple[int, ...], ...]


def base_critical_certificate() -> CriticalColorCertificate:
    g = cycle_five()
    full = (0, 1, 0, 1, 2)
    verify_coloring(g, full)
    deleted: list[tuple[int, ...]] = []
    for gone in range(5):
        colors = [-1] * 5
        start = (gone + 1) % 5
        for step in range(4):
            colors[(start + step) % 5] = step % 2
        verify_coloring(g, colors, gone)
        deleted.append(tuple(colors))
    return CriticalColorCertificate(3, full, tuple(deleted))


def lift_critical_certificate(
    g: Graph, mg: Graph, cert: CriticalColorCertificate
) -> CriticalColorCertificate:
    """Construct the standard vertex-critical colorings for M(g).

    If g is k-vertex-critical, these are k-colorings after deleting any
    vertex of M(g).  The lower bound chi(M(g))=k+1 is proved in the report by
    the usual apex-color recoloring argument.
    """
    n = g.n
    k = cert.chromatic
    full = tuple(cert.coloring) + tuple(cert.coloring) + (k,)
    verify_coloring(mg, full)

    deleted: list[tuple[int, ...]] = []
    # Delete an original v_i: color g-i with k-1 old colors, put every
    # shadow in the new kth color, and give the apex any old color.
    for i in range(n):
        old = cert.deletion_colorings[i]
        colors = [-1] * (2 * n + 1)
        for j in range(n):
            if j != i:
                colors[j] = old[j]
            colors[n + j] = k - 1
        colors[2 * n] = 0
        verify_coloring(mg, colors, i)
        deleted.append(tuple(colors))

    # Delete shadow u_i: use a (k-1)-coloring of g-i, give v_i and the apex
    # the new color, and color every remaining shadow like its original.
    for i in range(n):
        old = cert.deletion_colorings[i]
        colors = [-1] * (2 * n + 1)
        for j in range(n):
            colors[j] = k - 1 if j == i else old[j]
            if j != i:
                colors[n + j] = old[j]
        colors[2 * n] = k - 1
        verify_coloring(mg, colors, n + i)
        deleted.append(tuple(colors))

    # Delete the apex: copy any k-coloring of g to both layers.
    colors = tuple(cert.coloring) + tuple(cert.coloring) + (-1,)
    verify_coloring(mg, colors, 2 * n)
    deleted.append(colors)
    return CriticalColorCertificate(k + 1, full, tuple(deleted))


def critical_certificates(graphs: Sequence[Graph]) -> tuple[CriticalColorCertificate, ...]:
    certs = [base_critical_certificate()]
    for g, mg in zip(graphs, graphs[1:]):
        certs.append(lift_critical_certificate(g, mg, certs[-1]))
    return tuple(certs)


def triangle_count(g: Graph) -> int:
    nb = g.neighbor_masks()
    return sum((nb[i] & nb[j]).bit_count() for i, j in g.edges) // 3


def completely_crossed_two_edge_blocks(g: Graph) -> tuple[int, int] | None:
    """Return block masks if the global two-edge block screen fires."""
    nb = g.neighbor_masks()
    all_vertices = (1 << g.n) - 1
    blocks: dict[int, tuple[Edge, Edge]] = {}
    for e1, e2 in itertools.combinations(sorted(g.edges), 2):
        mask = sum(1 << v for v in set((*e1, *e2)))
        blocks.setdefault(mask, (e1, e2))
    for left in blocks:
        common = all_vertices
        work = left
        while work:
            bit = work & -work
            work ^= bit
            common &= nb[bit.bit_length() - 1]
        if common.bit_count() < 3:
            continue
        internal = [
            e for e in g.edges
            if ((1 << e[0] | 1 << e[1]) & ~common) == 0
        ]
        if len(internal) >= 2:
            right = sum(1 << v for v in set((*internal[0], *internal[1])))
            return left, right
    return None


def inherited_screens(g: Graph) -> dict[str, object]:
    nb = g.neighbor_masks()
    triangles = triangle_count(g)
    universal = tuple(i for i, mask in enumerate(nb)
                      if mask.bit_count() == g.n - 1)
    # In a triangle-free graph every graph edge has empty common
    # neighborhood.  This simultaneously kills K6-e, K2 join C4, and any
    # nonempty completely crossed block opposite an internal edge.
    edge_common_max = max((nb[i] & nb[j]).bit_count() for i, j in g.edges)
    cross = completely_crossed_two_edge_blocks(g)
    nonedge_common = [
        (nb[i] & nb[j]).bit_count()
        for i in range(g.n)
        for j in range(i + 1, g.n)
        if not g.adjacent(i, j)
    ]
    assert triangles == 0
    assert not universal
    assert edge_common_max == 0
    assert cross is None
    assert min(nonedge_common) >= 1  # The tower is maximal triangle-free.
    return {
        "triangles": triangles,
        "universal_vertices": universal,
        "max_common_neighbors_of_an_edge": edge_common_max,
        "two_edge_cross_block": cross,
        "minimum_common_neighbors_of_a_nonedge": min(nonedge_common),
    }


def support_pattern(g: Graph, rows: Sequence[int], cols: Sequence[int]) -> tuple[str, ...]:
    return tuple(
        "".join("0" if g.adjacent(i, j) else "+" for j in cols)
        for i in rows
    )


def rank_five_minor(g: Graph) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """The forced nonsingular original-shadow slack minor for T_2."""
    ix = g.label_index()
    row_labels = (
        "O2(O1(c0))",
        "O2(O1(c2))",
        "O2(S1(c0))",
        "S2(O1(c0))",
        "O2(O1(c1))",
    )
    col_labels = (
        "O2(O1(c0))",
        "O2(O1(c4))",
        "O2(S1(c1))",
        "S2(O1(c1))",
        "O2(O1(c1))",
    )
    rows = tuple(ix[x] for x in row_labels)
    cols = tuple(ix[x] for x in col_labels)
    pattern = support_pattern(g, rows, cols)
    assert pattern == ("+0000", "++000", "+0+00", "+00+0", "0++++")
    for i in range(5):
        assert pattern[i][i] == "+"
        assert all(pattern[i][j] == "0" for j in range(i + 1, 5))
    return row_labels, col_labels, pattern


def common_mask(nb: Sequence[int], vertices: Iterable[int], all_vertices: int) -> int:
    result = all_vertices
    for v in vertices:
        result &= nb[v]
    return result


@dataclass(frozen=True)
class PolytopeCertificate:
    ridge_count: int
    edge_count: int
    ridge_size_histogram: tuple[tuple[int, int], ...]
    edge_facet_degree_histogram: tuple[tuple[int, int], ...]
    facet_orbit_table: tuple[tuple[str, int, int, int, int, str, int], ...]


def polytope_certificate(g: Graph) -> PolytopeCertificate:
    """Verify the finite face-lattice premises used by the obstruction."""
    if g.n != 23:
        raise ValueError("the certificate is for T_2")
    nb = g.neighbor_masks()
    all_vertices = (1 << g.n) - 1
    ix = g.label_index()

    # Every proposed face has at least four vertices and a distinct vertex
    # set.  The witness table below gives a proper subface with >=3 vertices,
    # which rules out dimension two and forces a facet of a 4-polytope.
    assert min(mask.bit_count() for mask in nb) == 4
    assert len(set(nb)) == g.n

    A = [ix[f"O2(O1(c{i}))"] for i in range(5)]
    B = [ix[f"O2(S1(c{i}))"] for i in range(5)]
    a = ix["O2(w1)"]
    C = [ix[f"S2(O1(c{i}))"] for i in range(5)]
    D = [ix[f"S2(S1(c{i}))"] for i in range(5)]
    b = ix["S2(w1)"]
    w = ix["w2"]

    dimension_witness: dict[int, int] = {}
    for i in range(5):
        dimension_witness[A[i]] = A[(i + 2) % 5]
        dimension_witness[B[i]] = A[i]
        dimension_witness[C[i]] = A[i]
        dimension_witness[D[i]] = B[i]
    dimension_witness[a] = A[0]
    dimension_witness[b] = a
    dimension_witness[w] = A[0]
    assert len(dimension_witness) == g.n
    for i, j in dimension_witness.items():
        count = (nb[i] & nb[j]).bit_count()
        assert 3 <= count < nb[i].bit_count()

    # A pair of distinct proposed facets with >=3 common vertices meets in a
    # polygonal ridge.  All 62 vertex masks are different.
    ridges: list[tuple[int, int, int]] = []
    for i, j in itertools.combinations(range(g.n), 2):
        vertices = nb[i] & nb[j]
        if vertices.bit_count() >= 3:
            ridges.append((i, j, vertices))
    ridge_masks = {vertices for _, _, vertices in ridges}
    assert len(ridges) == len(ridge_masks) == 62

    # An intersection of three facets with exactly two vertices is an edge.
    edge_masks: set[int] = set()
    for triple in itertools.combinations(range(g.n), 3):
        vertices = common_mask(nb, triple, all_vertices)
        if vertices.bit_count() == 2:
            edge_masks.add(vertices)
    assert len(edge_masks) == 62

    # In every proposed polygonal ridge, the specified edges make one cycle
    # through all of its vertices.  Hence they are its complete edge set.
    for ridge in ridge_masks:
        vertices = {i for i in range(g.n) if ridge >> i & 1}
        boundary = [e for e in edge_masks if e & ~ridge == 0]
        assert len(boundary) == len(vertices)
        adjacency = {i: set() for i in vertices}
        for e in boundary:
            endpoints = [i for i in vertices if e >> i & 1]
            assert len(endpoints) == 2
            u, v = endpoints
            adjacency[u].add(v)
            adjacency[v].add(u)
        assert all(len(adjacency[i]) == 2 for i in vertices)
        reached = set()
        queue = [next(iter(vertices))]
        while queue:
            u = queue.pop()
            if u not in reached:
                reached.add(u)
                queue.extend(adjacency[u] - reached)
        assert reached == vertices

    # For each proposed 3-polytope facet, the listed vertices, edges, and
    # ridges already satisfy Euler.  Every listed edge is in exactly two
    # listed ridges of that facet.  The elementary completion lemma in the
    # report then proves that no additional edges or ridges exist.
    local_data: dict[int, tuple[int, int, int]] = {}
    for i in range(g.n):
        facet_vertices = nb[i]
        facet_edges = [e for e in edge_masks if e & ~facet_vertices == 0]
        facet_ridges = [
            vertices for a0, a1, vertices in ridges if i in (a0, a1)
        ]
        incidence = Counter()
        for e in facet_edges:
            incidence[e] = sum(e & ~r == 0 for r in facet_ridges)
        assert set(incidence.values()) == {2}
        vef = (facet_vertices.bit_count(), len(facet_edges), len(facet_ridges))
        assert vef[0] - vef[1] + vef[2] == 2
        local_data[i] = vef

    # The 62 ridges connect all 23 proposed facets.  Once the local Euler
    # lemma shows that none has an unlisted ridge, connectedness of the dual
    # graph of a polytope shows that no unlisted facet can exist.
    facet_adjacency = [set() for _ in range(g.n)]
    for i, j, _ in ridges:
        facet_adjacency[i].add(j)
        facet_adjacency[j].add(i)
    reached = {0}
    queue: deque[int] = deque([0])
    while queue:
        i = queue.popleft()
        for j in facet_adjacency[i] - reached:
            reached.add(j)
            queue.append(j)
    assert len(reached) == g.n

    expected_local = {
        **{A[i]: (8, 12, 6) for i in range(5)},
        **{B[i]: (6, 9, 5) for i in range(5)},
        a: (10, 15, 7),
        **{C[i]: (5, 8, 5) for i in range(5)},
        **{D[i]: (4, 6, 4) for i in range(5)},
        b: (6, 10, 6),
        w: (11, 20, 11),
    }
    assert local_data == expected_local

    orbit_rows: list[tuple[str, int, int, int, int, str, int]] = []
    orbit_specs = (
        ("A_i=O2(O1(c_i))", A, A[2]),
        ("B_i=O2(S1(c_i))", B, A[0]),
        ("a=O2(w1)", [a], A[0]),
        ("C_i=S2(O1(c_i))", C, A[0]),
        ("D_i=S2(S1(c_i))", D, B[0]),
        ("b=S2(w1)", [b], a),
        ("w=w2", [w], A[0]),
    )
    for name, members, representative_witness in orbit_specs:
        representative = members[0]
        v, e, f = local_data[representative]
        # For moving families the representative witnesses are precisely the
        # i=0 instances specified above.
        actual_witness = dimension_witness[representative]
        assert actual_witness == representative_witness
        intersection = (nb[representative] & nb[actual_witness]).bit_count()
        orbit_rows.append((name, len(members), v, e, f,
                           g.labels[actual_witness], intersection))

    edge_facet_degrees = Counter(
        sum(e & ~nb[i] == 0 for i in range(g.n)) for e in edge_masks
    )
    return PolytopeCertificate(
        ridge_count=len(ridges),
        edge_count=len(edge_masks),
        ridge_size_histogram=tuple(sorted(Counter(
            r.bit_count() for r in ridge_masks
        ).items())),
        edge_facet_degree_histogram=tuple(sorted(edge_facet_degrees.items())),
        facet_orbit_table=tuple(orbit_rows),
    )


def main() -> None:
    graphs = tower()
    expected = ((5, 5), (11, 20), (23, 71), (47, 236))
    observed = tuple((g.n, len(g.edges)) for g in graphs)
    assert observed == expected
    print("Mycielski tower (vertices, edges):", observed)

    certs = critical_certificates(graphs)
    assert tuple(c.chromatic for c in certs) == (3, 4, 5, 6)
    assert all(len(c.deletion_colorings) == g.n for c, g in zip(certs, graphs))
    print("chromatic/vertex-critical certificate levels:",
          tuple(c.chromatic for c in certs))

    screen = inherited_screens(graphs[3])
    print("inherited exact screens:", screen)

    rows, cols, pattern = rank_five_minor(graphs[2])
    print("rank-five cross-slack minor rows:", rows)
    print("rank-five cross-slack minor cols:", cols)
    print("rank-five cross-slack support:")
    for line in pattern:
        print(" ", line)

    poly = polytope_certificate(graphs[2])
    print("polytope certificate:")
    print(" ridges:", poly.ridge_count,
          "size histogram", poly.ridge_size_histogram)
    print(" edges:", poly.edge_count,
          "facet-degree histogram", poly.edge_facet_degree_histogram)
    print(" facet orbit table:")
    print("  type | mult | V E F | proper-face witness | intersection vertices")
    for name, mult, v, e, f, witness, intersection in poly.facet_orbit_table:
        print(f"  {name} | {mult} | {v} {e} {f} | {witness} | {intersection}")

    print("EXACT CONCLUSION: T_3=M^3(C5) is not the exact diameter graph")
    print("of any set of distinct points in R^4.")
    print("Scope: the proof uses strict inequalities on every T_3 nonedge.")


if __name__ == "__main__":
    main()
