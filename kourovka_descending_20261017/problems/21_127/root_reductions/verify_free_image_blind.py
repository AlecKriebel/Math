"""Exact integer witness for the P4 all-free-image-blind word.

No matrix faithfulness, scl computation, or general rationality is asserted.
"""
from pathlib import Path
import json


def identity():
    return [[int(i == j) for j in range(5)] for i in range(5)]


def generator(i, j):
    a = identity()
    a[i - 1][j - 1] += 1
    return a


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(5))
             for j in range(5)] for i in range(5)]


def inverse(a):
    # a=I+N for strictly upper-triangular N; inverse=sum_{k=0}^4(-N)^k.
    minus_n = [[int(i == j) - a[i][j] for j in range(5)] for i in range(5)]
    power = identity()
    out = [[0] * 5 for _ in range(5)]
    for _ in range(5):
        out = [[out[i][j] + power[i][j] for j in range(5)] for i in range(5)]
        power = multiply(power, minus_n)
    assert multiply(a, out) == identity() == multiply(out, a)
    return out


def commutator(a, b):
    return multiply(multiply(multiply(a, b), inverse(a)), inverse(b))


def main():
    g = {"a": generator(2, 3), "b": generator(4, 5),
         "c": generator(1, 2), "d": generator(3, 4)}
    relators = {x + y: commutator(g[x], g[y]) for x, y in
                [("a", "b"), ("b", "c"), ("c", "d")]}
    assert all(a == identity() for a in relators.values())
    ac, bd = commutator(g["a"], g["c"]), commutator(g["b"], g["d"])
    u = commutator(ac, bd)
    expected_ac, expected_bd = identity(), identity()
    expected_ac[0][2] = -1
    expected_bd[2][4] = -1
    assert ac == expected_ac and bd == expected_bd
    assert u == generator(1, 5) != identity()
    result = {"scope": "Exact nontriviality in P4; all-free-image theorem proved separately",
              "generators": g, "relators": relators,
              "inner_commutators": {"[a,c]": ac, "[b,d]": bd},
              "word": "[[a,c],[b,d]]", "word_image": u,
              "nontrivial": True}
    output = Path(__file__).with_name("free_image_blind_certificate.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print("P4 relators vanish; [[a,c],[b,d]] maps exactly to I+E15.")


if __name__ == "__main__":
    main()
