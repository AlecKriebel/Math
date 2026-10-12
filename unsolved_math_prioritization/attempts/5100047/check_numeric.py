#!/usr/bin/env python3
"""Non-interval high-precision diagnostics for actual polygons; not a proof."""
import mpmath as mp
from math import gcd
import json
mp.mp.dps=80
count=0;maxerr=mp.mpf(0);positive=True;rows=[]
def chk(e,label):
 global count,maxerr
 count+=1;e=abs(e);maxerr=max(maxerr,e)
 if e>mp.mpf('1e-62'):raise AssertionError((label,mp.nstr(e,15)))
def ar(P):return sum(x*v-y*u for (x,y),(u,v) in zip(P,P[1:]+P[:1]))/2
def inv(P,f):
 out=[]
 for x,y in P:
  x-=f;den=x*x+y*y
  assert den>0
  out.append((x/den,y/den))
 return out
for ks in ('0.25',str(mp.mpf(2)/3),'0.9'):
 k=mp.mpf(ks);m=k*k;kp=mp.sqrt(1-m);K=mp.ellipk(m)
 sn=lambda z:mp.ellipfun('sn',z,m);cn=lambda z:mp.ellipfun('cn',z,m);dn=lambda z:mp.ellipfun('dn',z,m)
 for N in (3,4,5,6,7,8,9,10,11,12,14,15,16):
  for tau in range(1,(N+1)//2):
   if gcd(tau,N)!=1:continue
   v=2*K*tau/N;delta=2*v;h=sn(v);C=cn(v);d=dn(v);t=h*h;q=C*C
   a=d/C;b=kp/C;c=k;Ao=a*d/C;Bo=b/C
   U=1-2*m*t+m*t*t;V=1-2*t+m*t*t
   L0=(U*U-m*V*V*t)/d;L1=(V*V-U*U*t)/C
   CP=b*h*d*q*q;CQ=Bo*h*d*q**4/C
   E=lambda z:CP*dn(z)*(1-m*t*sn(z)**2)/((1+k*sn(z))*(U+k*V*sn(z))**2)
   G=lambda z:CQ*dn(z)*(1-m*t*sn(z)**2)/((d+k*C*sn(z))**2*(L0+k*L1*sn(z)))
   ref=None
   for phase in (mp.mpf(0),mp.mpf(1)/11,mp.mpf(3)/7,mp.mpf(5)/6):
    w=phase*K
    P=[(-a*sn(w+j*delta),b*cn(w+j*delta)) for j in range(N)]
    Q=[]
    for (x,y),(X,Y) in zip(P,P[1:]+P[:1]):
     nx,ny=x/(a*a),y/(b*b);Nx,Ny=X/(a*a),Y/(b*b);det=nx*Ny-ny*Nx
     Q.append(((Ny-ny)/det,(nx-Nx)/det))
    for j,(x,y) in enumerate(Q):
     u=w+v+j*delta
     chk((x+Ao*sn(u))/(1+Ao),'actual_outer_x');chk((y-Bo*cn(u))/(1+Bo),'actual_outer_y')
    ratios=[]
    for f in (c,-c):
     A=ar(inv(P,f));B=ar(inv(Q,f));assert A>0 and B>0
     ratios.append(B/A);count+=2
     if f==c:
      F=sum(E(w+v+j*delta) for j in range(N));H=sum(G(w+2*v+j*delta) for j in range(N))
      chk((A-F)/(1+abs(A)),'original_edge_sum');chk((B-H)/(1+abs(B)),'outer_edge_sum')
    chk((ratios[0]-ratios[1])/(1+abs(ratios[0])),'both_foci_same_constant')
    if ref is None:ref=ratios[0]
    chk((ratios[0]-ref)/(1+abs(ref)),'phase_invariant_ratio')
    if N==4:chk(ref-mp.mpf('0.5'),'N4_ratio_half')
   rows.append({'k':mp.nstr(k,10),'N':N,'tau':tau,'ratio':mp.nstr(ref,24)})
# A half-step mismatch must be visible: outer-locus Q(w+j delta) is not the actual outer polygon.
k=mp.mpf('.6');m=k*k;kp=mp.sqrt(1-m);K=mp.ellipk(m);N=3;v=2*K/N;delta=2*v
sn=lambda z:mp.ellipfun('sn',z,m);cn=lambda z:mp.ellipfun('cn',z,m);dn=lambda z:mp.ellipfun('dn',z,m)
a=dn(v)/cn(v);b=kp/cn(v);Ao=a*dn(v)/cn(v);Bo=b/cn(v)
wrong=[]
for w in (0,K/3):
 P=[(-a*sn(w+j*delta),b*cn(w+j*delta)) for j in range(N)]
 Q=[(-Ao*sn(w+j*delta),Bo*cn(w+j*delta)) for j in range(N)]
 wrong.append(ar(inv(Q,k))/ar(inv(P,k)))
assert abs(wrong[0]-wrong[1])>mp.mpf('1e-8');count+=1
print(json.dumps({'status':'PASS','decimal_digits':mp.mp.dps,'diagnostic_assertions':count,'maximum_scaled_error':mp.nstr(maxerr,14),'families':len(rows),'all_real_areas_positive':positive,'wrong_half_step_ratio_gap':mp.nstr(abs(wrong[0]-wrong[1]),14),'interval_certificate':False,'rows':rows},indent=2,sort_keys=True))
