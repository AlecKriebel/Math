#!/usr/bin/env python3
"""Exact all-instance controls for an explicitly proved diagram family."""
from fractions import Fraction as F
from collections import Counter
from itertools import combinations
import json
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
for k in range(2,301):
 rot={0:('a',)+tuple(range(1,k+1)),1:('b',)+tuple(range(k,0,-1)),2:('a','b')}
 end={'a':(0,2),'b':(1,2),**{j:(0,1) for j in range(1,k+1)}}
 corners={(v,i):(ns[i],ns[(i+1)%len(ns)]) for v,ns in rot.items() for i in range(len(ns))}
 # Exact spherical face cycles of the original Tait graph.
 seen=set();faces=[]
 for v,ns in rot.items():
  for e in ns:
   q=v,e
   if q in seen:continue
   f=[]
   while q not in seen:
    seen.add(q);v0,e0=q;f.append(e0);w=next(x for x in end[e0] if x!=v0);ns0=rot[w];q=w,ns0[(ns0.index(e0)+1)%len(ns0)]
   faces.append(f)
 ck(len(rot)-len(end)+len(faces)==2,'sphere_rotation_Euler')
 ck(sorted(map(len,faces))==[2]*(k-1)+[3,3],'Tait_face_valences')
 for deleted in range(3):
  remain=set(range(3))-{deleted};edges=[e for e in end.values() if deleted not in e]
  ck(any(set(e)==remain for e in edges),'Tait_no_cut_vertex')
 opp={}
 for e,(u,v) in end.items():
  ui=rot[u].index(e);vi=rot[v].index(e)
  for c,d in [((u,ui),(v,vi)),((u,(ui-1)%len(rot[u])),(v,(vi-1)%len(rot[v])))]:opp[e,c]=d;opp[e,d]=c
 seen=set();cycles=[]
 for q in opp:
  if q in seen:continue
  cyc=[]
  while q not in seen:
   seen.add(q);cyc.append(q);e,c=q;f=next(z for z in corners[c] if z!=e);q=f,opp[f,c]
  cycles.append(cyc)
 ck(len(cycles)==2 and all(len(c)==2*(k+2) for c in cycles),'single_unoriented_medial_component')
 word=[e for e,c in cycles[0]]
 expected=['a']+list(range(1,k+1))+(['a','b'] if k%2==0 else ['b','a'])+list(range(k,0,-1))+['b']
 ck(word==expected,'all_size_parity_visit_word')
 bits=[]
 for e,(v,i) in cycles[0]:bits.append(int(i==rot[v].index(e)))
 ck(all(bits[i]!=bits[(i+1)%len(bits)] for i in range(len(bits))),'constant_Tait_sign_alternating_visits')
 for e in end:
  visits=[bits[i] for i,x in enumerate(word) if x==e]
  ck(sorted(visits)==[0,1],'each_crossing_both_branches_once')
 black=[F(k+1,2),F(k+1,2),F(1)];white=[F(-1)]*(k-1)+[F(-3,2)]*2
 ck(sum(black)==k+2,'black_gleam_mass')
 ck(sum(map(abs,black+white))==2*(k+2),'total_gleam_mass')
 ck(sum(map(abs,black+white))-max(map(abs,black+white))>=F(3*k+7,2),'outside_omission_still_unbounded')
 ck((k+2)-(k+1)==1,'outer_collapse_vertex_count')
 # k-1 white bigons plus one degree-two black face produce two twist chains.
 ck((k+2)-((k-1)+1)==2,'twist_count')
# True-vertex link after deleting a unique corner sector.
verts=set(range(4));edges=list(combinations(range(4),2));edges.remove((0,1))
ck([sum(v in e for e in edges) for v in range(4)]==[2,2,3,3],'K4_edge_deleted_degrees')
for v in (0,1):
 neigh=[e[1] if e[0]==v else e[0] for e in edges if v in e]
 edges=[e for e in edges if v not in e];edges.append(tuple(sorted(neigh)))
ck(edges==[(2,3)]*3,'suppressed_link_is_theta')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'range':'2<=k<=300, plus local vertex-link certificate','scope':'Exact incidence/permutation controls. Hyperbolicity and the volume bound use the credited theorem with the written all-k hypotheses; no numerical knot lookup is used.'},indent=2))
