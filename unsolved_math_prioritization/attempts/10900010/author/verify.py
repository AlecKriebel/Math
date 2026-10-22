#!/usr/bin/env python3
"""Exact controls for the authored partial results, not a 3-manifold decision tool.

Uses only the Python standard library. No network, corpus, or scholarly files.
Outputs deterministic JSON. Each negative control attacks a specific invalid
inference; none is advertised as a counterexample to Agol's question.
"""
from fractions import Fraction as Q
from itertools import permutations
import json
import sys


def require(value, message):
    if not value:
        raise AssertionError(message)


def chiminus(genera):
    return sum(max(0, 2*g-2) for g in genera)


def rank(matrix):
    a = [[Q(x) for x in row] for row in matrix]
    rows, cols = len(a), len(a[0]) if a else 0
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if a[i][c]), None)
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        val = a[r][c]
        a[r] = [x/val for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c]:
                val = a[i][c]
                a[i] = [x-val*y for x,y in zip(a[i],a[r])]
        r += 1
    return r


def compose(a,b):
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(a):
    return tuple(a.index(i) for i in range(len(a)))


def symplectic(g):
    m = [[0]*(2*g) for _ in range(2*g)]
    for i in range(g):
        m[2*i][2*i+1] = 1
        m[2*i+1][2*i] = -1
    return m


def main():
    results = []
    # 1. Actual PL height function in the product-manifold example.
    nodes = [(Q(0),Q(0)), (Q(1,3),Q(1)), (Q(2,3),Q(0)), (Q(1),Q(1))]
    roots, signs = [], []
    for (x0,y0),(x1,y1) in zip(nodes,nodes[1:]):
        slope = (y1-y0)/(x1-x0)
        root = x0+(Q(1,2)-y0)/slope
        require(x0 < root < x1, 'Regular root must be interior')
        roots.append(root)
        signs.append(1 if slope>0 else -1)
    require(roots == [Q(1,6),Q(1,2),Q(5,6)], 'Exact PL roots')
    require(signs == [1,-1,1] and sum(signs)==1, 'Oriented fiber class')
    require(sum([1,1,1]) != 1, 'Lost-sign mutant must fail the class test')
    costs = [{'g':g, 'one_slice':chiminus([g]), 'three_slices':chiminus([g,g,g])}
             for g in range(2,9)]
    require(all(row['three_slices']==3*row['one_slice']>row['one_slice'] for row in costs),
            'Essential three-slice representative is not norm-minimizing')
    results.append({'name':'PL dual surface and orientation negative control',
                    'roots':list(map(str,roots)), 'signs':signs, 'costs':costs, 'pass':True})

    # 2. Finite algebraic checks behind the cup-pairing argument.
    # The all-genus theorem itself is proved in prose, not inferred from this sweep.
    ranks = []
    for g in range(1,9):
        j = symplectic(g)
        require(rank(j)==2*g, 'Nondegenerate cup pairing')
        for d in [-3,-1,1,2]:
            require(rank([[d*x for x in row] for row in j])==2*g,
                    'Nonzero degree preserves pairing rank')
        require(rank([[0*x for x in row] for row in j])==0, 'Degree-zero mutant')
        ranks.append({'g':g,'rank':rank(j)})
    require(sum([2,-1])==1 and 1 not in [2,-1],
            'Total degree one does not require a degree-one component')
    results.append({'name':'Cup-pairing rank and disconnected-degree control',
                    'ranks':ranks,'degrees_with_total_one':[2,-1], 'pass':True})

    # 3. Dihedral example, t -> s*t+2*n, s in {1,-1}.
    # Equality with t=1/2 requires n=(1-s)/4; test integrality exactly.
    t = Q(1,2)
    solutions=[]
    for s in [-1,1]:
        n=(t-s*t)/2
        if n.denominator==1:
            solutions.append({'sign':s,'n':int(n)})
    require(solutions==[{'sign':1,'n':0}], 'Only identity fixes selected height')
    def act(s,n,x): return s*x+2*n
    for x in [Q(-7,3),Q(0),Q(1,2),Q(17,5)]:
        require(act(-1,0,act(-1,0,x))==x, 'r squared')
        require(act(-1,0,act(1,1,act(-1,0,x)))==act(1,-1,x), 'rar=a inverse')
    strict = [{'g':g,'upstairs_norm':2*g-2,'pushforward_norm':0} for g in range(2,9)]
    require(all(a['upstairs_norm']>a['pushforward_norm'] for a in strict), 'Strict lower bound')
    results.append({'name':'Dihedral descending-slice control',
                    'height':str(t),'stabilizing_height_solutions':solutions,
                    'strict_norm_gap_for_pushforward_only':strict,'pass':True})

    # 4. Nonnormal subgroup model. H acts by left multiplication on G.
    G=set(permutations(range(3)))
    I=(0,1,2); trans=(1,0,2); cycle=(1,2,0)
    H={I,trans}
    normalizer={g for g in G if {compose(compose(g,h),inverse(g)) for h in H}==H}
    require(normalizer==H, 'S3 subgroup must have trivial quotient deck group')
    good=set(H)
    bad=set(H)|{compose(h,cycle) for h in H}
    require(all({compose(h,x) for x in bad}==bad for h in H), 'H-invariance')
    def collisions(U, candidates):
        return sorted(g for g in candidates if U & {compose(g,x) for x in U})
    require(not collisions(good,G-H), 'Single coset passes full descent test')
    full_bad=collisions(bad,G-H)
    require(bool(full_bad), 'Multiple cosets fail full descent test')
    require(not collisions(bad,normalizer-H), 'Deck-only mutant misses collisions')
    results.append({'name':'Nonnormal-cover full-coset negative control',
                    'group_order':len(G),'subgroup_order':len(H),
                    'normalizer_order':len(normalizer),'bad_lift_size':len(bad),
                    'full_test_collision_elements':full_bad,
                    'deck_only_test_collision_elements':[], 'pass':True})

    # 5. Pure numerical warning, not a claimed topological exchange.
    before=[0,0]; after=[2,-2]
    trunc=lambda xs:sum(max(0,-x) for x in xs)
    require(sum(before)==sum(after), 'Euler sums match')
    require(trunc(before)==0 and trunc(after)==2, 'Truncation destroys inference')
    results.append({'name':'Euler-characteristic truncation negative control',
                    'before_chi':before,'after_chi':after,
                    'before_chiminus':trunc(before),'after_chiminus':trunc(after),
                    'topological_realizability_claimed':False,'pass':True})

    # 6. A graph-theoretic check on the meaning of two sides versus two ends.
    # Removing an edge of the 4-valent tree gives 3^depth outward branches on
    # each side. This finite count supports, but does not replace, the prose
    # observation that neither side must contain a unique end.
    branches=[{'depth':d,'outward_branches_per_side':3**d} for d in range(1,6)]
    require(all(row['outward_branches_per_side']>1 for row in branches), 'Sides are not single rays')
    results.append({'name':'Tree-sides convention control','branches':branches,'pass':True})
    return {'target':'10900010','classification':'NO RESOLUTION',
            'scope':'Exact arithmetic and finite coset controls only; no general topology verification',
            'control_groups':len(results),'all_pass':all(x['pass'] for x in results),
            'results':results}

if __name__=='__main__':
    try:
        print(json.dumps(main(),indent=2,sort_keys=True))
    except AssertionError as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
