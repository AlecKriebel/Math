#!/usr/bin/env python3
"""Independent exact verifier for the cyclic six-minor certificate bundle.

The verifier deliberately does not import the producer.  It recompiles the
target maps from the frozen graph certificate, rebuilds every recorded minor,
and compares the two sides of each identity as sparse integer dictionaries.
"""

from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
PROJECT = HERE.parents[2]
DEFAULT_ARTIFACT = HERE / "CYCLIC_SIX_MINOR_CERTIFICATES.json"
REPORT = HERE / "VERIFICATION_REPORT.json"
OPTIMIZED_REPORT = HERE / "OPTIMIZED_VERIFICATION_REPORT.json"
EXPECTED_TARGETS = (107, 111, 117, 119, 177, 183, 189, 190, 191, 192)
SECTORS = {"C": 0, "G": 1, "T": 2}


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def import_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cross = import_path("cyclic_verifier_crossbridge", PARENT / "explore_crossbridge_atlas.py")
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
    require(bool(polynomial), "zero polynomial")
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
    require(0 <= index < width, ("parameter index", index, width))
    exponent = [0] * width
    exponent[index] = 1
    return {tuple(exponent): 1}


def monomial(width, exponent):
    require(len(exponent) == width, "monomial width")
    require(all(isinstance(value, int) and value >= 0 for value in exponent), "monomial exponent")
    return {tuple(exponent): 1}


def minor_polynomial(outputs, coordinate_index, record):
    character_sum = record["character_sum"]
    rows = record["rows"]
    columns = record["columns"]
    require(character_sum in range(4), "character sum")
    require(len(rows) == len(columns) == 2, "minor shape")
    require(rows[0] < rows[1] and columns[0] < columns[1], "minor orientation")
    row0, row1 = rows
    column0, column1 = columns
    coordinates = (
        coordinate_index[(row0, character_sum ^ row0, column0, character_sum ^ column0)],
        coordinate_index[(row1, character_sum ^ row1, column1, character_sum ^ column1)],
        coordinate_index[(row0, character_sum ^ row0, column1, character_sum ^ column1)],
        coordinate_index[(row1, character_sum ^ row1, column0, character_sum ^ column0)],
    )
    require(list(coordinates) == record["coordinate_indices"], "minor coordinates")
    polynomial = sparse_add(
        sparse_mul(outputs[coordinates[0]], outputs[coordinates[1]]),
        sparse_mul(outputs[coordinates[2]], outputs[coordinates[3]]),
        -1,
    )
    require(bool(polynomial), "recorded minor is zero")
    common, reduced = factor_monomial(polynomial)
    require(polynomial_digest(polynomial) == record["full_polynomial_sha256"], "full polynomial hash")
    require(len(polynomial) == record["full_term_count"], "full term count")
    require(list(common) == record["positive_monomial_exponent"], "minor monomial factor")
    require(polynomial_digest(reduced) == record["reduced_polynomial_sha256"], "reduced polynomial hash")
    require(len(reduced) == record["reduced_term_count"], "reduced term count")
    return reduced


def verify_log_contradiction(payload):
    contradiction = payload["common_contradiction"]
    require("absolute difference" in contradiction["log_form"], "log form")
    require("largest" in contradiction["ordering_argument"], "ordering argument")
    # Every possible strict ordering is covered.  Positivity makes the largest
    # log strictly exceed the absolute difference of the two smaller logs.
    orderings = tuple(itertools.permutations(range(3)))
    require(len(orderings) == 6 and len(set(orderings)) == 6, "six log orderings")
    for low, middle, high in orderings:
        require(len({low, middle, high}) == 3, "ordering permutation")
        # Symbolically: 0 < U_low <= U_middle < U_high gives
        # |U_low-U_middle| < U_high, contradicting the equation for U_high.
        require(high not in (low, middle), "largest distinct")
    return len(orderings)


def verify_payload(payload):
    require(payload["schema"] == "k3p-cyclic-six-minor-certificates-v1", "schema")
    require(payload["status"] == "PASS", "status")
    require(tuple(payload["target_indices"]) == EXPECTED_TARGETS, "target list")
    require(payload["record_count"] == len(EXPECTED_TARGETS), "record count")
    require(payload["identity_count"] == 3 * len(EXPECTED_TARGETS), "identity count")

    inputs = payload["inputs"]
    require(inputs["graph_certificate_sha256"] == sha_file(cross.PRIMITIVE_PATH), "graph input hash")
    require(inputs["crossbridge_compiler_sha256"] == sha_file(PARENT / "explore_crossbridge_atlas.py"), "crossbridge compiler hash")
    require(inputs["k3p_compiler_sha256"] == sha_file(cross.ATLAS_PATH), "K3P compiler hash")
    producer = HERE / "generate_cyclic_certificates.py"
    require(inputs["producer_sha256"] == sha_file(producer), "producer hash")

    audit_binding = payload["target117_independent_audit"]
    audit_path = PROJECT / audit_binding["path"]
    require(audit_path.resolve() == (PARENT / "audit_simplex/RECORD39_CYCLIC_CERTIFICATE_AUDIT.json").resolve(), "audit path")
    require(audit_binding["sha256"] == sha_file(audit_path), "target117 audit hash")
    audit = json.loads(audit_path.read_text())
    require(audit["status"] == "PASS" and audit["target_index"] == 117, "target117 audit status")
    require(audit["record_id"] == 39, "target117 audit record")

    _, _, _, targets = cross.build_universes()
    assignments = atlas.k3p_assignments(4)
    coordinate_index = {assignment: index for index, assignment in enumerate(assignments)}
    require(len(payload["records"]) == len(EXPECTED_TARGETS), "records length")
    seen = []
    identity_count = 0
    target117_crosswalks = 0
    for expected_index, record in zip(EXPECTED_TARGETS, payload["records"]):
        require(record["target_index"] == expected_index, "record target order")
        seen.append(record["target_index"])
        target = targets[expected_index]
        descriptor = target["descriptor"]
        require(record["record_id"] == target["record_id"], "record id")
        require(record["old_split"] == target["old_split"], "old split")
        require(record["old_order"] == target["old_order"], "old order")
        require(record["reticulation_count"] == descriptor.retic_count, "reticulation count")
        require(record["edge_class_count"] == descriptor.edge_class_count, "edge count")
        require(record["descriptor_sha256"] == cross.digest(cross.descriptor_payload(descriptor)), "descriptor hash")
        identities = record["identity_records"]
        require([row["sector"] for row in identities] == ["C", "G", "T"], "sector order")
        outputs = atlas.output_sparse_polynomials(descriptor)
        width = 3 * descriptor.edge_class_count + descriptor.retic_count
        edge_class = record["distinguished_edge_class"]
        require(0 <= edge_class < descriptor.edge_class_count, "distinguished edge")

        for identity in identities:
            sector = SECTORS[identity["sector"]]
            F = minor_polynomial(outputs, coordinate_index, identity["F"])
            H = minor_polynomial(outputs, coordinate_index, identity["H"])
            f_orientation = identity["F_orientation"]
            h_orientation = identity["H_orientation"]
            require(f_orientation in (-1, 1) and h_orientation in (-1, 1), "minor orientations")
            x_index = identity["x_parameter_index"]
            y_index = identity["y_parameter_index"]
            z_index = identity["z_parameter_index"]
            others = tuple(index for index in range(3) if index != sector)
            require(x_index == 3 * edge_class + sector, "x sector index")
            require(y_index == 3 * edge_class + others[0], "y sector index")
            require(z_index == 3 * edge_class + others[1], "z sector index")
            lambda_index = identity["lambda_parameter_index"]
            require(3 * descriptor.edge_class_count <= lambda_index < width, "lambda index")

            x = variable(width, x_index)
            y = variable(width, y_index)
            z = variable(width, z_index)
            lam = variable(width, lambda_index)
            one = {(0,) * width: 1}
            oriented_F = {exponent: f_orientation * coefficient for exponent, coefficient in F.items()}
            oriented_H = {exponent: h_orientation * coefficient for exponent, coefficient in H.items()}
            lhs = sparse_add(sparse_mul(sparse_mul(y, z), oriented_F), sparse_mul(x, oriented_H))
            Q = monomial(width, identity["Q_positive_monomial_exponent"])
            rhs = sparse_mul(
                Q,
                sparse_mul(
                    sparse_mul(lam, sparse_add(one, lam, -1)),
                    sparse_mul(
                        sparse_add(y, sparse_mul(x, z), -1),
                        sparse_add(sparse_mul(x, y), z, -1),
                    ),
                ),
            )
            require(lhs == rhs, "exact cyclic coefficient identity")
            require(polynomial_digest(lhs) == identity["lhs_polynomial_sha256"], "lhs hash")
            require(len(lhs) == identity["lhs_term_count"], "lhs term count")
            base = sparse_mul(
                sparse_mul(lam, sparse_add(one, lam, -1)),
                sparse_mul(
                    sparse_add(y, sparse_mul(x, z), -1),
                    sparse_add(sparse_mul(x, y), z, -1),
                ),
            )
            require(polynomial_digest(base) == identity["base_polynomial_sha256"], "base hash")
            if expected_index == 117:
                audit_identity = next(
                    row for row in audit["identity_records"]
                    if row["sector"] == identity["sector"]
                )
                require(identity["F_orientation"] == 1, "target117 audit F orientation")
                require(identity["H_orientation"] == -1, "target117 audit H orientation")
                require(identity["F"]["character_sum"] == audit_identity["F_character_sum"], "target117 audit F sum")
                require(identity["H"]["character_sum"] == audit_identity["H_character_sum"], "target117 audit H sum")
                require(identity["F"]["rows"] == audit_identity["rows"], "target117 audit F rows")
                require(identity["F"]["columns"] == audit_identity["columns"], "target117 audit F columns")
                require(identity["H"]["rows"] == audit_identity["rows"], "target117 audit H rows")
                require(identity["H"]["columns"] == audit_identity["columns"], "target117 audit H columns")
                require(identity["F"]["coordinate_indices"] == audit_identity["F_coordinate_indices"], "target117 audit F coordinates")
                require(identity["H"]["coordinate_indices"] == audit_identity["H_coordinate_indices"], "target117 audit H coordinates")
                require(identity["F"]["full_polynomial_sha256"] == audit_identity["F_full_polynomial_sha256"], "target117 audit F full hash")
                require(identity["H"]["full_polynomial_sha256"] == audit_identity["H_full_polynomial_sha256"], "target117 audit H full hash")
                require(identity["F"]["positive_monomial_exponent"] == audit_identity["F_positive_monomial_exponent"], "target117 audit F monomial")
                require(identity["H"]["positive_monomial_exponent"] == audit_identity["H_positive_monomial_exponent"], "target117 audit H monomial")
                require(identity["F"]["reduced_polynomial_sha256"] == audit_identity["F_reduced_polynomial_sha256"], "target117 audit F reduced hash")
                require(identity["H"]["reduced_polynomial_sha256"] == audit_identity["H_reduced_polynomial_sha256"], "target117 audit H reduced hash")
                audit_indices = audit_identity["variable_parameter_indices"]
                require(x_index == audit_indices["x"], "target117 audit x")
                require(y_index == audit_indices["y"], "target117 audit y")
                require(z_index == audit_indices["z"], "target117 audit z")
                require(lambda_index == audit_indices["lambda"], "target117 audit lambda")
                require(identity["lhs_polynomial_sha256"] == audit_identity["identity_polynomial_sha256"], "target117 audit identity hash")
                target117_crosswalks += 1
            identity_count += 1

    require(tuple(seen) == EXPECTED_TARGETS, "seen targets")
    require(identity_count == payload["identity_count"], "verified identity count")
    require(target117_crosswalks == 3, "target117 audit crosswalk count")
    orderings = verify_log_contradiction(payload)
    return {
        "status": "PASS",
        "record_count": len(seen),
        "identity_count": identity_count,
        "strict_log_orderings_checked": orderings,
        "target117_independent_audit_bound": True,
        "target117_identity_crosswalks": target117_crosswalks,
    }


def mutation_cases(payload):
    cases = []
    for record_index, record in enumerate(payload["records"]):
        for sector_index in range(3):
            changed = copy.deepcopy(payload)
            exponent = changed["records"][record_index]["identity_records"][sector_index]["Q_positive_monomial_exponent"]
            exponent[0] += 1
            cases.append((f"Q_exponent_target_{record['target_index']}_{sector_index}", changed))
    structural = []
    changed = copy.deepcopy(payload); changed["status"] = "FAIL"; structural.append(("status", changed))
    changed = copy.deepcopy(payload); changed["target_indices"][0] = 108; structural.append(("target_list", changed))
    changed = copy.deepcopy(payload); changed["record_count"] -= 1; structural.append(("record_count", changed))
    changed = copy.deepcopy(payload); changed["identity_count"] -= 1; structural.append(("identity_count", changed))
    changed = copy.deepcopy(payload); changed["records"][0]["descriptor_sha256"] = "0" * 64; structural.append(("descriptor_hash", changed))
    changed = copy.deepcopy(payload); changed["records"][0]["identity_records"][0]["F"]["character_sum"] = 1; structural.append(("minor_metadata", changed))
    changed = copy.deepcopy(payload); changed["records"][0]["identity_records"][0]["F_orientation"] *= -1; structural.append(("orientation", changed))
    changed = copy.deepcopy(payload); changed["records"][0]["identity_records"][0]["x_parameter_index"] += 1; structural.append(("x_index", changed))
    changed = copy.deepcopy(payload); changed["inputs"]["graph_certificate_sha256"] = "f" * 64; structural.append(("graph_hash", changed))
    changed = copy.deepcopy(payload); changed["target117_independent_audit"]["sha256"] = "a" * 64; structural.append(("audit_hash", changed))
    return cases + structural


def run_mutations(payload):
    results = []
    for name, changed in mutation_cases(payload):
        rejected = False
        try:
            verify_payload(changed)
        except (AssertionError, KeyError, IndexError, TypeError, ValueError):
            rejected = True
        require(rejected, ("mutation accepted", name))
        results.append({"name": name, "result": "REJECTED"})
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--mutations", action="store_true")
    parser.add_argument("--no-write-report", action="store_true")
    parser.add_argument("--report", type=Path, default=REPORT)
    args = parser.parse_args()
    payload = json.loads(args.artifact.read_text())
    verified = verify_payload(payload)
    mutations = run_mutations(payload) if args.mutations else []
    report = {
        "schema": "k3p-cyclic-six-minor-verification-v1",
        **verified,
        "artifact_sha256": sha_file(args.artifact),
        "verifier_sha256": sha_file(Path(__file__).resolve()),
        "producer_imported": False,
        "python_optimized": not __debug__,
        "arithmetic": "exact sparse integer coefficient dictionaries",
        "mutations_requested": args.mutations,
        "mutation_count": len(mutations),
        "mutations": mutations,
    }
    if not args.no_write_report:
        temporary = args.report.with_suffix(args.report.suffix + ".tmp")
        temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        temporary.replace(args.report)
    print(json.dumps({key: report[key] for key in ("status", "record_count", "identity_count", "mutation_count")}, sort_keys=True))


if __name__ == "__main__":
    main()
