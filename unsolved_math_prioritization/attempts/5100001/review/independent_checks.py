#!/usr/bin/env python3
"""Independent rational orbit geometry and symbolic continuous-family checks."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
from hashlib import sha256
import json
import sympy as S

root=Path(__file__).resolve().parent
checks=0;families=0
def ck(v):
 global checks
 assert v
 checks+=1
def dot(v,w):return sum(x*y for x,y in zip(v,w))
def sub(v,w):return tuple(x-y for x,y in zip(v,w))
def scale(t,v):return tuple(t*x for x in v)
def det(v,w):return v[0]*w[1]-v[1]*w[0]
def norm(v):
 q=dot(v,v);n=isqrt(q.numerator);d=isqrt(q.denominator)
 ck(n*n==q.numerator and d*d==q.denominator)
 return F(n,d)
def area(p):return sum(det(p[i],p[(i+1)%4]) for i in range(4))/2
def meet(n,m):
 D=det(n,m);ck(D!=0)
 return ((m[1]-n[1])/D,(n[0]-m[0])/D)

def orbit(a,b,s,P):
 lam=a*a*b*b/(a*a+b*b);ca=a*a-lam;cb=b*b-lam
 ck(ca==a**4/s**2 and cb==b**4/s**2 and 0<lam<b*b)
 ck(len(set(P))==4)
 out=[];half2=[];lengths=[]
 for i in range(4):
  p=P[i];q=P[(i+1)%4];prev=P[(i-1)%4]
  ck(p[0]**2/a**2+p[1]**2/b**2==1)
  ck(det(p,q)>0)
  v=sub(q,p);ell=norm(v);ck(ell>0);lengths.append(ell)
  n=(v[1],-v[0]);h=dot(n,p);ck(h>0)
  ck(ca*n[0]**2+cb*n[1]**2==h*h)
  touch=(ca*n[0]/h,cb*n[1]/h)
  ck(dot(n,touch)==h)
  tau=dot(sub(touch,p),v)/(ell*ell);ck(0<tau<1)
  ck(touch==tuple(p[j]+tau*v[j] for j in (0,1)))
  normal=(p[0]/a**2,p[1]/b**2)
  inc=sub(p,prev);inc=scale(1/norm(inc),inc)
  outgoing=scale(1/ell,v)
  ck(sub(inc,scale(2*dot(inc,normal)/dot(normal,normal),normal))==outgoing)
  ck(dot(inc,normal)==1/s)
  co=-dot(inc,outgoing);ck(-1<co<1);half2.append((1-co)/2)
  nextnormal=(q[0]/a**2,q[1]/b**2)
  out.append(meet(normal,nextnormal))
 ck(sum(lengths)==4*s)
 A=area(P);Ap=area(out);ck(A>0 and Ap>0)
 ck(A*Ap==8*a*a*b*b)
 product=F(1)
 for x in half2:product*=x
 num=isqrt(product.numerator);den=isqrt(product.denominator)
 ck(num*num==product.numerator and den*den==product.denominator)
 H=F(num,den)
 return (A,Ap,H,Ap/A*H)

advertised={}
for m in range(2,13):
 for n in range(1,m):
  a,b=sorted((F(m*m-n*n),F(2*m*n)),reverse=True);s=F(m*m+n*n)
  D=[(a,F(0)),(F(0),b),(-a,F(0)),(F(0),-b)]
  R=[(a*a/s,b*b/s),(-a*a/s,b*b/s),(-a*a/s,-b*b/s),(a*a/s,-b*b/s)]
  v=orbit(a,b,s,D);w=orbit(a,b,s,R)
  ck(v==(2*a*b,4*a*b,a*a*b*b/s**4,2*a*a*b*b/s**4))
  ck(w==(4*a*a*b*b/s**2,2*s*s,F(1,4),s**4/(8*a*a*b*b)))
  ck(v[3]<F(1,2)<w[3])
  families+=1
  if a==4 and b==3:
   advertised={'diamond':[str(x) for x in v],'rectangle':[str(x) for x in w]}
ck(advertised['diamond'][-1]=='288/625')
ck(advertised['rectangle'][-1]=='625/1152')
ck(F(625,1152)-F(288,625)==F(58849,720000))

# Symbolic reductions for all parameters of the continuous family.
a,b,c,d,D,s=S.symbols('a b c d D s',nonzero=True)
G=S.groebner([c*c+d*d-1,D*D-a**4*d*d-b**4*c*c,s*s-a*a-b*b],D,s,c,d,domain=S.QQ.frac_field(a,b))
def zero(v):
 num=S.fraction(S.cancel(v))[0]
 ck(G.reduce(num)[1]==0)
P=S.Matrix([a*c,b*d]);Q=S.Matrix([-a**3*d/D,b**3*c/D])
zero((Q[0]/a)**2+(Q[1]/b)**2-1)
newD=a*a*b*b/D
zero(newD**2-(a**4*(Q[1]/b)**2+b**4*(Q[0]/a)**2))
zero(-a**2*(Q[1]/b)/newD+c)
zero(b**2*(Q[0]/a)/newD+d)
U=a*a*d*d+b*b*c*c
zero(S.det(S.Matrix.hstack(P,Q))-a*b*U/D)
v=Q-P;normal=S.Matrix([v[1],-v[0]]);h=normal.dot(P)
zero(a**4/s**2*normal[0]**2+b**4/s**2*normal[1]**2-h*h)
pq=P.dot(Q);lm=s-pq/s;lp=s+pq/s
zero(lm*lm-(Q-P).dot(Q-P))
zero(lp*lp-(P+Q).dot(P+Q))
vin=(P+Q)/lp;vout=(Q-P)/lm;nP=S.Matrix([P[0]/a**2,P[1]/b**2])
reflected=vin-2*vin.dot(nP)/nP.dot(nP)*nP
for j in range(2):zero(reflected[j]-vout[j])
zero(vin.dot(nP)-1/s)
# The integral tangent/reflection equivalence follows from this identity.
x,y,vx,vy,la=S.symbols('x y vx vy la')
identity=a*a*b*b*(x*vx/a**2+y*vy/b**2)**2-(a*a*vy*vy+b*b*vx*vx-(x*vy-y*vx)**2)
ck(S.factor(identity)==S.factor((b*b*vx*vx+a*a*vy*vy)*(x*x/a**2+y*y/b**2-1)))

receipt={'verdict':'PASS','assertions':checks,'independent_rational_axis_families':families,'exact_advertised_values':advertised,'artifact_sha256':sha256((root/'author_replay/COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'scope':'Direct rational geometry for two primitive orbits in each ellipse, and symbolic all-parameter family/reflection reductions; no corrected all-period invariant claim.'}
(root/'independent_results.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
