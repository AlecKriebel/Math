#!/usr/bin/env python3
"""Independent finite K3P cross-bridge atlas exploration.

This program deliberately does not import the fourteen-orbit classification.
It rebuilds K3P Fourier maps from the graph-derived switching signatures in
the corrected JC primitive certificate, which are model-independent data.

The source universe consists of two three-boundary endpoint tensors joined
by one K3P bridge.  The target universe consists of every four-boundary
one-active primitive tensor and every wrong quartet direction, normalized so
that the swallowed source bridge is 01|23.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS_PATH = PROJECT / "input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py"
PRIMITIVE_PATH = (
    PROJECT / "cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json"
)


def import_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


atlas = import_path("strong_crossbridge_k3p_atlas", ATLAS_PATH)


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def sector(mask: int, chars: tuple[int, ...]) -> int:
    answer = 0
    for index, value in enumerate(chars):
        if mask & (1 << index):
            answer ^= value
    return answer


def signature_descriptor(signatures, reticulation_count: int, k: int):
    """Compile a full three-sector descriptor from switching descendant masks."""
    signatures = tuple(tuple(int(x) for x in row) for row in signatures)
    switch_count = 1 << reticulation_count
    if any(len(row) != switch_count for row in signatures):
        raise AssertionError("switch count")
    assignments = atlas.k3p_assignments(k)
    outputs = []
    for chars in assignments:
        grouped = defaultdict(lambda: defaultdict(int))
        for switch_index in range(switch_count):
            bits = tuple(
                (switch_index >> (reticulation_count - 1 - j)) & 1
                for j in range(reticulation_count)
            )
            monomial = []
            for edge_index, row in enumerate(signatures):
                character = sector(row[switch_index], chars)
                if character:
                    monomial.append((edge_index, character, 1))
            monomial = tuple(monomial)
            for inheritance_mask, coefficient in atlas.weight_polynomial(bits):
                grouped[monomial][inheritance_mask] += coefficient
        expression = []
        for monomial, polynomial in grouped.items():
            polynomial = tuple(sorted((m, c) for m, c in polynomial.items() if c))
            if polynomial:
                expression.append((monomial, polynomial))
        outputs.append(tuple(sorted(expression)))
    return atlas.MapDescriptor(
        k,
        reticulation_count,
        len(signatures),
        tuple(outputs),
        signatures,
    )


def permute_mask(mask: int, old_to_new: dict[int, int]) -> int:
    answer = 0
    for old, new in old_to_new.items():
        if mask & (1 << old):
            answer |= 1 << new
    return answer


def permuted_signature_descriptor(record, old_order: tuple[int, ...]):
    """Place old labels in the requested new-label order."""
    old_to_new = {old: new for new, old in enumerate(old_order)}
    signatures = [
        [permute_mask(mask, old_to_new) for mask in row]
        for row in record["signatures"]
    ]
    return signature_descriptor(signatures, record["reticulation_count"], 4)


def shift_monomial(monomial, edge_shift: int):
    return tuple((edge + edge_shift, char, exponent) for edge, char, exponent in monomial)


def multiply_lambda_polynomials(left, right, right_shift: int):
    result = defaultdict(int)
    for mask_left, coefficient_left in left:
        for mask_right, coefficient_right in right:
            result[mask_left | (mask_right << right_shift)] += (
                coefficient_left * coefficient_right
            )
    return tuple(sorted((mask, value) for mask, value in result.items() if value))


def joined_descriptor(left, right):
    """Four-port map q_abcd=P_ab,h z_h Q_cd,h, h=a xor b."""
    if left.k != 3 or right.k != 3:
        raise AssertionError("endpoint arity")
    assignments3 = atlas.k3p_assignments(3)
    index3 = {chars: index for index, chars in enumerate(assignments3)}
    outputs = []
    bridge_edge = left.edge_class_count + right.edge_class_count
    for a, b, c, d in atlas.k3p_assignments(4):
        h = a ^ b
        if h != (c ^ d):
            raise AssertionError("conservation")
        expression = defaultdict(lambda: defaultdict(int))
        for left_monomial, left_polynomial in left.outputs[index3[(a, b, h)]]:
            for right_monomial, right_polynomial in right.outputs[index3[(c, d, h)]]:
                monomial = list(left_monomial)
                monomial.extend(shift_monomial(right_monomial, left.edge_class_count))
                if h:
                    monomial.append((bridge_edge, h, 1))
                monomial = tuple(sorted(monomial))
                polynomial = multiply_lambda_polynomials(
                    left_polynomial, right_polynomial, left.retic_count
                )
                for mask, coefficient in polynomial:
                    expression[monomial][mask] += coefficient
        normalized = []
        for monomial, polynomial in expression.items():
            polynomial = tuple(sorted((m, c0) for m, c0 in polynomial.items() if c0))
            if polynomial:
                normalized.append((monomial, polynomial))
        outputs.append(tuple(sorted(normalized)))
    return atlas.MapDescriptor(
        4,
        left.retic_count + right.retic_count,
        bridge_edge + 1,
        tuple(outputs),
        (),
    )


def descriptor_payload(descriptor):
    return {
        "k": descriptor.k,
        "retic_count": descriptor.retic_count,
        "edge_class_count": descriptor.edge_class_count,
        "outputs": descriptor.outputs,
    }


def rank(descriptor, salt=0):
    if 3 * descriptor.edge_class_count + descriptor.retic_count == 0:
        return 0
    return atlas.rank_certificate(descriptor, salt)["rank"]


def build_universes():
    primitive = json.loads(PRIMITIVE_PATH.read_text())
    endpoint_records = primitive["three_port_endpoint_dichotomy"]["records"]
    target_records = primitive["one_active_wrong_split"]["records"]

    endpoint_descriptors = [
        signature_descriptor(row["signatures"], row["reticulation_count"], 3)
        for row in endpoint_records
    ]
    target_directions = []
    for row in target_records:
        for split in row["splits"]:
            if split["displayed_by_all"]:
                continue
            first = tuple(split["split"])
            second = tuple(sorted(set(range(4)) - set(first)))
            old_order = first + second
            descriptor = permuted_signature_descriptor(row, old_order)
            target_directions.append(
                {
                    "record_id": row["id"],
                    "reticulation_count": row["reticulation_count"],
                    "old_split": list(first),
                    "old_order": list(old_order),
                    "descriptor": descriptor,
                }
            )
    return primitive, endpoint_records, endpoint_descriptors, target_directions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-ranks", action="store_true")
    args = parser.parse_args()
    primitive, endpoint_records, endpoints, targets = build_universes()

    endpoint_hashes = [digest(descriptor_payload(row)) for row in endpoints]
    target_hashes = [digest(descriptor_payload(row["descriptor"])) for row in targets]
    endpoint_rank_rows = []
    for index, descriptor in enumerate(endpoints):
        endpoint_rank_rows.append(
            {
                "record_id": endpoint_records[index]["id"],
                "reticulation_count": descriptor.retic_count,
                "descriptor_sha256": endpoint_hashes[index],
                "rank": rank(descriptor, index % 3),
            }
        )
    target_rank_rows = []
    for index, row in enumerate(targets):
        target_rank_rows.append(
            {
                "record_id": row["record_id"],
                "old_split": row["old_split"],
                "reticulation_count": row["reticulation_count"],
                "descriptor_sha256": target_hashes[index],
                "rank": rank(row["descriptor"], index % 3),
            }
        )

    joined_rows = []
    joined_rank_counter = Counter()
    if args.full_ranks:
        for left in range(len(endpoints)):
            for right in range(left, len(endpoints)):
                descriptor = joined_descriptor(endpoints[left], endpoints[right])
                certificate = atlas.rank_certificate(descriptor, (left + right) % 3)
                joined_rank_counter[certificate["rank"]] += 1
                joined_rows.append(
                    {
                        "left": left,
                        "right": right,
                        "reticulation_count": descriptor.retic_count,
                        "descriptor_sha256": digest(descriptor_payload(descriptor)),
                        "rank": certificate["rank"],
                    }
                )

    report = {
        "schema": "k3p-strong-crossbridge-exploration-v1",
        "inputs": {
            "primitive_certificate": str(PRIMITIVE_PATH.relative_to(PROJECT)),
            "primitive_certificate_sha256": sha_file(PRIMITIVE_PATH),
            "k3p_compiler": str(ATLAS_PATH.relative_to(PROJECT)),
            "k3p_compiler_sha256": sha_file(ATLAS_PATH),
        },
        "independence": {
            "fourteen_orbit_artifacts_imported": False,
            "model_specific_transfer": "all C/G/T sectors recompiled independently",
        },
        "counts": {
            "endpoint_records": len(endpoints),
            "endpoint_descriptor_classes": len(set(endpoint_hashes)),
            "one_active_target_records": 72,
            "wrong_target_directions": len(targets),
            "wrong_target_descriptor_classes": len(set(target_hashes)),
            "unordered_endpoint_pairs": len(endpoints) * (len(endpoints) + 1) // 2,
        },
        "endpoint_rank_distribution": dict(
            sorted(Counter(row["rank"] for row in endpoint_rank_rows).items())
        ),
        "target_rank_distribution": dict(
            sorted(Counter(row["rank"] for row in target_rank_rows).items())
        ),
        "joined_rank_distribution": dict(sorted(joined_rank_counter.items())),
        "endpoint_ranks": endpoint_rank_rows,
        "target_ranks": target_rank_rows,
        "joined_ranks": joined_rows,
    }
    output = HERE / "CROSSBRIDGE_EXPLORATION.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["counts"], sort_keys=True))
    print("endpoint ranks", report["endpoint_rank_distribution"])
    print("target ranks", report["target_rank_distribution"])
    print("joined ranks", report["joined_rank_distribution"])


if __name__ == "__main__":
    main()
