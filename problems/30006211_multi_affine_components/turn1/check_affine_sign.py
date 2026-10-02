#!/usr/bin/env python3
import itertools,json,random
checks=0;derivatives=0
def ck(x):
 global checks
 assert x;checks+=1

def monomial_partial(U,k,x):
 if k not in U:return 0
 z=1
 for j in U:
  if j!=k:z*=x[j]
 return z
for n in range(3,8):
 for d in range(3,n+1):
  mons=list(itertools.combinations(range(n),d))
  for S in mons:
   ell=S[-1];T=S[:-1];i=T[0];x=[0]*n
   for j in T[:-1]:x[j]=1
   x[T[-1]]=-(d-2);ck(sum(x)==0);ck(all(x[j] for j in T))
   val=1
   for j in T:val*=x[j]
   for U in mons:
    z=monomial_partial(U,ell,x)-monomial_partial(U,i,x)
    ck(z==(val if U==S else 0));derivatives+=1
# Verify the exact quadratic lift after eliminating the last active coordinate.
rng=random.Random(34501);lifts=0
for r in range(2,9):
 for _ in range(30):
  diag=[rng.randrange(-3,4) for _ in range(r-1)];off={(i,j):rng.randrange(-3,4) for i in range(r-1) for j in range(i+1,r-1)}
  a={(i,r-1):-diag[i] for i in range(r-1)}
  a.update({(i,j):off[i,j]-diag[i]-diag[j] for i,j in off})
  for i in range(r-1):ck(-a[i,r-1]==diag[i])
  for i,j in off:ck(a[i,j]-a[i,r-1]-a[j,r-1]==off[i,j])
  for _ in range(4):
   y=[rng.randrange(-3,4) for _ in range(r-1)];x=y+[-sum(y)]
   q=sum(diag[i]*y[i]**2 for i in range(r-1))+sum(c*y[i]*y[j] for (i,j),c in off.items())
   G=sum(c*x[i]*x[j] for (i,j),c in a.items());ck(q==G)
  lifts+=1
# Scope control: without the sign hypothesis two components occur.
for n in range(3,10):
 for x1 in (-1,1):
  y=[x1]+[0]*(n-2);x=y+[-sum(y)];G=-x[0]*sum(x[1:])-1;ck(sum(x)==0 and G==0)
print(json.dumps({'assertions':checks,'highest_degree_coefficient_tests':derivatives,'quadratic_lifts':lifts,'scope':'Exact polynomial identities and counter-controls; nonnegativity, local-minimum differentiation and connectedness are proved analytically.'},indent=2))
