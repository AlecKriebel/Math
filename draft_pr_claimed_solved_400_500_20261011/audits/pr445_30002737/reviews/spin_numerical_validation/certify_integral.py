#!/usr/bin/env python3
"""Certify the existing Frank–Mañibo Example 10 finite cocycle integral.

Only Python's standard library is required. Every acceptance guard is an explicit
exception, so optimization (-O) cannot remove it. See REPORT.md for the bounds.
"""
import argparse
import hashlib
import json
import math
import pathlib
import sys
import time
from datetime import datetime, timezone

MOD = 998244353
GENERATOR = 3


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def ceildiv(a, b):
    require(b > 0, 'nonpositive divisor')
    return -((-a) // b)


def ntt(values, inverse=False):
    n = len(values)
    require(n > 0 and n & (n - 1) == 0 and (MOD - 1) % n == 0,
            'unsupported NTT length')
    a = [v % MOD for v in values]
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = pow(GENERATOR, (MOD - 1) // length, MOD)
        if inverse:
            wlen = pow(wlen, MOD - 2, MOD)
        half = length // 2
        for start in range(0, n, length):
            w = 1
            for k in range(half):
                u = a[start + k]
                v = a[start + k + half] * w % MOD
                a[start + k] = (u + v) % MOD
                a[start + k + half] = (u - v) % MOD
                w = w * wlen % MOD
        length *= 2
    if inverse:
        inv = pow(n, MOD - 2, MOD)
        a = [v * inv % MOD for v in a]
    return a


def signed_residue(v):
    return v if v <= MOD // 2 else v - MOD


def matrix_polynomial(n):
    # Entries are (real coefficient list, imaginary coefficient list), in row order.
    a, b, c, d = ([1], [0]), ([0], [0]), ([0], [0]), ([1], [0])
    for _ in range(n):
        def first(p, q):
            return (p[0] + q[0], p[1] + q[1])
        def second(p, q):
            return ([-v for v in p[1]] + [-v for v in q[0]],
                    p[0] + [-v for v in q[1]])
        a, b, c, d = first(a, b), second(a, b), first(c, d), second(c, d)
    entries = [a, b, c, d]
    length = 1 << n
    require(all(len(v) == length for p in entries for v in p), 'polynomial length')
    require(all(r * r + i * i in (0, 1) for p in entries for r, i in zip(*p)),
            'unexpected coefficient magnitude')
    require(sum(r * r + i * i for p in entries for r, i in zip(*p)) == 1 << (n + 1),
            'coefficient norm/Parseval sanity failed')
    return entries


def exact_fourier_coefficients(entries, n):
    length = 1 << n
    size = 2 * length
    require(4 * length < MOD // 2, 'modular uniqueness bound fails')
    require(pow(GENERATOR, MOD - 1, MOD) == 1 and
            pow(GENERATOR, (MOD - 1) // 2, MOD) != 1 and
            pow(GENERATOR, (MOD - 1) // 7, MOD) != 1 and
            pow(GENERATOR, (MOD - 1) // 17, MOD) != 1,
            'NTT generator checks failed')
    # MOD is the known prime 119*2^23+1; check primality by exhaustive trial division.
    require(all(MOD % d for d in range(2, math.isqrt(MOD) + 1)), 'NTT modulus not prime')
    transformed = [(ntt(p[0] + [0] * length), ntt(p[1] + [0] * length))
                   for p in entries]
    re, im = [0] * size, [0] * size
    omega = pow(GENERATOR, (MOD - 1) // size, MOD)
    phase_step, phase = pow(omega, length - 1, MOD), 1
    for j in range(size):
        neg = (-j) % size
        for ar, ai in transformed:
            re[j] += phase * (ar[j] * ar[neg] + ai[j] * ai[neg])
            im[j] += phase * (ai[j] * ar[neg] - ar[j] * ai[neg])
        re[j] %= MOD
        im[j] %= MOD
        phase = phase * phase_step % MOD
    re, im = [signed_residue(v) for v in ntt(re, True)], [signed_residue(v) for v in ntt(im, True)]
    require(re[-1] == 0 and im[-1] == 0, 'convolution alias/padding failure')
    require(all(abs(v) <= 4 * length for v in re + im), 'autocorrelation bound failed')
    coeffs = {k: (re[k + length - 1], im[k + length - 1])
              for k in range(1 - length, length)}
    require(coeffs[0] == (1 << (n + 1), 0), 'exact mean failure')
    require(all(coeffs[-k] == (r, -i) for k, (r, i) in coeffs.items()),
            'Hermitian coefficient symmetry failed')
    require(all(pair == (0, 0) for k, pair in coeffs.items() if k & 1),
            'unexpected odd Fourier coefficients')
    # Independent exact determinant convolution uses the already transformed entries.
    ar, ai = transformed[0]
    br, bi = transformed[1]
    cr, ci = transformed[2]
    dr, di = transformed[3]
    detre = [(ar[j] * dr[j] - ai[j] * di[j] - br[j] * cr[j] + bi[j] * ci[j]) % MOD
             for j in range(size)]
    detim = [(ar[j] * di[j] + ai[j] * dr[j] - br[j] * ci[j] - bi[j] * cr[j]) % MOD
             for j in range(size)]
    detre = [signed_residue(v) for v in ntt(detre, True)]
    detim = [signed_residue(v) for v in ntt(detim, True)]
    er, ei = 1, 0
    for _ in range(n):
        er, ei = -er + ei, -er - ei
    require(all((r, i) == ((er, ei) if j == length - 1 else (0, 0))
                for j, (r, i) in enumerate(zip(detre, detim))),
            'exact determinant sanity failed')
    digest = hashlib.sha256(json.dumps(sorted(coeffs.items()), separators=(',', ':')).encode()).hexdigest()
    return coeffs, {'polynomial_length': length, 'ntt_length': size,
                    'coefficient_sha256': digest, 'exact_mean_S': 1 << (n + 1),
                    'determinant_coefficient': [er, ei],
                    'determinant_exponent': length - 1,
                    'determinant_modulus_squared': er * er + ei * ei}


class Fixed:
    def __init__(self, bits):
        self.R = 1 << bits

    def mul(self, x, y):
        products = [a * b for a in x for b in y]
        return min(products) // self.R, ceildiv(max(products), self.R)

    def add(self, x, y):
        return x[0] + y[0], x[1] + y[1]

    def sub(self, x, y):
        return x[0] - y[1], x[1] - y[0]

    def divint(self, x, d):
        return x[0] // d, ceildiv(x[1], d)

    def sqrt(self, x):
        require(x[0] >= 0, 'negative sqrt interval')
        low = math.isqrt(x[0] * self.R)
        upper_rad = x[1] * self.R
        high = math.isqrt(upper_rad)
        if high * high != upper_rad:
            high += 1
        return low, high

    def cmul(self, x, y):
        return (self.sub(self.mul(x[0], y[0]), self.mul(x[1], y[1])),
                self.add(self.mul(x[0], y[1]), self.mul(x[1], y[0])))

    def arctan_recip(self, q):
        lo, hi, power, j, sign = 0, 0, q, 0, 1
        while True:
            den = power * (2 * j + 1)
            a, b = self.R // den, ceildiv(self.R, den)
            if sign > 0:
                lo, hi = lo + a, hi + b
            else:
                lo, hi = lo - b, hi - a
            power *= q * q
            j += 1
            sign = -sign
            if power * (2 * j + 1) > self.R:
                tail = ceildiv(self.R, power * (2 * j + 1))
                return lo - tail, hi + tail
            require(j < 1000, 'arctan iteration limit')

    def pi(self):
        a, b = self.arctan_recip(5), self.arctan_recip(239)
        pi = (16 * a[0] - 4 * b[1], 16 * a[1] - 4 * b[0])
        require(3 * self.R < pi[0] < pi[1] < 4 * self.R, 'pi enclosure failure')
        return pi

    def sinc(self, k, cells, pi):
        if k == 0:
            return self.R, self.R
        t = self.divint((abs(k) * pi[0], abs(k) * pi[1]), cells)
        t2 = self.mul(t, t)
        require(0 <= t2[0] <= t2[1] < self.R, 'sinc alternating bound range failed')
        total, term = (self.R, self.R), (self.R, self.R)
        # Through j=20; the remainder is bounded by the next term.
        for j in range(1, 21):
            term = self.divint(self.mul(term, t2), (2 * j) * (2 * j + 1))
            total = self.sub(total, term) if j & 1 else self.add(total, term)
        nxt = self.divint(self.mul(term, t2), 42 * 43)[1]
        lo, hi = total[0] - nxt, total[1] + nxt
        require(0 < lo <= hi, 'nonpositive sinc enclosure')
        # sinc(t)<=1 for real t>=0, a separate elementary analytic bound.
        return lo, min(hi, self.R)

    def roots(self, cells):
        p = cells.bit_length() - 1
        require(cells == 1 << p and p >= 2, 'root order unsupported')
        powers = {2: ((0, 0), (self.R, self.R))}
        for order in range(3, p + 1):
            c = powers[order - 1][0]
            powers[order] = (
                self.sqrt(self.divint((self.R + c[0], self.R + c[1]), 2)),
                self.sqrt(self.divint((self.R - c[1], self.R - c[0]), 2)))
        roots, coordinate_error = [], 0
        for k in range(cells // 2):
            z = ((self.R, self.R), (0, 0))
            bits, j = k, 0
            while bits:
                if bits & 1:
                    z = self.cmul(z, powers[p - j])
                bits >>= 1
                j += 1
            r, i = (z[0][0] + z[0][1]) // 2, (z[1][0] + z[1][1]) // 2
            coordinate_error = max(coordinate_error,
                r - z[0][0], z[0][1] - r, i - z[1][0], z[1][1] - i)
            roots.append((r, i))
        # sqrt(dx^2+dy^2)<=2*max(|dx|,|dy|).
        return roots, 2 * coordinate_error

    def log_unit_series(self, u, terms=40, upper=True):
        # u is a fixed-point upper or lower bound, 0<=u<=1/3 (one ulp allowed).
        require(0 <= u <= ceildiv(self.R, 3), 'log series range failure')
        div = ceildiv if upper else (lambda a, b: a // b)
        u2 = div(u * u, self.R)
        power, total = u, 0
        for j in range(terms):
            total += div(power, 2 * j + 1)
            power = div(power * u2, self.R)
        if upper:
            # 2/(1-u^2)<3 in the allowed range; omitted tail starts with power.
            return 2 * total + ceildiv(3 * power, 2 * terms + 1)
        return 2 * total

    def log2_bounds(self):
        return (self.log_unit_series(self.R // 3, upper=False),
                self.log_unit_series(ceildiv(self.R, 3), upper=True))

    def log_upper(self, value, log2_upper):
        # value/R >= 1; exact normalization to [1,2).
        require(value >= self.R, 'log input below one')
        e = value.bit_length() - 1 - (self.R.bit_length() - 1)
        scale = self.R << e
        require(scale <= value < 2 * scale and e >= 0, 'log normalization failure')
        u = ceildiv(self.R * (value - scale), value + scale)
        return e * log2_upper + self.log_unit_series(u)


def fft_centers(a, roots, R):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        half, step = length // 2, n // length
        for start in range(0, n, length):
            for k in range(half):
                ar, ai = a[start + k]
                br, bi = a[start + k + half]
                cr, ci = roots[k * step]
                vr, vi = (br * cr - bi * ci) // R, (br * ci + bi * cr) // R
                a[start + k] = ar + vr, ai + vi
                a[start + k + half] = ar - vr, ai - vi
        length *= 2
    return a


def gauge_check():
    # Exact Gaussian-integer check: W^T=C W C^-1, C=diag(1,i).
    def gm(a, b):
        return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]
    W = [[(1, 0), (0, 1)], [(1, 0), (-1, 0)]]
    C, Ci = [(1, 0), (0, 1)], [(1, 0), (0, -1)]
    require(all(gm(gm(C[r], W[r][c]), Ci[c]) == W[c][r]
                for r in range(2) for c in range(2)), 'finite gauge identity failed')
    return {'C': ['1', 'i'], 'identity': 'W^T=C W C^-1',
            'commutes_with_D_z': True, 'unitary': True}


def certificate(n, cells, bits):
    started = time.monotonic()
    require(1 <= n <= 16, 'N outside audited coefficient/NTT range')
    require(cells & (cells - 1) == 0 and cells >= 4 * (1 << n),
            'cells must be power of two, at least 4*2^N')
    require(bits >= 80, 'precision below audited minimum')
    fixed = Fixed(bits)
    R = fixed.R
    coeffs, sanity = exact_fourier_coefficients(matrix_polynomial(n), n)
    pi = fixed.pi()
    inputs, input_coord_error = [(0, 0)] * cells, 0
    coefficient_l1 = sum(abs(r) + abs(i) for r, i in coeffs.values())
    for k, (r, i) in coeffs.items():
        sl, su = fixed.sinc(k, cells, pi)
        rl, ru = sorted((r * sl, r * su))
        il, iu = sorted((i * sl, i * su))
        rc, ic = (rl + ru) // 2, (il + iu) // 2
        inputs[k % cells] = rc, ic
        input_coord_error = max(input_coord_error, rc - rl, ru - rc, ic - il, iu - ic)
    roots, root_error = fixed.roots(cells)
    error = 2 * input_coord_error
    for _ in range(cells.bit_length() - 1):
        error = ceildiv((2 * R + root_error) * error, R) + root_error * coefficient_l1 + 2
    require(error < R, 'FFT error exceeds 1; increase precision')
    outputs = fft_centers(inputs, roots, R)
    require(all(abs(i) <= error for _, i in outputs), 'FFT imaginary enclosure failure')
    # Frobenius^2 >=2|det|; the weaker rational bound below suffices for positive logs.
    detsq = sanity['determinant_modulus_squared']
    lower_s = 2 * math.isqrt(detsq)
    require(all(r + error >= lower_s * R for r, _ in outputs),
            'cell-mean upper enclosure violates determinant lower sanity')
    require(sum(r for r, _ in outputs) >= cells * sanity['exact_mean_S'] * R - cells * error and
            sum(r for r, _ in outputs) <= cells * sanity['exact_mean_S'] * R + cells * error,
            'FFT exact-mean enclosure failure')
    log2_low, log2_high = fixed.log2_bounds()
    sum_logs_upper = sum(fixed.log_upper(r + error, log2_high) for r, _ in outputs)
    comparison_rhs = cells * n * log2_low
    require(sum_logs_upper < comparison_rhs, 'strict published inequality NOT certified')
    numerical_display = lambda numerator, denominator: format(numerator / denominator, '.16g')
    return {
        'status': 'CERTIFIED', 'N': n, 'cells': cells, 'bits': bits,
        'scale': str(R), 'source_cocycle_order': 'B(x)B(2x)...B(2^(N-1)x)',
        'integrand': 'log ||B^(N)(x)||_F^2',
        'bound_mechanism': 'Jensen on analytic cell means; certified fixed-point FFT and logarithms',
        'sum_cell_log_upper_scaled': str(sum_logs_upper),
        'comparison_M_N_log2_lower_scaled': str(comparison_rhs),
        'strict_integer_margin': str(comparison_rhs - sum_logs_upper),
        'normalized_integral_upper_display': numerical_display(sum_logs_upper, cells * n * R),
        'log2_lower_display': numerical_display(log2_low, R),
        'normalized_margin_lower_display': numerical_display(comparison_rhs - sum_logs_upper, cells * n * R),
        'log2_lower_scaled': str(log2_low), 'log2_upper_scaled': str(log2_high),
        'pi_lower_scaled': str(pi[0]), 'pi_upper_scaled': str(pi[1]),
        'coefficient_l1': coefficient_l1,
        'input_coordinate_error_scaled': str(input_coord_error),
        'root_euclidean_error_scaled': str(root_error),
        'final_fft_euclidean_error_scaled': str(error),
        'final_fft_error_display': numerical_display(error, R),
        'minimum_cell_mean_upper_display': numerical_display(min(r + error for r, _ in outputs), R),
        'gauge': gauge_check(), 'sanity': sanity,
        'elapsed_seconds': round(time.monotonic() - started, 3),
        'utc_completed': datetime.now(timezone.utc).isoformat(),
        'python': sys.version,
        'display_numbers_are_noncertifying': True,
        'acceptance_uses_exact_integer_comparison': True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--N', type=int, default=13)
    parser.add_argument('--cells', type=int, default=65536)
    parser.add_argument('--bits', type=int, default=100)
    parser.add_argument('--output', type=pathlib.Path)
    args = parser.parse_args()
    result = certificate(args.N, args.cells, args.bits)
    output = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(output)
    sys.stdout.write(output)


if __name__ == '__main__':
    main()
