#!/usr/bin/env python3
"""Independent exact finite audit controls; not a theorem or novelty verifier."""
from fractions import Fraction as Q
from math import gcd
from pathlib import Path
import hashlib, json, runpy, sys

EXPECTED_MANIFEST = '63df37afcb5592e0bde27cf8e66383025710e5fcc685d38afb954a37275d48b8'

def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def winding(poly, p):
    """Exact signed ray-crossing winding of a polygon about a nonboundary point."""
    total = 0
    for a,b in zip(poly,poly[1:]+poly[:1]):
        side=cross(a,b,p)
        if side==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1]):
            raise ValueError('point is on polygon')
        if a[1]<=p[1]<b[1] and side>0: total+=1
        if b[1]<=p[1]<a[1] and side<0: total-=1
    return total

def box(x0,y0,x1,y1):
    return [(Q(x0),Q(y0)),(Q(x1),Q(y0)),(Q(x1),Q(y1)),(Q(x0),Q(y1))]

def subdivide(poly):
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        out.extend([a,((2*a[0]+b[0])/3,(2*a[1]+b[1])/3)])
    return out[3:]+out[:3]

def run(submission):
    checks={}
    manifest_bytes=(submission/'SHA256SUMS.json').read_bytes()
    assert hashlib.sha256(manifest_bytes).hexdigest()==EXPECTED_MANIFEST
    records=json.loads(manifest_bytes)['files']
    actual={str(p.relative_to(submission)) for p in submission.rglob('*') if p.is_file() and p.name!='SHA256SUMS.json' and '__pycache__' not in p.parts}
    assert actual==set(records)
    for name,r in records.items():
        b=(submission/name).read_bytes()
        assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
    checks['bound_author_manifest_sha256']=EXPECTED_MANIFEST
    checks['author_files_verified']=len(records)
    result=runpy.run_path(str(submission/'verify.py'))['run']()
    assert result==json.loads((submission/'CONTROL_RESULTS.json').read_text())
    checks['author_control_replay_exact_equality']=True

    outer=box(-6,-6,6,6)
    h1=box(-4,-1,-2,1)[::-1]
    h2=box(2,-1,4,1)[::-1]
    loops=[outer,h1,h2]
    tests=0
    for xi in range(-15,16,2):
        for yi in range(-15,16,2):
            p=(Q(xi,2),Q(yi,2))
            inside=(-6<p[0]<6 and -6<p[1]<6 and not (-4<p[0]<-2 and -1<p[1]<1) and not (2<p[0]<4 and -1<p[1]<1))
            assert sum(winding(g,p) for g in loops)==int(inside)
            for g in loops:
                assert winding(subdivide(g),p)==winding(g,p)
                assert winding(g[::-1],p)==-winding(g,p)
            tests+=1
    checks['exact_three_boundary_region_grid_cases']=tests
    checks['orientation_preserving_reparametrization_cases']=tests*3
    checks['orientation_reversal_cases']=tests*3
    assert sum(winding(g,(Q(-3),Q(0))) for g in [outer,h1[::-1],h2])==2
    assert sum(winding(g,(Q(3),Q(0))) for g in [outer,h1,h2[::-1]])==2
    checks['wrong_hole_orientation_mutations_detected']=2

    # Factorization audit: roots/poles outside U, including inside its holes, contribute zero.
    zeros=[((Q(0),Q(0)),2),((Q(-3),Q(0)),7),((Q(8),Q(0)),11)]
    poles=[((Q(4),Q(3)),1),((Q(3),Q(0)),5),((Q(9),Q(0)),13)]
    product_index=sum(m*sum(winding(g,z) for g in loops) for z,m in zeros)-sum(m*sum(winding(g,z) for g in loops) for z,m in poles)
    assert product_index==2-1
    checks['rational_factorization_signed_index']=product_index
    checks['hole_root_and_pole_contributions_vanish']=True

    # Derive circle angular derivative independently of the author's polynomial dictionary.
    # For B=z^2(z-3)/(1-3z), logarithmic derivative on |z|=1 is
    # 2-8/(10-6*cos(t)) = 12*(1-cos(t))/(10-6*cos(t)).
    for k in range(-50,51):
        c=Q(k,50)
        lhs=2-Q(8)/(10-6*c)
        rhs=12*(1-c)/(10-6*c)
        assert lhs==rhs and rhs>=0 and (rhs==0)==(c==1)
    checks['critical_blaschke_monotonicity_identity_cases']=101
    # Local expansion at the smooth circle's critical point: B(1)=1 and B-1=(z-1)^3/(1-3z).
    # Coefficients in ascending order, checked without importing author's arithmetic.
    p=[0,0,-3,1]; q=[1,-3,0,0]
    assert sum(p)==sum(q)==-2
    assert [a-b for a,b in zip(p,q)]==[-1,3,-3,1]  # (z-1)^3
    assert [a+b for a,b in zip(p,q)]!=[-1,3,-3,1]
    checks['critical_blaschke_local_degree_at_one']=3

    resonance=0
    for lam in [Q(2),Q(3,2),Q(1,3)]:
        allowed=[k for k in range(-20,21) if lam**k==lam]
        assert allowed==[1]
        resonance+=41
    checks['nonunit_positive_multiplier_laurent_cases']=resonance
    d=3; L=1
    for p in [2,3,5]: L=L*p//gcd(L,p)
    assert L==30 and d**L-1==205891132094648
    checks['independent_period_lcm_control']={'d':d,'periods':[2,3,5],'L':L,'iterate_degree':d**L,'bound':d**L-1,'degree_only':False}
    return {'result':'PASS','limits':'Finite exact controls only. Mathematical validity rests on the written audit. No novelty, unrestricted-period, or analytic-existence certification.','checks':checks}

if __name__=='__main__':
    p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'submission'
    print(json.dumps(run(p),indent=2,sort_keys=True))
