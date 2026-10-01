"""Exact coefficient controls for the Ohtsuki/Ito scoped obstruction."""
import sympy as s,json
from collections import Counter,deque
from math import gcd,isqrt
from fractions import Fraction as Q
C=Counter()
def ck(v,k):
 assert v,k
 C[k]+=1
n,m,k,f,q,vx,vy,vz,v3=s.symbols('n m k f q vx vy vz v3')
d=n*m-k*(k+1)
A=(n+m)*(d-n*m/2)-k*(k+s.Rational(1,2))*(k+1)+12*v3
B=m*vx+n*vy-(k+s.Rational(1,2))*vz-3*v3
Theta=A*(-2-(2*d+1)*q/3)-4*B*(1+d*q)
base=s.expand(Theta.subs(m,0));D=-k*(k+1)
expected=f*(D*(-2-(2*D+1)*q/3)-4*vy*(1+D*q))
ck(s.expand(base.subs(n,n+f)-base-expected)==0,'full_primary_formula_finite_difference')
const=s.expand(expected/f).coeff(q,0);coef=s.expand(expected/f).coeff(q,1)
ck(s.expand(coef-D*const-D*(4*D-1)/3)==0,'unknown_tangle_coefficient_eliminates')
ck(s.expand((1-4*D)*expected.subs(q,0)-expected.subs(q,-4)-4*f*D*(4*D-1)/3)==0,'evaluation_invariant_difference')
for det in range(-100,101):
 for v in range(-15,16):
  c=-2*det-4*v;e=-Q(det*(2*det+1),3)-4*det*v
  ck(e-det*c==Q(det*(4*det-1),3),'rational_elimination_controls')
  if det:ck(c!=0 or e!=0,'nonzero_d_polynomial_not_zero')
for det,change,value in [(-42,11,104104),(-342,2,1248528)]:ck(abs(Q(4*change*det*(4*det-1),3))==value,'specific_gap_invariant_difference')
def ds(x):return {d for a in range(1,isqrt(x)+1)if x%a==0 for d in(a,x//a)}
for N in range(3,152,2):
 K=N//2;det=-K*(K+1);T={4*b*b*h*h%N for b in ds(K)for h in ds(K+1)}
 H={1};todo=deque([1])
 while todo:
  h=todo.popleft()
  for t in T:
   z=h*t%N
   if z not in H:H.add(z);todo.append(z)
 for a in range(1,N):
  if gcd(a,N)>1:continue
  for h in H:
   b=a*h%N
   ck((a-b)*det%6==0,'S_orbit_primary_coefficient_divisibility')
   w=(a-b)*det//6;u=3*w*pow(2*b,-1,N)%N;z=(2*b*u-3*w)//N
   ck(2*b*u-N*z==3*w,'Bezout_matching_second_coefficient')
   ck(b*det+6*w==a*det,'first_coefficient_matches')
   ck(gcd(2*b,N)==1,'primitive_Bezout_hypothesis')
for N,a,b,u,z,w in [(13,1,12,8,-3,77),(37,1,3,20,-6,114)]:
 K=N//2;det=-K*(K+1);ck(w==Q((a-b)*det,6),'reported_w')
 ck(2*b*u-N*z-3*w==0,'reported_second_coefficient')
 ck(b*det+6*w==a*det,'reported_first_coefficient')
ck(Q(77,2).denominator==2,'do_not_discard_half_integral_v3')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'scope':'Symbolic finite difference and exact formal coefficient compatibility. Does not construct tangles or prove knot equivalence; source topology/quantum invariant is an external input.'},indent=2,sort_keys=True))
