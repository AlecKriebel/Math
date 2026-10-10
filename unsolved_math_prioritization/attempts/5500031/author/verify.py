#!/usr/bin/env python3
"""Exact finite controls for scoped segment-mirror claims. No general solver."""
from fractions import Fraction as F
from itertools import product
import json

counts={}
def check(name,p):
    counts[name]=counts.get(name,0)+1
    if not p: raise AssertionError(name)
def vec(x,y): return (F(x),F(y))
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def sub(x,y): return (x[0]-y[0],x[1]-y[1])
def mul(t,x): return (t*x[0],t*x[1])
def dot(x,y): return x[0]*y[0]+x[1]*y[1]
def cross(x,y): return x[0]*y[1]-x[1]*y[0]
def reflect(v,u): return sub(mul(2*dot(v,u)/dot(u,u),u),v)
def hit(q,v,a,b):
    u=sub(b,a); den=cross(v,u)
    if den==0: return None
    t=cross(sub(a,q),u)/den; r=cross(sub(a,q),v)/den
    if t>0 and 0<r<1: return t,r
    return None

def trace(q,v,mirrors,limit=100,center=None):
    start,initial=q,v; elapsed=F(0); states=[]; seen={}
    for _ in range(limit):
        key=(q,v)
        if key in seen:
            return {'kind':'periodic','start':seen[key],'states':states}
        seen[key]=len(states)
        candidates=[]
        for i,(a,b) in enumerate(mirrors):
            h=hit(q,v,a,b)
            if h is not None: candidates.append((h[0],i,h[1]))
        if not candidates:
            return {'kind':'escaped','states':states,'last':q,'outgoing':v}
        t,i,r=min(candidates); q=add(q,mul(t,v)); elapsed+=t
        u=sub(mirrors[i][1],mirrors[i][0]); w=reflect(v,u)
        check('reflection_speed',dot(v,v)==dot(w,w))
        if center is not None:
            x=sub(q,center); s=sub(start,center)
            check('concurrent_radial_derivative',dot(x,v)==dot(x,w))
            check('concurrent_global_polynomial',dot(x,x)==dot(s,s)+2*dot(s,initial)*elapsed+dot(initial,initial)*elapsed**2)
        states.append({'mirror':i,'point':q,'parameter':r,'elapsed':elapsed})
        v=w
    return {'kind':'cutoff_unresolved','states':states}

def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,tuple):return [serial(z) for z in x]
    if isinstance(x,list):return [serial(z) for z in x]
    if isinstance(x,dict):return {k:serial(v) for k,v in x.items()}
    return x

# Reflection identities, including the common-center radial identity.
for a,b in product(range(-3,4),repeat=2):
    u=vec(a,b)
    if u==(0,0):continue
    for x,y in product(range(-3,4),repeat=2):
        v=vec(x,y); w=reflect(v,u)
        check('involution',reflect(w,u)==v)
        check('speed',dot(v,v)==dot(w,w))
        check('tangential',dot(u,v)==dot(u,w))
        for t in [F(-3,2),F(1,3),F(4)]:
            q=mul(t,u)
            check('concurrent_local',dot(q,v)==dot(q,w))

# Pairwise disjoint mirrors on distinct lines through the origin.
concurrent=[(vec(1,0),vec(3,0)),(vec(0,1),vec(0,3)),
            (vec(-1,-1),vec(-3,-3)),(vec(1,-2),vec(2,-4))]
concurrent_runs=[]
for s in [vec(F(1,5),F(1,7)),vec(F(-1,5),F(2,7))]:
    for x,y in product(range(-4,5),repeat=2):
        if not(x or y):continue
        r=trace(s,vec(x,y),concurrent,center=vec(0,0))
        check('concurrent_traces_escape',r['kind']=='escaped')
        concurrent_runs.append({'source':s,'direction':vec(x,y),'bounces':len(r['states'])})

# An acute concurrent wedge gives multiple reflections rather than one-bounce tests.
wedge=[(vec(1,F(1,10)),vec(20,2)),(vec(1,F(-1,10)),vec(20,-2))]
for x,y in product(range(-5,6),repeat=2):
    if not(x or y):continue
    r=trace(vec(10,0),vec(x,y),wedge,center=vec(0,0))
    check('concurrent_wedge_escape',r['kind']=='escaped')
    concurrent_runs.append({'source':vec(10,0),'direction':vec(x,y),'bounces':len(r['states'])})

# No direct visibility to infinity, although many reflected rays escape.
box=[(vec(1,-2),vec(1,2)),(vec(-1,-2),vec(-1,2)),
     (vec(F(-9,10),F(3,2)),vec(F(9,10),F(3,2))),
     (vec(F(-9,10),F(-3,2)),vec(F(9,10),F(-3,2)))]
for x,y in product(range(-20,21),repeat=2):
    if x or y: check('blocked_first_leg',any(hit(vec(0,0),vec(x,y),*m) for m in box))
# These checks sample the analytic universal first-hit proof in PROOF.md.
escape=trace(vec(0,0),vec(2,1),box)
check('box_escape',escape['kind']=='escaped')
check('box_escape_word',[z['mirror'] for z in escape['states']]==[0,1])
for j in range(1,100):
    slope=F(15,31)+(F(15,29)-F(15,31))*F(j,100)
    r=trace(vec(0,0),vec(1,slope),box)
    check('box_open_slope_interval',r['kind']=='escaped' and [z['mirror'] for z in r['states']]==[0,1])
for d in [vec(1,0),vec(0,1)]:
    check('box_periodic',trace(vec(0,0),d,box)['kind']=='periodic')

# Endpoints are transparent, not reflecting: this direction misses a sole endpoint.
a,b=vec(1,0),vec(1,1)
check('endpoint_transparent',hit(vec(0,0),vec(1,1),a,b) is None)
check('segment_interior_hit',hit(vec(0,0),vec(2,1),a,b)==(F(1,2),F(1,2)))

# Exact parallel tangent drift, including a normal periodic control.
parallel=[(vec(-2,-1),vec(2,-1)),(vec(-2,1),vec(2,1))]
for x,y in product(range(-6,7),repeat=2):
    if x==0:continue
    d=vec(x,y);r=trace(vec(0,0),d,parallel)
    check('parallel_escape',r['kind']=='escaped')
    for z in r['states']:check('parallel_drift',z['point'][0]==x*z['elapsed'])
check('parallel_normal_periodic',trace(vec(0,0),vec(0,1),parallel)['kind']=='periodic')

# Quadratic obstruction equations. x=0 forces A12=b1=0; y=0 forces
# A12=b2=0; x+y=1 then forces A11=A22 and A11=0, excluding PD.
for a,d,b1,b2,k in product(range(-2,3),repeat=5):
    x_line=(k==0 and b1==0)
    y_line=(k==0 and b2==0)
    diag_line=(a==d and a+k+b1+b2==0)
    if x_line and y_line and diag_line:
        check('nonconcurrent_quadratic_obstruction',a==d==k==b1==b2==0)

# Finite-prefix angular bound: ||t v-r w||^2 >= t*r*||v-w||^2.
# Use exact rational points on the unit circle.
unit=[vec((1-F(t)**2)/(1+F(t)**2),2*F(t)/(1+F(t)**2)) for t in range(-5,6)]
for v,w in product(unit,repeat=2):
    for t,r in product([F(1,2),F(1),F(3)],repeat=2):
        check('prefix_distance_identity',dot(sub(mul(t,v),mul(r,w)),sub(mul(t,v),mul(r,w)))==(t-r)**2+t*r*dot(sub(v,w),sub(v,w)))

result={'status':'PASS','problem_id':'5500031','scope':'Exact finite controls, not a proof of the unrestricted problem',
        'assertions':sum(counts.values()),'counts':counts,
        'concurrent_trace_count':len(concurrent_runs),
        'concurrent_max_bounces':max(r['bounces'] for r in concurrent_runs),
        'box_escape_certificate':serial(escape)}
print(json.dumps(result,sort_keys=True,indent=2))
