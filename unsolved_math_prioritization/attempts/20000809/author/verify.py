#!/usr/bin/env python3
"""Exact reproducible controls for the authored Hilbert-weight report.
Python 3.10+ standard library only. No network or third-party inputs required.
The controls supplement, rather than replace, the mathematical proofs.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path

checks = 0
def check(ok, label):
    global checks
    checks += 1
    if not ok:
        raise AssertionError(label)

def add(a, b): return tuple(x+y for x,y in zip(a,b))
def sub(a, b): return tuple(x-y for x,y in zip(a,b))
def divides(a, b): return all(x<=y for x,y in zip(a,b))
def member(m, gens): return any(divides(g,m) for g in gens)
def monomials(n, degree):
    if n == 1:
        yield (degree,)
    else:
        for a in range(degree+1):
            for t in monomials(n-1,degree-a):
                yield (a,)+t

def rank(rows, cols):
    pivots = {}
    for row in rows:
        v = {i:Fraction(x) for i,x in row.items() if x}
        while v:
            j=min(v)
            if j not in pivots:
                x=v[j]; pivots[j]={i:y/x for i,y in v.items()}; break
            x=v[j]
            for i,y in pivots[j].items():
                v[i]=v.get(i,Fraction(0))-x*y
                if not v[i]: del v[i]
    return len(pivots)

def hom_weights(gens, targets, quotient_gens):
    """Kernel of all Taylor pair-syzygies, split by fine character.
    targets[i] lists possible monomial images of generator i.
    """
    groups=defaultdict(list)
    for i,g in enumerate(gens):
        for b in targets[i]: groups[sub(b,g)].append((i,b))
    result=[]
    for w,arrows in sorted(groups.items()):
        rows=defaultdict(dict)
        for col,(i,b) in enumerate(arrows):
            for j,g in enumerate(gens):
                if i==j: continue
                lcm=tuple(max(a,c) for a,c in zip(gens[i],g))
                out=add(b,sub(lcm,gens[i]))
                if not member(out,quotient_gens):
                    key=(min(i,j),max(i,j),out)
                    rows[key][col]=1 if i<j else -1
        r=rank(rows.values(),len(arrows)); mult=len(arrows)-r
        if mult: result.append({'weight':list(w),'multiplicity':mult})
    return result

I=[(2,0),(1,3),(0,4)]
B=[(0,0),(1,0),(0,1),(1,1),(0,2),(1,2),(0,3)]
check(len(B)==7,'length seven')
check(set(B)=={m for d in range(6) for m in monomials(2,d) if not member(m,I)},'complete standard basis')
for g in I:
    if g[1]: check(member((g[0]+1,g[1]-1),I),'strong stability')
W=hom_weights(I,[B]*3,I)
check(sum(q['multiplicity'] for q in W)==14,'full affine tangent dimension')
wd={tuple(q['weight']):q['multiplicity'] for q in W}
check(wd[(-1,2)]>0 and wd[(1,-2)]>0,'opposite full-torus weights')
# Explicit maps: first generator to xy^2, or last generator to xy^2.
for images in [[(1,2),None,None],[None,None,(1,2)]]:
    for i,j in combinations(range(3),2):
        lcm=tuple(max(a,b) for a,b in zip(I[i],I[j]))
        val=[]
        for k in (i,j):
            m=add(images[k],sub(lcm,I[k])) if images[k] is not None else None
            val.append(None if m is None or member(m,I) else m)
        check(val[0]==val[1],'explicit tangent map respects every syzygy')
J=[g+(0,) for g in I]
HF=[sum(not member(m,J) for m in monomials(3,d)) for d in range(10)]
check(HF==[1,3,5,7,7,7,7,7,7,7],'projective Hilbert function')
naive_targets=[[m for m in monomials(3,sum(g)) if not member(m,J)] for g in J]
Wnaive=hom_weights(J,naive_targets,J)
check(sum(q['multiplicity'] for q in Wnaive)==12,'untruncated homogeneous Hom is too small')
check(all(3*q['weight'][0]+2*q['weight'][1]<0 for q in Wnaive),'naive Hom falsely passes half-space test')
check(any(3*q['weight'][0]+2*q['weight'][1]>=0 for q in W),'actual tangent fails naive certificate')
trunc=[]
for d in (4,7):
    G=[m for m in monomials(3,d) if member(m,J)]
    T=[m for m in monomials(3,d) if not member(m,J)]
    weights=hom_weights(G,[T]*len(G),J)
    check(sum(q['multiplicity'] for q in weights)==14,'truncation tangent dimension')
    lifted=sorted([{'weight':q['weight']+[-sum(q['weight'])], 'multiplicity':q['multiplicity']} for q in W],key=lambda q:q['weight'])
    check(weights==lifted,'truncation recovers every affine weight')
    trunc.append({'degree':d,'number_of_generators':len(G),'weights':weights})
# The known nonsegment certificate is valid at every tested degree >=4.
for d in range(4,15):
    u=(2,0,d-2);v=(0,4,d-4);w=(1,2,d-3)
    check(member(u,J) and member(v,J) and not member(w,J),'segment memberships')
    check(add(u,v)==add(w,w),'equal-product segment obstruction')
# Explicit distracted seven-point set for I at t=1, a_i=i.
points=B
for beta in points:
    for alpha in I:
        product=1
        for x,a in zip(beta,alpha):
            for j in range(a): product*=x-j
        check(product==0,'distraction vanishes on every standard-grid point')
E=[{j:(p[0]**b[0])*(p[1]**b[1]) for j,b in enumerate(B)} for p in points]
check(rank(E,len(B))==7,'evaluation basis on seven distinct points')
# A maximal-rank quadratic evaluation control for generic seven plane points.
generic_points=[(0,0),(1,0),(2,0),(0,1),(0,2),(1,1),(2,3)]
Q=[(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]
check(rank([{j:p[0]**b[0]*p[1]**b[1] for j,b in enumerate(Q)} for p in generic_points],6)==6,'general degree-two Hilbert value is six')
# All distinct-part partitions through six give exact strictly negative weights
# for an integer cocharacter. This is a bounded enumeration, not novelty evidence.
def strict_parts(n,maximum=None):
    if n==0:
        yield ();return
    for a in range(min(n,maximum if maximum is not None else n),0,-1):
        for rest in strict_parts(n-a,a-1): yield (a,)+rest
small=[]
for length in range(1,7):
    for heights in strict_parts(length):
        basis=[(i,j) for i,h in enumerate(heights) for j in range(h)]
        gens=[(len(heights),0)]+[(i,h) for i,h in enumerate(heights)]
        weights=hom_weights(gens,[basis]*len(gens),gens)
        check(sum(q['multiplicity'] for q in weights)==2*length,'small plane tangent dimension')
        witnesses=[(a,b) for a in range(1,31) for b in range(1,31) if all(q['weight'][0]*a+q['weight'][1]*b<0 for q in weights)]
        check(bool(witnesses),'small strongly stable ideal has a separating cocharacter')
        small.append({'length':length,'column_heights':list(heights),'negative_cocharacter':list(witnesses[0])})
# The credited odd-length family has the same obstruction, checked here for
# 3 <= m <= 12; the report proves it for every m >= 3.
family=[]
for m in range(3,13):
    gens=[(2,0),(1,m),(0,m+1)]
    basis=[(0,j) for j in range(m+1)]+[(1,j) for j in range(m)]
    weights=hom_weights(gens,[basis]*3,gens)
    ww={tuple(q['weight']):q['multiplicity'] for q in weights}
    check(sum(ww.values())==4*m+2,'odd family tangent dimension')
    check(ww.get((-1,2),0)>0 and ww.get((1,-2),0)>0,'odd family opposite weights')
    family.append({'m':m,'length':2*m+1,'tangent_dimension':4*m+2})
# Deliberate wrong assertions are rejected; each is a directly false candidate.
negative_controls=[
 ('whole_scheme_tangent_equals_untruncated',12==14),
 ('all_weights_strictly_positive_pairing',all(w[0]+2*w[1]>0 for w in [(-1,2),(1,-2)])),
 ('source_point_can_be_forced_by_sign_flip',all(-w[0]-2*w[1]>0 for w in [(-1,2),(1,-2)])),
 ('example_is_segment_product_distinct',add((2,0,2),(0,4,0))!=add((1,2,1),(1,2,1))),
 ('example_has_generic_quadratic_hilbert_function',HF[2]==6),
]
for name,incorrect in negative_controls: check(not incorrect,'reject '+name)
result={'status':'PASS_EXACT_SUPPLEMENTARY_CONTROLS','assertion_count':checks,
        'affine_tangent_weights':W,'untruncated_homogeneous_weights':Wnaive,
        'projective_hilbert_function_degrees_0_through_9':HF,
        'truncations':trunc,'small_plane_certificates':small,
        'negative_controls_rejected':[n for n,_ in negative_controls],
        'odd_family_controls':family,
        'scope':'No computation here proves the general AIM rationality question; see PROOFS.md.'}
print(json.dumps(result,indent=2,sort_keys=True))
