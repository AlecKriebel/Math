#!/usr/bin/env python3
"""Exact rational controls; the analytic argument is in CANDIDATE.md."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from collections import Counter
import random,json
C=Counter();rng=random.Random(2306064)
def ck(kind,b):
 if not b:raise AssertionError(kind)
 C[kind]+=1
class QI:
 def __init__(self,a=0,b=0):self.a=F(a);self.b=F(b)
 def __add__(x,y):
  if not isinstance(y,QI):y=QI(y)
  return QI(x.a+y.a,x.b+y.b)
 __radd__=__add__
 def __neg__(x):return QI(-x.a,-x.b)
 def __sub__(x,y):return x+-QI(y) if not isinstance(y,QI) else x+-y
 def __mul__(x,y):
  if not isinstance(y,QI):y=QI(y)
  return QI(x.a*y.a-x.b*y.b,x.a*y.b+x.b*y.a)
 __rmul__=__mul__
 def __truediv__(x,y):
  if not isinstance(y,QI):y=QI(y)
  d=y.norm();return QI((x.a*y.a+x.b*y.b)/d,(x.b*y.a-x.a*y.b)/d)
 def __pow__(x,n):
  y=QI(1)
  for _ in range(n):y=y*x
  return y
 def norm(x):return x.a*x.a+x.b*x.b

def values(alpha,coeff,z):
 P=QI(1);G=QI(1);H=QI()
 for n,a in coeff.items():
  v=a*z**(n-1);P=P+v;G=G+n*v;H=H+n*(n-1)*v
 ck('zero_avoidance_sample',P.norm()>0 and G.norm()>0)
 J=(1-alpha)*(G/P)+alpha*(QI(1)+H/G)
 return J
ks=sorted(set(F(i,j) for j in range(1,9) for i in range(1,25)))
params=[(F(0),F(0),'zero')]
for k in ks:
 if k<=1:params.append((2*k*k/(1+k),k,'interior'))
 params.append((-2*k*k/(3*k+1),k,'negative'))
 if k>1:params.append((2*k*(k+1)/(3*k+1),k,'above_one'))
for alpha,k,case in params:
 a=abs(1-alpha);b=abs(alpha);d=a+2*b-1
 ck('positive_root_polynomial',2*k*k-d*k-b==0)
 ck('piecewise_parameter_range',(case=='zero' and alpha==0) or (case=='interior' and 0<alpha<=1) or (case=='negative' and alpha<0) or (case=='above_one' and alpha>1))
 if k:ck('normalizing_identity',a/(1+2*k)+b/k==1)
 for rep in range(10):
  ns=(2,3,5,8);raw=[F(rng.randrange(1,8),20) for _ in ns];W=sum(n*(1+k*(n-1))*x for n,x in zip(ns,raw));budget=F(rep+1,10)
  magnitudes=[x*budget/W for x in raw]
  A=sum(magnitudes);B=sum(n*x for n,x in zip(ns,magnitudes));X=B-A;Y=sum(n*(n-1)*x for n,x in zip(ns,magnitudes))
  ck('weighted_budget',B+k*Y==budget);ck('moment_order',Y>=2*X and A<=B/2)
  if k:
   D=1-B;ck('positive_denominators',D>0 and 1-A>0)
   phi=a*X/(1-A)+b*Y/D
   ck('scalar_majorization',phi<=1)
   if budget<1:ck('strict_scalar_majorization',phi<1)
  else:ck('zero_alpha_majorization',X/(1-A)<=1)
  phases=[QI(1),QI(-1),QI(0,1),QI(0,-1),QI(F(3,5),F(4,5)),QI(F(-3,5),F(4,5))]
  coeff={n:x*phases[rng.randrange(len(phases))] for n,x in zip(ns,magnitudes)}
  for z in (QI(),QI(F(1,2)),QI(F(-3,4)),QI(0,F(2,3)),QI(F(3,10),F(2,5))):
   J=values(alpha,coeff,z);ck('exact_complex_disk_bound',(J-QI(1)).norm()<1);ck('exact_complex_positive_real',J.a>0)
for k in (x for x in ks if x<=1):
 alpha=2*k*k/(1+k);lam=k/2;cstar=1/(2*(1+k));upper=min(F(1,2),1/(2*(1+lam)));c=(cstar+upper)/2;z=(cstar/c+1)/2;x=c*z
 ck('sharpness_admissible',0<cstar<c<F(1,2) and 0<z<1)
 ck('smaller_weight_passes',2*(1+lam)*c<1)
 ck('boundary_root',1-(4+alpha)*cstar+4*cstar*cstar==0)
 J=values(alpha,{2:QI(-c)},QI(z));N=1-(4+alpha)*x+4*x*x;D=(1-x)*(1-2*x)
 ck('quadratic_identity',J.a==N/D and J.b==0)
 ck('sharpness_failure',J.a<0)
 if alpha<1:ck('naive_interpolation_too_small',k>alpha)
ck('endpoint_zero',params[0][0]==0 and params[0][1]==0)
ck('endpoint_one',any(alpha==1 and k==1 for alpha,k,_ in params))
J=values(F(1,2),{2:QI(F(-8,25))},QI(F(31,32)))
ck('explicit_naive_sum',3*F(8,25)==F(24,25)<1)
ck('explicit_naive_failure',J.a==F(-53,1311) and J.b==0)
root=Path(__file__).resolve().parent
out={'artifact_sha256':sha256((root/'CANDIDATE.md').read_bytes()).hexdigest(),'exact_assertions':sum(C.values()),'categories':dict(C),'rational_parameter_cases':len(params),'coefficient_vectors':10*len(params),'scope':'Exact rational parameter, scalar inequality, Gaussian-rational analytic-expression controls, and quadratic witnesses. Not a numerical proof of the all-function theorem.'}
print(json.dumps(out,indent=2))
