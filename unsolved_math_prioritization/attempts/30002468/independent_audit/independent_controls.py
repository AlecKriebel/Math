#!/usr/bin/env python3
"""Independent exact definition controls; never an asymptotic proof.
Uses adjacency traversal rather than the candidate's split enumeration for
induced bicliques; exact edge-mask dynamic programming computes bp/cover.
No candidate code is imported. Only Python's standard library is required.
"""
import json
from collections import deque
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import comb


def induced_split(vertices, edges):
    vs = frozenset(vertices)
    if len(vs) < 2:
        return None
    adjacency = {v: set() for v in vs}
    for a, b in edges:
        if a in vs and b in vs:
            adjacency[a].add(b)
            adjacency[b].add(a)
    color = {min(vs): 0}
    queue = deque(color)
    while queue:
        a = queue.popleft()
        for b in adjacency[a]:
            if b not in color:
                color[b] = 1-color[a]
                queue.append(b)
            elif color[a] == color[b]:
                return None
    if len(color) != len(vs):
        return None
    left = frozenset(v for v in vs if color[v] == 0)
    right = vs-left
    if not right or any(adjacency[v] != (right if v in left else left) for v in vs):
        return None
    return (left, right)


def all_biclique_masks(n, edge_order, graphmask):
    out = set()
    # 0: outside, 1: left, 2: right. These pieces need NOT be induced.
    for assignment in product(range(3), repeat=n):
        if 1 not in assignment or 2 not in assignment:
            continue
        mask = sum(1 << i for i, (a,b) in enumerate(edge_order)
                   if {assignment[a],assignment[b]} == {1,2})
        if mask & graphmask == mask:
            out.add(mask)
    return tuple(sorted(out))


def exact_partition_number(graphmask, pieces):
    @lru_cache(None)
    def solve(remaining):
        if not remaining:
            return 0
        first = remaining & -remaining
        return 1 + min(solve(remaining ^ b) for b in pieces
                       if b & first and (b & remaining) == b)
    return solve(graphmask)


def exact_cover_number(graphmask, pieces):
    @lru_cache(None)
    def solve(remaining):
        if not remaining:
            return 0
        first = remaining & -remaining
        return 1 + min(solve(remaining & ~b) for b in pieces if b & first)
    return solve(graphmask)


def main():
    results=[]
    graph_checks=0
    hereditary_checks=0
    star_construction_checks=0
    bound_checks=0
    for n in range(0,6):
        order=list(combinations(range(n),2))
        graphs=1 << len(order)
        counts={k:0 for k in range(2,n+1)}
        empty_side_counts={k:0 for k in range(2,n+1)}
        beta_histogram={}
        partition_histogram={}
        equality_count=0
        strict_count=0
        for mask in range(graphs):
            graph_checks += 1
            edges=frozenset(e for i,e in enumerate(order) if mask >> i & 1)
            induced=[]
            for k in counts:
                for vs in combinations(range(n),k):
                    if induced_split(vs,edges) is not None:
                        counts[k]+=1
                        induced.append(vs)
                    if induced_split(vs,edges) is not None or all(
                            not set(e)<=set(vs) for e in edges):
                        empty_side_counts[k]+=1
            largest=max(induced,key=len,default=())
            beta=len(largest)
            for vs in induced:
                for k in range(2,len(vs)+1):
                    assert any(induced_split(ss,edges) is not None
                               for ss in combinations(vs,k))
                    hereditary_checks += 1
            pieces=all_biclique_masks(n,order,mask)
            bp=exact_partition_number(mask,pieces)
            assert bp <= n-beta+1
            alpha=max(len(vs) for k in range(n+1)
                      for vs in combinations(range(n),k)
                      if all(not set(e)<=set(vs) for e in edges))
            assert bp <= n-max(beta,alpha)+1
            bound_checks += 1
            # Independently construct the one-biclique-plus-outside-stars bound.
            unassigned=set(edges)
            partition=[]
            if largest:
                s=set(largest)
                b={e for e in unassigned if set(e) <= s}
                partition.append(b)
                unassigned-=b
            for v in sorted(set(range(n))-set(largest)):
                star={e for e in unassigned if v in e}
                if star:
                    partition.append(star)
                    unassigned-=star
            assert not unassigned
            assert set().union(*partition) == set(edges)
            assert sum(map(len,partition)) == len(edges)
            assert len(partition) <= n-beta+1
            star_construction_checks += 1
            beta_histogram[str(beta)]=beta_histogram.get(str(beta),0)+1
            partition_histogram[str(bp)]=partition_histogram.get(str(bp),0)+1
            equality_count += bp == n-beta+1
            strict_count += bp < n-beta+1
        countchecks=[]
        for k,total in counts.items():
            expected=Fraction(comb(n,k)*(2**(k-1)-1),2**comb(k,2))
            observed=Fraction(total,graphs)
            assert observed == expected
            expected_empty=Fraction(comb(n,k)*2**(k-1),2**comb(k,2))
            assert Fraction(empty_side_counts[k],graphs) == expected_empty
            countchecks.append({'k':k,'induced_subset_total':total,
                                'expectation':str(expected),
                                'empty_sides_allowed_subset_total':empty_side_counts[k],
                                'empty_sides_allowed_expectation':str(expected_empty)})
        results.append({'n':n,'graph_count':graphs,'counts':countchecks,
                        'beta_histogram':beta_histogram,
                        'bp_histogram':partition_histogram,
                        'finite_equality_count':equality_count,
                        'finite_strict_inequality_count':strict_count})
    negatives=[]
    # Triangle has no induced K_1,2 despite a complete-bipartite subgraph.
    k4=frozenset(combinations(range(4),2))
    assert induced_split(range(4),k4) is None
    assert max(len(vs) for k in range(2,5) for vs in combinations(range(4),k)
               if induced_split(vs,k4)) == 2
    negatives.append({'name':'ordinary_biclique_is_not_induced',
                      'graph':'K4','maximum_ordinary_order':4,'induced_beta':2})
    order=list(combinations(range(4),2))
    pieces=all_biclique_masks(4,order,63)
    bp=exact_partition_number(63,pieces)
    cover=exact_cover_number(63,pieces)
    assert (bp,cover)==(3,2)
    negatives.append({'name':'cover_number_is_not_partition_number',
                      'graph':'K4','bp':bp,'cover':cover})
    star=frozenset((0,v) for v in range(1,5))
    assert induced_split(range(5),star)
    alpha=max(len(vs) for k in range(6) for vs in combinations(range(5),k)
              if all(not set(e)<=set(vs) for e in star))
    assert alpha==4
    negatives.append({'name':'alpha_is_not_beta_and_unbalanced_parts_are_required',
                      'graph':'K1,4','alpha':4,'beta':5})
    p=Fraction(1,3)
    star_probability=p**3*(1-p)**3
    balanced_probability=p**4*(1-p)**2
    assert star_probability != balanced_probability
    negatives.append({'name':'equal_pattern_probabilities_require_half',
                      'p':str(p),'K1,3_probability':str(star_probability),
                      'K2,2_probability':str(balanced_probability)})
    assert induced_split(range(5),frozenset()) is None
    negatives.append({'name':'empty_sides_can_change_finite_beta',
                      'graph':'edgeless graph on five vertices',
                      'nonempty_beta':0,'empty_sides_allowed_beta':5,
                      'same_asymptotic_upper_bound':True})
    # Rounding/exponent arithmetic is exact at n=2^L and rational epsilon.
    rounding_checks=0
    for L in range(1,81):
        for eps in (Fraction(1,100),Fraction(1,3),Fraction(1),Fraction(5,2)):
            threshold=(2+eps)*L
            k=-(-threshold.numerator//threshold.denominator)
            assert k-1 < threshold <= k
            exponent=Fraction(k)*(L+Fraction(3,2)-Fraction(k,2))
            assert exponent <= k*(Fraction(3,2)-eps*L/2)
            if eps*L >= 6:
                assert exponent <= -eps*(2+eps)*L*L/4
            rounding_checks += 1
    return {'status':'PASS','scope':'finite exact controls only; no random-graph limit is inferred',
            'candidate_code_imported':False,'graphs_checked':graph_checks,
            'induced_hereditary_checks':hereditary_checks,
            'deterministic_bound_checks':bound_checks,
            'star_partition_construction_checks':star_construction_checks,
            'exact_rounding_checks':rounding_checks,
            'graph_results':results,'negative_controls':negatives}

if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
