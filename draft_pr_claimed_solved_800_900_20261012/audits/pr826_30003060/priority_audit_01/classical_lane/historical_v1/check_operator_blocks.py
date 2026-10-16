#!/usr/bin/env python3
"""Independent integer control for the two classical word operators.

This checks the operators' defining word expansions, not the unlimited theorem.
No external packages, candidate verifier, or candidate implementation is imported.
"""

from collections import Counter
from itertools import product
from pathlib import Path
import json


def rho(word):
    return word[-1:] + word[:-1]


def orbit(word):
    result = []
    current = word
    while current not in result:
        result.append(current)
        current = rho(current)
    assert current == word
    return result


def b_on_orbit_sum(words):
    """b(a tensor v)=av-va, expanded before any coinvariant quotient."""
    values = Counter()
    for word in words:
        a, v = word[:-1], word[-1:]
        values[a + v] += 1
        values[v + a] -= 1
    return {word: count for word, count in values.items() if count}


def euler_cap_on_orbit_sum(words):
    """Goodwillie's degree-one e_D(a tensor v)=D(v)a=va, D(v)=v."""
    values = Counter()
    for word in words:
        a, v = word[:-1], word[-1:]
        values[v + a] += 1
    return values


def connes_from_cyclic_derivative(word):
    """Loday's phi(1,v1...vn), then concatenate its small-chain output.

    The ith summand is (v(i+1)...vn v1...v(i-1)) tensor vi.
    This expansion is deliberately evaluated separately from repeated rho.
    """
    return Counter(word[i + 1:] + word[:i] + word[i:i + 1]
                   for i in range(len(word)))


def inspect_block(word):
    words = orbit(word)
    n, d = len(word), len(words)
    assert n % d == 0
    assert b_on_orbit_sum(words) == {}
    euler = euler_cap_on_orbit_sum(words)
    assert euler == Counter({w: 1 for w in words})
    # The coinvariant quotient identifies the d basis words without division.
    euler_scalar = sum(euler.values())
    assert euler_scalar == d
    connes = connes_from_cyclic_derivative(word)
    assert set(connes) == set(words)
    assert set(connes.values()) == {n // d}
    connes_scalar = connes[word]
    assert euler_scalar * connes_scalar == n
    return {"length": n, "orbit_size": d, "euler_scalar": euler_scalar,
            "connes_scalar": connes_scalar}


def main():
    cases, blocks = [], 0
    for rank in (1, 2, 3):
        for n in range(1, 8):
            seen, block_count = set(), 0
            for word in product(range(rank), repeat=n):
                if word in seen:
                    continue
                inspect_block(word)
                seen.update(orbit(word))
                block_count += 1
            assert len(seen) == rank ** n
            cases.append({"rank": rank, "length": n, "words": len(seen),
                          "orbits_checked": block_count})
            blocks += block_count

    contrasts = []
    for p in (2, 3, 5, 7):
        for name, word in (("primitive_p", (0,) * (p - 1) + (1,)),
                           ("pure_power_p", (0,) * p)):
            record = inspect_block(word)
            record.update({"prime": p, "word_type": name,
                           "euler_mod_p": record["euler_scalar"] % p,
                           "connes_mod_p": record["connes_scalar"] % p})
            if name == "primitive_p":
                assert (record["euler_mod_p"], record["connes_mod_p"]) == (0, 1)
            else:
                assert (record["euler_mod_p"], record["connes_mod_p"]) == (1, 0)
            contrasts.append(record)

    result = {"status": "passed", "scope": "finite integer operator control",
              "case_count": len(cases), "orbit_blocks_checked": blocks,
              "cases": cases, "characteristic_contrasts": contrasts,
              "unlimited_proof": "REPORT.md, Constructive deduction from prior results"}
    Path(__file__).with_name("OPERATOR_CHECK.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in
                      ("status", "case_count", "orbit_blocks_checked")}, indent=2))


if __name__ == "__main__":
    main()
