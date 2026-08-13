#!/usr/bin/env python3
"""Restore every omitted target role in an equal bounded JC relation.

The bounded quartet-invariant atlas deliberately admits target tensors that
are marginals of a full standard-strong factor.  Their omitted repair, sink,
or rooted-incoming boundaries appear as zero-character dummy leaves.  An
equal invariant deck at that marginal is not a topology equivalence.

For each such presentation this compiler restores every dummy as a genuine
labelled boundary, inserts the corresponding labels in every possible source
segment position, and regenerates

    graph -> switchings -> masks -> JC descriptors -> invariant pullbacks.

Every restored directed relation is then classified as isomorphism/ordinary
T, generic polynomial separation, strict open-cube separation, or unresolved.
No topology identifier selects a polynomial witness.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path

from atlas_compiler import (
    EXPECTED_SEVENTH_SHA,
    EXPECTED_TEMPLATE_SHA,
    INCOMING,
    SEVENTH_TEMPLATE_FILE,
    TEMPLATE_FILE,
    compile_size,
    descriptor_bits,
    load_bit_cache,
    natural,
    parse_literal,
    sha256,
    stable_hash,
)
from completion_universe import build_graph, core_by_id, source_and_sinks
from graph_model import (
    RootedGraph,
    canonical_mixed,
    mixed_local_strong,
    rooted_validation,
    sd0,
    t_quotient,
)
from jc_tensor import canonicalize_rows, invariant_orbit, pullback, raw_descriptor
from sign_certificate import certify as certify_sign


HERE = Path(__file__).resolve().parent
OUT = HERE / "certificates" / "hard_cover_summary.json"


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
    answer = invariant_orbit((*templates, seventh))
    if len(answer) != 84:
        raise AssertionError(len(answer))
    return answer


def relabel(graph: RootedGraph, mapping: dict[str, str]) -> RootedGraph:
    return RootedGraph(
        graph.root,
        tuple(sorted((vertex, mapping.get(label, label)) for vertex, label in graph.labels)),
        graph.arcs,
    )


def insertion_words(words: tuple[tuple[str, ...], ...], labels: tuple[str, ...]):
    """Every extension preserving the old order on every directed segment."""
    states = {tuple(tuple(word) for word in words)}
    for label in labels:
        moved = set()
        for state in states:
            for segment, word in enumerate(state):
                for position in range(len(word) + 1):
                    row = list(state)
                    row[segment] = (*word[:position], label, *word[position:])
                    moved.add(tuple(tuple(values) for values in row))
        states = moved
    yield from sorted(states, key=repr)


def source_extensions(source_variant, source_assignment, new_labels: tuple[str, ...]):
    core_id, _repair_index, words = source_variant.provenance[:3]
    core = core_by_id()[core_id]
    _source, sinks = source_and_sinks(core["arcs"])
    sink_labels = {sink: f"Q_SINK_{index}" for index, sink in enumerate(sinks)}
    selected_mapping = {
        label: f"L_{actual}"
        for label, actual in zip(source_variant.labels, source_assignment)
    }
    for extended_words in insertion_words(tuple(words), new_labels):
        graph = build_graph(core["arcs"], extended_words, sink_labels)
        graph = relabel(graph, selected_mapping)
        valid, problems = rooted_validation(graph)
        if not valid:
            raise AssertionError((core_id, extended_words, problems))
        mixed = sd0(graph)
        if not mixed_local_strong(mixed):
            raise AssertionError((core_id, extended_words, "extension lost S_TC"))
        yield extended_words, graph


def restored_target(target_variant, target_assignment, new_labels: tuple[str, ...]):
    dummy = tuple(sorted(target_variant.dummy_labels, key=natural))
    if len(dummy) != len(new_labels):
        raise AssertionError((dummy, new_labels))
    mapping = {
        label: f"L_{actual}"
        for label, actual in zip(target_variant.labels, target_assignment)
    }
    mapping.update(dict(zip(dummy, new_labels)))
    graph = relabel(target_variant.graph, mapping)
    valid, problems = rooted_validation(graph)
    if not valid:
        raise AssertionError((target_variant.provenance, problems))
    mixed = sd0(graph)
    if not mixed_local_strong(mixed):
        raise AssertionError((target_variant.provenance, "restored target not S_TC"))
    return dummy, graph


def full_deck(graph: RootedGraph, port_count: int):
    labels = tuple(f"L_{index}" for index in range(port_count))
    retics, signatures = raw_descriptor(graph, labels)
    answer = []
    for quartet in combinations(range(port_count), 4):
        rows = []
        for signature in signatures:
            moved = []
            for mask in signature:
                new_mask = 0
                for new_index, old_index in enumerate(quartet):
                    if mask & (1 << old_index):
                        new_mask |= 1 << new_index
                # Every retained Fourier assignment has total character
                # zero.  A split side and its complement therefore induce
                # exactly the same JC factor.  Canonicalizing that choice
                # zips the two root arcs into the effective edge multiplier
                # of the locked semi-directed graph and makes the descriptor
                # independent of an admissible root location.
                new_mask = min(new_mask, 0b1111 ^ new_mask)
                moved.append(new_mask)
            rows.append(tuple(moved))
        answer.append(canonicalize_rows(retics, rows))
    return tuple(answer)


def deck_signature(descriptors, invariants, bit_cache):
    signature = 0
    width = len(invariants)
    for chunk, descriptor in enumerate(descriptors):
        signature |= descriptor_bits(descriptor, invariants, bit_cache) << (width * chunk)
    return signature


def exact_poly_hash(poly) -> str:
    return hashlib.sha256(repr(tuple(sorted(poly.items()))).encode()).hexdigest()


def quick_power_sign(poly):
    """Exact strict sign when all sparse power coefficients have one sign."""
    values = tuple(poly.values())
    if all(value >= 0 for value in values) and any(value > 0 for value in values):
        sign = 1
    elif all(value <= 0 for value in values) and any(value < 0 for value in values):
        sign = -1
    else:
        return {"certified": False, "method": "same-sign power coefficients"}
    return {
        "certified": True,
        "strict_sign": sign,
        "domain": "all effective variables lie in (0,1)",
        "method": "same-sign sparse power coefficients",
        "polynomial_sha256": exact_poly_hash(poly),
        "term_count": len(poly),
    }


def relation_witness(
    source_descriptors, target_descriptors, invariants, bit_cache, sign_cache,
    *, register_polynomial, exact_sign: bool = False,
):
    source_signature = deck_signature(source_descriptors, invariants, bit_cache)
    target_signature = deck_signature(target_descriptors, invariants, bit_cache)
    width = len(invariants)

    # A target identity that is generically nonzero on the source excludes a
    # source-full-dimensional containment; no target sign argument is needed.
    source_only = source_signature & ~target_signature
    if source_only:
        bit = source_only & -source_only
        absolute = bit.bit_length() - 1
        chunk, invariant_index = divmod(absolute, width)
        source_poly = pullback(source_descriptors[chunk], invariants[invariant_index])
        target_poly = pullback(target_descriptors[chunk], invariants[invariant_index])
        if not source_poly or target_poly:
            raise AssertionError("source-only bit does not bind to exact pullbacks")
        return "generic_polynomial_separation", {
            "quartet_chunk": chunk,
            "invariant_index": invariant_index,
            "source_pullback_id": register_polynomial(source_poly),
            "source_pullback_exact_sha256": exact_poly_hash(source_poly),
            "target_pullback": "0",
        }

    target_only = target_signature & ~source_signature
    candidates = []
    while target_only:
        bit = target_only & -target_only
        target_only ^= bit
        absolute = bit.bit_length() - 1
        chunk, invariant_index = divmod(absolute, width)
        source_poly = pullback(source_descriptors[chunk], invariants[invariant_index])
        if source_poly:
            continue
        key = (target_descriptors[chunk], invariant_index)
        target_poly = pullback(
            target_descriptors[chunk], invariants[invariant_index]
        )
        if not target_poly:
            raise AssertionError("target-only bit has zero exact pullback")
        candidates.append((
            0 if sign_cache.get(key, {}).get("certified") else 1,
            len(target_poly), chunk, invariant_index, key, target_poly,
        ))

    # At a terminal state exact factorization is potentially expensive.
    # Trying the sparsest graph-derived pullback first routinely exposes the
    # short open-cube factor that the broad invariant template was designed
    # to find, and never changes logical completeness.
    for _cached_order, _term_count, chunk, invariant_index, key, target_poly in sorted(candidates):
        if key not in sign_cache:
            # Keep the census fail-fast.  Mixed-sign polynomials are refined
            # by restoring another role and are sent to a targeted exact
            # factor/Bernstein pass only if they survive at a terminal state.
            sign_cache[key] = quick_power_sign(target_poly)
        sign = sign_cache[key]
        if exact_sign and not sign["certified"]:
            sign = certify_sign(target_poly, max_elevation=5)
            sign_cache[key] = sign
        if sign["certified"]:
            return "strict_open_cube_separation", {
                "quartet_chunk": chunk,
                "invariant_index": invariant_index,
                "source_pullback": "0",
                "target_pullback_id": register_polynomial(target_poly),
                "target_pullback_exact_sha256": exact_poly_hash(target_poly),
                "target_strict_sign": sign["strict_sign"],
                "target_sign_certificate": sign,
            }

    if source_signature != target_signature:
        return "unresolved_unsigned_signature", {
            "source_signature_sha256": hashlib.sha256(str(source_signature).encode()).hexdigest(),
            "target_signature_sha256": hashlib.sha256(str(target_signature).encode()).hexdigest(),
        }
    return "equal_invariant_signature", {}


def compile_hard_cover(
    n: int, working, invariants, bit_cache,
    *,
    signature_indices: tuple[int, ...] | None = None,
    root_case_indices: tuple[int, ...] | None = None,
    root_start: int | None = None,
    root_stop: int | None = None,
    list_root_cases: bool = False,
    tag: str = "all",
):
    sources, targets, _pairs = working
    common_all = sorted(set(sources) & set(targets))
    if signature_indices is None:
        common = common_all
    else:
        common = [common_all[index] for index in signature_indices]
    records: dict[str, dict] = {}
    states: dict[str, dict] = {}
    counts = defaultdict(int)
    sign_cache = {}
    deck_cache = {}
    graph_library: dict[str, dict] = {}
    polynomial_library: dict[str, dict] = {}

    def register_polynomial(poly):
        terms = tuple(
            (tuple(int(value) for value in exponents), int(coefficient))
            for exponents, coefficient in sorted(poly.items())
        )
        payload = {
            "schema": 1,
            "variable_count": len(terms[0][0]) if terms else 0,
            "terms": terms,
        }
        polynomial_id = stable_hash(payload)
        row = {**payload, "polynomial_id": polynomial_id}
        prior = polynomial_library.setdefault(polynomial_id, row)
        if prior != row:
            raise AssertionError("polynomial content-address collision")
        return polynomial_id

    def register_graph(graph):
        rooted_payload = {
            "root": int(graph.root),
            "labels": tuple(
                (int(vertex), str(label)) for vertex, label in graph.labels
            ),
            "arcs": tuple((int(u), int(v)) for u, v in graph.arcs),
        }
        graph_id = stable_hash(rooted_payload)
        mixed = sd0(graph)
        mixed_code, vertex_transport = canonical_mixed(mixed)
        t_code, _t_transport = canonical_mixed(t_quotient(mixed))
        valid, problems = rooted_validation(graph)
        row = {
            "schema": 1,
            "graph_id": graph_id,
            "rooted_graph": rooted_payload,
            "rooted_valid": valid,
            "rooted_validation_problems": problems,
            "standard_strong_local": mixed_local_strong(mixed),
            "standard_mixed_code": mixed_code,
            "standard_mixed_code_sha256": hashlib.sha256(
                mixed_code.encode()
            ).hexdigest(),
            "t_quotient_code": t_code,
            "t_quotient_code_sha256": hashlib.sha256(
                t_code.encode()
            ).hexdigest(),
            "raw_mixed_vertex_to_canonical": tuple(
                sorted(vertex_transport.items())
            ),
        }
        prior = graph_library.setdefault(graph_id, row)
        if prior != row:
            raise AssertionError("graph content-address collision")
        return graph_id, mixed_code, vertex_transport

    # A root case is one fixed bounded presentation relation before any
    # omitted target role is restored.  It is deliberately stronger than an
    # equality of selected marginal signatures: every later restoration path
    # remains attached to this exact source presentation, target completion,
    # and physical boundary matching.  This is the condition required by the
    # fixed-full-relation hard-cover lemma.
    root_cases = []
    for selected_signature in common:
        source_presentations = tuple(
            sources[selected_signature]["variant_presentations"].values()
        )
        target_presentations = tuple(
            targets[selected_signature]["variant_presentations"].values()
        )
        for source_row in source_presentations:
            source_variant, _source_base, source_assignment, _sd, _st = source_row
            for target_row in target_presentations:
                target_variant, _target_base, target_assignment, _td, _tt = target_row
                if target_variant.retains_strong_core:
                    continue
                dummy_roles = tuple(
                    sorted(target_variant.dummy_labels, key=natural)
                )
                if not dummy_roles:
                    raise AssertionError("nonretaining target has no restorable role")
                key = {
                    "selected_outgoing": n,
                    "selected_signature_sha256": hashlib.sha256(
                        str(selected_signature).encode()
                    ).hexdigest(),
                    "source_primitive_id": source_variant.primitive_id,
                    "target_primitive_id": target_variant.primitive_id,
                    "source_provenance": source_variant.provenance,
                    "target_provenance": target_variant.provenance,
                    "source_selected_labels": source_variant.labels,
                    "target_selected_labels": target_variant.labels,
                    "source_position_to_label": source_assignment,
                    "target_position_to_label": target_assignment,
                    "target_dummy_roles": dummy_roles,
                    "target_incoming_selected": target_variant.incoming_selected,
                }
                root_cases.append((
                    stable_hash(key), key, source_variant, source_assignment,
                    target_variant, target_assignment, dummy_roles,
                ))
    root_cases.sort(key=lambda row: (row[0], stable_hash(row[1])))
    if len({row[0] for row in root_cases}) != len(root_cases):
        raise AssertionError("duplicate hard-cover root-case identifier")
    all_root_case_count = len(root_cases)
    root_case_global_index = {
        row[0]: index for index, row in enumerate(root_cases)
    }
    if root_case_indices is not None and (root_start is not None or root_stop is not None):
        raise ValueError("use explicit root-case indices or a root range, not both")
    if root_case_indices is not None:
        root_cases = [root_cases[index] for index in root_case_indices]
    elif root_start is not None or root_stop is not None:
        root_cases = root_cases[root_start or 0:root_stop]

    root_case_inventory = [
        {
            "root_case_index": root_case_global_index[row[0]],
            "root_case_id": row[0],
            "dummy_role_count": len(row[6]),
            "target_incoming_selected": row[4].incoming_selected,
            "source_primitive_id": row[2].primitive_id,
            "target_primitive_id": row[4].primitive_id,
        }
        for row in root_cases
    ]
    if list_root_cases:
        return {
            "selected_outgoing": n,
            "all_common_selected_signatures": len(common_all),
            "common_selected_signatures": len(common),
            "all_root_cases": all_root_case_count,
            "selected_root_cases": len(root_cases),
            "root_case_inventory": root_case_inventory,
        }

    root_case_records = {
        row[0]: {
            "schema": 1,
            "root_case_id": row[0],
            "global_root_case_index": root_case_global_index[row[0]],
            "root_case": row[1],
            "entry_state_ids": (),
        }
        for row in root_cases
    }

    def cached_deck(graph, p, graph_id):
        # The sparse-polynomial variable order is induced by the exact rooted
        # graph's arc order.  Distinct rooted presentations can have the same
        # standard mixed code but only permutation-equivalent variable
        # orders; merging them here breaks the graph-to-polynomial binding.
        key = p, graph_id
        if key not in deck_cache:
            deck_cache[key] = full_deck(graph, p)
        return deck_cache[key]

    def source_graph_for(source_variant, source_assignment, words):
        core_id = source_variant.provenance[0]
        core = core_by_id()[core_id]
        _source, sinks = source_and_sinks(core["arcs"])
        sink_labels = {sink: f"Q_SINK_{index}" for index, sink in enumerate(sinks)}
        graph = build_graph(core["arcs"], words, sink_labels)
        mapping = {
            label: f"L_{actual}"
            for label, actual in zip(source_variant.labels, source_assignment)
        }
        graph = relabel(graph, mapping)
        valid, problems = rooted_validation(graph)
        if not valid or not mixed_local_strong(sd0(graph)):
            raise AssertionError((core_id, words, problems))
        return graph

    def target_graph_for(target_variant, target_assignment, restored):
        mapping = {
            label: f"L_{actual}"
            for label, actual in zip(target_variant.labels, target_assignment)
        }
        mapping.update(restored)
        graph = relabel(target_variant.graph, mapping)
        valid, problems = rooted_validation(graph)
        if not valid or not mixed_local_strong(sd0(graph)):
            raise AssertionError((target_variant.provenance, restored, problems))
        return graph

    def visit(
        source_variant,
        source_assignment,
        source_words,
        target_variant,
        target_assignment,
        restored,
        remaining,
        path_roles,
        raw_root,
        parent_state_id=None,
        parent_path_binding_id=None,
    ):
        result_ids = []
        current_p = n + 1 + len(restored)
        if not remaining:
            raise AssertionError("visit requires at least one omitted role")
        role = remaining[0]
        label = f"L_{current_p}"
        restored_next = {**restored, role: label}
        remaining_next = remaining[1:]
        target_graph = target_graph_for(
            target_variant, target_assignment, restored_next
        )
        target_graph_id, target_code, target_transport = register_graph(target_graph)
        target_descriptors = None

        local_seen = set()
        for extended_words in insertion_words(source_words, (label,)):
            source_graph = source_graph_for(
                source_variant, source_assignment, extended_words
            )
            source_graph_id, source_code, source_transport = register_graph(source_graph)
            state_id = stable_hash({
                "fixed_full_root_case_id": raw_root["root_case_id"],
                "selected_port_count": current_p + 1,
                "source_rooted_graph_id": source_graph_id,
                "target_rooted_graph_id": target_graph_id,
                "source_mixed_code": source_code,
                "target_completion_mixed_code": target_code,
                "remaining_target_roles": remaining_next,
                "port_matching": tuple(range(current_p + 1)),
            })
            if state_id in local_seen:
                continue
            local_seen.add(state_id)
            result_ids.append(state_id)
            coverage = {
                **raw_root,
                "restoration_path": (*path_roles, role),
                "source_extended_words": extended_words,
                "restored_target_roles": tuple(sorted(restored_next)),
                "parent_state_id": parent_state_id,
                "parent_path_binding_id": parent_path_binding_id,
                "dummy_order": raw_root["target_dummy_roles"],
                "restored_role_to_label": tuple(sorted(restored_next.items())),
                "source_graph_id": source_graph_id,
                "target_graph_id": target_graph_id,
                "source_raw_mixed_vertex_to_canonical": tuple(
                    sorted(source_transport.items())
                ),
                "target_raw_mixed_vertex_to_canonical": tuple(
                    sorted(target_transport.items())
                ),
                "canonical_state_id": state_id,
            }
            coverage["path_binding_payload_sha256"] = stable_hash(coverage)
            coverage["path_binding_id"] = coverage[
                "path_binding_payload_sha256"
            ]
            prior_state = states.get(state_id)
            if prior_state is not None:
                if "terminal_classification" not in prior_state:
                    raise AssertionError("canonical state revisited before child closure")
                if prior_state["terminal_classification"] == "refined_by_next_restoration":
                    child_ids = visit(
                        source_variant,
                        source_assignment,
                        extended_words,
                        target_variant,
                        target_assignment,
                        restored_next,
                        remaining_next,
                        (*path_roles, role),
                        raw_root,
                        state_id,
                        coverage["path_binding_id"],
                    )
                    if tuple(child_ids) != tuple(prior_state["children"]):
                        raise AssertionError(
                            "merged rooted state has provenance-dependent children"
                        )
                    coverage["child_state_ids"] = tuple(child_ids)
                else:
                    coverage["child_state_ids"] = ()
                prior_state["raw_coverage"].append(coverage)
                continue

            source_descriptors = cached_deck(
                source_graph, current_p + 1, source_graph_id
            )
            if target_descriptors is None:
                target_descriptors = cached_deck(
                    target_graph, current_p + 1, target_graph_id
                )
            classification, witness = relation_witness(
                source_descriptors, target_descriptors, invariants,
                bit_cache, sign_cache,
                register_polynomial=register_polynomial,
            )
            state = {
                "schema": 3,
                "state_id": state_id,
                "fixed_full_root_case_id": raw_root["root_case_id"],
                "selected_port_count": current_p + 1,
                "source_mixed_code_sha256": hashlib.sha256(
                    source_code.encode()
                ).hexdigest(),
                "source_graph_id": source_graph_id,
                "target_completion_mixed_code_sha256": hashlib.sha256(
                    target_code.encode()
                ).hexdigest(),
                "target_graph_id": target_graph_id,
                "port_matching": tuple(
                    (f"L_{index}", f"L_{index}")
                    for index in range(current_p + 1)
                ),
                "remaining_target_role_count": len(remaining_next),
                "remaining_target_roles": remaining_next,
                "probe_classification": classification,
                "probe_witness": witness,
                "raw_coverage": [],
                "children": [],
            }
            states[state_id] = state
            if len(states) % 250 == 0:
                print(json.dumps({
                    "hard_cover_progress": {
                        "selected_outgoing": n,
                        "states": len(states),
                        "current_ports": current_p + 1,
                        "remaining_roles": len(remaining_next),
                        "descriptor_cache": len(deck_cache),
                        "sign_cache": len(sign_cache),
                    }
                }, sort_keys=True), flush=True)

            if classification in {
                "generic_polynomial_separation",
                "strict_open_cube_separation",
            }:
                state["terminal_classification"] = classification
                coverage["child_state_ids"] = ()
                state["raw_coverage"].append(coverage)
                continue
            if remaining_next:
                child_ids = visit(
                    source_variant, source_assignment, extended_words,
                    target_variant, target_assignment, restored_next,
                    remaining_next, (*path_roles, role), raw_root,
                    state_id, coverage["path_binding_id"],
                )
                state["children"] = child_ids
                state["terminal_classification"] = "refined_by_next_restoration"
                coverage["child_state_ids"] = tuple(child_ids)
                state["raw_coverage"].append(coverage)
                continue

            if classification == "equal_invariant_signature":
                source_t = canonical_mixed(t_quotient(sd0(source_graph)))[0]
                target_t = canonical_mixed(t_quotient(sd0(target_graph)))[0]
                if source_t == target_t:
                    if source_code == target_code:
                        terminal = "support_prefix_labelled_isomorphism"
                    else:
                        terminal = "support_prefix_ordinary_T"
                    state["terminal_classification"] = terminal
                    state["terminal_witness"] = {
                        "t_quotient_code_sha256": hashlib.sha256(
                            source_t.encode()
                        ).hexdigest(),
                        "mixed_codes_equal": source_code == target_code,
                    }
                else:
                    state["terminal_classification"] = "unresolved_equal_non_T"
                    state["terminal_witness"] = {
                        "source_t_sha256": hashlib.sha256(source_t.encode()).hexdigest(),
                        "target_t_sha256": hashlib.sha256(target_t.encode()).hexdigest(),
                    }
            else:
                if classification == "unresolved_unsigned_signature":
                    refined, refined_witness = relation_witness(
                        source_descriptors, target_descriptors, invariants,
                        bit_cache, sign_cache,
                        register_polynomial=register_polynomial,
                        exact_sign=True,
                    )
                    state["probe_classification"] = refined
                    state["probe_witness"] = refined_witness
                    state["terminal_classification"] = refined
                else:
                    state["terminal_classification"] = classification
            coverage["child_state_ids"] = tuple(state["children"])
            state["raw_coverage"].append(coverage)
        return sorted(set(result_ids))

    for root_case_id, root_key, source_variant, source_assignment, target_variant, target_assignment, dummy_roles in root_cases:
        raw_root = {
            **root_key,
            "root_case_id": root_case_id,
        }
        entry_state_ids = visit(
            source_variant, source_assignment,
            tuple(tuple(word) for word in source_variant.provenance[2]),
            target_variant, target_assignment, {}, dummy_roles, (), raw_root,
        )
        root_case_records[root_case_id]["entry_state_ids"] = tuple(entry_state_ids)

    records = states

    def write_library(path, rows):
        hasher = hashlib.sha256()
        with path.open("wb") as raw:
            with gzip.GzipFile(
                filename="", mode="wb", fileobj=raw, mtime=0
            ) as handle:
                for key in sorted(rows):
                    line = (
                        json.dumps(
                            rows[key], sort_keys=True, separators=(",", ":")
                        )
                        + "\n"
                    ).encode()
                    handle.write(line)
                    hasher.update(line)
        return hasher.hexdigest()

    graph_path = (
        HERE / "certificates" / f"hard_cover_graphs_n{n}_{tag}.jsonl.gz"
    )
    polynomial_path = (
        HERE / "certificates" / f"hard_cover_polynomials_n{n}_{tag}.jsonl.gz"
    )
    root_case_path = (
        HERE / "certificates" / f"hard_cover_root_cases_n{n}_{tag}.jsonl.gz"
    )
    graph_stream_sha = write_library(graph_path, graph_library)
    polynomial_stream_sha = write_library(polynomial_path, polynomial_library)
    root_case_stream_sha = write_library(root_case_path, root_case_records)

    path = HERE / "certificates" / f"hard_cover_n{n}_{tag}.jsonl.gz"
    hasher = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as handle:
            for relation_id in sorted(records):
                row = records[relation_id]
                row["raw_coverage"] = sorted(
                    row["raw_coverage"], key=stable_hash
                )
                row["binding_sha256"] = stable_hash(row)
                counts[row.get("terminal_classification", row["probe_classification"])] += 1
                line = (json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n").encode()
                handle.write(line)
                hasher.update(line)
    unresolved = sum(value for key, value in counts.items() if key.startswith("unresolved"))
    return {
        "selected_outgoing": n,
        "selected_port_count": n + 1,
        "all_common_selected_signatures": len(common_all),
        "common_selected_signatures": len(common),
        "selected_signature_indices": signature_indices,
        "all_root_cases": all_root_case_count,
        "selected_root_cases": len(root_cases),
        "selected_root_case_indices": root_case_indices,
        "selected_root_range": [root_start, root_stop],
        "root_case_commitment": stable_hash([
            (row[0], row[1]) for row in root_cases
        ]),
        "canonical_restored_relations": len(records),
        "counts": dict(sorted(counts.items())),
        "unresolved": unresolved,
        "relation_path": str(path.relative_to(HERE.parent)),
        "relation_stream_sha256": hasher.hexdigest(),
        "descriptor_cache_scope": "selected_port_count_and_exact_rooted_graph_id",
        "descriptor_mask_normalization": (
            "minimum_of_quartet_side_and_complement_on_zero_sum_characters"
        ),
        "descriptor_cache_size": len(deck_cache),
        "sign_cache_size": len(sign_cache),
        "graph_library_records": len(graph_library),
        "graph_library_path": str(graph_path.relative_to(HERE.parent)),
        "graph_library_stream_sha256": graph_stream_sha,
        "polynomial_library_records": len(polynomial_library),
        "polynomial_library_path": str(
            polynomial_path.relative_to(HERE.parent)
        ),
        "polynomial_library_stream_sha256": polynomial_stream_sha,
        "root_case_records": len(root_case_records),
        "root_case_path": str(root_case_path.relative_to(HERE.parent)),
        "root_case_stream_sha256": root_case_stream_sha,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=(3, 4, 5, 6))
    parser.add_argument("--bit-cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--signature-index", action="append", type=int)
    parser.add_argument("--root-case-index", action="append", type=int)
    parser.add_argument("--root-start", type=int)
    parser.add_argument("--root-stop", type=int)
    parser.add_argument("--list-root-cases", action="store_true")
    parser.add_argument("--tag", default="all")
    parser.add_argument("--source-core-id", action="append")
    parser.add_argument("--source-extra-count", action="append", type=int)
    args = parser.parse_args()
    invariants = load_invariants()
    bit_cache = load_bit_cache(args.bit_cache)
    rows = []
    for n in args.sizes:
        summary, working = compile_size(
            n,
            invariants,
            bit_cache,
            source_core_ids=(
                frozenset(args.source_core_id)
                if args.source_core_id is not None else None
            ),
            source_extra_counts=(
                frozenset(args.source_extra_count)
                if args.source_extra_count is not None else None
            ),
        )
        indices = (
            tuple(args.signature_index) if args.signature_index is not None else None
        )
        cover = compile_hard_cover(
            n, working, invariants, bit_cache,
            signature_indices=indices,
            root_case_indices=(
                tuple(args.root_case_index)
                if args.root_case_index is not None else None
            ),
            root_start=args.root_start,
            root_stop=args.root_stop,
            list_root_cases=args.list_root_cases,
            tag=args.tag,
        )
        rows.append({"bounded_summary": summary, "hard_cover": cover})
        print(json.dumps(cover, sort_keys=True), flush=True)
        if not args.list_root_cases and cover["unresolved"]:
            raise SystemExit(f"unresolved hard-cover relations at n={n}")
    payload = {
        "schema": 1,
        "relation_action": "anchor every source boundary; full target S_p",
        "target_roles": ("selected incoming", "zero-character marginalized incoming"),
        "source_core_filter": args.source_core_id,
        "source_extra_count_filter": args.source_extra_count,
        "runs": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "sha256": sha256(args.output)}, sort_keys=True))


if __name__ == "__main__":
    main()
