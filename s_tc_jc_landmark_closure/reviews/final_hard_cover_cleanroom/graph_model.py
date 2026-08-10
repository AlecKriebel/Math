"""Independent rooted/mixed graph machinery for the final hard-cover audit.

This module deliberately uses no project graph code.  Vertices are integers,
arcs are ordered pairs, and labelled leaves carry arbitrary immutable colours.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
import hashlib
import itertools
import json
from typing import Dict, Hashable, Iterable, Iterator, List, Mapping, Sequence, Set, Tuple


Arc = Tuple[int, int]


def stable_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(obj) -> str:
    return hashlib.sha256(stable_json(obj).encode()).hexdigest()


@dataclass(frozen=True)
class RootedGraph:
    arcs: Tuple[Arc, ...]
    root: int
    labels: Tuple[Tuple[int, str], ...]

    @staticmethod
    def make(arcs: Iterable[Arc], root: int, labels: Mapping[int, Hashable]) -> "RootedGraph":
        return RootedGraph(
            tuple(sorted(set((int(u), int(v)) for u, v in arcs))),
            int(root),
            tuple(sorted((int(v), str(c)) for v, c in labels.items())),
        )

    @property
    def label_map(self) -> Dict[int, str]:
        return dict(self.labels)

    @property
    def vertices(self) -> Set[int]:
        out = {self.root}
        for u, v in self.arcs:
            out.add(u); out.add(v)
        out.update(v for v, _ in self.labels)
        return out

    def degrees(self):
        indeg = Counter(); outdeg = Counter()
        children = defaultdict(list); parents = defaultdict(list)
        for u, v in self.arcs:
            outdeg[u] += 1; indeg[v] += 1
            children[u].append(v); parents[v].append(u)
        return indeg, outdeg, children, parents


def topological_order(g: RootedGraph) -> List[int]:
    indeg, _, children, _ = g.degrees()
    q = deque(sorted(v for v in g.vertices if indeg[v] == 0))
    ans = []
    while q:
        u = q.popleft(); ans.append(u)
        for v in sorted(children[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(ans) != len(g.vertices):
        raise ValueError("directed cycle")
    return ans


def biconnected_components(vertices: Set[int], undirected_edges: Iterable[Tuple[int, int]]):
    adj = defaultdict(list)
    edges = []
    for i, (a, b) in enumerate(sorted({tuple(sorted(e)) for e in undirected_edges})):
        edges.append((a, b)); adj[a].append((b, i)); adj[b].append((a, i))
    timer = 0; tin = {}; low = {}; stack = []; comps = []

    def dfs(u: int, parent_edge: int | None):
        nonlocal timer
        timer += 1; tin[u] = low[u] = timer
        for v, ei in adj[u]:
            if ei == parent_edge:
                continue
            if v not in tin:
                stack.append(ei); dfs(v, ei); low[u] = min(low[u], low[v])
                if low[v] >= tin[u]:
                    comp = set()
                    while True:
                        ej = stack.pop(); comp.add(ej)
                        if ej == ei: break
                    comps.append(comp)
            elif tin[v] < tin[u]:
                stack.append(ei); low[u] = min(low[u], tin[v])

    for v in sorted(vertices):
        if v not in tin:
            dfs(v, None)
            if stack:
                comps.append(set(stack)); stack.clear()
    return [[edges[i] for i in sorted(c)] for c in comps]


def validate_standard_strong(g: RootedGraph) -> Dict[str, object]:
    """Validate the rooted presentation and the local level-two conditions."""
    indeg, outdeg, children, _ = g.degrees(); labels = g.label_map; V = g.vertices
    errors = []
    try:
        topo = topological_order(g)
    except ValueError:
        topo = []; errors.append("directed cycle")
    if indeg[g.root] != 0 or outdeg[g.root] != 2:
        errors.append("bad root degree")
    roots = [v for v in V if indeg[v] == 0]
    if roots != [g.root]: errors.append("root not unique")
    for v in V:
        d = (indeg[v], outdeg[v])
        if v == g.root:
            continue
        if v in labels:
            if d != (1, 0): errors.append(f"bad labelled leaf {v}:{d}")
        elif d not in ((1, 2), (2, 1)):
            errors.append(f"bad internal degree {v}:{d}")
    if len(set(labels.values())) != len(labels): errors.append("duplicate labels")
    if len(g.arcs) != len(set(g.arcs)): errors.append("parallel directed arcs")
    if any((v, u) in set(g.arcs) for u, v in g.arcs): errors.append("directed 2-cycle")
    rets = {v for v in V if (indeg[v], outdeg[v]) == (2, 1)}
    for v in V:
        if outdeg[v] and not any(c not in rets for c in children[v]):
            errors.append(f"tree-child failure {v}")
        if v in rets and any(c in rets for c in children[v]):
            errors.append(f"reticulation child failure {v}")
    if topo:
        leafset = set(labels)
        desc = {v: ({v} if v in leafset else set()) for v in V}
        for v in reversed(topo):
            for c in children[v]: desc[v] |= desc[c]
        if desc[g.root] != leafset: errors.append("root does not reach every leaf")
        if any(v != g.root and desc[v] == leafset for v in V):
            errors.append("root is not the lowest stable ancestor")
    comps = biconnected_components(V, ((u, v) for u, v in g.arcs))
    levels = []
    for comp in comps:
        cv = {x for e in comp for x in e}
        if len(comp) >= 3:
            levels.append(len(cv & rets))
    if any(x > 2 for x in levels): errors.append("level exceeds two")
    return {"ok": not errors, "errors": errors, "reticulations": len(rets), "blob_levels": levels}


def _refine(vertices, colours, relations, partition):
    """Equitable refinement for a directed/edge-coloured relational graph."""
    while True:
        cell_of = {v: i for i, cell in enumerate(partition) for v in cell}
        new = []
        changed = False
        for cell in partition:
            buckets = defaultdict(list)
            for v in cell:
                sig = [colours[v]]
                for j in range(len(partition)):
                    counts = Counter()
                    for w in vertices:
                        rel = relations.get((v, w))
                        if rel is not None and cell_of[w] == j:
                            counts[("o", rel)] += 1
                        rel = relations.get((w, v))
                        if rel is not None and cell_of[w] == j:
                            counts[("i", rel)] += 1
                    sig.append(tuple(sorted(counts.items())))
                buckets[tuple(sig)].append(v)
            if len(buckets) > 1: changed = True
            for key in sorted(buckets, key=repr): new.append(tuple(sorted(buckets[key])))
        partition = tuple(new)
        if not changed: return partition


def canonical_relational(vertices: Iterable[int], colours: Mapping[int, str],
                         relations: Mapping[Tuple[int, int], str]):
    """Exact individualization/refinement canonical form and one minimizing order."""
    V = tuple(sorted(vertices))
    byc = defaultdict(list)
    for v in V: byc[colours[v]].append(v)
    initial = tuple(tuple(sorted(byc[c])) for c in sorted(byc))
    best = None; best_order = None

    def encode(order):
        pos = {v: i for i, v in enumerate(order)}
        rels = sorted((pos[u], pos[v], c) for (u, v), c in relations.items())
        return (tuple(colours[v] for v in order), tuple(rels))

    def visit(partition):
        nonlocal best, best_order
        partition = _refine(V, colours, relations, partition)
        if all(len(c) == 1 for c in partition):
            order = tuple(c[0] for c in partition); code = encode(order)
            if best is None or code < best:
                best = code; best_order = order
            return
        # A smallest ambiguous cell gives reliable pruning on these tiny cores.
        _, idx = min((len(c), i) for i, c in enumerate(partition) if len(c) > 1)
        cell = partition[idx]
        for v in cell:
            rest = tuple(x for x in cell if x != v)
            nxt = partition[:idx] + ((v,), rest) + partition[idx + 1:]
            visit(nxt)

    visit(initial)
    obj = {"colours": best[0], "relations": best[1]}
    return stable_json(obj), best_order


def rooted_code(g: RootedGraph, selected_generic: bool = False):
    indeg, outdeg, _, _ = g.degrees(); lm = g.label_map
    colours = {}
    for v in g.vertices:
        if v == g.root: colours[v] = "ROOT"
        elif v in lm:
            c = lm[v]
            colours[v] = "SEL" if selected_generic and c.startswith("L_") else "LEAF:" + c
        elif (indeg[v], outdeg[v]) == (2, 1): colours[v] = "RETIC"
        else: colours[v] = "TREE"
    rel = {(u, v): "ARC" for u, v in g.arcs}
    return canonical_relational(g.vertices, colours, rel)


def semidirected(g: RootedGraph):
    """Suppress the root and retain arrowheads only at reticulation heads."""
    indeg, outdeg, children, _ = g.degrees(); rets = {v for v in g.vertices if (indeg[v], outdeg[v]) == (2, 1)}
    ch = list(children[g.root])
    if len(ch) != 2: raise ValueError("root must have two children")
    edges = {}
    for u, v in g.arcs:
        if u == g.root: continue
        a, b = sorted((u, v)); hu = int(u in rets); hv = int(v in rets)
        # Arc u->v can only carry an arrowhead at v.
        hu, hv = (0, int(v in rets)) if a == u else (int(v in rets), 0)
        edges[(a, b)] = (hu, hv)
    a, b = ch
    x, y = sorted((a, b))
    hx = int(x in rets); hy = int(y in rets)
    edges[(x, y)] = (hx, hy)
    V = g.vertices - {g.root}
    return V, edges, g.label_map


def standard_semidirected_audit(g: RootedGraph) -> Dict[str, object]:
    """Audit ``sd_0(g)`` and the locked local ``S_TC`` criterion.

    This is intentionally not an admissible-rooting census.  The supplied
    rooted graph is an existence witness.  After checking that its single
    root suppression is a valid simple binary mixed graph, the exact locked
    criterion says that *every* admissible rooting is tree-child precisely
    when both other incidences at every tail of a retained reticulation edge
    are wholly undirected.

    The implementation keeps a multiset until simplicity has been checked;
    a dictionary-based mixed representation would otherwise silently erase a
    root-created parallel edge.
    """
    rooted = validate_standard_strong(g)
    errors = []
    if not rooted["ok"]:
        errors.extend(f"rooted witness: {x}" for x in rooted["errors"])

    indeg, outdeg, children, _ = g.degrees()
    retics = {v for v in g.vertices if (indeg[v], outdeg[v]) == (2, 1)}
    root_children = tuple(children[g.root])
    if len(root_children) != 2:
        errors.append("root does not have two distinct suppression incidences")
        return {"ok": False, "errors": errors, "standard_strong": False}

    raw_edges = []
    for u, v in g.arcs:
        if u == g.root:
            continue
        a, b = sorted((u, v))
        raw_edges.append((a, b, int(a == v and v in retics), int(b == v and v in retics)))
    u, v = root_children
    if u == v:
        errors.append("root suppression creates a loop")
    else:
        a, b = sorted((u, v))
        raw_edges.append((a, b, int(a in retics), int(b in retics)))

    pair_counts = Counter((a, b) for a, b, _, _ in raw_edges)
    parallels = sorted(e for e, n in pair_counts.items() if n != 1)
    if parallels:
        errors.append(f"root suppression creates parallel edges: {parallels}")
    if any(ha and hb for _, _, ha, hb in raw_edges):
        errors.append("root suppression creates a two-arrowhead edge")

    # Continue only with a simple relation; retaining the first copy after an
    # already-recorded simplicity failure is safe for diagnostic counts.
    edges = {}
    for a, b, ha, hb in raw_edges:
        edges.setdefault((a, b), (ha, hb))
    vertices = g.vertices - {g.root}
    degree = Counter()
    arrowheads = Counter()
    adjacency = defaultdict(list)
    for (a, b), (ha, hb) in edges.items():
        degree[a] += 1; degree[b] += 1
        arrowheads[a] += ha; arrowheads[b] += hb
        adjacency[a].append(((a, b), ha, hb))
        adjacency[b].append(((a, b), hb, ha))
    labels = g.label_map
    for x in vertices:
        want = 1 if x in labels else 3
        if degree[x] != want:
            errors.append(f"nonbinary mixed degree {x}:{degree[x]} expected {want}")
        if x in labels and arrowheads[x]:
            errors.append(f"arrowhead at labelled leaf {x}")
        if x in retics:
            if arrowheads[x] != 2:
                errors.append(f"reticulation {x} has {arrowheads[x]} retained arrowheads")
        elif arrowheads[x]:
            errors.append(f"arrowhead at nonreticulation {x}")

    # Underlying connectedness and level are checked directly on sd_0.
    if vertices:
        seen = set(); todo = [min(vertices)]
        while todo:
            x = todo.pop()
            if x in seen: continue
            seen.add(x)
            for (a, b), _, _ in adjacency[x]: todo.append(b if x == a else a)
        if seen != vertices: errors.append("mixed graph is disconnected")
    comps = biconnected_components(vertices, edges)
    blob_levels = []
    for comp in comps:
        cv = {x for e in comp for x in e}
        if len(comp) >= 3: blob_levels.append(len(cv & retics))
    if any(x > 2 for x in blob_levels): errors.append("mixed level exceeds two")

    tail_failures = []
    for (a, b), (ha, hb) in edges.items():
        if ha ^ hb:
            tail = b if ha else a
            current = (a, b)
            other = [item for item in adjacency[tail] if item[0] != current]
            if len(other) != 2 or any(own_head or far_head for _, own_head, far_head in other):
                tail_failures.append(tail)
    if tail_failures:
        errors.append(f"locked S_TC tail criterion fails at {sorted(set(tail_failures))}")

    return {
        "ok": not errors,
        "errors": errors,
        "standard_strong": not tail_failures and not errors,
        "reticulations": len(retics),
        "blob_levels": blob_levels,
        "mixed_edge_count": len(edges),
        "tail_failures": sorted(set(tail_failures)),
    }


def mixed_code(g: RootedGraph, erase_triangle_arrowheads: bool = False):
    V, edges, labels = semidirected(g)
    if erase_triangle_arrowheads:
        adj = defaultdict(set)
        for u, v in edges: adj[u].add(v); adj[v].add(u)
        tri_edges = set()
        for a in V:
            for b in adj[a]:
                if b <= a: continue
                for c in adj[a] & adj[b]:
                    tri_edges |= {tuple(sorted((a, b))), tuple(sorted((a, c))), tuple(sorted((b, c)))}
        edges = {e: ((0, 0) if e in tri_edges else h) for e, h in edges.items()}
    deg = Counter()
    for u, v in edges: deg[u] += 1; deg[v] += 1
    colours = {}
    for v in V:
        if v in labels: colours[v] = "LEAF:" + labels[v]
        else: colours[v] = "INTERNAL"
    rel = {}
    for (u, v), (hu, hv) in edges.items():
        rel[(u, v)] = f"M:{hu}{hv}"
        rel[(v, u)] = f"M:{hv}{hu}"
    return canonical_relational(V, colours, rel)


def decorated_mixed_relation(source: RootedGraph, target: RootedGraph,
                             port_matching: Sequence[Tuple[str, str]],
                             direction: str = "source_to_target"):
    """Canonicalize a complete directed source--target mixed-graph relation.

    Canonicalizing the two sides separately is insufficient when raw
    presentations carry different boundary transports.  This routine forms
    one coloured disjoint union and adds the entire port-matching relation
    before individualization/refinement.  The returned transports are from
    raw source/target vertices to the canonical disjoint-union positions.
    """
    if direction != "source_to_target":
        raise ValueError("only the locked source-to-target direction is valid")
    for side, graph in (("source", source), ("target", target)):
        audit = standard_semidirected_audit(graph)
        if not audit["ok"]:
            raise ValueError((side, "not a standard S_TC presentation", audit))
    sv, se, sl = semidirected(source); tv, te, tl = semidirected(target)
    sorder = sorted(sv); torder = sorted(tv)
    smap = {v: i for i, v in enumerate(sorder)}
    tmap = {v: len(sorder) + i for i, v in enumerate(torder)}
    vertices = tuple(range(len(sorder) + len(torder)))
    colours = {}
    for v in sorder:
        colours[smap[v]] = "S|PORT:" + sl[v] if v in sl else "S|INTERNAL"
    for v in torder:
        colours[tmap[v]] = "T|PORT:" + tl[v] if v in tl else "T|INTERNAL"
    relations = {}
    for (u, v), (hu, hv) in se.items():
        a, b = smap[u], smap[v]
        relations[(a, b)] = f"S:M:{hu}{hv}"
        relations[(b, a)] = f"S:M:{hv}{hu}"
    for (u, v), (hu, hv) in te.items():
        a, b = tmap[u], tmap[v]
        relations[(a, b)] = f"T:M:{hu}{hv}"
        relations[(b, a)] = f"T:M:{hv}{hu}"
    sinv = defaultdict(list); tinv = defaultdict(list)
    for v, label in sl.items(): sinv[label].append(v)
    for v, label in tl.items(): tinv[label].append(v)
    normalized_matching = []
    for source_label, target_label in port_matching:
        if len(sinv[source_label]) != 1 or len(tinv[target_label]) != 1:
            raise ValueError(("invalid port match", source_label, target_label))
        a, b = smap[sinv[source_label][0]], tmap[tinv[target_label][0]]
        if (a, b) in relations or (b, a) in relations:
            raise ValueError("port matching collides with an internal relation")
        relations[(a, b)] = "PORT_MATCH"
        relations[(b, a)] = "PORT_MATCH"
        normalized_matching.append((source_label, target_label))
    if len(set(normalized_matching)) != len(normalized_matching):
        raise ValueError("duplicate port match")
    if len({x for x, _ in normalized_matching}) != len(normalized_matching):
        raise ValueError("source port matched more than once")
    if len({y for _, y in normalized_matching}) != len(normalized_matching):
        raise ValueError("target port matched more than once")
    code, order = canonical_relational(vertices, colours, relations)
    canonical_position = {v: i for i, v in enumerate(order)}
    return {
        "code": code,
        "sha256": digest(code),
        "direction": direction,
        "port_matching": tuple(sorted(normalized_matching)),
        "source_vertex_transport": tuple(sorted((v, canonical_position[smap[v]]) for v in sorder)),
        "target_vertex_transport": tuple(sorted((v, canonical_position[tmap[v]]) for v in torder)),
    }


def strip_word_ports(record: Mapping[str, object]):
    """Recover a skeleton and segment words from one frozen support record."""
    arcs = set(tuple(x) for x in record["arcs"])
    labels = {int(v): str(c) for v, c in record["labels"]}
    children = defaultdict(list); parents = defaultdict(list)
    for u, v in arcs: children[u].append(v); parents[v].append(u)
    role_vertex = {c: v for v, c in labels.items()}
    words = [list(w) for w in record["words"]]
    segment_edges = [None] * len(words)
    word_parents = set()
    for i, word in enumerate(words):
        if not word: continue
        ps = [parents[role_vertex[r]][0] for r in word]
        word_parents.update(ps)
        pred = next(x for x in parents[ps[0]] if x not in ps)
        path_children = [x for x in children[ps[-1]] if x != role_vertex[word[-1]]]
        if len(path_children) != 1: raise ValueError("ambiguous word chain")
        segment_edges[i] = (pred, path_children[0])
    word_leaves = {role_vertex[r] for w in words for r in w}
    sk_arcs = {(u, v) for u, v in arcs if u not in word_parents and v not in word_parents and u not in word_leaves and v not in word_leaves}
    for e in segment_edges:
        if e is not None: sk_arcs.add(e)
    sk_labels = {v: c for v, c in labels.items() if v not in word_leaves}
    sk = RootedGraph.make(sk_arcs, int(record["root"]), sk_labels)
    leaves = set(sk_labels)
    candidate = sorted((u, v) for u, v in sk.arcs if u != sk.root and u not in leaves and v not in leaves)
    used = {e for e in segment_edges if e is not None}
    remaining = [e for e in candidate if e not in used]
    empty = [i for i, e in enumerate(segment_edges) if e is None]
    # The rank-one skeleton has two abstract parallel S->X segments.  The
    # full binary graph is simple because a minimum repair subdivides one of
    # them.  Suppression deliberately exposes the duplicate abstract edge.
    if record["core_id"] == "cycle" and len(empty) == 1 and not remaining and len(used) == 1:
        remaining = [next(iter(used))]
    if len(remaining) != len(empty):
        raise ValueError((record["core_id"], "segment recovery", remaining, empty))
    for i, e in zip(empty, remaining): segment_edges[i] = e
    return sk, tuple(segment_edges), tuple(tuple(w) for w in words)


def recover_template(record: Mapping[str, object], universe_records: Sequence[Mapping[str, object]]):
    """Recover every abstract segment, including suppressed parallel ones.

    The frozen support input contains the one-extra-port probe on every
    segment.  We use those *graph encodings*, not a completion table, to read
    the two skeleton endpoints of each abstract segment independently.
    """
    # Build the skeleton by deleting all word ports.  strip_word_ports may be
    # short of abstract parallel edges, so perform the deletion directly.
    arcs = set(tuple(x) for x in record["arcs"])
    labels = {int(v): str(c) for v, c in record["labels"]}
    children = defaultdict(list); parents = defaultdict(list)
    for u, v in arcs: children[u].append(v); parents[v].append(u)
    rv = {c: v for v, c in labels.items()}
    words = [list(w) for w in record["words"]]
    word_parents = set(); word_leaves = set(); known_edges = {}
    for i, word in enumerate(words):
        if not word: continue
        ps = [parents[rv[r]][0] for r in word]
        word_parents.update(ps); word_leaves.update(rv[r] for r in word)
        pred = next(x for x in parents[ps[0]] if x not in ps)
        child = next(x for x in children[ps[-1]] if x != rv[word[-1]])
        known_edges[i] = (pred, child)
    sk_arcs = {(u, v) for u, v in arcs if u not in word_parents and v not in word_parents and u not in word_leaves and v not in word_leaves}
    sk_arcs.update(known_edges.values())
    sk_labels = {v: c for v, c in labels.items() if v not in word_leaves}
    sk = RootedGraph.make(sk_arcs, int(record["root"]), sk_labels)

    edges = []
    for si in range(len(words)):
        probes = []
        for q in universe_records:
            if q["core_id"] != record["core_id"] or q["repair_index"] != record["repair_index"] or q["extra_count"] != 1:
                continue
            if si >= len(q["words"]) or "P_0" not in q["words"][si]:
                continue
            probes.append(q)
        if not probes: raise ValueError(("missing one-port segment probe", record["core_id"], record["repair_index"], si))
        q = probes[0]; qa = set(tuple(x) for x in q["arcs"]); ql = {int(v): str(c) for v, c in q["labels"]}
        qc = defaultdict(list); qp = defaultdict(list)
        for u, v in qa: qc[u].append(v); qp[v].append(u)
        qrv = {c: v for v, c in ql.items()}; word = list(q["words"][si])
        ps = [qp[qrv[r]][0] for r in word]
        pred = next(x for x in qp[ps[0]] if x not in ps)
        child = next(x for x in qc[ps[-1]] if x != qrv[word[-1]])
        e = (pred, child)
        if e not in sk.arcs: raise ValueError(("probe endpoint not in skeleton", e, sorted(sk.arcs)))
        edges.append(e)
    return sk, tuple(edges), tuple(tuple(w) for w in words)


def build_from_skeleton(skeleton: RootedGraph, segment_edges: Sequence[Arc],
                        words: Sequence[Sequence[str]], fixed_leaf_labels: Mapping[str, str]):
    """Replace each core segment edge by the requested labelled port word."""
    arcs = set(skeleton.arcs); base_labels = skeleton.label_map
    labels = {}
    for v, old in base_labels.items(): labels[v] = fixed_leaf_labels.get(old, old)
    nxt = max(skeleton.vertices) + 1
    for e in set(segment_edges):
        if e not in arcs: raise ValueError(("missing segment edge", e))
        arcs.remove(e)
    direct_counts = Counter(e for e, word in zip(segment_edges, words) if not word)
    if any(n > 1 for n in direct_counts.values()):
        raise ValueError("parallel unsubdivided abstract segments")
    for e, word in zip(segment_edges, words):
        tail, head = e; prev = tail
        for role in word:
            tv, lv = nxt, nxt + 1; nxt += 2
            arcs.add((prev, tv)); arcs.add((tv, lv)); labels[lv] = str(role); prev = tv
        arcs.add((prev, head))
    return RootedGraph.make(arcs, skeleton.root, labels)


def insert_label_in_words(words: Sequence[Sequence[str]], label: str):
    """All segment positions, preserving the complete existing path order."""
    for i, word in enumerate(words):
        for j in range(len(word) + 1):
            out = [list(x) for x in words]
            out[i].insert(j, label)
            yield tuple(tuple(x) for x in out)


def weak_compositions(n: int, k: int):
    if k == 1:
        yield (n,); return
    for i in range(n + 1):
        for tail in weak_compositions(n - i, k - 1): yield (i,) + tail
