from fractions import Fraction as Q
from pathlib import Path
import random,json,hashlib
rng=random.Random(6064);count=0;cases=0
class C:
 def __init__(self,a=0,b=0):self.a=Q(a);self.b=Q(b)
 def __add__(self,o):
  if not isinstance(o,C):o=C(o)
  return C(self.a+o.a,self.b+o.b)
 __radd__=__add__
 def __neg__(self):return C(-self.a,-self.b)
 def __sub__(self,o):return self+-o if isinstance(o,C) else self+C(-o)
 def __mul__(self,o):
  if not isinstance(o,C):o=C(o)
  return C(self.a*o.a-self.b*o.b,self.a*o.b+self.b*o.a)
 __rmul__=__mul__
 def __truediv__(self,o):
  if not isinstance(o,C):o=C(o)
  d=o.a**2+o.b**2
  return C((self.a*o.a+self.b*o.b)/d,(self.b*o.a-self.a*o.b)/d)
 def abs2(self):return self.a**2+self.b**2
 def __pow__(self,n):
  r=C(1)
  for _ in range(n):r=r*self
  return r
phases=[C(1),C(-1),C(0,1),C(0,-1),C(Q(3,5),Q(4,5)),C(Q(-3,5),Q(4,5))]
def ck(t):
 global count
 if not t:raise AssertionError('independent control failed')
 count+=1
params=[(Q(0),Q(0))]
ks=sorted(set([Q(i,10) for i in range(1,31)]+[Q(1,1000),Q(1,100),Q(10),Q(100)]))
for k in ks:
 params.append((-2*k*k/(3*k+1),k))
 params.append((2*k*k/(k+1) if k<=1 else 2*k*(k+1)/(3*k+1),k))
for alpha,k in params:
 a=abs(1-alpha);b=abs(alpha)
 ck(2*k*k-(a+2*b-1)*k-b==0)
 if k:ck(a/(1+2*k)+b/k==1)
 for rep in range(12):
  raw=[rng.randrange(1,8) for n in range(2,9)];total=sum(raw);budget=[Q(1),Q(1,2),Q(0)][rep%3]
  amps={n:budget*Q(raw[n-2],total)/(n*(1+k*(n-1))) for n in range(2,9)}
  coeff={n:amps[n]*phases[rng.randrange(len(phases))] for n in amps}
  ck(sum(n*(1+k*(n-1))*amps[n] for n in amps)==budget)
  for radius in (Q(1,10),Q(1,2),Q(9,10),Q(99,100)):
   z=radius*phases[(rep+int(radius*100))%len(phases)]
   A=sum((v*z**(n-1) for n,v in coeff.items()),C());B=sum((n*v*z**(n-1) for n,v in coeff.items()),C());D=sum((n*(n-1)*v*z**(n-1) for n,v in coeff.items()),C())
   ck((1+A).abs2()>0);ck((1+B).abs2()>0)
   J=1+(1-alpha)*(B-A)/(1+A)+alpha*D/(1+B)
   ck(J.a>0);ck((J-1).abs2()<1);cases+=1
   Ar=sum(amps[n]*radius**(n-1) for n in amps);Br=sum(n*amps[n]*radius**(n-1) for n in amps);X=Br-Ar;Y=sum(n*(n-1)*amps[n]*radius**(n-1) for n in amps)
   ck(Ar<=Br/2);ck(Br<1);ck(Y>=2*X)
   if k and budget:
    ck(X/(1-Ar)<1/(1+2*k));ck(Y/(1-Br)<1/k)
for k in [Q(i,20) for i in range(1,21)]:
 alpha=2*k*k/(k+1);star=1/(2*(1+k))
 for lam in (k/2,99*k/100):
  c=(star+min(Q(1,2),1/(2*(1+lam))))/2;z=(star/c+1)/2;x=c*z
  ck(0<c<Q(1,2));ck(2*(1+lam)*c<1);ck(0<z<1)
  direct=1-(1-alpha)*x/(1-x)-alpha*2*x/(1-2*x)
  formula=(1-(4+alpha)*x+4*x*x)/((1-x)*(1-2*x))
  ck(direct==formula);ck(direct<0)
 ck(1-(4+alpha)*star+4*star*star==0)
alpha=Q(1,2);x=Q(31,100);ck((1-(4+alpha)*x+4*x*x)/((1-x)*(1-2*x))==Q(-53,1311))
r={'independent_assertions':count,'parameter_cases':len(params),'exact_complex_evaluations':cases,'sharpness_witnesses':40,'scope':'Gaussian-rational interior evaluations and independent scalar/jet/witness algebra; analytic proof audited separately.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
