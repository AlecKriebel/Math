#!/usr/bin/env python3
"""Clean-room mixed-graph and admissible-rooting implementation.

This module intentionally uses only the Python standard library.  It does not
import any project graph, canonicalization, or phylogenetic code.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations
from typing import Dict, FrozenSet, Iterable, Iterator, List, Mapping, Sequence, Set, Tuple


Edge = Tuple[int, int]


def edge_key(u: int, v: int) -> Edge:
    if u == v:
        raise ValueError("loops are not permitted")
    return (u, v) if u < v else (v, u)


@dataclass(frozen=True)
class MixedGraph:
    """A simple labelled mixed graph.

    Leaves are vertices ``0,...,n-1`` and carry those fixed labels.  Internal
    vertices are ``n,...,n+m-1``.  ``arrows[e]`` is the frozenset of endpoints
    at which the edge carries a retained arrowhead.  Ordinary edges have the
    empty frozenset.  Two arrowheads are represented because they can arise
    when a non-tree-child root with two reticulation children is suppressed;
    such a graph will fail the ``S_TC`` filter.
    """

    n: int
    m: int
    reticulations: FrozenSet[int]
    edges: FrozenSet[Edge]
    arrows: Tuple[Tuple[Edge, FrozenSet[int]], ...]

    @staticmethod
    def make(
        n: int,
        m: int,
        reticulations: Iterable[int],
        edges: Iterable[Tuple[int, int]],
        arrows: Mapping[Tuple[int, int], Iterable[int]],
    ) -> "MixedGraph":
        es = frozenset(edge_key(u, v) for u, v in edges)
        amap = []
        for e in sorted(es):
            heads = frozenset(arrows.get(e, arrows.get((e[1], e[0]), ())))
            if not heads.issubset(e):
                raise ValueError((e, heads))
            amap.append((e, heads))
        return MixedGraph(n, m, frozenset(reticulations), es, tuple(amap))

    @property
    def vertices(self) -> range:
        return range(self.n + self.m)

    @property
    def internals(self) -> range:
        return range(self.n, self.n + self.m)

    @property
    def leaves(self) -> range:
        return range(self.n)

    def arrow_map(self) -> Dict[Edge, FrozenSet[int]]:
        return dict(self.arrows)

    def neighbors(self) -> Dict[int, Set[int]]:
        out = {v: set() for v in self.vertices}
        for u, v in self.edges:
            out[u].add(v)
            out[v].add(u)
        return out

    def validate_binary(self) -> bool:
        if len(self.edges) != len(set(self.edges)):
            return False
        nbr = self.neighbors()
        if any(len(nbr[v]) != 1 for v in self.leaves):
            return False
        if any(len(nbr[v]) != 3 for v in self.internals):
            return False
        if not self.reticulations.issubset(set(self.internals)):
            return False
        amap = self.arrow_map()
        head_count = {v: 0 for v in self.internals}
        for e, heads in amap.items():
            if e not in self.edges or not heads.issubset(self.reticulations):
                return False
            for h in heads:
                head_count[h] += 1
        if any(head_count[v] != 2 for v in self.reticulations):
            return False
        if any(head_count[v] != 0 for v in set(self.internals) - set(self.reticulations)):
            return False
        return _connected_undirected(self.vertices, self.edges)


@dataclass(frozen=True)
class Rooting:
    root: int
    root_edge: Edge
    arcs: Tuple[Tuple[int, int], ...]
    tree_child: bool


def _connected_undirected(vertices: Iterable[int], edges: Iterable[Edge]) -> bool:
    verts = tuple(vertices)
    if not verts:
        return True
    adj = {v: [] for v in verts}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = {verts[0]}
    stack = [verts[0]]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == len(verts)


def _acyclic_and_reachable(root: int, vertices: Sequence[int], arcs: Sequence[Tuple[int, int]]) -> bool:
    out = {v: [] for v in vertices}
    indeg = {v: 0 for v in vertices}
    for u, v in arcs:
        out[u].append(v)
        indeg[v] += 1
    queue = [v for v in vertices if indeg[v] == 0]
    order = []
    while queue:
        u = queue.pop()
        order.append(u)
        for v in out[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if len(order) != len(vertices):
        return False
    seen = {root}
    stack = [root]
    while stack:
        u = stack.pop()
        for v in out[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == len(vertices)


def _is_lsa(root: int, leaves: Sequence[int], vertices: Sequence[int], arcs: Sequence[Tuple[int, int]]) -> bool:
    out = {v: [] for v in vertices}
    for u, v in arcs:
        out[u].append(v)
    for blocked in vertices:
        if blocked == root:
            continue
        reachable = set()
        if root != blocked:
            reachable.add(root)
        stack = list(reachable)
        while stack:
            u = stack.pop()
            for v in out[u]:
                if v != blocked and v not in reachable:
                    reachable.add(v)
                    stack.append(v)
        # ``blocked`` is a stable ancestor of the complete taxon set exactly
        # when every root-to-leaf path uses it, i.e. no leaf remains reachable.
        if all(leaf not in reachable for leaf in leaves):
            return False
    return True


def _tree_child(root: int, graph: MixedGraph, arcs: Sequence[Tuple[int, int]]) -> bool:
    out = {v: [] for v in list(graph.vertices) + [root]}
    for u, v in arcs:
        out[u].append(v)
    for u in list(graph.internals) + [root]:
        if not any(v not in graph.reticulations for v in out[u]):
            return False
    return True


def _orient_flexible_edges(
    flexible: Sequence[Edge],
    residual_indegree: Mapping[int, int],
) -> Iterator[Tuple[Tuple[int, int], ...]]:
    """Orient edges to meet exact residual indegrees, with forced propagation."""

    initial_edges = tuple(sorted(flexible))
    initial_residual = dict(residual_indegree)

    def recurse(
        remaining: Tuple[Edge, ...],
        residual: Dict[int, int],
        chosen: Tuple[Tuple[int, int], ...],
    ) -> Iterator[Tuple[Tuple[int, int], ...]]:
        incidence: Dict[int, List[Edge]] = {}
        for e in remaining:
            u, v = e
            incidence.setdefault(u, []).append(e)
            incidence.setdefault(v, []).append(e)
        for v, need in residual.items():
            available = len(incidence.get(v, ()))
            if need < 0 or need > available:
                return
        if not remaining:
            if all(need == 0 for need in residual.values()):
                yield chosen
            return

        forced = None
        for v in sorted(incidence):
            need = residual.get(v, 0)
            if need == 0 or need == len(incidence[v]):
                e = min(incidence[v])
                u, w = e
                # need==0 forces the edge out of v; need==available forces it
                # into v.  ``arc`` is always tail->head.
                if need == 0:
                    arc = (v, w if u == v else u)
                else:
                    arc = (w if u == v else u, v)
                forced = (e, arc)
                break

        branches = []
        if forced is not None:
            branches.append(forced)
        else:
            e = remaining[0]
            u, v = e
            branches.extend(((e, (u, v)), (e, (v, u))))

        for e, arc in branches:
            tail, head = arc
            new_residual = dict(residual)
            new_residual[head] = new_residual.get(head, 0) - 1
            new_remaining = tuple(x for x in remaining if x != e)
            yield from recurse(new_remaining, new_residual, chosen + (arc,))

    yield from recurse(initial_edges, initial_residual, ())


def enumerate_admissible_rootings(graph: MixedGraph) -> Tuple[Rooting, ...]:
    """Enumerate every literal ``sd_0`` rooting of ``graph`` exactly."""

    if not graph.validate_binary():
        return ()
    amap = graph.arrow_map()
    root = graph.n + graph.m
    vertices = tuple(graph.vertices) + (root,)
    rootings: List[Rooting] = []

    for root_edge in sorted(graph.edges):
        u0, v0 = root_edge
        heads0 = amap[root_edge]
        # A root arc entering a reticulation leaves an arrowhead after root
        # suppression.  Rooting an unmarked outgoing reticulation incidence
        # therefore cannot recover the same mixed edge.
        if any(v in graph.reticulations and v not in heads0 for v in root_edge):
            continue

        fixed: List[Tuple[int, int]] = [(root, u0), (root, v0)]
        flexible: List[Edge] = []
        impossible = False
        for e in sorted(graph.edges):
            if e == root_edge:
                continue
            u, v = e
            heads = amap[e]
            if len(heads) == 2:
                impossible = True
                break
            if len(heads) == 1:
                h = next(iter(heads))
                fixed.append((v if h == u else u, h))
            elif u in graph.reticulations and v in graph.reticulations:
                impossible = True
                break
            elif u in graph.reticulations:
                fixed.append((u, v))
            elif v in graph.reticulations:
                fixed.append((v, u))
            else:
                flexible.append(e)
        if impossible:
            continue

        fixed_indegree = {v: 0 for v in vertices}
        for _, v in fixed:
            fixed_indegree[v] += 1
        target_indegree = {
            v: (0 if v == root else 2 if v in graph.reticulations else 1)
            for v in vertices
        }
        residual = {v: target_indegree[v] - fixed_indegree[v] for v in vertices}

        for oriented in _orient_flexible_edges(flexible, residual):
            arcs = list(fixed) + list(oriented)

            indeg = {v: 0 for v in vertices}
            outdeg = {v: 0 for v in vertices}
            for u, v in arcs:
                outdeg[u] += 1
                indeg[v] += 1
            if (indeg[root], outdeg[root]) != (0, 2):
                continue
            if any((indeg[v], outdeg[v]) != (1, 0) for v in graph.leaves):
                continue
            if any(
                (indeg[v], outdeg[v]) != ((2, 1) if v in graph.reticulations else (1, 2))
                for v in graph.internals
            ):
                continue
            if not _acyclic_and_reachable(root, vertices, arcs):
                continue
            if not _is_lsa(root, tuple(graph.leaves), vertices, arcs):
                continue
            arcs_tuple = tuple(sorted(arcs))
            rootings.append(Rooting(root, root_edge, arcs_tuple, _tree_child(root, graph, arcs_tuple)))
    # There can be no duplicate arc set from two different root sites, but use
    # an exact key defensively.
    unique = {(r.root_edge, r.arcs): r for r in rootings}
    return tuple(unique[k] for k in sorted(unique))


def class_membership(graph: MixedGraph) -> Tuple[str, Tuple[Rooting, ...]]:
    roots = enumerate_admissible_rootings(graph)
    if not roots:
        return "NO_ADMISSIBLE_ROOTING", roots
    tc = sum(r.tree_child for r in roots)
    if tc == len(roots):
        return "S_TC", roots
    if tc:
        return "W_TC_NOT_S_TC", roots
    return "NOT_W_TC", roots


def _mixed_encoding_under_order(graph: MixedGraph, order: Sequence[int]) -> Tuple[int, ...]:
    """Encode after assigning ``order[j]`` to canonical internal position j."""

    if len(order) != graph.m:
        raise ValueError("bad order")
    old_to_new = {old: graph.n + j for j, old in enumerate(order)}
    old_to_new.update({leaf: leaf for leaf in graph.leaves})
    amap = graph.arrow_map()
    states: Dict[Edge, int] = {}
    for e in graph.edges:
        u, v = e
        nu, nv = old_to_new[u], old_to_new[v]
        ne = edge_key(nu, nv)
        heads = {old_to_new[h] for h in amap[e]}
        state = 1  # edge present
        if ne[0] in heads:
            state |= 2
        if ne[1] in heads:
            state |= 4
        states[ne] = state
    code: List[int] = [graph.n, graph.m, len(graph.reticulations)]
    total = graph.n + graph.m
    for u in range(total):
        for v in range(u + 1, total):
            code.append(states.get((u, v), 0))
    return tuple(code)


def canonical_mixed_code(graph: MixedGraph) -> Tuple[int, ...]:
    """Exact labelled mixed-graph canonical form by role-preserving search."""

    retics = sorted(graph.reticulations)
    trees = sorted(set(graph.internals) - set(graph.reticulations))
    best = None
    for pr in permutations(retics):
        for pt in permutations(trees):
            code = _mixed_encoding_under_order(graph, pr + pt)
            if best is None or code < best:
                best = code
    assert best is not None
    return best


def isomorphic(g1: MixedGraph, g2: MixedGraph) -> bool:
    return canonical_mixed_code(g1) == canonical_mixed_code(g2)


def triangles(graph: MixedGraph) -> Tuple[Tuple[int, int, int], ...]:
    nbr = graph.neighbors()
    out = []
    for a, b, c in combinations(graph.vertices, 3):
        if b in nbr[a] and c in nbr[a] and c in nbr[b]:
            out.append((a, b, c))
    return tuple(out)


def ordinary_T_neighbors(graph: MixedGraph) -> Tuple[MixedGraph, ...]:
    """Return all valid one-step ordinary triangle redirections."""

    amap0 = graph.arrow_map()
    out: Dict[Tuple[int, ...], MixedGraph] = {}
    for tri in triangles(graph):
        tri_set = set(tri)
        tri_edges = {edge_key(u, v) for u, v in combinations(tri, 2)}
        for target in tri:
            amap = {e: set(hs) for e, hs in amap0.items()}
            # Remove all triangle-internal arrowheads at triangle vertices;
            # every arrowhead outside the triangle remains literally fixed.
            for e in tri_edges:
                amap[e] -= tri_set
            for other in tri_set - {target}:
                amap[edge_key(target, other)].add(target)
            retics = set()
            valid = True
            for v in graph.internals:
                count = sum(v in amap[e] for e in graph.edges)
                if count == 2:
                    retics.add(v)
                elif count != 0:
                    valid = False
                    break
            if not valid or len(retics) != len(graph.reticulations):
                continue
            candidate = MixedGraph.make(graph.n, graph.m, retics, graph.edges, amap)
            if not candidate.validate_binary():
                continue
            code = canonical_mixed_code(candidate)
            if code != canonical_mixed_code(graph):
                out[code] = candidate
    return tuple(out[k] for k in sorted(out))


def T_class_code(graph: MixedGraph) -> Tuple[int, ...]:
    """Minimum isomorphism code in the finite ordinary-T closure."""

    start = canonical_mixed_code(graph)
    seen = {start}
    queue = [graph]
    while queue:
        current = queue.pop()
        for nxt in ordinary_T_neighbors(current):
            code = canonical_mixed_code(nxt)
            if code not in seen:
                seen.add(code)
                queue.append(nxt)
    return min(seen)


def biconnected_edge_blocks(graph: MixedGraph) -> Tuple[FrozenSet[Edge], ...]:
    """Tarjan edge-block decomposition of the underlying simple graph."""

    nbr = graph.neighbors()
    disc: Dict[int, int] = {}
    low: Dict[int, int] = {}
    parent: Dict[int, int] = {}
    stack: List[Edge] = []
    blocks: List[FrozenSet[Edge]] = []
    time = 0

    def dfs(u: int) -> None:
        nonlocal time
        time += 1
        disc[u] = low[u] = time
        for v in sorted(nbr[u]):
            e = edge_key(u, v)
            if v not in disc:
                parent[v] = u
                stack.append(e)
                dfs(v)
                low[u] = min(low[u], low[v])
                if low[v] >= disc[u]:
                    block = set()
                    while stack:
                        f = stack.pop()
                        block.add(f)
                        if f == e:
                            break
                    blocks.append(frozenset(block))
            elif parent.get(u) != v and disc[v] < disc[u]:
                stack.append(e)
                low[u] = min(low[u], disc[v])

    for v in graph.vertices:
        if v not in disc:
            dfs(v)
            if stack:
                blocks.append(frozenset(stack))
                stack.clear()
    return tuple(blocks)


def level(graph: MixedGraph) -> int:
    answer = 0
    for block in biconnected_edge_blocks(graph):
        verts = {x for e in block for x in e}
        answer = max(answer, len(verts & set(graph.reticulations)))
    return answer


def triangle_counts_by_blob(graph: MixedGraph) -> Tuple[int, ...]:
    tris = [set(t) for t in triangles(graph)]
    counts = []
    for block in biconnected_edge_blocks(graph):
        verts = {x for e in block for x in e}
        counts.append(sum(t.issubset(verts) for t in tris))
    return tuple(sorted(counts, reverse=True))


def graph_to_record(graph: MixedGraph, roots: Sequence[Rooting] | None = None) -> dict:
    if roots is None:
        roots = enumerate_admissible_rootings(graph)
    amap = graph.arrow_map()
    return {
        "n": graph.n,
        "m": graph.m,
        "reticulations": sorted(graph.reticulations),
        "edges": [
            {"u": u, "v": v, "arrowheads": sorted(amap[(u, v)])}
            for u, v in sorted(graph.edges)
        ],
        "canonical_code": list(canonical_mixed_code(graph)),
        "T_class_code": list(T_class_code(graph)),
        "level": level(graph),
        "triangles": [list(t) for t in triangles(graph)],
        "triangle_counts_by_blob": list(triangle_counts_by_blob(graph)),
        "rootings": [
            {
                "root_edge": list(r.root_edge),
                "arcs": [list(a) for a in r.arcs],
                "tree_child": r.tree_child,
            }
            for r in roots
        ],
    }
