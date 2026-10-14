#!/usr/bin/env python3
"""Finite regressions; no finite computation proves the asymptotic statements."""
from itertools import permutations, combinations
from fractions import Fraction
from pathlib import Path
from math import comb
import hashlib, json, sys
P=Path(__file__).resolve().parent

def require(ok, data):
    if not ok: raise RuntimeError(data)
def std(p):
    ranks={v:i+1 for i,v in enumerate(sorted(p))}
    return tuple(ranks[v] for v in p)
def av(p,t):
    return not any(std(tuple(p[i] for i in ix))==t for ix in combinations(range(len(p)),len(t)))
def av1324(p):
    return not any(p[i]<p[k]<p[j]<p[l] for i,j,k,l in combinations(range(len(p)),4))
def S(p):
    n=len(p); inv=[0]*n
    for i,v in enumerate(p,1): inv[v-1]=i
    return tuple(n+1-v for v in inv[::-1])
def top(p):
    n=len(p)
    for m in range(1,n+1):
        if not av(tuple(v for v in p if v>n-m),(2,1,3)):return m-1
    return n
def greedy(p):
    out=[]
    while p:
        if len(out)%2==0:
            m=top(p); chosen=std(tuple(v for v in p if v>len(p)-m))
            p=std(tuple(v for v in p if v<=len(p)-m))
        else:
            m=len(p)
            for j in range(1,len(p)+1):
                if not av(p[:j],(1,3,2)):m=j-1;break
            chosen=S(std(p[:m]));p=std(p[m:])
        out.append(chosen)
    return out

def K(A,C):
    B=S(C);a=len(A);b=len(B);cnt=0
    for ix in combinations(range(a+b),a):
        upper=set(ix); ai=iter(v+b for v in A); bi=iter(B)
        p=tuple(next(ai) if i in upper else next(bi) for i in range(a+b))
        if av1324(p) and top(p)==a:cnt+=1
    return cnt

frontier=[]
for n in range(1,8):
    count=0; moment=0; tails=[0]*(n+1)
    for p in permutations(range(1,n+1)):
        if not av1324(p):continue
        count+=1; T=top(p); inv=[0]*n
        for i,v in enumerate(p,1):inv[v-1]=i
        q=tuple(inv[::-1]); L=n+1
        for j in range(1,n+1):
            if not av(q[:j],(3,1,2)):L=j;break
        require(T==L-1,('frontier bijection',p,T,L))
        moment+=2**T
        for m in range(1,T+1):tails[m]+=1
    require(moment==count+sum(2**(m-1)*tails[m] for m in range(1,n+1)),('tail identity',n))
    frontier.append({'n':n,'avoidance_count':count,'u2_first_cell_moment':moment})

states=[p for n in range(1,4) for p in permutations(range(1,n+1)) if av(p,(2,1,3))]
z=Fraction(1,10);q={A:Fraction(i+1,i+2) for i,A in enumerate(states)}
ks={(A,C):K(A,C) for A in states for C in states}
hs=sum(z**(len(A)+len(C))*ks[A,C]**2*(q[C]/q[A])**2 for A in states for C in states)
rec=sum(z**(len(A)+len(C))*ks[A,C]*ks[C,A] for A in states for C in states)
require(hs>=rec,('weighted AMGM',hs,rec))

# Reconstruct the stated staircase by independently imposing both coordinate orders.
def mountain(k):
    sizes=[2**j for j in range(1,k+1)]+[2**j for j in range(k-1,0,-1)]
    cells=[[(j,t) for t in range(a)] for j,a in enumerate(sizes)]
    points=sum(cells,[]); X={p:set() for p in points};Y={p:set() for p in points}
    def seq(graph,word):
        for p,q in zip(word,word[1:]):graph[p].add(q)
    def before(graph,A,B):
        for p in A:graph[p].update(B)
    for cell in cells:seq(X,cell);seq(Y,cell)
    for j in range(len(cells)):
        for l in range(j+1,len(cells)):
            A,B=cells[j],cells[l]
            if l>j+1:before(X,A,B);before(Y,B,A)
            elif j%2==0:
                seq(X,A[:1]+B+A[1:]);before(Y,B,A)
            else:
                before(X,A,B);seq(Y,A[:-1]+B+A[-1:])
    def order(graph):
        deg={p:0 for p in points}
        for children in graph.values():
            for p in children:deg[p]+=1
        out=[]
        while len(out)<len(points):
            avail=[p for p in points if deg[p]==0]
            require(len(avail)==1,('coordinate order ambiguity',k,avail))
            p=avail[0];out.append(p);deg[p]=-1
            for q in graph[p]:deg[q]-=1
        return out
    x=order(X);y=order(Y);yr={p:i+1 for i,p in enumerate(y)}
    pi=tuple(yr[p] for p in x)
    require(av1324(pi),('mountain avoidance',k,pi))
    actual=greedy(pi)
    require(actual==[tuple(range(1,a+1)) for a in sizes],('canonical mountain',k,actual,sizes))
    n=len(pi);inc=sum(pi[i]<pi[j] for i,j in combinations(range(n),2))
    require(n==3*2**k-4 and inc>=comb(2**k,2),('mountain counts',k,n,inc))
    return {'k':k,'n':n,'cell_sizes':sizes,'increasing_pairs':inc,'t12':str(Fraction(inc,comb(n,2))),'permutation':pi}
mountains=[mountain(k) for k in range(1,5)]
files=['WEIGHTED_OPERATOR_BOUNDARY.md','GRADED_CELL_OBSTRUCTION.md',Path(__file__).name]
result={'status':'passed','scope':'Finite exact regressions only, not a limiting or radius proof',
 'frontier_and_tail_checks':frontier,'weighted_matrix_state_count':len(states),'weighted_HS_square':str(hs),'reciprocal_sum':str(rec),'graded_examples':mountains,
 'pins':{name:{'sha256':hashlib.sha256((P/name).read_bytes()).hexdigest(),'bytes':(P/name).stat().st_size} for name in files}}
out=P/(sys.argv[1] if len(sys.argv)>1 else 'CHECK_NORMAL.json')
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
