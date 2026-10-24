#!/usr/bin/env python3
"""Exact small permutation covers of the published Hydra square complex.
No bounded search is a test of virtual specialness of the group.
"""
from itertools import permutations
from collections import Counter
import json
from pathlib import Path

def mul(p,q):
    # Right action: vertex v, then p, then q.
    return tuple(q[p[v]] for v in range(len(p)))
def inv(p):
    ans=[0]*len(p)
    for i,j in enumerate(p): ans[j]=i
    return tuple(ans)
def conj(s,a): return mul(mul(inv(a),s),a)
def partitions(n,least=1):
    if not n: yield ()
    for i in range(least,n+1):
        for rest in partitions(n-i,i): yield (i,)+rest

def cycle_type_rep(parts):
    ans=[];at=0
    for k in parts:
        ans.extend(list(range(at+1,at+k))+[at]);at+=k
    return tuple(ans)

def alpha_perms(s,top,m):
    # arrays indexed 0=s, 1=alpha1,...,m=alpha_m
    arr=[s]+[None]*m;arr[m]=top
    for i in range(m,1,-1): arr[i-1]=conj(s,arr[i])
    return arr if mul(s,arr[1])==mul(arr[1],s) else None

def transitive(arr):
    todo=[0];seen={0}
    for v in todo:
        for p in arr:
            q=p[v]
            if q not in seen: seen.add(q);todo.append(q)
    return len(seen)==len(arr[0])

class DSU:
    def __init__(self,n): self.p=list(range(n))
    def find(self,a):
        while self.p[a]!=a:
            self.p[a]=self.p[self.p[a]];a=self.p[a]
        return a
    def union(self,a,b):
        a,b=self.find(a),self.find(b)
        if a!=b:self.p[b]=a

def hyperplanes(arr):
    n=len(arr[0]);m=len(arr)-1;d=DSU(n*(m+1))
    eid=lambda x,v:x*n+v
    for i in range(1,m+1):
        prev=0 if i==1 else i-1
        for v in range(n):
            # square boundary s alpha_i alpha_prev^-1 alpha_i^-1
            d.union(eid(i,v),eid(i,arr[0][v]))
            d.union(eid(0,v),eid(prev,arr[i][v]))
    roots=[d.find(i) for i in range(n*(m+1))]
    crosses=[]
    for i in range(1,m+1):
        for v in range(n):
            if roots[eid(0,v)]==roots[eid(i,v)]:crosses.append((i,v))
    return roots,crosses

def search(m,n):
    stat=Counter();first=None;least=None
    for typ in partitions(n):
        s=cycle_type_rep(typ)
        for top in permutations(range(n)):
            stat['pairs_mod_S_conjugacy']+=1
            arr=alpha_perms(s,top,m)
            if arr is None:continue
            stat['relator_satisfying']+=1
            if not transitive(arr):continue
            stat['connected_covers']+=1
            roots,cross=hyperplanes(arr)
            stat['self_crossing_covers' if cross else 'without_self_crossing']+=1
            if least is None or len(cross)<least['self_crossing_squares']:
                least={'self_crossing_squares':len(cross),'S':list(s),'top':list(top),'hyperplanes':len(set(roots))}
            if not cross and first is None:first={'S':list(s),'top':list(top),'all_generators':[list(p) for p in arr],'hyperplanes':len(set(roots))}
    return {'rank':m,'cover_degree':n,'counts':dict(stat),'least_crossing_example':least,'first_without_self_crossing':first}

if __name__=='__main__':
    rows=[search(m,n) for m in (2,3,4,5,6) for n in range(1,7)]
    out={'warning':'Only the canonical published square cubulation, bounded degree<=6. No group virtual-specialness conclusion. S reduced only by simultaneous conjugation.','rows':rows}
    Path(__file__).with_name('cover_search_results.json').write_text(json.dumps(out,indent=2)+'\n')
    for r in rows:print(r['rank'],r['cover_degree'],r['counts'].get('connected_covers',0),r['counts'].get('without_self_crossing',0),r['least_crossing_example']['self_crossing_squares'])
