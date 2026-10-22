#!/usr/bin/env python3
"""Exact local algebra controls; these do not decide the link conjecture.

Python 3.10+ standard library only. Run from any directory. Output is deterministic.
The polynomial ring in four real variables is implemented with sparse rational
coefficients so the Jacobian identities are symbolic, not sampled assertions.
"""
from fractions import Fraction as Q
from itertools import combinations, product
import json

ZERO = (0, 0, 0, 0)


def clean(p):
    return {m: Q(c) for m, c in p.items() if c}


def const(c):
    return clean({ZERO: c})


def var(i):
    m = [0] * 4
    m[i] = 1
    return {tuple(m): Q(1)}


def add(a, b):
    p = dict(a)
    for m, c in b.items():
        p[m] = p.get(m, 0) + c
    return clean(p)


def scale(a, c):
    return clean({m: v*c for m, v in a.items()})


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    p = {}
    for m, c in a.items():
        for n, d in b.items():
            e = tuple(i+j for i, j in zip(m, n))
            p[e] = p.get(e, 0) + c*d
    return clean(p)


def power(a, n):
    r = const(1)
    for _ in range(n):
        r = mul(r, a)
    return r


def diff(a, i):
    p = {}
    for m, c in a.items():
        if m[i]:
            n = list(m)
            n[i] -= 1
            p[tuple(n)] = c*m[i]
    return clean(p)


def restrict_zero(a, indices):
    return {m: c for m, c in a.items() if all(m[i] == 0 for i in indices)}


def on_diagonal_curve(a):
    """Substitute (x,y,z,w)=(t,0,t,0), retaining coefficients in Q[t]."""
    p = {}
    for (x, y, z, w), c in a.items():
        if y == w == 0:
            p[x+z] = p.get(x+z, 0)+c
    return {d: c for d, c in p.items() if c}


def jacobian(f):
    return [[diff(a, i) for i in range(4)] for a in f]


def minor(jac, i, j):
    return sub(mul(jac[0][i], jac[1][j]), mul(jac[0][j], jac[1][i]))


def minors(jac):
    return [minor(jac, i, j) for i, j in combinations(range(4), 2)]


def poly_rem_mod2(a, b):
    while a and a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length()-b.bit_length())
    return a


def univariate_mul(a, b, modulus):
    p = [0] * (len(a)+len(b)-1)
    for i, c in enumerate(a):
        for j, d in enumerate(b):
            p[i+j] = (p[i+j]+c*d) % modulus
    return p


def main():
    checks = []
    x, y, z, w = [var(i) for i in range(4)]
    R = add(add(power(x, 2), power(y, 2)), add(power(z, 2), power(w, 2)))
    G = [mul(x, R), mul(y, R)]
    A = sub(R, scale(power(x, 2), 2))
    H = [mul(x, R), mul(mul(y, R), A)]
    JG, JH = jacobian(G), jacobian(H)
    expected_good = mul(R, add(R, scale(add(power(x, 2), power(y, 2)), 2)))
    assert minor(JG, 0, 1) == expected_good
    checks.append('G positive minor identity verified symbolically')
    Rplane = add(power(z, 2), power(w, 2))
    assert restrict_zero(minor(JH, 0, 1), [0, 1]) == power(Rplane, 3)
    checks.append('H zero-plane minor equals (z^2+w^2)^3 symbolically')
    assert all(not on_diagonal_curve(a) for a in JH[1])
    assert on_diagonal_curve(JH[0][0]) == {2: Q(4)}
    assert all(not on_diagonal_curve(a) for a in minors(JH))
    checks.append('H rank-one punctured critical curve verified symbolically')
    assert all(ZERO not in a for row in JG+JH for a in row)
    checks.append('Both differentials vanish at the origin')

    # z_complex=x+iy, w_complex=z+iw.
    zu = (sub(power(x, 2), power(y, 2)), scale(mul(x, y), 2))
    wu = (sub(power(z, 2), power(w, 2)), scale(mul(z, w), 2))
    f = (add(zu[0], wu[0]), add(zu[1], wu[1]))
    g = (sub(zu[0], wu[0]), sub(zu[1], wu[1]))
    real = add(mul(f[0], g[0]), mul(f[1], g[1]))
    imag = sub(mul(f[1], g[0]), mul(f[0], g[1]))
    JJ = jacobian([real, imag])
    assert restrict_zero(real, [2, 3]) == power(add(power(x, 2), power(y, 2)), 2)
    assert all(not restrict_zero(a, [2, 3]) for a in JJ[1])
    assert all(not restrict_zero(a, [2, 3]) for a in minors(JJ))
    checks.append('Conjugate-product rank failure on w_complex=0 verified symbolically')

    # Fourier rescaling checks. The universal obstruction is parity, not this loop.
    for k in range(1, 65):
        assert (2*k-1) % 2 == 1
    for mode, exponents in [(2, (3, 1)), (4, (4, 0))]:
        assert exponents == ((4+mode)//2, (4-mode)//2)
    a = Q(1, 4)
    numerator_lower = 1-3*a+2*a*a
    denominator_upper = (1+a)**2
    assert numerator_lower == Q(3, 8)
    assert denominator_upper == Q(25, 16)
    assert numerator_lower/denominator_upper == Q(6, 25)
    checks.append('Fourier parity and critical-angle lower bound 6/25 verified exactly')

    # Degree-6 irreducibility: any reducible degree-6 polynomial has a factor
    # of degree <=3. Test all monic polynomials, including zero constant term.
    D2 = (1 << 6) | (1 << 3) | 1
    trial_factors = [b for d in range(1, 4) for b in range(1 << d, 1 << (d+1))]
    assert len(trial_factors) == 14
    assert all(poly_rem_mod2(D2, b) != 0 for b in trial_factors)
    assert next(k for k in range(1, 7) if pow(2, k, 9) == 1) == 6
    assert D2 != (1 << 7)-1
    checks.append('Delta mod 2 irreducible: all 14 monic divisors of degrees 1--3 excluded')

    # Squaring is injective over F_2, so q mod 2 must be 1+t^3+t^6.
    parity = [1, 0, 0, 1, 0, 0, 1]
    D = [1, -4, 8, -9, 8, -4, 1]
    target = [0]*13
    for i, c in enumerate(D):
        target[2*i] = c % 4
    possible_mid = set()
    count = 0
    for lifts in product([0, 2], repeat=7):
        coeffs = [p+l for p, l in zip(parity, lifts)]
        opposite = [(-1)**i*c for i, c in enumerate(coeffs)]
        norm = univariate_mul(coeffs, opposite, 4)
        possible_mid.add(norm[6])
        assert norm[6] == 1 and target[6] == 3
        assert norm != target
        count += 1
    assert count == 128 and possible_mid == {1}
    checks.append('All 128 parity-compatible q mod 4 fail Delta(t^2)=q(t)q(-t)')

    print(json.dumps({
        'status': 'PASS',
        'arithmetic': 'exact sparse rational polynomial identities and finite-ring arithmetic',
        'controls': checks,
        'monic_binary_trial_factors': len(trial_factors),
        'norm_candidates_mod4': count,
        'norm_middle_residues_mod4': sorted(possible_mid),
        'required_middle_residue_mod4': target[6],
        'angle_derivative_lower_bound': '6/25',
        'limits': [
            'No universal proof or counterexample to KP-1.87.',
            'No computer verification of analytic Lojasiewicz or isotopy theorems.',
            'The Alexander polynomial of 8_16, its fibering, the periodicity criteria, and the Newton classification are credited source inputs.',
            'The mod-4 norm check does not claim full irreducibility of Delta(t^2) over Q.',
            'The finite parity loop is illustrative; the proof for every k is the displayed congruence.',
            'No source PDFs, imported corpus, or network fetches are needed for these controls.'
        ]
    }, indent=2))


if __name__ == '__main__':
    main()
