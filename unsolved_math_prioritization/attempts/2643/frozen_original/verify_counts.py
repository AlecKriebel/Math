#!/usr/bin/env python3
"""Arithmetic checks of Li--Shi's published table, not group enumeration."""
import json
import math

COUNTS = {1: 1, 2: 435, 3: 2240, 4: 6300, 5: 8064,
          6: 6720, 7: 5760, 8: 5040, 14: 5760}


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def phi(n):
    return sum(math.gcd(k, n) == 1 for k in range(1, n + 1))


def mobius(n):
    factors = 0
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            factors += 1
            if n % p == 0:
                return 0
        p += 1
    if n > 1:
        factors += 1
    return (-1) ** factors


def main():
    order = sum(COUNTS.values())
    exponent = math.lcm(*COUNTS)
    assert order == 40320
    assert order == 16 * math.factorial(7) // 2
    # |PSL_3(q)| = q^3(q^3-1)(q^2-1)/gcd(3,q-1).
    simple_order = 4**3 * (4**3 - 1) * (4**2 - 1) // math.gcd(3, 4 - 1)
    assert simple_order == 20160 and order == 2 * simple_order
    assert exponent == 840
    assert all(order % d == 0 for d in COUNTS)
    assert all(c % phi(d) == 0 for d, c in COUNTS.items())
    ds = divisors(exponent)
    types = {n: sum(c for d, c in COUNTS.items() if n % d == 0) for n in ds}
    recovered = {n: sum(mobius(n // d) * types[d] for d in divisors(n)) for n in ds}
    assert all(recovered[n] == COUNTS.get(n, 0) for n in ds)
    assert types[1] == 1 and types[exponent] == order
    assert types[2] == 436 and types[3] == 2241 and types[14] == 11956
    print(json.dumps({
        'status': 'PASS',
        'scope': 'Arithmetic consistency of the published Li--Shi table only; no independent group enumeration.',
        'group_order': order,
        'simple_socle_order': simple_order,
        'exponent': exponent,
        'number_of_divisors': len(ds),
        'exact_order_counts': COUNTS,
        'type_values_on_exponent_divisors': types,
        'mobius_inversion_exact': True,
        'source': 'https://arxiv.org/abs/2303.09460v1, Theorem 9'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
