#!/usr/bin/env python3
"""Independent rational-circle, Jacobian and exact-slice diagnostics."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
C={}
def ck(x,k):
    assert x,k
    C[k]=C.get(k,0)+1

def mult(z,w):return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def determinant(z,w):return z[0]*w[1]-z[1]*w[0]
def norm(z):return z[0]**2+z[1]**2

def crossing_winding(vertices):
    """Integer winding of a polygon avoiding zero, via positive-ray crossings."""
    value=0
    for a,b in zip(vertices,vertices[1:]):
        d=determinant(a,b)
        ck(not(d==0 and a[0]*b[0]+a[1]*b[1]<=0),'segments_avoid_zero')
        if a[1]<=0<b[1] and d>0:value+=1
        if b[1]<=0<a[1] and d<0:value-=1
    return value

for m in range(5,45):
    # Rational upper unit semicircle from +1 to -1, a different path from submission.
    roots=[]
    for k in range(m):
        t=F(k,m-k)
        roots.append(((1-t*t)/(1+t*t),2*t/(1+t*t)))
    roots.append((F(-1),F(0)))
    params=[mult(w,w) for w in roots]
    ck(roots[0]==(1,0) and roots[-1]==(-1,0),'opposite_endpoints')
    ck(params[0]==params[-1]==(1,0),'closed_squared_loop')
    ck(crossing_winding(params)==1,'parameter_winding_one')
    for w,z in zip(roots,params):
        ck(norm(w)==norm(z)==1,'unit_circle_norm')
        for c in (F(1,3),F(2,7),F(5,11)):
            x,y=(c*w[0],c*w[1]);u,v=(c*c*z[0],c*c*z[1])
            ck(x*x-y*y-u==0 and x*y-v/2==0,'exact_scaled_slice_roots')
            # Independent derivative of the real equation pair.
            jac=2*x*x+2*y*y
            ck(jac==2*c*c and jac>0,'nonzero_slice_jacobian')
            ck(u*u+v*v/4<=c**4,'coefficient_ball_inclusion')
            ck(x*x+y*y==c*c,'approximation_threshold')
# General coefficient slice identity on an independent rational grid.
for x in (F(k,5) for k in range(-5,6)):
    for y in (F(k,7) for k in range(-6,7)):
        for u,v in [(F(3,2),F(-4,3)),(F(-5,7),F(11,9)),(F(0),F(0))]:
            f=x*x-y*y-u;g=x*y-v/2
            ck((f,2*g)==(mult((x,y),(x,y))[0]-u,mult((x,y),(x,y))[1]-v),'all_roots_equivalence')
# Endpoint degree equation is impossible for every integer; these are diagnostic instances.
for d in range(-50,51):ck(2*d!=1,'integer_degree_obstruction_controls')
base=Path(__file__).resolve().parent
artifact=base/'author_replay'/'NO_COVER.md'
expected='d88322ab825acd97914b898018116f2544dc92c460fe3c37ac86eeab331a8448'
ck(hashlib.sha256(artifact.read_bytes()).hexdigest()==expected,'frozen_artifact')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'categories':C,'rational_circle_polygons':40,
 'scope':'Exact diagnostic algebra and polygon winding only; the proof uses the all-integer degree equation and local openness, not finite sampling',
 'artifact_sha256':expected,'independent_checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2,sort_keys=True))
