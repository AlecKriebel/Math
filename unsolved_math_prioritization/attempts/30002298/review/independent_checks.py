#!/usr/bin/env python3
"""Exact independent controls; no replacement for the cone kernel theorem."""
from itertools import product, permutations
from collections import Counter
from pathlib import Path
import json
import sympy as s
counts=Counter()
def ck(v,key):
    assert bool(v),key
    counts[key]+=1

# All 256 unions of coordinate orthants, with all eight generic sign chambers
# for the flipping direction. Each full orthant has coefficient +/- 1/prod(u).
signs=list(product((-1,1),repeat=3))
fan_masks=[]
for mask in range(256):
    selected=[z for j,z in enumerate(signs) if mask & (1<<j)]
    alternating=sum(s.prod(z) for z in selected)
    for eta in signs:
        eps=[s.prod(eta[i]*z[i] for i in range(3)) for z in selected]
        signed_coverage=sum(eps)
        ck(signed_coverage==s.prod(eta)*alternating,'flipped_chamber_weight')
        ck((signed_coverage==0)==(alternating==0),'generic_direction_zero_invariance')
    fan_masks.append(int(alternating))

# Finite affine-pole controls at the common apex of unions of orthant tetrahedra.
# Work before imposing L=1-v.u: the common numerator is elementary and exact.
L,x,y,z=s.symbols('L x y z')
variables=(x,y,z)
for mask in range(1,256):
    selected=[a for j,a in enumerate(signs) if mask & (1<<j)]
    N=s.Poly(s.expand(sum(s.prod(L+a[i]*variables[i] for i in range(3))
                             for a in selected)),L,x,y,z)
    constant=s.expand(N.as_expr().subs(L,0))
    ck(constant==s.prod(variables)*fan_masks[mask],'common_apex_residue_numerator')
    ck((constant==0)==(fan_masks[mask]==0),'apex_cancellation_iff_cone_zero')
    # Each used outer axis vertex survives its corresponding factor.
    for i in range(3):
        for a in (-1,1):
            used=any(q[i]==a for q in selected)
            restricted=s.expand(N.as_expr().subs(L,a*variables[i]))
            ck((restricted!=0)==used,'outer_vertex_factor_presence')

# Opposite-orthant parity, including dimensions outside the author's examples.
for d in range(1,8):
    for signs_d in product((-1,1),repeat=d):
        total=s.prod(signs_d)+s.prod([-a for a in signs_d])
        ck((total==0)==bool(d%2),'opposite_cone_dimension_parity')

def dot(v,u):return sum(a*b for a,b in zip(v,u))
def simplex_F(V,u):
    B=s.Matrix.hstack(*(s.Matrix(w)-s.Matrix(V[0]) for w in V[1:]))
    return abs(B.det())/s.prod(1-dot(w,u) for w in V)

# Independent box integration formula from repeated one-dimensional primitives,
# checked against a standard permutation triangulation and exact moments.
box_cases=[]
for d in (1,2,3):
    u=s.symbols('u0:'+str(d))
    for a,b in [(tuple(0 for _ in range(d)),tuple(i+1 for i in range(d))),
                (tuple(i+2 for i in range(d)),tuple(2*i+4 for i in range(d)))]:
        corners=[tuple(b[i] if e[i] else a[i] for i in range(d)) for e in product((0,1),repeat=d)]
        finite_difference=sum((-1)**(d-sum(e))/(1-dot(tuple(b[i] if e[i] else a[i] for i in range(d)),u))
                              for e in product((0,1),repeat=d))/s.prod(u)
        simplices=[]
        for perm in permutations(range(d)):
            V=[a];cur=list(a)
            for j in perm:
                cur=cur.copy();cur[j]=b[j];V.append(tuple(cur))
            simplices.append(V)
        F=s.cancel(sum(simplex_F(V,u) for V in simplices))
        ck(s.cancel(F-finite_difference)==0,'box_direct_integration_identity')
        numerator,denominator=s.fraction(F)
        D=s.expand(denominator/denominator.subs(dict.fromkeys(u,0)))
        expected=s.expand(s.prod(1-dot(v,u) for v in corners))
        ck(s.expand(D-expected)==0,'box_exact_reduced_denominator')
        ck(s.gcd(s.Poly(numerator,*u),s.Poly(denominator,*u)).total_degree()==0,'box_reduced_coprimality')
        for I in product(range(3),repeat=d):
            if sum(I)>2:continue
            derivative=F
            for q,n in zip(u,I):derivative=s.diff(derivative,q,n)
            coefficient=derivative.subs(dict.fromkeys(u,0))/s.prod(s.factorial(n) for n in I)
            moment=s.prod(s.Rational(b[j]**(I[j]+1)-a[j]**(I[j]+1),I[j]+1) for j in range(d))
            predicted=s.factorial(sum(I)+d)/s.prod(s.factorial(n) for n in I)*moment
            ck(s.simplify(coefficient-predicted)==0,'box_exact_low_moments')
        box_cases.append({'dimension':d,'lower':a,'upper':b,'simplices':len(simplices)})

# Origin exception in d=3, independently obtained from the signed-orthant numerator.
for v in [(0,0,0),(2,3,5),(-2,1,4)]:
    U=(x,y,z);lv=1-dot(v,U)
    F=s.cancel((s.prod(lv+q for q in U)+s.prod(lv-q for q in U))
               /(lv*s.prod(lv*lv-q*q for q in U)))
    n,d=s.fraction(F);omega=s.expand(d/d.subs({x:0,y:0,z:0}))
    outer=[tuple(v[j]+a*int(i==j) for j in range(3)) for i in range(3) for a in (-1,1)]
    product_outer=s.expand(s.prod(1-dot(w,U) for w in outer))
    ck(s.expand(omega-product_outer)==0,'opposite_tetrahedra_outer_factors')
    ck((s.expand(omega-lv*product_outer)==0)==(v==(0,0,0)),'origin_unit_exception')
    ck(s.cancel(F-2*(lv**2+x*y+x*z+y*z)/s.prod(lv**2-q**2 for q in U))==0,
       'explicit_tetrahedra_formula')
# The signed indicator identity on all open coordinate orthants.
for h in product((0,1),repeat=3):
    h1,h2,h3=h
    ck(h1*h2*h3+(1-h1)*(1-h2)*(1-h3)==1-h1-h2-h3+h1*h2+h1*h3+h2*h3,
       'explicit_signed_line_cone_identity')
out={'status':'PASS','exact_assertions':sum(counts.values()),'failed':0,
     'categories':dict(counts),'orthant_union_masks':256,'flip_directions_per_mask':8,
     'nonempty_apex_pole_models':255,'direct_integral_box_cases':box_cases,
     'sympy_version':s.__version__,'scope':'Finite exact cone-flipping, cancellation, integration and normalization controls. The general geometric theorem is audited in REVIEW.md.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['categories','direct_integral_box_cases']},indent=2))
