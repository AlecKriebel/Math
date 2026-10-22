"""Finite exact diagnostics for the strong-grid/Grandis comparison; not an all-n proof."""
from itertools import combinations, product
from collections import Counter
import json

counts=Counter()
def check(p, label):
    assert p, label
    counts[label]+=1

def graphs(n):
    pairs=list(combinations(range(n),2))
    for bits in product((False,True),repeat=len(pairs)):
        e={(i,i) for i in range(n)}
        for (a,b),on in zip(pairs,bits):
            if on:e.update(((a,b),(b,a)))
        yield e

def clique(s,e):return all((a,b) in e for a in s for b in s)

# All reflexive symmetric 3-vertex domain and target graphs and every map pair.
for ge in graphs(3):
    simplices=[s for mask in range(1,8) if clique(s:=tuple(i for i in range(3) if mask>>i&1),ge)]
    for he in graphs(3):
        maps=[f for f in product(range(3),repeat=3) if all((f[a],f[b]) in he for a,b in ge)]
        for f,g in product(maps,repeat=2):
            cross=all((f[a],g[b]) in he for a,b in ge)
            contiguous=all(clique({f[a] for a in s}|{g[a] for a in s},he) for s in simplices)
            check(cross==contiguous,'graph_strong_equals_clique_contiguity')

# Exact integer-coordinate certificate of the caterpillar, independent of labels.
def delay(x,s):return x if x<=s else x-1
for n in range(1,6):
    for coord in range(n):
        for s in range(-3,5):
            for j in range(-5,7):
                origins=[0]*n;origins[coord]=j
                vertices=list(product(*[(z,z+1) for z in origins]))
                images=[]
                for t in (s,s+1):
                    for v in vertices:
                        w=list(v);w[coord]=delay(w[coord],t);images.append(tuple(w))
                check(all(max(v[k] for v in images)-min(v[k] for v in images)<=1 for k in range(n)), 'delay_pair_in_one_original_cube')
                for x,y in product(vertices,repeat=2):
                    a=list(x);b=list(y);a[coord]=delay(a[coord],s);b[coord]=delay(b[coord],s+1)
                    check(all(abs(c-d)<=1 for c,d in zip(a,b)),'delay_cross_time_edges')

# Explicit based loops in C4: boundary-preserving caterpillars and zero extensions.
e={(i,i) for i in range(4)}|{(i,(i+1)%4) for i in range(4)}|{((i+1)%4,i) for i in range(4)}
loops=[]
for length in range(1,7):
    for inside in product(range(4),repeat=length-1):
        f=(0,)+inside+(0,)
        if all((a,b) in e for a,b in zip(f,f[1:])):loops.append(f)
for f in loops:
    def a(i):return f[i] if 0<=i<len(f) else 0
    L=len(f)-1
    for s in range(0,L+1):
        for i in range(-1,L+3):
            check((a(delay(i,s)),a(delay(i,s))) in e,'reflexive_delay')
            for j in (i-1,i,i+1):
                check((a(delay(i,s)),a(delay(j,s+1))) in e,'actual_loop_caterpillar_cross_edges')
        check(a(delay(0,s))==a(delay(L+1,s))==0,'fixed_finite_boundary')
    check(all(a(delay(i,0))==a(i-1) for i in range(-1,L+3)),'right_translation_is_boundary_delay')

# The shortcut really fails, and box products are a different theory.
a=(0,1,2,3,0)
z=lambda i:a[i] if 0<=i<len(a) else 0
check((z(2),z(0)) not in e,'invalid_one_step_shift_witness')
stages=[(0,1,2,3),(0,0,3,3),(0,0,0,0)]
for f in stages:check(all((f[i],f[(i+1)%4]) in e for i in range(4)),'box_contraction_slices')
for f,g in zip(stages,stages[1:]):check(all((f[i],g[i]) in e for i in range(4)),'box_contraction_tracks')
check(any((f[i],g[j]) not in e for f,g in zip(stages,stages[1:]) for i,j in e),'box_contraction_is_not_strong')

# Exact interpolation weights and degree-2 product placement on every small array.
from fractions import Fraction
for n in range(1,7):
    t=[Fraction(j+1,n+2) for j in range(n)]
    weights=[__import__('functools').reduce(lambda a,b:a*b, (t[i] if eps[i] else 1-t[i] for i in range(n)),Fraction(1)) for eps in product((0,1),repeat=n)]
    check(sum(weights)==1 and all(w>0 for w in weights),'multiaffine_barycentric_weights')
    for coord in range(n):
        t0=t.copy();t0[coord]=0
        ws=[__import__('functools').reduce(lambda a,b:a*b,(t0[i] if eps[i] else 1-t0[i] for i in range(n)),Fraction(1)) for eps in product((0,1),repeat=n)]
        check(sum(ws)==1,'boundary_interpolation_weights')

# Universal separator condition for pasting an arbitrary right-slab homotopy.
for m,r,h,T in product(range(1,6),range(1,5),range(1,5),range(1,4)):
    for left,right in product(product(range(m+1),range(h+1),range(T+1)),product(range(m+1,m+r+2),range(h+1),range(T+1))):
        if all(abs(a-b)<=1 for a,b in zip(left,right)):
            check(left[0]==m and right[0]==m+1,'slab_cross_edges_hit_both_basepoint_faces')

# Actual two-dimensional arrays in the octahedral reflexive graph.
oct_e={(i,j) for i in range(6) for j in range(6) if j != (i^1)}
base=0
selected=[]
for m,n in [(2,2),(2,3),(3,2),(3,3)]:
    pts=list(product(range(m+1),range(n+1)))
    inner=[v for v in pts if 0<v[0]<m and 0<v[1]<n]
    bucket=[]
    for labels in product(range(6),repeat=len(inner)):
        f=dict.fromkeys(pts,base);f.update(zip(inner,labels))
        if all((f[u],f[v]) in oct_e for u in pts for v in pts if max(abs(u[i]-v[i]) for i in range(2))<=1):
            bucket.append((m,n,f))
    # Deterministic spread including all-base and several distinct nonbase labels.
    picks=sorted(set([0,len(bucket)-1]+[j*len(bucket)//7 for j in range(1,7)]))
    selected.extend(bucket[j] for j in picks)
for mf,nf,f in selected:
    for mg,ng,g in selected:
        M,N=mf+mg+1,nf+ng+1
        pts=list(product(range(M+1),range(N+1)))
        edges=[(u,v) for u in pts for v in pts if max(abs(u[i]-v[i]) for i in range(2))<=1]
        off=0
        current=lambda x,y:g.get((x,y),base)
        def combine(right):
            return {v:(f.get(v,base) if v[0]<=mf else right(v[0]-mf-1,v[1])) for v in pts}
        previous=combine(current)
        for h in range(nf+1):
            old=current
            for threshold in range(ng+h,-1,-1):
                step=lambda x,y,old=old,threshold=threshold:old(x,delay(y,threshold))
                nxt=combine(step)
                check(all((previous[u],nxt[v]) in oct_e for u,v in edges),'actual_diagonal_product_homotopy')
                check(all(nxt[v]==base for v in pts if v[0] in (0,M) or v[1] in (0,N)),'actual_product_fixed_boundary')
                previous=nxt
            current=lambda x,y,h=h:g.get((x,y-h-1),base)
            check(previous==combine(current),'actual_product_translation_endpoint')
        diag={v:(f[v] if v in f else g.get((v[0]-mf-1,v[1]-nf-1),base)) for v in pts}
        check(previous==diag,'actual_diagonal_equals_published_product')

print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'finite_loops_checked':len(loops),'scope':'Finite exact diagnostics only. Grandis Theorem 6.6 and the written arbitrary-dimension comparison carry the theorem.'},indent=2,sort_keys=True))
