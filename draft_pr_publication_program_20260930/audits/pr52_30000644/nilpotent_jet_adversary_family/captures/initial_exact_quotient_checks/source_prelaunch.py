#!/usr/bin/env python3
"""Handwritten sparse exact quotient-ring jet checks; no author-code imports.

Coordinates of monomials are (t,u,v,y_1,...,y_n). Coefficient rings are
Q, Q[u]/u^2, Q[u,v]/(u^3,v^2), Q[u,v]/uv and Q[u]/(u^2-u).
Only t is truncated; polynomial coordinate degrees are never truncated.
"""
import itertools
import json
import math
from fractions import Fraction as Q
from functools import lru_cache

CHECKS = 0
def check(condition, description):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(description)

class Algebra:
    def __init__(self, n, kind, m=None):
        self.n, self.kind, self.m, self.k = n, kind, m, n + 3
        self.zero = {}
        self.one = self.mono((0,) * self.k)
        self.t = self.variable(0)
        self.u = self.variable(1)
        self.v = self.variable(2)
        self.y = tuple(self.variable(i + 3) for i in range(n))

    def normal(self, e):
        e = list(e)
        if self.m is not None and e[0] >= self.m:
            return None
        if self.kind == 'Q' and (e[1] or e[2]): return None
        if self.kind == 'dual' and (e[1] >= 2 or e[2]): return None
        if self.kind == 'mixed' and (e[1] >= 3 or e[2] >= 2): return None
        if self.kind == 'nodal' and e[1] and e[2]: return None
        if self.kind == 'idempotent':
            if e[2]: return None
            e[1] = min(e[1], 1)
        return tuple(e)

    def mono(self, e, c=1):
        e = self.normal(e)
        return {} if e is None or not c else {e: Q(c)}

    def variable(self, i):
        e = [0] * self.k
        e[i] = 1
        return self.mono(e)

    def scalar(self, c): return self.mono((0,) * self.k, c)
    def add(self, *polys):
        out = {}
        for p in polys:
            for e, c in p.items():
                out[e] = out.get(e, Q(0)) + c
                if not out[e]: del out[e]
        return out

    def scale(self, p, c): return {e: a * c for e, a in p.items() if a * c}
    def neg(self, p): return self.scale(p, -1)
    def sub(self, p, q): return self.add(p, self.neg(q))
    def mul(self, p, q):
        out = {}
        for e, a in p.items():
            for f, b in q.items():
                g = self.normal(tuple(x + y for x, y in zip(e, f)))
                if g is None: continue
                out[g] = out.get(g, Q(0)) + a * b
                if not out[g]: del out[g]
        return out

    def power(self, p, n):
        out = self.one
        while n:
            if n % 2: out = self.mul(out, p)
            p = self.mul(p, p)
            n //= 2
        return out

    def substitute(self, p, ys):
        out = {}
        powers = {}
        for e, c in p.items():
            base = self.mono(e[:3] + (0,) * self.n, c)
            for i, d in enumerate(e[3:]):
                key = (i, d)
                if key not in powers: powers[key] = self.power(ys[i], d)
                base = self.mul(base, powers[key])
            out = self.add(out, base)
        return out

    def compose(self, f, g):
        """Point-map convention: f o g evaluates f at g."""
        return tuple(self.substitute(p, g) for p in f)

    def derivative(self, p, i):
        out = {}
        for e, c in p.items():
            if e[i + 3]:
                f = list(e)
                f[i + 3] -= 1
                out[tuple(f)] = c * e[i + 3]
        return out

    def integrate(self, p, i):
        out = {}
        for e, c in p.items():
            f = list(e)
            f[i + 3] += 1
            out[tuple(f)] = c / f[i + 3]
        return out

    def determinant(self, matrix):
        out = {}
        for perm in itertools.permutations(range(len(matrix))):
            sign = (-1) ** sum(perm[i] > perm[j]
                              for i in range(len(perm))
                              for j in range(i + 1, len(perm)))
            term = self.scalar(sign)
            for i, j in enumerate(perm): term = self.mul(term, matrix[i][j])
            out = self.add(out, term)
        return out

    def jacobian(self, f):
        return self.determinant([[self.derivative(p, j) for j in range(self.n)]
                                 for p in f])

    def divergence(self, f):
        return self.add(*(self.derivative(p, i) for i, p in enumerate(f)))

    def transfer(self, p):
        out = {}
        for e, c in p.items(): out = self.add(out, self.mono(e, c))
        return out

    def coefficient(self, p, r):
        return { (0,) + e[1:]: c for e, c in p.items() if e[0] == r }

    def congruent_identity(self, f, r):
        return all(all(e[0] >= r for e in self.sub(p, y))
                   for p, y in zip(f, self.y))

@lru_cache(None)
def interpolation(d, b):
    """Solve binary-power coefficient matrix over Q, never over coefficient R."""
    a = [[Q(math.comb(d, j) * q ** j) for q in range(d + 1)]
         + [Q(int(j == b))] for j in range(d + 1)]
    for i in range(d + 1):
        pivot = next(j for j in range(i, d + 1) if a[j][i])
        a[i], a[pivot] = a[pivot], a[i]
        c = a[i][i]
        a[i] = [x / c for x in a[i]]
        for j in range(d + 1):
            if i != j:
                c = a[j][i]
                a[j] = [x - c * y for x, y in zip(a[j], a[i])]
    return tuple(row[-1] for row in a)

def shear_decomposition(a, f):
    """Return finite (h,constant rational direction) list with sum h v=F."""
    check(not a.divergence(f), 'input coefficient must have zero divergence')
    if a.n == 1:
        check(not a.derivative(f[0], 0), 'one-variable coefficient is constant')
        return [(f[0], (Q(1),))] if f[0] else []
    rest = list(f)
    shears = []
    last = a.n - 1
    for i in range(last):
        hamiltonian = a.integrate(rest[i], last)
        check(a.derivative(hamiltonian, last) == rest[i], 'termwise integral')
        rest[i] = {}
        rest[last] = a.add(rest[last], a.derivative(hamiltonian, i))
        for e, c in hamiltonian.items():
            alpha, beta = e[i + 3], e[last + 3]
            d = alpha + beta
            if not d: continue
            base = list(e)
            base[i + 3] = base[last + 3] = 0
            coefficient = a.mono(base, c)
            for q, weight in enumerate(interpolation(d, beta)):
                if not weight: continue
                linear = a.add(a.y[i], a.scale(a.y[last], q))
                h = a.scale(a.mul(coefficient, a.power(linear, d - 1)), weight * d)
                v = [Q(0)] * a.n
                v[i], v[last] = Q(q), Q(-1)
                shears.append((h, tuple(v)))
    check(not a.derivative(rest[last], last), 'last remainder independent of last variable')
    if rest[last]:
        v = [Q(0)] * a.n
        v[last] = Q(1)
        shears.append((rest[last], tuple(v)))
    rebuilt = tuple(a.add(*(a.scale(h, v[i]) for h, v in shears))
                    for i in range(a.n))
    check(rebuilt == f, 'exact divergence-free decomposition')
    return shears

def shear(a, h, v, r=0, sign=1):
    factor = a.mul(a.power(a.t, r), h)
    return tuple(a.add(y, a.scale(factor, sign * c)) for y, c in zip(a.y, v))

def elementary(a, i, h, r=0, sign=1):
    v = tuple(Q(int(j == i)) for j in range(a.n))
    check(not a.derivative(h, i), 'elementary shear coefficient independent of target')
    return shear(a, h, v, r, sign)

def base_map(a, variant=0):
    if a.n == 1:
        h = a.add(a.scalar(2), a.u)
        return elementary(a, 0, h), elementary(a, 0, h, sign=-1)
    if variant == 1 and a.n == 3:
        x, y, z = a.y
        delta = a.add(a.mul(x, z), a.power(y, 2))
        f = (a.sub(a.sub(x, a.scale(a.mul(y, delta), 2)),
                   a.mul(z, a.power(delta, 2))), a.add(y, a.mul(z, delta)), z)
        inv = (a.sub(a.add(x, a.scale(a.mul(y, delta), 2)),
                     a.mul(z, a.power(delta, 2))), a.sub(y, a.mul(z, delta)), z)
        return f, inv
    p = elementary(a, 0, a.add(a.power(a.y[1], 2), a.u, a.scalar(1)))
    pi = elementary(a, 0, a.add(a.power(a.y[1], 2), a.u, a.scalar(1)), sign=-1)
    q = elementary(a, 1, a.add(a.y[0], a.v, a.scalar(2)))
    qi = elementary(a, 1, a.add(a.y[0], a.v, a.scalar(2)), sign=-1)
    return a.compose(p, q), a.compose(qi, pi)

def case(n, kind, m, variant=0):
    global_a = Algebra(n, kind)
    a = Algebra(n, kind, m)
    base, base_inv = base_map(global_a, variant)
    check(global_a.compose(base, base_inv) == global_a.y, 'base inverse right over R')
    check(global_a.compose(base_inv, base) == global_a.y, 'base inverse left over R')
    check(global_a.jacobian(base) == global_a.one, 'base Jacobian globally one')
    c, ci = tuple(map(a.transfer, base)), tuple(map(a.transfer, base_inv))
    target, inverse = c, ci
    generated = 0
    for r in range(1, m):
        for i in range(n):
            if n == 1:
                h = a.add(a.scalar(r), a.u, a.v)
            else:
                y = a.y[(i + 1) % n]
                h = a.add(y, a.mul(a.add(a.u, a.v), a.power(y, 2)), a.scalar(r))
            p, pi = elementary(a, i, h, r), elementary(a, i, h, r, -1)
            target, inverse = a.compose(target, p), a.compose(pi, inverse)
            generated += 1
    check(a.compose(target, inverse) == a.y, 'generated target inverse right')
    check(a.compose(inverse, target) == a.y, 'generated target inverse left')
    check(a.jacobian(target) == a.one, 'generated target determinant one')
    residual = a.compose(ci, target)
    accumulated, accumulated_inv = c, ci
    stages, genuine_factors = [], 0
    for r in range(1, m):
        check(a.congruent_identity(residual, r), 'residual belongs to expected jet subgroup')
        f = tuple(a.coefficient(a.sub(p, y), r) for p, y in zip(residual, a.y))
        check(not a.divergence(f), 'determinant condition forces divergence-free coefficient')
        phi, phi_inv = a.y, a.y
        pieces = shear_decomposition(a, f)
        for h, v in pieces:
            gh = global_a.transfer(h)
            gp, gi = shear(global_a, gh, v, r), shear(global_a, gh, v, r, -1)
            check(not global_a.add(*(global_a.scale(global_a.derivative(gh, i), v[i])
                                   for i in range(n))), 'global directional derivative zero')
            check(global_a.compose(gp, gi) == global_a.y, 'genuine polynomial inverse right')
            check(global_a.compose(gi, gp) == global_a.y, 'genuine polynomial inverse left')
            check(global_a.jacobian(gp) == global_a.one, 'genuine global determinant one')
            p, pi = tuple(map(a.transfer, gp)), tuple(map(a.transfer, gi))
            phi, phi_inv = a.compose(phi, p), a.compose(pi, phi_inv)
            genuine_factors += 1
        check(tuple(a.coefficient(a.sub(p, y), r) for p, y in zip(phi, a.y)) == f,
              'composition adds precisely required rth coefficients')
        check(a.compose(phi, phi_inv) == a.y, 'correction inverse in target')
        residual = a.compose(phi_inv, residual)
        accumulated = a.compose(accumulated, phi)
        accumulated_inv = a.compose(phi_inv, accumulated_inv)
        check(a.congruent_identity(residual, r + 1), 'correction kills next jet')
        check(a.compose(accumulated, residual) == target, 'ordered factorization preserved')
        check(a.compose(accumulated, accumulated_inv) == a.y, 'accumulated inverse order')
        stages.append({'r': r, 'divergence_free': True, 'genuine_factors': len(pieces)})
    check(residual == a.y, 'finite induction terminates with identity')
    check(accumulated == target, 'certificate product reduces to target')
    check(a.compose(accumulated_inv, accumulated) == a.y, 'final inverse left')
    return {'n': n, 'ring': kind, 'm': m, 'base_variant': variant,
            'generated_target_factors': generated, 'genuine_correction_factors': genuine_factors,
            'stages': stages, 'target_terms': sum(map(len, target))}

def controls():
    a = Algebra(2, 'Q', 4)
    x, y = a.y
    p, pi = elementary(a, 0, a.power(y, 2), 1), elementary(a, 0, a.power(y, 2), 1, -1)
    q, qi = elementary(a, 1, x, 1), elementary(a, 1, x, 1, -1)
    composed = a.compose(p, q)
    linear_sum = tuple(a.add(z, a.sub(f, z), a.sub(g, z)) for z, f, g in zip(a.y, p, q))
    cross = a.sub(composed[0], linear_sum[0])
    expected = a.add(a.scale(a.mul(a.power(a.t, 2), a.mul(x, y)), 2),
                     a.mul(a.power(a.t, 3), a.power(x, 2)))
    check(cross == expected and bool(cross), 'retained 2r cross terms are nonzero')
    check(a.compose(composed, a.compose(pi, qi)) != a.y, 'wrong inverse factor order rejected')
    check(a.compose(composed, a.compose(qi, pi)) == a.y, 'correct inverse factor order accepted')
    c = elementary(a, 0, a.power(y, 2))
    ci = elementary(a, 0, a.power(y, 2), sign=-1)
    sigma = a.compose(c, q)
    wrong_residual = a.compose(sigma, ci)
    check(a.compose(c, wrong_residual) != sigma, 'wrong side of base normalization rejected')
    check(a.compose(ci, sigma) == q, 'correct side of base normalization accepted')
    dual = Algebra(1, 'dual', 3)
    check(bool(dual.mul(dual.u, dual.t)), 't coefficient with nilpotent u is nonzero')
    check(not dual.mul(dual.power(dual.t, 2), dual.t), 't is a zero divisor in target')
    bad = (dual.add(dual.y[0], dual.mul(dual.t, dual.mul(dual.u, dual.y[0]))),)
    check(dual.jacobian(bad) != dual.one, 'nonzero nilpotent determinant defect rejected')
    check(bool(dual.derivative(dual.mul(dual.u, dual.power(dual.y[0], 2)), 0)),
          'nilpotent coefficient does not erase characteristic-zero derivative')
    idem = Algebra(1, 'idempotent', 3)
    check(not idem.mul(idem.u, idem.sub(idem.one, idem.u)), 'orthogonal nonzero idempotents')
    check(bool(idem.u) and bool(idem.sub(idem.one, idem.u)), 'both zero-divisor factors nonzero')
    nodal = Algebra(1, 'nodal', 3)
    check(not nodal.mul(nodal.u, nodal.v) and bool(nodal.u) and bool(nodal.v),
          'reduced nodal coefficient ring has zero divisors')
    # The coefficient of t^r is extractable for every r<m even though t is nonunit.
    for ring in ('dual', 'mixed', 'nodal', 'idempotent'):
        b = Algebra(1, ring, 5)
        for r in range(5):
            f = b.add(b.u, b.v, b.scalar(Q(2, 3)))
            check(b.coefficient(b.mul(b.power(b.t, r), f), r) == f,
                  'unique t coefficient over nonreduced or zero-divisor ring')
    return {'negative_controls': ['drop cross terms past first jet', 'wrong inverse order',
                                  'wrong base normalization side', 'ignore nilpotent determinant defect'],
            'boundary_controls': ['unique t coefficients without cancelling t',
                                  'characteristic-zero nilpotent derivative',
                                  'orthogonal idempotents', 'reduced nodal zero divisors']}

def main():
    cases = []
    for n in (1, 2, 3):
        for kind in ('Q', 'dual', 'mixed', 'nodal', 'idempotent'):
            for m in (1, 2, 3, 4):
                cases.append(case(n, kind, m))
    cases.append(case(3, 'dual', 3, 1))
    control = controls()
    print(json.dumps({'schema': 'pr52-independent-nilpotent-jet-checks/v1', 'status': 'PASS',
                      'assertions': CHECKS, 'case_count': len(cases), 'cases': cases,
                      'controls': control,
                      'scope': 'Exact finite corroboration. Universal proof is a separate artifact. '
                               'A finite word of globally verified shears certifies the lift; '
                               'the potentially enormous global product is not expanded.'},
                     sort_keys=True, indent=2))

if __name__ == '__main__': main()
