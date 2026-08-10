#!/usr/bin/env python3
"""Dependency-free independent reconstruction of the finite atlas.

This implementation deliberately does not import the discovery/atlas modules.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import permutations
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
N=('0','A','B','C','2A','2B','2C','AB','AC','BC')
V=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(2,0,0),(0,2,0),(0,0,2),(1,1,0),(1,0,1),(0,1,1))
H=((1,1,0),(2,3,0),(1,2,0),(1,3,0))

def classify(mask,h,active=(0,1)):
 ys=[i for i in range(10) if mask>>i&1];val={i:sum(h[j]*V[i][j] for j in range(3)) for i in ys};mx=max(val.values());top={i for i in ys if val[i]==mx}
 if len(top)==len(ys):return ('inv','flat')
 if any(sum(V[y][j] for j in active)>=2 for y in top):return ('avail','two')
 K={j for y in top for j in active if V[y][j]}
 if all(sum(V[y][j] for j in K)==1 for y in ys):return ('inv','q1')
 if any(sum(V[y])==1 for y in top):return ('avail','unary')
 D={j for y in top for j in range(3) if j not in active and V[y][j]}
 if any(any(V[y][j] for j in D) for y in set(ys)-top):return ('avail','service')
 return ('inv','signed')

def rref(rows):
 A=[list(map(Fraction,r)) for r in rows if any(r)];m=len(A);rr=0
 for c in range(3):
  p=next((i for i in range(rr,m) if A[i][c]),None)
  if p is None:continue
  A[rr],A[p]=A[p],A[rr];z=A[rr][c];A[rr]=[x/z for x in A[rr]]
  for i in range(m):
   if i!=rr and A[i][c]:
    z=A[i][c];A[i]=[A[i][j]-z*A[rr][j] for j in range(3)]
  rr+=1
 return tuple(tuple(x for x in row) for row in A[:rr])
def rows(mask):
 ys=[i for i in range(10) if mask>>i&1];root=V[ys[0]]
 return tuple(tuple(V[y][j]-root[j] for j in range(3)) for y in ys[1:])
def invariant(m1,m2):
 R=rref(rows(m1)+rows(m2));r=len(R)
 if r==0:return True
 if r==3:return False
 if r==1:
  a,b,c=R[0]
  return bool(c or (a*b<0) or (not a and not b))
 u,v=R;n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
 return bool(n[0] and n[1] and n[0]*n[1]>0)
def pidx(i,p):
 q=[0,0,0]
 for j in range(3):q[p[j]]=V[i][j]
 return V.index(tuple(q))
def canon(m1,m2,h):
 out=[]
 for p in permutations(range(3)):
  hp=[0,0,0]
  for j in range(3):hp[p[j]]=h[j]
  ms=[]
  for m in (m1,m2):
   q=0
   for i in range(10):
    if m>>i&1:q|=1<<pidx(i,p)
   ms.append(q)
  out.append((tuple(sorted((p[0],p[1]))),tuple(hp),tuple(sorted(ms))))
 return min(out)
def deficiency(m1,m2):return m1.bit_count()+m2.bit_count()-2-len(rref(rows(m1)+rows(m2)))
def strong(nodes,edges):
 for root in nodes:
  seen={root};st=[root]
  while st:
   u=st.pop()
   for a,b in edges:
    if a==u and b not in seen:seen.add(b);st.append(b)
  if len(seen)!=len(nodes):return False
 return True
def support_count(nodes):
 E=tuple(permutations(nodes,2));n=0
 for mask in range(1<<len(E)):
  ed=tuple(E[i] for i in range(len(E)) if mask>>i&1)
  if strong(nodes,ed):n+=1
 return n

def verify():
 subs=[m for m in range(1,1<<10) if m.bit_count()>=2];out={};raw=0
 for h in H:
  C={m:classify(m,h) for m in subs};shield=[m for m in subs if C[m][0]=='inv']
  for i,m1 in enumerate(shield):
   for m2 in shield[i:]:
    if m1&m2:continue
    raw+=1
    if invariant(m1,m2):continue
    key=canon(m1,m2,h)
    out.setdefault(key,deficiency(key[2][0],key[2][1]))
 assert len(out)==29
 assert list(out.values()).count(0)==27 and list(out.values()).count(1)==2
 exc=[]
 for (active,h,masks),d in out.items():
  if d==1:exc.append(tuple(tuple(N[i] for i in range(10) if m>>i&1) for m in masks))
 assert sorted(exc)==[(('0','C','2C'),('A','2A','BC')),(('C','2C'),('0','A','2A','BC'))]
 entries=[{'active':list(a),'workload':list(h),'masks':list(ms),'deficiency':d} for (a,h,ms),d in sorted(out.items())]
 digest=hashlib.sha256(json.dumps(entries,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return {'status':'pass','assignment_universe':3**10,'workload_chambers':4,'raw_shielded_nonoverlap_pairs':raw,
         'canonical_noninvariant_classes':29,'deficiency_zero_classes':27,'service_exception_classes':2,
         'reduced_atlas_sha256':digest,
         'type_I_four_vertex_scc_supports':support_count(('0','A','2A','BC')),
         'three_vertex_scc_supports':support_count(('0','C','2C'))}

def main():
 out=verify();print(json.dumps(out,sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
