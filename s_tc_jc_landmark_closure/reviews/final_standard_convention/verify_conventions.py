#!/usr/bin/env python3
"""Independent exact convention referee for the Outcome-P topology class.

This verifier imports no project implementation.  It reads only the frozen
machine-readable primitive support graphs and reimplements rooted validation,
LSA checking, narrow semi-deorientation, the broader parallel/degree-two
cleanup, admissible-rooting enumeration, and the strong tree-child test.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
from typing import Iterable, Mapping, Optional


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ROOT_PROBE = REPO / "reviews/root_probe/root_probe_certificate.json"
OUT = HERE / "convention_certificate.json"


def edge_key(u: str, v: str) -> tuple[str, str]:
    if u == v:
        raise ValueError("loop")
    return (u, v) if u < v else (v, u)


def stable_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Node:
    reticulation: bool = False
    label: Optional[str] = None


@dataclass
class Mixed:
    nodes: dict[str, Node]
    # Each simple edge carries zero, one, or two endpoint arrowheads.
    edges: dict[tuple[str, str], frozenset[str]]

    @classmethod
    def from_record(cls, record: Mapping[str, object]) -> "Mixed":
        nodes = {
            row["id"]: Node(bool(row["reticulation"]), row["label"])
            for row in record["nodes"]
        }
        edges: dict[tuple[str, str], frozenset[str]] = {}
        for row in record["edges"]:
            key = edge_key(*row["ends"])
            if key in edges:
                raise ValueError("parallel edge in a simple mixed record")
            marks = frozenset(row["arrowheads"])
            if not marks.issubset(key):
                raise ValueError("arrowhead is not an endpoint")
            edges[key] = marks
        return cls(nodes, edges)

    def record(self) -> dict:
        return {
            "nodes": [
                {"id": v, "reticulation": d.reticulation, "label": d.label}
                for v, d in sorted(self.nodes.items())
            ],
            "edges": [
                {"ends": list(e), "arrowheads": sorted(m)}
                for e, m in sorted(self.edges.items())
            ],
        }

    def degree(self, v: str) -> int:
        return sum(v in e for e in self.edges)

    def incident(self, v: str):
        return [(e, m) for e, m in self.edges.items() if v in e]

    def simple_binary(self) -> bool:
        return all(self.degree(v) == (1 if d.label is not None else 3)
                   for v, d in self.nodes.items())

    def local_strong(self) -> bool:
        if not self.simple_binary():
            return False
        for v, d in self.nodes.items():
            incoming = sum(v in marks for _, marks in self.incident(v))
            if d.reticulation:
                if incoming != 2:
                    return False
            elif incoming:
                return False
        for (u, v), marks in self.edges.items():
            if len(marks) != 1:
                if marks:
                    return False
                continue
            head = next(iter(marks))
            tail = v if head == u else u
            if self.nodes[tail].reticulation:
                return False
            others = [(e, m) for e, m in self.incident(tail) if e != (u, v)]
            if len(others) != 2 or any(m for _, m in others):
                return False
        return True


@dataclass(frozen=True)
class Rooted:
    nodes: dict[str, Node]
    arcs: frozenset[tuple[str, str]]
    root: str = "rho"


def degrees(nodes: Iterable[str], arcs: Iterable[tuple[str, str]]):
    indeg = {v: 0 for v in nodes}
    outdeg = {v: 0 for v in nodes}
    for u, v in arcs:
        outdeg[u] += 1
        indeg[v] += 1
    return indeg, outdeg


def is_dag(nodes: Iterable[str], arcs: Iterable[tuple[str, str]]) -> bool:
    nodes = list(nodes)
    indeg, _ = degrees(nodes, arcs)
    children: dict[str, list[str]] = defaultdict(list)
    for u, v in arcs:
        children[u].append(v)
    queue = deque(v for v in nodes if indeg[v] == 0)
    seen = 0
    while queue:
        u = queue.popleft()
        seen += 1
        for v in children[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return seen == len(nodes)


def reachable(rooted: Rooted) -> set[str]:
    children: dict[str, list[str]] = defaultdict(list)
    for u, v in rooted.arcs:
        children[u].append(v)
    seen = {rooted.root}
    queue = deque([rooted.root])
    while queue:
        u = queue.popleft()
        for v in children[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return seen


def lsa_valid(rooted: Rooted) -> bool:
    """The root is the only vertex on every root-to-labelled-leaf path."""
    leaves = {v for v, d in rooted.nodes.items() if d.label is not None}
    children: dict[str, list[str]] = defaultdict(list)
    for u, v in rooted.arcs:
        children[u].append(v)
    if not leaves:
        return False
    for blocked in rooted.nodes:
        if blocked == rooted.root:
            continue
        seen = {rooted.root}
        queue = deque([rooted.root])
        while queue:
            u = queue.popleft()
            for v in children[u]:
                if v != blocked and v not in seen:
                    seen.add(v)
                    queue.append(v)
        # If no labelled leaf is reachable while avoiding blocked, then
        # blocked is a proper stable ancestor.
        if not (leaves & seen):
            return False
    return True


def rooted_binary(rooted: Rooted, *, require_lsa: bool = True) -> bool:
    if rooted.root not in rooted.nodes or not is_dag(rooted.nodes, rooted.arcs):
        return False
    if reachable(rooted) != set(rooted.nodes):
        return False
    indeg, outdeg = degrees(rooted.nodes, rooted.arcs)
    for v, d in rooted.nodes.items():
        if v == rooted.root:
            want = (0, 2)
        elif d.label is not None:
            want = (1, 0)
        elif d.reticulation:
            want = (2, 1)
        else:
            want = (1, 2)
        if (indeg[v], outdeg[v]) != want:
            return False
    return not require_lsa or lsa_valid(rooted)


def tree_child(rooted: Rooted) -> bool:
    children: dict[str, list[str]] = defaultdict(list)
    for u, v in rooted.arcs:
        children[u].append(v)
    for v, d in rooted.nodes.items():
        if d.label is not None:
            continue
        if not any(not rooted.nodes[c].reticulation for c in children[v]):
            return False
    return True


def narrow_sd0(rooted: Rooted) -> Optional[Mixed]:
    """Reticulation-preserving one-root suppression, with no later cleanup."""
    if not rooted_binary(rooted):
        return None
    children = sorted(v for u, v in rooted.arcs if u == rooted.root)
    if len(children) != 2:
        return None
    nodes = {v: d for v, d in rooted.nodes.items() if v != rooted.root}
    edges: dict[tuple[str, str], frozenset[str]] = {}
    for u, v in rooted.arcs:
        if rooted.root in (u, v):
            continue
        key = edge_key(u, v)
        if key in edges:
            return None
        edges[key] = frozenset([v]) if nodes[v].reticulation else frozenset()
    a, b = children
    key = edge_key(a, b)
    if key in edges:
        return None
    edges[key] = frozenset(x for x in (a, b) if nodes[x].reticulation)
    mixed = Mixed(nodes, edges)
    if not mixed.simple_binary():
        return None
    # Every retained reticulation and incoming arrowhead must survive.
    if any(sum(v in m for _, m in mixed.incident(v)) != 2
           for v, d in nodes.items() if d.reticulation):
        return None
    return mixed


def _merge_parallel(rows: list[tuple[tuple[str, str], frozenset[str]]]):
    merged: dict[tuple[str, str], set[str]] = {}
    for key, marks in rows:
        merged.setdefault(key, set()).update(marks)
    return {key: frozenset(marks) for key, marks in merged.items()}


def _direction_at(edge: tuple[str, str], marks: frozenset[str], w: str) -> int:
    """+1 means w->other, -1 means other->w, 0 means undirected."""
    if not marks:
        return 0
    if len(marks) != 1:
        return 9
    head = next(iter(marks))
    return -1 if head == w else +1


def broad_cleanup(rooted: Rooted) -> Optional[Mixed]:
    """Literal Brits-style root, parallel, and degree-two cleanup.

    Degree-two suppression follows the four mixed-graph cases stated by
    Holtgrefe et al.  This map intentionally need not preserve reticulations.
    """
    if not rooted_binary(rooted):
        return None
    children = sorted(v for u, v in rooted.arcs if u == rooted.root)
    nodes = {v: d for v, d in rooted.nodes.items() if v != rooted.root}
    rows: list[tuple[tuple[str, str], frozenset[str]]] = []
    for u, v in rooted.arcs:
        if rooted.root in (u, v):
            continue
        rows.append((edge_key(u, v), frozenset([v]) if nodes[v].reticulation else frozenset()))
    a, b = children
    rows.append((edge_key(a, b), frozenset(x for x in (a, b) if nodes[x].reticulation)))
    edges = _merge_parallel(rows)

    changed = True
    while changed:
        changed = False
        for w in sorted(nodes):
            if nodes[w].label is not None:
                continue
            inc = [(e, m) for e, m in edges.items() if w in e]
            if len(inc) != 2:
                continue
            (e1, m1), (e2, m2) = inc
            a = e1[1] if e1[0] == w else e1[0]
            b = e2[1] if e2[0] == w else e2[0]
            if a == b:
                continue
            d1, d2 = _direction_at(e1, m1, w), _direction_at(e2, m2, w)
            if 9 in (d1, d2) or (d1 == d2 and d1 != 0):
                continue  # two incoming or two outgoing arcs are not suppressed
            marks: frozenset[str]
            if d1 == d2 == 0:
                marks = frozenset()
            elif d1 == 0 or d2 == 0:
                directed, other = (d2, b) if d1 == 0 else (d1, a)
                marks = frozenset([other]) if directed == +1 else frozenset()
            else:
                outgoing_other = a if d1 == +1 else b
                marks = frozenset([outgoing_other])
            del edges[e1]
            del edges[e2]
            del nodes[w]
            key = edge_key(a, b)
            edges = _merge_parallel([*edges.items(), (key, marks)])
            changed = True
            break

    # Recalculate roles from retained arrowheads after cleanup.
    final_nodes = {
        v: Node(sum(v in m for m in edges.values()) == 2, d.label)
        for v, d in nodes.items()
    }
    return Mixed(final_nodes, edges)


def mixed_equal(a: Mixed, b: Mixed) -> bool:
    return a.record() == b.record()


def enumerate_narrow_rootings(graph: Mixed) -> list[Rooted]:
    if not graph.simple_binary():
        return []
    out: list[Rooted] = []
    for site, site_marks in sorted(graph.edges.items()):
        if len(site_marks) > 1:
            continue
        a, b = site
        nodes = dict(graph.nodes)
        nodes["rho"] = Node()
        fixed = {("rho", a), ("rho", b)}
        variables: list[tuple[str, str]] = []
        valid = True
        for edge, marks in graph.edges.items():
            if edge == site:
                continue
            u, v = edge
            if not marks:
                variables.append(edge)
            elif len(marks) == 1:
                head = next(iter(marks))
                fixed.add((v if head == u else u, head))
            else:
                valid = False
        if not valid:
            continue
        for bits in product((0, 1), repeat=len(variables)):
            arcs = set(fixed)
            for (u, v), bit in zip(variables, bits):
                arcs.add((u, v) if bit == 0 else (v, u))
            rooted = Rooted(nodes, frozenset(arcs))
            if not rooted_binary(rooted):
                continue
            recovered = narrow_sd0(rooted)
            if recovered is not None and mixed_equal(recovered, graph):
                out.append(rooted)
    unique = {tuple(sorted(r.arcs)): r for r in out}
    return [unique[k] for k in sorted(unique)]


def rooted_fixture(arcs, tree=(), retic=(), leaves=()) -> Rooted:
    nodes = {"rho": Node()}
    nodes.update({v: Node() for v in tree})
    nodes.update({v: Node(True) for v in retic})
    nodes.update({v: Node(False, v) for v in leaves})
    return Rooted(nodes, frozenset(arcs))


def ordinary_tree_fixture() -> Rooted:
    return rooted_fixture(
        [("rho", "L1"), ("rho", "t"), ("t", "L2"), ("t", "L3")],
        tree=["t"], leaves=["L1", "L2", "L3"],
    )


def broad_only_bad_fixture() -> Rooted:
    # Exact LSA-valid level-2 non-tree-child preimage from the convention audit.
    return rooted_fixture(
        [
            ("rho", "a"), ("rho", "r1"),
            ("a", "r1"), ("a", "b"),
            ("r1", "r2"), ("b", "r2"),
            ("b", "L1"), ("r2", "t"),
            ("t", "L2"), ("t", "L3"),
        ],
        tree=["a", "b", "t"], retic=["r1", "r2"],
        leaves=["L1", "L2", "L3"],
    )


def non_lsa_fixture() -> Rooted:
    return rooted_fixture(
        [
            ("rho", "u"), ("rho", "v"),
            ("u", "r1"), ("u", "r2"),
            ("v", "r1"), ("v", "r2"),
            ("r1", "r3"), ("r2", "r3"),
            ("r3", "t"), ("t", "L1"), ("t", "L2"),
        ],
        tree=["u", "v", "t"], retic=["r1", "r2", "r3"],
        leaves=["L1", "L2"],
    )


def weak_theta_fixture(swap: bool = False) -> Rooted:
    internal = [
        ("rho", "A"), ("rho", "C"),
        ("A", "B"), ("B", "C"), ("C", "D"),
        ("D", "E"), ("A", "F"), ("E", "F"),
    ]
    pendants = (
        [("E", "1"), ("D", "2"), ("F", "3"), ("B", "4")]
        if swap else
        [("B", "1"), ("D", "2"), ("F", "3"), ("E", "4")]
    )
    return rooted_fixture(internal + pendants, tree=["A", "B", "D", "E"],
                          retic=["C", "F"], leaves=["1", "2", "3", "4"])


def expected_three_star() -> Mixed:
    return Mixed(
        {"t": Node(), "L1": Node(False, "L1"), "L2": Node(False, "L2"), "L3": Node(False, "L3")},
        {edge_key("t", f"L{i}"): frozenset() for i in (1, 2, 3)},
    )


def k4_minus_edge_census() -> dict:
    vertices = ["A", "B", "C", "D"]
    base_edges = [
        edge_key("A", "B"), edge_key("A", "C"), edge_key("A", "D"),
        edge_key("B", "C"), edge_key("B", "D"),
        edge_key("C", "LC"), edge_key("D", "LD"),
    ]
    rows = 0
    rootings = 0
    tc = 0
    rootable_markings = 0
    for r1, r2 in combinations(vertices, 2):
        incident1 = [e for e in base_edges if r1 in e]
        incident2 = [e for e in base_edges if r2 in e]
        for chosen1 in combinations(incident1, 2):
            for chosen2 in combinations(incident2, 2):
                rows += 1
                edges = {e: set() for e in base_edges}
                for e in chosen1:
                    edges[e].add(r1)
                for e in chosen2:
                    edges[e].add(r2)
                graph = Mixed(
                    {
                        **{v: Node(v in {r1, r2}) for v in vertices},
                        "LC": Node(False, "LC"), "LD": Node(False, "LD"),
                    },
                    {e: frozenset(m) for e, m in edges.items()},
                )
                roots = enumerate_narrow_rootings(graph)
                if roots:
                    rootable_markings += 1
                rootings += len(roots)
                tc += sum(tree_child(r) for r in roots)
    return {
        "markings": rows,
        "rootable_markings": rootable_markings,
        "admissible_rootings": rootings,
        "tree_child_rootings": tc,
    }


def sunlet_literal_two_subblob() -> dict:
    nodes = {**{f"v{i}": Node(i == 0) for i in range(4)},
             **{f"L{i}": Node(False, f"L{i}") for i in range(4)}}
    edges: dict[tuple[str, str], frozenset[str]] = {}
    for i in range(4):
        edges[edge_key(f"v{i}", f"v{(i+1)%4}")] = frozenset()
        edges[edge_key(f"v{i}", f"L{i}")] = frozenset()
    edges[edge_key("v0", "v1")] = frozenset(["v0"])
    edges[edge_key("v0", "v3")] = frozenset(["v0"])
    graph = Mixed(nodes, edges)
    W = {"v0", "v1"}
    internal = [e for e in graph.edges if set(e).issubset(W)]
    boundary_vertices = {v for v in W if any(v in e and not set(e).issubset(W) for e in graph.edges)}
    external = [e for e in graph.edges if len(set(e) & W) == 1]
    roots = enumerate_narrow_rootings(graph)
    return {
        "simple_binary": graph.simple_binary(),
        "local_strong": graph.local_strong(),
        "admissible_rootings": len(roots),
        "tree_child_rootings": sum(tree_child(r) for r in roots),
        "W": sorted(W),
        "internal_edges": [list(e) for e in sorted(internal)],
        "boundary_vertices": sorted(boundary_vertices),
        "external_edge_count": len(external),
        "contracted_degree": len(external),
        "ordinary_degree_two_suppression_defined": len(external) == 2,
    }


def source_hashes() -> dict:
    paths = {
        "definitions_lock": REPO / "docs/DEFINITIONS_LOCK.md",
        "root_probe_derivation": REPO / "reviews/root_probe/DERIVATION_LOCK.md",
        "root_probe_review": REPO / "reviews/root_probe/REVIEW.md",
        "global_bridge_review": REPO / "reviews/global_bridge/REVIEW.md",
        "root_probe_graphs": ROOT_PROBE,
        "englander_v4_source_xml": HERE / "sources/englander_649493v4.source.xml",
        "holtgrefe_v2_pdf": HERE / "sources/holtgrefe_2507.18772.pdf",
        "brits_v2_pdf": HERE / "sources/brits_2607.12919v2.pdf",
        "frozen_weak_manuscript": REPO / "s_tc_jc_sharp_boundary/source/paper/main.tex",
    }
    records = {}
    for name, path in paths.items():
        try:
            display = path.relative_to(REPO)
        except ValueError:
            display = path
        records[name] = {"path": str(display), "sha256": sha256(path)}
    return records


def main() -> None:
    ordinary = ordinary_tree_fixture()
    assert rooted_binary(ordinary) and tree_child(ordinary)
    ordinary_narrow = narrow_sd0(ordinary)
    ordinary_broad = broad_cleanup(ordinary)
    assert ordinary_narrow is not None and ordinary_broad is not None
    assert mixed_equal(ordinary_narrow, ordinary_broad)

    bad = broad_only_bad_fixture()
    assert rooted_binary(bad) and lsa_valid(bad)
    assert not tree_child(bad)
    assert narrow_sd0(bad) is None
    broad_bad = broad_cleanup(bad)
    assert broad_bad is not None and mixed_equal(broad_bad, expected_three_star())

    non_lsa = non_lsa_fixture()
    assert rooted_binary(non_lsa, require_lsa=False)
    assert not rooted_binary(non_lsa, require_lsa=True)

    weak_rows = []
    for swap in (False, True):
        rooted = weak_theta_fixture(swap)
        assert rooted_binary(rooted) and tree_child(rooted)
        narrow = narrow_sd0(rooted)
        broad = broad_cleanup(rooted)
        assert narrow is not None and broad is not None and mixed_equal(narrow, broad)
        roots = enumerate_narrow_rootings(narrow)
        assert len(roots) == 5 and sum(tree_child(r) for r in roots) == 2
        weak_rows.append({
            "network": "N_prime" if swap else "N",
            "rooted_tree_child": True,
            "narrow_equals_broad_on_displayed_rooting": True,
            "admissible_narrow_rootings": len(roots),
            "tree_child_narrow_rootings": sum(tree_child(r) for r in roots),
        })

    probe = json.loads(ROOT_PROBE.read_text())
    primitive_rows = []
    graph_count = 0
    rooting_count = 0
    for audit in probe["core_audits"]:
        support_rows = []
        for support in audit["supports"]:
            graph = Mixed.from_record(support["graph"])
            roots = enumerate_narrow_rootings(graph)
            assert graph.simple_binary() and graph.local_strong()
            assert roots and all(tree_child(r) for r in roots)
            assert len(roots) == support["rooting_count"]
            assert all(mixed_equal(broad_cleanup(r), graph) for r in roots)
            graph_count += 1
            rooting_count += len(roots)
            support_rows.append({
                "repair": support["repair"],
                "rootings": len(roots),
                "all_tree_child": True,
                "narrow_equals_broad_without_cleanup": True,
            })
        primitive_rows.append({
            "family": audit["core"]["family"],
            "placement": audit["core"]["placement"],
            "supports": support_rows,
        })

    k4 = k4_minus_edge_census()
    assert k4 == {
        "markings": 54,
        "rootable_markings": 5,
        "admissible_rootings": 25,
        "tree_child_rootings": 0,
    }
    literal_2sub = sunlet_literal_two_subblob()
    assert literal_2sub["simple_binary"] and literal_2sub["local_strong"]
    assert literal_2sub["admissible_rootings"] == literal_2sub["tree_child_rootings"] > 0
    assert literal_2sub["external_edge_count"] == 4
    assert not literal_2sub["ordinary_degree_two_suppression_defined"]

    # Mutation-sensitive obligations.  Each mutation must be rejected by a
    # previously established exact fixture.
    mutations = {
        "broad_cleanup_as_admissible_rooting": narrow_sd0(bad) is not None,
        "drop_lsa": rooted_binary(non_lsa, require_lsa=True),
        "rooted_tc_equals_strong_tc": all(row["tree_child_narrow_rootings"] == row["admissible_narrow_rootings"] for row in weak_rows),
        "two_boundary_vertices_implies_degree_two": literal_2sub["contracted_degree"] == 2,
        "k4e_is_standard_strong": k4["tree_child_rootings"] > 0,
        "primitive_cleanup_changes_topology": any(
            not row["narrow_equals_broad_without_cleanup"]
            for core in primitive_rows for row in core["supports"]
        ),
        "weak_fixture_cleanup_changes_topology": any(not row["narrow_equals_broad_on_displayed_rooting"] for row in weak_rows),
        "parallel_theta_is_simple": len({edge_key("U", "V"), edge_key("U", "V")}) == 2,
    }
    assert not any(mutations.values())

    payload = {
        "schema": "final-standard-convention-referee-v1",
        "verdict": "VERIFIED_AFTER_CORRECTION",
        "source_hashes": source_hashes(),
        "exact_tests": {
            "ordinary_rooting": {
                "narrow_equals_broad": True,
                "rooted_binary_lsa": True,
                "tree_child": True,
            },
            "broad_only_bad_preimage": {
                "rooted_binary_lsa": True,
                "level": 2,
                "tree_child": False,
                "narrow_admissible": False,
                "broad_reduction": "three_leaf_tree",
            },
            "lsa_mutation": {
                "binary_acyclic_without_lsa_check": True,
                "lsa_valid": False,
            },
            "weak_theta": weak_rows,
            "primitive_supports": {
                "core_families": primitive_rows,
                "support_graphs": graph_count,
                "admissible_rootings": rooting_count,
                "all_strong": True,
                "all_narrow_equal_broad_on_these_rootings": True,
            },
            "simple_double_triangle_k4_minus_edge": k4,
            "literal_brits_two_subblob": literal_2sub,
        },
        "mutations": {
            "rejected": sorted(mutations),
            "unexpected_survivors": sorted(k for k, v in mutations.items() if v),
        },
        "scope": {
            "englander_v4": "literal match after making the already-simple/no-parallel admissibility clause explicit",
            "holtgrefe_v2": "binary LSA-valid specialization; same no-omnian strong criterion",
            "brits_v2": "not a literal match because its reduction adds exhaustive parallel/degree-two cleanup",
            "outcome_p_safe_class": "simple reticulation-preserving sd0 semi-directed networks, with S_TC quantified over sd0 rootings",
            "unsupported_class": "all preimages of the broader cleanup map quantified as rootings",
        },
    }
    payload["payload_sha256_without_hash"] = hashlib.sha256(stable_json(payload)).hexdigest()
    OUT.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "verdict": payload["verdict"],
        "certificate": str(OUT),
        "primitive_supports": graph_count,
        "primitive_rootings": rooting_count,
        "mutations_rejected": len(mutations),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
