#!/usr/bin/env python3
"""Exact small certificates for the all-r affine-module proof, using only integers."""
import itertools, json
from pathlib import Path

def mul(a,b,p):
 return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2))%p for i in range(2) for j in range(2))
def act(a,v,p): return tuple(sum(a[2*i+j]*v[j] for j in range(2))%p for i in range(2))
def closure(gens,e,op):
 seen={e};todo=[e]
 while todo:
  x=todo.pop()
  for g in gens:
   y=op(x,g)
   if y not in seen: seen.add(y);todo.append(y)
 return seen

def rank(vs,p):
 basis={}
 for v in vs:
  v=list(v)
  for i,b in sorted(basis.items()):
   if v[i]:
    q=v[i];v=[(x-q*y)%p for x,y in zip(v,b)]
  if any(v):
   i=next(i for i,a in enumerate(v) if a);u=pow(v[i],-1,p);basis[i]=[(a*u)%p for a in v]
 return len(basis)

def check_gl2():
 p=2;e=(1,0,0,1);Q=[a for a in itertools.product(range(p),repeat=4) if (a[0]*a[3]-a[1]*a[2])%p]
 inv={a:next(b for b in Q if mul(a,b,p)==e) for a in Q}
 reps={}
 total=0
 for t in itertools.product(Q,repeat=2):
  if len(closure(t,e,lambda a,b:mul(a,b,p)))!=len(Q):continue
  total+=1
  orbit=[tuple(mul(mul(q,a,p),inv[q],p) for a in t) for q in Q]
  reps[min(orbit)]=None
 tuples=list(reps);N=len(tuples)
 gens=[tuple(t[j] for t in tuples) for j in range(2)]
 B=closure(gens,tuple([e]*N),lambda a,b:tuple(mul(x,y,p) for x,y in zip(a,b)))
 orbit=[sum((act(q,(1,0),p) for q in b),()) for b in B]
 r=rank(orbit,p)
 assert total==18 and N==3 and r==2*N
 # Kernel sets distinguish inflated modules; all coordinate maps are onto.
 kernels=[frozenset(b for b in B if b[i]==e) for i in range(N)]
 assert len(set(kernels))==N
 assert all(len({b[i] for b in B})==6 for i in range(N))
 return dict(group='GL(2,2)',prime=p,group_order=len(Q),generating_pairs=total,automorphism_orbit_representatives=N,subdirect_group_order=len(B),module_dimension=2*N,cyclic_vector_rank=r,distinct_projection_kernels=len(set(kernels)))

def check_cyclic(p,q,root,r):
 assert pow(root,q,p)==1 and all(pow(root,j,p)!=1 for j in range(1,q))
 # Distinct generating epimorphism kernels of Z^r -> C_q. Taking one full
 # automorphism orbit of generating tuples ensures nonisomorphic inflations.
 units=[u for u in range(q) if __import__('math').gcd(u,q)==1]
 reps={}
 for t in itertools.product(range(q),repeat=r):
  if __import__('math').gcd(q,*t)!=1: continue
  reps[min(tuple(u*x%q for x in t) for u in units)]=None
 tuples=list(reps);N=len(tuples)
 B=closure([tuple(t[j] for t in tuples) for j in range(r)],(0,)*N,lambda a,b:tuple((x+y)%q for x,y in zip(a,b)))
 rs=rank([tuple(pow(root,a,p) for a in b) for b in B],p)
 assert rs==N
 return dict(group=f'C{q} acting on F{p}',rank=r,orbit_representatives=N,subdirect_group_order=len(B),cyclic_vector_rank=rs)

out=dict(gl2=check_gl2(),cyclic=[check_cyclic(5,4,2,2),check_cyclic(7,3,2,2)],status='PASS',scope='Finite checks support the written all-r proof; they do not resolve the universal problem.')
print(json.dumps(out,indent=2))
Path(__file__).with_name('affine_module_results.json').write_text(json.dumps(out,indent=2)+'\n')
