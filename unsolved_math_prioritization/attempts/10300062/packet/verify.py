#!/usr/bin/env python3
"""Exact guardrails, not a proof verifier. Standard library only."""
from fractions import Fraction
from itertools import product
from math import gcd, isqrt, lcm
from pathlib import Path
import json


def inverse(w):
    return [-x for x in reversed(w)]


def reduced(w):
    ans = []
    for x in w:
        if ans and ans[-1] == -x:
            ans.pop()
        else:
            ans.append(x)
    return ans


def comm(a, b):
    return a + b + inverse(a) + inverse(b)


def substitute(w, images):
    ans = []
    for x in w:
        v = images[abs(x)]
        ans += v if x > 0 else inverse(v)
    return reduced(ans)


def exponent_vector(w, rank):
    return [sum((1 if x == j else -1 if x == -j else 0) for x in w)
            for j in range(1, rank + 1)]


def run():
    r3 = comm([1], [2]) + comm([3], [4]) + comm([5], [6])
    r2 = comm([1], [2]) + comm([3], [4])
    pinch = {1: [], 2: [], 3: [1], 4: [2], 5: [3], 6: [4]}
    assert substitute(r3, pinch) == r2
    retract = {1: [1], 2: [2], 3: [2], 4: [1], 5: [], 6: []}
    assert substitute(r3, retract) == []
    assert substitute([1], retract) == [1]
    assert substitute([2], retract) == [2]
    noncommuting = reduced(comm([1], [2]))
    assert noncommuting == [1, 2, -1, -2]
    for k in range(1, 17):
        assert reduced(comm([1] * k, [2] * k)) != []

    # Surface double: [a+,b+]=[a-,b-].
    double_relator = comm([1], [2]) + inverse(comm([3], [4]))
    fold = {1: [1], 2: [2], 3: [1], 4: [2]}
    assert substitute(double_relator, fold) == []
    kernel_word = [1, -3]
    assert substitute(kernel_word, fold) == []
    kernel_homology = exponent_vector(kernel_word, 4)
    assert kernel_homology == [1, 0, -1, 0]
    assert exponent_vector(double_relator, 4) == [0, 0, 0, 0]

    # A central-fiber-killing homomorphism also respects the extension relator.
    extension_relator = r3 + [7, 7]  # product commutators = z^-2
    extension_retract = dict(retract, **{})
    extension_retract[7] = []
    assert substitute(extension_relator, extension_retract) == []

    # Samples guard against erroneous signs/formulas. The all-degree result is proved in prose.
    h, g, degree = 2, 3, 1
    e = degree * (2 - 2 * h)
    assert e == -2 and abs(e) <= 2 * g - 2
    e_cover = [d * e for d in range(1, 65)]
    assert all(x != 0 for x in e_cover)
    double_cover_genera = {str(k): k - 1 for k in range(3, 13)}
    assert all(x >= 2 for x in double_cover_genera.values())

    # Image-convergence countercontrol: n U_11=1 has no integral solution for n>1.
    cover_controls = []
    for n in range(2, 17):
        assert 1 % n != 0
        cover_controls.append({"n": n, "image_index": n,
                               "integral_right_inverse_impossible": True})
    # pi<22/7 gives pi*sqrt(2)<5, so r_n=n covers the target image for n>=5.
    assert 2 * Fraction(22, 7) ** 2 < 25

    # Bounded lattice checks: exact integer arithmetic, not an asymptotic proof.
    lattice = []
    box = 12
    for m in (10, 100, 1000, 10000, 100000):
        a, b = isqrt(2 * m * m), isqrt(3 * m * m)
        assert a * a <= 2 * m * m < (a + 1) ** 2
        assert b * b <= 3 * m * m < (b + 1) ** 2
        w = (m, a, b)
        short = []
        for z in product(range(-box, box + 1), repeat=3):
            if z != (0, 0, 0) and sum(x * y for x, y in zip(w, z)) == 0:
                short.append(z)
        lattice.append({"m": m, "normal": list(w),
                        "primitive_normal": [x // gcd(*w) for x in w],
                        "box_infinity_radius": box,
                        "nonzero_lattice_vectors_in_box": len(short),
                        "shortest_squared_norm_in_box":
                            min((sum(x * x for x in z) for z in short), default=None),
                        "normal_error_each_last_coordinate_less_than": f"1/{m}"})

    weights = [Fraction(5, 6), Fraction(1, 2), Fraction(1, 3)]
    assert weights[0] == weights[1] + weights[2]
    scale = lcm(*(x.denominator for x in weights))
    integer_weights = [int(scale * x) for x in weights]
    assert integer_weights == [5, 3, 2]
    assert integer_weights[0] == sum(integer_weights[1:])

    c, C = Fraction(1, 2), Fraction(2)
    good, bad = Fraction(4), Fraction(1)
    assert c * good - C * bad == 0
    assert bad / good == c / C

    return {
        "status": "PASS",
        "scope": "Exact finite algebraic guardrails only; not a formal topological proof or an original-question resolution.",
        "pinch_relator": "Maps genus-3 relator exactly to genus-2 relator.",
        "free_retraction": "Genus-3 relator and central extension relator map to empty reduced words.",
        "punctured_torus_commutator": noncommuting,
        "double_kernel_word": kernel_word,
        "double_kernel_homology": kernel_homology,
        "bundle_euler_number": e,
        "finite_cover_euler_samples": e_cover,
        "nonorientable_double_cover_genera_samples": double_cover_genera,
        "torus_cover_controls": cover_controls,
        "lattice_controls": lattice,
        "rational_branch_weights": {"scale": scale, "integers": integer_weights},
        "area_ratio_control": str(c / C),
        "unverified_by_code": [
            "The classification and topology of surface groups and circle bundles.",
            "The existence, smoothness and tautness of the suspension foliation.",
            "All-degree Euler nonvanishing and asymptotic lattice escape, which require the written proofs.",
            "Whether coherent compact-domain convergence is the convergence intended by Calegari Question 14.2.",
            "Novelty, priority, or any full resolution of the original question."
        ]
    }


if __name__ == "__main__":
    result = run()
    output = Path(__file__).with_name("verification_results.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "result_file": output.name,
                      "scope": result["scope"]}, sort_keys=True))
