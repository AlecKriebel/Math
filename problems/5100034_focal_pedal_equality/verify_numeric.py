#!/usr/bin/env python3
"""Non-interval high-precision diagnostics. No numerical test is a proof."""
import mpmath as m
from math import gcd
import json
m.mp.dps=70;checks=0;cases=0;polecases=0
maxerr=m.mpf(0)
def near(x,y,tol=m.mpf('1e-55')):
 global checks,maxerr
 e=abs(x-y)/(1+abs(x)+abs(y));assert e<tol;checks+=1;maxerr=max(maxerr,e)
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def area(P):return sum(det(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2
def foot(F,X,Y):
 d=sub(Y,X);t=dot(sub(F,X),d)/dot(d,d);return(X[0]+t*d[0],X[1]+t*d[1])
for kval in ('0.25','0.7'):
 k=m.mpf(kval);kp=m.sqrt(1-k*k);K=m.ellipk(k*k);Kp=m.ellipk(1-k*k)
 sn=lambda u:m.ellipfun('sn',u,k*k);cn=lambda u:m.ellipfun('cn',u,k*k);dn=lambda u:m.ellipfun('dn',u,k*k)
 for N in range(3,12):
  for tau in range(1,(N+1)//2):
   if gcd(N,tau)!=1:continue
   v=2*K*tau/N;delta=2*v;a=dn(v)/cn(v);b=kp/cn(v)
   q=lambda u:((k-sn(u))/(1-k*sn(u)),kp*cn(u)/(1-k*sn(u)))
   Q=lambda u:(a*(k-a*sn(u))/(a-k*sn(u)),a*b*cn(u)/(a-k*sn(u)))
   def traces(w):return area([q(w+v+i*delta) for i in range(N)]),area([Q(w+i*delta) for i in range(N)])
   C0=None
   for w in (K/11,3*K/7,9*K/8):
    P=[(-a*sn(w+i*delta),b*cn(w+i*delta)) for i in range(N)];norm=[(x/(a*a),y/(b*b)) for x,y in P]
    outer=[]
    for i,n in enumerate(norm):
     z=norm[(i+1)%N];D=det(n,z);outer.append(((z[1]-n[1])/D,(n[0]-z[0])/D))
    aa=[];bb=[]
    for fs in (1,-1):
     F=(fs*k,m.mpf(0));f1=[foot(F,P[i],P[(i+1)%N]) for i in range(N)];f2=[foot(F,outer[i],outer[(i+1)%N]) for i in range(N)]
     A=area(f1);B=area(f2);assert A>0 and B>0;checks+=2;aa.append(A);bb.append(B)
     expected=traces(w+(0 if fs==1 else 2*K));near(A,expected[0]);near(B,expected[1])
    near(aa[0]*bb[1],aa[1]*bb[0]);ratio=bb[0]/aa[0]
    if C0 is None:C0=ratio
    else:near(C0,ratio)
    cases+=1
   if N in (3,4,5,8,11):
    e=m.mpf('1e-16');pole=K-v+1j*Kp
    A1,B1=traces(pole+e);A2,B2=traces(pole+2*e)
    near(e*A1,2*e*A2,m.mpf('1e-12'));near(e*B1,2*e*B2,m.mpf('1e-12'));near(B1,C0*A1,m.mpf('1e-30'))
    polecases+=1
print(json.dumps({'status':'PASS','precision_decimal_digits':m.mp.dps,'diagnostic_comparisons':checks,'real_cases':cases,'complex_pole_cases':polecases,'max_relative_discrepancy':m.nstr(maxerr,12),'scope':'Non-interval high-precision diagnostics only; not certified bounds or a replacement for the analytic proof.'},indent=2))
