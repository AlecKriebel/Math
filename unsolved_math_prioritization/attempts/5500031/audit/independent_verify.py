#!/usr/bin/env python3
"""Independent rational-arithmetic controls. Does not import author code.

Ray-line hits use the supporting normal equation and a dot-product segment
coordinate; reflection uses the normal Householder operator. This differs from
the author's determinant hit test and tangent projection reflection formula.
All finite results are controls, not a solver for the unrestricted conjecture.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from collections import Counter
import json

C = Counter()
def require(label, condition):
    C[label] += 1
    if not condition:
        raise AssertionError(label)

def p(x,y): return Q(x),Q(y)
def plus(a,b): return tuple(x+y for x,y in zip(a,b))
def minus(a,b): return tuple(x-y for x,y in zip(a,b))
def times(t,a): return tuple(t*x for x in a)
def inner(a,b): return sum(x*y for x,y in zip(a,b))
def norm2(a): return inner(a,a)
def perp(a): return -a[1],a[0]
def line_hit(q,v,seg):
    a,b=seg; d=minus(b,a); n=perp(d)
    denominator=inner(n,v)
    if denominator == 0: return None
    t=inner(n,minus(a,q))/denominator
    z=plus(q,times(t,v))
    r=inner(minus(z,a),d)/norm2(d)
    return t,r,z
def bounce(v,seg):
    n=perp(minus(seg[1],seg[0]))
    return minus(v,times(2*inner(n,v)/norm2(n),n))
def point_segment_distance2(q,seg):
    a,b=seg; d=minus(b,a)
    t=max(Q(0),min(Q(1),inner(minus(q,a),d)/norm2(d)))
    return norm2(minus(q,plus(a,times(t,d))))
def segment_distance2(s,t):
    h=line_hit(s[0],minus(s[1],s[0]),t)
    if h and 0 <= h[0] <= 1 and 0 <= h[1] <= 1: return Q(0)
    return min(*(point_segment_distance2(q,t) for q in s),
               *(point_segment_distance2(q,s) for q in t))
def clearance(mirrors):
    ds=[segment_distance2(a,b) for a,b in combinations(mirrors,2)]
    require('closed_segments_disjoint',bool(ds) and min(ds)>0)
    return min(ds)

def shoot(q,v,mirrors,limit=200,center=None,delta2=None):
    initial_q,initial_v=q,v
    elapsed=Q(0); seen=set(); states=[]; singular=False
    for _ in range(limit):
        if (q,v) in seen:
            return {'kind':'periodic','states':states,'singular':singular}
        seen.add((q,v))
        hits=[]; endpoints=[]
        for i,seg in enumerate(mirrors):
            h=line_hit(q,v,seg)
            if h is not None:
                if h[0]>0 and 0<h[1]<1: hits.append((h[0],i,h[1],h[2]))
                if h[0]>0 and h[1] in (0,1): endpoints.append(h[0])
            elif inner(perp(minus(seg[1],seg[0])),minus(q,seg[0]))==0:
                for e in seg:
                    u=inner(minus(e,q),v)/norm2(v)
                    if u>0: endpoints.append(u)
        hit=min(hits) if hits else None
        if any(t <= hit[0] for t in endpoints) if hit else bool(endpoints): singular=True
        if center is not None:
            dt=hit[0]/2 if hit else Q(13)
            now=plus(q,times(dt,v)); time=elapsed+dt
            x=minus(initial_q,center)
            require('radial_between_collisions',norm2(minus(now,center))==norm2(x)+2*inner(x,initial_v)*time+norm2(initial_v)*time*time)
        if hit is None:
            return {'kind':'escaped','states':states,'last':q,'outgoing':v,'singular':singular}
        dt,i,r,qnew=hit
        if states and delta2 is not None:
            require('distinct_successive_mirrors',states[-1]['mirror']!=i)
            require('no_zeno_flight_bound',dt*dt*norm2(v)>=delta2)
        out=bounce(v,mirrors[i]); elapsed+=dt
        require('speed_at_collision',norm2(v)==norm2(out))
        if center is not None:
            x=minus(qnew,center)
            require('radial_jump_zero',inner(x,v)==inner(x,out))
            require('radial_linear_derivative',inner(x,v)==inner(minus(initial_q,center),initial_v)+norm2(initial_v)*elapsed)
            require('radial_at_collision',norm2(x)==norm2(minus(initial_q,center))+2*inner(minus(initial_q,center),initial_v)*elapsed+norm2(initial_v)*elapsed**2)
        states.append({'mirror':i,'point':qnew,'parameter':r,'elapsed':elapsed})
        q,v=qnew,out
    return {'kind':'cutoff_unresolved','states':states,'singular':singular}

def jsonable(x):
    if isinstance(x,Q): return str(x)
    if isinstance(x,(tuple,list)): return [jsonable(y) for y in x]
    if isinstance(x,dict): return {k:jsonable(v) for k,v in x.items()}
    return x

# Householder invariants, with translations and nonunit tangent/normal vectors.
for a,b in product(range(-4,5),repeat=2):
    if not (a or b): continue
    d=p(a,b); seg=(p(3,-2),plus(p(3,-2),d))
    for x,y in product(range(-4,5),repeat=2):
        v=p(x,y); w=bounce(v,seg)
        require('householder_norm',norm2(v)==norm2(w))
        require('householder_involution',bounce(w,seg)==v)
        require('householder_tangent',inner(d,v)==inner(d,w))
        require('householder_normal',inner(perp(d),v)==-inner(perp(d),w))

base=[(p(1,0),p(3,0)),(p(0,1),p(0,3)),(p(-1,-1),p(-3,-3)),(p(1,-2),p(2,-4))]
wedge=[(p(1,Q(1,10)),p(20,2)),(p(1,Q(-1,10)),p(20,-2))]
fixtures=[(base,[p(Q(1,5),Q(1,7)),p(Q(-1,5),Q(2,7))],4),
          (wedge,[p(10,0)],5)]
rotations=[(Q(1),Q(0)),(Q(3,5),Q(4,5)),(Q(-5,13),Q(12,13))]
concurrent_runs=[]
for coss,sinn in rotations:
    c=p(Q(7,3),Q(-11,5))
    def rotate(v): return coss*v[0]-sinn*v[1],sinn*v[0]+coss*v[1]
    def transform(q): return plus(c,rotate(q))
    for mirrors,sources,bound in fixtures:
        mirrors=[tuple(transform(z) for z in m) for m in mirrors]
        delta2=clearance(mirrors)
        for s in sources:
            for x,y in product(range(-bound,bound+1),repeat=2):
                if not (x or y): continue
                ray=shoot(transform(s),rotate(p(x,y)),mirrors,center=c,delta2=delta2)
                require('concurrent_escape',ray['kind']=='escaped')
                concurrent_runs.append((len(ray['states']),ray['singular']))

box=[(p(1,-2),p(1,2)),(p(-1,-2),p(-1,2)),
     (p(Q(-9,10),Q(3,2)),p(Q(9,10),Q(3,2))),
     (p(Q(-9,10),Q(-3,2)),p(Q(9,10),Q(-3,2)))]
box_delta2=clearance(box)
require('box_exact_clearance',box_delta2==Q(1,100))
for x,y in product(range(-40,41),repeat=2):
    if x or y:
        h=[line_hit(p(0,0),p(x,y),m) for m in box]
        require('box_direct_hit',any(z and z[0]>0 and 0<z[1]<1 for z in h))

certificate=shoot(p(0,0),p(2,1),box,delta2=box_delta2)
require('certificate_kind',certificate['kind']=='escaped')
require('certificate_word',[z['mirror'] for z in certificate['states']]==[0,1])
require('certificate_points',[z['point'] for z in certificate['states']]==[p(1,Q(1,2)),p(-1,Q(3,2))])
require('certificate_regular',not certificate['singular'])
require('certificate_outgoing',certificate['outgoing']==p(2,1))

lower,upper=Q(15,31),Q(15,29)
# Exact interval signs: the four nontrivial constraints after positive scaling.
require('interval_positive',0<lower<Q(1,2)<upper)
require('first_hit_below_top',upper<Q(3,2))
require('second_hit_inside_vertical',3*upper<2)
require('final_vertical_missed',5*lower>2)
require('lower_top_gap_equivalence',31*lower-15==0)
require('upper_top_gap_equivalence',15-29*upper==0)
for j in range(1,401):
    m=lower+(upper-lower)*Q(j,401)
    ray=shoot(p(0,0),p(1,m),box,delta2=box_delta2)
    require('interval_two_bounces',ray['kind']=='escaped' and [s['mirror'] for s in ray['states']]==[0,1])
    require('interval_regular',not ray['singular'])
    require('interval_top_gap', Q(2)-Q(3,2)/m<Q(-9,10) if m>Q(1,2) else Q(3,2)/m-4<Q(-9,10))
for m in (lower,upper):
    ray=shoot(p(0,0),p(1,m),box)
    require('boundary_transparent_escape',ray['kind']=='escaped' and len(ray['states'])==2 and ray['singular'])
for d in (p(1,0),p(0,1)):
    require('box_normal_periodic',shoot(p(0,0),d,box)['kind']=='periodic')
require('finite_cutoff_not_trapping',shoot(p(0,0),p(2,1),box,limit=1)['kind']=='cutoff_unresolved')

sole=[(p(1,0),p(1,1))]
ep=shoot(p(0,0),p(1,1),sole)
require('endpoint_transparency',ep['kind']=='escaped' and ep['singular'] and not ep['states'])
collinear=shoot(p(0,0),p(1,0),[(p(1,0),p(2,0))])
require('collinear_transparent_extension',collinear['kind']=='escaped' and collinear['singular'] and not collinear['states'])
require('endpoint_source_extension',shoot(p(1,0),p(1,1),sole)['kind']=='escaped')

parallel=[(p(-2,-1),p(2,-1)),(p(-2,1),p(2,1))]
pd=clearance(parallel)
for x,y in product(range(-9,10),repeat=2):
    if x==0: continue
    ray=shoot(p(0,0),p(x,y),parallel,delta2=pd)
    require('parallel_escape',ray['kind']=='escaped')
    for state in ray['states']:
        require('parallel_drift',state['point'][0]==x*state['elapsed'])
require('parallel_normal_periodic',shoot(p(0,0),p(0,1),parallel)['kind']=='periodic')
require('parallel_unbracketed_escape',shoot(p(0,2),p(0,-1),parallel)['kind']=='escaped')

# Exact coefficient rank for A11,A12,A22,b1,b2 on x=0,y=0,x+y=1.
matrix=[[0,1,0,0,0],[0,0,0,1,0],[0,1,0,0,0],[0,0,0,0,1],
        [1,0,-1,0,0],[0,1,1,1,1]]
matrix=[[Q(x) for x in row] for row in matrix]
rank=0
for col in range(5):
    pivot=next((i for i in range(rank,len(matrix)) if matrix[i][col]),None)
    if pivot is None: continue
    matrix[rank],matrix[pivot]=matrix[pivot],matrix[rank]
    factor=matrix[rank][col]; matrix[rank]=[x/factor for x in matrix[rank]]
    for i in range(len(matrix)):
        if i!=rank:
            factor=matrix[i][col]
            matrix[i]=[a-factor*b for a,b in zip(matrix[i],matrix[rank])]
    rank+=1
require('quadratic_obstruction_full_rank',rank==5)
nonconcurrent=[(p(0,2),p(0,3)),(p(2,0),p(3,0)),(p(2,-1),p(3,-2))]
clearance(nonconcurrent)

# Rational unit-circle checks of the exact prefix estimate identity.
unit=[p((1-Q(k,3)**2)/(1+Q(k,3)**2),2*Q(k,3)/(1+Q(k,3)**2)) for k in range(-9,10)]
for v,w in product(unit,repeat=2):
    for t,r in product((Q(1,7),Q(1),Q(13,3)),repeat=2):
        require('prefix_exact_identity',norm2(minus(times(t,v),times(r,w)))==(t-r)**2+t*r*norm2(minus(v,w)))
        require('prefix_lower_bound',norm2(minus(times(t,v),times(r,w)))>=t*r*norm2(minus(v,w)))

result={'status':'PASS','problem_id':5500031,'assertions':sum(C.values()),
        'counts':dict(sorted(C.items())),'concurrent_trace_count':len(concurrent_runs),
        'concurrent_max_bounces':max(n for n,s in concurrent_runs),
        'concurrent_singular_trace_count':sum(s for n,s in concurrent_runs),
        'box_escape_certificate':jsonable(certificate),
        'box_closed_segment_clearance_squared':str(box_delta2),
        'two_bounce_interval':[str(lower),str(upper)],
        'quadratic_constraint_rank':rank,
        'clock_note':'elapsed is the affine ray parameter; multiply by velocity norm for unit-speed physical time',
        'scope':'Independent finite controls; universal claims are evaluated in the written audit.'}
print(json.dumps(result,sort_keys=True,indent=2))
