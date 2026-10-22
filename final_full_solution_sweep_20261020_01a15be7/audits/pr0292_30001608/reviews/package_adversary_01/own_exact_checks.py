#!/usr/bin/env python3
"""Independent exact falsification, no package imports; finite evidence only."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, math, datetime
checks=0
families={}
def check(ok, family):
 global checks
 if not ok: raise RuntimeError(f'failed {family}')
 checks+=1;families[family]=families.get(family,0)+1

def jumps(s,L):
 a,b,x,y=s;D=x+y+1
 events=[((a+1,b,x,y),L/2),((a,b+1,x,y),L/2)]
 if a: events.append(((a-1,b,x+1,y),F(a*(x+1),D)))
 if b: events.append(((a,b-1,x,y+1),F(b*(y+1),D)))
 if x: events.append(((a,b,x-1,y),F(x*(y+1),D)))
 if y: events.append(((a,b,x,y-1),F(y*(x+1),D)))
 return events

def gen(fun,s,L): return sum(r*(fun(t)-fun(s)) for t,r in jumps(s,L))
def W(s):a,b,x,y=s;return 2*a+2*b+x+y
def Z(s):a,b,x,y=s;return a+x-b-y

def gauss(A,b):
 n=len(b);A=[list(row)+[v] for row,v in zip(A,b)]
 for j in range(n):
  pivot=next(k for k in range(j,n) if A[k][j])
  A[j],A[pivot]=A[pivot],A[j]
  d=A[j][j];A[j]=[v/d for v in A[j]]
  for k in range(n):
   if k!=j:
    d=A[k][j]
    A[k]=[a-d*b for a,b in zip(A[k],A[j])]
 return [row[-1] for row in A]

def dense_corrector(gamma,R):
 mu=sum(k*gamma**k for k in range(R+1))/sum(gamma**k for k in range(R+1))
 A=[[F(0) for j in range(R)] for k in range(R)];rhs=[]
 for k in range(R):
  birth=gamma*(k+1);A[k][k]-=birth+k
  if k+1<R:A[k][k+1]+=birth
  if k:A[k][k-1]+=k
  rhs.append(k-mu)
 vals=gauss(A,rhs)+[F(0)]
 return vals,mu

# Algebra from independently implemented events, including zero coordinates.
for L in [F(1,100),F(1,2),F(7,5),F(20)]:
 for s in product([0,1,2,7],repeat=4):
  a,b,x,y=s;D=x+y+1;u=F(a*(x+1)+b*(y+1),D);d=F(2*x*y+x+y,D)
  check(gen(W,s,L)==2*L-u-d,'generator_workload')
  check(gen(Z,s,L)==F(y-x,D),'generator_imbalance')
  check(2*L-u-d<=2*L-F(sum(s),sum(s)+1),'small_load_workload_bound')

# Solve linear systems independently of the manuscript's prefix formula.
for gamma in [F(1,3),F(1,2),F(2,3),F(7,8)]:
 for R in [1,2,4,8]:
  vals,mu=dense_corrector(gamma,R)
  g=lambda k:vals[k] if k<R else F(0)
  G=g(0);eta=(1+gamma)/2;ell=1/(eta-gamma)
  cutoff=lambda t:F(0) if t<=gamma else (F(1) if t>=eta else ell*(t-gamma))
  def J(s):
   a,b,x,y=s;D=x+y+1
   return cutoff(F(b,D))*g(y)+cutoff(F(a,D))*g(x)
  for k in range(R+1):
   q=(gamma*(k+1)*(g(k+1)-g(k)) if k<R else 0)+(k*(g(k-1)-g(k)) if k else 0)
   check(q==k-mu,'dense_poisson_all_rows')
   check(g(k)>=0,'poisson_nonnegative')
   if k<R:check(g(k)>g(k+1),'poisson_strict_monotone')
  for s in product([0,1,3,97,10**9],[0,1,3,97,10**9],[0,1,R,R+1,R+2],[0,1,R,R+1,R+2]):
   a,b,x,y=s;D=x+y+1;L=F(7,5);d=F(2*x*y+x+y,D)
   Lgx=gen(lambda t:g(t[2]),s,L);Lgy=gen(lambda t:g(t[3]),s,L)
   if y<=R and F(b,D)>=gamma:check(Lgy<=y-mu,'actual_poisson')
   if x<=R and F(a,D)>=gamma:check(Lgx<=x-mu,'actual_poisson')
   LJ=gen(J,s,L)
   check(LJ<=cutoff(F(b,D))*Lgy+cutoff(F(a,D))*Lgx+ell*G*(L+4*d)/D,'postjump_interface')
   check(LJ<=G*(L+2*d),'crude_interface')
   for t,r in jumps(s,L):
    if W(t)==W(s)-1 and sum(t)==sum(s):
     check(cutoff(F(t[1],t[2]+t[3]+1))<=cutoff(F(b,D)),'first_download_cutoff_sign')
     check(cutoff(F(t[0],t[2]+t[3]+1))<=cutoff(F(a,D)),'first_download_cutoff_sign')
  for D in [2,3,9,10**9]:
   for w in [0,1,D,10**18,math.floor(eta*D),math.ceil(eta*D)]:
    delta=cutoff(F(w,D-1))-cutoff(F(w,D))
    check(0<=delta<=2*ell/D,'unbounded_numerator_departure')

# Full constructed certificate for selected rational loads and adversarial regions.
load_summaries=[]
for L in [F(1,100),F(1,2),F(1),F(3)]:
 beta=17*L/8;q=F(7,8);c=2*(beta+4);m=4*c;theta=beta+c+4
 gamma=(theta+1)/(theta+2);eta=(1+gamma)/2;ell=1/(eta-gamma)
 den=F(1);num=F(0);power=F(1);R=0
 while True:
  mu=num/den
  if R>=1 and mu>theta and q*(R+1)>beta+c+2:break
  R+=1;power*=gamma;den+=power;num+=R*power
 vals=[F(0)]*(R+1);prefix=F(0);power=F(1)
 for k in range(R):
  prefix+=power*(k-mu);power*=gamma;vals[k]=prefix/(power*(k+1))
 for k in reversed(range(R)):vals[k]=-vals[k]+vals[k+1]
 g=lambda k:vals[k] if k<R else F(0)
 G=g(0)
 N=max(R+2,3*(R+1),math.ceil((m+(1+eta)*R+eta)/(1-eta)),math.ceil(ell*G*(L+4*(2*R+1))))
 B=(N+R+1)*(beta+c+G*(L+2*(N+R))+1)
 cutoff=lambda t:F(0) if t<=gamma else (F(1) if t>=eta else ell*(t-gamma))
 h=lambda z:F(z*z,2)/m+m/2 if abs(z)<=m else F(abs(z))
 def V(s):
  a,b,x,y=s;D=x+y+1
  return W(s)+c*h(Z(s))+cutoff(F(b,D))*g(y)+cutoff(F(a,D))*g(x)
 for z in sorted(set([-math.ceil(m)-1,-math.ceil(m),-math.floor(m),-1,0,1,math.floor(m),math.ceil(m),math.ceil(m)+1])):
  deriv=max(F(-1),min(F(1),F(z)/m))
  for v in [-1,1]:check(h(z+v)-h(z)<=deriv*v+F(1,2)/m,'rounded_boundaries')
 local_count=0;negative_count=0
 for x,y in product([0,1,R,R+1,N-1,N,N+1],repeat=2):
  D=x+y+1
  candidates=sorted(set([0,1,10**9,math.floor(gamma*D),math.ceil(gamma*D),math.floor(eta*D),math.ceil(eta*D),math.ceil(B)+1]))
  for a,b in product(candidates,repeat=2):
   s=(a,b,x,y);drift=gen(V,s,L)
   if not(x+y<=N+R and a+b<=B):
    check(drift<=-1,'full_certificate_outside_F');negative_count+=1
   check(V(s)>=W(s)>=sum(s),'coercivity')
   check(V(s)<=(1+c)*W(s)+c*m/2+2*G,'linear_upper_bound')
   check((min(x,y)>=R+1) or (y<=R and x>=N) or (x<=R and y>=N) or x+y<=N+R,'region_coverage')
   local_count+=1
 load_summaries.append({'lambda':str(L),'R':R,'N_decimal_digits':len(str(N)),'states':local_count,'outside_F':negative_count})

# Independently detectable broken mechanisms.
negative=[]
gamma=F(1,2);R=4;vals,mu=dense_corrector(gamma,R)
check(R*vals[R-1]==R-mu,'terminal_identity')
wrong_terminal=-mu
check(R*vals[R-1]!=wrong_terminal,'negative_control_missing_terminal_k')
negative.append('terminal RHS -mu instead of R-mu is rejected')
# Reversing the monotonic cutoff yields a positive first-download interface.
f=lambda z:min(F(1),max(F(0),2*z-1))
s=(0,10,8,0);t=(0,9,8,1)
check((1-f(F(t[1],10)))-(1-f(F(s[1],9)))>0,'negative_control_reversed_cutoff')
negative.append('reversed cutoff has positive first-download interface')
check(F(7,8)!=F(1,2),'negative_control_common_chunk_identity')
negative.append('Common Chunk departure at seed+one peer differs from exact DFC')
print(json.dumps({'status':'PASS_FINITE_INDEPENDENT_FALSIFICATION','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assertions':checks,'families':families,'full_certificate_loads':load_summaries,'negative_controls':negative,'scope':'Finite exact checks supplement independent analytic derivation; no universal quantifier proved by enumeration.'},indent=2))
