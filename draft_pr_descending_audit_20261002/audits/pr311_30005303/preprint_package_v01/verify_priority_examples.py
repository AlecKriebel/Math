#!/usr/bin/env python3
"""Independent, exact, candidate-code-free reproduction of all comparison laws.

Usage: python3 verify_laws.py --output new_results.json
The output argument permits reproduction without modifying sealed outputs.
"""
from itertools import product, combinations
from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse
import json

def proj(x, indices):
    return tuple(x[i] for i in indices)

def separates(n, edges, A, B, C):
    allowed = set(range(n)) - set(C)
    seen, stack = set(A), list(A)
    while stack:
        i = stack.pop()
        for u, v in edges:
            j = v if u == i else u if v == i else None
            if j is not None and j in allowed and j not in seen:
                seen.add(j)
                stack.append(j)
    return not seen.intersection(B)

def verify_law(n, edges, weights, left_states, right_states):
    states = tuple(product((0, 1), repeat=n))
    assert set(weights) == set(states)
    assert all(type(w) is int and w >= 0 for w in weights.values())
    total = sum(weights.values())
    assert total > 0
    mtp2_bad = []
    lattice_bad = []
    for x in states:
        for y in states:
            meet = tuple(min(a,b) for a,b in zip(x,y))
            join = tuple(max(a,b) for a,b in zip(x,y))
            lhs, rhs = weights[meet]*weights[join], weights[x]*weights[y]
            if lhs < rhs:
                mtp2_bad.append({'x':x,'y':y,'meet':meet,'join':join,'integer_left':lhs,'integer_right':rhs})
            if weights[x] and weights[y] and (not weights[meet] or not weights[join]):
                lattice_bad.append({'x':x,'y':y})
    global_bad = []
    nontrivial_separations = []
    determinant_count = 0
    for assignment in product(range(4), repeat=n):
        A = tuple(i for i,a in enumerate(assignment) if a==0)
        B = tuple(i for i,a in enumerate(assignment) if a==1)
        C = tuple(i for i,a in enumerate(assignment) if a==2)
        if not A or not B or not separates(n,edges,A,B,C):
            continue
        nontrivial_separations.append({'A':[i+1 for i in A],'B':[i+1 for i in B],'C':[i+1 for i in C]})
        rows = tuple(product((0,1), repeat=len(A)))
        cols = tuple(product((0,1), repeat=len(B)))
        for c in product((0,1), repeat=len(C)):
            table = {(a,b):0 for a in rows for b in cols}
            for x in states:
                if proj(x,C)==c:
                    table[proj(x,A),proj(x,B)] += weights[x]
            for a1,a2 in combinations(rows,2):
                for b1,b2 in combinations(cols,2):
                    determinant_count += 1
                    determinant = table[a1,b1]*table[a2,b2]-table[a1,b2]*table[a2,b1]
                    if determinant:
                        global_bad.append({'A':A,'B':B,'C':C,'c':c,'determinant':determinant})
    balance = []
    for e in edges:
        left = Counter(proj(x,e) for x in left_states)
        right = Counter(proj(x,e) for x in right_states)
        balance.append({'edge':[i+1 for i in e], 'left':dict(Counter(''.join(map(str,proj(x,e))) for x in left_states)),
            'right':dict(Counter(''.join(map(str,proj(x,e))) for x in right_states)), 'equal':left==right})
    left_prod = right_prod = 1
    for x in left_states: left_prod *= weights[x]
    for x in right_states: right_prod *= weights[x]
    return {'n':n,'edges':[[i+1 for i in e] for e in edges], 'integer_weights':{''.join(map(str,x)):w for x,w in weights.items()},
        'normalizer':total,'support_closed_meet_join':not lattice_bad,'lattice_failures':lattice_bad[:4],
        'mtp2_ordered_pairs':len(states)**2,'mtp2_failure_count':len(mtp2_bad),'first_mtp2_failures':mtp2_bad[:4],
        'ordered_nontrivial_separations':len(nontrivial_separations),'all_separations':nontrivial_separations,
        'unique_conditioning_2x2_minors_checked':determinant_count,'global_markov_failure_count':len(global_bad),
        'first_global_markov_failures':global_bad[:4], 'invariant':{'left_states':left_states,'right_states':right_states,
        'edge_balances':balance,'integer_products':[left_prod,right_prod],
        'normalized_products':[str(Fraction(left_prod,total**len(left_states))),str(Fraction(right_prod,total**len(right_states)))],
        'normalized_difference':str(Fraction(left_prod-right_prod,total**len(left_states)))}}

def bits(*strings):
    return tuple(tuple(map(int,s)) for s in strings)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    E4=((0,1),(1,2),(2,3),(0,3))
    states4=tuple(product((0,1),repeat=4))
    gl={x:(2 if x==(1,1,1,1) else 1) if x[2]==x[3] else 0 for x in states4}
    candidate4={x:(2 if x==(1,1,1,1) else 1) if x[0]==x[1] else 0 for x in states4}
    ks={x:(7 if x==(0,0,0,0) else 1) if x[0]==x[1] else 0 for x in states4}
    U4=bits('0000','0011','1101','1110')
    W4=bits('0001','0010','1100','1111')
    gl_U=bits('0000','0111','1011','1100')
    gl_W=bits('0011','0100','1000','1111')
    exact_rotation=all(candidate4[(x[2],x[3],x[0],x[1])]==gl[x] for x in states4)
    rotated_edges={frozenset(((i+2)%4,(j+2)%4)) for i,j in E4}
    assert exact_rotation and rotated_edges=={frozenset(e) for e in E4}
    E6=tuple((i,(i+1)%6) for i in range(6))
    states6=tuple(product((0,1),repeat=6))
    c6={x:(2 if all(x) else 1) if x[0]==x[1] and x[2]==x[3] and x[4]==x[5] else 0 for x in states6}
    U6=bits('000000','001111','110011','111100')
    W6=bits('000011','001100','110000','111111')
    core_lift=True
    for a,b,c in product((0,1),repeat=3):
        expected=2 if a*b*c else 1
        core_lift &= candidate4[(a,a,b,c)]==expected and c6[(a,a,b,b,c,c)]==expected and gl[(b,c,a,a)]==expected
    assert core_lift
    laws={
        'gandolfi_lenarda_lemma5_2':verify_law(4,E4,gl,gl_U,gl_W),
        'kahle_sullivant_example6_5':verify_law(4,E4,ks,U4,W4),
        'released_candidate_C4':verify_law(4,E4,candidate4,U4,W4),
        'released_candidate_C6':verify_law(6,E6,c6,U6,W6)}
    for r in laws.values():
        assert r['support_closed_meet_join'] and r['mtp2_failure_count']==0 and r['global_markov_failure_count']==0
        assert all(e['equal'] for e in r['invariant']['edge_balances'])
        assert r['invariant']['integer_products'][0]!=r['invariant']['integer_products'][1]
    recoding_controls={}
    for name,supp in [('gms_example7',bits('0000','0001','1000','0011','1100','0111','1110','1111')),
                      ('gms_example8',bits('0100','0111','1001','1010'))]:
        orient={}
        for flip in states4:
            moved={tuple(a^b for a,b in zip(x,flip)) for x in supp}
            w={x:int(x in moved) for x in states4}
            failures=0
            for x in states4:
                for y in states4:
                    meet=tuple(min(a,b) for a,b in zip(x,y));join=tuple(max(a,b) for a,b in zip(x,y))
                    failures += w[meet]*w[join] < w[x]*w[y]
            orient[''.join(map(str,flip))]=failures
        recoding_controls[name]={'all_16_coordinate_flips_mtp2_failure_counts':orient,'some_orientation_mtp2':any(v==0 for v in orient.values()),
            'note':'Coordinate permutations preserve MTP2; these16 checks also exclude every flip-plus-permutation recoding if all countspositive.'}
    output={'arithmetic':'integer products and exact fractions only','candidate_code_read':False,
        'gandolfi_to_candidate_rotation':{'old_to_new_configuration':'x_new=(x_old3,x_old4,x_old1,x_old2)',
            'verified_all16_states':exact_rotation,'graph_edges_preserved':True},
        'C6_core_lift_verified_all8_core_states':core_lift,'laws':laws,'recoding_controls':recoding_controls}
    encoded=json.dumps(output,indent=2,sort_keys=True)+'\n'
    if args.output.exists():
        raise SystemExit('Refusing to overwrite any existing output; use a fresh --output path.')
    args.output.write_text(encoded)
    print(json.dumps({'output':str(args.output),'rotation_exact':exact_rotation,'C6_core_lift':core_lift,
        'law_checks':{k:{'MTP2_pairs':v['mtp2_ordered_pairs'],'MTP2_failures':v['mtp2_failure_count'],
            'ordered_global_separations':v['ordered_nontrivial_separations'], 'minors':v['unique_conditioning_2x2_minors_checked'],
            'global_failures':v['global_markov_failure_count'],'invariant_products':v['invariant']['integer_products']} for k,v in laws.items()},
        'old_GMS_orientation_some_MTP2':{k:v['some_orientation_mtp2'] for k,v in recoding_controls.items()}},indent=2))

if __name__=='__main__': main()
