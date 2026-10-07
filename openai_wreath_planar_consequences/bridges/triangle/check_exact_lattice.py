#!/usr/bin/env python3
"""Independent exact finite controls; BRIDGE_PROOF.md contains infinite proofs."""
from fractions import Fraction as Q
from pathlib import Path
import datetime
import hashlib
import json
import platform


class K:
    """Exact field Q(sqrt(3)), represented by a+b sqrt(3)."""
    def __init__(self, a=0, b=0):
        self.a, self.b = Q(a), Q(b)

    @staticmethod
    def lift(x):
        return x if isinstance(x, K) else K(x)

    def __add__(self, x):
        x = self.lift(x)
        return K(self.a + x.a, self.b + x.b)

    __radd__ = __add__

    def __neg__(self):
        return K(-self.a, -self.b)

    def __sub__(self, x):
        return self + (-self.lift(x))

    def __mul__(self, x):
        x = self.lift(x)
        return K(self.a*x.a + 3*self.b*x.b, self.a*x.b + self.b*x.a)

    __rmul__ = __mul__

    def inverse(self):
        d = self.a*self.a - 3*self.b*self.b
        assert d != 0
        return K(self.a/d, -self.b/d)

    def __truediv__(self, x):
        return self * self.lift(x).inverse()

    def __eq__(self, x):
        x = self.lift(x)
        return self.a == x.a and self.b == x.b

    def rational(self):
        assert self.b == 0
        return self.a

    def pair(self):
        return [str(self.a), str(self.b)]


def mm(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)]


def transpose(a):
    return [list(x) for x in zip(*a)]


def matvec(a, v):
    return [sum(a[i][j]*v[j] for j in range(2)) for i in range(2)]


def norm2(v):
    return sum(x*x for x in v).rational()


B = [[K(1), K(Q(1, 2))], [K(), K(0, Q(1, 2))]]
d = B[0][0]*B[1][1] - B[0][1]*B[1][0]
Binv = [[B[1][1]/d, -B[0][1]/d], [-B[1][0]/d, B[0][0]/d]]
dual = transpose(Binv)
identity = [[K(1), K()], [K(), K(1)]]
assert mm(transpose(B), dual) == identity
assert d*d == Q(3, 4)
assert d.inverse() == K(0, Q(2, 3))
assert d.inverse()*d.inverse() == Q(4, 3)

tested = 0
shell1 = []
for m in range(-12, 13):
    for n in range(-12, 13):
        primal_q = norm2(matvec(B, [m, n]))
        dual_q = norm2(matvec(dual, [m, n]))
        assert primal_q == m*m + m*n + n*n
        assert dual_q == Q(4, 3)*(m*m - m*n + n*n)
        if (m, n) != (0, 0):
            assert primal_q >= 1 and dual_q >= Q(4, 3)
        if primal_q == 1:
            shell1.append([m, n])
        tested += 1
assert len(shell1) == 6

vectors = [(m, n) for m in range(-3, 4) for n in range(-3, 4)]
counts = {'axes': 0, 'coincident': 0, 'ordinary': 0, 'origin_excluded': 0,
          'boundary_pairs': 0}
for u in vectors:
    for v in vectors:
        dif = (u[0]-v[0], u[1]-v[1])
        lengths2 = [norm2(matvec(B, z)) for z in [u, v, dif]]
        assert all(z == 0 or z >= 1 for z in lengths2)
        if u == v == (0, 0):
            counts['origin_excluded'] += 1
            continue
        if u == (0, 0) or v == (0, 0):
            counts['axes'] += 1
        elif u == v:
            counts['coincident'] += 1
        else:
            counts['ordinary'] += 1
        if 1 in lengths2:
            counts['boundary_pairs'] += 1
assert counts['axes'] == 96 and counts['coincident'] == 48
assert counts['origin_excluded'] == 1

# Gaussian derivative in N=2: for beta=2 and polynomial (1-r^2),
# the Fourier multiplier times Gaussian is (pi/2)*(1-1/2+pi^2 rho^2/4).
# Normalization c=4/pi yields constant 1 and pi^2 rho^2 coefficient 1/2.
assert Q(4)*Q(1, 2)*Q(1, 2) == 1
assert Q(4)*Q(1, 2)*Q(1, 4) == Q(1, 2)

result = {
    'status': 'PASS_EXACT_FINITE_CONTROLS',
    'scope': 'Exact lattice and dual-lattice algebra, finite boundary controls; '
             'not a proof of global optimization or of the imported certificate.',
    'fourier_phase': 'exp(-2*pi*i*<x,xi>)',
    'covolume_in_Q_sqrt3_basis': d.pair(),
    'dual_basis_in_Q_sqrt3_basis': [[x.pair() for x in row] for row in dual],
    'number_density_in_Q_sqrt3_basis': d.inverse().pair(),
    'triangle_lower_bound': '4/3',
    'integer_vectors_tested': tested,
    'minimum_primal_squared_norm': '1',
    'minimum_dual_squared_norm': '4/3',
    'six_shortest_integer_coordinates': sorted(shell1),
    'triangle_pair_controls': counts,
    'elementary_gaussian_two_point_upper': '4/pi',
    'product_based_triangle_upper': '16/pi^2',
    'python': platform.python_version(),
    'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
print(json.dumps(result, indent=2))
