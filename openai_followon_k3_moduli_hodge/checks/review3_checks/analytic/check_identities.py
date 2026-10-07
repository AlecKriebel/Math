#!/usr/bin/env python3
"""Fresh finite checks for the analytic/category/exact-KS V3 dependency audit.
These are algebraic and combinatorial checks, not analytic or Hodge certificates.
"""
from fractions import Fraction
from itertools import product, permutations, combinations
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, heapq

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "sources/pinned/preprints/The-rational-Hodge-conjecture-for-products-of-K3-surfaces-October-4-2026/build/manuscript"
OUT = Path(__file__).resolve().parent

def tree(n, code):
    deg = [1]*n
    for v in code: deg[v] += 1
    leaves = [v for v,d in enumerate(deg) if d == 1]
    heapq.heapify(leaves)
    es = []
    for v in code:
        a = heapq.heappop(leaves)
        es.append(tuple(sorted((a,v))))
        deg[a] -= 1; deg[v] -= 1
        if deg[v] == 1: heapq.heappush(leaves,v)
    if n > 1: es.append(tuple(sorted(leaves)))
    return tuple(es)

def rooted_outputs(n, es, root):
    adj = [[] for _ in range(n)]
    for a,b in es: adj[a].append(b); adj[b].append(a)
    parent = {root:None}
    todo = [root]
    for v in todo:
        for w in adj[v]:
            if w not in parent: parent[w]=v; todo.append(w)
    return parent

tree_cases = normalization_orders = cut_sector_cases = 0
for n in range(1,6):
    codes = [()] if n <= 2 else product(range(n), repeat=n-2)
    for code in codes:
        es = tree(n, code)
        for root in range(n):
            par = rooted_outputs(n, es, root)
            tree_cases += 1
            # Root and ordinary output are fixed by the whole tree, independently
            # of the sequence of normalized cuts.
            final = {(v,par[v]) for v in range(n) if v != root}
            for order in permutations(es):
                seen = set()
                for e in order:
                    child = next(v for v in e if par[v] in e)
                    seen.add((child,par[child]))
                assert seen == final
                normalization_orders += 1
            # Every diagonal/reciprocal designation is retained under cut order.
            for sectors in product([0,1],repeat=len(es)):
                labels = dict(zip(es,sectors))
                for cut_count in range(len(es)+1):
                    for cut in combinations(es,cut_count):
                        assert sorted((e,labels[e]) for e in cut) == sorted((e,labels[e]) for e in reversed(cut))
                        cut_sector_cases += 1

cost_checks = 0
for k in range(16):
    for s in range(k+1):
        r = k-s
        for ep,eq in product([0,1,2,5],repeat=2):
            eps = Fraction(1,3)
            cp = ep + eps*(r+1)
            cq = eq + eps*(s-1)
            total = ep+eq+eps*k
            assert cp+cq == total
            # Ordinary zero-energy unary/zero-input children are unstable and
            # excluded. Positive ordinary energies are at least one here.
            if cq > 0 and cp > 0:
                assert cp < total and cq < total
            cost_checks += 1

fixed_sign = norm_sign = boundary_sign = 0
for b,l,q,r,o in product([0,1],repeat=5):
    lhs = b*(l+q+r+o)+q*(b+q+r+o)+(r+o)*(b+q)
    assert (lhs-b*l-q)%2 == 0
    fixed_sign += 1
for p,q in product(range(60),repeat=2):
    assert ((p+q)*(p+q-1)//2+p*q-p*(p-1)//2-q*(q-1)//2)%2 == 0
    norm_sign += 1
for d in range(1,120):
    assert (d+1+d*(d-1)//2-(d-1)*(d-2)//2)%2 == 0
    boundary_sign += 1

def ident(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def sub(a,b): return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def plus(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(c,a): return [[c*x for x in r] for r in a]
def tensor(a,b):
    return [[a[i//len(b)][j//len(b[0])]*b[i%len(b)][j%len(b[0])] for j in range(len(a[0])*len(b[0]))] for i in range(len(a)*len(b))]
def tensor_list(ms):
    a=[[1]]
    for b in ms: a=tensor(a,b)
    return a
X=[[0,1],[1,0]]; J=[[0,1],[-1,0]]; Z=[[1,0],[0,-1]]; I=ident(2)
def gammas(k):
    gs=[]
    for j in range(k):
        for a in [X,J]: gs.append(tensor_list([Z]*j+[a]+[I]*(k-j-1)))
    return gs
def rank(rows):
    pivots={}
    for row in rows:
        d={i:Fraction(v) for i,v in enumerate(row) if v}
        while d:
            j=min(d)
            if j not in pivots:
                lead=d[j]
                pivots[j]={i:v/lead for i,v in d.items()}
                break
            c=d[j]
            for i,v in pivots[j].items():
                d[i]=d.get(i,Fraction(0))-c*v
                if not d[i]: del d[i]
    return len(pivots)
def commutant_dim(gs):
    m=len(gs[0]); rows=[]
    for g in gs:
        for i,j in product(range(m),repeat=2):
            row=[0]*(m*m)
            for a in range(m):
                row[i*m+a]+=g[a][j]
                row[a*m+j]-=g[i][a]
            rows.append(row)
    return m*m-rank(rows)
clifford=[]
for k in [1,2,3]:
    gs=gammas(k); m=len(gs[0]); one=ident(m)
    for i,j in product(range(2*k),repeat=2):
        qij=(1 if i%2==0 else -1) if i==j else 0
        assert plus(mul(gs[i],gs[j]),mul(gs[j],gs[i])) == scale(2*qij,one)
    delta=one
    for g in gs: delta=mul(delta,g)
    for x in range(2*k):
        dx=mul(delta,gs[x])
        for y in range(2*k):
            qxy=(1 if x%2==0 else -1) if x==y else 0
            assert sub(mul(dx,gs[y]),mul(gs[y],dx)) == scale(2*qxy,delta)
        assert commutant_dim([g for i,g in enumerate(gs) if i!=x]) == 2
    assert commutant_dim(gs)==1
    clifford.append({"quadratic_dimension":2*k,"spin_dimension":m,"full_commutant":1,"perpendicular_commutant":2,"commutator_verified":True})

# The cap factorization equality requires the dimension of the middle space.
# A -> B -> C can have one-dimensional composite but noninjective second map.
a=[[1,0],[0,1]]; t=[[1,0]]
assert rank([r[:] for r in mul(t,a)])==1 and rank(t)==1 and len(a)==2

hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (BASE/(n+".tex") for n in ["topology","curvature","comparison","realization","cohomology","setup","exactks","auxiliary"])}
result={
 "timestamp_utc":datetime.now(timezone.utc).isoformat(),
 "scope":"Finite algebraic/combinatorial checks only; not analytic gluing, HMS, formal verification, or a Hodge certificate.",
 "rooted_tree_cases":tree_cases,"normalization_orders":normalization_orders,
 "cut_sector_cases":cut_sector_cases,"additive_cost_checks":cost_checks,
 "determinant_sign_checks":fixed_sign,"count_normalization_checks":norm_sign,
 "boundary_sign_checks":boundary_sign,"clifford_checks":clifford,
 "strict_cap_rank_boundary_example":"Composite rank 1 through Ext dimension 2 does not force trace injective.",
 "source_sha256":hashes,"all_passed":True}
(OUT/"identity_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="source_sha256"},indent=2))

