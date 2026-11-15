#!/usr/bin/env python3
"""Exact finite controls of the independent derivation; stdout only.

The comparison search uses only bounded-multiple comparisons and a brute
additive oracle. This is not the quasilinear BDH implementation and cannot
prove an asymptotic running-time bound. Universal proofs are in DERIVATION.
"""
from collections import Counter, deque
from fractions import Fraction as F
from functools import cmp_to_key
from itertools import combinations, product
from math import factorial
import json

counts=Counter()
negative=[]


def graph_distances(n,edges):
    adj=[[] for _ in range(n)]
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    out=[]
    for u in range(n):
        row=[-1]*n;row[u]=0;queue=deque([u])
        while queue:
            x=queue.popleft()
            for y in adj[x]:
                if row[y]<0:row[y]=row[x]+1;queue.append(y)
        if -1 in row:return None
        out.append(row)
    return out


def median(d):
    return all(sum(all(d[u][x]+d[x][v]==d[u][v] for u,v in
                      [(a,b),(b,c),(c,a)]) for x in range(len(d)))==1
               for a,b,c in combinations(range(len(d)),3))


class Comparisons:
    def __init__(self,weights):self.w=weights;self.D=len(weights)-1
    def cmp(self,a,b):
        k,u=a;j,v=b
        if not (0<=k<=self.D and 0<=j<=self.D):
            raise ValueError('original-profile multiplier out of stated range')
        counts['bounded_original_profile_comparisons']+=1
        av,bv=k*self.w[u],j*self.w[v]
        return (av>bv)-(av<bv)


def budget_oracle(d,comparison,R):
    n=len(d);D=n-1;labels=[]
    for u in range(n):
        lo,hi=0,D+1
        while hi-lo>1:
            mid=(lo+hi)//2
            if comparison.cmp((mid,u),R)<=0:lo=mid
            else:hi=mid
        labels.append(D-lo)
    answer=[x for x in range(n) if max(d[x][u]+labels[u] for u in range(n))<=D]
    counts['brute_additive_oracle_calls']+=1
    return answer


def optimize(d,weights):
    n=len(weights);D=n-1;comparison=Comparisons(weights)
    direct=[max(weights[u]*d[x][u] for u in range(n)) for x in range(n)]
    optimum=min(direct)
    if n==1:return F(0),[0]
    max_u=0
    for u in range(1,n):
        if comparison.cmp((1,u),(1,max_u))>0:max_u=u
    B=(D,max_u);witness=0
    if comparison.cmp(B,(0,0))==0:return F(0),list(range(n))
    intervals=[[0,D] for _ in range(n)];iterations=0
    while (mass:=sum(max(0,hi-lo+1) for lo,hi in intervals)):
        mids=[(((lo+hi)//2,u),hi-lo+1) for u,(lo,hi) in enumerate(intervals) if lo<=hi]
        mids.sort(key=cmp_to_key(lambda a,b:comparison.cmp(a[0],b[0])))
        cumulative=0
        for q,L in mids:
            cumulative+=L
            if 2*cumulative>=mass:break
        assert 2*sum(L for value,L in mids if comparison.cmp(value,q)<=0)>=mass
        assert 2*sum(L for value,L in mids if comparison.cmp(value,q)>=0)>=mass
        feasible=budget_oracle(d,comparison,q)
        qvalue=q[0]*weights[q[1]]
        assert feasible==[x for x,r in enumerate(direct) if r<=qvalue]
        if feasible and comparison.cmp(q,B)<0:B=q;witness=feasible[0]
        # Delete by binary searching the first >=q or >q. No real division.
        for u,(lo,hi) in enumerate(intervals):
            left,right=lo,hi+1
            while left<right:
                mid=(left+right)//2
                cmp=comparison.cmp((mid,u),q)
                if (cmp>=0 if feasible else cmp>0):right=mid
                else:left=mid+1
            if feasible:intervals[u][1]=left-1
            else:intervals[u][0]=left
        after=sum(max(0,hi-lo+1) for lo,hi in intervals)
        assert 4*after<=3*mass
        bound=B[0]*weights[B[1]]
        assert direct[witness]<=bound
        assert bound==optimum or any(k*weights[u]==optimum
            for u,(lo,hi) in enumerate(intervals) for k in range(lo,hi+1))
        iterations+=1;counts['search_progress_invariants']+=1
    value=B[0]*weights[B[1]]
    centers=budget_oracle(d,comparison,B)
    assert value==optimum and centers==[x for x,r in enumerate(direct) if r==optimum]
    assert direct[witness]==optimum
    counts['max_iterations']=max(counts['max_iterations'],iterations)
    return value,centers


def run():
    by_n={}
    # Include nonmedian graphs as deliberate controls of the general reduction;
    # this does not pretend the fast median oracle applies to those graphs.
    palette=(F(0),F(1,7),F(2),F(9,4))
    for n in range(1,5):
        edges=list(combinations(range(n),2));connected=ismedian=0
        for bits in range(1<<len(edges)):
            d=graph_distances(n,[edge for i,edge in enumerate(edges) if bits>>i&1])
            if d is None:continue
            connected+=1;ismedian+=median(d)
            for weights in product(palette,repeat=n):
                optimize(d,weights);counts['exact_profiles']+=1
        by_n[n]={'connected_labelled_graphs':connected,'median_labelled_graphs':ismedian}

    # Exhaustive integer-index progress for all row lengths/middle positions;
    # weak-side rounding, including singleton/even intervals, is checked here.
    for lo in range(33):
        for hi in range(lo,65):
            middle=(lo+hi)//2;length=hi-lo+1
            assert 2*(middle-lo+1)>=length and 2*(hi-middle+1)>=length
            counts['exact_middle_rounding_cases']+=1

    # Exact recurrence/label bounds at every small order and large word edges.
    for s in list(range(3,4097))+[2**k+j for k in (32,64,128) for j in (-1,0,1)]:
        L=(s-1).bit_length();f=2*L
        assert (1<<(L-1))<s<=1<<L and f>=2
        for ell in (1,L):
            # Strict integer slice size below s/f.
            cap=(s-1)//f
            assert 2*ell*cap<=s and cap*f<s
        counts['exact_recursion_parameter_cases']+=1
    n=10**12;dimension=30;leaves=17_000_000_000
    zero_leaves=n-(1<<dimension)-dimension*leaves
    minority=(1<<(dimension-1))+leaves
    union=(1<<dimension)-1+dimension*leaves
    partial=sum((F(7**k,factorial(k)) for k in range(30)),F(0))
    assert partial>1000 and zero_leaves==488_926_258_176
    assert 56*minority==982_064_771_072<n
    assert 2*union==1_022_147_483_646>n
    compressed={'N':n,'cube_dimension':dimension,'leaves_at_each_unit':leaves,
      'leaves_at_zero':zero_leaves,'minority':minority,'minority_times_56':56*minority,
      'minority_union':union,'duplicated_slice_volume':2*union,
      'exp7_Taylor_partial_sum_terms':30,'exp7_partial_gt_1000_exact':True,
      'natural_log_volume_estimate_refuted':True,'corrected_algorithm_refuted':False}

    # Large-bit rational and boundary cases with exact expected complete output.
    path=graph_distances(4,[(0,1),(1,2),(2,3)])
    for weights in [(F(0),)*4,(F(0),F(2**512+1),F(0),F(0)),
                    (F(1,2**512+1),F(0),F(2**512+1),F(0)),(F(1),)*4]:
        optimize(path,weights);counts['large_bit_and_boundary_profiles']+=1
    comparison=Comparisons((F(1),F(2)))
    try:comparison.cmp((2,0),(1,1))
    except ValueError:negative.append('out-of-range real multiplier rejected')
    else:raise AssertionError('multiplier guard not effective')

    # Dropping the original-weight slice call fails even on an unbalanced star.
    n=17;omega=[0]*n;omega[1]=100
    star=graph_distances(n,[(0,u) for u in range(1,n)])
    f=2*(n-1).bit_length();assert f<n
    original=omega[1];open_fiber=max(star[1][u]+omega[u] for u in range(n) if u!=1)
    assert original==100 and open_fiber==2 and original>open_fiber
    negative.append('fiber reweight does not dominate original slice weight')
    # Directly replacing multiplicative weights by additive arrivals changes centers.
    d=graph_distances(6,[(u,u+1) for u in range(5)])
    w=[F(1),F(0),F(0),F(0),F(0),F(3)]
    multiplicative=[max(w[u]*row[u] for u in range(6)) for row in d]
    additive=[max(w[u]+row[u] for u in range(6)) for row in d]
    cm=[x for x,v in enumerate(multiplicative) if v==min(multiplicative)]
    ca=[x for x,v in enumerate(additive) if v==min(additive)]
    assert cm!=ca;negative.append('untransformed additive objective has different centers')

    result={'verdict':'PASS','exact_counts':dict(counts),'graph_inventory':by_n,
      'compressed_exact_countermodel':compressed,'negative_controls':negative,
      'untransformed_objective_control':{'multiplicative_centers':cm,'additive_centers':ca},
      'limitations':['Brute additive oracle is a reference, not BDH fast implementation.',
        'Finite enumeration does not prove the universal theorem or asymptotic bound.',
        'Universal threshold/search/recursion/bit proofs and actual primary imports are recorded separately.'],
      'source_imports':[],'writes':[]}
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
