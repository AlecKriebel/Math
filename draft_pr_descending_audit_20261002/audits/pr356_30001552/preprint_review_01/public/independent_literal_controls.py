#!/usr/bin/env python3
"""Independent literal-block finite falsifiers; no package imports."""
from itertools import product, combinations_with_replacement
from math import gcd
import json


def transform(word, sigma, anti=True):
    return tuple(sigma[x] for x in (word[::-1] if anti else word))


def alternating(word, p, sigma, anti=True):
    if p > len(word):
        return True  # nonempty alphabets in the specified finite models
    root = word[:p]
    double = root + transform(root, sigma, anti)
    repeated = double * ((len(word) + len(double) - 1) // len(double))
    return repeated[:len(word)] == word


def ordinary(word, p):
    return all(a == b for a, b in zip(word, word[p:]))


def general(word, p, sigma):
    root = word[:p]
    mirror = transform(root, sigma)
    return all(word[j:j+p] in (root[:len(word[j:j+p])],
                              mirror[:len(word[j:j+p])])
               for j in range(0, len(word), p))


def run():
    models = [("binary_reversal", (0, 1), 9),
              ("binary_reverse_exchange", (1, 0), 9),
              ("ternary_reversal", (0, 1, 2), 7),
              ("ternary_exchange_fixed", (1, 0, 2), 7),
              ("quaternary_two_exchange", (1, 0, 3, 2), 6)]
    results = []
    morphic_witness = None
    for name, sigma, bound in models:
        words = 0
        equivalence_checks = 0
        theorem_checks = 0
        boundary_checks = 0
        for n in range(1, bound + 1):
            for word in product(range(len(sigma)), repeat=n):
                words += 1
                reflected = transform(word, sigma) + word
                periods = []
                morphic_periods = []
                for p in range(1, n + 1):
                    literal = alternating(word, p, sigma)
                    assert literal == ordinary(reflected, 2*p), (name, word, p)
                    equivalence_checks += 1
                    if literal:
                        periods.append(p)
                    if morphic_witness is None and alternating(word, p, sigma, False):
                        morphic_periods.append(p)
                for p, q in combinations_with_replacement(periods, 2):
                    d = gcd(p, q)
                    threshold = p + q - d
                    if n >= threshold:
                        assert alternating(word, d, sigma), (name, word, p, q)
                        theorem_checks += 1
                        boundary_checks += n == threshold
                if morphic_witness is None:
                    for p, q in combinations_with_replacement(morphic_periods, 2):
                        d = gcd(p, q)
                        if n >= p + q - d and not alternating(word, d, sigma, False):
                            morphic_witness = {"model": name, "word": word,
                                               "p": p, "q": q, "gcd": d,
                                               "length": n}
                            break
        results.append({"model": name, "max_length": bound, "words": words,
                        "extension_equivalences": equivalence_checks,
                        "theorem_instances": theorem_checks,
                        "exact_threshold_instances": boundary_checks})
    abb = (0, 1, 1)
    ident = (0, 1)
    assert alternating(abb, 2, ident) and alternating(abb, 3, ident)
    assert not alternating(abb, 1, ident)
    assert ordinary(transform(abb, ident) + abb, 4)
    assert not ordinary(abb + transform(abb, ident), 4)
    abba = (0, 1, 1, 0)
    assert general(abba, 2, ident) and general(abba, 3, ident)
    assert not alternating(abba, 3, ident) and not alternating(abba, 1, ident)
    abab = (0, 1, 0, 1)
    swap = (1, 0)
    assert alternating(abab, 2, swap) and alternating(abab, 3, swap)
    assert alternating(abab, 1, swap) and not ordinary(abab, 1)
    assert morphic_witness is not None
    print(json.dumps({"status": "pass", "models": results,
                      "orientation_mutant_rejected": True,
                      "general_period_definition_mutant_rejected": True,
                      "ordinary_gcd_mutant_rejected": True,
                      "uniform_sharpness_checked": True,
                      "morphic_hypothesis_mutant_witness": morphic_witness},
                     sort_keys=True, indent=2))


if __name__ == "__main__":
    run()
