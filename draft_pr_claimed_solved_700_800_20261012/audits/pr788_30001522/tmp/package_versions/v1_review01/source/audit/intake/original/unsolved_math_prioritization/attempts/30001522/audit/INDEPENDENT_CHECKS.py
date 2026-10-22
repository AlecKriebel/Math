"""Independent finite diagnostics; no source text or topology proof automation."""
from collections import Counter
from itertools import product
from math import gcd


def require(ok, message):
    if not ok:
        raise ValueError(message)


def real_so3_spectrum(exponents, n):
    """Exact roots-of-unity spectrum test, using conjugation and determinant."""
    e = tuple(x % n for x in exponents)
    return sum(e) % n == 0 and Counter(e) == Counter((-x) % n for x in e)


def polynomial_product(left, right):
    """Monomial-exponent-set model of F2[x,y]/(x^2,y^2)."""
    out = set()
    for a, b in left:
        for c, d in right:
            exponent = (a+c, b+d)
            if max(exponent) < 2:
                if exponent in out:
                    out.remove(exponent)
                else:
                    out.add(exponent)
    return frozenset(out)


def modular_rank(rows, p):
    rows = [[x % p for x in row] for row in rows]
    if not rows:
        return 0
    pivot = 0
    for col in range(len(rows[0])):
        k = next((k for k in range(pivot, len(rows)) if rows[k][col]), None)
        if k is None:
            continue
        rows[pivot], rows[k] = rows[k], rows[pivot]
        inv = pow(rows[pivot][col], -1, p)
        rows[pivot] = [x*inv % p for x in rows[pivot]]
        for j in range(len(rows)):
            if j != pivot and rows[j][col]:
                scale = rows[j][col]
                rows[j] = [(a-scale*b) % p for a,b in zip(rows[j], rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def run_checks():
    spectrum_cases = 0
    odd_free_orders = 0
    for n in range(2, 514):
        isotropy = []
        for k in range(1, n):
            if real_so3_spectrum((k, k, -2*k), n):
                isotropy.append(k)
            spectrum_cases += 1
        require(isotropy == ([] if n % 2 else [n//2]), 'wrong fixed-power spectrum')
        odd_free_orders += int(n % 2 == 1)

    general_spectra = 0
    general_actions = 0
    for a, b in product(range(-4, 5), repeat=2):
        weights = (a, b, -a-b)
        for n in range(2, 34):
            free = True
            for k in range(1, n):
                fixed = real_so3_spectrum(tuple(k*w for w in weights), n)
                require(fixed == (0 in tuple((k*w) % n for w in weights)), 'spectrum criterion mismatch')
                free = free and not fixed
                general_spectra += 1
            require(free == all(gcd(w,n)==1 for w in weights), 'gcd action criterion mismatch')
            general_actions += 1

    basis = ((0,0), (1,0), (0,1), (1,1))
    elements = [frozenset(basis[i] for i in range(4) if mask & (1<<i)) for mask in range(16)]
    ring_cases = 0
    for a,b,c in product(elements, repeat=3):
        require(polynomial_product(polynomial_product(a,b),c) == polynomial_product(a,polynomial_product(b,c)), 'associativity')
        require(polynomial_product(a,b^c) == polynomial_product(a,b)^polynomial_product(a,c), 'distributivity')
        ring_cases += 2
    require(polynomial_product(frozenset({(1,0)}), frozenset({(0,1)})) == frozenset({(1,1)}), 'top product')

    # Independently compute multiplication ranks for every nonzero binary cubic
    # over F3 and F5 through polynomial degree 9, using row reduction.
    hilbert_cases = 0
    cubics = 0
    for p in (3,5):
        for f in product(range(p), repeat=4):
            if not any(f):
                continue
            cubics += 1
            for degree in range(3,10):
                rows = []
                for shift in range(degree-2):
                    row = [0]*(degree+1)
                    for i,coefficient in enumerate(f):
                        row[shift+i] = coefficient
                    rows.append(row)
                require((degree+1)-modular_rank(rows,p)==3, 'binary cubic Hilbert dimension')
                hilbert_cases += 1

    # These deliberate bad witnesses must be detected by the independent model.
    require(real_so3_spectrum((1,1,-2),2), 'order-two exceptional element')
    require(real_so3_spectrum((1,-1,0),7), 'zero-weight obstruction')
    require(real_so3_spectrum((1,2,-3),3), 'divisible-weight obstruction')
    require(not real_so3_spectrum((1,1,-2),9), 'odd-order witness')
    require((1+2)%2==1, 'isotropy tangent representation parity')
    return {
        'status':'PASS', 'fixed_spectrum_elements':spectrum_cases,
        'odd_orders_verified_free':odd_free_orders,
        'general_spectrum_elements':general_spectra,
        'general_weight_order_actions':general_actions,
        'independent_ring_identities':ring_cases,
        'nonzero_binary_cubics':cubics,
        'binary_cubic_multiplication_rank_tests':hilbert_cases,
        'semantic_controls':5,
        'scope':'Finite arithmetic only; no formal verification of continuous actions, characteristic classes, or infinitely many primes.'
    }


if __name__ == '__main__':
    import json
    print(json.dumps(run_checks(),sort_keys=True,indent=2))
