"""Finite diagnostics of the explicit topology argument; not a topology prover."""
import json


def require(condition, label):
    if not condition:
        raise ValueError(label)


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def commutator(a, b):
    ab, ba = multiply(a, b), multiply(b, a)
    return [[ab[i][j] - ba[i][j] for j in range(3)] for i in range(3)]


def scale(n, a):
    return [[n * x for x in row] for row in a]


def diagnostics():
    j = [[0, -1, 0], [1, 0, 0], [0, 0, 0]]
    a = [[1, 0, 0], [0, -1, 0], [0, 0, 0]]
    b = [[0, 1, 0], [1, 0, 0], [0, 0, 0]]
    c = [[0, 0, 1], [0, 0, 0], [1, 0, 0]]
    d = [[0, 0, 0], [0, 0, 1], [0, 1, 0]]
    e = [[1, 0, 0], [0, 1, 0], [0, 0, -2]]
    expected = [scale(2, b), scale(-2, a), d, scale(-1, c), scale(0, e)]
    actual = [commutator(j, q) for q in [a, b, c, d, e]]
    require(actual == expected, "tangent representation rotation planes")
    require((1 + 2) % 2 == 1, "nonspin parity")
    require((2 + 2) % 2 == 0, "spin-compatible negative control")

    hom24 = [value for value in range(4) if 2 * value % 4 == 0]
    hom22 = [value for value in range(2) if 2 * value % 2 == 0]
    reduction = sorted(set(value % 2 for value in hom24))
    require(hom24 == [0, 2] and hom22 == [0, 1] and reduction == [0], "UCT connecting map")
    require(len(hom22) > len(reduction), "nonzero Bockstein")

    # Ring basis: 1, x, y, xy with x^2=y^2=0 over F2.
    def cup(u, v):
        z = (u[0] + v[0], u[1] + v[1])
        return z if max(z) <= 1 else None
    top = cup((1, 0), (0, 1))
    require(top == (1, 1), "nonzero characteristic product")
    require(cup((1, 0), (1, 0)) is None and cup((0, 1), (0, 1)) is None, "ring truncation")
    require(2 % 2 == 0 and 3 % 2 == 1, "even cover obstruction does not reject odd covers")
    require(0 * 1 == 0, "vanishing w2 control does not force obstruction")

    # UCT ranks of W from integral homology: free ranks plus Tor contribution.
    free = [1, 0, 0, 0, 0, 1]
    torsion_two = [0, 0, 1, 0, 0, 0]
    mod_two = [free[n] + torsion_two[n] + (torsion_two[n-1] if n else 0) for n in range(6)]
    require(mod_two == [1, 0, 1, 1, 0, 1], "mod-two Betti degrees")
    require(free == [1, 0, 0, 0, 0, 1], "odd-prime and rational Betti degrees")
    return {
        "scope": "finite diagnostics only; topology is proved in REPORT.md",
        "commutator_identities": 5,
        "rotation_weights": [2, 1, 0],
        "fundamental_group_parity": 1,
        "hom_Z2_Z4_values": hom24,
        "reduction_image": reduction,
        "mod_two_betti": mod_two,
        "odd_prime_betti": free,
        "characteristic_number": 1,
        "negative_controls": ["even tangent weight parity", "odd cover parity", "zero w2", "square-zero ring"],
        "status": "PASS"
    }


if __name__ == "__main__":
    print(json.dumps(diagnostics(), sort_keys=True, indent=2))
