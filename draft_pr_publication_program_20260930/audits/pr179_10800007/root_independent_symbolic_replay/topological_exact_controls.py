#!/usr/bin/env python3
"""Exact symbolic controls for the independent topological audit.

This does not infer nonexistence of sections from computation. The topology is
proved in MATHEMATICAL_AUDIT.md. Uses Python's standard library only.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json


class Poly:
    def __init__(self, n, terms=None):
        self.n = n
        self.terms = {e: Q(c) for e, c in (terms or {}).items() if c}

    @classmethod
    def constant(cls, n, c):
        return cls(n, {(0,) * n: Q(c)})

    @classmethod
    def variable(cls, n, i):
        e = [0] * n
        e[i] = 1
        return cls(n, {tuple(e): 1})

    def coerce(self, p):
        if isinstance(p, Poly):
            assert p.n == self.n
            return p
        return Poly.constant(self.n, p)

    def __add__(self, p):
        p = self.coerce(p)
        out = self.terms.copy()
        for e, c in p.terms.items():
            out[e] = out.get(e, 0) + c
        return Poly(self.n, out)

    __radd__ = __add__

    def __neg__(self):
        return Poly(self.n, {e: -c for e, c in self.terms.items()})

    def __sub__(self, p):
        return self + -self.coerce(p)

    def __rsub__(self, p):
        return self.coerce(p) + -self

    def __mul__(self, p):
        p = self.coerce(p)
        out = {}
        for a, c in self.terms.items():
            for b, d in p.terms.items():
                e = tuple(x + y for x, y in zip(a, b))
                out[e] = out.get(e, 0) + c * d
        return Poly(self.n, out)

    __rmul__ = __mul__

    def __pow__(self, k):
        assert isinstance(k, int) and k >= 0
        out = Poly.constant(self.n, 1)
        for _ in range(k):
            out = out * self
        return out

    def __eq__(self, p):
        return self.terms == self.coerce(p).terms


checks = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


# Symbolic identities, with all six variables indeterminate.
x, y, h, k, u, v = [Poly.variable(6, i) for i in range(6)]
f = x*x - y*y - 2*h*x + 2*k*y + h*h - k*k - u
g = x*y - k*x - h*y + h*k - Q(1, 2)*v
check('translated_slice_real_identity', f == (x-h)**2 - (y-k)**2 - u)
check('translated_slice_imaginary_identity', 2*g == 2*(x-h)*(y-k) - v)
det = (2*x - 2*h)*(x-h) - (-2*y + 2*k)*(y-k)
check('translated_slice_jacobian', det == 2*((x-h)**2 + (y-k)**2))

# Exact general complex-coordinate change H=f+2*i*g=z^2+alpha*z+beta*conj(z)+gamma.
x, y, a1, a2, a0, b1, b2, b0 = [Poly.variable(8, i) for i in range(8)]
ar, ai = Q(1, 2)*a1 + b2, b1 - Q(1, 2)*a2
br, bi = Q(1, 2)*a1 - b2, b1 + Q(1, 2)*a2
lin_re = (ar*x - ai*y) + (br*x + bi*y)
lin_im = (ar*y + ai*x) + (-br*y + bi*x)
check('all_coefficients_complex_real_identity', lin_re == a1*x + a2*y)
check('all_coefficients_complex_imaginary_identity', lin_im == 2*b1*x + 2*b2*y)


def mm(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


# A faithful 4-dimensional quotient representation for x^2-y^2=xy=0.
X = [[0,0,0,0], [1,0,0,0], [0,0,0,0], [0,1,0,0]]
Y = [[0,0,0,0], [0,0,0,0], [1,0,0,0], [0,0,1,0]]
zero = [[0]*4 for _ in range(4)]
check('quotient_relations_X2_equals_Y2', mm(X,X) == mm(Y,Y))
check('quotient_relations_XY_equals_YX_zero', mm(X,Y) == mm(Y,X) == zero)
check('quotient_nilpotence', mm(mm(X,X),X) == mm(mm(Y,Y),Y) == zero)
columns = [[int(i == j) for i in range(4)] for j in range(4)]
e0 = columns[0]
def mv(A, z):
    return [sum(A[i][j]*z[j] for j in range(4)) for i in range(4)]
check('quotient_four_independent_monomial_vectors', [e0,mv(X,e0),mv(Y,e0),mv(mm(Y,Y),e0)] == columns)


def system(p, x, y):
    a1,a2,a0,b1,b2,b0 = p
    return x*x-y*y+a1*x+a2*y+a0, x*y+b1*x+b2*y+b0


def jacobian(p, x, y):
    a1,a2,_,b1,b2,_ = p
    return (2*x+a1)*(x+b2) - (-2*y+a2)*(y+b1)


# A nonzero coefficient with the same fatal translated square-root degeneration.
p = (Q(-2),Q(0),Q(1),Q(0),Q(-1),Q(0))
check('punctured_six_space_still_contains_bad_value', any(p) and system(p,Q(1),Q(0)) == (0,0))
check('translated_bad_root_singular', jacobian(p,Q(1),Q(0)) == 0)

# A singular fiber that nevertheless has a simple root available for a section.
p = (Q(1),Q(0),Q(-3,4),Q(0),Q(-1,2),Q(0))
check('mixed_fiber_singular_root', system(p,Q(1,2),Q(0)) == (0,0) and jacobian(p,Q(1,2),Q(0)) == 0)
check('mixed_fiber_simple_escape_root', system(p,Q(-3,2),Q(0)) == (0,0) and jacobian(p,Q(-3,2),Q(0)) == 4)

out = {
    'status': 'PASS',
    'exact_checks': len(checks),
    'checks': checks,
    'scope': 'Polynomial identities and exact boundary examples; not a computational proof of nonexistence or continuity.',
    'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
Path(__file__).with_name('exact_controls_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
