#!/usr/bin/env python3
"""Exact replay of path-bound ``A+p`` and ``A+p+q`` certificates.

This verifier does not trust classifications printed by the producer.  It
rebuilds every rooted graph, insertion/deletion, quartet descriptor, selected
invariant pullback, strict-sign certificate, and ordinary-T transport from the
content-addressed streams.  A separately written clean-room package remains
the independent implementation required for theorem promotion.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

from atlas_compiler import load_bit_cache, stable_hash
from graph_model import (
    canonical_mixed,
    mixed_local_strong,
    rooted_validation,
    sd0,
    t_quotient,
)
from hard_cover_compiler import (
    deck_signature,
    exact_poly_hash,
    full_deck,
    load_invariants,
)
from jc_tensor import pullback
from probe_extension_compiler import (
    ALLOWED_BASE,
    ALLOWED_CHILD,
    SEPARATED,
    admissible_internal_arcs,
    delete_port,
    graph_from_row,
    graph_payload,
    insert_port,
    quotient_transport,
    restricts_to,
    transport_metadata,
)
from sign_certificate import certify as certify_sign


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path, key: str) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    digest = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            digest.update(line.encode())
            row = json.loads(line)
            identifier = str(row[key])
            if identifier in rows:
                raise AssertionError((path, "duplicate", identifier))
            rows[identifier] = row
    return rows, digest.hexdigest()


def resolve(path: str, *, summary_path: Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    choices = (
        PROJECT / candidate,
        summary_path.parent / candidate,
        HERE.parent.parent / candidate,
    )
    for choice in choices:
        if choice.exists():
            return choice.resolve()
    raise FileNotFoundError(path)


def exact_record_id(row: dict, key: str) -> str:
    payload = {name: value for name, value in row.items() if name not in {"schema", key}}
    return stable_hash(payload)


def polynomial_from_row(row: dict):
    return {
        tuple(int(value) for value in exponents): int(coefficient)
        for exponents, coefficient in row["terms"]
    }


def verify_graph_row(identifier: str, row: dict):
    graph = graph_from_row(row)
    if stable_hash(graph_payload(graph)) != identifier:
        raise AssertionError((identifier, "graph content address"))
    valid, problems = rooted_validation(graph)
    if not valid or problems:
        raise AssertionError((identifier, "invalid rooted graph", problems))
    mixed = sd0(graph)
    if not mixed_local_strong(mixed):
        raise AssertionError((identifier, "outside standard-strong local class"))
    code, raw_map = canonical_mixed(mixed)
    t_code, t_map = canonical_mixed(t_quotient(mixed))
    expected = {
        "rooted_valid": valid,
        "rooted_validation_problems": problems,
        "standard_strong_local": True,
        "standard_mixed_code": code,
        "t_quotient_code": t_code,
        "raw_mixed_vertex_to_canonical": [list(pair) for pair in sorted(raw_map.items())],
        "raw_t_quotient_vertex_to_canonical": [list(pair) for pair in sorted(t_map.items())],
        "admissible_internal_arcs": [list(arc) for arc in admissible_internal_arcs(graph)],
    }
    for key, value in expected.items():
        if row[key] != value:
            raise AssertionError((identifier, key, row[key], value))
    return graph


def load_base_paths(summary_paths: set[Path]):
    states: dict[tuple[str, str], dict] = {}
    paths: dict[tuple[str, str], tuple[dict, dict]] = {}
    for summary_path in sorted(summary_paths):
        summary = json.loads(summary_path.read_text())
        for run in summary["runs"]:
            cover = run["hard_cover"]
            state_path = resolve(cover["relation_path"], summary_path=summary_path)
            state_rows, _digest = load_jsonl(state_path, "state_id")
            for state_id, state in state_rows.items():
                key = str(summary_path), state_id
                if key in states:
                    raise AssertionError((summary_path, state_id, "duplicate base state"))
                states[key] = state
                for coverage in state["raw_coverage"]:
                    path_key = str(summary_path), str(coverage["path_binding_id"])
                    if path_key in paths:
                        raise AssertionError((summary_path, path_key, "duplicate base path"))
                    paths[path_key] = state, coverage
    return states, paths


def verify_selected_witness(
    state: dict,
    source_graph,
    target_graph,
    source_deck,
    target_deck,
    polynomials: dict[str, dict],
    invariants,
    bit_cache,
    sign_cache,
):
    source_signature = deck_signature(source_deck, invariants, bit_cache)
    target_signature = deck_signature(target_deck, invariants, bit_cache)
    probe = state["probe_classification"]
    witness = state["probe_witness"]

    if probe == "generic_polynomial_separation":
        chunk = int(witness["quartet_chunk"])
        invariant_index = int(witness["invariant_index"])
        source_poly = pullback(source_deck[chunk], invariants[invariant_index])
        target_poly = pullback(target_deck[chunk], invariants[invariant_index])
        if not source_poly or target_poly:
            raise AssertionError((state["state_id"], "bad generic separator"))
        if exact_poly_hash(source_poly) != witness["source_pullback_exact_sha256"]:
            raise AssertionError((state["state_id"], "source polynomial hash"))
        row = polynomials[witness["source_pullback_id"]]
        if polynomial_from_row(row) != source_poly:
            raise AssertionError((state["state_id"], "source polynomial body"))
        if state["classification"] != probe:
            raise AssertionError((state["state_id"], "generic class"))
        return

    if probe == "strict_open_cube_separation":
        chunk = int(witness["quartet_chunk"])
        invariant_index = int(witness["invariant_index"])
        source_poly = pullback(source_deck[chunk], invariants[invariant_index])
        target_poly = pullback(target_deck[chunk], invariants[invariant_index])
        if source_poly or not target_poly:
            raise AssertionError((state["state_id"], "bad strict separator"))
        if exact_poly_hash(target_poly) != witness["target_pullback_exact_sha256"]:
            raise AssertionError((state["state_id"], "target polynomial hash"))
        row = polynomials[witness["target_pullback_id"]]
        if polynomial_from_row(row) != target_poly:
            raise AssertionError((state["state_id"], "target polynomial body"))
        polynomial_hash = exact_poly_hash(target_poly)
        if polynomial_hash not in sign_cache:
            sign_cache[polynomial_hash] = certify_sign(
                target_poly, max_elevation=5
            )
        sign = sign_cache[polynomial_hash]
        if not sign["certified"] or int(sign["strict_sign"]) != int(witness["target_strict_sign"]):
            raise AssertionError((state["state_id"], "strict sign replay", sign))
        if state["classification"] != probe:
            raise AssertionError((state["state_id"], "strict class"))
        return

    if probe != "equal_invariant_signature" or source_signature != target_signature:
        raise AssertionError((state["state_id"], "unresolved or inconsistent signature", probe))
    _code, transport, canonical = quotient_transport(source_graph, target_graph)
    source_code = canonical_mixed(sd0(source_graph))[0]
    target_code = canonical_mixed(sd0(target_graph))[0]
    expected_class = "labelled_isomorphism" if source_code == target_code else "ordinary_T"
    if expected_class not in ALLOWED_CHILD or state["classification"] != expected_class:
        raise AssertionError((state["state_id"], "terminal topology", expected_class))
    expected_transport = transport_metadata(source_graph, target_graph, transport)
    if state.get("transport") != json.loads(json.dumps(expected_transport)):
        raise AssertionError((state["state_id"], "transport"))
    if state.get("canonicalization") != json.loads(json.dumps(canonical)):
        raise AssertionError((state["state_id"], "canonicalization"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--bit-cache", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    summary_path = args.summary.resolve()
    summary = json.loads(summary_path.read_text())
    if summary["schema"] != "path-bound-common-anchor-probe-extension-v1":
        raise AssertionError("unexpected probe-extension schema")
    if summary["status"] != "EXACTLY_COMPUTED":
        raise AssertionError(("producer status", summary["status"]))

    streams = {}
    stream_digests = {}
    keys = {
        "states": "state_id",
        "bindings": "probe_path_binding_id",
        "graphs": "graph_id",
        "polynomials": "polynomial_id",
    }
    for name, key in keys.items():
        path = resolve(summary["streams"][name]["path"], summary_path=summary_path)
        rows, digest = load_jsonl(path, key)
        if len(rows) != int(summary["streams"][name]["records"]):
            raise AssertionError((name, "record count"))
        if digest != summary["streams"][name]["sha256"]:
            raise AssertionError((name, "normalized stream hash"))
        streams[name] = rows
        stream_digests[name] = digest

    input_paths = {resolve(path, summary_path=summary_path) for path in summary["input_sha256"]}
    for original, expected in summary["input_sha256"].items():
        path = resolve(original, summary_path=summary_path)
        if sha256(path) != expected:
            raise AssertionError((original, "input hash"))
    base_summaries = {
        path for path in input_paths
        if path.name.endswith("summary.json") or "summary" in path.name
    }
    _base_states, base_paths = load_base_paths(base_summaries)

    graphs = {
        identifier: verify_graph_row(identifier, row)
        for identifier, row in streams["graphs"].items()
    }
    polynomials = streams["polynomials"]
    for identifier, row in polynomials.items():
        payload = {key: row[key] for key in ("schema", "variable_count", "terms")}
        if stable_hash(payload) != identifier:
            raise AssertionError((identifier, "polynomial content address"))
        poly = polynomial_from_row(row)
        if poly and len(next(iter(poly))) != int(row["variable_count"]):
            raise AssertionError((identifier, "variable count"))

    states = streams["states"]
    invariants = load_invariants()
    bit_cache = load_bit_cache(args.bit_cache)
    deck_cache = {}
    sign_cache = {}
    for identifier, state in states.items():
        if exact_record_id(state, "state_id") != identifier:
            raise AssertionError((identifier, "state content address"))
        source_graph = graphs[state["source_graph_id"]]
        target_graph = graphs[state["target_graph_id"]]
        p = int(state["selected_port_count"])
        source_key = state["source_graph_id"], p
        target_key = state["target_graph_id"], p
        if source_key not in deck_cache:
            deck_cache[source_key] = full_deck(source_graph, p)
        if target_key not in deck_cache:
            deck_cache[target_key] = full_deck(target_graph, p)
        verify_selected_witness(
            state, source_graph, target_graph,
            deck_cache[source_key], deck_cache[target_key], polynomials,
            invariants, bit_cache, sign_cache,
        )

    bindings = streams["bindings"]
    counts = Counter()
    referenced_states = set()
    for identifier, binding in bindings.items():
        if exact_record_id(binding, "probe_path_binding_id") != identifier:
            raise AssertionError((identifier, "binding content address"))
        stage = binding["stage"]
        if stage not in {"A_plus_p", "A_plus_p_plus_q"}:
            raise AssertionError((identifier, stage))
        state = states[binding["state_id"]]
        if state["stage"] != stage:
            raise AssertionError((identifier, "state stage"))
        referenced_states.add(state["state_id"])
        source_parent = graphs[binding["source_parent_graph_id"]]
        target_parent = graphs[binding["target_parent_graph_id"]]
        source_child = graphs[binding["source_child_graph_id"]]
        target_child = graphs[binding["target_child_graph_id"]]
        rebuilt_source, source_deletion = insert_port(
            source_parent,
            tuple(binding["source_insertion"]["subdivided_parent_arc"]),
            str(binding["source_insertion"]["inserted_label"]),
        )
        rebuilt_target, target_deletion = insert_port(
            target_parent,
            tuple(binding["target_insertion"]["subdivided_parent_arc"]),
            str(binding["target_insertion"]["inserted_label"]),
        )
        if rebuilt_source != source_child or rebuilt_target != target_child:
            raise AssertionError((identifier, "insertion child"))
        if source_deletion != binding["source_insertion"] or target_deletion != binding["target_insertion"]:
            raise AssertionError((identifier, "insertion metadata"))
        if delete_port(source_child, binding["source_insertion"]) != source_parent:
            raise AssertionError((identifier, "source deletion"))
        if delete_port(target_child, binding["target_insertion"]) != target_parent:
            raise AssertionError((identifier, "target deletion"))
        if not binding["source_deletion_exact_parent"] or not binding["target_deletion_exact_parent"]:
            raise AssertionError((identifier, "stored deletion boolean"))
        if state["source_graph_id"] != binding["source_child_graph_id"] or state["target_graph_id"] != binding["target_child_graph_id"]:
            raise AssertionError((identifier, "state graph binding"))

        base_key = (str(Path(binding["base_summary"])), str(binding["base_path_binding_id"]))
        if base_key not in base_paths:
            # Normalize relative/absolute spelling without weakening identity.
            normalized = str(resolve(binding["base_summary"], summary_path=summary_path))
            matches = [key for key in base_paths if str(Path(key[0]).resolve()) == normalized and key[1] == base_key[1]]
            if len(matches) != 1:
                raise AssertionError((identifier, "base path binding", base_key))
            base_key = matches[0]
        base_state, base_coverage = base_paths[base_key]
        if base_state["state_id"] != binding["base_state_id"]:
            raise AssertionError((identifier, "base state"))
        if base_state["terminal_classification"] not in ALLOWED_BASE:
            raise AssertionError((identifier, "disallowed base terminal"))
        if base_coverage["root_case_id"] != binding["restoration_root_id"]:
            raise AssertionError((identifier, "root case"))
        if base_coverage["dummy_order"] != binding["base_dummy_order"]:
            raise AssertionError((identifier, "dummy order"))
        if base_coverage["restored_role_to_label"] != binding["base_restored_role_to_label"]:
            raise AssertionError((identifier, "restored roles"))

        if stage == "A_plus_p":
            if binding["parent_probe_path_binding_id"] is not None:
                raise AssertionError((identifier, "p has probe parent"))
            _code, base_transport, canonical = quotient_transport(source_parent, target_parent)
            if binding["base_transport"] != json.loads(json.dumps(
                transport_metadata(source_parent, target_parent, base_transport)
            )):
                raise AssertionError((identifier, "base transport"))
            if binding["base_canonicalization"] != json.loads(json.dumps(canonical)):
                raise AssertionError((identifier, "base canonicalization"))
            if state["classification"] in ALLOWED_CHILD:
                child_transport = tuple(
                    tuple(pair) for pair in state["transport"]["vertex_transport"]
                )
                if not restricts_to(child_transport, base_transport):
                    raise AssertionError((identifier, "p incoherent transport"))
        else:
            parent_id = binding["parent_probe_path_binding_id"]
            if parent_id not in bindings:
                raise AssertionError((identifier, "missing p parent"))
            parent = bindings[parent_id]
            parent_state = states[parent["state_id"]]
            if parent["stage"] != "A_plus_p" or parent_state["classification"] not in ALLOWED_CHILD:
                raise AssertionError((identifier, "q descended from disallowed p"))
            if parent["source_child_graph_id"] != binding["source_parent_graph_id"] or parent["target_child_graph_id"] != binding["target_parent_graph_id"]:
                raise AssertionError((identifier, "q parent graphs"))
            parent_transport = tuple(
                tuple(pair) for pair in parent_state["transport"]["vertex_transport"]
            )
            if binding["parent_transport"] != parent_state["transport"]:
                raise AssertionError((identifier, "stored parent transport"))
            if state["classification"] in ALLOWED_CHILD:
                child_transport = tuple(
                    tuple(pair) for pair in state["transport"]["vertex_transport"]
                )
                if not restricts_to(child_transport, parent_transport):
                    raise AssertionError((identifier, "q incoherent transport"))
        counts[f"{stage}::{state['classification']}"] += 1

    if referenced_states != set(states):
        raise AssertionError(("orphan states", sorted(set(states) - referenced_states)[:5]))
    if dict(sorted(counts.items())) != summary["counts"]:
        raise AssertionError(("classification counts", counts, summary["counts"]))
    unresolved = set(row["classification"] for row in states.values()) - SEPARATED - ALLOWED_CHILD
    if unresolved:
        raise AssertionError(("unresolved classes", unresolved))
    if len([row for row in bindings.values() if row["stage"] == "A_plus_p"]) < int(summary["base_terminal_paths"]):
        raise AssertionError("not every base path has a p extension")

    result = {
        "schema": "probe-extension-primary-replay-v1",
        "status": "EXACTLY_VERIFIED",
        "summary_path": str(summary_path),
        "summary_sha256": sha256(summary_path),
        "stream_sha256": stream_digests,
        "base_terminal_states": int(summary["base_terminal_states"]),
        "base_terminal_paths": int(summary["base_terminal_paths"]),
        "graphs": len(graphs),
        "polynomials": len(polynomials),
        "states": len(states),
        "bindings": len(bindings),
        "counts": dict(sorted(counts.items())),
        "unresolved": [],
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
