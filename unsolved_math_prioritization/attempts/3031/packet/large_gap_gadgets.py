#!/usr/bin/env python3
"""Proper-clique deficit semigroups for gaps6r. Exact certificate generation."""
import json,math,heapq
from gap_six_gadgets import proper_clique,signature

def weight(t):return math.comb(t,2)-(t if t%2 else t-1)

def apery(coins):
    # Each residue's minimum representable value; Dijkstra gives short checked certificates.
    mod=min(coins);dist=[None]*mod;dist[0]=0;reps=[None]*mod;reps[0]=[];heap=[(0,0)]
    while heap:
      v,r=heapq.heappop(heap)
      if v!=dist[r]:continue
      for c in coins:
        w=v+c;s=w%mod
        if dist[s] is None or w<dist[s]:dist[s]=w;reps[s]=reps[r]+[c];heapq.heappush(heap,(w,s))
    assert all(v is not None for v in dist)
    for r,v in enumerate(dist):assert sum(reps[r])==v and v%mod==r
    C=max(dist)-mod+1
    for p in range(C,C+mod):
      r=p%mod;assert p>=dist[r] and (p-dist[r])%mod==0
    return {'modulus':mod,'conductor':C,'residue_minima':dist,'representations':reps}

def main():
    out={'gap12_full_subset_checks':{},'semigroups':{}}
    for t in range(8,13):
      e=proper_clique(t);sg=signature(t,e);d=weight(t)
      loss=sorted({d-x for vals in sg.values() for x in vals})
      assert 12 not in loss and all(x==0 or x>=7 for x in loss)
      out['gap12_full_subset_checks'][str(t)]={'deficit':d,'deficits_by_size':sg,'losses':loss,'subsets_checked':2**t}
    for r in range(2,9):
      d=6*r;orders=list(range(d//2+2,d+1));coins=[weight(t) for t in orders]
      assert math.gcd(*coins)==1
      for t in orders:assert t-1>d/2 and t-1<d and 2*t-3>d
      out['semigroups'][str(d)]={'orders':orders,'coins':coins,**apery(coins)}
    print(json.dumps({k:({'conductor':v['conductor'],'coins':v['coins']}) for k,v in out['semigroups'].items()},indent=2))
    open('large_gap_checks.json','w').write(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
