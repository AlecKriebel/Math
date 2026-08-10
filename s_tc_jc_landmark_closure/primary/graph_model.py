"""Primary rooted/mixed graph and JC displayed-tree primitives.

Only the Python standard library is used.  The independent atlas has its own
representations and canonicalizer.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from itertools import permutations, product
from typing import Iterable, Iterator, Mapping, Sequence


@dataclass(frozen=True, order=True)
class MixedEdge:
    u: int
    v: int
    head_u: int = 0
    head_v: int = 0

    @staticmethod
    def make(u: int, v: int, heads: Iterable[int] = ()) -> "MixedEdge":
        head_set = set(heads)
        if u < v:
            return MixedEdge(u, v, int(u in head_set), int(v in head_set))
        return MixedEdge(v, u, int(v in head_set), int(u in head_set))

    def endpoints(self) -> tuple[int, int]:
        return self.u, self.v

    def heads(self) -> frozenset[int]:
        return frozenset(v for v, bit in ((self.u, self.head_u), (self.v, self.head_v)) if bit)

    def other(self, vertex: int) -> int:
        if vertex == self.u:
            return self.v
        if vertex == self.v:
            return self.u
        raise KeyError(vertex)

    def head_at(self, vertex: int) -> int:
        if vertex == self.u:
            return self.head_u
        if vertex == self.v:
            return self.head_v
        raise KeyError(vertex)


@dataclass(frozen=True)
class MixedGraph:
    labels: tuple[tuple[int, str], ...]
    edges: tuple[MixedEdge, ...]

    @property
    def label_map(self) -> dict[int, str]:
        return dict(self.labels)

    @property
    def vertices(self) -> tuple[int, ...]:
        values = set(dict(self.labels))
        for edge in self.edges:
            values.update(edge.endpoints())
        return tuple(sorted(values))

    def incidence(self) -> dict[int, list[MixedEdge]]:
        answer = {v: [] for v in self.vertices}
        for edge in self.edges:
            answer[edge.u].append(edge)
            answer[edge.v].append(edge)
        return answer

    def reticulations(self) -> frozenset[int]:
        heads = Counter(v for edge in self.edges for v in edge.heads())
        return frozenset(v for v, count in heads.items() if count == 2)


@dataclass(frozen=True)
class RootedGraph:
    root: int
    labels: tuple[tuple[int, str], ...]
    arcs: tuple[tuple[int, int], ...]

    @property
    def label_map(self) -> dict[int, str]:
        return dict(self.labels)

    @property
    def vertices(self) -> tuple[int, ...]:
        values = {self.root, *dict(self.labels)}
        for u, v in self.arcs:
            values.add(u)
            values.add(v)
        return tuple(sorted(values))

    def degrees(self) -> tuple[dict[int, int], dict[int, int]]:
        indegree = {v: 0 for v in self.vertices}
        outdegree = {v: 0 for v in self.vertices}
        for u, v in self.arcs:
            outdegree[u] += 1
            indegree[v] += 1
        return indegree, outdegree


def rooted_validation(graph: RootedGraph) -> tuple[bool, tuple[str, ...]]:
    problems: list[str] = []
    indegree, outdegree = graph.degrees()
    labels = graph.label_map
    if len(set(graph.arcs)) != len(graph.arcs):
        problems.append("parallel arc")
    if len(labels) != len(set(labels.values())):
        problems.append("duplicate label")
    if (indegree[graph.root], outdegree[graph.root]) != (0, 2):
        problems.append("root bidegree")
    for v in graph.vertices:
        degree = indegree[v], outdegree[v]
        if v == graph.root:
            continue
        if v in labels:
            if degree != (1, 0):
                problems.append(f"leaf {labels[v]} bidegree {degree}")
        elif degree not in {(1, 2), (2, 1)}:
            problems.append(f"internal {v} bidegree {degree}")
    children: dict[int, list[int]] = defaultdict(list)
    for u, v in graph.arcs:
        children[u].append(v)
    # Kahn order and reachability.
    work = dict(indegree)
    queue = deque(sorted(v for v in graph.vertices if work[v] == 0))
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for w in children[v]:
            work[w] -= 1
            if work[w] == 0:
                queue.append(w)
    if len(order) != len(graph.vertices):
        problems.append("directed cycle")
    reached = {graph.root}
    queue = deque([graph.root])
    while queue:
        v = queue.popleft()
        for w in children[v]:
            if w not in reached:
                reached.add(w)
                queue.append(w)
    if reached != set(graph.vertices):
        problems.append("not root reachable")
    return not problems, tuple(problems)


def root_is_lsa(graph: RootedGraph) -> bool:
    labels = set(graph.label_map)
    children: dict[int, list[int]] = defaultdict(list)
    for u, v in graph.arcs:
        children[u].append(v)
    for omitted in graph.vertices:
        if omitted == graph.root:
            continue
        reached = {graph.root}
        queue = deque([graph.root])
        while queue:
            v = queue.popleft()
            for w in children[v]:
                if w != omitted and w not in reached:
                    reached.add(w)
                    queue.append(w)
        if not (labels & reached):
            return False
    return True


def rooted_tree_child(graph: RootedGraph) -> bool:
    indegree, outdegree = graph.degrees()
    labels = set(graph.label_map)
    children: dict[int, list[int]] = defaultdict(list)
    for u, v in graph.arcs:
        children[u].append(v)
    good_children = labels | {v for v in graph.vertices if (indegree[v], outdegree[v]) == (1, 2)}
    return all(any(w in good_children for w in children[v]) for v in graph.vertices if outdegree[v])


def sd0(graph: RootedGraph) -> MixedGraph:
    """Narrow standard reduction: mark reticulation heads, suppress root once."""
    valid, problems = rooted_validation(graph)
    if not valid:
        raise ValueError(problems)
    indegree, _ = graph.degrees()
    edges = [MixedEdge.make(u, v, (v,) if indegree[v] == 2 else ()) for u, v in graph.arcs]
    incident = [edge for edge in edges if graph.root in edge.endpoints()]
    if len(incident) != 2:
        raise ValueError("root does not have two incident edges")
    retained = [edge for edge in edges if graph.root not in edge.endpoints()]
    first, second = incident
    a, b = first.other(graph.root), second.other(graph.root)
    if a == b:
        raise ValueError("root suppression loop")
    heads = set()
    if first.head_at(a):
        heads.add(a)
    if second.head_at(b):
        heads.add(b)
    retained.append(MixedEdge.make(a, b, heads))
    if len(retained) != len(set(retained)):
        raise ValueError("root suppression parallel edge")
    mixed = MixedGraph(graph.labels, tuple(sorted(retained)))
    incidence = mixed.incidence()
    labels = mixed.label_map
    if any(len(incidence[v]) != (1 if v in labels else 3) for v in mixed.vertices):
        raise ValueError("root suppression is not simple binary")
    if any(len(edge.heads()) > 1 for edge in mixed.edges):
        raise ValueError("bidirected edge")
    if any(sum(edge.head_at(v) for edge in incidence[v]) != 2 for v in mixed.reticulations()):
        raise ValueError("reticulation arrowheads lost")
    return mixed


def mixed_local_strong(graph: MixedGraph) -> bool:
    """Exact local criterion for every admissible rooting to be tree-child."""
    incidence = graph.incidence()
    for edge in graph.edges:
        heads = edge.heads()
        if len(heads) != 1:
            continue
        head = next(iter(heads))
        tail = edge.other(head)
        undirected = sum(not local.heads() for local in incidence[tail])
        if undirected != 2:
            return False
    return True


def admissible_rootings(graph: MixedGraph) -> tuple[RootedGraph, ...]:
    """Exhaust all narrow rootings; intended for finite convention audits."""
    answers: dict[tuple[tuple[int, int], ...], RootedGraph] = {}
    vertices = graph.vertices
    root = max(vertices, default=-1) + 1
    for split_index, split in enumerate(graph.edges):
        fixed: list[tuple[int, int]] = [(root, split.u), (root, split.v)]
        unoriented: list[MixedEdge] = []
        compatible = True
        # A bidirected split cannot arise under the lock.
        if len(split.heads()) > 1:
            continue
        for index, edge in enumerate(graph.edges):
            if index == split_index:
                continue
            heads = edge.heads()
            if not heads:
                unoriented.append(edge)
            elif len(heads) == 1:
                head = next(iter(heads))
                fixed.append((edge.other(head), head))
            else:
                compatible = False
                break
        if not compatible:
            continue
        for bits in product((0, 1), repeat=len(unoriented)):
            arcs = list(fixed)
            for edge, bit in zip(unoriented, bits):
                arcs.append((edge.u, edge.v) if bit == 0 else (edge.v, edge.u))
            rooted = RootedGraph(root, graph.labels, tuple(sorted(arcs)))
            valid, _ = rooted_validation(rooted)
            if not valid or not root_is_lsa(rooted):
                continue
            try:
                reduced = sd0(rooted)
            except ValueError:
                continue
            if canonical_mixed(reduced)[0] != canonical_mixed(graph)[0]:
                continue
            answers[rooted.arcs] = rooted
    return tuple(answers[key] for key in sorted(answers))


def standard_strong_by_census(graph: MixedGraph) -> tuple[bool, int, int]:
    roots = admissible_rootings(graph)
    return bool(roots) and all(rooted_tree_child(r) for r in roots), len(roots), sum(rooted_tree_child(r) for r in roots)


def _wl_colours(graph: MixedGraph) -> dict[int, int]:
    labels = graph.label_map
    incidence = graph.incidence()
    retics = graph.reticulations()
    signatures = {
        v: (("L", labels[v]) if v in labels else (("R",) if v in retics else ("I",)))
        for v in graph.vertices
    }
    while True:
        enriched = {}
        for v in graph.vertices:
            neighbours = []
            for edge in incidence[v]:
                w = edge.other(v)
                neighbours.append((edge.head_at(v), edge.head_at(w), signatures[w]))
            enriched[v] = (signatures[v], tuple(sorted(neighbours, key=repr)))
        palette = {signature: i for i, signature in enumerate(sorted(set(enriched.values()), key=repr))}
        new = {v: palette[enriched[v]] for v in graph.vertices}
        old_partition = {v: signatures[v] for v in graph.vertices}
        if all((old_partition[a] == old_partition[b]) == (new[a] == new[b]) for a in graph.vertices for b in graph.vertices):
            return new
        signatures = new


def canonical_mixed(graph: MixedGraph) -> tuple[str, dict[int, int]]:
    """Exact labelled mixed-graph canonical form and raw-to-canonical map."""
    labels = graph.label_map
    colours = _wl_colours(graph)
    cells: dict[int, list[int]] = defaultdict(list)
    for v, colour in colours.items():
        cells[colour].append(v)
    ordered_cells = [tuple(sorted(cells[key])) for key in sorted(cells)]
    # Labels are already singleton cells; remaining ties are small path/core
    # automorphism cells.  Enumerating only within stable WL cells is exact.
    best: tuple | None = None
    best_map: dict[int, int] | None = None
    choices = [tuple(permutations(cell)) for cell in ordered_cells]
    for cell_orders in product(*choices):
        order = tuple(v for cell in cell_orders for v in cell)
        mapping = {v: i for i, v in enumerate(order)}
        encoded_labels = tuple(sorted((mapping[v], label) for v, label in labels.items()))
        encoded_edges = []
        for edge in graph.edges:
            u, v = mapping[edge.u], mapping[edge.v]
            heads = {mapping[h] for h in edge.heads()}
            encoded_edges.append(MixedEdge.make(u, v, heads))
        code_tuple = (encoded_labels, tuple(sorted(encoded_edges)))
        if best is None or code_tuple < best:
            best = code_tuple
            best_map = mapping
    assert best is not None and best_map is not None
    return repr(best), best_map


def mixed_automorphisms(graph: MixedGraph) -> tuple[dict[int, int], ...]:
    """All label- and arrowhead-preserving automorphisms.

    Stable WL cells only restrict the exact permutation search; every
    permutation inside every cell is still tested against the complete mixed
    edge set.  Primitive/support graphs are small enough that this is a direct
    certificate rather than a heuristic canonicalization claim.
    """
    colours = _wl_colours(graph)
    cells: dict[int, list[int]] = defaultdict(list)
    for vertex, colour in colours.items():
        cells[colour].append(vertex)
    ordered_cells = [tuple(sorted(cells[key])) for key in sorted(cells)]
    original_labels = graph.label_map
    original_edges = set(graph.edges)
    answers = []
    for moved_cells in product(*(tuple(permutations(cell)) for cell in ordered_cells)):
        mapping = {
            old: new
            for cell, moved in zip(ordered_cells, moved_cells)
            for old, new in zip(cell, moved)
        }
        if any(original_labels.get(mapping[vertex]) != label for vertex, label in graph.labels):
            continue
        moved_edges = set()
        for edge in graph.edges:
            heads = {mapping[head] for head in edge.heads()}
            moved_edges.add(MixedEdge.make(mapping[edge.u], mapping[edge.v], heads))
        if moved_edges == original_edges:
            answers.append(mapping)
    return tuple(answers)


def underlying_triangles(graph: MixedGraph) -> tuple[tuple[int, int, int], ...]:
    adjacency = {v: set() for v in graph.vertices}
    for edge in graph.edges:
        adjacency[edge.u].add(edge.v)
        adjacency[edge.v].add(edge.u)
    answer = []
    vertices = graph.vertices
    for i, u in enumerate(vertices):
        for j in range(i + 1, len(vertices)):
            v = vertices[j]
            if v not in adjacency[u]:
                continue
            for k in range(j + 1, len(vertices)):
                w = vertices[k]
                if w in adjacency[u] and w in adjacency[v]:
                    answer.append((u, v, w))
    return tuple(answer)


def t_quotient(graph: MixedGraph) -> MixedGraph:
    triangles = underlying_triangles(graph)
    if not triangles:
        return graph
    if len(triangles) > 1:
        raise ValueError("ordinary T quotient requested with multiple triangles")
    triangle = set(triangles[0])
    edges = []
    for edge in graph.edges:
        if edge.u in triangle and edge.v in triangle:
            edges.append(MixedEdge.make(edge.u, edge.v))
        else:
            edges.append(edge)
    return MixedGraph(graph.labels, tuple(sorted(edges)))


def displayed_switchings(graph: RootedGraph):
    indegree, _ = graph.degrees()
    retics = tuple(sorted(v for v in graph.vertices if indegree[v] == 2))
    incoming = {r: tuple(i for i, (_, v) in enumerate(graph.arcs) if v == r) for r in retics}
    for choices in product((0, 1), repeat=len(retics)):
        removed = {incoming[r][1 - choice] for r, choice in zip(retics, choices)}
        active = tuple(i for i in range(len(graph.arcs)) if i not in removed)
        yield choices, active


def descendant_masks(graph: RootedGraph, active: Sequence[int], ordered_labels: Sequence[str]) -> tuple[int, ...]:
    label_index = {label: i for i, label in enumerate(ordered_labels)}
    leaves = {v: label_index[label] for v, label in graph.labels if label in label_index}
    all_leaves = set(dict(graph.labels))
    children: dict[int, list[int]] = defaultdict(list)
    for index in active:
        u, v = graph.arcs[index]
        children[u].append(v)
    cache: dict[int, int] = {}

    def visit(v: int) -> int:
        if v in cache:
            return cache[v]
        if v in all_leaves:
            value = (1 << leaves[v]) if v in leaves else 0
        else:
            value = 0
            for w in children[v]:
                value |= visit(w)
        cache[v] = value
        return value

    return tuple(visit(graph.arcs[index][1]) for index in active)
