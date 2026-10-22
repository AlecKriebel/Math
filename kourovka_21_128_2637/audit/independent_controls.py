"""Independent audit controls; never imports or runs author scripts.
Builds relation differences from positive paths, and computes cyclic homology by
cyclotomic group-algebra decomposition. For the noncyclic cover, collapses a
spanning tree before a separate dense finite-field elimination.
"""
import sympy as S
from collections import Counter, deque
from itertools import product, permutations
from fractions import Fraction
from pathlib import Path
import json, hashlib
import numpy as np
x=S.Symbol('x')
BASE=Path(__file__).resolve().parents[1]
OUT=Path(__file__).parent

def relations(edge_labels,power):
    eq=[]
    for a in range(4):
        for b in range(a+1,4):
            m=edge_labels.get((a,b),2)
            eq.append(([a,b]*(m//2)+([a] if m%2 else []), [b,a]*(m//2)+([b] if m%2 else [])))
    eq.append(([0,1,2,3]*power,[]))
    return eq

def cyclotomic_rank(a,phi):
    def red(t): return S.rem(t,phi,x,domain=S.QQ).expand()
    a=[[red(t) for t in row] for row in a]
    rank=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(rank,len(a)) if a[i][j]!=0),None)
        if pivot is None: continue
        a[rank],a[pivot]=a[pivot],a[rank]
        inv=S.invert(a[rank][j],phi,x)
        a[rank]=[red(t*inv) for t in a[rank]]
        for i in range(rank+1,len(a)):
            c=a[i][j]
            if c: a[i]=[red(t-c*u) for t,u in zip(a[i],a[rank])]
        rank+=1
        if rank==len(a): break
    return rank

def cyclic(n,weights,eq):
    a=[]
    for left,right in eq:
        col=[0]*4
        ends=[]
        for word,sgn in [(left,1),(right,-1)]:
            pos=0
            for g in word:
                col[g]+=sgn*x**pos
                pos+=weights[g]
            ends.append(pos)
        assert (ends[0]-ends[1])%n==0
        # Fox identity before imposing x^n=1.
        assert S.expand(sum(col[g]*(x**weights[g]-1) for g in range(4))) == x**ends[0]-x**ends[1]
        a.append(col)
    data=[]
    for d in S.divisors(n):
        phi=S.cyclotomic_poly(d,x)
        r=cyclotomic_rank(a,phi)
        null=4-r-(d!=1)
        data.append({'character_order':int(d),'multiplicity':int(S.totient(d)),'rank_d2':r,'h1_per_character':int(null)})
    return {'degree':n,'rank_d2_Q':sum(z['multiplicity']*z['rank_d2'] for z in data),'b1_Q':sum(z['multiplicity']*z['h1_per_character'] for z in data),'character_blocks':data}

def gf_rank(A,p):
    # Independent dense, column-oriented Gaussian elimination after tree collapse.
    A=np.array(A,dtype=np.int64)%p
    r=0
    pivots=[]
    for c in range(A.shape[1]):
        nonzero=np.flatnonzero(A[r:,c])
        if not len(nonzero): continue
        k=r+int(nonzero[0]); A[[r,k]]=A[[k,r]]
        A[r,c:]=(A[r,c:]*pow(int(A[r,c]),-1,p))%p
        mask=np.flatnonzero(A[r+1:,c])+r+1
        if len(mask):
            A[mask,c:]=(A[mask,c:]-A[mask,c,None]*A[r,None,c:])%p
        pivots.append(c); r+=1
        if r==A.shape[1]: break
    return r,pivots

def large_cover(eq):
    five=[[0,1,2,3,4],[1,2,3,4,0],[0,2,1,4,3],[2,1,0,4,3]]
    inverse=[[p.index(i) for i in range(5)] for p in five]
    actions=[[5*((l+1)%60)+(inverse[g][j] if l%2==0 else five[g][j]) for l in range(60) for j in range(5)] for g in range(4)]
    for t in actions: assert sorted(t)==list(range(300))
    for g in range(4):
        assert all(actions[g][v]//5==(v//5+1)%60 for v in range(300))
    visited={0}; queue=deque([0]); tree=set()
    while queue:
        v=queue.popleft()
        for g in range(4):
            w=actions[g][v]
            if w not in visited:
                visited.add(w); queue.append(w); tree.add(4*v+g)
    assert len(visited)==300 and len(tree)==299
    non_tree=sorted(set(range(1200))-tree)
    projected=[]; relation_closure_counts=[]
    for left,right in eq:
        count=0
        for start in range(300):
            row=Counter(); ends=[]
            for word,sgn in [(left,1),(right,-1)]:
                v=start
                for g in word:
                    row[4*v+g]+=sgn; v=actions[g][v]
                ends.append(v)
            assert ends[0]==ends[1]
            count+=1
            boundary=Counter()
            for e,c in row.items():
                v,g=divmod(e,4); boundary[v]-=c; boundary[actions[g][v]]+=c
            assert all(c==0 for c in boundary.values())
            projected.append([row[e] for e in non_tree])
        relation_closure_counts.append(count)
    ranks={}
    for p in [101,103]:
        rank,pivots=gf_rank(projected,p)
        ranks[str(p)]=rank
        print('300-point rank',p,rank,flush=True)
    assert ranks['101']==len(non_tree)==901
    return {'degree':300,'orbit_size':len(visited),'tree_edges':len(tree),'cycle_space_dimension':len(non_tree),'relator_closures':relation_closure_counts,'integer_boundary_zero':True,'ranks_after_tree_collapse':ranks,'b1_Q':0,'matrix_sha256':hashlib.sha256(np.asarray(projected,dtype='<i8').tobytes()).hexdigest()}

def s3(eq):
    elems=list(permutations(range(3))); hist=Counter()
    def evalword(word,quad):
        v=(0,1,2)
        for g in word: v=tuple(quad[g][i] for i in v)
        return v
    for quad in product(elems,repeat=4):
        if not all(evalword(a,quad)==evalword(b,quad) for a,b in eq): continue
        seen={(0,1,2)}; todo=list(seen)
        for p in todo:
            for q in quad:
                z=tuple(q[i] for i in p)
                if z not in seen: seen.add(z);todo.append(z)
        hist[len(seen)]+=1
    return dict(sorted(hist.items()))

f=relations({(0,1):3,(1,2):4,(2,3):3},6)
h=relations({(0,1):5,(1,2):3,(2,3):3},15)
result={}
result['F4_cyclic']=cyclic(12,[1,1,0,0],f)
print('F4',result['F4_cyclic'],flush=True)
result['H4_cyclic']=cyclic(60,[1,1,1,1],h)
print('H4',result['H4_cyclic'],flush=True)
result['H4_300']=large_cover(h)
result['S3']={'F4':s3(f),'H4':s3(h)}
manifest=json.loads((BASE/'MANIFEST.json').read_text())
manifest_hash=hashlib.sha256((BASE/'MANIFEST.json').read_bytes()).hexdigest()
assert manifest_hash=='7e2b93458975bfafb1141847cfd878cd4be801e8b1a8b058bcf66e63cffd3c2b'
assert all(hashlib.sha256((BASE/e['path']).read_bytes()).hexdigest()==e['sha256'] and (BASE/e['path']).stat().st_size==e['bytes'] for e in manifest['files'])
# New additive publication/audit files are outside the original author manifest.
result['frozen_integrity']={'files':len(manifest['files'])+1,'bytes':sum(e['bytes'] for e in manifest['files'])+(BASE/'MANIFEST.json').stat().st_size,'manifest_sha256':manifest_hash}
(OUT/'independent_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2),flush=True)
