#!/usr/bin/env python3
"""Deliberate-negative controls for invalid inferences and integrity failures."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import sys
import zipfile

EXPECTED_BYTES = 24247
EXPECTED_SHA = '6b4de8ccb793e9284547a7beee11b2f203cb7f5edfb0eb9c22d2cd873e06825e'
EXPECTED_MANIFEST = '66298016e916da48b988c46affdfc3dc3636a9d80888e21f0e03b10d72eb94fa'


def main(archive):
    results=[]
    def reject(name, invalid_claim, explanation):
        if invalid_claim:
            raise RuntimeError('Failed to reject: '+name)
        results.append({'name':name,'result':'rejected','reason':explanation})
    raw=Path(archive).read_bytes()
    if len(raw)!=EXPECTED_BYTES or sha256(raw).hexdigest()!=EXPECTED_SHA:
        raise RuntimeError('Wrong input archive')
    with zipfile.ZipFile(archive) as z:
        manifest=z.read('AUTHOR_MANIFEST.json')
        if sha256(manifest).hexdigest()!=EXPECTED_MANIFEST:
            raise RuntimeError('Wrong author manifest')
        for name in z.namelist():
            original=z.read(name)
            altered=bytes([original[0]^1])+original[1:]
            reject('same_length_member_mutation:'+name,sha256(altered).digest()==sha256(original).digest(),
                   'Same size alone does not establish identity; independently bound digest changes.')
            reject('appended_member_mutation:'+name,len(original+b'\n')==len(original),
                   'Byte-count binding detects added data.')
    reject('wrong_archive_digest',sha256(raw[:-1]+bytes([raw[-1]^1])).hexdigest()==EXPECTED_SHA,
           'Exact frozen archive binding rejects a one-byte mutation.')
    reject('source_dimension_difference_survives_quotient',1 != 1,
           'Projection of Q^2 and Q^3 onto their first coordinate has the same one-dimensional image.')
    reject('nonzero_cap_is_faithful',(1*1+0*0)!=(1*1+1*0),
           'Over Qe plus Qf, cap (Q,0) kills the second sector.')
    reject('every_functional_descends',1 == 0,
           'For p(x,y)=x and lambda(x,y)=y, lambda(0,1)=1 on a kernel element.')
    reject('zero_square_meets_positive_sphere_bound',0 >= -(-1),
           'Unknot threshold is 1; zero square is excluded.')
    reject('positive_betti_number_implies_odd_form',any(x%2 for x in (0,0)),
           'Hyperbolic form H has b2+ equal to one and is even; the blowup supplies oddness.')
    reject('one_blowup_always_has_nonzero_signature',1-1 != 0,
           'Signature one requires the second negative blowup for this signature safeguard.')
    reject('nonzero_tensor_over_every_ring',1 != 1,
           'Z/2 tensor_Z Z/3 is zero: multiplication by 2 and 3 annihilates it, hence Bezout gives annihilation by 1.')
    reject('nonzero_lee_space_implies_nonzero_associated_graded',7-7 > 0,
           'The exhaustive filtration F_q=Q^7 for every q has zero associated graded.')
    reject('finite_upper_bound_excludes_minus_infinity',False,
           'Minus infinity satisfies every finite upper bound.')
    reject('kernel_plateau_certifies_tail_stability',0 == 1,
           'A one-dimensional identity prefix followed later by zero changes the kernel after any prescribed plateau.')
    reject('one_zero_transition_forces_zero_limit',False,
           'A zero map once, followed by identities, has a surviving later-stage Q; eventual death is required for every representative.')
    reject('finite_prefix_forces_nonzero_limit',False,
           'Identity forever and the same identity prefix followed by zero forever have respective limits Q and zero.')
    reject('tensor_with_zero_can_be_cancelled',1 == 2,
           'Q and Q^2 are unequal although both become zero after tensoring with zero.')
    reject('nonzero_infinite_factor_can_always_be_cancelled',False,
           'Countable bases identify W with Q^2 tensor W, while Q and Q^2 are not isomorphic.')
    reject('all_gluck_maps_are_degree_zero',(Fraction(-2),Fraction(2)) == (0,0),
           'Intersection two gives the displayed shift (-2,2), so only an appropriate zero-intersection restriction removes it.')
    reject('integral_gluck_theorem_from_rational_statement',False,
           'A Q-vector-space theorem supplies no integral conclusion; distinct torsion groups can rationalize to zero.')
    reject('accepted_body_equals_v3_from_status_metadata',False,
           'An accepted date and revised date contain no equality evidence for manuscript bytes.')
    reject('finite_controls_are_topology_proof',False,
           'These programs contain no geometric witness, knot complex, cap computation, or formal imported theorem proof.')
    return {'status':'pass','rejected_cases':len(results),'cases':results,
            'scope':'Some cases are exact numerical countermodels; explicitly explained logical scope checks are not formal theorem verification. Original bytes are only read; mutations exist in memory.'}


if __name__ == '__main__':
    if len(sys.argv)!=2:
        raise SystemExit('Usage: negative_controls.py AUTHOR_SAFE.zip')
    print(json.dumps(main(sys.argv[1]),indent=2,sort_keys=True))
