#!/usr/bin/env python3
"""Independent exact finite corroboration; no finite check proves a universal claim."""
import argparse
from itertools import product
import importlib.util
import json
import os
from pathlib import Path
import sys


def require(value, message):
    if not value:
        raise RuntimeError(message)


class Reference:
    """Word normalization by adjacent swaps, independent of exponent-inversion formula."""
    def __init__(self, degrees, modulus=0, exterior=True):
        self.degrees = tuple(degrees)
        self.modulus = modulus
        self.exterior = exterior

    def normalize(self, word):
        word = list(word)
        sign = 1
        for end in range(len(word), 0, -1):
            for j in range(end - 1):
                if word[j] > word[j+1]:
                    if self.degrees[word[j]] % 2 and self.degrees[word[j+1]] % 2:
                        sign = -sign
                    word[j], word[j+1] = word[j+1], word[j]
        if self.exterior:
            for a, b in zip(word, word[1:]):
                if a == b and self.degrees[a] % 2:
                    return None, 0
        return tuple(word), sign

    def clean(self, terms):
        out = {}
        for word, value in terms:
            key, sign = self.normalize(word)
            if key is not None:
                out[key] = out.get(key, 0) + sign * value
        if self.modulus:
            out = {k: int(v) % self.modulus for k, v in out.items()}
        return {k: v for k, v in out.items() if v}

    def c(self, value):
        return self.clean([((), value)])

    def gen(self, i):
        return {(i,): 1}

    def add(self, *polys):
        return self.clean([(k, v) for p in polys for k, v in p.items()])

    def scale(self, p, value):
        return self.clean([(k, value*v) for k, v in p.items()])

    def mul(self, *polys):
        out = self.c(1)
        for p in polys:
            out = self.clean([(a+b, x*y) for a, x in out.items() for b, y in p.items()])
        return out

    def power(self, p, n):
        return self.mul(*([p] * n))

    def d(self, p, differentials):
        out = []
        for word, coeff in p.items():
            for j, letter in enumerate(word):
                sign = -1 if sum(self.degrees[k] for k in word[:j]) % 2 else 1
                for replacement, v in differentials[letter].items():
                    out.append((word[:j] + replacement + word[j+1:], coeff * sign * v))
        return self.clean(out)

    def degree_part(self, p, degree):
        return {k: v for k, v in p.items() if sum(self.degrees[i] for i in k) == degree}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('native_checker', type=Path)
    args = parser.parse_args()
    require(os.getuid() == 1000, 'actual UID must be 1000')
    spec = importlib.util.spec_from_file_location('audited_checker', args.native_checker)
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    results = {}

    comparisons = 0
    for modulus, exterior in [(0, True), (2, True), (3, True), (5, True), (2, False)]:
        degrees = [-3, 2, 1, -2]
        R = Reference(degrees, modulus, exterior)
        N = native.Algebra(degrees, modulus=modulus, exterior=exterior)
        for length in range(6):
            for word in product(range(4), repeat=length):
                ref = R.clean([(word, 1)])
                got = N.c(1)
                for i in word:
                    got = N.mul(got, N.gen(i))
                expected = {}
                for k, v in ref.items():
                    expected[tuple(k.count(i) for i in range(4))] = v
                require(got == expected, 'independent word normalization mismatch')
                comparisons += 1
    results['word_normalization_comparisons'] = comparisons

    # Higher nilpotent correction: the quadratic correction term is essential.
    R = Reference([2, -2, 1, 1, -1, 3, -3])
    x, t, a, b, c, e, f = [R.gen(i) for i in range(7)]
    eta = R.add(R.mul(b, c), R.mul(e, f))
    ds = [b, f, R.add(R.c(1), eta), {}, {}, {}, {}]
    require(all(not R.d(p, ds) for p in ds), 'd squared in higher correction example')
    require(bool(R.power(eta, 2)), 'quadratic correction must be nonzero')
    require(not R.power(eta, 3), 'nilpotence index three')
    short = R.mul(a, R.add(R.c(1), R.scale(eta, -1)))
    corrected = R.mul(a, R.add(R.c(1), R.scale(eta, -1), R.power(eta, 2)))
    require(R.d(short, ds) != R.c(1), 'short correction incorrectly passed')
    require(R.d(corrected, ds) == R.c(1), 'full correction failed')
    require(R.degree_part(corrected, 1) == corrected, 'mixed degree primitive homogeneity')
    results['higher_nilpotent_correction'] = {'square_nonzero': True, 'cube_zero': True, 'short_rejected': True, 'full_pass': True}

    # Extract an actual homogeneous certificate from inhomogeneous coefficients.
    R = Reference([2, -2, 1, 3])
    x, t, a, b = [R.gen(i) for i in range(4)]
    q1 = R.add(R.c(1), R.mul(x, t)); q2 = x
    r = R.add(R.c(1), x)
    a1 = R.add(R.c(1), R.mul(r, q2))
    a2 = R.add(R.scale(t, -1), R.scale(R.mul(r, q1), -1))
    require(R.add(R.mul(a1, q1), R.mul(a2, q2)) == R.c(1), 'inhomogeneous ideal certificate')
    e1 = R.degree_part(a1, 0); e2 = R.degree_part(a2, -2)
    require(e1 == R.c(1) and e2 == R.scale(t, -1), 'homogeneous extraction')
    h = R.add(R.mul(e1, a), R.mul(e2, b))
    require(R.d(h, [{}, {}, q1, q2]) == R.c(1), 'extracted primitive')
    results['mixed_degree_extraction'] = 'PASS'

    # A sign-only characteristic-two certificate whose naive primitive fails.
    R = Reference([0, 1, -1, 0, 1], modulus=2, exterior=False)
    x, a, c, b, e = [R.gen(i) for i in range(5)]
    ds = [c, b, {}, {}, R.c(1)]
    coeffs = [R.mul(x, b), R.mul(x, c), R.c(1)]
    generators = [x, a, e]
    images = [c, b, R.c(1)]
    certificate = R.add(*(R.mul(u, v) for u, v in zip(coeffs, images)))
    require(certificate == R.c(1), 'characteristic-two ideal certificate')
    naive = R.add(*(R.mul(u, v) for u, v in zip(coeffs, generators)))
    require(R.d(naive, ds) != R.c(1), 'naive characteristic-two primitive must fail')
    h = R.add(*(R.mul(R.power(u, 2), v, dv) for u, v, dv in zip(coeffs, generators, images)))
    require(R.d(h, ds) == R.c(1), 'characteristic-two squaring construction')
    require(R.d(R.degree_part(h, 1), ds) == R.c(1), 'degree-one extraction after squaring')
    require(bool(R.power(c, 2)), 'odd square must survive in sign-only characteristic two')
    results['char2_sign_only_nonlinear_certificate'] = 'PASS'

    # Independently vary every defining-system primitive in a bounded coefficient set.
    cases = 0
    for n in range(1, 11):
        R = Reference([0, 0, -1])
        x, z, y = [R.gen(i) for i in range(3)]
        xn = R.power(x, n); ds = [{}, R.mul(xn, y), {}]
        for p0, p1, q0, q1 in product(range(-1, 2), repeat=4):
            p = R.add(R.c(p0), R.scale(x, p1))
            q = R.add(R.c(q0), R.scale(x, q1))
            u = R.add(z, p); v = R.add(z, q)
            require(R.d(u, ds) == R.mul(y, xn), 'left Massey primitive')
            require(R.d(v, ds) == R.mul(xn, y), 'right Massey primitive')
            m = R.add(R.mul(y, v), R.mul(u, y))
            remainder = {word: coeff for word, coeff in m.items() if word.count(0) < n and word.count(1) > 0}
            require(remainder == R.scale(R.mul(z, y), 2), 'Massey quotient obstruction')
            require(not R.d(m, ds), 'Massey representative cycle')
            cases += 1
        require(bool({w:c for w,c in R.mul(R.power(x, n-1), y).items() if w.count(0)<n}), 'annihilator lower exponent witness')
        require(not {w:c for w,c in R.mul(xn, y).items() if w.count(0)<n}, 'annihilator exponent n')
    results['massey_defining_system_samples'] = cases
    results['annihilator_exponents_checked'] = list(range(1, 11))

    # Matrix-level count independently uses only determinant and differential relation.
    counts = {}
    for p in (2, 3, 5, 7):
        for k in range(p):
            count = 0
            for a, b, c, d in product(range(p), repeat=4):
                det = (a*d-b*c) % p
                for lam in range(p):
                    if det and lam and (k*lam-det) % p == 0:
                        count += 1
            expected = 0 if k == 0 else (p*p-1)*(p*p-p)
            require(count == expected, 'independent strict isomorphism count')
            counts[f'{p}:{k}'] = count
    results['finite_field_matrix_counts'] = counts
    print(json.dumps({'status': 'PASS', 'uid': os.getuid(), 'optimization': sys.flags.optimize, 'checks': results, 'scope': 'Finite exact corroboration, not a universal proof.'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
