#!/usr/bin/env python3
"""New finite exact controls for PR1262. Not an asymptotic LLT certificate.

Standard library only. Essential checks use explicit exceptions, so -O/-OO
retain them. Output is deterministic. No historical author's code is imported.
"""
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F
from math import comb

def require(ok, label):
    if not ok:
        raise ValueError(label)

def falling(a, k):
    value = 1
    for j in range(k):
        value *= a-j
    return value

def run():
    output = {'schema':'pr1262-new-finite-exact-controls-v1',
      'scope':'Finite identities only; no verification of the imported local limit theorem or any asymptotic convergence by enumeration.',
      'graph_enumerations':[], 'conditional_variance_checks':0,
      'unconditional_moment_checks':0, 'orthogonal_expansion_checks':0,
      'overlap_counts':[], 'negative_controls':[]}
    for n in range(3, 7):
        edges = list(itertools.combinations(range(n), 2))
        N = len(edges)
        edge_index = {e:i for i,e in enumerate(edges)}
        triangles = [tuple(edge_index[e] for e in itertools.combinations(v,2))
                     for v in itertools.combinations(range(n),3)]
        adjacent = [(i,j) for i,j in itertools.combinations(range(N),2)
                    if set(edges[i]) & set(edges[j])]
        disjoint = [(i,j) for i,j in itertools.combinations(range(N),2)
                    if not set(edges[i]) & set(edges[j])]
        tri_masks = [sum(1<<i for i in t) for t in triangles]
        adj_masks = [sum(1<<i for i in pair) for pair in adjacent]
        dis_masks = [sum(1<<i for i in pair) for pair in disjoint]
        A = len(adjacent)
        require(A == N*(n-2) == 3*comb(n,3), 'wedge count')
        require(len(disjoint) == 3*comb(n,4), 'disjoint pair count')
        overlaps = [sum(len(set(w)&set(v)) == 1 for v in adjacent) for w in adjacent]
        require(all(c == 4*n-10 for c in overlaps), 'one-edge wedge overlaps')
        B = sum(overlaps)
        require(B == A*(4*n-10), 'ordered wedge overlap B')
        require(F(B)-F(4*A*A,N) == -2*A, 'leading conditional cancellation')
        output['overlap_counts'].append({'n':n,'N':N,'A':A,'B':B,
          'B_minus_4A2_over_N':str(F(B)-F(4*A*A,N))})
        # Each stratum stores [number, sum T, sum T^2, sum W, sum W^2,
        # sum Y, sum Y^2]. Enumeration uses integer bitsets independently of
        # the moment formulas under test.
        strata = defaultdict(lambda:[0]*7)
        triangle_support = set()
        disjoint_support = set()
        chosen = {0, (1<<N)-1, (1<<N)//3, (1<<N)//7}
        if tri_masks: chosen.add(tri_masks[0])
        if dis_masks: chosen.add(dis_masks[0])
        for graph in range(1<<N):
            m = graph.bit_count()
            T = sum(graph & s == s for s in tri_masks)
            W = sum(graph & s == s for s in adj_masks)
            Y = sum(graph & s == s for s in dis_masks)
            triangle_support.add(T)
            disjoint_support.add(Y)
            require(Y == comb(m,2)-W, 'edge-pair partition identity')
            row = strata[m]
            for j,value in enumerate((1,T,T*T,W,W*W,Y,Y*Y)):
                row[j] += value
            if graph in chosen:
                for p in (F(1,5),F(1,2),F(4,5)):
                    centered = [F((graph>>i)&1)-p for i in range(N)]
                    edge_sum = sum(centered)
                    wedge_sum = sum(centered[i]*centered[j] for i,j in adjacent)
                    triangle_sum = sum(centered[i]*centered[j]*centered[k] for i,j,k in triangles)
                    dis_sum = sum(centered[i]*centered[j] for i,j in disjoint)
                    require(F(T)-comb(n,3)*p**3 == p**2*(n-2)*edge_sum+p*wedge_sum+triangle_sum,
                            'pointwise triangle expansion')
                    require(F(Y)-len(disjoint)*p**2 == p*comb(n-2,2)*edge_sum+dis_sum,
                            'pointwise disjoint-pair expansion')
                    output['orthogonal_expansion_checks'] += 2
        for m,row in sorted(strata.items()):
            require(row[0] == comb(N,m), 'edge stratum size')
            # pi_4 requires N>=4; n=3 is excluded from this test only.
            if N >= 4:
                pi = {j:F(falling(m,j),falling(N,j)) for j in (2,3,4)}
                empirical = F(row[4],row[0])-F(row[3],row[0])**2
                formula = A*(pi[2]-pi[4])+B*(pi[3]-pi[4])+A*A*(pi[4]-pi[2]**2)
                require(empirical == formula, 'conditional wedge variance')
                output['conditional_variance_checks'] += 1
                if n == 4 and m == 3:
                    wrong = A*(pi[2]-pi[4])+F(4*A*A,N)*(pi[3]-pi[4])+A*A*(pi[4]-pi[2]**2)
                    require(empirical != wrong, 'negative altered B not detected')
                    output['negative_controls'].append('Replacing B by 4A^2/N is rejected in n=4, M=3; the -2A correction is necessary.')
        for p in (F(1,5),F(1,2),F(4,5)):
            raw = [sum(F(row[j])*p**m*(1-p)**(N-m) for m,row in strata.items())
                   for j in range(1,7)]
            mean_t, second_t, mean_w, second_w, mean_y, second_y = raw
            vt = second_t-mean_t**2
            vy = second_y-mean_y**2
            tri_orth = N*(n-2)**2*p**5*(1-p)+3*comb(n,3)*p**4*(1-p)**2+comb(n,3)*p**3*(1-p)**3
            tri_cov = comb(n,3)*p**3*(1-p**3)+12*comb(n,4)*p**5*(1-p)
            y_orth = N*comb(n-2,2)**2*p**3*(1-p)+3*comb(n,4)*p**2*(1-p)**2
            require(mean_t == comb(n,3)*p**3 and mean_y == 3*comb(n,4)*p**2, 'exact means')
            require(vt == tri_orth == tri_cov, 'triangle variance, two forms')
            require(vy == y_orth, 'disjoint pair variance')
            require(vt >= p**5*(1-p)*N*(n-2)**2 > 0, 'exact concentration scale')
            output['unconditional_moment_checks'] += 5
            if n == 4 and p == F(1,2):
                require(vt != comb(n,3)*p**3*(1-p**3)+6*comb(n,4)*p**5*(1-p), 'negative wrong coefficient not detected')
                output['negative_controls'].append('Triangle covariance coefficient 6 rejected against exact enumeration.')
                require(vy != 2*y_orth, 'negative disjoint doubled variance not detected')
                output['negative_controls'].append('Doubled ordinary disjoint-pair variance rejected.')
        output['graph_enumerations'].append({'n':n,'graphs':1<<N,'strata':len(strata),
          'triangle_support_contains_0_and_1':{0,1}.issubset(triangle_support),
          'disjoint_support_contains_0_and_1':{0,1}.issubset(disjoint_support)})
        require({0,1}.issubset(triangle_support), 'triangle span-one witnesses')
        if n >= 4:
            require({0,1}.issubset(disjoint_support), 'disjoint-pair span-one witnesses')
    # Exact first-order hypergeometric expansion by derivative at z=1/N=0.
    # Product (r-jz)/(1-jz), j=0..k-1, has derivative
    # -binom(k,2) r^(k-1)(1-r). Compute that derivative directly.
    expansion_checks = 0
    for r in (F(1,7),F(2,5),F(1,2),F(6,7)):
        for k in (2,3,4):
            actual = sum(F(j)*(r-1)*r**(k-1) for j in range(k))
            expected = -comb(k,2)*r**(k-1)*(1-r)
            require(actual == expected, 'first-order hypergeometric coefficient')
            expansion_checks += 1
    output['hypergeometric_first_order_checks'] = expansion_checks
    # Midpoint remainder constant is int_{-1/2}^{1/2} u^2/2 du = 1/24.
    midpoint = F(1,2)*F(2,3)*F(1,2)**3
    require(midpoint == F(1,24), 'midpoint Taylor constant')
    output['midpoint_taylor_integral_constant'] = str(midpoint)
    output['total_graphs_enumerated'] = sum(x['graphs'] for x in output['graph_enumerations'])
    output['status'] = 'PASS'
    return output

if __name__ == '__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
