#!/usr/bin/env python3
"""Exact incidence and rotation-system controls; no numerical knot identification."""
from itertools import combinations,product
from collections import Counter
import json
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
for n in range(2,6):
 possible=list(combinations(range(n),2))
 for mask in range(1,1<<len(possible)):
  edges=[e for i,e in enumerate(possible) if mask>>i&1]
  seen={0}
  while True:
   nxt=seen|{v for u,v in edges if u in seen}|{u for u,v in edges if v in seen}
   if nxt==seen:break
   seen=nxt
  if len(seen)!=n:continue
  deg=[sum(v in e for e in edges) for v in range(n)]
  for signs in product((-1,1),repeat=len(edges)):
   sums=[sum(s for e,s in zip(edges,signs) if v in e) for v in range(n)]
   saturated=all(abs(x)==d for x,d in zip(sums,deg));uniform=len(set(signs))==1
   ck(saturated==uniform,'connected_graph_saturation_iff_uniform')
   ck((sum(map(abs,sums))==2*len(edges))==saturated,'aggregate_saturation')
   minority=sum(min((d+x)//2,(d-x)//2) for d,x in zip(deg,sums))
   ck(2*len(edges)-sum(map(abs,sums))==2*minority,'integral_defect_identity')
# Loops and parallel edges count incidences with multiplicity.
for edges in [[(0,0)],[(0,0),(0,1),(0,1),(1,1)],[(0,1)]*4,[(0,0),(0,1),(1,2),(2,2)]]:
 n=1+max(max(e) for e in edges)
 for signs in product((-1,1),repeat=len(edges)):
  vals=[sum(s*e.count(v) for e,s in zip(edges,signs)) for v in range(n)]
  deg=[sum(e.count(v) for e in edges) for v in range(n)]
  ck(all(abs(x)==d for x,d in zip(vals,deg))==(len(set(signs))==1),'loop_parallel_incidence_control')
rot={0:(1,2,3,4),1:(2,0,4),2:(3,0,1),3:(4,0,2),4:(1,0,3)}
def edge(v,w):return tuple(sorted((v,w)))
E=sorted({edge(v,w) for v,ns in rot.items() for w in ns})
# Face cycles of the planar rotation system.
darts=[(v,w) for v,ns in rot.items() for w in ns];seen=set();faces=[]
for q in darts:
 if q in seen:continue
 f=[]
 while q not in seen:
  seen.add(q);f.append(q);v,w=q;ns=rot[w];q=w,ns[(ns.index(v)+1)%len(ns)]
 faces.append(f)
ck(len(rot)-len(E)+len(faces)==2,'wheel_spherical_rotation_system')
ck(sorted(map(len,faces))==[3,3,3,3,4],'wheel_face_degrees')
corners={}
for v,ns in rot.items():
 for i,w in enumerate(ns):corners[v,i]=(edge(v,w),edge(v,ns[(i+1)%len(ns)]))
opp={}
for e in E:
 u,v=e;ui=rot[u].index(v);vi=rot[v].index(u)
 for c,d in [((u,ui),(v,vi)),((u,(ui-1)%len(rot[u])),(v,(vi-1)%len(rot[v])))]:opp[e,c]=d;opp[e,d]=c
seen=set();cycles=[]
for q in opp:
 if q in seen:continue
 cyc=[]
 while q not in seen:
  seen.add(q);cyc.append(q);e,c=q;f=next(x for x in corners[c] if x!=e);q=f,opp[f,c]
 cycles.append(cyc)
ck(len(cycles)==2 and sorted(map(len,cycles))==[16,16],'wheel_medial_one_unoriented_component')
ck(len(seen)==32,'all_medial_halfedges_covered')
signs={e:1 for e in E};signs[0,1]=-1
black={v:sum(signs[edge(v,w)] for w in ns) for v,ns in rot.items()}
white=[-sum(signs[edge(*e)] for e in f) for f in faces]
ck(list(black.values())==[2,1,3,3,3],'wheel_black_twice_gleams')
ck(sorted(white)==[-4,-3,-3,-1,-1],'wheel_white_twice_gleams')
ck(all(v>0 for v in black.values()) and all(v<0 for v in white),'strict_checkerboard_signs_without_uniform_crossings')
word=[];allplus=[];changed=[]
labels={(0,1):'a',(0,2):'b',(0,3):'c',(0,4):'d',(1,2):'e',(2,3):'f',(3,4):'g',(1,4):'h'}
for e,(v,i) in cycles[0]:
 w=next(x for x in e if x!=v);following=(i==rot[v].index(w))
 word.append(labels[e]);allplus.append(int(following));changed.append(int(following)^(signs[e]<0))
ck(' '.join(word)=='a b f g d a e f c d h e b c g h','exact_medial_visit_word')
ck(all(allplus[i]!=allplus[(i+1)%16] for i in range(16)),'uniform_sign_diagram_alternating')
ck(sum(changed[i]==changed[(i+1)%16] for i in range(16))==4,'single_sign_change_breaks_four_arcs')
ck((2*len(E)-sum(abs(x) for x in black.values()))//2==2,'wheel_defect_two')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'wheel':{'rotation':rot,'black_twice_gleams':black,'white_twice_gleams':white,'crossing_visit_word':word,'all_positive_over_bits':allplus,'one_changed_over_bits':changed,'unoriented_components':len(cycles)//2},'scope':'Finite algebraic and explicit plane-rotation certificate checks. The volume consequence uses the cited theorem and does not extend to unmarked general shadows.'},indent=2))
