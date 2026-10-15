#!/usr/bin/env python3
"""New review02 exact finite identities; no third-party dependencies or source imports."""
from fractions import Fraction as F
from math import factorial, comb
import json,datetime
from pathlib import Path
assertions=0
def check(ok):
 global assertions
 assertions+=1
 assert ok
# Bernoulli numbers from their defining triangular recurrence.
B=[F(1)]
for m in range(1,21):
 B.append(-sum(F(comb(m+1,k))*B[k] for k in range(m))/F(m+1))
a=[F(0)]+[(-1)**(j+1)*B[2*j]*F(2**(2*j-1),factorial(2*j)*2*j) for j in range(1,11)]
check(a[1]==F(1,12));check(a[2]==F(1,360))
# a_j here is zeta(2j)/(2j*pi^(2j)); pi^(2n) cancels at fixed total n.
h=[F(1)]
for n in range(1,11):
 h.append(sum(F(j)*a[j]*h[n-j] for j in range(1,n+1))/n)
def vectors(n,j=1):
 if j>n:
  yield ()
 else:
  def rec(rem,k):
   if k>n:
    if rem==0:yield ()
    return
   for c in range(rem//k+1):
    for v in rec(rem-k*c,k+1): yield (c,)+v
  yield from rec(n,1)
def falling(x,r):
 return factorial(x)//factorial(x-r) if x>=r else 0
records=[]
for n in range(1,11):
 vs=list(vectors(n)); ws=[]
 for v in vs:
  w=F(1)
  for j,c in enumerate(v,1):w*=a[j]**c/factorial(c)
  ws.append(w)
 check(sum(ws)==h[n])
 # Finite independent Poisson vector: unnormalized mass omits exactly exp(-sum a_j).
 check(all(sum(j*c for j,c in enumerate(v,1))==n for v in vs))
 for length in range(1,min(n,3)+1):
  # all ordered selectors, allowing repetitions
  import itertools
  for js in itertools.product(range(1,n+1),repeat=length):
   rs={j:js.count(j) for j in set(js)}
   lhs=sum(w*__import__('functools').reduce(lambda z,j:z*falling(v[j-1],rs[j]),rs,F(1)) for v,w in zip(vs,ws))/h[n]
   m=sum(js)
   rhs=F(0) if m>n else h[n-m]/h[n]*__import__('functools').reduce(lambda z,j:z*a[j],js,F(1))
   check(lhs==rhs)
 # Exchangeable order and the k! divisor, repeated sizes included.
 ordered_total=F(0)
 for v,w in zip(vs,ws):
  k=sum(v); multiplicity=factorial(k)
  for c in v:multiplicity//=factorial(c)
  product=F(1)
  for j,c in enumerate(v,1):product*=a[j]**c
  check(F(multiplicity)*product/factorial(k)==w)
  ordered_total+=F(multiplicity)*product/factorial(k)
 check(ordered_total==h[n]);records.append({'n':n,'partition_vectors':len(vs)})
for g in range(2,40):
 for k in range(1,g):
  def d(x):return F(factorial(6*g-5-2*x)*2**(2*x-3),factorial(g-x)*factorial(3*g-3-x)*3**(g-x)) if x>=2 else F(factorial(6*g-5-2*x),2*factorial(g-x)*factorial(3*g-3-x)*3**(g-x))
  check(d(k+1)/d(k)==F(12*(g-k)*(3*g-3-k),(6*g-5-2*k)*(6*g-6-2*k)))
# Finite telescoping product gives B(1) as a limit, without numerical zeta.
for m in range(2,100):
 p=F(1)
 for t in range(2,m+1):p*=1-F(1,t*t)
 check(p==F(m+1,2*m))
# Rational lower bounds for eta and the positive Gamma lower-tail exponent.
# log(1+x)>=x-x^2/2 for x>0; .6*(.1-.005)-.05=.007 >1/220.
check(F(3,5)*(F(1,10)-F(1,200))-F(1,20)>F(1,220))
# log(1.5)>=.5-.125=.375, so 2log1.5-.5>=.25>0.
check(2*(F(1,2)-F(1,8))-F(1,2)>0)
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assertions':assertions,'partition_ranges':records,'mechanisms':['Bernoulli-derived true zeta weights after cancelling pi^(2n)','finite Poisson vector coefficient normalization','all ordered selectors with repetitions through order 3','ordered composition k! and repeated-size multiplicities','exact graph-prefactor cancellation','telescoping B(1)','rational lower bounds for cutoff and Gamma-tail exponents'],'limitations':'Finite algebra controls; asymptotic arguments are reconstructed in INDEPENDENT_RECONSTRUCTION.md.'}
Path(__file__).with_name('INDEPENDENT_CONTROL_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
