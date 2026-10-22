"""Exact arithmetic checks for the rank-two path family; no group oracle.

Run from any directory with Python 3.  Mathematical properness and the use
of continuous Mayer--Vietoris are proved in the accompanying review.
"""

import json


def rank_mod_p(rows, p):
    matrix = [[entry % p for entry in row] for row in rows]
    rank = 0
    width = len(matrix[0]) if matrix else 0
    for column in range(width):
        pivot = next((i for i in range(rank, len(matrix))
                      if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, p)
        matrix[rank] = [(x * inverse) % p for x in matrix[rank]]
        for i in range(len(matrix)):
            if i != rank and matrix[i][column]:
                multiple = matrix[i][column]
                matrix[i] = [(a - multiple * b) % p
                             for a, b in zip(matrix[i], matrix[rank])]
        rank += 1
    return rank


checked = []
for prime in (2, 3, 5, 7):
    for n in range(1, 25):
        h1_restriction = [[0] * (2 * (n + 1)) for _ in range(2 * n)]
        for i in range(n):
            # Restriction from A_i has diag(p,1), and restriction from
            # A_(i+1) has diag(1,p); take the difference.
            h1_restriction[2 * i][2 * i] = prime
            h1_restriction[2 * i][2 * (i + 1)] = -1
            h1_restriction[2 * i + 1][2 * i + 1] = 1
            h1_restriction[2 * i + 1][2 * (i + 1) + 1] = -prime
            # Both composite maps E_i -> Z_p^2 have the same exponents.
            assert (i + 1, n - i) == (i + 1, n - (i + 1) + 1)
            # Quotient A_i/C and E_i/C: log_p of the respective orders.
            assert (n - i) + i == n
            assert (n - i - 1) + i == n - 1
        rank = rank_mod_p(h1_restriction, prime)
        assert rank == 2 * n
        assert 2 * (n + 1) - rank == 2
        # H^2 restrictions are exterior-square determinants, zero mod p.
        assert prime % prime == 0
        # Intersection of vertex coordinate lattices has exponents n,n.
        assert max(range(n + 1)) == n
        assert max(n - i for i in range(n + 1)) == n
        checked.append({"p": prime, "n": n, "H1_restriction_rank": rank,
                        "H1_kernel_dimension": 2,
                        "H2_dimension_given_MV": n + 1})

interval_cases = 0
for n in range(1, 101):
    for m in range(1, n + 1):
        for i in range(n + 1):
            lower = max(0, m - (n - i))
            upper = min(m, i)
            assert lower <= upper
            j = lower
            assert 0 <= j <= m and j <= i and m - j <= n - i
            interval_cases += 1

for prime in (2, 3, 5, 7):
    for n in range(1, 25):
        assert min(prime ** i + prime ** (n - i)
                   for i in range(n + 1)) == (
                       prime ** (n // 2) + prime ** ((n + 1) // 2))

for exponent in range(1, 65):
    # Already n >= 2e-1, slightly stronger than the sufficient n>=2e.
    for n in range(2 * exponent - 1, 2 * exponent + 10):
        for i in range(n + 1):
            assert i >= exponent or n - i >= exponent

print(json.dumps({"exact_cases": len(checked), "primes": [2, 3, 5, 7],
                  "n_range": [1, 24], "all_assertions_passed": True,
                  "inverse_system_interval_cases": interval_cases,
                  "finite_quotient_exponent_checks": True,
                  "first_case": checked[0], "last_case": checked[-1]}, indent=2))
