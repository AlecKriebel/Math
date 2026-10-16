"""Exact-arithmetic boundary probes for the PR12 audit.

These checks corroborate algebra and counterexample diagnostics. They are not
formal certification of the general theorem. Python standard library only.
Run from this folder: python3 adversarial_probes.py
"""

from fractions import Fraction as F
import json


def matvec(a, x):
    return tuple(sum(row[i] * x[i] for i in range(len(x))) for row in a)


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def power_apply(a, inv, exponent, x):
    for _ in range(abs(exponent)):
        x = matvec(a if exponent >= 0 else inv, x)
    return x


def infnorm(x):
    return max(abs(t) for t in x)


def shift(x):
    return {k - 1: (F(1, 2) if k - 1 < 0 else F(2)) * v
            for k, v in x.items() if v}


def inverse_shift(x):
    return {k + 1: v / (F(1, 2) if k < 0 else F(2))
            for k, v in x.items() if v}


def shift_power(x, exponent):
    for _ in range(abs(exponent)):
        x = (shift if exponent >= 0 else inverse_shift)(x)
    return x


def add_dicts(*items):
    answer = {}
    for item in items:
        for k, v in item.items():
            answer[k] = answer.get(k, F(0)) + v
    return {k: v for k, v in answer.items() if v}


def negate(x):
    return {k: -v for k, v in x.items()}


def project(x, stable):
    return {k: v for k, v in x.items() if (k <= 0) == stable}


def test_dual_endpoints():
    s = ((F(2), F(1)), (F(0), F(1, 2)))
    sinv = ((F(1, 2), F(-1)), (F(0), F(2)))
    u = (F(1), F(2))
    zero = (F(0), F(0))
    count = 0
    for a in range(-5, 6):
        for b in range(a, 7):
            sequence = {j: power_apply(s, sinv, -j, u)
                        for j in range(-b, -a + 1)}
            residuals = {
                j: sub(sequence.get(j - 1, zero),
                       matvec(s, sequence.get(j, zero)))
                for j in range(-b - 1, -a + 3)
            }
            residuals = {j: v for j, v in residuals.items() if v != zero}
            expected = {
                -b: tuple(-v for v in power_apply(s, sinv, b + 1, u)),
                -a + 1: power_apply(s, sinv, a, u),
            }
            assert residuals == expected
            assert sum(infnorm(v) for v in residuals.values()) == (
                infnorm(power_apply(s, sinv, a, u))
                + infnorm(power_apply(s, sinv, b + 1, u)))
            count += 1
    return count


def test_green_noncommuting():
    # The bands n<=0 and n>=1 have one-sided invariance and rate 1/2.
    e1 = {1: F(1)}
    assert project(shift(e1), True) != shift(project(e1, True))
    forcing = {k: {-2: F(k + 1), 1: F(2 - k), 3: F(1, k + 10)}
               for k in range(-3, 4)}

    def b(k):
        return {coordinate: value for coordinate, value in forcing.get(k, {}).items()
                if value}

    def truncated_y(n, depth):
        terms = []
        for j in range(depth + 1):
            terms.append(shift_power(project(b(n - 1 - j), True), j))
            terms.append(negate(shift_power(project(b(n + j), False), -j - 1)))
        return add_dicts(*terms)

    count = 0
    for depth in range(8):
        for n in range(-10, 11):
            residual = add_dicts(truncated_y(n + 1, depth),
                                 negate(shift(truncated_y(n, depth))))
            expected = add_dicts(
                b(n),
                negate(shift_power(project(b(n - 1 - depth), True), depth + 1)),
                negate(shift_power(project(b(n + depth + 1), False), -depth - 1)))
            assert residual == expected
            count += 1
    for n in range(-10, 11):
        assert add_dicts(truncated_y(n + 1, 20),
                         negate(shift(truncated_y(n, 20)))) == b(n)
    for k in range(-12, 13):
        homogeneous = shift_power({0: F(1)}, k)
        assert sum(abs(v) for v in homogeneous.values()) == F(1, 2) ** abs(k)
    return count


def test_uniform_fiber_gap():
    # For every tested d and eta, explicitly find an atom i of positive mass
    # whose contraction factor (1+1/i)^(-d) is greater than eta.
    count = 0
    for d in range(1, 13):
        for eta in (F(1, 4), F(1, 2), F(3, 4), F(99, 100)):
            i = 1
            while (F(i, i + 1) ** d) <= eta:
                i *= 2
            assert F(i, i + 1) ** d > eta
            # Atom weight 2^-i is small but strictly positive: essential
            # suprema do not permit throwing the bad atom away.
            assert F(1, 2) ** i > 0
            count += 1
    return count


def test_localization():
    # On three positive atoms, the global vector masks the last bad atom.
    plus = (F(3), F(1), F(3, 2))
    minus = (F(1), F(3), F(3, 2))
    global_vector = (F(1), F(1), F(1))
    assert infnorm(tuple(a * h for a, h in zip(plus, global_vector))) == 3
    assert infnorm(tuple(a * h for a, h in zip(minus, global_vector))) == 3
    local_vector = (F(0), F(0), F(1))
    assert infnorm(tuple(a * h for a, h in zip(plus, local_vector))) == F(3, 2)
    assert infnorm(tuple(a * h for a, h in zip(minus, local_vector))) == F(3, 2)
    return 1


if __name__ == "__main__":
    result = {
        "arithmetic": "exact rational, Python standard library",
        "dual_orbit_segment_endpoint_checks": test_dual_endpoints(),
        "green_truncation_identities_noncommuting": test_green_noncommuting(),
        "uniform_fiber_counterexample_witnesses": test_uniform_fiber_gap(),
        "L_infinity_localization_masking_examples": test_localization(),
        "status": "all probes passed",
        "limitation": "probes corroborate derivations; no finite test proves the general theorem",
    }
    print(json.dumps(result, indent=2))
