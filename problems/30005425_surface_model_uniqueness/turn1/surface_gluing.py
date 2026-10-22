# Credited PPP lozenge construction; reused from reviewed PR301 finite checker.
#!/usr/bin/env python3
"""Supplementary exact finite controls, not the full exhaustive PL algorithm."""
from itertools import product,combinations
from fractions import Fraction as F
import json, random
class DSU:
 def __init__(self,n):self.p=list(range(n))
 def get(self,a):
  while self.p[a]!=a:self.p[a]=self.p[self.p[a]];a=self.p[a]
  return a
 def join(self,a,b):self.p[self.get(a)]=self.get(b)
def surface(n,arrows,relations,completion_choices=None):
 arr=list(arrows); rel=set(relations); nxt=n
 # Choose finite 2x2 completion preserving the original pair table.
 for v in range(n):
  inc=[i for i,(s,t) in enumerate(arr) if t==v]
  out=[i for i,(s,t) in enumerate(arr) if s==v]
  oi,oo=set(inc),set(out)
  while len(inc)<2:inc.append(len(arr));arr.append((nxt,v));nxt+=1
  while len(out)<2:out.append(len(arr));arr.append((v,nxt));nxt+=1
  possibilities=[{(inc[0],out[j]),(inc[1],out[1-j])} for j in (0,1)]
  compatible=[m for m in possibilities if all(((a,b) in m)==((a,b) in rel) for a in oi for b in oo)]
  match=compatible[(completion_choices or {}).get(v,0)%len(compatible)]
  rel|=match
 A=len(arr);d=DSU(4*A);ed=DSU(4*A)
 # Corners s,v,t,f; sides s-v, v-t, t-f, f-s.
 used=set()
 for a,(s,t) in enumerate(arr):
  for b,(u,z) in enumerate(arr):
   if t!=u:continue
   if (a,b) in rel:
    ea,eb=4*a+2,4*b+3;d.join(4*a+2,4*b);d.join(4*a+3,4*b+3)
   else:
    ea,eb=4*a+1,4*b;d.join(4*a+2,4*b);d.join(4*a+1,4*b+1)
   assert ea not in used and eb not in used
   used|={ea,eb};ed.join(ea,eb)
 V=len({d.get(i) for i in range(4*A)});E=len({ed.get(i) for i in range(4*A)})
 bd={}
 for a in range(A):
  for k in range(4):
   if 4*a+k in used:continue
   x,y=d.get(4*a+k),d.get(4*a+(k+1)%4)
   bd.setdefault(x,[]).append(y);bd.setdefault(y,[]).append(x)
 assert all(len(z)==2 for z in bd.values())
 todo=set(bd);b=0
 while todo:
  b+=1;stack=[todo.pop()]
  while stack:
   for y in bd[stack.pop()]:
    if y in todo:todo.remove(y);stack.append(y)
 whites={d.get(4*a+1) for a in range(A)};blacks={d.get(4*a+3) for a in range(A)}
 pw=len(whites-set(bd));pb=len(blacks-set(bd));chi=V-E+A
 assert (2-b-chi)%2==0
 return {'cell_vertices':V,'cell_edges':E,'lozenges':A,'Euler_characteristic':chi,'genus':(2-b-chi)//2,'boundaries':b,'white_punctures':pw,'black_punctures':pb,'white_marks':len(whites&set(bd)),'black_marks':len(blacks&set(bd))}
