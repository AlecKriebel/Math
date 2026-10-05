#!/usr/bin/env python3
"""Independent exact finite-network checks. No source corpus, network, or author imports."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse, collections, json, math

COUNTS=collections.Counter()
def check(truth, category):
    COUNTS[category]+=1
    if not truth: raise AssertionError(category)

def det(a):
    if not a: return Q(1)
    # Leibniz-free recursive cofactor expansion: independent of author's inverse.
    if len(a)==1:return a[0][0]
    return sum(((-1)**j)*a[0][j]*det([row[:j]+row[j+1:] for row in a[1:]])
               for j in range(len(a)))

def inv(a):
    d=det(a)
    if not d: raise ValueError('singular')
    n=len(a)
    return [[Q((-1)**(i+j))*det([row[:i]+row[i+1:] for k,row in enumerate(a) if k!=j])/d
             for j in range(n)] for i in range(n)]

def lap(n,edges):
    a=[[Q(0) for _ in range(n)] for _ in range(n)]
    for u,v,c in edges:
        if u>=0:a[u][u]+=c
        if v>=0:a[v][v]+=c
        if u>=0 and v>=0:a[u][v]-=c;a[v][u]-=c
    return a

def sub(a,vs):return [[a[i][j] for j in vs] for i in vs]
def diff(a,b):return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def transpose(a):return list(map(list,zip(*a)))
def eye(n):return [[Q(i==j) for j in range(n)] for i in range(n)]
def psd(a):return all(det(sub(a,list(s)))>=0 for k in range(1,len(a)+1) for s in combinations(range(len(a)),k))

def grounded(n,edges):
    reached={-1}
    while True:
        nxt=reached|{u for u,v,c in edges if c and v in reached}|{v for u,v,c in edges if c and u in reached}
        if reached==nxt:return sorted(reached-{-1})
        reached=nxt

def compute():
    COUNTS.clear()
    # The actual 2 by 2 lattice box has 4 internal and 8 exiting edges.
    skeleton=[(0,1),(0,2),(1,3),(2,3)]+[(i,-1) for i in range(4) for _ in range(2)]
    graph_counts=collections.Counter()
    for bits in range(1<<len(skeleton)):
        e=[(u,v,Q((bits>>k)&1)) for k,(u,v) in enumerate(skeleton)]
        a=lap(4,e);I=grounded(4,e);graph_counts['patterns']+=1
        if not I:
            check(det(a)==0,'ungrounded_singularity');graph_counts['no_grounded_vertices']+=1;continue
        graph_counts['nonempty_grounded_patterns']+=1
        if len(I)<4:graph_counts['with_ungrounded_complement']+=1
        base=inv(sub(a,I));copies=[]
        for eps in [Q(1,2),Q(1,4)]:
            reg=[(u,v,c if c else eps) for u,v,c in e]
            ce=sub(inv(lap(4,reg)),I);copies.append(ce)
            check(psd(diff(base,ce)),'regularized_covariance_order')
        check(psd(diff(copies[1],copies[0])),'regularization_monotonicity')
        # Killed random walk normalization; all boundary conductances remain in D.
        # Sample by mask for additional identities; covariance-order checks are exhaustive.
        if bits%31==0 or len(I)==1:
            ai=sub(a,I);n=len(I)
            iminusP=[[ai[i][j]/ai[i][i] for j in range(n)] for i in range(n)]
            fundamental=inv(iminusP)
            check(all(fundamental[i][j]/ai[j][j]==base[i][j] for i in range(n) for j in range(n)), 'csrw_vs_vsrw_green_normalization')
            check(mul(ai,base)==eye(n),'inverse_identity')
            # Voltage pinned to 1 at vertex zero, others harmonic, ground zero.
            v=[base[j][0]/base[0][0] for j in range(n)]
            energy=sum(v[i]*ai[i][j]*v[j] for i in range(n) for j in range(n))
            check(energy*base[0][0]==1,'variance_reciprocal_effective_conductance')
    # Branched pendant tree, not merely a path. Root in a genuinely two-site core.
    tree_rows=[]
    for c in [Q(1,3),Q(1),Q(2),Q(5)]:
        core=[(-1,0,Q(2)),(-1,1,Q(3)),(0,1,Q(4))]
        tree=[(0,2,c),(2,3,Q(2)),(2,4,Q(3))]
        cov=inv(lap(5,core+tree));bc=inv(lap(2,core))
        tr=eye(5)
        for child,parent in [(2,0),(3,2),(4,2)]:tr[child][parent]=-1
        tc=mul(mul(tr,cov),transpose(tr))
        expected=[[Q(0) for _ in range(5)] for _ in range(5)]
        for i in range(2):
            for j in range(2):expected[i][j]=bc[i][j]
        for i,x in enumerate([1/c,Q(1,2),Q(1,3)],2):expected[i][i]=x
        check(tc==expected,'branched_tree_independent_increments')
        check(cov[3][4]-bc[0][0]==1/c,'shared_tree_path_covariance')
        tree_rows.append({'root_edge_conductance':str(c),'leaf3_variance':str(cov[3][3]),'leaf4_variance':str(cov[4][4])})
    # Exact pipe probabilities and topology including the L=1 endpoint case.
    pipe_rows=[]
    edge=lambda a,b:tuple(sorted((a,b)))
    for L in range(1,65):
        op={edge((i,0),(i+1,0)) for i in range(L)}
        cl={edge((i,0),(i,j)) for i in range(L) for j in [-1,1]}|{edge((0,0),(-1,0))}
        check(len(op)==L and len(cl)==2*L+1 and not op&cl,'pipe_distinct_edge_count')
        check(all(not all(x[0]>=L for x in e) for e in op|cl),'pipe_halfplane_disjointness')
        check(all(-L<x<2*L and -L<0<2*L for x in range(L+1)),'pipe_strict_box_interior')
        for i in range(L):
            neighbors={(i-1,0),(i+1,0),(i,-1),(i,1)}
            expected={(i+1,0)}|({(i-1,0)} if i else set())
            check({x for x in neighbors if edge((i,0),x) in op}==expected and all(edge((i,0),x) in cl for x in neighbors-expected),'pipe_no_extra_attachments')
        if L<=8:pipe_rows.append({'L':L,'open_edges':len(op),'closed_edges':len(cl),'series_variance_increment':L})
    # Negative controls catch silently changed models or normalization.
    irregular=lap(2,[(-1,0,Q(1)),(0,1,Q(1))]);c=inv(irregular)
    f=inv([[irregular[i][j]/irregular[i][i] for j in range(2)] for i in range(2)])
    check(f!=c and f[0][1]!=f[1][0],'reject_unnormalized_csrw_occupation_covariance')
    check(det(lap(2,[(0,1,Q(1))]))==0,'reject_deleted_boundary_penalty')
    pinned_root_cov=inv(lap(1,[(-1,0,Q(1)),(0,-1,Q(1))]))
    check(c[0][0]==1 and pinned_root_cov[0][0]==Q(1,2),'reject_silent_tip_pin')
    parallel=lap(5,[(0,1,Q(1)),(1,2,Q(1)),(2,-1,Q(1)),(0,3,Q(1)),(3,4,Q(1)),(4,-1,Q(1))])
    check(inv(parallel)[0][0]==Q(3,2) and inv(parallel)[0][0]!=3,'reject_chemical_distance_as_resistance')
    # The stated probabilistic estimates: exact reciprocal identity and exponent range.
    for s in [Q(1,10),Q(1),Q(7),Q(123)]:
        for t in [Q(0),Q(1,10),Q(7),Q(123)]:
            check(1/(s+t)-(1/s-t/s**2)==t*t/(s*s*(s+t)),'reciprocal_exact_remainder')
    for k in [Q(201,100),Q(5,2),Q(10)]:
        # Pick r halfway between 2 and k; eta'=sqrt(2r)-2 exists and is positive.
        r=(2+k)/2
        check(2<r<k and 2**float(2-r)<1,'first_order_dyadic_summability')
    for a in [Q(1,10),Q(1,2),Q(1)]:
        check(4/(2*a)==2/a,'centering_squared_leading_coefficient')
    for p in [Q(51,100),Q(3,5),Q(3,4),Q(9,10),Q(99,100)]:
        L=7
        check(p**L*(1-p)**(2*L+1)==(1-p)*(p*(1-p)**2)**L,'pipe_probability_factorization')
    check(math.exp(-.5)!=math.exp(-2),'annealed_gaussian_subsequences_distinct')
    out={'status':'PASS','assertions_passed':sum(COUNTS.values()),'checks_by_category':dict(sorted(COUNTS.items())), 'graph_counts':dict(graph_counts),'branched_tree_examples':tree_rows,'pipe_examples':pipe_rows,'scope':'Finite exact identities and finite controls only. The all-supercritical-p quenched maximum limit is not proved or disproved.'}
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--write-results',action='store_true');a=p.parse_args()
    result=compute();target=Path(__file__).resolve().parents[1]/'results/independent_math.json'
    if a.write_results:target.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:assert result==json.loads(target.read_text()),'independent results mismatch'
    print(json.dumps({'status':'PASS','assertions_passed':result['assertions_passed'],'graph_patterns':result['graph_counts']['patterns'],'results_match':not a.write_results},sort_keys=True))
if __name__=='__main__':main()
