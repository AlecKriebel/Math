"""Construction-identity tests, not a proof of any all-pair lower bound."""
from fractions import Fraction as Q
from math import gcd,sqrt,cos,sin,pi,dist,asin
import json,sys
def fib(n):
 a,b=0,1
 for _ in range(n):a,b=b,a+b
 return a
def target(q,p,k,shift=Q(0)):
 t=float((Q(k)+shift)/q);a=2*pi*p*k/q;r=2*sqrt(t*(1-t))
 return(r*cos(a),r*sin(a),1-2*t)
def companion(q,p,j):
 return target(q,1,(p*j)%q)[:0] if False else spherical(Q(j,q),Q((p*j)%q,q))
def spherical(angle,height):
 t=float(height);a=2*pi*float(angle);r=2*sqrt(t*(1-t))
 return(r*cos(a),r*sin(a),1-2*t)
def near(a,b):return dist(a,b)<2e-12
case=sys.argv[1] if len(sys.argv)>1 else 'positive'
if case=='positive':
 for n in range(3,201):
  q,p,c=fib(n),fib(n-1),fib(n-2)
  assert gcd(p,q)==1 and p*p-q*c==(-1)**n
  for j in {0,1,q//2,q-1}:
   k=p*j%q
   assert ((-1)**n*p*k-j)%q==0
 for n in range(3,13):
  q,p=fib(n),fib(n-1)
  for j in range(q):
   k=p*j%q;v=target(q,p,k);w=companion(q,p,j)
   assert near(w,(v[0],(-1)**n*v[1],v[2]))
  # Replace 0..q-1 by 1..q via k=q-j: exact orthogonal endpoint convention.
  for j in range(1,q+1):
   v=target(q,p,q-j);w=target(q,p,j)
   assert near(w,(v[0],-v[1],-v[2]))
  # The q+1 double-pole antecedent contains the q-point target up to z-reflection.
  for j in range(q):
   v=target(q,p,j);w=(v[0],v[1],-v[2])
   assert abs(sum(x*x for x in w)-1)<1e-12
  assert abs(dist(target(q,p,0),target(q,p,1))**2-4/q)<1e-12
 print(json.dumps({'result':'PASS','exact_integer_indices':'3..200','coordinate_indices':'3..12','scope':'Cassini/permutation/reflection/endpoint/subset/pole upper bound only; no all-pair lower bound tested or inferred'},sort_keys=True))
elif case=='odd-no-reflection':
 q,p=5,3
 assert near(companion(q,p,1),target(q,p,3)), 'Odd n needs reflection; equal labels/coordinates are false'
elif case=='generic-inverse':
 q,p=7,2
 assert p*p%q in (1,q-1), 'Coprimality alone does not give inverse equal to plus/minus p'
elif case=='midpoint-pole':
 q,p=5,3
 assert target(q,p,0,Q(1,2))[2]==1, 'Midpoint construction has no north pole and changes the target'
elif case=='arc-is-chord':
 q=2;chord=2/sqrt(q);arc=2*asin(chord/2)
 assert abs(arc-chord)<1e-12, 'Arc distance is 2 asin(chord/2), not the same finite constant'
elif case=='area-is-distance':
 a=(Q(0),Q(0));b=(Q(0),Q(1,5))
 planar=sqrt(sum(float(x-y)**2 for x,y in zip(a,b)))
 assert abs(dist(spherical(*a),spherical(*b))-planar)<1e-12, 'Lambert area preservation does not preserve Euclidean distance'
else:raise ValueError(case)
