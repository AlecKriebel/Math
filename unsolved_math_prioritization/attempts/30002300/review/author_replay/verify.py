#!/usr/bin/env python3
"""Exact bounded controls for the credited signed-simplex representation.

The general result is Akopyan--Barany--Robins Theorem 1. These checks do not
replace it and do not establish the separate universal +/-1 conjecture.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import permutations,product
from math import factorial
from pathlib import Path
import hashlib,json

checks=Counter()
def check(v,key):
    assert v,key
    checks[key]+=1

def det(a):
    n=len(a);out=Q(0)
    for p in permutations(range(n)):
        v=Q((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
        for i in range(n):v*=a[i][p[i]]
        out+=v
    return out

def aug(T):return [[Q(1)]*len(T)]+[[Q(v[i]) for v in T] for i in range(len(T)-1)]
def volume(T):return abs(det(aug(T)))/factorial(len(T)-1)
def inside(T,p):
    a=aug(T);D=det(a);target=[Q(1)]+list(p);bs=[]
    for j in range(len(T)):
        b=[row[:] for row in a]
        for i in range(len(T)):b[i][j]=target[i]
        bs.append(det(b)/D)
    if any(x==0 for x in bs):return None
    return all(x>0 for x in bs)

def moment(T,powers):
    d=len(powers);n=d+1;poly={(0,)*n:Q(1)}
    for axis,pow_ in enumerate(powers):
        for _ in range(pow_):
            nxt=Counter()
            for ex,c in poly.items():
                for j in range(n):
                    ee=list(ex);ee[j]+=1;nxt[tuple(ee)]+=c*T[j][axis]
            poly=nxt
    D=abs(det(aug(T)))
    return D*sum(c*prod(factorial(x) for x in ex)/factorial(d+sum(ex)) for ex,c in poly.items())
def prod(xs):
    out=Q(1)
    for x in xs:out*=x
    return out

def boxmoment(box,powers):
    return prod(Q(hi**(a+1)-lo**(a+1),a+1) for (lo,hi),a in zip(box,powers))
V=[(0,0),(3,0),(3,2),(2,2),(2,1),(1,1),(1,2),(0,2)]
tri=[]
for i in range(1,len(V)-1):
    T=(V[0],V[i],V[i+1]);D=det(aug(T))
    if D:tri.append((1 if D>0 else -1,T))
check(len(tri)==6 and sum(a<0 for a,T in tri)==1,'signed_fan_structure')
boxes2=[((0,3),(0,1)),((0,1),(1,2)),((2,3),(1,2))]
check(len({V[i][1] for i in (2,3,6,7)})==1,'four_collinear_vertices_violate_weak_position_2D')
for i in range(len(V)):
    a,b,c=V[i-1],V[i],V[(i+1)%len(V)]
    check(det([[b[0]-a[0],c[0]-b[0]],[b[1]-a[1],c[1]-b[1]]])!=0,'polygon_vertices_are_genuine_corners')
V3=[v+(z,) for v in V for z in (0,1)];tet=[]
for sg,T in tri:
    a,b,c=T
    a0,b0,c0=a+(0,),b+(0,),c+(0,)
    a1,b1,c1=a+(1,),b+(1,),c+(1,)
    pieces=[(a0,b0,c0,c1),(a0,b0,b1,c1),(a0,a1,b1,c1)]
    check(sum(volume(S) for S in pieces)==volume(T),'prism_staircase_volume')
    tet.extend((sg,S) for S in pieces)
check(len(tet)==18,'eighteen_signed_tetrahedra')
check(all(v[2]==0 for v in V3[::2][:5]),'five_coplanar_vertices_violate_weak_position_3D')
check(det(aug(tuple(v+(0,) for v in V[:4])))==0,'degenerate_tetrahedron_has_zero_volume')
boxes3=[b+((0,1),) for b in boxes2]
examples=[]
for d,verts,simp,boxes in [(2,V,tri,boxes2),(3,V3,tet,boxes3)]:
    for sg,T in simp:
        check(all(v in verts for v in T),'vertices_stay_in_allowed_set')
        check(volume(T)>0,'occurring_simplex_nondegenerate')
        check(sg in (-1,1),'example_integer_coefficient')
    check(sum(sg*volume(T) for sg,T in simp)==5,'signed_mass')
    probcoef=[Q(sg)*volume(T)/5 for sg,T in simp]
    check(sum(probcoef)==1,'probability_coefficients_sum_to_one')
    check(any(a<0 for a in probcoef),'probability_normalization_preserves_signs')
    check(any(a.denominator>1 for a in probcoef),'probability_coefficients_need_not_be_integer')
    for powers in product(range(4),repeat=d):
        if sum(powers)>3:continue
        exact=sum(boxmoment(b,powers) for b in boxes)
        check(sum(sg*moment(T,powers) for sg,T in simp)==exact,'unit_density_moments_through_degree_three')
        check(sum(a*moment(T,powers)/volume(T) for a,(_,T) in zip(probcoef,simp))==exact/5,'probability_moments_through_degree_three')
    xs=[Q(-1),Q(1,5),Q(3,5),Q(6,5),Q(9,5),Q(11,5),Q(14,5),Q(16,5)]
    ys=[Q(-1),Q(1,7),Q(4,7),Q(8,7),Q(11,7),Q(15,7)]
    axes=[xs,ys]+([[Q(-1),Q(1,11),Q(5,11),Q(10,11),Q(2)]] if d==3 else [])
    tested=skipped=0
    for p in product(*axes):
        memberships=[inside(T,p) for _,T in simp]
        if any(v is None for v in memberships):skipped+=1;continue
        target=int(any(all(lo<p[i]<hi for i,(lo,hi) in enumerate(b)) for b in boxes))
        check(sum(sg*int(v) for (sg,T),v in zip(simp,memberships))==target,'signed_coverage_off_boundaries')
        check(sum(a*int(v)/volume(T) for a,(_,T),v in zip(probcoef,simp,memberships))==Q(target,5),'normalized_density_off_boundaries')
        tested+=1
    examples.append({'dimension':d,'vertices':len(verts),'simplices':len(simp),'volume':5,'point_controls':tested,'boundary_points_skipped':skipped})

here=Path(__file__).resolve().parent
print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),'checks':dict(sorted(checks.items())),
 'examples':examples,'source_status_sha256':hashlib.sha256((here/'SOURCE_STATUS.md').read_bytes()).hexdigest(),
 'limitation':'Finite exact controls illustrate published theorem coverage, not a new general proof or a resolution of the separate +/-1-coefficient question.'},indent=2,sort_keys=True))
