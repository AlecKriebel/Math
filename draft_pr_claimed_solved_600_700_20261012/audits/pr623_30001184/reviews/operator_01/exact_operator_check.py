#!/usr/bin/env python3
"""Independent exact check in Q(sqrt(2),sqrt(3),sqrt(5)); no packet imports.

This verifies finite algebraic identities only. Universal time, topology,
generation and GNS claims are proved in FINDINGS.md, not inferred from sampling.
"""
from fractions import Fraction as F
import json

RADICANDS = (2, 3, 5)
COUNT = 0


class K:
    def __init__(self, terms=0):
        if isinstance(terms, K):
            self.c = terms.c
        elif isinstance(terms, dict):
            self.c = tuple(F(terms.get(i, 0)) for i in range(8))
        else:
            self.c = (F(terms),) + (F(0),) * 7

    def __add__(self, other):
        o = K(other)
        return K({i: self.c[i] + o.c[i] for i in range(8)})

    __radd__ = __add__

    def __neg__(self):
        return K({i: -self.c[i] for i in range(8)})

    def __sub__(self, other):
        return self + -K(other)

    def __rsub__(self, other):
        return K(other) + -self

    def __mul__(self, other):
        o = K(other)
        result = {i: F(0) for i in range(8)}
        for i, a in enumerate(self.c):
            for j, b in enumerate(o.c):
                common = i & j
                factor = 1
                for bit, value in enumerate(RADICANDS):
                    if common & (1 << bit):
                        factor *= value
                result[i ^ j] += a * b * factor
        return K(result)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.c == K(other).c

    def json(self):
        return {str(i): str(v) for i, v in enumerate(self.c) if v}


def root(mask):
    return K({mask: 1})


def matrix(rows):
    return tuple(tuple(K(x) for x in row) for row in rows)


def mt(a):
    return tuple(tuple(a[j][i] for j in range(2)) for i in range(2))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def ma(a, b):
    return tuple(tuple(a[i][j] + b[i][j] for j in range(2)) for i in range(2))


def ms(s, a):
    return tuple(tuple(s * x for x in row) for row in a)


def conj(u, a):
    return mm(mm(u, a), mt(u))


def expect(a, b, message):
    global COUNT
    assert a == b, message
    COUNT += 1


def main():
    global COUNT
    I = matrix([[1, 0], [0, 1]])
    O = matrix([[0, 0], [0, 0]])
    q = matrix([[1, 0], [0, 0]])
    qp = matrix([[0, 0], [0, 1]])
    e12 = matrix([[0, 1], [0, 0]])
    e21 = mt(e12)
    sqrt3, sqrt5 = root(2), root(4)

    # Independently select the rotations by their exact double-angle cosines.
    c1, s1 = sqrt3 * F(1, 2), K(F(1, 2))
    c2, s2 = root(5) * F(1, 4), root(3) * F(1, 4)
    R1 = matrix([[c1, -s1], [s1, c1]])
    R2 = matrix([[c2, -s2], [s2, c2]])
    expect(mm(mt(R1), R1), I, 'R1 is orthogonal')
    expect(mm(mt(R2), R2), I, 'R2 is orthogonal')
    expect(c1 * c1 - s1 * s1, F(1, 2), 'exp(-log 2)')
    expect(c2 * c2 - s2 * s2, F(1, 4), 'exp(-2 log 2)')

    Q = conj(R1, q)
    expect(Q, matrix([[F(3, 4), sqrt3 * F(1, 4)],
                      [sqrt3 * F(1, 4), F(1, 4)]]), 'evaluated shifted q')
    expect(mm(Q, Q), Q, 'Q is a projection')
    expect(mm(mm(q, Q), qp), ms(sqrt3 * F(1, 4), e12), 'GNS cyclic e12')
    expect(mm(mm(qp, Q), q), ms(sqrt3 * F(1, 4), e21), 'GNS cyclic e21')

    # At x=log 2, the cocycle is R1^* R2, without numerical angles.
    Rdelta = mm(mt(R1), R2)
    Qx = conj(Rdelta, q)
    d = (sqrt5 - 1) * F(3, 16)
    expect(Qx[0][0], (9 + 3 * sqrt5) * F(1, 16), 'shifted upper entry')
    a0 = ma(mm(mm(q, Q), q), ms(K(F(-3, 4)), q))
    ax = ma(mm(mm(q, Qx), q), ms(K(F(-3, 4)), q))
    expect(a0, O, 'true representation kernel at x=0')
    expect(ax, ms(d, q), 'nonzero witness at x=log 2')
    shifted_a0 = conj(R1, ax)
    expect(shifted_a0, ms(d, Q), 'nonzero represented evolved witness')
    expect(mm(shifted_a0, shifted_a0), ms(d * d, Q), 'positive square witness')
    expect(mm(a0, a0), O, 'positive square initially in kernel')
    expect(shifted_a0[0][0], d * F(3, 4), 'expectation first coordinate')
    expect(shifted_a0[1][1], d * F(1, 4), 'expectation second coordinate')

    # Exact Markov idempotent decomposition at selected times. The universal
    # calculation is carried out symbolically in the accompanying proof.
    J = matrix([[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]])
    H = matrix([[F(1, 2), F(-1, 2)], [F(-1, 2), F(1, 2)]])
    expect(mm(J, J), J, 'stationary idempotent')
    expect(mm(H, H), H, 'decaying idempotent')
    expect(mm(J, H), O, 'orthogonal spectral components')
    expect(mm(H, J), O, 'reverse orthogonal spectral components')
    P = ma(J, ms(K(F(1, 2)), H))
    expect(mm(P, P), ma(J, ms(K(F(1, 4)), H)), 'Markov exact time addition')
    expect(d * d, (54 - 18 * sqrt5) * F(1, 256), 'square coefficient')

    print(json.dumps({
        'status': 'PASS', 'exact_assertions': COUNT,
        'field': 'Q(sqrt(2),sqrt(3),sqrt(5)); basis indexed by radical masks',
        'imports_packet_code': False,
        'd': d.json(),
        'd_positive_proof': 'sqrt(5)>1, so 3(sqrt(5)-1)/16>0',
        'shifted_a_eval0': [[x.json() for x in row] for row in shifted_a0],
        'limitations': 'Finite exact identities only; no time samples used as a universal proof.'
    }, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
