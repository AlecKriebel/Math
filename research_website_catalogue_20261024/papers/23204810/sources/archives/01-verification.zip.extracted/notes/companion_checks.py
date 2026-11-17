"""Exact finite checks for the companion EGH audit (not an EGH proof).

Run with Python 3. Uses only the standard library and deterministic exhaustive
coefficient enumeration. Arithmetic is in (Z/p^v)[u]/(u^(h+1)).
"""
from itertools import product
from math import comb


def truncated_product(a, q, modulus, h):
    return tuple(sum(a[i] * q[n-i]
                     for i in range(len(a)) if 0 <= n-i < len(q)) % modulus
                 for n in range(h+1))


def check_case(p, v, nu):
    modulus = p**v
    h = v * nu
    count = 0
    solutions = 0
    # All A of degree nu with exact order nu after reduction modulo p.
    lows = range(0, modulus, p)
    leading = [a for a in range(modulus) if a % p]
    for low in product(lows, repeat=nu):
        for lead in leading:
            a = low + (lead,)
            for q in product(range(modulus), repeat=h+1):
                count += 1
                if not any(truncated_product(a, q, modulus, h)):
                    solutions += 1
                    assert q[0] == 0, (p, v, nu, a, q)
    return {"p": p, "v": v, "nu": nu, "h": h,
            "pairs_checked": count, "annihilating_pairs": solutions}


def a_b(b):
    return tuple((-1)**i * comb(b, i+1) for i in range(b))


if __name__ == "__main__":
    for case in [(2, 1, 0), (2, 2, 1), (2, 2, 2), (3, 2, 1), (2, 3, 1)]:
        print(check_case(*case))
    # Deliberately violate the truncation bound: h=1 < v*nu=2.
    assert truncated_product((2, 1), (2, -1), 4, 1) == (0, 0)
    print({"sharpness_example": "(2+u)(2-u)=0 mod (4,u^2), Q(0)=2"})
    # Frobenius-order check used in the last step of the division theorem.
    checked = 0
    for p in [2, 3, 5, 7]:
        for b in range(2, 101):
            power = 1
            temp = b
            while temp % p == 0:
                power *= p
                temp //= p
            order = next(i for i, c in enumerate(a_b(b)) if c % p)
            assert order == power - 1, (p, b, order, power)
            checked += 1
    print({"frobenius_orders_checked": checked})
