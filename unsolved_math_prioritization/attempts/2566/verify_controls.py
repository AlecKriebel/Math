#!/usr/bin/env python3
"""Small exact controls. These are not odd-prime counterexamples to KOU-21.57."""
import itertools,json,collections,hashlib

def mul(p,q):return tuple(p[q[x]] for x in range(len(p)))
def inv(p):
 r=[0]*len(p)
 for i,j in enumerate(p):r[j]=i
 return tuple(r)
def order(p):
 e=tuple(range(len(p)));q=p;n=1
 while q!=e:q=mul(q,p);n+=1
 return n
def generate(gs):
 e=tuple(range(len(gs[0])));found={e};todo=[e]
 while todo:
  p=todo.pop()
  for g in gs:
   q=mul(p,g)
   if q not in found:found.add(q);todo.append(q)
 return frozenset(found)
def prime_factors(n):
 out=[];p=2
 while p*p<=n:
  if n%p==0:
   out.append(p)
   while n%p==0:n//=p
  p+=1
 if n>1:out.append(n)
 return out

G=set();N=set()
for a,b,c,d in itertools.product(range(7),repeat=4):
 det=(a*d-b*c)%7
 if det==0:continue
 p=[]
 for x in range(8):
  y,z=(a,c) if x==7 else ((a*x+b)%7,(c*x+d)%7)
  p.append(7 if z==0 else y*pow(z,-1,7)%7)
 p=tuple(p);G.add(p)
 if pow(det,3,7)==1:N.add(p)
assert len(G)==336 and len(N)==168
r=next(p for p in sorted(G) if order(p)==8)
R=generate([r]);ri=inv(r)
s=next(p for p in sorted(G-R) if order(p)==2 and mul(mul(p,r),p)==ri)
H=generate([r,s]);A=H&N
assert len(H)==16 and len(A)==8
x=next(x for x in sorted(N-A) if len(generate(list(A)+[x]))==24)
B=generate(list(A)+[x]);assert A<B<=N
# Every proper pi-overgroup of A contains <A,g> for an outsider g.
# Here each such pi-generated group has order24, the full {2,3}-part
# of |N|=168, so it is Hall and admits no larger pi-overgroup.
pi_overgroups={generate(list(A)+[g]) for g in N}
pi_overgroups={B for B in pi_overgroups if set(prime_factors(len(B)))<={2,3}}
assert {len(B) for B in pi_overgroups}=={8,24}
assert len(N)==24*7
omega=[B for B in pi_overgroups if not any(B<C for C in pi_overgroups)]
assert len(omega)==2 and all(len(B)==24 for B in omega)
assert frozenset(mul(mul(inv(r),b),r) for b in omega[0])==omega[1]
hist=collections.Counter()
for g in G-H:
 L=generate([r,s,g]);hist[len(L)]+=1
 assert not set(prime_factors(len(L)))<={2,3}
assert all(mul(mul(inv(g),n),g) in N for g in G for n in N)

def fm(x,y):return ((x[0]+pow(2,x[1],7)*y[0])%7,(x[1]+y[1])%3)
F=list(itertools.product(range(7),range(3)));E=(0,0);C={(0,b) for b in range(3)}
def fi(x):return next(y for y in F if fm(x,y)==E and fm(y,x)==E)
normalizer=[g for g in F if {fm(fm(fi(g),a),g) for a in C}==C]
assert set(normalizer)==C
result={
 'scope':'Exact control examples only; neither is a counterexample to the odd-prime normal-intersection assertion.',
 'even_control':{'G':'PGL(2,7) in its projective-line action','G_order':len(G),'N':'PSL(2,7)','N_order':len(N),'N_normal_verified':True,'pi':[2,3],'H_order':len(H),'H_generators':[r,s],'A_H_intersect_N_order':len(A),'B_containing_A_order':len(B),'B_extra_generator':x,'outside_element_count':len(G-H),'generated_order_histogram':dict(sorted(hist.items())),'H_pi_maximal_exhaustive_one_element_test':True,'A_not_pi_maximal_witness':True,'maximal_pi_overgroups_of_A':len(omega),'overgroup_orders':sorted(map(len,omega)),'H_generator_swaps_overgroups':True,'source':'Guo–Revin–Vdovin arXiv:1808.10107v2 §1.4'},
 'odd_normalizer_control':{'B':'C7 semidirect C3, (a,b)(c,d)=(a+2^b*c mod7,b+d mod3)','B_order':21,'pi':[3,7],'A_order':3,'A_proper':True,'normalizer_equals_A':True,'interpretation':'Normalizer quotient pi-free does not alone force pi-maximality. This A is not asserted submaximal.'}
}
print(json.dumps(result,indent=2))
