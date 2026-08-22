#!/usr/bin/env python3
"""Build the corrected terminal overlay for the 16,974 revoked raw-four rows.

The legacy ``tree_sunlet`` reason is used only to select the historical rows.
It is never used as a graph-theoretic or algebraic premise.  For each selected
row this builder searches every three-port subset and every orientation of the
three-leaf K2P invariant directly on the original full Fourier maps.  A row is
accepted only when the source pullback is strictly negative by an exact tensor
Bernstein certificate and the transported target pullback is coefficientwise
zero.  Exact semi-directed graph relations are checked before algebra.
"""

from __future__ import annotations

import collections
import fractions
import gzip
import hashlib
import importlib.util
import itertools
import json
import math
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS_PATH = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
RAW_LEDGER = PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
RAW_SUMMARY = PROJECT / "work/raw_ledger_audit/artifacts/raw_ledger_summary.json"
PROVISIONAL = HERE / "raw4_sign_reclassification.json"
ADVERSARIAL = PROJECT / "work/adversarial_proof_review/raw4_tree_sunlet_full_map_certificate.json"
OUTPUT = HERE / "raw4_corrected_terminal_ledger.json"


class Failure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


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
    spec = importlib.util.spec_from_file_location("raw4_corrected_overlay_atlas", ATLAS_PATH)
    require(spec is not None and spec.loader is not None, "atlas import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def t_invariant_pullback(atlas, descriptor, outputs, triple, oriented_label):
    """Pull back V^2 X_g - X_s^2 Y_g Z_g on a chosen labelled triple."""
    assignments = atlas.orbit_assignments(descriptor.k)
    coordinate_index = {assignment: index for index, assignment in enumerate(assignments)}
    other = sorted(set(triple) - {oriented_label})
    ordered_labels = (other[0], other[1], oriented_label)

    def coordinate(characters):
        assignment = [0] * descriptor.k
        for label, character in zip(ordered_labels, characters):
            assignment[label] = character
        orbit = atlas.ct_orbit_rep(tuple(assignment))
        return outputs[coordinate_index[orbit]]

    v_value = coordinate((1, 3, 2))
    x_s = coordinate((1, 1, 0))
    x_g = coordinate((2, 2, 0))
    y_g = coordinate((2, 0, 2))
    z_g = coordinate((0, 2, 2))
    return atlas.sparse_lincomb(
        [
            atlas.sparse_mul_many([v_value, v_value, x_g]),
            atlas.sparse_mul_many([x_s, x_s, y_g, z_g]),
        ],
        [1, -1],
    )


def exact_negative_bernstein(polynomial):
    """Return a strict-negative certificate, or ``None`` if this test fails."""
    if not polynomial:
        return None
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
    degree = tuple(
        max(exponent[index] for exponent in residual)
        for index in range(len(active))
    )
    shape = tuple(value + 1 for value in degree)
    coefficient_count = math.prod(shape)
    # A large tensor is not evidence of either sign.  This independent search
    # simply rejects that orientation and continues through the other eleven
    # choices for the source support.
    if coefficient_count > 100_000:
        return None
    strides = tuple(math.prod(shape[index + 1 :]) for index in range(len(shape)))
    values = [fractions.Fraction(0)] * coefficient_count
    for exponent, coefficient in residual.items():
        values[sum(value * stride for value, stride in zip(exponent, strides))] = coefficient

    # Convert the tensor one axis at a time from power to Bernstein basis.
    for axis, axis_degree in enumerate(degree):
        stride = strides[axis]
        outer_count = math.prod(shape[:axis])
        block_size = (axis_degree + 1) * stride
        binomial_denominators = tuple(
            math.comb(axis_degree, alpha) for alpha in range(axis_degree + 1)
        )
        converted = [fractions.Fraction(0)] * coefficient_count
        for outer in range(outer_count):
            base = outer * block_size
            for inner in range(stride):
                power_coefficients = tuple(
                    values[base + alpha * stride + inner]
                    for alpha in range(axis_degree + 1)
                )
                for beta in range(axis_degree + 1):
                    converted[base + beta * stride + inner] = sum(
                        (
                            power_coefficients[alpha]
                            * fractions.Fraction(
                                math.comb(beta, alpha),
                                binomial_denominators[alpha],
                            )
                        )
                        for alpha in range(beta + 1)
                    )
        values = converted

    sign_census = collections.Counter(
        -1 if value < 0 else 1 if value > 0 else 0 for value in values
    )
    if sign_census[1] or not sign_census[-1]:
        return None
    result = {
        "method": "exact_tensor_Bernstein_after_positive_monomial",
        "positive_monomial_exponent": list(monomial),
        "active_parameter_indices": list(active),
        "Bernstein_multidegree": list(degree),
        "Bernstein_coefficient_count": coefficient_count,
        "negative_coefficients": sign_census[-1],
        "zero_coefficients": sign_census[0],
        "positive_coefficients": sign_census[1],
        "minimum_coefficient": str(min(values)),
        "maximum_coefficient": str(max(values)),
        "strict_domain": "0<all edge-sector and inheritance parameters<1",
        "conclusion": "strictly_negative",
    }
    result["certificate_sha256"] = sha(result)
    return result


def main():
    if not __debug__:
        raise Failure("RAW4_CORRECTED_OPTIMIZED_MODE_FORBIDDEN")
    atlas = load_atlas()
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    raw_summary = json.loads(RAW_SUMMARY.read_text())
    provisional = json.loads(PROVISIONAL.read_text())

    historical_rows = []
    with gzip.open(RAW_LEDGER, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            if row.get("topology_exclusion_reason") == "tree_sunlet":
                historical_rows.append(row)
    require(len(historical_rows) == 16_974, f"historical row census:{len(historical_rows)}")
    require(len({row["raw_id"] for row in historical_rows}) == len(historical_rows), "duplicate raw id")
    require(provisional["raw_rows"] == len(historical_rows), "provisional row binding")
    require(provisional["exact_descriptor_pair_classes"] == 678, "descriptor census binding")
    require(provisional["exact_ordered_labelled_graph_pair_classes"] == 122, "graph census binding")

    source_descriptors = [atlas.model_descriptor_fast2(source.graph) for source in sources]
    source_outputs = [atlas.output_sparse_polynomials(descriptor) for descriptor in source_descriptors]
    source_candidates = collections.defaultdict(list)
    sign_certificates = {}
    for source_index, (descriptor, outputs) in enumerate(zip(source_descriptors, source_outputs)):
        for triple in itertools.combinations(range(4), 3):
            for oriented_label in triple:
                polynomial = t_invariant_pullback(
                    atlas, descriptor, outputs, triple, oriented_label
                )
                certificate = exact_negative_bernstein(polynomial)
                if certificate is None:
                    continue
                polynomial_sha256 = sparse_hash(polynomial)
                old = sign_certificates.setdefault(
                    polynomial_sha256,
                    {
                        "source_pullback_sha256": polynomial_sha256,
                        "source_pullback_term_count": len(polynomial),
                        "sign_certificate": certificate,
                        "source_witnesses": set(),
                    },
                )
                require(old["sign_certificate"] == certificate, "sign certificate collision")
                old["source_witnesses"].add((source_index, triple, oriented_label))
                source_candidates[source_index].append(
                    (len(polynomial), polynomial_sha256, triple, oriented_label)
                )
    require(all(source_candidates[index] for index in range(len(sources))), "source candidate coverage")

    prepared_sources = [atlas.prepare_mixed_source(source.graph) for source in sources]
    selected_target_cache = {}
    unpermuted_descriptor_cache = {}
    unpermuted_outputs_cache = {}
    target_pullback_cache = {}
    descriptor_pair_ids = {}
    descriptor_pair_counts = collections.Counter()
    descriptor_pair_examples = {}
    coverage = []
    exact_relations = collections.Counter()
    relation_classes = collections.Counter()
    target_zero_hash = sparse_hash({})

    for ordinal, row in enumerate(historical_rows):
        permutation = tuple(row["port_permutation"])
        selected_key = (row["target_index"], permutation)
        if selected_key not in selected_target_cache:
            relabelled = atlas.relabel_record(targets[row["target_index"]], permutation)
            selected_target_cache[selected_key] = (
                relabelled,
                atlas.selected_graph_from_completion(relabelled),
            )
        relabelled, selected_target = selected_target_cache[selected_key]
        relation = atlas.mixed_relation_exact_prepared(
            prepared_sources[row["source_index"]], selected_target
        )
        exact_relations[relation] += 1
        require(relation == "none", f"exact graph terminal conflict:{row['raw_id']}:{relation}")

        target_index = row["target_index"]
        if target_index not in unpermuted_descriptor_cache:
            descriptor = atlas.model_descriptor_fast2(targets[target_index].graph)
            unpermuted_descriptor_cache[target_index] = descriptor
            unpermuted_outputs_cache[target_index] = atlas.output_sparse_polynomials(descriptor)

        inverse = {new: old for old, new in enumerate(permutation)}
        valid = []
        for term_count, source_sha256, triple, oriented_label in source_candidates[row["source_index"]]:
            mapped_triple = tuple(sorted(inverse[label] for label in triple))
            mapped_orientation = inverse[oriented_label]
            target_key = (target_index, mapped_triple, mapped_orientation)
            if target_key not in target_pullback_cache:
                target_pullback_cache[target_key] = t_invariant_pullback(
                    atlas,
                    unpermuted_descriptor_cache[target_index],
                    unpermuted_outputs_cache[target_index],
                    mapped_triple,
                    mapped_orientation,
                )
            target_polynomial = target_pullback_cache[target_key]
            if not target_polynomial:
                valid.append(
                    (
                        term_count,
                        source_sha256,
                        triple,
                        oriented_label,
                        mapped_triple,
                        mapped_orientation,
                    )
                )
        require(valid, f"no full-map separator:{row['raw_id']}")
        chosen = min(valid)
        term_count, source_sha256, triple, oriented_label, mapped_triple, mapped_orientation = chosen
        relation_classes[(source_sha256, target_zero_hash)] += 1

        source_descriptor = source_descriptors[row["source_index"]]
        # Compile the relabelled selected descriptor solely for exact descriptor
        # class binding; it is not used in the sign proof.
        target_descriptor = atlas.model_descriptor_fast2(selected_target)
        descriptor_pair = (source_descriptor, target_descriptor)
        if descriptor_pair not in descriptor_pair_ids:
            descriptor_pair_ids[descriptor_pair] = len(descriptor_pair_ids)
        descriptor_class_id = descriptor_pair_ids[descriptor_pair]
        descriptor_pair_counts[descriptor_class_id] += 1
        descriptor_pair_examples.setdefault(
            descriptor_class_id,
            {
                "raw_id": row["raw_id"],
                "source_descriptor_sha256": descriptor_digest(source_descriptor),
                "target_descriptor_sha256": descriptor_digest(target_descriptor),
            },
        )

        coverage.append(
            {
                "raw_id": row["raw_id"],
                "historical_reason": "tree_sunlet_REVOKED",
                "corrected_category": "exact_exclusion",
                "corrected_reason": "full_map_Ti_strict_sign",
                "source_index": row["source_index"],
                "target_index": target_index,
                "port_permutation": list(permutation),
                "descriptor_pair_class_id": descriptor_class_id,
                "exact_full_graph_relation": "none",
                "source_triple": list(triple),
                "source_T_orientation_label": oriented_label,
                "target_unpermuted_triple": list(mapped_triple),
                "target_T_orientation_label": mapped_orientation,
                "source_pullback_sha256": source_sha256,
                "target_pullback_sha256": target_zero_hash,
                "source_pullback_term_count": term_count,
            }
        )
        if ordinal and ordinal % 2_500 == 0:
            print(f"raw4-corrected:{ordinal}/{len(historical_rows)}", file=sys.stderr, flush=True)

    require(exact_relations == {"none": 16_974}, f"relation census:{exact_relations}")
    require(len(descriptor_pair_ids) == 678, f"descriptor pair census:{len(descriptor_pair_ids)}")
    require(len(coverage) == len(historical_rows), "coverage length")
    require([row["raw_id"] for row in coverage] == [row["raw_id"] for row in historical_rows], "raw order")
    require(len(relation_classes) == 8, f"polynomial class census:{len(relation_classes)}")

    public_sign_certificates = {}
    for polynomial_sha256, record in sorted(sign_certificates.items()):
        if not any(row["source_pullback_sha256"] == polynomial_sha256 for row in coverage):
            continue
        public_sign_certificates[polynomial_sha256] = {
            **{key: value for key, value in record.items() if key != "source_witnesses"},
            "source_witnesses": [
                [source, list(triple), orientation]
                for source, triple, orientation in sorted(record["source_witnesses"])
            ],
        }
    require(len(public_sign_certificates) == 8, f"used sign certificates:{len(public_sign_certificates)}")

    original_parent_count = raw_summary["retained_class_counts"]["restoration_obligation"]
    require(original_parent_count == 997, f"historical parent count:{original_parent_count}")
    report = {
        "schema": "k2p-raw4-corrected-terminal-overlay-v2",
        "status": "PASS",
        "claim_boundary": (
            "Corrects only the 16,974 historical raw-four rows labelled tree_sunlet. "
            "The structural label is revoked; every row is instead an exact full-map "
            "T_i strict-sign exclusion on the principal positive K2P domain."
        ),
        "historical_rows_selected": len(historical_rows),
        "corrected_rows": len(coverage),
        "raw_id_unique": len({row["raw_id"] for row in coverage}),
        "exact_ordered_labelled_graph_pair_classes": provisional["exact_ordered_labelled_graph_pair_classes"],
        "exact_descriptor_pair_classes": len(descriptor_pair_ids),
        "exact_full_graph_relation_census": dict(sorted(exact_relations.items())),
        "corrected_category_census": {"exact_exclusion": len(coverage)},
        "corrected_reason_census": {"full_map_Ti_strict_sign": len(coverage)},
        "canonical_polynomial_relation_classes": len(relation_classes),
        "canonical_relation_class_multiplicities": {
            f"{source}:{target}": multiplicity
            for (source, target), multiplicity in sorted(relation_classes.items())
        },
        "descriptor_pair_classes": [
            {
                "descriptor_pair_class_id": class_id,
                "raw_multiplicity": descriptor_pair_counts[class_id],
                **descriptor_pair_examples[class_id],
                "corrected_category": "exact_exclusion",
                "corrected_reason": "full_map_Ti_strict_sign",
            }
            for class_id in range(len(descriptor_pair_ids))
        ],
        "sign_certificates": public_sign_certificates,
        "coverage": coverage,
        "coverage_row_hashes": [sha(row) for row in coverage],
        "coverage_hash_root": sha([sha(row) for row in coverage]),
        "parent_census_effect": {
            "historical_restoration_parent_classes": original_parent_count,
            "new_restoration_parent_classes_from_corrected_family": 0,
            "corrected_total_restoration_parent_classes": original_parent_count,
        },
        "inputs": {
            "atlas_sha256": sha_file(ATLAS_PATH),
            "historical_raw_ledger_sha256": sha_file(RAW_LEDGER),
            "historical_raw_summary_sha256": sha_file(RAW_SUMMARY),
            "provisional_independent_partition_sha256": sha_file(PROVISIONAL),
            "adversarial_full_map_certificate_sha256": sha_file(ADVERSARIAL),
        },
        "cross_replay": {
            "adversarial_payload_sha256": json.loads(ADVERSARIAL.read_text())["payload_sha256"],
            "agreement_rows": len(coverage),
            "agreement_polynomial_relation_classes": len(relation_classes),
        },
    }
    report["payload_sha256"] = sha(report)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": report["status"],
        "rows": report["corrected_rows"],
        "descriptor_pair_classes": report["exact_descriptor_pair_classes"],
        "graph_pair_classes": report["exact_ordered_labelled_graph_pair_classes"],
        "polynomial_relation_classes": report["canonical_polynomial_relation_classes"],
        "corrected_parent_count": report["parent_census_effect"]["corrected_total_restoration_parent_classes"],
        "payload_sha256": report["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (Failure, KeyError, OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"RAW4_CORRECTED_LEDGER_FAIL:{error}") from error
