#!/usr/bin/env python3
"""Exact independent-of-CAT(0) finite checks supporting the sign lemma."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from datetime import datetime, timezone
import json,hashlib

def construct(p,q):
    for i in range(2):
        if bool(p[i])==bool(q[i]):
            a,b=(q[i],p[i]) if p[i] else (F(1),F(1))
            j=1-i;c=-(p[j]*a+q[j]*b)/2
            signs=[-1,-1];signs[i]=1
            return a,b,c,signs
    dp,dq=p[0]-p[1],q[0]-q[1]
    if bool(dp)==bool(dq):
        a,b=(dq,-dp) if dp else (F(1),F(1))
        c=-(p[0]*a+q[0]*b)/2
        return a,b,c,[-1,-1]
    return None

def det3(m):
    return sum(m[0][i]*(m[1][(i+1)%3]*m[2][(i+2)%3]-m[1][(i+2)%3]*m[2][(i+1)%3]) for i in range(3))

def run():
    vals=[F(i,j) for j in range(1,4) for i in range(-3,4)]
    vals=sorted(set(vals));count=exceptional=0
    for p1,p2,q1,q2 in product(vals,repeat=4):
        p,q=[p1,p2],[q1,q2]
        exc=(p1==p2==0 and len({F(0),q1,q2})==3) or (q1==q2==0 and len({F(0),p1,p2})==3)
        r=construct(p,q)
        assert (r is None)==exc,(p,q,r,exc)
        if r:
            a,b,c,signs=r
            assert a and b
            for pi,qi,s in zip(p,q,signs):assert pi*a+c==s*(qi*b+c)
        count+=1;exceptional+=exc
    pell=[(3,2),(20,14),(119,84)]
    assert all(p*(p+1)==2*q*(q+1) for p,q in pell)
    determinants=[]
    for signs in product([-1,1],repeat=3):
        d=det3([[p,-s*q,1-s] for (p,q),s in zip(pell,signs)])
        assert (d==0)==(signs==(1,1,1))
        determinants.append({'signs':signs,'determinant':d})
    assert pell[0][0]*pell[1][1]-pell[1][0]*pell[0][1] !=0
    return {'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS','rational_values':len(vals),'sign_lemma_grid_cases':count,'exceptional_cases':exceptional,'pell_pairs':pell,'pell_sign_determinants':determinants,'scope':'Finite exact checks supplement the written general proof. No arbitrary finite-holonomy obstruction or full Kourovka solution is claimed.'}

if __name__=='__main__':
    result=run();path=Path(__file__).with_name('theta_certificate.json');path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
