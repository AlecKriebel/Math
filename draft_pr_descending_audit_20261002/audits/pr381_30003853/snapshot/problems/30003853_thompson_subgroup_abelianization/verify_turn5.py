#!/usr/bin/env python3
import itertools,json,random
from verify_turn4 import bump,comp,inv,power,slope,Q
checks=0
def ck(x):
 global checks
 assert x;checks+=1
rng=random.Random(5278)
pts=list(itertools.product(range(-2,3),repeat=3));e=(0,0,0)
for m in range(1,13):
 def mul(u,v):a,b,c=u;d,f,g=v;return a+d,b+f,c+g+m*a*f
 def inverse(u):a,b,c=u;return -a,-b,-c+m*a*b
 def pw(u,n):a,b,c=u;return n*a,n*b,n*c+m*n*(n-1)*a*b//2
 def pos(u):return u>e
 x=(1,0,0);y=(0,1,0);z=(0,0,1)
 ck(mul(mul(mul(x,y),inverse(x)),inverse(y))==(0,0,m))
 for u in pts:
  ck(mul(u,inverse(u))==e)
  ck(mul(inverse(u),u)==e)
  a,b,c=u
  ck(mul(mul(pw(x,a),pw(y,b)),pw(z,c-m*a*b))==u)
  for n in range(1,6):
   w=e
   for _ in range(n):w=mul(w,u)
   ck(w==pw(u,n));ck((w==e)==(u==e))
  for v in pts:
   a,b,c=u;d,f,g=v
   comm=mul(mul(mul(u,v),inverse(u)),inverse(v))
   ck(comm==(0,0,m*(a*f-d*b)))
   con=mul(mul(inverse(v),u),v)
   ck(pos(con)==pos(u))
   if pos(u) and pos(v):ck(pos(mul(u,v)))
 for n in range(1,6):ck(len({pw(u,n) for u in pts})==len(pts))
 for _ in range(500):
  u,v,w=[rng.choice(pts) for _ in range(3)]
  ck(mul(mul(u,v),w)==mul(u,mul(v,w)))
 for p in (2,3,5,7,11):
  cnt=sum((m*c)%p==0 for a,b,c in itertools.product(range(p),repeat=3))
  ck(cnt==p**(3 if m%p==0 else 2))
f=bump(0,1);g=bump(Q(1,4),Q(3,4))
for n in range(-8,9):
 h=power(f,n)
 ck(slope(h)==slope(f)**n)
 ck(slope(h,False)==slope(f,False)**n)
 for k in range(-5,6):
  s=power(g,k);c=comp(comp(inv(s),h),s)
  ck(slope(c)==slope(h));ck(slope(c,False)==slope(h,False))
print(json.dumps({'turn':5,'assertions':checks,'parameters':list(range(1,13)),'integer_triples':len(pts),'prime_controls':[2,3,5,7,11],'scope':'exact bounded controls for formulas and failed proxy route, no F embedding claimed'},sort_keys=True,indent=2))
