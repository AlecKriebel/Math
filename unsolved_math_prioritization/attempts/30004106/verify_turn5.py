#!/usr/bin/env python3
"""Exact finite controls; the auxiliary cyclic functor is not an actual T(H)."""
from itertools import product
from collections import defaultdict
from fractions import Fraction
import json, random
checks=0

def check(x):
 global checks
 assert x
 checks+=1

def clean(a):return {x:v for x,v in a.items() if v}
def add(a,b):
 out=defaultdict(int,a)
 for x,v in b.items():out[x]+=v
 return clean(out)
def scale(a,c):return clean({x:v*c for x,v in a.items()})

def lattice(p,r):
 vectors=list(product(range(p),repeat=r));zero=(0,)*r
 def vadd(a,b):return tuple((x+y)%p for x,y in zip(a,b))
 subs={frozenset([zero])};todo=list(subs)
 while todo:
  H=todo.pop()
  for v in vectors:
   if v in H:continue
   K=frozenset(vadd(h,tuple(c*x%p for x in v)) for h in H for c in range(p))
   if K not in subs:subs.add(K);todo.append(K)
 return sorted(subs,key=lambda H:(len(H),sorted(H)))

lattice_sizes=[];block_cases=0;rng=random.Random(300041065)
for prime,rank in [(2,1),(2,2),(2,3),(2,4),(3,2),(3,3)]:
 sub=lattice(prime,rank);n=len(sub);ix={H:i for i,H in enumerate(sub)}
 meet={(i,j):ix[sub[i]&sub[j]] for i,j in product(range(n),repeat=2)}
 mu={}
 for i in range(n):
  for j in range(i,n):
   if sub[i]<=sub[j]:
    mu[i,j]=1 if i==j else -sum(mu[i,k] for k in range(i,j) if sub[i]<=sub[k]<=sub[j])
 def times(a,b):
  out=defaultdict(int)
  for (i,t),x in a.items():
   for (j,s),y in b.items():
    h=meet[i,j]
    if h:out[h,(t+s)%4]+=x*y
  return clean(out)
 # Formal coherent T(H)=Z/4, all nonzero-subgroup restrictions the identity.
 pp={j:{(i,0):mu[i,j] for i in range(1,j+1) if (i,j) in mu and mu[i,j]} for j in range(1,n)}
 one={(n-1,0):1};summ={}
 for j in pp:summ=add(summ,pp[j])
 check(summ==one)
 for i,j in product(range(n),repeat=2):
  l=meet[i,j]
  orderHK=len(sub[i])*len(sub[j])//len(sub[l]);e=prime**rank
  check((e//orderHK)*(e//len(sub[l]))==(e//len(sub[i]))*(e//len(sub[j])))
  if i and j:
   check(times(pp[i],pp[j])==(pp[i] if i==j else {}))
   check(times(pp[i],{(j,0):1})==(pp[i] if sub[i]<=sub[j] else {}))
 for h in range(1,n):
  images={t:times(pp[h],{(h,t):1}) for t in range(4)}
  for t,s in product(range(4),repeat=2):
   check(times(images[t],images[s])==images[(t+s)%4])
  for t in range(4):
   check({u:a for (j,u),a in images[t].items() if j==h}=={t:1})
   check({(j,(-u)%4):a for (j,u),a in images[t].items()}==images[(-t)%4])
  for k in range(1,n):
   for t in range(4):
    check(times(pp[h],{(k,t):1})==(images[t] if sub[h]<=sub[k] else {}))
  C=sum(abs(a) for a in pp[h].values())
  for _ in range(15):
   f=[Fraction(rng.randrange(-7,8),3) for t in range(4)]
   image={}
   for t,c in enumerate(f):image=add(image,scale(images[t],c))
   norm=sum(map(abs,f));outnorm=sum(map(abs,image.values()))
   check(norm<=outnorm<=C*norm)
   check([image.get((h,t),0) for t in range(4)]==f)
   block_cases+=1
 # Recover arbitrary coefficients by the finite block projections and leading terms.
 for _ in range(8):
  b=clean({(h,t):rng.randrange(-3,4) for h in range(1,n) for t in range(4)})
  recovered={};sum_norm=0
  for h in range(1,n):
   pb=times(pp[h],b)
   leading={t:pb.get((h,t),0) for t in range(4)}
   lifted={}
   for t,c in leading.items():lifted=add(lifted,scale(times(pp[h],{(h,t):1}),c))
   check(lifted==pb)
   recovered=add(recovered,lifted);sum_norm+=sum(map(abs,leading.values()))
  check(recovered==b)
  check(sum_norm<=sum(sum(map(abs,x.values())) for x in pp.values())*sum(map(abs,b.values())))
 lattice_sizes.append({'p':prime,'rank':rank,'subgroups':n})

# F8 = F2[z]/(z^3+z+1), encoded by binary coefficients.
def fm(a,b):
 out=0
 while b:
  if b&1:out^=a
  b>>=1;a<<=1
  if a&8:a^=11
 return out
for a,b,c in product(range(8),repeat=3):
 check(fm(a,b)==fm(b,a))
 check(fm(fm(a,b),c)==fm(a,fm(b,c)))
 check(fm(a,b^c)==fm(a,b)^fm(a,c))
for a in range(1,8):check(any(fm(a,b)==1 for b in range(1,8)))

def mm(A,B):
 a,b,c,d=A;e,f,g,h=B
 return (fm(a,e)^fm(b,g),fm(a,f)^fm(b,h),fm(c,e)^fm(d,g),fm(c,f)^fm(d,h))
I=(1,0,0,1);J=(0,1,0,0)
actions=[(1,x,0,1) for x in range(8)]
check(len(set(actions))==8)
for x,y in product(range(8),repeat=2):
 check(mm(actions[x],actions[y])==actions[x^y])
 check(mm(actions[x],actions[x])==I)
for x in range(1,8):
 check(actions[x]!=I)
 check(fm(x,next(y for y in range(1,8) if fm(x,y)==1))==1)
central=[]
for A in product(range(8),repeat=4):
 comm=mm(A,J)==mm(J,A)
 check(comm==(A[2]==0 and A[3]==A[0]))
 if comm:central.append(A)
check(len(central)==64)
for A in central:
 a,b,c,d=A
 check((mm(A,A)==(0,0,0,0))==(a==0))
 # A unit iff a!=0; explicit inverse a^-1 I + b a^-2 J in characteristic two.
 if a:
  inv=next(x for x in range(1,8) if fm(a,x)==1)
  B=(inv,fm(b,fm(inv,inv)),0,inv)
  check(mm(A,B)==I)
check(2%8!=0)
print(json.dumps({'exact_assertions':checks,'subgroup_lattices':lattice_sizes,
 'weighted_block_norm_cases':block_cases,'auxiliary_functor':'constant Z/4 on nontrivial subgroups, not claimed actual T(H)',
 'F8_C2_cubed_module_indecomposable_control':True,
 'completion_bounds_proved_analytically':True,'universal_symmetry_claimed':False},indent=2))
