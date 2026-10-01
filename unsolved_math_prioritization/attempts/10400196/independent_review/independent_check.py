#!/usr/bin/env python3
"""Independent rational controls of the scoped Spin-c formulas, not topology proofs."""
from fractions import Fraction as F
from math import gcd
from itertools import product
import json
count=0

def check(x):
 global count
 assert x
 count+=1

def mod(x,m=1): return x % m

def eta(x):
 x=mod(x)
 check(x.denominator%2==1)
 return mod(F(2*((x.numerator*pow(2,-1,x.denominator))%x.denominator),x.denominator),2) if x.denominator>1 else F(0)

# All characteristic cyclic forms up to order 40, with the canonical odd-Chern origin.
examples=0
for n in range(1,41):
 for c in range(n%2,2*n,2):
  q=lambda j:mod(F(j*j-c*j,2*n))
  for j in range(n):check(q(j+n)==q(j))
  order=n//gcd(n,c)
  if order%2==0:continue
  odd=[a for a in range(n) if (n//gcd(n,a))%2 and (2*a-c)%n==0]
  check(len(odd)==1)
  t=odd[0];c0=(c-2*t)%(2*n);check(c0 in (0,n))
  q0=lambda j:mod(F(j*j-c0*j,2*n))
  a=(-t)%n;x=q0(a);e=eta(x)
  check(mod(e)==x)
  check(mod(x.denominator*e,2)==0)
  for j in range(n):
   check(q(j)==mod(q0(j+a)-x))
   check(q0(-j)==q0(j))
  for j in range(-3,4):check(q0(j*a)==mod(j*j*x))
  examples+=1
# eta is a homomorphism on a genuinely mixed family of odd denominators.
xs=[F(a,n) for n in (1,3,5,7,9,15) for a in range(n)]
for x in xs:
 for y in xs:check(mod(eta(x+y)-eta(x)-eta(y),2)==0)
# Four copies of the two order-two forms are isometric; lift sums cannot agree.
for bits in product((0,1),repeat=4):
 w=sum(bits);image=tuple((b+w)%2 for b in bits)
 check(mod(F(sum(image),4))==mod(F(-w,4)))
for e,f in product((0,1),repeat=2):check((4*(1+8*e)-4*(-1+8*f))%16==8)
# Characteristic representative cocycle, arbitrary signs and off-diagonal entries.
matrix_cases=0
for u,v,w in product(range(-3,4),repeat=3):
 det=u*w-v*v
 if not det:continue
 B=((u,v),(v,w))
 def dot(x,y):return sum(x[i]*y[i] for i in range(2))
 def mul(x):return (u*x[0]+v*x[1],v*x[0]+w*x[1])
 def Q(x):return dot(x,mul(x))
 def invq(c):return F(w*c[0]*c[0]-2*v*c[0]*c[1]+u*c[1]*c[1],det)
 for d in ((0,0),(1,-1)):
  c=(u+2*d[0],w+2*d[1])
  def rho(c,z):
   val=dot(c,z)+Q(z);check(val%2==0);return val//2
  for z in product((-1,0,1),repeat=2):
   bz=mul(z);cp=(c[0]+2*bz[0],c[1]+2*bz[1])
   check(-invq(cp)+invq(c)==-4*(dot(c,z)+Q(z)))
   for y in ((1,0),(0,-1),(1,1)):
    zp=(z[0]+y[0],z[1]+y[1])
    check(rho(c,zp)==rho(c,z)+rho(cp,y))
  matrix_cases+=1
# Stabilization and the specific spin-origin/signature-defect failures.
for sign in (-1,1):
 for k in range(-15,16,2):
  check((k*k-1)%8==0)
  check((sign*(1-k*k)+8*(sign*(k*k-1)//8))%16==0)
check((F(1)-F(10*10,4)-(F(1)-F(2*2,4)))%16==8)
check((F(1)-8*F(1,8))%16==0)
check((F(-3)-8*F(5,8))%16==8)
# Cohomological odd-half naturality under every cyclic unit isomorphism.
for n in range(1,33):
 for c in range(n):
  if (n//gcd(n,c))%2==0:continue
  a=next(a for a in range(n) if (2*a-c)%n==0 and (n//gcd(n,a))%2)
  for u in range(n):
   if gcd(u,n)==1:
    aa=(u*a)%n;cc=(u*c)%n
    check((2*aa-cc)%n==0 and (n//gcd(n,aa))%2==1)
# The Floer source calibration and the exact parity condition.
for d,chi,lam,R in [(F(-2),0,1,8),(F(0),-1,-1,8),(F(0),0,0,0)]:
 check(F(chi)-d/2==lam)
 check((8*lam)%16==R)
check((-4*F(-2))%16 != (-4*F(0))%16)
for delta_d_half in range(-10,11):
 for delta_chi in range(-10,11):
  defect=8*(delta_chi-delta_d_half)
  check((defect%16==0)==((delta_chi-delta_d_half)%2==0))
# I^2 does not force even coefficients in the cyclic order-four group ring.
a=(-1,1,0,0)
poly=tuple(sum(a[i]*a[(k-i)%4] for i in range(4)) for k in range(4))
check(poly==(1,-2,1,0));check(sum(poly)==0);check(any(c%2 for c in poly))
print(json.dumps({'status':'PASS','exact_assertions':count,'cyclic_odd_Chern_cases':examples,'matrix_characteristic_cases':matrix_cases,'scope':'Independent exact finite rational checks of odd-primary lifting, canonical spin-origin algebra, square completion, representative cocycles, stabilization and specified failures. No general topological theorem or Floer computation is inferred from enumeration.'},indent=2))
