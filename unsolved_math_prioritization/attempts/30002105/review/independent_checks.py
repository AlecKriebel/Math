#!/usr/bin/env python3
"""Independent exact diagnostics for the scoped kNN identifiability theorem.

Standard library only. No author checker or external software is imported.
The all-sample smooth-density claim is an analytic theorem, not an inference
from these finite controls.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json

counts = Counter()
def check(value, category):
    assert value, category
    counts[category] += 1

def squared(a, b):
    return sum((x-y)**2 for x, y in zip(a, b))

def arcs(points, k):
    result = set()
    for i, x in enumerate(points):
        ranked = sorted((squared(x, y), j) for j, y in enumerate(points) if i != j)
        result.update((i, j) for _, j in ranked[:k])
    return result

def union_edges(directed):
    return {tuple(sorted(e)) for e in directed}

def mutual_edges(directed):
    return {tuple(sorted((i,j))) for i,j in directed if (j,i) in directed}

# Rebuild the finite example from integer coordinates, with explicit sorted
# distances. A common positive scale is immaterial.
X = [(x,) for x in (0, 10, 19, 41)]
Y = [(x,) for x in (0, 10, 21, 38)]
DX, DY = arcs(X, 2), arcs(Y, 2)
check(DX != DY, 'finite_direction_ambiguity')
check(DX ^ DY == {(2,0),(2,3)}, 'exact_changed_arcs')
expected = {(i,j) for i in range(4) for j in range(i+1,4)} - {(0,3)}
check(union_edges(DX) == union_edges(DY) == expected, 'same_union_graph')
for points in (X,Y):
    for i,x in enumerate(points):
        ds = sorted(squared(x,y) for j,y in enumerate(points) if i != j)
        check(all(a < b for a,b in zip(ds,ds[1:])), 'strict_distance_orders')
adj = [{j for j in range(4) if tuple(sorted((i,j))) in expected} for i in range(4)]
check([len(adj[2]&adj[j]) for j in (0,1,3)] == [1,2,1], 'common_neighbor_counts')

# All binary component assignments on deterministic interleaved clouds.
# Ties in these finite diagnostics are resolved by the same label rule in
# each model. The continuous densities have distance ties with probability 0.
cloud_cases = graph_cases = 0
for n in range(4,9):
    for d in (1,2,3):
        latent = [tuple(Q((i+1)**(j+1) % 97 - 48, 100*d)
                        for j in range(d)) for i in range(n)]
        check(len(set(latent)) == n, 'distinct_latent_cloud')
        check(all(squared(u,(0,)*d)<1 for u in latent), 'latent_unit_ball')
        for s in (Q(5,4), Q(2), Q(7,2)):
            L=10*s
            check(L-1-s > 2*s, 'uniform_cross_distance_margin')
            for labels in product((0,1),repeat=n):
                n1=sum(labels)
                if min(n1,n-n1)<2:
                    continue
                left=[]; right=[]
                for u,z in zip(latent,labels):
                    left.append(tuple(u[j]+(L*z if j==0 else 0) for j in range(d)))
                    right.append(tuple(s**z*u[j]+(L*z if j==0 else 0) for j in range(d)))
                cloud_cases+=1
                for i in range(n):
                    for j in range(i):
                        if labels[i]==labels[j]:
                            check(squared(right[i],right[j]) ==
                                  s**(2*labels[i])*squared(left[i],left[j]),
                                  'all_within_pair_scale')
                        else:
                            check(min(squared(left[i],left[j]),squared(right[i],right[j]))
                                  > (2*s)**2,'all_cross_pairs_separated')
                for k in range(1,min(n1,n-n1)):
                    B,C=arcs(left,k),arcs(right,k)
                    graph_cases+=1
                    check(B==C,'all_admissible_k_directed_equality')
                    check(union_edges(B)==union_edges(C),'union_observation_equality')
                    check(mutual_edges(B)==mutual_edges(C),'mutual_observation_equality')
                    check(all(labels[i]==labels[j] for i,j in B),'no_cross_arcs')

# Exact binomial tails and a rational Chernoff estimate independent of the
# submitted choice of transform. Hoeffding's exponential estimate is proved
# in the report; these control its probabilistic setup without float logs.
for n in range(4,81):
    for k in range(1,(n+1)//2):
        tail=sum(comb(n,j) for j in range(k+1))
        failure=Q(2*tail,2**n)
        success=Q(sum(comb(n,j) for j in range(k+1,n-k)),2**n)
        check(failure+success==1,'exact_two_component_event_probability')
        z=Q(k,n-k)
        mgf=((1+z)/2)**n
        check(Q(tail,2**n)<=mgf/z**k,'independent_rational_chernoff_bound')
        # Fixed labels 0,1 for the random density target. Do not assume that
        # these labels are independent of the occupancy event.
        mass2=Q(sum(comb(n-2,j-1) for j in range(k+1,n-k)),2**n)
        check(mass2>=Q(1,4)-failure,'fixed_two_labels_intersection_bound')
        mass4=Q(sum(comb(n-4,j-2) for j in range(k+1,n-k)
                    if 0<=j-2<=n-4),2**n)
        check(mass4>=Q(1,16)-failure,'fixed_four_labels_intersection_bound')

# Both affine maps have the stated Jacobian and retain component mass 1/2.
for d in range(1,8):
    for s in (Q(9,8),Q(3,2),Q(2),Q(11,3)):
        check(Q(1,2)/s**d*s**d == Q(1,2), 'density_normalization_jacobian')
        for a,b in product((Q(1,9),Q(2,7),Q(3,5)),repeat=2):
            rp=a/b
            rq=(a/2)/(b/(2*s**d))
            check(rq==s**d*rp,'density_target_scaling')
            lo,hi=min(a,b),max(a,b)
            delta=(s**d-1)*lo/hi
            check(rq-rp>=delta>0,'density_target_uniform_gap')
            # Any two intervals of radius delta/3 about the targets are
            # disjoint, including their endpoints.
            check(rp+delta/3 < rq-delta/3,'disjoint_success_intervals')

# Exact geometric event and ratio-gap checks; all endpoint combinations
# lie in the closed balls used for the positive-probability event in d=1.
for left,right in product((Q(-5,8),Q(-1,2),Q(-3,8)),
                          (Q(3,8),Q(1,2),Q(5,8))):
    check(Q(3,4)<=right-left<=Q(5,4),'event_pair_distance_bounds')
for a,b,s in product((Q(3,4),Q(1),Q(5,4)),
                      (Q(3,4),Q(1),Q(5,4)),(Q(5,4),Q(2),Q(7,2))):
    t=a/b
    check(t>=Q(3,5),'event_ratio_lower_bound')
    check(t-t/s>=(1-1/s)*Q(3,5)>0,'geometry_target_uniform_gap')

result={'status':'PASS','assertions':sum(counts.values()),
        'categories':dict(sorted(counts.items())),
        'interleaved_component_clouds':cloud_cases,
        'labelled_graph_pairs':graph_cases,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'Exact finite diagnostics only; the fixed smooth-law and all-n statistical conclusions are audited analytically in REVIEW.md.'}
print(json.dumps(result,indent=2,sort_keys=True))
