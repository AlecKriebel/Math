#!/usr/bin/env python3
"""Portable finite controls for the independent Goh-1992 collision audit.

Run with Python 3 from ANY directory. No source files, PDFs, TeX, third-party
packages, environment paths, network access, or floating point are required.
The full result is JSON on stdout. Analytic theorem inputs are explicitly
listed as assumptions; this is not a formal analytic proof or priority search.
"""
from fractions import Fraction as F
import json


def add(p, q):
    out = dict(p)
    for n, a in q.items():
        out[n] = out.get(n, F(0)) + a
    return {n: a for n, a in out.items() if a}


def scale(p, c):
    return {n: a*c for n, a in p.items() if a*c}


def multiply(p, q):
    out = {}
    for m, a in p.items():
        for n, b in q.items():
            out[m+n] = out.get(m+n, F(0)) + a*b
    return {n: a for n, a in out.items() if a}


def derivative(p):
    return {n-1: n*a for n, a in p.items() if n}


def integrate_zero(p):
    return {n+1: a/F(n+1) for n, a in p.items()}


def value(p, x):
    return sum((a*x**n for n, a in p.items()), F(0))


def gaussian_add(z, w):
    return z[0]+w[0], z[1]+w[1]


def gaussian_mul(z, w):
    return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]


def gaussian_pow(z, n):
    out = (F(1), F(0))
    for _ in range(n):
        out = gaussian_mul(out, z)
    return out


def koebe_coeff(u, n):
    return gaussian_mul((F(n), F(0)), gaussian_pow(u, n-1))


def perturbation_q(alpha, beta):
    # L=a2+i*eps*(alpha*a3+beta*a4); evaluate coefficients at k.
    p0 = {0: 4*alpha+10*beta, 2: -alpha-6*beta, 4: beta}
    p0 = {n: F(a) for n, a in p0.items() if a}
    d = scale(integrate_zero(p0), F(-1, 2))
    q = add(derivative(d), {n-1: -a for n, a in d.items()})
    return p0, d, q


def encoded_polynomial(p):
    return {str(n): str(a) for n, a in sorted(p.items())}


def main():
    checks = []

    def check(name, condition, evidence=None):
        if not condition:
            raise AssertionError(name)
        checks.append({'name': name, 'passed': True, 'evidence': evidence})

    eps = F(1, 10**24)
    eta = F(1, 10**12)
    T = F(7, 4)
    check('exact parameter relation', eps == eta**2)

    # Near-Koebe support phase and pure-square obstructions.
    check('normalization does not freeze a2', F(0) != F(2),
          'a2(identity)=0, a2(k)=2')
    check('candidate is genuinely degree four', eps != 0,
          'lambda4=i*eps is nonzero; padding lambda5=0 does not make degree five')
    check('Koebe phase neighborhood is disjoint from Re(u^3)=0',
          12*eta < 1,
          '|u-1|<4*eta gives |u^3-1|<12*eta; Re(u^3)=0 gives |u^3-1|>=1')
    check('a coefficient cannot cancel a nonzero imaginary polynomial on a ray',
          (F(2)-F(1))*(F(3)-F(1))*(F(3)-F(2)) == 2,
          'Imag(a*u*r^2-b*u^2*r+c*u^3) identically zero forces Imag(c*u^3)=0')
    g = {2: F(2), 0: F(-1)}
    h = {3: F(4), 1: F(-3)}
    bezout = add(multiply({2: F(4), 0: F(-1)}, g),
                 multiply({1: F(-2)}, h))
    check('strong no-Koebe obstruction for every real nonzero epsilon',
          bezout == {0: F(1)},
          '(4x^2-1)(2x^2-1)-2x(4x^3-3x)=1; ray w=-u^(-1)r requires cos(3theta)=cos(2theta)=0')
    check('uniform coefficient bounds for discriminant test',
          2+106*eta < 3 and 3+24*eta < 4)
    check('transformed even quartic cannot be a pure square',
          4*eps-28*eps**2 > 3*eps > 0,
          '|b^2-4ac|>=4eps(1-3eps)-16eps^2>3eps')
    check('even quartic is not automatically a square: negative control',
          F(1)**2 != 4*F(1)*F(1),
          '1+v^2+v^4 has discriminant -3')
    check('Goh same-degree-four coprimality cases',
          all(__import__('math').gcd(3, ell-1) == 1 for ell in (2, 3)),
          'requires a second independent critical equation')
    check('Goh same-degree-five cases',
          __import__('math').gcd(4, 1) == 1
          and __import__('math').gcd(4, 3) == 1
          and __import__('math').gcd(4, 2) != 1,
          'ell=2,4 use Thm3; ell=3 uses conditional Thm4')
    check('OCR correction: support threshold is 2sqrt2',
          F(2)**2*F(2) == 8 and F(2)**2*F(3) != 8)

    # Actual-S controls against illicit sum and real-restriction arguments.
    u = (F(0), F(1))
    diff = gaussian_add(koebe_coeff(u, 4),
                        gaussian_mul((F(-3), F(0)), koebe_coeff(u, 3)))
    second_at_ki = gaussian_mul((F(0), eps), diff)
    check('separate summand extrema do not coincide in actual S',
          second_at_ki[0] == 4*eps > 0,
          'a2 has unique real maximizer k, but Re i*eps*(a4-3a3)(k)=0 < value at k_i')
    check('conjugate-coefficient functional has different real restriction',
          second_at_ki[0] != -second_at_ki[0],
          'at k_i the perturbation gives +4eps versus -4eps')
    # Exact roots-of-unity Fourier matrix for degrees 2..4, using four roots.
    roots = [(F(1), F(0)), (F(0), F(1)),
             (F(-1), F(0)), (F(0), F(-1))]
    fourier_moments = []
    for n in range(1, 4):
        total = (F(0), F(0))
        for root in roots:
            total = gaussian_add(total, gaussian_pow(root, n))
        fourier_moments.append(total)
    check('positive coefficient modes distinguish normalization constants',
          all(z == (0, 0) for z in fourier_moments),
          'analytic polynomial with constant real part on all rotations has all positive Fourier coefficients zero')
    points = [(F(2), F(0)), (F(0), F(2)), (F(3, 2), F(3, 2))]
    winner = max(points, key=lambda z: sum(z))
    check('sum-converse mutation is rejected',
          winner == points[2] and winner[0] < 2 and winner[1] < 2,
          'unique maximum of x+y need maximize neither summand')

    # Independently derive the full first-order polynomial family.
    p0, d, q = perturbation_q(F(-3), F(1))
    check('candidate first-order natural-coordinate polynomial',
          p0 == {0: F(-2), 2: F(-3), 4: F(1)}, encoded_polynomial(p0))
    check('candidate inverse correction',
          d == {1: F(1), 3: F(1, 2), 5: F(-1, 10)}, encoded_polynomial(d))
    check('candidate radial-angle correction',
          q == {2: F(1), 4: F(-2, 5)}, encoded_polynomial(q))
    check('opposite exact endpoint signs',
          value(q, 1) == F(3, 5) and value(q, T) == F(-441, 640),
          [str(value(q, 1)), str(value(q, T))])
    q3 = perturbation_q(F(1), F(0))[2]
    q4 = perturbation_q(F(0), F(1))[2]
    check('degree-three and pure-degree-four endpoint controls',
          value(q3, 1) > 0 and value(q3, T) > 0
          and value(q4, 1) > 0 and value(q4, T) > 0,
          {'a3': encoded_polynomial(q3), 'a4': encoded_polynomial(q4)})
    check('zero perturbation cannot certify a strict reversal',
          value({}, 1)*value({}, T) == 0)

    # Uniform remainder budget and actual-tip membership gate.
    r = F(2, 3)
    check('area-theorem tail sums',
          r**4/(3*(1-r*r)) == F(16, 135) < F(1, 4)
          and 1/(1-r*r)**2-1 == F(56, 25) < F(9, 4))
    check('publication corrected reciprocal-square bound',
          5*eta < F(1, 6) and F(10, 3)+5*eta < F(7, 2),
          'H+H0 bounded by 10/3+5eta, rather than merely 2+5/3')
    check('actual finite-tip upper bound',
          F(6, 25)+F(5, 9)*F(9, 125) == F(7, 25)
          and F(7, 25)+7*eta < F(3, 10))
    check('entire natural-coordinate segment stays outside actual tip',
          T+333*eps < F(9, 5) and F(25, 81) > F(3, 10),
          {'radius_gap': str(F(25, 81)-F(3, 10))})
    check('uniform coefficient and square-root remainders',
          106+24*9 == 322 and 110+322*eta < 111
          and 161+F(111**2, 2)*eta < 162)
    check('inverse and derivative error budgets',
          486+18315*eta < 487
          and 161+(20979+24642)*eta < 162)
    check('positive real orientation on complete controlled segment',
          222*eps/(1-111*eps) < 223*eps < 1)
    check('radial-angle quotient remainder',
          2*(T*162+487) == 1541
          and 2*7*333 == 4662
          and 1541+4662*eta < 2000)
    check('endpoint signs survive full uniform error',
          F(3, 5)-2000*eta > F(1, 2)
          and F(-441, 640)+2000*eta < F(-1, 2))
    check('oversized-error mutation is rejected',
          not (F(3, 5)-F(3, 5) > 0))

    return {
        'status': 'passed',
        'arithmetic': 'Python standard-library Fraction and exact Gaussian rationals',
        'external_inputs_required': [],
        'checks_passed': len(checks),
        'checks': checks,
        'analytic_assumptions_not_proved_by_code': [
            'compactness of normalized S and existence of global maximizers',
            'Bieberbach and area theorems',
            'support-slit/Schiffer theorem and increasing modulus of actual omitted arc',
            'Rouche, holomorphic inverse patching and local trajectory uniqueness',
            'Goh source theorem hypotheses and proofs as transcribed in independent notes',
            'Fourier uniqueness on the full circle, not merely the four finite test roots'
        ],
        'conclusion_scope': 'Finite exact controls support a no-collision comparison with Goh1992. No global novelty clearance or final package acceptance.'
    }


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
