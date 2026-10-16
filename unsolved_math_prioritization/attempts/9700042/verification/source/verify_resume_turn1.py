#!/usr/bin/env python3
"""Independent finite primal/dual checks, using only Python standard library.
Research checks do not prove the infinite-volume theorem.
"""
from itertools import product
from heapq import heappop, heappush
from math import comb, sqrt
from random import Random
import json
from pathlib import Path


def edges(n):
 return [((x,y),(x+dx,y+dy)) for x in range(n) for y in range(n)
         for dx,dy in [(1,0),(0,1)] if x+dx<n and y+dy<n]

def primal(n,closed):
 source={(x,y) for x in range(n) for y in range(n) if (x==0 or y==0) and x<n-1 and y<n-1}
 interior=[(x,y) for x in range(1,n-1) for y in range(1,n-1)]
 es=edges(n); best=2*n
 for bits in product((0,1),repeat=len(interior)):
  S=source|{v for v,bit in zip(interior,bits) if bit}
  best=min(best,sum(u in S and v not in S and (u,v) not in closed for u,v in es))
 return best

def dual_arcs(n):
 # Reflect the dual y-coordinate so that forward directions are east and north.
 N=n-2; arcs=[]
 for x in range(N+1):
  for y in range(N+1):
   if x<N:
    e=((x+1,n-2-y),(x+1,n-1-y))
    arcs += [((x,y),(x+1,y),e,True),((x+1,y),(x,y),e,False)]
   if y<N:
    e=((x,n-2-y),(x+1,n-2-y))
    arcs += [((x,y),(x,y+1),e,True),((x,y+1),(x,y),e,False)]
 return arcs

def dual(n,closed,monotone=False):
 N=n-2; adj={v:[] for v in product(range(N+1),repeat=2)}
 for u,v,e,forward in dual_arcs(n):
  if monotone and not forward: continue
  adj[u].append((v,int(forward and e not in closed)))
 d={(0,0):0};heap=[(0,(0,0))]
 while heap:
  dist,u=heappop(heap)
  if dist!=d[u]:continue
  for v,w in adj[u]:
   nd=dist+w
   if nd<d.get(v,10**9):d[v]=nd;heappush(heap,(nd,v))
 forced=[((0,n-2),(0,n-1)),((n-2,0),(n-1,0))]
 return d[N,N]+sum(e not in closed for e in forced)

def relevant(n):
 return sorted({e for _,_,e,_ in dual_arcs(n)}|{((0,n-2),(0,n-1)),((n-2,0),(n-1,0))})

def coordinate_checks():
 results=[]
 for N in range(1,5):
  for k in range(1,6):
   actual=sum(sum(max(a-b,0) for a,b in zip((0,)+xs,xs+(N,)))<=k
              for xs in product(range(N+1),repeat=k))
   bound=sum(comb(k+1,t)*comb(k,t)*comb(N+2*k-t,k-t) for t in range(k+1))
   smooth=comb(N+2*k,k)*(1+sqrt(k/(N+2*k)))**(2*k+1)
   assert actual<=bound<=smooth+1e-8
   results.append({'N':N,'k':k,'actual':actual,'combinatorial_bound':bound,'smooth_bound':smooth})
 return results

def main():
 reports=[];witness=None
 for n in (2,3,4):
  es=relevant(n);count=0
  for bits in product((0,1),repeat=len(es)):
   closed={e for e,b in zip(es,bits) if b}
   a=primal(n,closed);b=dual(n,closed)
   assert a==b,(n,closed,a,b)
   m=dual(n,closed,True)
   if a<m and (witness is None or len(closed)<len(witness['closed_edges'])):
    witness={'n':n,'closed_edges':sorted(closed),'flow':a,'monotone_cut':m}
   count+=1
  reports.append({'n':n,'relevant_edges':len(es),'exhaustive_configurations':count,'primal_dual_matches':count})
 rng=Random(9700042);random_reports=[]
 for n,trials in [(5,120),(6,30)]:
  es=relevant(n)
  for i in range(trials):
   q=[.01,.1,.3,.5,.9][i%5];closed={e for e in es if rng.random()<q}
   assert primal(n,closed)==dual(n,closed)
  random_reports.append({'n':n,'trials':trials,'matches':trials})
 out={'schema':'oriented-flow-new-continuation-checks-v1','exhaustive':reports,'seeded':random_reports,
      'recovered_monotone_obstruction':witness,'coordinate_counts':coordinate_checks(),
      'limits':'Finite tests are not a proof of the limiting inequality or conjecture.'}
 Path(__file__).with_name('TURN_C1_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='coordinate_counts'},indent=2))
if __name__=='__main__':main()
