#!/usr/bin/env python3
"""Independent exact-word checks for the literal growth-metric observation.

Uses string rewriting rather than the author's signed-letter stack reducer.
Finite checks supplement, and do not replace, the all-n proof in AUDIT.md.
The non-specialness conclusion relies on the explicitly identified prior theorem.
"""
from pathlib import Path
import datetime
import hashlib
import json

LETTERS = "abcABC"
INVERSE = dict(zip(LETTERS, "ABCabc"))


def inverse(word):
    return "".join(INVERSE[x] for x in reversed(word))


def reduce_word(word):
    while True:
        old = word
        for x in LETTERS:
            word = word.replace(x + INVERSE[x], "")
        if word == old:
            return word


def substitute(word, images):
    signed = dict(images)
    signed.update({x.upper(): inverse(w) for x, w in images.items()})
    return reduce_word("".join(signed[x] for x in word))


def conjugate(p, w):
    return reduce_word(p + w + inverse(p))


def cyclic_length(word):
    word = reduce_word(word)
    while len(word) > 1 and word[0] == INVERSE[word[-1]]:
        word = word[1:-1]
    return len(word)


ALPHA = {"a": "a", "b": "ba", "c": "caa"}
ALPHA_INV = {"a": "a", "b": "bA", "c": "cAA"}
PHI = {x: conjugate("b", w) for x, w in ALPHA.items()}
PHI_INV = {x: substitute(conjugate("B", x), ALPHA_INV) for x in "abc"}

for maps, back in ((ALPHA, ALPHA_INV), (PHI, PHI_INV)):
    assert all(substitute(maps[x], back) == x for x in "abc")
    assert all(substitute(back[x], maps) == x for x in "abc")

rows = []
state = {x: x for x in "abc"}
for n in range(49):
    p = "".join("b" + "a" * i for i in range(n))
    expected = {"a": "a", "b": "b" + "a" * n, "c": "c" + "a" * (2 * n)}
    assert all(state[x] == conjugate(p, expected[x]) for x in "abc")
    lengths = [len(state[x]) for x in "abc"]
    cycles = [cyclic_length(state[x]) for x in "abc"]
    if n:
        assert lengths == [n*n - n + 3, n*n + 3, n*n + n + 3]
        assert cycles == [1, n + 1, 2*n + 1]
    rows.append({"n": n, "word_lengths": lengths, "cyclic_lengths": cycles})
    state = {x: substitute(state[x], PHI) for x in "abc"}

negative_rows = []
state = {x: x for x in "abc"}
for n in range(33):
    p = "".join("a" * i + "B" for i in range(1, n + 1))
    expected = {"a": "a", "b": "b" + "A" * n, "c": "c" + "A" * (2 * n)}
    assert all(state[x] == conjugate(p, expected[x]) for x in "abc")
    lengths = [len(state[x]) for x in "abc"]
    if n:
        b_length = 2 if n == 1 else n*n - 1
        assert lengths == [n*n + 3*n + 1, b_length, n*n + 5*n + 1]
    negative_rows.append({"n": n, "word_lengths_of_phi_minus_n": lengths})
    state = {x: substitute(state[x], PHI_INV) for x in "abc"}


def iterate_alpha(word, power):
    maps = ALPHA if power >= 0 else ALPHA_INV
    for _ in range(abs(power)):
        word = substitute(word, maps)
    return word


def multiply(pair, other):
    word, exponent = pair
    right, degree = other
    return reduce_word(word + iterate_alpha(right, exponent)), exponent + degree


stable = ("b", 1)
stable_inverse = (iterate_alpha("B", -1), -1)
assert multiply(stable, stable_inverse) == ("", 0)
assert multiply(stable_inverse, stable) == ("", 0)
for x in "abc":
    assert multiply(multiply(stable, (x, 0)), stable_inverse) == (PHI[x], 0)

result = {
    "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "PASS",
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "alpha": ALPHA,
    "alpha_inverse": ALPHA_INV,
    "phi": PHI,
    "phi_inverse": PHI_INV,
    "positive_n_range": [0, 48],
    "negative_n_range": [0, 32],
    "positive_checks": rows,
    "negative_checks": negative_rows,
    "mapping_torus_convention": "t x t^-1 = alpha(x)",
    "phi_stable_letter_in_alpha_torus": "b t",
    "mapping_torus_relation_checks": "PASS in exact semidirect-product normal forms",
    "scope": "Literal 21.125(a) counterexample from prior Gersten obstruction; no Hydra or originality claim",
    "limitations": [
        "Finite experiments do not prove the displayed formulas for all n; see AUDIT.md for that proof.",
        "Virtual nonembedding is the cited prior Brady-Soroko Corollary10.3, not a computational claim.",
        "No full 21.125 resolution or publication approval is asserted."
    ]
}
Path(__file__).with_name("INDEPENDENT_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print("PASS: inverses, all three exact lengths, cyclic lengths, and stable-letter relations.")
