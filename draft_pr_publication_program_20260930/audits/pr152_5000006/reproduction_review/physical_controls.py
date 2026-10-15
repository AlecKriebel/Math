#!/usr/bin/env python3
"""Stdlib-only physical billiard controls, independent of candidate generation equations.

Enumerate reflected polygon copies, propose rays to their vertices, then perform
first-hit physical billiard tracing in the original polygon. End angles and
terminal copy labels are measured; neither is generated from the index formula.
Floating controls are falsification searches, not interval-certified proofs.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from math import pi, sin, cos, tan, atan2, hypot, acos, gcd
from fractions import Fraction
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
EPS = 1e-9
ANGLE_EPS = 2e-8
counts = Counter()
failures = []
max_errors = defaultdict(float)

def ck(name, ok, witness=None):
    counts[name] += 1
    if not ok:
        failures.append({'test': name, 'witness': witness})

def cross(a, b):
    return a.real*b.imag-a.imag*b.real

def polygon(n):
    c = complex(.5, .5/tan(pi/n))
    r = .5/sin(pi/n)
    v = [c+r*complex(cos(-pi/2-pi/n-2*pi*j/n),sin(-pi/2-pi/n-2*pi*j/n)) for j in range(n)]
    v[0] = 0j
    v[-1] = 1+0j
    return v

def reflected(poly, edge):
    a,b = poly[edge],poly[(edge+1)%len(poly)]
    u=(b-a)/abs(b-a)
    return [a+u*((z-a)/u).conjugate() for z in poly]

def physical_trace(n, vertices, direction, limit, hit_eps=EPS):
    d=direction/abs(direction)
    x=0j
    total=0.
    edges=[]
    current_copy=list(vertices)
    min_interior_margin=1.
    for segment in range(1,101):
        hits=[]
        for edge in range(n):
            a=vertices[edge]; b=vertices[(edge+1)%n]; w=b-a
            den=cross(d,w)
            if abs(den)<1e-13:
                continue
            t=cross(a-x,w)/den
            u=cross(a-x,d)/den
            if t>hit_eps and -hit_eps<=u<=1+hit_eps:
                hits.append((t,edge,u))
        if not hits:
            return None
        t,edge,u=min(hits)
        if total+t>limit+hit_eps*50:
            return None
        y=x+t*d
        j=min(range(n), key=lambda j: abs(y-vertices[j]))
        error=abs(y-vertices[j])
        if error<hit_eps*20:
            # Source Fig.8: pi-beta is the interior angle between the
            # backward end ray and the clockwise lower incident side.
            lo=(vertices[(j-1)%n]-vertices[j])
            offset=atan2(cross(lo,-d), (lo.conjugate()*(-d)).real)%(2*pi)
            if offset>2*pi-ANGLE_EPS: offset=0.
            alpha=atan2(direction.imag,direction.real)
            beta=pi-offset
            center=sum(current_copy)/n
            pcenter=sum(vertices)/n
            sign=1 if segment%2 else -1
            residuals=[abs(current_copy[j]-center-sign*(vertices[k]-pcenter)) for k in range(n)]
            ell=min(range(n),key=residuals.__getitem__)
            return {'n':n,'theta':alpha,'alpha':alpha/pi,'beta':beta/pi,'N':segment,
                    'j':j,'ell':ell,'edges':edges,'length':total+t,'endpoint_error':error,
                    'copy_match_error':residuals[ell], 'min_interior_margin':min_interior_margin,
                    'end_backward_direction':[(-d).real,(-d).imag],
                    'direction':[direction.real,direction.imag]}
        min_interior_margin=min(min_interior_margin,u,1-u)
        total+=t
        tangent=(vertices[(edge+1)%n]-vertices[edge])
        tangent/=abs(tangent)
        d=tangent*(d/tangent).conjugate()
        current_copy=reflected(current_copy,edge)
        x=y
        edges.append(edge)
    return None

def source_labels(n,a,b,segments):
    """Fresh transcription of Fuchs Def.2.1, in radians/pi; selected parity."""
    result=set()
    h=n//2
    eq=lambda x,y: abs(x-y)<ANGLE_EPS
    le=lambda x,y: x<=y+ANGLE_EPS
    ge=lambda x,y: x>=y-ANGLE_EPS
    for k in range(n-1):
        if segments%2:
            if n%2==0:
                valid=(k<=h-1 and ge(a,(h-k-1)/h) and eq(b+a,(n-k-1)/h)) or (k>=h-1 and le(a,(n-k-2)/h) and eq(b+a,(n-k-1)/h))
            else:
                valid=(k<=h-1 and ge(a,(n-2*(k+1))/n) and eq(b+a,2*(n-k-1)/n)) or (k>=h and le(a,2*(n-k-2)/n) and eq(b+a,2*(n-k-1)/n))
        else:
            if n%2==0:
                valid=(k<=h-1 and le(a,(h-k-1)/h) and eq(b-a,(k+1)/h)) or (k>=h-1 and ge(a,(n-k-2)/h) and eq(b-a,(k+3-n)/h))
            else:
                valid=(k<=h+1 and le(a,(n-2*(k+1))/n) and eq(b-a,2*(k+1)/n)) or (k>=h and ge(a,2*(n-k-2)/n) and eq(b-a,2*(k+3-n)/n))
        if valid: result.add(k%(n-2))
    return sorted(result)

def source_direction_class(n,theta):
    # Fuchs says sum or difference modulo 2pi/n; unoriented slopes are
    # represented modulo pi. Take full orbit instead of assuming half-step.
    return min((s*theta+2*pi*j/n)%pi for s in (1,-1) for j in range(n))

def annotate(t):
    n=t['n'];a=t['alpha'];b=t['beta'];N=t['N'];ell=t['ell']
    labs=source_labels(n,a,b,N)
    ck('physical_source_unique',len(labs)==1,t)
    if len(labs)!=1: return False
    k=labs[0]; t['k']=k
    t['weight']=sin((k+1)*pi/n)
    t['quotient']=t['length']/t['weight']
    e=0 if n%2 else ((ell%2) if N%2 else (1-ell%2))
    corner_t=ell
    if n%2 and (corner_t%2)!=(0 if N%2 else 1): corner_t+=n
    cone=corner_t*(n-2)/n+(1-a-b if N%2 else b-a-2/n)
    m=(cone-(1-e))/2
    err=abs(m-round(m));max_errors['corner_integer']=max(max_errors['corner_integer'],err)
    ck('physical_corner_integer',err<ANGLE_EPS,t)
    ck('physical_cone_source_index',(2*round(m)+1-e)%(n-2)==k,t)
    ck('physical_copy_translation_match',t['copy_match_error']<ANGLE_EPS,t)
    ck('physical_source_angle_range',-ANGLE_EPS<=a<=(n-2)/n+ANGLE_EPS and 2/n-ANGLE_EPS<=b<=1+ANGLE_EPS,t)
    t['cone_index']=round(m);t['endpoint_class']=e
    t['class']=source_direction_class(n,t['theta'])
    max_errors['endpoint']=max(max_errors['endpoint'],t['endpoint_error'])
    max_errors['copy_match']=max(max_errors['copy_match'],t['copy_match_error'])
    return True

def candidates(n, depth):
    v=polygon(n); frontier=[(v,None)]; seen=set(); rays={}
    for level in range(depth+1):
        nxt=[]
        for p,last in frontier:
            center=sum(p)/n
            # These center keys only reduce duplicate unfolded copies. They
            # do not define a trajectory or provide its type or length.
            key=(round(center.real,10),round(center.imag,10),level%2)
            if key in seen: continue
            seen.add(key)
            for z in p:
                if abs(z)<1e-8: continue
                theta=atan2(z.imag,z.real)
                if -1e-10<=theta<=(n-2)*pi/n+1e-10:
                    k=round(theta,12)
                    # A nearer vertex in an overlapping, nonphysical copy
                    # need not be the first vertex on the physical sheet.
                    # Keep the longest proposal to avoid cutting off a valid
                    # trace at such an irrelevant point.
                    if k not in rays or abs(z)>abs(rays[k]): rays[k]=z
            if level<depth:
                for edge in range(n):
                    if edge!=last: nxt.append((reflected(p,edge),edge))
        frontier=nxt
    return v,rays,len(seen)

def exact_hex_lattice(radius=30):
    # Point-set visibility by exhaustive collinear lattice points, rather
    # than the candidate's built-in first-endpoint multiplier.
    squared_weights={0:Fraction(1,4),1:Fraction(3,4),2:Fraction(1),3:Fraction(3,4)}
    def ty(p,q):
        if (p%3,q%3)==(1,2):return 1
        if p%2==0 and q%2==0:return 2
        if (p%3,q%3)==(2,1):return 3
        return 0
    def norm(p,q):return p*p-p*q+q*q
    def first(p,q):
        pts=[(d*p,d*q) for d in range(1,7) if (d*p+d*q)%3!=2]
        return pts[0]
    for p in range(-radius,radius+1):
        for q in range(-radius,radius+1):
            if gcd(p,q)!=1:continue
            x,y=first(p,q)
            d=gcd(x,y)
            ck('hex_exhaustive_first_vertex',all((i*p+i*q)%3==2 for i in range(1,d)),[p,q,x,y])
            ck('hex_multiplier_matches_claim',d==(2 if (p+q)%3==2 else 1),[p,q,x,y])
            quotient=Fraction(norm(x,y))/squared_weights[ty(x,y)]
            # Actual 12 unoriented slope symmetries of triangular lattice,
            # generated directly by 60-degree rotation and reflection.
            transforms=[]; a,b=p,q
            for _ in range(6):
                transforms.extend([(a,b),(b,a)])
                a,b=a-b,a
            for a,b in transforms:
                z,w=first(a,b)
                ck('hex_full_dihedral_squared_ratio',Fraction(norm(z,w))/squared_weights[ty(z,w)]==quotient,[p,q,a,b])

def physical_small_cases(radius=25):
    result={}
    for n in (3,4,6):
        v=polygon(n);good=0;max_segments=0
        for p in range(radius+1):
            for q in range(radius+1):
                if gcd(p,q)!=1:continue
                if n==3:
                    z=complex(p+q/2,q*3**.5/2);predicted_k=0
                elif n==4:
                    z=complex(p,q);predicted_k=int(p%2==q%2==1)
                else:
                    multiplier=2 if (p+q)%3==2 else 1
                    x,y=multiplier*p,multiplier*q
                    z=complex(x-y/2,y*3**.5/2)
                    if (x%3,y%3)==(1,2):predicted_k=1
                    elif x%2==0 and y%2==0:predicted_k=2
                    elif (x%3,y%3)==(2,1):predicted_k=3
                    else:predicted_k=0
                # The lattice check predicts only target and type; actual
                # physical tracing supplies its independent endpoint label.
                t=physical_trace(n,v,z,abs(z)*(1+1e-8))
                ck('small_lattice_physical_vertex',t is not None,[n,p,q])
                if not t or not annotate(t):continue
                good+=1;max_segments=max(max_segments,t['N'])
                ck('small_lattice_physical_length',abs(t['length']/abs(z)-1)<1e-8,t)
                ck('small_lattice_physical_type',t['k']==predicted_k,t)
        result[n]={'radius':radius,'physical_lattice_paths':good,'max_segments':max_segments}
    return result

def run():
    by_n={}; witnesses=[]; tolerance_comparisons=0
    for n in range(3,17):
        depth=5 if n<=6 else (4 if n<=10 else 3)
        v,rays,cells=candidates(n,depth)
        traces=[]
        for z in rays.values():
            t=physical_trace(n,v,z,abs(z)*(1+1e-8))
            if t and annotate(t):traces.append(t)
        groups=defaultdict(list)
        for t in traces:groups[round(t['class'],9)].append(t)
        pair_count=0; multi_type=0
        for members in groups.values():
            base=members[0]
            if len({t['k'] for t in members})>1: multi_type+=1
            for t in members[1:]:
                pair_count+=1
                relative=abs(t['quotient']/base['quotient']-1)
                max_errors['labelled_ratio_relative']=max(max_errors['labelled_ratio_relative'],relative)
                ck('physical_source_parallel_ratio',relative<1e-6,{'first':base,'second':t,'relative':relative})
            if len({t['k'] for t in members})>1 and len(witnesses)<100:
                witnesses.append({'n':n,'direction_class':base['class'],'connections':members[:20]})
        # Repeat a deterministic subset at tighter hit tolerance and compare
        # reflection sequence, physical endpoint, source type, and length.
        for t in traces[::max(1,len(traces)//100)]:
            z=complex(*t['direction'])
            s=physical_trace(n,v,z,abs(z)*(1+1e-8),1e-11)
            tolerance_comparisons+=1
            ck('physical_tolerance_repeat',s is not None and s['N']==t['N'] and s['j']==t['j'] and s['edges']==t['edges'] and abs(s['length']/t['length']-1)<1e-8,t)
            # Reverse the actual terminal ray and rotate its start corner
            # to vertex zero. This reconstructs a separate physical path.
            backwards=complex(*t['end_backward_direction'])
            turn=complex(cos(2*pi*t['j']/n),sin(2*pi*t['j']/n))
            reverse=physical_trace(n,v,backwards*turn,t['length']*(1+1e-8),1e-11)
            ck('physical_reversal_length',reverse is not None and abs(reverse['length']/t['length']-1)<1e-8,t)
            if reverse and annotate(reverse):
                ck('candidate_unqualified_physical_reversal',reverse['k']==(-t['k'])%(n-2),{'forward':t,'reverse':reverse})
                expected=(-t['k'])%(n-2) if t['N']%2 else t['k']
                ck('repaired_physical_reversal_type',reverse['k']==expected,{'forward':t,'reverse':reverse})
                ck('physical_reversal_weight',abs(reverse['weight']-t['weight'])<ANGLE_EPS,{'forward':t,'reverse':reverse})
            # Reflect the initial direction across the actual vertex angle
            # bisector, then measure the reflected physical path from scratch.
            angle=(n-2)*pi/n-t['theta']
            reflection=physical_trace(n,v,complex(cos(angle),sin(angle)),t['length']*(1+1e-8),1e-11)
            ck('physical_reflection_length',reflection is not None and abs(reflection['length']/t['length']-1)<1e-8,t)
            if reflection and annotate(reflection):
                ck('physical_reflection_type',reflection['k']==(-t['k'])%(n-2),{'forward':t,'reflected':reflection})
        by_n[n]={'depth':depth,'copy_count':cells,'candidate_directions':len(rays),'verified_physical_trajectories':len(traces),
                 'source_parallel_classes':len(groups),'labelled_ratio_comparisons':pair_count,'classes_with_distinct_types':multi_type,
                 'max_segments':max((t['N'] for t in traces),default=0),'type_counts':dict(Counter(t['k'] for t in traces))}
        print(json.dumps({'n':n,**by_n[n]},sort_keys=True),flush=True)
    exact_hex_lattice()
    small_cases=physical_small_cases()
    result={'timestamp':datetime.now(timezone.utc).isoformat(),'status':'PASS' if not failures else 'FAIL',
            'mechanism':'Reflected-copy vertex proposals, independently measured first-hit physical billiard paths, source angle labels, and full source-parallel classes.',
            'counts':dict(counts),'total_controls':sum(counts.values()),'failures':failures,'max_errors':dict(max_errors),'per_n':by_n,'small_cases':small_cases,
            'limitations':['finite reflection depths and n=3..16 only','double-precision physical search, not validated interval arithmetic',
                          'copy/direction deduplication has finite precision','does not certify Veech/cusp theorem applicability or universal affine invariance']}
    result['failure_interpretation']='Intentional test of unqualified physical source-label reversal. Distinguish reversal of an oriented saddle connection from physical billiard reversal; a Q-start chart requires a source-orientation conversion.'
    (ROOT/'physical_results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (ROOT/'physical_witnesses.json').write_text(json.dumps(witnesses,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'total_controls':result['total_controls'],'failures':len(failures),'max_errors':result['max_errors']},sort_keys=True))

if __name__=='__main__':run()
