#!/usr/bin/env python3
"""Exact midpoint-refinement controls, using squared vertex multipliers instead of logs."""
from fractions import Fraction as Q
from itertools import product
from collections import Counter,deque
import json
checks=Counter()
def ck(x,label):
 assert x,label
 checks[label]+=1
def key(i,j):return tuple(sorted((i,j)))
def edges(faces):return sorted({key(i,j) for a,b,c in faces for i,j in [(a,b),(b,c),(c,a)]})
def valid(faces,L):return all(L[key(a,b)]+L[key(b,c)]>L[key(c,a)] and L[key(b,c)]+L[key(c,a)]>L[key(a,b)] and L[key(c,a)]+L[key(a,b)]>L[key(b,c)] for a,b,c in faces)
def refine(faces,L):
 E=edges(faces);n=1+max(i for f in faces for i in f);mid={e:n+j for j,e in enumerate(E)};R={};F=[]
 for (i,j),m in mid.items():R[key(i,m)]=R[key(j,m)]=L[i,j]/2
 for i,j,k in faces:
  a,b,c=mid[key(i,j)],mid[key(j,k)],mid[key(k,i)]
  R[key(a,b)]=L[key(i,k)]/2;R[key(b,c)]=L[key(i,j)]/2;R[key(c,a)]=L[key(j,k)]/2
  F.extend([(i,a,c),(j,b,a),(k,c,b),(a,b,c)])
 return F,R,mid
def conformal(faces,L,M):
 # Every component contains a triangle: its odd cycle fixes the squared multiplier.
 R={e:M[e]/L[e] for e in L};adj={i:[] for f in faces for i in f}
 for i,j in L:adj[i].append(j);adj[j].append(i)
 w={}
 for a,b,c in faces:
  if a in w:continue
  w[a]=R[key(a,b)]*R[key(a,c)]/R[key(b,c)];todo=deque([a])
  while todo:
   i=todo.popleft()
   for j in adj[i]:
    v=R[key(i,j)]**2/w[i]
    if j in w:
     if w[j]!=v:return False
    else:w[j]=v;todo.append(j)
 return all(w[i]*w[j]==R[i,j]**2 for i,j in L)
# All ordered integer-sided triangles in this finite box, and every pair of them.
f=[(0,1,2)];E=edges(f);metrics=[]
for lengths in product(range(1,6),repeat=3):
 L=dict(zip(E,map(Q,lengths)))
 if valid(f,L):metrics.append(L)
pairs=0
for L in metrics:
 f1,L1,mid=refine(f,L);ck(valid(f1,L1),'valid_induced_midpoint_metric')
 for M in metrics:
  f2,M1,_=refine(f,M)
  ck(conformal(f,L,M),'single_triangle_original_equivalence')
  homothetic=len({M[e]/L[e] for e in E})==1
  ck(conformal(f1,L1,M1)==homothetic,'triangle_pair_rigidity')
  pairs+=1
 for i,j,k in [(0,1,2),(1,2,0),(2,0,1)]:
  a,b,c=mid[key(i,j)],mid[key(j,k)],mid[key(k,i)]
  ratio=L1[key(i,c)]*L1[key(a,b)]/(L1[key(i,a)]*L1[key(c,b)])
  ck(ratio==(L[key(i,k)]/L[key(i,j)])**2,'refined_crossratio_identity')
# Connected examples with boundary and without boundary.
meshes={'two_face_disk':[(0,1,2),(0,2,3)],'tetrahedron':[(0,1,2),(0,3,1),(0,2,3),(1,3,2)],'octahedron':[(0,2,3),(0,3,4),(0,4,5),(0,5,2),(1,3,2),(1,4,3),(1,5,4),(1,2,5)]}
records={}
for name,faces in meshes.items():
 E=edges(faces);L={e:Q(1) for e in E};n=1+max(i for f in faces for i in f);F,L1,_=refine(faces,L);accepted=rejected=0
 for a in product((Q(3,4),Q(1),Q(5,4)),repeat=n):
  M={e:a[e[0]]*a[e[1]] for e in E}
  if not valid(faces,M):rejected+=1;continue
  F2,M1,_=refine(faces,M)
  ck(conformal(faces,L,M),'mesh_original_vertex_scaling')
  ck(valid(F2,M1),'mesh_refined_triangle_inequalities')
  ck(conformal(F,L1,M1)==(len(set(M.values()))==1),'mesh_midpoint_rigidity')
  accepted+=1
 records[name]={'valid_scalings':accepted,'invalid_scalings_skipped':rejected}
# Exact counterexample and connectedness scope control.
L={e:Q(1) for e in edges(f)};a=[Q(3,2),Q(1),Q(1)];M={e:a[e[0]]*a[e[1]] for e in L};F,L1,mid=refine(f,L);_,M1,_=refine(f,M)
ck(valid(f,M) and conformal(f,L,M) and not conformal(F,L1,M1),'explicit_rational_counterexample')
i,j,k=1,0,2;aa,bb,cc=mid[key(i,j)],mid[key(j,k)],mid[key(k,i)]
value=M1[key(i,cc)]*M1[key(aa,bb)]/(M1[key(i,aa)]*M1[key(cc,bb)])
ck(value==Q(4,9),'counterexample_crossratio_4_over_9')
dis=[(0,1,2),(3,4,5)];E=edges(dis);L={e:Q(1) for e in E};M={e:Q(2 if e[0]<3 else 3) for e in E};F,L1,_=refine(dis,L);_,M1,_=refine(dis,M)
ck(conformal(F,L1,M1) and len(set(M.values()))==2,'disconnected_componentwise_scaling_control')
print(json.dumps({'status':'PASS','arithmetic':'exact rational lengths and squared vertex multipliers','assertions':sum(checks.values()),'by_scope':dict(checks),'valid_ordered_integer_triangles':len(metrics),'all_triangle_pairs':pairs,'mesh_controls':records,'scope':'Only the induced Euclidean midpoint1-to-4 scheme is excluded; the general source existence question and metric-compatibility formulation remain unresolved.'},indent=2,sort_keys=True))
