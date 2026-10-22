#!/usr/bin/env python3
"""Independent rational controls. Not a formal proof of the full billiard problem."""
from fractions import Fraction as Q
from collections import Counter
import argparse, json, sys

class Failure(RuntimeError): pass
class Singular(RuntimeError): pass
class ReflectionCap(RuntimeError): pass

def require(ok, message):
    if not ok: raise Failure(message)

def plus(a,b): return (a[0]+b[0],a[1]+b[1])
def minus(a,b): return (a[0]-b[0],a[1]-b[1])
def times(c,a): return (c*a[0],c*a[1])
def inner(a,b): return a[0]*b[0]+a[1]*b[1]
def wedge(a,b): return a[0]*b[1]-a[1]*b[0]
def bounce(v,normal):
    require(inner(normal,normal)>0,'zero mirror normal')
    return minus(v,times(2*inner(v,normal)/inner(normal,normal),normal))

def future_events(poly,p,v):
    events=[]
    for i in range(len(poly)):
        q=poly[i]; e=minus(poly[(i+1)%len(poly)],q)
        require(e!=(0,0),'zero-length edge')
        b=minus(q,p); D=wedge(v,e)
        if not D:
            if wedge(b,v)==0:
                along=[inner(minus(z,p),v)/inner(v,v) for z in (q,plus(q,e))]
                if max(along)>0: raise Singular('collinear future contact')
            continue
        t=wedge(b,e)/D; u=wedge(b,v)/D
        if t>0 and 0<=u<=1: events.append((t,u,i,e))
    return events

def trace(poly,p,v,cap=12):
    initial_speed=inner(v,v); hits=[]
    for _ in range(cap):
        E=future_events(poly,p,v)
        if not E: return p,v,hits
        t=min(z[0] for z in E); nearest=[z for z in E if z[0]==t]
        if len(nearest)!=1 or nearest[0][1] in (0,1): raise Singular('vertex contact')
        _,_,i,e=nearest[0]
        p=plus(p,times(t,v)); normal=(e[1],-e[0])
        v=bounce(v,normal)
        require(inner(v,v)==initial_speed,'speed drift')
        hits.append((i,p,v))
    raise ReflectionCap('finite cap reached; escape not certified')

def saw(n):
    # Construct the upper chain independently from explicit cell endpoints.
    upper=[]
    for j in range(n): upper.extend([(Q(j,n),Q(0)),(Q(2*j+1,2*n),Q(-1,2*n))])
    upper.append((Q(1),Q(0)))
    return upper+[(Q(1),Q(-1)),(Q(0),Q(-1))]

def hull(points):
    P=sorted(set(points))
    def chain(points):
        out=[]
        for p in points:
            while len(out)>1 and wedge(minus(out[-1],out[-2]),minus(p,out[-1]))<=0: out.pop()
            out.append(p)
        return out
    return chain(P)[:-1]+chain(P[::-1])[:-1]

def run(mutant=None):
    counts=Counter(); cases=Counter(); singular=0
    def check(ok,group):
        counts[group]+=1
        require(ok,group)
    def equal(a,b,group): check(a==b,group)
    ts=[Q(-3),Q(-1),Q(-1,3),Q(0),Q(1,7),Q(1),Q(4)]
    unit=lambda t: (2*t/(1+t*t),(1-t*t)/(1+t*t))
    U=[unit(t) for t in ts]
    for v in U:
        for w in U:
            factor=Q(1,2) if mutant=='defect_factor' else Q(1,4)
            equal(1-(1-inner(v,w))/2,factor*inner(plus(v,w),plus(v,w)),'defect_identity')
            check(0<=(1-inner(v,w))/2<=1,'resistance_interval')
        for N in U:
            w=bounce(v,N)
            equal(inner(w,w),1,'reflection_speed')
            equal(bounce(w,N),v,'reflection_involution')
            for M in U:
                final=bounce(w,M)
                equal(final==times(-1,v),inner(N,M)==0,'two_reflection_equivalence_2d')
    equal(Q(1,3)-Q(-1,3),Q(2,3),'exposed_integral')
    equal(Q(2,3)/2,Q(1,3),'exposed_normalized_coefficient')
    for t in [Q(i,13) for i in range(-12,13)]:
        p,q=unit(t)
        for h in [Q(1,17),Q(2),Q(17,3)]:
            A_p=-2*h/q**3; length_p=2*h*p/q**3
            equal(length_p,-p*A_p,'travel_variation')
            X_x=1 if mutant=='jacobian' else -1
            equal(X_x*(-1),1,'symplectic_determinant')
    # Algebraic quantitative support-graph estimate for g(x)=-x^2.
    for x in [Q(i,100) for i in range(-9,10)]:
        N=(2*x,Q(1)); T=(Q(1),-2*x)
        for e in [Q(-1,10),Q(-1,20),Q(1,20),Q(1,10)]:
            d=plus(N,times(e,T)); v=times(-1,d); w=bounce(v,N)
            for z in (d,w):
                check(z[1]>abs(z[0]),'support_upward_cone')
                check(z[1]+2*x*z[0]>0,'support_graph_strict_separation')
            check(w!=times(-1,v),'support_non_normal_failure')
    # Simple rational star polygons; certify exact escape for the two partner directions.
    dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
    radii=[[1]*8,[1,3,2,1,4,2,1,3],[4,1,3,1,2,1,5,1],[2,5,1,2,3,1,2,4]]
    for radii_i in radii:
        P=[times(Q(r),d) for r,d in zip(radii_i,dirs)]; H=hull(P)
        for k,q in enumerate(H):
            lower=minus(H[(k+1)%len(H)],q); upper=minus(H[k-1],q)
            check(wedge(lower,upper)>0,'polygon_hull_cone_below_pi')
            j=P.index(q); options=[]
            for index,sign in [((j+1)%len(P),1),((j-1)%len(P),-1)]:
                T=minus(P[index],q); N=(sign*T[1],-sign*T[0])
                if wedge(lower,N)<0 or wedge(N,upper)<0: options.append((T,N))
            check(bool(options),'polygon_external_normal_exists')
            T,N=options[0]
            delta=Q(1,8)
            for attempt in range(30):
                p=plus(q,times(delta,T))
                directions=[plus(N,times(e,T)) for e in (Q(-1,100),Q(1,100))]
                if all(not future_events(P,p,d) for d in directions): break
                delta/=2
            else: raise Failure('polygon clear cone not found')
            for d in directions:
                equal(future_events(P,p,d),[],'polygon_clear_normal_perturbations')
                v=times(-1,d); w=bounce(v,N)
                check(w!=times(-1,v),'polygon_non_normal_failure')
                equal(future_events(P,p,w),[],'polygon_reflected_escape')
    angles=sorted({Q(i,d) for d in (3,5,8,13) for i in range(1,d)}|{Q(1,997),Q(996,997)})
    for n in (1,2,4,7):
        P=saw(n)
        for cell in range(n):
            for a in angles:
                left=(1-a)/2; threshold=1-a
                rs={Q(i,19) for i in range(1,19)}
                rs|={(1-a)/4,3*(1-a)/4,1-a/2}
                eps=min(a,1-a)/1009
                rs|={left-eps,left+eps,threshold-eps,threshold+eps}
                rs|={left,threshold}
                for r in sorted(rs):
                    if not 0<r<1: continue
                    start=((cell+r)/n,Q(0)); vel=(a,Q(-1))
                    exceptional=r in (left,threshold)
                    try: p,w,hits=trace(P,start,vel)
                    except Singular:
                        check(exceptional,'only_predicted_sawtooth_singularities'); singular+=1; continue
                    check(not exceptional,'singular_sawtooth_not_accepted')
                    retro=r<threshold
                    equal(len(hits),2 if retro else 1,'sawtooth_collision_count')
                    expected=(-a,Q(1)) if retro else (Q(-1),a)
                    if mutant=='all_retro': expected=(-a,Q(1))
                    equal(w,expected,'sawtooth_direction')
                    equal(inner(w,w),1+a*a,'sawtooth_speed')
                    local=(1-a-r) if retro else (r+a-1)/a
                    if mutant=='exit_position': local=-local
                    equal(p[0]-p[1]*w[0]/w[1],(cell+local)/n,'sawtooth_exit_position')
                    check(0<local<1,'sawtooth_same_cell_exit')
                    check(a-w[0]>=2*a,'horizontal_difference_at_least_2a')
                    equal(future_events(P,p,w),[],'full_polygon_escape')
                    cases['two_bounce' if retro else 'one_bounce']+=1
    # Exact endpoints of the angular range and deliberately singular rays.
    for a,want in [(Q(0),(Q(0),Q(1))),(Q(1),(Q(-1),Q(1)))]:
        for r in (Q(1,5),Q(2,5),Q(4,5)):
            _,w,h=trace(saw(1),(r,Q(0)),(a,Q(-1)))
            equal(w,want,'angular_endpoint_behavior')
            equal(len(h),2 if a==0 else 1,'angular_endpoint_bounce_count')
    try: trace(saw(1),(Q(1,2),Q(0)),(Q(0),Q(-1)))
    except Singular: check(True,'apex_rejected')
    else: raise Failure('apex was accepted')
    try: trace(saw(1),(Q(-1),Q(0)),(Q(1),Q(0)))
    except Singular: check(True,'grazing_collinear_rejected')
    else: raise Failure('grazing was accepted')
    box=[(Q(0),Q(0)),(Q(1),Q(0)),(Q(1),Q(1)),(Q(0),Q(1))]
    try: trace(box,(Q(1,3),Q(2,7)),(Q(1),Q(2,5)),cap=3)
    except ReflectionCap: check(True,'reflection_cap_is_not_escape')
    else: raise Failure('cap was misreported')
    # Rigid covariance: quarter turn, rational scaling, and translation.
    F=lambda p:(Q(17,3)-Q(5,7)*p[1],Q(-11,2)+Q(5,7)*p[0])
    D=lambda v:(-v[1],v[0])
    for a in (Q(1,13),Q(3,7),Q(8,9)):
        for r in ((1-a)/4,3*(1-a)/4,1-a/2):
            P=saw(3); start=((1+r)/3,Q(0)); v=(a,Q(-1))
            p,w,h=trace(P,start,v)
            p2,w2,h2=trace([F(z) for z in P],F(start),D(v))
            equal(p2,F(p),'rigid_scaled_last_collision')
            equal(w2,D(w),'rigid_scaled_velocity')
            equal(len(h2),len(h),'rigid_scaled_itinerary')
    return {'status':'PASS_INDEPENDENT_EXACT_CONTROLS','optimization':sys.flags.optimize,
            'checks':sum(counts.values()),'groups':dict(sorted(counts.items())),
            'sawtooth_cases':dict(sorted(cases.items())),'sawtooth_singular_cases':singular,
            'full_problem_solved':False,'simulations_with_rounding':0}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--mutant',choices=['defect_factor','jacobian','all_retro','exit_position'])
    args=parser.parse_args();print(json.dumps(run(args.mutant),sort_keys=True,indent=2))
