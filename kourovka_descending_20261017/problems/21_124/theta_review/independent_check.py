#!/usr/bin/env python3
"""Fresh exact checks; does not import the author checker or modify its outputs."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "tubular"


def nullspace(rows, width=3):
    a = [[F(x) for x in row] for row in rows]
    pivots = []
    r = 0
    for c in range(width):
        j = next((j for j in range(r, len(a)) if a[j][c]), None)
        if j is None:
            continue
        a[r], a[j] = a[j], a[r]
        scale = a[r][c]
        a[r] = [v / scale for v in a[r]]
        for j in range(len(a)):
            if j != r:
                scale = a[j][c]
                a[j] = [x - scale * y for x, y in zip(a[j], a[r])]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    basis = []
    for c in range(width):
        if c not in pivots:
            v = [F(0)] * width
            v[c] = F(1)
            for row, pivot in zip(a, pivots):
                v[pivot] = -row[c]
            basis.append(v)
    return basis


def independent_witness(p, q):
    # Exhaust every sign, then solve by exact row reduction rather than the
    # constructive branch choices in the author checker.
    for signs in product((-1, 1), repeat=2):
        basis = nullspace([[pi, -s * qi, 1 - s]
                           for pi, qi, s in zip(p, q, signs)])
        for coeffs in product((-1, 0, 1), repeat=len(basis)):
            v = [sum((k * b[i] for k, b in zip(coeffs, basis)), F(0))
                 for i in range(3)]
            if v[0] and v[1]:
                assert all(pi * v[0] + v[2] == s * (qi * v[1] + v[2])
                           for pi, qi, s in zip(p, q, signs))
                return v, signs
    return None


def determinant(rows):
    a = [[F(x) for x in row] for row in rows]
    result = F(1)
    for c in range(len(a)):
        j = next((j for j in range(c, len(a)) if a[j][c]), None)
        if j is None:
            return F(0)
        if j != c:
            a[j], a[c] = a[c], a[j]
            result = -result
        pivot = a[c][c]
        result *= pivot
        for j in range(c + 1, len(a)):
            scale = a[j][c] / pivot
            a[j] = [x - scale * y for x, y in zip(a[j], a[c])]
    return result


def reduce_word(word):
    result = []
    for x in word:
        if result and result[-1] == -x:
            result.pop()
        else:
            result.append(x)
    return result


def inverse(word):
    return [-x for x in reversed(word)]


def substitute(word, images):
    out = []
    for x in word:
        image = images[abs(x)]
        out.extend(image if x > 0 else inverse(image))
    return reduce_word(out)


def run():
    vals = [F(-2), F(-1), F(-1, 2), F(0), F(1, 2), F(1), F(2)]
    sign_cases = exceptions = 0
    for p1, p2, q1, q2 in product(vals, repeat=4):
        exc = ((p1 == p2 == 0 and len({F(0), q1, q2}) == 3)
               or (q1 == q2 == 0 and len({F(0), p1, p2}) == 3))
        witness = independent_witness((p1, p2), (q1, q2))
        assert (witness is None) == exc, (p1, p2, q1, q2, witness)
        sign_cases += 1
        exceptions += exc

    # Direct checks on integral vertex lattices whose height images are 2Z
    # and 3Z. Edge generators can have negative or nonprimitive heights.
    lattice_cases = lattice_exceptions = 0
    for k0, k1, k2 in product((-2, -1, 1, 2), repeat=3):
        for l0, r0 in product((-1, 1), repeat=2):
            left = [(3 * k0, l0), (3 * k1, -2), (3 * k2, 3)]
            right = [(2 * k0, r0), (2 * k1, 2), (2 * k2, -1)]
            n = [6 * k0, 6 * k1, 6 * k2]
            tl, tr = F(l0, n[0]), F(r0, n[0])
            p = [F(left[i][1], n[i]) - tl for i in (1, 2)]
            q = [F(right[i][1], n[i]) - tr for i in (1, 2)]
            witness = independent_witness(p, q)
            if witness is None:
                lattice_exceptions += 1
                continue
            (a, b, c), signs = witness
            # Images are (E-coordinate, H-coordinate).
            def image(v, hfactor, kernel_scale, tau_second):
                h = hfactor * v[0]
                return (kernel_scale * (v[1] - h * tau_second) + h * c, h)
            for i, s in enumerate((1,) + signs):
                u = image(left[i], 2, a, tl)
                v = image(right[i], 3, b, tr)
                assert u == (s * v[0], v[1])
            # Nonzero lattice determinants establish injective discrete maps.
            assert determinant([image((1, 0), 2, a, tl), image((0, 1), 2, a, tl)])
            assert determinant([image((1, 0), 3, b, tr), image((0, 1), 3, b, tr)])
            lattice_cases += 1

    pairs = [(3, 2), (20, 14), (119, 84)]
    assert all(p * (p + 1) == 2 * q * (q + 1) for p, q in pairs)
    gram_left = [[F(1), F(1, 2)], [F(1, 2), F(2)]]
    gram_right = [[F(2), F(1)], [F(1), F(2)]]
    assert determinant(gram_left) == F(7, 4)
    assert determinant(gram_right) == F(3)
    assert gram_left[0][0] > 0 and gram_right[0][0] > 0
    for p, q in [(0, 0)] + pairs:
        for k in (-7, -2, -1, 1, 2, 7):
            def norm2(matrix, v):
                return sum(matrix[i][j] * v[i] * v[j]
                           for i in range(2) for j in range(2))
            assert norm2(gram_left, (k * p, k)) == norm2(gram_right, (k * q, k))

    sign_determinants = []
    for signs in product((-1, 1), repeat=3):
        rows = [[p, -s * q, 1 - s] for (p, q), s in zip(pairs, signs)]
        d = determinant(rows)
        sign_determinants.append({"signs": list(signs), "determinant": int(d)})
        if signs == (1, 1, 1):
            assert nullspace(rows) == [[F(0), F(0), F(1)]]
        else:
            assert not nullspace(rows)
    author_certificate = json.loads((AUTHOR / "theta_certificate.json").read_text())
    assert sign_determinants == author_certificate["pell_sign_determinants"]

    phi = {1: [1], 2: [2]}
    psi = {1: [1], 2: [2]}
    for i, (p, q) in enumerate(pairs, start=3):
        phi[i] = [-2] * q + [i] + [1] * p
        psi[i] = [2] * q + [i] + [-1] * p
    automorphism_cases = 0
    for i in range(1, 6):
        for word in ([i], [-i]):
            assert substitute(substitute(word, phi), psi) == word
            assert substitute(substitute(word, psi), phi) == word
            automorphism_cases += 2
    # The original s_i a^p_i t s_i^-1=t b^q_i relations become
    # phi(s_i) = b^-q_i s_i a^p_i upon eliminating t.
    for i, (p, q) in enumerate(pairs, start=3):
        assert reduce_word([-2] * q + [i] + [1] * p) == phi[i]

    wrong_pairs = [(2, 1), (14, 10), (84, 59)]
    assert all(p * (p + 1) != 2 * q * (q + 1) for p, q in wrong_pairs)
    inputs = {name: hashlib.sha256((AUTHOR / name).read_bytes()).hexdigest()
              for name in ("THETA_SUBCLASS.md", "PELL_CANDIDATE.md", "check_theta.py", "theta_certificate.json")}
    return {
        "utc": datetime.now(timezone.utc).isoformat(),
        "result": "PASS",
        "sign_cases_by_independent_rref": sign_cases,
        "exceptional_sign_cases": exceptions,
        "integral_lattice_relation_cases": lattice_cases,
        "integral_lattice_exceptional_cases": lattice_exceptions,
        "lattice_height_images": ["2Z", "3Z"],
        "pell_gram_determinants": ["7/4", "3"],
        "pell_sign_determinants": sign_determinants,
        "free_automorphism_composition_checks": automorphism_cases,
        "wrong_pell_pairs_rejected": wrong_pairs,
        "input_sha256": inputs,
        "scope": "Supports the written theta-subclass proof and elementary abelian-2 Pell filter only. No arbitrary finite-holonomy exclusion, novelty, or complete Kourovka solution."
    }


if __name__ == "__main__":
    result = run()
    (HERE / "independent_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
