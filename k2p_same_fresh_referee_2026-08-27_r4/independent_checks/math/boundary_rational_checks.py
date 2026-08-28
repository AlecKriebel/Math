#!/usr/bin/env python3
"""Review-owned exact rational attacks on every strict physical inequality.

No submitted verifier, certificate reader, floating-point arithmetic, or
sampled numerical tolerance is used.  The points are constructed directly at
rational distance from each relevant open face.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


N = 10**6


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def fs(value: F) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def dplus_margins(s: F, g: F, label: str) -> dict[str, str]:
    margins = {
        "s>0": s,
        "1-s>0": 1 - s,
        "g>0": g,
        "1-g>0": 1 - g,
        "g-(2s-1)>0": g - (2 * s - 1),
        "1+2s+g>0": 1 + 2 * s + g,
        "1-2s+g>0": 1 - 2 * s + g,
    }
    for name, value in margins.items():
        require(value > 0, f"{label}:{name}:{value}")
    require(s * g != 0, f"{label}:s*g!=0")
    probabilities = [(1 + 2 * s + g) / 4, (1 - g) / 4,
                     (1 - 2 * s + g) / 4, (1 - g) / 4]
    require(all(value > 0 for value in probabilities), f"{label}:transition positivity")
    require(sum(probabilities) == 1, f"{label}:transition normalization")
    return {name: fs(value) for name, value in margins.items()} | {
        "s*g!=0": str(s * g != 0),
        "transition_probabilities": [fs(value) for value in probabilities],
    }


def ct_margins(s: F, g: F, label: str) -> dict[str, str]:
    result = dplus_margins(s, g, label)
    gap = g - s * s
    require(gap > 0, f"{label}:g-s^2:{gap}")
    result["g-s^2>0"] = fs(gap)
    return result


def subdivide(s: F, g: F, label: str) -> dict[str, object]:
    # Choosing epsilon below half of every relevant input margin makes the
    # displayed factorization exact while staying strictly physical.
    epsilon = min(1 - s, 1 - g, g - (2 * s - 1), F(1, 2)) / 2
    require(epsilon > 0, f"{label}:positive epsilon")
    first = (s / (1 - epsilon), g / (1 - epsilon))
    second = (1 - epsilon, 1 - epsilon)
    first_margins = dplus_margins(*first, f"{label}:first")
    second_margins = dplus_margins(*second, f"{label}:second")
    require(first[0] * second[0] == s and first[1] * second[1] == g,
            f"{label}:serial product")
    return {
        "input": [fs(s), fs(g)],
        "epsilon": fs(epsilon),
        "first": [fs(x) for x in first],
        "second": [fs(x) for x in second],
        "first_margins": first_margins,
        "second_margins": second_margins,
    }


def serial_section(S: F, G: F, m: int, label: str) -> dict[str, object]:
    dplus_margins(S, G, f"{label}:target")
    bound = max(S, G, 2 * S - G, F(0))
    # Bernoulli's inequality guarantees this rational r has r^(m-1)>bound;
    # the exact comparison below checks it directly.
    r = 1 - (1 - bound) / (2 * m)
    power = r ** (m - 1)
    require(bound < power < 1, f"{label}:section interval")
    factors = [(r, r)] * (m - 1) + [(S / power, G / power)]
    for index, pair in enumerate(factors):
        dplus_margins(*pair, f"{label}:factor:{index}")
    product_s = F(1)
    product_g = F(1)
    for s, g in factors:
        product_s *= s
        product_g *= g
    require((product_s, product_g) == (S, G), f"{label}:section product")
    return {"target": [fs(S), fs(G)], "m": m, "r": fs(r),
            "last_factor": [fs(x) for x in factors[-1]]}


def transformed_pair_check(A: F, B: F, s: F, g: F, ct: bool, label: str) -> dict[str, object]:
    checker = ct_margins if ct else dplus_margins
    checker(s, g, f"{label}:base")
    transformed = (s / A, g / B)
    checker(*transformed, f"{label}:transformed")
    return {"A": fs(A), "B": fs(B), "base": [fs(s), fs(g)],
            "transformed": [fs(x) for x in transformed], "domain": "CT" if ct else "D_plus"}


def simultaneous_ct(pairs: list[tuple[F, F]], label: str) -> dict[str, object]:
    L = max([F(1)] + [B / (A * A) for A, B in pairs])
    U = min([F(1)] + [B for _, B in pairs])
    cap = min([F(1)] + [A for A, _ in pairs])
    s = min(cap / 2, U / (2 * (L + 1)))
    g = (L * s * s + U) / 2
    require(0 < s < cap and L * s * s < g < U, f"{label}:choice interval")
    ct_margins(s, g, f"{label}:base")
    transformed = []
    for index, (A, B) in enumerate(pairs):
        pair = (s / A, g / B)
        ct_margins(*pair, f"{label}:transformed:{index}")
        transformed.append([fs(x) for x in pair])
    return {"A_B": [[fs(A), fs(B)] for A, B in pairs], "L": fs(L), "U": fs(U),
            "base": [fs(s), fs(g)], "transformed": transformed}


def main() -> None:
    dplus_points = {
        "near_s0_g0": (F(1, N), F(1, N * N)),
        "near_s1_g1": (1 - F(1, N), 1 - F(1, 2 * N)),
        "near_slanted_face": (F(3, 4), F(1, 2) + F(1, N)),
        "near_g0": (F(1, 4), F(1, N)),
        "near_g1": (F(3, 4), 1 - F(1, N)),
    }
    dplus = {name: {"point": [fs(s), fs(g)], "margins": dplus_margins(s, g, name)}
             for name, (s, g) in dplus_points.items()}
    subdivisions = {name: subdivide(s, g, name) for name, (s, g) in dplus_points.items()}

    ct_points = {
        "near_ct_face": (F(3, 4), F(9, 16) + F(1, N)),
        "near_s0": (F(1, N), F(2, N * N)),
        "near_s1_g1": (1 - F(1, N), ((1 - F(1, N)) ** 2 + 1) / 2),
        "near_g1": (F(1, 2), 1 - F(1, N)),
    }
    ct = {name: {"point": [fs(s), fs(g)], "margins": ct_margins(s, g, name)}
          for name, (s, g) in ct_points.items()}

    inheritance = {}
    for name, lam in {"near_zero": F(1, N), "near_one": 1 - F(1, N)}.items():
        require(lam > 0 and 1 - lam > 0, f"inheritance:{name}")
        inheritance[name] = {"lambda": fs(lam), "1-lambda": fs(1 - lam)}

    products = []
    values = list(dplus_points.values())
    for i, left in enumerate(values):
        for j, right in enumerate(values):
            pair = (left[0] * right[0], left[1] * right[1])
            dplus_margins(*pair, f"product:{i}:{j}")
            products.append({"left": i, "right": j, "product": [fs(x) for x in pair]})

    sections = [serial_section(S, G, m, f"section:{name}:{m}")
                for name, (S, G) in dplus_points.items() for m in range(2, 6)]

    # Rational CT factors imply rational effective products; this checks the
    # power-root/subdivision inequality without introducing irrational floats.
    ct_power_products = []
    for factor in [(F(2, 3), F(1, 2)),
                   (1 - F(1, N), (((1 - F(1, N)) ** 2) + 1) / 2)]:
        ct_margins(*factor, "ct_factor")
        for m in range(2, 6):
            effective = (factor[0] ** m, factor[1] ** m)
            ct_margins(*effective, f"ct_power:{m}")
            ct_power_products.append({"factor": [fs(x) for x in factor], "m": m,
                                      "effective": [fs(x) for x in effective]})

    dplus_gluing_data = [
        (F(2, 3), F(7, 5), F(1, 6), F(1, 3)),
        (F(5, 4), F(3, 7), F(1, 4), F(1, 7)),
        (F(11, 9), F(13, 8), F(1, 4), F(1, 3)),
    ]
    ct_gluing_data = [
        (F(2, 3), F(7, 5), F(1, 15), F(507, 1000)),
        (F(5, 4), F(3, 7), F(1, 10), F(307, 1400)),
        (F(11, 9), F(13, 8), F(1, 10), F(97853, 193600)),
    ]
    gluing = [transformed_pair_check(*row, False, f"dplus_glue:{i}")
              for i, row in enumerate(dplus_gluing_data)]
    gluing += [transformed_pair_check(*row, True, f"ct_glue:{i}")
               for i, row in enumerate(ct_gluing_data)]
    simultaneous = [
        simultaneous_ct([(F(2, 3), F(7, 5)), (F(5, 4), F(3, 7))], "simultaneous:0"),
        simultaneous_ct([(F(11, 9), F(13, 8)), (F(3, 5), F(2, 7))], "simultaneous:1"),
    ]

    result = {
        "schema": "k2p-r4-independent-boundary-rational-check-v1",
        "arithmetic": "fractions.Fraction only; no floating-point comparisons",
        "dplus_face_points": dplus,
        "continuous_time_face_points": ct,
        "strict_inheritance_points": inheritance,
        "strict_subdivisions": subdivisions,
        "dplus_pair_products": products,
        "dplus_surjective_sections": sections,
        "continuous_time_power_products": ct_power_products,
        "bridge_transformed_pairs": gluing,
        "simultaneous_ct_gluing": simultaneous,
        "status": "PASS",
    }
    result["payload_sha256"] = canonical_hash(result)
    output = Path(__file__).with_name("boundary_rational_checks_result.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "payload_sha256": result["payload_sha256"],
                      "dplus_points": len(dplus), "ct_points": len(ct),
                      "sections": len(sections), "pair_products": len(products)}, sort_keys=True))


if __name__ == "__main__":
    main()
