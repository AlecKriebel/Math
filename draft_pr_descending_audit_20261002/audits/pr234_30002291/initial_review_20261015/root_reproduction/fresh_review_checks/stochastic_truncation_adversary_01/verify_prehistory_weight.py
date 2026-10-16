#!/usr/bin/env python3
"""Exact arithmetic supplement to the review, not a stochastic theorem test.

For rectangle indicators h=1_[a,b], compare the two independently integrated
regions in integral_0^T integral_0^infinity h(u+r) dr du.
The general identity follows analytically by Tonelli and x=u+r; this check
covers zero, corner, and relative-order cases without floating point.
"""
from fractions import Fraction as Q
from pathlib import Path
import datetime, hashlib, json

def lhs(T, a, b):
    # Integrate in r first after writing the u-section's exact interval length.
    knots = sorted({Q(0), b, max(Q(0), a), max(Q(0), a-T), max(Q(0), b-T)})
    def length(r):
        return max(Q(0), min(T,b-r)-max(Q(0),a-r))
    return sum((y-x)*(length(x)+length(y))/2 for x,y in zip(knots,knots[1:]))

def rhs(T,a,b):
    # Integrate min(x,T) directly in x, splitting at T.
    c=min(b,max(a,T))
    return (c*c-a*a)/2 + T*(b-c)

vals=[Q(i,4) for i in range(17)]
count=0
for T in vals[1:]:
    for a in vals:
        for b in vals:
            if b<a: continue
            assert lhs(T,a,b)==rhs(T,a,b), (T,a,b,lhs(T,a,b),rhs(T,a,b))
            count+=1
root=Path(__file__).resolve().parent
proof=root.parent/'submitted/unsolved_math_prioritization/attempts/30002291/PROOF.md'
expected='508f71b81ee669d4934ef1cc9e061c129e47d36359896ad7b3e20574dbfbc539'
actual=hashlib.sha256(proof.read_bytes()).hexdigest()
assert actual==expected
receipt={
 'executed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'PASS',
 'exact_rational_rectangle_cases':count,
 'verified_identity':'int_0^T int_0^infty h(u+r) dr du = int_0^infty min(x,T) h(x) dx',
 'proof_sha256':actual,
 'proof_matches_frozen_manifest':actual==expected,
 'scope':'Exact deterministic geometry and frozen-input integrity only; stochastic justifications are analytic in REPORT.md.',
 'simulation_used':False,
}
(root/'INDEPENDENT_CHECK_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
