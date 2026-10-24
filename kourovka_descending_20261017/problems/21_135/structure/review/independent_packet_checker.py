#!/usr/bin/env python3
"""Read-only audit from explicit base degree lists, without hook formulas.

This verifies arithmetic necessary conditions. It does not realize a group or
verify the provenance of the two displayed base degree lists.
"""
from collections import Counter
from datetime import datetime, timezone
from functools import reduce
from hashlib import sha256
from itertools import product
from math import gcd, prod
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / "character_constraints_results.json"
BASES = {
    5: (1, 3, 3, 4, 5),
    7: (1, 6, 10, 10, 14, 14, 15, 21, 35),
}
BASE_ORDERS = {5: 60, 7: 2520}
BASE_LCMS = {5: 60, 7: 210}


def reject_duplicate_keys(pairs):
    out = {}
    for key, value in pairs:
        assert key not in out, ("duplicate JSON key", key)
        out[key] = value
    return out


def degrees(mapping):
    out = {}
    for key, value in mapping.items():
        degree = int(key)
        assert str(degree) == key and degree > 0
        assert type(value) is int and value > 0
        out[degree] = value
    return Counter(out)


def mass(multiset):
    return sum(count * degree**2 for degree, count in multiset.items())


def lcmm(values):
    return reduce(lambda a, b: a * b // gcd(a, b), values, 1)


def prime_divisors(value):
    ans = []
    candidate = 2
    while candidate * candidate <= value:
        if value % candidate == 0:
            ans.append(candidate)
            while value % candidate == 0:
                value //= candidate
        candidate += 1
    if value > 1:
        ans.append(value)
    return ans


def matrix_product(a, b):
    return (a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
            a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3])


def main():
    raw = INPUT.read_bytes()
    data = json.loads(raw, object_pairs_hook=reject_duplicate_keys)
    assert len(data["records"]) == 12
    records = {row["group"]: row for row in data["records"]}
    assert len(records) == 12
    independent = {}
    checks = []
    for n, base in BASES.items():
        for k in range(1, 7):
            name = f"A{n}^{k}"
            # Enumerate ordered character tuples, including repeated base
            # degrees as separate character choices. No convolution is used.
            actual = Counter(prod(choices) for choices in product(base, repeat=k))
            independent[name] = actual
            row = records[name]
            assert degrees(row["degrees"]) == actual, name
            order = BASE_ORDERS[n] ** k
            lcm_value = BASE_LCMS[n] ** k
            assert mass(actual) == order == row["order"], name
            assert sum(actual.values()) == len(base) ** k, name
            assert lcmm(actual) == lcm_value == row["lcm_degrees"], name
            assert row["ito_gap"] == order // lcm_value, name
            assert row["multiplicity_gcd"] == gcd(*actual.values()) == 1, name
            assert row["linear_multiplicity"] == actual[1] == 1, name
            prime_masses = {
                str(p): sum(c * d**2 for d, c in actual.items() if d % p)
                for p in prime_divisors(order)
            }
            assert row["prime_free_square_masses"] == prime_masses, name
            checks.append({
                "group": name,
                "ordered_tuples_enumerated": len(base) ** k,
                "distinct_degrees": len(actual),
                "order": order,
                "lcm_degrees": lcm_value,
                "ito_gap": order // lcm_value,
                "all_reported_fields_reproduced": True,
            })

    packet = data["central_C2_numeric_packet_A7_cubed"]
    principal = degrees(packet["principal_sector"])
    nontrivial = degrees(packet["nontrivial_sector"])
    available = independent["A7^3"]
    order = 2520**3
    half_order = order // 2
    assert set(principal) | set(nontrivial) == set(available)
    assert all(principal[d] + nontrivial[d] == available[d] for d in available)
    assert all(principal[d] <= available[d] for d in principal)
    assert all(nontrivial[d] <= available[d] for d in nontrivial)
    assert principal[1] == 1 and nontrivial[1] == 0
    assert all(d % 2 == 0 for d in nontrivial)
    assert all(principal[d] == count for d, count in available.items() if d % 2)
    assert mass(principal) == mass(nontrivial) == half_order == 8001504000
    assert all(half_order % d == 0 for d in set(principal) | set(nontrivial))
    odd_mass = sum(c * d**2 for d, c in available.items() if d % 2)
    even_mass = sum(c * d**2 for d, c in available.items() if not d % 2)
    assert odd_mass == 1892**3 == 6772724288
    assert odd_mass <= half_order
    assert order % 8 == 0
    assert even_mass >= half_order
    # For p=2, the multiplicity equation m=a+(p-1)b is the
    # already checked partition equation, with no other nontrivial sectors.
    packet_checks = {
        "source_group_label": "A7^3",
        "source_character_count": sum(available.values()),
        "source_distinct_degrees": len(available),
        "source_order": order,
        "principal_character_count": sum(principal.values()),
        "nontrivial_character_count": sum(nontrivial.values()),
        "principal_mass": mass(principal),
        "nontrivial_mass": mass(nontrivial),
        "principal_linear_character_count": principal[1],
        "nontrivial_linear_character_count": nontrivial[1],
        "odd_degree_mass": odd_mass,
        "even_degree_capacity": even_mass,
        "all_degrees_divide_half_order": True,
        "all_nontrivial_degrees_even": True,
        "full_multiset_partition": True,
        "central_conditions_1_through_4_pass": True,
        "group_or_projective_factor_set_realization": "not established",
    }
    identity = (1, 0, 0, 1)
    minus_identity = (-1, 0, 0, -1)
    rotation = (0, 1, -1, 0)
    reflection = (1, 0, 0, -1)
    square = matrix_product(rotation, rotation)
    cube = matrix_product(square, rotation)
    assert square == minus_identity
    assert matrix_product(square, square) == identity
    assert matrix_product(reflection, reflection) == identity
    commutator = matrix_product(matrix_product(matrix_product(
        cube, reflection), rotation), reflection)
    assert commutator == minus_identity
    assert matrix_product(matrix_product(reflection, rotation), reflection) == cube
    matrix_group = {identity}
    frontier = [identity]
    while frontier:
        element = frontier.pop()
        for generator in (rotation, reflection):
            new_element = matrix_product(element, generator)
            if new_element not in matrix_group:
                matrix_group.add(new_element)
                frontier.append(new_element)
    assert len(matrix_group) == 8
    # All negative d-dimensional blocks repeat the same 2D matrix d/2
    # times. Positive blocks are identity. This computes the global regular
    # trace without constructing any large block matrix.
    global_traces = Counter(
        half_order + half_order // 2 * (element[0] + element[3])
        for element in matrix_group
    )
    assert global_traces == Counter({order: 1, 0: 1, half_order: 6})
    matrix_checks = {
        "J_squared_is_minus_identity": True,
        "J_order": 4,
        "D_order": 2,
        "commutator_J_inverse_D_inverse_J_D": list(commutator),
        "generated_matrix_group_order": len(matrix_group),
        "D_conjugates_J_to_its_inverse": True,
        "global_regular_trace_multiplicities": dict(sorted(global_traces.items())),
        "nonidentity_unit_u_regular_trace": half_order,
        "group_basis_status": "These D8 units fail the nonidentity trace-zero requirement",
    }
    report = {
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "method": "Explicit base lists; independent ordered-tuple enumeration; exact integers",
        "input_sha256": sha256(raw).hexdigest(),
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "record_checks": checks,
        "central_packet_checks": packet_checks,
        "central_unit_matrix_checks": matrix_checks,
        "verdict": "All reported arithmetic reproduced; numerical feasibility only",
    }
    destination = HERE / "independent_packet_results.json"
    destination.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"records_checked": len(checks), "packet": packet_checks,
                      "matrices": matrix_checks}, sort_keys=True))


if __name__ == "__main__":
    main()
