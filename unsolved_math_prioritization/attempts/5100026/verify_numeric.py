#!/usr/bin/env python3
"""Locally authored high-precision geometry diagnostics, explicitly not proof."""
import math,json,mpmath as mp
from collections import Counter
mp.mp.dps=110;C=Counter();worst={};families=0

def ck(x,key,tol='1e-75'):
 x=abs(x);assert x<mp.mpf(tol),(key,mp.nstr(x,12));C[key]+=1;worst[key]=max(worst.get(key,mp.mpf(0)),x)
def vadd(a,b):return(a[0]+b[0],a[1]+b[1])
def vsub(a,b):return(a[0]-b[0],a[1]-b[1])
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def norm(a):return abs(a[0])+abs(a[1])
def lines(n,h,q,g):
 dd=det(n,q);return((h*q[1]-g*n[1])/dd,(n[0]*g-q[0]*h)/dd)
def avg(vs):return(tuple(sum(v[i] for v in vs)/len(vs) for i in (0,1)))
for N in range(4,25,2):
 for tau in range(1,N//2):
  if math.gcd(N,tau)>1:continue
  for kk in ('0.17','0.63','0.94'):
   k=mp.mpf(kk);kp=mp.sqrt(1-k*k);K=mp.ellipk(k*k);p=1j*mp.ellipk(kp*kp);v=2*K*tau/N;delta=2*v
   sn=lambda w:mp.ellipfun('sn',w,k*k);cn=lambda w:mp.ellipfun('cn',w,k*k);dn=lambda w:mp.ellipfun('dn',w,k*k)
   s=sn(v);c=cn(v);d=dn(v);a=d/c;b=kp/c;A=d*d/(c*c);B=kp/(c*c)
   P=lambda w:(-a*sn(w),b*cn(w));R=lambda w:(-A*sn(w),B*cn(w))
   normal=lambda w:(-sn(w)/a,cn(w)/b)
   def anti(x,y,M):
    q=vsub(x,M);t=vsub(y,M);return vadd(M,lines(q,dot(q,q),t,dot(t,t)))
   def U(u,M):return anti(R(u-v),R(u+v),M)
   references={}
   for focus in (-1,1):
    M=(focus*k,mp.mpf(0));ref=None
    for ph in (mp.mpf(0),mp.mpf(3)/19,mp.mpf(11)/23):
     w=ph*K;rs=[]
     for j in range(N):
      u=w+j*delta
      n1=normal(u-v);n2=normal(u+v);direct=lines(n1,1,n2,1);r=R(u);rs.append(direct)
      ck(norm(vsub(direct,r))/(1+norm(r)),'actual_outer_tangent_intersection')
      q=vsub(R(u-v),M);t=vsub(R(u+v),M)
      expected=2*B*s*d*dn(u)*(a+focus*k*sn(u))/(1-k*k*s*s*sn(u)**2)
      ck((det(q,t)-expected)/(1+abs(expected)),'actual_antipedal_determinant')
      assert det(q,t)>0;C['positive_real_determinant']+=1
     us=[anti(rs[j],rs[(j+1)%N],M) for j in range(N)];cen=avg(us)
     for j,q in enumerate(us):
      n1=vsub(rs[j],M);n2=vsub(rs[(j+1)%N],M)
      ck((dot(n1,vsub(q,rs[j])))/(1+norm(n1)*norm(q)),'antipedal_first_line_incidence')
      ck((dot(n2,vsub(q,rs[(j+1)%N])))/(1+norm(n2)*norm(q)),'antipedal_second_line_incidence')
     ck(cen[1]/(1+norm(cen)),'focal_axis_centroid')
     if ref is not None:ck(norm(vsub(cen,ref))/(1+norm(ref)),'real_phase_constancy')
     ref=cen
     if N==4:ck(norm(cen),'four_period_origin')
    references[focus]=ref
   ck(norm(vadd(references[-1],references[1]))/(1+norm(references[1])),'opposite_focus_negation')
   if N>=6:
    eps=mp.mpf('1e-28');M=(k,mp.mpf(0));h=mp.ellipf(mp.asin(1/a),k*k)
    for u,key in [(K+p,'coincident_endpoint_removal'),(p-h,'isotropic_focus_removal'),(p,'midpoint_Jacobi_pole_regular')]:
     up=U(u+eps,M);um=U(u-eps,M)
     ck(norm(vsub(up,um))/(1+norm(up)+norm(um)),key,'1e-22')
    # Entire cyclic sum evaluated next to a genuine outer-vertex pole, not in a real sample.
    for shift in (mp.mpf(0),2*p):
     w=p+shift+eps
     rr=[R(w+j*delta) for j in range(N)]
     cen=avg([anti(rr[j],rr[(j+1)%N],M) for j in range(N)])
     ck(norm(vsub(cen,references[1]))/(1+norm(references[1])),'complex_complete_pole_cancellation','1e-45')
   families+=1
print(json.dumps({'status':'PASS','precision_digits':mp.mp.dps,'primitive_families':families,'diagnostics':sum(C.values()),'families':dict(C),'max_normalized_residuals':{k:mp.nstr(v,10) for k,v in worst.items()},'limitations':'Finite high-precision diagnostics only. Exact singularity removal and every primitive even period are proved in PROOF.md.'},indent=2))
