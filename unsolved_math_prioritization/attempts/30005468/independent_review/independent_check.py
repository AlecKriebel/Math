#!/usr/bin/env python3
"""Independent symbolic and finite controls for the fixed-p certificate audit.
No finite search is used to assert the all-degree impossibility theorem.
"""
import json
from itertools import combinations, permutations, product
import sympy as s
n=0
def ck(v):
 global n
 assert v
 n+=1
x,y,z,t,b=s.symbols('x y z t b')
f=x**4+x*y**3+y**4-3*x*x*y*z-4*x*y*y*z+2*x*x*z*z+x*z**3+y*z**3+z**4
h=t**4-t+1
ck(s.expand(s.resultant(h,x+t*y+t*t*z,t)-f)==0)
ck(s.Poly(h,t,modulus=2).is_irreducible)
fac=s.factor_list(h,modulus=3)[1]
ck(sorted((s.degree(a,t),e) for a,e in fac)==[(1,1),(3,1)])
ck(s.gcd(h,s.diff(h,t),modulus=2)==1)
ck(s.gcd(h,s.diff(h,t),modulus=3)==1)
# Independent exact real-root count: all roots of h are nonreal.
ck(s.Poly(h,t).count_roots(-s.oo,s.oo)==0)
ck(s.Poly(b**3-4*b-1,b).count_roots(-2,-1)==1)
# Norm-positive SOS identity with denominator clearing and polynomial remainder.
U=2*x*x+b*y*y-y*z+(2+1/b)*z*z
V=2*x*y-y*y/b+2*x*z/b+b*y*z-z*z
num=s.cancel(b*b*(U*U-b*V*V-4*f))
ck(s.rem(num,b**3-4*b-1,b)==0)
# S4 acts transitively on unordered pairs; independently check the orbit.
pair=(0,1)
ck(len({tuple(sorted((q[pair[0]],q[pair[1]]))) for q in permutations(range(4))})==6)
# The vanishing constraints at all six pair intersections annihilate quadratics.
# This finite test supplements the general line-restriction proof.
for roots in combinations(range(-4,5),4):
 rows=[]
 for aa,bb in combinations(roots,2):
  pt=(aa*bb,-aa-bb,1)
  ck(pt[0]+aa*pt[1]+aa*aa*pt[2]==0)
  ck(pt[0]+bb*pt[1]+bb*bb*pt[2]==0)
  rows.append([pt[0]**2,pt[0]*pt[1],pt[0]*pt[2],pt[1]**2,pt[1]*pt[2],pt[2]**2])
 ck(s.Matrix(rows).rank()==6)
 for aa,bb,cc in combinations(roots,3):
  ck(s.Matrix([[1,aa,aa*aa],[1,bb,bb*bb],[1,cc,cc*cc]]).det()!=0)
# Total-degree truncated moment indexing and full moment matrix obstruction.
mon=[(i,j,k) for i in range(5) for j in range(5) for k in range(5) if i+j+k<=4]
ck(len(mon)==35)
def moment(v):return int(v==(0,0,0))-int(v==(4,0,0))
P=s.Poly(1+f,x,y,z)
ck(sum(c*moment(a) for a,c in P.terms())==0)
ck(moment((0,0,0))==1)
ck(moment((4,0,0))==-1)
mon2=[v for v in mon if sum(v)<=2]
M=s.Matrix([[moment(tuple(a+b for a,b in zip(v,w))) for w in mon2] for v in mon2])
ck(M[mon2.index((2,0,0)),mon2.index((2,0,0))]==-1)
ck(sum(c*moment(a) for a,c in s.Poly(1+x**4,x,y,z).terms())==0)
# All-degree jet bookkeeping is a degree argument. Exhaustive finite exponent
# pairs through degree 8 illustrate the exact degree-four possibilities.
mons=[v for v in product(range(9),repeat=3) if 2<=sum(v)<=8]
jet_pairs=0
for aa in mons:
 for bb in mons:
  d=sum(aa)+sum(bb)
  if d==4:ck(sum(aa)==sum(bb)==2);jet_pairs+=1
  if d+2<=4:raise AssertionError('ball multiplier could enter the fourth jet')
ck(jet_pairs==36)
# Construct full rational polynomials with arbitrary higher tails and compare
# every degree-four coefficient, including cross terms and the ball weight.
g=1-x*x-y*y-z*z
for j in range(1,41):
 a2=(j*x*x+(j-2)*x*y-y*y+s.Rational(1,j)*y*z+z*z)
 b2=(x*x-j*x*z+(j+1)*y*y-z*z)
 aa=a2+(j+2)*x**3-y*z**4+x**8
 bb=b2-x*y*z+(j-3)*z**6-y**7
 expr=s.Poly(s.expand(aa**2+g*bb**2),x,y,z)
 lead=sum(c*x**a[0]*y**a[1]*z**a[2] for a,c in expr.terms() if sum(a)==4)
 ck(s.expand(lead-a2*a2-b2*b2)==0)
 ck(all(sum(a)>=4 for a,c in expr.terms()))
# Exact original normalization example and strict-margin scaling controls.
ck(32+s.Rational(8,9)*(32-34-34)==0)
for c in [s.Rational(j,k) for k in range(1,8) for j in range(k+1,k+6)]:
 cp=s.Poly(c*(1+f),x,y,z)
 ck(sum(a*moment(m) for m,a in cp.terms())==0)
 ck(c-1>0)
print(json.dumps({'status':'PASS','exact_assertions':n,'quadratic_intersection_configurations':126,'moment_entries':35,'jet_pairs_of_quadratic_monomials':jet_pairs,'scope':'Independent exact controls supplement the source/Galois/all-degree-jet proof. No finite test proves universal absence of rational certificates.'},sort_keys=True,indent=2))
