#!/usr/bin/env python3
"""Independent finite checks of Euler algebra, never an L-function moment test.

Standard library only. Every guard remains executable under python -O.
Exact coefficients use Gaussian rational pairs; quadrature uses floating point.
No network access or writes. Bad mathematical predicates are tested in actual
child processes via --negative; no invalid source fixtures are created.
"""
import argparse
import cmath
from fractions import Fraction as F
import json
import math
import subprocess
import sys

ZERO = (F(0), F(0))
ONE = (F(1), F(0))
I = (F(0), F(1))
MINUS = (F(-1), F(0))
MINUS_I = (F(0), F(-1))
COUNT = 0


def require(predicate, label):
    global COUNT
    COUNT += 1
    if not predicate:
        raise ValueError(label)


def add(z, w):
    return z[0] + w[0], z[1] + w[1]


def mul(z, w):
    return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]


def scale(z, a):
    return z[0]*a, z[1]*a


def conj(z):
    return z[0], -z[1]


def norm(z):
    return z[0]**2+z[1]**2


def conv(a, b, degree):
    result = []
    for n in range(degree+1):
        value = ZERO
        for j in range(n+1):
            value = add(value, mul(a[j], b[n-j]))
        result.append(value)
    return result


PRIMITIVES = {
    'one': (1, [ONE]),
    'quad3': (3, [ZERO, ONE, MINUS]),
    'quad4': (4, [ZERO, ONE, ZERO, MINUS]),
    'quart5': (5, [ZERO, ONE, I, MINUS_I, MINUS]),
    'quart5bar': (5, [ZERO, ONE, MINUS_I, I, MINUS]),
    'quad8': (8, [ZERO, ONE, ZERO, MINUS, ZERO, MINUS, ZERO, ONE]),
}


def primitive(name, n):
    f, values = PRIMITIVES[name]
    return values[n % f]


def char(name, q, n):
    f = PRIMITIVES[name][0]
    if q < 1 or q % f:
        raise ValueError('modulus must be a positive multiple of conductor')
    return primitive(name, n) if math.gcd(q, n) == 1 else ZERO


def coefficients(terms, degree):
    result = [ONE]+[ZERO]*degree
    for z, a in terms:
        values = [ONE]
        for n in range(1, degree+1):
            values.append(scale(mul(values[-1], z), (a+n-1)/n))
        result = conv(result, values, degree)
    return result


def sharp_hybrid_coefficients(rows, p, K, degree):
    """Actual sharp P_X local factor from Sahay, with K=floor(log X/log p)."""
    logarithm = [ZERO]*(degree+1)
    deletions = []
    for name, q, a in rows:
        u = primitive(name, p)
        power = ONE
        for j in range(1, min(K, degree)+1):
            power = mul(power, u)
            logarithm[j] = add(logarithm[j], scale(power, a/j))
        if q % p == 0:
            deletions.append((u, -a))
    exponential = [ONE]
    for n in range(1, degree+1):
        c = ZERO
        for j in range(1, n+1):
            c = add(c, scale(mul(logarithm[j], exponential[n-j]), F(j, n)))
        exponential.append(c)
    return conv(exponential, coefficients(deletions, degree), degree)


def grouped(rows):
    result = {}
    for name, q, a in rows:
        if a < 0:
            raise ValueError('only nonnegative input weights are in scope')
        char(name, q, 1)
        if a:
            result[name] = result.get(name, F(0))+a
    return result


def exponent(rows):
    return sum((a*a for a in grouped(rows).values()), F(0))


CASES = [
    [('one', 1, F(1)), ('one', 2, F(1))],
    [('quad3', 3, F(1, 2)), ('quad3', 12, F(3, 2)),
     ('quad4', 20, F(1, 3))],
    [('quart5', 5, F(1)), ('quart5bar', 10, F(1))],
    [('quart5', 5, F(1, 4)), ('quart5', 10, F(3, 4)),
     ('quart5', 20, F(1))],
    [('one', 6, F(0)), ('quad4', 4, F(1, 2))],
    [('one', 2, F(0))],
    [('one', 30, F(1, 2)), ('quad8', 56, F(5, 4)),
     ('quad3', 45, F(2, 3)), ('quart5', 20, F(1, 4))],
    [('one', 1, F(1, 8)), ('one', 210, F(3, 8)),
     ('quart5', 35, F(7, 6)), ('quart5bar', 110, F(1, 6))],
    [('quad3', 3, F(1)), ('quad4', 4, F(1))],
    [('quart5', 5, F(0)), ('quart5bar', 5, F(0))],
]
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]


def j_series(terms, p, degree=240):
    # Independent numerical calculation, separate from the exact rational code.
    c = [1+0j]+[0j]*degree
    for z, a in terms:
        d = [1+0j]
        for n in range(1, degree+1):
            d.append(d[-1]*z*(a+n-1)/n)
        c = [sum(c[j]*d[n-j] for j in range(n+1))
             for n in range(degree+1)]
    return math.fsum(abs(z)**2/p**n for n, z in enumerate(c))


def j_phase(terms, p, mesh=16384):
    values = []
    for k in range(mesh):
        z = cmath.exp(2j*math.pi*k/mesh)/math.sqrt(p)
        values.append(math.prod(abs(1-u*z)**(-2*a) for u, a in terms))
    return math.fsum(values)/mesh


def rational_one(x):
    return 1/(1-x)


def rational_two(x):
    return (1+x)/(1-x)**3


NEGATIVES = [
    'wrong_lift_sign', 'wrong_deletion_sign', 'separate_local_phases',
    'primitive_collision_exponent', 'conjugate_collision_exponent',
    'wrong_regularization_sign', 'inverse_cross_L_sign',
    'ignored_bad_prime', 'zero_weight_kept_as_nonzero',
    'zero_exceptional_factor', 'distinct_quotient_principal',
    'truncated_hybrid_equals_full_Euler',
]


def negative(name):
    """Each intentionally wrong conclusion must fail an ordinary runtime guard."""
    x = F(1, 2)
    if name == 'wrong_lift_sign':
        actual = coefficients([(ONE, F(1))], 5)
        wrong = coefficients([(ONE, F(-1))], 5)
        require(actual == wrong, name)
    elif name == 'wrong_deletion_sign':
        actual = coefficients([(ONE, F(1))], 5)
        wrong = coefficients([(ONE, F(2)), (ONE, F(1))], 5)
        require(actual == wrong, name)
    elif name == 'separate_local_phases':
        require(rational_two(x) == rational_one(x)**2, name)
    elif name == 'primitive_collision_exponent':
        require(exponent(CASES[0]) == 2, name)
    elif name == 'conjugate_collision_exponent':
        require(exponent(CASES[2]) == 4, name)
    elif name == 'wrong_regularization_sign':
        # At p=2 the quartic and its conjugate sum to zero, rho=-1.
        raw_linear, cross_real = F(-2), F(-1)
        require(raw_linear+2*cross_real == 0, name)
    elif name == 'inverse_cross_L_sign':
        # J*(1-x)^2 = (1-x^2)/|1-rho*x|^2, rho=-1.
        actual = (1-x*x)/(1+x)**2
        wrong = (1-x*x)*(1+x)**2
        require(actual == wrong, name)
    elif name == 'ignored_bad_prime':
        require(rational_one(x)/rational_two(x) == 1, name)
    elif name == 'zero_weight_kept_as_nonzero':
        require(coefficients([(ONE, F(0))], 5) ==
                coefficients([(ONE, F(1))], 5), name)
    elif name == 'zero_exceptional_factor':
        require(j_series([(0j, 1.0)], 2) == 0, name)
    elif name == 'distinct_quotient_principal':
        require(all(mul(primitive('quart5', n),
                        conj(primitive('quart5bar', n))) == ONE
                    for n in range(1, 5)), name)
    elif name == 'truncated_hybrid_equals_full_Euler':
        # At X=3,p=2 the zeta prime component is exp(z), not (1-z)^-1.
        upper_bound = 1+x+x*x/(4*(1-x))
        require(upper_bound >= rational_one(x), name)
    else:
        raise ValueError('unknown negative control')
    raise RuntimeError('negative control was unexpectedly accepted')


def run():
    exact_cases = 0
    for rows in CASES:
        q = math.lcm(*(q for name, q, a in rows))
        groups = grouped(rows)
        A = sum((a for name, q, a in rows), F(0))
        for p in PRIMES:
            actual = coefficients([(char(name, mod, p), a)
                                   for name, mod, a in rows], 10)
            common = [(char(name, q, p), a) for name, mod, a in rows]
            common += [(primitive(name, p), a) for name, mod, a in rows
                       if q % p == 0 and mod % p != 0]
            lifted = coefficients(common, 10)
            core = coefficients([(primitive(name, p), a)
                                 for name, mod, a in rows], 10)
            aggregate = coefficients([(primitive(name, p), a)
                                      for name, a in groups.items()], 10)
            bound = coefficients([(ONE, A)], 10)
            for r in range(11):
                require(actual[r] == lifted[r], 'common modulus inverse lift')
                require(core[r] == aggregate[r], 'primitive weight aggregation')
                require(norm(actual[r]) <= norm(bound[r]), 'coefficient bound')
            require(actual[0] == ONE, 'nonzero local constant coefficient')
            hybrid_bound = coefficients([(ONE, 2*A)], 10)
            for K in [1, 2, 4, 10]:
                truncated = sharp_hybrid_coefficients(rows, p, K, 10)
                for r in range(11):
                    require(norm(truncated[r]) <= norm(hybrid_bound[r]),
                            'uniform sharp hybrid coefficient majorant')
                    if r <= K:
                        require(truncated[r] == actual[r],
                                'sharp hybrid exact coefficients through K')
            if q % p:
                first = norm(actual[1])
                E = sum((a*a for a in groups.values()), F(0))
                cross = F(0)
                items = list(groups.items())
                for j, (name, a) in enumerate(items):
                    for other, b in items[j+1:]:
                        rho = mul(primitive(name, p), conj(primitive(other, p)))
                        cross += 2*a*b*rho[0]
                require(first == E+cross, 'diagonal and cross first coefficient')
                require(first-E-cross == 0, 'regularized p^-1 coefficient')
            exact_cases += 1

    # Check every distinct pair on an explicit common modulus, not just primes.
    names = list(PRIMITIVES)
    pair_checks = []
    for j, name in enumerate(names):
        for other in names[j+1:]:
            q = math.lcm(PRIMITIVES[name][0], PRIMITIVES[other][0])
            units = [n for n in range(1, q+1) if math.gcd(n, q) == 1]
            quotients = [mul(primitive(name, n), conj(primitive(other, n)))
                         for n in units]
            require(any(z != ONE for z in quotients), 'distinct quotient nonprincipal')
            for n in units:
                for m in units:
                    require(mul(mul(primitive(name, n), conj(primitive(other, n))),
                                mul(primitive(name, m), conj(primitive(other, m)))) ==
                            mul(primitive(name, n*m), conj(primitive(other, n*m))),
                            'quotient character multiplicativity')
            pair_checks.append({'characters': [name, other], 'common_modulus': q,
                                'unit_residues': len(units), 'nonprincipal': True})

    # Exact first two normalizations, imprimitive ratio, and quartic collision.
    for p in PRIMES:
        x = F(1, p)
        require((1-x)*rational_one(x) == 1, 'mean-square good-prime factor')
        require((1-x)**4*rational_two(x) == 1-x*x, 'fourth-moment good-prime factor')
        require((1-x)**4/(1-x*x) == (1-x)**3/(1+x), 'fourth bad-prime correction')
        require(rational_one(x)/rational_two(x) == (1-x)**2/(1+x), 'deletion ratio')
        for rho in [ONE, MINUS, I, MINUS_I]:
            # Coefficients of the closed two-unit formula are checked to degree 10.
            b = coefficients([(ONE, F(1)), (rho, F(1))], 10)
            J = [(norm(z), F(0)) for z in b]
            denominator = coefficients([(ONE, F(-2)), (rho, F(-1)),
                                        (conj(rho), F(-1))], 10)
            product = conv(J, denominator, 10)
            target = [ONE, ZERO, MINUS]+[ZERO]*8
            for r in range(11):
                require(product[r] == target[r], 'two-factor closed local identity')
    require(rational_one(F(1, 2))/rational_two(F(1, 2)) == F(1, 6),
            'zeta times principal mod2 exact ratio')
    require(exponent(CASES[0]) == 4, 'same primitive exponent')
    require(exponent(CASES[2]) == 2, 'conjugate distinct exponent')
    require(exponent(CASES[5]) == 0 and not grouped(CASES[5]), 'all-zero omission')
    x = F(1, 2)
    truncated_upper_bound = 1+x+x*x/(4*(1-x))
    require(truncated_upper_bound == F(13, 8), 'X3 exponential local upper bound')
    require(truncated_upper_bound < rational_one(x), 'actual truncated mean differs from full J2')

    # Agreement with Topacogullari's printed leading factor at exceptional primes.
    for p in PRIMES:
        x = F(1, p)
        for present1, present2 in [(True, False), (False, True), (True, True)]:
            J = F(1) if present1 and present2 else rational_one(x)
            euler_correction = (1-x)**2*J/(1-x*x)
            totient_ratio = (1-x) if present1 and present2 else F(1)
            printed_correction = totient_ratio*(1-F(1, p+1))
            require(euler_correction == printed_correction, 'published two-factor bad-prime factor')

    # G(n) is evaluated exactly via G(n)=product_{j=1}^{n-2} j!.
    def barnes_integer(n):
        return math.prod(math.factorial(j) for j in range(1, n-1))
    require(F(barnes_integer(2)**2, barnes_integer(3)) == 1, 'G weight1')
    require(F(barnes_integer(3)**2, barnes_integer(5)) == F(1, 12), 'G weight2')
    for m in [1, 2, 3]:
        for N in [1, 2, 4, 8]:
            direct = F(1)
            for j in range(1, N+1):
                direct *= F(math.factorial(j-1)*math.factorial(j+2*m-1),
                            math.factorial(j+m-1)**2)
            telescoped = F(barnes_integer(N+1)*barnes_integer(N+2*m+1)*
                           barnes_integer(m+1)**2,
                           barnes_integer(2*m+1)*barnes_integer(N+m+1)**2)
            require(direct == telescoped, 'Barnes telescoping of unitary identity')

    fractional_matrix = []
    for m in [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0]:
        mesh = 131072
        integral = math.fsum((2*math.sin(math.pi*(k+0.5)/mesh))**(2*m)
                             for k in range(mesh))/mesh
        exact_gamma = math.exp(math.lgamma(1+2*m)-2*math.lgamma(1+m))
        relative = abs(integral/exact_gamma-1)
        require(relative < 1e-7, 'fractional CUE N1 integral/gamma normalization')
        values = []
        for N in [10, 100, 1000, 10000]:
            log_value = math.fsum(math.lgamma(j)+math.lgamma(j+2*m)-
                                  2*math.lgamma(j+m) for j in range(1, N+1))
            values.append(math.exp(log_value-m*m*math.log(N)))
        # This checks convergence behavior at finite N, not the Barnes limit.
        errors = [abs(v/values[-1]-1) for v in values[:-1]]
        require(errors[0] > errors[1] > errors[2],
                'fractional normalized CUE gamma product converges numerically')
        fractional_matrix.append({'weight': m, 'N1_relative_integral_gamma_error': relative,
                                  'normalized_products_N10_N100_N1000_N10000': values,
                                  'relative_errors_against_finite_N10000': errors,
                                  'finite_N10000_is_not_the_Barnes_limit': True})

    phase = []
    for ci in range(len(CASES)):
        rows = CASES[ci]
        for p in [2, 3, 5, 7]:
            terms = [(complex(float(char(name, q, p)[0]),
                              float(char(name, q, p)[1])), float(a))
                     for name, q, a in rows if a]
            series = j_series(terms, p)
            quad = j_phase(terms, p)
            relative = abs(series-quad)/max(1.0, series)
            require(math.isfinite(series) and series >= 1-1e-14, 'positive finite local series')
            require(math.isfinite(quad) and quad > 0, 'positive finite local phase')
            require(relative < 2e-13, 'real-weight numerical Parseval')
            phase.append({'case': ci, 'prime': p, 'relative_difference': relative})

    # A finite numerical regularization diagnostic. Analytic proof supplies tail.
    regularized = []
    rows = CASES[6]
    groups = grouped(rows)
    E = float(exponent(rows))
    for p in [101, 503, 1009, 5003, 10007]:
        terms = [(complex(float(char(name, q, p)[0]), float(char(name, q, p)[1])), float(a))
                 for name, q, a in rows]
        J = j_series(terms, p, 30)
        logH = math.log(J)+E*math.log1p(-1/p)
        items = list(groups.items())
        for j, (name, a) in enumerate(items):
            for other, b in items[j+1:]:
                rho = mul(primitive(name, p), conj(primitive(other, p)))
                z = complex(float(rho[0]), float(rho[1]))
                logH += 2*float(a*b)*math.log(abs(1-z/p))
        scaled = p*p*logH
        require(math.isfinite(scaled) and abs(scaled) < 30, 'finite regularized p^-2 diagnostic')
        regularized.append({'prime': p, 'p_squared_logH': scaled})

    negative_controls = []
    for name in NEGATIVES:
        child = subprocess.run([sys.executable, __file__, '--negative', name],
                               capture_output=True, text=True)
        require(child.returncode != 0, 'actual wrong-predicate subprocess must reject')
        require('ValueError: '+name in child.stderr, 'expected guard is the rejection cause')
        require(not child.stdout, 'negative control must not emit a success report')
        negative_controls.append({'name': name, 'returncode': child.returncode,
                                  'guard_rejected': True})
    return {'status': 'PASS', 'check_count': COUNT, 'exact_row_prime_cases': exact_cases,
            'exact_coefficient_degree': 10, 'character_pair_checks': pair_checks,
            'phase_mesh': 16384, 'phase_series_degree': 240,
            'phase_checks': phase, 'regularization_diagnostics': regularized,
            'fractional_matrix_checks': fractional_matrix,
            'negative_controls': negative_controls, 'negative_control_count': len(negative_controls),
            'runtime_optimization': sys.flags.optimize,
            'truncated_hybrid_counterexample': {
                'cutoff_X': 3, 'prime': 2, 'weight': 1,
                'actual_local_series': 'sum_r (1/2)^r/(r!)^2',
                'actual_local_upper_bound': '13/8',
                'full_Euler_J2': '2', 'finite_X_equality_false': True},
            'asymptotic_proved': False,
            'scope': 'finite Euler/local/matrix identities and wrong-predicate rejection; analytic derivation supplies infinite convergence; no critical-line moment verification'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', choices=NEGATIVES)
    args = parser.parse_args()
    if args.negative:
        negative(args.negative)
    else:
        print(json.dumps(run(), indent=2, sort_keys=True))
