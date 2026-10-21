from fractions import Fraction as Q
from itertools import product
import random,json
def F(x,arcs):
 y=[0]*len(x)
 for u,v,w in arcs:y[v]=max(y[v],w-x[u])
 return tuple(y)

def phi(x):
 q=x//2;r=x-2*q
 return min(r,2-r)
def forbidden(a,b):
 a,b=sorted((a,b)); vals=[phi(a),phi(b)]
 for z in range(a.numerator//a.denominator-1,b.numerator//b.denominator+2):
  if a<=z<=b:vals.append(phi(Q(z)))
 return min(vals),max(vals)
def rounded(x,t):
 k=x//2;s=x-2*k
 if s<=t:return 2*k
 if s>=2-t:return 2*k+2
 return 2*k+1
random.seed(3000062)
count=0
for _ in range(30000):
 n=random.randrange(1,7)
 A=[(u,v,2*random.randrange(5)) for u in range(n) for v in range(n) if random.random()<.3]
 x=tuple(Q(random.randrange(65),8) for _ in range(n));y=F(x,A)
 if max(abs(a-b) for a,b in zip(x,y))>=Q(1,n):continue
 intervals=[forbidden(a,b) for a,b in zip(x,y)]
 endpoints=sorted(set([Q(0),Q(1)]+[z for interval in intervals for z in interval]))
 t=next((a+b)/2 for a,b in zip(endpoints,endpoints[1:]) if a<b and not any(c<=(a+b)/2<=d for c,d in intervals))
 z=tuple(rounded(a,t) for a in x)
 assert F(z,A)==z
 count+=1
# Fixed nearest rounding fails for small residual; adjustable rounding succeeds.
eta=Q(1,1000);x=(Q(1,2)+eta,Q(3,2)+eta);A=[(0,1,2),(1,0,2)]
assert max(abs(a-b) for a,b in zip(x,F(x,A)))==2*eta
assert F(tuple(round(a) for a in x),A)!=tuple(round(a) for a in x)
print(json.dumps({'random_trials':30000,'approximate_fixed_points_rounded':count,'small_residual_fixed_rounding_failure_verified':True},indent=2))
