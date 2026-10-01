"""Independent exact orbit and cyclotomic controls; asymptotic claims require the proof."""
from fractions import Fraction as F
from math import gcd,isqrt
from itertools import product
from collections import Counter
import sympy as s
import json
C=Counter()
def ck(v,k):
 assert v,k
 C[k]+=1
def prime(n):return n>=2 and all(n%d for d in range(2,isqrt(n)+1))
def factors(n):
 out=[];d=2
 while d*d<=n:
  if n%d==0:
   out.append(d)
   while n%d==0:n//=d
  d+=1
 if n>1:out.append(n)
 return out
def phi(n):
 v=n
 for q in factors(n):v=v//q*(q-1)
 return v
def mu(n):
 f=factors(n)
 return 0 if any(n%(q*q)==0 for q in f) else (-1)**len(f)
def primitive(a,p):return all(pow(a,(p-1)//q,p)!=1 for q in factors(p-1))
samples=[]
for p in [p for p in range(3,200) if prime(p) and p%4==3]:
 nxt=[(i//p)*p+(((i//p)**2+1)*(i%p)%p) for i in range(p*p)]
 ck(len(set(nxt))==p*p,'array_permutation')
 periods=[0]*(p*p)
 for start in range(p*p):
  if periods[start]:continue
  v=start;cycle=[]
  while not cycle or v!=start:
   ck(not periods[v],'unvisited_cycle_point')
   cycle.append(v);v=nxt[v]
  for v in cycle:periods[v]=len(cycle)
 N=p-1;P=sum(primitive((u*u+1)%p,p) for u in range(p));theta=F(phi(N),N)
 for u in range(p):
  ck(periods[u*p]==1,'zero_section_fixed')
  ck(len({periods[u*p+v] for v in range(1,p)})==1,'nonzero_fiber_constant_period')
  ck((periods[u*p+1]==N)==primitive((u*u+1)%p,p),'full_length_fiber_test')
 for x in [F(1,2),F(2,3),F(3,4),F(4,5),F(99,100)]:
  if N>p*x:
   D=F(sum(F(T,p)<=x for T in periods),p*p)
   ck(D==1-F(N*P,p*p),'point_cdf_exact')
 W=2**len(factors(N))
 ck((F(P,p)-theta)**2*p<=theta**2*(W-1)**2,'uniform_character_estimate_squared')
 samples.append({'p':p,'P':P,'theta':str(theta),'D_three_quarters':str(F(sum(4*T<=3*p for T in periods),p*p))})
# Exact character checks use each character's own cyclotomic order.
z=s.Symbol('z')
for p in (3,7,11,19,23,31,43):
 N=p-1;g=next(g for g in range(1,p) if primitive(g,p));log={pow(g,j,p):j for j in range(N)}
 def eta(a):return 0 if a%p==0 else (1 if pow(a%p,N//2,p)==1 else -1)
 for k in range(1,N):
  e=gcd(k,N);d=N//e;j=k//e
  S=[0]*d;J=[0]*d
  for u in range(p):S[j*log[(u*u+1)%p]%d]+=1
  for t in range(p):
   if (1-t)%p:J[j*log[(1-t)%p]%d]+=eta(t)
  mod=s.Poly(s.cyclotomic_poly(d,z),z,domain=s.ZZ)
  def zero(v):return s.rem(s.Poly.from_dict({(a,):b for a,b in enumerate(v) if b},z,domain=s.ZZ),mod).is_zero
  ck(zero([a+b for a,b in zip(S,J)]),'jacobi_identity_exact_order_ring')
  norm=[0]*d
  for a,x in enumerate(S):
   for b,y in enumerate(S):norm[(a-b)%d]+=x*y
  norm[0]-=1 if k==N//2 else p
  ck(zero(norm),'character_norm_exact_order_ring')
  if k==N//2:
   S[0]+=1;ck(zero(S),'quadratic_character_is_minus_one')
# Constants and uniform bounds.
for n in range(1,1201):
 ck(2*phi(n)**2>=n,'totient_square_lower_bound')
 ck((2**len(factors(n)))**4<=64**4*n,'squarefree_divisor_growth_bound')
for B in range(5,70):
 partial=sum((F(1,n*(n-1)) for n in range(3,B+1) if n!=4),F())
 ck(partial<=F(5,12),'odd_prime_tail_majorant')
ck(F(1,2)*(1-F(5,12))==F(7,24)>F(13,48),'mean_class_separation')
Q=1
for q in (3,5,7,11,13):
 Q*=q;r=2*Q+1
 ck(r%4==3 and r%Q==1 and gcd(r,4*Q)==1,'explicit_CRT_residue')
 witness=next(r+4*Q*j for j in range(10000) if prime(r+4*Q*j))
 bound=F(1,2)
 for ell in factors(Q):bound*=F(ell-1,ell)
 ck(F(phi(witness-1),witness-1)<=bound,'CRT_witness_totient_bound')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'samples':samples,'scope':'Exact finite controls only. No finite prime range certifies the two infinite subsequences, Siegel-Walfisz or historical novelty.'},indent=2,sort_keys=True))
