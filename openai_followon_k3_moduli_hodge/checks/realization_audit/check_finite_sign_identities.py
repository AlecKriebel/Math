"""Check only the finite algebraic sign identities used in comparison.tex.

No analytic moduli-space, determinant-orientation, or Kuranishi premise is
verified by this script. Run with Python 3; no third-party dependencies.
"""

from itertools import product


def check_sign_identities():
    for b, l, q, r, o in product(range(2), repeat=5):
        exponent = b * (l + q + r + o) + q * (b + q + r + o)
        exponent += (r + o) * (b + q)
        assert exponent % 2 == (b * l + q) % 2

    for p, q in product(range(40), repeat=2):
        exponent = (p + q) * (p + q - 1) // 2 + p * q
        exponent -= p * (p - 1) // 2 + q * (q - 1) // 2
        assert exponent % 2 == 0

    for d in range(1, 80):
        exponent = d * (d - 1) // 2 + d + 1
        exponent -= (d - 1) * (d - 2) // 2
        assert exponent % 2 == 0


if __name__ == "__main__":
    check_sign_identities()
    print("All 32 + 1600 + 79 finite sign checks passed.")
