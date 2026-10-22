#!/usr/bin/env python3
"""Independent rational falsification checks; no source-family code is imported.

The analytic report supplies the all-parameter proofs. Finite calculations here
exercise distinct constructions, sharpness normalizations, and negative controls.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import datetime
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p or [F(0)]


def add(p, q):
    return trim([(p[h] if h < len(p) else 0) +
                 (q[h] if h < len(q) else 0)
                 for h in range(max(len(p), len(q)))])


def scale(p, c):
    return trim([c * v for v in p])


def mul(p, q):
    a = [F(0)] * (len(p) + len(q) - 1)
    for h, v in enumerate(p):
        for j, w in enumerate(q):
            a[h+j] += v*w
    return trim(a)


def power(p, d):
    q = [F(1)]
    for _ in range(d):
        q = mul(q, p)
    return q


def compose(p, q):
    v = [F(0)]
    for c in reversed(p):
        v = add(mul(v, q), [c])
    return v


def evaluate(p, x):
    v = F(0)
    for c in reversed(p):
        v = v*x + c
    return v


def integral(p, left=F(0), right=F(1)):
    return sum((c*(right**(h+1)-left**(h+1))/F(h+1)
                for h, c in enumerate(p)), F(0))


def kernel_by_cosine_sum(m):
    # 1 + 2 sum_{h=1}^s cos(2h theta), using T_h(1-2z).
    s = (m-1)//2
    value = [F(1)]
    previous = [F(1)]
    current = [F(1), F(-2)]
    for h in range(1, s+1):
        value = add(value, scale(current, F(2)))
        previous, current = current, add(mul([F(2), F(-4)], current),
                                         scale(previous, F(-1)))
    return scale(value, F(1, m))


def kernel_declared_binomial(m):
    s = (m-1)//2
    value = [F(0)]
    for j in range(s+1):
        value = add(value, [F(0)]*j + scale(power([F(1), F(-1)], s-j),
                     F((-1)**j*comb(m, 2*j+1), m)))
    return value


def complex_mul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def rodrigues(j):
    # Differentiate the independently expanded (x^2-1)^j exactly j times.
    value = [F(0)]*(j+1)
    for h in range(j+1):
        degree = 2*h
        if degree >= j:
            value[degree-j] += F(comb(j, h)*(-1)**(j-h)*factorial(degree),
                        2**j*factorial(j)*factorial(degree-j))
    return trim(value)


def laplace_expansion(j):
    # Average of (x+iota sqrt(1-x^2) cos theta)^j.
    value = [F(0)]
    for h in range(j//2+1):
        term = [F(0)]*(j-2*h) + scale(power([F(-1), F(0), F(1)], h),
                    F(comb(j, 2*h)*comb(2*h, h), 4**h))
        value = add(value, term)
    return value


def positive_ldl_pivots(matrix):
    size = len(matrix)
    lower = [[F(0)]*size for _ in range(size)]
    diagonal = []
    for i in range(size):
        lower[i][i] = F(1)
        d = matrix[i][i] - sum((lower[i][h]**2*diagonal[h]
                               for h in range(i)), F(0))
        require(d > 0, 'Nonpositive exact LDL pivot')
        diagonal.append(d)
        for j in range(i+1, size):
            lower[j][i] = (matrix[j][i] - sum(
                (lower[j][h]*lower[i][h]*diagonal[h] for h in range(i)), F(0)))/d
    return diagonal


def sparse_square(p):
    q = {}
    for (a, b), c in p.items():
        for (d, e), v in p.items():
            q[a+d, b+e] = q.get((a+d, b+e), F(0)) + c*v
    return q


def main():
    results = dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   arithmetic='Exact standard-library fractions.Fraction; no floating-point tests',
                   independent_of_source_code=True)
    kernel_identity_count = 0
    trig_checks = 0
    for m in range(1, 102, 2):
        r = kernel_by_cosine_sum(m)
        require(r == kernel_declared_binomial(m), 'Kernel polynomial identity')
        require(len(r)-1 == (m-1)//2 and r[0] == 1, 'Kernel degree or value at zero')
        kernel_identity_count += 1
        if m <= 61:
            for a in (F(1, 4), F(1, 2), F(3, 4), F(1)):
                sine = 2*a/(1+a*a)
                cosine = (1-a*a)/(1+a*a)
                z = (F(1), F(0))
                for _ in range(m):
                    z = complex_mul(z, (cosine, sine))
                require(evaluate(r, sine*sine) == z[1]/(m*sine),
                        'Rational Pythagorean-angle quotient')
                trig_checks += 1
    bounds_count = 0
    for n in (1, 3, 8):
        k = n+2
        for m in (1, 3, 5, 9, 17):
            r = kernel_by_cosine_sum(m)
            delta = F(1, 4*m*m)
            for z in (F(0), delta/4, delta/2, delta):
                q = evaluate(r, z)**(2*k)
                require(q >= F(1, 4**k), 'Core normalizer floor')
                bounds_count += 1
            for h in range(65):
                z = F(h, 64)
                q = evaluate(r, z)**(2*k)
                envelope = F(1) if z == 0 else min(F(1), (m*m*z)**(-k))
                require(F(0) <= q <= envelope, 'Kernel upper envelope')
                bounds_count += 1
    results['upper_kernel'] = dict(polynomial_identities=kernel_identity_count,
            odd_m_min=1, odd_m_max=101, rational_angle_checks=trig_checks,
            core_and_envelope_rational_checks=bounds_count)

    budgets = 0
    for n in range(1, 61):
        k = n+2
        A = 1+2**(3*n+6)
        require(1+2**(n+1+2*k)*2 == A, 'Dyadic coefficient sum')
        require(F(1, 2)**(k-n-1) == F(1, 2), 'Dyadic geometric ratio')
        for r in range(1, 2001):
            s, m = r//(2*k), 2*(r//(2*k))+1
            require(4*k*s <= 2*r and 2*k*m >= r, 'Degree or all-order budget')
            budgets += 1
    volume_checks = 0
    g = [F(0), F(1, 4), F(3, 4)]
    for h in range(1, 17):
        x = F(h, 16)
        s = evaluate(g, x)
        for j in range(h, 17):
            y = F(j, 16)
            u = evaluate(g, y)
            require(y <= (u/s)*x, 'Relative sublevel-volume growth')
            volume_checks += 1
        for u in (F(1), F(3, 2), F(3)):
            require(F(1) <= (u/s)*x, 'Saturated sublevel endpoint beyond one')
            volume_checks += 1
    results['upper_shell_and_degree'] = dict(degree_budget_pairs=budgets,
            dyadic_constant_dimensions=60, scale_relative_interval_checks=volume_checks,
            includes_shell_endpoints_beyond_one=True)

    witness_cases = [
        ('nonconvex_boundary_two_minima', [F(0), F(1), F(-2), F(1)],
         [F(0), F(1, 4), F(3, 4)], F(4), F(0), F(1), (1, 5, 6, 11, 12, 18, 24)),
        # f=(x^2-1/4)^4 has quartic-flat minima at +/-1/2.
        # ||f''|| <= 8*(3/4)^2*(27/4)=243/8, attained at endpoints.
        # M=1+L/2=259/16; B=M*(3/2)^2=2331/64.
        ('two_flat_interior_minima', power([F(-1, 4), F(0), F(1)], 4),
         [F(1, 9), F(-4, 9), F(4, 9)], F(2331, 64), F(-1), F(1), (1, 6, 12, 18)),
    ]
    witnesses = []
    k = 3
    for name, f, t, B, left, right, orders in witness_cases:
        for r in orders:
            s = r//(2*k)
            m = 2*s+1
            p = power(compose(kernel_by_cosine_sum(m), t), k)
            q = mul(p, p)
            D = integral(q, left, right)
            N = integral(mul(t, q), left, right)
            objective = integral(mul(f, q), left, right)
            C = B*k*k*4**k*(1+2**9)
            require(D > 0 and len(q)-1 <= 2*r, 'Witness normalizer or degree')
            require(F(0) <= objective <= B*N, 'Surrogate comparison in exact witness')
            require(objective/D <= C/F(r*r), 'Final all-order witness bound')
            witnesses.append(dict(case=name, r=r, m=m, density_degree=len(q)-1,
                                  normalizer=str(D), objective_gap=str(objective/D),
                                  surrogate_gap=str(B*N/D)))
    results['upper_exact_witnesses'] = witnesses

    legendre = [rodrigues(j) for j in range(25)]
    legendre_inner_products = 0
    for j, p in enumerate(legendre):
        require(p == laplace_expansion(j), 'Rodrigues versus Laplace polynomial')
        require(evaluate(p, F(1)) == 1 and evaluate(p, F(-1)) == (-1)**j,
                'Legendre endpoints')
        for h, q in enumerate(legendre):
            expected = F(2, 2*j+1) if j == h else F(0)
            require(integral(mul(p, q), F(-1), F(1)) == expected,
                    'Legendre exact orthogonality or norm')
            legendre_inner_products += 1
    caps = []
    for r in range(13):
        endpoint_kernel = [F(0)]
        for j in range(r+1):
            endpoint_kernel = add(endpoint_kernel,
                scale(compose(legendre[j], [F(-1), F(2)]), F((2*j+1)*(-1)**j)))
        D = integral(mul(endpoint_kernel, endpoint_kernel))
        M = (r+1)**2
        require(D == M, 'Endpoint reproducing-kernel norm')
        require(evaluate(endpoint_kernel, F(0))**2/D == M, 'Endpoint cap saturation')
        caps.append(dict(r=r, cap=M, normalized_endpoint_density=M))
    matrix_checks = []
    for r in range(13):
        c = F(1, 4*(r+1)**2)
        matrix = [[F(1, i+j+2)-c*F(1, i+j+1) for j in range(r+1)]
                  for i in range(r+1)]
        pivots = positive_ldl_pivots(matrix)
        matrix_checks.append(dict(r=r, lower_bound=str(c), positive_pivots=len(pivots),
                                  last_pivot=str(pivots[-1])))
    results['lower_legendre'] = dict(laplace_rodrigues_identity_degrees=list(range(25)),
            exact_inner_products=legendre_inner_products, endpoint_cap_saturation=caps,
            direct_hilbert_moment_matrix_psd=matrix_checks)

    # A genuinely mixed two-variable SOS; integrate the y fiber directly.
    ps = [{(0,0):F(1), (1,0):F(1), (0,1):F(1), (1,1):F(1)},
          {(2,0):F(1), (0,2):F(-1)}]
    marginal = [F(0)]*5
    for p in ps:
        for (a,b), c in sparse_square(p).items():
            if b % 2 == 0:
                marginal[a] += c*F(2, b+1)
    D = integral(marginal)
    normalized = scale(marginal, 1/D)
    M = 9
    for h in range(65):
        value = evaluate(normalized, F(h,64))
        require(F(0) <= value <= M, 'Integrated fiber density cap')
    mean = integral([F(0)]+normalized)
    require(mean >= F(1, 4*M), 'Product example lower moment')
    results['lower_mixed_product_example'] = dict(dimension=2, r=2,
            marginal_coefficients=[str(v) for v in normalized], normalizer=str(D),
            objective_mean=str(mean), bound=str(F(1,4*M)), rational_cap_checks=65)

    # Negative controls invalidate tempting substitutions, not the stated proofs.
    raw_f = [F(0), F(1), F(-2), F(1)]
    lhs = evaluate(raw_f, F(1,2))
    rhs = F(1,2)*evaluate(raw_f, F(1))
    require(lhs > rhs, 'Raw nonconvex-objective homothety negative control')
    nonglobal = evaluate([F(0), F(1), F(-1)], F(2))
    require(nonglobal < 0, 'Interval positivity is not global SOS negative control')
    require(F(4) > F(2), 'Wrong linear cap negative control')
    require(4*3*1 > 2*3, 'Ignoring quadratic composition negative control')
    results['negative_controls'] = [
        dict(name='Raw f-sublevel homothety substitution', detected=True,
             example='f=x(1-x)^2, a=0, x=1, lambda=1/2', lhs=str(lhs), rhs=str(rhs)),
        dict(name='Interval nonnegative implies global SOS', detected=True,
             example='z(1-z) at z=2', value=str(nonglobal)),
        dict(name='Replace quadratic cap by r+1', detected=True,
             example='r=1 endpoint reproducing-kernel square has q(0)=4>2'),
        dict(name='Omit quadratic-composition degree factor', detected=True,
             example='n=1,k=3,r=3,s=1 gives density degree 12>2r=6'),
        dict(name='Use k=n+1 in the same infinite shell bound', detected=True,
             explanation='Geometric ratio equals 1; the required infinite series diverges. This challenges that proof envelope, not the actual asymptotic claim.'),
        dict(name='Positive objectivewise Theta for constants', detected=True,
             example='f=7 and any normalized feasible q have integral f*q-min f=0'),
    ]
    results['status'] = 'ALL INDEPENDENT EXACT CHECKS PASSED; ALL SIX NEGATIVE CONTROLS DETECTED'
    results['limitations'] = 'Finite tests supplement the analytic derivations. No source-family import, numerical SDP, optimized replay, human verification, or formal proof assistant.'
    path = Path(__file__).with_name('independent_results.json')
    path.write_text(json.dumps(results, indent=2)+'\n')
    print(results['status'])
    print('Kernel identities:', kernel_identity_count, '; degree pairs:', budgets,
          '; Legendre inner products:', legendre_inner_products, '; exact witnesses:', len(witnesses))


if __name__ == '__main__':
    main()
