#!/usr/bin/env python3
"""Exact scope control: trace invariance does not imply component invariance.

Standard library only; no native-package imports, network, writes, or assertions.
Polynomials are sparse maps (s exponent, t exponent) -> integer.
"""
import json


def add(a, b):
    c = dict(a)
    for m, v in b.items():
        c[m] = c.get(m, 0) + v
    return {m: v for m, v in c.items() if v}


def neg(a):
    return {m: -v for m, v in a.items()}


def mul(a, b):
    c = {}
    for (i, j), v in a.items():
        for (k, l), w in b.items():
            m = (i + k, j + l)
            c[m] = c.get(m, 0) + v * w
    return {m: v for m, v in c.items() if v}


def mm(a, b):
    return [[add(mul(a[i][0], b[0][j]), mul(a[i][1], b[1][j]))
             for j in range(2)] for i in range(2)]


def diff(a, b):
    return [[add(a[i][j], neg(b[i][j])) for j in range(2)] for i in range(2)]


def tr(a):
    return add(a[0][0], a[1][1])


def det(a):
    return add(mul(a[0][0], a[1][1]), neg(mul(a[0][1], a[1][0])))


def encode(p):
    return [[i, j, p[(i, j)]] for i, j in sorted(p)]


def main():
    z, one, s, t = {}, {(0, 0): 1}, {(1, 0): 1}, {(0, 1): 1}
    ident = [[one, z], [z, one]]
    a, ai = [[one, s], [z, one]], [[one, neg(s)], [z, one]]
    b, bi = [[one, z], [t, one]], [[one, z], [neg(t), one]]
    conjugate = lambda c: mm(mm(a, c), ai)
    displacement = diff(conjugate(b), b)
    expected = [[{(1, 1): 1}, {(2, 1): -1}], [z, {(1, 1): -1}]]
    checks = {
        "a_and_b_are_SL2_over_Z_s_t": det(a) == one and det(b) == one,
        "exact_inverse_controls": mm(a, ai) == ident and mm(b, bi) == ident,
        "component_displacement_exact": displacement == expected,
        "displacement_has_nonzero_total_degree2": displacement[0][0].get((1, 1)) == 1,
        "no_component_displacement_below_degree2": all(
            sum(m) >= 2 for row in displacement for p in row for m in p),
        "trace_is_fixed_on_four_representative_words": all(
            tr(conjugate(c)) == tr(c) for c in [a, b, mm(a, b), mm(a, bi)]),
        "trace_of_displacement_zero": tr(displacement) == z,
        "wrong_component_invariance_is_rejected": conjugate(b) != b,
    }
    if not all(checks.values()):
        raise RuntimeError("priority-scope control failed")
    return {
        "status": "PASS", "checks": checks, "check_count": len(checks),
        "component_displacement": [[encode(p) for p in row] for row in displacement],
        "interpretation": "Common conjugation fixes every trace by cyclicity, but this"
                          " inner automorphism is not in the component D_n(2):"
                          " its s*t term cannot be in (s,t)^3.",
        "limitations": "This distinguishes two filtrations. It neither proves the"
                       " PR counterexamples nor certifies historical priority.",
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
