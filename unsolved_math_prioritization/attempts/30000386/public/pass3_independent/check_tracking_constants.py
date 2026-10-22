"""Exact finite certificates for the directional rank and charge inequalities.
The analytic radial and probabilistic arguments remain in the proof files.
"""
from fractions import Fraction as F
import json
from pathlib import Path

D=[F(0),F(1,2),F(2,3),F(1),F(1),F(4,3),F(2),F(2),F(2)]
# All changes in sorted order occur at a=1/2, 2/3, 1 for direction(a,1-a).
# Each rank is affine between these breakpoints, so endpoint extrema suffice.
actual=[F(0) for _ in range(9)]
for a in [F(1,2), F(2,3), F(1)]:
    b=1-a
    vals=sorted([a*x+b*y for x in [-1,0,1] for y in [-1,0,1]], reverse=True)
    for k,v in enumerate(vals):
        actual[k]=max(actual[k],1-v)
assert actual==D
for k in range(9):
    assert D[k] <= F(k,2)
    assert D[k] <= F(2*(k+7),13)
count=0
for m in range(9):
    for b in range(16-m):
        for r in range(max(0,b-7)+1):
            k=m+r
            assert k<=8
            assert D[k] <= F(m,2)+F(2*b,13)
            count+=1
# C=17 sqrt(2)/26<93/100, checked without floating arithmetic.
assert F(17*17*2,26*26) < F(93*93,100*100)
assert F(62)+15*F(93,100) < 76
# 59.99-sqrt(2)>50 since 9.99>sqrt(2).
assert F(999,100)**2>2
assert F(100*161**2,3000000)==F(25921,30000)<1
out={"status":"passed", "rank_losses":[str(x) for x in D],
     "integer_guard_charge_cases":count,
     "tracking_speed":"1/100", "conservative_tracking_radius":80,
     "long_collision_union_bound_strict_upper":"25921/30000",
     "survival_probability_strict_lower":"4079/30000"}
Path(__file__).with_name('TRACKING_CONSTANTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
