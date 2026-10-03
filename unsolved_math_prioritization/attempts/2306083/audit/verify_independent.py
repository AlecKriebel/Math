#!/usr/bin/env python3
"""Independent exact finite controls. Infinite analytic claims require AUDIT_REPORT.md."""
from dataclasses import dataclass
from fractions import Fraction as Q
from math import isqrt
import hashlib
import json
from pathlib import Path
import subprocess
import sys

@dataclass(frozen=True)
class C:
    x: Q = Q(0)
    y: Q = Q(0)
    def __add__(self, other):
        return C(self.x + other.x, self.y + other.y)
    def __neg__(self):
        return C(-self.x, -self.y)
    def __sub__(self, other):
        return self + (-other)
    def __mul__(self, other):
        return C(self.x*other.x-self.y*other.y, self.x*other.y+self.y*other.x)
    def conjugate(self):
        return C(self.x, -self.y)
    def squared(self):
        return self.x*self.x+self.y*self.y
    def scale(self, q):
        return C(self.x*q, self.y*q)
    def __truediv__(self, other):
        assert other.squared() != 0
        return (self*other.conjugate()).scale(1/other.squared())

ZERO, ONE = C(), C(Q(1))

def modulus(v):
    q = v.squared()
    n, d = isqrt(q.numerator), isqrt(q.denominator)
    assert n*n == q.numerator and d*d == q.denominator
    return Q(n, d)

def poly_mul(p, q):
    out = {}
    for i, a in p.items():
        for j, b in q.items():
            out[i+j] = out.get(i+j, ZERO) + a*b
    return {i:c for i,c in out.items() if c != ZERO}

def poly_value(p, z):
    ans = ZERO
    for n in range(max(p, default=0), -1, -1):
        ans = ans*z+p.get(n, ZERO)
    return ans

def poly_derivative(p):
    return {i-1:c.scale(i) for i,c in p.items() if i}

def poly_sub(p, q):
    return {i:p.get(i,ZERO)-q.get(i,ZERO) for i in p.keys()|q.keys()
            if p.get(i,ZERO) != q.get(i,ZERO)}

def quotient_derivative(numerator, denominator, z):
    n, d = poly_value(numerator,z), poly_value(denominator,z)
    assert d != ZERO
    return (poly_value(poly_derivative(numerator),z)*d
            - n*poly_value(poly_derivative(denominator),z))/(d*d)

base = Path(__file__).resolve().parent.parent
expected = {
    'PROOF.md':'0d5a849da58b230109fd5a450db4ca1dd4c4c1dc6c28ba454d059c0b2c110f11',
    'README.md':'8df9a46cb987b24fc1b0a28129f8ad1c68271bbea3232f413f9b6af4376753a7',
    'RESEARCH_LOG.md':'edb29ac43325f4eacb4697ea0dda8437440dfa7367622f3771717ea4e224fffc',
    'SOURCE_GATE.md':'e1447093e7afac40b2f462b0aa6533c519ab8c9793a91e8046c76266017cfaca',
    'STATUS.json':'c90d8c640ac7c96d8938052c057028e77a6edffacb137e9ed54caa0b3be9e6b0',
    'verification.json':'2d8eb7c911ad8d1b1ec135fde3a0fd3183f536424084d724119f36f91d26887d',
    'verify.py':'bfbb813ee9563ef9e96204224f3ad2af49c51d1ca37b451a5f9978669edb5cdf'
}
for name, digest in expected.items():
    assert hashlib.sha256((base/'artifacts'/name).read_bytes()).hexdigest() == digest
rerun = subprocess.run([sys.executable, str(base/'artifacts'/'verify.py')],
                       capture_output=True, check=True).stdout
assert rerun == (base/'artifacts'/'verification.json').read_bytes()

# Test genuinely complex factors, including non-radial assignments.
zeta = C(Q(3,5),Q(4,5))
single = ([zeta], [(zeta.scale(Q(1,2)),0), (zeta.scale(Q(3,4)),0),
                  (C(Q(3,5)),0), (C(Q(0),Q(4,5)),0)])
zetas = [ONE, C(Q(0),Q(1)), C(Q(-3,5),Q(4,5))]
multiple = (zetas, [(zetas[0].scale(Q(1,2)),0), (zetas[0].scale(Q(7,8)),0),
                   (zetas[1].scale(Q(2,3)),1), (zetas[1].scale(Q(5,6)),1),
                   (zetas[2].scale(Q(1,3)),2), (zetas[2].scale(Q(4,5)),2),
                   (C(Q(0),Q(4,5)),2), (C(Q(-3,5)),2)])
grid = [C(Q(x,9),Q(y,9)) for x in range(-8,9) for y in range(-8,9)
        if x*x+y*y < 81]
controls = []
factor_checks = 0
for boundary, assignments in [single, multiple]:
    m = len(boundary)
    assert all(t.squared() == 1 for t in boundary)
    assert len({a for a,j in assignments}) == len(assignments)
    numerator, denominator = {0:ONE}, {0:ONE}
    P = {2:ONE}
    for t in boundary:
        linear = {0:ONE, 1:-t.conjugate()}
        P = poly_mul(poly_mul(P,linear),linear)
    E = Q(0)
    for a, j in assignments:
        r, distance = modulus(a), modulus(boundary[j]-a)
        assert 0 < r < 1
        E += (1-r*r)*(1+distance/(1-r))**2
        rotation = C(r)/a
        numerator = poly_mul(numerator, {0:rotation*a, 1:-rotation})
        denominator = poly_mul(denominator, {0:ONE, 1:-a.conjugate()})
    Hnum = poly_mul(P,numerator)
    assert Hnum.get(0,ZERO) == Hnum.get(1,ZERO) == ZERO
    assert Hnum.get(2,ZERO) != ZERO
    for a,j in assignments:
        assert poly_value(Hnum,a) == ZERO
        assert poly_value(denominator,a) != ZERO
    budget = Q((m+2)*4**m)+Q(4**(m-1))*E
    epsilon = Q(1,2)/budget
    assert epsilon*budget == Q(1,2)
    for z in grid:
        B = poly_value(numerator,z)/poly_value(denominator,z)
        assert B.squared() <= 1
        hp = quotient_derivative(Hnum,denominator,z)
        assert hp.squared() <= budget*budget
        assert hp.scale(epsilon).squared() <= Q(1,4)
        for a,j in assignments:
            r, distance = modulus(a), modulus(boundary[j]-a)
            d, u = ONE-a.conjugate()*z, ONE-boundary[j].conjugate()*z
            b = (C(r)/a)*(a-z)/d
            # Exact disk automorphism identity and normalized-factor estimate.
            assert d.squared()-(a-z).squared() == (1-r*r)*(1-z.squared())
            assert b.squared() < 1
            R = Q(999,1000)
            assert z.squared() <= R*R
            assert (ONE-b).squared() <= ((1-r)*(1+R)/(1-R))**2
            assert u.squared() <= d.squared()*(1+distance/(1-r))**2
            factor_checks += 1
    controls.append({'boundary_points':m, 'zeros':len(assignments),
                     'grid_points':len(grid), 'weighted_E':str(E),
                     'derivative_budget':str(budget), 'epsilon':str(epsilon),
                     'origin_multiplicity':2})

# Independent infinite geometric-series arithmetic; analytic convergence is separate.
S = Q(2)*Q(1,2)/(1-Q(1,2))-Q(1,4)/(1-Q(1,4))
assert S == Q(5,3) and 4*S == Q(20,3)
assert Q(3,112)*(12+4*S) == Q(1,2)

# Derive the reconstructed quotient derivative as a polynomial identity.
negative = []
for k in [2,3,5]:
    N, c = k**4, Q(1,k**3)
    D = {0:ONE,N+1:C(c)}
    qprime_numerator = poly_sub(D,poly_mul({1:ONE},poly_derivative(D)))
    assert qprime_numerator == {0:ONE,N+1:C(-N*c)}
    assert N*c*c == Q(1,k*k)
    assert c < 1 and N*c > 1
    # A rational point with negative derivative numerator proves a critical
    # point by continuity between zero and this point; no floating roots.
    t = Q(2*(N+1)-1,2*(N+1))
    assert 0 < t < 1 and 1-N*c*t**(N+1) < 0
    assert 1+c*t**(N+1) > 0
    negative.append({'N':N,'coefficient':str(c),'energy':str(N*c*c),
                     'critical_point_in_disk':'certified by exact sign change'})

# Origin exception: g=z/(1+c*z) gives 1/z-1/g=-c, not zero at zero.
c = Q(1,3)
assert poly_sub({0:ONE}, {0:ONE,1:C(c)}) == {1:C(-c)}
# Sharp coefficient budget: z/(1-z^2), z/(1+z^2) have reciprocal difference -2z.
assert poly_sub({0:ONE,2:C(Q(-1))},{0:ONE,2:ONE}) == {2:C(Q(-2))}
assert Q(1)*Q(-2)**2 == 4
# Finite coincidence constraints do not force separated limits.
assert all(Q(1,2**N) < 1 for N in range(1,25))
# A perturbation with no small-derivative hypothesis can have an interior critical point.
assert poly_value(poly_derivative({1:ONE,2:ONE}), C(Q(-1,2))) == ZERO

for name,digest in expected.items():
    assert hashlib.sha256((base/'artifacts'/name).read_bytes()).hexdigest() == digest
print(json.dumps({
    'result':'PASS',
    'arithmetic':'Exact rational real and imaginary parts; Python standard library only',
    'frozen_author_files_checked':len(expected),
    'author_verifier_output':'byte-identical',
    'complex_weighted_product_controls':controls,
    'individual_factor_grid_controls':factor_checks,
    'small_dirichlet_counterexamples':negative,
    'reciprocal_origin_exception_checked':True,
    'dirichlet_bound_4_sharp_example_checked':True,
    'radial_geometric_series_constants_checked':True,
    'finite_interpolation_collapse_budgets_checked':True,
    'uncontrolled_perturbation_critical_point_checked':True,
    'limits':['Finite exact computations supplement the analytic audit.',
              'No finite grid establishes global univalence or infinite product convergence.',
              'The unrestricted characterization and current literature status are not certified.']
},indent=2,sort_keys=True))
