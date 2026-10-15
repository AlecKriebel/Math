#!/usr/bin/env python3
"""Independent direct geometric diagnostics; not interval certificates."""
import mpmath as m
from math import gcd
from collections import Counter
import json
m.mp.dps=80;C=Counter();worst=m.mpf(0)
def ck(e,label,scale=1):
 global worst
 r=abs(e)/max(1,abs(scale));worst=max(worst,r);assert r<m.mpf('1e-60'),(label,str(r));C[label]+=1
def cr(p,q):return p[0]*q[1]-p[1]*q[0]
def d(p,q):return p[0]*q[0]+p[1]*q[1]
def hom(p,q):return(p[1]*q[2]-p[2]*q[1],p[2]*q[0]-p[0]*q[2],p[0]*q[1]-p[1]*q[0])
def ar(ps):return sum(cr(ps[j],ps[(j+1)%len(ps)]) for j in range(len(ps)))/2
rows=[]
for k in [m.mpf(1)/4,m.mpf(4)/5]:
 K=m.ellipk(k*k);kp=m.sqrt(1-k*k)
 sn=lambda z:m.ellipfun('sn',z,k*k)
 cn=lambda z:m.ellipfun('cn',z,k*k)
 dn=lambda z:m.ellipfun('dn',z,k*k)
 for N in (3,5,7,11):
  for t in sorted({1,(N-1)//2}):
   v=2*K*t/N;delta=2*v;alpha=m.mpf(3);beta=alpha*kp;a=alpha*dn(v)/cn(v);b=beta/cn(v)
   products=[];ratios=[]
   for phase in [m.mpf(17)/100,m.mpf(41)/100,m.mpf(79)/100]:
    w=K*phase;ps=[(-a*sn(w+j*delta),b*cn(w+j*delta)) for j in range(N)];feet=[];anti=[]
    for j,p in enumerate(ps):
     q=ps[(j+1)%N];L=hom((*p,1),(*q,1));Q=(-L[2]*L[0]/(L[0]**2+L[1]**2),-L[2]*L[1]/(L[0]**2+L[1]**2));feet.append(Q)
     ck(L[0]*Q[0]+L[1]*Q[1]+L[2],'named_original_support_line',max(abs(x) for x in L))
     ck(d(Q,(q[0]-p[0],q[1]-p[1])),'perpendicular_projection')
     ck(L[0]**2*alpha**2+L[1]**2*beta**2-L[2]**2,'same_caustic_dual_tangency',L[2]**2)
     T=hom((*p,-d(p,p)),(*q,-d(q,q)));R=(T[0]/T[2],T[1]/T[2]);anti.append(R)
     ck(d(p,R)-d(p,p),'first_named_antipedal_line',d(p,p));ck(d(q,R)-d(q,q),'second_named_antipedal_line',d(q,q))
     assert cr(p,q)>0;C['consecutive_determinant_positive']+=1
    U=ar(anti);V=ar(feet);products.append(U*V)
    S=sum(dn(w+j*delta) for j in range(N));ratios.append(U/S)
   for val in products[1:]:ck(val-products[0],'source_area_product',products[0])
   for val in ratios[1:]:ck(val-ratios[0],'antipedal_trace_ratio',ratios[0])
   rows.append({'k':str(k),'N':N,'winding':t,'product_display':m.nstr(products[0],18)})
print(json.dumps({'status':'PASS_DIAGNOSTICS_ONLY','assertions':sum(C.values()),'categories':dict(C),'decimal_digits':80,'families':len(rows),'max_scaled_residual':m.nstr(worst,8),'rows':rows,'scope':'Uncertified high-precision direct geometric diagnostics; the written meromorphic proof and its separate audit establish the theorem.'},indent=2))
