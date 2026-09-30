#!/usr/bin/env python3
"""Exact diagnostics for the scoped Yamabe-cone results, not a global topology computation."""
from fractions import Fraction as F
from itertools import product,combinations
from math import isqrt
from pathlib import Path
from hashlib import sha256
import json
C={}
def ck(name,ok):
    assert ok,name
    C[name]=C.get(name,0)+1
def qdiag(x,rminus,rzero):
    return -sum(t*t for t in x[:rminus])+sum(t*t for t in x[rminus+rzero:])
def exactsqrt(x):
    a=isqrt(x.numerator);b=isqrt(x.denominator)
    assert a*a==x.numerator and b*b==x.denominator
    return F(a,b)
# The nonpositive deformation retains the negative and null components.
for dim in range(1,5):
    for rm in range(dim+1):
        for rz in range(dim-rm+1):
            for raw in product((-1,0,1),repeat=dim):
                if not any(raw):continue
                x=tuple(map(F,raw));qx=qdiag(x,rm,rz)
                if qx<=0:
                    ck('closed_nonzero_retained',any(x[:rm+rz]))
                    for t in (F(0),F(1,3),F(1)):
                        y=x[:rm+rz]+tuple((1-t)*z for z in x[rm+rz:])
                        ck('closed_deformation_preserves_set',qdiag(y,rm,rz)<=0 and any(y))
                    y=x[:rm+rz]+tuple(F(0) for _ in x[rm+rz:])
                    ck('closed_retraction_fixed_on_target',y[:rm+rz]==x[:rm+rz])
                if qx<0:
                    ck('strict_negative_component_nonzero',any(x[:rm]))
                    for t in (F(0),F(2,5),F(1)):
                        y=x[:rm]+tuple((1-t)*z for z in x[rm:])
                        ck('strict_deformation_preserves_set',qdiag(y,rm,rz)<0 and any(y))
# Positive diagonal congruence for arbitrary tested triples, using squared
# factors and positivity so no approximate square roots are introduced.
for a,b,c in product((F(1,5),F(2,3),F(1),F(7,2)),repeat=3):
    d2=(a*b/c,a*c/b,b*c/a)
    ck('positive_diagonal_factors',min(d2)>0)
    ck('three_point_pair_products',d2[0]*d2[1]==a*a and d2[0]*d2[2]==b*b and d2[1]*d2[2]==c*c)
    ck('three_point_determinant',2*a*b*c>0)
# Exact congruence on rational D and direct quadratic evaluations.
for d in product((F(1,2),F(1),F(3)),repeat=3):
    for u in [tuple(map(F,z)) for z in [(1,0,0),(1,-1,0),(1,2,-3),(-2,1,1)]]:
        v=tuple(d[i]*u[i] for i in range(3))
        qa=2*sum(d[i]*d[j]*u[i]*u[j] for i,j in combinations(range(3),2))
        qb=sum(v)**2-sum(z*z for z in v)
        ck('diagonal_quadratic_congruence',qa==qb)
# Rectangle matrices, reconstructing every coefficient from actual distances.
H=[(1,1,1,1),(1,1,-1,-1),(1,-1,1,-1),(1,-1,-1,1)]
records=[]
for c,s,expected in [
    (F(4,5),F(3,5),[F(47,24),-F(7,24),-F(17,24),-F(23,24)]),
    (F(12,13),F(5,13),[F(281,120),F(31,120),-F(151,120),-F(161,120)])]:
    points=[(c,s,0),(c,-s,0),(-c,s,0),(-c,-s,0)]
    ck('unit_spherical_coordinates',all(sum(z*z for z in p)==1 for p in points))
    A=[[F(0) if i==j else 1/exactsqrt(sum((points[i][k]-points[j][k])**2 for k in range(3))) for j in range(4)] for i in range(4)]
    a,b,d=1/(2*s),1/(2*c),F(1,2)
    ev=[a+b+d,a-b-d,-a+b-d,-a-b+d]
    ck('exact_eigenvalues',ev==expected)
    for v,lam in zip(H,ev):
        ck('Hadamard_eigenvector',all(sum(A[i][j]*v[j] for j in range(4))==lam*v[i] for i in range(4)))
    for i,j in combinations(range(4),2):
        ck('orthogonal_eigenbasis',sum(H[i][k]*H[j][k] for k in range(4))==0)
    neg=sum(z<0 for z in ev);pos=sum(z>0 for z in ev)
    ck('zero_trace',sum(ev)==0)
    ck('nondegenerate_witness',neg+pos==4)
    records.append({'cos':str(c),'sin':str(s),'eigenvalues':[str(z) for z in ev],'negative':neg,'positive':pos,'weak_fiber_sphere_dimension':neg-1})
ck('two_different_fiber_types',[z['weak_fiber_sphere_dimension'] for z in records]==[2,1])
# Rational half-angle parametrization t in [1/5,1/3]. The one crossing
# eigenvalue has numerator 1-4t-t^4 and a positive denominator.
for j in range(41):
    t=F(1,5)+F(j,40)*(F(1,3)-F(1,5))
    c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
    a,b,d=1/(2*s),1/(2*c),F(1,2)
    ck('half_angle_circle_identity',c*c+s*s==1 and 0<s<c)
    ck('crossing_eigenvalue_numerator',a-b-d==(1-4*t-t**4)/(4*t*(1-t*t)))
    ck('other_three_signs',a+b+d>0 and -a+b-d<0 and -a-b+d<0)
    ck('strict_crossing_polynomial_derivative',4*t**3+4>0)
ck('crossing_bracket',(F(1,5)**4+4*F(1,5)-1)<0<(F(1,3)**4+4*F(1,3)-1))
# Stereographic chord identity in exact rational coordinates.
def stereo(x):
    n=sum(z*z for z in x);return tuple(2*z/(1+n) for z in x)+((n-1)/(n+1),)
pts=[(F(0),F(0),F(0)),(F(1),F(0),F(0)),(F(1),F(2),F(-1)),(F(-2),F(1),F(3)),(F(1,3),F(2,5),F(4,7))]
for x,y in combinations(pts,2):
    sx,sy=stereo(x),stereo(y)
    n1,n2=sum(t*t for t in x),sum(t*t for t in y)
    dist2=sum((a-b)**2 for a,b in zip(x,y));chord2=sum((a-b)**2 for a,b in zip(sx,sy))
    ck('stereographic_unit_spheres',sum(z*z for z in sx)==sum(z*z for z in sy)==1)
    ck('chord_distance_congruence',chord2==4*dist2/((1+n1)*(1+n2)))
root=Path(__file__).resolve().parent
r={'status':'PASS','exact_assertions':sum(C.values()),'categories':C,'rectangle_witnesses':records,'artifact_sha256':sha256((root/'PARTIAL.md').read_bytes()).hexdigest(),'scope':'Exact algebra and finite deformation controls for stated partial results only; no classification of the general total Yamabe asymptotic set.'}
out=json.dumps(r,indent=2,sort_keys=True)+'\n';(root/'verification.json').write_text(out);print(out,end='')

