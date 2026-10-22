"""Independent protocol and mass-action transfer controls; standard library."""
from fractions import Fraction as F
from itertools import product
import json
import math


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def dfc_events(state, lam):
    a, b, x, y = state
    D = x + y + 1
    ds = ((1, 0, 0, 0), (0, 1, 0, 0), (-1, 0, 1, 0),
          (0, -1, 0, 1), (0, 0, -1, 0), (0, 0, 0, -1))
    rs = (lam / 2, lam / 2, F(a * (x + 1), D), F(b * (y + 1), D),
          F(x * (y + 1), D), F(y * (x + 1), D))
    return [(d, q, tuple(v + dv for v, dv in zip(state, d)))
            for d, q in zip(ds, rs) if q]


def generator(state, lam, fn):
    old = fn(state)
    return sum(rate * (fn(after) - old) for _, rate, after in dfc_events(state, lam))


def common_chunk_rates(z, x, y):
    rates = [F(0)] * 4
    counts = (z, x, y, 1)
    S = sum(counts)
    for sample in product(range(4), repeat=3):
        probability = math.prod(F(counts[m], S) for m in sample)
        n1 = sum(bool(m & 1) for m in sample)
        n2 = sum(bool(m & 2) for m in sample)
        rare = [j for j, n in enumerate((n1, n2)) if n == 1]
        for j in rare:
            rates[j] += z * probability / len(rare)
        if n1 >= 2 and n2 >= 1:
            rates[2] += x * probability
        if n2 >= 2 and n1 >= 1:
            rates[3] += y * probability
    return rates


def network(lam):
    zero = (0, 0, 0, 0)
    unit = [tuple(int(i == j) for i in range(4)) for j in range(4)]
    add = lambda s, t: tuple(a + b for a, b in zip(s, t))
    A, B, X, Y = unit
    channels = []
    for target in (A, B):
        for catalyst in (zero, X, Y):
            channels.append((catalyst, add(catalyst, target), lam / 2))
    channels += [(A, X, F(1)), (add(A, X), add(X, X), F(1)),
                 (B, Y, F(1)), (add(B, Y), add(Y, Y), F(1)),
                 (X, zero, F(1)), (add(X, Y), Y, F(1)),
                 (Y, zero, F(1)), (add(X, Y), X, F(1))]
    return channels


def mass_action(s, source):
    result = 1
    for count, order in zip(s, source):
        for j in range(order):
            result *= count - j
    return result


def reaction_checks(lam):
    channels = network(lam)
    for s in product(range(3), repeat=4):
        got = {}
        for source, target, coefficient in channels:
            delta = tuple(a - b for a, b in zip(target, source))
            got[delta] = got.get(delta, 0) + coefficient * mass_action(s, source)
        expected = {delta: rate * (s[2] + s[3] + 1)
                    for delta, rate, _ in dfc_events(s, lam)}
        got = {k: v for k, v in got.items() if v}
        require(got == expected, 'D times generator differs from canonical mass-action realization')
    complexes = {s for source, target, _ in channels for s in (source, target)}
    edges = {s: set() for s in complexes}
    for source, target, _ in channels:
        edges[source].add(target)
    double_x = (0, 0, 2, 0)
    require(double_x in complexes and not edges[double_x], '2X must be a sink')
    require(((1, 0, 1, 0), double_x, F(1)) in channels, 'Missing forced ax channel')
    # An outgoing nonnull 2X reaction would give a positive x(x-1) off-diagonal rate.
    for x in (2, 5, 100):
        s = (0, 0, x, 0)
        require(sum(q for _, q, _ in dfc_events(s, lam)) * (x + 1)
                == lam * (x + 1) + x, 'Unexpected quadratic pure-X rate')
    return {'lambda': str(lam), 'grid_states': 81, 'channels': len(channels),
            'complexes': len(complexes), 'weakly_reversible': False,
            'forced_sink': 'A+X -> 2X; no nonnull 2X outgoing rate can be present'}


def main():
    cc_exit = common_chunk_rates(0, 1, 0)[2]
    cc_first = sum(common_chunk_rates(1, 0, 0)[:2])
    require(cc_exit == F(7, 8) and cc_first == F(3, 8), 'Protocol witness wrong')
    require(cc_exit / F(1, 2) != cc_first, 'Constant clock identity unexpectedly holds')
    for M in range(1, 31):
        require(sum(common_chunk_rates(M, 0, 0)[:2]) == F(3 * M**3, (M + 1)**3), 'Empty-plane seed rate wrong')
    old_potential = lambda s: 2 * (s[0] + s[1]) + 2 * sum(s) + (s[2] - s[3])**2
    old_function_rows = []
    for M in (2, 20, 200):
        value = generator((M, 0, M, 0), F(1), old_potential)
        expected = 4 + M * (2 * M - 1) - F(M * (2 * M + 1), M + 1)
        require(value == expected and value > 0, 'Old two-chunk function transfer control failed')
        old_function_rows.append({'M': M, 'DFC_L_old_potential': str(value)})
    print(json.dumps({'common_chunk_exit': str(cc_exit), 'DFC_exit': '1/2',
                      'common_chunk_first': str(cc_first), 'DFC_first': '1',
                      'empty_plane_samples': 30, 'old_two_chunk_function_rows': old_function_rows,
                      'reaction_network_rows': [reaction_checks(F(1, 3)), reaction_checks(F(7, 4))],
                      'scope': 'Exact finite protocol/realization checks. Nontransfer follows from the accompanying analytic derivation; no global historical absence certificate.'}, indent=2))


if __name__ == '__main__':
    main()
