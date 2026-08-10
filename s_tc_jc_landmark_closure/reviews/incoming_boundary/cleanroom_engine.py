#!/usr/bin/env python3
"""Clean-room bounded directed JC relation atlas.

This file deliberately imports no producer or historical atlas module.  It
derives the cycle/theta orientation cores, rigid sources, selected completion
targets, displayed switchings, descendant masks, JC Fourier tensors, and
invariant pullbacks from the locked graph definitions.

The implementation is intentionally explicit.  Certificate files are outputs
of this program and are never used as topology-to-polynomial lookup tables.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import math
import os
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Iterator, Sequence


HERE = Path(__file__).resolve().parent
CERT = HERE / "certificates"


def stable_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value) -> str:
    if not isinstance(value, (str, bytes)):
        value = stable_json(value)
    if isinstance(value, str):
        value = value.encode()
    return hashlib.sha256(value).hexdigest()


def compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


@dataclass(frozen=True)
class MixedEdge:
    u: str
    v: str
    head_u: int = 0
    head_v: int = 0

    def reversed(self) -> "MixedEdge":
        return MixedEdge(self.v, self.u, self.head_v, self.head_u)


@dataclass
class BuiltGraph:
    arcs: tuple[tuple[str, str], ...]
    node_kind: dict[str, str]
    leaf_label: dict[str, str]
    boundary_labels: tuple[str, ...]
    dummy_labels: tuple[str, ...]
    incoming_label: str
    retics: tuple[str, ...]
    provenance: dict

    def mixed_edges(self, clear_triangle: bool = False) -> tuple[MixedEdge, ...]:
        underlying = {tuple(sorted((u, v))) for u, v in self.arcs}
        triangles: set[frozenset[str]] = set()
        if clear_triangle:
            vertices = sorted({x for edge in underlying for x in edge})
            for a, b, c in itertools.combinations(vertices, 3):
                if all(tuple(sorted(e)) in underlying for e in ((a, b), (a, c), (b, c))):
                    triangles.add(frozenset((a, b, c)))
        result = []
        for u, v in self.arcs:
            hu = 0
            hv = int(self.node_kind.get(v) == "R")
            # A rooted binary arc cannot leave a reticulation and enter another
            # reticulation in the locked class.  Only the child endpoint can
            # carry a retained arrowhead.
            if clear_triangle and any({u, v} <= tri for tri in triangles):
                hv = 0
            result.append(MixedEdge(u, v, 0, hv))
        return tuple(result)


def _edge_relation(edge: MixedEdge, a: str, b: str) -> str:
    if edge.u == a and edge.v == b:
        return f"{edge.head_u}{edge.head_v}"
    if edge.u == b and edge.v == a:
        return f"{edge.head_v}{edge.head_u}"
    raise AssertionError


def canonical_mixed(graph: BuiltGraph, *, triangle_quotient: bool = False) -> tuple[str, dict[str, int]]:
    """Exact individualization/refinement canonical form.

    Unique taxon colours anchor every boundary.  Internal vertices begin in
    one colour class: reticulation status is encoded by retained arrowheads,
    not by an extra colour.  This is important for ordinary-T quotienting.
    """
    edges = graph.mixed_edges(clear_triangle=triangle_quotient)
    vertices = sorted({x for e in edges for x in (e.u, e.v)} | set(graph.node_kind))
    incident: dict[str, list[tuple[str, str]]] = {v: [] for v in vertices}
    pair_rel: dict[tuple[str, str], str] = {}
    for e in edges:
        rel_uv = _edge_relation(e, e.u, e.v)
        rel_vu = _edge_relation(e, e.v, e.u)
        if (e.u, e.v) in pair_rel or (e.v, e.u) in pair_rel:
            # The standard graph is simple.  Parallel abstract cycle segments
            # must have acquired a repair vertex before reaching this routine.
            raise ValueError("parallel mixed edge")
        pair_rel[(e.u, e.v)] = rel_uv
        pair_rel[(e.v, e.u)] = rel_vu
        incident[e.u].append((e.v, rel_uv))
        incident[e.v].append((e.u, rel_vu))

    initial_groups: dict[str, list[str]] = defaultdict(list)
    for v in vertices:
        if v in graph.leaf_label:
            colour = "L:" + graph.leaf_label[v]
        else:
            colour = "I"
        initial_groups[colour].append(v)
    partition = tuple(tuple(sorted(initial_groups[k])) for k in sorted(initial_groups))

    def refine(part):
        part = tuple(tuple(cell) for cell in part)
        while True:
            which = {v: i for i, cell in enumerate(part) for v in cell}
            refined = []
            changed = False
            for cell in part:
                buckets: dict[tuple, list[str]] = defaultdict(list)
                for v in cell:
                    counts: dict[tuple[int, str], int] = defaultdict(int)
                    for w, rel in incident[v]:
                        counts[(which[w], rel)] += 1
                    buckets[tuple(sorted(counts.items()))].append(v)
                if len(buckets) > 1:
                    changed = True
                for key in sorted(buckets, key=repr):
                    refined.append(tuple(sorted(buckets[key])))
            part2 = tuple(refined)
            if not changed:
                return part2
            part = part2

    best: tuple | None = None
    best_order: tuple[str, ...] | None = None

    def search(part):
        nonlocal best, best_order
        part = refine(part)
        if all(len(cell) == 1 for cell in part):
            order = tuple(cell[0] for cell in part)
            labels = tuple(graph.leaf_label.get(v, "I") for v in order)
            adj = []
            for i, a in enumerate(order):
                for b in order[i + 1 :]:
                    forward = pair_rel.get((a, b), "-")
                    backward = pair_rel.get((b, a), "-")
                    adj.append(forward + "/" + backward)
            code = (labels, tuple(adj))
            if best is None or code < best:
                best = code
                best_order = order
            return
        idx = min((i for i, c in enumerate(part) if len(c) > 1), key=lambda i: (len(part[i]), i))
        cell = part[idx]
        for chosen in cell:
            remainder = tuple(v for v in cell if v != chosen)
            new = list(part[:idx]) + [(chosen,)]
            if remainder:
                new.append(remainder)
            new.extend(part[idx + 1 :])
            search(tuple(new))

    search(partition)
    assert best is not None and best_order is not None
    mapping = {v: i for i, v in enumerate(best_order)}
    return stable_json(best), mapping


@dataclass(frozen=True)
class CoreTemplate:
    name: str
    kinds: tuple[tuple[str, str], ...]
    segments: tuple[tuple[str, str], ...]
    sinks: tuple[str, ...]
    repairs: tuple[tuple[int, ...], ...]

    def kind_map(self) -> dict[str, str]:
        return dict(self.kinds)


def _orient_edges(nodes: dict[str, str], edges: Sequence[tuple[str, str]], source: str) -> Iterator[tuple[tuple[str, str], ...]]:
    required_indegree = {v: (0 if v == source else (2 if kind == "R" else 1)) for v, kind in nodes.items()}
    for bits in itertools.product((0, 1), repeat=len(edges)):
        arcs = tuple((b, a) if bit else (a, b) for bit, (a, b) in zip(bits, edges))
        indeg = defaultdict(int)
        out = defaultdict(list)
        for a, b in arcs:
            indeg[b] += 1
            out[a].append(b)
        if any(indeg[v] != required_indegree[v] for v in nodes):
            continue
        seen = {source}
        stack = [source]
        while stack:
            stack.extend(w for w in out[stack.pop()] if w not in seen and not seen.add(w))
        if len(seen) != len(nodes):
            continue
        # Reachability in a finite graph with the exact indegrees excludes a
        # directed cycle, but retain an explicit topological audit.
        temp = {v: indeg[v] for v in nodes}
        q = [v for v in nodes if temp[v] == 0]
        count = 0
        while q:
            v = q.pop()
            count += 1
            for w in out[v]:
                temp[w] -= 1
                if temp[w] == 0:
                    q.append(w)
        if count == len(nodes):
            yield arcs


def _template_key(nodes: dict[str, str], arcs: Sequence[tuple[str, str]], source: str) -> str:
    # Small coloured directed canonicalizer used only to quotient the raw
    # event allocations.  X vertices share a colour; U/V names do not.
    verts = tuple(nodes)
    groups: dict[str, list[str]] = defaultdict(list)
    for v, kind in nodes.items():
        groups["S" if v == source else kind].append(v)
    best = None
    for products in itertools.product(*(itertools.permutations(groups[k]) for k in sorted(groups))):
        order = tuple(v for part in products for v in part)
        idx = {v: i for i, v in enumerate(order)}
        code = (
            tuple("S" if v == source else nodes[v] for v in order),
            tuple(sorted((idx[a], idx[b]) for a, b in arcs)),
        )
        if best is None or code < best:
            best = code
    return repr(best)


def derive_templates() -> tuple[CoreTemplate, ...]:
    """Derive the one cycle and four theta orientation templates."""
    cycle = CoreTemplate(
        "cycle",
        (("S", "T"), ("X0", "R")),
        (("S", "X0"), ("S", "X0")),
        ("X0",),
        ((0,), (1,)),
    )

    raw = {}
    # There are two reticulations.  A branch pole may carry at most one of
    # them.  The remaining reticulations are internal path sinks X.
    for branch_retic in (0, 1):
        x_count = 2 - branch_retic
        tokens = ("S",) + tuple(f"X{i}" for i in range(x_count))
        # Allocate an ordered token sequence to each of three U--V paths.
        for perm in itertools.permutations(tokens):
            for cuts in compositions(len(tokens), 3):
                paths = []
                at = 0
                for width in cuts:
                    paths.append(perm[at : at + width])
                    at += width
                nodes = {"U": "R" if branch_retic else "T", "V": "T"}
                nodes.update({token: ("T" if token == "S" else "R") for token in tokens})
                edges = []
                for path in paths:
                    chain = ("U",) + tuple(path) + ("V",)
                    edges.extend(zip(chain, chain[1:]))
                # Parallel abstract segments are retained here.  A standard
                # simple realization must subdivide all but one of them; the
                # minimum-repair derivation below enforces that condition.
                for arcs in _orient_edges(nodes, edges, "S"):
                    key = _template_key(nodes, arcs, "S")
                    raw.setdefault(key, (nodes.copy(), tuple(arcs)))

    if len(raw) != 4:
        raise AssertionError(("theta template count", len(raw)))

    templates = []
    for _ordinal, (_key, (nodes, arcs)) in enumerate(sorted(raw.items())):
        # Every arc between special vertices is one insertion segment.
        segments = tuple(sorted(arcs))
        sinks = tuple(sorted(v for v, k in nodes.items() if k == "R" and v.startswith("X")))
        repairs = []
        for width in range(len(segments) + 1):
            for subset in itertools.combinations(range(len(segments)), width):
                if any(set(old) <= set(subset) for old in repairs):
                    continue
                try:
                    g = build_graph(
                        CoreTemplate("tmp", tuple(sorted(nodes.items())), segments, sinks, (subset,)),
                        tuple((f"D{j}",) if j in subset else () for j in range(len(segments))),
                        tuple((sink, f"SINK_{sink}") for sink in sinks),
                        boundary=("B_IN",),
                        dummy=tuple(f"D{j}" for j in subset) + tuple(f"SINK_{s}" for s in sinks),
                        incoming_label="B_IN",
                        provenance={"repair_test": subset},
                    )
                except (AssertionError, ValueError):
                    continue
                if rooted_tree_child(g):
                    repairs.append(tuple(subset))
            if repairs:
                break
        if not repairs:
            raise AssertionError(("no repair", nodes, arcs))
        branch_retic = any(nodes[v] == "R" for v in ("U", "V"))
        branch_pair_count = sum({a, b} == {"U", "V"} for a, b in segments)
        placement = "nested" if (
            branch_pair_count >= (2 if branch_retic else 1)
        ) else "separated"
        family = ("TR" if branch_retic else "TT") + "-" + placement
        templates.append(CoreTemplate(
            family, tuple(sorted(nodes.items())), segments, sinks, tuple(repairs)
        ))
    return (cycle,) + tuple(sorted(templates, key=lambda t: t.name))


def build_graph(
    template: CoreTemplate,
    words: Sequence[Sequence[str]],
    sink_labels: Sequence[tuple[str, str]],
    *,
    boundary: Sequence[str],
    dummy: Sequence[str],
    incoming_label: str,
    provenance: dict,
) -> BuiltGraph:
    if len(words) != len(template.segments):
        raise AssertionError("word/segment mismatch")
    node_kind = template.kind_map()
    arcs: list[tuple[str, str]] = []
    leaf_label = {f"leaf:{incoming_label}": incoming_label}
    node_kind[f"leaf:{incoming_label}"] = "L"
    arcs.append((f"leaf:{incoming_label}", "S"))
    used_pairs = set()
    for sid, ((tail, head), word) in enumerate(zip(template.segments, words)):
        chain = [tail]
        for pos, label in enumerate(word):
            v = f"seg:{sid}:{pos}"
            leaf = f"leaf:{label}"
            node_kind[v] = "T"
            node_kind[leaf] = "L"
            leaf_label[leaf] = label
            chain.append(v)
            arcs.append((v, leaf))
        chain.append(head)
        for a, b in zip(chain, chain[1:]):
            pair = tuple(sorted((a, b)))
            if pair in used_pairs:
                raise ValueError("parallel edge")
            used_pairs.add(pair)
            arcs.append((a, b))
    supplied_sinks = dict(sink_labels)
    if set(supplied_sinks) != set(template.sinks):
        raise AssertionError((supplied_sinks, template.sinks))
    for sink in template.sinks:
        label = supplied_sinks[sink]
        leaf = f"leaf:{label}"
        node_kind[leaf] = "L"
        leaf_label[leaf] = label
        arcs.append((sink, leaf))
    graph = BuiltGraph(
        tuple(arcs), node_kind, leaf_label, tuple(boundary), tuple(dummy), incoming_label,
        tuple(sorted(v for v, kind in node_kind.items() if kind == "R")), provenance,
    )
    validate_rooted(graph)
    return graph


def validate_rooted(graph: BuiltGraph) -> None:
    indeg = defaultdict(int)
    out = defaultdict(list)
    for a, b in graph.arcs:
        indeg[b] += 1
        out[a].append(b)
    root = f"leaf:{graph.incoming_label}"
    for v, kind in graph.node_kind.items():
        if v == root:
            expected = (0, 1)
        elif kind == "L":
            expected = (1, 0)
        elif kind == "T":
            expected = (1, 2)
        elif kind == "R":
            expected = (2, 1)
        else:
            raise AssertionError(kind)
        got = (indeg[v], len(out[v]))
        if got != expected:
            raise AssertionError((v, kind, got, expected, graph.provenance))
    seen = {root}
    stack = [root]
    while stack:
        v = stack.pop()
        for w in out[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    if seen != set(graph.node_kind):
        raise AssertionError(("unreachable", set(graph.node_kind) - seen))
    # Reachability plus the exact indegree quotas is not used as a shortcut.
    deg = dict(indeg)
    q = [v for v in graph.node_kind if deg[v] == 0]
    count = 0
    while q:
        v = q.pop()
        count += 1
        for w in out[v]:
            deg[w] -= 1
            if deg[w] == 0:
                q.append(w)
    if count != len(graph.node_kind):
        raise AssertionError("directed cycle")


def rooted_tree_child(graph: BuiltGraph) -> bool:
    out = defaultdict(list)
    for a, b in graph.arcs:
        out[a].append(b)
    for v, kind in graph.node_kind.items():
        if kind not in {"T", "R"}:
            continue
        if not any(graph.node_kind[w] in {"T", "L"} for w in out[v]):
            return False
        if kind == "R" and any(graph.node_kind[w] == "R" for w in out[v]):
            return False
    return True


def role_key(role: str) -> tuple:
    if role.startswith("Q_REPAIR_"):
        return (0, int(role.rsplit("_", 1)[1]))
    if role.startswith("Q_SINK_"):
        return (1, int(role.rsplit("_", 1)[1]))
    if role.startswith("P_"):
        return (2, int(role.rsplit("_", 1)[1]))
    return (9, role)


@dataclass
class Presentation:
    graph: BuiltGraph
    descriptor: tuple
    mixed_code: str
    t_code: str | None
    roles: tuple[str, ...]
    retains_core: bool
    completion_code: str
    raw_key: tuple


def relabel_real_boundaries(graph: BuiltGraph, mapping: dict[str, str]) -> BuiltGraph:
    if set(mapping) != set(graph.boundary_labels):
        raise AssertionError((mapping, graph.boundary_labels))
    node_map = {
        f"leaf:{old}": f"leaf:{new}" for old, new in mapping.items()
    }
    arcs = tuple((node_map.get(a, a), node_map.get(b, b)) for a, b in graph.arcs)
    node_kind = {node_map.get(v, v): kind for v, kind in graph.node_kind.items()}
    leaf_label = {
        node_map.get(v, v): mapping.get(label, label)
        for v, label in graph.leaf_label.items()
    }
    provenance = dict(graph.provenance)
    provenance["rooted_role_to_physical"] = dict(sorted(mapping.items()))
    return BuiltGraph(
        arcs, node_kind, leaf_label,
        tuple(f"L_{i}" for i in range(len(mapping))), graph.dummy_labels,
        mapping[graph.incoming_label], graph.retics, provenance,
    )


def anchor_source_graph(graph: BuiltGraph) -> BuiltGraph:
    """Anchor the simultaneous full-boundary action without fixing IN.

    All real boundary leaves receive one temporary colour.  Their positions
    in an exact canonical mixed-graph order define the source labels.  Rooted
    incoming status is retained only in the resulting provenance map.
    """
    unlabelled = BuiltGraph(
        graph.arcs, graph.node_kind,
        {v: ("BOUNDARY" if label in graph.boundary_labels else label)
         for v, label in graph.leaf_label.items()},
        graph.boundary_labels, graph.dummy_labels, graph.incoming_label,
        graph.retics, graph.provenance,
    )
    _, vertex_map = canonical_mixed(unlabelled)
    boundary_nodes = sorted(
        (f"leaf:{label}" for label in graph.boundary_labels),
        key=lambda v: vertex_map[v],
    )
    mapping = {
        graph.leaf_label[v]: f"L_{i}" for i, v in enumerate(boundary_nodes)
    }
    return relabel_real_boundaries(graph, mapping)


def source_presentations(template: CoreTemplate, outgoing: int) -> list[BuiltGraph]:
    generated: dict[str, BuiltGraph] = {}
    for rid, repair in enumerate(template.repairs):
        support = len(template.sinks) + len(repair)
        extras = outgoing - support
        if extras not in (0, 1, 2):
            continue
        fixed = {sid: [f"Q_REPAIR_{j}"] for j, sid in enumerate(repair)}
        extra_roles = tuple(f"P_{i}" for i in range(extras))
        for placements in itertools.product(range(len(template.segments)), repeat=extras):
            members = {sid: list(fixed.get(sid, ())) for sid in range(len(template.segments))}
            for role, sid in zip(extra_roles, placements):
                members[sid].append(role)
            choices = [tuple(itertools.permutations(members[sid])) for sid in range(len(template.segments))]
            for words in itertools.product(*choices):
                sinks = tuple((sink, f"Q_SINK_{j}") for j, sink in enumerate(template.sinks))
                outgoing_roles = tuple(sorted(
                    [x for word in words for x in word] + [label for _, label in sinks],
                    key=role_key,
                ))
                roles = ("INCOMING",) + outgoing_roles
                graph0 = build_graph(
                    template, words, sinks,
                    boundary=roles, dummy=(), incoming_label="INCOMING",
                    provenance={
                        "side": "source", "template": template.name,
                        "repair": rid, "role_words": words, "roles": roles,
                    },
                )
                graph = anchor_source_graph(graph0)
                if not rooted_tree_child(graph):
                    raise AssertionError(("source not tree-child", graph.provenance))
                code, _ = canonical_mixed(graph)
                generated.setdefault(code, graph)
    return [generated[k] for k in sorted(generated)]


def target_bases(template: CoreTemplate, outgoing: int) -> list[dict]:
    boundary_count = outgoing + 1
    bases = {}
    sink_count = len(template.sinks)
    for incoming_mode in ("incoming_selected", "incoming_dummy"):
      incoming_selected = int(incoming_mode == "incoming_selected")
      for sink_mask in itertools.product((0, 1), repeat=sink_count):
        selected_sinks = sum(sink_mask)
        ordinary = boundary_count - incoming_selected - selected_sinks
        if ordinary < 0:
            continue
        for counts in compositions(ordinary, len(template.segments)):
            occupied = {sid for sid, width in enumerate(counts) if width}
            if any(set(repair) <= occupied for repair in template.repairs):
                completion_repairs = ((-1, ()),)
            else:
                completion_repairs = tuple(
                    (rid, tuple(sid for sid in repair if counts[sid] == 0))
                    for rid, repair in enumerate(template.repairs)
                )
            for rid, dummy_segments in completion_repairs:
                # The selected slots are deterministic before target labels
                # are permuted: segment order, then sink order.
                slots = ([('incoming', 0, 0)] if incoming_selected else [])
                for sid, width in enumerate(counts):
                    slots.extend(("segment", sid, pos) for pos in range(width))
                slots.extend(("sink", j, 0) for j, bit in enumerate(sink_mask) if bit)
                if len(slots) != boundary_count:
                    raise AssertionError
                key = (template.name, incoming_mode, counts, sink_mask, dummy_segments)
                prior = bases.setdefault(key, {
                    "template": template,
                    "incoming_mode": incoming_mode,
                    "counts": counts,
                    "sink_mask": sink_mask,
                    "dummy_segments": dummy_segments,
                    "repair_index": rid,
                    "raw_repair_indices": [],
                    "slots": tuple(slots),
                })
                prior["raw_repair_indices"].append(rid)
    return [bases[k] for k in sorted(bases, key=repr)]


def instantiate_target(base: dict, assignment: Sequence[int]) -> BuiltGraph:
    template = base["template"]
    words: list[list[str]] = [[] for _ in template.segments]
    sinks: dict[str, str] = {}
    if len(assignment) != len(base["slots"]):
        raise AssertionError((assignment, base["slots"]))
    slot_labels = {slot: f"L_{label}" for slot, label in zip(base["slots"], assignment)}
    for sid, width in enumerate(base["counts"]):
        for pos in range(width):
            words[sid].append(slot_labels[("segment", sid, pos)])
        if sid in base["dummy_segments"]:
            words[sid].append(f"D_REPAIR_{sid}")
    dummy = [f"D_REPAIR_{sid}" for sid in base["dummy_segments"]]
    for j, sink in enumerate(template.sinks):
        if base["sink_mask"][j]:
            sinks[sink] = slot_labels[("sink", j, 0)]
        else:
            sinks[sink] = f"D_SINK_{j}"
            dummy.append(f"D_SINK_{j}")
    boundary = tuple(f"L_{i}" for i in range(len(assignment)))
    if base["incoming_mode"] == "incoming_selected":
        incoming_label = slot_labels[("incoming", 0, 0)]
    else:
        incoming_label = "D_INCOMING"
        dummy.append(incoming_label)
    graph = build_graph(
        template, tuple(tuple(w) for w in words), tuple(sinks.items()),
        boundary=boundary, dummy=tuple(dummy), incoming_label=incoming_label,
        provenance={
            "side": "target", "template": template.name,
            "incoming_mode": base["incoming_mode"],
            "counts": base["counts"], "sink_mask": base["sink_mask"],
            "dummy_segments": base["dummy_segments"],
            "assignment": tuple(assignment),
        },
    )
    if not rooted_tree_child(graph):
        raise AssertionError(("completion not tree-child", graph.provenance))
    return graph


def retains_original_core(base: dict) -> bool:
    if base["incoming_mode"] != "incoming_selected":
        return False
    if not all(base["sink_mask"]):
        return False
    occupied = {sid for sid, width in enumerate(base["counts"]) if width}
    return any(set(repair) <= occupied for repair in base["template"].repairs)


def selected_graph(completion: BuiltGraph) -> BuiltGraph | None:
    if completion.dummy_labels:
        return None
    return completion


def _descendants(out: dict[str, list[str]], start: str, selected_index: dict[str, int]) -> int:
    mask = 0
    stack = [start]
    seen = set()
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        if v in selected_index:
            mask |= 1 << selected_index[v]
        stack.extend(out.get(v, ()))
    return mask


def descriptor(graph: BuiltGraph) -> tuple:
    selected_order = tuple(graph.boundary_labels)
    selected_index = {f"leaf:{label}": i for i, label in enumerate(selected_order)}
    incoming_edges = {}
    for r in graph.retics:
        incoming_edges[r] = tuple((a, b) for a, b in graph.arcs if b == r)
        if len(incoming_edges[r]) != 2:
            raise AssertionError((r, incoming_edges[r]))
    retics = tuple(graph.retics)
    switchings = tuple(itertools.product((0, 1), repeat=len(retics)))
    edge_rows = {edge: [] for edge in graph.arcs}
    for choice in switchings:
        deleted = {incoming_edges[r][1 - bit] for r, bit in zip(retics, choice)}
        kept = tuple(edge for edge in graph.arcs if edge not in deleted)
        out = defaultdict(list)
        indeg = defaultdict(int)
        for a, b in kept:
            out[a].append(b)
            indeg[b] += 1
        root = f"leaf:{graph.incoming_label}"
        if indeg[root] != 0 or any(indeg[v] != 1 for v in graph.node_kind if v != root):
            raise AssertionError(("not arborescence", graph.provenance, choice))
        for edge in graph.arcs:
            edge_rows[edge].append(0 if edge in deleted else _descendants(out, edge[1], selected_index))
    rows = tuple(row for row in edge_rows.values() if any(row))

    # Quotient parent order and reticulation order exactly and zip repeated
    # complete mask rows to one effective multiplier.
    return canonical_descriptor(len(retics), rows)


def presentation_from_graph(graph: BuiltGraph, retains: bool) -> Presentation:
    code, _ = canonical_mixed(graph)
    t_code = canonical_mixed(graph, triangle_quotient=True)[0] if retains else None
    roles = tuple(graph.provenance.get("roles", ()))
    return Presentation(
        graph=graph,
        descriptor=descriptor(graph),
        mixed_code=code if retains else "",
        t_code=t_code,
        roles=roles,
        retains_core=retains,
        completion_code=code,
        raw_key=tuple(sorted((k, repr(v)) for k, v in graph.provenance.items())),
    )


JC_REPRESENTATIVES = (
    (0, 0, 0, 0),
    (0, 0, 1, 1),
    (0, 1, 0, 1),
    (0, 1, 1, 0),
    (0, 1, 2, 3),
    (1, 0, 0, 1),
    (1, 0, 1, 0),
    (1, 0, 2, 3),
    (1, 1, 0, 0),
    (1, 1, 1, 1),
    (1, 1, 2, 2),
    (1, 2, 0, 3),
    (1, 2, 1, 2),
    (1, 2, 2, 1),
    (1, 2, 3, 0),
)


def representative_index(assignment: Sequence[int]) -> int:
    if len(assignment) != 4 or assignment[0] ^ assignment[1] ^ assignment[2] ^ assignment[3]:
        raise ValueError(assignment)
    candidates = []
    for perm in itertools.permutations((1, 2, 3)):
        mapping = {0: 0, 1: perm[0], 2: perm[1], 3: perm[2]}
        candidates.append(tuple(mapping[x] for x in assignment))
    canonical = min(candidates)
    try:
        return JC_REPRESENTATIVES.index(canonical)
    except ValueError as exc:
        raise AssertionError((assignment, canonical)) from exc


Invariant = tuple[tuple[int, tuple[int, ...]], ...]
Poly = dict[tuple[int, ...], int]


def normalize_invariant(terms: Iterable[tuple[int, Sequence[int]]]) -> Invariant:
    combined = defaultdict(int)
    for coefficient, monomial in terms:
        combined[tuple(sorted(int(i) for i in monomial))] += int(coefficient)
    items = sorted((m, c) for m, c in combined.items() if c)
    if items and items[0][1] < 0:
        items = [(m, -c) for m, c in items]
    return tuple((c, m) for m, c in items)


def invariant_orbit() -> tuple[Invariant, ...]:
    payload = json.loads((HERE / "proposed_invariants.json").read_text())
    templates = [normalize_invariant(row) for row in payload["templates"]]
    # The seventh input is indexed in the fourteen nontrivial coordinates.
    templates.append(normalize_invariant((c, tuple(i + 1 for i in m)) for c, m in payload["seventh"]))
    orbit = set()
    for invariant in templates:
        for leaf_perm in itertools.permutations(range(4)):
            moved_terms = []
            for coefficient, monomial in invariant:
                moved = []
                for index in monomial:
                    assignment = JC_REPRESENTATIVES[index]
                    transported = tuple(assignment[leaf_perm[i]] for i in range(4))
                    moved.append(representative_index(transported))
                moved_terms.append((coefficient, moved))
            orbit.add(normalize_invariant(moved_terms))
    answer = tuple(sorted(orbit, key=repr))
    if len(answer) != 84:
        raise AssertionError(("invariant orbit", len(answer)))
    # Port-arm multihomogeneity is checked directly in character coordinates.
    for invariant in answer:
        degrees = set()
        for _coefficient, monomial in invariant:
            degree = [0, 0, 0, 0]
            for index in monomial:
                for leaf, character in enumerate(JC_REPRESENTATIVES[index]):
                    degree[leaf] += int(character != 0)
            degrees.add(tuple(degree))
        if len(degrees) != 1:
            raise AssertionError(("not port multihomogeneous", invariant, degrees))
    return answer


def canonical_descriptor(r: int, rows: Iterable[Sequence[int]]) -> tuple:
    rows = tuple(sorted(set(tuple(int(x) for x in row) for row in rows if any(row))))
    displays = tuple(itertools.product((0, 1), repeat=r))
    candidates = []
    for permutation in itertools.permutations(range(r)):
        for flips in itertools.product((0, 1), repeat=r):
            column_order = []
            for new_bits in displays:
                old_bits = [0] * r
                for new_pos, old_pos in enumerate(permutation):
                    old_bits[old_pos] = new_bits[new_pos] ^ flips[new_pos]
                old_index = 0
                for bit in old_bits:
                    old_index = (old_index << 1) | bit
                column_order.append(old_index)
            candidates.append((r, tuple(sorted(set(tuple(row[i] for i in column_order) for row in rows)))))
    return min(candidates)


def restrict_descriptor(full: tuple, ordered_positions: Sequence[int]) -> tuple:
    r, rows = full
    moved_rows = []
    for row in rows:
        moved = []
        for mask in row:
            new_mask = 0
            for new, old in enumerate(ordered_positions):
                if mask & (1 << old):
                    new_mask |= 1 << new
            moved.append(new_mask)
        moved_rows.append(tuple(moved))
    return canonical_descriptor(r, moved_rows)


def permute_descriptor(full: tuple, assignment: Sequence[int]) -> tuple:
    """Move structural boundary positions to physical labels.

    ``assignment[position]`` is the physical label index at that structural
    position.  The returned mask bits are in physical-label order.
    """
    r, rows = full
    moved = []
    for row in rows:
        outrow = []
        for mask in row:
            outmask = 0
            for position, actual in enumerate(assignment):
                if mask & (1 << position):
                    outmask |= 1 << actual
            outrow.append(outmask)
        moved.append(tuple(outrow))
    return canonical_descriptor(r, moved)


def poly_add(left: Poly, right: Poly, scale: int = 1) -> Poly:
    answer = dict(left)
    for exponent, coefficient in right.items():
        answer[exponent] = answer.get(exponent, 0) + scale * coefficient
        if not answer[exponent]:
            del answer[exponent]
    return answer


def poly_mul(left: Poly, right: Poly) -> Poly:
    if not left or not right:
        return {}
    answer = defaultdict(int)
    for a, ca in left.items():
        for b, cb in right.items():
            answer[tuple(x + y for x, y in zip(a, b))] += ca * cb
    return {e: c for e, c in answer.items() if c}


def poly_pow(poly: Poly, power: int, variables: int) -> Poly:
    answer = {(0,) * variables: 1}
    base = poly
    while power:
        if power & 1:
            answer = poly_mul(answer, base)
        power >>= 1
        if power:
            base = poly_mul(base, base)
    return answer


@lru_cache(maxsize=256)
def coordinate_polynomials(desc: tuple) -> tuple[Poly, ...]:
    r, rows = desc
    edge_count = len(rows)
    variables = edge_count + r
    displays = tuple(itertools.product((0, 1), repeat=r))
    coordinates = []
    for assignment in JC_REPRESENTATIVES:
        total: Poly = {}
        for display_index, bits in enumerate(displays):
            edge_exp = [0] * edge_count
            for edge, row in enumerate(rows):
                state = 0
                mask = row[display_index]
                for leaf, character in enumerate(assignment):
                    if mask & (1 << leaf):
                        state ^= character
                edge_exp[edge] = int(state != 0)
            weight: Poly = {tuple(edge_exp + [0] * r): 1}
            for k, bit in enumerate(bits):
                zero = [0] * variables
                zero[edge_count + k] = 1
                lam = {tuple(zero): 1}
                if bit:
                    factor = lam
                else:
                    factor = {(0,) * variables: 1, tuple(zero): -1}
                weight = poly_mul(weight, factor)
            total = poly_add(total, weight)
        coordinates.append(total)
    return tuple(coordinates)


@lru_cache(maxsize=512)
def coordinate_power(desc: tuple, index: int, power: int) -> Poly:
    coordinates = coordinate_polynomials(desc)
    variables = len(next(iter(coordinates[0]))) if coordinates[0] else len(desc[1]) + desc[0]
    return poly_pow(coordinates[index], power, variables)


@lru_cache(maxsize=1024)
def monomial_pullback(desc: tuple, monomial: tuple[int, ...]) -> Poly:
    variables = len(desc[1]) + desc[0]
    term = {(0,) * variables: 1}
    multiplicities = defaultdict(int)
    for index in monomial:
        multiplicities[index] += 1
    for index, power in multiplicities.items():
        term = poly_mul(term, coordinate_power(desc, index, power))
    return term


@lru_cache(maxsize=512)
def pullback(desc: tuple, invariant: Invariant) -> Poly:
    return pullbacks_shared_clean(desc, (invariant,))[0]


def pullbacks_shared_clean(desc: tuple, invariants: Sequence[Invariant]) -> tuple[Poly, ...]:
    coordinates = coordinate_polynomials(desc)
    variables = len(desc[1]) + desc[0]
    monomial_cache: dict[tuple[int, ...], Poly] = {(): {(0,) * variables: 1}}

    def monomial(indices: tuple[int, ...]) -> Poly:
        if indices not in monomial_cache:
            monomial_cache[indices] = poly_mul(monomial(indices[:-1]), coordinates[indices[-1]])
        return monomial_cache[indices]

    answers = []
    for invariant in invariants:
        answer: Poly = {}
        for coefficient, indices in invariant:
            answer = poly_add(answer, monomial(indices), coefficient)
        answers.append(answer)
    return tuple(answers)


def _mod_values(desc: tuple, seed: int, prime: int = 2147483647) -> tuple[int, ...]:
    r, rows = desc
    edge_values = [((seed * 104729 + i * 1009 + 17) % (prime - 2)) + 1 for i in range(len(rows))]
    lambdas = [((seed * 130363 + i * 1013 + 29) % (prime - 2)) + 1 for i in range(r)]
    displays = tuple(itertools.product((0, 1), repeat=r))
    answer = []
    for assignment in JC_REPRESENTATIVES:
        total = 0
        for display_index, bits in enumerate(displays):
            value = 1
            for edge, row in enumerate(rows):
                state = 0
                for leaf, character in enumerate(assignment):
                    if row[display_index] & (1 << leaf):
                        state ^= character
                if state:
                    value = value * edge_values[edge] % prime
            for k, bit in enumerate(bits):
                value = value * (lambdas[k] if bit else 1 - lambdas[k]) % prime
            total = (total + value) % prime
        answer.append(total)
    return tuple(answer)


def _invariant_mod(coordinates: Sequence[int], invariant: Invariant, prime: int = 2147483647) -> int:
    total = 0
    for coefficient, monomial in invariant:
        value = coefficient % prime
        for index in monomial:
            value = value * coordinates[index] % prime
        total = (total + value) % prime
    return total


class BitEngine:
    def __init__(self, invariants: Sequence[Invariant]):
        self.invariants = tuple(invariants)
        self.cache: dict[tuple, int] = {}
        self.exact_zero_checks = 0

    def load(self, path: Path) -> int:
        if not path.is_file():
            return 0
        with gzip.open(path, "rt") as handle:
            payload = json.load(handle)
        if payload.get("schema") != "cleanroom-descriptor-bits-v1":
            raise ValueError("bad bit-cache schema")
        if payload.get("invariant_orbit_sha256") != digest(self.invariants):
            raise ValueError("bit-cache invariant mismatch")
        for row in payload["rows"]:
            r, rows = row["descriptor"]
            desc = (int(r), tuple(tuple(int(x) for x in values) for values in rows))
            bits = int(row["bits"])
            prior = self.cache.setdefault(desc, bits)
            if prior != bits:
                raise ValueError("conflicting cached bit record")
        return len(payload["rows"])

    def save(self, path: Path) -> None:
        payload = {
            "schema": "cleanroom-descriptor-bits-v1",
            "invariant_orbit_sha256": digest(self.invariants),
            "rows": [
                {"descriptor": serialize_descriptor(desc), "bits": str(bits)}
                for desc, bits in sorted(self.cache.items(), key=lambda kv: repr(kv[0]))
            ],
        }
        data = (stable_json(payload) + "\n").encode()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as handle:
                handle.write(data)

    def bits(self, desc: tuple) -> int:
        if desc in self.cache:
            return self.cache[desc]
        values = tuple(_mod_values(desc, seed) for seed in (101, 1009, 10007))
        bits = 0
        uncertain = []
        for i, invariant in enumerate(self.invariants):
            if any(_invariant_mod(row, invariant) for row in values):
                bits |= 1 << i
            else:
                uncertain.append((i, invariant))
        exact = pullbacks_shared_clean(desc, tuple(invariant for _i, invariant in uncertain))
        for (i, _invariant), polynomial in zip(uncertain, exact):
            self.exact_zero_checks += 1
            if polynomial:
                bits |= 1 << i
        self.cache[desc] = bits
        return bits


def full_deck_signature(desc: tuple, boundary_count: int, engine: BitEngine) -> tuple[int, tuple[tuple, ...]]:
    signature = 0
    deck = []
    width = len(engine.invariants)
    for chunk, quartet in enumerate(itertools.combinations(range(boundary_count), 4)):
        local = restrict_descriptor(desc, quartet)
        deck.append(local)
        signature |= engine.bits(local) << (width * chunk)
    return signature, tuple(deck)


def source_models(outgoing: int, engine: BitEngine) -> list[dict]:
    templates = derive_templates()
    grouped: dict[str, dict] = {}
    boundary_count = outgoing + 1
    for template in templates:
        for graph in source_presentations(template, outgoing):
            code, vertex_map = canonical_mixed(graph)
            desc = descriptor(graph)
            signature, deck = full_deck_signature(desc, boundary_count, engine)
            row = grouped.setdefault(code, {
                "mixed_code": code,
                "mixed_code_sha256": digest(code),
                "t_code": canonical_mixed(graph, triangle_quotient=True)[0],
                "rooted_variants": [],
                "signatures": set(),
                "descriptors": {},
            })
            variant = {
                "template": graph.provenance["template"],
                "repair": graph.provenance["repair"],
                "role_words": graph.provenance["role_words"],
                "roles": graph.provenance["roles"],
                "rooted_role_to_physical": graph.provenance["rooted_role_to_physical"],
                "incoming_physical": graph.incoming_label,
                "descriptor_sha256": digest(desc),
                "canonical_vertex_map": vertex_map,
            }
            row["rooted_variants"].append(variant)
            row["signatures"].add(signature)
            row["descriptors"][digest(desc)] = (desc, deck, graph)
    answer = []
    for code, row in sorted(grouped.items()):
        # Reversible rerooting of one standard mixed graph must not change its
        # invariant deck.  This is checked, never assumed.
        if len(row["signatures"]) != 1:
            raise AssertionError(("rooted deck mismatch", digest(code), row["signatures"]))
        signature = next(iter(row["signatures"]))
        representative_key = min(row["descriptors"])
        desc, deck, graph = row["descriptors"][representative_key]
        answer.append({
            **{k: v for k, v in row.items() if k not in {"signatures", "descriptors"}},
            "signature": signature,
            "descriptor": desc,
            "deck": deck,
            "graph": graph,
            "rooted_variants": sorted(row["rooted_variants"], key=repr),
            "rooted_descriptor_count": len(row["descriptors"]),
        })
    return answer


def base_record(base: dict) -> dict:
    return {
        "template": base["template"].name,
        "incoming_mode": base["incoming_mode"],
        "counts": base["counts"],
        "sink_mask": base["sink_mask"],
        "dummy_segments": base["dummy_segments"],
        "raw_repair_indices": tuple(sorted(set(base["raw_repair_indices"]))),
    }


def target_descriptor_groups(outgoing: int) -> dict[tuple, list[dict]]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    identity = tuple(range(outgoing + 1))
    for template in derive_templates():
        for base in target_bases(template, outgoing):
            graph = instantiate_target(base, identity)
            desc = descriptor(graph)
            groups[desc].append(base)
    return groups


def serialize_descriptor(desc: tuple) -> list:
    return [desc[0], [list(row) for row in desc[1]]]


def screen_size(outgoing: int) -> dict:
    invariants = invariant_orbit()
    engine = BitEngine(invariants)
    loaded_bit_records = engine.load(CERT / "descriptor_bits.json.gz")
    sources = source_models(outgoing, engine)
    source_signatures = sorted({row["signature"] for row in sources})
    source_by_signature = defaultdict(list)
    for index, source in enumerate(sources):
        source_by_signature[source["signature"]].append(index)

    groups = target_descriptor_groups(outgoing)
    p = outgoing + 1
    permutations = tuple(itertools.permutations(range(p)))
    target_signature_rows: dict[int, dict] = {}
    necessary_pairs = set()
    descriptor_orbit_total = 0
    candidate_modes = defaultdict(int)
    equal_modes = defaultdict(int)
    fixed_incoming_candidate_pairs = set()
    full_only_candidate_pairs = set()
    dummy_incoming_pairs = set()

    for group_index, (structural_desc, bases) in enumerate(sorted(groups.items(), key=lambda kv: repr(kv[0]))):
        orbit_seen = {}
        for assignment in permutations:
            moved = permute_descriptor(structural_desc, assignment)
            if moved in orbit_seen:
                orbit_seen[moved].append(assignment)
            else:
                orbit_seen[moved] = [assignment]
        descriptor_orbit_total += len(orbit_seen)
        for moved, assignments in orbit_seen.items():
            target_signature, deck = full_deck_signature(moved, p, engine)
            compatible_sources = [s for s in source_signatures if not (s & ~target_signature)]
            if not compatible_sources:
                continue
            target_key = digest([serialize_descriptor(moved), target_signature])
            target_row = target_signature_rows.setdefault(target_signature, {
                "signature": target_signature,
                "presentations": [],
            })
            target_row["presentations"].append({
                "target_key": target_key,
                "descriptor": moved,
                "deck": deck,
                "structural_descriptor": structural_desc,
                "bases": bases,
                "assignments": tuple(assignments),
            })
            for source_signature in compatible_sources:
                pair = (source_signature, target_signature)
                necessary_pairs.add(pair)
                modes = {base["incoming_mode"] for base in bases}
                for mode in modes:
                    candidate_modes[mode] += 1
                    if source_signature == target_signature:
                        equal_modes[mode] += 1
                if "incoming_dummy" in modes:
                    dummy_incoming_pairs.add(pair)
                # A fixed-incoming representative exists only if at least one
                # selected-incoming base/assignment maps its structural
                # incoming slot to the source rooted incoming physical label.
                fixed = False
                for source_index in source_by_signature[source_signature]:
                    source_incoming = sources[source_index]["graph"].incoming_label
                    source_actual = int(source_incoming.split("_")[-1])
                    for base in bases:
                        if base["incoming_mode"] != "incoming_selected":
                            continue
                        incoming_position = base["slots"].index(("incoming", 0, 0))
                        if any(assignment[incoming_position] == source_actual for assignment in assignments):
                            fixed = True
                            break
                    if fixed:
                        break
                (fixed_incoming_candidate_pairs if fixed else full_only_candidate_pairs).add(pair)

    equal_pairs = {pair for pair in necessary_pairs if pair[0] == pair[1]}
    summary = {
        "schema": "cleanroom-full-boundary-screen-v1",
        "outgoing": outgoing,
        "boundary_count": p,
        "invariant_count": len(invariants),
        "source_standard_topologies": len(sources),
        "source_signatures": len(source_signatures),
        "target_structural_bases": sum(len(v) for v in groups.values()),
        "target_structural_descriptor_groups": len(groups),
        "target_descriptor_orbit_total": descriptor_orbit_total,
        "target_candidate_signatures": len(target_signature_rows),
        "necessary_signature_pairs": len(necessary_pairs),
        "equal_signature_pairs": len(equal_pairs),
        "fixed_incoming_candidate_pairs": len(fixed_incoming_candidate_pairs),
        "full_boundary_only_candidate_pairs": len(full_only_candidate_pairs),
        "pairs_with_dummy_incoming_presentation": len(dummy_incoming_pairs),
        "candidate_mode_occurrences": dict(sorted(candidate_modes.items())),
        "equal_mode_occurrences": dict(sorted(equal_modes.items())),
        "projected_descriptor_bit_records": len(engine.cache),
        "projected_descriptor_bit_records_loaded": loaded_bit_records,
        "exact_zero_pullback_checks": engine.exact_zero_checks,
        "source_rows": [{
            "mixed_code_sha256": row["mixed_code_sha256"],
            "t_code_sha256": digest(row["t_code"]),
            "signature": str(row["signature"]),
            "descriptor": serialize_descriptor(row["descriptor"]),
            "rooted_descriptor_count": row["rooted_descriptor_count"],
            "rooted_variants": row["rooted_variants"],
        } for row in sources],
        "necessary_pairs_sha256": digest(sorted((str(a), str(b)) for a, b in necessary_pairs)),
        "equal_pairs_sha256": digest(sorted(str(a) for a, _ in equal_pairs)),
    }
    summary["body_sha256"] = digest(summary)
    write_json(CERT / f"screen_n{outgoing}.json", summary)

    # Candidate detail remains self-contained and deterministic.  It is a
    # graph-regenerated intermediate, not a separator lookup table.
    detail_path = CERT / f"screen_candidates_n{outgoing}.jsonl.gz"
    with detail_path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as handle:
            for target_signature in sorted(target_signature_rows):
                row = target_signature_rows[target_signature]
                serial = {
                    "target_signature": str(target_signature),
                    "presentations": [{
                        "target_key": p0["target_key"],
                        "descriptor": serialize_descriptor(p0["descriptor"]),
                        "structural_descriptor_sha256": digest(p0["structural_descriptor"]),
                        "base_records": [base_record(b) for b in p0["bases"]],
                        "assignments": [list(a) for a in p0["assignments"]],
                    } for p0 in row["presentations"]],
                }
                handle.write((stable_json(serial) + "\n").encode())
    engine.save(CERT / "descriptor_bits.json.gz")
    return summary


def seed_bits_from_screen(outgoing: int) -> dict:
    invariants = invariant_orbit()
    engine = BitEngine(invariants)
    engine.load(CERT / "descriptor_bits.json.gz")
    screen = json.loads((CERT / f"screen_n{outgoing}.json").read_text())
    if screen["boundary_count"] != 4:
        raise ValueError("direct signature seeding is valid only for four boundaries")
    added = 0
    for row in screen["source_rows"]:
        r, rows = row["descriptor"]
        desc = (int(r), tuple(tuple(values) for values in rows))
        bits = int(row["signature"])
        if desc not in engine.cache:
            engine.cache[desc] = bits
            added += 1
        elif engine.cache[desc] != bits:
            raise AssertionError("source seed conflict")
    with gzip.open(CERT / f"screen_candidates_n{outgoing}.jsonl.gz", "rt") as handle:
        for line in handle:
            row = json.loads(line)
            bits = int(row["target_signature"])
            for presentation in row["presentations"]:
                r, rows = presentation["descriptor"]
                desc = (int(r), tuple(tuple(values) for values in rows))
                if desc not in engine.cache:
                    engine.cache[desc] = bits
                    added += 1
                elif engine.cache[desc] != bits:
                    raise AssertionError("target seed conflict")
    engine.save(CERT / "descriptor_bits.json.gz")
    result = {"schema": "cleanroom-bit-seed-v1", "outgoing": outgoing, "added": added, "total": len(engine.cache)}
    result["body_sha256"] = digest(result)
    write_json(CERT / f"bit_seed_n{outgoing}.json", result)
    return result


def primitive_polynomial(poly: Poly) -> tuple[tuple[tuple[int, ...], int], ...]:
    if not poly:
        return ()
    content = 0
    for coefficient in poly.values():
        content = math.gcd(content, abs(coefficient))
    rows = [(exponent, coefficient // content) for exponent, coefficient in poly.items()]
    rows.sort()
    if rows[0][1] < 0:
        rows = [(exponent, -coefficient) for exponent, coefficient in rows]
    return tuple(rows)


def bernstein_sign(poly: Poly, limit: int = 200_000) -> tuple[int | None, dict]:
    if not poly:
        return 0, {"method": "zero"}
    variables = len(next(iter(poly)))
    active = [i for i in range(variables) if any(exponent[i] for exponent in poly)]
    if not active:
        value = next(iter(poly.values()))
        return (1 if value > 0 else -1), {"method": "constant", "value": value}
    degrees = [max(exponent[i] for exponent in poly) for i in active]
    grid = math.prod(d + 1 for d in degrees)
    if grid > limit:
        return None, {"method": "bernstein_grid_too_large", "grid": grid, "degrees": degrees}
    signs = set()
    minimum = None
    maximum = None
    for beta in itertools.product(*(range(d + 1) for d in degrees)):
        value = Fraction(0)
        for exponent, coefficient in poly.items():
            alpha = tuple(exponent[i] for i in active)
            if any(a > b for a, b in zip(alpha, beta)):
                continue
            factor = Fraction(coefficient)
            for a, b, d in zip(alpha, beta, degrees):
                factor *= Fraction(math.comb(b, a), math.comb(d, a))
            value += factor
        minimum = value if minimum is None or value < minimum else minimum
        maximum = value if maximum is None or value > maximum else maximum
        signs.add((value > 0) - (value < 0))
    cert = {
        "method": "tensor_bernstein",
        "active_variables": active,
        "degrees": degrees,
        "coefficient_count": grid,
        "minimum": [minimum.numerator, minimum.denominator],
        "maximum": [maximum.numerator, maximum.denominator],
    }
    if signs <= {0, 1} and 1 in signs:
        return 1, cert
    if signs <= {0, -1} and -1 in signs:
        return -1, cert
    return None, cert


def certify_factor_sign(poly: Poly) -> tuple[int | None, dict]:
    coefficients = list(poly.values())
    if all(c > 0 for c in coefficients):
        return 1, {"method": "positive_monomial_coefficients"}
    if all(c < 0 for c in coefficients):
        return -1, {"method": "negative_monomial_coefficients"}
    return bernstein_sign(poly)


def exact_sign_certificate(poly: Poly) -> dict:
    """Prove strict sign on the open unit cube by exact factor certificates."""
    if not poly:
        return {"certified": False, "reason": "zero polynomial"}
    direct_sign, direct_certificate = certify_factor_sign(poly)
    if direct_sign is not None:
        return {
            "certified": True,
            "strict_sign": direct_sign,
            "constant_factor": "1",
            "factors": [{
                "factor_sha256": digest(primitive_polynomial(poly)),
                "multiplicity": 1,
                "strict_sign": direct_sign,
                "certificate": direct_certificate,
            }],
            "exact_polynomial_sha256": digest(tuple(sorted(poly.items()))),
            "primitive_polynomial_sha256": digest(primitive_polynomial(poly)),
        }
    import sympy as sp

    variables = len(next(iter(poly)))
    symbols = sp.symbols(f"z0:{variables}")
    expression = sum(
        coefficient * math.prod(symbols[i] ** exponent[i] for i in range(variables))
        for exponent, coefficient in poly.items()
    )
    constant, factors = sp.factor_list(expression, *symbols)
    sign = 1 if constant > 0 else -1
    factor_certificates = []
    for factor_expression, multiplicity in factors:
        factor_poly_sp = sp.Poly(factor_expression, *symbols, domain=sp.ZZ)
        factor_poly: Poly = {
            tuple(int(x) for x in monomial): int(coefficient)
            for monomial, coefficient in factor_poly_sp.terms()
        }
        factor_sign, cert = certify_factor_sign(factor_poly)
        if factor_sign is None:
            active = [i for i in range(variables) if factor_poly_sp.degree(symbols[i]) > 0]
            if len(active) == 1:
                univariate = sp.Poly(factor_expression, symbols[active[0]], domain=sp.ZZ)
                roots = int(univariate.count_roots(0, 1))
                midpoint = univariate.eval(Fraction(1, 2))
                if roots == 0 and midpoint:
                    factor_sign = 1 if midpoint > 0 else -1
                    cert = {
                        "method": "sturm_open_interval",
                        "variable": active[0],
                        "root_count": roots,
                        "midpoint": [int(midpoint.p), int(midpoint.q)] if hasattr(midpoint, "p") else str(midpoint),
                    }
        if factor_sign is None:
            return {
                "certified": False,
                "reason": "unresolved factor",
                "factor": str(factor_expression),
                "partial_certificate": cert,
            }
        if multiplicity % 2:
            sign *= factor_sign
        factor_certificates.append({
            "factor_sha256": digest(primitive_polynomial(factor_poly)),
            "multiplicity": int(multiplicity),
            "strict_sign": factor_sign,
            "certificate": cert,
        })
    return {
        "certified": True,
        "strict_sign": sign,
        "constant_factor": str(constant),
        "factors": factor_certificates,
        "exact_polynomial_sha256": digest(tuple(sorted(poly.items()))),
        "primitive_polynomial_sha256": digest(primitive_polynomial(poly)),
    }


def deserialize_descriptor(value) -> tuple:
    r, rows = value
    return int(r), tuple(tuple(int(x) for x in row) for row in rows)


def write_deterministic_gzip_json_atomic(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    payload = (stable_json(value) + "\n").encode()
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as handle:
            handle.write(payload)
    os.replace(temporary, path)


def strict_descriptor_audit(outgoing: int) -> dict:
    invariants = invariant_orbit()
    width = len(invariants)
    p = outgoing + 1
    screen = json.loads((CERT / f"screen_n{outgoing}.json").read_text())
    source_rows = defaultdict(list)
    for row in screen["source_rows"]:
        full = deserialize_descriptor(row["descriptor"])
        deck = tuple(restrict_descriptor(full, q) for q in itertools.combinations(range(p), 4))
        source_rows[int(row["signature"])].append((row["mixed_code_sha256"], deck))

    work_path = CERT / f"strict_sign_workcache_n{outgoing}.json.gz"
    if work_path.exists():
        with gzip.open(work_path, "rt") as handle:
            work = json.load(handle)
        if work.get("schema") != "cleanroom-strict-sign-workcache-v1":
            raise ValueError("strict-sign work-cache schema mismatch")
        if work.get("invariant_orbit_sha256") != digest(invariants):
            raise ValueError("strict-sign work-cache invariant mismatch")
        sign_attempts = dict(work["certificates"])
    else:
        sign_attempts = {}

    def checkpoint() -> None:
        body = {
            "schema": "cleanroom-strict-sign-workcache-v1",
            "outgoing": outgoing,
            "invariant_orbit_sha256": digest(invariants),
            "certificates": dict(sorted(sign_attempts.items())),
        }
        body["body_sha256"] = digest(body)
        write_deterministic_gzip_json_atomic(work_path, body)

    sign_cache = {}
    signs = {}
    failures = []
    records = []
    with gzip.open(CERT / f"screen_candidates_n{outgoing}.jsonl.gz", "rt") as handle:
        for line in handle:
            target_row = json.loads(line)
            target_signature = int(target_row["target_signature"])
            compatible = [s for s in source_rows if not (s & ~target_signature) and s != target_signature]
            if not compatible:
                continue
            for presentation in target_row["presentations"]:
                full_target = deserialize_descriptor(presentation["descriptor"])
                target_deck = tuple(restrict_descriptor(full_target, q) for q in itertools.combinations(range(p), 4))
                for source_signature in compatible:
                    difference = target_signature & ~source_signature
                    witness = None
                    while difference:
                        low = difference & -difference
                        absolute = low.bit_length() - 1
                        difference ^= low
                        chunk, invariant_index = divmod(absolute, width)
                        invariant = invariants[invariant_index]
                        source_zero = all(not pullback(deck[chunk], invariant) for _hash, deck in source_rows[source_signature])
                        if not source_zero:
                            continue
                        target_desc = target_deck[chunk]
                        key = (target_desc, invariant_index)
                        if key not in sign_cache:
                            target_poly = pullback(target_desc, invariant)
                            polynomial_key = digest(tuple(sorted(target_poly.items())))
                            if polynomial_key not in sign_attempts:
                                sign_attempts[polynomial_key] = exact_sign_certificate(target_poly)
                                checkpoint()
                            sign_cache[key] = sign_attempts[polynomial_key]
                        certificate = sign_cache[key]
                        if certificate["certified"]:
                            signs[polynomial_key] = certificate
                            witness = {
                                "quartet_chunk": chunk,
                                "quartet": list(tuple(itertools.combinations(range(p), 4))[chunk]),
                                "invariant_index": invariant_index,
                                "source_pullback": "0",
                                "target_pullback_sha256": certificate["exact_polynomial_sha256"],
                                "strict_sign": certificate["strict_sign"],
                            }
                            break
                    record = {
                        "source_signature": str(source_signature),
                        "target_signature": str(target_signature),
                        "target_key": presentation["target_key"],
                        "target_descriptor_sha256": digest(full_target),
                        "witness": witness,
                    }
                    records.append(record)
                    if witness is None:
                        failures.append(record)

    checkpoint()
    records.sort(key=repr)
    write_json(CERT / f"strict_sign_library_n{outgoing}.json", signs)
    with (CERT / f"strict_descriptor_records_n{outgoing}.jsonl.gz").open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as handle:
            for row in records:
                handle.write((stable_json(row) + "\n").encode())
    summary = {
        "schema": "cleanroom-strict-descriptor-audit-v1",
        "outgoing": outgoing,
        "directed_descriptor_relations": len(records),
        "distinct_strict_polynomials": len(signs),
        "failure_count": len(failures),
        "failures": failures[:20],
        "records_sha256": digest(records),
        "sign_library_sha256": digest(signs),
    }
    summary["body_sha256"] = digest(summary)
    write_json(CERT / f"strict_descriptor_audit_n{outgoing}.json", summary)
    return summary


def anchored_source_graphs(outgoing: int) -> dict[str, BuiltGraph]:
    answer = {}
    for template in derive_templates():
        for graph in source_presentations(template, outgoing):
            code, _ = canonical_mixed(graph)
            answer.setdefault(code, graph)
    return answer


def equal_audit(outgoing: int) -> dict:
    screen = json.loads((CERT / f"screen_n{outgoing}.json").read_text())
    source_signature_by_hash = {
        row["mixed_code_sha256"]: int(row["signature"])
        for row in screen["source_rows"]
    }
    source_groups = defaultdict(list)
    for code, graph in anchored_source_graphs(outgoing).items():
        code_hash = digest(code)
        if code_hash not in source_signature_by_hash:
            raise AssertionError(("source screen binding missing", code_hash))
        source_groups[source_signature_by_hash[code_hash]].append((code, graph))

    base_lookup = {}
    for template in derive_templates():
        for base in target_bases(template, outgoing):
            base_lookup[digest(base_record(base))] = base

    records = {}
    failures = []
    counts = defaultdict(int)
    candidate_path = CERT / f"screen_candidates_n{outgoing}.jsonl.gz"
    with gzip.open(candidate_path, "rt") as handle:
        for line in handle:
            candidate = json.loads(line)
            target_signature = int(candidate["target_signature"])
            if target_signature not in source_groups:
                continue
            for presentation in candidate["presentations"]:
                for base_json in presentation["base_records"]:
                    key = digest(base_json)
                    if key not in base_lookup:
                        raise AssertionError(("base transport missing", base_json))
                    base = base_lookup[key]
                    for assignment_json in presentation["assignments"]:
                        assignment = tuple(assignment_json)
                        target_graph = instantiate_target(base, assignment)
                        target_completion_code, target_map = canonical_mixed(target_graph)
                        retained = retains_original_core(base)
                        target_selected_code = target_completion_code if retained else None
                        target_t_code = (
                            canonical_mixed(target_graph, triangle_quotient=True)[0]
                            if retained else None
                        )
                        for source_code, source_graph in source_groups[target_signature]:
                            source_map = canonical_mixed(source_graph)[1]
                            source_t_code = canonical_mixed(source_graph, triangle_quotient=True)[0]
                            relation_body = {
                                "schema": "cleanroom-equal-relation-v1",
                                "outgoing": outgoing,
                                "boundary_count": outgoing + 1,
                                "direction": "source_precedes_target",
                                "source_mixed_code_sha256": digest(source_code),
                                "target_completion_mixed_code_sha256": digest(target_completion_code),
                                "target_selected_mixed_code_sha256": (
                                    digest(target_selected_code) if target_selected_code else None
                                ),
                                "port_correspondence": list(range(outgoing + 1)),
                                "target_incoming_mode": base["incoming_mode"],
                                "target_retains_original_strong_core": retained,
                            }
                            relation_id = digest(relation_body)
                            raw = {
                                "source_rooted_incoming_physical": source_graph.incoming_label,
                                "target_rooted_incoming_physical": target_graph.incoming_label,
                                "target_assignment": list(assignment),
                                "target_base": base_record(base),
                                "source_rooted_provenance": source_graph.provenance,
                                "source_raw_to_canonical_vertex": source_map,
                                "target_raw_to_canonical_vertex": target_map,
                            }
                            prior = records.get(relation_id)
                            if prior is not None:
                                prior["raw_coverage"].append(raw)
                                continue
                            if retained:
                                if source_code == target_selected_code:
                                    classification = "labelled_isomorphism"
                                elif source_t_code == target_t_code:
                                    classification = "ordinary_T"
                                else:
                                    classification = "EQUAL_SIGNATURE_NON_T_RETAINED"
                                    failures.append({**relation_body, "relation_id": relation_id})
                            else:
                                classification = "pending_support_completion"
                            records[relation_id] = {
                                **relation_body,
                                "relation_id": relation_id,
                                "classification": classification,
                                "source_signature": str(target_signature),
                                "source_descriptor_sha256": digest(descriptor(source_graph)),
                                "target_descriptor_sha256": digest(descriptor(target_graph)),
                                "raw_coverage": [raw],
                            }

    for row in records.values():
        row["raw_coverage"] = sorted(row["raw_coverage"], key=lambda x: digest(x))
        row["binding_sha256"] = digest(row)
        counts[row["classification"]] += 1
        counts[f"mode_{row['target_incoming_mode']}_{row['classification']}"] += 1
        fixed = any(
            raw["source_rooted_incoming_physical"] == raw["target_rooted_incoming_physical"]
            for raw in row["raw_coverage"]
            if raw["target_rooted_incoming_physical"] != "D_INCOMING"
        )
        if fixed:
            counts["relations_with_fixed_incoming_representative"] += 1
        else:
            counts["relations_without_fixed_incoming_representative"] += 1

    output = CERT / f"equal_relations_n{outgoing}.jsonl.gz"
    stream_hash = hashlib.sha256()
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as handle:
            for relation_id in sorted(records):
                line = (stable_json(records[relation_id]) + "\n").encode()
                handle.write(line)
                stream_hash.update(line)
    summary = {
        "schema": "cleanroom-equal-audit-v1",
        "outgoing": outgoing,
        "canonical_equal_relations": len(records),
        "counts": dict(sorted(counts.items())),
        "failure_count": len(failures),
        "failures": failures[:20],
        "relation_stream_sha256": stream_hash.hexdigest(),
        "relation_file_sha256": digest(output.read_bytes()),
    }
    summary["body_sha256"] = digest(summary)
    write_json(CERT / f"equal_audit_n{outgoing}.json", summary)
    return summary


def census_only() -> dict:
    templates = derive_templates()
    result = {
        "templates": [],
        "sizes": {},
    }
    for t in templates:
        result["templates"].append({
            "name": t.name, "kinds": t.kinds, "segments": t.segments,
            "sinks": t.sinks, "repairs": t.repairs,
        })
    for n in (3, 4, 5, 6):
        source_graphs_by_code = {}
        bases = []
        for t in templates:
            for graph in source_presentations(t, n):
                code, _ = canonical_mixed(graph)
                source_graphs_by_code.setdefault(code, graph)
            bases.extend(target_bases(t, n))
        source_graphs = list(source_graphs_by_code.values())
        result["sizes"][str(n)] = {
            "source_presentations": len(source_graphs),
            "target_bases": len(bases),
            "target_labelled_full_boundary": len(bases) * math.factorial(n + 1),
            "rejected_fixed_incoming_target_labelled": len(bases) * math.factorial(n),
            "sources_by_template": {
                t.name: len(source_presentations(t, n)) for t in templates
            },
            "target_bases_by_template": {
                t.name: len(target_bases(t, n)) for t in templates
            },
        }
    result["body_sha256"] = digest(result)
    return result


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", action="store_true")
    parser.add_argument("--screen", type=int, choices=(3, 4, 5, 6))
    parser.add_argument("--equal-audit", type=int, choices=(3, 4, 5, 6))
    parser.add_argument("--strict-audit", type=int, choices=(3, 4, 5, 6))
    parser.add_argument("--seed-bits", type=int, choices=(3,))
    args = parser.parse_args()
    if args.census:
        value = census_only()
        write_json(CERT / "cleanroom_census.json", value)
        print(json.dumps(value, indent=2, sort_keys=True))
        return
    if args.screen is not None:
        value = screen_size(args.screen)
        print(json.dumps({k: v for k, v in value.items() if k != "source_rows"}, indent=2, sort_keys=True))
        return
    if args.equal_audit is not None:
        value = equal_audit(args.equal_audit)
        print(json.dumps(value, indent=2, sort_keys=True))
        return
    if args.strict_audit is not None:
        value = strict_descriptor_audit(args.strict_audit)
        print(json.dumps(value, indent=2, sort_keys=True))
        return
    if args.seed_bits is not None:
        value = seed_bits_from_screen(args.seed_bits)
        print(json.dumps(value, indent=2, sort_keys=True))
        return
    parser.error("select a mode")


if __name__ == "__main__":
    main()
