"""Independently authored finite controls for two earlier full-family mechanisms.
Not an all-n proof or a historical firstness certificate. No network/native writes.
"""
from collections import defaultdict, deque, Counter
from itertools import product, permutations
from math import comb
from pathlib import Path
import json, hashlib, datetime

def exact_determinant(matrix):
    # Fraction-free Bareiss elimination with row pivoting.
    a=[list(row) for row in matrix]; n=len(a); old=1; sign=1
    for k in range(n-1):
        if a[k][k]==0:
            j=next((j for j in range(k+1,n) if a[j][k]),None)
            if j is None:return 0
            a[k],a[j]=a[j],a[k];sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=a[i][j]*pivot-a[i][k]*a[k][j]
                if numerator%old:raise ArithmeticError('nonexact Bareiss division')
                a[i][j]=numerator//old
            a[i][k]=0
        old=pivot
    return sign*a[-1][-1]

def count_original(signs,m):
    counts=[1]*(m+1)
    for s in signs:
        counts=[sum(c for b,c in enumerate(counts) if (a+b<=m if s=='-' else a+b>=m)) for a in range(m+1)]
    return sum(counts)

def reflected_word(signs):
    return ''.join('y' if ((i%2==1 and s=='+') or (i%2==0 and s=='-')) else 'x' for i,s in enumerate(signs,1))

def count_descent(word,m):
    counts=[1]*(m+1)
    for s in word:
        counts=[sum(c for b,c in enumerate(counts) if (b<=a if s=='x' else b>=a)) for a in range(m+1)]
    return sum(counts)

def series_add(a,b):
    d=Counter(a);d.update(b)
    return {w:v for w,v in d.items() if v}

def series_mul(a,b,L):
    out=defaultdict(int)
    for u,c in a.items():
        for v,d in b.items():
            if len(u)+len(v)<=L:out[u+v]+=c*d
    return {w:v for w,v in out.items() if v}

def prior_ehrhart_series(m,L):
    # Chebikin-Ehrenborg (2011), Theorem 4.2. Noncommuting variables.
    U={'y'*j:1 for j in range(L+1)}
    Z=series_mul({'x':1,'y':-1},U,L)
    Q={};power={'':1}
    for j in range(L+1):
        Q=series_add(Q,{w:comb(m+j+1,j+1)*c for w,c in power.items()})
        power=series_mul(power,Z,L)
    R=series_mul(series_mul({'y':1},U,L),Q,L)
    inverse={};power={'':1}
    for j in range(L+1):
        inverse=series_add(inverse,power);power=series_mul(power,R,L)
    return series_mul(series_mul(U,Q,L),inverse,L)

def alcove_data(n):
    vertices=[];family=[];facets=defaultdict(list)
    for ranks in permutations(range(1,n+1)):
        floors=[0]*n
        for i in range(1,n):floors[i]=floors[i-1]+(ranks[i]<ranks[i-1])
        scaled=[floors[i]*(n+1)+ranks[i]-(0 if i==0 else floors[i-1]*(n+1)+ranks[i-1]) for i in range(n)]
        signs=''.join('-' if scaled[i]+scaled[i+1]<n+1 else '+' for i in range(n-1))
        assert all(scaled[i]+scaled[i+1]!=n+1 for i in range(n-1))
        ordered=sorted(range(n),key=lambda i:ranks[i]); f=[0]*n; vv=[]
        for j in range(n+1):
            y=[a+b for a,b in zip(floors,f)]
            x=tuple(y[i]-(0 if i==0 else y[i-1]) for i in range(n))
            assert all(z in (0,1) for z in x)
            vv.append(x)
            if j<n:f[ordered[n-j-1]]=1
        assert len(set(vv))==n+1
        key=tuple(sorted(vv));assert key not in vertices
        a=len(vertices);vertices.append(key);family.append(signs)
        for j in range(n+1):facets[key[:j]+key[j+1:]].append(a)
    adjacency=[set() for _ in vertices]
    for members in facets.values():
        assert len(members)<=2
        if len(members)==2:
            a,b=members;adjacency[a].add(b);adjacency[b].add(a)
    return vertices,family,adjacency

def graph_hist(members,adjacency,root,n):
    distances={root:0};q=deque([root]);allowed=set(members)
    while q:
        a=q.popleft()
        for b in adjacency[a]&allowed:
            if b not in distances:distances[b]=distances[a]+1;q.append(b)
    assert len(distances)==len(members)
    hist=[0]*(n+1)
    for a in members:
        nb=adjacency[a]&allowed
        assert all(abs(distances[a]-distances[b])==1 for b in nb)
        hist[sum(distances[b]<distances[a] for b in nb)]+=1
    return hist

def main():
    results=[];old_cases=graph_cases=unimodular_cases=0
    # All 63 signed families in dimensions 1..6. Every original dilation 0..n.
    for n in range(1,7):
        vv,ff,aa=alcove_data(n);groups=defaultdict(list)
        for simplex in vv:
            determinant=exact_determinant([[v[i]-simplex[0][i] for i in range(n)] for v in simplex[1:]])
            if abs(determinant)!=1:raise ArithmeticError(('nonunimodular alcove',n,simplex,determinant))
            unimodular_cases+=1
        for a,s in enumerate(ff):groups[s].append(a)
        prior=[prior_ehrhart_series(m,n-1) for m in range(n+1)]
        for ss in product('-+',repeat=n-1):
            s=''.join(ss);word=reflected_word(s);lattice=[]
            for m in range(n+1):
                direct=count_original(s,m);reflected=count_descent(word,m);published=prior[m][word]
                assert direct==reflected==published,(n,s,m,direct,reflected,published)
                lattice.append(direct);old_cases+=1
            h=[sum((-1)**j*comb(n+1,j)*lattice[k-j] for j in range(k+1)) for k in range(n+1)]
            g=groups[s]
            for root in {g[0],g[-1]}:
                assert graph_hist(g,aa,root,n)==h,(n,s,root,h)
                graph_cases+=1
            results.append({'n':n,'signs':s,'prior_descent_word':word,'lattice_counts_0_to_n':lattice,'hstar':h,'alcove_count':len(g),'graph_edges':sum(len(aa[a]&set(g)) for a in g)//2})
    out={'format':'pr407-independent-prior-family-controls-v2','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','dimensions':list(range(1,7)),'signed_families':len(results),'old_theorem_ehrhart_cases':old_cases,'dual_graph_root_cases':graph_cases,'unimodular_simplex_determinants':unimodular_cases,'original_cumulative_map_and_reflection':'integer and inverse integer; vertices are checked 0/1','source_lemma_negative_control':{'simplex':'[0,2] in Z','actual_hstar':[1,1],'unrestricted_lemma3_2_prediction':[1],'reason':'All vertex denominators1 alone do not imply numerator1. Theorem3.1 gcd-one condition is necessary; every tested type-A alcove satisfies it.'},'claims_limited':'Finite reproduction of precise prior theorem specializations; does not prove all-n mathematics or historical original-question closure.','cases':results}
    dest=Path(__file__).with_name('INDEPENDENT_PRIOR_CONTROLS.json');dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'}))
if __name__=='__main__':main()
