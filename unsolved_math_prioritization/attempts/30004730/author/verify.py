#!/usr/bin/env python3
"""Exact finite regression checks for REPORT.md; not a formal proof checker."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent

def distance(x, y):
    return max(abs(a-b) for a,b in zip(x,y))

def tent(x, y, t):
    return ((1-t)*x[0]+t*y[0],
            max((1-t)*x[1]+t*y[1], min(t,1-t)*abs(y[0]-x[0])))

def midpoint(x,y):
    return tent(x,y,F(1,2))

def mesh(x,y,n):
    # Closed form is asserted only for these endpoints, not arbitrary inputs.
    assert x == (F(-1),F(0)) and y == (F(1),F(0)) and n>=2
    return [x]+[(F(-1)+F(2*i,n),F(2,n)) for i in range(1,n)]+[y]

def interpolate(points,t):
    n=len(points)-1
    if t==1:return points[-1]
    scaled=n*t;i=scaled.numerator//scaled.denominator
    return tent(points[i],points[i+1],scaled-i)

def weighted_distance(p,q):
    assert len(p)==len(q)
    n=len(p)-1
    return max(distance(p[i],q[i])/F(i*(n-i)) for i in range(1,n))

def step(points):
    return [points[0]]+[midpoint(points[i-1],points[i+1])
                            for i in range(1,len(points)-1)]+[points[-1]]

def run_checks():
    counts={}
    points=[(F(a),F(b)) for a in range(-2,3) for b in range(3)]
    times=[F(i,4) for i in range(5)]
    count=0
    for x,y in product(points,repeat=2):
        assert tent(x,y,0)==x and tent(x,y,1)==y
        for s,t in product(times,repeat=2):
            assert distance(tent(x,y,s),tent(x,y,t))==abs(s-t)*distance(x,y)
            count+=1
        for t in times:assert tent(x,y,t)==tent(y,x,1-t)
    counts['geodesic_equalities']=count
    counts['reversal_equalities']=len(points)**2*len(times)
    count=0
    for x,y,u,v in product(points,repeat=4):
        for t in times:
            assert distance(tent(x,y,t),tent(u,v,t))<=(1-t)*distance(x,u)+t*distance(y,v)
            count+=1
    counts['conical_inequalities']=count
    x,y=(F(-1),F(0)),(F(1),F(0))
    p,q=tent(x,y,F(1,4)),tent(x,y,F(3,4))
    assert p==(F(-1,2),F(1,2)) and q==(F(1,2),F(1,2))
    assert distance(midpoint(p,q),midpoint(x,y))==F(1,2)
    # A midpoint-insertion construction retains these values forever.
    arr=[x,y]
    for depth in range(1,7):
        arr=[z for i in range(len(arr)-1) for z in (arr[i],midpoint(arr[i],arr[i+1]))]+[arr[-1]]
        assert arr[2**(depth-1)]==(F(0),F(1))
        if depth>=2:
            assert arr[2**(depth-2)]==p
            assert arr[3*2**(depth-2)]==q
    a=b=(F(-2),F(0));c=(F(-2),F(1));d=(F(-1),F(0))
    lhs=midpoint(midpoint(a,b),midpoint(c,d))
    rhs=midpoint(midpoint(a,c),midpoint(b,d))
    assert lhs==(F(-7,4),F(1,4)) and rhs==(F(-7,4),F(1,2))
    count=0
    for n in range(2,101):
        M=(n*n)//4;q_bound=1-F(1,M)
        assert 0<=q_bound<1
        weights=[F(i*(n-i)) for i in range(n+1)]
        for i in range(1,n):
            assert (weights[i-1]+weights[i+1])/2==weights[i]-1
            assert (weights[i-1]+weights[i+1])/(2*weights[i])<=q_bound
            count+=1
    counts['weight_identities_and_contraction_bounds']=count
    count=0
    for n in range(2,33):
        ps=mesh(x,y,n)
        assert step(ps)==ps
        for i,j in product(range(n+1),repeat=2):
            assert distance(ps[i],ps[j])==F(2*abs(i-j),n)
            count+=1
        for t in [F(i,64) for i in range(65)]:
            assert interpolate(ps,t)==(-1+2*t,2*min(t,F(1,n),1-t))
        assert interpolate(ps,F(1,2))[1]==F(2,n)
    counts['fixed_mesh_pairwise_distances']=count
    counts['closed_form_interpolation_values']=31*65
    assert interpolate(mesh(x,y,2),F(1,2))!=(interpolate(mesh(x,y,4),F(1,2)))
    for n in range(2,21):
        p0=[x]+[(F(i%5-2),F(i%3)) for i in range(1,n)]+[y]
        p1=[x]+[(F((2*i)%7-3),F((i+1)%4)) for i in range(1,n)]+[y]
        qb=1-F(1,(n*n)//4)
        assert weighted_distance(step(p0),step(p1))<=qb*weighted_distance(p0,p1)
    counts['explicit_product_contraction_checks']=19
    # Rational model of the squared Hilbert distances between basis vectors.
    assert all(sum((int(k==i)-int(k==j))**2 for k in range(8))==2
               for i in range(8) for j in range(8) if i!=j)
    # A falsely uniform 0.9 contraction coefficient fails for parabolic weights.
    n=20;i=10;w=lambda j:F(j*(n-j))
    assert (w(i-1)+w(i+1))/(2*w(i))>F(9,10)
    return {
      'status':'PASS', 'arithmetic':'Python fractions.Fraction; exact integer/rational checks',
      'problem_id':30004730,'counts':counts,
      'consistency_defect':'1/2','medial_defect':'1/4',
      'two_mesh_midpoint_height':'1','four_mesh_midpoint_height':'1/2',
      'negative_controls':[
        'Automatic consistency of symmetric conical dyadic subdivision rejected.',
        'Invariance of earlier midpoint under finite harmonic mesh refinement rejected.',
        'Medial identity as a consequence of symmetry and conicality rejected.',
        'Mesh-independent 0.9 bound from the parabolic weighted metric rejected.'
      ],
      'limits':'Finite checks do not prove universal metric statements, global convergence, or open-problem resolution. Written proofs are in REPORT.md.'
    }

def check_manifest():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    expected={x['path'] for x in manifest['files']}
    actual={p.name for p in ROOT.iterdir() if p.is_file() and p.name!='MANIFEST.json'}
    assert actual==expected,('payload names differ',actual,expected)
    for item in manifest['files']:
        assert '/' not in item['path'] and '\\' not in item['path']
        p=ROOT/item['path'];b=p.read_bytes()
        assert len(b)==item['bytes'],item['path']
        assert hashlib.sha256(b).hexdigest()==item['sha256'],item['path']
    return len(expected)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-results',action='store_true',help='Author mode: write deterministic finite-check results before freezing.')
    args=parser.parse_args()
    results=run_checks()
    if args.write_results:
        (ROOT/'verification_results.json').write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps(results,indent=2));return
    assert results==json.loads((ROOT/'verification_results.json').read_text())
    count=check_manifest()
    print(json.dumps({'status':'PASS','manifest_files':count,'finite_checks':results},indent=2))

if __name__=='__main__':main()
