"""Integral algebra verification for the priority specialization, not proof search.

Polynomials represent the coefficient of t in a Chern-class loop. x,y have
degree two; p,q occur only linearly, so their graded commutativity causes no
additional sign. Every equality is checked over Z before torsion substitution.
"""
from datetime import datetime, timezone
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path

NAMES = ("x", "y", "p", "q")
ZERO = (0, 0, 0, 0)


def clean(a):
    return {m: c for m, c in a.items() if c}


def add(*polys):
    result = {}
    for poly in polys:
        for m, c in poly.items():
            result[m] = result.get(m, 0) + c
    return clean(result)


def scale(n, a):
    return clean({m: n * c for m, c in a.items()})


def mul(a, b):
    result = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(i + j for i, j in zip(ma, mb))
            result[m] = result.get(m, 0) + ca * cb
    return clean(result)


def derivative(a, i):
    result = {}
    for m, c in a.items():
        if m[i]:
            n = list(m)
            n[i] -= 1
            result[tuple(n)] = c * m[i]
    return clean(result)


def var(i):
    m = list(ZERO)
    m[i] = 1
    return {tuple(m): 1}


def chern2(roots):
    return add(*(mul(roots[i], roots[j])
                 for i in range(len(roots)) for j in range(i + 1, len(roots))))


def encoded(poly):
    return [{"powers": dict(zip(NAMES, m)), "coefficient": c}
            for m, c in sorted(poly.items(), reverse=True)]


def determinant(matrix):
    n = len(matrix)
    result = 0
    for order in permutations(range(n)):
        inversions = sum(order[i] > order[j]
                         for i in range(n) for j in range(i + 1, n))
        term = (-1) ** inversions
        for i, j in enumerate(order):
            term *= matrix[i][j]
        result += term
    return result


def main():
    x, y, p, q = (var(i) for i in range(4))
    roots0 = [x, y, scale(-1, add(x, y))]
    rootsrho = [add(roots0[j], scale(-1, roots0[i]))
                for i in range(3) for j in range(i + 1, 3)]
    q0 = chern2(roots0)
    primary = add(*rootsrho)
    qrho = chern2(rootsrho)
    assert q0 == scale(-1, add(mul(x, x), mul(x, y), mul(y, y)))
    assert primary == add(scale(-4, x), scale(-2, y))
    assert qrho == add(scale(5, mul(x, x)), scale(5, mul(x, y)),
                       scale(-1, mul(y, y)))

    def directional(poly):
        return add(mul(derivative(poly, 0), p), mul(derivative(poly, 1), q))

    a = scale(-1, directional(q0))
    k = directional(primary)
    raw = scale(-1, directional(qrho))
    normalized = add(raw, mul(primary, k))
    expected_a = add(mul(add(scale(2, x), y), p),
                     mul(add(x, scale(2, y)), q))
    assert a == expected_a
    assert k == add(scale(-4, p), scale(-2, q))
    assert normalized == scale(3, a)

    shear = [[-3, 0, 1], [0, 1, 0], [1, 0, 0]]
    inverse = [[0, 0, 1], [0, 1, 0], [1, 0, 3]]
    assert determinant(shear) == -1
    assert [[sum(shear[i][j] * inverse[j][k] for j in range(3))
             for k in range(3)] for i in range(3)] == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    image = [a, k, normalized]
    transformed = [add(*(scale(n, poly) for n, poly in zip(row, image)))
                   for row in shear]
    assert transformed == [{}, k, a]

    root = Path(__file__).resolve().parent
    frozen = root.parent / "source_snapshot/CANDIDATE.md"
    candidate_hash = sha256(frozen.read_bytes()).hexdigest()
    assert candidate_hash == "501c9a536246ad06b29e16720c613bcb292c863857849f837bb0250c45a58050"
    result = {
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "candidate_sha256": candidate_hash,
        "ring": "Z[x,y,p,q], with p,q only linear; coefficient-of-t calculation",
        "checks": {"representation_c2_and_c1": True, "integral_directional_derivatives": True,
                   "fixed_E_coordinate_shear": True, "normalized_image_third_is_3a": True,
                   "last_shear_unimodular": True, "image_transformed_to_0_k_a": True},
        "Q0": encoded(q0), "P": encoded(primary), "Qrho": encoded(qrho),
        "a": encoded(a), "k": encoded(k), "raw_v": encoded(raw),
        "normalized_v": encoded(normalized),
        "last_shear_determinant": determinant(shear),
        "scope_limit": "Algebra substitution verification; published topological hypotheses are checked in SPECIALIZATION_CERTIFICATE.md."
    }
    (root / "SPECIALIZATION_CHECK.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"all_checks_passed": True, "script_sha256": result["script_sha256"]}))


if __name__ == "__main__":
    main()
