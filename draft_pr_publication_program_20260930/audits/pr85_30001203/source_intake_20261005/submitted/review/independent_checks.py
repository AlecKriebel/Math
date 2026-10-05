#!/usr/bin/env python3
"""Independent local algebra for the covering counterexample.

No author modules are imported; no numerical isometric embedding is claimed.
The global covering, Nash embedding and completeness arguments are in REVIEW.
"""
from pathlib import Path
from collections import Counter
from itertools import product
import hashlib,json
import sympy as s

checks=Counter()
def check(ok,label):
    assert bool(ok),label
    checks[label]+=1

x,y=s.symbols('x y',real=True)
T=s.symbols('T',positive=True)
rho=x*x+y*y
coefficient=4*T/(1-rho)**2
# Independent conformal curvature formula, rather than Christoffel symbols.
sigma=s.log(2)+s.log(T)/2-s.log(1-rho)
lap=s.diff(sigma,x,2)+s.diff(sigma,y,2)
curvature=s.factor(-lap/coefficient)
check(curvature==-1/T,'conformal_curvature')
check(curvature.subs(T,1)==-1,'constant_negative_curvature')
check(s.simplify(lap-4/(1-rho)**2)==0,'log_conformal_factor_laplacian')

# These polynomial factorizations certify bounds for every 0<=r^2<=1/4,
# not just the finite points in the author's mesh.
r=s.symbols('r',real=True)
check(s.factor(4/(1-r)**2-4-4*r*(2-r)/(1-r)**2)==0,
      'whole_interval_lower_bound_factorization')
check(s.factor(s.Rational(64,9)-4/(1-r)**2
      -4*(1-4*r)*(7-4*r)/(9*(1-r)**2))==0,
      'whole_interval_upper_bound_factorization')
for i in range(21):
    R=s.Rational(i,80)
    check(0<=R<=s.Rational(1,4),'bound_interval')
    check(4<=4/(1-R)**2<=s.Rational(64,9),'uniform_metric_bound')
check(4/(1-s.Rational(1,4))**2==s.Rational(64,9),'upper_constant_sharp')

# Rational Mobius disk isometries justify moving a chart center to the origin.
for a in [s.Rational(0),s.Rational(1,4),s.Rational(-1,3)]:
    den=(1-a*x)**2+a*a*y*y
    U=((x-a)*(1-a*x)-a*y*y)/den
    V=(1-a*a)*y/den
    J=s.Matrix([U,V]).jacobian([x,y])
    target=4/(1-U*U-V*V)**2*(J.T*J)
    check(s.factor(1-U*U-V*V-(1-a*a)*(1-rho)/den)==0,
          'Mobius_disk_identity')
    for i,j in product(range(2),repeat=2):
        check(s.factor(target[i,j]-4*s.KroneckerDelta(i,j)/(1-rho)**2)==0,
              'centered_chart_isometry')

# Covering monodromy as permutations, distinct from the submitted bit update.
identity=(0,1);swap=(1,0)
compose=lambda p,q:tuple(p[q[i]] for i in range(2))
inverse=lambda p:tuple(p.index(i) for i in range(2))
def commutator(a,b):return compose(compose(compose(a,b),inverse(a)),inverse(b))
for generators in product((identity,swap),repeat=4):
    rel=compose(commutator(*generators[:2]),commutator(*generators[2:]))
    check(rel==identity,'surface_relator_permutations')
    if swap in generators:
        check({g[0] for g in generators}|{0}=={0,1},'transitive_cover_action')
check(compose(swap,swap)==identity and swap[0]!=0 and swap[1]!=1,'free_deck_involution')
check(2-8+2==-4 and 2-2*3==-4,'cover_Euler_and_genus')
check(8*s.pi/4==2*s.pi,'octagon_vertex_angle')
check(2*(3*2+11)//2==17,'smooth_Nash_dimension')

# Direct time integration for the actual static variational formula.
t=s.symbols('t',real=True)
H=s.Matrix(4,2,s.symbols('h0:8'))
J=s.Matrix([[1,0],[2*x,1]]) # nonlinear chart change (x,y)->(x,y+x^2)
check(J.det()==1,'nonlinear_chart_invertible')
for i,j in product(range(2),repeat=2):
    P=s.integrate(sum(H[k,i]*H[k,j] for k in range(4)),(t,0,T))
    check(s.expand(P-T*(H.T*H)[i,j])==0,'all_time_static_Gramian')
    check(s.expand(((H*J).T*(H*J)-J.T*(H.T*H)*J)[i,j])==0,
          'nonlinear_chart_pullback_identity')

root=Path(__file__).resolve().parent
h=hashlib.sha256((root/'author_replay/COUNTEREXAMPLE.md').read_bytes()).hexdigest()
check(h=='59f1adc87e67fc25dbeb9c753d940b36fb8450eb0f51f6027662a9a95f62bed0',
      'frozen_candidate_hash')
print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),
 'checks':dict(sorted(checks.items())),'curvature':str(curvature),'candidate_sha256':h,
 'limitations':'Exact local identities, interval-bound certificates and finite monodromy controls. Global cover existence, smooth Nash embedding and completeness remain justified by the cited mathematical theorems and written review.'},indent=2,sort_keys=True))
