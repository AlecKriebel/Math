#!/usr/bin/env python3
"""Independent non-interval diagnostics via homogeneous lines and scaled geometry."""
import mpmath as mp
from collections import Counter
from math import gcd
import json
mp.mp.dps=125;C=Counter();errors={}
def ck(e,key,tol='1e-90'):
 e=abs(e);C[key]+=1;errors[key]=max(errors.get(key,mp.mpf(0)),e)
 if e>mp.mpf(tol):raise AssertionError((key,mp.nstr(e,15)))
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def intersection(l,r):
 h=cross(l,r);return(h[0]/h[2],h[1]/h[2])
def anti(P,Q,M):
 n=sub(P,M);m=sub(Q,M)
 return intersection((n[0],n[1],-dot(n,P)),(m[0],m[1],-dot(m,Q)))
def avg(P):return tuple(sum(x[j] for x in P)/len(P) for j in (0,1))
def dist(P,Q):return abs(P[0]-Q[0])+abs(P[1]-Q[1])
casecount=0
for ks in ('0.31','0.8'):
 k=mp.mpf(ks);m=k*k;kp=mp.sqrt(1-m);K=mp.ellipk(m);p=1j*mp.ellipk(1-m);alpha=mp.mpf(7)/3
 sn=lambda z:mp.ellipfun('sn',z,m);cn=lambda z:mp.ellipfun('cn',z,m);dn=lambda z:mp.ellipfun('dn',z,m)
 for N in (4,6,8,10,14):
  for tau in range(1,N//2):
   if gcd(N,tau)>1:continue
   v=2*K*tau/N;delta=2*v;s=sn(v);c=cn(v);d=dn(v)
   a=alpha*d/c;b=alpha*kp/c;Ao=a*d/c;Bo=b/c
   P=lambda u:(-a*sn(u),b*cn(u));R=lambda u:(-Ao*sn(u),Bo*cn(u))
   def tangent(u):
    x,y=P(u);return(x/(a*a),y/(b*b),-1)
   refs={}
   for f in (1,-1):
    M=(f*alpha*k,mp.mpf(0));ref=None
    for w in (K/13,4*K/11,7*K/9):
     Q=[intersection(tangent(w+j*delta-v),tangent(w+j*delta+v)) for j in range(N)]
     for j,z in enumerate(Q):ck(dist(z,R(w+j*delta))/(1+abs(z[0])+abs(z[1])),'direct_scaled_outer_locus')
     U=[anti(Q[j],Q[(j+1)%N],M) for j in range(N)];cen=avg(U)
     for j,z in enumerate(U):
      for jj in (j,(j+1)%N):ck(dot(sub(Q[jj],M),sub(z,Q[jj]))/(1+abs(z[0])**2+abs(z[1])**2),'named_antipedal_line_incidence')
     ck(cen[1]/alpha,'centroid_on_focal_axis')
     if ref is not None:ck(dist(cen,ref)/(1+abs(ref[0])+abs(ref[1])),'scaled_real_phase_invariance')
     ref=cen
     if N==4:ck(dist(cen,(0,0))/alpha,'N4_origin')
    refs[f]=ref
   ck(dist(refs[1],(-refs[-1][0],-refs[-1][1]))/(1+abs(refs[1][0])),'focus_negation')
   if N>=6:
    eps=mp.mpf('1e-24');h=mp.ellipf(mp.asin(alpha/a),m)
    for f in (1,-1):
     M=(f*alpha*k,mp.mpf(0))
     def U(u):return anti(R(u-v),R(u+v),M)
     # Every translated common-pole and coincident-endpoint class.
     for base,tag in [(p,'common_midpoint_regular'),(K+p,'coincident_endpoint_regular')]:
      for rr in (0,2*K):
       for ii in (0,2*p):
        u=base+rr+ii;z1=U(u+eps);z2=U(u-eps)
        ck(dist(z1,z2)/(1+abs(z1[0])+abs(z1[1])),'all_translates_'+tag,'1e-18')
     # Both critical focal roots, with both imaginary translates.
     roots=[p-f*h,p+2*K+f*h]
     for root in roots:
      for ii in (0,2*p):
       u=root+ii
       ck((a/alpha+f*k*sn(u)),'actual_focal_root','1e-95')
       z1=U(u+eps);z2=U(u-eps)
       ck(dist(z1,z2)/(1+abs(z1[0])+abs(z1[1])),'all_isotropic_root_removals','1e-18')
     # Complete centroid beside every common Jacobi-pole translate and a cyclicly moved slot.
     for rr in (0,2*K,delta):
      for ii in (0,2*p):
       w=p+rr+ii+eps
       Q=[R(w+j*delta) for j in range(N)]
       cen=avg([anti(Q[j],Q[(j+1)%N],M) for j in range(N)])
       ck(dist(cen,refs[f])/(1+abs(refs[f][0])+abs(refs[f][1])),'all_translated_cyclic_pole_removals','1e-65')
   casecount+=1
# Explicit nonfocal negative control: phase invariance is not an arbitrary-M theorem.
k=mp.mpf('.55');m=k*k;K=mp.ellipk(m);kp=mp.sqrt(1-m);N=6;v=K/3;delta=2*v
sn=lambda z:mp.ellipfun('sn',z,m);cn=lambda z:mp.ellipfun('cn',z,m);dn=lambda z:mp.ellipfun('dn',z,m)
A=dn(v)**2/cn(v)**2;B=kp/cn(v)**2;R=lambda u:(-A*sn(u),B*cn(u));M=(k/2,mp.mpf('.2'));cens=[]
for w in (0,K/7):
 Q=[R(w+j*delta) for j in range(N)];cens.append(avg([anti(Q[j],Q[(j+1)%N],M) for j in range(N)]))
gap=dist(*cens);assert gap>mp.mpf('1e-10');C['nonfocal_phase_negative_control']+=1
print(json.dumps({'status':'PASS','decimal_digits':mp.mp.dps,'diagnostic_assertions':sum(C.values()),'primitive_families':casecount,'counts':dict(C),'maximum_residuals':{k:mp.nstr(v,13) for k,v in errors.items()},'nonfocal_centroid_gap':mp.nstr(gap,15),'interval_certificate':False,'scope':'Actual scaled Euclidean geometry, both foci, every translated local singularity type and complex cyclic sums. Non-interval finite diagnostics only.'},indent=2,sort_keys=True))
