from fractions import Fraction as F
from itertools import product
from math import prod,factorial
import json
checks=0
def ck(x):
 global checks
 checks+=1
 assert x
for r in range(1,4):
 pts=list(product([F(j,8) for j in range(-2,3)],repeat=r))
 for u in pts:
  for v in pts:
   a=1-sum(x*x for x in u);b=1-sum(x*x for x in v);D=sum((x-y)**2 for x,y in zip(u,v));R=(a+b-D/3)/2
   ck(a>=F(3,4) and b>=F(3,4))
   ck(R<=0 or a*b>=R*R)
for d in range(2,101):
 for m in range(0,31):
  odd=prod(range(1,2*m,2));den=prod(d+2*j for j in range(m));moment=F(d**m*odd,den)
  ck(moment<=odd)
ck(sum(F(3**j,factorial(j)) for j in range(5))>9)
ck(sum(F(3,4)**j/factorial(j) for j in range(3))>2)
for d in range(2,1001):
 for r in [1,max(1,d//512),max(1,d//512+1),d]:
  if r<=F(d,512):ck(F(32*r,d)<=F(1,16));ck(F(d,64*r)>=F(9*d,8192*r))
  else:ck(F(9,16)>=F(9*d,8192*r))
for n in range(1,1001):
 ck(F(3*n,8)-F(n,16)-F(n,16)==F(n,4));ck(F(n,256)/F(1,16)==F(n,16))
print(json.dumps({'assertions':checks,'lift_ranks':[1,3],'sphere_moment_dimensions':[2,100],'scope':'Exact rational constants and inequalities; probability and uniformity proved analytically'},indent=2,sort_keys=True))
