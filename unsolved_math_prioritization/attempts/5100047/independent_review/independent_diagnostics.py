#!/usr/bin/env python3
"""Independent direct geometry plus complex trace diagnostics; not interval certificates."""
import mpmath as mp
from math import gcd
from collections import Counter
import json
mp.mp.dps=85;counts=Counter();err=mp.mpf(0);rows=[]
def close(x,y,label):
 global err
 r=abs(x-y)/(1+abs(x)+abs(y));err=max(err,r);assert r<mp.mpf('1e-65'),(label,str(r));counts[label]+=1
def positive(x,label):assert x>0,label;counts[label]+=1
def det(P,Q):return P[0]*Q[1]-P[1]*Q[0]
def dot(P,Q):return P[0]*Q[0]+P[1]*Q[1]
def area(P):return sum(det(P[j],P[(j+1)%len(P)]) for j in range(len(P)))/2
def invert(P,focus):
 I=[]
 for x,y in P:
  R=(x-focus,y);d=dot(R,R);positive(d,'finite_actual_inverse');J=(R[0]/d,R[1]/d);close(dot(J,J)*d,1,'named_unit_inversion');I.append(J)
 return I
for kval in ['0.12','0.74','0.97']:
 k=mp.mpf(kval);m=k*k;kp=mp.sqrt(1-m);K=mp.ellipk(m);p=1j*mp.ellipk(1-m);alpha=mp.mpf('1.37')
 sn=lambda z:mp.ellipfun('sn',z,m);cn=lambda z:mp.ellipfun('cn',z,m);dn=lambda z:mp.ellipfun('dn',z,m)
 for N in [3,4,5,6,7,8,10,12]:
  for tau in range(1,(N+1)//2):
   if gcd(N,tau)!=1:continue
   v=2*K*tau/N;delta=2*v;h=sn(v);C=cn(v);d=dn(v);q=C*C;t=h*h
   a=alpha*d/C;b=alpha*kp/C;focus=alpha*k;Ao=a*d/C;Bo=b/C
   U=1-2*m*t+m*t*t;V=1-2*t+m*t*t;L0=(U*U-m*V*V*t)/d;L1=(V*V-U*U*t)/C
   cp=b*h*d*q*q/alpha**3;cq=Bo*h*d*q**4/(alpha**3*C)
   E=lambda u:cp*dn(u)*(1-m*t*sn(u)**2)/((1+k*sn(u))*(U+k*V*sn(u))**2)
   G=lambda u:cq*dn(u)*(1-m*t*sn(u)**2)/((d+k*C*sn(u))**2*(L0+k*L1*sn(u)))
   F=lambda u:sum(E(u+j*delta) for j in range(N));H=lambda u:sum(G(u+j*delta) for j in range(N))
   ratios=[]
   for w in [K/mp.mpf(13),K*mp.mpf(9)/17,K*mp.mpf(19)/23]:
    P=[(-a*sn(w+j*delta),b*cn(w+j*delta)) for j in range(N)];Q=[]
    for j in range(N):
     nx,ny=P[j][0]/a**2,P[j][1]/b**2;mx,my=P[(j+1)%N][0]/a**2,P[(j+1)%N][1]/b**2;D=nx*my-ny*mx
     R=((my-ny)/D,(nx-mx)/D);Q.append(R)
     close(nx*R[0]+ny*R[1],1,'first_specific_tangent');close(mx*R[0]+my*R[1],1,'second_specific_tangent')
     close(R[0],-Ao*sn(w+v+j*delta),'outer_midphase_x');close(R[1],Bo*cn(w+v+j*delta),'outer_midphase_y')
    for fc in [focus,-focus]:
     I=invert(P,fc);J=invert(Q,fc);A=area(I);B=area(J);positive(A,'positive_original_area');positive(B,'positive_outer_area');ratios.append(B/A)
     for j in range(N):positive(det(I[j],I[(j+1)%N]),'positive_original_edge');positive(det(J[j],J[(j+1)%N]),'positive_outer_edge')
     if fc==focus:close(A,F(w+v),'original_trace_actual_area');close(B,H(w+2*v),'outer_trace_actual_area')
   for R in ratios:close(R,ratios[0],'phase_and_focus_ratio')
   if N==4:close(ratios[0],mp.mpf(1)/2,'N4_exact_ratio_half')
   # Meromorphic controls away from pole classes. All use bilinear rather than conjugate norms.
   z=K*mp.mpf('0.217')+p*mp.mpf('0.173');r=3*K+p;ell=4*K/N
   close(E(2*r-z),-E(z),'original_odd_reflection');close(G(2*r-z),-G(z),'outer_odd_reflection')
   close(F(z+ell),F(z),'original_quotient_period');close(H(z+ell),H(z),'outer_quotient_period')
   close(F(z+2*p),-F(z),'original_imaginary_antiperiod');close(H(z+2*p),-H(z),'outer_imaginary_antiperiod')
   close(H(z+v),ratios[0]*F(z),'full_complex_shifted_comparison')
   rows.append({'k':kval,'N':N,'winding':tau,'ratio_display':mp.nstr(ratios[0],20)})
print(json.dumps({'status':'PASS_DIAGNOSTICS_ONLY','assertions':sum(counts.values()),'categories':dict(counts),'families':len(rows),'precision_digits':mp.mp.dps,'maximum_scaled_residual':mp.nstr(err,10),'interval_certificates':False,'rows':rows},indent=2))
