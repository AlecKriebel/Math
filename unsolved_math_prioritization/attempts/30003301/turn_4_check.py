"""Exact finite-group controls. These inputs are algebraic fixtures, not a
certified monodromy word for the original surface problem."""
from itertools import product
import json
p=3;G=list(product(range(p),repeat=3));E=(0,0,0);X=(1,0,0);Y=(0,1,0);Z=(0,0,1)
checks=0
def mul(a,b):return ((a[0]+b[0])%p,(a[1]+b[1])%p,(a[2]+b[2]+a[0]*b[1])%p)
def inv(a):return ((-a[0])%p,(-a[1])%p,(-a[2]+a[0]*a[1])%p)
def upper(a):
 x,y,z=a;return ((x+y)%p,y,(z+y*(y-1)//2)%p)
def lower(a):
 x,y,z=a;return (x,(y-x)%p,(z-x*(x-1)//2)%p)
def identity(a):return a
def eq(a,b):
 global checks
 assert a==b,(a,b);checks+=1
for a,b,c in product(G,repeat=3):eq(mul(mul(a,b),c),mul(a,mul(b,c)))
for a in G:eq(mul(a,inv(a)),E)
for f in (upper,lower):
 eq(len({f(a) for a in G}),len(G))
 for a,b in product(G,repeat=2):eq(f(mul(a,b)),mul(f(a),f(b)))
def local(z,sigma):return {mul(mul(x,E if eps==0 else z),sigma(inv(x))) for x in G for eps in (0,1)}
def compute(zs,sigmas):
 assert len(zs)==len(sigmas), "One action is required for each vanishing cycle"
 R={E};prefix=identity;sizes=[1]
 for z,sigma in zip(zs,sigmas):
  D=local(z,sigma);R={mul(r,prefix(d)) for r in R for d in D};sizes.append(len(R))
  old=prefix;prefix=lambda x,old=old,sigma=sigma:old(sigma(x))
 return R,sizes
R,sizes=compute([X,Y],[upper,lower])
direct=set()
for x,y,eps,eta in product(G,G,(0,1),(0,1)):
 d1=mul(mul(x,E if eps==0 else X),upper(inv(x)))
 d2=mul(mul(y,E if eta==0 else Y),lower(inv(y)))
 direct.add(mul(d1,upper(d2)))
eq(R,direct)
# An order-sensitive singleton fixture checks that prefix action is not omitted.
eq(mul(X,upper(Y)),(2,1,1))
assert mul(X,upper(Y))!=mul(X,Y);checks+=1
one,s1=compute([Z],[identity]);two,s2=compute([Z,Z],[identity,identity])
eq(one,{E,Z});eq(two,{E,Z,mul(Z,Z)})
assert mul(Z,Z) not in one and mul(Z,Z) in two;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'group_order':len(G),'nontrivial_action_reachable_sizes':sizes,'one_central_factor_size':len(one),'two_central_factor_size':len(two),'single_obstructed_image':mul(Z,Z),'limitations':'Finite algebraic fixtures validate recursion only; no surface-factorization or global cap-class certificate is asserted.'},indent=2))
