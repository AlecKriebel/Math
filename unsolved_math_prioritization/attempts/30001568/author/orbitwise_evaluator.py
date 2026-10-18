#!/usr/bin/env python3
"""Exact finite-jet implementation of a credited GPZ evaluator application.

This is supporting code, not an independent verification of the proof.
Dependencies: Python 3 and SymPy.  No network or external state changes.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import product, permutations
import json
import sympy as sp


class Evaluator:
    def __init__(self, dimension, inner_product):
        self.d = dimension
        self.x = sp.symbols(f"x0:{dimension}")
        self.Q = sp.Matrix(inner_product)
        if self.Q.shape != (dimension, dimension) or self.Q != self.Q.T:
            raise ValueError("Q must be a symmetric d by d rational matrix")
        if any(not q.is_Rational for q in self.Q):
            raise ValueError("Q must have rational entries")
        if any(self.Q[:k, :k].det() <= 0 for k in range(1, dimension + 1)):
            raise ValueError("Q must be positive definite")

    def linear(self, v):
        return sum(sp.Rational(a) * x for a, x in zip(v, self.x))

    @staticmethod
    def normalize_denominators(vectors):
        """Return a scalar and normalized distinct factors with multiplicities."""
        scalar = sp.S.One
        factors = {}
        for v in vectors:
            v = tuple(map(sp.Rational, v))
            first = next((a for a in v if a), None)
            if first is None:
                raise ValueError("A binomial exponent vector cannot be zero")
            v = tuple(a / first for a in v)
            scalar /= first
            factors[v] = factors.get(v, 0) + 1
        return scalar, tuple(sorted(factors.items()))

    def degree_zero(self, polynomial, denominator_vectors):
        """E_Q(P / product L_b), for homogeneous deg(P)=number of factors."""
        if any(len(v) != self.d for v in denominator_vectors):
            raise ValueError("All denominator vectors must have dimension d")
        scalar, factors = self.normalize_denominators(denominator_vectors)
        polynomial = sp.expand(scalar * polynomial)
        degree = len(denominator_vectors)
        if polynomial and any(sum(m) != degree for m, c in sp.Poly(polynomial, *self.x).terms() if c):
            raise ValueError("Numerator must be homogeneous of denominator degree")
        return sp.factor(self._reduce(polynomial, factors))

    @lru_cache(maxsize=None)
    def _reduce(self, polynomial, factors):
        polynomial = sp.expand(polynomial)
        if polynomial == 0:
            return sp.S.Zero
        if not factors:
            return polynomial.subs(dict.fromkeys(self.x, 0))
        vectors = [sp.Matrix(v) for v, s in factors]
        B = sp.Matrix.hstack(*vectors)
        relations = B.nullspace()
        if relations:
            # 1/prod L_i^s_i = sum_i c_i/(L_p^(s_p+1) L_i^(s_i-1) ...).
            # The relation and pivot depend only on support, not multiplicities.
            relation = relations[0]
            pivot = next(i for i, c in enumerate(relation) if c)
            total = sp.S.Zero
            for i, c in enumerate(relation):
                if i == pivot or c == 0:
                    continue
                new = dict(factors)
                new[factors[pivot][0]] += 1
                new[factors[i][0]] -= 1
                new_factors = tuple((v, s) for v, s in sorted(new.items()) if s)
                total += (-c / relation[pivot]) * self._reduce(polynomial, new_factors)
            return sp.factor(total)

        # Independent support. Use Q-orthogonal complementary numerator variables.
        complement = (B.T * self.Q).nullspace()
        M = sp.Matrix.hstack(*vectors, *complement)
        assert M.shape == (self.d, self.d) and M.det() != 0
        y = sp.symbols(f"y0:{self.d}")
        x_of_y = M.T.inv() * sp.Matrix(y)
        transformed = sp.Poly(sp.expand(polynomial.subs(dict(zip(self.x, x_of_y)), simultaneous=True)), *y)
        k = len(factors)
        quotients = [sp.S.Zero] * k
        for exponents, coefficient in transformed.terms():
            first = next((i for i in range(k) if exponents[i]), None)
            if first is None:
                # A numerator depending only on U-perp gives a polar germ.
                continue
            powers = list(exponents)
            powers[first] -= 1
            quotients[first] += coefficient * sp.prod(t ** n for t, n in zip(y, powers))
        y_of_x = M.T * sp.Matrix(self.x)
        total = sp.S.Zero
        for i, quotient in enumerate(quotients):
            if quotient == 0:
                continue
            numerator = sp.expand(quotient.subs(dict(zip(y, y_of_x)), simultaneous=True))
            new = dict(factors)
            new[factors[i][0]] -= 1
            new_factors = tuple((v, s) for v, s in sorted(new.items()) if s)
            total += self._reduce(numerator, new_factors)
        return sp.factor(total)

    def term(self, exponent, denominator_vectors, center=None):
        """Evaluate exp((a-c).x)/prod(1-exp(b.x)) via its finite numerator jet."""
        a = tuple(map(sp.Rational, exponent))
        if len(a) != self.d or any(len(b) != self.d for b in denominator_vectors):
            raise ValueError("All exponent vectors must have dimension d")
        center = tuple(map(sp.Rational, center if center is not None else [0] * self.d))
        if len(center) != self.d:
            raise ValueError("The center must have dimension d")
        m = len(denominator_vectors)
        if m == 0:
            return sp.S.One
        z = sp.Symbol("jet_parameter")
        A = self.linear([u-v for u, v in zip(a, center)])
        jet = sum(A**k * z**k / sp.factorial(k) for k in range(m+1))
        for b in denominator_vectors:
            L = self.linear(b)
            if L == 0:
                raise ValueError("A binomial exponent vector cannot be zero")
            # SymPy's Bernoulli polynomial at 0 gives B_1=-1/2.
            todd = sum(sp.bernoulli(k, 0) * L**k * z**k / sp.factorial(k) for k in range(m+1))
            jet = sp.Poly(sp.expand(jet * todd), z)
            jet = sum(c * z**mon[0] for mon, c in jet.terms() if mon[0] <= m)
        numerator = (-1)**m * sp.expand(jet).coeff(z, m)
        return self.degree_zero(numerator, denominator_vectors)


def self_test():
    tests = []
    def check(name, got, expected):
        difference = sp.simplify(got - expected)
        if difference != 0:
            raise AssertionError((name, got, expected, difference))
        tests.append({"test": name, "actual": str(got), "expected": str(expected), "passed": True})

    one = Evaluator(1, [[1]])
    check("monomial_no_poles", one.term([-4], [], [sp.Rational(7,3)]), 1)
    check("half_line", one.term([0], [[1]]), sp.Rational(1, 2))
    for N in [0, 1, 2, 7]:
        check(f"affine_segment_{N}", 2*one.term([0], [[1]], [sp.Rational(N,2)]), N+1)
    for a in [-3, 0, 4]:
        check(f"inverse_binomial_identity_{a}", one.term([a], [[2]]), -one.term([a-2], [[-2]]))

    two = Evaluator(2, [[2, 1], [1, 2]])
    x, y = two.x
    check("nonorthogonal_numerator_x_over_y", two.degree_zero(x, [[0,1]]), sp.Rational(1,2))
    check("dependent_pole_polynomial_identity", two.degree_zero(x*y*(x+y), [[1,0],[0,1],[1,1]]), 1)
    check("repeated_pole_identity", two.degree_zero(x*x*y, [[1,0],[1,0],[0,1]]), 1)
    check("opposite_proportional_poles", two.degree_zero(-2*x*x, [[1,0],[-2,0]]), 1)
    check("geometric_cancellation_regular_value",
          two.term([2,-1], [[1,2]], [sp.Rational(1,3), sp.Rational(2,5)])
          - two.term([7,9], [[1,2]], [sp.Rational(1,3), sp.Rational(2,5)]), 5)

    # S3 acts affinely by permuting barycentric coordinates (N-x-y,x,y).
    for N in [0, 1, 2, 5]:
        center = [sp.Rational(N,3)] * 2
        weight = two.term([0,0], [[1,0],[0,1]], center)
        check(f"triangle_orbit_count_{N}", 3*weight, sp.Rational((N+1)*(N+2),2))
        check(f"triangle_vertex_2_{N}", two.term([N,0], [[-1,0],[-1,1]], center), weight)
        check(f"triangle_vertex_3_{N}", two.term([0,N], [[0,-1],[1,-1]], center), weight)

    for d in [2, 3]:
        cube = Evaluator(d, sp.eye(d))
        directions = [list(sp.eye(d)[:,j]) for j in range(d)]
        for N in [1, 4]:
            weight = cube.term([0]*d, directions, [sp.Rational(N,2)]*d)
            check(f"cube_{d}_{N}", 2**d*weight, (N+1)**d)

    # A genuinely dependent-pole seed and its image under a Q-isometry.
    A = sp.Matrix([[-1,-1],[0,1]])
    assert A.T*two.Q*A == two.Q
    seed_a = sp.Matrix([2,-1])
    seed_b = [sp.Matrix(v) for v in [[1,0],[0,1],[1,1],[1,0]]]
    check("dependent_pole_group_covariance",
          two.term(list(A*seed_a), [list(A*b) for b in seed_b]),
          two.term(list(seed_a), [list(b) for b in seed_b]))

    # Covariance under a nonorthogonal change of lattice basis, transforming Q.
    T = sp.Matrix([[1,2],[0,1]])
    new_Q = T.inv().T * two.Q * T.inv()
    transformed = Evaluator(2, new_Q)
    check("change_of_basis_covariance",
          transformed.term(list(T*seed_a), [list(T*b) for b in seed_b]),
          two.term(list(seed_a), [list(b) for b in seed_b]))
    return {"scope": "Author diagnostic checks only; not independent review", "sympy_version": sp.__version__, "passed": len(tests), "tests": tests}


if __name__ == "__main__":
    print(json.dumps(self_test(), indent=2))
