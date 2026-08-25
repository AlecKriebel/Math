#!/usr/bin/env python3
"""Generate exact cyclic six-minor certificates from frozen target descriptors.

This is the deterministic certificate producer.  It rebuilds the one-active
four-port K3P maps from the frozen graph certificate, searches only exact
integer coefficient dictionaries, and writes one theorem-facing bundle.
"""

from __future__ import annotations

import collections
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
PROJECT = HERE.parents[2]
OUTPUT = HERE / "CYCLIC_SIX_MINOR_CERTIFICATES.json"
TARGET_INDICES = (107, 111, 117, 119, 177, 183, 189, 190, 191, 192)
SECTOR_NAMES = ("C", "G", "T")


def import_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cross = import_path("cyclic_certificate_crossbridge", PARENT / "explore_crossbridge_atlas.py")
atlas = cross.atlas


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    answer = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            answer.update(block)
    return answer.hexdigest()


def sparse_add(left, right, right_multiplier=1):
    answer = collections.defaultdict(int)
    for exponent, coefficient in left.items():
        answer[exponent] += coefficient
    for exponent, coefficient in right.items():
        answer[exponent] += right_multiplier * coefficient
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def sparse_mul(left, right):
    answer = collections.defaultdict(int)
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(left_exponent, right_exponent))
            answer[exponent] += left_coefficient * right_coefficient
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def factor_monomial(polynomial):
    if not polynomial:
        raise ValueError("zero polynomial")
    width = len(next(iter(polynomial)))
    common = tuple(min(exponent[axis] for exponent in polynomial) for axis in range(width))
    reduced = {
        tuple(exponent[axis] - common[axis] for axis in range(width)): coefficient
        for exponent, coefficient in polynomial.items()
    }
    return common, reduced


def polynomial_payload(polynomial):
    return [[list(exponent), str(coefficient)] for exponent, coefficient in sorted(polynomial.items())]


def polynomial_digest(polynomial):
    return digest(polynomial_payload(polynomial))


def variable(width, index):
    exponent = [0] * width
    exponent[index] = 1
    return {tuple(exponent): 1}


def one(width):
    return {(0,) * width: 1}


def minor_polynomial(outputs, coordinate_index, character_sum, rows, columns):
    row0, row1 = rows
    column0, column1 = columns
    coordinates = (
        coordinate_index[(row0, character_sum ^ row0, column0, character_sum ^ column0)],
        coordinate_index[(row1, character_sum ^ row1, column1, character_sum ^ column1)],
        coordinate_index[(row0, character_sum ^ row0, column1, character_sum ^ column1)],
        coordinate_index[(row1, character_sum ^ row1, column0, character_sum ^ column0)],
    )
    polynomial = sparse_add(
        sparse_mul(outputs[coordinates[0]], outputs[coordinates[1]]),
        sparse_mul(outputs[coordinates[2]], outputs[coordinates[3]]),
        -1,
    )
    return polynomial, coordinates


def all_unique_minors(outputs, coordinate_index):
    pairs = tuple(itertools.combinations(range(4), 2))
    by_reduced_digest = {}
    for character_sum in range(4):
        for rows in pairs:
            for columns in pairs:
                full, coordinates = minor_polynomial(
                    outputs, coordinate_index, character_sum, rows, columns
                )
                if not full:
                    continue
                common, reduced = factor_monomial(full)
                key = polynomial_digest(reduced)
                metadata = (character_sum, rows, columns)
                candidate = {
                    "character_sum": character_sum,
                    "rows": list(rows),
                    "columns": list(columns),
                    "coordinate_indices": list(coordinates),
                    "full": full,
                    "common": common,
                    "reduced": reduced,
                }
                if key not in by_reduced_digest or metadata < (
                    by_reduced_digest[key]["character_sum"],
                    tuple(by_reduced_digest[key]["rows"]),
                    tuple(by_reduced_digest[key]["columns"]),
                ):
                    by_reduced_digest[key] = candidate
    return tuple(
        sorted(
            by_reduced_digest.values(),
            key=lambda row: (
                row["character_sum"], tuple(row["rows"]), tuple(row["columns"])
            ),
        )
    )


def base_identity(width, x_index, y_index, z_index, lambda_index):
    x = variable(width, x_index)
    y = variable(width, y_index)
    z = variable(width, z_index)
    lam = variable(width, lambda_index)
    first = sparse_add(y, sparse_mul(x, z), -1)
    second = sparse_add(sparse_mul(x, y), z, -1)
    inheritance = sparse_mul(lam, sparse_add(one(width), lam, -1))
    return sparse_mul(inheritance, sparse_mul(first, second))


def exact_match(F, H, width, edge_index, sector, lambda_index):
    other = tuple(index for index in range(3) if index != sector)
    x_index = 3 * edge_index + sector
    y_index = 3 * edge_index + other[0]
    z_index = 3 * edge_index + other[1]
    x = variable(width, x_index)
    y = variable(width, y_index)
    z = variable(width, z_index)
    base = base_identity(width, x_index, y_index, z_index, lambda_index)
    base_common, base_reduced = factor_monomial(base)
    for h_coefficient in (-1, 1):
        lhs = sparse_add(
            sparse_mul(sparse_mul(y, z), F["reduced"]),
            sparse_mul(x, H["reduced"]),
            h_coefficient,
        )
        if not lhs:
            continue
        lhs_common, lhs_reduced = factor_monomial(lhs)
        for orientation in (1, -1):
            oriented = {exponent: orientation * coefficient for exponent, coefficient in lhs_reduced.items()}
            if oriented != base_reduced:
                continue
            quotient_exponent = tuple(
                lhs_common[axis] - base_common[axis] for axis in range(width)
            )
            if min(quotient_exponent) < 0:
                continue
            return {
                "F_orientation": orientation,
                "H_orientation": orientation * h_coefficient,
                "x_parameter_index": x_index,
                "y_parameter_index": y_index,
                "z_parameter_index": z_index,
                "lambda_parameter_index": lambda_index,
                "Q_positive_monomial_exponent": list(quotient_exponent),
                "lhs_polynomial_sha256": polynomial_digest(
                    {exponent: orientation * coefficient for exponent, coefficient in lhs.items()}
                ),
                "lhs_term_count": len(lhs),
                "base_polynomial_sha256": polynomial_digest(base),
            }
    return None


def search_sector(minors, descriptor, sector):
    width = 3 * descriptor.edge_class_count + descriptor.retic_count
    inheritance_offset = 3 * descriptor.edge_class_count

    # The cyclic family always admits a principal zero-block representative.
    # Try those first so the selected certificate is canonical and compact.
    character = sector + 1
    preferred = [
        row for row in minors
        if row["character_sum"] == 0
        and row["rows"] == [0, character]
        and row["columns"] == [0, character]
    ]
    f_candidates = preferred + [row for row in minors if row not in preferred]

    for F in f_candidates:
        for H in minors:
            for edge_index in range(descriptor.edge_class_count):
                for inheritance_index in range(descriptor.retic_count):
                    match = exact_match(
                        F,
                        H,
                        width,
                        edge_index,
                        sector,
                        inheritance_offset + inheritance_index,
                    )
                    if match is not None:
                        return F, H, match
    raise AssertionError(f"no cyclic identity in sector {sector}")


def public_minor(row):
    return {
        "character_sum": row["character_sum"],
        "rows": row["rows"],
        "columns": row["columns"],
        "coordinate_indices": row["coordinate_indices"],
        "full_polynomial_sha256": polynomial_digest(row["full"]),
        "full_term_count": len(row["full"]),
        "positive_monomial_exponent": list(row["common"]),
        "reduced_polynomial_sha256": polynomial_digest(row["reduced"]),
        "reduced_term_count": len(row["reduced"]),
    }


def main():
    _, _, _, targets = cross.build_universes()
    assignments = atlas.k3p_assignments(4)
    coordinate_index = {assignment: index for index, assignment in enumerate(assignments)}
    records = []
    for target_index in TARGET_INDICES:
        target = targets[target_index]
        descriptor = target["descriptor"]
        outputs = atlas.output_sparse_polynomials(descriptor)
        minors = all_unique_minors(outputs, coordinate_index)
        identities = []
        for sector in range(3):
            F, H, match = search_sector(minors, descriptor, sector)
            identities.append(
                {
                    "sector": SECTOR_NAMES[sector],
                    "F": public_minor(F),
                    "H": public_minor(H),
                    **match,
                    "exact_identity": (
                        "y*z*(F_orientation*F_reduced) + "
                        "x*(H_orientation*H_reduced) = "
                        "Q*lambda*(1-lambda)*(y-x*z)*(x*y-z)"
                    ),
                }
            )
        x_edges = {row["x_parameter_index"] // 3 for row in identities}
        if len(x_edges) != 1:
            raise AssertionError((target_index, "incoherent distinguished edge", x_edges))
        records.append(
            {
                "target_index": target_index,
                "record_id": target["record_id"],
                "old_split": target["old_split"],
                "old_order": target["old_order"],
                "reticulation_count": descriptor.retic_count,
                "edge_class_count": descriptor.edge_class_count,
                "descriptor_sha256": cross.digest(cross.descriptor_payload(descriptor)),
                "distinguished_edge_class": next(iter(x_edges)),
                "identity_records": identities,
            }
        )
        print(json.dumps({"target_index": target_index, "identities": 3}, sort_keys=True), flush=True)

    payload = {
        "schema": "k3p-cyclic-six-minor-certificates-v1",
        "status": "PASS",
        "target_indices": list(TARGET_INDICES),
        "inputs": {
            "graph_certificate": str(cross.PRIMITIVE_PATH.relative_to(PROJECT)),
            "graph_certificate_sha256": sha_file(cross.PRIMITIVE_PATH),
            "crossbridge_compiler": str((PARENT / "explore_crossbridge_atlas.py").relative_to(PROJECT)),
            "crossbridge_compiler_sha256": sha_file(PARENT / "explore_crossbridge_atlas.py"),
            "k3p_compiler": str(cross.ATLAS_PATH.relative_to(PROJECT)),
            "k3p_compiler_sha256": sha_file(cross.ATLAS_PATH),
            "producer_sha256": sha_file(Path(__file__).resolve()),
        },
        "method": {
            "arithmetic": "exact sparse integer coefficient dictionaries",
            "minor_scope": "all nonzero 2x2 minors of all four 4x4 Fourier blocks",
            "identity": "y*z*F+x*H=Q*lambda*(1-lambda)*(y-x*z)*(x*y-z), with recorded orientations",
            "Q_domain": "a strictly positive monomial in open-cube edge spectra and inheritances",
        },
        "common_contradiction": {
            "vanishing_consequence": (
                "Because Q, lambda, and 1-lambda are positive, F=H=0 forces "
                "y=x*z or z=x*y in each of C,G,T."
            ),
            "log_form": (
                "Writing U_C=-log(x_C), U_G=-log(x_G), U_T=-log(x_T)>0, "
                "each U is the absolute difference of the other two."
            ),
            "ordering_argument": (
                "If M is the largest of the three positive U values, its required "
                "equality to the absolute difference of the other two is strictly "
                "less than M, a contradiction."
            ),
        },
        "records": records,
        "record_count": len(records),
        "identity_count": sum(len(row["identity_records"]) for row in records),
        "target117_independent_audit": {
            "path": str((PARENT / "audit_simplex/RECORD39_CYCLIC_CERTIFICATE_AUDIT.json").relative_to(PROJECT)),
            "sha256": sha_file(PARENT / "audit_simplex/RECORD39_CYCLIC_CERTIFICATE_AUDIT.json"),
            "note": "Pre-existing independently generated audit; not imported by this producer.",
        },
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(OUTPUT)
    print(json.dumps({"status": "PASS", "records": len(records), "identities": payload["identity_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
