#!/usr/bin/env python3
import itertools as it,json,math
from fractions import Fraction as F
checks=0;counts={}
def ck(v):
 global checks
 assert v
 checks+=1
def sg(p):return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
perms={q:list((p,sg(p)) for p in it.permutations(range(q))) for q in (1,3,5,7)}
def alt(es):
 return sum(s for p,s in perms[len(es)] if all(es[p[j]][1]==es[p[(j+1)%len(es)]][0] for j in range(len(es))))
def tensor_trace(gs,r,s):
 z=0
 for x in range(r):
  for y in range(s):
   u,v=x,y
   for t,a,b in gs:
    if t==0:
     if u!=a:break
     u=b
    else:
     if v!=a:break
     v=b
   else:z+=int((u,v)==(x,y))
 return z
def tensor_alt(gs,r,s):return sum(z*tensor_trace([gs[j] for j in p],r,s) for p,z in perms[len(gs)])
for r,s in ((1,1),(1,2),(2,1),(2,2),(2,3),(3,2)):
 basis=[(0,a,b) for a in range(r) for b in range(r)]+[(1,a,b) for a in range(s) for b in range(s)]
 for q in (1,3,5):
  total=0
  for gs in it.combinations(basis,q):
   target=0
   if all(t==0 for t,a,b in gs):target=s*alt([(a,b) for t,a,b in gs])
   if all(t==1 for t,a,b in gs):target=r*alt([(a,b) for t,a,b in gs])
   ck(tensor_alt(gs,r,s)==target);total+=1
  counts[f'tensor ranks{r},{s} degree{q}']=total
# Complete multilinear basis dual checks, including the degree-seven sign.
for n in range(1,4):
 basis=list(it.product(range(n),repeat=2))
 for q in (1,3,5,7):
  for es in it.combinations(basis,q):
   lhs=(-1)**q*alt([(b,a) for a,b in es]);i=(q+1)//2
   ck(lhs==(-1)**i*alt(es))
# Formal character product rule, with coefficient x^d/d! calculated exactly.
for a,b,x,y in it.product(range(-3,4),repeat=4):
 for d in range(6):
  lhs=F((a+b)*(x+y)**d,math.factorial(d))
  rhs=sum(F(a*x**j*y**(d-j)+b*x**j*y**(d-j),math.factorial(j)*math.factorial(d-j)) for j in range(d+1))
  ck(lhs==rhs)
# Tate shifts and dual grading; no vanishing assumed for an individual root.
for m,t,x in it.product(range(-5,6),repeat=3):
 for d in range(6):
  ck(F((m-t)*x**d,math.factorial(d))==F(m*x**d,math.factorial(d))-t*F(x**d,math.factorial(d)))
  ck(F((-m)*(-x)**d,math.factorial(d))==(-1)**(d+1)*F(m*x**d,math.factorial(d)))
# C=2 but weighted degree one nonzero in Q[x]/x^2.
C=(F(1)+F(1),F(1)+F(-1));T=(F(0)*1+F(1)*1,F(0)*1+F(1)*(-1))
ck(C==(2,0));ck(T==(1,-1));ck(T[1]!=0)
for r in range(1,31):
 for i in range(2,15):ck((r*(1+(-1)**i)==0)==(i%2==1))
print(json.dumps({'status':'PASS','assertions':checks,'basis_controls':counts,'scope':'exact finite multilinear and polynomial identities; p-adic input remains credited theory'},indent=2,sort_keys=True))
