#!/usr/bin/env python3
"""Independent direct original-focal geometry; floating diagnostics only."""
import mpmath as m,json
from collections import Counter
from math import gcd
m.mp.dps=80;C=Counter();worst=m.mpf(0)
def ck(e,k,scale=1):
 global worst
 x=abs(e)/max(1,abs(scale));worst=max(worst,x);assert x<m.mpf('1e-57'),(k,str(x));C[k]+=1
def cr(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def hom(p,q):return[p[1]*q[2]-p[2]*q[1],p[2]*q[0]-p[0]*q[2],p[0]*q[1]-p[1]*q[0]]
def ar(P):return sum(cr(P[j],P[(j+1)%len(P)]) for j in range(len(P)))/2
rows=[]
for kk in ('0.31','0.89'):
 k=m.mpf(kk);K=m.ellipk(k*k);bp=m.sqrt(1-k*k)
 sn=lambda w:m.ellipfun('sn',w,k*k)
 cn=lambda w:m.ellipfun('cn',w,k*k)
 dn=lambda w:m.ellipfun('dn',w,k*k)
 for N in (4,8,12,16):
  for tau in sorted({1,max(t for t in range(1,N//2) if gcd(t,N)==1)}):
   v=2*K*tau/N;delta=2*v;a=dn(v)/cn(v);b=bp/cn(v);base=None
   for phase in ('0.113','0.397','0.783'):
    w=K*m.mpf(phase);P=[[-a*sn(w+j*delta),b*cn(w+j*delta)] for j in range(N)];out=[]
    for focus in (k,-k):
     IV=[];AN=[]
     for j,p in enumerate(P):
      q=P[(j+1)%N];V=[p[0]-focus,p[1]];W=[q[0]-focus,q[1]];norm=dot(V,V)
      assert norm>0 and cr(V,W)>0;C['both_objects_finite']+=1
      inv=[focus+V[0]/norm,V[1]/norm];IV.append(inv)
      ck(dot([inv[0]-focus,inv[1]],V)-1,'exact_named_unit_inversion_relation')
      R=hom([*V,-dot(V,p)],[*W,-dot(W,q)]);R=[R[0]/R[2],R[1]/R[2]];AN.append(R)
      ck(dot(V,R)-dot(V,p),'first_named_antipedal_line',dot(V,p));ck(dot(W,R)-dot(W,q),'second_named_antipedal_line',dot(W,q))
     out.append((ar(P),ar(IV),ar(AN)))
    for j in (1,2):ck(out[0][j]-out[1][j],'opposite_focus_area_equality',out[0][j])
    A,V,B=out[0]
    if base is None:base=(A,V,B)
    else:
     ck(A*V-base[0]*base[1],'input_inverse_area_product',base[0]*base[1])
     ck(B/A-base[2]/base[0],'input_antipedal_proportionality',base[2]/base[0])
     ck(V*B-base[1]*base[2],'source_corollary_product',base[1]*base[2])
    if N==4:ck(V*B-8,'unit_N4_value_eight',8)
   rows.append({'k':kk,'N':N,'winding':tau,'product_display':m.nstr(base[1]*base[2],18)})
print(json.dumps({'status':'PASS_DIAGNOSTICS_ONLY','assertions':sum(C.values()),'categories':dict(C),'families':len(rows),'precision_digits':80,'max_scaled_residual':m.nstr(worst,8),'rows':rows,'scope':'Finite unverified floating diagnostics using direct geometry; universal result rests on the separately audited exact inputs and algebraic corollary.'},indent=2))
