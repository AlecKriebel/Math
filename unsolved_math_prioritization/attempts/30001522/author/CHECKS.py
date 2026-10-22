"""Finite arithmetic diagnostics only. This is not a topology proof checker."""
from math import gcd


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fixed_powers(weights, order):
    require(isinstance(order, int) and order >= 2, "order must be >=2")
    require(len(weights) == 3 and sum(weights) == 0, "SU(3) weights must sum to zero")
    # Necessary and sufficient spectrum test for conjugacy into SO(3).
    return tuple(k for k in range(1, order)
                 if any((k * w) % order == 0 for w in weights))


def free_by_gcd(weights, order):
    return all(gcd(abs(w), order) == 1 for w in weights)


def ring_multiply(a, b):
    """F2[x,y]/(x^2,y^2), basis 1,x,y,xy and bitset elements."""
    ans = 0
    for i in range(4):
        for j in range(4):
            if (a >> i) & 1 and (b >> j) & 1 and not (i & j):
                ans ^= 1 << (i | j)
    return ans


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def run_checks():
    count = 0
    for n in range(2, 513):
        actual = fixed_powers((1, 1, -2), n)
        expected = () if n % 2 else (n // 2,)
        require(actual == expected, "fixed-power parity test failed")
        count += 1
    generalized = 0
    for a in range(-4, 5):
        for b in range(-4, 5):
            weights = (a, b, -a-b)
            for n in range(2, 48):
                require((not fixed_powers(weights, n)) == free_by_gcd(weights, n),
                        "enumerated/gcd freeness mismatch")
                generalized += 1
    primes = [p for p in range(3, 998) if is_prime(p)]
    for p in primes:
        require(not fixed_powers((1, 1, -2), p), "odd prime diagnostic failed")
    # Semantic negative controls: bad weights and the exceptional prime really fail.
    require(fixed_powers((1, 1, -2), 2) == (1,), "p=2 must fail")
    require(fixed_powers((1, -1, 0), 7) == tuple(range(1, 7)), "zero weight must fail")
    require(fixed_powers((1, 2, -3), 3) == (1, 2), "weight divisible by p must fail")
    require(not fixed_powers((1, 2, -3), 5), "coprime positive control must pass")
    require(not fixed_powers((1, 1, -2), 9), "odd composite positive control must pass")
    require(fixed_powers((1, 1, -2), 10) == (5,), "even composite negative control")
    try:
        fixed_powers((1, 1, -1), 5)
    except ValueError:
        pass
    else:
        raise ValueError("non-SU(3) weights were accepted")

    ring_tests = 0
    for a in range(16):
        require(ring_multiply(a, 1) == a, "ring identity failed")
        ring_tests += 1
        for b in range(16):
            require(ring_multiply(a, b) == ring_multiply(b, a), "commutativity failed")
            ring_tests += 1
            for c in range(16):
                require(ring_multiply(ring_multiply(a, b), c) ==
                        ring_multiply(a, ring_multiply(b, c)), "associativity failed")
                require(ring_multiply(a, b ^ c) ==
                        ring_multiply(a, b) ^ ring_multiply(a, c), "distributivity failed")
                ring_tests += 2
    x, y, xy = 2, 4, 8
    require(ring_multiply(x, x) == ring_multiply(y, y) == 0, "square relation failed")
    require(ring_multiply(x, y) == xy, "top characteristic product failed")
    top_evaluation = lambda a: (a >> 3) & 1
    characteristic_number = top_evaluation(ring_multiply(x, y))
    require(characteristic_number == 1, "assumed classical number not one")
    require((2 * characteristic_number) % 2 == 0, "even cover parity failed")
    require((3 * characteristic_number) % 2 == 1, "odd cover control failed")

    # A nonzero cubic in two polynomial variables has this Hilbert function.
    hilbert = [(m+1) - max(0, m-2) for m in range(13)]
    require(hilbert == [1, 2, 3] + [3]*10, "cubic quotient Hilbert diagnostic failed")
    return {
        "fixed_space": "SU(3)/SO(3)",
        "weights": [1, 1, -2],
        "cyclic_orders_checked": [2, 512],
        "cyclic_parity_cases": count,
        "general_weight_order_cases": generalized,
        "odd_primes_checked": len(primes),
        "largest_odd_prime_checked": max(primes),
        "ring_identity_cases": ring_tests,
        "semantic_controls": 9,
        "classical_w2w3_evaluation_replayed": characteristic_number,
        "cubic_quotient_hilbert_degrees_0_through_12": hilbert,
        "scope": "Finite arithmetic diagnostics; not a proof of topological or infinite-prime claims."
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_checks(), sort_keys=True, indent=2))
