#!/usr/bin/env python3
"""Independent exhaustive fixed-inversion D check through n=7.
Uses every permutation, not a generating-tree closure assumption.
"""
from itertools import permutations, combinations
from collections import Counter
import json

def avoids(p, pattern):
    for idx in combinations(range(len(p)), len(pattern)):
        q=tuple(p[i] for i in idx)
        ranks={v:j+1 for j,v in enumerate(sorted(q))}
        if tuple(ranks[v] for v in q)==pattern:
            return False
    return True

def in_D(p):
    return avoids(p,(1,3,2,4)) and any(
        avoids(p[:t],(1,3,2)) and avoids(p[t:],(2,3,1))
        for t in range(len(p)+1))

def inversions(p):
    return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))

rows=[]
for n in range(8):
    counts=Counter(inversions(p) for p in permutations(range(1,n+1)) if in_D(p))
    rows.append({'n':n,'total':sum(counts.values()),'counts':[counts[k] for k in range(n*(n-1)//2+1)]})
checks=[]
for n in range(7):
    old=rows[n]['counts']; new=rows[n+1]['counts']
    for k in range(n+1):
        a=old[k] if k<len(old) else 0;b=new[k] if k<len(new) else 0
        if a>b: raise RuntimeError((n,k,a,b))
        checks.append({'n':n,'k':k,'count_n':a,'count_n_plus_1':b})
result={'definition':'Av(1324) intersect horizontal Grid([Av132|Av231]), ungridded, empty cells allowed','rows':rows,'all_k_le_n_checks_pass':True,'checks':checks}
print(json.dumps(result,indent=2))
