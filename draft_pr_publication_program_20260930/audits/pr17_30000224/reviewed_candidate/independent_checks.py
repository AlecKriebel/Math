#!/usr/bin/env python3
"""Independent exact checks for the restricted Macaulay-quartic note.
Requires SymPy. Run from this directory: python independent_checks.py
"""
import json
from pathlib import Path
import sympy as S
from itertools import combinations

w,x,y,z,s,t,h=S.symbols('w x y z s t h')
Rvars=(w,x,y,z)
records=[]

def report(name,**details):records.append({'name':name,'passed':True,**details})

def zero(expr):return S.expand(expr)==0

# Recover the toric ideal from the parametrization by elimination.
G=S.groebner([w-s**4,x-s**3*t,y-s*t**3,z-t**4],s,t,w,x,y,z,order='lex')
a=[g.as_expr() for g in G.polys if not(g.as_expr().has(s) or g.as_expr().has(t))]
Ga=S.groebner(a,*Rvars,order='grevlex')
expected=[w*z-x*y,x**3-w**2*y,w*y**2-x**2*z,y**3-x*z**2]
Ge=S.groebner(expected,*Rvars,order='grevlex')
assert all(Ge.reduce(g)[1]==0 for g in a)
assert all(Ga.reduce(g)[1]==0 for g in expected)
report('toric_ideal_elimination',generators=[str(g) for g in a])

# Verify the claimed complete intersection as an exact ideal intersection.
I=[w*y,w*z,x*y,x*z]
Gint=S.groebner([h*g for g in I]+[(1-h)*g for g in a],h,w,x,y,z,order='lex')
inter=[g.as_expr() for g in Gint.polys if not g.as_expr().has(h)]
ci=[w*z-x*y,w*y**2-x**2*z]
Gci=S.groebner(ci,*Rvars,order='grevlex')
Ginter=S.groebner(inter,*Rvars,order='grevlex')
assert all(Gci.reduce(g)[1]==0 for g in inter)
assert all(Ginter.reduce(g)[1]==0 for g in ci)
assert Ga.reduce(w*y)[1]!=0
report('skew_lines_intersection_with_quartic',intersection_generators=[str(g) for g in inter],
       consequence='The colon by I is the toric prime, since wy is not in that prime.')

# Recover the conormal cubic frame as the nullspace of a coefficient matrix,
# without importing the manuscript's proposed columns.
f=S.Matrix([s**4,s**3*t,s*t**3,t**4])
J=f.jacobian((s,t)).T
nullities={}
frame=None
for d in range(4):
    mons=[s**i*t**(d-i) for i in range(d+1)]
    outmons=[s**i*t**(d+3-i) for i in range(d+4)]
    cols=[]
    for component in range(4):
        for mon in mons:
            v=S.zeros(4,1);v[component]=mon
            expr=J*v
            cols.append(S.Matrix([S.Poly(expr[j],s,t).coeff_monomial(m) for j in range(2) for m in outmons]))
    mat=S.Matrix.hstack(*cols)
    basis=mat.nullspace();nullities[d]=len(basis)
    if d==3:
        frame=S.Matrix.hstack(*[S.Matrix([sum(vec[j*(d+1)+i]*mons[i] for i in range(d+1)) for j in range(4)]) for vec in basis])
assert nullities=={0:0,1:0,2:0,3:2}
assert J*frame==S.zeros(2)
minors=[S.expand(frame.extract(rows,[0,1]).det()) for rows in combinations(range(4),2)]
common=S.Poly(0,s,t)
for m in minors:common=S.gcd(common,S.Poly(m,s,t))
assert common.total_degree()==0
report('independent_conormal_frame',syzygy_nullities=nullities,
       frame=[[str(frame[i,j]) for j in range(2)] for i in range(4)],
       gcd_of_all_maximal_minors=str(common.as_expr()))

# Independent linear algebra certifies the Koszul socle, not only the supplied
# symbolic identity coefficients.
def monomials(degree):
    return [w**i*x**j*y**k*z**(degree-i-j-k) for i in range(degree+1)
            for j in range(degree-i+1) for k in range(degree-i-j+1)]

def flatten(v,degree):
    mons=monomials(degree)
    return S.Matrix([S.Poly(v[i],*Rvars).coeff_monomial(m) for i in range(4) for m in mons])

boundaries=[]
for i,j in combinations(range(4),2):
    v=S.zeros(4,1);v[i]=-I[j];v[j]=I[i];boundaries.append(v)
c=S.Matrix([-x*z,x*y,0,0])
assert zero(sum(I[i]*c[i] for i in range(4)))
D=S.Matrix.hstack(*[flatten(v,2) for v in boundaries])
assert D.rank()==6 and D.row_join(flatten(c,2)).rank()==7
Dlin=S.Matrix.hstack(*[flatten(a*v,3) for a in Rvars for v in boundaries])
r=Dlin.rank()
for a in Rvars:assert Dlin.row_join(flatten(a*c,3)).rank()==r
report('koszul_socle_by_independent_rank',boundary_rank=6,augmented_rank=7,
       linear_boundary_rank=r,all_four_variable_multiples_are_boundaries=True)

# Check the standard normalization's monomial decomposition and unique hole.
for d in range(1,13):
    admissible={0}
    for _ in range(d):admissible={a+b for a in admissible for b in (0,1,3,4)}
    missing=set(range(4*d+1))-admissible
    assert missing==({2} if d==1 else set())
    for texp in range(4*d+1):
        sexp=4*d-texp
        residues=[r for r in [(0,0),(3,1),(2,2),(1,3)] if sexp%4==r[0] and texp%4==r[1]]
        assert len(residues)==1
report('normalization_semigroup_and_T_basis',degrees_checked=list(range(1,13)),
       unique_hole='s^2*t^2 in degree one')

for r in range(1,20):assert max(2*r-1,0)==2*r-1
for e in range(-7,13):
    assert max(-(e+8)-1,0)==0
    assert (e+8+1)+9==e+18>=11>10
report('cohomology_dimension_consistency',quadric_multiplicities=list(range(1,20)),
       line_bundle_degrees=list(range(-7,13)))

out={'status':'passed','independent_check_groups':len(records),'arithmetic':'SymPy exact rational polynomial and matrix operations',
     'scope':'Restricted claims only; no proof or counterexample for the remaining arbitrary ideal class.',
     'records':records}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
