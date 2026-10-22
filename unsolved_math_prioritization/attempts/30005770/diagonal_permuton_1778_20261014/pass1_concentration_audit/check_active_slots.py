#!/usr/bin/env python3
"""Independent finite check of minimum-insertion indexing, not a proof."""
from itertools import permutations, combinations
from collections import Counter
import json
from pathlib import Path

def pattern(xs):
    order={v:i+1 for i,v in enumerate(sorted(xs))}
    return tuple(order[x] for x in xs)

def first_end(pi, alpha):
    m=len(alpha)
    return min((inds[-1]+1 for inds in combinations(range(len(pi)),m)
                if pattern([pi[i] for i in inds])==alpha), default=len(pi)+1)

def avoids(pi,tau):
    return first_end(pi,tau)==len(pi)+1

def ins_min(pi,k):
    shifted=tuple(x+1 for x in pi)
    return shifted[:k]+(1,)+shifted[k:]

def run():
    totals=Counter(); by_length=[]
    for m,nmax in [(2,6),(3,6),(4,5)]:
        counts=Counter()
        for alpha in permutations(range(1,m+1)):
            tau=tuple(x+1 for x in alpha)+(1,)
            r=alpha.index(1)+1
            for n in range(nmax+1):
                for pi in permutations(range(1,n+1)):
                    if not avoids(pi,tau): continue
                    counts['parents']+=1
                    L=first_end(pi,alpha)
                    children=[]
                    for k in range(n+1):
                        child=ins_min(pi,k)
                        good=avoids(child,tau)
                        assert good==(k<L),(alpha,pi,L,k,'active gap')
                        counts['slots']+=1
                        if not good: continue
                        b=first_end(child,alpha)
                        bound=L+1 if k<r-1 else min(L+1,k+m-r+1)
                        assert b>=bound,(alpha,pi,L,k,b,bound)
                        children.append(b)
                    assert len(children)==L
                    for j,b in enumerate(sorted(children),start=1):
                        assert b>=j+1,(alpha,pi,L,children)
                    counts['valid_children']+=len(children)
        by_length.append({'alpha_length':m,'parent_size_max':nmax,**counts})
        totals.update(counts)
    return {'result':'passed','scope':'Finite independent indexing and sorted-label checks only; no asymptotic inference.','by_length':by_length,'totals':dict(totals)}

if __name__=='__main__':
    out=run()
    p=Path(__file__).with_name('finite_active_slot_checks.json')
    p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
