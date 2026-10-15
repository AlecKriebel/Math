#!/usr/bin/env python3
"""New exact controls: Fomin permutation-matrix growth diagrams and inverse RSK.
No imports from author/inherited scripts. Standard library only. Finite controls
supplement the all-size counting proof in the frozen reconstruction.
"""
from collections import Counter, defaultdict
from functools import cache
from fractions import Fraction as F
from itertools import permutations, product
from math import factorial
import json

C=Counter()
def ck(ok,kind):
    if not ok: raise AssertionError(kind)
    C[kind]+=1

@cache
def partitions(n,cap=None):
    if not n:return ((),)
    out=[]
    for k in range(1,min(n,n if cap is None else cap)+1):
        out.extend((k,)+q for q in partitions(n-k,k))
    return tuple(out)
def inside(a,b):return len(b)<=len(a) and all(x>=y for x,y in zip(a,b))
def transpose(a):return tuple(sum(k>=j for k in a) for j in range(1,max(a,default=0)+1))

@cache
def direct_skew_tableaux(a,b=()):
    """Enumerate cell label assignments, filtering all row/column comparisons.
    Returns tableaux flattened in row-major order (no corner recurrence or DP).
    """
    if not inside(a,b):return ()
    cells=tuple((i,j) for i,k in enumerate(a) for j in range(b[i] if i<len(b) else 0,k))
    relations=tuple((i,j) for i,u in enumerate(cells) for j,v in enumerate(cells)
                    if (u[0]==v[0] and u[1]<v[1]) or (u[1]==v[1] and u[0]<v[0]))
    return tuple(q for q in permutations(range(1,len(cells)+1)) if all(q[i]<q[j] for i,j in relations))
def f(a,b=()):return len(direct_skew_tableaux(a,b))

def bareiss(A):
    """Fraction-free determinant over integers after row denominator clearing."""
    from math import lcm
    B=[];scale=1
    for row in A:
        den=lcm(*(v.denominator for v in row)) if row else 1
        scale*=den;B.append([int(v*den) for v in row])
    n=len(B)
    if not n:return F(1)
    previous=1;sign=1
    for k in range(n-1):
        if not B[k][k]:
            z=next((i for i in range(k+1,n) if B[i][k]),None)
            if z is None:return F(0)
            B[k],B[z]=B[z],B[k];sign=-sign
        pivot=B[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=B[i][j]*pivot-B[i][k]*B[k][j]
                assert numerator%previous==0
                B[i][j]=numerator//previous
        for i in range(k+1,n):B[i][k]=0
        previous=pivot
    return F(sign*B[-1][-1],scale)
@cache
def D(a,b,t=F(1),dimension=None):
    if not inside(a,b):return F(0)
    n=max(len(a),len(b)) if dimension is None else dimension
    if n<max(len(a),len(b)):raise ValueError('insufficient dimension')
    aa=a+(0,)*(n-len(a));bb=b+(0,)*(n-len(b));t=F(t)
    return bareiss([[F(0) if (k:=aa[i]-bb[j]-i+j)<0 else t**k/factorial(k) for j in range(n)] for i in range(n)])

def add_box(a,k):
    q=list(a)+( [0] if k==len(a) else [])
    q[k]+=1
    return tuple(q)
def growth_prefixes(p):
    """Fomin local rule on the permutation matrix; no row insertion."""
    n=len(p);grid=[[() for _ in range(n+1)] for _ in range(n+1)]
    for i in range(1,n+1):
        for j in range(1,n+1):
            alpha,beta,gamma=grid[i-1][j-1],grid[i-1][j],grid[i][j-1]
            if beta!=gamma:
                delta=tuple(max(beta[k] if k<len(beta) else 0,gamma[k] if k<len(gamma) else 0) for k in range(max(len(beta),len(gamma))))
            elif beta==alpha:
                delta=add_box(alpha,0) if p[i-1]==j else alpha
            else:
                row=next(k for k in range(len(beta)) if beta[k]!=(alpha[k] if k<len(alpha) else 0))
                delta=add_box(beta,row+1)
            grid[i][j]=delta
    return tuple(grid[i][n] for i in range(n+1))

def inverse_rsk(a,P,Q):
    rows=[];qrows=[];offset=0
    for k in a:
        rows.append(list(P[offset:offset+k]));qrows.append(list(Q[offset:offset+k]));offset+=k
    answer=[]
    for label in range(sum(a),0,-1):
        r=next(i for i,row in enumerate(qrows) if row and row[-1]==label)
        qrows[r].pop();carry=rows[r].pop()
        for i in range(r-1,-1,-1):
            j=max(j for j,v in enumerate(rows[i]) if v<carry)
            rows[i][j],carry=carry,rows[i][j]
        answer.append(carry)
    return tuple(reversed(answer))

def tableau_prefix_shapes(a,Q):
    rows=[];offset=0
    for k in a:rows.append(Q[offset:offset+k]);offset+=k
    return tuple(tuple(k for row in rows if (k:=sum(v<=cut for v in row))) for cut in range(sum(a)+1))

def direct_lis(p):
    best=[]
    for j,v in enumerate(p):best.append(1+max((best[i] for i in range(j) if p[i]<v),default=0))
    return max(best,default=0)

# Broad determinant boundaries, including actual noncontainment and zero parameters.
shapes=tuple(p for n in range(8) for p in partitions(n))
for a in shapes:
    for b in shapes:
        if not inside(a,b):
            ck(D(a,b)==0,'noncontained_weight_zero');continue
        degree=sum(a)-sum(b);count=f(a,b)
        for t in (F(0),F(1,7),F(3,2),F(-2,3)):
            expected=F(count,factorial(degree))*t**degree
            ck(D(a,b,t)==expected,'bareiss_vs_direct_skew_labelings')
            ck(D(transpose(a),transpose(b),t)==expected,'transpose_vs_direct_skew_labelings')
        for pad in (1,3):ck(D(a,b,F(2,5),max(len(a),len(b))+pad)==D(a,b,F(2,5)),'oversized_padding')
        if a==b:ck(D(a,b,F(0))==1,'equal_shape_zero_parameter')

# All pairs of directly labelled straight tableaux, reverse bumping to permutations.
all_prefixes={};inverse_counts={}
for n in range(8):
    seen=set();hist=Counter()
    for a in partitions(n):
        tabs=direct_skew_tableaux(a)
        for P,Q in product(tabs,repeat=2):
            p=inverse_rsk(a,P,Q)
            ck(sorted(p)==list(range(1,n+1)),'inverse_rsk_is_permutation')
            ck(p not in seen,'inverse_rsk_injective');seen.add(p)
            prefixes=growth_prefixes(p)
            ck(prefixes==tableau_prefix_shapes(a,Q),'growth_diagram_vs_recording_prefixes')
            for cut in range(n+1):ck((prefixes[cut][0] if prefixes[cut] else 0)==direct_lis(p[:cut]),'growth_first_row_vs_quadratic_LIS')
            all_prefixes[p]=prefixes;hist[a]+=1
    ck(len(seen)==factorial(n),'inverse_rsk_exhaustive')
    for a,count in hist.items():ck(count==f(a)**2,'inverse_rsk_final_shape_count')
    inverse_counts[n]=len(seen)

# Every weakly increasing three-block cut, every actual prefix-shape chain,
# and all 64 index triples from 1,...,4. Weak cuts include empty increments.
queries=tuple(product(range(1,5),repeat=3));deltas=(F(2,7),F(3,5),F(5,6))
raw={rs:[F(0)]*8 for rs in queries};selected_chains=[];total_chain_histograms=0
for n in range(8):
    perms=tuple(permutations(range(1,n+1)))
    for a in range(n+1):
        for b in range(a,n+1):
            hist=Counter((all_prefixes[p][a],all_prefixes[p][b],all_prefixes[p][n]) for p in perms)
            total_chain_histograms+=len(hist)
            for chain,count in hist.items():
                l1,l2,l3=chain
                expected=f(l3)*f(l1)*f(l2,l1)*f(l3,l2)
                ck(count==expected,'every_three_prefix_chain_exact_count')
                # Determinant conditional probability, including zero-size blocks.
                ds=(a,b-a,n-b)
                detfactor=D(l3,())*D(l1,(),deltas[0])*D(l2,l1,deltas[1])*D(l3,l2,deltas[2])
                poisson=F(count,factorial(n))
                for d,t in zip(ds,deltas):poisson*=t**d/factorial(d)
                ck(detfactor==poisson,'strip_poisson_permutation_factorials')
            ds=(a,b-a,n-b)
            for rs in queries:
                direct=sum(v for chain,v in hist.items() if all((s[0] if s else 0)<r for s,r in zip(chain,rs)))
                table=0
                for l1 in partitions(a):
                    if max(l1,default=0)>=rs[0]:continue
                    for l2 in partitions(b):
                        if not inside(l2,l1) or max(l2,default=0)>=rs[1]:continue
                        for l3 in partitions(n):
                            if inside(l3,l2) and max(l3,default=0)<rs[2]:table+=f(l3)*f(l1)*f(l2,l1)*f(l3,l2)
                ck(direct==table,'all_index_orders_three_blocks')
                weight=F(direct,factorial(n))
                for d,t in zip(ds,deltas):weight*=t**d/factorial(d)
                raw[rs][n]+=weight
    ck(sum(raw[(4,4,4)][n:n+1])<=sum(deltas)**n/factorial(n),'constrained_coefficient_mass_bound')
    # Exact unconstrained normalization reconstructed through all count allocations.
    un=F(0)
    for a in range(n+1):
        for b in range(a,n+1):
            ds=(a,b-a,n-b);z=F(1)
            for d,t in zip(ds,deltas):z*=t**d/factorial(d)
            un+=z
    ck(un==sum(deltas)**n/factorial(n),'unconstrained_terminal_mass')

# Preprocessing controls on deterministic u ranks for all permutations <=6.
# Comparisons are to direct LIS at every raw query; no determinant evaluator.
def canonical(queries):
    merged={}
    for r,x in queries:
        if x>0:merged[x]=min(r,merged.get(x,r))
    return tuple((merged[x],x) for x in sorted(merged))
query_lists=[(),((2,-1),(1,0)),((4,3),(2,1),(3,3),(1,-2)),((3,2),(1,1),(2,2)),((2,3),(2,1),(4,0)),((3,1),(2,2),(4,3))]
for n in range(7):
    for p in permutations(range(1,n+1)):
        for qs in query_lists:
            original=all(direct_lis(p[:max(0,min(n,x))])<r for r,x in qs)
            cleaned=all(direct_lis(p[:min(n,x)])<r for r,x in canonical(qs))
            ck(original==cleaned,'query_repetition_nonpositive_arbitrary_order')

# Low-index series coefficients and exact gap normalization telescoping.
for n in range(80):
    derivative=F(1,factorial(n)*factorial(n+1))-F(1,factorial(n)*factorial(n+2))
    density=F(n+1,factorial(n)*factorial(n+2))
    ck(derivative==density,'two_particle_mixed_derivative_coefficient')
    ck(density*factorial(n)==F(1,factorial(n+1))-F(1,factorial(n+2)),'gap_density_integral_telescopes')
    if n<8:
        ck(raw[(1,1,1)][n]==int(n==0),'B_zero_all_empty_chain')
        ck(raw[(4,1,2)][n]==deltas[2]**n/factorial(n)**2,'decreasing_indices_force_empty_prefix')

print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),
    'mechanisms':['direct cell-label assignments','inverse RSK reverse row bumping','permutation-matrix Fomin growth diagrams','fraction-free integer Bareiss determinant','quadratic direct LIS'],
    'author_or_inherited_modules_imported':False,'inverse_RSK_permutation_counts_by_size':inverse_counts,
    'max_exhaustive_permutation_size':7,'max_skew_shape_size':7,'index_triples_exhausted':64,
    'three_block_chain_histogram_entries':total_chain_histograms,'strip_lengths':[str(x) for x in deltas],
    'selected_raw_coefficients':{str(rs):[str(v) for v in raw[rs]] for rs in [(1,2,3),(4,1,2),(4,2,3),(2,3,2),(1,1,1),(3,3,3)]},
    'scope_limits':'Finite exact controls through terminal size 7, not proof for unbounded size/indices. No dynamics, uniqueness, multi-time formula, general particle-gap independence, priority, source explicitness, or numerical efficiency claim. All-size analytic joint counting proof is separately frozen.'},indent=2))
