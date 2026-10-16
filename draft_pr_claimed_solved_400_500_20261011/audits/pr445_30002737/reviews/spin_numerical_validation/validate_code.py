#!/usr/bin/env python3
"""Check exact convolution against independent quadratic sums for small N."""
import json
from certify_integral import Fixed, exact_fourier_coefficients, gauge_check, matrix_polynomial, require


def main():
    checks = []
    for n in range(1, 7):
        entries = matrix_polynomial(n)
        coeffs, _ = exact_fourier_coefficients(entries, n)
        L = 1 << n
        for k in range(1 - L, L):
            real, imag = 0, 0
            for re, im in entries:
                for s in range(L):
                    r = s + k
                    if 0 <= r < L:
                        real += re[r] * re[s] + im[r] * im[s]
                        imag += im[r] * re[s] - re[r] * im[s]
            require(coeffs[k] == (real, imag), 'independent exact autocorrelation mismatch')
        checks.append({'N': n, 'exact_direct_autocorrelation_matches_NTT': True})
    f = Fixed(100)
    lo, hi = f.log2_bounds()
    require(lo < hi, 'nontrivial log2 enclosure')
    # Exact monotonicity checks on representative rational arguments.
    values = [f.R, f.R + 1, 3 * f.R // 2, 2 * f.R, 180 * f.R, 16384 * f.R]
    uppers = [f.log_upper(x, hi) for x in values]
    require(uppers == sorted(uppers), 'log upper monotonicity sanity failed')
    require(uppers[0] == 0, 'log1 should be zero')
    print(json.dumps({'status': 'PASSED', 'checks': checks, 'finite_gauge': gauge_check(),
                      'log1_and_monotonicity_sanity': True}, indent=2))


if __name__ == '__main__':
    main()
