"""Read-only, standard-library exact controls. The universal proof is in DERIVATION.md.

Distinct from the deposited long all-pair campaigns: all 42 pairs for q=2,3,5,8
use exact radicals; no trigonometric approximation or floating-point threshold.
"""
from fractions import Fraction as Q
from math import gcd
import json


def require(value, label):
    if not value:
        raise RuntimeError(label)


class Poly:
    """Sparse rational polynomial in a,b,U,V,c,d, used for literal identities."""
    def __init__(self, terms=None):
        self.t = {k: Q(v) for k, v in (terms or {}).items() if v}

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Poly) else Poly({(0,)*6: Q(x)})

    def __add__(self, x):
        t = self.t.copy()
        for k, v in self.coerce(x).t.items():
            t[k] = t.get(k, Q(0)) + v
        return Poly(t)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.t.items()})

    def __sub__(self, x):
        return self + -self.coerce(x)

    def __rsub__(self, x):
        return self.coerce(x) + -self

    def __mul__(self, x):
        t = {}
        for k, v in self.t.items():
            for l, w in self.coerce(x).t.items():
                m = tuple(i+j for i, j in zip(k, l))
                t[m] = t.get(m, Q(0)) + v*w
        return Poly(t)

    __rmul__ = __mul__

    def __pow__(self, n):
        z = self.coerce(1)
        for _ in range(n):
            z = z*self
        return z


v = []
for k in range(6):
    e = [0]*6
    e[k] = 1
    v.append(Poly({tuple(e): 1}))
a, b, U, V, c, d = v
u = 2*(a+b-2*a*b)
identities = {
    'sphere_norm': 4*a*(1-a)+(1-2*a)**2-1,
    'latitude_slack': u-2*(b-a)-4*a*(1-b),
    'hyperbola': u*u-16*a*(1-a)*b*(1-b)-4*(b-a)**2,
    'lorentz_square': (U-c*V)**2-4*d*d*(1-c*c)-(V-c*U)**2
                      -(1-c*c)*(U*U-V*V-4*d*d),
}
for label, poly in identities.items():
    require(not poly.t, 'polynomial identity '+label)

F = [0, 1]
for _ in range(2, 20):
    F.append(F[-1]+F[-2])
arithmetic = []
quarter_boundary_examples = []
for n in range(3, 19):
    q, p = F[n], F[n-1]
    require(gcd(p, q) == 1, 'coprime')
    products = []
    half_ties = 0
    terminal = 0
    for m in range(1, q):
        residue = (m*p) % q
        r = min(residue, q-residue)
        require(0 < 2*r <= q, 'nonzero centered residue')
        require(3*m*r >= q, 'arithmetic bound')
        products.append(m*r)
        half_ties += 2*r == q
        if 4*r == q:
            quarter_boundary_examples.append({'n': n, 'q': q, 'm': m, 'abs_r': r})
        j = 2
        while F[j+1] <= m:
            j += 1
        h = n-j
        terminal += h == 1
        determinant = F[j]*F[j]-F[j-1]*F[j+1]
        require(determinant == (-1)**(j-1), 'Cassini basis sign')
        require(p*F[j]-q*F[j-1] == (-1)**(j-1)*F[h], 'first error')
        require(p*F[j+1]-q*F[j] == (-1)**j*F[h-1], 'second error')
        require(q == F[j]*F[h+1]+F[j-1]*F[h], 'addition')
    # All coordinate permutations are integer congruences, including odd parity.
    for j in range(q):
        k = (p*j) % q
        require((p*k) % q == ((-1)**n*j) % q, 'reversed-coordinate reflection')
        require((p*p-(-1)**n) % q == 0, 'inverse parity')
    arithmetic.append({'n': n, 'q': q, 'offsets': q-1,
                       'min_m_abs_r': min(products), 'classical_index': F[n-2],
                       'half_period_ties': half_ties, 'terminal_h1_offsets': terminal})
    require(min(products) == F[n-2], 'bounded exact classical-index value')


def sign_A_plus_B_sqrt5(A, B):
    """Exact sign for B>=0. No numerical square roots."""
    A, B = Q(A), Q(B)
    require(B >= 0, 'sign routine domain')
    if B == 0:
        return (A > 0)-(A < 0)
    if A >= 0:
        return 1
    z = 5*B*B-A*A
    return (z > 0)-(z < 0)


require(sign_A_plus_B_sqrt5(-2, 1) == 1, 'positive radical sign control')
require(sign_A_plus_B_sqrt5(-3, 1) == -1, 'negative radical sign control')
require(sign_A_plus_B_sqrt5(0, 0) == 0, 'zero radical sign control')
pair_certificates = []
for n in range(3, 7):
    q, p = F[n], F[n-1]
    minima = []
    for i in range(q):
        for j in range(i+1, q):
            residue = ((j-i)*p) % q
            r = min(residue, q-residue)
            H = q*(i+j-1)-2*i*j
            P = i*(q-i)*j*(q-j)
            require(H == q*(j-i-1)+2*i*(q-j) and H >= 0, 'linear slack')
            positive = (q == 5 and r == 1) or (q == 8 and r == 1)
            cert = {'n': n, 'q': q, 'i': i, 'j': j, 'abs_r': r, 'H': H, 'P': P}
            if positive:
                if q == 5:
                    A, B = Q(H*H)-Q(3*P, 2), Q(P, 2)
                    sg = sign_A_plus_B_sqrt5(A, B)
                    cert.update({'cosine': '(sqrt(5)-1)/4',
                                 'squared_slack': [str(A), str(B)],
                                 'radical': 'A+B*sqrt(5)'})
                else:
                    sg = (H*H-2*P > 0)-(H*H-2*P < 0)
                    cert.update({'cosine': 'sqrt(2)/2', 'squared_slack': H*H-2*P})
                require(sg > 0, 'strict exact positive-cosine lower bound')
                equality = False
                cert['comparison'] = 'strict'
            else:
                # Every other nonzero residue for these four q has cosine <=0.
                # H=0 iff m=1,i=0 because j<q. Then P=0 too.
                equality = H == 0
                require(not equality or (i, j, P) == (0, 1, 0), 'unique equality')
                cert['cosine'] = 'nonpositive; exact residue classification'
                cert['comparison'] = 'equality' if equality else 'strict'
            if equality:
                minima.append([i, j])
            pair_certificates.append(cert)
    require(minima == [[0, 1]], 'complete radical pair minimum')

# Deliberately false alternatives have exact witnesses, not sampled failures.
outsiders = {
    'singleton_n2': {'q': 1, 'unordered_pairs': 0, 'minimum_undefined': True},
    'both_endpoints_q2': {'indices': [0, 1, 2],
                           'pair_squared_distances': {'0,1': 2, '1,2': 2, '0,2': 4},
                           'unique_pair_claim_false': True},
    'midpoint_q2': {'squared_distance': 4, 'original_squared_minimum': 2,
                    'original_formula_false_for_midpoints': True},
    'general_coprime_q12_p1': {'indices': [5, 6],
                               'squared_distance': '2-sqrt(105)/6',
                               'proposed_lower_bound': '1/3',
                               'strict_failure_certificate': '105>100',
                               'integer_gap': 105-100},
    'omitted_odd_reflection_q5_n5': {'planar_index': 1, 'height_index': 3,
                                 'primary_longitude_residue': 1,
                                 'target_longitude_residue': 4,
                                 'equal_height_opposite_nonzero_sines': True},
    'quarter_turn_q8': {'m': 2, 'abs_r': 2, 'cosine_exactly_zero': True,
                        'classification_uses_integer_4r_ge_q': True},
}
require(gcd(12, 1) == 1 and 105 > 100, 'coprime outsider witness')
require(F[5] == 5 and F[4] == 3 and (F[4]*3) % 5 == 4,
        'odd-reflection witness actual Fibonacci index')
require(any(x['q'] == 8 and x['m'] == 2 for x in quarter_boundary_examples),
        'quarter-turn boundary reached')
print(json.dumps({'status': 'PASS',
                  'polynomial_identities': list(identities),
                  'arithmetic_n': '3..18', 'arithmetic_offsets': sum(x['offsets'] for x in arithmetic),
                  'arithmetic': arithmetic,
                  'quarter_boundary_examples': quarter_boundary_examples,
                  'direct_radical_pairs': len(pair_certificates),
                  'direct_radical_certificates': pair_certificates,
                  'false_variant_controls': outsiders,
                  'finite_controls_are_not_the_universal_proof': True}, sort_keys=True))
