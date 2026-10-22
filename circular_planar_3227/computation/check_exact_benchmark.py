"""Check matching graph inputs, both certificates, and the finite rational gap.

The mathematical connection is proved in exact_dodecahedron_value.md.
"""
import json
import os
from fractions import Fraction
from verify_certificate import verify as verify_sat
from verify_unsat_certificate import verify as verify_unsat
base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, 'dodecahedron_20_7.json')) as f:
    sat = json.load(f)
with open(os.path.join(base, 'dodecahedron_17_6_unsat.json')) as f:
    unsat = json.load(f)
if sat['vertices'] != unsat['vertices'] or {frozenset(e) for e in sat['edges']} != {frozenset(e) for e in unsat['edges']}:
    raise ValueError('Certificates describe different graphs')
if (sat['p'],sat['q']) != (20,7) or (unsat['p'],unsat['q']) != (17,6) or len(sat['vertices']) != 20:
    raise ValueError('Unexpected targets or graph size')
print(verify_sat(sat))
print(verify_unsat(unsat))
values = [Fraction(k,q) for k in range(2,21) for q in range(1,k//2+1)]
if max(r for r in values if r < Fraction(20,7)) != Fraction(17,6):
    raise ValueError('Incorrect rational gap')
print('PASS: same edge-list graph; K20/7 SAT, K17/6 UNSAT, numerator-gap check.')
print('Together with the written tight-cycle and rounding lemmas: chi_c = 20/7.')
