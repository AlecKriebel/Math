"""Independent-style algebra controls within this author package, not an independent review."""
from math import gcd
import json
p=1336337;q=17;N=p-1
assert p==16*q**4+1
assert pow(3,N,p)==1 and gcd(pow(3,N//2,p)-1,p)==gcd(pow(3,N//q,p)-1,p)==1
beta=pow(3,N//q,p);assert beta==1267487

def mul(a,b,c):
 z=[0]*(2*q-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):z[i+j]=(z[i+j]+x*y)%p
 for i in range(2*q-2,q-1,-1):z[i-q]=(z[i-q]+c*z[i])%p
 return z[:q]
def power(a,n,c):
 z=[1]+[0]*(q-1)
 while n:
  if n&1:z=mul(z,a,c)
  a=mul(a,a,c);n//=2
 return z
T=[0,1]+[0]*(q-2);u=T;orbit=[]
for k in range(1,q+1):
 u=power(u,p,3);orbit.append(u)
 assert u[1]==pow(beta,k,p) and all(u[i]==0 for i in range(q)if i!=1)
assert orbit[-1]==T and all(u!=T for u in orbit[:-1])
h=pow(3,q,p)
assert power(T,p,h)==T
roots=[3*pow(beta,j,p)%p for j in range(q)]
assert len(set(roots))==q and all(pow(r,q,p)==h for r in roots)
for b in [3,h]:
 disc=((-1)**(q*(q-1)//2)*pow(q,q,p)*pow(b,q-1,p))%p
 assert pow(disc,N//2,p)==1
 bta=pow(b,N//q,p)
 assert pow(bta,q*(q-1)//2,p)==1
for k in [2,4,8,16]:assert pow(3,N//k,p)==pow(h,N//k,p)
print(json.dumps({'status':'PASS_EXACT_FROBENIUS_ALGEBRA_CONTROLS','q':q,'p':p,'base3_beta':beta,'base3_frobenius_orbit_length':len(orbit),'neighbor_base':h,'neighbor_split_roots':roots,'qualification':'This controls the dichotomy and invariant limitations, not the universal primitive-root assertion.'},indent=2))
