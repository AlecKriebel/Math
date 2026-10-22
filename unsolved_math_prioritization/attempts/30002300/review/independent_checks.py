#!/usr/bin/env python3
"""Independent exact finite controls for a credited theorem application.

Polygon moments use Green's boundary formula, not the submitted barycentric
moment routine. Prism partition checks use explicit barycentric inequalities.
"""
from fractions import Fraction as Q
from collections import Counter
from itertools import product
from math import comb
from pathlib import Path
import hashlib,json

checks=Counter()
def check(ok,name):
    assert ok,name
    checks[name]+=1
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def edges(P):return zip(P,P[1:]+P[:1])
def area2(P):return sum(a[0]*b[1]-a[1]*b[0] for a,b in edges(P))
def green(P,A,B):
    value=Q(0)
    for v,w in edges(P):
        dx,dy=w[0]-v[0],w[1]-v[1]
        for i in range(A+2):
            for j in range(B+1):
                value += Q(comb(A+1,i)*comb(B,j)*v[0]**(A+1-i)*dx**i
                           *v[1]**(B-j)*dy**j*dy,(A+1)*(i+j+1))
    return value
def winding(P,p):
    ans=0
    for a,b in edges(P):
        if a[1]<=p[1]<b[1] and cross(a,b,p)>0:ans+=1
        if b[1]<=p[1]<a[1] and cross(a,b,p)<0:ans-=1
    return ans
def triangle_indicator(T,p):
    signs=[cross(a,b,p) for a,b in edges(T)]
    if 0 in signs:return None
    return int(all(q>0 for q in signs) or all(q<0 for q in signs))

base=[(0,0),(3,0),(3,2),(2,2),(2,1),(1,1),(1,2),(0,2)]
maps=[((1,0,0,1),(0,0)),((2,1,1,1),(3,-2)),
      ((-1,0,0,1),(0,0)),((1,2,0,3),(-1,2))]
degenerate=0;coverage=0
for (a,b,c,d),(e,f) in maps:
    determinant=a*d-b*c
    P=[(a*x+b*y+e,c*x+d*y+f) for x,y in base]
    if area2(P)<0:P=list(reversed(P))
    mass=Q(area2(P),2)
    check(mass==5*abs(determinant),'affine_mass')
    col=[(a*x+b*2+e,c*x+d*2+f) for x in range(4)]
    check(all(cross(col[0],col[1],v)==0 for v in col[2:]),'four_collinear_allowed_vertices')
    for shift in range(8):
        V=P[shift:]+P[:shift];fan=[]
        for i in range(1,7):
            T=[V[0],V[i],V[i+1]];D=area2(T)
            if D==0:degenerate+=1;continue
            fan.append((1 if D>0 else -1,T,Q(abs(D),2)))
        check(sum(sg*vol for sg,T,vol in fan)==mass,'signed_fan_mass')
        for A in range(5):
            for B in range(5-A):
                exact=green(P,A,B)
                check(sum(sg*(1 if area2(T)>0 else -1)*green(T,A,B)
                          for sg,T,vol in fan)==exact,'Green_moments_degree_four')
                check(sum(Q(sg)*vol/mass*((1 if area2(T)>0 else -1)*green(T,A,B)/vol)
                          for sg,T,vol in fan)==exact/mass,'probability_rescaling_moments')
        for x,y in product([Q(1,7),Q(5,7),Q(10,7),Q(16,7),Q(23,7)],
                           [Q(-1,11),Q(3,11),Q(9,11),Q(15,11),Q(20,11),Q(25,11)]):
            point=(a*x+b*y+e,c*x+d*y+f)
            values=[triangle_indicator(T,point) for sg,T,vol in fan]
            if None in values:continue
            check(sum(sg*inside for (sg,T,vol),inside in zip(fan,values))==winding(P,point),
                  'winding_vs_signed_coverage')
            coverage+=1
check(degenerate>0,'apex_on_facet_degeneracies_exercised')

# Every point of the standard triangular prism lies in one staircase simplex:
# z<=c; c<=z<=b+c; or b+c<=z. This works under every nondegenerate affine map.
prism_points=0
tetrahedra=[[(0,0,0),(1,0,0),(0,1,0),(0,1,1)],
            [(0,0,0),(1,0,0),(1,0,1),(0,1,1)],
            [(0,0,0),(0,0,1),(1,0,1),(0,1,1)]]
for i in range(1,8):
    for j in range(1,9-i):
        b,c=Q(i,9),Q(j,9);a=1-b-c
        for k in range(1,13):
            z=Q(k,13)
            if z in (c,b+c):continue
            bary=[(a,b,c-z,z),(a,b+c-z,z-c,c),(1-z,z-b-c,b,c)]
            admissible=[all(v>0 for v in t) for t in bary]
            check(sum(admissible)==1,'prism_exact_partition')
            for T,weights in zip(tetrahedra,bary):
                check(sum(weights)==1,'prism_barycentric_sum')
                check(tuple(sum(q*v[axis] for q,v in zip(weights,T)) for axis in range(3))
                      ==(b,c,z),'prism_barycentric_reconstruction')
            prism_points+=1

root=Path(__file__).resolve().parent
h=hashlib.sha256((root/'author_replay/SOURCE_STATUS.md').read_bytes()).hexdigest()
check(h=='48d460bed68baef63064bab715d4148cedf9c42d28436a3e30eda7f17c728b34',
      'frozen_source_hash')
print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),
 'checks':dict(sorted(checks.items())),'signed_coverage_controls':coverage,
 'prism_partition_points':prism_points,'degenerate_fan_terms_omitted':degenerate,
 'source_status_sha256':h,'limitation':'Finite controls for boundary cancellation, degeneracies and normalization supplement the published general theorem; they do not prove a universal +/-1 representation.'},indent=2,sort_keys=True))
