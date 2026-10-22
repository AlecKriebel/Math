#!/usr/bin/env python3
"""Independent finite audits of the scoped constructions, using exact fractions."""
from fractions import Fraction as F
from itertools import combinations
from bisect import bisect_left
from collections import Counter
import json
C=Counter()
def ck(v,k):
 assert v,k;C[k]+=1
# A nonlinear flattening, distinct from the author's affine control.
for r,s in combinations([F(i,12) for i in range(13)],2):
 for c in [F(-1),F(-1,2),F(0),F(1,2),F(1)]:
  z=F(1,2);a=(1-z)*r+z*s+c*z*(1-z)*(r-s)
  ck(r<a<s,'strict_nonlinear_collision')
  diagonal=(1-z)*a+z*a+c*z*(1-z)*(a-a)
  ck(a==diagonal,'shared_output_diagonal')
  for t in [F(i,12) for i in range(13)]:
   val=(1-t)*r+t*s+c*t*(1-t)*(r-s)
   ck(r<=val<=s,'nonlinear_map_range')
# A fresh construction of every exclusion history through n=7 and global decoder mesh.
totalhist=0
for n in range(1,8):
 H=[];mesh={}
 def descend(hist,S,l,r):
  H.append((hist,S,l,r));mesh[l]=min(S);mesh[r]=min(S)
  if len(S)==1:return
  den=3*len(S)+1
  for j,i in enumerate(sorted(S)):
   left=l+(r-l)*F(3*j+1,den);right=l+(r-l)*F(3*j+2,den)
   ck(l<left<right<r,'proper_history_child')
   descend(hist+(i,),S-{i},left,right)
 descend((),frozenset(range(n)),F(0),F(1));totalhist+=len(H)
 ck(len(mesh)==2*len(H),'mesh_endpoint_distinctness')
 xs=sorted(mesh)
 for h,S,l,r in H:
  i=bisect_left(xs,l);j=bisect_left(xs,r)
  ck(set(h).isdisjoint(S) and set(h)|set(S)==set(range(n)),'history_partition')
  for k in range(i,j+1):ck(mesh[xs[k]] in S,'endpoint_decoder_soundness')
  for k in range(i,j):
   # Each open segment has exactly the endpoint support; verify nontrivial weights too.
   a,b=xs[k:k+2]
   for theta in (F(1,7),F(1,2),F(6,7)):
    x=a+(b-a)*theta;weights={}
    for label,w in [(mesh[a],1-theta),(mesh[b],theta)]:weights[label]=weights.get(label,0)+w
    ck(sum(weights.values())==1 and all(v>0 for v in weights.values()),'simplex_partition')
    ck(all(label in S for label in weights),'interior_decoder_soundness')
    ck(l<x<r,'mesh_interval_containment')
 if n>=3:
  nodes={h:(l,r) for h,S,l,r in H};p=nodes[(0,1)];q=nodes[(1,0)]
  ck(p[1]<q[0] or q[1]<p[0],'same_set_different_history')
# Independent rational K4 cell incidence and decoder, dense edge samples.
V=[(F(1,8),F(1,8)),(F(7,8),F(1,8)),(F(1,2),F(7,8)),(F(1,2),F(3,8))]
E=list(combinations(range(4),2))
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def on(p,a,b):return cross(a,b,p)==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])
for e in E:
 for f in E:
  if set(e)&set(f):continue
  a,b=[V[i] for i in e];c,d=[V[i] for i in f]
  ck(not (cross(a,b,c)*cross(a,b,d)<=0 and cross(c,d,a)*cross(c,d,b)<=0),'independent_K4_disjoint')
for mask in range(1,16):
 S={i for i in range(4) if mask>>i&1};P={V[i] for i in S}
 for i,j in E:
  if i in S and j in S:
   for t in [F(k,31) for k in range(32)]:P.add(tuple((1-t)*a+t*b for a,b in zip(V[i],V[j])))
 for p in P:
  allowed=[]
  for i in range(4):
   bad=any(p==V[j] for j in range(4) if j!=i) or any(on(p,V[j],V[k]) for j,k in E if i not in (j,k))
   if not bad:allowed.append(i)
  ck(bool(allowed) and set(allowed)<=S,'K4_decoder_all_possible_answers')
# Curved arc, arbitrary initial plateaus, first-exit squared Euclidean radius.
for end in [F(i,10) for i in range(1,11)]:
 for u in [end*F(i,11) for i in range(1,11)]:
  radius2=u*u+u**4
  for plateau in [F(0),F(1,3),F(2,3)]:
   exit_time=plateau+(1-plateau)*u/end
   ck(plateau<exit_time<1,'initial_plateau_first_exit')
   for j in range(17):
    time=exit_time*F(j,17);t=F(0) if time<=plateau else end*(time-plateau)/(1-plateau)
    ck(t*t+t**4<radius2,'earlier_curved_path_inside')
   q=u/2;ck(0<q<u and (q,q*q)!=(q,0),'rational_nonchord_subarc_witness')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'histories_through_n7':totalhist,'scope':'Finite exact audits only; name-continuity, nonuniform point existence and Baire arguments require the separate mathematical review.'},indent=2,sort_keys=True))
