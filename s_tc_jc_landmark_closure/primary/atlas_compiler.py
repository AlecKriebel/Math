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
from itertools import chain, combinations, permutations
import json
from pathlib import Path
import time

from completion_universe import (
    INCOMING,
    Completion,
    completions,
    marginal_incoming_completions,
    selected_graph,
    selected_retains_strong_core,
)
from graph_model import (
    RootedGraph,
    canonical_mixed,
    mixed_local_strong,
    rooted_validation,
    sd0,
    t_quotient,
)
from jc_tensor import (
    Descriptor,
    all_port_quartet_deck,
    coordinate_values_mod,
    invariant_value_mod,
    invariant_orbit,
    parse_literal,
    pullback,
    pullbacks_shared,
    primitive,
)
from sign_certificate import certify as certify_sign


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
TEMPLATE_FILE = PROJECT / "strong_level2_phylo_identifiability" / "src" / "jc_root_spanning_atlas_data.py"
EXPECTED_TEMPLATE_SHA = "dd4b47f018d8f261fe296430513cedc1691b39cdb57fa075e42d884ecfba9ee3"
SEVENTH_TEMPLATE_FILE = HERE / "seventh_invariant.json"
EXPECTED_SEVENTH_SHA = "f737f9bee9cc04045355416b95629c18cb5aa9bc31d9719e319eb0a3907babed"
SUPPORT_CERT = HERE / "certificates" / "support_universe.json"
OUT = HERE / "certificates" / "bounded_atlas_summary.json"
BIT_CACHE_FILE = HERE / "certificates" / "descriptor_bits_cache.json.gz"


def stable_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_bit_cache(path: Path, cache: dict[Descriptor, int]) -> None:
    rows = [
        {
            "descriptor": [retics, [list(row) for row in signatures]],
            "bits": str(bits),
        }
        for (retics, signatures), bits in sorted(cache.items())
    ]
    payload = json.dumps({"schema": 1, "rows": rows}, sort_keys=True, separators=(",", ":"))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as handle:
            handle.write((payload + "\n").encode())


def load_bit_cache(path: Path) -> dict[Descriptor, int]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        payload = json.load(handle)
    if payload.get("schema") != 1:
        raise ValueError("unsupported descriptor-bit cache schema")
    answer = {}
    for row in payload["rows"]:
        retics, signatures = row["descriptor"]
        descriptor = int(retics), tuple(tuple(int(x) for x in values) for values in signatures)
        bits = int(row["bits"])
        prior = answer.setdefault(descriptor, bits)
        if prior != bits:
            raise ValueError("descriptor-bit cache conflict")
    return answer


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
class ModelVariant:
    primitive_id: str
    graph: RootedGraph
    labels: tuple[str, ...]
    retains_strong_core: bool
    provenance: tuple
    topology_graph: RootedGraph | None
    dummy_labels: tuple[str, ...]
    incoming_selected: bool


@dataclass(frozen=True)
class BaseModel:
    primitive_id: str
    graph: RootedGraph
    labels: tuple[str, ...]
    ordered: tuple[tuple[tuple[int, int, int, int], Descriptor], ...]
    retains_strong_core: bool
    provenance: tuple
    variants: tuple[ModelVariant, ...]

    def deck_map(self) -> dict[tuple[int, int, int, int], Descriptor]:
        return dict(self.ordered)


def deck(graph: RootedGraph, labels: tuple[str, ...]):
    if len(labels) < 4:
        raise ValueError("the quartet deck needs at least four selected boundaries")
    # The tensor compiler treats its last argument only as the final ordered
    # label.  It need not be the rooted presentation's structural incoming
    # leaf; this is how a zero-character incoming boundary is marginalized.
    return all_port_quartet_deck(graph, labels[:-1], labels[-1])


def model_key(ordered: dict[tuple[int, int, int, int], Descriptor], n: int):
    # A canonical unlabelled base key may use increasing positions.  Labelled
    # transports below use every ordered four-tuple.
    return tuple(ordered[quartet] for quartet in combinations(range(n + 1), 4))


def source_bases(
    n: int,
    *,
    core_ids: frozenset[str] | None = None,
    extra_counts: frozenset[int] | None = None,
) -> tuple[BaseModel, ...]:
    data = json.loads(SUPPORT_CERT.read_text())
    answer = []
    for index, row in enumerate(data["records"]):
        if int(row["outgoing_count"]) != n:
            continue
        if core_ids is not None and str(row["core_id"]) not in core_ids:
            continue
        if extra_counts is not None and int(row["extra_count"]) not in extra_counts:
            continue
        graph = graph_from_record(row)
        labels = (*outgoing(graph), INCOMING)
        ordered = deck(graph, labels)
        primitive = stable_hash({
            "kind": "source", "core": row["core_id"], "repair": row["repair_index"],
            "words": row["words"], "sink_labels": row["sink_labels"],
            "mixed": canonical_mixed(sd0(graph))[0],
        })
        provenance = (row["core_id"], row["repair_index"], row["words"])
        variant = ModelVariant(
            primitive, graph, labels, True, provenance, graph, (), True
        )
        answer.append(BaseModel(
            primitive, graph, labels, tuple(sorted(ordered.items())), True,
            provenance, (variant,),
        ))
    return tuple(answer)


def target_bases(n: int) -> tuple[BaseModel, ...]:
    grouped: dict[tuple, dict[str, ModelVariant]] = defaultdict(dict)
    ordered_by_key = {}
    # A target rooted presentation may place its structural incoming boundary
    # either inside the selected source support or outside it.  The latter is
    # represented by a zero-character dummy incoming leaf in the full strong
    # completion.  Both cases have n+1 selected tensor ports.
    completion_rows = chain(completions(n), marginal_incoming_completions(n + 1))
    for index, completion in enumerate(completion_rows):
        graph = completion.graph
        selected = tuple(sorted(completion.selected_labels, key=natural))
        labels = ((*selected, INCOMING) if completion.incoming_selected else selected)
        if len(labels) != n + 1:
            raise AssertionError((n, completion.incoming_selected, labels))
        ordered = deck(graph, labels)
        retains_core = (
            completion.incoming_selected and selected_retains_strong_core(completion)
        )
        kind = "cycle" if completion.core_id == "cycle" else "theta"
        primitive = stable_hash({
            "kind": "target", "core": completion.core_id,
            "sink_mask": completion.selected_sink_mask,
            "repair": completion.repair_index, "words": completion.words,
            "selected": completion.selected_labels, "dummies": completion.dummy_labels,
            "incoming_selected": completion.incoming_selected,
            "arcs": graph.arcs, "labels": graph.labels,
        })
        provenance = (
            completion.core_id, completion.selected_sink_mask, completion.repair_index,
            completion.words, completion.dummy_labels, completion.incoming_selected,
        )
        topology_graph = selected_graph(completion) if retains_core else None
        if topology_graph is not None:
            valid, problems = rooted_validation(topology_graph)
            if not valid or not mixed_local_strong(sd0(topology_graph)):
                raise AssertionError((completion.core_id, completion.words, problems))
        variant = ModelVariant(
            primitive, graph, labels, retains_core, provenance, topology_graph,
            completion.dummy_labels, completion.incoming_selected,
        )
        ordered_tuple = tuple(sorted(ordered.items()))
        key = kind, ordered_tuple
        ordered_by_key[key] = ordered_tuple
        variant_key = stable_hash({
            "primitive": primitive,
            "mixed": canonical_mixed(sd0(graph))[0],
            "selected": labels,
            "dummies": completion.dummy_labels,
        })
        grouped[key][variant_key] = variant
    answer = []
    for key in sorted(grouped, key=repr):
        variants = tuple(grouped[key][variant_key] for variant_key in sorted(grouped[key]))
        representative = min(
            variants, key=lambda row: (not row.retains_strong_core, row.primitive_id)
        )
        answer.append(BaseModel(
            representative.primitive_id,
            representative.graph,
            representative.labels,
            ordered_by_key[key],
            representative.retains_strong_core,
            representative.provenance,
            variants,
        ))
    return tuple(answer)


def descriptor_bits(descriptor: Descriptor, invariants, cache: dict[Descriptor, int]) -> int:
    if descriptor not in cache:
        bits = 0
        evaluations = tuple(
            coordinate_values_mod(descriptor, seed)
            for seed in (101, 1009, 10007)
        )
        exact_candidates = []
        for index, invariant in enumerate(invariants):
            modular_nonzero = any(
                invariant_value_mod(coordinates, invariant)
                for coordinates in evaluations
            )
            if modular_nonzero:
                bits |= 1 << index
            else:
                exact_candidates.append((index, invariant))
        if exact_candidates:
            candidate_invariants = tuple(invariant for _index, invariant in exact_candidates)
            for (index, _invariant), polynomial in zip(
                exact_candidates,
                pullbacks_shared(descriptor, candidate_invariants),
            ):
                if polynomial:
                    bits |= 1 << index
        cache[descriptor] = bits
    return cache[descriptor]


def labelled_signature(
    base: BaseModel,
    assignment: tuple[int, ...],
    invariants,
    cache: dict[Descriptor, int],
) -> tuple[int, tuple[Descriptor, ...]]:
    # ``assignment`` transports *every* boundary position, including the
    # distinguished incoming boundary used by this rooted presentation, to
    # the fixed labels of the source relation.  The standard semi-directed
    # topology does not retain an incoming-port colour, so restricting this
    # permutation to outgoing ports would omit genuine relations (including
    # ordinary-T variants whose admissible incoming boundary changes).
    p = len(assignment)
    inverse = [0] * p
    for position, actual in enumerate(assignment):
        inverse[actual] = position
    ordered = base.deck_map()
    signature = 0
    descriptors = []
    for chunk, actual_quartet in enumerate(combinations(range(p), 4)):
        positional = tuple(inverse[value] for value in actual_quartet)
        descriptor = ordered[positional]
        descriptors.append(descriptor)
        signature |= descriptor_bits(descriptor, invariants, cache) << (len(invariants) * chunk)
    return signature, tuple(descriptors)


def labelled_records(
    bases: tuple[BaseModel, ...], n: int, invariants, cache,
    *,
    topology_filter: set[int] | None = None,
    topology_for_all: bool = False,
    anchor_source_labels: bool = False,
):
    records: dict[int, dict] = {}
    raw = 0
    for base in bases:
        # Base positions are ``(*outgoing, incoming)``.  Anchor all source
        # boundary labels simultaneously, but allow the target's rooted
        # incoming position to correspond to any source boundary.
        assignments = (
            (tuple(range(n + 1)),)
            if anchor_source_labels
            else permutations(range(n + 1))
        )
        for assignment in assignments:
            raw += 1
            signature, descriptors = labelled_signature(base, assignment, invariants, cache)
            row = records.setdefault(signature, {
                "presentations": {},
                "variant_presentations": {},
                "core_retention_statuses": set(),
                "kinds": set(),
                "t_codes": set(),
                "variant_ids": set(),
                "presentation_coverage": defaultdict(set),
                "presentation_t_codes": defaultdict(set),
            })
            descriptor_hash = stable_hash(descriptors)
            for variant in base.variants:
                kind = "cycle" if variant.provenance[0] == "cycle" else "theta"
                presentation_key = (variant.retains_strong_core, kind, descriptor_hash)
                row["presentations"].setdefault(
                    presentation_key, (variant, base, assignment, descriptors)
                )
                row["core_retention_statuses"].add(variant.retains_strong_core)
                row["kinds"].add(kind)
                row["variant_ids"].add(variant.primitive_id)
                row["presentation_coverage"][presentation_key].add(variant.primitive_id)
                variant_key = stable_hash({
                    "primitive": variant.primitive_id,
                    "assignment": assignment,
                    "descriptor_deck": descriptor_hash,
                })
                variant_t_code = None
                if topology_for_all or (topology_filter is not None and signature in topology_filter):
                    if variant.retains_strong_core:
                        if variant.topology_graph is None:
                            raise AssertionError("strong variant lacks selected topology graph")
                        mixed = sd0(relabel_selected(
                            variant.topology_graph, variant.labels, assignment
                        ))
                        t_code = canonical_mixed(t_quotient(mixed))[0]
                        variant_t_code = t_code
                        row["t_codes"].add(t_code)
                        row["presentation_t_codes"][presentation_key].add(t_code)
                row["variant_presentations"].setdefault(
                    variant_key,
                    (variant, base, assignment, descriptors, variant_t_code),
                )
    return records, raw


def directed_pairs(sources: dict[int, dict], targets: dict[int, dict], chunks: int, bits_per_chunk: int):
    mask = (1 << bits_per_chunk) - 1
    indexes = []
    for chunk in range(chunks):
        groups: dict[int, list[int]] = defaultdict(list)
        for target in targets:
            groups[(target >> (bits_per_chunk * chunk)) & mask].append(target)
        indexes.append(groups)
    pairs = []
    examined = 0
    for source in sources:
        shortlist = None
        for chunk, groups in enumerate(indexes):
            source_chunk = (source >> (bits_per_chunk * chunk)) & mask
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
    if len(assignment) != len(labels):
        raise ValueError("boundary assignment must cover every selected position")
    mapping = {label: f"L_{actual}" for label, actual in zip(labels, assignment)}
    return RootedGraph(
        graph.root,
        tuple(sorted((v, mapping.get(label, label)) for v, label in graph.labels)),
        graph.arcs,
    )


def equal_topology_audit(common_signatures: set[int], sources: dict[int, dict], targets: dict[int, dict]):
    failures = []
    nonretained = 0
    checked = 0
    presentation_matrix: dict[str, int] = defaultdict(int)
    for signature in common_signatures:
        nonretained_here = False
        source_presentations = sources[signature]["presentation_t_codes"]
        target_presentations = targets[signature]["presentation_t_codes"]
        for source_key, source_t0 in source_presentations.items():
            source_retains, source_kind, _ = source_key
            if not source_retains:
                raise AssertionError("source support presentation loses its primitive core")
            source_t = set(source_t0)
            for target_key in targets[signature]["presentations"]:
                target_retains, target_kind, _ = target_key
                presentation_matrix[
                    f"{source_kind}_to_{target_kind}_target_"
                    f"{'retained' if target_retains else 'nonretained'}"
                ] += 1
                if not target_retains:
                    nonretained_here = True
                    continue
                target_t = set(target_presentations.get(target_key, ()))
                checked += len(source_t) * len(target_t)
                if len(source_t) != 1 or len(target_t) != 1 or source_t != target_t:
                    failures.append({
                        "signature_sha": hashlib.sha256(str(signature).encode()).hexdigest(),
                        "source_kind": source_kind,
                        "target_kind": target_kind,
                        "source_t_classes": len(source_t),
                        "target_t_classes": len(target_t),
                        "source_only": sorted(source_t - target_t)[:2],
                        "target_only": sorted(target_t - source_t)[:2],
                    })
        nonretained += int(nonretained_here)
    return {
        "failures": failures,
        "common_signatures_also_having_a_nonretaining_presentation": nonretained,
        "strong_presentation_t_class_comparisons": checked,
        "equal_signature_presentation_matrix": dict(sorted(presentation_matrix.items())),
    }


def compile_size(
    n: int,
    invariants,
    bit_cache,
    *,
    source_core_ids: frozenset[str] | None = None,
    source_extra_counts: frozenset[int] | None = None,
):
    start = time.monotonic()
    sources_base = source_bases(
        n,
        core_ids=source_core_ids,
        extra_counts=source_extra_counts,
    )
    targets_base = target_bases(n)
    sources, source_raw = labelled_records(
        sources_base, n, invariants, bit_cache,
        topology_for_all=True, anchor_source_labels=True,
    )
    targets, target_raw = labelled_records(
        targets_base, n, invariants, bit_cache, topology_filter=set(sources),
    )
    pairs, examined = directed_pairs(sources, targets, math_comb(n + 1, 4), len(invariants))
    equal = {(s, t) for s, t in pairs if s == t}
    strict = len(pairs) - len(equal)
    common = set(sources) & set(targets)
    topology = equal_topology_audit(common, sources, targets)
    retention_signatures: dict[str, int] = defaultdict(int)
    for row in targets.values():
        retention_signatures[
            repr(tuple(sorted(row["core_retention_statuses"])))
        ] += 1
    pair_target_kinds: dict[str, int] = defaultdict(int)
    pair_kind_matrix: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for source, target in pairs:
        for kind in targets[target]["kinds"]:
            pair_target_kinds[kind] += 1
        relation = "equal" if source == target else "strict"
        for source_kind in sources[source]["kinds"]:
            for target_kind in targets[target]["kinds"]:
                pair_kind_matrix[f"{source_kind}_to_{target_kind}"][relation] += 1
    return {
        "outgoing": n,
        "descriptor_mask_convention": (
            "rooted_selected_side_masks_before_zero_sum_complement_zip"
        ),
        "source_core_filter": (
            sorted(source_core_ids) if source_core_ids is not None else None
        ),
        "source_extra_count_filter": (
            sorted(source_extra_counts)
            if source_extra_counts is not None else None
        ),
        "source_bases": len(sources_base),
        "target_bases": len(targets_base),
        "source_raw_labelled": source_raw,
        "target_raw_labelled": target_raw,
        "source_signatures": len(sources),
        "target_signatures": len(targets),
        "target_signature_core_retention_status": dict(retention_signatures),
        "common_signatures": len(common),
        "necessary_directed_pairs": len(pairs),
        "equal_pairs": len(equal),
        "strict_pairs": strict,
        "necessary_pairs_by_target_kind_membership": dict(pair_target_kinds),
        "necessary_pair_kind_matrix": {
            key: dict(value) for key, value in sorted(pair_kind_matrix.items())
        },
        "indexed_candidates_examined": examined,
        "topology_audit": topology,
        "signature_pair_commitment": stable_hash(sorted((str(s), str(t)) for s, t in pairs)),
        "elapsed_seconds": time.monotonic() - start,
    }, (sources, targets, pairs)


def compile_relation_records(n: int, working, invariants):
    """Bind every necessary directed presentation pair to graph-derived algebra.

    Core-retaining target restrictions are compared as intrinsic selected
    topologies; non-core-retaining target restrictions retain their full
    strong completion graph and are marked for the support-completion gate.
    Thus a dummy completion can never be promoted to a topology, while its
    exact marginalized tensor remains available for algebraic separation.
    """
    sources, targets, pairs = working
    relation_path = HERE / "certificates" / f"bounded_relations_n{n}.jsonl.gz"
    sign_path = HERE / "certificates" / f"bounded_sign_library_n{n}.json"
    graph_path = HERE / "certificates" / f"bounded_relation_graphs_n{n}.jsonl.gz"
    polynomial_path = HERE / "certificates" / f"bounded_relation_polynomials_n{n}.jsonl.gz"
    sign_library: dict[str, dict] = {}
    graph_library: dict[str, dict] = {}
    polynomial_library: dict[str, dict] = {}
    sign_cache: dict[tuple[Descriptor, int], tuple[object, dict, str]] = {}
    failures = []
    counts = defaultdict(int)
    records: dict[str, dict] = {}
    raw_relations_examined = 0

    def register_graph(graph: RootedGraph) -> str:
        payload = {
            "root": int(graph.root),
            "labels": tuple(sorted(
                (int(vertex), str(label)) for vertex, label in graph.labels
            )),
            "arcs": tuple(sorted((int(u), int(v)) for u, v in graph.arcs)),
        }
        identifier = stable_hash(payload)
        mixed = sd0(graph)
        code, transport = canonical_mixed(mixed)
        t_code, t_transport = canonical_mixed(t_quotient(mixed))
        valid, problems = rooted_validation(graph)
        row = {
            "schema": 1,
            "graph_id": identifier,
            "rooted_graph": payload,
            "rooted_valid": valid,
            "rooted_validation_problems": problems,
            "standard_strong_local": mixed_local_strong(mixed),
            "standard_mixed_code": code,
            "t_quotient_code": t_code,
            "raw_mixed_vertex_to_canonical": tuple(sorted(transport.items())),
            "raw_t_quotient_vertex_to_canonical": tuple(
                sorted(t_transport.items())
            ),
        }
        prior = graph_library.setdefault(identifier, row)
        if prior != row:
            raise AssertionError("bounded graph content-address collision")
        return identifier

    def register_polynomial(poly) -> tuple[str, str]:
        terms = tuple(
            (tuple(int(value) for value in exponents), int(coefficient))
            for exponents, coefficient in sorted(poly.items())
        )
        payload = {
            "schema": 1,
            "variable_count": len(terms[0][0]) if terms else 0,
            "terms": terms,
        }
        identifier = stable_hash(payload)
        exact_hash = hashlib.sha256(repr(tuple(sorted(poly.items()))).encode()).hexdigest()
        row = {
            **payload,
            "polynomial_id": identifier,
            "exact_polynomial_sha256": exact_hash,
        }
        prior = polynomial_library.setdefault(identifier, row)
        if prior != row:
            raise AssertionError("bounded polynomial content-address collision")
        return identifier, exact_hash

    def write_library(path: Path, rows: dict[str, dict]) -> str:
        digest = hashlib.sha256()
        with path.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as out:
                for identifier in sorted(rows):
                    line = (
                        json.dumps(
                            rows[identifier], sort_keys=True, separators=(",", ":")
                        )
                        + "\n"
                    ).encode()
                    out.write(line)
                    digest.update(line)
        return digest.hexdigest()

    def labelled_mixed_code(variant: ModelVariant, assignment, *, topology: bool) -> str | None:
        graph = variant.topology_graph if topology else variant.graph
        if graph is None:
            return None
        moved = relabel_selected(graph, variant.labels, assignment)
        return canonical_mixed(sd0(moved))[0]

    for source_signature, target_signature in pairs:
        source_presentations = tuple(
            sources[source_signature]["variant_presentations"].values()
        )
        target_presentations = tuple(
            targets[target_signature]["variant_presentations"].values()
        )
        if not source_presentations or not target_presentations:
            failures.append({"missing_variant_presentations": [source_signature, target_signature]})
            continue
        for source_presentation in source_presentations:
          for target_presentation in target_presentations:
            raw_relations_examined += 1
            if raw_relations_examined % 1000 == 0:
                print(json.dumps({
                    "bounded_relation_progress": {
                        "outgoing": n,
                        "raw_presentations": raw_relations_examined,
                        "canonical_relations": len(records),
                        "sign_cache": len(sign_cache),
                        "failures": len(failures),
                    }
                }, sort_keys=True), flush=True)
            (
                source_variant, _source_base, source_assignment,
                source_descriptors, source_t_code,
            ) = source_presentation
            (
                target_variant, _target_base, target_assignment,
                target_descriptors, target_t_code,
            ) = target_presentation
            source_kind = "cycle" if source_variant.provenance[0] == "cycle" else "theta"
            target_kind = "cycle" if target_variant.provenance[0] == "cycle" else "theta"
            source_code = labelled_mixed_code(source_variant, source_assignment, topology=True)
            target_completion_code = labelled_mixed_code(
                target_variant, target_assignment, topology=False
            )
            target_selected_code = labelled_mixed_code(
                target_variant, target_assignment, topology=True
            )
            if source_code is None or target_completion_code is None:
                raise AssertionError("missing graph in decorated relation")
            source_graph = relabel_selected(
                source_variant.topology_graph,
                source_variant.labels,
                source_assignment,
            )
            target_completion_graph = relabel_selected(
                target_variant.graph,
                target_variant.labels,
                target_assignment,
            )
            source_graph_id = register_graph(source_graph)
            target_completion_graph_id = register_graph(target_completion_graph)
            target_selected_graph_id = None
            if target_variant.topology_graph is not None:
                target_selected_graph_id = register_graph(relabel_selected(
                    target_variant.topology_graph,
                    target_variant.labels,
                    target_assignment,
                ))
            relation_id = stable_hash({
                "direction": "source_precedes_target",
                "outgoing": n,
                "source_rooted_graph_id": source_graph_id,
                "target_completion_rooted_graph_id": target_completion_graph_id,
                "target_selected_rooted_graph_id": target_selected_graph_id,
                "source_side_coloured_mixed_graph": source_code,
                "target_completion_side_coloured_mixed_graph": target_completion_code,
                "target_selected_side_coloured_mixed_graph": target_selected_code,
                "port_matching": tuple((f"L_{i}", f"L_{i}") for i in range(n + 1)),
            })
            record = {
                "schema": 3,
                "relation_id": relation_id,
                "outgoing": n,
                "direction": "source_precedes_target",
                "source_kind": source_kind,
                "target_kind": target_kind,
                "target_retains_strong_core": target_variant.retains_strong_core,
                "source_mixed_code_sha256": hashlib.sha256(source_code.encode()).hexdigest(),
                "target_completion_mixed_code_sha256": hashlib.sha256(
                    target_completion_code.encode()
                ).hexdigest(),
                "target_selected_mixed_code_sha256": (
                    hashlib.sha256(target_selected_code.encode()).hexdigest()
                    if target_selected_code is not None else None
                ),
                "source_graph_id": source_graph_id,
                "target_completion_graph_id": target_completion_graph_id,
                "target_selected_graph_id": target_selected_graph_id,
                "source_signature_sha256": hashlib.sha256(
                    str(source_signature).encode()
                ).hexdigest(),
                "target_signature_sha256": hashlib.sha256(
                    str(target_signature).encode()
                ).hexdigest(),
                "port_correspondence": tuple(range(n + 1)),
                "source_descriptor_deck_sha256": stable_hash(source_descriptors),
                "target_descriptor_deck_sha256": stable_hash(target_descriptors),
                "raw_coverage": [{
                    "source_primitive_id": source_variant.primitive_id,
                    "target_primitive_id": target_variant.primitive_id,
                    "source_graph_id": source_graph_id,
                    "target_completion_graph_id": target_completion_graph_id,
                    "target_selected_graph_id": target_selected_graph_id,
                    "source_position_to_label": source_assignment,
                    "target_position_to_label": target_assignment,
                    "source_incoming_actual_label": (
                        source_assignment[source_variant.labels.index(INCOMING)]
                        if INCOMING in source_variant.labels else None
                    ),
                    "target_incoming_actual_label": (
                        target_assignment[target_variant.labels.index(INCOMING)]
                        if INCOMING in target_variant.labels else None
                    ),
                    "source_roles": source_variant.provenance,
                    "target_roles": target_variant.provenance,
                }],
            }
            if source_signature == target_signature:
                if target_variant.retains_strong_core:
                    if source_t_code is None or target_t_code is None:
                        failures.append({"missing_T_code": record})
                        continue
                    if source_t_code != target_t_code:
                        failures.append({"equal_signature_non_T_strong_relation": record})
                        continue
                    record["classification"] = "isomorphism_or_T"
                    record["t_quotient_code_sha256"] = hashlib.sha256(
                        source_t_code.encode()
                    ).hexdigest()
                else:
                    record["classification"] = "pending_support_completion"
            else:
                difference = target_signature & ~source_signature
                witness = None
                candidates = []
                while difference:
                    lowest = difference & -difference
                    absolute_bit = lowest.bit_length() - 1
                    difference ^= lowest
                    chunk, invariant_index = divmod(absolute_bit, len(invariants))
                    source_poly = pullback(source_descriptors[chunk], invariants[invariant_index])
                    target_poly = pullback(target_descriptors[chunk], invariants[invariant_index])
                    if source_poly or not target_poly:
                        continue
                    cache_key = target_descriptors[chunk], invariant_index
                    coefficients = tuple(target_poly.values())
                    same_sign = (
                        (all(value >= 0 for value in coefficients)
                         and any(value > 0 for value in coefficients))
                        or
                        (all(value <= 0 for value in coefficients)
                         and any(value < 0 for value in coefficients))
                    )
                    candidates.append((
                        0 if cache_key in sign_cache else (1 if same_sign else 2),
                        len(target_poly),
                        chunk,
                        invariant_index,
                        cache_key,
                        target_poly,
                    ))
                for (
                    _cached,
                    _term_count,
                    chunk,
                    invariant_index,
                    cache_key,
                    target_poly,
                ) in sorted(candidates):
                    if cache_key not in sign_cache:
                        sign = certify_sign(target_poly)
                        exact_hash = hashlib.sha256(
                            repr(tuple(sorted(target_poly.items()))).encode()
                        ).hexdigest()
                        sign_cache[cache_key] = target_poly, sign, exact_hash
                    _poly, sign, exact_hash = sign_cache[cache_key]
                    if sign["certified"]:
                        polynomial_id, stored_exact_hash = register_polynomial(target_poly)
                        if stored_exact_hash != exact_hash:
                            raise AssertionError("strict polynomial hash disagreement")
                        sign_library.setdefault(exact_hash, {
                            **sign,
                            "exact_polynomial_sha256": exact_hash,
                            "polynomial_id": polynomial_id,
                        })
                        witness = {
                            "quartet_chunk": chunk,
                            "invariant_index": invariant_index,
                            "source_pullback": "0",
                            "target_pullback_exact_sha256": exact_hash,
                            "target_pullback_id": polynomial_id,
                            "target_pullback_primitive_sha256": sign["polynomial_sha256"],
                            "strict_sign": sign["strict_sign"],
                        }
                        break
                if witness is None:
                    failures.append({"no_strict_witness": record})
                    continue
                record["classification"] = "strict_open_cube_separation"
                record["witness"] = witness

            prior = records.get(relation_id)
            if prior is None:
                records[relation_id] = record
            else:
                comparable = lambda row: {
                    key: value for key, value in row.items()
                    if key not in {"raw_coverage"}
                }
                if comparable(prior) != comparable(record):
                    failures.append({"canonical_relation_disagreement": [prior, record]})
                    continue
                prior["raw_coverage"].extend(record["raw_coverage"])

    hasher = hashlib.sha256()
    for record in records.values():
        record["raw_coverage"] = sorted(
            record["raw_coverage"], key=lambda value: stable_hash(value)
        )
        record["binding_sha256"] = stable_hash(record)
        counts[record["classification"]] += 1
        counts[
            f"{record['source_kind']}_to_{record['target_kind']}_"
            f"{record['classification']}"
        ] += 1
    with relation_path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as handle:
            for relation_id in sorted(records):
                line = (
                    json.dumps(records[relation_id], sort_keys=True, separators=(",", ":"))
                    + "\n"
                ).encode()
                handle.write(line)
                hasher.update(line)
    sign_path.write_text(json.dumps(sign_library, sort_keys=True, indent=2) + "\n")
    graph_stream_sha = write_library(graph_path, graph_library)
    polynomial_stream_sha = write_library(polynomial_path, polynomial_library)
    return {
        "relation_path": str(relation_path.relative_to(HERE.parent)),
        "relation_stream_sha256": hasher.hexdigest(),
        "sign_library_path": str(sign_path.relative_to(HERE.parent)),
        "sign_library_sha256": sha256(sign_path),
        "graph_library_path": str(graph_path.relative_to(HERE.parent)),
        "graph_library_records": len(graph_library),
        "graph_library_stream_sha256": graph_stream_sha,
        "polynomial_library_path": str(polynomial_path.relative_to(HERE.parent)),
        "polynomial_library_records": len(polynomial_library),
        "polynomial_library_stream_sha256": polynomial_stream_sha,
        "canonical_decorated_relations": len(records),
        "raw_presentations_examined": raw_relations_examined,
        "counts": dict(sorted(counts.items())),
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
    parser.add_argument("--load-bit-cache", type=Path)
    parser.add_argument("--write-bit-cache", type=Path, default=BIT_CACHE_FILE)
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--source-core-id", action="append")
    parser.add_argument("--source-extra-count", action="append", type=int)
    args = parser.parse_args()
    template_sha = sha256(TEMPLATE_FILE)
    if template_sha != EXPECTED_TEMPLATE_SHA:
        raise SystemExit(f"inert invariant template hash changed: {template_sha}")
    templates = parse_literal(TEMPLATE_FILE, "INVARIANT_TEMPLATES")
    seventh_sha = sha256(SEVENTH_TEMPLATE_FILE)
    if seventh_sha != EXPECTED_SEVENTH_SHA:
        raise SystemExit(f"seventh invariant hash changed: {seventh_sha}")
    seventh_payload = json.loads(SEVENTH_TEMPLATE_FILE.read_text())
    # The source certificate indexes the fourteen nontrivial coordinates
    # A,...,O, whereas jc_tensor includes the normalized trivial coordinate at
    # index zero.  The explicit +1 transport is part of the certificate.
    seventh = tuple(
        (tuple(int(index) + 1 for index in monomial), int(coefficient))
        for coefficient, monomial in seventh_payload["invariant"]
    )
    templates = (*templates, seventh)
    invariants = invariant_orbit(templates)
    if len(invariants) != 84:
        raise AssertionError(len(invariants))
    cache: dict[Descriptor, int] = (
        load_bit_cache(args.load_bit_cache) if args.load_bit_cache else {}
    )
    loaded_descriptor_types = len(cache)
    runs = []
    for n in args.sizes:
        row, working = compile_size(
            n,
            invariants,
            cache,
            source_core_ids=(
                frozenset(args.source_core_id)
                if args.source_core_id is not None else None
            ),
            source_extra_counts=(
                frozenset(args.source_extra_count)
                if args.source_extra_count is not None else None
            ),
        )
        if args.relations:
            row["bounded_relation_certificate"] = compile_relation_records(
                n, working, invariants
            )
            if row["bounded_relation_certificate"]["failure_count"]:
                raise SystemExit(f"relation failures at n={n}")
        runs.append(row)
        if args.write_bit_cache:
            write_bit_cache(args.write_bit_cache, cache)
        print(json.dumps(row, sort_keys=True), flush=True)
    payload = {
        "schema": 1,
        "template_path": str(TEMPLATE_FILE.relative_to(PROJECT)),
        "template_sha256": template_sha,
        "seventh_template_path": str(SEVENTH_TEMPLATE_FILE.relative_to(HERE.parent)),
        "seventh_template_sha256": seventh_sha,
        "invariant_orbit_size": len(invariants),
        "descriptor_types_exactly_expanded": len(cache),
        "descriptor_types_loaded": loaded_descriptor_types,
        "runs": runs,
    }
    if args.write_bit_cache:
        write_bit_cache(args.write_bit_cache, cache)
        payload["descriptor_bit_cache"] = {
            "path": str(args.write_bit_cache.relative_to(HERE.parent)),
            "sha256": sha256(args.write_bit_cache),
            "records": len(cache),
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "descriptor_types": len(cache)}, sort_keys=True))


if __name__ == "__main__":
    main()
