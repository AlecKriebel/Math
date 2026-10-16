#!/usr/bin/env python3
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import os,json,datetime,math
sys.path.insert(0,os.environ['PR204_RUNTIME_PACKAGES'])
import mpmath as mp
import sympy as sp
mp.mp.dps=100
H=Path(__file__).resolve().parent
def need(x,label):
 if not x: raise RuntimeError(label)
def dot(x,y): return x[0]*y[0]+x[1]*y[1]
def sub(x,y): return (x[0]-y[0],x[1]-y[1])
def det(x,y): return x[0]*y[1]-x[1]*y[0]
def norm(x): return mp.sqrt(dot(x,x))
def rel(x,y): return abs(x-y)/max(1,abs(x),abs(y))
def finite(x): need(mp.isfinite(x),'nonfinite'); return x
def area(P): return sum(det(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2
def feet(P):
 out=[]
 for i,p in enumerate(P):
  d=sub(P[(i+1)%len(P)],p);z=dot(p,d)/dot(d,d)
  out.append((p[0]-z*d[0],p[1]-z*d[1]))
 return out
def shoot(a,b,al,be,t,direction,N):
 p=(a*mp.cos(t),b*mp.sin(t));R=(p[0]/al,p[1]/be);D=dot(R,R);s=mp.sqrt(D-1)
 tangents=[(al*(R[0]-sgn*R[1]*s)/D,be*(R[1]+sgn*R[0]*s)/D) for sgn in (-1,1)]
 T=next(q for q in tangents if direction*det(p,sub(q,p))>0)
 vv=sub(T,p);v=tuple(x/norm(vv) for x in vv)
 P=[]; residuals=[]
 for i in range(N):
  P.append(p);den=v[0]**2/a**2+v[1]**2/b**2
  step=-2*(p[0]*v[0]/a**2+p[1]*v[1]/b**2)/den
  need(step>0,'forward ray')
  q=(p[0]+step*v[0],p[1]+step*v[1])
  normal=(q[0]/a**2,q[1]/b**2);z=2*dot(v,normal)/dot(normal,normal)
  newv=(v[0]-z*normal[0],v[1]-z*normal[1])
  residuals.append(abs(q[0]**2/a**2+q[1]**2/b**2-1))
  p=q;v=newv
 return P,max(residuals),norm(sub(p,P[0]))/max(a,b)
rows=[];allerr=[];wrong=[]
families=[(3,1),(4,1),(5,2),(7,3),(8,3),(12,5),(13,5),(6,1),(10,3)]
for kstr in ('0.000001','0.63','0.999999'):
 k=mp.mpf(kstr);kp=mp.sqrt(1-k*k);K=mp.ellipk(k*k)
 sn=lambda z:mp.ellipfun('sn',z,k*k)
 cn=lambda z:mp.ellipfun('cn',z,k*k)
 dn=lambda z:mp.ellipfun('dn',z,k*k)
 for N,tau in families:
  need(math.gcd(N,tau)==1,'least')
  v=2*K*tau/N;delta=2*v;al=mp.mpf(1);be=kp;a=dn(v)/cn(v);b=kp/cn(v)
  lam=a*a-1;need(rel(lam,b*b-be*be)<mp.mpf('1e-90') and 0<lam<b*b,'confocal')
  products=[];worst=mp.mpf(0);phaseareas=[]
  for t in (mp.mpf('0'),mp.mpf('.137'),mp.mpf('1.2')):
   for direction in (-1,1):
    P,on,closure=shoot(a,b,al,be,t,direction,N)
    A=area(P);B=area(feet(P));products.append(finite(A*B))
    need(direction*A>0 and direction*B>0,'signed orientation')
    need(min(norm(sub(P[i],P[j])) for i in range(N) for j in range(i))/max(a,b)>mp.mpf('1e-20'),'distinct vertices')
    w=mp.ellipf(t-mp.pi/2,k*k)
    S=lambda z:sum(dn(z+j*delta) for j in range(N))
    CA=a*b*sn(v)*cn(v)/dn(v)
    CT=sn(delta)*(dn(delta)+kp*kp)/(1+dn(delta))**2
    e=max(on,closure,rel(abs(A),CA*S(w)),rel(abs(B),CT*S(w+v+K)))
    worst=max(worst,e);need(e<mp.mpf('1e-65'),'Cartesian vs traces')
    phaseareas.append([mp.nstr(A,20),mp.nstr(B,20)])
  spread=max(abs(x-products[0])/max(1,abs(products[0])) for x in products)
  target=N%4!=2
  if target: need(spread<mp.mpf('1e-65'),'phase product')
  else: need(spread>mp.mpf('1e-35'),'excluded parity variation');wrong.append(mp.nstr(spread,12))
  rows.append(dict(k=kstr,N=N,tau=tau,target=target,orbits=6,max_residual=mp.nstr(worst,12),product_spread=mp.nstr(spread,12),phase_signed_areas=phaseareas))
  allerr.append(worst)
# exact physical checks written from geometric definitions
sqrt=sp.sqrt
polys={
'H':[(2,0),(sp.Rational(4,3),sqrt(5)/3),(-sp.Rational(4,3),sqrt(5)/3),(-2,0),(-sp.Rational(4,3),-sqrt(5)/3),(sp.Rational(4,3),-sqrt(5)/3)],
'J':[(0,1),(-4*sqrt(2)/3,sp.Rational(1,3)),(-4*sqrt(2)/3,-sp.Rational(1,3)),(0,-1),(4*sqrt(2)/3,-sp.Rational(1,3)),(4*sqrt(2)/3,sp.Rational(1,3))]}
exact={}
for name,P in polys.items():
 P=[tuple(map(sp.sympify,p)) for p in P];Q=[]
 for i,p in enumerate(P):
  need(sp.simplify(p[0]**2/4+p[1]**2-1)==0,'exact ellipse')
  d=sub(P[(i+1)%6],p);n=(-d[1],d[0]);c=dot(n,p)
  need(sp.simplify(sp.Rational(32,9)*n[0]**2+sp.Rational(5,9)*n[1]**2-c*c)==0,'exact confocal tangent')
  prev=P[(i-1)%6]; incoming=sub(p,prev);outgoing=d
  incoming=tuple(x/sp.sqrt(dot(incoming,incoming)) for x in incoming)
  outgoing=tuple(x/sp.sqrt(dot(outgoing,outgoing)) for x in outgoing)
  normal=(p[0]/4,p[1]);fac=2*dot(incoming,normal)/dot(normal,normal)
  need(all(sp.simplify(outgoing[j]-incoming[j]+fac*normal[j])==0 for j in range(2)),'exact forward reflection')
  Q.append(tuple(sp.simplify(c*x/dot(n,n)) for x in n))
 A=sp.simplify(area(P));B=sp.simplify(area(Q));prod=sp.simplify(A*B)
 exact[name]=dict(A=str(A),B=str(B),AB=str(prod),distinct=len(set(P))==6)
need(exact['H']['AB']=='14000/729' and exact['J']['AB']=='14336/729','six products')
report=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS',independence='New Cartesian tangent construction and physical line intersection/reflection; canonical relation only selects closed confocal parameter pairs. Direct projection/shoelace does not use the area theorem.',runtime=dict(python=sys.version,sympy=sp.__version__,mpmath=mp.__version__,bytecode_disabled=sys.dont_write_bytecode),configurations=len(rows),orbits=sum(r['orbits'] for r in rows),max_residual=mp.nstr(max(allerr),15),cases=rows,exact=exact,repeated_twelve_difference=str(sp.Rational(4)*(sp.Rational(14336,729)-sp.Rational(14000,729))),limits='Finite exact radical identities and noninterval high precision checks do not prove universal constancy.')
(H/'fresh_geometry_output.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))

