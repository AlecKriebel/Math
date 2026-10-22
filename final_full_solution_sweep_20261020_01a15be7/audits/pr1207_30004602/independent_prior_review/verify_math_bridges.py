#!/usr/bin/env python3
"""Read-only, self-authored exact arithmetic checks; finite support, not a universal proof."""
from fractions import Fraction
import json

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def add(*polys):
    out = {}
    for p in polys:
        for e, c in p.items():
            out[e] = out.get(e, 0) + c
    return {e: c for e, c in out.items() if c}

def mul(a, b):
    out = {}
    for u, c in a.items():
        for v, d in b.items():
            e = tuple(x+y for x, y in zip(u, v))
            out[e] = out.get(e, 0) + c*d
    return {e: c for e, c in out.items() if c}

def monomials(degree):
    return [(a,b,degree-a-b) for a in range(degree,-1,-1)
            for b in range(degree-a,-1,-1)] if degree >= 0 else []

def rank(columns):
    if not columns:
        return 0
    mat = [[Fraction(x) for x in row] for row in zip(*columns)]
    lead = 0
    for col in range(len(columns)):
        pivot = next((i for i in range(lead,len(mat)) if mat[i][col]), None)
        if pivot is None:
            continue
        mat[lead],mat[pivot] = mat[pivot],mat[lead]
        scale = mat[lead][col]
        mat[lead] = [v/scale for v in mat[lead]]
        for i in range(lead+1,len(mat)):
            scale = mat[i][col]
            if scale:
                mat[i] = [a-scale*b for a,b in zip(mat[i],mat[lead])]
        lead += 1
        if lead == len(mat):
            break
    return lead

def columns(polys,degree):
    basis=monomials(degree)
    return [[q.get(e,0) for e in basis] for q in polys]

def ideal_columns(gens,degree):
    polys=[]
    for g in gens:
        gd=sum(next(iter(g)))
        polys.extend(mul(g,{m:1}) for m in monomials(degree-gd))
    return columns(polys,degree)

x={(1,0,0):1};y={(0,1,0):1};z={(0,0,1):1};s=add(x,y,z)
q=[mul(mul(y,z),s),mul(mul(x,z),s),mul(mul(x,y),s),mul(mul(x,y),z)]
f=[add(a,q[3]) for a in q[:3]]
require(rank(columns(q,3))==4,'four saturation generators independent')
require(rank(columns(f,3))==3,'three partial derivatives independent')
for v,a in zip([x,y,z],q[:3]):
    require(mul(v,a)==mul(s,q[3]),'all-degree annihilator identity')
points=[(0,0,1),(0,1,0),(1,0,0),(0,1,-1),(1,0,-1),(1,-1,0)]
eval_cols=[[p[0]**m[0]*p[1]**m[1]*p[2]**m[2]
            for p in points] for m in monomials(2)]
require(rank(eval_cols)==6,'quadratic interpolation')
ell=add(x,{e:2*c for e,c in y.items()},{e:3*c for e,c in z.items()})
ell_values=[p[0]+2*p[1]+3*p[2] for p in points]
require(all(ell_values),'ell avoids six nodes')
rows=[]
for degree in range(10):
    ji=ideal_columns(f,degree);si=ideal_columns(q,degree)
    jnext=ideal_columns(f,degree+1)
    image=columns([mul(ell,{m:1}) for m in monomials(degree)],degree+1)
    h=len(monomials(degree))-rank(ji)
    hs=len(monomials(degree))-rank(si)
    hn=len(monomials(degree+1))-rank(jnext)
    multiplication_rank=rank(jnext+image)-rank(jnext)
    require(h==[1,3,6,7][degree] if degree<4 else h==6,'Jacobian Hilbert prefix')
    require(hs==[1,3][degree] if degree<2 else hs==6,'saturation Hilbert prefix')
    require(rank(si)-rank(ji)==(1 if degree==3 else 0),'torsion prefix')
    require(multiplication_rank==min(h,hn),'four-line WLP finite check')
    rows.append({'source_degree':degree,'M_dimension':h,'A_dimension':hs,'N_dimension':rank(si)-rank(ji),'ell_rank':multiplication_rank})
syzygies=[]
for total_degree in range(3,6):
    nullity=3*len(monomials(total_degree-3))-rank(ideal_columns(f,total_degree))
    syzygies.append([total_degree,nullity])
require([n for _,n in syzygies]==[0,0,3],'minimum syzygy degree5')

# Bounded enumeration tests implementation of the independently proved inequalities.
# It is not a claim that every enumerated integer pair comes from a bundle.
counts={'unstable':0,'semistable_even':0,'semistable_odd':0}
for D in range(3,121):
    for m in range(1,D+1):
        for p in range(max(0,D-m-1)):
            require(p<=D-m-2,'saturation premise')
            if 2*m<D:
                c=max(p,m-2)
                require(c<=D-m-2,'unstable overlap')
                require(c>=p and c>=m-2,'unstable surjection overlap')
                counts['unstable']+=1
            else:
                c=(D-3)//2;r=D//2
                inject_end=r-2
                surject_start=r-2 if D%2==0 else r-1
                require(p<=c and c-1<=inject_end and c>=surject_start,'semistable overlap')
                counts['semistable_even' if D%2==0 else 'semistable_odd']+=1
            for i in [c-1,c,c+1]:
                j=D-i-4
                require(D-j-4==i,'duality involution source shift')
print(json.dumps({'status':'PASS','scope':'finite corroboration only; see REPORT.md for universal deductions','four_line':rows,'ell_values':ell_values,'syzygy_nullities':syzygies,'threshold_grid_D_max':120,'threshold_cases':counts,'candidate_or_author_code_executed':False},indent=2))
