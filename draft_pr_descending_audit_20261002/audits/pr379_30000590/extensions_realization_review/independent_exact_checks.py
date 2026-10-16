#!/usr/bin/env python3
"""Exact integral group-ring computations in F(a,b) x F(c,d).

This code uses reduced noncommuting free words, never exponent-vector
substitution. Finite checks supplement the universal proofs in
INDEPENDENT_MATHEMATICS.md; they do not assert universal exactness.
"""
import json
from collections import defaultdict


def reduce_word(w):
    out = []
    for s in w:
        if out and out[-1] == -s:
            out.pop()
        else:
            out.append(s)
    return tuple(out)


ONE = ((), ())


def mul_g(x, y):
    return (reduce_word(x[0] + y[0]), reduce_word(x[1] + y[1]))


def inv_g(x):
    return (tuple(-s for s in x[0][::-1]), tuple(-s for s in x[1][::-1]))


def pow_g(x, n):
    if n < 0:
        return pow_g(inv_g(x), -n)
    out = ONE
    for _ in range(n):
        out = mul_g(out, x)
    return out


def clean(p):
    return {w: n for w, n in p.items() if n}


def add(p, q):
    out = defaultdict(int, p)
    for w, n in q.items():
        out[w] += n
    return clean(out)


def neg(p):
    return {w: -n for w, n in p.items()}


def sub(p, q):
    return add(p, neg(q))


def mul(p, q):
    out = defaultdict(int)
    for w, n in p.items():
        for v, m in q.items():
            out[mul_g(w, v)] += n * m
    return clean(out)


def mono(g):
    return {g: 1}


E = mono(ONE)
a, b, c, d = ((1,), ()), ((2,), ()), ((), (1,)), ((), (2,))
x, y, z = mul_g(a, inv_g(b)), mul_g(c, inv_g(d)), mul_g(b, inv_g(d))
G4 = [a, b, c, d]
H3 = [x, y, z]
minus = [sub(mono(s), E) for s in G4]
hminus = [sub(mono(s), E) for s in H3]


def g_name(g):
    def wr(w, labels):
        return ''.join(labels[abs(k)-1] + ('^-1' if k < 0 else '') for k in w) or '1'
    return wr(g[0], 'ab') + '|' + wr(g[1], 'cd')


def encode(p):
    return [[g_name(w), n] for w, n in sorted(p.items())]


def encode_vec(v):
    return [encode(p) for p in v]


def eval_h_word(w):
    out = ONE
    for k in w:
        q = H3[abs(k)-1]
        out = mul_g(out, q if k > 0 else inv_g(q))
    return out


def inv_h_word(w):
    return tuple(-s for s in w[::-1])


def fox_suffix(w):
    """D_s(wv)=D_s(w)v+D_s(v), so w-1=sum (s-1)D_s(w)."""
    deriv = [{}, {}, {}]
    suffix = ONE
    for k in w[::-1]:
        i = abs(k)-1
        s = H3[i]
        if k > 0:
            deriv[i] = add(deriv[i], mono(suffix))
            suffix = mul_g(s, suffix)
        else:
            term = mul_g(inv_g(s), suffix)
            deriv[i] = sub(deriv[i], mono(term))
            suffix = term
    assert suffix == eval_h_word(w)
    return deriv


def bad_map(v):
    out = {}
    for s, q in zip(hminus, v):
        out = add(out, mul(s, q))
    return out


def counterfeit_transpose(v):
    out = {}
    for s, q in zip(hminus, v):
        out = add(out, mul(q, s))
    return out


def delta0(q):
    return [mul(s, q) for s in minus]


def delta1(v):
    out = []
    for i in range(2):
        for j in range(2, 4):
            out.append(sub(mul(minus[i], v[j]), mul(minus[j], v[i])))
    return out


def wrong_delta1(v):
    return [add(mul(minus[i], v[j]), mul(minus[j], v[i]))
            for i in range(2) for j in range(2, 4)]


def right_vec(v, q):
    return [mul(p, q) for p in v]


def chi(g):
    return sum(1 if s > 0 else -1 for w in g for s in w)


def relator(k):
    zv = (3,) * k if k >= 0 else (-3,) * -k
    v = zv + (2,) + inv_h_word(zv)
    return (1,) + v + (-1,) + inv_h_word(v)


def main():
    tests = {}
    tests['chi_H_generators_zero'] = [chi(s) for s in H3]
    assert tests['chi_H_generators_zero'] == [0, 0, 0]
    tests['noncommutative_control_ab_minus_ba'] = encode(sub(mono(mul_g(a,b)), mono(mul_g(b,a))))
    assert tests['noncommutative_control_ab_minus_ba']
    assert mul_g(a,c) == mul_g(c,a)
    assert mul_g(a,b) != mul_g(b,a)
    tests['commutator_ab_augmentation_difference'] = encode(sub(mono(mul_g(mul_g(mul_g(a,b),inv_g(a)),inv_g(b))), E))
    assert tests['commutator_ab_augmentation_difference']
    cycles = []
    for k in range(-5, 6):
        r = relator(k)
        v = fox_suffix(r)
        residual = bad_map(v)
        assert eval_h_word(r) == ONE and residual == {}
        assert any(v)
        cycles.append({'k': k, 'relator_in_G': g_name(eval_h_word(r)),
                       'vector': encode_vec(v), 'matrix_residual': encode(residual)})
    tests['exact_bad_matrix_cycles'] = cycles
    transposed = counterfeit_transpose(fox_suffix(relator(2)))
    assert transposed
    tests['negative_wrong_side_residual_k2'] = encode(transposed)
    v = [E, {}, {}]
    assert bad_map(v)
    tests['negative_unit_vector_not_cycle'] = encode(bad_map(v))
    q = add(sub(mono(mul_g(a,b)), mono(mul_g(b,a))), mono(mul_g(c,inv_g(d))))
    rhs = add(mono(mul_g(b,c)), neg(mono(mul_g(a,d))))
    assert delta1(delta0(q)) == [{}, {}, {}, {}]
    assert delta0(mul(q,rhs)) == right_vec(delta0(q),rhs)
    cochain = [q, rhs, sub(q,rhs), mul(q,rhs)]
    assert delta1(right_vec(cochain,rhs)) == right_vec(delta1(cochain),rhs)
    tests['actual_product_tree_resolution'] = {
        'C_ranks': [1,4,4], 'input': encode(q),
        'delta0_input': encode_vec(delta0(q)),
        'delta1_delta0': encode_vec(delta1(delta0(q))),
        'delta0_right_equivariance': True,
        'delta1_right_equivariance': True,
        'delta1_arbitrary_cochain': encode_vec(delta1(cochain))}
    wrong = wrong_delta1(delta0(E))
    assert any(wrong)
    tests['negative_missing_product_sign'] = encode_vec(wrong)
    # A free-factor augmentation complex is evaluated with actual words.
    free_delta = [mul(minus[i],q) for i in range(2)]
    assert any(free_delta)
    tests['actual_free_group_C_ranks'] = [1,2]
    tests['actual_free_group_delta0_nonzero_sample'] = encode_vec(free_delta)
    # Integral tensor/cohomology counterfeits: differential 2 in degrees 0,1.
    tests['negative_nonflat_tensor_counterexample'] = {
        'integral_complex': 'Z --2--> Z in degrees 0,1',
        'integral_H0': 0, 'integral_H1': 'Z/2',
        'tensor_with_Z2_H0': 'Z/2', 'tensor_with_Z2_H1': 'Z/2',
        'naive_only_top_formula_H0': 0,
        'Tor1_top_with_Z2': 'Z/2'}
    tests['scope'] = 'Exact finite word checks only. Universal conclusions are proved separately.'
    print(json.dumps(tests, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
