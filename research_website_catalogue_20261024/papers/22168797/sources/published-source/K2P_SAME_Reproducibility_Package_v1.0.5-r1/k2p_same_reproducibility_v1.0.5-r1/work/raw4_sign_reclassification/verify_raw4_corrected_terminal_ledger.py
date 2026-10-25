#!/usr/bin/env python3
"""Fail-closed independent replay of the corrected raw-four terminal overlay."""

from __future__ import annotations

import argparse
import collections
import fractions
import hashlib
import importlib.util
import itertools
import json
import math
import sys
import time
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (  # noqa: E402
    StrictJSONError,
    decode_json_document,
    iter_canonical_gzip_jsonl,
)

ATLAS_PATH = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
RAW_LEDGER = PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
RAW_SUMMARY = PROJECT / "work/raw_ledger_audit/artifacts/raw_ledger_summary.json"
DEFAULT_CERTIFICATE = HERE / "raw4_corrected_terminal_ledger.json"
DEFAULT_REPORT = HERE / "raw4_corrected_replay_certificate.json"


class ReplayFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ReplayFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sparse_payload(polynomial):
    return [[list(exponent), str(coefficient)] for exponent, coefficient in sorted(polynomial.items())]


def sparse_hash(polynomial):
    return sha(sparse_payload(polynomial))


def descriptor_digest(descriptor):
    return sha([
        descriptor.k,
        descriptor.retic_count,
        descriptor.edge_class_count,
        descriptor.outputs,
        descriptor.edge_signatures,
    ])


def load_atlas():
    spec = importlib.util.spec_from_file_location("raw4_corrected_replay_atlas", ATLAS_PATH)
    require(spec is not None and spec.loader is not None, "atlas import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def t_pullback(atlas, descriptor, outputs, triple, orientation):
    assignments = atlas.orbit_assignments(descriptor.k)
    output_index = {assignment: index for index, assignment in enumerate(assignments)}
    others = sorted(set(triple) - {orientation})
    order = (others[0], others[1], orientation)

    def get(characters):
        assignment = [0] * descriptor.k
        for label, character in zip(order, characters):
            assignment[label] = character
        return outputs[output_index[atlas.ct_orbit_rep(tuple(assignment))]]

    v_value = get((1, 3, 2))
    x_s = get((1, 1, 0))
    x_g = get((2, 2, 0))
    y_g = get((2, 0, 2))
    z_g = get((0, 2, 2))
    return atlas.sparse_lincomb(
        [atlas.sparse_mul_many([v_value, v_value, x_g]),
         atlas.sparse_mul_many([x_s, x_s, y_g, z_g])],
        [1, -1],
    )


def direct_bernstein_certificate(polynomial):
    """Replay by the closed multivariate coefficient formula.

    This intentionally differs from the builder's successive axis transforms.
    """
    require(polynomial, "empty source pullback")
    parameter_count = len(next(iter(polynomial)))
    monomial = tuple(
        min(exponent[index] for exponent in polynomial)
        for index in range(parameter_count)
    )
    active = tuple(
        index
        for index in range(parameter_count)
        if len({exponent[index] - monomial[index] for exponent in polynomial}) > 1
    )
    residual = {
        tuple(exponent[index] - monomial[index] for index in active): fractions.Fraction(coefficient)
        for exponent, coefficient in polynomial.items()
    }
    degree = tuple(max(exponent[index] for exponent in residual) for index in range(len(active)))
    coefficient_count = math.prod(value + 1 for value in degree)
    require(coefficient_count <= 100_000, f"replay Bernstein tensor bound:{coefficient_count}")
    values = []
    for beta in itertools.product(*(range(value + 1) for value in degree)):
        total = fractions.Fraction(0)
        for alpha, coefficient in residual.items():
            if not all(left <= right for left, right in zip(alpha, beta)):
                continue
            multiplier = fractions.Fraction(1)
            for n, left, right in zip(degree, alpha, beta):
                multiplier *= fractions.Fraction(math.comb(right, left), math.comb(n, left))
            total += coefficient * multiplier
        values.append(total)
    signs = collections.Counter(-1 if value < 0 else 1 if value > 0 else 0 for value in values)
    require(signs[1] == 0 and signs[-1] > 0, f"nonnegative Bernstein replay:{signs}")
    result = {
        "method": "exact_tensor_Bernstein_after_positive_monomial",
        "positive_monomial_exponent": list(monomial),
        "active_parameter_indices": list(active),
        "Bernstein_multidegree": list(degree),
        "Bernstein_coefficient_count": coefficient_count,
        "negative_coefficients": signs[-1],
        "zero_coefficients": signs[0],
        "positive_coefficients": signs[1],
        "minimum_coefficient": str(min(values)),
        "maximum_coefficient": str(max(values)),
        "strict_domain": "0<all edge-sector and inheritance parameters<1",
        "conclusion": "strictly_negative",
    }
    result["certificate_sha256"] = sha(result)
    return result


def ordered_pair_graph(atlas, source_graph, target_graph):
    result = nx.Graph()
    for side, graph in (("S", source_graph), ("T", target_graph)):
        try:
            expanded = atlas.mixed_incidence_graph(atlas.sd0_mixed(graph))
        except ValueError:
            expanded = nx.Graph()
            for node, data in graph.nodes(data=True):
                expanded.add_node(
                    ("v", node),
                    kind=f"rooted_vertex:{data.get('role')}",
                    label=data.get("label"),
                )
            for number, (tail, head) in enumerate(
                sorted(graph.edges(), key=lambda edge: (repr(edge[0]), repr(edge[1])))
            ):
                edge_node = ("a", number)
                expanded.add_node(edge_node, kind="rooted_arc", label=None)
                expanded.add_edge(edge_node, ("v", tail), head=False)
                expanded.add_edge(edge_node, ("v", head), head=True)
        for node, data in expanded.nodes(data=True):
            result.add_node(
                (side, node),
                color=f"{side}|{data.get('kind')}|{data.get('label')!r}",
            )
        for left, right, data in expanded.edges(data=True):
            result.add_edge((side, left), (side, right), head=bool(data.get("head")))
    return result


class PairRegistry:
    def __init__(self):
        self.representatives = []
        self.buckets = collections.defaultdict(list)

    def add(self, graph):
        digest = nx.weisfeiler_lehman_graph_hash(
            graph, node_attr="color", edge_attr="head", iterations=8
        )
        node_match = lambda left, right: left.get("color") == right.get("color")
        edge_match = lambda left, right: left.get("head") == right.get("head")
        for class_id in self.buckets[digest]:
            if nx.is_isomorphic(
                graph,
                self.representatives[class_id],
                node_match=node_match,
                edge_match=edge_match,
            ):
                return class_id
        class_id = len(self.representatives)
        self.representatives.append(graph)
        self.buckets[digest].append(class_id)
        return class_id


def main():
    if not __debug__:
        raise ReplayFailure("RAW4_CORRECTED_REPLAY_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    started = time.monotonic()
    certificate = decode_json_document(
        args.certificate.read_bytes(),
        label=args.certificate.name,
        require_object=True,
    )
    claimed_payload = certificate.get("payload_sha256")
    unhashed = dict(certificate)
    unhashed.pop("payload_sha256", None)
    require(claimed_payload == sha(unhashed), "payload hash")
    require(certificate.get("schema") == "k2p-raw4-corrected-terminal-overlay-v2", "schema")
    require(certificate.get("status") == "PASS", "status")
    require(certificate["inputs"]["atlas_sha256"] == sha_file(ATLAS_PATH), "atlas input")
    require(certificate["inputs"]["historical_raw_ledger_sha256"] == sha_file(RAW_LEDGER), "raw input")
    require(certificate["inputs"]["historical_raw_summary_sha256"] == sha_file(RAW_SUMMARY), "summary input")

    raw_rows = []
    for row in iter_canonical_gzip_jsonl(RAW_LEDGER, label=RAW_LEDGER.name):
        if row.get("topology_exclusion_reason") == "tree_sunlet":
            raw_rows.append(row)
    coverage = certificate.get("coverage", [])
    require(len(raw_rows) == 16_974 and len(coverage) == len(raw_rows), "coverage census")
    require(len({row["raw_id"] for row in coverage}) == len(coverage), "coverage raw-id uniqueness")
    require([row["raw_id"] for row in coverage] == [row["raw_id"] for row in raw_rows], "ordered raw coverage")
    require(certificate["coverage_row_hashes"] == [sha(row) for row in coverage], "coverage row hashes")
    require(certificate["coverage_hash_root"] == sha(certificate["coverage_row_hashes"]), "coverage hash root")
    require(certificate["corrected_reason_census"] == {"full_map_Ti_strict_sign": 16_974}, "reason census")
    require(certificate["corrected_category_census"] == {"exact_exclusion": 16_974}, "category census")
    require(certificate["parent_census_effect"] == {
        "historical_restoration_parent_classes": 997,
        "new_restoration_parent_classes_from_corrected_family": 0,
        "corrected_total_restoration_parent_classes": 997,
    }, "parent census effect")

    atlas = load_atlas()
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    source_descriptors = [atlas.model_descriptor_fast2(source.graph) for source in sources]
    source_outputs = [atlas.output_sparse_polynomials(descriptor) for descriptor in source_descriptors]

    # Recompute every stored signed polynomial and its Bernstein tensor before
    # accepting any raw-row assignment.
    signed_polynomials = {}
    sign_records = certificate.get("sign_certificates", {})
    require(len(sign_records) == 8, "sign certificate census")
    for polynomial_sha256, record in sorted(sign_records.items()):
        witnesses = record.get("source_witnesses", [])
        require(witnesses, f"missing source witness:{polynomial_sha256}")
        source_index, triple, orientation = witnesses[0]
        polynomial = t_pullback(
            atlas,
            source_descriptors[source_index],
            source_outputs[source_index],
            tuple(triple),
            orientation,
        )
        require(sparse_hash(polynomial) == polynomial_sha256, "signed polynomial hash")
        require(len(polynomial) == record["source_pullback_term_count"], "signed term count")
        replayed = direct_bernstein_certificate(polynomial)
        require(replayed == record["sign_certificate"], f"Bernstein certificate mismatch:{polynomial_sha256}")
        signed_polynomials[polynomial_sha256] = polynomial

    prepared_sources = [atlas.prepare_mixed_source(source.graph) for source in sources]
    selected_cache = {}
    target_descriptor_cache = {}
    target_outputs_cache = {}
    target_pullback_cache = {}
    descriptor_pair_ids = {}
    descriptor_pair_counts = collections.Counter()
    pair_registry = PairRegistry()
    exact_relations = collections.Counter()
    relation_classes = collections.Counter()
    target_zero_sha256 = sparse_hash({})

    for ordinal, (raw, bound) in enumerate(zip(raw_rows, coverage)):
        for field in ("raw_id", "source_index", "target_index"):
            require(bound[field] == raw[field], f"raw binding {field}:{ordinal}")
        require(tuple(bound["port_permutation"]) == tuple(raw["port_permutation"]), f"raw permutation:{ordinal}")
        require(bound["historical_reason"] == "tree_sunlet_REVOKED", f"historical marker:{ordinal}")
        require(bound["corrected_category"] == "exact_exclusion", f"category:{ordinal}")
        require(bound["corrected_reason"] == "full_map_Ti_strict_sign", f"reason:{ordinal}")
        require(bound["source_pullback_sha256"] in sign_records, f"unknown sign certificate:{ordinal}")

        selected_key = (raw["target_index"], tuple(raw["port_permutation"]))
        if selected_key not in selected_cache:
            relabelled = atlas.relabel_record(targets[raw["target_index"]], selected_key[1])
            selected_cache[selected_key] = atlas.selected_graph_from_completion(relabelled)
        selected_target = selected_cache[selected_key]
        relation = atlas.mixed_relation_exact_prepared(
            prepared_sources[raw["source_index"]], selected_target
        )
        require(relation == bound["exact_full_graph_relation"] == "none", f"graph relation:{ordinal}")
        exact_relations[relation] += 1
        pair_registry.add(ordered_pair_graph(atlas, sources[raw["source_index"]].graph, selected_target))

        source_descriptor = source_descriptors[raw["source_index"]]
        target_descriptor = atlas.model_descriptor_fast2(selected_target)
        descriptor_pair = (source_descriptor, target_descriptor)
        if descriptor_pair not in descriptor_pair_ids:
            descriptor_pair_ids[descriptor_pair] = len(descriptor_pair_ids)
        descriptor_class_id = descriptor_pair_ids[descriptor_pair]
        require(bound["descriptor_pair_class_id"] == descriptor_class_id, f"descriptor class:{ordinal}")
        descriptor_pair_counts[descriptor_class_id] += 1

        triple = tuple(bound["source_triple"])
        orientation = bound["source_T_orientation_label"]
        require(len(triple) == 3 and orientation in triple, f"source orientation:{ordinal}")
        source_polynomial = t_pullback(
            atlas, source_descriptor, source_outputs[raw["source_index"]], triple, orientation
        )
        require(sparse_hash(source_polynomial) == bound["source_pullback_sha256"], f"source pullback:{ordinal}")
        require(len(source_polynomial) == bound["source_pullback_term_count"], f"source terms:{ordinal}")

        inverse = {new: old for old, new in enumerate(raw["port_permutation"])}
        mapped_triple = tuple(sorted(inverse[label] for label in triple))
        mapped_orientation = inverse[orientation]
        require(tuple(bound["target_unpermuted_triple"]) == mapped_triple, f"triple transport:{ordinal}")
        require(bound["target_T_orientation_label"] == mapped_orientation, f"orientation transport:{ordinal}")
        target_index = raw["target_index"]
        if target_index not in target_descriptor_cache:
            descriptor = atlas.model_descriptor_fast2(targets[target_index].graph)
            target_descriptor_cache[target_index] = descriptor
            target_outputs_cache[target_index] = atlas.output_sparse_polynomials(descriptor)
        target_key = (target_index, mapped_triple, mapped_orientation)
        if target_key not in target_pullback_cache:
            target_pullback_cache[target_key] = t_pullback(
                atlas,
                target_descriptor_cache[target_index],
                target_outputs_cache[target_index],
                mapped_triple,
                mapped_orientation,
            )
        target_polynomial = target_pullback_cache[target_key]
        require(not target_polynomial, f"target pullback nonzero:{ordinal}")
        require(bound["target_pullback_sha256"] == sparse_hash(target_polynomial) == target_zero_sha256, f"target hash:{ordinal}")
        relation_classes[(bound["source_pullback_sha256"], bound["target_pullback_sha256"])] += 1
        if ordinal and ordinal % 2_500 == 0:
            print(f"raw4-replay:{ordinal}/{len(raw_rows)}", file=sys.stderr, flush=True)

    require(exact_relations == {"none": 16_974}, f"relation census:{exact_relations}")
    require(len(pair_registry.representatives) == certificate["exact_ordered_labelled_graph_pair_classes"] == 122, "graph pair census")
    require(len(descriptor_pair_ids) == certificate["exact_descriptor_pair_classes"] == 678, "descriptor pair census")
    descriptor_rows = certificate["descriptor_pair_classes"]
    require(len(descriptor_rows) == len(descriptor_pair_ids), "descriptor ledger length")
    for row in descriptor_rows:
        class_id = row["descriptor_pair_class_id"]
        require(row["raw_multiplicity"] == descriptor_pair_counts[class_id], f"descriptor multiplicity:{class_id}")
        require(row["corrected_category"] == "exact_exclusion", f"descriptor category:{class_id}")
        require(row["corrected_reason"] == "full_map_Ti_strict_sign", f"descriptor reason:{class_id}")
    public_relation_counts = {
        f"{source}:{target}": count
        for (source, target), count in sorted(relation_classes.items())
    }
    require(public_relation_counts == certificate["canonical_relation_class_multiplicities"], "polynomial class multiplicities")
    require(len(relation_classes) == certificate["canonical_polynomial_relation_classes"] == 8, "polynomial class census")

    report = {
        "schema": "k2p-raw4-corrected-independent-replay-v1",
        "status": "PASS",
        "certificate_sha256": sha_file(args.certificate),
        "certificate_payload_sha256": claimed_payload,
        "raw_rows_replayed": len(raw_rows),
        "graph_pair_classes_replayed": len(pair_registry.representatives),
        "descriptor_pair_classes_replayed": len(descriptor_pair_ids),
        "sign_classes_replayed": len(sign_records),
        "target_zero_rows": len(raw_rows),
        "strict_source_negative_rows": len(raw_rows),
        "unresolved": 0,
        "false_graph_terminal_conflicts": 0,
        "corrected_restoration_parent_classes": 997,
        "runtime_seconds": time.monotonic() - started,
    }
    report["payload_sha256"] = sha(report)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (
        ReplayFailure,
        StrictJSONError,
        KeyError,
        IndexError,
        OSError,
        json.JSONDecodeError,
    ) as error:
        raise SystemExit(f"RAW4_CORRECTED_REPLAY_FAIL:{error}") from error
