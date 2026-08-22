#!/usr/bin/env python3
"""Full-map repair of all 16,974 revoked raw-four tree/sunlet rows.

The rooted restriction names are not trusted.  For each row this verifier
substitutes all relevant three-leaf Fourier coordinates directly into the
original full K2P polynomial maps.  It requires the target pullback to vanish
coefficientwise and certifies a strictly signed source pullback by exact
tensor-product Bernstein coefficients on the open unit cube.
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
LEDGER = PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
OUTPUT = HERE / "raw4_tree_sunlet_full_map_certificate.json"


class TruthFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise TruthFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sparse_payload(polynomial):
    return [[list(exponent), str(coefficient)] for exponent, coefficient in sorted(polynomial.items())]


def sparse_hash(polynomial):
    return sha(sparse_payload(polynomial))


def load_atlas():
    spec = importlib.util.spec_from_file_location("raw4_tree_sunlet_truth_atlas", ATLAS_PATH)
    require(spec is not None and spec.loader is not None, "atlas import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def t_pullback(atlas, descriptor, outputs, triple, reticulation_label):
    assignments = atlas.orbit_assignments(descriptor.k)
    index = {assignment: number for number, assignment in enumerate(assignments)}
    other = sorted(set(triple) - {reticulation_label})
    order = (other[0], other[1], reticulation_label)

    def coordinate(values):
        row = [0] * descriptor.k
        for label, value in zip(order, values):
            row[label] = value
        return outputs[index[atlas.ct_orbit_rep(tuple(row))]]

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


def bernstein_sign_certificate(polynomial):
    require(polynomial, "empty signed pullback")
    parameter_count = len(next(iter(polynomial)))
    monomial = tuple(min(exponent[i] for exponent in polynomial) for i in range(parameter_count))
    active = [
        i
        for i in range(parameter_count)
        if len({exponent[i] - monomial[i] for exponent in polynomial}) > 1
    ]
    residual = {
        tuple(exponent[i] - monomial[i] for i in active): fractions.Fraction(coefficient)
        for exponent, coefficient in polynomial.items()
    }
    degree = tuple(max(exponent[i] for exponent in residual) for i in range(len(active)))
    shape = tuple(value + 1 for value in degree)
    coefficient_count = math.prod(shape)
    require(coefficient_count <= 2_000_000, f"Bernstein tensor too large:{coefficient_count}")
    strides = tuple(math.prod(shape[i + 1 :]) for i in range(len(shape)))
    values = [fractions.Fraction(0)] * coefficient_count
    for exponent, coefficient in residual.items():
        values[sum(value * stride for value, stride in zip(exponent, strides))] = coefficient
    for axis, axis_degree in enumerate(degree):
        stride = strides[axis]
        outer = math.prod(shape[:axis])
        block = (axis_degree + 1) * stride
        denominators = [math.comb(axis_degree, value) for value in range(axis_degree + 1)]
        transformed = [fractions.Fraction(0)] * coefficient_count
        for outer_index in range(outer):
            base = outer_index * block
            for inner_index in range(stride):
                source = [
                    values[base + value * stride + inner_index]
                    for value in range(axis_degree + 1)
                ]
                for beta in range(axis_degree + 1):
                    total = fractions.Fraction(0)
                    for alpha in range(beta + 1):
                        if source[alpha]:
                            total += source[alpha] * fractions.Fraction(
                                math.comb(beta, alpha), denominators[alpha]
                            )
                    transformed[base + beta * stride + inner_index] = total
        values = transformed
    signs = collections.Counter(-1 if value < 0 else 1 if value > 0 else 0 for value in values)
    require(signs[1] == 0 and signs[-1] > 0, f"pullback is not Bernstein-negative:{signs}")
    # Every tensor Bernstein basis function is strictly positive on (0,1)^m.
    # Hence one negative coefficient and no positive coefficient gives strict
    # negativity; the stripped monomial is also strictly positive there.
    certificate = {
        "method": "exact_tensor_Bernstein_after_positive_monomial",
        "parameter_count": parameter_count,
        "positive_monomial_exponent": list(monomial),
        "active_parameter_indices": active,
        "Bernstein_multidegree": list(degree),
        "Bernstein_coefficient_count": coefficient_count,
        "negative_coefficients": signs[-1],
        "zero_coefficients": signs[0],
        "positive_coefficients": signs[1],
        "minimum_coefficient": str(min(values)),
        "maximum_coefficient": str(max(values)),
        "domain": (
            "the full open unit cube in edge-sector and inheritance variables; "
            "therefore also its physical D_plus subset"
        ),
        "conclusion": "strictly_negative",
    }
    certificate["certificate_sha256"] = sha(certificate)
    return certificate


def main():
    atlas = load_atlas()
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    rows = []
    with gzip.open(LEDGER, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            if row.get("topology_exclusion_reason") == "tree_sunlet":
                rows.append(row)
    require(len(rows) == 16974, f"raw row census:{len(rows)}")

    # Reconstruct the old witness triple only to bind the row that was claimed.
    # Its structural type labels are not used as proof.
    metadata = []
    target_needs = collections.defaultdict(set)
    exact_relations = collections.Counter()
    prepared_sources = [atlas.prepare_mixed_source(source.graph) for source in sources]
    for row in rows:
        permutation = tuple(row["port_permutation"])
        relabelled = atlas.relabel_record(targets[row["target_index"]], permutation)
        selected_target = atlas.selected_graph_from_completion(relabelled)
        source_graph = sources[row["source_index"]].graph
        witness = None
        for triple in itertools.combinations(range(4), 3):
            source_type = atlas.triple_type(source_graph, triple)
            target_type = atlas.triple_type(selected_target, triple)
            if {source_type, target_type} == {"tree", "sunlet"}:
                witness = (triple, source_type, target_type)
                break
        require(witness is not None, f"missing legacy witness:{row['raw_id']}")
        triple, source_type, target_type = witness
        require((source_type, target_type) == ("sunlet", "tree"), f"legacy direction:{row['raw_id']}")
        relation = atlas.mixed_relation_exact_prepared(
            prepared_sources[row["source_index"]], selected_target
        )
        exact_relations[relation] += 1
        require(relation == "none", f"topology claim contradicts exact relation:{row['raw_id']}:{relation}")
        inverse = {new: old for old, new in enumerate(permutation)}
        mapped_triple = tuple(sorted(inverse[label] for label in triple))
        target_needs[row["target_index"]].add(mapped_triple)
        metadata.append((row, triple, mapped_triple, inverse))

    source_descriptors = [atlas.model_descriptor_fast2(source.graph) for source in sources]
    source_outputs = [atlas.output_sparse_polynomials(descriptor) for descriptor in source_descriptors]
    source_polynomials = {}
    for source_index, descriptor in enumerate(source_descriptors):
        for triple in itertools.combinations(range(4), 3):
            for reticulation_label in triple:
                source_polynomials[(source_index, triple, reticulation_label)] = t_pullback(
                    atlas,
                    descriptor,
                    source_outputs[source_index],
                    triple,
                    reticulation_label,
                )

    # Compile each unpermuted target graph once.  Relabelling only transports
    # the triple and chosen reticulation label through the inverse permutation.
    target_polynomials = {}
    for target_index, triples in sorted(target_needs.items()):
        descriptor = atlas.model_descriptor_fast2(targets[target_index].graph)
        outputs = atlas.output_sparse_polynomials(descriptor)
        for triple in triples:
            for reticulation_label in triple:
                target_polynomials[(target_index, triple, reticulation_label)] = t_pullback(
                    atlas, descriptor, outputs, triple, reticulation_label
                )

    sign_certificates = {}
    chosen_by_source_triple = {}
    row_hashes = []
    relation_classes = collections.Counter()
    for row, triple, mapped_triple, inverse in metadata:
        source_key = (row["source_index"], triple)
        if source_key not in chosen_by_source_triple:
            candidates = []
            for reticulation_label in triple:
                polynomial = source_polynomials[
                    (row["source_index"], triple, reticulation_label)
                ]
                candidates.append((len(polynomial), reticulation_label, polynomial))
            for _, reticulation_label, polynomial in sorted(candidates):
                try:
                    sign = bernstein_sign_certificate(polynomial)
                except TruthFailure:
                    continue
                polynomial_sha256 = sparse_hash(polynomial)
                previous = sign_certificates.setdefault(
                    polynomial_sha256,
                    {
                        "pullback_sha256": polynomial_sha256,
                        "pullback_term_count": len(polynomial),
                        "sign": sign,
                        "source_presentations": [],
                    },
                )
                require(previous["sign"] == sign, "sign certificate collision")
                chosen_by_source_triple[source_key] = reticulation_label
                break
            require(source_key in chosen_by_source_triple, f"no strict orientation:{source_key}")
        chosen = chosen_by_source_triple[source_key]
        source_polynomial = source_polynomials[(row["source_index"], triple, chosen)]
        mapped_reticulation = inverse[chosen]
        target_polynomial = target_polynomials[
            (row["target_index"], mapped_triple, mapped_reticulation)
        ]
        require(not target_polynomial, f"target T pullback nonzero:{row['raw_id']}")
        source_sha256 = sparse_hash(source_polynomial)
        sign_certificates[source_sha256]["source_presentations"].append(
            [row["source_index"], list(triple), chosen]
        )
        truth_row = {
            "raw_id": row["raw_id"],
            "source_index": row["source_index"],
            "target_index": row["target_index"],
            "permutation_index": row["permutation_index"],
            "legacy_witness_triple": list(triple),
            "chosen_T_orientation_label": chosen,
            "source_pullback_sha256": source_sha256,
            "target_pullback_sha256": sparse_hash(target_polynomial),
            "exact_full_graph_relation": "none",
            "result": "strict_source_negative_target_zero",
        }
        row_hashes.append(sha(truth_row))
        relation_classes[(source_sha256, sparse_hash(target_polynomial))] += 1

    for certificate in sign_certificates.values():
        certificate["source_presentations"] = sorted(
            {tuple([row[0], tuple(row[1]), row[2]]) for row in certificate["source_presentations"]}
        )
        certificate["source_presentations"] = [
            [source, list(triple), orientation]
            for source, triple, orientation in certificate["source_presentations"]
        ]

    require(exact_relations == {"none": 16974}, f"exact relation census:{exact_relations}")
    require(len(row_hashes) == 16974, "truth row coverage")
    require(len(relation_classes) == 8, f"polynomial relation classes:{len(relation_classes)}")
    report = {
        "schema": "k2p-raw4-tree-sunlet-full-map-truth-v1",
        "status": "PASS",
        "claim_boundary": (
            "The legacy rooted tree/sunlet structural names are revoked.  The "
            "replacement claim is the exact full-map strict-sign separator recorded here."
        ),
        "inputs": {
            "atlas_sha256": sha_file(ATLAS_PATH),
            "raw_ledger_sha256": sha_file(LEDGER),
        },
        "claimed_rows": len(rows),
        "exact_full_graph_relation_census": dict(exact_relations),
        "false_iso_or_triangle_conflicts": 0,
        "full_map_target_zero_rows": len(row_hashes),
        "full_map_strict_source_sign_rows": len(row_hashes),
        "unresolved": 0,
        "incoherent": 0,
        "canonical_polynomial_relation_classes": len(relation_classes),
        "canonical_relation_class_multiplicities": {
            f"{source}:{target}": count
            for (source, target), count in sorted(relation_classes.items())
        },
        "chosen_orientation_by_source_triple": {
            f"s{source}:{''.join(map(str, triple))}": orientation
            for (source, triple), orientation in sorted(chosen_by_source_triple.items())
            if any(row["source_index"] == source and item_triple == triple for row, item_triple, _, _ in metadata)
        },
        "sign_certificates": dict(sorted(sign_certificates.items())),
        "ordered_truth_row_hashes": row_hashes,
        "ordered_truth_row_hash_root": sha(row_hashes),
    }
    report["payload_sha256"] = sha(report)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": report["status"],
        "rows": report["claimed_rows"],
        "classes": report["canonical_polynomial_relation_classes"],
        "false_conflicts": report["false_iso_or_triangle_conflicts"],
        "payload_sha256": report["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (TruthFailure, KeyError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"RAW4_TREE_SUNLET_TRUTH_FAIL:{exc}") from exc
