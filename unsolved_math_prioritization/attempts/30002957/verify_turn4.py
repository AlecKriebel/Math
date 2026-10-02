#!/usr/bin/env python3
"""Exact octahedral geometry and additive planar-deficit controls."""
from fractions import Fraction as F
from itertools import combinations,product
import json
checks=0

def ok(x):
 global checks
 assert x
 checks+=1

def norm(p):return sum(x*x for x in p)
def sub(p,q):return tuple(a-b for a,b in zip(p,q))
def det(a,b,c):
 u=sub(b,a);v=sub(c,a);return u[0]*v[1]-u[1]*v[0]
def circum(a,b,c):
 u=sub(b,a);v=sub(c,a);x=(norm(b)-norm(a))/2;y=(norm(c)-norm(a))/2;de=u[0]*v[1]-u[1]*v[0]
 return ((x*v[1]-y*u[1])/de,(u[0]*y-v[0]*x)/de)
P=[tuple(map(F,p)) for p in [(0,4),(-4,-2),(4,-2),(0,-1),(1,F(1,2)),(-1,F(1,2))]]
faces=[(0,1,5),(0,2,4),(0,4,5),(1,2,3),(1,3,5),(2,3,4),(3,4,5)]
centers=[(F(-205,32),F(63,16)),(F(205,32),F(63,16)),(0,F(59,28)),(0,F(-19,2)),(F(-115,56),F(-9,7)),(F(115,56),F(-9,7)),(0,F(1,12))]
radii=[F(42029,1024),F(42029,1024),F(2809,784),F(289,4),F(13481,3136),F(13481,3136),F(169,144)]
E=set()
for t,c,r2 in zip(faces,centers,radii):
 ok(circum(*(P[i] for i in t))==c);ok(norm(sub(P[t[0]],c))==r2)
 ok(abs(det(*(P[i] for i in t)))>=3)
 for i in set(range(6))-set(t):ok(norm(sub(P[i],c))-r2>=F(85,14))
 E.update(combinations(sorted(t),2))
ok(E==set(combinations(range(6),2))-{(0,3),(1,4),(2,5)})
tri=[t for t in combinations(range(6),3) if all(e in E for e in combinations(t,2))]
ok(len(tri)==8);ok(sum(any(v>=3 for v in t) for t in tri)==7)
for i,j in [(0,1),(1,2),(2,0)]:
 for z in P[3:]:ok(det(P[i],P[j],z)>=8)
h=F(1,10000)
ok(F(16,3)/(1-F(16,3)*4*h)<=6);ok(11065*h<F(85,14));ok(64*h+8*h*h<1);ok(27*27*2<50*50)
for signs in product((-1,1),repeat=12):
 Q=[tuple(P[i][r]+h*signs[2*i+r] for r in range(2)) for i in range(6)]
 for t,c in zip(faces,centers):
  cc=circum(*(Q[i] for i in t));rr=norm(sub(Q[t[0]],cc))
  ok(max(abs(a-b) for a,b in zip(c,cc))<=342*h)
  for i in set(range(6))-set(t):ok(norm(sub(Q[i],cc))>rr)
 for i,j in [(0,1),(1,2),(2,0)]:
  for z in Q[3:]:ok(det(Q[i],Q[j],z)>0)
# Start with K4 and insert octahedral or stacked disks into a current face.
E=set(combinations(range(4),2));FACES=list(combinations(range(4),3));n=4;patches=0
for step in range(28):
 a,b,c=FACES.pop((step*17)%len(FACES))
 if step%3:
  x,y,z=n,n+1,n+2;n+=3;patches+=1
  local=[(a,b,z),(a,c,y),(a,y,z),(b,c,x),(b,x,z),(c,x,y),(x,y,z)]
 else:
  x=n;n+=1;local=[(a,b,x),(a,c,x),(b,c,x)]
 FACES.extend(local)
 for t in local:E.update(combinations(sorted(t),2))
 count=sum(all(e in E for e in combinations(t,2)) for t in combinations(range(n),3))
 ok(count==3*n-8-2*patches);ok(len(FACES)==2*n-4)
print(json.dumps(dict(status='PASS',assertions=checks,all_cube_corners=4096,planar_insertions=28,scope='exact finite supplements to the analytic uniform-neighborhood and positive-density argument'),sort_keys=True,indent=2))
