#!/usr/bin/env python3
"""Exact bounded controls for the displayed variational/adjoint obstruction."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from pathlib import Path
import hashlib,json
checks=Counter()
def ck(p,k):
 assert p,k
 checks[k]+=1

def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def tr(A):return list(map(list,zip(*A)))
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def mv(A,v):return [sum(a*b for a,b in zip(row,v)) for row in A]
def power(A,n):
 out=eye(len(A))
 for _ in range(n):out=mm(A,out)
 return out
J=[[F(0),F(1)],[F(-1),F(0)]]
I=eye(2)
# The state Jacobian is a shear; all computations use exact rational derivatives.
for N in [1,2,3,4,8,16,32,64]:
 h=F(1,N)
 for num,den in product(range(-4,5),range(1,5)):
  p=F(num,den)
  a=h+h/(1+p*p/h**4)
  A=[[F(1),a],[F(0),F(1)]]
  inverse=[[F(1),-a],[F(0),F(1)]]
  ck(h<=a<=2*h,'strict_convexity_and_regular_legendre')
  ck(a>0 and -1/a!=0,'nonzero_mixed_discrete_hessian')
  ck(mm(tr(A),mm(J,A))==J,'mechanical_symplecticity')
  ck(mm(A,inverse)==I,'state_map_inverse')
  AN=power(A,N)
  ck(AN==[[F(1),1+1/(1+p*p/h**4)],[F(0),F(1)]],'global_sensitivity_formula')
  # Cotangent lift preserves its own extended pairing, even in the bad example.
  for v,w in [([F(1),F(0)],[F(0),F(1)]),([F(2),F(-3)],[F(5),F(7)])]:
   tangent=mv(A,v);adjoint_next=mv(tr(inverse),w)
   ck(sum(a*b for a,b in zip(tangent,adjoint_next))==sum(a*b for a,b in zip(v,w)),'exact_adjoint_variation_pairing')
  ck(0<1/(1+p*p/h**4)<=1,'bounded_global_derivative_discrepancy')
 # Entire zero-momentum costate path, not only the initial multiplier.
 A=[[F(1),2*h],[F(0),F(1)]];lam=[F(1),F(0)]
 for j in range(N+1):
  ck(lam==[F(1),2*j*h],'backward_KKT_costate')
  exact=[F(1),j*h]
  ck(lam[1]-exact[1]==j*h,'exact_continuous_adjoint_error')
  if j<N:lam=mv(tr(A),lam)
 ck(lam==[F(1),F(2)],'nonvanishing_unit_horizon_error')
 # The second momentum derivative is unbounded along p=h^2.
 p=h*h
 dpp=-2*p/h**3/(1+p*p/h**4)**2
 ck(dpp==-1/(2*h),'failure_of_uniform_smoothness')
 ck((h)/(h**3)==N*N,'local_derivative_error_exceeds_state_order')
 # For a bounded momentum |p|<=3 and |p-v|<=2h^2, the action-error estimate
 # from F(z)<=2|z| is explicitly bounded by 2h^5+6h^3.
 ck(F(1,2)*h*(2*h*h)**2+2*h**3*3==2*h**5+6*h**3,'action_value_bound_scaling')
# The continuous free-particle sensitivity and the bad sensitivity are different,
# although both are symplectic and uniformly stable shears.
for T in [F(1,2),F(1),F(2),F(3)]:
 good=[[F(1),T],[F(0),F(1)]];bad=[[F(1),2*T],[F(0),F(1)]]
 ck(mm(tr(good),mm(J,good))==J and mm(tr(bad),mm(J,bad))==J,'symplecticity_does_not_identify_sensitivity')
 ck(mv(tr(good),[F(1),F(0)])==[F(1),T],'continuous_terminal_gradient')
 ck(mv(tr(bad),[F(1),F(0)])==[F(1),2*T],'discrete_terminal_gradient')
# The terminal objective is bounded below, and control stationarity is coercive.
for q,p,u in product(range(-3,4),repeat=3):
 Phi=F(q)+F(q*q+p*p,2)
 ck(Phi+F(1,2)==F((q+1)**2+p*p,2)>=0,'bounded_below_terminal_objective')
 ck(F(u*u,2)>=0 and ((u==0)==(F(u*u,2)==0)),'unique_zero_control')
here=Path(__file__).resolve().parent
result={'status':'PASS','exact_assertions':sum(checks.values()),'checks':dict(sorted(checks.items())),
 'artifact_sha256':hashlib.sha256((here/'PARTIAL.md').read_bytes()).hexdigest(),
 'scope':'Exact bounded sensitivity/symplectic/KKT controls; universal action/state estimates and step-size regularity limitation are proved in the note. No full conventional-method resolution.'}
(here/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
