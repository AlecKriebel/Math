"""Independent direct-word controls; no submitted modules or graph algorithms used."""
from itertools import product
from math import gcd
import json
import random

counts = {
    "word_involution_cases": 0,
    "reflection_period_checks": 0,
    "qualifying_gcd_checks": 0,
    "nondividing_gcd_checks": 0,
    "direct_subtraction_checks": 0,
    "random_seed_prefix_cases": 0,
    "sharpness_witnesses": 0,
    "excluded_model_counterexamples": 0,
    "boundary_cases": 0,
}


def theta(word, tau):
    return tuple(tau[x] for x in word[::-1])


def is_alternating(word, period, tau):
    assert period > 0
    # If the block exceeds the observed word, complete it arbitrarily.
    if period >= len(word):
        return True
    seed = word[:period]
    block = seed + theta(seed, tau)
    repeats, tail = divmod(len(word), len(block))
    return word == block * repeats + block[:tail]


def ordinary_period(word, period):
    return word[:-period] == word[period:] if period < len(word) else True


def verify(word, tau):
    counts["word_involution_cases"] += 1
    n = len(word)
    periods = [p for p in range(1, n + 1) if is_alternating(word, p, tau)]
    reflected = theta(word, tau) + word
    for p in periods:
        assert ordinary_period(reflected, 2 * p), (word, tau, p)
        counts["reflection_period_checks"] += 1
    for p in periods:
        for q in periods:
            d = gcd(p, q)
            if n < p + q - d:
                continue
            assert is_alternating(word, d, tau), (word, tau, p, q)
            counts["qualifying_gcd_checks"] += 1
            if p % q and q % p:
                counts["nondividing_gcd_checks"] += 1
            if p > q:
                # A consequence, not an input to the theorem proof.
                assert is_alternating(word, p - q, tau), (word, tau, p, q)
                counts["direct_subtraction_checks"] += 1


# Mixed fixed-letter/two-cycle action is absent from the submitted binary scan.
for tau in ((0, 1, 2), (1, 0, 2)):
    for n in range(1, 10):
        for word in product(range(3), repeat=n):
            verify(word, tau)


# Deterministic longer prefixes vary the ending phase without enumerating graphs.
rng = random.Random(35630001552)
for tau in ((0,), (0, 1, 2), (1, 0, 2), (1, 0, 3, 2), (0, 1, 3, 2)):
    for p in range(1, 65):
        seed = tuple(rng.randrange(len(tau)) for _ in range(p))
        block = seed + theta(seed, tau)
        for n in sorted({p, p + 1, 2 * p - 1, 2 * p, 2 * p + 1, 3 * p + 2}):
            k, r = divmod(n, 2 * p)
            word = block * k + block[:r]
            assert is_alternating(word, p, tau)
            reflected = theta(word, tau) + word
            assert ordinary_period(reflected, 2 * p), (tau, p, n)
            counts["random_seed_prefix_cases"] += 1


for p, q, word, tau in (
    (2, 3, (0, 1, 1), (0, 1)),
    (3, 4, (0, 1, 1, 1, 1), (0, 1)),
    (4, 7, (0, 0, 0, 1, 1, 0, 0, 0, 0), (0, 1)),
    (2, 3, (0, 0, 1), (1, 0)),
):
    assert len(word) == p + q - gcd(p, q) - 1
    assert is_alternating(word, p, tau) and is_alternating(word, q, tau)
    assert not is_alternating(word, gcd(p, q), tau)
    counts["sharpness_witnesses"] += 1


# The finite-word doubling reduction actually fails for the excluded models.
mixed = (0, 1, 0, 1, 1, 0)  # ab | ab | ba for reversal and seed ab.
assert not ordinary_period(theta(mixed, (0, 1)) + mixed, 4)
counts["excluded_model_counterexamples"] += 1
morphic_word = (0, 0, 1)  # Prefix of aa | bb | aa | bb for morphic swap.
morphic_image = tuple(1 - x for x in morphic_word)
assert not ordinary_period(morphic_image + morphic_word, 4)
counts["excluded_model_counterexamples"] += 1


for tau in ((0,), (1, 0, 2)):
    assert is_alternating((), 1, tau)
    assert not (0 >= 1 + 1 - gcd(1, 1))
    assert is_alternating((0,), 2, tau)
    counts["boundary_cases"] += 1

print(json.dumps({
    "status": "PASS",
    "mechanism": "direct finite-word equality and prefix construction, no imported checker or constraint graph",
    "exhaustive_scope": "every ternary word length1..9, identity and mixed swap/fixed-letter involutions",
    "random_scope": "fixed PR/problem seed; five involution types; p1..64; six ending-phase choices",
    "counts": counts,
    "proof_scope": "supplementary finite controls; universal theorem verified in written assessment",
}, indent=2))
