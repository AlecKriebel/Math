#!/usr/bin/env python3
"""Exact arithmetic checks. Not a formal certificate for geometric hypotheses."""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from functools import reduce
from math import gcd
import json

COUNTS = {}
NEGATIVE_CONTROLS = []

def check(condition, family):
    if not condition:
        raise RuntimeError('Check failed: ' + family)
    COUNTS[family] = COUNTS.get(family, 0) + 1

def reject(name, false_claim):
    if false_claim:
        raise RuntimeError('False shortcut was not rejected: ' + name)
    NEGATIVE_CONTROLS.append(name)

def det(matrix):
    a = [[Q(x) for x in row] for row in matrix]
    n = len(a)
    out = Q(1)
    for i in range(n):
        p = next((p for p in range(i, n) if a[p][i]), None)
        if p is None:
            return Q(0)
        if p != i:
            a[i], a[p] = a[p], a[i]
            out = -out
        pivot = a[i][i]
        out *= pivot
        for j in range(i + 1, n):
            ratio = a[j][i] / pivot
            for k in range(i + 1, n):
                a[j][k] -= ratio * a[i][k]
    return out

def graph_value(A, edges):
    A = list(map(Q, A))
    degree = [0] * len(A)
    for i, j in edges:
        degree[i] += 1
        degree[j] += 1
    return sum((Q(2 - degree[i], 1) / A[i] for i in range(len(A))), Q(0)) + sum((Q(1)/(A[i]*A[j]) for i, j in edges), Q(0))

def partial(A, edges, i):
    neighbors = [b if a == i else a for a, b in edges if a == i or b == i]
    return -(2-len(neighbors)+sum((Q(1)/A[j] for j in neighbors), Q(0)))/A[i]**2

def open_value(strata, A):
    total = Q(0)
    for J, e in strata.items():
        total += Q(e) * reduce(lambda x, j: x/Q(A[j]), J, Q(1))
    return total

def closed_to_open(closed, n):
    out = {}
    for mask in range(1 << n):
        out[tuple(i for i in range(n) if mask & (1 << i))] = sum((Q(value)*((-1)**((sup ^ mask).bit_count())) for sup, value in closed.items() if sup & mask == mask), Q(0))
    return out

def closed_value(closed, A):
    return sum((Q(e)*reduce(lambda x, i:x*(Q(1)/A[i]-1), (i for i in range(len(A)) if mask & (1 << i)), Q(1)) for mask,e in closed.items()),Q(0))

def run():
    COUNTS.clear()
    NEGATIVE_CONTROLS.clear()
    # Inclusion-exclusion is checked for formal closed-stratum values.
    for n in range(1, 6):
        closed = {mask: Q(7 + 3 * mask) for mask in range(1 << n)}
        strata = closed_to_open(closed, n)
        for shift in range(1, 6):
            A = [Q(i + shift, i + 1) for i in range(n)]
            check(open_value(strata, A) == closed_value(closed, A), 'inclusion_exclusion')
    # Smooth blowup and one smooth exceptional divisor formulas.
    for codim in range(2, 10):
        for center_e in (1, 2, 5, 17):
            e_x = 100 + (codim - 1) * center_e
            e_exc = codim * center_e
            a = Q(codim - 1)
            e_target = Q(e_x) - a/(a+1)*e_exc
            check(e_target == 100 and e_x-e_target > 0, 'smooth_blowups')
    for a in (Q(1,7), Q(1,2), Q(1), Q(3), Q(21,2)):
        for E in (2, 3, 7, 20):
            check(Q(1)*E-Q(E)/(a+1) == a*E/(a+1) > 0, 'smooth_exceptional_formula')
    # Primitive toric weighted blowups of a fixed point of P^n.
    toric_count = 0
    for n in range(2, 5):
        for weights in product(range(1, 6), repeat=n):
            if reduce(gcd, weights) != 1:
                continue
            contributions=[]
            for i in range(n):
                matrix=[[int(r == c) for c in range(n)] for r in range(n)]
                for r in range(n):
                    matrix[r][i] = weights[r]
                contributions.append(abs(det(matrix)))
            check(contributions == list(weights), 'toric_determinants')
            check(sum(contributions)-1 == sum(weights)-1 > 0, 'toric_strict_decrease')
            toric_count += 1
    # Canonical-surface arithmetic after the geometric reduction.
    for rho in range(1, 11):
        for k in range(1, 13):
            check((2+rho+k)-(2+rho) == k > 0, 'canonical_surface_blowup_counts')
    # Actual common-resolution configuration for the ordinary P2 point blowup.
    resolution_values=[]
    for m in range(21):
        edges=[(0,i) for i in range(1,m+1)]
        A=[Q(1)]+[Q(2)]*m
        B=[Q(2)]+[Q(3)]*m
        delta=graph_value(A,edges)-graph_value(B,edges)
        check(delta == 1, 'actual_resolution_cancellation')
        resolution_values.append(str(delta))
    # Derivative criterion: all target entries <=1, including branching graphs.
    graph_cases=0
    for n in range(1, 9):
        graphs = [[(i,i+1) for i in range(n-1)]]
        if n >= 3:
            graphs.append([(0,i) for i in range(1,n)])
        for edges in graphs:
            for t in range(1, 9):
                A=[Q(1,2+(i+t)%5) for i in range(n)]
                B=[(a+1)/2 for a in A]
                check(graph_value(A,edges)>graph_value(B,edges),'surface_unit_cube_decrease')
                for i in range(n):
                    check(partial(B,edges,i) <= -Q(2)/B[i]**2,'surface_unit_cube_derivative')
                graph_cases += 1
    # Chain criterion at discrepancies not bounded by 1.
    for n in range(1, 10):
        edges=[(i,i+1) for i in range(n-1)]
        A=[Q(i+1,2) for i in range(n)]
        B=[a+Q(i+1,3) for i,a in enumerate(A)]
        check(graph_value(A,edges)>graph_value(B,edges),'surface_chain_decrease')
    # Finite numerical star search: center weight 1..5, 0..4 one-vertex arms,
    # arm weights 2..8, sorted to remove relabelings. No realization asserted.
    attempted=eligible=bound_exceeding=0
    minimum=None
    sample=None
    for m in range(5):
        edges=[(0,i) for i in range(1,m+1)]
        for arms in combinations_with_replacement(range(2,9),m):
            for b0 in range(1,6):
                attempted += 1
                s=sum((Q(1,b) for b in arms),Q(0))
                if b0 <= s:
                    continue
                delta=2-m-b0+2*s
                if delta <= 0:
                    continue
                A=[Q(1)]+[Q(2,b) for b in arms]
                B0=Q(2-m+s,b0-s)
                B=[B0]+[(1+B0)/b for b in arms]
                check(all(a>0 and b>=a for a,b in zip(A,B)) and B[0]>A[0],'star_discrepancy_constraints')
                # Check M B = (2-degree_i) directly, including center.
                check(b0*B0-sum(B[1:])==2-m and all(b*B[i+1]-B0==1 for i,b in enumerate(arms)),'star_adjunction')
                gap=graph_value(A,edges)-graph_value(B,edges)
                check(gap>0,'star_numerical_decrease')
                eligible+=1
                if max(B)>1:
                    bound_exceeding+=1
                if minimum is None or gap<minimum:
                    minimum=gap
                    sample={'center':b0,'arms':list(arms),'A':list(map(str,A)),'B':list(map(str,B)),'gap':str(gap)}
    # False-shortcut controls. Each asserts that a tempting universal assertion fails.
    reject('open_algebraic_Euler_always_nonnegative',2-3>=0)
    star_edges=[(0,i) for i in (1,2,3)]
    formal_delta=graph_value([Q(1),Q(10),Q(10),Q(10)],star_edges)-graph_value([Q(2),Q(10),Q(10),Q(10)],star_edges)
    check(formal_delta==Q(-7,20),'formal_negative_countermodel')
    reject('discrepancy_order_alone_forces_positive_sum',formal_delta>0)
    reject('algebraic_equals_topological_for_all_curves',2==2-2*2)
    reject('positive_projective_factors_can_have_zero_algebraic_Euler',2==0)
    reject('codimension_one_blowup_strictly_decreases',(1-1)*2>0)
    reject('crepant_smooth_divisor_forces_strict_drop',Q(0,1)*2>0)
    # Exact local star controls: primitive rays and primitive inserted vector.
    v1,v2,v=(1,0),(1,2),(1,1)
    original=abs(det([[v1[0],v2[0]],[v1[1],v2[1]]]))
    refined=abs(det([[v1[0],v[0]],[v1[1],v[1]]]))+abs(det([[v[0],v2[0]],[v[1],v2[1]]]))
    check(original==refined==2,'crepant_toric_equality')
    reject('every_nontrivial_toric_subdivision_has_positive_drop',refined-original>0)
    v1,v2,v=(1,2),(2,1),(1,1)
    original=abs(det([[v1[0],v2[0]],[v1[1],v2[1]]]))
    refined=abs(det([[v1[0],v[0]],[v1[1],v[1]]]))+abs(det([[v[0],v2[0]],[v[1],v2[1]]]))
    check((original,refined)==(3,2),'non_mori_toric_reversal')
    reject('toric_sign_without_K_negative_assumption',refined-original>0)
    reject('all_common_surface_resolution_log_discrepancies_at_most_one',Q(2)<=1)
    reject('surface_derivative_negative_on_entire_positive_orthant',partial([Q(1),Q(10),Q(10),Q(10)],star_edges,0)<0)
    return {
        'problem_id':'30003230',
        'general_result':'unresolved',
        'formal_proof_certificate':False,
        'checks':dict(sorted(COUNTS.items())),
        'total_exact_checks':sum(COUNTS.values()),
        'negative_controls_rejected':NEGATIVE_CONTROLS,
        'negative_control_count':len(NEGATIVE_CONTROLS),
        'toric_family':{'dimensions':[2,3,4],'weight_values':[1,2,3,4,5],'primitive_tuples':toric_count},
        'surface_graph_cases':graph_cases,
        'star_search':{'attempted':attempted,'numerically_eligible':eligible,'eligible_with_target_discrepancy_above_one':bound_exceeding,'minimum_gap':str(minimum),'minimizer_sample':sample,'geometric_realization_claim':False},
        'real_common_resolution_gap_for_m_0_through_20':resolution_values,
        'formal_non_geometric_countermodel_gap':str(formal_delta),
        'limitations':['No universal geometric proof from finite arithmetic checks.','Formal discrepancy arrays are not geometric counterexamples.','Surface graph search does not certify algebraization or projectivity.','No unrestricted prior-result or current-openness certification.']
    }

if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
