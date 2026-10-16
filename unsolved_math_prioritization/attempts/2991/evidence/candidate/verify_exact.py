#!/usr/bin/env python3
"""Source-free exact checks. Geometric theorems still require the written proof.

Prints JSON to stdout unless --output names an existing external directory's file.
Never writes inside this candidate directory. All checks remain active with -O/-OO.
"""
import argparse
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import sys

class VerificationError(RuntimeError):
    pass

def require(condition, message):
    if not condition:
        raise VerificationError(message)

def expect_failure(fn, label):
    try:
        fn()
    except VerificationError:
        return label
    raise VerificationError('negative control did not fail: ' + label)

def sign_class(a, p):
    return min(a % p, (-a) % p)

def same_multiset_after_multiplier(xs, p, q):
    return sorted(sign_class(x,p) for x in xs) == sorted(sign_class(q*x,p) for x in xs)

def candidate_preconditions(p, q, xs):
    require(p >= 2, 'cyclic group order must be at least two')
    require(math.gcd(p,q) == 1, 'multiplier must be a unit')
    require(q*q % p == 1, 'coordinate swap must normalize this deck action')
    require(q % p not in (1,p-1), 'multiplier must act nontrivially modulo sign')
    require(len(xs) % 2 == 1, 'odd sector count is required for the counting obstruction')
    require(all(math.gcd(x,p) == 1 for x in xs), 'all sector images must generate C_p')
    require(not same_multiset_after_multiplier(xs,p,q), 'obstruction unexpectedly failed')

def transpose(a):
    return [list(x) for x in zip(*a)]

def mm(a,b):
    require(bool(a) and bool(b) and len(a[0]) == len(b), 'matrix dimension mismatch')
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def det(a):
    n=len(a)
    require(n > 0 and all(len(row)==n for row in a), 'determinant requires square matrix')
    if n==1:
        return a[0][0]
    return sum((-1)**j*a[0][j]*det([row[:j]+row[j+1:] for row in a[1:]]) for j in range(n))

def check_graph(s):
    n=len(s)
    require(s == transpose(s), 'graph form must be symmetric')
    require(abs(det(s)) == 1, 'graph form must be integrally unimodular')
    eye=[[int(i==j) for j in range(n)] for i in range(n)]
    zero=[[0]*n for _ in range(n)]
    j=[zero[i]+eye[i] for i in range(n)]+[[-x for x in eye[i]]+zero[i] for i in range(n)]
    c=s+eye
    require(mm(mm(transpose(c),j),c) == zero, 'graph not Lagrangian')
    return {'rank':n,'determinant':det(s)}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', help='Explicit output JSON file outside the candidate tree')
    parser.add_argument('--inject-fault', choices=['multiplier','surjectivity','matrix','expected-count'])
    args=parser.parse_args()
    p,q=8,3
    if args.inject_fault=='multiplier':
        q=1
    units=[x for x in range(p) if math.gcd(x,p)==1]
    require(units==[1,3,5,7], 'incorrect unit set')
    classes=sorted(set(sign_class(x,p) for x in units))
    require(classes==[1,3], 'incorrect unit/sign classes')
    require(q*q % p == 1, 'deck normalizer relation failed')
    require(all(sign_class(q*x,p)!=sign_class(x,p) for x in units), 'multiplier has a fixed unit/sign class')
    swaps=0
    for xs in itertools.product(units, repeat=3):
        candidate_preconditions(p,q,xs)
        for perm in itertools.permutations(range(3)):
            require(any(sign_class(xs[i],p)!=sign_class(q*xs[perm[i]],p) for i in range(3)), 'sector permutation escaped obstruction')
            swaps+=1
    expected=385 if args.inject_fault=='expected-count' else 384
    require(swaps==expected, 'exhaustive permutation count mismatch')
    if args.inject_fault=='surjectivity':
        candidate_preconditions(8,3,[0,0,0])
    controls=[]
    controls.append(expect_failure(lambda:candidate_preconditions(8,1,[1,1,1]), 'identity multiplier rejected'))
    controls.append(expect_failure(lambda:candidate_preconditions(8,7,[1,1,1]), 'sign-only multiplier rejected'))
    controls.append(expect_failure(lambda:candidate_preconditions(8,3,[0,0,0]), 'non-generating images rejected'))
    controls.append(expect_failure(lambda:candidate_preconditions(8,3,[1,3]), 'even-sector hypothesis rejected'))
    require(same_multiset_after_multiplier([1,3],8,3), 'even-sector counterexample missing')
    require(same_multiset_after_multiplier([0,0,0],8,3), 'nonunit counterexample missing')
    require(same_multiset_after_multiplier([1,3,5],8,7), 'sign-only control missing')
    real_swap=[[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]]
    require(det(real_swap)==1, 'coordinate swap reverses R4 orientation')
    forms=[[[1]],[[0,1],[1,0]],[[1,0],[0,-1]],[[2,1],[1,1]]]
    form_results=[check_graph(s) for s in forms]
    controls.append(expect_failure(lambda:check_graph([[2,0],[0,1]]), 'nonunimodular graph rejected'))
    controls.append(expect_failure(lambda:check_graph([[1,1],[0,1]]), 'nonsymmetric graph rejected'))
    if args.inject_fault=='matrix':
        check_graph([[1,1],[0,1]])
    s=[[0,1],[1,0]]
    change=[[1,1],[0,1]]
    changed=mm(mm(change,s),transpose(change))
    require(changed==[[2,1],[1,0]], 'integral congruence computation wrong')
    check_graph(changed)
    g,k,p_page,b=2,1,0,2
    double_g,double_k=2*g+b-1,2*k-2*p_page-b+1
    require((double_g,double_k)==(5,1), 'relative doubling formula wrong')
    require(2+double_g-3*double_k==4, 'double Euler characteristic mismatch')
    exterior_cases=[]
    for b2,genus,sector_rank in [(2,5,1),(22,22,0)]:
        require(genus==b2+3*sector_rank, 'balanced parameter relation failed')
        ranks=[1,1,b2+2*genus,0,0]
        require(sum((-1)**i*r for i,r in enumerate(ranks))==(2+b2)-(2-2*genus), 'exterior Euler characteristic mismatch')
        exterior_cases.append({'ambient_b2':b2,'central_genus':genus,'exterior_betti_numbers':ranks})
    proof=Path(__file__).resolve().parent/'PART_A_PROOF.md'
    proof_bytes=proof.read_bytes()
    require(hashlib.sha256(proof_bytes).hexdigest()=='90be5ae3ab394227e9b22db5db3c49e1798714f70a7c554eed4fadb539ee820b', 'part A proof changed after audit handoff')
    result={'status':'pass','geometric_proof_certified_by_code':False,
            'unit_triples':64,'sector_permutation_checks':swaps,'negative_controls':controls,
            'graph_forms':form_results,'double_parameters':[double_g,double_k],
            'exterior_cases':exterior_cases,'proof_sha256':hashlib.sha256(proof_bytes).hexdigest(),
            'uid':os.geteuid(),'optimization':sys.flags.optimize,
            'candidate_read_only':not os.access(Path(__file__).resolve().parent,os.W_OK)}
    data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        path=Path(args.output).expanduser().resolve()
        root=Path(__file__).resolve().parent
        require(not path.is_relative_to(root), 'output must be outside candidate tree')
        require(path.parent.is_dir(), 'external output parent must already exist')
        require(not path.exists(), 'refuse to overwrite existing output')
        path.write_text(data)
    else:
        print(data,end='')

if __name__=='__main__':
    main()
