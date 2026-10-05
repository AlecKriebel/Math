#!/usr/bin/env python3
"""Independent exact regressions; imports no author code. Not a proof checker."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent

def norm(a, b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))

def path4(a, b, j):
    """Integer coordinates of 4*S(a,b,j/4), for integer input points."""
    return ((4-j)*a[0]+j*b[0], max((4-j)*a[1]+j*b[1], min(j,4-j)*abs(b[0]-a[0])))

def curve(a, b, t):
    t = Q(t)
    x = a[0] + t*(b[0]-a[0])
    h = a[1] + t*(b[1]-a[1])
    roof = abs(b[0]-a[0])*(t if t <= Q(1,2) else 1-t)
    return (x, h if h >= roof else roof)

def mid(a, b):
    return curve(a,b,Q(1,2))

def upper_hull_mesh(a, b, n):
    """Solve this particular tent model by a concave-envelope algorithm."""
    if n == 1:
        return [a,b]
    floor = abs(b[0]-a[0])/Q(n)
    vertices = [(0,a[1])] + [(i,floor) for i in range(1,n)] + [(n,b[1])]
    hull=[]
    for z in vertices:
        hull.append(z)
        while len(hull)>=3:
            r,s,t=hull[-3:]
            left=(s[1]-r[1])/Q(s[0]-r[0])
            right=(t[1]-s[1])/Q(t[0]-s[0])
            if left>=right:
                break
            hull.pop(-2)
    heights={}
    for r,s in zip(hull,hull[1:]):
        for i in range(r[0],s[0]+1):
            heights[i]=r[1]+Q(i-r[0],s[0]-r[0])*(s[1]-r[1])
    return [(a[0]+Q(i,n)*(b[0]-a[0]),heights[i]) for i in range(n+1)]

def value(mesh,t):
    n=len(mesh)-1
    if t==1:
        return mesh[-1]
    j=int(n*t)
    return curve(mesh[j],mesh[j+1],n*t-j)

def update(mesh):
    return [mesh[0]]+[mid(mesh[i-1],mesh[i+1]) for i in range(1,len(mesh)-1)]+[mesh[-1]]

def metric(mesh,other):
    n=len(mesh)-1
    return max(norm(mesh[i],other[i])/Q(i*(n-i)) for i in range(1,n))

def run():
    counts={}
    grid=list(product(range(-2,3),range(3)))
    cache={(a,b,j):path4(a,b,j) for a,b in product(grid,repeat=2) for j in range(5)}
    for a,b,c,d in product(grid,repeat=4):
        for j in range(5):
            assert norm(cache[a,b,j],cache[c,d,j]) <= (4-j)*norm(a,c)+j*norm(b,d)
    counts['conical_inequalities']=len(grid)**4*5
    for a,b in product(grid,repeat=2):
        for i,j in product(range(5),repeat=2):
            assert norm(cache[a,b,i],cache[a,b,j])==abs(i-j)*norm(a,b)
        for j in range(5):
            assert cache[a,b,j]==cache[b,a,4-j]
    counts['geodesic_equalities']=len(grid)**2*25
    counts['reversal_equalities']=len(grid)**2*5
    a,b=(Q(-1),Q(0)),(Q(1),Q(0))
    v,w=curve(a,b,Q(1,4)),curve(a,b,Q(3,4))
    assert mid(a,b)==(0,1) and mid(v,w)==(0,Q(1,2))
    dyadic=[a,b]
    for level in range(1,11):
        refined=[]
        for p,q in zip(dyadic,dyadic[1:]):
            refined.extend([p,mid(p,q)])
        dyadic=refined+[b]
        assert dyadic[2**(level-1)]==(0,1)
        if level>=2:
            assert dyadic[2**(level-2)]==v
            assert dyadic[3*2**(level-2)]==w
    counts['dyadic_refinement_levels']=10
    p=q=(Q(-2),Q(0));r=(Q(-2),Q(1));s=(Q(-1),Q(0))
    lhs,rhs=mid(mid(p,q),mid(r,s)),mid(mid(p,r),mid(q,s))
    assert lhs==(Q(-7,4),Q(1,4)) and rhs==(Q(-7,4),Q(1,2))
    weights=0
    for n in range(2,101):
        rho=1-Q(1,n*n//4)
        assert 0<=rho<1
        for i in range(1,n):
            wi=i*(n-i)
            neighbours=(i-1)*(n-i+1)+(i+1)*(n-i-1)
            assert neighbours==2*(wi-1)
            assert Q(neighbours,2*wi)<=rho
            weights+=1
    counts['parabolic_weight_checks']=weights
    pairs=interpolations=0
    for n in range(2,33):
        mesh=upper_hull_mesh(a,b,n)
        assert update(mesh)==mesh
        assert all(mesh[i]==(-1+Q(2*i,n),Q(2,n)) for i in range(1,n))
        for i,j in product(range(n+1),repeat=2):
            assert norm(mesh[i],mesh[j])==Q(2*abs(i-j),n)
            pairs+=1
        for j in range(65):
            t=Q(j,64)
            assert value(mesh,t)==(-1+2*t,2*min(t,Q(1,n),1-t))
            interpolations+=1
    counts['fixed_mesh_pairwise_distances']=pairs
    counts['closed_form_interpolation_values']=interpolations
    assert value(upper_hull_mesh(a,b,2),Q(1,2))==(0,1)
    assert value(upper_hull_mesh(a,b,4),Q(1,2))==(0,Q(1,2))
    contractions=errors=0
    for n in range(2,21):
        p=[a]+[(Q(i%5-2),Q(i%3)) for i in range(1,n)]+[b]
        q=[a]+[(Q((2*i)%7-3),Q((i+1)%4)) for i in range(1,n)]+[b]
        rho=1-Q(1,n*n//4)
        assert metric(update(p),update(q))<=rho*metric(p,q)
        contractions+=1
        fixed=upper_hull_mesh(a,b,n)
        initial_residual=metric(update(p),p)
        for k in range(13):
            assert metric(p,fixed)<=rho**k/(1-rho)*initial_residual
            p=update(p)
            errors+=1
    counts['product_contraction_checks']=contractions
    counts['a_posteriori_iteration_bounds']=errors
    model_points=[(Q(-2),Q(0)),(Q(-1),Q(2)),(Q(0),Q(1,3)),(Q(2),Q(0)),(Q(3),Q(4))]
    fixed=blocks=blockvalues=0
    for a,b in product(model_points,repeat=2):
        for n in range(1,13):
            mesh=upper_hull_mesh(a,b,n)
            assert update(mesh)==mesh
            fixed+=1
            for i in range(n):
                for j in range(i+1,n+1):
                    small=upper_hull_mesh(mesh[i],mesh[j],j-i)
                    assert small==mesh[i:j+1]
                    blocks+=1
                    for u in [Q(0),Q(1,3),Q(1,2),Q(1)]:
                        assert value(mesh,Q(i,n)+Q(j-i,n)*u)==value(small,u)
                        blockvalues+=1
    counts['arbitrary_endpoint_model_fixed_meshes']=fixed
    counts['contiguous_block_string_equalities']=blocks
    counts['cross_mesh_interpolation_equalities']=blockvalues
    n=20;i=10
    ratio=Q((i-1)*(n-i+1)+(i+1)*(n-i-1),2*i*(n-i))
    assert ratio==Q(99,100)>Q(9,10)
    # Independent positive medial model: arithmetic averaging on rational pairs.
    average=lambda x,y:tuple((r+s)/2 for r,s in zip(x,y))
    for a,b,c,d in product(model_points,repeat=4):
        assert average(average(a,b),average(c,d))==average(average(a,c),average(b,d))
    counts['medial_positive_control_quadruples']=len(model_points)**4
    return {'status':'PASS','problem_id':30004730,'implementation':'Independent scaled-integer conical grid and rational concave-envelope model; no author imports.','counts':counts,'exact_witnesses':{'dyadic_consistency_defect':'1/2','medial_defect':'1/4','two_mesh_midpoint_height':'1','four_mesh_midpoint_height':'1/2','n20_weight_ratio':'99/100'},'scope':'Finite exact regressions support, but do not replace, universal proofs. No infinite-mesh convergence or general solution is asserted.'}

def verify_manifest():
    m=json.loads((HERE/'AUDIT_MANIFEST.json').read_text())
    expected={r['path'] for r in m['files']}
    actual={p.name for p in HERE.iterdir() if p.is_file() and p.name!='AUDIT_MANIFEST.json'}
    assert actual==expected
    for r in m['files']:
        data=(HERE/r['path']).read_bytes()
        assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
    return len(expected)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-results',action='store_true')
    args=parser.parse_args()
    results=run()
    if args.write_results:
        (HERE/'independent_results.json').write_text(json.dumps(results,indent=2)+'\n')
    else:
        assert results==json.loads((HERE/'independent_results.json').read_text())
        results={'status':'PASS','manifest_files':verify_manifest(),'independent_checks':results}
    print(json.dumps(results,indent=2))
