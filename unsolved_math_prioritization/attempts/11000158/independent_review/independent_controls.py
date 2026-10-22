#!/usr/bin/env python3
"""Independent convention controls. These do not certify 3-manifold topology."""
from itertools import product
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent
PACKET = ROOT.parent / 'boundary_three_manifolds_11000158' / 'public'
P = 5
I = (1, 0, 0, 1)

def mm(x, y):
    a,b,c,d=x; e,f,g,h=y
    return ((a*e+b*g)%P,(a*f+b*h)%P,(c*e+d*g)%P,(c*f+d*h)%P)

def det(x):
    a,b,c,d=x
    return (a*d-b*c)%P

def inv(x):
    a,b,c,d=x; q=pow(det(x),-1,P)
    return ((q*d)%P,(-q*b)%P,(-q*c)%P,(q*a)%P)

def double_orbit(L,x,R):
    return {mm(mm(l,x),inv(r)) for l in L for r in R}

def coset_count(G,L,R):
    unseen=set(G); count=0
    while unseen:
        unseen-=double_orbit(L,next(iter(unseen)),R)
        count+=1
    return count

def compose(p,q): return tuple(p[q[i]] for i in range(len(p)))
def pinv(p): return tuple(p.index(i) for i in range(len(p)))
def comm(p,q): return compose(compose(compose(p,q),pinv(p)),pinv(q))

def main():
    # A genuine determinant-minus-one torsor, rather than using one ungraded group.
    G={x for x in product(range(P),repeat=4) if det(x)==1}
    T={x for x in product(range(P),repeat=4) if det(x)==P-1}
    assert len(G)==len(T)==120
    L={x for x in G if x[2]==0}
    rotation=(0,P-1,1,0)
    R={I,rotation,mm(rotation,rotation),inv(rotation)}
    j=(0,1,1,0)
    assert det(j)==P-1
    JLj={mm(mm(inv(j),l),j) for l in L}
    omitted=swapped=0
    relation_checks=0
    for phi in G:
        alpha=mm(j,phi)
        direct=double_orbit(L,alpha,R)
        translated={mm(inv(j),a) for a in direct}
        assert translated==double_orbit(JLj,phi,R)
        # Check pointwise compatibility alpha2*r = l*alpha, in both directions.
        compatible={mm(mm(l,alpha),inv(r)) for l in L for r in R}
        for phi2 in G:
            assert (phi2 in translated)==(mm(j,phi2) in compatible)
            relation_checks+=1
        # Reversing the gluing direction exchanges factors and inverts maps.
        assert {inv(a) for a in direct}==double_orbit(R,inv(alpha),L)
        omitted+=translated!=double_orbit(L,phi,R)
        swapped+=translated!=double_orbit(R,phi,JLj)
    assert omitted and swapped
    # Product-body full, pointwise-relative and slope-marked groups differ.
    quotients={
        'unmarked_product_left_group_G':coset_count(G,G,L),
        'relative_product_left_group_identity':coset_count(G,{I},L),
        'slope_marked_left_group_L':coset_count(G,L,L),
    }
    assert quotients=={
        'unmarked_product_left_group_G':1,
        'relative_product_left_group_identity':6,
        'slope_marked_left_group_L':2,
    }
    # Integral torus witnesses: preserving the exterior solid-torus meridian
    # need not preserve the selected meridian of the solid torus used to fill.
    twist=(1,1,0,1)
    assert twist[2]==0 and twist[1]!=0
    swap=(0,-1,1,0)
    assert swap[2]!=0
    # Homology alone cannot retain separating compression data. A genus-two
    # surface representation with c=b,d=a has [a,b][c,d]=1 but [a,b]!=1.
    a=(1,0,2);b=(0,2,1);one=(0,1,2)
    assert comm(a,b)!=one
    assert compose(comm(a,b),comm(b,a))==one
    # Independent graph derivation: k product components form graph vertices;
    # n connecting/additional handles form edges. Cycle rank is n-k+1.
    arithmetic=0
    for k in range(1,6):
        for hs in product(range(1,4),repeat=k):
            for cycles in range(7):
                n=k-1+cycles
                g=sum(hs)+cycles
                assert g==sum(hs)+n-k+1
                assert 2-2*g+sum(2-2*h for h in hs)==2*(sum(2-2*h for h in hs)-n)
                arithmetic+=1
    manifest=json.loads((PACKET/'MANIFEST.json').read_text())
    for name,want in manifest.items():
        assert hashlib.sha256((PACKET/name).read_bytes()).hexdigest()==want,name
    original=json.loads(subprocess.check_output(['python3',str(PACKET/'verify.py')]))
    assert original==json.loads((PACKET/'verification.json').read_text())
    answer={
        'status':'PASS',
        'independent_torsor':'det=-1 matrices over F_5 acted on by det=1 matrices',
        'ambient_orientation_preserving_group_order':len(G),
        'left_group_order':len(L),
        'right_group_order':len(R),
        'pair_relation_checks':relation_checks,
        'omitted_conjugation_mutant_failures':omitted,
        'wrong_factor_side_mutant_failures':swapped,
        'inverse_gluing_side_exchange_checks':len(G),
        'marking_sensitive_finite_quotient_counts':quotients,
        'exterior_meridian_versus_filling_meridian_control':'PASS',
        'separating_compression_is_invisible_to_homology_control':'PASS',
        'graph_handle_genus_checks':arithmetic,
        'packet_manifest_hashes_verified':len(manifest),
        'original_verifier_replayed_and_output_matched':original,
        'topology_certified_by_computation':False,
    }
    print(json.dumps(answer,indent=2,sort_keys=True))

if __name__=='__main__':main()
