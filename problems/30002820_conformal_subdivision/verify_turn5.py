#!/usr/bin/env python3
"""Exact certificates for the stellar height obstruction and positive disk scope control."""
from fractions import Fraction as Q
from itertools import product,combinations
from collections import Counter,deque
import json
checks=Counter()
def ck(x,label):
 assert x,label;checks[label]+=1
def edge(i,j):return tuple(sorted((i,j)))
def tri(a,b,c):return a+b>c and a+c>b and b+c>a
F=[(0,1,2),(0,1,3),(0,2,3),(1,2,3)];E=sorted({edge(i,j) for f in F for i,j in combinations(f,2)})
certs=[]
for beta,gamma in product([Q(i,4) for i in range(1,7)],repeat=2):
 for extra in (Q(0),Q(1,4),Q(1,2)):
  alpha=max(beta,gamma)+extra;delta=alpha-abs(beta-gamma);S=beta+gamma
  ck(delta>0,'positive_maximal_distance_gap')
  # Rational Pythagorean heights give rational closed-sphere edge metrics.
  n=2
  while True:
   r=Q(n,n+1);h=(1-r*r)/(4*r);b=(1+r*r)/(4*r)
   if h<=Q(1,4) and h<delta/(6*S):break
   n+=1
  ck(b*b==Q(1,4)+h*h and 0<h<=Q(1,4),'rational_thin_triangle_realization')
  ck(delta/S>3*h,'strict_linear_contradiction_certificate')
  a=[b,Q(1),Q(1),Q(3,4)];L={e:a[e[0]]*a[e[1]] for e in E}
  ck(all(tri(L[edge(i,j)],L[edge(i,k)],L[edge(j,k)]) for i,j,k in F),'valid_intrinsic_closed_sphere_input')
  ck(L[1,2]==1 and L[0,1]==L[0,2]==b,'chosen_face_exact_height')
  for I in range(9):
   for J in range(9-I):
    u=Q(I,8);v=Q(J,8);x=u/2+v;y=u*h
    ck(x*x+y*y<=(x+h)**2,'base_vertex_distance_bound_j')
    ck((1-x)**2+y*y<=(1-x+h)**2,'base_vertex_distance_bound_k')
    ck((x-Q(1,2))**2+(y-h)**2<=(abs(x-Q(1,2))+h)**2,'apex_distance_bound')
  certs.append({'alpha':str(alpha),'beta':str(beta),'gamma':str(gamma),'height':str(h),'equal_side':str(b)})
# Positive isometric one-edge disk rule, with actual induced squared diagonal length.
def refine(a,b,c):
 t=b/(a+b);H=(1-t)*b*b+t*a*a-t*(1-t)*c*c
 return {(0,3):(t*c)**2,(1,3):((1-t)*c)**2,(0,2):b*b,(1,2):a*a,(2,3):H},t
faces=[(0,3,2),(3,1,2)]
def conformal(L,M):
 ratio={e:M[e]/L[e] for e in L};adj={v:[] for v in range(4)}
 for i,j in L:adj[i].append(j);adj[j].append(i)
 i,j,k=faces[0];w={i:ratio[edge(i,j)]*ratio[edge(i,k)]/ratio[edge(j,k)]};todo=deque([i])
 while todo:
  i=todo.popleft()
  for j in adj[i]:
   t=ratio[edge(i,j)]**2/w[i]
   if j in w:
    if w[j]!=t:return False
   else:w[j]=t;todo.append(j)
 return True
metrics=[]
for aa,bb,cc in product(range(1,6),repeat=3):
 a,b,c=Q(aa),Q(bb),Q(cc)
 if not tri(a,b,c):continue
 L,t=refine(a,b,c)
 ck(L[0,2]*L[1,3]==L[1,2]*L[0,3],'angle_foot_squared_crossratio_one')
 for i,j,k in faces:
  A,B,C=L[edge(i,j)],L[edge(i,k)],L[edge(j,k)]
  ck(A>0 and B>0 and C>0 and 2*(A*B+A*C+B*C)-A*A-B*B-C*C>0,'induced_disk_triangles_nondegenerate')
 metrics.append(L)
for L in metrics:
 for M in metrics:ck(conformal(L,M),'all_disk_refinement_pairs_conformal')
print(json.dumps({'status':'PASS','arithmetic':'exact rational height certificates and squared lengths','assertions':sum(checks.values()),'by_scope':dict(checks),'rational_stellar_obstruction_certificates':len(certs),'max_pythagorean_height':str(max(Q(x['height']) for x in certs)),'disk_metrics':len(metrics),'disk_metric_pairs':len(metrics)**2,'scope':'The universal stellar obstruction is a proof, not a finite search. The positive isometric edge rule is restricted to one triangular disk. The intended all-surface isometric source problem remains unresolved.'},indent=2,sort_keys=True))
