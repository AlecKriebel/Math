#!/usr/bin/env python3
"""Exact elementary transfer controls; does not certify the imported existence theorem."""
import json
from fractions import Fraction
from itertools import product
from pathlib import Path

EXPECTED_CLAIM = {
    "schema": 1,
    "problem_id": 30003467,
    "problem_code": "OWR-15427-009",
    "disposition": "already_solved",
    "answer": "negative",
    "approaches": 0,
    "colors": 3,
    "threshold": 4,
    "coloring": "primal_points_weak_proper",
    "quantifiers": "for_each_family_and_point_set_there_exists_a_coloring",
    "witness_family": "finite_distinct_closed_euclidean_disks_variable_radii",
    "exact_trace_size": 4,
    "external_geometric_theorem": "Damásdi-Pálvölgyi Theorem 1, arXiv:2011.12187v1; Combinatorica 42 (2022) 1027-1048",
    "novelty_claim": False,
    "explicit_geometric_certificate": False,
    "formal_proof_certification": False,
    "dual_resolution_claim": False,
    "fixed_radius_counterexample_claim": False,
    "independent_human_review": False,
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def check_claim(claim):
    require(type(claim) is dict, "Claim must be an object")
    require(set(claim) == set(EXPECTED_CLAIM), "Claim key inventory differs")
    for key, wanted in EXPECTED_CLAIM.items():
        require(type(claim[key]) is type(wanted), "Claim type differs: " + key)
        require(claim[key] == wanted, "Wrongful or out-of-scope claim: " + key)

def strict_json(path):
    def pairs(items):
        d = {}
        for k, v in items:
            require(k not in d, "Duplicate JSON key: " + k)
            d[k] = v
        return d
    def bad_constant(value):
        raise ValueError("Nonfinite JSON constant: " + value)
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_constant=bad_constant)

def squared_distance(p, o):
    return sum((Fraction(x) - Fraction(y)) ** 2 for x, y in zip(p, o))

def closed_radius_squared(points, center, radius_squared):
    require(type(radius_squared) is Fraction and radius_squared > 0,
            "Positive exact squared radius required")
    distances = [squared_distance(p, center) for p in points]
    inside = [d for d in distances if d < radius_squared]
    require(bool(inside), "Nonempty original trace required")
    return (max(inside) + radius_squared) / 2

def run_controls():
    point_checks = 0
    cases = 0
    excluded_boundary_cases = 0
    points = list(product(range(-2, 3), repeat=2))
    for center in product(range(-1, 2), repeat=2):
        for r2 in map(Fraction, ["1/4", "1", "2", "5", "10"]):
            new_r2 = closed_radius_squared(points, center, r2)
            require(0 < new_r2 < r2, "Strict positive shrink failed")
            for p in points:
                d2 = squared_distance(p, center)
                require((d2 < r2) == (d2 <= new_r2), "Trace was changed")
                require(d2 != new_r2, "New boundary contains a point")
                point_checks += 1
            excluded_boundary_cases += int(any(squared_distance(p, center) == r2 for p in points))
            cases += 1

    # Failure controls exercise the assumptions, rather than accepting assertions as proof.
    failures = 0
    for r2 in [Fraction(0), Fraction(-1), 1.0]:
        try:
            closed_radius_squared([(0, 0)], (0, 0), r2)
        except ValueError:
            failures += 1
        else:
            raise ValueError("Invalid radius accepted")
    try:
        closed_radius_squared([(2, 0)], (0, 0), Fraction(1))
    except ValueError:
        failures += 1
    else:
        raise ValueError("Empty trace accepted")

    # Keeping the same radius when changing open to closed can fail.
    require(squared_distance((1, 0), (0, 0)) == Fraction(1), "Boundary fixture failed")
    require(not (Fraction(1) < Fraction(1)) and Fraction(1) <= Fraction(1),
            "Naive open-to-closed mutation was not detected")

    # Weak properness is not the all-three-colors property.
    color_sets = [set(c) for c in product(range(3), repeat=4)]
    weak = sum(len(s) >= 2 for s in color_sets)
    all_three = sum(len(s) == 3 for s in color_sets)
    require(weak == 78 and all_three == 36, "Coloring semantics mismatch")
    require(weak > all_three, "Weak properness conflated with polychromaticity")
    return {
        "scope": "elementary_transfer_and_scope_controls_only",
        "disk_cases": cases,
        "point_trace_checks": point_checks,
        "cases_with_excluded_original_boundary_points": excluded_boundary_cases,
        "invalid_transfer_inputs_rejected": failures,
        "four_point_three_label_assignments": len(color_sets),
        "weak_proper_assignments": weak,
        "all_three_color_assignments": all_three,
        "geometric_existence_theorem": "external_published_input_not_computationally_verified",
    }

def main():
    root = Path(__file__).resolve().parent
    check_claim(strict_json(root / "CLAIM.json"))
    print(json.dumps(run_controls(), sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
