#!/usr/bin/env python3
"""End-to-end decorated cycle-source/theta-target JC separation compiler.

The compiler closes the only bounded-support direction in which a weak theta
restriction can hide its second reticulation from a rigid cycle support.  It
does not read a historical topology id, signature table, relation table, or
separator assignment.  Every record is regenerated through

    graph -> switchings -> descendant masks -> exact JC tensor -> pullback.

Selected four-port equalities are completed by restoring every omitted theta
repair/sink port and, independently, inserting the same labels in every
possible ordered position of the cycle source.  The resulting decorated
directed relations are then separated by a strict three-port F polynomial or
by one of the multihomogeneous quartet invariants.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import argparse
import gzip
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path

from atlas_compiler import (
    EXPECTED_SEVENTH_SHA,
    EXPECTED_TEMPLATE_SHA,
    INCOMING,
    SEVENTH_TEMPLATE_FILE,
    TEMPLATE_FILE,
    descriptor_bits,
    labelled_signature,
    sha256,
    stable_hash,
)
from completion_universe import build_graph, completions, core_rows
from graph_model import RootedGraph, canonical_mixed, mixed_local_strong, rooted_validation, sd0
from jc_tensor import (
    Descriptor,
    all_port_quartet_deck,
    canonical_descriptor,
    invariant_orbit,
    parse_literal,
    pullback,
    primitive,
    trinet_F_pullback,
)
from sign_certificate import certify as certify_sign


HERE = Path(__file__).resolve().parent
OUT = HERE / "certificates" / "cycle_theta_union_summary.json"
RELATIONS = HERE / "certificates" / "cycle_theta_union_relations.jsonl.gz"
SIGNS = HERE / "certificates" / "cycle_theta_union_signs.json"


@dataclass(frozen=True)
class CyclePresentation:
    outgoing: int
    sink: int
    words: tuple[tuple[int, ...], tuple[int, ...]]
    graph: RootedGraph
    mixed_code: str
    signature: int | None
    descriptors: tuple[Descriptor, ...]


def load_invariants():
    if sha256(TEMPLATE_FILE) != EXPECTED_TEMPLATE_SHA:
        raise AssertionError("six-template source changed")
    if sha256(SEVENTH_TEMPLATE_FILE) != EXPECTED_SEVENTH_SHA:
        raise AssertionError("seventh-template source changed")
    templates = parse_literal(TEMPLATE_FILE, "INVARIANT_TEMPLATES")
    payload = json.loads(SEVENTH_TEMPLATE_FILE.read_text())
    seventh = tuple(
        (tuple(int(index) + 1 for index in monomial), int(coefficient))
        for coefficient, monomial in payload["invariant"]
    )
    orbit = invariant_orbit((*templates, seventh))
    if len(orbit) != 84:
        raise AssertionError(len(orbit))
    return orbit


def relabel(graph: RootedGraph, mapping: dict[str, str]) -> RootedGraph:
    return RootedGraph(
        graph.root,
        tuple(sorted((vertex, mapping.get(label, label)) for vertex, label in graph.labels)),
        graph.arcs,
    )


def fixed_deck(graph: RootedGraph, outgoing: int):
    labels = tuple(f"L_{index}" for index in range(outgoing))
    complete = all_port_quartet_deck(graph, labels, INCOMING)
    descriptors = tuple(complete[quartet] for quartet in combinations(range(outgoing + 1), 4))
    return complete, descriptors


def fixed_signature(descriptors, invariants, cache):
    signature = 0
    for chunk, descriptor in enumerate(descriptors):
        signature |= descriptor_bits(descriptor, invariants, cache) << (len(invariants) * chunk)
    return signature


def cycle_core():
    rows = [row for row in core_rows() if row["id"] == "cycle"]
    if len(rows) != 1:
        raise AssertionError(len(rows))
    return rows[0]


def normalized_words(words):
    return tuple(sorted((tuple(words[0]), tuple(words[1]))))


def cycle_presentations(outgoing: int, invariants, cache, *, compute_signature: bool = True):
    core = cycle_core()
    arcs = core["arcs"]
    _source, sinks = __import__("completion_universe").source_and_sinks(arcs)
    if len(sinks) != 1:
        raise AssertionError(sinks)
    records = {}
    labels = tuple(range(outgoing))
    for sink in labels:
        ordinary = tuple(value for value in labels if value != sink)
        for order in permutations(ordinary):
            for cut in range(len(order) + 1):
                words_int = (tuple(order[:cut]), tuple(order[cut:]))
                words = tuple(tuple(f"L_{value}" for value in word) for word in words_int)
                graph = build_graph(arcs, words, {sinks[0]: f"L_{sink}"})
                valid, problems = rooted_validation(graph)
                if not valid:
                    raise AssertionError(problems)
                mixed = sd0(graph)
                if not mixed_local_strong(mixed):
                    raise AssertionError("cycle presentation not S_TC")
                code = canonical_mixed(mixed)[0]
                if compute_signature:
                    _deck, descriptors = fixed_deck(graph, outgoing)
                    signature = fixed_signature(descriptors, invariants, cache)
                else:
                    descriptors = ()
                    signature = None
                key = code
                candidate = CyclePresentation(
                    outgoing, sink, normalized_words(words_int), graph, code, signature, descriptors,
                )
                prior = records.get(key)
                if prior is not None and (prior.sink, prior.words, prior.signature) != (
                    candidate.sink, candidate.words, candidate.signature
                ):
                    raise AssertionError("cycle canonicalization merged incompatible roles")
                records[key] = candidate
    return tuple(records[key] for key in sorted(records))


def extension_candidates(source: CyclePresentation, total: int, all_cycles):
    old = source.outgoing
    answer = []
    for candidate in all_cycles:
        if candidate.sink != source.sink:
            continue
        restricted = tuple(tuple(value for value in word if value < old) for word in candidate.words)
        if normalized_words(restricted) == source.words:
            answer.append(candidate)
    return tuple(answer)


def selected_theta_equalities(invariants, cache, source_by_signature):
    """Return every decorated weak-theta four-port equality presentation."""
    records = {}
    raw = 0
    for completion in completions(4):
        if completion.core_id == "cycle":
            continue
        labels = tuple(sorted(completion.selected_labels))
        ordered = all_port_quartet_deck(completion.graph, labels, INCOMING)
        # Use the same transport routine as the bounded compiler, but retain
        # every full graph/dummy-role presentation instead of one signature
        # representative.
        base = type("Deck", (), {"deck_map": lambda self, value=ordered: value})()
        for assignment in permutations(range(4)):
            raw += 1
            signature, descriptors = labelled_signature(base, assignment, invariants, cache)
            source = source_by_signature.get(signature)
            if source is None:
                continue
            mapping = {label: f"L_{actual}" for label, actual in zip(labels, assignment)}
            graph = relabel(completion.graph, mapping)
            full_code = canonical_mixed(sd0(graph))[0]
            dummy_roles = tuple(sorted(completion.dummy_labels))
            record = {
                "source_code": source.mixed_code,
                "source_signature_sha256": hashlib.sha256(str(signature).encode()).hexdigest(),
                "target_selected_code": full_code,
                "target_graph": graph,
                "target_core": completion.core_id,
                "target_repair_index": completion.repair_index,
                "target_words": completion.words,
                "target_selected_sink_mask": completion.selected_sink_mask,
                "dummy_roles": dummy_roles,
                "selected_mapping": tuple(sorted(mapping.items())),
                "target_descriptor_sha256": stable_hash(descriptors),
            }
            key = stable_hash({
                "source": source.mixed_code,
                "target": full_code,
                "dummy_roles": dummy_roles,
                "selected_mapping": record["selected_mapping"],
            })
            records.setdefault(key, record)
    return raw, tuple(records[key] for key in sorted(records))


def completed_targets(equality):
    graph = equality["target_graph"]
    dummies = equality["dummy_roles"]
    old = 4
    answer = {}
    for assignment in permutations(range(old, old + len(dummies))):
        mapping = {dummy: f"L_{label}" for dummy, label in zip(dummies, assignment)}
        completed = relabel(graph, mapping)
        valid, problems = rooted_validation(completed)
        if not valid:
            raise AssertionError(problems)
        mixed = sd0(completed)
        if not mixed_local_strong(mixed):
            raise AssertionError("restored theta support is not S_TC")
        code = canonical_mixed(mixed)[0]
        answer.setdefault(code, {
            "graph": completed,
            "mixed_code": code,
            "dummy_assignment": tuple(sorted(mapping.items())),
        })
    return tuple(answer[key] for key in sorted(answer))


def relation_witness(source, target, total, invariants, sign_cache, sign_library):
    # The cycle's unique sink is excluded.  Every such trinet is a tree
    # marginal and therefore has F=0; the exact assertion is replayed for
    # every compiled source graph rather than assumed from the role label.
    labels = tuple(range(total))
    for triple in combinations((value for value in labels if value != source.sink), 3):
        names = tuple(f"L_{value}" for value in triple)
        source_descriptor = canonical_descriptor(source.graph, names)
        target_descriptor = canonical_descriptor(target["graph"], names)
        source_poly = trinet_F_pullback(source_descriptor)
        if source_poly:
            raise AssertionError("cycle F identity failed away from its sink")
        target_poly = trinet_F_pullback(target_descriptor)
        if not target_poly:
            continue
        key = ("F", target_descriptor)
        if key not in sign_cache:
            sign_cache[key] = certify_sign(target_poly)
        sign = sign_cache[key]
        if sign["certified"]:
            sign_library.setdefault(sign["polynomial_sha256"], sign)
            return {
                "kind": "trinet_F",
                "ports": triple,
                "zero_side": "cycle_source",
                "nonzero_side": "theta_target",
                "target_polynomial_sha256": sign["polynomial_sha256"],
                "strict_sign": sign["strict_sign"],
            }

    source_deck, source_descriptors = fixed_deck(source.graph, total)
    target_deck, target_descriptors = fixed_deck(target["graph"], total)
    del source_deck, target_deck
    for chunk, (source_descriptor, target_descriptor) in enumerate(
        zip(source_descriptors, target_descriptors)
    ):
        for invariant_index, invariant in enumerate(invariants):
            source_poly = pullback(source_descriptor, invariant)
            target_poly = pullback(target_descriptor, invariant)
            if bool(source_poly) == bool(target_poly):
                continue
            nonzero_side = "cycle_source" if source_poly else "theta_target"
            descriptor = source_descriptor if source_poly else target_descriptor
            polynomial = source_poly if source_poly else target_poly
            key = ("I", descriptor, invariant_index)
            if key not in sign_cache:
                sign_cache[key] = certify_sign(polynomial)
            sign = sign_cache[key]
            if sign["certified"]:
                sign_library.setdefault(sign["polynomial_sha256"], sign)
                return {
                    "kind": "quartet_invariant",
                    "quartet_chunk": chunk,
                    "invariant_index": invariant_index,
                    "zero_side": "theta_target" if source_poly else "cycle_source",
                    "nonzero_side": nonzero_side,
                    "polynomial_sha256": sign["polynomial_sha256"],
                    "strict_sign": sign["strict_sign"],
                }
    return None


def compile_relations(invariants, cache, sources, equalities):
    source_by_code = {source.mixed_code: source for source in sources}
    cycles_by_total = {
        total: cycle_presentations(total, invariants, cache, compute_signature=False)
        for total in range(5, 8)
    }
    extension_cache = {}
    sign_cache = {}
    sign_library = {}
    relation_ids = set()
    failures = []
    counts = defaultdict(int)
    hasher = hashlib.sha256()
    with gzip.open(RELATIONS, "wt", encoding="utf-8", newline="\n") as handle:
        for equality_index, equality in enumerate(equalities):
            source0 = source_by_code[equality["source_code"]]
            missing = len(equality["dummy_roles"])
            if missing not in (1, 2, 3):
                failures.append({"equality": equality_index, "unexpected_missing": missing})
                continue
            total = 4 + missing
            extension_key = source0.mixed_code, total
            if extension_key not in extension_cache:
                extension_cache[extension_key] = extension_candidates(
                    source0, total, cycles_by_total[total]
                )
            source_extensions = extension_cache[extension_key]
            target_completions = completed_targets(equality)
            counts[f"equalities_missing_{missing}"] += 1
            counts[f"source_extensions_missing_{missing}"] += len(source_extensions)
            counts[f"target_completions_missing_{missing}"] += len(target_completions)
            for source in source_extensions:
                for target in target_completions:
                    relation_id = stable_hash({
                        "direction": "cycle_source_precedes_theta_target",
                        "source": source.mixed_code,
                        "target": target["mixed_code"],
                        "ports": tuple(range(total)),
                        "parent_source": source0.mixed_code,
                        "parent_target": equality["target_selected_code"],
                    })
                    if relation_id in relation_ids:
                        continue
                    relation_ids.add(relation_id)
                    witness = relation_witness(
                        source, target, total, invariants, sign_cache, sign_library
                    )
                    row = {
                        "schema": 1,
                        "relation_id": relation_id,
                        "direction": "cycle_source_precedes_theta_target",
                        "outgoing": total,
                        "source_mixed_code_sha256": hashlib.sha256(source.mixed_code.encode()).hexdigest(),
                        "target_mixed_code_sha256": hashlib.sha256(target["mixed_code"].encode()).hexdigest(),
                        "source_sink_label": source.sink,
                        "source_words": source.words,
                        "target_core": equality["target_core"],
                        "target_dummy_assignment": target["dummy_assignment"],
                        "port_correspondence": tuple(range(total)),
                        "witness": witness,
                    }
                    if witness is None:
                        failures.append(row)
                        row["classification"] = "UNRESOLVED"
                    else:
                        row["classification"] = "strict_open_cube_separation"
                        counts[f"witness_{witness['kind']}"] += 1
                    row["binding_sha256"] = stable_hash(row)
                    line = json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
                    handle.write(line)
                    hasher.update(line.encode())
    SIGNS.write_text(json.dumps(sign_library, sort_keys=True, indent=2) + "\n")
    return {
        "canonical_decorated_relations": len(relation_ids),
        "relation_stream_sha256": hasher.hexdigest(),
        "relation_file_sha256": sha256(RELATIONS),
        "sign_library_sha256": sha256(SIGNS),
        "distinct_strict_polynomials": len(sign_library),
        "counts": dict(sorted(counts.items())),
        "failure_count": len(failures),
        "failures": failures[:20],
        "cycle_extension_counts": {
            str(total): len(cycles) for total, cycles in sorted(cycles_by_total.items())
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()
    invariants = load_invariants()
    cache = {}
    sources = cycle_presentations(4, invariants, cache)
    source_by_signature = {}
    for source in sources:
        if source.signature in source_by_signature:
            raise AssertionError("two labelled cycle topologies share a full invariant deck")
        source_by_signature[source.signature] = source
    raw, equalities = selected_theta_equalities(invariants, cache, source_by_signature)
    relation = compile_relations(invariants, cache, sources, equalities)
    payload = {
        "schema": 1,
        "status": "EXACTLY_COMPUTED" if not relation["failure_count"] else "UNRESOLVED",
        "scope": "all cycle rigid-support four-port equalities completed by every omitted theta support role",
        "invariant_orbit_size": len(invariants),
        "cycle_source_presentations": len(sources),
        "raw_theta_labelled_presentations_examined": raw,
        "decorated_selected_equalities": len(equalities),
        "descriptor_types": len(cache),
        "relation_certificate": relation,
    }
    OUT.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps(payload, sort_keys=True, indent=2))
    if relation["failure_count"]:
        raise SystemExit("unresolved cycle-to-theta completed relation")


if __name__ == "__main__":
    main()
