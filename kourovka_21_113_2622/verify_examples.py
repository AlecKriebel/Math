#!/usr/bin/env python3
"""Exact, bounded checks for KOU-21.113; no external data or packages required."""
from itertools import permutations
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path

def mul(a,b): return tuple(a[b[i]] for i in range(len(a)))
def one(n): return tuple(range(n))
def power(a,k):
 r=one(len(a))
 while k:
  if k&1:r=mul(r,a)
  a=mul(a,a); k//=2
 return r

def order(a):
 r=one(len(a)); b=a; k=1
 while b!=r: b=mul(b,a);k+=1
 return k

def parity(a): return sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a)))%2

def ppart_order(m,p):
 q=1
 while m%p==0:m//=p;q*=p
 return q,m

def regular_part(g,p):
 q,r=ppart_order(order(g),p)
 return power(g,q*pow(q,-1,r)) if r>1 else one(len(g))

def p_element(g,p):return ppart_order(order(g),p)[1]==1

def psi_by_two_methods(G,p):
 counts=Counter(regular_part(g,p) for g in G)
 out={}
 pe=[g for g in G if p_element(g,p)]
 for x in G:
  c=0 if order(x)%p==0 else sum(mul(x,u)==mul(u,x) for u in pe)
  assert c==counts[x]
  out[x]=c
 assert sum(out.values())==len(G)
 return out

def cycle(n,*cycles):
 x=list(range(n))
 for cyc in cycles:
  for a,b in zip(cyc,cyc[1:]+cyc[:1]):x[a]=b
 return tuple(x)

def main():
 out={"root_fiber_checks":[],"induced_linear_checks":[]}
 for n in [3,4,5]:
  Sn=list(permutations(range(n)))
  for p in [2,3,5]:
   if p>n:continue
   ps=psi_by_two_methods(Sn,p)
   out['root_fiber_checks'].append({"group":f"S{n}","p":p,"order":len(Sn),"psi_degree":ps[one(n)],"pointwise_verified":len(Sn)})
 G=list(permutations(range(4))); H=[x for x in G if parity(x)==0]
 V=[x for x in H if order(x) in [1,2]]
 t=cycle(4,(0,1,2))
 labels={mul(power(t,j),v):j for j in range(3) for v in V}
 assert len(labels)==len(H)
 assert all(labels[mul(a,b)]==(labels[a]+labels[b])%3 for a in H for b in H)
 counts=Counter(labels[y] for x in G if (y:=regular_part(x,2)) in labels)
 assert counts=={0:16,1:4,2:4}
 out['induced_linear_checks'].append({"G":"S4","H":"A4","p":2,"lambda_order":3,"fiber_counts":[counts[j] for j in range(3)],"multiplicity":(counts[0]-counts[1])//len(H)})
 G=list(permutations(range(5))); t=cycle(5,(0,1,2),(3,4));H=[power(t,j) for j in range(6)]
 labels={power(t,j):j%3 for j in range(6)}
 counts=Counter(labels[y] for x in G if (y:=regular_part(x,2)) in labels)
 assert counts=={0:56,1:2,2:2}
 out['induced_linear_checks'].append({"G":"S5","H":"C6","p":2,"lambda_order":3,"fiber_counts":[counts[j] for j in range(3)],"multiplicity":(counts[0]-counts[1])//len(H)})
 # A5 root counts, without importing a character table.
 G=[x for x in permutations(range(5)) if parity(x)==0]
 result={"group_order":len(G),"by_prime":{}}
 assert len(G)==60
 for p in [2,3,5]:
  ps=psi_by_two_methods(G,p)
  grouped={}
  for x in G:grouped.setdefault(order(x),set()).add(ps[x])
  result['by_prime'][str(p)]={str(k):sorted(v) for k,v in sorted(grouped.items())}
 assert result['by_prime']['2']=={'1':[16],'2':[0],'3':[1],'5':[1]}
 out['A5']=result
 return out

if __name__=='__main__':
 result=main(); dest=Path(__file__).with_name('verification.json');dest.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
