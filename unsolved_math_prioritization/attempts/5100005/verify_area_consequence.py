#!/usr/bin/env python3
"""Exact target-specific area consequence of the prior PR147 witness.
No prior search/verifier is rerun or imported; this checks only contact/outer
polygon construction and the newly evaluated printed expression.
"""
from fractions import Fraction as F
import json
A2,B2=F(16),F(9);C2,D2=F(256,25),F(81,25)
orbits={'diamond':[(F(4),F(0)),(F(0),F(3)),(F(-4),F(0)),(F(0),F(-3))],
 'rectangle':[(F(16,5),F(9,5)),(F(-16,5),F(9,5)),(F(-16,5),F(-9,5)),(F(16,5),F(-9,5))]}
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def area(P):return sum(det(p,q) for p,q in zip(P,P[1:]+P[:1]))/2
def two_tangents(p,q):
 a,b=p[0]/A2,p[1]/B2;c,d=q[0]/A2,q[1]/B2
 v=a*d-b*c;assert v
 return((d-b)/v,(a-c)/v)
assert A2-C2==B2-D2==F(144,25) and 0<A2-C2<B2
factor=C2*D2/(A2*B2);assert factor==F(144,625)
results={}
for name,P in orbits.items():
 assert len(set(P))==4
 assert all(p[0]*p[0]/A2+p[1]*p[1]/B2==1 for p in P)
 outer=[];inner=[]
 for p,q in zip(P,P[1:]+P[:1]):
  v=sub(q,p);n=(v[1],-v[0]);h=dot(n,p);assert h
  assert C2*n[0]*n[0]+D2*n[1]*n[1]==h*h
  contact=(C2*n[0]/h,D2*n[1]/h)
  assert contact[0]*contact[0]/C2+contact[1]*contact[1]/D2==1
  j=0 if v[0] else 1;t=(contact[j]-p[j])/v[j]
  assert 0<t<1 and contact==(p[0]+t*v[0],p[1]+t*v[1])
  T=two_tangents(p,q)
  assert contact==(C2/A2*T[0],D2/B2*T[1])
  outer.append(T);inner.append(contact)
 a,ap,app=map(area,[P,outer,inner]);assert a>0 and ap>0 and app>0
 assert app==factor*ap
 results[name]={'original_area':str(a),'outer_area':str(ap),'inner_area':str(app),'old_k111_Aprime_Asecond':str(ap*app),'k110_control_A_Asecond':str(a*app),'outer_vertices':[[str(v) for v in p] for p in outer],'contact_vertices':[[str(v) for v in p] for p in inner]}
assert results['diamond']['old_k111_Aprime_Asecond']=='331776/625'
assert results['rectangle']['old_k111_Aprime_Asecond']=='576'
assert F(results['rectangle']['old_k111_Aprime_Asecond'])-F(results['diamond']['old_k111_Aprime_Asecond'])==F(28224,625)
assert results['diamond']['k110_control_A_Asecond']==results['rectangle']['k110_control_A_Asecond']=='165888/625'
print(json.dumps({'status':'PASS','arithmetic':'exact rational, Python standard library','prior_witness':'AlecKriebel/Math PR147, problem5100001, commit502de2f863a63ca205814da4194411847797a7c3','new_proof_search_turns':0,'new_discovery_claim':False,'area_scale_factor':str(factor),'positive_difference':str(F(28224,625)),'results':results},indent=2))
