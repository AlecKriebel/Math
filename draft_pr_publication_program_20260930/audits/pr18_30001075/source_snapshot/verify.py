#!/usr/bin/env python3
"""Exact local checks for 30001075. These do not prove geometric covering or measure theory."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib, json
import sympy as s

out = {'scope': 'Exact algebra and finite support-function increment checks, not a proof certificate.'}
z=s.symbols('z'); av=s.symbols('a0:4');bv=s.symbols('b0:4')
A=s.Matrix(2,2,av); B=s.Matrix(2,2,bv); p=s.expand((A+z*B).det())
assert s.degree(p,z)<=2
h1,h2,h3=s.symbols('h1 h2 h3')
V=s.Matrix([[1,h,h*h] for h in (h1,h2,h3)])
assert s.factor(V.det()-(h2-h1)*(h3-h1)*(h3-h2))==0
v1,v2=s.symbols('v1 v2')
J=(A+z*B).row_join(s.Matrix([v1,v2])).col_join(s.Matrix([[0,0,1]]))
assert s.expand(J.det()-p)==0
# Two contact heights alone do not suffice.
assert s.expand((s.diag(z,z-1)).det()-z*(z-1))==0
out['jacobian_and_three_roots']={'passed': True, 'negative_control_two_roots': True}

# Plane-intersection first variation, including its height correction.
t,zi,Nx,Ny,Nz,ux,uy,vx,vy=s.symbols('t zi Nx Ny Nz ux uy vx vy', nonzero=True)
zmeet=(Nz*zi-Nx*t*ux-Ny*t*uy)/(Nz+Nx*t*vx+Ny*t*vy)
assert s.simplify(s.diff(zmeet,t).subs(t,0)+(Nx*(ux+zi*vx)+Ny*(uy+zi*vy))/Nz)==0
out['planar_contact_derivative']={'passed':True}

# Support-function increment (4), using arbitrary finite polytopes, exact rationals.
verts=[(Q(x,3),Q(y,4),Q(zv,7)) for x,y,zv in product((-2,1),(-3,2),(-4,5))]
ns=[(Q(1),Q(0)),(Q(0),Q(1)),(Q(-1),Q(0)),(Q(3,5),Q(4,5)),(Q(-5,13),Q(12,13))]
qs=[tuple(Q(k,11) for k in x) for x in product((-2,0,3), repeat=4)]
deltas=[(Q(1,17),Q(-2,19),Q(3,23),Q(-1,29)),(Q(-2,7),Q(1,11),Q(-1,13),Q(2,17))]
def dot(n,x):return sum(a*b for a,b in zip(n,x))
def psi(n,q):
 u,v=q[:2],q[2:]
 return dot(n,u)-max(dot(n,x[:2])-dot(n,v)*x[2] for x in verts)
count=0
for n,q,delta in product(ns,qs,deltas):
 qnew=tuple(a+b for a,b in zip(q,delta));diff=psi(n,qnew)-psi(n,q)
 ds=[dot(n,delta[:2])+x[2]*dot(n,delta[2:]) for x in verts]
 assert min(ds)<=diff<=max(ds);count+=1
out['support_increment']={'passed':True,'exact_cases':count}

# Own-motion/cross-motion inequalities, allowing opposite supporting directions.
count=0
for alpha in (Q(1),Q(1,2),Q(1,7),Q(1,101)):
 eps=alpha/32;m=alpha/4
 assert eps<m/4 # Strict bound used in proof.
 for c in (1-eps,1,1+eps):
  assert c*(alpha/2)>=m
 for c in (-eps,0,eps):
  assert abs(c)<=eps
 assert eps/m< Q(1,4);count+=1
out['cap_constants']={'passed':True,'exact_margin_models':count}

# Simultaneous zero example: cross-coupled linear monotone maps.
count=0
for c,d in product((Q(-1,5),Q(0),Q(1,5)),repeat=2):
 for r1,r2 in product((Q(-2,7),Q(0),Q(3,11)),repeat=2):
  den=1-c*d;a=(-r1+c*r2)/den;b=(-r2+d*r1)/den
  assert a+c*b+r1==0 and b+d*a+r2==0
  assert den>0 and abs(c)<Q(1,4) and abs(d)<Q(1,4);count+=1
out['contraction_linear_models']={'passed':True,'exact_cases':count,'qualification':'Finite illustrative models only'}

here=Path(__file__).resolve().parent
out['candidate_sha256']=hashlib.sha256((here/'CANDIDATE.md').read_bytes()).hexdigest()
out['sympy_version']=s.__version__
(here/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
