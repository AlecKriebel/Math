#!/usr/bin/env python3
"""Finite proper-coloring gadgets with total deficits3,5,9,11 and no loss6."""
import itertools,json,math

def proper_clique(n):
    assert n>=3
    mod=n if n%2 else n-1;inf=n-1
    return {(i,j):((2*i)%mod if not n%2 and j==inf else (i+j)%mod) for i in range(n) for j in range(i+1,n)}

def gadget(d):
    n={3:4,5:5,9:6,11:7}[d];e=proper_clique(n)
    if d==9:e[0,5]=5
    if d==11:e[1,6]=7;e[2,5]=8;e[0,1]=9
    assert math.comb(n,2)-len(set(e.values()))==d
    return n,e

def signature(n,e):
    sig={}
    for mask in range(1<<n):
      S=[i for i in range(n) if mask>>i&1];cols={e[i,j] for i,j in itertools.combinations(S,2)}
      d=math.comb(len(S),2)-len(cols);sig.setdefault(len(S),set()).add(d)
    return {k:sorted(v) for k,v in sig.items()}

def representation(p):
    assert p>=10
    base=10+(p-10)%5
    ds={10:[5,5],11:[11],12:[3,9],13:[3,5,5],14:[5,9]}[base]+[5]*((p-base)//5)
    assert sum(ds)==p and ds.count(3)<=1
    return ds

def main():
    out={}
    for d in [3,5,9,11]:
      n,e=gadget(d);s=signature(n,e);loss=sorted({d-x for v in s.values() for x in v})
      assert 6 not in loss
      if d!=3:assert all(x==0 or x>=4 for x in loss)
      out[str(d)]={'vertices':n,'edge_colors':[[i,j,c] for (i,j),c in e.items()],'deficits_by_size':s,'deficit_losses':loss}
    for p in range(10,10001):
      ds=representation(p);n=sum(gadget(d)[0] for d in ds);assert n<=p+1
      reachable={0}
      for d in ds:
        # truncate to loss<=6 because all losses are nonnegative
        losses=out[str(d)]['deficit_losses'];reachable={x+y for x in reachable for y in losses if x+y<=6}
      assert 6 not in reachable
    result={'gadgets':out,'representations_checked':{'p_min':10,'p_max':10000},'status':'exact finite checks, not a full Erickson-conjecture resolution'}
    print(json.dumps(result,indent=2));open('gap_six_checks.json','w').write(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
