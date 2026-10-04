#!/usr/bin/env python3
"""Explicit read-only finite comparison controls; no file writes or network."""
import itertools
import json
import math

def theta(word, sigma):
    return tuple(sigma[x] for x in reversed(word))


def alternating(word, p, sigma):
    assert 1 <= p <= len(word)
    u = word[:p]
    block = u + theta(u, sigma)
    return all(x == block[i % (2*p)] for i, x in enumerate(word))


def parity(word, sigma):
    return tuple(sigma[x] if i % 2 else x for i, x in enumerate(word))


def orbit_code(sigma):
    code = {}
    fresh = 0
    for a in range(len(sigma)):
        if a in code:
            continue
        partner = sigma[a]
        if partner == a:
            code[a] = (fresh, fresh)
            fresh += 1
        else:
            code[a] = (fresh, fresh+1)
            code[partner] = (fresh+1, fresh)
            fresh += 2
    assert len(set(code.values())) == len(sigma)
    return code, tuple(range(fresh))


def comparison_checks():
    sigmas = [s for s in itertools.permutations(range(3))
              if all(s[s[i]] == i for i in range(3))]
    assert len(sigmas) == 4
    periods = words = 0
    identity = (0, 1, 2)
    for sigma in sigmas:
        code, encoded_identity = orbit_code(sigma)
        encode = lambda w: tuple(y for x in w for y in code[x])
        for n in range(1, 8):
            for word in itertools.product(range(3), repeat=n):
                transformed = parity(word, sigma)
                assert parity(transformed, sigma) == word
                encoded = encode(word)
                assert encode(theta(word, sigma)) == encoded[::-1]
                words += 1
                for p in range(1, n+1):
                    original = alternating(word, p, sigma)
                    assert original == alternating(transformed, p, identity)
                    assert original == alternating(encoded, 2*p, encoded_identity)
                    periods += 1
    substitutions = 0
    for p in range(1, 51):
        for q in range(1, 51):
            g = math.gcd(p, q)
            target = p+q-g
            D = math.gcd(0, 2*p, 2*q)
            assert D == 2*g
            assert 2*p+2*q-D == 2*target
            encoded_D = math.gcd(0, 4*p, 4*q)
            assert 4*p+4*q-encoded_D == 4*target
            assert target >= max(p, q)
            substitutions += 1
    witness = (0, 1, 1)  # abb, theta=reversal
    assert alternating(witness, 2, identity)
    assert alternating(witness, 3, identity)
    assert not alternating(witness, 1, identity)
    return {"words_permutations": words,
            "period_equivalences_each": periods,
            "numeric_prior_bound_substitutions": substitutions,
            "uniform_sharpness_witness": "abb; reversal; p=2,q=3"}



if __name__ == "__main__":
    print(json.dumps({
        "status": "PASS",
        "checker_version": 1,
        "scope": "Finite comparison controls only; algebra is in mechanism_comparison.md. This is not a universal proof or a priority certificate.",
        "comparison_checks": comparison_checks()
    }, indent=2))
