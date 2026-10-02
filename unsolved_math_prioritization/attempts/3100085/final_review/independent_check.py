#!/usr/bin/env python3
"""Independent exact controls; authored scripts are not imported or executed here."""
from pathlib import Path
from math import comb,factorial,gcd,lcm,isqrt
from fractions import Fraction as F
from collections import Counter
from itertools import combinations
import json,sys
import sympy as sp

ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
C=Counter()
def ck(g,v):
 if not v:raise AssertionError(g)
 C[g]+=1
def root(n,k):
 if k==1:return n
 if k==2:return isqrt(n)
 lo=0;hi=(1<<((n.bit_length()+k-1)//k))+1
 while hi-lo>1:
  z=(lo+hi)//2
  if z**k<=n:lo=z
  else:hi=z
 return lo
def radical_key(a,b,r):
 g=gcd(a,b);a//=g;b//=g
 for e in range(r,0,-1):
  if r%e:continue
  ra=root(a,e);rb=root(b,e)
  if ra**e==a and rb**e==b:return ra,rb,r//e
def sign(x):return (x>0)-(x<0)
def rising(x,k):return factorial(x+k)//factorial(x)

# Alternate exact pair test using perfect-power reduction, not prime vectors.
pairs=0;hits=[]
for n in range(3,81):
 row=[comb(n,k) for k in range(n+1)];registry={}
 for a,b in combinations(range(n+1),2):
  pairs+=1
  if row[a]==row[b]:
   ck('zero_odds_key_exact_symmetry',a+b==n);continue
  key=radical_key(row[a],row[b],b-a)
  A,B,d=key
  ck('alternate_perfect_power_identity',A**((b-a)//d)*row[b]==B**((b-a)//d)*row[a])
  for c,e in registry.get(key,[]):
   if len({a,b,c,e})==4:hits.append([n,a,b,c,e])
  registry.setdefault(key,[]).append((a,b))
ck('all_real_pair_count',pairs==88556)
ck('all_real_no_collision_through80',not hits)

# Rebuild formal identities through a different polynomial implementation.
x,t=sp.symbols('x t');data=json.loads((ROOT/'TURN_2_CERTIFICATES.json').read_text())
cases=data['cases'];expected={(r,c,r-d) for r in range(3,7) for c,d in combinations(range(1,r),2)}
ck('formal_case_count_and_uniqueness',len(cases)==len(expected)==20 and {(z['r'],z['u'],z['v']) for z in cases}==expected)
for z in cases:
 r,u,v,s,shift=[z[k] for k in ['r','u','v','s','A_shift']]
 ck('formal_inner_span',s==r-u-v>0)
 ck('formal_shift_boundary',shift==(1 if (r,u,v)==(6,2,3) else 0))
 A=sp.Poly(x+shift,x,t,domain=sp.ZZ);B=A+sp.Poly(1+t,x,t,domain=sp.ZZ)
 def rising_poly(Y,n):
  out=sp.Poly(1,x,t,domain=sp.ZZ)
  for i in range(1,n+1):out*=Y+i
  return out
 target=rising_poly(A,r)**s*rising_poly(B+v,s)**r-rising_poly(B,r)**s*rising_poly(A+u,s)**r
 fact=sp.Poly(z['prefactor'],x,t,domain=sp.ZZ)
 ck('formal_nonzero_prefactor',z['prefactor']!=0)
 for f in z['positive_factors']:
  terms=f['terms'];powers=[(i,j) for i,j,c in terms]
  ck('formal_unique_nonnegative_exponents',len(powers)==len(set(powers)) and all(i>=0 and j>=0 for i,j in powers))
  ck('formal_positive_cone',all(c>=0 for i,j,c in terms) and any(i==j==0 and c>0 for i,j,c in terms))
  ck('formal_positive_integer_power',isinstance(f['power'],int) and f['power']>=1)
  fact*=sp.Poly(sum(c*x**i*t**j for i,j,c in terms),x,t,domain=sp.ZZ)**f['power']
 ck('independent_full_factor_identity',fact==target)

B=sp.symbols('B');Q=B**4-230*B**3-2523*B**2-8672*B-9620
ck('boundary_factor_identity',sp.expand(720*(B+4)**6-729*sp.prod(B+j for j in range(1,7))+9*(B+4)*(B+7)*Q)==0)
ck('boundary_strict_bracket',Q.subs(B,240)<0<Q.subs(B,241))
ck('quartic_ratio_derivative',sp.simplify(sp.diff(Q/B**4,B)-(230/B**2+5046/B**3+26016/B**4+38480/B**5))==0)

# Independently enumerate using interior support-position pairs rather than
# author offset loops. Locate cutoff by inequalities to check floor endpoints.
cert=json.loads((ROOT/'TURN_5_CERTIFICATES.json').read_text());given={(z['r'],z['u'],z['v'],z['A']):z for z in cert['cases']}
survive={};total=0;reject=0;pattern_count=0
for r in range(3,13):
 for c,d in combinations(range(1,r),2):
  u=c;v=r-d;s=d-c
  if u>=v:continue
  pattern_count+=1;delta=v-u;T=1
  while T<r-1 or 6*delta*T<=r*r-1:T+=1
  ck('strict_cutoff_floor_agreement',T==max(r-1,(r*r-1)//(6*delta)+1))
  for A in range(T-1):
   total+=1;pa=rising(A,r)**s;pi=rising(A+u,s)**r
   key=(r,u,v,A)
   if pa>=pi:reject+=1;ck('nonroot_gate_coverage',key not in given);continue
   ck('root_gate_coverage',key in given);z=given[key];survive[key]=z
   ck('unique_adjacent_integer_bracket',z['U']==z['L']+1 and isinstance(z['L'],int) and A<=z['L'])
   for side,wantsign in [('L',1),('U',-1)]:
    tail=z[side];N=A+tail+r
    # Direct original-binomial-ratio cross product, distinct from rising powers.
    value=comb(N,A)**s*comb(N,A+r-v)**r-comb(N,A+r)**s*comb(N,A+u)**r
    productvalue=pa*rising(tail+v,s)**r-rising(tail,r)**s*pi
    ck('original_binomial_endpoint_sign',sign(value)==wantsign)
    ck('rising_endpoint_exact_value',productvalue==z['D_'+side])
    ck('endpoint_four_distinct_support_indices',len({A,A+u,A+r-v,A+r})==4 and A+r<=N)
    ck('endpoint_biased_orientation',tail>A and comb(N,A)<comb(N,A+r))
ck('all_938_cases',total==938)
ck('all_879_noroot_cases',reject==879)
ck('all_59_root_certificates',len(survive)==59 and set(survive)==set(given))

# Exact derivative-average and Taylor-constant controls over the claimed spans.
for r in range(3,26):
 mean=F(r+1,2)
 ck('variance_identity',sum((F(j)-mean)**2 for j in range(1,r+1))==F(r*(r*r-1),12))
 for c,d in combinations(range(1,r),2):
  u=c;v=r-d;s=d-c
  for w in {u,v}:
   other=r-s-w
   if w<other:continue
   for A in [F(0),F(1,3),F(7,2),F(29)]:
    outer=sum(1/(A+j) for j in range(1,r+1))/r
    inner=sum(1/(A+j) for j in range(w+1,w+s+1))/s
    ck('strict_reciprocal_average',outer>inner)
  if u>=v:continue
  delta=v-u;T=max(r-1,(r*r-1)//(6*delta)+1)
  for A in [T-1,T,2*T]:
   ck('Taylor_strict_positive_bound',F(delta,2)/(A+mean)-F(r*r-1,24*(A+1)**2)>0)
   # Powers exactly check H_u(A)>0 at these boundary controls.
   ck('integer_cutoff_sign',rising(A,r)**s>rising(A+u,s)**r)

# Classical LCM checked directly, plus sharp arithmetic and irrational-domain
# countercontrols: only the rational-odds consequences are inferred.
squarefree=[]
def factors(n):
 out={};p=2
 while p*p<=n:
  while n%p==0:out[p]=out.get(p,0)+1;n//=p
  p+=1
 if n>1:out[n]=out.get(n,0)+1
 return out
for n in range(81):
 L=lcm(*(comb(n,k) for k in range(n+1)));R=lcm(*range(1,n+2))
 ck('classical_row_lcm_direct',L*(n+1)==R)
 es=factors(L)
 if all(e<=1 for e in es.values()):squarefree.append(n)
 for r in range(2,14):
  K=1
  for p,e in es.items():K*=p**(e//r)
  ck('divisibility_root_not_ordinary_root',L%(K**r)==0)
ck('classical_squarefree_rows',squarefree==[0,1,2,3,5,7,11,23])
ck('rational_odds_threshold',2**13==8192)
ck('Mersenne_range',2**20<3**13<2**21)
ck('LCM_filter_no_converse',lcm(*(comb(8,k) for k in range(9)))==280 and root(280,2)!=2)

print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'alternate_pair_count':pairs,'alternate_collision_count':len(hits),'formal_polynomial_identities':20,'bounded_left_cases':total,'nonroot_gate_cases':reject,'root_brackets':len(survive),'maximum_bracket_endpoint':max(x['U'] for x in survive.values()),'arithmetic':'integer/rational and exact symbolic polynomials; no floating-point comparisons','scope':'Independent finite controls and all finite certificates within the stated claims. The infinite analytic reduction is separately reviewed in REVIEW.md; no author search beyond the frozen scope.'},indent=2,sort_keys=True))
