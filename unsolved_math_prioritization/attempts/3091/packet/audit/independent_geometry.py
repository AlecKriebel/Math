#!/usr/bin/env python3
"""Independent finite geometry audit. Exact Caratheodory oracle; no assertions."""
import argparse
import importlib.util
import itertools as it
import json
import sys
from fractions import Fraction as F
from pathlib import Path

class AuditFailure(Exception): pass

def need(v, message):
    if not v: raise AuditFailure(message)

def det(a,b,c):
    return a[0]*(b[1]-c[1])+b[0]*(c[1]-a[1])+c[0]*(a[1]-b[1])

def on_segment(p,a,b):
    return det(p,a,b)==0 and sum((p[i]-a[i])*(p[i]-b[i]) for i in (0,1))<=0

def contained(p,S):
    # Caratheodory in R^2: singleton, segment, or nondegenerate triangle.
    if p in S: return True
    if any(on_segment(p,a,b) for a,b in it.combinations(S,2)): return True
    for a,b,c in it.combinations(S,3):
        d=det(a,b,c)
        if d and all(d*t>=0 for t in (det(a,b,p),det(b,c,p),det(c,a,p))): return True
    return False

def extreme(S):
    return len(S)>=3 and len(set(S))==len(S) and all(not contained(p,S[:i]+S[i+1:]) for i,p in enumerate(S))

def hole(P,S):
    return extreme(S) and set(S)<=set(P) and all(not contained(p,S) for p in P if p not in S)

def area(S):
    return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(S,S[1:]+S[:1])))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('packet',type=Path);a=ap.parse_args()
    sys.dont_write_bytecode=True
    spec=importlib.util.spec_from_file_location('native',a.packet/'check_geometry.py')
    native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
    sets={k:[tuple(p) for p in v] for k,v in json.loads((a.packet/'fixtures.json').read_text())['point_sets'].items()}
    counts={}
    def count(k): counts[k]=counts.get(k,0)+1
    # Definition oracle checks independent of native hull sorting and halfplanes.
    grid=list(it.product(range(4),repeat=2))
    for k in (3,4,5,6):
        for T in it.combinations(grid,k):
            S=list(T)
            ex=extreme(S)
            need(native.strict(S)==ex,'strict-convexity oracle disagreement')
            if k>=5:
                result=hole(grid,S)
                need(native.is_hole(grid,S,k)==result,'closed-hole oracle disagreement')
                need(not result,'independent parity-grid enumeration found hole')
            count('grid_subsets_'+str(k))
    # Every edge replacement preserves GLOBAL extreme points, not merely local turns.
    for k in range(3,11):
        S=[(j,j*j) for j in range(k)]
        for i in range(k):
            u,v=S[i],S[(i+1)%k]
            for t in (F(1,100),F(1,3),F(1,2),F(99,100)):
                p=tuple((1-t)*u[d]+t*v[d] for d in (0,1))
                T=S[:i]+[p]+S[i+1:]
                need(extreme(T),'edge replacement destroyed an extreme vertex')
                need(all(contained(x,S) for x in T),'replacement left original hull')
                need(area(T)<area(S),'replacement failed strict area decrease')
                count('global_edge_replacements')
    # Many simultaneous boundary blockers; native minimum-area outputs checked by oracle.
    for k in range(3,8):
        S=[(j,j*j) for j in range(k)]
        for t in (F(1,3),F(1,2),F(2,3)):
            P=S+[tuple((1-t)*u[d]+t*v[d] for d in (0,1)) for u,v in zip(S,S[1:]+S[:1])]
            T=native.boundary_cleanup(P,S)
            need(len(T)==k and hole(P,T),'independent cleanup output failure')
            need(all(contained(x,S) for x in T),'cleanup hull escaped')
            count('multi_blocker_cleanups')
    H=sets['hexagon']; P=H+sets['boundary_blocker']
    need(extreme(H) and not hole(P,H),'independent edge-blocker rejection failed')
    W=sets['degenerate_six']; need(not extreme(W),'weak boundary six accepted')
    for n in range(1,17):
        e=F(1,2**n);S=[(0,0),(2,-e),(4,0),(2+e,2+e),(0,4),(-e,2)]
        need(hole(S,S),'rational perturbation oracle failed');count('perturbation_scales')
    # All five open ear regions with rational points. Classify without native hull.
    S=sets['pentagon']
    for i in range(5):
        E=[]
        for x,y in it.product(range(-8,17),repeat=2):
            q=(F(x,2),F(y,2));d=[det(u,v,q) for u,v in zip(S,S[1:]+S[:1])]
            if d[i]<0 and all(d[j]>0 for j in range(5) if j!=i): E.append(q)
        need(bool(E),'ear oracle test vacuous')
        P=S+E
        need(hole(P,S),'ear points invaded pentagon')
        q=min(E,key=lambda q:(-det(S[i],S[(i+1)%5],q),q))
        need(hole(P,S+[q]),'nearest-ear oracle failure')
        ni=native.extension_regions(S,q)
        need(len(ni)==1 and native.nearest_ear(P,S,ni[0])==q,'nearest-ear native mismatch')
        count('rational_ear_regions');counts['rational_ear_points']=counts.get('rational_ear_points',0)+len(E)
    q=sets['two_edge_point'][0];need(hole(S+[q],S) and not extreme(S+[q]),'two-edge example false')
    # Affine transformations with positive and negative determinant and rational scale.
    for mapper in (lambda p:(-p[0]+2*p[1],3*p[0]+p[1]),lambda p:(F(p[0],7)+11,F(p[1],3)-2)):
        for name,P in sets.items():
            need(native.strict([mapper(p) for p in P])==extreme(P),'affine strictness disagreement')
            count('affine_fixture_checks')
    print(json.dumps({'status':'PASS','scope':'independent exact finite checks, not universal proofs','counts':counts},sort_keys=True,indent=2))

if __name__=='__main__':
    try: main()
    except (AuditFailure,OSError,ValueError,TypeError,KeyError) as e:
        print(json.dumps({'status':'FAIL','error':str(e)},sort_keys=True));sys.exit(2)
