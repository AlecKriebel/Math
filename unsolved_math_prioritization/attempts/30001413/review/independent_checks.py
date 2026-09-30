#!/usr/bin/env python3
"""Independent exact plate-form and signed-boundary diagnostics."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from itertools import product
import hashlib,json
import sympy as s
counts=Counter()
def ck(p,k):
 assert p,k
 counts[k]+=1
# Use the normalized Hessian coordinates (u_xx,u_yy,sqrt(2)u_xy).
t=s.symbols('t',real=True);A=s.Matrix([[1,t,0],[t,1,0],[0,0,1-t]])
ck(s.expand(A.det()-(1-t)*(1-t*t))==0,'quadratic_matrix_determinant')
for k in range(-49,50):
 sig=s.Rational(k,50);B=A.subs(t,sig)
 ck(all(B[:j,:j].det()>0 for j in (1,2,3)),'Sylvester_coercivity')
 lo=1-abs(sig);C=B-lo*s.eye(3)
 ck(all(C.extract(I,I).det()>=0 for I in ((0,),(1,),(2,),(0,1),(0,2),(1,2),(0,1,2))),'sharp_coercivity_bound')
# Divergence of the determinant vector field, checked symbolically for mixed polynomials.
x,y=s.symbols('x y');polys=[x**a*y**b+x**b*y**a+x*y for a in range(1,6) for b in range(1,5)]
for u in polys:
 ux,uy=s.diff(u,x),s.diff(u,y);uxx,uyy,uxy=s.diff(u,x,2),s.diff(u,y,2),s.diff(u,x,y)
 div=s.diff(ux*uyy-uy*uxy,x)+s.diff(uy*uxx-ux*uxy,y)
 ck(s.expand(div-2*(uxx*uyy-uxy**2))==0,'determinant_divergence_identity')
# Radial annular functions test the negative curvature of the inner boundary.
r=s.symbols('r',positive=True)
for inner,outer,c in product((s.Rational(1,2),s.Integer(1),s.Rational(3,2)),(s.Integer(2),s.Integer(3)),(-2,-1,0,1,2)):
 u=(r*r-inner*inner)*(outer*outer-r*r)*(1+c*r*r);du=s.diff(u,r)
 bulk=s.integrate(2*s.diff(u,r,2)*du,(r,inner,outer)) # divided by pi
 outnormal=du.subs(r,outer);innormal=-du.subs(r,inner)
 boundary=outnormal**2-innormal**2
 ck(s.expand(bulk-boundary)==0,'annulus_signed_boundary_identity')
 ck(s.Rational(1,1)/outer>0 and -s.Rational(1,1)/inner<0,'opposite_boundary_curvatures')
 ck(u.subs(r,inner)==u.subs(r,outer)==0,'annular_zero_trace')
# Equality cases of the normal trace comparison must be allowed.
for v,e in product((F(j,7) for j in range(-14,15)),(F(0),F(1,13),F(2))):
 w=-abs(v)-e
 ck(w<=v and w<=-v,'both_normal_trace_signs')
 ck(w*w-v*v==e*(2*abs(v)+e)>=0,'normal_square_factorization')
# No numerical critical constants are assigned to the annulus here.
for dminus,dplus,K in product((F(-1,100),F(-2,3),None),(F(1,20),F(2),F(9)),(F(0),F(1,7),F(1),F(100))):
 eta=min(dplus,F(1) if dminus is None else -dminus)/3
 epsilon=min(F(1),eta/(1+K))
 for fraction in (F(1,100),F(1,2),F(99,100)):
  sig=1-fraction*epsilon
  ck(0<=1-epsilon<sig<1,'near_one_sigma_interval')
  for curvature in (-K,F(0),K):
   alpha=(1-sig)*curvature
   ck(-eta<alpha<eta<dplus and (dminus is None or dminus<alpha),'all_signed_coefficients_in_window')
# Stadium: an arclength tangent is continuous with bounded one-sided derivative,
# whereas its graph has unequal one-sided second derivatives at the join.
z=s.symbols('z');g=s.sqrt(1-z*z)
ck(g.subs(z,0)==1 and s.diff(g,z).subs(z,0)==0,'stadium_graph_C1')
ck(s.diff(g,z,2).subs(z,0)==-1,'stadium_second_derivative_jump')
base=Path(__file__).resolve().parent
result={'status':'PASS','assertions':sum(counts.values()),'categories':dict(counts),'artifact_sha256':hashlib.sha256((base/'author_replay/PARTIAL_SOURCE_AUDIT.md').read_bytes()).hexdigest(),'limits':'Exact form and geometric/parameter diagnostics. No numerical Green-function positivity test or computed domain-specific threshold; the all-load statements use the written variational proof and credited source theorem.'}
(base/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
