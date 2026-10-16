"""Fresh small falsification controls; neither field is algebraically closed or EC."""
from itertools import product
from pathlib import Path
from datetime import datetime, timezone
import json


def require(value, label):
    if not value:
        raise ValueError(label)


def field_case(p, a, b):
    values = list(product(range(p), repeat=2))
    zero, one = (0, 0), (1, 0)
    require(all((v*v+a*v+b) % p for v in range(p)), 'quadratic is reducible')

    def add(x, y):
        return ((x[0]+y[0]) % p, (x[1]+y[1]) % p)

    def mul(x, y):
        return ((x[0]*y[0]-b*x[1]*y[1]) % p,
                (x[0]*y[1]+x[1]*y[0]-a*x[1]*y[1]) % p)

    def power(x, n):
        if n < 0:
            require(x != zero, 'negative power of zero')
            return power(power(x, p*p-2), -n)
        result = one
        for _ in range(n):
            result = mul(result, x)
        return result

    rho = {}
    for x in values:
        roots = [y for y in values if power(y, p) == x]
        require(len(roots) == 1, 'root graph not a function')
        rho[x] = roots[0]
    for x, y, z in product(values, repeat=3):
        require(mul(x, add(y, z)) == add(mul(x, y), mul(x, z)), 'distributivity')
        require(mul(x, mul(y, z)) == mul(mul(x, y), z), 'associativity')
    for x, y in product(values, repeat=2):
        require(rho[add(x, y)] == add(rho[x], rho[y]), 'rho additivity')
        require(rho[mul(x, y)] == mul(rho[x], rho[y]), 'rho multiplicativity')
    nonzero = [x for x in values if x != zero]
    require(any(power(x, p) != one for x in nonzero), 'field characteristic confused with ring zero')
    require(all(power(rho[x], p) == x for x in values), 'Frobenius inverse')
    require(all(rho[x] == power(x, p) for x in values), 'finite inverse not integer power')
    checks = 0
    for k in range(-2, p*p-1):
        for x in nonzero:
            require(rho[power(x, k)] == power(rho[x], k), 'centrality/sign')
            require(mul(power(rho[x], p), power(x, -1)) == one, 'non-EC theta=rho control')
            checks += 1
    power2_nonadditive = any(power(add(x, y), 2) != add(power(x, 2), power(y, 2))
                             for x, y in product(values, repeat=2))
    power2_noninjective = len({power(x, 2) for x in nonzero}) < len(nonzero)
    if p == 3:
        require(power2_nonadditive and power2_noninjective, 'missing nonadditive/noninjective boundary')
    return {'p': p, 'order': p*p, 'modulus': [b, a, 1], 'signed_centrality_checks': checks,
            'unique_root_and_field_identities': True, 'inverse_is_integer_power_here': p,
            'theta_rho_annihilated_by_pX_minus_one': True, 'power2_nonadditive': power2_nonadditive,
            'power2_noninjective': power2_noninjective, 'ACFH_model': False}


def run():
    vectors = 0
    for p in (2, 3):
        for d in range(3):
            for coefficients in product((-2, -1, 0, 1, 2), repeat=d+1):
                q = (p*coefficients[0]-1,) + tuple(p*c for c in coefficients[1:])
                require(q[0] % p == p-1 and any(q), 'integer polynomial obstruction')
                # Formal Laurent monomials are equal precisely when all exponents agree.
                positive = tuple(max(c, 0) for c in q)
                negative = tuple(max(-c, 0) for c in q)
                require(positive != negative, 'negative/empty-product transfer')
                vectors += 1
    return {'timestamp': datetime.now(timezone.utc).isoformat(), 'result': 'PASS',
            'fields': [field_case(2, 1, 1), field_case(3, 0, 1)],
            'signed_laurent_vectors': vectors,
            'scope': 'Fresh finite falsification and formal exponent sanity controls only; independent written deduction establishes the universal EC theorem.'}


if __name__ == '__main__':
    receipt = run()
    (Path(__file__).resolve().parent / 'INDEPENDENT_CONTROL_RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))
