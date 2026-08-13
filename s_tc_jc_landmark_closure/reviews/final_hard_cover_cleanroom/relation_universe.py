"""Independent four-boundary source and target completion universe."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import itertools
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from graph_model import (
    RootedGraph, build_from_skeleton, digest, recover_template, rooted_code,
    stable_json, standard_semidirected_audit, validate_standard_strong,
    weak_compositions,
)


def natural_key(s: str):
    return tuple(int(x) if x.isdigit() else x for x in re.split(r"(\d+)", s))


@dataclass(frozen=True)
class Template:
    template_id: str
    core_id: str
    repair_index: int
    skeleton: RootedGraph
    segment_edges: Tuple[Tuple[int, int], ...]
    repair_segments: Tuple[int, ...]
    incoming_leaf: int
    sink_leaves: Tuple[int, ...]
    sink_names: Tuple[str, ...]


@dataclass(frozen=True)
class SourceSupport:
    source_id: str
    core_id: str
    graph: RootedGraph
    skeleton: RootedGraph
    segment_edges: Tuple[Tuple[int, int], ...]
    words: Tuple[Tuple[str, ...], ...]
    role_to_label: Tuple[Tuple[str, str], ...]


@dataclass(frozen=True)
class Completion:
    completion_id: str
    core_id: str
    graph: RootedGraph
    incoming_selected: bool
    dummy_order: Tuple[str, ...]
    selected_leaf_order: Tuple[int, ...]
    origin_ids: Tuple[str, ...]


def load_support(path: Path):
    obj = json.loads(path.read_text())
    if obj.get("schema") != 1 or not obj.get("all_supports_pointwise_rigid"):
        raise ValueError("unexpected support input")
    return obj["records"]


def load_cores(path: Path):
    obj = json.loads(path.read_text())
    if obj.get("schema") != 1 or len(obj.get("cores", [])) != 5:
        raise ValueError("unexpected core input")
    return {x["id"]: x for x in obj["cores"]}


def templates(records, cores) -> List[Template]:
    """One orientation core times every non-equivalent minimum repair.

    The pointwise-labelled support table has already quotiented a repair that
    becomes symmetric after its repair labels are fixed.  Four *unselected*
    boundary slots can break that symmetry.  We therefore take the complete
    minimum-repair list from the primitive core record, except for the
    rank-one cycle where the two paths are the declared template automorphism.
    """
    ans = []
    by_core = defaultdict(list)
    for r in records:
        if r["extra_count"] == 0: by_core[r["core_id"]].append(r)
    for core_id in sorted(by_core):
        r = sorted(by_core[core_id], key=lambda x: int(x["repair_index"]))[0]
        sk, edges, _ = recover_template(r, records)
        lm = sk.label_map
        incoming = [v for v, c in lm.items() if c == "INCOMING"]
        sinks = sorted((c, v) for v, c in lm.items() if c.startswith("Q_SINK"))
        if len(incoming) != 1: raise ValueError("missing structural incoming")
        repair_sets = [tuple(int(x) for x in z) for z in cores[core_id]["minimum_repairs"]]
        if core_id == "cycle": repair_sets = [repair_sets[0]]
        for repair_index, repair_set in enumerate(repair_sets):
            t_obj = {
                "core": core_id, "repair": repair_index,
                "rooted_skeleton": rooted_code(sk)[0],
                "segments": list(edges), "repair_segments": list(repair_set),
            }
            ans.append(Template(
                digest(t_obj), core_id, repair_index, sk, edges,
                repair_set, incoming[0], tuple(v for _, v in sinks),
                tuple(c for c, _ in sinks),
            ))
    if len(ans) != 11: raise AssertionError(("minimum repair templates", len(ans)))
    return ans


def _canonical_relabel_completion(g: RootedGraph):
    """Assign deterministic selected slots and dummy identities after setwise quotient."""
    lm = g.label_map
    generic_labels = {}
    for v, c in lm.items():
        if c.startswith("D_REPAIR"): generic_labels[v] = "D_REPAIR"
        elif c.startswith("D_SINK"): generic_labels[v] = "D_SINK"
        else: generic_labels[v] = c
    generic_graph = RootedGraph.make(g.arcs, g.root, generic_labels)
    generic_code, order = rooted_code(generic_graph, selected_generic=True)
    pos = {v: i for i, v in enumerate(order)}
    selected = sorted((v for v, c in lm.items() if c.startswith("L_SLOT")), key=pos.get)
    if not selected: raise ValueError("no selected boundaries")
    by_dummy = defaultdict(list)
    for v, c in lm.items():
        if c.startswith("D_REPAIR"): by_dummy["D_REPAIR"].append(v)
        elif c.startswith("D_SINK"): by_dummy["D_SINK"].append(v)
        elif c == "D_INCOMING": by_dummy["D_INCOMING"].append(v)
    new = dict(lm)
    for i, v in enumerate(selected): new[v] = f"L_{i}"
    for kind in ("D_REPAIR", "D_SINK"):
        for i, v in enumerate(sorted(by_dummy[kind], key=pos.get)): new[v] = f"{kind}_{i}"
    for v in by_dummy["D_INCOMING"]: new[v] = "D_INCOMING"
    out = RootedGraph.make(g.arcs, g.root, new)
    final_code, _ = rooted_code(out)
    dummies = []
    if by_dummy["D_INCOMING"]: dummies.append("D_INCOMING")
    dummies.extend(f"D_REPAIR_{i}" for i in range(len(by_dummy["D_REPAIR"])))
    dummies.extend(f"D_SINK_{i}" for i in range(len(by_dummy["D_SINK"])))
    return generic_code, final_code, out, tuple(selected), tuple(dummies)


def generate_completions(ts: Sequence[Template], selected_total: int = 4) -> List[Completion]:
    """All ``selected_total``-port standard-strong target completions.

    Selected ports are first treated as one colour.  This quotients structural
    duplicates before the full S4 physical-label action is applied later.
    """
    merged: Dict[str, Tuple[RootedGraph, bool, Tuple[str, ...], Tuple[int, ...], str, Tuple[str, ...]]] = {}
    for t in ts:
        s = len(t.segment_edges); sink_count = len(t.sink_leaves)
        for incoming_selected in (False, True):
            for sink_bits in itertools.product((0, 1), repeat=sink_count):
                ordinary = selected_total - int(incoming_selected) - sum(sink_bits)
                if ordinary < 0: continue
                for counts in weak_compositions(ordinary, s):
                    words = [[] for _ in range(s)]; slot = 0
                    for i, n in enumerate(counts):
                        for _ in range(n): words[i].append(f"L_SLOT_{slot}"); slot += 1
                    for i in t.repair_segments:
                        if counts[i] == 0: words[i].append(f"D_REPAIR_RAW_{i}")
                    fixed = {}
                    if incoming_selected:
                        fixed["INCOMING"] = f"L_SLOT_{slot}"; slot += 1
                    else: fixed["INCOMING"] = "D_INCOMING"
                    for sink_i, (bit, name) in enumerate(zip(sink_bits, t.sink_names)):
                        if bit:
                            fixed[name] = f"L_SLOT_{slot}"; slot += 1
                        else: fixed[name] = f"D_SINK_RAW_{sink_i}"
                    if slot != selected_total: raise AssertionError(slot)
                    g = build_from_skeleton(t.skeleton, t.segment_edges, words, fixed)
                    check = validate_standard_strong(g)
                    if not check["ok"]: raise AssertionError((t.core_id, t.repair_index, counts, check))
                    sd_check = standard_semidirected_audit(g)
                    if not sd_check["ok"]:
                        raise AssertionError((t.core_id, t.repair_index, counts, "standard S_TC", sd_check))
                    generic, final, out, selected, dummies = _canonical_relabel_completion(g)
                    origin_id = digest({
                        "template": t.template_id, "incoming_selected": incoming_selected,
                        "sink_bits": sink_bits, "ordinary_counts": counts,
                    })
                    # Incoming-selected is structurally visible in the final rooted graph but
                    # retained explicitly as an audit assertion.
                    key = generic
                    if key in merged:
                        old = merged[key]
                        merged[key] = old[:-1] + (old[-1] + (origin_id,),)
                    else:
                        merged[key] = (out, incoming_selected, dummies, selected, t.core_id, (origin_id,))
    ans = []
    for generic in sorted(merged):
        g, inc, dummies, selected, core, origins = merged[generic]
        final, order = rooted_code(g)
        lm = g.label_map; pos = {v: i for i, v in enumerate(order)}
        selected = tuple(sorted((v for v, c in lm.items() if c.startswith("L_")), key=lambda v: int(lm[v].split("_")[1])))
        cid = digest({"generic_rooted_graph": generic})
        ans.append(Completion(cid, core, g, inc, dummies, selected, tuple(sorted(origins))))
    return ans


def generate_sources(records, outgoing_count: int = 3, minimum_only: bool = False) -> List[SourceSupport]:
    ans = []
    for r in records:
        if int(r["outgoing_count"]) != outgoing_count: continue
        if minimum_only and int(r["extra_count"]) != 0: continue
        sk, edges, words0 = recover_template(r, records)
        roles = [c for _, c in r["labels"]]
        ordered = ["INCOMING"] + sorted((x for x in roles if x != "INCOMING"), key=natural_key)
        role_to = {role: f"L_{i}" for i, role in enumerate(ordered)}
        words = tuple(tuple(role_to[x] for x in w) for w in words0)
        g = build_from_skeleton(sk, edges, words, role_to)
        check = validate_standard_strong(g)
        if not check["ok"]: raise AssertionError((r["core_id"], check))
        sd_check = standard_semidirected_audit(g)
        if not sd_check["ok"]: raise AssertionError((r["core_id"], "standard S_TC", sd_check))
        sid = digest({"rooted_graph": rooted_code(g)[0]})
        ans.append(SourceSupport(sid, r["core_id"], g, sk, edges, words, tuple(sorted(role_to.items()))))
    # Exact pointwise-labelled graph quotient; no topology identifier is used.
    unique = {rooted_code(x.graph)[0]: x for x in ans}
    if outgoing_count == 3 and not minimum_only and len(unique) != 8:
        raise AssertionError(("source support count", len(ans), len(unique)))
    return [unique[k] for k in sorted(unique)]


def relabel_selected(g: RootedGraph, permutation: Sequence[int]) -> RootedGraph:
    lm = g.label_map; new = {}
    for v, c in lm.items():
        if c.startswith("L_"):
            old = int(c.split("_")[1]); new[v] = f"L_{permutation[old]}"
        else: new[v] = c
    return RootedGraph.make(g.arcs, g.root, new)


def universe_summary(sources, completions):
    return {
        "source_supports": len(sources),
        "completion_bases": len(completions),
        "completion_origins_before_quotient": sum(len(x.origin_ids) for x in completions),
        "by_core": {c: sum(x.core_id == c for x in completions) for c in sorted({x.core_id for x in completions})},
        "by_incoming_selected": {str(b).lower(): sum(x.incoming_selected == b for x in completions) for b in (False, True)},
        "by_dummy_count": {str(k): sum(len(x.dummy_order) == k for x in completions) for k in sorted({len(x.dummy_order) for x in completions})},
    }


def graph_object(g: RootedGraph):
    return {"root": g.root, "arcs": [list(e) for e in g.arcs], "labels": [[v, c] for v, c in g.labels]}


def graph_from_object(obj):
    return RootedGraph.make(obj["arcs"], obj["root"], dict(obj["labels"]))


def completion_object(c: Completion):
    return {
        "completion_id": c.completion_id, "core_id": c.core_id,
        "graph": graph_object(c.graph), "incoming_selected": c.incoming_selected,
        "dummy_order": list(c.dummy_order), "origin_ids": list(c.origin_ids),
        "standard_semidirected_audit": standard_semidirected_audit(c.graph),
    }


def source_object(s: SourceSupport):
    return {
        "source_id": s.source_id, "core_id": s.core_id, "graph": graph_object(s.graph),
        "skeleton": graph_object(s.skeleton), "segment_edges": [list(e) for e in s.segment_edges],
        "words": [list(w) for w in s.words], "role_to_label": [list(x) for x in s.role_to_label],
        "standard_semidirected_audit": standard_semidirected_audit(s.graph),
    }
