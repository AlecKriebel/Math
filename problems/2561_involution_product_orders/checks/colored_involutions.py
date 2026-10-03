"""Exact modest-size colored-graph search; Python standard library only."""
from itertools import combinations, product
from collections import Counter
from math import gcd
import json, time

def compose(p,q): return tuple(p[q[i]] for i in range(len(p)))
def order(p):
    visited=set(); ans=1
    for i in range(len(p)):
        if i in visited: continue
        j=i; k=0
        while j not in visited: visited.add(j); k+=1; j=p[j]
        ans=ans*k//gcd(ans,k)
    return ans

def matching(vertices):
    if not vertices: yield []; return
    a=vertices[0]
    for j in range(1,len(vertices)):
        b=vertices[j]
        for rest in matching(vertices[1:j]+vertices[j+1:]): yield [(a,b)]+rest

def alternating_class(n,k):
    out=[]
    for support in combinations(range(n),2*k):
        for pairs in matching(list(support)):
            p=list(range(n))
            for a,b in pairs:p[a]=b;p[b]=a
            out.append(tuple(p))
    return out

def psl2_prime_class(p):
    # faithful action on the projective line F_p union {infinity}; trace-zero matrices
    out=set()
    for a,b,c in product(range(p),repeat=3):
        if (-a*a-b*c)%p !=1:continue
        perm=[]
        for x in range(p):
            num=(a*x+b)%p; den=(c*x-a)%p
            perm.append(num*pow(den,-1,p)%p if den else p)
        perm.append(a*pow(c,-1,p)%p if c else p)
        out.add(tuple(perm))
    return sorted(out)

def tables(D):
    pos={x:i for i,x in enumerate(D)}; n=len(D)
    M=[[order(compose(a,b)) for b in D] for a in D]
    C=[[pos[compose(compose(a,b),a)] for b in D] for a in D]
    assert all(M[i][i]==1 for i in range(n))
    assert all(M[i][j]==M[j][i] for i in range(n) for j in range(n))
    # Closure and injectivity of the involution-to-conjugation map are checked.
    assert len(set(tuple(x) for x in C))==n
    return M,C

def solve(M,C,max_nodes=200000,max_seconds=90):
    n=len(M); colors=sorted(set(sum(M,[]))); t0=time.monotonic(); nodes=0; autos=[]
    def refine(P,Q):
        while True:
            sigs=[]
            for part in [P,Q]:
                ss={}
                for cell in part:
                    for x in cell:
                        sig=[]
                        for target in part:
                            cc=Counter(M[x][y] for y in target)
                            sig.extend(cc[c] for c in colors)
                        ss[x]=tuple(sig)
                sigs.append(ss)
            PP=[]; QQ=[]
            for a,b in zip(P,Q):
                da={};db={}
                for x in a:da.setdefault(sigs[0][x],[]).append(x)
                for x in b:db.setdefault(sigs[1][x],[]).append(x)
                if set(da)!=set(db):return None
                for s in sorted(da):
                    if len(da[s])!=len(db[s]):return None
                    PP.append(da[s]);QQ.append(db[s])
            if len(PP)==len(P):return PP,QQ
            P,Q=PP,QQ
    def search(P,Q):
        nonlocal nodes
        nodes+=1
        if nodes>max_nodes or time.monotonic()-t0>max_seconds:raise TimeoutError((nodes,len(autos)))
        r=refine(P,Q)
        if r is None:return
        P,Q=r
        candidates=[(len(a),i) for i,a in enumerate(P) if len(a)>1]
        if not candidates:
            f=[None]*n
            for a,b in zip(P,Q):f[a[0]]=b[0]
            assert all(M[f[i]][f[j]]==M[i][j] for i in range(n) for j in range(n))
            assert all(f[C[i][j]]==C[f[i]][f[j]] for i in range(n) for j in range(n)), ('nonextendible',f)
            autos.append(f);return
        _,i=min(candidates);a=P[i][0]
        for b in Q[i]:
            search(P[:i]+[[a],[x for x in P[i] if x!=a]]+P[i+1:], Q[:i]+[[b],[x for x in Q[i] if x!=b]]+Q[i+1:])
    search([[0],list(range(1,n))],[[0],list(range(1,n))])
    return {'vertices':n,'colors':colors,'stabilizer_size':len(autos),'group_order':n*len(autos),'nodes':nodes,'seconds':round(time.monotonic()-t0,3),'all_stabilizer_automorphisms_extend':True}

def a5_local(D,M):
    blocks={i:[j for j,a in enumerate(D) if a[i]==i] for i in range(5)}
    for i,B in blocks.items():
        assert len(B)==3
        for a in B:
            neighbors={j:[b for b in blocks[j] if M[a][b]==3] for j in blocks if j!=i}
            assert all(len(bs)==1 for bs in neighbors.values())
            for j,k in combinations(neighbors,2):
                assert (M[neighbors[j][0]][neighbors[k][0]]==3)==(D[a][j]==k)
    assert all((M[a][b]==2)==any(a in B and b in B for B in blocks.values()) for a in range(15) for b in range(a+1,15))

if __name__=='__main__':
    cases=[('A5_2',alternating_class(5,2)),('A6_2',alternating_class(6,2)),('PSL2_7',psl2_prime_class(7)),('PSL2_11',psl2_prime_class(11)),('A7_2',alternating_class(7,2)),('A8_4',alternating_class(8,4))]
    result={}
    for name,D in cases:
        M,C=tables(D)
        if name=='A5_2':a5_local(D,M)
        try: result[name]=solve(M,C)
        except TimeoutError as e:result[name]={'incomplete':True,'limit':str(e),'vertices':len(D)}
        print(name,json.dumps(result[name]),flush=True)
    with open('small_group_results.json','w') as f:json.dump(result,f,indent=2)
