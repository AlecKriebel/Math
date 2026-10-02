#!/usr/bin/env python3
"""Independent direct geometry diagnostics, not interval certificates."""
import mpmath as m,json
from math import gcd
from collections import Counter
m.mp.dps=85;C=Counter();worst=m.mpf(0)
def ck(e,label,scale=1):
 global worst
 e=abs(e)/max(1,abs(scale));worst=max(worst,e);assert e<m.mpf('1e-60'),(label,str(e));C[label]+=1
def cr(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def hom(a,b):return[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def area(ps):return sum(cr(ps[j],ps[(j+1)%len(ps)]) for j in range(len(ps)))/2
rows=[]
for kval in ('0.17','0.67','0.96'):
 k=m.mpf(kval);kp=m.sqrt(1-k*k);K=m.ellipk(k*k);p=m.j*m.ellipk(1-k*k)
 sn=lambda z:m.ellipfun('sn',z,k*k)
 cn=lambda z:m.ellipfun('cn',z,k*k)
 dn=lambda z:m.ellipfun('dn',z,k*k)
 for N in (6,10,14,18):
  for tau in sorted({1,max(t for t in range(1,N//2) if gcd(t,N)==1)}):
   v=2*K*tau/N;delta=2*v;a=dn(v)/cn(v);b=kp/cn(v)
   def calc(w,focus,controls):
    ps=[[-a*sn(w+j*delta),b*cn(w+j*delta)] for j in range(N)];q=[];u=[]
    for j,P in enumerate(ps):
     Q=ps[(j+1)%N];ell=hom([*P,1],[*Q,1]);z=ell[0]*focus+ell[2];norm=ell[0]**2+ell[1]**2
     foot=[focus-z*ell[0]/norm,-z*ell[1]/norm];q.append(foot)
     V=[P[0]-focus,P[1]];W=[Q[0]-focus,Q[1]];L=[*V,-dot(V,P)];M=[*W,-dot(W,Q)];R=hom(L,M);R=[R[0]/R[2],R[1]/R[2]];u.append(R)
     if controls:
      ck(ell[0]*foot[0]+ell[1]*foot[1]+ell[2],'named_original_side',max(abs(x) for x in ell))
      ck(dot([foot[0]-focus,foot[1]],[Q[0]-P[0],Q[1]-P[1]]),'foot_perpendicular')
      ck(dot(V,R)-dot(V,P),'first_antipedal_named_line',dot(V,P));ck(dot(W,R)-dot(W,Q),'second_antipedal_named_line',dot(W,Q))
      assert cr(V,W)>0;C['focal_consecutive_normals_independent']+=1
    if controls:
     for j in range(N):assert cr([q[j][0]-focus,q[j][1]],[q[(j+1)%N][0]-focus,q[(j+1)%N][1]])>0;C['each_star_pedal_cross_product_positive']+=1
     assert area(q)>0;C['whole_pedal_area_positive']+=1
    return area(u),area(q),sum(dn(w+j*delta) for j in range(N))
   base=None
   for phase in ('0.091','0.337','0.761'):
    w=K*m.mpf(phase);plus=calc(w,k,True);minus=calc(w,-k,True)
    for j in range(2):ck(plus[j]-minus[j],'foci_have_same_signed_area',plus[j])
    ratio=plus[0]/plus[1]
    if base is None:base=plus
    else:
     ck(ratio-base[0]/base[1],'source_ratio_phase_constancy',base[0]/base[1])
     ck(plus[0]/plus[2]-base[0]/base[2],'antipedal_trace_proportionality',base[0]/base[2])
     ck(plus[1]/plus[2]-base[1]/base[2],'pedal_trace_proportionality',base[1]/base[2])
   z=K*m.mpf('0.031')+m.j*m.mpf('0.009');Bplus=calc(p+z,k,False)[0];Bminus=calc(p-z,k,False)[0]
   ck(Bplus+Bminus,'odd_Laurent_symmetry_at_actual_pole',Bplus)
   w=K*m.mpf('0.203')+m.j*m.mpf('0.129');r=calc(w,k,False)[0]
   ck(calc(-w,k,False)[0]-r,'reflection_even_area',r)
   ck(calc(w+2*p,k,False)[0]+r,'imaginary_anti_period_area',r)
   rows.append({'k':kval,'N':N,'winding':tau,'ratio_display':m.nstr(base[0]/base[1],18)})
print(json.dumps({'status':'PASS_DIAGNOSTICS_ONLY','assertions':sum(C.values()),'categories':dict(C),'families':len(rows),'precision_digits':85,'max_scaled_residual':m.nstr(worst,8),'rows':rows,'scope':'Uncertified high-precision controls using actual homogeneous lines and direct projections. Full analytic proof and domain audit are separate.'},indent=2))
