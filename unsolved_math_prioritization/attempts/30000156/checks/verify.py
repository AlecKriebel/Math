"""Exact finite controls for the birational cycle-distribution counterexample.
No finite experiment proves the asymptotic or infinitude claims.
"""
from fractions import Fraction as F
from math import gcd
from collections import Counter
import json
import sympy as s
C=Counter()
def ck(b,k):
 assert b,k
 C[k]+=1
def prime(n):return n>=2 and all(n%d for d in range(2,int(n**.5)+1))
def factors(n):return [q for q in range(2,n+1) if prime(q) and n%q==0]
def phi(n):return sum(gcd(i,n)==1 for i in range(1,n+1))
def mu(n):
 f=factors(n)
 return 0 if any(n%(q*q)==0 for q in f) else (-1)**len(f)
def order(a,p):
 b=1
 for k in range(1,p):
  b=b*a%p
  if b==1:return k
 raise AssertionError('nonunit')
def ram(d,k):return sum(mu(d//h)*h for h in range(1,d+1) if d%h==0 and k%h==0)
# Direct whole-plane permutation and cycle decomposition, separately from divisor formula.
records=[]
for p in [q for q in range(3,100) if prime(q) and q%4==3]:
 N=p-1;theta=F(phi(N),N);W=2**len(factors(N))
 c=lambda z:(z[0],(z[0]*z[0]+1)*z[1]%p)
 ci=lambda z:(z[0],pow((z[0]*z[0]+1)%p,-1,p)*z[1]%p)
 pts={(u,v) for u in range(p) for v in range(p)}
 ck({c(z) for z in pts}==pts,'whole_plane_permutation')
 for z in pts:ck(ci(c(z))==z and c(ci(z))==z,'two_sided_inverse')
 periods={};remaining=set(pts)
 while remaining:
  start=min(remaining);seen=[];z=start
  while z not in seen:
   ck(z in remaining,'no_tail_or_overlap')
   seen.append(z);z=c(z)
  ck(z==start,'actual_cycle_closes_at_start')
  for z in seen:periods[z]=len(seen);remaining.remove(z)
 P=sum(order((u*u+1)%p,p)==N for u in range(p))
 for z,T in periods.items():ck(T==(1 if z[1]==0 else order((z[0]*z[0]+1)%p,p)),'period_formula')
 for x in (F(1,2),F(3,5),F(3,4),F(9,10)):
  if N>p*x:
   exact=F(sum(T<=p*x for T in periods.values()),p*p)
   ck(exact==1-F((p-1)*P,p*p),'point_weighted_cdf')
 ck((F(P,p)-theta)**2<=theta**2*(W-1)**2/F(p),'character_bound_squared')
 # Exact Ramanujan-sum primitive indicator for every group exponent.
 for k in range(N):
  v=theta*sum(F(mu(d)*ram(d,k),phi(d)) for d in range(1,N+1) if N%d==0)
  ck(v==int(gcd(k,N)==1),'primitive_indicator')
 records.append({'p':p,'primitive_multiplier_count':P,'theta':str(theta),'D_at_three_quarters':str(F(sum(4*T<=3*p for T in periods.values()),p*p))})
# Cyclotomic-ring verification of all character sums, not floating-point magnitudes.
z=s.Symbol('z')
for p in (3,7,11,19,23,31,43):
 N=p-1;g=next(a for a in range(1,p) if order(a,p)==N);logs={pow(g,k,p):k for k in range(N)}
 modulus=s.Poly(s.cyclotomic_poly(N,z),z,domain=s.ZZ)
 def red(co):return s.rem(s.Poly.from_dict({(i,):a for i,a in enumerate(co) if a},z,domain=s.ZZ),modulus).as_expr()
 for k in range(1,N):
  S=[0]*N;J=[0]*N
  for u in range(p):S[k*logs[(u*u+1)%p]%N]+=1
  for t in range(1,p):
   if t==1:continue
   J[((N//2)*logs[t]+k*logs[(1-t)%p])%N]+=1
  ck(red([a+b for a,b in zip(S,J)])==0,'quadratic_to_jacobi_identity') # eta(-1)=-1
  norm=[0]*N
  for a,x in enumerate(S):
   for b,y in enumerate(S):norm[(a-b)%N]+=x*y
  target=1 if k==N//2 else p
  norm[0]-=target
  ck(red(norm)==0,'exact_character_norm')
# Uniform elementary growth/mean inequalities used in the asymptotic proof.
for n in range(1,400):
 ck(2*phi(n)**2>=n,'totient_sqrt_bound')
 ck((2**len(factors(n)))**4<=64**4*n,'omega_bound_fourth_power')
ck(F(1,2)*(1-(F(1,2)-F(1,12)))==F(7,24),'Artin_product_lower_bound')
ck(F(1,4)+F(1,48)==F(13,48)<F(7,24),'separated_class_average_contradiction')
# CRT residue and an actual prime witness for several initial odd primorials.
Q=1
for q in (3,5,7,11):
 Q*=q;r=next(t for t in range(1,4*Q,2) if t%4==3 and t%Q==1)
 ck(gcd(r,4*Q)==1,'CRT_reduced_residue')
 p=next(r+4*Q*j for j in range(1000) if prime(r+4*Q*j))
 upper=F(1,2)
 for ell in factors(Q):upper*=F(ell-1,ell)
 ck(F(phi(p-1),p-1)<=upper,'CRT_totient_upper_bound')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'sample_records':records,'scope':'Exact finite controls only; unconditional prime asymptotics, Dirichlet infinitude and the written proof establish nonconvergence.'},indent=2,sort_keys=True))
