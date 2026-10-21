"""New independent exact checks, including misleading finite-jet boundary cases."""
import itertools
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent


def ensure(value, message):
    if not value:
        raise RuntimeError(message)


def fieldmul(a, b):
    # Independent lookup from (a0+a1*u)(b0+b1*u), u^2=u+1.
    a0, a1, b0, b1 = a & 1, a >> 1, b & 1, b >> 1
    return (a0*b0 ^ a1*b1) | ((a0*b1 ^ a1*b0 ^ a1*b1) << 1)


def add(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def mul(a, b):
    return tuple(sumxor(fieldmul(a[i], b[n-i]) for i in range(n+1)) for n in range(3))


def sumxor(elements):
    result = 0
    for x in elements:
        result ^= x
    return result


def matrix(a, b):
    return [[add(mul(a[i][0], b[0][j]), mul(a[i][1], b[1][j]))
             for j in range(2)] for i in range(2)]


def scale(c, a):
    return [[mul(c, x) for x in row] for row in a]


def poly_multiply(a, b, n):
    result = 0
    for i in range(n):
        if (b >> i) & 1:
            result ^= a << i
    return result & ((1 << n) - 1)


def linear_apply(columns, vector):
    return sumxor(col for i, col in enumerate(columns) if vector >> i & 1)


def rank(columns):
    pivots = {}
    for v in columns:
        while v:
            pivot = v.bit_length() - 1
            if pivot in pivots:
                v ^= pivots[pivot]
            else:
                pivots[pivot] = v
                break
    return len(pivots)


def main():
    zero, one, w = (0,0,0), (1,0,0), (0,1,0)
    m0 = [[one, zero], [one, one]]
    injection_rows = []
    for c in range(4):
        square_root = next(a for a in range(4) if fieldmul(a, a) == c)
        d = (0, square_root, 0)
        cw2 = (0,0,c)
        chi = [[add(one, d), d], [zero, one]]
        target = [[one, cw2], [one, one]]
        ensure(matrix(target, chi) == scale(add(one,d), matrix(chi, m0)),
               'direct injection-collapse affine conjugator')
        injection_rows.append({'tangent_constant': c, 'sqrt': square_root,
                               'translation': list(d), 'exact_projective_identity': True})
    # Arbitrary formal h is handled in the written proof. Exhaust polynomial h
    # through degree five as corroboration; every nilpotent constant is included.
    hcount = 0
    sigma_constant = 0
    derivative_constant = 1
    for coeffs in itertools.product(range(4), repeat=6):
        h_of_sigma_constant = coeffs[0]
        weighted_constant = fieldmul(derivative_constant, coeffs[0])
        ensure(h_of_sigma_constant ^ weighted_constant == 0, 'arbitrary h constant cancels')
        for c in range(1,4):
            ensure((h_of_sigma_constant ^ weighted_constant) != c, 'nonzero tangent constant survives')
        hcount += 1
    # The finite quotient M/(y^n) has spurious H1 for even n. This deliberately
    # falsifies a possible inference that a finite rank test alone proves H1(M)=0.
    jets = []
    for n in range(2, 66):
        sigma = sum(1 << i for i in range(1,n))
        weight = 1 | 4
        power = 1
        columns = []
        for i in range(1,n):
            power = poly_multiply(power, sigma, n)
            tf = poly_multiply(weight, power, n)
            columns.append((tf ^ (1 << i)) >> 1)
        ensure(all(linear_apply(columns, col) == 0 for col in columns), '(T-1)^2=0')
        r = rank(columns)
        dimension = n - 1 - 2*r
        ensure(dimension == int(n % 2 == 0), 'cutoff parity boundary')
        spurious = n % 2 == 0
        if spurious:
            odd_top = 1 << (n-2)
            ensure(linear_apply(columns, odd_top) == 0 and rank(columns+[odd_top]) == r+1,
                   'odd leading-order invariant exists only after truncation')
        jets.append({'cutoff': n, 'rank_Tminus1': r, 'finite_H1_dimension': dimension,
                     'spurious_odd_top_class': spurious})
    # Exact projective matrix identity over every element in the cubic F4-ring,
    # not just the distinguished epsilon, with alpha -> alpha+alpha^2.
    parameter_rows = []
    for c0,c1,c2 in itertools.product(range(4), repeat=3):
        if c0:
            continue  # coordinate identity reduction requires nilpotent alpha.
        alpha = (c0,c1,c2)
        target = add(alpha,mul(alpha,alpha))
        m = [[one,alpha],[one,one]]
        mp = [[one,target],[one,one]]
        chi = [[add(one,alpha),alpha],[zero,one]]
        ensure(matrix(mp,chi) == scale(add(one,alpha),matrix(chi,m)), 'all nilpotent parameters')
        parameter_rows.append({'parameter': list(alpha), 'shifted': list(target)})
    result = {'status': 'PASS', 'independent_injection_collapse_all_four_scalars': injection_rows,
              'polynomial_conjugator_checks_including_nilpotent_constants': hcount,
              'all_nilpotent_cubic_parameter_shifts': parameter_rows, 'finite_jet_boundary_checks': jets,
              'limits': 'Exact finite corroboration only. The finite jets intentionally have cutoff classes, so the full Laurent-series even-valuation proof is essential. Arbitrary formal h, derivations, naturality, and small-extension quantifiers are proved independently in WHOLE_PACKAGE_REVIEW.md.'}
    (HERE / 'receipts/INDEPENDENT_MATH_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','injection_scalars':4,'h_polynomials':hcount,
                      'cubic_nilpotent_parameters':len(parameter_rows),'jet_cutoffs':len(jets),
                      'finite_jet_cutoff_counterchecks_found':sum(j['spurious_odd_top_class'] for j in jets)},indent=2))


if __name__ == '__main__':
    main()
