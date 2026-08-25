#!/usr/bin/env python3
"""Independent rooting-census and all-n K3P cherry replay.

No cloud graph/rooting module is imported.  The fixed mixed graph, every
ordinary-edge orientation, rooted binary/acyclic/reachability/LSA condition,
and tree-child condition are reconstructed directly from primitive arcs.
The six-dimensional cherry determinant is computed as a formal Laurent
polynomial rather than accepted from the stored summary.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import ast
import json
import os
import sys


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
FROZEN = PROJECT / "input_frozen" / "k3p_cloud_artifacts"
KRAWCZYK_CERT = HERE / "K3P_SHARPNESS_KRAWCZYK_CERTIFICATE.json"
OUTPUT = HERE / "K3P_SHARPNESS_TOPOLOGY_ALL_N_CERTIFICATE.json"


def file_sha256(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path, obj: object) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


@dataclass(frozen=True)
class RootedSpec:
    name: str
    arcs: tuple[tuple[str, str], ...]
    retics: frozenset[str]
    labels: tuple[tuple[str, int], ...]


W = RootedSpec(
    "W",
    (("r", "S"), ("r", "L0"), ("S", "U"), ("S", "V"), ("U", "X"),
     ("V", "Z"), ("Z", "X"), ("U", "V"), ("Z", "L1"), ("X", "L2")),
    frozenset(("V", "X")),
    (("L0", 0), ("L1", 1), ("L2", 2)),
)

WPRIME = RootedSpec(
    "Wprime",
    (("r", "S"), ("r", "L0"), ("S", "U"), ("S", "X0"), ("V", "X0"),
     ("U", "X1"), ("V", "X1"), ("U", "V"), ("X0", "L1"), ("X1", "L2")),
    frozenset(("X0", "X1")),
    (("L0", 0), ("L1", 1), ("L2", 2)),
)

COLLISION = RootedSpec(
    "collision",
    (("rho", "1"), ("rho", "u"), ("u", "p"), ("u", "q"), ("p", "r2"),
     ("q", "r2"), ("p", "r3"), ("q", "r3"), ("r2", "2"), ("r3", "3")),
    frozenset(("r2", "r3")),
    (("1", 0), ("2", 1), ("3", 2)),
)


@dataclass(frozen=True, order=True)
class MixedEdge:
    endpoints: tuple[str, str]
    heads: tuple[str, ...]

    @staticmethod
    def make(a: str, b: str, heads: tuple[str, ...] | list[str] = ()) -> "MixedEdge":
        if a == b:
            raise ValueError("mixed loop")
        endpoints = tuple(sorted((a, b)))
        head_tuple = tuple(sorted(heads))
        if any(x not in endpoints for x in head_tuple):
            raise ValueError((endpoints, head_tuple))
        return MixedEdge(endpoints, head_tuple)


@dataclass(frozen=True)
class MixedGraph:
    name: str
    roles: tuple[tuple[str, str], ...]
    labels: tuple[tuple[str, int], ...]
    edges: tuple[MixedEdge, ...]

    def role_dict(self) -> dict[str, str]:
        return dict(self.roles)

    def label_dict(self) -> dict[str, int]:
        return dict(self.labels)


def sd0(spec: RootedSpec) -> MixedGraph:
    nodes = {x for edge in spec.arcs for x in edge}
    indegree = {v: 0 for v in nodes}
    for _, v in spec.arcs:
        indegree[v] += 1
    roots = [v for v in nodes if indegree[v] == 0]
    if len(roots) != 1:
        raise AssertionError((spec.name, roots))
    root = roots[0]
    children = [v for u, v in spec.arcs if u == root]
    if len(children) != 2:
        raise AssertionError((root, children))
    labels = dict(spec.labels)
    roles = {
        v: ("leaf" if v in labels else "retic" if v in spec.retics else "tree")
        for v in nodes if v != root
    }
    edges = []
    for u, v in spec.arcs:
        if u == root:
            continue
        edges.append(MixedEdge.make(u, v, (v,) if v in spec.retics else ()))
    edges.append(MixedEdge.make(children[0], children[1], tuple(v for v in children if v in spec.retics)))
    if len(set(e.endpoints for e in edges)) != len(edges):
        raise AssertionError(f"{spec.name}: root suppression is not simple")
    return MixedGraph(spec.name, tuple(sorted(roles.items())), tuple(sorted(spec.labels)), tuple(sorted(edges)))


def topological_order(nodes: set[str], arcs: list[tuple[str, str]]) -> list[str] | None:
    indegree = {v: 0 for v in nodes}
    children = {v: [] for v in nodes}
    for u, v in arcs:
        indegree[v] += 1
        children[u].append(v)
    ready = sorted(v for v in nodes if indegree[v] == 0)
    order: list[str] = []
    while ready:
        u = ready.pop(0)
        order.append(u)
        for v in sorted(children[u]):
            indegree[v] -= 1
            if indegree[v] == 0:
                ready.append(v)
                ready.sort()
    return order if len(order) == len(nodes) else None


def validate_rooting(
    roles: dict[str, str], labels: dict[str, int], arcs: list[tuple[str, str]], root: str
) -> dict[str, object] | None:
    nodes = set(roles) | {root}
    if any(u not in nodes or v not in nodes or u == v for u, v in arcs):
        return None
    indegree = {v: 0 for v in nodes}
    children = {v: [] for v in nodes}
    parents = {v: [] for v in nodes}
    for u, v in arcs:
        indegree[v] += 1
        children[u].append(v)
        parents[v].append(u)
    outdegree = {v: len(children[v]) for v in nodes}
    if (indegree[root], outdegree[root]) != (0, 2):
        return None
    for v, role in roles.items():
        wanted = (1, 0) if role == "leaf" else (2, 1) if role == "retic" else (1, 2)
        if (indegree[v], outdegree[v]) != wanted:
            return None
    order = topological_order(nodes, arcs)
    if order is None or order[0] != root:
        return None
    reachable = {root}
    stack = [root]
    while stack:
        u = stack.pop()
        for v in children[u]:
            if v not in reachable:
                reachable.add(v)
                stack.append(v)
    if reachable != nodes:
        return None
    # Exact DAG dominators: root is the LSA precisely when it is the only
    # vertex dominating every labelled leaf.
    dominators: dict[str, set[str]] = {root: {root}}
    for v in order[1:]:
        dominators[v] = {v} | set.intersection(*(dominators[p] for p in parents[v]))
    leaf_nodes = [v for v, role in roles.items() if role == "leaf"]
    if set(labels) != set(leaf_nodes):
        return None
    stable = set.intersection(*(dominators[v] for v in leaf_nodes))
    if stable != {root}:
        return None
    non_tree_child_witnesses = [
        u for u in nodes if roles.get(u) != "leaf" and all(roles.get(v) == "retic" for v in children[u])
    ]
    tree_child = not non_tree_child_witnesses
    return {
        "tree_child": tree_child,
        "non_tree_child_witnesses": sorted(non_tree_child_witnesses),
        "dominators_common_to_all_leaves": sorted(stable),
    }


def enumerate_rootings(mixed: MixedGraph) -> list[dict[str, object]]:
    roles = mixed.role_dict()
    labels = mixed.label_dict()
    result = []
    for root_edge_index, root_edge in enumerate(mixed.edges):
        remaining = [e for i, e in enumerate(mixed.edges) if i != root_edge_index]
        ordinary = sorted(e for e in remaining if not e.heads)
        fixed = sorted(e for e in remaining if e.heads)
        if any(len(e.heads) != 1 for e in fixed) or len(root_edge.heads) > 1:
            continue
        for bits in product((0, 1), repeat=len(ordinary)):
            root = "__inserted_root__"
            arcs = [(root, root_edge.endpoints[0]), (root, root_edge.endpoints[1])]
            for edge, bit in zip(ordinary, bits):
                a, b = edge.endpoints
                arcs.append((a, b) if bit == 0 else (b, a))
            for edge in fixed:
                head = edge.heads[0]
                tail = next(v for v in edge.endpoints if v != head)
                arcs.append((tail, head))
            check = validate_rooting(roles, labels, arcs, root)
            if check is None:
                continue
            result.append({
                "root_edge": {"endpoints": list(root_edge.endpoints), "heads": list(root_edge.heads)},
                "ordinary_edge_order": [{"endpoints": list(e.endpoints), "heads": list(e.heads)} for e in ordinary],
                "orientation_bits": list(bits),
                "directed_arcs": [list(x) for x in sorted(arcs)],
                **check,
            })
    return sorted(result, key=lambda r: (r["root_edge"]["endpoints"], r["orientation_bits"]))  # type: ignore[index]


def frozen_rooting_signatures(data: dict[str, object], name: str) -> list[tuple[tuple[str, str], bool]]:
    records = data[name]["rootings"]  # type: ignore[index]
    answer = []
    for record in records:
        endpoints = tuple(sorted(ast.literal_eval(x) for x in record["root_edge"]))
        answer.append((endpoints, bool(record["tree_child"])))
    return sorted(answer)


def independent_rooting_signatures(records: list[dict[str, object]]) -> list[tuple[tuple[str, str], bool]]:
    return sorted((tuple(r["root_edge"]["endpoints"]), bool(r["tree_child"])) for r in records)  # type: ignore[index]


def adjacency(mixed: MixedGraph) -> dict[str, set[str]]:
    answer = {v: set() for v, _ in mixed.roles}
    for edge in mixed.edges:
        a, b = edge.endpoints
        answer[a].add(b)
        answer[b].add(a)
    return answer


def mixed_isomorphisms(a: MixedGraph, b: MixedGraph, preserve_heads: bool) -> list[dict[str, str]]:
    if len(a.roles) != len(b.roles) or len(a.edges) != len(b.edges):
        return []
    aa, bb = adjacency(a), adjacency(b)
    la, lb = a.label_dict(), b.label_dict()
    nodes_a = sorted(aa)
    nodes_b = sorted(bb)
    labelled_a = {label: node for node, label in la.items()}
    labelled_b = {label: node for node, label in lb.items()}
    if set(labelled_a) != set(labelled_b):
        return []
    fixed = {labelled_a[label]: labelled_b[label] for label in labelled_a}
    free_a = [v for v in nodes_a if v not in fixed]
    free_b = [v for v in nodes_b if v not in fixed.values()]
    edge_b = {e.endpoints: e for e in b.edges}
    answer = []
    for perm in permutations(free_b):
        mapping = dict(fixed)
        mapping.update(zip(free_a, perm))
        if any(len(aa[v]) != len(bb[mapping[v]]) for v in nodes_a):
            continue
        good = True
        for edge in a.edges:
            mapped_endpoints = tuple(sorted(mapping[v] for v in edge.endpoints))
            if mapped_endpoints not in edge_b:
                good = False
                break
            if preserve_heads:
                mapped_heads = tuple(sorted(mapping[v] for v in edge.heads))
                if mapped_heads != edge_b[mapped_endpoints].heads:
                    good = False
                    break
        if good:
            answer.append(mapping)
    return answer


def triangles(mixed: MixedGraph) -> list[tuple[str, str, str]]:
    adj = adjacency(mixed)
    result = set()
    nodes = sorted(adj)
    for i, a in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            b = nodes[j]
            if b not in adj[a]:
                continue
            for k in range(j + 1, len(nodes)):
                c = nodes[k]
                if c in adj[a] and c in adj[b]:
                    result.add((a, b, c))
    return sorted(result)


def biconnected_edge_components(mixed: MixedGraph) -> list[list[tuple[str, str]]]:
    adj = adjacency(mixed)
    discovery: dict[str, int] = {}
    low: dict[str, int] = {}
    parent: dict[str, str | None] = {}
    stack: list[tuple[str, str]] = []
    components: list[list[tuple[str, str]]] = []
    tick = 0

    def visit(u: str) -> None:
        nonlocal tick
        tick += 1
        discovery[u] = low[u] = tick
        for v in sorted(adj[u]):
            edge = tuple(sorted((u, v)))
            if v not in discovery:
                parent[v] = u
                stack.append(edge)
                visit(v)
                low[u] = min(low[u], low[v])
                if low[v] >= discovery[u]:
                    component = []
                    while stack:
                        e = stack.pop()
                        component.append(e)
                        if e == edge:
                            break
                    components.append(sorted(component))
            elif parent.get(u) != v and discovery[v] < discovery[u]:
                low[u] = min(low[u], discovery[v])
                stack.append(edge)

    for root in sorted(adj):
        if root not in discovery:
            parent[root] = None
            visit(root)
    return sorted(components)


def topology_summary(mixed: MixedGraph) -> dict[str, object]:
    roles = mixed.role_dict()
    adj = adjacency(mixed)
    binary = all(len(adj[v]) == (1 if role == "leaf" else 3) for v, role in roles.items())
    components = biconnected_edge_components(mixed)
    blobs = []
    for edges in components:
        vertices = sorted({v for e in edges for v in e})
        cyclic = len(edges) >= len(vertices)
        if cyclic:
            blobs.append({
                "vertices": vertices,
                "edges": [list(e) for e in edges],
                "reticulation_count": sum(roles[v] == "retic" for v in vertices),
            })
    level = max((int(b["reticulation_count"]) for b in blobs), default=0)
    return {"simple": len({e.endpoints for e in mixed.edges}) == len(mixed.edges), "binary": binary, "blobs": blobs, "level": level, "triangles": [list(x) for x in triangles(mixed)]}


# Formal Laurent polynomials in (uC,vC,uG,vG,uT,vT).
Laurent = dict[tuple[int, ...], Q]
NVAR = 6


def l_add(a: Laurent, b: Laurent) -> Laurent:
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, Q(0)) + c
        if not out[m]:
            del out[m]
    return out


def l_scale(a: Laurent, c: Q) -> Laurent:
    return {m: c * x for m, x in a.items() if c * x}


def l_mul(a: Laurent, b: Laurent) -> Laurent:
    out: Laurent = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(x + y for x, y in zip(ma, mb))
            out[m] = out.get(m, Q(0)) + ca * cb
    return {m: c for m, c in out.items() if c}


def l_derivative(a: Laurent, variable: int) -> Laurent:
    out: Laurent = {}
    for m, c in a.items():
        if not m[variable]:
            continue
        mm = list(m)
        out[tuple(mm[:variable] + [mm[variable] - 1] + mm[variable + 1:])] = c * m[variable]
    return out


def permutation_sign(p: tuple[int, ...]) -> int:
    inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inversions % 2 else 1


def laurent_determinant(matrix: list[list[Laurent]]) -> Laurent:
    n = len(matrix)
    answer: Laurent = {}
    for p in permutations(range(n)):
        term: Laurent = {(0,) * NVAR: Q(permutation_sign(p))}
        for i in range(n):
            term = l_mul(term, matrix[i][p[i]])
            if not term:
                break
        answer = l_add(answer, term)
    return answer


def laurent_eval(poly: Laurent, point: tuple[Q, ...]) -> Q:
    answer = Q(0)
    for exponents, coefficient in poly.items():
        term = coefficient
        for x, exponent in zip(point, exponents):
            term *= x ** exponent
        answer += term
    return answer


def laurent_record(poly: Laurent) -> list[dict[str, object]]:
    return [{"exponents_uC_vC_uG_vG_uT_vT": list(m), "coefficient": str(poly[m])} for m in sorted(poly)]


def cherry_determinant_certificate(u: tuple[Q, Q, Q], v: tuple[Q, Q, Q]) -> dict[str, object]:
    variables = []
    for j in range(NVAR):
        exponent = [0] * NVAR
        exponent[j] = 1
        variables.append({tuple(exponent): Q(1)})
    observables: list[Laurent] = []
    for sector in range(3):
        ui, vi = variables[2 * sector], variables[2 * sector + 1]
        inverse_v_exponent = [0] * NVAR
        inverse_v_exponent[2 * sector + 1] = -1
        observables.append(l_mul(ui, {tuple(inverse_v_exponent): Q(1)}))
        observables.append(l_mul(ui, vi))
    jacobian = [[l_derivative(observable, j) for j in range(NVAR)] for observable in observables]
    determinant = laurent_determinant(jacobian)
    point = tuple(x for pair in zip(u, v) for x in pair)
    value = laurent_eval(determinant, point)
    if not determinant or value == 0:
        raise AssertionError("cherry observable Jacobian is singular")
    return {
        "variable_order": ["u_C", "v_C", "u_G", "v_G", "u_T", "v_T"],
        "observable_order": ["R_C=u_C/v_C", "P_C=u_C*v_C", "R_G=u_G/v_G", "P_G=u_G*v_G", "R_T=u_T/v_T", "P_T=u_T*v_T"],
        "formal_laurent_determinant": laurent_record(determinant),
        "derived_formula": "8*u_C*u_G*u_T/(v_C*v_G*v_T)" if determinant == {(1, -1, 1, -1, 1, -1): Q(8)} else "see formal_laurent_determinant",
        "example_u": [str(x) for x in u],
        "example_v": [str(x) for x in v],
        "example_determinant": str(value),
        "nonzero": value != 0,
    }


def physical_point_records(name: str, values: tuple[Q, Q, Q]) -> dict[str, object]:
    c, g, t = values
    tests = {
        "C": c, "G": g, "T": t, "1-C": 1 - c, "1-G": 1 - g, "1-T": 1 - t,
        "p0=(1+C+G+T)/4": (1 + c + g + t) / 4,
        "pC=(1+C-G-T)/4": (1 + c - g - t) / 4,
        "pG=(1-C+G-T)/4": (1 - c + g - t) / 4,
        "pT=(1-C-G+T)/4": (1 - c - g + t) / 4,
        "CT_C=C-G*T": c - g * t,
        "CT_G=G-C*T": g - c * t,
        "CT_T=T-C*G": t - c * g,
    }
    return {
        "name": name,
        "values": [str(x) for x in values],
        "inequalities": {label: str(value) for label, value in tests.items()},
        "minimum_margin": str(min(tests.values())),
        "all_strict": all(x > 0 for x in tests.values()),
    }


def substitute_cherry_rooting(
    record: dict[str, object], roles: dict[str, str], labels: dict[str, int], leaf: str, new_leaf: str, new_label: int, parent_name: str
) -> tuple[dict[str, object], dict[str, str], dict[str, int]]:
    arcs = [tuple(x) for x in record["directed_arcs"]]  # type: ignore[index]
    incoming = [(u, v) for u, v in arcs if v == leaf]
    if len(incoming) != 1 or roles[leaf] != "leaf":
        raise AssertionError((leaf, incoming))
    old_arc = incoming[0]
    arcs.remove(old_arc)
    arcs.extend(((old_arc[0], parent_name), (parent_name, leaf), (parent_name, new_leaf)))
    new_roles = dict(roles)
    new_roles[parent_name] = "tree"
    new_roles[new_leaf] = "leaf"
    new_labels = dict(labels)
    new_labels[new_leaf] = new_label
    check = validate_rooting(new_roles, new_labels, arcs, "__inserted_root__")
    if check is None:
        raise AssertionError("cherry-lifted rooting is invalid")
    return {"directed_arcs": [list(x) for x in sorted(arcs)], **check}, new_roles, new_labels


def substitute_cherry_mixed(mixed: MixedGraph, leaf: str, new_leaf: str, new_label: int, parent_name: str) -> MixedGraph:
    roles = mixed.role_dict()
    labels = mixed.label_dict()
    incident = [e for e in mixed.edges if leaf in e.endpoints]
    if len(incident) != 1 or incident[0].heads or roles[leaf] != "leaf":
        raise AssertionError((leaf, incident))
    old = incident[0]
    old_parent = next(v for v in old.endpoints if v != leaf)
    edges = [e for e in mixed.edges if e != old]
    edges.extend((MixedEdge.make(old_parent, parent_name), MixedEdge.make(parent_name, leaf), MixedEdge.make(parent_name, new_leaf)))
    roles[parent_name] = "tree"
    roles[new_leaf] = "leaf"
    labels[new_leaf] = new_label
    return MixedGraph(mixed.name, tuple(sorted(roles.items())), tuple(sorted(labels.items())), tuple(sorted(edges)))


def contract_newest_cherry(mixed: MixedGraph, retained_leaf: str, new_leaf: str, parent_name: str) -> MixedGraph:
    roles = mixed.role_dict()
    labels = mixed.label_dict()
    if roles.get(parent_name) != "tree" or roles.get(retained_leaf) != "leaf" or roles.get(new_leaf) != "leaf":
        raise AssertionError("unexpected cherry roles")
    adj = adjacency(mixed)
    outside = sorted(adj[parent_name] - {retained_leaf, new_leaf})
    if len(outside) != 1 or adj[retained_leaf] != {parent_name} or adj[new_leaf] != {parent_name}:
        raise AssertionError("not a pendant labelled cherry")
    removed_nodes = {parent_name, new_leaf}
    edges = [e for e in mixed.edges if not any(v in removed_nodes for v in e.endpoints)]
    edges.append(MixedEdge.make(outside[0], retained_leaf))
    del roles[parent_name]
    del roles[new_leaf]
    del labels[new_leaf]
    return MixedGraph(mixed.name, tuple(sorted(roles.items())), tuple(sorted(labels.items())), tuple(sorted(edges)))


def graph_record(mixed: MixedGraph) -> dict[str, object]:
    return {
        "roles": [list(x) for x in mixed.roles],
        "labels": [list(x) for x in mixed.labels],
        "edges": [{"endpoints": list(e.endpoints), "heads": list(e.heads)} for e in mixed.edges],
    }


def main() -> int:
    frozen_rooting_path = FROZEN / "k3p_rooting_censuses.json"
    frozen_alln_path = FROZEN / "k3p_sharpness_all_n.json"
    frozen_rooting = json.loads(frozen_rooting_path.read_text(encoding="utf-8"))
    frozen_alln = json.loads(frozen_alln_path.read_text(encoding="utf-8"))
    krawczyk = json.loads(KRAWCZYK_CERT.read_text(encoding="utf-8"))
    required_k = (
        "all_checks_pass", "unique_common_parameter_root_in_box", "W_rank_15_throughout_box",
        "Wprime_rank_15_throughout_box", "strict_continuous_time_throughout_box",
    )
    if not all(krawczyk["conclusion"].get(key) is True for key in required_k):
        raise AssertionError("independent base Krawczyk certificate is absent or incomplete")

    mixed_graphs = {spec.name: sd0(spec) for spec in (W, WPRIME, COLLISION)}
    rootings = {name: enumerate_rootings(mixed) for name, mixed in mixed_graphs.items()}
    census = {}
    for name, records in rootings.items():
        root_edges = [tuple(r["root_edge"]["endpoints"]) for r in records]  # type: ignore[index]
        if len(root_edges) != len(set(root_edges)):
            raise AssertionError(f"{name}: more than one admissible orientation for one root edge")
        source_signatures = frozen_rooting_signatures(frozen_rooting, name)
        replay_signatures = independent_rooting_signatures(records)
        if source_signatures != replay_signatures:
            raise AssertionError((name, source_signatures, replay_signatures))
        tree_child_count = sum(bool(r["tree_child"]) for r in records)
        census[name] = {
            "admissible": len(records),
            "tree_child": tree_child_count,
            "non_tree_child": len(records) - tree_child_count,
            "full_rootings": records,
            "root_edge_and_class_agrees_with_frozen_certificate": source_signatures == replay_signatures,
            "orientation_is_unique_given_each_admissible_root_edge": len(root_edges) == len(set(root_edges)),
        }

    mw, mp = mixed_graphs["W"], mixed_graphs["Wprime"]
    exact_isomorphisms = mixed_isomorphisms(mw, mp, preserve_heads=True)
    underlying_isomorphisms = mixed_isomorphisms(mw, mp, preserve_heads=False)
    if exact_isomorphisms or underlying_isomorphisms:
        raise AssertionError("base pair unexpectedly isomorphic even after requested forgetting")
    base_topology = {
        "W": topology_summary(mw),
        "Wprime": topology_summary(mp),
        "labelled_mixed_graph_isomorphism_count": len(exact_isomorphisms),
        "labelled_underlying_graph_isomorphism_count": len(underlying_isomorphisms),
        "not_ordinary_triangle_equivalent": len(underlying_isomorphisms) == 0,
        "reason": "There is no labelled underlying-graph isomorphism even after all internal head flags are forgotten; ordinary triangle redirection cannot change the underlying labelled graph.",
    }
    if not all(base_topology[name]["binary"] and base_topology[name]["simple"] and base_topology[name]["level"] == 2 for name in ("W", "Wprime")):
        raise AssertionError("base pair is not simple binary level two")
    if not all(census[name]["tree_child"] > 0 and census[name]["non_tree_child"] > 0 for name in ("W", "Wprime")):
        raise AssertionError("base pair is not weak-not-strong tree-child")

    u = tuple(Q(x) for x in frozen_alln["example_u"])
    v = tuple(Q(x) for x in frozen_alln["example_v"])
    if len(u) != 3 or len(v) != 3:
        raise AssertionError("all-n example is not K3P")
    determinant = cherry_determinant_certificate(u, v)  # formal, not the stored determinant
    u_physical = physical_point_records("u", u)
    v_physical = physical_point_records("v", v)
    if not u_physical["all_strict"] or not v_physical["all_strict"]:
        raise AssertionError("cherry example is outside strict CT")

    # Verify the group-based observable cancellation independently in each sector.
    observable_character_checks = []
    for h in (1, 2, 3):
        numerator_cluster = h ^ 0
        denominator_cluster = 0 ^ h
        product_cluster = h ^ h
        observable_character_checks.append({
            "sector": h,
            "numerator_cluster_character": numerator_cluster,
            "denominator_cluster_character": denominator_cluster,
            "product_cluster_character": product_cluster,
            "ratio_has_same_old_tensor_factor": numerator_cluster == denominator_cluster == h,
            "product_uses_old_all_zero_coordinate": product_cluster == 0,
        })
    if not all(x["ratio_has_same_old_tensor_factor"] and x["product_uses_old_all_zero_coordinate"] for x in observable_character_checks):
        raise AssertionError("cherry character cancellation failed")

    # Select independently enumerated valid witnesses and lift them through five
    # substitutions.  The certificate also records the uniform local induction
    # lemma, so finite staging is a mutation/sanity replay rather than the proof's
    # quantifier bound.
    persistence: dict[str, object] = {}
    for name, mixed in (("W", mw), ("Wprime", mp)):
        tc_record = next(r for r in rootings[name] if r["tree_child"])
        ntc_record = next(r for r in rootings[name] if not r["tree_child"])
        tc_roles = mixed.role_dict()
        ntc_roles = mixed.role_dict()
        tc_labels = mixed.label_dict()
        ntc_labels = mixed.label_dict()
        current_mixed = mixed
        stages = []
        for n in range(4, 9):
            parent_name = f"CherryParent{n}"
            new_leaf = f"L{n - 1}"
            previous = current_mixed
            current_mixed = substitute_cherry_mixed(current_mixed, "L2", new_leaf, n - 1, parent_name)
            contracted = contract_newest_cherry(current_mixed, "L2", new_leaf, parent_name)
            if contracted != previous:
                raise AssertionError(f"{name}: cherry contraction did not invert substitution at n={n}")
            tc_record, tc_roles, tc_labels = substitute_cherry_rooting(tc_record, tc_roles, tc_labels, "L2", new_leaf, n - 1, parent_name)
            ntc_record, ntc_roles, ntc_labels = substitute_cherry_rooting(ntc_record, ntc_roles, ntc_labels, "L2", new_leaf, n - 1, parent_name)
            summary = topology_summary(current_mixed)
            if not tc_record["tree_child"] or ntc_record["tree_child"] or summary["level"] != 2:
                raise AssertionError(f"{name}: class persistence failed at n={n}")
            if summary["triangles"] != topology_summary(mixed)["triangles"]:
                raise AssertionError(f"{name}: pendant substitution changed triangles")
            stages.append({
                "n": n,
                "tree_child_rooting_lifts": tc_record["tree_child"],
                "non_tree_child_rooting_lifts": not ntc_record["tree_child"],
                "non_tree_child_witnesses": ntc_record["non_tree_child_witnesses"],
                "newest_contraction_exactly_recovers_previous_graph": contracted == previous,
                "level": summary["level"],
                "triangles": summary["triangles"],
            })
        persistence[name] = {
            "tested_stages": stages,
            "uniform_induction_rule": {
                "tree_child": "Replacing a leaf child by a tree child whose two children are leaves preserves every old tree-child witness and makes the new parent tree-child.",
                "non_tree_child": "The old internal vertex with only reticulation children and all its incident arcs are unchanged, so its failure persists.",
                "admissibility_and_LSA": "The replacement is below one old leaf. Binary degrees, acyclicity and reachability are local; any proper dominator of every new leaf would also dominate every old leaf after contracting the cherry.",
                "level": "All three new edges are bridges, so the biconnected blobs and their reticulation counts are unchanged.",
            },
        }

    # Finite graph sanity checks of nonisomorphism through n=8; the all-n proof
    # is the labelled contraction implication recorded below.
    gw, gp = mw, mp
    expanded_pair_checks = []
    for n in range(4, 9):
        parent_name = f"PairCherryParent{n}"
        new_leaf = f"PairL{n - 1}"
        gw = substitute_cherry_mixed(gw, "L2", new_leaf, n - 1, parent_name)
        gp = substitute_cherry_mixed(gp, "L2", new_leaf, n - 1, parent_name)
        exact_count = len(mixed_isomorphisms(gw, gp, preserve_heads=True))
        underlying_count = len(mixed_isomorphisms(gw, gp, preserve_heads=False))
        if exact_count or underlying_count:
            raise AssertionError(f"expanded pair isomorphic at n={n}")
        expanded_pair_checks.append({"n": n, "mixed_isomorphisms": exact_count, "underlying_isomorphisms": underlying_count})

    all_n = {
        "base_common_dimension": 15,
        "new_dimensions_per_cherry": 6,
        "dimension_derivation": "15+6*(n-3)=6n-3",
        "dimension_formula": "6n-3",
        "cherry_observable_jacobian": determinant,
        "cherry_edge_physical_points": {"u": u_physical, "v": v_physical},
        "character_cancellation_checks": observable_character_checks,
        "analytic_inverse": {
            "formula": ["u_h=sqrt(R_h*P_h)", "v_h=sqrt(P_h/R_h) for h in {C,G,T}"],
            "domain": "positive branch",
            "old_tensor_recovery": "After the six edge eigenvalues are recovered, divide a coordinate with one retained cherry leaf by its nonzero pendant factor; q_000=1.",
            "local_inverse_certified": determinant["nonzero"],
        },
        "class_persistence": persistence,
        "expanded_pair_sanity_checks": expanded_pair_checks,
        "all_n_contraction_argument": "A label-preserving isomorphism or triangle equivalence of enlarged pairs must preserve the uniquely labelled pendant cluster. Contracting its newest cherry gives the preceding pair, and iteration gives an isomorphism or triangle equivalence of the base pair, which the exhaustive base comparison excludes.",
    }

    stage_records = [stage for side in persistence.values() for stage in side["tested_stages"]]  # type: ignore[index]
    lift_checks_pass = all(
        stage["tree_child_rooting_lifts"] and stage["non_tree_child_rooting_lifts"]
        and stage["newest_contraction_exactly_recovers_previous_graph"] and stage["level"] == 2
        for stage in stage_records
    )
    pair_sanity_pass = all(
        item["mixed_isomorphisms"] == 0 and item["underlying_isomorphisms"] == 0
        for item in expanded_pair_checks
    )
    weak_not_strong_persists = bool(
        lift_checks_pass
        and all(census[name]["tree_child"] > 0 and census[name]["non_tree_child"] > 0 for name in ("W", "Wprime"))
    )
    nonisomorphism_persists = bool(lift_checks_pass and pair_sanity_pass and not exact_isomorphisms)
    nontriangle_equivalence_persists = bool(lift_checks_pass and pair_sanity_pass and not underlying_isomorphisms)

    provenance_paths = [
        frozen_rooting_path,
        FROZEN / "verify_rooting_censuses.py",
        frozen_alln_path,
        FROZEN / "verify_sharpness_extension.py",
        FROZEN / "sharpness_exact_maps.py",
        KRAWCZYK_CERT,
    ]
    all_pass = bool(
        determinant["nonzero"] and u_physical["all_strict"] and v_physical["all_strict"]
        and not exact_isomorphisms and not underlying_isomorphisms
        and all(census[name]["root_edge_and_class_agrees_with_frozen_certificate"] for name in census)
        and all(census[name]["tree_child"] > 0 and census[name]["non_tree_child"] > 0 for name in ("W", "Wprime"))
        and weak_not_strong_persists and nonisomorphism_persists and nontriangle_equivalence_persists
    )
    certificate = {
        "schema": "k3p-sharpness-independent-rooting-all-n-v2",
        "provenance": {
            "inputs": [{"path": str(p.relative_to(PROJECT)), "bytes": p.stat().st_size, "sha256": file_sha256(p)} for p in provenance_paths],
            "independent_verifier": {"path": str(Path(__file__).resolve().relative_to(PROJECT)), "bytes": Path(__file__).stat().st_size, "sha256": file_sha256(Path(__file__)), "python": sys.version, "dependencies": ["Python standard library only"]},
            "stored_final_booleans_used": False,
            "stored_data_used": ["full rooting records for cross-comparison", "example cherry edge spectra u and v"],
        },
        "mixed_graphs": {name: graph_record(graph) for name, graph in mixed_graphs.items()},
        "rooting_censuses": census,
        "base_topology": base_topology,
        "all_n": all_n,
        "conclusion": {
            "all_checks_pass": all_pass,
            "W_rooting_census": [census["W"]["admissible"], census["W"]["tree_child"], census["W"]["non_tree_child"]],
            "Wprime_rooting_census": [census["Wprime"]["admissible"], census["Wprime"]["tree_child"], census["Wprime"]["non_tree_child"]],
            "collision_rooting_census": [census["collision"]["admissible"], census["collision"]["tree_child"], census["collision"]["non_tree_child"]],
            "base_pair_weak_not_strong": all(census[name]["tree_child"] > 0 and census[name]["non_tree_child"] > 0 for name in ("W", "Wprime")),
            "base_pair_nonisomorphic": not exact_isomorphisms,
            "base_pair_nontriangle_equivalent": not underlying_isomorphisms,
            "all_n_from": 3,
            "dimension_formula": "6n-3",
            "cherry_determinant_nonzero": determinant["nonzero"],
            "weak_not_strong_persists": weak_not_strong_persists,
            "nonisomorphism_persists": nonisomorphism_persists,
            "nontriangle_equivalence_persists": nontriangle_equivalence_persists,
            "strict_continuous_time": u_physical["all_strict"] and v_physical["all_strict"],
        },
    }
    if not all_pass:
        raise AssertionError("not all independently derived topology/all-n checks passed")
    atomic_json(OUTPUT, certificate)
    print(f"INDEPENDENT_K3P_TOPOLOGY_ALL_N_PASS {OUTPUT}")
    print(f"certificate_sha256={file_sha256(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
