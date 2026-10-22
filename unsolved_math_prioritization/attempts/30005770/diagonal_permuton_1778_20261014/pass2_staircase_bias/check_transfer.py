from itertools import permutations, combinations
from collections import defaultdict, Counter
from pathlib import Path
import json, functools, sys

def require(condition, context):
    if not condition:
        raise RuntimeError(context)

def std(p):
    ranks={v:i+1 for i,v in enumerate(sorted(p))}
    return tuple(ranks[v] for v in p)
def avoids(p,t):
    return not any(std(tuple(p[i] for i in I))==t for I in combinations(range(len(p)),len(t)))
def S(p):
    n=len(p);q=[0]*n
    for i,v in enumerate(p,1):q[v-1]=i
    return tuple(n+1-v for v in q[::-1])
def top(p):
    n=len(p)
    for k in range(1,n+1):
        if not avoids(tuple(v for v in p if v>n-k),(2,1,3)):return k-1
    return n

def greedy(p):
    out=[];current=p
    while current:
        if len(out)%2==0:
            m=top(current);chosen=tuple(v for v in current if v>len(current)-m)
            current=std(tuple(v for v in current if v<=len(current)-m))
        else:
            m=len(current)
            for k in range(1,len(current)+1):
                if not avoids(current[:k],(1,3,2)):m=k-1;break
            chosen=current[:m];current=std(current[m:])
        st=std(chosen)
        out.append(st if len(out)%2==0 else S(st))
    return tuple(out)

@functools.cache
def K(a,c):
    b=S(c);m=len(a);k=len(b);ans=0
    for I in combinations(range(m+k),m):
        J=set(I);ai=iter(v+k for v in a);bi=iter(b)
        p=tuple(next(ai) if i in J else next(bi) for i in range(m+k))
        if avoids(p,(1,3,2,4)) and top(p)==m:ans+=1
    return ans

N=8
states={m:[p for p in permutations(range(1,m+1)) if avoids(p,(2,1,3))] for m in range(1,N+1)}
@functools.cache
def chains(n):
    out={ (a,):1 for a in states[n] }
    for m in range(2,n):
        for a in states[m]:
            for chain,w in chains(n-m).items():
                k=K(a,chain[0])
                if k:out[(a,)+chain]=k*w
    return out
result={'scope':'Finite checks only; not a limiting-law proof','n_results':[]}
for n in range(1,N+1):
    actual=Counter(greedy(p) for p in permutations(range(1,n+1)) if avoids(p,(1,3,2,4)))
    predicted=chains(n)
    require(dict(actual)==predicted, (n,[(c,actual.get(c),predicted.get(c)) for c in actual.keys()|predicted.keys() if actual.get(c)!=predicted.get(c)][:3]))
    result['n_results'].append({'n':n,'permutations':sum(actual.values()),'distinct_state_chains':len(actual)})
examples=[]
for m in range(1,5):
    for k in range(1,5):
        if m+k>N:continue
        for a in states[m]:
            for c in states[k]:
                require(K((1,2),c)>=1, ('universal incoming state',c))
                require((K(a,(1,2))>=1)==(a!=tuple(range(m,0,-1))), ('ascents permit outgoing edge',a))
                if K(a,c)!=K(c,a) and len(examples)<8:
                    examples.append({'a':a,'c':c,'K_a_c':K(a,c),'K_c_a':K(c,a)})
result['non_symmetric_kernel_examples']=examples
result['squared_kernel_size_coefficients']=[{'n':n,'S_n':sum(v*v for c,v in chains(n).items() if len(c)==2)} for n in range(2,N+1)]
for k in range(1,5):
    for m in range(1,5):
        from math import comb
        require(K(tuple(range(1,k+1)),tuple(range(m,0,-1)))==comb(k+m-1,k-1)-1, ('increasing-decreasing formula',k,m))
result['increasing_decreasing_kernel_formula_checks']=16
result['status']='passed'
Path(__file__).with_name(sys.argv[1] if len(sys.argv)>1 else 'TRANSFER_FINITE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
