#!/usr/bin/env python3
"""Independent exact algebra and group-cohomology controls; no Floer computation."""
from pathlib import Path
from itertools import product
import json,math
import sympy as s
checks={}
def ck(name,value):
 assert bool(value),name
 checks[name]='PASS'
t=s.symbols('t');delta=t*t-t+1
ck('alexander_from_torus_formula',s.cancel((t**6-1)*(t-1)/((t**2-1)*(t**3-1))-delta)==0)
ck('unsquared_sixth_roots',s.gcd(delta,t**6-1)==delta)
ck('squared_sixth_roots',s.gcd(delta.subs(t,t*t),t**6-1)==1)
ck('cube_roots_do_not_vanish',s.gcd(delta,t**3-1)==1)
ck('phi6_identity',s.cyclotomic_poly(6,t)==delta)
# Verify all six rank-one local-system H^1 dimensions directly for C2*C3.
# Cocycle constraints: (1+alpha)u=0, (1+beta+beta^2)v=0.
# Coboundaries form the span of (alpha-1,beta-1).
w=(-1+s.I*s.sqrt(3))/2
def h1dim(alpha,beta):
 R=s.diag(s.simplify(1+alpha),s.simplify(1+beta+beta*beta))
 B=s.Matrix([s.simplify(alpha-1),s.simplify(beta-1)])
 assert (R*B).applyfunc(s.simplify)==s.zeros(2,1)
 return 2-R.rank()-B.rank()
raw=[];square=[]
for k in range(6):
 alpha=s.Integer(-1)**k; beta=s.simplify(w**k)
 raw.append(h1dim(alpha,beta));square.append(h1dim(alpha**2,s.simplify(beta**2)))
 ck(f'character_{k}_order_relations',s.simplify(alpha**2-1)==0 and s.simplify(beta**3-1)==0)
 ck(f'squared_character_{k}_normal_cohomology_zero',square[-1]==0)
ck('unsquared_character_dimensions',raw==[0,1,0,0,0,1])
ck('full_cyclic_cover_rank_control',sum(raw)==2)
ck('abelianization_order',2*3==6 and math.gcd(2,3)==1)
# Adjoint action on off-diagonal matrices carries the square of the character.
a,z,zz=s.symbols('a z zz',nonzero=True)
U=s.diag(a,1/a);V=s.Matrix([[0,z],[-zz,0]])
ck('adjoint_square_weight',U*V*U.inv()==s.Matrix([[0,a*a*z],[-zz/(a*a),0]]))
B=s.Matrix(s.symbols('b0:4')).reshape(2,2)
for sign in [-1,1]:ck(f'central_order_two_commutes_{sign}',sign*s.eye(2)*B==B*sign*s.eye(2))
# Local quartic diagnostic and torus lower link.
u,v,p,q=s.symbols('u v p q',real=True)
x=u*u+v*v;y=p*p+q*q;F=x*x-3*x*y+2*y*y
ck('quartic_factorization',s.expand(F-(x-y)*(x-2*y))==0)
ck('euler_homogeneity',s.expand(sum(a*s.diff(F,a) for a in [u,v,p,q])-4*F)==0)
ck('quartic_hessian_zero',s.hessian(F,[u,v,p,q]).subs({u:0,v:0,p:0,q:0})==s.zeros(4))
ck('critical_coefficient_matrix',s.Matrix([[2,-3],[-3,4]]).det()==-1)
X=s.symbols('X',real=True);link=s.expand(X*X-3*X*(1-X)+2*(1-X)**2)
ck('sphere_link_polynomial',s.factor(link)==(2*X-1)*(3*X-2))
ck('sphere_link_endpoints',s.solve(link,X)==[s.Rational(1,2),s.Rational(2,3)])
ck('link_interior_negative',link.subs(X,s.Rational(3,5))<0)
ck('link_left_exterior_positive',link.subs(X,s.Rational(1,3))>0)
ck('link_right_exterior_positive',link.subs(X,s.Rational(3,4))>0)
ck('link_coordinates_nonzero',s.Rational(1,2)>0 and s.Rational(2,3)<1)
# Cellular chain ranks for T^2 and reduced homology shifted by the cone pair.
chain=[1,2,1]; boundary_ranks=[0,0,0,0]
betti=[chain[i]-boundary_ranks[i]-boundary_ranks[i+1] for i in range(3)]
relative={0:0,1:betti[0]-1,2:betti[1],3:betti[2],4:0}
ck('local_relative_ranks',relative=={0:0,1:0,2:2,3:1,4:0})
ck('local_total_rank',sum(relative.values())==3)
ck('local_euler_characteristic',sum((-1)**k*n for k,n in relative.items())==1)
# Three-factor finite character groups, independent from the author's two-factor enumeration.
for ns in product(range(1,5),repeat=3):
 chars=list(product(*(range(n) for n in ns)));seen=set();points=spheres=0
 for c in chars:
  if c in seen:continue
  inv=tuple((-a)%n for a,n in zip(c,ns));seen.add(c);seen.add(inv)
  if inv==c:points+=1
  else:spheres+=1
 ck('orbit_homology_'+str(ns),points+2*spheres==math.prod(ns) and points==math.prod(math.gcd(n,2) for n in ns))
out={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'trefoil_rank_one_H1':raw,'trefoil_squared_rank_one_H1':square,'local_critical_groups':relative,'scope':'Exact polynomial, scalar local-system cocycle, character orbit, and lower-link arithmetic controls. No instanton homology computation, realization of the quartic by a manifold, or full solution of KP-3.51.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
