from fractions import Fraction as Q
from itertools import product
import json
checks=0
def ck(v):
 global checks;checks+=1;assert v
rows=[]
for n in range(2,13):
 for sign in [-1,1]:
  c=[Q(0)]*n;c[0]=Q(sign,2);c[-1]=-c[0];points=set()
  for signs in product([-1,1],repeat=n-1):
   x=c.copy()
   for i,s in enumerate(signs):x[i]+=Q(s,2);x[i+1]-=Q(s,2)
   ck(all(t.denominator==1 and -1<=t<=1 for t in x));points.add(tuple(x))
  ck(len(points)==2**(n-1));ck((Q(0),)*n in points)
  alpha=-c[0];z=c.copy()
  for i in range(n-1):z[i]+=alpha;z[i+1]-=alpha
  ck(z==[0]*n);ck(alpha in [-Q(1,2),Q(1,2)])
 if n>=3:
  points=set()
  for signs in product([-1,1],repeat=n):
   x=[0]*n
   for i,s in enumerate(signs):x[i]+=Q(s,2);x[(i+1)%n]-=Q(s,2)
   ck(all(t.denominator==1 and -1<=t<=1 for t in x));points.add(tuple(x))
  for x in points:ck(tuple(-v for v in x) in points)
  ck(len(points)==2**n-1) # two cyclic corner assignments both map to zero
  rows.append({'cycle_size':n,'endpoint_images':len(points)})
for sign in [-1,1]:
 x=[sign,-sign];ck(sum(x)==0 and all(abs(t)<=1 for t in x))
print(json.dumps({'assertions':checks,'cycle_controls':rows,'scope':'Finite controls; all-dimensional root-zonotope theorem is proved in TURN_2.md.'},indent=2))
