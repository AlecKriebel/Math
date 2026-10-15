#!/usr/bin/env python3
"""Exact finite controls for canonical vertex rotation and handle surgery.

These controls supplement the general derivation; they do not implement LPVV,
the end-avoidance homeomorphisms, or the submitted full algorithm.
"""
import datetime, hashlib, json, os, pathlib
from fractions import Fraction
BASE=pathlib.Path(__file__).resolve().parent
def cycles(p):
    seen=set(); out=[]
    for x in p:
        if x in seen: continue
        q=[]; y=x
        while y not in seen:
            seen.add(y); q.append(y); y=p[y]
        assert y==x
        out.append(q)
    return out
def det(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def crosses(a,b,c,d):
    return det(a,b,c)*det(a,b,d)<0 and det(c,d,a)*det(c,d,b)<0
assertions=0; cross_checks=0; rows=[]
for g in range(1,65):
    n=4*g
    face={i:(i+1)%n for i in range(n)}
    reverse={4*k+j:4*k+(j+2)%4 for k in range(g) for j in range(4)}
    rotation={i:face[reverse[i]] for i in range(n)}
    cyc=cycles(rotation)
    assert len(cyc)==1; assertions+=1
    assert cyc[0]==[4*k+j for k in range(g) for j in (0,3,2,1)]; assertions+=1
    assert len(cycles({i:rotation[reverse[i]] for i in range(n)}))==1; assertions+=1
    # Distinct rational ports on the convex polygon formed by a parabola arc.
    rank={x:i for i,x in enumerate(cyc[0])}
    point={x:(Fraction(rank[x]),Fraction(rank[x]**2)) for x in range(n)}
    chords=[(4*k+j,reverse[4*k+j],k,j) for k in range(g) for j in (0,1)]
    actual=0
    for i,(a,b,k,j) in enumerate(chords):
        for c,d,l,m in chords[i+1:]:
            expected=(k==l)
            observed=crosses(point[a],point[b],point[c],point[d])
            assert observed==expected,(g,k,l); assertions+=1; cross_checks+=1
            actual+=observed
    assert actual==g; assertions+=1
    # The ribbon order of each separated one-crossing pair has one boundary.
    localrotation={i:(i+1)%4 for i in range(4)}
    localreverse={i:(i+2)%4 for i in range(4)}
    assert len(cycles({i:localrotation[localreverse[i]] for i in range(4)}))==1; assertions+=1
    rows.append({'g':g,'proper_chord_crossings':actual,'closed_surface_chi':2-2*g,
                 'sum_handle_chi':-g,'connected_complement_chi':2-g,
                 'connected_complement_boundary_count':g,'deduced_complement_genus':0})
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),
        'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
        'status':'PASS_EXACT_FINITE_CONTROLS','assertions':assertions,
        'chord_pair_checks':cross_checks,'g_range':[1,64],'cases':rows,
        'limits':'Does not implement LPVV, cap moves, or full basis enumeration. Connectedness is proved in the derivation, not assumed from these Euler counts.'}
(BASE/'LOCAL_SURGERY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
