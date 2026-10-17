"""Independent arithmetic/finite checks of the proved periodic family.
This does not search for a general winning strategy or prove forceability
of the preload history against an uncooperative Angel.
"""
from itertools import product
from fractions import Fraction
from pathlib import Path
import json

out=[]
for k in (2,3,5):
    m=12*k
    N=8*m*m
    H=N+k-1
    B={(x,y) for x,y in product(range(3*m),repeat=2)
       if not (x%3==0 and y%3==0)}
    assert len(B)==N
    checked=0
    for q in product(range(1,3*m-1),repeat=2):
        holes=[(q[0]+dx,q[1]+dy) for dx,dy in product((-1,0,1),repeat=2)
               if (q[0]+dx,q[1]+dy) not in B]
        assert len(holes)==1
        checked+=1
    for j in range(1,H+1):
        count=N if j<=k else 0
        assert count<=H-j+1
    lower=(3*m-2*k)**2
    assert Fraction(lower,N)==Fraction(289,288)>1
    assert 3*m-1<=N
    assert (N+k)-1==H
    out.append({'k':k,'m':m,'bombs':N,'max_lead':H,
                'verified_penultimate_centers':checked,
                'losing_center_lower_bound':lower,
                'amplification_lower_bound':'289/288'})
p=Path(__file__).with_name('MASS_FAMILY_CHECK.json')
p.write_text(json.dumps({'status':'passed','examples':out},indent=2)+'\n')
print(p.read_text())
