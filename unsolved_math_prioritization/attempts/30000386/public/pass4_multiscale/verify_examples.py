#!/usr/bin/env python3
"""Exact checks of examples, not a search for a full-game Devil strategy."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from hashlib import sha256
import json

N=set(product((-1,0,1),repeat=2));origin=(0,0)
ring=sorted(N-{origin})
announcements=[]
for r,p in enumerate(ring,1):announcements.append((r,p,18))
for r,p in enumerate(ring,9):announcements.append((r,p,17))
assert len({r for r,p,t in announcements})==16
assert all(1<=t-r<=17 for r,p,t in announcements)
assert {t-r for r,p,t in announcements[:8]}==set(range(10,18))
assert {t-r for r,p,t in announcements[8:]}==set(range(1,9))
assert all(t>16 for r,p,t in announcements)
A={p for r,p,t in announcements if t==17}
B={p for r,p,t in announcements if t==18}
immediate=N-A
assert immediate=={origin}
hood=lambda p:{(p[0]+x,p[1]+y)for x,y in N}
guard={p for p in N if len(B&hood(p))<=7}
assert origin not in guard and guard
assert not immediate&guard
B.add(origin)
assert B==N

# Uniform-radius equal-block expression: exact arithmetic spot checks
# supplement the symbolic all-L inequality in REPORT.md.
for L in range(1,10001):
    M=L//4
    radius_square_lower_bound=2*L
    expression=L*min(Q(1),Q(radius_square_lower_bound,(2*M+1)**2))
    assert expression>=1
    if L>=2:assert expression>=2
assert 141**2<2*100**2<=142**2

here=Path(__file__).parent
receipt={
 'status':'PASS',
 'scope':'Exact example and algebra spot checks; no full-game losing claim',
 'two_class_history':{'preload_announcements':16,'maximum_lead':17,
     'safe_stay_moves_through':16,'only_safe_move_17':[0,0],
     'boundary_announcement':{'round':17,'position':[0,0],'target_time':18},
     'all_nine_move_18_destinations_bombed':True,
     'meaning':'Reachable under the specified stay-put path, not forced against every Angel'},
 'block_union_expression_checked_for_L':10000,
 'minimum_rounds_to_interpolate_every_king_step_at_speed_1_over_100':142,
 'report_sha256':sha256((here/'REPORT.md').read_bytes()).hexdigest(),
}
(here/'EXAMPLE_CHECKS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
