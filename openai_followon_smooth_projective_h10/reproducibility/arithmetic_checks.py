"""Exact finite checks for family004; these do not certify global theorems."""
from math import gcd,isqrt
import json
def m(x,y):return x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def p(x,n):
 a=(1,0)
 for _ in range(n):a=m(a,x)
 return a
def neg(x):return -x[0],-x[1]
def add(x,y):return x[0]+y[0],x[1]+y[1]
def prime(n):return n>1 and all(n%j for j in range(2,isqrt(n)+1))
def order(q,d):
 s={j*j%q for j in range(1,q)}
 return 1+sum(1 if (r:=(x*x*x-d*d*x)%q)==0 else 2*(r in s) for x in range(q))
d,dc,w=(75,-53),(75,53),(-5,4)
assert m(d,dc)==(7,0) and m(d,p((1,1),3))==w
assert add(p(w,3),neg(w))==m((-8,0),d)
x=neg(m(d,w));y=m((0,2),p(d,2))
assert p(y,2)==add(p(x,3),neg(m(p(d,2),x)))
assert 75**2>2*53**2 and x[0]**2<2*x[1]**2
assert 3 not in {j*j%7 for j in range(7)}
out=[]
for q in range(11,5000):
 if q%8!=1 or q%7!=3 or not prime(q):continue
 r=next(j for j in range(q) if j*j%q==2)
 ns=[order(q,(75-53*r)%q),order(q,(75+53*r)%q)]
 assert sum(ns)==2*(q+1) and all(n%4==0 and n%q for n in ns)
 g=gcd(*ns);assert g%4==0 and (g//4)%2==1
 a=abs(ns[0]-q-1)//2;b=isqrt(q-a*a)
 assert a and b*b==q-a*a
 for l in range(3,g+1,2):
  if g%l==0 and prime(l):assert a%l==0 and (b*b+1)%l==0 and l%4==1
 out.append([q,*ns,g,a,b])
assert len(out)==26
print(json.dumps(dict(point_Q=[x,y],selected_prime_count=len(out),bad_order_samples=[s for s in out if s[3]>4],all_checks_passed=True),sort_keys=True))
