#!/usr/bin/env python3
"""Exact rational checks for the n=3 negative-depth simplex."""

from fractions import Fraction as F


def check_sector_identity() -> None:
    # Arbitrary rational masses indexed by the traceless-site bit mask.
    w = {
        0b000: F(2, 7),
        0b001: F(3, 11),
        0b010: F(5, 13),
        0b100: F(7, 17),
        0b011: F(11, 19),
        0b101: F(13, 23),
        0b110: F(17, 29),
        0b111: F(19, 31),
    }
    for i in range(3):
        j, k = [x for x in range(3) if x != i]
        bi, bj, bk = 1 << i, 1 << j, 1 << k
        q_i = (
            F(1, 4) * (w[0] + w[bi])
            - F(1, 2) * (w[bj] + w[bk] + w[bi | bj] + w[bi | bk])
            + w[bj | bk]
            + w[0b111]
        )
        t_i = 3 * (
            F(1, 4) * w[0]
            - F(1, 2) * (w[bj] + w[bk])
            + w[bj | bk]
        )
        g_i = (
            F(1, 4) * w[bi]
            - F(1, 2) * (w[bi | bj] + w[bi | bk])
            + w[0b111]
        )
        assert 3 * q_i - t_i == 3 * g_i


def check_simplex() -> None:
    delta = F(3, 25)
    sigma = F(7, 5)
    theta = [F(1, 6), F(1, 3), F(1, 2)]
    lam = [F(1, 4), F(2, 3), F(1, 1)]
    assert sum(theta) == 1
    gap = 1 - 5 * delta

    f = [sigma * (2 * delta + gap * th) for th in theta]
    r = [
        sigma * F(3, 2) * gap * th * (1 - la)
        for th, la in zip(theta, lam)
    ]
    s = [
        sigma * F(3, 4) * gap * th * la
        for th, la in zip(theta, lam)
    ]
    g = [x / 3 for x in s]
    u = [rr / 3 + 2 * ss / 3 for rr, ss in zip(r, s)]

    assert all(ff / 2 - delta * sigma == uu for ff, uu in zip(f, u))
    assert sum(f) == (1 + delta) * sigma
    assert sum(u) == F(1, 2) * gap * sigma
    assert all(ss == 3 * gg for ss, gg in zip(s, g))
    assert all(2 * delta < ff / sigma < 1 - 3 * delta for ff in f)
    assert all(abs(ff / sigma - F(2, 5)) < F(3, 5) * gap for ff in f)
    assert sum(r) <= F(3, 2) * gap * sigma
    assert sum(s) <= F(3, 4) * gap * sigma
    assert sum(g) <= F(1, 4) * gap * sigma


def check_constants() -> None:
    assert F(12, 5) / 1_944_000 == F(1, 810_000)
    # K/S = 1/2 + (5/2) H/S and delta = -H/S.
    delta = F(3, 25)
    mu = F(1, 2) - F(5, 2) * delta
    assert delta == F(1, 5) - F(2, 5) * mu
    # If every g_i >= eta and sigma=1, the total-slack bound gives:
    eta = F(1, 10_000)
    delta_bound = F(1, 5) - F(12, 5) * eta
    assert 3 * eta == F(1, 4) * (1 - 5 * delta_bound)
    assert F(3564, 1584) == F(9, 4)
    assert F(1188, 1584) == F(3, 4)
    assert 1_944_000 * F(4, 9) == 864_000

    # Formal common-trace endpoint.
    delta_ct = F(3, 22)
    gap_ct = 1 - 5 * delta_ct
    p_i = gap_ct / 3
    x = F(4, 99)
    c_i = F(25, 198)
    d = c_i
    assert gap_ct == F(7, 22)
    assert p_i == F(7, 66)
    assert 3 * c_i == F(1, 3) * (1 + delta_ct)
    assert 1584 * delta_ct == 216
    assert x + 3 * c_i + d == F(6, 11)


if __name__ == "__main__":
    check_sector_identity()
    check_simplex()
    check_constants()
    print("n=3 negative-depth stability identities: exact checks passed")
