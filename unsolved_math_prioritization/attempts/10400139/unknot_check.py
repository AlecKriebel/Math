#!/usr/bin/env python3
"""Direct old2001 state sum on the boundary of an ordered4-simplex.
The Hamiltonian5-cycle bounds the embedded fan of three2-faces, hence is an unknot.
No later invariant/Jones formula is used in constructing or summing the tensors.
"""
import itertools,json,hashlib
from pathlib import Path
import mpmath as mp
mp.mp.dps=80;N=3;m=1;half=2;q=mp.exp(2j*mp.pi/N)
V=range(5);ts=list(itertools.combinations(V,4));edges=list(itertools.combinations(V,2));faces=list(itertools.combinations(V,3));fi={x:i for i,x in enumerate(faces)}
H={tuple(sorted((i,(i+1)%5))) for i in V}
charges=[(0,2,-1),(2,-3,2),(-2,3,0),(1,0,0),(1,0,0)]
opposites=[((0,1),(2,3)),((1,2),(0,3)),((0,2),(1,3))]
for c in charges:assert sum(c)==1
for e in edges:
 total=sum(c[k] for T,c in zip(ts,charges) for k,pair in enumerate(opposites) if e in [tuple(sorted(T[i] for i in ep)) for ep in pair])
 assert total==(0 if e in H else 2)
# Exact cellular gauge cancellation on this closed triangulation.
exponents={f:0 for f in faces}
for T in ts:
 omitted=next(v for v in V if v not in T);sigma=(-1)**omitted
 for j in range(4):exponents[tuple(v for k,v in enumerate(T) if k!=j)]+=sigma*((-1)**(j+1))
assert set(exponents.values())=={0}

def root(x):return mp.mpf(x)**(mp.mpf(1)/N)
def g(x):return mp.exp(sum(mp.mpf(j)/N*mp.log(1-x*q**j) for j in range(1,N)))
g1=g(1)
def h(x):return x**(-m)*g(x)/g1
def om(x,y,z,n):return mp.fprod(y/(z-x*q**j) for j in range(1,n%N+1))
def bracket(x):return (1-x**N)/(N*(1-x))
local=[]
for T,c in zip(ts,charges):
 omitted=next(v for v in V if v not in T);sigma=(-1)**omitted
 x01=root(T[1]-T[0]);x12=root(T[2]-T[1]);x23=root(T[3]-T[2]);x02=root(T[2]-T[0]);x13=root(T[3]-T[1]);x03=root(T[3]-T[0])
 X=x03*x12;Y=x01*x23;Z=x02*x13;hh=h(Z/X)
 a=(half*c[0])%N;cc=(half*c[1])%N
 ids=[fi[tuple(v for j,v in enumerate(T) if j!=i)] for i in range(4)]
 table={}
 for states in itertools.product(range(N),repeat=4):
  gamma,delta,alpha,beta=states[2],states[0],states[3],states[1]
  if (gamma+delta-beta)%N: val=mp.mpc(0)
  elif sigma==1:
   val=Z**m*q**(cc*(gamma-alpha)-half*a*cc)*hh*q**(alpha*delta+half*alpha*alpha)*om(X,Y,Z,gamma-alpha-a)
  else:
   val=Z**m*q**(cc*(gamma-alpha)+half*a*cc)*bracket(X/Z)/hh*q**(-alpha*delta-half*alpha*alpha)/om(X/q,Y,Z,gamma-alpha+a)
  table[states]=val
 local.append((ids,table))
summ=mp.mpc(0);nonzero=0
for s in itertools.product(range(N),repeat=len(faces)):
 val=mp.mpc(1)
 for ids,tab in local:
  v=tab[tuple(s[j] for j in ids)]
  if not v: val=0;break
  val*=v
 if val:nonzero+=1;summ+=val
edge=mp.fprod(root(b-a)**(1-N) for a,b in edges if (a,b) not in H)
oldH=summ*edge/N**5;oldK=oldH**N;expected=mp.mpf(N)**(-2*N)
error=abs(oldK-expected)
assert error<mp.mpf('1e-65'),mp.nstr(oldK,30)
out={'N':N,'vertices':5,'tetrahedra':5,'faces':10,'enumerated_states':N**10,'nonzero_states':nonzero,'integer_charges':charges,'normalization':'N^(-5) times off-H edge factors times contracted old2001 c-6j symbols','H_real':mp.nstr(oldH.real,35),'H_imag':mp.nstr(oldH.imag,35),'K_real':mp.nstr(oldK.real,35),'K_imag':mp.nstr(oldK.imag,35),'expected_K':'1/729','absolute_error':mp.nstr(error,12),'mpmath_dps':80,'scope':'Direct finite complex diagnostic, not an interval proof; the arbitrary-N factor is established analytically in PROOF.md.','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(out,indent=2,sort_keys=True))
