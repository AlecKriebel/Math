#!/usr/bin/env python3
"""Exact regression certificate for the K2P edge domain and root movement."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_object(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def probabilities(s: F, g: F) -> tuple[F, F, F, F]:
    return ((1 + 2 * s + g) / 4, (1 - g) / 4, (1 - 2 * s + g) / 4, (1 - g) / 4)


def strict_edge(s: F, g: F) -> bool:
    return s != 0 and g != 0 and all(value > 0 for value in probabilities(s, g))


def d_plus(s: F, g: F) -> bool:
    return 0 < s < 1 and 0 < g < 1 and g > 2 * s - 1


def factor_near_identity(s: F, g: F) -> tuple[tuple[F, F], tuple[F, F], F]:
    margins = (1 - g, 1 + 2 * s + g, 1 - 2 * s + g, F(1))
    require(all(value > 0 for value in margins), "input is not a strict nonsingular edge")
    epsilon = min(margins) / 2
    first = (s / (1 - epsilon), g / (1 - epsilon))
    second = (1 - epsilon, 1 - epsilon)
    require(strict_edge(*first), "first near-identity factor is not strict")
    require(strict_edge(*second), "second near-identity factor is not strict")
    require(first[0] * second[0] == s and first[1] * second[1] == g, "factor product changed")
    return first, second, epsilon


def main() -> None:
    if not __debug__:
        raise SystemExit("K2P_DOMAIN_OPTIMIZED_MODE_FORBIDDEN")

    # Representatives exercise positive, mixed-sign, and the square-root obstruction.
    examples = ((F(1, 3), F(2, 5)), (F(-1, 5), F(1, 4)), (F(9, 10), F(801, 1000)))
    factor_rows = []
    for s_value, g_value in examples:
        require(strict_edge(s_value, g_value), "locked example is not strict stochastic")
        first, second, epsilon = factor_near_identity(s_value, g_value)
        factor_rows.append(
            {
                "input": [str(s_value), str(g_value)],
                "epsilon": str(epsilon),
                "first": [str(first[0]), str(first[1])],
                "second": [str(second[0]), str(second[1])],
            }
        )

    # Squaring the transition inequality shows the coordinatewise square root fails here:
    # sqrt(g) > 2 sqrt(s)-1 is equivalent to g > (2 sqrt(s)-1)^2.
    s_bad, g_bad = examples[-1]
    # Avoid irrational arithmetic: failure of 1-2 sqrt(s)+sqrt(g)>0 is equivalent,
    # since 2 sqrt(s)-1>0, to g>(2 sqrt(s)-1)^2.  Rearranging and squaring once
    # gives (4s+1-g)^2 < 16s.  Its negation is exact rational arithmetic.
    require(2 * s_bad > 1, "bad example is in the wrong sign chamber")
    require((4 * s_bad + 1 - g_bad) ** 2 >= 16 * s_bad, "square-root counterexample disappeared")

    # Exact finite regression of the logical equivalence on rational witnesses.
    grid = tuple(F(i, 20) for i in range(-19, 20) if i != 0)
    checked = 0
    for s_value in grid:
        for g_value in grid:
            lhs = strict_edge(s_value, g_value)
            rhs = (
                1 - g_value > 0
                and 1 + 2 * s_value + g_value > 0
                and 1 - 2 * s_value + g_value > 0
                and s_value != 0
                and g_value != 0
            )
            require(lhs == rhs, "edge-domain equivalence failed")
            if lhs and s_value > 0 and g_value > 0:
                require(d_plus(s_value, g_value), "positive strict edge is outside D_plus")
            checked += 1

    # The continuous-time power subdivision theorem is checked at exact perfect powers.
    ct_rows = []
    for root_s, root_g, length in ((F(1, 2), F(3, 4), 2), (F(2, 3), F(5, 6), 3)):
        s_value, g_value = root_s**length, root_g**length
        require(0 < s_value < 1 and s_value * s_value < g_value < 1, "CT input failed")
        require(root_g > root_s * root_s, "CT root factor failed")
        require(root_s**length == s_value and root_g**length == g_value, "CT composition failed")
        ct_rows.append({
            "length": length,
            "effective": [str(s_value), str(g_value)],
            "factor": [str(root_s), str(root_g)],
        })

    payload = {
        "schema": "k2p-domain-rooting-v1",
        "fourier_spectrum": ["1", "s", "g", "s"],
        "transition_probabilities": ["(1+2*s+g)/4", "(1-g)/4", "(1-2*s+g)/4", "(1-g)/4"],
        "strict_nonsingular_inequalities": ["1-g>0", "1+2*s+g>0", "1-2*s+g>0", "s*g!=0"],
        "D_plus": ["0<s<1", "0<g<1", "g>2*s-1"],
        "continuous_time": ["0<s<1", "s^2<g<1"],
        "rational_grid_checks": checked,
        "near_identity_factorizations": factor_rows,
        "continuous_time_subdivisions": ct_rows,
        "rooting_argument": {
            "reversibility": "the uniform stationary distribution and symmetric K2P transition matrices permit reversal of every non-arrowhead edge",
            "subdivision": "in Fourier coordinates edge composition is (s1*s2,g1*g2), and the displayed strict factorization realizes insertion of the root inside any edge",
            "conclusion": "all admissible rooted representatives of one fixed semi-directed network have the same strict physical image on D_plus and on the strict continuous-time cone",
        },
    }
    certificate = dict(payload)
    certificate["payload_sha256"] = sha_object(payload)
    output = HERE / "domain_rooting_certificate.json"
    output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print("K2P_DOMAIN_ROOTING_PASS")
    print(json.dumps({
        "payload_sha256": certificate["payload_sha256"],
        "certificate_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "grid_checks": checked,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
