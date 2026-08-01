#!/usr/bin/env python3
"""Dependency-free arithmetic verifier for the DTH site-symmetry census.

The companion exact-chart verifier derives the dimensions and stabilizer
characters over QQ.  This small independent layer pins those integer data
and checks all representation-theoretic multiplicities and both coordinate
totals using only the Python standard library.
"""


# triple: (K dimension, stabilizer kind, characters)
# For ``aab``, characters=(transposition character,).
# For ``aaa``, characters=(transposition character, three-cycle character).
DATA = {
    (0, 0, 0): (0, "aaa", (0, 0)),
    (0, 0, 1): (0, "aab", (0,)),
    (0, 0, 2): (1, "aab", (1,)),
    (0, 0, 3): (0, "aab", (0,)),
    (0, 0, 4): (1, "aab", (1,)),
    (0, 1, 1): (1, "aab", (1,)),
    (0, 1, 2): (2, "abc", ()),
    (0, 1, 3): (2, "abc", ()),
    (0, 1, 4): (2, "abc", ()),
    (0, 2, 2): (2, "aab", (2,)),
    (0, 2, 3): (2, "abc", ()),
    (0, 2, 4): (2, "abc", ()),
    (0, 3, 3): (4, "aab", (2,)),
    (0, 3, 4): (2, "abc", ()),
    (0, 4, 4): (2, "aab", (2,)),
    (1, 1, 1): (5, "aaa", (1, -1)),
    (1, 1, 2): (7, "aab", (3,)),
    (1, 1, 3): (8, "aab", (0,)),
    (1, 1, 4): (7, "aab", (3,)),
    (1, 2, 2): (8, "aab", (2,)),
    (1, 2, 3): (10, "abc", ()),
    (1, 2, 4): (8, "abc", ()),
    (1, 3, 3): (12, "aab", (2,)),
    (1, 3, 4): (10, "abc", ()),
    (1, 4, 4): (8, "aab", (2,)),
    (2, 2, 2): (11, "aaa", (3, -1)),
    (2, 2, 3): (12, "aab", (0,)),
    (2, 2, 4): (11, "aab", (3,)),
    (2, 3, 3): (16, "aab", (4,)),
    (2, 3, 4): (12, "abc", ()),
    (2, 4, 4): (11, "aab", (3,)),
    (3, 3, 3): (16, "aaa", (0, -2)),
    (3, 3, 4): (15, "aab", (3,)),
    (3, 4, 4): (12, "aab", (0,)),
    (4, 4, 4): (10, "aaa", (2, -2)),
}


def symmetric_dimension(dimension):
    return dimension * (dimension + 1) // 2


def orbit_size(kind):
    return {"aaa": 1, "aab": 3, "abc": 6}[kind]


def invariant_dimension(dimension, kind, characters):
    if kind == "abc":
        return symmetric_dimension(dimension), ()
    if kind == "aab":
        (transposition,) = characters
        plus = (dimension + transposition) // 2
        minus = (dimension - transposition) // 2
        assert plus + minus == dimension
        return symmetric_dimension(plus) + symmetric_dimension(minus), (plus, minus)

    transposition, cycle = characters
    trivial = (dimension + 3 * transposition + 2 * cycle) // 6
    sign = (dimension - 3 * transposition + 2 * cycle) // 6
    standard = (dimension - cycle) // 3
    assert trivial + sign + 2 * standard == dimension
    return (
        symmetric_dimension(trivial)
        + symmetric_dimension(sign)
        + symmetric_dimension(standard)
    ), (trivial, sign, standard)


def main():
    assert len(DATA) == 35
    ordered = 0
    invariant = 0
    modules = {}
    for triple, (dimension, kind, characters) in DATA.items():
        assert tuple(sorted(triple)) == triple
        ordered += orbit_size(kind) * symmetric_dimension(dimension)
        contribution, module = invariant_dimension(dimension, kind, characters)
        invariant += contribution
        modules[triple] = module

    assert ordered == 4139
    assert invariant == 761
    assert modules[(3, 3, 3)] == (2, 2, 6)
    assert modules[(4, 4, 4)] == (2, 0, 4)
    assert modules[(3, 3, 4)] == (9, 6)

    print("ordered/invariant target coordinates:", ordered, invariant)
    print("PASS: dependency-free DTH site-symmetric census arithmetic")


if __name__ == "__main__":
    main()
