from itertools import permutations, combinations
from collections import Counter
from pathlib import Path
import functools,json,sys

def require(p,ctx):
    if not p:raise RuntimeError(ctx)
def std(p):
    d={v:i+1 for i,v in enumerate(sorted(p))};return tuple(d[v] for v in p)
def avoids(p,t):
    return not any(std(tuple(p[i] for i in I))==t for I in combinations(range(len(p)),len(t)))
def S(p):
    n=len(p);q=[0]*n
    for i,v in enumerate(p,1):q[v-1]=i
    return tuple(n+1-v for v in q[::-1])
def skew(a,b):return tuple(x+len(b) for x in a)+tuple(b)
def top(p):
    for k in range(1,len(p)+1):
        if not avoids(tuple(v for v in p if v>len(p)-k),(2,1,3)):return k-1
    return len(p)
def cells(p):
    remaining=list(enumerate(p));out=[]
    while remaining:
        q=std(tuple(v for i,v in remaining))
        if len(out)%2==0:
            m=top(q);cut=sorted(v for i,v in remaining)[-m];C=[x for x in remaining if x[1]>=cut]
        else:
            m=len(q)
            for k in range(1,len(q)+1):
                if not avoids(q[:k],(1,3,2)):m=k-1;break
            C=remaining[:m]
        out.append(C);chosen=set(C);remaining=[x for x in remaining if x not in chosen]
    return out

def domino(A,C,word):
    b=S(C);ai=iter(v+len(b) for v in A);bi=iter(b)
    return tuple(next(ai) if t else next(bi) for t in word)
def guard(p,a,c):
    n=len(p);b=len(c)
    q=(n+2,b+1,n+3)+tuple(v if v<=b else v+1 for v in p)
    AA=skew((1,2),a);CC=skew((1,),c)
    require(std(tuple(v for v in q if v>len(CC)))==AA,('guard upper',p,a,c,q))
    require(std(tuple(v for v in q if v<=len(CC)))==S(CC),('guard lower',p,a,c,q))
    require(avoids(q,(1,3,2,4)),('guard avoidance',p,a,c,q))
    require(top(q)==len(AA),('guard greedy',p,a,c,q))
    require(std(q[3:])==p,('guard recovery',p,q))
    return AA,CC,q

def symmetric_guard(p,a,c):
    n=len(p);b=len(c)
    q=(n+3,b+1,b+2,n+4)+tuple(v if v<=b else v+2 for v in p)
    AA=skew((1,2),a);CC=skew((1,2),c)
    require(std(tuple(v for v in q if v>len(CC)))==AA,('symmetric upper',p,a,c,q))
    require(std(tuple(v for v in q if v<=len(CC)))==S(CC),('symmetric lower',p,a,c,q))
    require(avoids(q,(1,3,2,4)),('symmetric avoidance',p,a,c,q))
    require(top(q)==len(AA),('symmetric greedy',p,a,c,q))
    require(std(q[4:])==p,('symmetric recovery',p,q))
    return AA,CC,q

counts=Counter();results=[]
for n in range(0,9):
    keys=set();a_n=0
    for p in permutations(range(1,n+1)):
        if not avoids(p,(1,3,2,4)):continue
        a_n+=1;cs=cells(p) if n else[]
        blue={i for c in cs[::2] for i,v in c}
        A=std(tuple(v for i,v in enumerate(p) if i in blue))
        C=S(std(tuple(v for i,v in enumerate(p) if i not in blue)))
        w=tuple(i in blue for i in range(n))
        byvalue={v:i for i,v in enumerate(p)}
        w2=tuple(byvalue[v] not in blue for v in range(n,0,-1))
        d1=domino(A,C,w);d2=domino(C,A,w2)
        require(avoids(A,(2,1,3)) and avoids(C,(2,1,3)),('cell classes',p,A,C))
        require(avoids(d1,(1,3,2,4)) and avoids(d2,(1,3,2,4)),('two collapses',p,d1,d2))
        key=(A,C,w,w2);require(key not in keys,('collapse collision',p));keys.add(key)
        counts['double_collapses']+=1
    results.append({'n':n,'a_n':a_n,'unique_two_collapse_codes':len(keys)})
# Every unrestricted domino with total size <=7, including empty cells.
Dcounts={};Sgcounts={}
for n in range(0,8):
    D=Counter()
    images={}
    for p in permutations(range(1,n+1)):
        if not avoids(p,(1,3,2,4)):continue
        for b in range(n+1):
            A=std(tuple(v for v in p if v>b));C=S(tuple(v for v in p if v<=b))
            if not (avoids(A,(2,1,3)) and avoids(C,(2,1,3))):continue
            D[(A,C)]+=1
            AA,CC,q=guard(p,A,C)
            symmetric_guard(p,A,C)
            counts['symmetric_guarded_dominoes']+=1
            key=(AA,CC,q)
            require(key not in images,('guard collision',p,A,C))
            images[key]=(p,A,C);counts['guarded_dominoes']+=1
    mixed=sum(d*D[(C,A)] for (A,C),d in D.items())
    square=sum(d*d for d in D.values())
    require(results[n]['a_n']<=mixed<=square,('count inequalities',n,results[n],mixed,square))
    results[n]['unrestricted_cross_product']=mixed;results[n]['unrestricted_square']=square
r={'status':'passed','scope':'Finite checks only; all-size proof is separate','checks':dict(counts),'results':results}
Path(__file__).with_name(sys.argv[1] if len(sys.argv)>1 else 'FINITE_OBSTRUCTION_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
