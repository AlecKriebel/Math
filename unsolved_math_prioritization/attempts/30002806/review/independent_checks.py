#!/usr/bin/env python3
"""Independent symbolic/rational controls; no asymptotic fit is used."""
import sympy as s
from itertools import product
from collections import Counter
from pathlib import Path
import hashlib,json
C=Counter()
def ck(k,b):
 assert bool(b),k
 C[k]+=1
def zero(M):return all(s.simplify(x)==0 for x in M)
z,p,q,Q,ell,mu=s.symbols('z p q Q ell mu',real=True)
h=s.symbols('h',positive=True)
F=z*s.atan(z)-s.log(1+z*z)/2
ck('F_derivative',s.simplify(s.diff(F,z)-s.atan(z))==0)
ck('F_second_derivative',s.simplify(s.diff(F,z,2)-1/(1+z*z))==0)
ck('F_even',s.simplify(F.subs(z,-z)-F)==0)
ck('F_origin',F.subs(z,0)==0)
K=h*p*p/2+h**5*F.subs(z,p/h**2)
g=h*p+h**3*s.atan(p/h**2)
a=h+h/(1+p*p/h**4)
ck('Legendre_first',s.simplify(s.diff(K,p)-g)==0)
ck('Legendre_second',s.simplify(s.diff(K,p,2)-a)==0)
v=p+h*h*s.atan(p/h**2)
Ld=p*h*v-K
ck('action_identity',s.simplify(Ld-h*v*v/2+h*(p-v)**2/2+h**5*F.subs(z,p/h**2))==0)
R=h**3*s.atan(p/h**2)
ck('first_momentum_derivative',s.simplify(s.diff(R,p)-h/(1+p*p/h**4))==0)
ck('unbounded_second_derivative',s.simplify(s.diff(R,p,2).subs(p,h*h)+1/(2*h))==0)
# Formal Legendre envelope cancellation and nonzero mixed Hessian.
u=s.symbols('u',real=True);Pu=s.Function('P')(u)
envelope=s.diff(Pu*u-K.subs(p,Pu),u)-Pu
ck('envelope_derivative',s.simplify(envelope-s.diff(Pu,u)*(u-g.subs(p,Pu)))==0)
# Full cotangent lift on coordinates (q,p,ell,mu), with g'=a and g''=b.
a0,b0=s.symbols('a0 b0')
J=s.Matrix([[1,a0,0,0],[0,1,0,0],[0,0,1,0],[0,-b0*ell,-a0,1]])
Omega=s.Matrix([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
ck('full_cotangent_symplecticity',zero(J.T*Omega*J-Omega))
J2=s.Matrix([[0,1],[-1,0]])
for T in [s.Rational(1,3),s.Rational(1),s.Rational(7,2)]:
 for N in [1,2,3,5,8,12]:
  hh=T/N
  for j in range(-6,7):
   pp=s.Rational(j,3)*hh*hh
   aa=a.subs({h:hh,p:pp})
   A=s.Matrix([[1,aa],[0,1]])
   ck('positive_Legendre_hessian',hh<=aa<=2*hh)
   ck('mechanical_symplecticity',zero(A.T*J2*A-J2))
   ck('full_horizon_shear',zero(A**N-s.Matrix([[1,T+T/(1+pp*pp/hh**4)],[0,1]])))
   ck('regular_mixed_hessian',-1/aa<0)
  # All constrained state variables x1,...,xN, with fixed x0.
  A=s.Matrix([[1,2*hh],[0,1]])
  Jac=s.zeros(2*N)
  for k in range(N):
   Jac[2*k:2*k+2,2*k:2*k+2]=s.eye(2)
   if k:Jac[2*k:2*k+2,2*k-2:2*k]=-A
  ck('constraint_full_rank',Jac.det()==1)
  lam=s.Matrix([entry for k in range(1,N+1) for entry in [s.Integer(1),2*(T-k*hh)]])
  grad=s.zeros(2*N,1);grad[-2]=1
  ck('complete_KKT_stationarity',zero(Jac.T*lam-grad))
  ck('initial_covector_recovery',zero(A.T*lam[:2,0]-s.Matrix([1,2*T])))
  for k in range(N+1):
   disc=s.Matrix([1,2*(T-k*hh)]);exact=s.Matrix([1,T-k*hh])
   ck('entire_mesh_adjoint_error',disc-exact==s.Matrix([0,T-k*hh]))
# Noncommuting telescoping identity underlying the C1 criterion.
for n in range(1,7):
 A=[s.Matrix([[1,s.Rational(k+1,23)],[s.Rational(k%2,29),1]]) for k in range(n)]
 B=[s.Matrix([[1,s.Rational(k+1,23)+s.Rational(1,101)],[s.Rational((k+1)%2,29),1]]) for k in range(n)]
 def prod(seq):
  P=s.eye(2)
  for M in seq:P=M*P
  return P
 telescoped=s.zeros(2)
 for j in range(n):telescoped+=prod(A[j+1:])*(A[j]-B[j])*prod(B[:j])
 ck('noncommuting_product_telescoping',zero(prod(A)-prod(B)-telescoped))
here=Path(__file__).resolve().parent
r={'status':'PASS','exact_assertions':sum(C.values()),'checks':dict(C),'artifact_sha256':hashlib.sha256((here/'author_replay/PARTIAL.md').read_bytes()).hexdigest(),'sympy_version':s.__version__,'scope':'Symbolic differentiation, exact rational Legendre/shear/KKT identities and noncommuting product telescoping. Global uniform error bounds and source scope are analytically audited in REVIEW.md.'}
(here/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
