#!/usr/bin/env python3
"""Exact finite diagnostics for 10000046, independent of the author's matcher.
The solver groups identical ranges with integer multiplicities and uses a
capacitated Dinic flow, then reconstructs a matching on labeled paths.
Run: python independent_checks.py > independent_results.json
Python standard library only. This does not evaluate the infinite-horizon limit.
"""
from collections import defaultdict, deque
from fractions import Fraction
from itertools import product
from math import factorial, prod
import json

assertions = 0
def check(ok, label):
    global assertions
    assert ok, label
    assertions += 1

def walks(d, n, start):
    result = [(start,)]
    for _ in range(n):
        nxt = []
        for path in result:
            for j in range(d):
                for sign in (-1,1):
                    z=list(path[-1]); z[j]+=sign
                    nxt.append(path+(tuple(z),))
        result = nxt
    return result

def group_ranges(paths):
    groups=defaultdict(list)
    for i,p in enumerate(paths):
        groups[frozenset(p)].append(i)
    return list(groups.items())

class Flow:
    def __init__(self,n):
        self.g=[[] for _ in range(n)]
    def add(self,u,v,c):
        a=[v,len(self.g[v]),c,c]
        b=[u,len(self.g[u]),0,0]
        self.g[u].append(a); self.g[v].append(b)
        return a
    def run(self,source,sink):
        answer=0
        while True:
            level=[-1]*len(self.g);level[source]=0;q=deque([source])
            while q:
                u=q.popleft()
                for v,rev,c,old in self.g[u]:
                    if c and level[v]<0:level[v]=level[u]+1;q.append(v)
            if level[sink]<0:return answer
            current=[0]*len(self.g)
            def send(u,amount):
                if u==sink:return amount
                while current[u]<len(self.g[u]):
                    edge=self.g[u][current[u]];v,rev,c,old=edge
                    if c and level[v]==level[u]+1:
                        z=send(v,min(c,amount))
                        if z:
                            edge[2]-=z; self.g[v][rev][2]+=z
                            return z
                    current[u]+=1
                return 0
            while True:
                z=send(source,10**20)
                if not z:break
                answer+=z
    def reachable(self,source):
        seen={source};q=[source]
        while q:
            u=q.pop()
            for v,rev,c,old in self.g[u]:
                if c and v not in seen:seen.add(v);q.append(v)
        return seen

def test(d,n,displacement):
    X=walks(d,n,(0,)*d);Y=walks(d,n,displacement)
    L=len(X);A=group_ranges(X);B=group_ranges(Y)
    na,nb=len(A),len(B);sink=1+na+nb
    flow=Flow(sink+1)
    for i,(a,ids) in enumerate(A):flow.add(0,1+i,len(ids))
    for j,(b,ids) in enumerate(B):flow.add(1+na+j,sink,len(ids))
    links=[]
    for i,(a,_) in enumerate(A):
        for j,(b,_) in enumerate(B):
            if a.isdisjoint(b):
                links.append((i,j,flow.add(1+i,1+na+j,L+1)))
    maximum=flow.run(0,sink)
    reached=flow.reachable(0)
    coverA={i for i in range(na) if 1+i not in reached}
    coverB={j for j in range(nb) if 1+na+j in reached}
    dual=sum(len(A[i][1]) for i in coverA)+sum(len(B[j][1]) for j in coverB)
    check(dual==maximum,'flow equals weighted cover')
    check(all(i in coverA or j in coverB for i,j,e in links),'every edge is covered')
    # Reconstruct a literal matching of individual path labels.
    pendingA=[ids.copy() for a,ids in A];pendingB=[ids.copy() for b,ids in B]
    matching=[]
    for i,j,e in links:
        for _ in range(e[3]-e[2]):
            matching.append((pendingA[i].pop(),pendingB[j].pop()))
    check(len(matching)==maximum,'matching size')
    check(len({i for i,j in matching})==maximum,'left labels unique')
    check(len({j for i,j in matching})==maximum,'right labels unique')
    check(all(set(X[i]).isdisjoint(Y[j]) for i,j in matching),'every matched pair has disjoint full ranges')
    # Complete to a permutation, checking both exact full-path marginals.
    restA=[i for ids in pendingA for i in ids];restB=[j for ids in pendingB for j in ids]
    permutation=matching+list(zip(restA,restB))
    check(sorted(i for i,j in permutation)==list(range(L)),'first finite marginal uniform')
    check(sorted(j for i,j in permutation)==list(range(L)),'second finite marginal uniform')
    check(sum(set(X[i]).isdisjoint(Y[j]) for i,j in permutation)==maximum,'permutation optimal mass')
    # A direct exhaustive Hall deficiency audit, with original path multiplicity.
    if L<=8:
        neighbors=[{j for j,b in enumerate(Y) if set(a).isdisjoint(b)} for a in X]
        defect=0
        for mask in range(1<<L):
            ids=[i for i in range(L) if mask>>i&1]
            union=set().union(*(neighbors[i] for i in ids))
            defect=max(defect,len(ids)-len(union))
        check(maximum==L-defect,'exhaustive Hall deficiency')
    distance=sum(map(abs,displacement))
    if n<distance:check(maximum==L,'synchronous finite-horizon threshold')
    if distance==0:check(maximum==0,'time-zero collision excludes every edge')
    return {'d':d,'N':n,'displacement':displacement,'labeled_paths':L,
            'range_groups':[na,nb],'maximum_matching':maximum,'minimum_cover':dual,
            'a_N':str(Fraction(maximum,L))}

cases=[]
for n in range(11):cases.append((1,n,(2,)))
for d in (2,3):
    for n in range(4):cases.append((d,n,(2,)+(0,)*(d-1)))
    cases.append((d,2,(1,1)+(0,)*(d-2)))
cases.extend([(4,1,(2,0,0,0)),(4,2,(2,0,0,0)),
              (3,2,(10,0,0)),(4,2,(10,0,0,0)),
              (1,2,(0,)),(3,1,(0,0,0)),(1,10,(10,))])
results=[test(*case) for case in cases]
for d in (1,2,3):
    seq=[Fraction(r['a_N']) for r in results if r['d']==d and r['displacement']==(2,)+(0,)*(d-1)]
    check(all(a>=b for a,b in zip(seq,seq[1:])),'finite optimal masses decrease')

# Independent unrestricted SRW endpoint recursion, including negative steps.
# At graph distance ten the first possible hitting time is exactly ten.
shortest=0
hit_records=[]
for d in (3,4):
    counts={(0,)*d:1}
    for n in range(1,11):
        out=defaultdict(int)
        for z,m in counts.items():
            for j in range(d):
                for sign in (-1,1):
                    w=list(z);w[j]+=sign;out[tuple(w)]+=m
        counts=out
        check(sum(counts.values())==(2*d)**n,'SRW endpoint total mass')
    for a in product(range(11),repeat=d):
        if sum(a)!=10:continue
        value=factorial(10)//prod(factorial(k) for k in a)
        check(counts[a]==value,'distance-ten multinomial first-hit count')
        shortest+=1
    # A signed non-axis displacement, plus the original axis convention.
    targets=[(10,)+(0,)*(d-1), ((3,-4,3) if d==3 else (2,-3,1,4))]
    for z in targets:
        count=factorial(10)//prod(factorial(abs(k)) for k in z)
        check(counts[z]==count,'signed shortest-path count')
        hit_records.append({'d':d,'displacement':z,'hit_by_10':str(Fraction(count,(2*d)**10))})
        # One fixed ten-step word gives a cross-time collision for synchronous translation.
        path=[(0,)*d]
        for j,a in enumerate(z):
            for _ in range(abs(a)):
                nxt=list(path[-1]);nxt[j]+=1 if a>0 else -1;path.append(tuple(nxt))
        Y=[tuple(v+w for v,w in zip(pos,z)) for pos in path]
        check(len(path)==11 and path[-1]==Y[0],'translation collision at different times')
        check(all(a!=b for a,b in zip(path,Y)),'translation has no simultaneous collision')
        check(set(path[:-1]).isdisjoint(Y[:-1]),'the first nine-step ranges are disjoint')

print(json.dumps({'pass':True,'assertions':assertions,'matching_cases':results,
                  'distance_ten_shortest_path_counts':shortest,
                  'first_hit_examples':hit_records,
                  'scope':'Exact finite transport certificates and elementary controls only. No positive lower bound uniform in the horizon, no three-dimensional solution, and no full proof audit of the cited four-dimensional preprint.'},indent=2))
