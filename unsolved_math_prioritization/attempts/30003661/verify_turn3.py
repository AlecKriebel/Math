#!/usr/bin/env python3
"""Exact finite-history interval coding controls; not an infinite WKL test."""
from fractions import Fraction as F
from itertools import combinations
from math import factorial
from collections import Counter
from bisect import bisect_right
import json
C=Counter()
def ck(g,v):
    if not v:raise AssertionError(g)
    C[g]+=1
total_nodes=0;max_mesh=0
for n in range(1,6):
    nodes={};labels={}
    def build(h,S,l,r):
        ck('positive_interval',l<r)
        nodes[h]=(S,l,r)
        for x in (l,r):
            ck('distinct_mesh_endpoints',x not in labels)
            labels[x]=min(S)
        k=len(S)
        if k==1:return
        children=[]
        for j,i in enumerate(sorted(S)):
            ll=l+(r-l)*F(3*j+1,3*k+1);rr=l+(r-l)*F(3*j+2,3*k+1)
            ck('strict_child_nesting',l<ll<rr<r)
            ck('exact_child_length',rr-ll==(r-l)/F(3*k+1))
            children.append((ll,rr));build(h+(i,),S-{i},ll,rr)
        for (a,b),(c,d) in combinations(children,2):ck('sibling_positive_separation',b<c or d<a)
    build((),frozenset(range(n)),F(0),F(1))
    mesh=sorted(labels);total_nodes+=len(nodes);max_mesh=max(max_mesh,len(mesh))
    ck('complete_history_count',len(nodes)==sum(factorial(n)//factorial(n-d) for d in range(n)))
    ck('leaf_count',sum(len(S)==1 for S,l,r in nodes.values())==factorial(n))
    lower=F(1)
    for k in range(2,n+1):lower/=3*k+1
    def weights(x):
        out=[F(0)]*n
        if x in labels:out[labels[x]]=1;return out
        j=bisect_right(mesh,x)-1;a,b=mesh[j],mesh[j+1]
        lam=(x-a)/(b-a);out[labels[a]]+=1-lam;out[labels[b]]+=lam
        return out
    for h,(S,l,r) in nodes.items():
        ck('history_survivors_exact',S==frozenset(range(n))-set(h))
        ck('positive_uniform_length_bound',r-l>=lower)
        local=[x for x in mesh if l<=x<=r]
        ck('all_local_mesh_labels_allowed',all(labels[x] in S for x in local))
        points=local+[(a+b)/2 for a,b in zip(local,local[1:])]
        for x in points:
            w=weights(x)
            ck('simplex_weights',all(v>=0 for v in w) and sum(w)==1)
            ck('all_positive_decoder_labels_allowed',all(i in S for i,v in enumerate(w) if v>0))
        for i in S:
            if len(S)>1:
                child=nodes[h+(i,)]
                ck('one_exclusion_removes_exact_label',child[0]==S-{i})
                ck('negative_output_nested',l<=child[1]<=child[2]<=r)
    if n>=3:
        h1=(0,1);h2=(1,0);S1,l1,r1=nodes[h1];S2,l2,r2=nodes[h2]
        ck('same_set_different_names',S1==S2)
        ck('actual_nonextensional_targets',r1<l2 or r2<l1)
print(json.dumps({'problem_id':30003661,'turn':3,'status':'PASS','counts':dict(sorted(C.items())),
    'exact_assertions':sum(C.values()),'history_nodes_tested':total_nodes,'largest_finite_mesh':max_mesh,
    'arithmetic':'exact rational arithmetic only','scope':'All finite histories for n<=5 audit a proof valid for each finite n. This is not an infinite coding, a reduction of WKL, or a test of arbitrary finite sets with unknown point locations.'},indent=2,sort_keys=True))
