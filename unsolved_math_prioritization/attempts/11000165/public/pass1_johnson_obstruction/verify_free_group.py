"""Exact reduced-word check for the outer-automorphism obstruction.

This checks finite examples and catches convention errors. The all-genus,
all-power conclusion is the proof in PROOF.md, not the finite test set.
"""
import json
from pathlib import Path


def require(condition):
    if not condition:
        raise AssertionError("Free-group identity check failed")


def reduce_word(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)


def inverse(word):
    return tuple(-x for x in reversed(word))


def multiply(*words):
    return reduce_word(x for word in words for x in word)


def apply(automorphism, word):
    return multiply(*(automorphism[abs(x)] if x > 0 else
                      inverse(automorphism[abs(x)]) for x in word))


def compose(a, b):
    # a*b means apply b first, then a.
    return {i: apply(a, b[i]) for i in b}


def power_word(word, n):
    return multiply(*((word if n >= 0 else inverse(word),) * abs(n)))


def test_rank(g):
    identity = {i: (i,) for i in range(1, g+1)}
    a = {**identity, 1: (2, 1, -2)}
    ai = {**identity, 1: (-2, 1, 2)}
    b = {**identity, 2: (3, 2, -3)}
    bi = {**identity, 2: (-3, 2, 3)}
    require(compose(a, ai) == identity == compose(ai, a))
    require(compose(b, bi) == identity == compose(bi, b))
    phi = compose(compose(compose(a, b), ai), bi)
    phii = compose(compose(compose(b, a), bi), ai)
    require(compose(phi, phii) == identity == compose(phii, phi))
    w = (3, -2, -3, 2)
    require(phi == {**identity, 1: multiply(w, (1,), inverse(w))})
    require(all(phi[i] == (i,) for i in range(2, g+1)))
    require(apply(phi, w) == w)
    for n in range(-12, 13):
        actual = identity
        for _ in range(abs(n)):
            actual = compose(phi if n >= 0 else phii, actual)
        wn = power_word(w, n)
        expected = {**identity, 1: multiply(wn, (1,), inverse(wn))}
        require(actual == expected)
        require(len(actual[1]) == 8*abs(n)+1)
        if n:
            require(actual[1] != (1,))
        for i in range(1, g+1):
            abelianization = [sum((1 if x > 0 else -1) for x in actual[i]
                                 if abs(x) == j) for j in range(1, g+1)]
            require(abelianization == [int(i == j) for j in range(1, g+1)])
    return {"rank": g, "powers_checked": [-12, 12],
            "commutator_image_x1": list(phi[1]), "all_checks_passed": True}


if __name__ == "__main__":
    result = {"composition_convention": "rightmost map acts first",
              "word_encoding": "signed integers are free generators and inverses",
              "results": [test_rank(g) for g in range(3, 13)],
              "limitation": "Finite convention check; infinitude and non-innerness are proved in PROOF.md."}
    output = Path(__file__).with_name("FREE_GROUP_CHECK.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"all_checks_passed": True, "ranks": [3, 12],
                      "powers": [-12, 12], "output": output.name}))
