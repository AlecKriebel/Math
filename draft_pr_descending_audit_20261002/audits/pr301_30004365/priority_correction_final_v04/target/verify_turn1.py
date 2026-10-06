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
def surface(n,arrows,relations):
 arr=list(arrows); rel=set(relations); nxt=n
 # Choose finite 2x2 completion preserving the original pair table.
 for v in range(n):
  inc=[i for i,(s,t) in enumerate(arr) if t==v]
  out=[i for i,(s,t) in enumerate(arr) if s==v]
  oi,oo=set(inc),set(out)
  while len(inc)<2:inc.append(len(arr));arr.append((nxt,v));nxt+=1
  while len(out)<2:out.append(len(arr));arr.append((v,nxt));nxt+=1
  possibilities=[{(inc[0],out[j]),(inc[1],out[1-j])} for j in (0,1)]
  match=next(m for m in possibilities if all(((a,b) in m)==((a,b) in rel) for a in oi for b in oo))
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
 return {'genus':(2-b-chi)//2,'boundaries':b,'white_punctures':pw,'black_punctures':pb,'white_marks':len(whites&set(bd)),'black_marks':len(blacks&set(bd))}
checks=0
for n in range(1,9):
 for signs in product((0,1),repeat=n-1):
  arr=[(i,i+1) if s else(i+1,i) for i,s in enumerate(signs)]
  z=surface(n,arr,set());assert z==dict(genus=0,boundaries=1,white_punctures=0,black_punctures=0,white_marks=n+1,black_marks=n+1);checks+=1
for n in range(1,15):
 arr=[(i,(i+1)%n) for i in range(n)];rel={(i,(i+1)%n) for i in range(n)}
 z=surface(n,arr,rel);assert z==dict(genus=0,boundaries=1,white_punctures=0,black_punctures=1,white_marks=n,black_marks=n);checks+=1
# Rational intersection controls: no floating-point use.
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def transverse(a,b,c,d):
 u,v,w=sub(b,a),sub(d,c),sub(c,a);den=cross(u,v)
 if not den:return False
 t,s=F(cross(w,v),den),F(cross(w,u),den)
 return 0<t<1 and 0<s<1
for den in range(2,25):
 for i in range(1,den):
  t=F(i,den)
  assert transverse((0,t),(1,t),(t,0),(t,1))
  assert not transverse((0,0),(1,0),(t,0),(t,1));checks+=2
# Canonical handle tags: orientation reversal leaves gcd/Arf/parity data unchanged.
def tag(g,a,b,c):
 import math,functools
 if g==0:return()
 if g==1:return('gcd',functools.reduce(math.gcd,a+b+[x+2 for x in c],0))
 if any(x%2 for x in a+b+c):return('odd',)
 if any(x%4==0 for x in c):return('even_boundary_zero',)
 return('arf',sum((x//2+1)*(y//2+1) for x,y in zip(a,b))%2)
for g in (1,2,3):
 for a0,b0 in product(range(-6,7),repeat=2):
  a=[a0]*g;b=[b0]*g;c=[-2]
  assert tag(g,a,b,c)==tag(g,[-x for x in a],b,c);checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'scope':'Finite surface-gluing, rational-intersection and invariant-arithmetic controls. Not a full PL enumeration implementation or independent review.'},indent=2))
