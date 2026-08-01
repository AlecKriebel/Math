#!/usr/bin/env python3
"""Exact/computational diagnostics for Route B (graph-first search).

Discovery in this file is deliberately self-contained.  The exact screens use
only the Python standard library.  The optional numerical screen needs NumPy
and SciPy, and is *not* a proof: it only minimizes the equal-edge residual for
a rank-four coordinate factor.

The principal exact screens are:

* chromatic backtracking for small derived graphs;
* the K_6-e (regular 4-simplex completion) obstruction;
* the C4 obstruction after joining a universal K_2; and
* exact spectral algebra for an S_8-invariant Gram matrix of KG(8,2).
"""

from __future__ import annotations

import argparse
import itertools
import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence


Edge = tuple[int, int]


def _edge(i: int, j: int) -> Edge:
    if i == j:
        raise ValueError("loops are not allowed")
    return (i, j) if i < j else (j, i)


@dataclass(frozen=True)
class Graph:
    n: int
    edges: frozenset[Edge]
    labels: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.labels:
            object.__setattr__(self, "labels", tuple(map(str, range(self.n))))
        if len(self.labels) != self.n:
            raise ValueError("wrong number of labels")
        for i, j in self.edges:
            if not (0 <= i < j < self.n):
                raise ValueError((i, j))

    @staticmethod
    def make(n: int, edges: Iterable[Edge], labels: Sequence[str] = ()) -> "Graph":
        return Graph(n, frozenset(_edge(i, j) for i, j in edges), tuple(labels))

    def adjacent(self, i: int, j: int) -> bool:
        return i != j and _edge(i, j) in self.edges

    def neighbors(self, i: int) -> set[int]:
        return {j for j in range(self.n) if self.adjacent(i, j)}

    def degrees(self) -> tuple[int, ...]:
        return tuple(len(self.neighbors(i)) for i in range(self.n))


def complete(n: int, prefix: str = "q") -> Graph:
    return Graph.make(n, itertools.combinations(range(n), 2),
                      [f"{prefix}{i}" for i in range(n)])


def cycle(n: int, prefix: str = "v") -> Graph:
    if n < 3:
        raise ValueError("a cycle needs at least three vertices")
    return Graph.make(n, ((_edge(i, (i + 1) % n)) for i in range(n)),
                      [f"{prefix}{i}" for i in range(n)])


def join(g: Graph, h: Graph) -> Graph:
    edges = set(g.edges)
    edges.update((i + g.n, j + g.n) for i, j in h.edges)
    edges.update((i, g.n + j) for i in range(g.n) for j in range(h.n))
    return Graph.make(g.n + h.n, edges, g.labels + h.labels)


def mycielski(g: Graph) -> Graph:
    """The elementary shadow construction M(G), with chi raised by one."""
    n = g.n
    edges = set(g.edges)
    for i, j in g.edges:
        edges.add(_edge(i, n + j))
        edges.add(_edge(j, n + i))
    w = 2 * n
    edges.update((n + i, w) for i in range(n))
    labels = tuple(f"v:{x}" for x in g.labels)
    labels += tuple(f"u:{x}" for x in g.labels) + ("w",)
    return Graph.make(2 * n + 1, edges, labels)


def hajos_sum_k6() -> Graph:
    """Two copies of K6-e sharing x, with an edge between missing mates.

    Each K6-e forces its two nonadjacent vertices to receive the same color in
    any five-coloring, while the added edge demands different colors.
    """
    block1 = list(range(0, 6))       # x=0, y1=1, z1..z4=2..5
    block2 = [0, 6, 7, 8, 9, 10]    # x=0, y2=6, z'1..z'4=7..10
    edges: set[Edge] = set()
    for block, missing in ((block1, _edge(0, 1)),
                           (block2, _edge(0, 6))):
        for i, j in itertools.combinations(block, 2):
            if _edge(i, j) != missing:
                edges.add(_edge(i, j))
    edges.add((1, 6))
    labels = ("x", "y1", "a1", "a2", "a3", "a4",
              "y2", "b1", "b2", "b3", "b4")
    return Graph.make(11, edges, labels)


def kg_8_2() -> Graph:
    """Vertices are two-subsets of {0,...,7}; disjointness is adjacency."""
    pairs = list(itertools.combinations(range(8), 2))
    edges = []
    for i, a in enumerate(pairs):
        for j in range(i + 1, len(pairs)):
            if set(a).isdisjoint(pairs[j]):
                edges.append((i, j))
    return Graph.make(len(pairs), edges, [f"{i}{j}" for i, j in pairs])


def kg82_matching_blocks() -> dict[str, object]:
    """Structural certificate for the 4+4-label obstruction in KG(8,2).

    Each block has six vertices and induces a matching of three diameter
    edges.  Every one of the 6*6 cross pairs is a diameter edge.
    """
    g = kg_8_2()
    pairs = list(itertools.combinations(range(8), 2))
    left = tuple(i for i, pair in enumerate(pairs) if set(pair) <= set(range(4)))
    right = tuple(i for i, pair in enumerate(pairs) if set(pair) <= set(range(4, 8)))

    def internal_edges(block: tuple[int, ...]) -> tuple[Edge, ...]:
        return tuple((i, j) for i, j in itertools.combinations(block, 2)
                     if g.adjacent(i, j))

    le = internal_edges(left)
    re = internal_edges(right)
    cross = tuple((i, j) for i in left for j in right if g.adjacent(i, j))
    assert len(left) == len(right) == 6
    assert len(le) == len(re) == 3
    assert {x for edge in le for x in edge} == set(left)
    assert {x for edge in re for x in edge} == set(right)
    assert len(cross) == 36
    return {
        "left_labels": tuple(g.labels[i] for i in left),
        "right_labels": tuple(g.labels[i] for i in right),
        "left_matching": tuple((g.labels[i], g.labels[j]) for i, j in le),
        "right_matching": tuple((g.labels[i], g.labels[j]) for i, j in re),
        "cross_edge_count": len(cross),
    }


def c5_circle_step_candidates() -> tuple[Fraction, ...]:
    """Exact possible delta/pi values from closing five signed equal chords.

    A chord with minor central angle delta<pi changes angular coordinate by
    either +delta or -delta.  Five such changes close only for the ratios
    returned here.  Geometry then rejects 2/3 (only three angular positions)
    and 2/5 (the two-step chord is longer), leaving 4/5.
    """
    ratios: set[Fraction] = set()
    for signs in itertools.product((-1, 1), repeat=5):
        total = abs(sum(signs))
        if total == 0:
            continue
        for winding in range(1, total):
            ratio = Fraction(2 * winding, total)
            if 0 < ratio < 1:
                ratios.add(ratio)
    return tuple(sorted(ratios))


def join_block_certificate(g: Graph, h: Graph) -> dict[str, int | bool]:
    """Verify the complete cross block used by the two-edge join lemma."""
    joined = join(g, h)
    cross = sum(joined.adjacent(i, g.n + j)
                for i in range(g.n) for j in range(h.n))
    return {
        "left_edges": len(g.edges),
        "right_edges": len(h.edges),
        "cross_edges": cross,
        "expected_cross_edges": g.n * h.n,
        "two_edge_obstruction_applies": (
            len(g.edges) >= 2 and len(h.edges) >= 2 and cross == g.n * h.n
        ),
    }


def clique_number(g: Graph) -> int:
    """Exact Bron--Kerbosch maximum clique, using integer bitsets."""
    nb = [sum(1 << j for j in g.neighbors(i)) for i in range(g.n)]
    best = 0

    def expand(size: int, candidates: int) -> None:
        nonlocal best
        if size + candidates.bit_count() <= best:
            return
        while candidates:
            vbit = candidates & -candidates
            candidates ^= vbit
            v = vbit.bit_length() - 1
            expand(size + 1, candidates & nb[v])
            if size + candidates.bit_count() <= best:
                break
        best = max(best, size)

    expand(0, (1 << g.n) - 1)
    return best


def find_k6_or_k6_minus_edge(g: Graph) -> tuple[tuple[int, ...], list[Edge]] | None:
    """Find six vertices spanning at least 14 of their 15 possible edges."""
    for six in itertools.combinations(range(g.n), 6):
        missing = [(i, j) for i, j in itertools.combinations(six, 2)
                   if not g.adjacent(i, j)]
        if len(missing) <= 1:
            return six, missing
    return None


def find_two_edge_join_block(
        g: Graph,
) -> tuple[tuple[Edge, Edge], tuple[Edge, Edge], tuple[int, ...], tuple[int, ...]] | None:
    """Find disjoint blocks, each with two edges, with all cross edges present."""
    witnesses: dict[frozenset[int], tuple[Edge, Edge]] = {}
    edges = sorted(g.edges)
    for e1, e2 in itertools.combinations(edges, 2):
        block = frozenset((*e1, *e2))
        witnesses.setdefault(block, (e1, e2))
    blocks = sorted(witnesses, key=lambda x: (len(x), tuple(sorted(x))))
    for pos, left in enumerate(blocks):
        for right in blocks[pos + 1:]:
            if left & right:
                continue
            if all(g.adjacent(i, j) for i in left for j in right):
                return (witnesses[left], witnesses[right],
                        tuple(sorted(left)), tuple(sorted(right)))
    return None


def induced_c4s(g: Graph) -> list[tuple[int, int, int, int]]:
    """List each induced C4 once, in a canonical cyclic order."""
    found: set[tuple[int, int, int, int]] = set()
    for four in itertools.combinations(range(g.n), 4):
        es = [_edge(i, j) for i, j in itertools.combinations(four, 2)
              if g.adjacent(i, j)]
        if len(es) != 4:
            continue
        deg = {i: 0 for i in four}
        for i, j in es:
            deg[i] += 1
            deg[j] += 1
        if set(deg.values()) != {2}:
            continue
        start = min(four)
        nbs = sorted(j for j in four if g.adjacent(start, j))
        second = nbs[0]
        third = next(j for j in four
                     if j not in (start, second) and g.adjacent(second, j))
        fourth = next(j for j in four if j not in (start, second, third))
        cyc = (start, second, third, fourth)
        rev = (start, fourth, third, second)
        found.add(min(cyc, rev))
    return sorted(found)


def c4_subgraphs(g: Graph) -> list[tuple[int, int, int, int]]:
    """List all (not necessarily induced) four-cycles canonically."""
    found: set[tuple[int, int, int, int]] = set()
    for four in itertools.combinations(range(g.n), 4):
        a = min(four)
        others = tuple(x for x in four if x != a)
        # A cyclic order beginning at the least vertex is determined up to
        # reversal by a permutation of the other three vertices.
        for perm in itertools.permutations(others):
            cyc = (a,) + perm
            rev = (a, perm[2], perm[1], perm[0])
            if cyc > rev:
                continue
            if all(g.adjacent(cyc[i], cyc[(i + 1) % 4]) for i in range(4)):
                found.add(cyc)
    return sorted(found)


def universal_clique_size(g: Graph) -> int:
    universal = [i for i, d in enumerate(g.degrees()) if d == g.n - 1]
    # Universal vertices are automatically pairwise adjacent.
    return len(universal)


def k_color(g: Graph, k: int) -> tuple[int, ...] | None:
    """Exact DSATUR-style k-coloring search, adequate for the small screens."""
    n = g.n
    nbs = [g.neighbors(i) for i in range(n)]
    colors = [-1] * n
    color_masks = [0] * n

    def search(colored: int, used: int) -> bool:
        if colored == n:
            return True
        v = max((i for i in range(n) if colors[i] < 0),
                key=lambda i: (color_masks[i].bit_count(), len(nbs[i])))
        forbidden = color_masks[v]
        # Color symmetry: at most the first new color need be tried.
        limit = min(k, used + 1)
        for c in range(limit):
            if forbidden >> c & 1:
                continue
            colors[v] = c
            changed: list[tuple[int, int]] = []
            ok = True
            for u in nbs[v]:
                if colors[u] == c:
                    ok = False
                    break
                if colors[u] < 0 and not (color_masks[u] >> c & 1):
                    changed.append((u, color_masks[u]))
                    color_masks[u] |= 1 << c
                    if color_masks[u].bit_count() == k:
                        ok = False
                        break
            if ok and search(colored + 1, max(used, c + 1)):
                return True
            for u, old in reversed(changed):
                color_masks[u] = old
            colors[v] = -1
        return False

    return tuple(colors) if search(0, 0) else None


def chromatic_small(g: Graph, upper: int = 6) -> int | None:
    lo = clique_number(g)
    for k in range(max(1, lo), upper + 1):
        if k_color(g, k) is not None:
            return k
    return None


def c4_gram_determinant(q: Fraction, t: Fraction,
                        c: Fraction = Fraction(1, 3)) -> Fraction:
    """Determinant for a unit-vector C4 (diagonals may also be edges).

    Cycle entries equal c, while q and t are its two diagonal entries.
    The factored determinant is
        (q-1)(t-1)((q+1)(t+1)-4c^2).
    """
    return (q - 1) * (t - 1) * ((q + 1) * (t + 1) - 4 * c * c)


def join_spherical_reduction(t: int) -> dict[str, Fraction | int]:
    """Parameters left after a universal K_t in an R^4 diameter graph.

    The K_t is a regular (t-1)-simplex of side one.  Every remaining vertex
    of the join lies on a sphere in the perpendicular (5-t)-dimensional
    linear space.  After normalizing that sphere to unit radius, diameter
    edges have inner product 1/(t+1).
    """
    if not 1 <= t <= 5:
        raise ValueError("the reduction is for 1 <= t <= 5")
    return {
        "ambient_linear_dimension": 5 - t,
        "radius_squared": Fraction(t + 1, 2 * t),
        "edge_inner_product": Fraction(1, t + 1),
    }


def kg82_invariant_spectrum(gap: Fraction) -> dict[str, object]:
    """Exact spectrum of every S8-invariant centered KG(8,2) Gram matrix.

    Diameter squared is normalized to one.  If c is the Gram entry on
    disjoint pairs and b on intersecting pairs, ``gap = b-c``.  Strictly
    shorter nonedges require gap>0.  Centering and a-c=1/2 give the entries
    and the two nonconstant eigenvalues below.
    """
    c = -(Fraction(1, 2) + 12 * gap) / 28
    a = c + Fraction(1, 2)
    b = c + gap
    return {
        "diag_a": a,
        "intersect_b": b,
        "disjoint_c": c,
        "lambda_standard_mult_7": Fraction(1, 2) + 4 * gap,
        "lambda_other_mult_20": Fraction(1, 2) - 2 * gap,
        "lambda_constant_mult_1": Fraction(0),
    }


def summarize_exact() -> None:
    graphs = {
        "K3_join_C5": join(complete(3, "a"), cycle(5)),
        "C5_join_C5": join(cycle(5, "a"), cycle(5, "b")),
        "Mycielski_K5": mycielski(complete(5)),
        "Hajos_K6_sum": hajos_sum_k6(),
        "K2_join_Mycielski_C5": join(complete(2, "a"), mycielski(cycle(5))),
        "Mycielski_of_K2_join_C5": mycielski(
            join(complete(2, "a"), cycle(5))
        ),
        "Mycielski_squared_K4": mycielski(mycielski(complete(4))),
        "KG_8_2": kg_8_2(),
    }
    for name, g in graphs.items():
        obs = find_k6_or_k6_minus_edge(g)
        induced_c4_count = len(induced_c4s(g))
        cycles4 = c4_subgraphs(g)
        c4_count = len(cycles4)
        universal = [i for i, d in enumerate(g.degrees()) if d == g.n - 1]
        residual = set(range(g.n)) - set(universal[:2])
        residual_c4_count = sum(set(cyc) <= residual for cyc in cycles4)
        print(f"{name}: n={g.n} m={len(g.edges)} omega={clique_number(g)} "
              f"universal={universal_clique_size(g)} C4={c4_count} "
              f"induced_C4={induced_c4_count} "
              f"K2_remainder_C4={residual_c4_count if len(universal) >= 2 else 0}")
        if g.n <= 19:
            print(f"  exact_chromatic={chromatic_small(g, 6)}")
        if obs:
            six, missing = obs
            pretty = tuple(g.labels[i] for i in six)
            print(f"  K6/K6-e obstruction on {pretty}; missing={missing}")
        if len(universal) >= 2 and residual_c4_count:
            print("  K2-join C4 rank obstruction applies")
        if name in {"Mycielski_of_K2_join_C5", "Mycielski_squared_K4"}:
            block = find_two_edge_join_block(g)
            if block:
                left_edges, right_edges, left, right = block
                print("  two-edge join-block obstruction:")
                print("   left_edges=", tuple((g.labels[i], g.labels[j])
                                               for i, j in left_edges))
                print("   right_edges=", tuple((g.labels[i], g.labels[j])
                                                for i, j in right_edges))
                print("   blocks=", tuple(g.labels[i] for i in left),
                      tuple(g.labels[i] for i in right))

    print("KG(8,2) conceptual chromatic certificate: chi=6")
    print("  lower: every pairwise-intersecting edge family in K8 is a star "
          "or is contained in a triangle; five such families cannot cover E(K8)")
    print("  upper: five successive stars on vertices 0..4, then the triangle 5,6,7")
    print(f"KG(8,2) orthogonal matching-block certificate: {kg82_matching_blocks()}")
    print("C5 join C5 two-edge block certificate: "
          f"{join_block_certificate(cycle(5, 'a'), cycle(5, 'b'))}")
    print(f"C5 circle closure delta/pi candidates: {c5_circle_step_candidates()}")
    print("  2/3 repeats after three positions; 2/5 has a longer two-step chord; "
          "4/5 survives")
    print("  surviving radius^2 x is the root 1/4<x<1/3 of 5*x^2-5*x+1=0")
    for gap in (Fraction(1, 100), Fraction(1, 4)):
        print(f"KG(8,2) invariant spectrum at gap={gap}: "
              f"{kg82_invariant_spectrum(gap)}")
    for t in (1, 2, 3):
        print(f"universal K{t} reduction: {join_spherical_reduction(t)}")
    det_sample = c4_gram_determinant(Fraction(1, 2), Fraction(2, 3))
    print(f"C4 determinant sample (q=1/2,t=2/3,c=1/3): {det_sample}>0")


def numerical_edge_fit(name: str, restarts: int, seed: int) -> None:
    """Heuristic rank-four equal-edge fit; a nonzero residual proves nothing."""
    try:
        import numpy as np
        from scipy.optimize import least_squares
    except ImportError as exc:  # pragma: no cover - environment diagnostic
        raise SystemExit("numerical mode needs NumPy and SciPy") from exc

    choices = {
        "kg82": kg_8_2(),
        "k2_mycielski_c5": join(complete(2), mycielski(cycle(5))),
    }
    g = choices[name]
    edges = sorted(g.edges)
    nonedges = [(i, j) for i in range(g.n) for j in range(i + 1, g.n)
                if (i, j) not in g.edges]
    rng = np.random.default_rng(seed)

    def unpack(x):
        return np.vstack((np.zeros((1, 4)), x.reshape(g.n - 1, 4)))

    def residual(x):
        p = unpack(x)
        return np.asarray([np.dot(p[i] - p[j], p[i] - p[j]) - 1
                           for i, j in edges])

    best = None
    for trial in range(restarts):
        p = rng.normal(size=(g.n, 4))
        p -= p[0]
        mean_edge = np.mean([np.dot(p[i] - p[j], p[i] - p[j])
                             for i, j in edges])
        p /= math.sqrt(mean_edge)
        fit = least_squares(residual, p[1:].ravel(), method="trf",
                            max_nfev=1200, ftol=1e-12, xtol=1e-12,
                            gtol=1e-12)
        edge_res = residual(fit.x)
        score = float(np.linalg.norm(edge_res))
        if best is None or score < best[0]:
            q = unpack(fit.x)
            nonedge_d2 = np.asarray([
                np.dot(q[i] - q[j], q[i] - q[j]) for i, j in nonedges
            ])
            best = (score, float(np.max(np.abs(edge_res))),
                    float(np.min(nonedge_d2)), float(np.max(nonedge_d2)),
                    trial, fit.nfev)
    assert best is not None
    print(f"heuristic {name} restarts={restarts} seed={seed}")
    print("  edge_L2 edge_Linf nonedge_min_d2 nonedge_max_d2 trial nfev")
    print(" ", *best)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact", action="store_true",
                        help="run the deterministic exact screens")
    parser.add_argument("--numeric", choices=("kg82", "k2_mycielski_c5"))
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260801)
    args = parser.parse_args()
    if args.exact or args.numeric is None:
        summarize_exact()
    if args.numeric:
        numerical_edge_fit(args.numeric, args.restarts, args.seed)


if __name__ == "__main__":
    main()
