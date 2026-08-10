#!/usr/bin/env python3
"""Compile graph-derived bounded JC feature decks and directed candidates.

The output is a discovery certificate.  Pair-level strict witnesses and the
independent normalized-record comparison are added by later gates.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import hashlib
import gzip
from itertools import combinations, permutations
import json
from pathlib import Path
import time

from completion_universe import INCOMING, Completion, completions
from graph_model import RootedGraph, canonical_mixed, sd0, t_quotient
from jc_tensor import (
    Descriptor,
    invariant_orbit,
    ordered_quartet_deck,
    parse_literal,
    pullback,
    primitive,
)
from sign_certificate import certify as certify_sign


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
TEMPLATE_FILE = PROJECT / "strong_level2_phylo_identifiability" / "src" / "jc_root_spanning_atlas_data.py"
EXPECTED_TEMPLATE_SHA = "dd4b47f018d8f261fe296430513cedc1691b39cdb57fa075e42d884ecfba9ee3"
SUPPORT_CERT = HERE / "certificates" / "support_universe.json"
OUT = HERE / "certificates" / "bounded_atlas_summary.json"


def stable_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def natural(label: str):
    prefix, _, suffix = label.rpartition("_")
    return prefix, int(suffix) if suffix.isdigit() else -1, label


def graph_from_record(row: dict) -> RootedGraph:
    return RootedGraph(
        int(row["root"]),
        tuple((int(v), str(label)) for v, label in row["labels"]),
        tuple((int(u), int(v)) for u, v in row["arcs"]),
    )


def outgoing(graph: RootedGraph) -> tuple[str, ...]:
    return tuple(sorted((label for _, label in graph.labels if label != INCOMING and not label.startswith("D_")), key=natural))


@dataclass(frozen=True)
class BaseModel:
    primitive_id: str
    graph: RootedGraph
    labels: tuple[str, ...]
    ordered: tuple[tuple[tuple[int, int, int], Descriptor], ...]
    selected_strong: bool
    provenance: tuple

    def deck_map(self) -> dict[tuple[int, int, int], Descriptor]:
        return dict(self.ordered)


def deck(graph: RootedGraph, labels: tuple[str, ...]):
    return ordered_quartet_deck(graph, labels, INCOMING)


def model_key(ordered: dict[tuple[int, int, int], Descriptor], n: int):
    return tuple(ordered[triple] for triple in combinations(range(n), 3))


def source_bases(n: int) -> tuple[BaseModel, ...]:
    data = json.loads(SUPPORT_CERT.read_text())
    answer = []
    for index, row in enumerate(data["records"]):
        if int(row["outgoing_count"]) != n:
            continue
        graph = graph_from_record(row)
        labels = outgoing(graph)
        ordered = deck(graph, labels)
        primitive = stable_hash({
            "kind": "source", "core": row["core_id"], "repair": row["repair_index"],
            "words": row["words"], "sink_labels": row["sink_labels"],
            "mixed": canonical_mixed(sd0(graph))[0],
        })
        answer.append(BaseModel(
            primitive, graph, labels, tuple(sorted(ordered.items())), True,
            (row["core_id"], row["repair_index"], row["words"]),
        ))
    return tuple(answer)


def target_bases(n: int) -> tuple[BaseModel, ...]:
    unique: dict[tuple, BaseModel] = {}
    for index, completion in enumerate(completions(n)):
        graph = completion.graph
        labels = tuple(sorted(completion.selected_labels, key=natural))
        ordered = deck(graph, labels)
        key = model_key(ordered, n)
        strong = not completion.dummy_labels
        primitive = stable_hash({
            "kind": "target", "core": completion.core_id,
            "sink_mask": completion.selected_sink_mask,
            "repair": completion.repair_index, "words": completion.words,
            "selected": completion.selected_labels, "dummies": completion.dummy_labels,
            "arcs": graph.arcs, "labels": graph.labels,
        })
        candidate = BaseModel(
            primitive, graph, labels, tuple(sorted(ordered.items())), strong,
            (completion.core_id, completion.selected_sink_mask, completion.repair_index,
             completion.words, completion.dummy_labels),
        )
        previous = unique.get(key)
        if previous is None or (strong and not previous.selected_strong):
            unique[key] = candidate
    return tuple(unique[key] for key in sorted(unique, key=repr))


def descriptor_bits(descriptor: Descriptor, invariants, cache: dict[Descriptor, int]) -> int:
    if descriptor not in cache:
        bits = 0
        for index, invariant in enumerate(invariants):
            if pullback(descriptor, invariant):
                bits |= 1 << index
        cache[descriptor] = bits
    return cache[descriptor]


def labelled_signature(
    base: BaseModel,
    assignment: tuple[int, ...],
    invariants,
    cache: dict[Descriptor, int],
) -> tuple[int, tuple[Descriptor, ...]]:
    n = len(assignment)
    inverse = [0] * n
    for position, actual in enumerate(assignment):
        inverse[actual] = position
    ordered = base.deck_map()
    signature = 0
    descriptors = []
    for chunk, actual_triple in enumerate(combinations(range(n), 3)):
        positional = tuple(inverse[value] for value in actual_triple)
        descriptor = ordered[positional]
        descriptors.append(descriptor)
        signature |= descriptor_bits(descriptor, invariants, cache) << (60 * chunk)
    return signature, tuple(descriptors)


def labelled_records(
    bases: tuple[BaseModel, ...], n: int, invariants, cache,
    *, topology_filter: set[int] | None = None, topology_for_all: bool = False,
):
    records: dict[int, dict] = {}
    raw = 0
    for base in bases:
        for assignment in permutations(range(n)):
            raw += 1
            signature, descriptors = labelled_signature(base, assignment, invariants, cache)
            row = records.setdefault(signature, {
                "presentations": {},
                "strengths": set(),
                "kinds": set(),
                "t_codes": set(),
            })
            # One descriptor presentation per strength/core type is sufficient
            # for strict-witness discovery.  Topology completeness is retained
            # separately as the complete set of T-quotient codes.
            kind = "cycle" if base.provenance[0] == "cycle" else "theta"
            presentation_key = (base.selected_strong, kind)
            row["presentations"].setdefault(presentation_key, (base, assignment, descriptors))
            row["strengths"].add(base.selected_strong)
            row["kinds"].add(kind)
            if topology_for_all or (topology_filter is not None and signature in topology_filter):
                if base.selected_strong:
                    mixed = sd0(relabel_selected(base.graph, base.labels, assignment))
                    row["t_codes"].add(canonical_mixed(t_quotient(mixed))[0])
    return records, raw


def directed_pairs(sources: dict[int, dict], targets: dict[int, dict], chunks: int):
    mask = (1 << 60) - 1
    indexes = []
    for chunk in range(chunks):
        groups: dict[int, list[int]] = defaultdict(list)
        for target in targets:
            groups[(target >> (60 * chunk)) & mask].append(target)
        indexes.append(groups)
    pairs = []
    examined = 0
    for source in sources:
        shortlist = None
        for chunk, groups in enumerate(indexes):
            source_chunk = (source >> (60 * chunk)) & mask
            candidates = []
            for target_chunk, rows in groups.items():
                if source_chunk & ~target_chunk == 0:
                    candidates.extend(rows)
            if shortlist is None or len(candidates) < len(shortlist):
                shortlist = candidates
        assert shortlist is not None
        examined += len(shortlist)
        for target in shortlist:
            if source & ~target == 0:
                pairs.append((source, target))
    return pairs, examined


def relabel_selected(graph: RootedGraph, labels: tuple[str, ...], assignment: tuple[int, ...]) -> RootedGraph:
    mapping = {label: f"L_{actual}" for label, actual in zip(labels, assignment)}
    return RootedGraph(
        graph.root,
        tuple(sorted((v, mapping.get(label, label)) for v, label in graph.labels)),
        graph.arcs,
    )


def equal_topology_audit(common_signatures: set[int], sources: dict[int, dict], targets: dict[int, dict]):
    failures = []
    weak = 0
    checked = 0
    for signature in common_signatures:
        source_t = set(sources[signature]["t_codes"])
        target_t = set(targets[signature]["t_codes"])
        weak += int(False in targets[signature]["strengths"])
        checked += len(source_t) * len(target_t)
        if not target_t or source_t != target_t:
            failures.append({
                "signature_sha": hashlib.sha256(str(signature).encode()).hexdigest(),
                "source_t_classes": len(source_t), "target_t_classes": len(target_t),
                "source_only": sorted(source_t - target_t)[:2],
                "target_only": sorted(target_t - source_t)[:2],
            })
    return {"failures": failures, "common_signatures_also_having_a_weak_presentation": weak, "t_class_comparisons": checked}


def compile_size(n: int, invariants, bit_cache):
    start = time.monotonic()
    sources_base = source_bases(n)
    targets_base = target_bases(n)
    sources, source_raw = labelled_records(
        sources_base, n, invariants, bit_cache, topology_for_all=True,
    )
    targets, target_raw = labelled_records(
        targets_base, n, invariants, bit_cache, topology_filter=set(sources),
    )
    pairs, examined = directed_pairs(sources, targets, math_comb(n, 3))
    equal = {(s, t) for s, t in pairs if s == t}
    strict = len(pairs) - len(equal)
    common = set(sources) & set(targets)
    topology = equal_topology_audit(common, sources, targets)
    strength_signatures: dict[str, int] = defaultdict(int)
    for row in targets.values():
        strength_signatures[repr(tuple(sorted(row["strengths"])))] += 1
    pair_target_kinds: dict[str, int] = defaultdict(int)
    for source, target in pairs:
        for kind in targets[target]["kinds"]:
            pair_target_kinds[kind] += 1
    return {
        "outgoing": n,
        "source_bases": len(sources_base),
        "target_bases": len(targets_base),
        "source_raw_labelled": source_raw,
        "target_raw_labelled": target_raw,
        "source_signatures": len(sources),
        "target_signatures": len(targets),
        "target_signature_strength_status": dict(strength_signatures),
        "common_signatures": len(common),
        "necessary_directed_pairs": len(pairs),
        "equal_pairs": len(equal),
        "strict_pairs": strict,
        "necessary_pairs_by_target_kind_membership": dict(pair_target_kinds),
        "indexed_candidates_examined": examined,
        "topology_audit": topology,
        "signature_pair_commitment": stable_hash(sorted((str(s), str(t)) for s, t in pairs)),
        "elapsed_seconds": time.monotonic() - start,
    }, (sources, targets, pairs)


def compile_relation_records(n: int, working, invariants):
    """Bind every theta-directed necessary pair to graph-derived algebra."""
    sources, targets, pairs = working
    relation_path = HERE / "certificates" / f"theta_relations_n{n}.jsonl.gz"
    sign_path = HERE / "certificates" / f"theta_sign_library_n{n}.json"
    sign_library: dict[str, dict] = {}
    sign_cache: dict[tuple[Descriptor, int], tuple[object, dict]] = {}
    failures = []
    counts = defaultdict(int)
    hasher = hashlib.sha256()

    def presentation(row, kind: str):
        candidates = [
            value for (strength, row_kind), value in row["presentations"].items()
            if row_kind == kind
        ]
        return candidates[0] if candidates else None

    with gzip.open(relation_path, "wt", encoding="utf-8", newline="\n") as handle:
        for source_signature, target_signature in pairs:
            if "theta" not in targets[target_signature]["kinds"]:
                continue
            source_presentation = presentation(sources[source_signature], "theta")
            target_presentation = presentation(targets[target_signature], "theta")
            if source_presentation is None or target_presentation is None:
                failures.append("missing theta presentation")
                continue
            source_base, source_assignment, source_descriptors = source_presentation
            target_base, target_assignment, target_descriptors = target_presentation
            record = {
                "schema": 1,
                "outgoing": n,
                "direction": "source_precedes_target",
                "source_signature_sha256": hashlib.sha256(str(source_signature).encode()).hexdigest(),
                "target_signature_sha256": hashlib.sha256(str(target_signature).encode()).hexdigest(),
                "source_primitive_id": source_base.primitive_id,
                "target_primitive_id": target_base.primitive_id,
                "source_position_to_label": source_assignment,
                "target_position_to_label": target_assignment,
                "port_correspondence": tuple(range(n)),
                "source_roles": source_base.provenance,
                "target_roles": target_base.provenance,
                "source_descriptor_deck_sha256": stable_hash(source_descriptors),
                "target_descriptor_deck_sha256": stable_hash(target_descriptors),
            }
            if source_signature == target_signature:
                source_codes = sorted(sources[source_signature]["t_codes"])
                target_codes = sorted(targets[target_signature]["t_codes"])
                if source_codes != target_codes or not source_codes:
                    failures.append({"equal_signature_not_T": record})
                    continue
                record["classification"] = "isomorphism_or_T"
                record["t_quotient_code_sha256"] = hashlib.sha256(source_codes[0].encode()).hexdigest()
                counts["equal"] += 1
            else:
                difference = target_signature & ~source_signature
                witness = None
                while difference:
                    lowest = difference & -difference
                    absolute_bit = lowest.bit_length() - 1
                    difference ^= lowest
                    chunk, invariant_index = divmod(absolute_bit, 60)
                    source_poly = pullback(source_descriptors[chunk], invariants[invariant_index])
                    target_poly = pullback(target_descriptors[chunk], invariants[invariant_index])
                    if source_poly or not target_poly:
                        continue
                    cache_key = target_descriptors[chunk], invariant_index
                    if cache_key not in sign_cache:
                        sign_cache[cache_key] = target_poly, certify_sign(target_poly)
                    _poly, sign = sign_cache[cache_key]
                    if sign["certified"]:
                        poly_hash = sign["polynomial_sha256"]
                        sign_library.setdefault(poly_hash, sign)
                        witness = {
                            "quartet_chunk": chunk,
                            "invariant_index": invariant_index,
                            "source_pullback": "0",
                            "target_pullback_sha256": poly_hash,
                            "target_pullback_primitive_sha256": hashlib.sha256(repr(primitive(target_poly)).encode()).hexdigest(),
                            "strict_sign": sign["strict_sign"],
                        }
                        break
                if witness is None:
                    failures.append({"no_strict_witness": record})
                    continue
                record["classification"] = "strict_open_cube_separation"
                record["witness"] = witness
                counts["strict"] += 1
            record["relation_id"] = stable_hash({
                "source": record["source_primitive_id"],
                "target": record["target_primitive_id"],
                "source_assignment": record["source_position_to_label"],
                "target_assignment": record["target_position_to_label"],
                "direction": record["direction"],
                "ports": record["port_correspondence"],
            })
            record["binding_sha256"] = stable_hash(record)
            line = json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
            handle.write(line)
            hasher.update(line.encode())
    sign_path.write_text(json.dumps(sign_library, sort_keys=True, indent=2) + "\n")
    return {
        "relation_path": str(relation_path.relative_to(HERE.parent)),
        "relation_stream_sha256": hasher.hexdigest(),
        "sign_library_path": str(sign_path.relative_to(HERE.parent)),
        "sign_library_sha256": sha256(sign_path),
        "counts": dict(counts),
        "distinct_strict_polynomials": len(sign_library),
        "failures": failures[:20],
        "failure_count": len(failures),
    }


def math_comb(n: int, k: int) -> int:
    value = 1
    for i in range(k):
        value = value * (n - i) // (i + 1)
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=(5, 6))
    parser.add_argument("--relations", action="store_true")
    args = parser.parse_args()
    template_sha = sha256(TEMPLATE_FILE)
    if template_sha != EXPECTED_TEMPLATE_SHA:
        raise SystemExit(f"inert invariant template hash changed: {template_sha}")
    templates = parse_literal(TEMPLATE_FILE, "INVARIANT_TEMPLATES")
    invariants = invariant_orbit(templates)
    if len(invariants) != 60:
        raise AssertionError(len(invariants))
    cache: dict[Descriptor, int] = {}
    runs = []
    for n in args.sizes:
        row, working = compile_size(n, invariants, cache)
        if args.relations:
            row["theta_relation_certificate"] = compile_relation_records(n, working, invariants)
            if row["theta_relation_certificate"]["failure_count"]:
                raise SystemExit(f"relation failures at n={n}")
        runs.append(row)
        print(json.dumps(row, sort_keys=True), flush=True)
    payload = {
        "schema": 1,
        "template_path": str(TEMPLATE_FILE.relative_to(PROJECT)),
        "template_sha256": template_sha,
        "invariant_orbit_size": len(invariants),
        "descriptor_types_exactly_expanded": len(cache),
        "runs": runs,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"output": str(OUT), "descriptor_types": len(cache)}, sort_keys=True))


if __name__ == "__main__":
    main()
