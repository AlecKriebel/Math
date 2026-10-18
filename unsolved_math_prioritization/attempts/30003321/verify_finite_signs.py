#!/usr/bin/env python3
"""Finite sign/finite-support diagnostics, not an all-ordinal theorem proof.

Run normally or with -O. Mutation modes alter the actual construction and must
fail a computed mathematical property; no unconditional rejection is used.
"""
import argparse
from fractions import Fraction
from itertools import product
import json


def need(ok, why):
    if not ok:
        raise ValueError(why)


def cmp(x, y):
    for j in range(max(len(x), len(y))):
        a = x[j] if j < len(x) else 0
        b = y[j] if j < len(y) else 0
        if a != b:
            return (a > b) - (a < b)
    return 0


def prefix(x, y):
    return len(x) < len(y) and y[:len(x)] == x


def rotate(s, a, mutation):
    if s == a:
        return (1,) if mutation == 'keep_minimum' else ()
    if s[:len(a)] == a:
        if mutation == 'omit_deletion':
            return (1,) + s
        return (1,) + a + s[len(a) + 1:]
    return s + (1,) if mutation == 'append_plus' else (1,) + s


def inverse(z, a):
    if not z:
        return a
    v = z[1:]
    return a + (1,) + v[len(a):] if v[:len(a)] == a else v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutation', choices=['omit_deletion', 'keep_minimum',
                                         'append_plus', 'omit_scaling'])
    opt = ap.parse_args()
    counts = dict(minima=0, nodes=0, ordered_pairs=0, prefix_sets=0,
                  right_predecessors=0, support_additions=0, bottom_generators=0)
    words = [v for k in range(8) for v in product((-1, 1), repeat=k)]
    for alpha in range(7):
        a = (-1,) * alpha
        gamma = [s for s in words if cmp(s, a) >= 0]
        image = {s: rotate(s, a, opt.mutation) for s in gamma}
        delta = set(image.values())
        counts['minima'] += 1
        need(len(delta) == len(gamma), 'rotation collision')
        need(image[a] == (), 'minimum did not map to zero')
        for s in gamma:
            counts['nodes'] += 1
            fs = image[s]
            need(inverse(fs, a) == s, 'explicit inverse failure')
            need(cmp(fs, ()) >= 0, 'negative target exponent')
            actual = {fs[:k] for k in range(len(fs))}
            expected = {()} | {image[s[:k]] for k in range(len(s))
                               if s[:k] != a}
            if s == a:
                expected = set()
            need(actual == expected, 'complete finite prefix identity failure')
            need(actual <= delta, 'image is not prefix closed')
            counts['prefix_sets'] += 1
            for t in gamma:
                counts['ordered_pairs'] += 1
                ft = image[t]
                need(cmp(s, t) == cmp(fs, ft), 'order comparison failure')
                if s != a and t != a:
                    need(prefix(s, t) == prefix(fs, ft), 'prefix reflection failure')
                if prefix(fs, ft) and cmp(fs, ft) > 0:
                    counts['right_predecessors'] += 1
                    need(s != a and prefix(s, t) and cmp(s, t) > 0,
                         'new right-predecessor obligation')
        for n in range(4):
            scale = 1 if opt.mutation == 'omit_scaling' else 2 ** n
            need(Fraction(1, 2 ** n) * scale == 1,
                 'bottom source generator does not map to target unit')
            counts['bottom_generators'] += 1
            def transport(v):
                return {image[y]: r * (scale if y == a else 1)
                        for y, r in v.items() if r}
            def add(u, v):
                return {y: u.get(y, 0) + v.get(y, 0)
                        for y in set(u) | set(v) if u.get(y, 0) + v.get(y, 0)}
            for j in range(32):
                u = {gamma[(j + k * 7) % len(gamma)]: Fraction((-1) ** k * (j + 1), 8)
                     for k in range(4)}
                v = {gamma[(2 * j + k * 11) % len(gamma)]: Fraction((-1) ** (k + 1) * (j + 2), 4)
                     for k in range(4)}
                # Ensure every sampled bottom coefficient belongs to 2^-n Z.
                if a in u:
                    u[a] = Fraction(j + 1, 2 ** n)
                if a in v:
                    v[a] = Fraction(-(j + 2), 2 ** n)
                need(transport(add(u, v)) == add(transport(u), transport(v)),
                     'finite-support additivity failure')
                counts['support_additions'] += 1
    print(json.dumps({'status': 'PASS', 'scope': 'finite signs through length7; minima0..6; finite-support rational diagnostics only',
                      'counts': counts, 'not_all_ordinal_or_class_proof': True}, sort_keys=True))


if __name__ == '__main__':
    main()
