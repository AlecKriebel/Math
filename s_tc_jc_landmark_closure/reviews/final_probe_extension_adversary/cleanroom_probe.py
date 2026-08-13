"""Independent exact machinery for the terminal-extension adversarial gate.

This module deliberately uses no project research implementation.  Sparse
integer polynomials, rooted validation, bridge detection, standard mixed
reduction, displayed-tree enumeration, JC Fourier pullbacks, graph maps, and
modular Jacobian ranks are implemented here from first principles.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import itertools
import json
from collections import Counter, defaultdict, deque


PRIME = 1_000_003


def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(obj):
    return hashlib.sha256(canonical_json(obj).encode()).hexdigest()


# Sparse integer polynomials.  A monomial is a sorted tuple (variable, power).
ZERO = {}
ONE = {(): 1}


def _mono(d):
    return tuple(sorted((str(k), int(v)) for k, v in d.items() if v))


def pvar(name):
    return {((str(name), 1),): 1}


def padd(a, b):
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, 0) + c
        if out[m] == 0:
            del out[m]
    return out


def pscale(a, c):
    if c == 0:
        return {}
    return {m: c * v for m, v in a.items() if c * v}


def pmul(a, b):
    if not a or not b:
        return {}
    out = {}
    for ma, ca in a.items():
        da = dict(ma)
        for mb, cb in b.items():
            d = dict(da)
            for v, e in mb:
                d[v] = d.get(v, 0) + e
            m = _mono(d)
            out[m] = out.get(m, 0) + ca * cb
    return {m: c for m, c in out.items() if c}


def ppow(a, n):
    out = ONE
    for _ in range(n):
        out = pmul(out, a)
    return out


def pone_minus(name):
    return padd(ONE, pscale(pvar(name), -1))


def pderiv(a, name):
    out = {}
    for m, c in a.items():
        d = dict(m)
        e = d.get(name, 0)
        if not e:
            continue
        if e == 1:
            del d[name]
        else:
            d[name] = e - 1
        mm = _mono(d)
        out[mm] = out.get(mm, 0) + c * e
    return out


def peval(a, values, modulus=None):
    total = 0
    for m, c in a.items():
        z = c
        for v, e in m:
            z *= pow(values[v], e, modulus) if modulus else values[v] ** e
            if modulus:
                z %= modulus
        total += z
        if modulus:
            total %= modulus
    return total % modulus if modulus else total


def poly_json(a):
    return [[[[v, e] for v, e in m], c] for m, c in sorted(a.items())]


def poly_digest(a):
    return digest(poly_json(a))


@dataclass(frozen=True)
class RootedGraph:
    root: int
    arcs: tuple
    labels: tuple

    @classmethod
    def from_json(cls, obj):
        labels = obj.get("labels", {})
        if isinstance(labels, list):
            labels = dict(labels)
        return cls(
            int(obj["root"]),
            tuple(sorted((int(u), int(v)) for u, v in obj["arcs"])),
            tuple(sorted((int(v), str(l)) for v, l in labels.items())),
        )

    def to_json(self):
        return {
            "root": self.root,
            "arcs": [list(e) for e in self.arcs],
            "labels": {str(v): l for v, l in self.labels},
        }

    @property
    def label_map(self):
        return dict(self.labels)

    @property
    def vertices(self):
        return set(itertools.chain.from_iterable(self.arcs)) | {self.root} | set(self.label_map)

    def indegrees(self):
        d = Counter(v for _, v in self.arcs)
        return {v: d[v] for v in self.vertices}

    def outdegrees(self):
        d = Counter(u for u, _ in self.arcs)
        return {v: d[v] for v in self.vertices}

    @property
    def reticulations(self):
        return tuple(sorted(v for v, d in self.indegrees().items() if d == 2))


def validate_rooted(g, require_tree_child=True):
    problems = []
    if len(set(g.arcs)) != len(g.arcs):
        problems.append("parallel directed arc")
    if any(u == v for u, v in g.arcs):
        problems.append("directed loop")
    indeg, outdeg = g.indegrees(), g.outdegrees()
    if indeg.get(g.root, 0) != 0 or outdeg.get(g.root, 0) != 2:
        problems.append("root bidegree")
    labels = g.label_map
    if len(set(labels.values())) != len(labels):
        problems.append("duplicate label")
    for v in g.vertices:
        pair = (indeg[v], outdeg[v])
        if v == g.root:
            continue
        if v in labels:
            if pair != (1, 0):
                problems.append(f"labelled vertex {v} has bidegree {pair}")
        elif pair not in ((1, 2), (2, 1)):
            problems.append(f"internal vertex {v} has bidegree {pair}")
    # DAG and reachability.
    children = defaultdict(list)
    for u, v in g.arcs:
        children[u].append(v)
    color = {}

    def visit(v):
        if color.get(v) == 1:
            return False
        if color.get(v) == 2:
            return True
        color[v] = 1
        if not all(visit(w) for w in children[v]):
            return False
        color[v] = 2
        return True

    if not visit(g.root):
        problems.append("directed cycle")
    if set(color) != g.vertices:
        problems.append("not all vertices reachable")
    if require_tree_child:
        # Concrete tree-child condition for this rooted presentation.
        rets = set(g.reticulations)
        for v in g.vertices:
            if outdeg[v] and not any(w not in rets for w in children[v]):
                problems.append(f"vertex {v} has only reticulation children")
        for r in rets:
            if any(w in rets for w in children[r]):
                problems.append(f"reticulation {r} has reticulation child")
    return problems


def root_is_lsa(g):
    """Check that no nonroot vertex is stable above every labelled leaf."""
    children = defaultdict(list)
    for u, v in g.arcs:
        children[u].append(v)
    leaves = set(g.label_map)
    for blocked in g.vertices - {g.root}:
        seen = {g.root}
        todo = [g.root]
        while todo:
            v = todo.pop()
            for w in children[v]:
                if w != blocked and w not in seen:
                    seen.add(w)
                    todo.append(w)
        # blocked is stable for every leaf iff removing it disconnects every
        # labelled leaf from the root.
        if not (leaves & seen):
            return False
    return True


def undirected_bridges(g):
    edges = list(g.arcs)
    adj = defaultdict(list)
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    tin, low, bridges = {}, {}, set()
    tick = [0]

    def dfs(v, parent_edge=-1):
        tick[0] += 1
        tin[v] = low[v] = tick[0]
        for w, ei in adj[v]:
            if ei == parent_edge:
                continue
            if w in tin:
                low[v] = min(low[v], tin[w])
            else:
                dfs(w, ei)
                low[v] = min(low[v], low[w])
                if low[w] > tin[v]:
                    bridges.add(ei)

    dfs(g.root)
    return {edges[i] for i in bridges}


def admissible_internal_blob_arcs(g):
    labels = set(g.label_map)
    bridges = undirected_bridges(g)
    return tuple(
        e for e in g.arcs
        if e not in bridges and g.root not in e and e[0] not in labels and e[1] not in labels
    )


def insert_port(g, arc, label):
    if arc not in admissible_internal_blob_arcs(g):
        raise ValueError(f"not an admissible internal blob arc: {arc}")
    if label in g.label_map.values():
        raise ValueError(f"duplicate physical label: {label}")
    w = max(g.vertices) + 1
    leaf = w + 1
    arcs = []
    for e in g.arcs:
        if e == arc:
            arcs.extend([(e[0], w), (w, e[1]), (w, leaf)])
        else:
            arcs.append(e)
    labels = dict(g.labels)
    labels[leaf] = label
    child = RootedGraph(g.root, tuple(sorted(arcs)), tuple(sorted(labels.items())))
    return child, {"old_to_new": [[v, v] for v in sorted(g.vertices)], "subdivision": w, "leaf": leaf}


def delete_port(g, label):
    labels = g.label_map
    leaves = [v for v, x in labels.items() if x == label]
    if len(leaves) != 1:
        raise ValueError("new label must occur exactly once")
    leaf = leaves[0]
    parents = [u for u, v in g.arcs if v == leaf]
    if len(parents) != 1:
        raise ValueError("new port leaf has wrong parent count")
    w = parents[0]
    incoming = [u for u, v in g.arcs if v == w]
    outgoing = [v for u, v in g.arcs if u == w and v != leaf]
    if len(incoming) != 1 or len(outgoing) != 1:
        raise ValueError("new port parent is not a suppressible insertion vertex")
    u, v = incoming[0], outgoing[0]
    arcs = [e for e in g.arcs if w not in e and leaf not in e]
    if (u, v) in arcs:
        raise ValueError("deletion creates a parallel arc")
    arcs.append((u, v))
    del labels[leaf]
    parent = RootedGraph(g.root, tuple(sorted(arcs)), tuple(sorted(labels.items())))
    return parent, {"deleted_leaf": leaf, "suppressed_vertex": w, "recovered_arc": [u, v]}


def rooted_equal(a, b):
    return a == b


def standard_mixed(g):
    """Suppress exactly the root and retain arrowheads entering reticulations."""
    rets = set(g.reticulations)
    children = [v for u, v in g.arcs if u == g.root]
    if len(children) != 2:
        raise ValueError("root must have two children")
    edges = []
    root_heads = {}
    for u, v in g.arcs:
        if u == g.root:
            root_heads[v] = int(v in rets)
            continue
        # endpoint tuple: u,v,head-at-u,head-at-v
        edges.append((u, v, 0, int(v in rets)))
    a, b = children
    edges.append((min(a, b), max(a, b), root_heads.get(a, 0) if a < b else root_heads.get(b, 0),
                  root_heads.get(b, 0) if a < b else root_heads.get(a, 0)))
    norm = []
    for u, v, hu, hv in edges:
        if u <= v:
            norm.append((u, v, hu, hv))
        else:
            norm.append((v, u, hv, hu))
    if len(set((u, v) for u, v, _, _ in norm)) != len(norm):
        raise ValueError("standard root suppression creates parallel edge")
    return {"vertices": sorted(g.vertices - {g.root}), "labels": dict(g.labels), "edges": tuple(sorted(norm))}


def admissible_rootings(g):
    """Enumerate all binary acyclic rootings of the locked standard mixed graph.

    This is deliberately a small exact backtracker, not a graph-catalogue
    lookup.  Each mixed edge is tried as the root site.  Reticulation arrows
    remain fixed and all undirected edges are oriented subject to the binary
    indegree requirements.
    """
    m = standard_mixed(g)
    vertices = set(m["vertices"])
    labels = set(m["labels"])
    headdeg = Counter()
    for u, v, hu, hv in m["edges"]:
        headdeg[u] += hu
        headdeg[v] += hv
    retics = {v for v in vertices if headdeg[v] == 2}
    results = []
    for site_index, site in enumerate(m["edges"]):
        root = max(vertices) + 1
        root_arcs = [(root, site[0]), (root, site[1])]
        fixed = []
        free = []
        for i, (u, v, hu, hv) in enumerate(m["edges"]):
            if i == site_index:
                continue
            if hu and hv:
                fixed = None
                break
            if hu:
                fixed.append((v, u))
            elif hv:
                fixed.append((u, v))
            else:
                free.append((u, v))
        if fixed is None:
            continue
        required = {v: (2 if v in retics else 1) for v in vertices}
        current = Counter(v for _, v in root_arcs + fixed)
        remaining = Counter()
        for u, v in free:
            remaining[u] += 1
            remaining[v] += 1
        oriented = []

        def rec(i):
            if i == len(free):
                if any(current[v] != required[v] for v in vertices):
                    return
                arcs = tuple(sorted(root_arcs + fixed + oriented))
                rg = RootedGraph(root, arcs, tuple(sorted(m["labels"].items())))
                if not validate_rooted(rg, require_tree_child=False) and root_is_lsa(rg):
                    results.append(rg)
                return
            u, v = free[i]
            remaining[u] -= 1
            remaining[v] -= 1
            # u -> v
            if current[v] < required[v]:
                current[v] += 1
                if all(current[x] <= required[x] <= current[x] + remaining[x] for x in (u, v)):
                    oriented.append((u, v))
                    rec(i + 1)
                    oriented.pop()
                current[v] -= 1
            # v -> u
            if current[u] < required[u]:
                current[u] += 1
                if all(current[x] <= required[x] <= current[x] + remaining[x] for x in (u, v)):
                    oriented.append((v, u))
                    rec(i + 1)
                    oriented.pop()
                current[u] -= 1
            remaining[u] += 1
            remaining[v] += 1

        if all(current[v] <= required[v] <= current[v] + remaining[v] for v in vertices):
            rec(0)
    # Exact rooted graph deduplication.
    uniq = {}
    for r in results:
        uniq[digest(r.to_json())] = r
    return tuple(uniq.values())


def standard_strong(g):
    roots = admissible_rootings(g)
    return bool(roots) and all(not validate_rooted(r, require_tree_child=True) for r in roots), len(roots)


def _vertex_colors(m, ignore_triangle_heads=False):
    labels = m["labels"]
    # Reticulation color comes from arrowhead indegree; for T maps it is ignored
    # on the triangle but labels and degrees remain fixed.
    headdeg = Counter()
    deg = Counter()
    for u, v, hu, hv in m["edges"]:
        deg[u] += 1
        deg[v] += 1
        headdeg[u] += hu
        headdeg[v] += hv
    return {v: (labels.get(v), deg[v], None if ignore_triangle_heads else headdeg[v]) for v in m["vertices"]}


def triangles(m):
    adj = defaultdict(set)
    for u, v, _, _ in m["edges"]:
        adj[u].add(v)
        adj[v].add(u)
    out = set()
    for a in m["vertices"]:
        for b in adj[a]:
            for c in adj[a] & adj[b]:
                out.add(tuple(sorted((a, b, c))))
    return tuple(sorted(out))


def _edge_attr(m):
    return {(u, v): (hu, hv) for u, v, hu, hv in m["edges"]}


def mixed_maps(source, target, allow_T=False):
    """Exact labelled mixed-graph maps; in T mode ignore only triangle heads."""
    s, t = standard_mixed(source), standard_mixed(target)
    if len(s["vertices"]) != len(t["vertices"]) or len(s["edges"]) != len(t["edges"]):
        return []
    st = triangles(s)
    tt = triangles(t)
    if allow_T and (len(st) != 1 or len(tt) != 1):
        return []
    sc = _vertex_colors(s, ignore_triangle_heads=allow_T)
    tc = _vertex_colors(t, ignore_triangle_heads=allow_T)
    classes_s, classes_t = defaultdict(list), defaultdict(list)
    for v, c in sc.items():
        classes_s[c].append(v)
    for v, c in tc.items():
        classes_t[c].append(v)
    if {c: len(vs) for c, vs in classes_s.items()} != {c: len(vs) for c, vs in classes_t.items()}:
        return []
    sattr, tattr = _edge_attr(s), _edge_attr(t)
    sedges = set(sattr)
    tedges = set(tattr)
    stri = set(st[0]) if allow_T else set()
    ttri = set(tt[0]) if allow_T else set()
    class_items = sorted(classes_s, key=repr)
    choices = []
    for c in class_items:
        ss = sorted(classes_s[c])
        ts = sorted(classes_t[c])
        choices.append([(ss, perm) for perm in itertools.permutations(ts)])
    maps = []
    for pick in itertools.product(*choices):
        mp = {}
        for ss, perm in pick:
            mp.update(zip(ss, perm))
        ok = True
        for u, v in sedges:
            a, b = sorted((mp[u], mp[v]))
            if (a, b) not in tedges:
                ok = False
                break
            hu, hv = sattr[(u, v)]
            if mp[u] > mp[v]:
                hu, hv = hv, hu
            if allow_T and u in stri and v in stri:
                if a not in ttri or b not in ttri:
                    ok = False
                    break
            elif (hu, hv) != tattr[(a, b)]:
                ok = False
                break
        if ok:
            maps.append(mp)
    return maps


def classify_topology(source, target, parent_transport=None):
    literal = mixed_maps(source, target, allow_T=False)
    t_maps = mixed_maps(source, target, allow_T=True)
    candidates = [("labelled_isomorphism", m) for m in literal]
    if not candidates:
        candidates = [("ordinary_T", m) for m in t_maps]
    if parent_transport is not None:
        parent_transport = {int(a): int(b) for a, b in parent_transport}
        candidates = [
            (c, m) for c, m in candidates
            if all(m.get(v) == w for v, w in parent_transport.items())
        ]
    return candidates


def switching_data(g):
    labels = g.label_map
    incoming = {r: tuple(sorted((u, r) for u, v in g.arcs if v == r)) for r in g.reticulations}
    children_all = defaultdict(list)
    for e in g.arcs:
        children_all[e[0]].append(e[1])
    out = []
    for bits in itertools.product((0, 1), repeat=len(incoming)):
        chosen = dict(zip(sorted(incoming), bits))
        keep = set(g.arcs)
        weight = ONE
        for r in sorted(incoming):
            inc = incoming[r]
            bit = chosen[r]
            keep.remove(inc[1 - bit])
            lam = f"l:{r}"
            weight = pmul(weight, pvar(lam) if bit == 0 else pone_minus(lam))
        children = defaultdict(list)
        for u, v in keep:
            children[u].append(v)
        order, seen = [], set()

        def dfs(v):
            if v in seen:
                return
            seen.add(v)
            for w in children[v]:
                dfs(w)
            order.append(v)

        dfs(g.root)
        desc = {}
        for v in order:
            s = {labels[v]} if v in labels else set()
            for w in children[v]:
                s |= desc[w]
            desc[v] = frozenset(s)
        out.append((keep, {e: desc[e[1]] for e in keep}, weight))
    return out


def _gl22_maps():
    maps = []
    for p in itertools.permutations((1, 2, 3)):
        mp = {0: 0, 1: p[0], 2: p[1], 3: p[2]}
        if all(mp[a ^ b] == (mp[a] ^ mp[b]) for a in range(4) for b in range(4)):
            maps.append(mp)
    return maps


GL22 = _gl22_maps()


def jc_reps(k):
    return tuple(sorted({
        min(tuple(mp[x] for x in a) for mp in GL22)
        for a in itertools.product(range(4), repeat=k)
        if __import__("functools").reduce(int.__xor__, a, 0) == 0
    }))


JC4_REPS = jc_reps(4)


def orbit_tensor(g, selected_labels):
    if len(selected_labels) < 2 or len(set(selected_labels)) != len(selected_labels):
        raise ValueError("selected labels must be distinct")
    if not set(selected_labels) <= set(g.label_map.values()):
        raise ValueError("selected label absent from graph")
    switchings = switching_data(g)
    ans = []
    for assignment in jc_reps(len(selected_labels)):
        chars = dict(zip(selected_labels, assignment))
        coord = {}
        for keep, desc, weight in switchings:
            monomial = ONE
            for e in keep:
                value = 0
                for label in desc[e]:
                    value ^= chars.get(label, 0)
                if value:
                    monomial = pmul(monomial, pvar(f"x:{e[0]}>{e[1]}"))
            coord = padd(coord, pmul(weight, monomial))
        ans.append(coord)
    return tuple(ans)


def quartet_tensor(g, quartet):
    if len(quartet) != 4:
        raise ValueError("quartet must contain four labels")
    return orbit_tensor(g, quartet)


def invariant_pullback(tensor, invariant):
    out = {}
    for term in invariant["terms"]:
        z = {(): int(term["coefficient"])}
        for i, power in term["coordinate_powers"]:
            z = pmul(z, ppow(tensor[int(i)], int(power)))
        out = padd(out, z)
    return out


def verify_strict_factor(poly, cert):
    z = {(): int(cert["constant"])}
    for factor in cert.get("factors", []):
        base = pvar(factor["variable"]) if factor["kind"] == "var" else pone_minus(factor["variable"])
        z = pmul(z, ppow(base, int(factor.get("power", 1))))
    return z == poly and cert["constant"] != 0


def graph_variables(g):
    return tuple([f"x:{u}>{v}" for u, v in g.arcs] + [f"l:{r}" for r in g.reticulations])


def all_rank_coordinates(g):
    labels = sorted(g.label_map.values())
    selections = [tuple(labels)] if len(labels) <= 4 else itertools.combinations(labels, 4)
    for selected in selections:
        for i, poly in enumerate(orbit_tensor(g, selected)):
            yield selected, i, poly


def modular_matrix_rank(rows, modulus=PRIME):
    basis = {}
    pivots = []
    for row_id, row in rows:
        row = [x % modulus for x in row]
        while True:
            nz = next((i for i, x in enumerate(row) if x), None)
            if nz is None:
                break
            if nz not in basis:
                inv = pow(row[nz], modulus - 2, modulus)
                row = [(x * inv) % modulus for x in row]
                basis[nz] = row
                pivots.append((row_id, nz))
                break
            q = row[nz]
            br = basis[nz]
            row = [(x - q * y) % modulus for x, y in zip(row, br)]
    return len(basis), pivots


def jacobian_rank_certificate(g, seed=29, modulus=PRIME, structural_upper_bound=None):
    variables = graph_variables(g)
    values = {v: (seed + 17 * i) % modulus for i, v in enumerate(variables)}
    rows = []
    for quartet, i, poly in all_rank_coordinates(g):
        row = [peval(pderiv(poly, v), values, modulus) for v in variables]
        rows.append(((list(quartet), i), row))
    rank, pivots = modular_matrix_rank(rows, modulus)
    upper_bound = structural_upper_bound
    return {
        "modulus": modulus,
        "seed": seed,
        "variables": list(variables),
        "rank": rank,
        "structural_upper_bound": upper_bound,
        "exact": upper_bound is not None and rank == upper_bound,
        "pivots": [[[list(rid[0]), rid[1]], col] for rid, col in pivots],
    }


def relation_payload(record):
    keys = [
        "raw_terminal_id", "restoration_root_id", "parent_path_id", "Q_s", "Q_t",
        "port_matching", "parent_relation_id", "level", "new_label", "source_arc",
        "target_arc",
    ]
    return {k: record.get(k) for k in keys}


def expected_relation_id(record):
    return digest(relation_payload(record))


def base_identity_payload(record):
    return {
        "fixed_full_root_case_id": record.get("fixed_full_root_case_id"),
        "raw_terminal_id": record.get("raw_terminal_id"),
        "parent_path_id": record.get("parent_path_id"),
        "source_rooted_graph_id": record.get("source_graph_id"),
        "target_rooted_graph_id": record.get("target_graph_id"),
        "Q_s": record.get("Q_s"),
        "Q_t": record.get("Q_t"),
        "port_matching": record.get("port_matching"),
    }


def expected_base_relation_id(record):
    return digest(base_identity_payload(record))


def linear_invariant_basis(tensor):
    """Exact rational nullspace among the fifteen orbit coordinates."""
    monomials = sorted(set().union(*(set(p) for p in tensor)))
    # Matrix has monomial rows and coordinate columns.
    A = [[Fraction(tensor[j].get(m, 0)) for j in range(len(tensor))] for m in monomials]
    m, n = len(A), len(A[0])
    pivots, r = [], 0
    for c in range(n):
        z = next((i for i in range(r, m) if A[i][c]), None)
        if z is None:
            continue
        A[r], A[z] = A[z], A[r]
        q = A[r][c]
        A[r] = [x / q for x in A[r]]
        for i in range(m):
            if i != r and A[i][c]:
                q = A[i][c]
                A[i] = [x - q * y for x, y in zip(A[i], A[r])]
        pivots.append(c)
        r += 1
    free = [c for c in range(n) if c not in pivots]
    basis = []
    for f in free:
        v = [Fraction(0) for _ in range(n)]
        v[f] = Fraction(1)
        for rr, c in enumerate(pivots):
            v[c] = -A[rr][f]
        den = 1
        for x in v:
            den = den * x.denominator // __import__("math").gcd(den, x.denominator)
        ints = [int(x * den) for x in v]
        g = 0
        for x in ints:
            g = __import__("math").gcd(g, abs(x))
        if g:
            ints = [x // g for x in ints]
        if next((x for x in ints if x), 1) < 0:
            ints = [-x for x in ints]
        basis.append(ints)
    return basis


def find_linear_separator(source, target, labels):
    common = sorted(set(source.label_map.values()) & set(target.label_map.values()))
    for quartet in itertools.combinations(common, 4):
        st = quartet_tensor(source, quartet)
        tt = quartet_tensor(target, quartet)
        for coeffs in linear_invariant_basis(tt):
            inv = {
                "terms": [
                    {"coefficient": c, "coordinate_powers": [[i, 1]]}
                    for i, c in enumerate(coeffs) if c
                ]
            }
            ps = invariant_pullback(st, inv)
            if ps:
                return quartet, inv, ps, {}
        for coeffs in linear_invariant_basis(st):
            inv = {
                "terms": [
                    {"coefficient": c, "coordinate_powers": [[i, 1]]}
                    for i, c in enumerate(coeffs) if c
                ]
            }
            pt = invariant_pullback(tt, inv)
            if pt:
                return quartet, inv, {}, pt
    return None
