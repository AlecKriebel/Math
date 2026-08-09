#!/usr/bin/env python3
"""Exact replay of the one-step and two-step orbit-monotonicity refutation."""

from fractions import Fraction


F = Fraction
N = 3


def matvec(matrix, vector):
    return [
        sum(matrix[i][j] * vector[j] for j in range(N))
        for i in range(N)
    ]


def mean(p, vector):
    return sum(p[i] * vector[i] for i in range(N))


def floor_grid(value, denominator):
    return F(value.numerator * denominator // value.denominator, denominator)


def ceil_grid(value, denominator):
    return F(
        (value.numerator * denominator + value.denominator - 1)
        // value.denominator,
        denominator,
    )


def main() -> None:
    p = list(map(F, [".01310931", ".48313850", ".50375219"]))
    W = [
        [F(".354565456"), F("1.20258024e6"), F("8.47598231e-7")],
        [F("1.20258024e6"), F("2.31795454e-5"), F(".0173375395")],
        [F("8.47598231e-7"), F(".0173375395"), F(1)],
    ]
    delta = [sum(p[j] * W[i][j] for j in range(N)) for i in range(N)]
    P = [[p[j] * W[i][j] / delta[i] for j in range(N)] for i in range(N)]
    R = [[p[j] * P[j][i] / p[i] for j in range(N)] for i in range(N)]
    t = [sum(R[i]) for i in range(N)]

    assert sum(p) == 1
    assert all(W[i][j] == W[j][i] > 0 for i in range(N) for j in range(N))
    assert all(sum(P[i]) == 1 for i in range(N))
    assert all(
        p[i] * P[i][j] == p[j] * R[j][i]
        for i in range(N)
        for j in range(N)
    )

    center = list(
        map(
            F,
            [
                "0.96948239826535802050938820707621778646742193737385736227345792180589513635579072",
                "0.4199411432700926607783210061254230001938538469625538224507489769296075637032733",
                "0.49070699498837739796609529383495858341569927656915196311175990432278933108462736",
            ],
        )
    )
    radii = [F(2, 10**60), F(16, 10**60), F(3, 10**60)]
    q_lower = [center[i] - radii[i] for i in range(N)]
    q_upper = [center[i] + radii[i] for i in range(N)]

    def bd_map(q):
        Pq = matvec(P, q)
        return [t[i] / (t[i] + 2 * (1 - Pq[i])) for i in range(N)]

    assert all(F(0) < q_lower[i] < q_upper[i] < F(1) for i in range(N))
    assert all(bd_map(q_lower)[i] >= q_lower[i] for i in range(N))
    assert all(bd_map(q_upper)[i] <= q_upper[i] for i in range(N))

    def db_survival_map(y):
        Ry = matvec(R, y)
        return [2 * value / (1 + 2 * value) for value in Ry]

    # Directed rounding after every map keeps all interval denominators
    # bounded while preserving the coordinatewise enclosure exactly.
    grid_denominator = 10**45
    lower = [q_lower]
    upper = [q_upper]
    for _ in range(15):
        lower.append(
            [
                floor_grid(value, grid_denominator)
                for value in db_survival_map(lower[-1])
            ]
        )
        upper.append(
            [
                ceil_grid(value, grid_denominator)
                for value in db_survival_map(upper[-1])
            ]
        )

    # Every true orbit has lower[k] <= y_k <= upper[k].  These strict
    # cross-time interval separations therefore refute both monotonicity
    # claims, with ample rational margins.
    one_step_gap = mean(p, lower[10]) - mean(p, upper[9])
    two_step_gap = mean(p, lower[15]) - mean(p, upper[13])
    assert one_step_gap > F(1437, 10**10)
    assert two_step_gap > F(1, 25_000_000)

    print("PASS exact symmetric-W orbit-monotonicity refutation")
    print("E_p[y_10-y_9] lower bound:", one_step_gap)
    print("E_p[y_15-y_13] lower bound:", two_step_gap)


if __name__ == "__main__":
    main()
