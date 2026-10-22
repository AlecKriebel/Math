"""Independently authored exact polynomial-identity checks; standard library only.

No source-author script is imported or executed. This does not validate the
alternative paper's numerical certificates or all its analytic hypotheses.
"""
from fractions import Fraction as F
import json
N=4
class Poly:
 def __init__(self,v=0):
  if isinstance(v,Poly):self.d=v.d.copy()
  elif isinstance(v,dict):self.d={k:F(x) for k,x in v.items() if x}
  else:self.d={} if not v else {(0,)*N:F(v)}
 def __add__(self,o):
  o=Poly(o);d=self.d.copy()
  for k,v in o.d.items():d[k]=d.get(k,F(0))+v
  return Poly(d)
 __radd__=__add__
 def __neg__(self):return Poly({k:-v for k,v in self.d.items()})
 def __sub__(self,o):return self+-Poly(o)
 def __mul__(self,o):
  o=Poly(o);d={}
  for a,x in self.d.items():
   for b,y in o.d.items():
    k=tuple(u+v for u,v in zip(a,b));d[k]=d.get(k,F(0))+x*y
  return Poly(d)
 def diff(self,i):
  d={}
  for k,v in self.d.items():
   if k[i]:
    z=list(k);z[i]-=1;d[tuple(z)]=v*k[i]
  return Poly(d)
 def ev(self,x):return sum((c*prod(t**n for t,n in zip(x,k)) for k,c in self.d.items()),F(0))
def prod(xs):
 p=F(1)
 for x in xs:p*=x
 return p
class Rat:
 def __init__(self,a=0,b=1):
  if isinstance(a,Rat) and b==1:self.a,self.b=a.a,a.b
  else:self.a,self.b=Poly(a),Poly(b)
  if not self.b.d:raise ValueError('zero denominator')
 def __add__(self,o):
  o=Rat(o);return Rat(self.a*o.b+o.a*self.b,self.b*o.b)
 __radd__=__add__
 def __neg__(self):return Rat(-self.a,self.b)
 def __sub__(self,o):return self+-Rat(o)
 def __rsub__(self,o):return Rat(o)+-self
 def __mul__(self,o):
  o=Rat(o);return Rat(self.a*o.a,self.b*o.b)
 __rmul__=__mul__
 def __truediv__(self,o):
  o=Rat(o);return Rat(self.a*o.b,self.b*o.a)
 def __rtruediv__(self,o):return Rat(o)/self
 def __pow__(self,n):
  if type(n)is not int or n<0:raise ValueError('power')
  x=Rat(1)
  for _ in range(n):x=x*self
  return x
 def diff(self,i):return Rat(self.a.diff(i)*self.b-self.a*self.b.diff(i),self.b*self.b)
 def ev(self,x):return self.a.ev(x)/self.b.ev(x)
def var(i):
 k=[0]*N;k[i]=1;return Rat(Poly({tuple(k):F(1)}))
q,y,v,L=[var(i) for i in range(N)]
checks=[]
def same(name,a,b):
 a,b=Rat(a),Rat(b)
 residual=a.a*b.b-b.a*a.b
 if residual.d:raise RuntimeError('identity failed: '+name)
 checks.append(name)
s=(1-q)/(1+q);H=2*q/(1+q)**2
U=lambda t:(1+t)/(1-t)
W=lambda t:t+1/t
X=lambda t:(2*s*s-1-t*t)/(1-t*t)
same('Möbius parameter inverse',(1-s)/(1+s),q)
same('capacity H equals (1-s^2)/2',H,(1-s*s)/2)
same('right/left exterior log argument',(U(y)-q)/(1-q*U(y)),(s+y)/(s-y))
same('physical abscissa identity',s*s-H*W(U(y)),X(y))
same('exact positive width identity',X(y)-X(v),H*(W(U(v))-W(U(y))))
same('Jacobian of DPT coordinate',X(y).diff(1),-4*y*(1-s*s)/(1-y*y)**2)
same('root atom location X_s(s)=-1',(2*s*s-1-s*s)/(1-s*s),-1)
# Log(y) is a formal symbol L. Its derivative is 1/y.
a=y*(y-1-L)/(y-1)**2;b=y*(1+y+L)/(1+y)**2
same('a derivative including chain rule',a.diff(1)+a.diff(3)/y,((y+1)*L-2*(y-1))/(y-1)**3)
same('b minus a exact numerator',b-a,2*y*((y*y+1)*L-y*y+1)/((y-1)**2*(y+1)**2))
# Finite exact evaluations corroborate the small independent polynomial engine.
for x in [F(1,5),F(2,5),F(3,5)]:
 for t in [F(1,7),F(2,7)]:
  point=(x,t,F(4,5),F(1,3))
  for z in [s,H,U(y),X(y)]:
   if z.ev(point)!=z.a.ev(point)/z.b.ev(point):raise RuntimeError('evaluation oracle')
# Deliberately wrong scaling and wrong root branch maps must fail exact identity.
controls=[]
for name,left,right in [('wrong H factor',H,(1-s*s)/4),('wrong branch map',s*s-H*W(U(y)),(2*s*s-1+y*y)/(1-y*y))]:
 try:same(name,left,right)
 except RuntimeError:controls.append(name)
 else:raise RuntimeError('false identity accepted')
print(json.dumps({'schema':'pr1310-independent-identity/v1','exact_identities':checks,'false_identities_rejected':controls,'scope':'rational identities and documented log-domain argument only; no numerical proof certificates','third_party_runtime':False},sort_keys=True,ensure_ascii=False,indent=2))
