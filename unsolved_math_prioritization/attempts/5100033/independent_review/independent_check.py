"""Independent exact geometry, cyclic-divisor controls and numerical stress tests.
Only installed standard-library and mpmath modules are used. Finite diagnostics
are not a replacement for the universal meromorphic proof.
"""
from fractions import Fraction as F
from math import gcd
import json
import mpmath as mp
exact=0
def eq(a,b):
 global exact
 assert a==b,(a,b);exact+=1
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def foot(P,a,b,c):
 n=(P[0]/a**2,P[1]/b**2);f=(c,0);v=(1-dot(n,f))/dot(n,n)
 return tuple(f[i]+v*n[i] for i in range(2))
for aa,bb,cc in ((5,3,4),(13,5,12),(17,15,8)):
 a,b,c=map(F,(aa,bb,cc))
 for numerator in range(-17,18):
  for denominator in (3,7,11):
   t=F(numerator,denominator);s=2*t/(1+t*t);cn=(1-t*t)/(1+t*t)
   P=(-a*s,b*cn);q=foot(P,a,b,c)
   qf=(a*(c-a*s)/(a-c*s),a*b*cn/(a-c*s))
   eq(q,qf);eq(dot(q,q),a*a)
   eq(dot((P[0]/a**2,P[1]/b**2),q),1)
   eq(det(sub(q,(c,0)),(P[0]/a**2,P[1]/b**2)),0)
   qm=foot(P,a,b,-c);qar=foot((-P[0],-P[1]),a,b,c)
   eq(qm,tuple(-x for x in qar))
rotations=0
for N in range(3,104,2):
 for tau in range(1,(N+1)//2):
  if gcd(N,tau)!=1:continue
  rotations+=1
  orbit={(j*tau)%N:j for j in range(N)}
  eq(len(orbit),N);eq({orbit[0],orbit[tau]},{0,1})
  eq(F(N,2)%1,F(1,2))
  b=F(N-2*tau,4)
  # In reduced real coordinates the reflection center is b modulo 1.
  eq((2*b-(F(N,2)))%1,0)
  poles={(F(0),1),(F(0),3)}
  zeros={(F(1,2),1),(F(1,2),3)}
  eq({((x+F(1,2))%1,y) for x,y in poles},zeros)
  for x,y in zeros:
   eq((-x%1,-y%4),(x,(y+2)%4))
mp.mp.dps=85
num=0;worst=mp.mpf(0);poleworst=mp.mpf(0)
def close(x,y=0,tol=mp.mpf('1e-64')):
 global num,worst
 err=abs(x-y)/(1+abs(x)+abs(y));assert err<tol,(mp.nstr(err,10),mp.nstr(x,10),mp.nstr(y,10))
 num+=1;worst=max(worst,err)
def area(q):return sum(det(q[i],q[(i+1)%len(q)]) for i in range(len(q)))/2
families=0;polecases=0
for N,tau in ((3,1),(5,1),(5,2),(7,2),(7,3),(9,2),(9,4),(11,3),(13,5)):
 for ks in ('0.07','0.53','0.96'):
  k=mp.mpf(ks);m=k*k;K=mp.ellipk(m);Kp=mp.ellipk(1-m);h=2*K*tau/N;d=2*h
  sn=lambda w:mp.ellipfun('sn',w,m)
  cn=lambda w:mp.ellipfun('cn',w,m)
  dn=lambda w:mp.ellipfun('dn',w,m)
  a=dn(h)/cn(h);b=mp.sqrt(1-m)/cn(h);c=k
  def Q(w):return (a*(c-a*sn(w))/(a-c*sn(w)),a*b*cn(w)/(a-c*sn(w)))
  def T(w):return area([Q(w+j*d) for j in range(N)])
  def P(w):return (-a*sn(w),b*cn(w))
  products=[];families+=1
  for phase in ('0.039','0.419','0.877'):
   w=K*mp.mpf(phase);p=P(w);start=p
   ray=sub(P(w+d),p);rn=mp.sqrt(dot(ray,ray));ray=tuple(x/rn for x in ray)
   vertices=[]
   for j in range(N):
    vertices.append(p)
    close(p[0]*p[0]/(a*a)+p[1]*p[1]/(b*b),1)
    t=-2*(p[0]*ray[0]/a**2+p[1]*ray[1]/b**2)/(ray[0]**2/a**2+ray[1]**2/b**2)
    nxt=tuple(p[l]+t*ray[l] for l in range(2));normal=(nxt[0]/a**2,nxt[1]/b**2)
    lam=2*dot(ray,normal)/dot(normal,normal)
    ray=tuple(ray[l]-lam*normal[l] for l in range(2));p=nxt
   close(p[0],start[0]);close(p[1],start[1])
   ns=[(p[0]/a**2,p[1]/b**2) for p in vertices]
   outer=[]
   for i,n in enumerate(ns):
    z=ns[(i+1)%N];cross=det(n,z)
    outer.append(((z[1]-n[1])/cross,(n[0]-z[0])/cross))
   areas=[]
   for sign in (1,-1):
    focus=(sign*c,mp.mpf(0));feet=[]
    for i in range(N):
     x=outer[i-1];e=sub(outer[i],x);tt=dot(sub(focus,x),e)/dot(e,e)
     q=tuple(x[j]+tt*e[j] for j in range(2));feet.append(q)
     direct=foot(vertices[i],a,b,sign*c)
     close(q[0],direct[0]);close(q[1],direct[1]);close(dot(q,q),a*a)
    areas.append(area(feet))
   close(areas[0],T(w));close(areas[1],T(w+2*K));products.append(areas[0]*areas[1])
  close(products[0],products[1]);close(products[0],products[2])
  # Complex character and exact predicted zero, plus a near-pole product test.
  L=4*K/N;center=K-h;z=center+mp.mpf('.231')*L+mp.mpf('.29')*1j*Kp
  close(T(z+L),T(z));close(T(z+2j*Kp),-T(z));close(T(2*center-z),T(z))
  close(T(center+1j*Kp+L/2),0)
  # At both adjacent poles, residue numerators agree, denominator slopes oppose.
  r=K+1j*Kp;zm=r-h;zp=r+h;eps=K*mp.mpf('1e-20')
  rm=tuple(eps*x for x in Q(zm+eps));rp=tuple(eps*x for x in Q(zp+eps))
  err=max(abs(rm[i]+rp[i]) for i in range(2));assert err<mp.mpf('1e-16');num+=1
  poleworst=max(poleworst,err)
  dp=abs(det(rm,rp));assert dp<mp.mpf('1e-16');num+=1;poleworst=max(poleworst,dp)
  # Product remains finite and approaches the same real constant through complex points.
  close(T(zm+eps)*T(zm+eps+L/2),products[0],mp.mpf('1e-40'))
  close(eps*T(zm+eps),(eps/2)*T(zm+eps/2),mp.mpf('1e-16'))
  polecases+=1
print(json.dumps({'status':'PASS','exact_assertions':exact,'primitive_rotations_checked':rotations,'numerical_comparisons':num,'real_families':families,'complex_pole_cases':polecases,'precision_digits':mp.mp.dps,'max_scaled_error':mp.nstr(worst,16),'max_finite_epsilon_residue_error':mp.nstr(poleworst,16),'limits':'Finite exact controls and non-interval numerical stress tests; not a universal proof.'},indent=2))
