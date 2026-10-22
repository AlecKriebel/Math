#!/usr/bin/env python3
"""Independent exact finite checks. Does not import the author implementation."""
from itertools import product, combinations
from fractions import Fraction
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def placements(a, b, D):
    return [(x, y, w, h) for w, h in sorted({(a,b),(b,a)})
            for x in range(D-w+1) for y in range(D-h+1)]


def disjoint(a,b):
    # Positive overlap in both coordinate intervals is exactly interior overlap.
    return (min(a[0]+a[2], b[0]+b[2]) <= max(a[0],b[0]) or
            min(a[1]+a[3], b[1]+b[3]) <= max(a[1],b[1]))


def independent_grid(dimensions, D):
    # Natural input order, x-major positions, no masks, memoization or symmetry cuts.
    choices=[placements(a,b,D) for a,b in dimensions]
    node_counts=[0]*(len(dimensions)+1)
    tested=[0]*len(dimensions)
    first=None
    def visit(chosen):
        nonlocal first
        depth=len(chosen);node_counts[depth]+=1
        if depth==len(dimensions):
            if first is None:first=list(chosen)
            return 1
        total=0
        for candidate in choices[depth]:
            tested[depth]+=1
            if all(disjoint(candidate,old) for old in chosen):
                total+=visit(chosen+[candidate])
        return total
    count=visit([])
    return {'denominator':D,'complete_packing_count':count,'placements_per_piece':list(map(len,choices)),
            'nodes_by_depth':node_counts,'candidate_trials_by_depth':tested,'first_witness':first}


def longest_paths(n,edges):
    # Independent synchronous relaxation: after n rounds, any change witnesses a
    # positive cycle. Otherwise the minimal nonnegative solution has been found.
    distances=[0]*n
    for _ in range(n):
        old=distances
        distances=old.copy()
        for src,dst,weight in edges:
            distances[dst]=max(distances[dst],old[src]+weight)
        if distances==old:return distances
    return None


def separator_enumeration(dimensions,D):
    # Every real axis-parallel packing chooses an orientation and at least one
    # true separator for every pair. Enumerate all such systems independently.
    n=len(dimensions);pairs=list(combinations(range(n),2))
    orientation_options=[sorted({(a,b),(b,a)}) for a,b in dimensions]
    total=0;acyclic=0;feasible=0;first=None
    for sizes in product(*orientation_options):
        for separators in product(range(4),repeat=len(pairs)):
            total+=1;horizontal=[];vertical=[]
            for (i,j),separator in zip(pairs,separators):
                if separator==0:horizontal.append((i,j,sizes[i][0]))
                elif separator==1:horizontal.append((j,i,sizes[j][0]))
                elif separator==2:vertical.append((i,j,sizes[i][1]))
                else:vertical.append((j,i,sizes[j][1]))
            x=longest_paths(n,horizontal);y=longest_paths(n,vertical)
            if x is None or y is None:continue
            acyclic+=1
            if any(x[i]+sizes[i][0]>D or y[i]+sizes[i][1]>D for i in range(n)):continue
            feasible+=1
            proposed=[(x[i],y[i],*sizes[i]) for i in range(n)]
            require(all(disjoint(a,b) for a,b in combinations(proposed,2)), 'separator certificate overlaps')
            if first is None:first=proposed
    return {'systems_tested':total,'acyclic_systems':acyclic,'feasible_systems':feasible,'first_witness':first}


def checks():
    dims=[(12,6),(6,4),(4,3)];with_hole=dims+[(6,6)]
    prefix=independent_grid(dims,12);hole=independent_grid(with_hole,12)
    require(prefix['complete_packing_count']>0,'prefix should pack')
    require(hole['complete_packing_count']==0,'square-hole should fail')
    prefix_separator=separator_enumeration(dims,12)
    hole_separator=separator_enumeration(with_hole,12)
    require(prefix_separator['feasible_systems']>0,'prefix separators should exist')
    require(hole_separator['feasible_systems']==0,'no square-hole separator system may fit')
    require(hole_separator['systems_tested']==32768,'incomplete separator enumeration')
    sums=all(sum((Fraction(1,n*(n+1)) for n in range(1,N+1)),Fraction(0))==1-Fraction(1,N+1)
             for N in range(1,101))
    require(sums,'telescoping check failed')
    rational_square_indices=[m for m in range(1,101) if any(k*k==m for k in range(1,11))]
    a=(Fraction(0),Fraction(0),Fraction(1,2),Fraction(1,2))
    contact=(Fraction(1,2),Fraction(0),Fraction(1,2),Fraction(1,2))
    overlap=(Fraction(1,2)-Fraction(1,10**50),Fraction(0),Fraction(1,2),Fraction(1,2))
    require(disjoint(a,contact) and not disjoint(a,overlap),'boundary model failed')
    return {'schema':'independent-reciprocal-rectangle-checks-v1','problem_id':'3900015',
            'full_problem_resolved':False,'prefix_grid':prefix,'m4_grid':hole,
            'prefix_separator_systems':prefix_separator,'m4_separator_systems':hole_separator,
            'telescoping_prefixes_checked':100,'contact_allowed':True,
            'positive_overlap_1_over_10_pow_50_rejected':True,
            'square_indices_up_to_100':rational_square_indices,
            'threshold_is_square':(10**500)**2==10**1000,
            'scope':'finite axis-parallel obstructions only; no numerical evidence certifies infinite existence'}

if __name__=='__main__':
    print(json.dumps(checks(),sort_keys=True,indent=2))
