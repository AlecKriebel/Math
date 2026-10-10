#!/usr/bin/env python3
"""Exact finite checks for KP-4.80. No source inputs or third-party packages.

These checks validate finite algebra in REPORT.md. They do not determine any
smooth isotopy class or prove the nonvanishing of a gauge-theoretic invariant.
"""
import argparse
import itertools
import json
import math
from pathlib import Path


def require(condition, message):
    """Enforce an audit condition even under python -O and -OO."""
    if not condition:
        raise AssertionError(message)


def span(vectors):
    out = {0}
    for v in vectors:
        out |= {x ^ v for x in tuple(out)}
    return frozenset(out)


def swap(v, i):
    if ((v >> i) ^ (v >> (i + 1))) & 1:
        return v ^ (1 << i) ^ (1 << (i + 1))
    return v


def invariant_closure(vectors, n):
    out = span(vectors)
    while True:
        nxt = span(list(out) + [swap(v, i) for v in out for i in range(n - 1)])
        if nxt == out:
            return out
        out = nxt


def invariant_subspaces_with_diagonal(n):
    """Enumerate all S_n-invariant subspaces containing the all-ones vector.

    Exhaustive: adjoining each outside vector and closing under adjacent
    transpositions can reach every invariant superspace of a current space.
    """
    start = span([(1 << n) - 1])
    found = {start}
    todo = [start]
    while todo:
        w = todo.pop()
        for v in range(1 << n):
            if v not in w:
                new = invariant_closure(list(w) + [v], n)
                if new not in found:
                    found.add(new)
                    todo.append(new)
    return sorted(found, key=lambda w: (len(w), sorted(w)))


def matmul(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n))
                       for j in range(n)) for i in range(n))


def transpose(a):
    return tuple(zip(*a))


def identity(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def root_checks(r):
    # Negative Cartan matrix of A_r, in the simple root basis.
    q = tuple(tuple(-2 if i == j else int(abs(i - j) == 1)
                    for j in range(r)) for i in range(r))
    one = identity(r)
    refl = []
    for i in range(r):
        s = [list(row) for row in one]
        for j in range(r):
            s[i][j] += q[i][j]
        s = tuple(map(tuple, s))
        require(matmul(s, s) == one, 'check failed: matmul(s, s) == one')
        require(matmul(matmul(transpose(s), q), s) == q, 'check failed: matmul(matmul(transpose(s), q), s) == q')
        refl.append(s)
    for i, a in enumerate(refl):
        for j, b in enumerate(refl):
            if abs(i-j) == 1:
                require(matmul(matmul(a,b),a) == matmul(matmul(b,a),b), 'check failed: matmul(matmul(a,b),a) == matmul(matmul(b,a),b)')
            elif abs(i-j) > 1:
                require(matmul(a,b) == matmul(b,a), 'check failed: matmul(a,b) == matmul(b,a)')
    found = {one}
    todo = [one]
    while todo:
        a = todo.pop()
        for s in refl:
            b = matmul(a,s)
            if b not in found:
                found.add(b)
                todo.append(b)
    require(len(found) == math.factorial(r+1), 'check failed: len(found) == math.factorial(r+1)')
    coxeter = one
    for s in refl:
        coxeter = matmul(coxeter,s)
    power = one
    coxeter_order = None
    for k in range(1, len(found)+1):
        power = matmul(power,coxeter)
        if power == one:
            coxeter_order = k
            break
    require(coxeter_order == r+1, 'check failed: coxeter_order == r+1')
    return {'rank':r, 'negative_cartan_matrix':[list(x) for x in q],
            'generated_matrix_group_order':len(found),
            'expected_symmetric_group_order':math.factorial(r+1),
            'coxeter_element_order':coxeter_order,
            'identity_matrix_count':sum(a==one for a in found)}


def run():
    modules=[]
    for n in range(2,9):
        spaces=invariant_subspaces_with_diagonal(n)
        dims=sorted({(len(w).bit_length()-1) for w in spaces})
        ranks=sorted({n-d for d in dims})
        expected=sorted({0,n-1} if n%2 else {0,1,n-1})
        require(ranks==expected, 'check failed: ranks==expected')
        # The scalar label vector must be permutation-invariant and kill Delta.
        scalar_labels=[v for v in range(1<<n)
                       if all(swap(v,i)==v for i in range(n-1)) and v.bit_count()%2==0]
        require(len(scalar_labels)==(1 if n%2 else 2), 'check failed: len(scalar_labels)==(1 if n%2 else 2)')
        modules.append({'n':n,'invariant_relation_space_dimensions':dims,
                        'permitted_twist_group_ranks':ranks,
                        'permutation_invariant_F2_scalar_characters':len(scalar_labels)})
    # Explicit three-generator standard quotient by the diagonal.
    delta=7
    rep=lambda v:min(v,v^delta)
    cosets=sorted({rep(v) for v in range(8)})
    generators=[rep(1<<i) for i in range(3)]
    require(len(cosets)==4 and len(set(generators))==3 and 0 not in generators, 'check failed: len(cosets)==4 and len(set(generators))==3 and 0 not in generators')
    require(rep(1^2^4)==0, 'check failed: rep(1^2^4)==0')
    addition=[[rep(a^b) for b in cosets] for a in cosets]
    roots=[root_checks(r) for r in range(1,6)]
    # Arithmetic consequence of imported eta^4=0, not a computation of stems.
    bf=[]
    for n in range(2,9):
        cases=[]
        for a in range(1,n):
            b=n-a
            first='eta^3_nonzero_order_2' if (a%2 and n==2) else 'zero'
            second='eta^3_nonzero_order_2' if (b%2 and n==2) else 'zero'
            cases.append({'left_summands':a,'right_summands':b,
                          'spin_choice_left':first,'spin_choice_right':second})
        bf.append({'summands':n,'neck_cases':cases,
                   'basis':'KM Proposition 5.1 plus connected-sum product and imported eta^4=0'})
    return {'problem_id':2956,'all_assertions_passed':True,
            'permutation_modules':modules,
            'triple_quotient':{'representatives':cosets,'neck_generators':generators,
                              'addition_table':addition},
            'A_type_reflection_groups':roots,
            'nonequivariant_BF_arithmetic':bf,
            'K3_sums':[{'summands':n,'b2':22*n,'euler_characteristic':22*n+2,
                        'signature':-16*n} for n in range(1,9)],
            'limits':['No smooth isotopy decision is performed.',
                      'No geometric independence or gauge nonvanishing is inferred from finite tests.',
                      'The stable-stem and gauge-theory inputs are imported theorems, not machine-proved here.']}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    data=json.dumps(run(),indent=2,sort_keys=True)+'\n'
    if a.output:
        a.output.write_text(data)
    else:
        print(data,end='')
