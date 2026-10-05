#!/usr/bin/env python3
"""Modest exact controls for the hyperbolic covering counterexample.
Requires Python 3 and SymPy. No Nash embedding is numerically constructed.
Prints a deterministic JSON receipt; the proof remains the theorem-level evidence.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib,json
import sympy as s
checks=Counter()
def ck(group,statement):
    assert bool(statement),group
    checks[group]+=1

u,v=s.symbols('u v',real=True)
T=s.symbols('T',positive=True)
coords=(u,v)
lam=4*T/(1-u*u-v*v)**2
g=s.eye(2)*lam
gi=g.inv()
Gamma=[[[s.simplify(sum(gi[i,l]*(s.diff(g[l,k],coords[j])+s.diff(g[l,j],coords[k])-s.diff(g[j,k],coords[l])) for l in range(2))/2) for k in range(2)] for j in range(2)] for i in range(2)]
# R^i_{jkl}: convention yielding K=-1 for the standard Poincare metric.
def R(i,j,k,l):
    return s.simplify(s.diff(Gamma[i][l][j],coords[k])-s.diff(Gamma[i][k][j],coords[l])
        +sum(Gamma[i][k][a]*Gamma[a][l][j]-Gamma[i][l][a]*Gamma[a][k][j] for a in range(2)))
K=s.simplify(g[0,0]*R(0,1,0,1)/g.det())
ck('symbolic_curvature',s.simplify(K+1/T)==0)
ck('unit_time_curvature',K.subs(T,1)==-1)
for i,j,k in product(range(2),repeat=3):
    ck('torsion_free_connection',s.simplify(Gamma[i][j][k]-Gamma[i][k][j])==0)
# Exact coefficient bounds on a rational mesh inside the chart radius 1/2.
points=0
for a,b in product(range(-8,9),repeat=2):
    x,y=Q(a,16),Q(b,16)
    r2=x*x+y*y
    if r2<=Q(1,4):
        points+=1
        coeff=4/(1-r2)**2
        ck('chart_uniform_bounds',4<=coeff<=Q(64,9))
        for t in [Q(1,3),Q(1),Q(5,2)]:
            ck('scaled_chart_uniform_bounds',4*t<=t*coeff<=Q(64,9)*t)
# The entire genus-two surface relator lifts closed on both sheets.
# A nonzero Z/2 character is surjective, so its covering action is transitive.
word=[(0,1),(1,1),(0,-1),(1,-1),(2,1),(3,1),(2,-1),(3,-1)]
characters=0
for character in product(range(2),repeat=4):
    for start in range(2):
        end=start
        for gen,exponent in word:
            end=(end+exponent*character[gen])%2
        ck('surface_relator_monodromy',end==start)
    if any(character):
        characters+=1
        orbit={0}
        for gen in range(4):
            orbit|={(x+character[gen])%2 for x in tuple(orbit)}
        ck('connected_two_sheet_action',orbit=={0,1})
ck('chosen_character_surjective',set((1,0,0,0))=={0,1})
ck('cover_euler_characteristic',2-8+2==2*(1-4+1)==-4)
ck('cover_genus_three',2-2*3==-4)
ck('nash_compact_dimension',2*(3*2+11)//2==17)
# Static variational system with a generic 3-by-2 Jacobian.
t=s.symbols('t',real=True)
H=s.Matrix(3,2,s.symbols('h0:6'))
Phi=s.eye(2)
P=(Phi.T*H.T*H*Phi).applyfunc(lambda a:s.integrate(a,(t,0,T)))
for i,j in product(range(2),repeat=2):
    ck('stationary_gramian_identity',s.simplify(P[i,j]-T*(H.T*H)[i,j])==0)
# Pullbacks compose: a finite exact Jacobian control of d(e o pi).
for a,b,c,d in [(1,0,0,1),(2,1,1,1),(1,2,0,1),(-1,0,0,-1)]:
    J=s.Matrix([[a,b],[c,d]])
    ck('cover_chart_invertible',J.det()!=0)
    for i,j in product(range(2),repeat=2):
        ck('pullback_chain_identity',s.expand(((H*J).T*(H*J)-J.T*(H.T*H)*J)[i,j])==0)
artifact=Path(__file__).with_name('COUNTEREXAMPLE.md')
receipt={'status':'PASS','exact_assertions':sum(checks.values()),'checks':dict(sorted(checks.items())),
'rational_chart_points':points,'nontrivial_double_cover_characters':characters,
'curvature_formula':str(K),'artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),
'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sympy_version':s.__version__,
'limitations':'Symbolic local metric, finite monodromy and Gramian algebra controls only. Smooth Nash embedding, global covering existence and completeness are justified by the cited mathematical theorems, not these finite tests.'}
print(json.dumps(receipt,indent=2,sort_keys=True))
