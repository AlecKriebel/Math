"""Independent diagram-constraint falsifiers; imports no author checker.
MIT, copyright 2026 Alec Kriebel. These finite tests do not establish completeness.
"""
from collections import defaultdict, Counter
from itertools import permutations
import random,json

def letter(i,e=1):return (i,e)
def virtual(i):return (i,0)
def inverse(w):return tuple((i,-e) for i,e in w[::-1])
def shifted(w):return tuple((i+1,e) for i,e in w)

def color_count(n,w,q):
    # Arc variables and Fox constraints, independent of the author's color-map simulator.
    arcs=list(range(n));variables=n;rows=[]
    for i,e in w:
        i-=1
        if e==0:arcs[i],arcs[i+1]=arcs[i+1],arcs[i];continue
        left,right=arcs[i:i+2]
        over,under=(left,right) if e==1 else (right,left)
        new=variables;variables+=1
        r=defaultdict(int);r[under]+=1;r[new]+=1;r[over]-=2;rows.append(r)
        arcs[i:i+2]=[new,over] if e==1 else [over,new]
    for j,out in enumerate(arcs):
        r=defaultdict(int);r[j]+=1;r[out]-=1;rows.append(r)
    matrix=[[r.get(j,0)%q for j in range(variables)] for r in rows]
    rank=0
    for col in range(variables):
        pivot=next((k for k in range(rank,len(matrix)) if matrix[k][col]),None)
        if pivot is None:continue
        matrix[rank],matrix[pivot]=matrix[pivot],matrix[rank]
        reciprocal=pow(matrix[rank][col],-1,q)
        matrix[rank]=[(x*reciprocal)%q for x in matrix[rank]]
        for k in range(rank+1,len(matrix)):
            factor=matrix[k][col]
            if factor:matrix[k]=[(x-factor*y)%q for x,y in zip(matrix[k],matrix[rank])]
        rank+=1
    return q**(variables-rank)

def crossing_matrix(n,w):
    # Close the explicit endpoint wiring with union-find, rather than permutation cycles.
    parent=list(range(n));wire=list(range(n));events=[]
    def root(x):
        while parent[x]!=x:x=parent[x]
        return x
    for i,e in w:
        i-=1;left,right=wire[i:i+2]
        if e:events.append((left,right,e) if e==1 else (right,left,e))
        wire[i],wire[i+1]=right,left
    for j,end in enumerate(wire):parent[root(j)]=root(end)
    roots=sorted(set(root(j) for j in range(n)));index={r:i for i,r in enumerate(roots)}
    matrix=[[0]*len(roots) for _ in roots]
    for o,u,e in events:
        a,b=index[root(o)],index[root(u)]
        if a!=b:matrix[a][b]+=e
    return tuple(tuple(row) for row in matrix)

def same_matrix(a,b):
    if len(a)!=len(b):return False
    return any(all(a[i][j]==b[p[i]][p[j]] for i in range(len(a)) for j in range(len(a))) for p in permutations(range(len(a))))

def endpoints(k,n,a,b,g):
    S=lambda i,e=1:(letter(i,e),);V=lambda i:(virtual(i),)
    if k=='C':return (n,b),(n,a+b+inverse(a))
    if k=='BC':return (n,b+S(n-1)),(n,a+b+inverse(a)+S(n-1))
    if k=='T':return (n,b+S(n-1)),(n,b+(g,))
    if k=='D':return (n,b),(n+2,b+(g,)+S(n+1))
    if k=='R':return (n,a+S(n-1,-1)+b+S(n-1)),(n,a+V(n-1)+b+V(n-1))
    if k=='L':return (n,shifted(a)+S(1,-1)+shifted(b)+S(1)),(n,shifted(a)+V(1)+shifted(b)+V(1))
    if k=='BR':return (n,a+S(n-2,-1)+b+S(n-2)+S(n-1)),(n,a+V(n-2)+b+V(n-2)+S(n-1))
    if k=='BL':return (n,shifted(a)+S(1,-1)+shifted(b)+S(1)+S(n-1)),(n,shifted(a)+V(1)+shifted(b)+V(1)+S(n-1))
    raise ValueError(k)

def main():
    rng=random.Random(713110642);coverage=Counter();checks=0
    for n in (2,4,6):
        for k in ('C','BC','T','D','R','L','BR','BL'):
            if n==2 and k in ('BR','BL'):continue
            bound=n-1 if k in ('C','D') else n-3 if k in ('BR','BL') else n-2
            letters=[(i,e) for i in range(1,bound+1) for e in (-1,0,1)]
            for trial in range(80):
                a=tuple(rng.choice(letters) for _ in range(trial%5)) if letters else ()
                b=tuple(rng.choice(letters) for _ in range((trial//5)%5)) if letters else ()
                g=(n if k=='D' else n-1,(-1,0,1)[trial%3])
                x,y=endpoints(k,n,a,b,g)
                assert same_matrix(crossing_matrix(*x),crossing_matrix(*y)),(k,n,a,b,'matrix')
                for q in (3,5):assert color_count(*x,q)==color_count(*y,q),(k,n,a,b,q,'Fox')
                coverage[k]+=1;checks+=3
    s=((1,1),);v=((1,0),)
    assert color_count(2,s*3,3)==9 and color_count(2,s,3)==3
    assert not same_matrix(crossing_matrix(2,s*2),crossing_matrix(2,s+v+s+v))
    assert len(crossing_matrix(1,()))!=len(crossing_matrix(2,()))
    # The buffered left tail cannot be shifted along with the blocks: at N=4,
    # a=sigma_1 shifts to sigma_2 while the retained tail must remain sigma_3.
    x,y=endpoints('BL',4,((1,1),),(),None)
    assert x[1][-1]==y[1][-1]==(3,1)
    # False extension of T with b=sigma_1^2 identifies trefoil and unknot.
    print(json.dumps({'status':'PASS_INDEPENDENT_FINITE_CLOSURE_INVARIANT_CONTROLS','legal_scheme_pairs':sum(coverage.values()),'invariant_comparisons':checks,'coverage':dict(coverage),'fox3_trefoil_unknot':[color_count(2,s*3,3),color_count(2,s,3)],'false_R_ordered_matrices':[crossing_matrix(2,s*2),crossing_matrix(2,s+v+s+v)],'mechanisms':['Fox coloring by diagram arc constraints and exact modular rank, q=3 and q=5','Ordered intercomponent signs using explicit closure union-find'],'limits':'Necessary invariants only; no equivalence oracle, completeness proof or novelty certificate'},indent=2))
if __name__=='__main__':main()
