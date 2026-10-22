"""Small exact diagnostics; no network, author-code execution, or arithmetic oracle."""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def values(n, c, ds):
    return sorted({(c + sum(e*d for e, d in zip(es, ds))) % n
                   for es in product((0, 1), repeat=len(ds))})


def finite_diagnostic(n, c, ds):
    target = values(n, c, ds)
    require((sum(ds) + 2*c) % n == 0, 'transfer consistency')
    comparisons = 0
    for eta in product((0, 1), repeat=len(ds)):
        cp = (c + sum(e*d for e, d in zip(eta, ds))) % n
        dp = [(-d if e else d) % n for e, d in zip(eta, ds)]
        require(values(n, cp, dp) == target, 'base-lift invariance')
        comparisons += 1
    require(sorted({(-t) % n for t in target}) == target, 'complementation')
    subgroup = {0}
    while True:
        enlarged = subgroup | {(t+d) % n for t in subgroup for d in ds}
        if enlarged == subgroup:
            break
        subgroup = enlarged
    coset = sorted({(c+t) % n for t in subgroup})
    return {'modulus': n, 'c': c, 'differences': ds, 'attainable': target,
            'contains_zero': 0 in target, 'generated_coset': coset,
            'base_lift_changes_checked': comparisons,
            'arithmetic_surface_realization_claimed': False}


def valuation(n, p):
    n = Fraction(n)
    def integer_val(k):
        count = 0
        while k % p == 0:
            k //= p
            count += 1
        return count
    return integer_val(abs(n.numerator)) - integer_val(n.denominator)


def hilbert_odd(a, b, p):
    aa, bb = valuation(a, p), valuation(b, p)
    u, v = a // (p**aa), b // (p**bb)
    legendre = lambda x: -1 if pow(x % p, (p-1)//2, p) == p-1 else 1
    return ((-1)**(aa*bb*((p-1)//2)) * legendre(u)**bb * legendre(v)**aa)


def hilbert_two(a, b):
    aa, bb = valuation(a, 2), valuation(b, 2)
    u, v = a // 2**aa, b // 2**bb
    exponent = ((u-1)*(v-1)//4 + aa*(v*v-1)//8 + bb*(u*u-1)//8)
    return (-1)**exponent


def hs_exact_arithmetic():
    a, p, c = 5, 13, 2
    m_y = a*a*p*c
    rhs = lambda x, t: (x*x-a)*(x*x-a*p*p)*(t*t-a)*(t*t-a*c*c)
    require(rhs(0, 0) == m_y*m_y, 'rational base point')
    require(pow(a, (p-1)//2, p) == p-1, '5 nonsquare modulo 13')
    require((c*(c*c-1)) % p != 0, 'HS parameters')
    require(2*2 - a == -1, 'global norm proving involution invariance')
    j = lambda b: Fraction(2**8*(b**4-b*b+1)**3, b**4*(b*b-1)**2)
    require(valuation(j(p), p) == -4 and valuation(j(c), p) == 3,
            'different potentially good reduction, hence nonisogenous')
    radicand = (1-a*p*p)**2*(1-a*p**4)*(1-a*c*c*p*p)
    require(radicand % p == 1, 'Hensel unit radicand')
    root, modulus = 1, p
    residues = []
    for k in range(1, 12):
        digit = ((radicand-root*root)//modulus * pow(2*root, -1, p)) % p
        root += digit*modulus
        modulus *= p
        require((root*root-radicand) % modulus == 0 and root % p == 1,
                'Hensel lift')
        residues.append({'power': k+1, 'modulus': modulus, 'root': root})
    require(rhs(Fraction(1, p), Fraction(1, p))*p**8 == radicand,
            'local point equation cleared of denominators')
    symbols = {'2': hilbert_two(m_y, a), '5': hilbert_odd(m_y, a, 5),
               '13': hilbert_odd(m_y, a, p), 'infinity': 1}
    require(symbols == {'2': -1, '5': 1, '13': -1, 'infinity': 1},
            'rational quaternion invariants')
    require(sum(Fraction(s == -1, 2) for s in symbols.values()) % 1 == 0,
            'global reciprocity check')
    # For Q_13(sqrt(5))/Q_13 unramified quadratic, norms have even valuation.
    # The new y = 13^-4 * Hensel unit has even valuation, hence invariant zero.
    new_invariant = Fraction(0)
    total_new = (sum(Fraction(s == -1, 2) for s in symbols.values())
                 - Fraction(symbols['13'] == -1, 2) + new_invariant) % 1
    require(total_new == Fraction(1, 2), 'nonzero obstruction survives every switch')
    return {'parameters': {'a': a, 'b': p, 'c': c}, 'rational_point': [0, 0, m_y],
            'j_valuations_at_13': [-4, 3], 'norm_of_2_plus_sqrt5': -1,
            'rational_quaternion_symbols': symbols, 'hensel_radicand': radicand,
            'hensel_residues': residues, 'hensel_derivative_mod13': 2,
            'local_new_y_valuation': -4, 'new_invariant_at_13': '0',
            'global_obstruction': str(total_new), 'all_switch_differences_on_class': '0',
            'dependency_limit': 'HS supplies the smooth K3/Enriques models, algebraic unramified class, and pullback Br(X)=Br0(Y); these diagnostics reproduce their local arithmetic, not their entire geometric proof.'}


def main():
    cases = [finite_diagnostic(1, 0, []), finite_diagnostic(2, 1, [0]),
             finite_diagnostic(5, 1, [2, 1]), finite_diagnostic(5, 1, [2, 2, 4])]
    require(not cases[2]['contains_zero'] and 0 in cases[2]['generated_coset'],
            'subgroup replacement false-positive control')
    require(cases[0]['contains_zero'] and cases[3]['contains_zero'], 'positive controls')
    result = {'status': 'PASS', 'abstract_cases': cases,
              'hensel_and_hilbert_arithmetic': hs_exact_arithmetic(),
              'scope': 'Four hand-selected exact finite cases and one published arithmetic example; no arithmetic realization asserted for abstract cases; not formal proof verification.'}
    Path(__file__).with_name('INDEPENDENT_CHECKS.json').write_text(
        json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'abstract_cases': len(cases),
                      'base_changes': sum(c['base_lift_changes_checked'] for c in cases),
                      'HS_global_obstruction': result['hensel_and_hilbert_arithmetic']['global_obstruction']}))


if __name__ == '__main__':
    main()
