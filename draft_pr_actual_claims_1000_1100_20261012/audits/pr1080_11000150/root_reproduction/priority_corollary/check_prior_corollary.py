#!/usr/bin/env python3
"""Exact finite fault controls for the authored prior-corollary derivation.

No surface theorem or cited theorem is proved by these finite checks.
Run: python3 -I check_prior_corollary.py
"""
from itertools import product
from pathlib import Path
import hashlib
import json

ID = (0, 0, 0)

def mul(x, y):
    a, b, c = x
    d, e, f = y
    return (a + d, b + e, c + f + a * e)

def inv(x):
    a, b, c = x
    return (-a, -b, a * b - c)

def conj(x, y):
    return mul(mul(x, y), inv(x))

def pos(x):
    # Normal positive cone for the integer Heisenberg group, lexicographic order.
    return x > ID

def leq(x, y):
    return mul(y, inv(x)) == ID or pos(mul(y, inv(x)))

def evaluate(w, alphabet):
    r = ID
    for a in w:
        r = mul(r, alphabet[a])
    return r

def subsequence(u, v):
    j = 0
    for a in v:
        if j < len(u) and u[j] == a:
            j += 1
    return j == len(u)

def gaussian_add(x, y):
    return (x[0] + y[0], x[1] + y[1])

def gaussian_mul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])

def matrix_mul(x, y):
    return tuple(gaussian_add(gaussian_mul(x[2*i], y[j]),
                              gaussian_mul(x[2*i+1], y[2+j]))
                 for i in range(2) for j in range(2))

def matrix_power(x, n):
    r = ((1, 0), (0, 0), (0, 0), (1, 0))
    for _ in range(n):
        r = matrix_mul(r, x)
    return r

def main():
    cube = list(product(range(-1, 2), repeat=3))
    cone = [x for x in cube if pos(x)]
    normal_checks = 0
    for x in cube:
        assert mul(x, inv(x)) == mul(inv(x), x) == ID
        for q in cone:
            assert pos(conj(x, q))
            normal_checks += 1
    for q in cone:
        for r in cone:
            assert pos(mul(q, r))
            assert not pos(inv(q))
    invariant_checks = 0
    for x in cube:
        for y in cube:
            if leq(x, y):
                assert not leq(y, x) or x == y
                for u in cube:
                    assert leq(mul(u, x), mul(u, y))
                    assert leq(mul(x, u), mul(y, u))
                    if x != y:
                        assert mul(u, x) != mul(u, y)
                    invariant_checks += 2

    alphabet = {'A': (1, 0, 0), 'B': (0, 1, 0), 'C': (1, 1, 1)}
    expansions = {'A': 'A', 'B': 'B', 'C': 'AB'}
    atom_alphabet = {k: alphabet[k] for k in 'AB'}
    fibers = {}
    expansion_checks = 0
    for n in range(9):
        for letters in product('ABC', repeat=n):
            w = ''.join(letters)
            h = evaluate(w, alphabet)
            e = ''.join(expansions[a] for a in w)
            assert evaluate(e, atom_alphabet) == h
            assert len(w) <= len(e) == h[0] + h[1]
            fibers.setdefault(h, []).append(w)
            expansion_checks += 1
    target = (2, 2, 1)
    target_words = fibers[target]
    assert target != ID
    assert conj((0, 1, 0), target) != target  # Generic target is noncentral.
    assert max(map(len, target_words)) <= target[0] + target[1] == 4
    assert evaluate('C', alphabet) == evaluate('AB', alphabet)
    assert expansions['C'] == expansions['A'] + expansions['B']
    # The substitution need not be injective; the length argument is sufficient.
    for u in target_words:
        for v in target_words:
            if subsequence(u, v):
                assert u == v

    # Finite generation and no positive identity alone do not imply the claim.
    # X = diag(2i,2), Y = [[1,1],[0,1]] in GL_2(Q(i)).
    # det magnitude is 4^a for a occurrences of X; if a=0, Y^b != I.
    # Hence no nonempty positive X,Y word is I, but Y^m X^2 Y^m = X^2.
    X = ((0, 2), (0, 0), (0, 0), (2, 0))
    Y = ((1, 0), (1, 0), (0, 0), (1, 0))
    X2 = matrix_power(X, 2)
    missing_normality_checks = 0
    for m in range(1, 21):
        Ym = matrix_power(Y, m)
        assert matrix_mul(matrix_mul(Ym, X2), Ym) == X2
        missing_normality_checks += 1
    # The analytic determinant argument above establishes no positive identity
    # for all lengths, while these exact finite equalities catch a false lemma.

    # An identity-valued letter permits arbitrary length with an erasing code.
    erasing_control = ['E' * m + 'A' for m in range(21)]
    for w in erasing_control:
        assert w.replace('E', '') == 'A'
    assert len(set(map(len, erasing_control))) == 21

    # CT's equivalence permits arbitrary injections; ordered equality is stronger.
    assert sorted('AB') == sorted('BA')
    assert evaluate('AB', alphabet) != evaluate('BA', alphabet)

    # Global support normalization may change a noncentral target.
    assert conj((0, 1, 0), alphabet['A']) != alphabet['A']
    assert all(conj(x, (0, 0, 1)) == (0, 0, 1) for x in cube)

    # Support cardinality controls do not discard repeated letters.
    for g in range(1, 7):
        distinct_bound = 2 ** (2 * g) * (3 * g - 2) + 1
        chain_length = 4 * g * (2 * g + 1)
        assert 2 * g <= distinct_bound
        assert chain_length > 2 * g

    b = Path(__file__).resolve().parent
    inp = json.loads((b/'INPUT_PINS.json').read_text())
    root = b.parents[4]
    # Locate workspace by pinned relative path, without invoking Git.
    while not (root/'AGENTS.md').is_file():
        root = root.parent
        if root == root.parent:
            raise RuntimeError('workspace root missing')
    verified = []
    for r in inp['files']:
        f = root/r['path']
        assert f.stat().st_size == r['bytes']
        assert hashlib.sha256(f.read_bytes()).hexdigest() == r['sha256']
        verified.append(r['path'])
    result = {
        'finite_checks_only': True,
        'normal_cone_checks': normal_checks,
        'two_sided_order_checks': invariant_checks,
        'nonerasing_atomic_expansion_checks': expansion_checks,
        'noncentral_target': target,
        'target_words': target_words,
        'target_max_length': max(map(len, target_words)),
        'missing_normality_counterexample_checks': missing_normality_checks,
        'erasing_identity_control_lengths': list(map(len, erasing_control)),
        'ct_scrambled_equivalence_distinguished_from_ordered_equality': True,
        'support_vs_length_control': True,
        'frozen_inputs_reverified': len(verified),
        'status': 'PASS'
    }
    (b/'CONTROL_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
