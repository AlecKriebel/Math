"""Exact algebra controls for Turn 1; no Helmholtz simulation or counterexample."""
from fractions import Fraction as F
import json
from collections import Counter
import sympy as s
C=Counter()
def ck(g,b):
 if not b:raise AssertionError(g)
 C[g]+=1
A,B=s.symbols('A B')
P=2*A-1+2*B;Q=A+B
relation=B*B-A*(A-1)
def reduce(x):return s.rem(s.Poly(s.expand(x),B),s.Poly(relation,B)).as_expr().expand()
ck('quadratic_root',reduce(P*P+(2-4*A)*P+1)==0)
ck('printed_residual',reduce(Q*Q+(2-4*A)*Q+1+(A-1)*(2*A+1+2*B))==0)
ck('corrected_product_relation',s.expand(P-(2*Q-1))==0)
for a0 in range(2,21):
 for b0 in range(2,21):
  AA=F(a0*b0);disc=AA*(AA-1)
  ck('positive_quadratic_discriminant',disc>0 and AA>1)
  # P+1=2a L1=2b L0; symbolic product identity uses B²=A(A-1).
  l0=(P+1)/(2*b0);l1=(P+1)/(2*a0)
  ck('two_cycle_product',s.simplify((l0*l1-P).subs({A:a0*b0,B:s.sqrt(a0*b0*(a0*b0-1))}))==0)
rho=F(1,4);sigma=F(1,2)
for k in range(1,81):
 for j in (0,1,k//2,k,2*k,3*k):
  u=rho**j+F(1,2**k)*sigma**j
  v=rho**(j+1)+F(1,2**k)*sigma**(j+1)
  t=F(1,2**k)*2**j
  ck('hidden_mode_ratio',v/u==rho+(sigma-rho)*t/(1+t))
  ck('strictly_decaying_iterates',rho<v/u<sigma)
  if j==k:ck('fixed_crossover_error',v/u-rho==F(1,8))
for k in range(1,51):
 for m in range(0,101,5):
  for period in (1,2,3,7):
   Pm=F(m,3);Pn=F(m+period,3)
   ratio=(k+Pn)/(k+Pm)
   ck('unbounded_remainder_bounded_increment',abs(ratio-1)<=F(period,3*k))
   R=F(2,7);err=F(3,5*k)
   actual=ratio*(R+err)
   bound=(1+F(period,3*k))*err+R*F(period,3*k)
   ck('period_relative_error_bound',abs(actual-R)<=bound)
print(json.dumps({'status':'PASS_EXACT_CONTROLS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Quadratic recurrence correction, normalized-period identity and abstract two-mode obstruction; no actual-density PDE theorem or counterexample.'},indent=2,sort_keys=True))
