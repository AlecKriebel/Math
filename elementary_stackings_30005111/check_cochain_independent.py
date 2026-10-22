#!/usr/bin/env python3
"""Independent exact certificate validation and negative corruption controls."""
from fractions import Fraction
from itertools import product
import json
import check_cochain as source


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_input(vs, es):
    n = len(vs)
    require(n > 0 and len(es) == n, 'input dimensions')
    endpoints = {}
    for i, (e, sign) in enumerate(es):
        require(sign in (-1, 1), 'invalid direction')
        end = (vs[i], vs[(i + 1) % n])
        if sign == -1:
            end = end[::-1]
        require(e not in endpoints or endpoints[e] == end, 'inconsistent graph edge')
        endpoints[e] = end
        f, next_sign = es[(i + 1) % n]
        require(e != f or sign != -next_sign, 'nonimmersed input')


def validate(vs, es, h):
    n = len(vs)
    require(n > 0 and len(es) == n and len(h) == n, 'certificate dimensions')
    require(all(isinstance(x, Fraction) for x in h), 'nonexact certificate')
    endpoints = {}
    for i, (e, sign) in enumerate(es):
        require(sign in (-1, 1), 'invalid direction')
        end = (vs[i], vs[(i + 1) % n])
        if sign == -1:
            end = end[::-1]
        require(e not in endpoints or endpoints[e] == end, 'inconsistent graph edge')
        endpoints[e] = end
    for i in range(n):
        for j in range(i):
            if vs[i] == vs[j]:
                require(h[i] != h[j], 'vertex collision')
            if es[i][0] == es[j][0]:
                ai, bi = h[i], h[(i + 1) % n]
                aj, bj = h[j], h[(j + 1) % n]
                if es[i][1] < 0:
                    ai, bi = bi, ai
                if es[j][1] < 0:
                    aj, bj = bj, aj
                require((ai - aj) * (bi - bj) > 0, 'edge collision')


def inspect(vs, es):
    validate_input(vs, es)
    h, trace, degree = source.solve(vs, es)
    require(all(a[0] < b[0] for a, b in zip(trace, trace[1:])), 'nonincreasing vertex count')
    require(all(t[0] <= len(vs) and t[2] == t[1] - t[0] + 1 for t in trace), 'bad trace')
    require(trace[-1][2] == 1, 'noncircle terminal image')
    require(trace[-1][0] * degree == len(vs), 'invalid covering degree')
    if h is not None:
        validate(vs, es, h)
    return h, degree


def main():
    counts = {'rose_cases': 0, 'subdivided_cases': 0, 'additional_graph_cases': 0,
              'rejected_corruptions': 0, 'rejected_invalid_inputs': 0}
    for n in range(1, 8):
        for w in product((1, -1, 2, -2), repeat=n):
            if any(w[i] == -w[(i + 1) % n] for i in range(n)):
                continue
            vs = [0] * n
            es = [(abs(x), 1 if x > 0 else -1) for x in w]
            h, degree = inspect(vs, es)
            period = next(p for p in range(1, n + 1) if n % p == 0 and all(w[i] == w[i % p] for i in range(n)))
            require(degree == n // period, 'incorrect exact root degree')
            require((h is not None) == (period == n), 'wrong existence outcome')
            counts['rose_cases'] += 1
            if n <= 5:
                sv, se = [], []
                for e, sign in es:
                    sv += [0, e]
                    se += [(2*e, 1), (2*e+1, -1)] if sign > 0 else [(2*e+1, 1), (2*e, -1)]
                hh, dd = inspect(sv, se)
                require(dd == degree and (hh is not None) == (h is not None), 'subdivision mismatch')
                counts['subdivided_cases'] += 1
    graphs = [([0, 0, 1, 1], [(1, 1), (3, 1), (2, 1), (3, -1)]),
              ([0, 1, 0, 1, 0, 1], [(1, 1), (2, -1), (3, 1), (1, -1), (2, 1), (3, -1)])]
    for vs, es in graphs:
        for k in (1, 2, 3):
            h, degree = inspect(vs*k, es*k)
            require(degree == k and (h is not None) == (k == 1), 'additional graph root failure')
            counts['additional_graph_cases'] += 1
    vs = [0]*4
    es = [(1, 1), (2, 1), (1, -1), (2, -1)]
    good, _ = inspect(vs, es)
    bad = [([Fraction(0)]*4, 'vertex collision'),
           ([Fraction(0), Fraction(1), Fraction(1, 3), Fraction(4, 3)], 'edge collision'),
           (good[:-1], 'certificate dimensions'),
           ([float(x) for x in good], 'nonexact certificate')]
    for h, reason in bad:
        try:
            validate(vs, es, h)
        except ValueError as exc:
            require(str(exc) == reason, 'unexpected corruption rejection reason')
            counts['rejected_corruptions'] += 1
        else:
            raise ValueError('accepted corrupted certificate: ' + reason)
    invalid = [([], [], 'input dimensions'),
               ([0], [(1, 0)], 'invalid direction'),
               ([0, 1], [(1, 1), (1, 1)], 'inconsistent graph edge'),
               ([0, 1], [(1, 1), (1, -1)], 'nonimmersed input')]
    for iv, ie, reason in invalid:
        try:
            inspect(iv, ie)
        except ValueError as exc:
            require(str(exc) == reason, 'unexpected invalid-input rejection')
            counts['rejected_invalid_inputs'] += 1
        else:
            raise ValueError('accepted invalid input: ' + reason)
    print(json.dumps({'PASS': True, 'counts': counts}, indent=2))


if __name__ == '__main__':
    main()
