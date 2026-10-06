#!/usr/bin/env python3
"""Source-scope controls only; no mathematical proof or novelty certification."""
import argparse
import copy
import hashlib
import json
from math import gcd, prod
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    'rank': 1,
    'closed': True,
    'connected': True,
    'oriented': True,
    'dimension': 3,
    'prescribed_homology': 'full_group_isomorphism_type',
    'coefficient_ring': 'Z[H/Tors H]',
    'cover': 'maximal_free_abelian',
    'normalization': 'integral_order_mod_plus_minus_t_power',
    'preserve_content': True,
    'symmetry_power_parity': 'even',
}
MUTATIONS = {
    'cardinality_only': {'prescribed_homology': 'torsion_cardinality_only'},
    'refined_torsion': {'coefficient_ring': 'Z[H]', 'normalization': 'refined_torsion'},
    'rational_ring': {'coefficient_ring': 'Q[t,t^-1]'},
    'content_removed': {'preserve_content': False},
    'rank_two': {'rank': 2},
    'boundary_allowed': {'closed': False},
    'disconnected_allowed': {'connected': False},
    'unoriented_allowed': {'oriented': False},
    'odd_symmetry_power': {'symmetry_power_parity': 'unrestricted'},
    'relative_order_substitution': {'normalization': 'relative_first_order_without_equivalence'},
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def check_scope(model):
    for key, expected in EXPECTED.items():
        need(model.get(key) == expected, 'scope mismatch: ' + key)


def reduced(poly):
    return {int(e): int(c) for e, c in poly.items() if c}


def content(poly):
    result = 0
    for c in poly.values():
        result = gcd(result, abs(c))
    return result


def canonical_integral_unit_class(poly):
    poly = reduced(poly)
    if not poly:
        return ()
    first = min(poly)
    sign = 1 if poly[first] > 0 else -1
    return tuple(sorted((e-first, sign*c) for e, c in poly.items()))


def same_integral_unit_class(left, right):
    return canonical_integral_unit_class(left) == canonical_integral_unit_class(right)


def target_conditions(factors, poly):
    poly = reduced(poly)
    if not poly:
        return False
    k = min(poly) + max(poly)
    return (k % 2 == 0 and
            poly == {k-e: c for e, c in poly.items()} and
            abs(sum(poly.values())) == prod(factors))


def torsion_profile(factors):
    # The multiplicities of each p-power cyclic summand determine finite abelian
    # isomorphism type, unlike cardinality or the number of supplied generators.
    values = {}
    for d in factors:
        need(d >= 2, 'torsion cyclic factor must have order at least two')
        p = 2
        remaining = d
        while p*p <= remaining:
            power = 0
            while remaining % p == 0:
                power += 1
                remaining //= p
            if power:
                values.setdefault(p, []).append(power)
            p += 1
        if remaining > 1:
            values.setdefault(remaining, []).append(1)
    return tuple((p, tuple(sorted(powers))) for p, powers in sorted(values.items()))


def check_polynomial_only_claim(realization_claim):
    need(realization_claim.get('full_target_torsion_prescribed') is False,
         'polynomial-only theorem upgraded to prescribed full torsion group')
    need(realization_claim.get('cut_homology_torsion_free') is False,
         'rational cut rank upgraded to torsion-free integral homology')


def check_sources(fake=False):
    provenance = json.loads((ROOT/'PROVENANCE.json').read_text())
    for source in provenance['sources']:
        actual = hashlib.sha256((ROOT/source['file']).read_bytes()).hexdigest()
        expected = '0'*64 if fake else source['sha256']
        need(actual == expected, 'source hash mismatch: ' + source['id'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--falseguard', choices=list(MUTATIONS)+[
        'polynomial_only_upgraded', 'integral_cut_freeness', 'fake_source_hash',
        'same_order_same_group', 'content_is_unit'])
    args = parser.parse_args()
    if args.falseguard:
        name = args.falseguard
        if name in MUTATIONS:
            model = copy.deepcopy(EXPECTED)
            model.update(MUTATIONS[name])
            check_scope(model)
        elif name == 'polynomial_only_upgraded':
            check_polynomial_only_claim({'full_target_torsion_prescribed': True,
                                         'cut_homology_torsion_free': False})
        elif name == 'integral_cut_freeness':
            check_polynomial_only_claim({'full_target_torsion_prescribed': False,
                                         'cut_homology_torsion_free': True})
        elif name == 'fake_source_hash':
            check_sources(fake=True)
        elif name == 'same_order_same_group':
            need(torsion_profile([8]) == torsion_profile([2, 2, 2]),
                 'equal cardinality does not establish group isomorphism')
        elif name == 'content_is_unit':
            need(same_integral_unit_class({0: 8}, {0: 1}),
                 'non-unit integer content cannot be removed')
        raise RuntimeError('falseguard was incorrectly accepted')

    check_scope(EXPECTED)
    check_sources()
    checkpoint = json.loads((ROOT/'PRIMARY_RECONSTRUCTION.json').read_text())
    need(checkpoint['independence']['candidate_read'] is False,
         'independent checkpoint came after candidate access')
    need(checkpoint['independence']['independent_old_review_read'] is False,
         'independent checkpoint came after prior review access')
    need(set(checkpoint['literal_ohtsuki']['manifold_assumptions']) ==
         {'closed', 'connected', 'oriented', 'dimension 3'}, 'assumption reconstruction mismatch')

    count = 0
    for name, mutation in MUTATIONS.items():
        model = copy.deepcopy(EXPECTED)
        model.update(mutation)
        try:
            check_scope(model)
        except ValueError:
            count += 1
        else:
            raise ValueError('mutation admitted: ' + name)
    claim = {'full_target_torsion_prescribed': False,
             'cut_homology_torsion_free': False}
    check_polynomial_only_claim(claim)
    for key in claim:
        bad = dict(claim)
        bad[key] = True
        try:
            check_polynomial_only_claim(bad)
        except ValueError:
            count += 1
        else:
            raise ValueError('stronger source claim admitted: ' + key)

    candidate = {-1: 1, 0: 6, 1: 1}
    need(target_conditions([2, 2, 2], candidate), 'candidate fails source conditions')
    need(target_conditions([8], candidate), 'cyclic same-order control fails source conditions')
    need(torsion_profile([8]) != torsion_profile([2, 2, 2]), 'torsion cardinality collapsed')
    need(torsion_profile([2, 3]) == torsion_profile([6]), 'Chinese remainder control failed')
    need(torsion_profile([2, 4]) != torsion_profile([8]), 'noncyclic control collapsed')
    need(target_conditions([], {0: 1}), 'torsion-free boundary case failed')
    need(not target_conditions([2], {0: 1, 1: 1}), 'odd reciprocal exponent accepted')
    need(not target_conditions([8], {}), 'zero polynomial accepted')
    need(content(candidate) == 1, 'candidate integral content mismatch')
    need(content({0: 8}) == 8, 'constant integral content mismatch')
    need(not same_integral_unit_class({0: 8}, {0: 1}), 'content discarded as unit')
    need(target_conditions([8], {0: 8}), 'integral constant normalization control failed')
    unit_cases = 0
    for shift in range(-12, 13):
        for sign in [-1, 1]:
            shifted = {e+shift: sign*c for e, c in candidate.items()}
            need(same_integral_unit_class(candidate, shifted), 'integral unit class failed')
            need(target_conditions([2, 2, 2], shifted), 'source conditions not unit-invariant')
            need(content(shifted) == 1, 'unit changed content')
            unit_cases += 1
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        poly = {-1: 1, 0: p**3-2, 1: 1}
        need(target_conditions([p, p, p], poly), 'family fails literal source conditions')
        need(content(poly) == 1, 'candidate family content mismatch')
    receipt = {
        'verdict': 'PASS_LITERAL_SCOPE_AND_NORMALIZATION_CONTROLS',
        'scope_mutations_rejected': count,
        'unit_variants_checked': unit_cases,
        'candidate_family_primes_checked': 11,
        'candidate_torsion_profile': [[2, [1, 1, 1]]],
        'same_order_cyclic_control_profile': [[2, [3]]],
        'source_pdf_hashes_verified': 3,
        'central_topological_proof_certified': False,
        'novelty_or_priority_certified': False,
        'source_claims_are_manual_read_reconstruction': True,
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
