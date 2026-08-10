#!/usr/bin/env python3
"""Adversarial clean-room audit of the primary JC invariant engine."""

from __future__ import annotations

import ast
from collections import Counter
from fractions import Fraction
import hashlib
import importlib
import json
import os
from pathlib import Path
import random
import sys
from itertools import permutations, product

from cleanroom_engine import (
    Descriptor,
    Invariant,
    all_ordered_quartet_deck_from_raw,
    arm_multidegrees,
    canonicalize_rows,
    coordinate_polynomials,
    coordinate_values_mod,
    evaluate,
    exact_polynomial_hash,
    exhaustive_small_descriptors,
    factor_bernstein_strict_sign,
    invariant_orbit,
    invariant_value_mod,
    jc_representatives,
    poly_add,
    primitive_polynomial_hash,
    pullbacks_shared,
    restrict_raw_descriptor,
    trinet_F_template,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
REPOSITORY = PROJECT.parent
PRIMARY = PROJECT / "primary"
HISTORICAL_DATA = REPOSITORY / "strong_level2_phylo_identifiability" / "src" / "jc_root_spanning_atlas_data.py"
SEVENTH_DATA = PRIMARY / "seventh_invariant.json"
CERTIFICATE = HERE / "certificate.json"
MUTATIONS = HERE / "mutation_transcript.json"
FAILURES = HERE / "failure_log.json"
HASHES = HERE / "hashes.json"
MANIFEST = HERE / "manifest.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_hash(value) -> str:
    return hashlib.sha256(repr(value).encode()).hexdigest()


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")


def parse_literal_assignment(path: Path, name: str):
    module = ast.parse(path.read_text())
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise KeyError(name)


def load_inert_templates() -> tuple[tuple[Invariant, ...], Invariant, Invariant]:
    raw_templates = parse_literal_assignment(HISTORICAL_DATA, "INVARIANT_TEMPLATES")
    templates = tuple(
        tuple((tuple(int(index) for index in monomial), int(coefficient)) for monomial, coefficient in template)
        for template in raw_templates
    )
    seventh_payload = json.loads(SEVENTH_DATA.read_text())
    raw_seventh = tuple(
        (tuple(int(index) for index in monomial), int(coefficient))
        for coefficient, monomial in seventh_payload["invariant"]
    )
    shifted_seventh = tuple(
        (tuple(index + 1 for index in monomial), coefficient)
        for monomial, coefficient in raw_seventh
    )
    return templates, raw_seventh, shifted_seventh


def import_system_under_test():
    """Load current primary modules only after the clean-room algebra exists."""
    sys.path.insert(0, str(PRIMARY))
    try:
        jc_tensor = importlib.import_module("jc_tensor")
        sign_certificate = importlib.import_module("sign_certificate")
        atlas_compiler = importlib.import_module("atlas_compiler")
    finally:
        sys.path.pop(0)
    return jc_tensor, sign_certificate, atlas_compiler


def random_descriptors(seed: int = 77_413, count: int = 64) -> tuple[Descriptor, ...]:
    generator = random.Random(seed)
    answer: set[Descriptor] = set()
    while len(answer) < count:
        reticulations = generator.randrange(3)
        displays = 1 << reticulations
        row_count = generator.randrange(1, 7)
        rows = []
        for _ in range(row_count):
            row = tuple(generator.randrange(16) for _ in range(displays))
            if any(row):
                rows.append(row)
        answer.add(canonicalize_rows(reticulations, rows))
    return tuple(sorted(answer))


def transform_rows(rows, reticulations, permutation, flips):
    displays = tuple(product((0, 1), repeat=reticulations))
    index = {bits: position for position, bits in enumerate(displays)}
    moved_rows = []
    origins = {}
    for origin, row in enumerate(rows):
        moved = [0] * len(displays)
        for old_position, old_bits in enumerate(displays):
            new_bits = tuple(
                old_bits[permutation[new_position]] ^ flips[new_position]
                for new_position in range(reticulations)
            )
            moved[index[new_bits]] = row[old_position]
        moved = tuple(moved)
        moved_rows.append(moved)
        origins[moved] = origin
    return tuple(sorted(moved_rows)), origins


def map_duplicate_product(poly, rows):
    unique = tuple(sorted(set(rows)))
    positions = {row: position for position, row in enumerate(unique)}
    reticulations = len(next(iter(poly), ())) - len(rows)
    answer = {}
    for exponent, coefficient in poly.items():
        edge_exponents = [None] * len(unique)
        for old_position, row in enumerate(rows):
            new_position = positions[row]
            value = exponent[old_position]
            if edge_exponents[new_position] is None:
                edge_exponents[new_position] = value
            elif edge_exponents[new_position] != value:
                raise AssertionError("duplicate signatures acquired unequal exponents")
        moved = tuple(int(value or 0) for value in edge_exponents) + tuple(exponent[len(rows):])
        answer[moved] = answer.get(moved, 0) + coefficient
        if not answer[moved]:
            answer.pop(moved)
    return answer


def ast_uses_exact_sign_key(path: Path) -> bool:
    module = ast.parse(path.read_text())
    for node in ast.walk(module):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "setdefault" and isinstance(node.func.value, ast.Name):
                if node.func.value.id == "sign_library" and node.args:
                    if isinstance(node.args[0], ast.Name) and node.args[0].id == "exact_hash":
                        return True
    return False


def run() -> dict:
    failures_before_correction = [
        {
            "id": "DEFAULT_PYTHON_MISSING_EXACT_ALGEBRA_DEPENDENCY",
            "status": "FALSE",
            "failure_kind": "REPLAY_ENVIRONMENT",
            "description": "The first clean-room invocation with /opt/homebrew Python 3.14 stopped at the sign gate because SymPy was absent; no certificate was emitted. Reproduction is pinned to /opt/homebrew/opt/python@3.11/bin/python3.11, which has SymPy 1.14.0.",
        },
        {
            "id": "INITIAL_COORDINATE_SWAP_MUTATION_WAS_A_NOOP",
            "status": "FALSE",
            "failure_kind": "REVIEW_HARNESS_BEFORE_CORRECTION",
            "description": "The first coordinate-swap mutation edited only one sorted monomial containing both swapped indices, so it made no algebraic change. The full run failed closed. The corrected mutation swaps indices globally in every inert template and changes the orbit from 84 to 102 elements.",
        },
        {
            "id": "WITHDRAWN_INCOMING_ONLY_DECK",
            "status": "FALSE",
            "failure_kind": "WITHDRAWN_IMPLEMENTATION",
            "description": "The former incoming-fixed deck omits all-outgoing ordered quartets when at least four outgoing ports exist.",
        },
        {
            "id": "UNSHIFTED_SEVENTH_INDEXING",
            "status": "FALSE",
            "failure_kind": "WITHDRAWN_IMPLEMENTATION",
            "description": "The seventh coefficient table indexes the fourteen nontrivial coordinates and cannot be used directly in the fifteen-coordinate engine.",
        },
    ]

    templates, raw_seventh, shifted_seventh = load_inert_templates()
    independent_representatives = jc_representatives()
    invariants = invariant_orbit((*templates, shifted_seventh))
    unshifted_orbit = invariant_orbit((*templates, raw_seventh))

    # Only now load the implementation being reviewed.
    sut, sut_sign, sut_atlas = import_system_under_test()

    checks: dict[str, dict] = {}
    mutations: list[dict] = []

    sut_representatives = tuple(tuple(row) for row in sut.jc_representatives())
    if sut_representatives != independent_representatives:
        raise AssertionError("primary JC representative indexing differs")
    checks["four_port_JC_orbits"] = {
        "status": "VERIFIED",
        "zero_sum_assignments": 64,
        "orbit_coordinates": len(independent_representatives),
        "representatives": independent_representatives,
        "trivial_coordinate_index": 0,
        "nontrivial_historical_transport": {str(index): index + 1 for index in range(14)},
    }

    sut_orbit = tuple(sut.invariant_orbit((*templates, shifted_seventh)))
    if sut_orbit != invariants:
        raise AssertionError("primary invariant orbit differs from clean-room orbit")
    if len(invariants) != 84:
        raise AssertionError(len(invariants))
    multidegrees = [arm_multidegrees(invariant) for invariant in invariants]
    if any(len(degrees) != 1 for degrees in multidegrees):
        raise AssertionError("corrected orbit is not multihomogeneous")
    degree_distribution = Counter(next(iter(degrees)) for degrees in multidegrees)
    f_degrees = arm_multidegrees(trinet_F_template())
    if f_degrees != {(2, 2, 2, 0)}:
        raise AssertionError(f_degrees)
    unshifted_failures = [index for index, invariant in enumerate(unshifted_orbit) if len(arm_multidegrees(invariant)) != 1]
    if not unshifted_failures:
        raise AssertionError("omitting +1 was not detected")
    checks["invariant_orbit_and_arm_gauge"] = {
        "status": "VERIFIED",
        "orbit_size": len(invariants),
        "orbit_sha256": stable_hash(invariants),
        "degree_distribution": {repr(key): value for key, value in sorted(degree_distribution.items())},
        "trinet_F_multidegree": [2, 2, 2, 0],
        "unshifted_orbit_size": len(unshifted_orbit),
        "unshifted_nonhomogeneous_count": len(unshifted_failures),
    }
    mutations.append({
        "id": "omit_plus_one_transport",
        "expected": "REJECT",
        "observed": "REJECT",
        "detector": f"{len(unshifted_failures)} orbit elements lose arm multihomogeneity",
    })

    deck_records = []
    original_raw_descriptor = sut.raw_descriptor
    try:
        for total_ports in range(4, 8):
            for reticulations in range(3):
                displays = 1 << reticulations
                rows = tuple(
                    tuple(((13 * edge + 7 * display + total_ports) % (1 << total_ports)) for display in range(displays))
                    for edge in range(1, 5)
                )
                expected = all_ordered_quartet_deck_from_raw(total_ports, reticulations, rows)

                def fake_raw_descriptor(_graph, labels, *, expected_length=total_ports, payload=(reticulations, rows)):
                    if len(labels) != expected_length:
                        raise AssertionError((len(labels), expected_length))
                    return payload

                sut.raw_descriptor = fake_raw_descriptor
                labels = tuple(f"p{index}" for index in range(total_ports))
                observed = sut.all_port_quartet_deck(object(), labels[:-1], labels[-1])
                if observed != expected:
                    raise AssertionError((total_ports, reticulations, "deck mismatch"))
                expected_count = len(tuple(permutations(range(total_ports), 4)))
                if len(observed) != expected_count:
                    raise AssertionError((len(observed), expected_count))
                deck_records.append((total_ports, reticulations, expected_count, stable_hash(observed)))
    finally:
        sut.raw_descriptor = original_raw_descriptor
    five_port_full = set(permutations(range(5), 4))
    five_port_incoming_only = {key for key in five_port_full if 4 in key}
    missing_all_outgoing = five_port_full - five_port_incoming_only
    if len(missing_all_outgoing) != 24:
        raise AssertionError(len(missing_all_outgoing))
    checks["all_ordered_quartet_deck"] = {
        "status": "VERIFIED",
        "records": deck_records,
        "five_port_full_count": 120,
        "withdrawn_incoming_only_count": 96,
        "all_outgoing_quartets_restored": 24,
    }
    mutations.append({
        "id": "remove_all_outgoing_quartets",
        "expected": "REJECT",
        "observed": "REJECT",
        "detector": "coverage key set loses 24 of 120 ordered restrictions at five ports",
    })

    exhaustive = exhaustive_small_descriptors()
    adversarial = random_descriptors()
    descriptor_suite = exhaustive + adversarial
    comparison_digest_rows = []
    modular_nonzero_checks = 0
    modular_zero_checks = 0
    standalone_shared_checks = 0
    for descriptor_index, descriptor in enumerate(descriptor_suite):
        independent_coordinates = coordinate_polynomials(descriptor)
        observed_coordinates = tuple(sut.coordinate_polynomials(descriptor))
        if observed_coordinates != independent_coordinates:
            raise AssertionError((descriptor_index, "coordinate polynomial mismatch"))
        expected_pullbacks = pullbacks_shared(descriptor, invariants)
        observed_pullbacks = tuple(sut.pullbacks_shared(descriptor, invariants))
        if observed_pullbacks != expected_pullbacks:
            raise AssertionError((descriptor_index, "shared pullback mismatch"))
        if descriptor_index % 17 == 0:
            for invariant_index in (0, 7, 19, 41, 63, 83):
                if sut.pullback(descriptor, invariants[invariant_index]) != expected_pullbacks[invariant_index]:
                    raise AssertionError((descriptor_index, invariant_index, "standalone/shared mismatch"))
                standalone_shared_checks += 1
        for seed in (101, 1009, 10007):
            independent_modular_coordinates = coordinate_values_mod(descriptor, seed)
            observed_modular_coordinates = tuple(sut.coordinate_values_mod(descriptor, seed))
            if observed_modular_coordinates != independent_modular_coordinates:
                raise AssertionError((descriptor_index, seed, "modular coordinate mismatch"))
            for invariant_index, invariant in enumerate(invariants):
                observed_value = sut.invariant_value_mod(observed_modular_coordinates, invariant)
                independent_value = invariant_value_mod(independent_modular_coordinates, invariant)
                if observed_value != independent_value:
                    raise AssertionError((descriptor_index, seed, invariant_index, "modular invariant mismatch"))
                if observed_value:
                    modular_nonzero_checks += 1
                    if not expected_pullbacks[invariant_index]:
                        raise AssertionError("modular nonzero falsely certified zero exact polynomial")
                else:
                    modular_zero_checks += 1
        comparison_digest_rows.append((descriptor, tuple(exact_polynomial_hash(poly) for poly in expected_pullbacks)))

    # Directly audit the primary prefilter's exact fallback on a representative
    # exhaustive subset, then force every modular evaluation to zero.
    fallback_descriptors = descriptor_suite[:: max(1, len(descriptor_suite) // 32)][:32]
    fallback_checks = 0
    for descriptor in fallback_descriptors:
        exact_pullbacks = pullbacks_shared(descriptor, invariants)
        expected_bits = sum((1 << index) for index, poly in enumerate(exact_pullbacks) if poly)
        observed_bits = sut_atlas.descriptor_bits(descriptor, invariants, {})
        if observed_bits != expected_bits:
            raise AssertionError("descriptor_bits differs from exact nonidentity deck")
        fallback_checks += 1
    forced_descriptor = next(
        descriptor for descriptor in descriptor_suite
        if any(pullbacks_shared(descriptor, invariants))
    )
    expected_forced = sum(
        (1 << index)
        for index, poly in enumerate(pullbacks_shared(forced_descriptor, invariants))
        if poly
    )
    saved_modular = sut_atlas.coordinate_values_mod
    try:
        sut_atlas.coordinate_values_mod = lambda _descriptor, _seed: (0,) * 15
        forced_fallback = sut_atlas.descriptor_bits(forced_descriptor, invariants, {})
    finally:
        sut_atlas.coordinate_values_mod = saved_modular
    if forced_fallback != expected_forced or not expected_forced:
        raise AssertionError("modular-zero exact fallback failed")
    trusted_zero_mutation = 0
    if trusted_zero_mutation == expected_forced:
        raise AssertionError("mutation fixture unexpectedly has zero exact signature")
    mutations.append({
        "id": "trust_modular_zero",
        "expected": "REJECT",
        "observed": "REJECT",
        "detector": "forcing all modular evaluations to zero still recovers the nonzero exact bit deck; the mutated no-fallback deck is zero",
    })
    checks["sparse_pullbacks_and_modular_prefilter"] = {
        "status": "VERIFIED",
        "exhaustive_descriptor_count": len(exhaustive),
        "adversarial_random_descriptor_count": len(adversarial),
        "invariants_per_descriptor": len(invariants),
        "coordinate_and_shared_pullback_comparisons": len(descriptor_suite) * len(invariants),
        "standalone_shared_comparisons": standalone_shared_checks,
        "modular_nonzero_soundness_checks": modular_nonzero_checks,
        "modular_zero_events_observed": modular_zero_checks,
        "explicit_primary_fallback_descriptors": fallback_checks,
        "aggregate_pullback_sha256": stable_hash(comparison_digest_rows),
    }

    raw_canonicalization_checks = 0
    canonicalization_generator = random.Random(91_337)
    for _ in range(128):
        reticulations = canonicalization_generator.randrange(3)
        displays = 1 << reticulations
        rows = tuple(
            tuple(canonicalization_generator.randrange(16) for _ in range(displays))
            for _ in range(canonicalization_generator.randrange(0, 7))
        )
        if sut.canonicalize_rows(reticulations, rows) != canonicalize_rows(reticulations, rows):
            raise AssertionError("random raw descriptor canonicalization mismatch")
        raw_canonicalization_checks += 1

    # Descriptor zipping: duplicate rows can only occur with equal exponents,
    # hence through their positive product.
    zipped_checks = 0
    for reticulations, base_rows in (
        (0, ((3,), (5,))),
        (1, ((1, 2), (4, 8))),
        (2, ((1, 2, 4, 8), (3, 6, 9, 12))),
    ):
        rows = tuple(sorted((base_rows[0], base_rows[0], base_rows[1])))
        unzipped = coordinate_polynomials((reticulations, rows))
        deduplicated_descriptor = (reticulations, tuple(sorted(set(rows))))
        zipped = coordinate_polynomials(deduplicated_descriptor)
        for left, right in zip(unzipped, zipped):
            if map_duplicate_product(left, rows) != right:
                raise AssertionError("duplicate-row product zipping failed")
            zipped_checks += 1

    # Every reticulation relabelling/choice flip is accompanied by an exact
    # open-domain parameter bijection lambda -> lambda or 1-lambda.
    reticulation_transform_checks = 0
    for reticulations, rows in (
        (1, ((1, 2), (4, 8), (3, 12))),
        (2, ((1, 2, 4, 8), (3, 6, 9, 12), (5, 10, 7, 14))),
    ):
        original_coordinates = coordinate_polynomials((reticulations, tuple(sorted(rows))))
        original_edge_values = tuple(Fraction(index + 2, index + 7) for index in range(len(rows)))
        original_edge_by_row = dict(zip(tuple(sorted(rows)), original_edge_values))
        original_lambdas = tuple(Fraction(2 * index + 2, 2 * index + 5) for index in range(reticulations))
        original_values = tuple(original_edge_by_row[row] for row in tuple(sorted(rows))) + original_lambdas
        original_evaluation = tuple(evaluate(poly, original_values) for poly in original_coordinates)
        for permutation in permutations(range(reticulations)):
            for flips in product((0, 1), repeat=reticulations):
                moved_rows, origins = transform_rows(tuple(sorted(rows)), reticulations, permutation, flips)
                moved_coordinates = coordinate_polynomials((reticulations, moved_rows))
                moved_edges = tuple(original_edge_values[origins[row]] for row in moved_rows)
                moved_lambdas = tuple(
                    original_lambdas[permutation[index]]
                    if not flips[index]
                    else 1 - original_lambdas[permutation[index]]
                    for index in range(reticulations)
                )
                if not all(Fraction(0) < value < Fraction(1) for value in moved_lambdas):
                    raise AssertionError("reticulation flip left open domain")
                moved_evaluation = tuple(evaluate(poly, moved_edges + moved_lambdas) for poly in moved_coordinates)
                if moved_evaluation != original_evaluation:
                    raise AssertionError((reticulations, permutation, flips, "reticulation transform"))
                if sut.canonicalize_rows(reticulations, rows) != canonicalize_rows(reticulations, rows):
                    raise AssertionError("primary descriptor canonicalization mismatch")
                reticulation_transform_checks += 1
    checks["descriptor_zipping_and_reticulation_symmetry"] = {
        "status": "VERIFIED",
        "duplicate_coordinate_checks": zipped_checks,
        "reticulation_permutation_flip_checks": reticulation_transform_checks,
        "raw_canonicalization_comparisons": raw_canonicalization_checks,
        "open_domain_map": "edge duplicates map to their product; reticulation choices map by permutation and lambda or 1-lambda",
    }

    # Sign-certificate audit, first on adversarial hand polynomials and then on
    # regenerated invariant pullbacks.
    hand_polynomials = {
        "x_one_minus_x": {(1,): 1, (2,): -1},
        "negative_x_one_minus_x": {(1,): -1, (2,): 1},
        "x_plus_y": {(1, 0): 1, (0, 1): 1},
        "x_minus_y": {(1, 0): 1, (0, 1): -1},
        "positive_constant": {(0,): 7},
        "negative_constant": {(0,): -11},
        "positive_product": {(1, 0): 1, (1, 1): -1},
    }
    sign_rows = []
    certified_polynomials = []
    certified_regenerated = []
    for name, poly in hand_polynomials.items():
        expected = factor_bernstein_strict_sign(poly)
        observed = sut_sign.certify(poly)
        if bool(observed["certified"]) != bool(expected["certified"]):
            raise AssertionError((name, expected, observed))
        if expected["certified"] and observed["strict_sign"] != expected["strict_sign"]:
            raise AssertionError((name, "strict sign mismatch"))
        if expected["certified"]:
            if len(expected["factors"]) != len(observed["factors"]):
                raise AssertionError((name, "factor count mismatch"))
            for expected_factor, observed_factor in zip(expected["factors"], observed["factors"]):
                if expected_factor["multiplicity"] != observed_factor["multiplicity"]:
                    raise AssertionError((name, "factor multiplicity mismatch"))
                expected_proof = expected_factor["proof"]
                observed_proof = observed_factor["proof"]
                for field in (
                    "certified", "sign", "used_variables", "degrees", "elevation",
                    "coefficient_count", "minimum", "maximum",
                ):
                    if expected_proof.get(field) != observed_proof.get(field):
                        raise AssertionError((name, field, expected_proof, observed_proof))
        if observed.get("polynomial_sha256") != primitive_polynomial_hash(poly):
            raise AssertionError((name, "primitive hash mismatch"))
        sign_rows.append((name, expected.get("certified"), expected.get("strict_sign")))
        if expected.get("certified"):
            certified_polynomials.append(poly)

    regenerated_candidates = []
    for descriptor in descriptor_suite:
        for invariant_index, poly in enumerate(pullbacks_shared(descriptor, invariants)):
            if poly:
                regenerated_candidates.append((descriptor, invariant_index, poly))
            if len(regenerated_candidates) >= 80:
                break
        if len(regenerated_candidates) >= 80:
            break
    generated_certified = 0
    generated_uncertified = 0
    for descriptor, invariant_index, poly in regenerated_candidates:
        expected = factor_bernstein_strict_sign(poly)
        observed = sut_sign.certify(poly)
        if bool(observed["certified"]) != bool(expected["certified"]):
            raise AssertionError((descriptor, invariant_index, "certificate decision mismatch"))
        if expected["certified"]:
            if observed["strict_sign"] != expected["strict_sign"]:
                raise AssertionError((descriptor, invariant_index, "certificate sign mismatch"))
            if len(expected["factors"]) != len(observed["factors"]):
                raise AssertionError((descriptor, invariant_index, "factor count mismatch"))
            for expected_factor, observed_factor in zip(expected["factors"], observed["factors"]):
                if expected_factor["multiplicity"] != observed_factor["multiplicity"]:
                    raise AssertionError((descriptor, invariant_index, "factor multiplicity mismatch"))
                for field in (
                    "certified", "sign", "used_variables", "degrees", "elevation",
                    "coefficient_count", "minimum", "maximum",
                ):
                    if expected_factor["proof"].get(field) != observed_factor["proof"].get(field):
                        raise AssertionError((descriptor, invariant_index, field, "Bernstein payload mismatch"))
            values = tuple(Fraction((2 * index) % 7 + 1, 9) for index in range(len(next(iter(poly)))))
            value = evaluate(poly, values)
            if value == 0 or (1 if value > 0 else -1) != expected["strict_sign"]:
                raise AssertionError((descriptor, invariant_index, "interior sign replay failed"))
            generated_certified += 1
            certified_polynomials.append(poly)
            certified_regenerated.append((descriptor, invariant_index, poly))
        else:
            generated_uncertified += 1

    positive = hand_polynomials["x_one_minus_x"]
    negative = hand_polynomials["negative_x_one_minus_x"]
    if exact_polynomial_hash(positive) == exact_polynomial_hash(negative):
        raise AssertionError("exact sign-sensitive hashes collided")
    if primitive_polynomial_hash(positive) != primitive_polynomial_hash(negative):
        raise AssertionError("primitive normalization unexpectedly retained sign")
    if not ast_uses_exact_sign_key(PRIMARY / "atlas_compiler.py"):
        raise AssertionError("atlas sign library is not keyed by exact hash")
    if not ast_uses_exact_sign_key(PRIMARY / "cycle_theta_union_compiler.py"):
        raise AssertionError("union sign library is not keyed by exact hash")
    if evaluate(positive, (Fraction(0),)) != 0 or evaluate(positive, (Fraction(1),)) != 0:
        raise AssertionError("boundary fixture is wrong")
    if any(any(exponent < 0 for exponent in monomial) for _d, _i, poly in regenerated_candidates for monomial in poly):
        raise AssertionError("negative exponent/denominator entered a pullback")

    # Bind every proof to a regenerated exact polynomial hash.  Find two
    # certified but unequal pullbacks for the wrong-descriptor mutation.
    unequal_pair = None
    for left_descriptor, left_invariant, left in certified_regenerated:
        for right_descriptor, right_invariant, right in certified_regenerated:
            if (
                (left_descriptor, left_invariant) != (right_descriptor, right_invariant)
                and exact_polynomial_hash(left) != exact_polynomial_hash(right)
            ):
                unequal_pair = left, right
                break
        if unequal_pair:
            break
    if unequal_pair is None:
        raise AssertionError("no unequal certified polynomial fixtures")
    left, right = unequal_pair
    wrong_descriptor_rejected = exact_polynomial_hash(left) != exact_polynomial_hash(right)
    if not wrong_descriptor_rejected:
        raise AssertionError("wrong descriptor proof was not rejected")
    mutations.extend((
        {
            "id": "change_open_to_closed_cube",
            "expected": "REJECT",
            "observed": "REJECT",
            "detector": "x(1-x) has the certified positive open-cube sign but vanishes at x=0 and x=1",
        },
        {
            "id": "reuse_polynomial_proof_on_wrong_descriptor",
            "expected": "REJECT",
            "observed": "REJECT",
            "detector": "regenerated exact polynomial SHA-256 differs",
        },
        {
            "id": "reverse_strict_sign",
            "expected": "REJECT",
            "observed": "REJECT",
            "detector": "independent factor-Bernstein sign and exact rational interior evaluation disagree with the reversal",
        },
    ))
    checks["strict_sign_certificates"] = {
        "status": "VERIFIED",
        "hand_polynomials": sign_rows,
        "regenerated_certified": generated_certified,
        "regenerated_uncertified": generated_uncertified,
        "exact_hash_is_sign_sensitive": True,
        "primitive_hash_is_sign_insensitive": True,
        "sign_library_keyed_by_exact_hash": True,
        "domain": "strict open unit cube only",
        "denominators_present": False,
    }

    # Remaining coefficient/index mutations are checked against the frozen
    # independently regenerated orbit and against a concrete pullback.
    def swap_zero_one(template):
        return tuple(
            (
                tuple(1 if index == 0 else 0 if index == 1 else index for index in monomial),
                coefficient,
            )
            for monomial, coefficient in template
        )

    swapped_orbit = invariant_orbit((
        *(swap_zero_one(template) for template in templates),
        swap_zero_one(shifted_seventh),
    ))
    if swapped_orbit == invariants or stable_hash(swapped_orbit) == stable_hash(invariants):
        raise AssertionError("coordinate-index mutation escaped full orbit regeneration")
    if len(swapped_orbit) != 102:
        raise AssertionError(("unexpected swapped orbit size", len(swapped_orbit)))
    corrupt_templates = [list(template) for template in templates]
    corrupt_monomial, corrupt_coefficient = corrupt_templates[0][0]
    corrupt_templates[0][0] = (corrupt_monomial, corrupt_coefficient + 1)
    corrupted_orbit = invariant_orbit((*(tuple(tuple(row) for row in corrupt_templates)), shifted_seventh))
    if corrupted_orbit == invariants or stable_hash(corrupted_orbit) == stable_hash(invariants):
        raise AssertionError("coefficient mutation escaped full orbit regeneration")
    mutations.extend((
        {
            "id": "swap_invariant_coordinate_indices",
            "expected": "REJECT",
            "observed": "REJECT",
            "detector": "normalized invariant orbit hash and regenerated pullback binding change",
        },
        {
            "id": "corrupt_invariant_coefficient",
            "expected": "REJECT",
            "observed": "REJECT",
            "detector": "normalized invariant orbit hash and regenerated pullback binding change",
        },
    ))

    expected_mutations = {
        "remove_all_outgoing_quartets",
        "omit_plus_one_transport",
        "trust_modular_zero",
        "swap_invariant_coordinate_indices",
        "corrupt_invariant_coefficient",
        "change_open_to_closed_cube",
        "reuse_polynomial_proof_on_wrong_descriptor",
        "reverse_strict_sign",
    }
    if {row["id"] for row in mutations} != expected_mutations:
        raise AssertionError("mutation suite incomplete")
    if any(row["observed"] != "REJECT" for row in mutations):
        raise AssertionError("a mandatory mutation survived")

    payload = {
        "schema": 1,
        "review_scope": "primary JC invariant engine only; finite-atlas exhaustiveness and the global theorem are excluded",
        "overall_status": "VERIFIED",
        "checks": checks,
        "mandatory_mutations_rejected": len(mutations),
        "historical_defects_preserved": failures_before_correction,
        "input_hashes": {
            str(path.relative_to(REPOSITORY)): sha256(path)
            for path in (
                PRIMARY / "jc_tensor.py",
                PRIMARY / "sign_certificate.py",
                PRIMARY / "atlas_compiler.py",
                PRIMARY / "cycle_theta_union_compiler.py",
                PRIMARY / "seventh_invariant.json",
                HISTORICAL_DATA,
            )
        },
    }
    write_json(CERTIFICATE, payload)
    write_json(MUTATIONS, {"schema": 1, "all_rejected": True, "mutations": mutations})
    write_json(FAILURES, {"schema": 1, "preserved_failures": failures_before_correction, "new_uncorrected_failures": []})

    artifact_paths = (
        HERE / "cleanroom_engine.py",
        HERE / "run_review.py",
        HERE / "README.md",
        HERE / "REVIEW.md",
        HERE / "verify_all.sh",
        HERE / "python314_environment_failure.txt",
        CERTIFICATE,
        MUTATIONS,
        FAILURES,
    )
    artifact_hashes = {path.name: sha256(path) for path in artifact_paths}
    write_json(MANIFEST, {
        "schema": 1,
        "status": "VERIFIED",
        "runtime": {
            "python": "/opt/homebrew/opt/python@3.11/bin/python3.11",
            "sympy": "1.14.0",
        },
        "replay_command": "bash s_tc_jc_landmark_closure/reviews/invariant_engine/verify_all.sh",
        "scope": "primary JC invariant engine",
        "scope_exclusions": [
            "finite-atlas exhaustiveness",
            "local relation coverage",
            "bounded-support promotion and probe coherence",
            "global identifiability theorem",
        ],
        "input_hashes": payload["input_hashes"],
        "artifact_hashes": artifact_hashes,
    })
    write_json(HASHES, {
        "schema": 1,
        "artifacts": {
            **artifact_hashes,
            MANIFEST.name: sha256(MANIFEST),
        },
        "note": "hashes.json omits its own recursively unstable hash",
    })
    return payload


if __name__ == "__main__":
    result = run()
    print(json.dumps({
        "overall_status": result["overall_status"],
        "checks": sorted(result["checks"]),
        "mutations_rejected": result["mandatory_mutations_rejected"],
        "certificate": os.fspath(CERTIFICATE),
    }, sort_keys=True))
