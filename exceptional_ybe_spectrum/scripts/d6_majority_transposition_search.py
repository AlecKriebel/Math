#!/usr/bin/env python3
"""Exact finite search in a qubit-qutrit majority-reflection ansatz.

The local space is C^2 tensor C^3.  On each qutrit factor fix a transposition
T, and use tensor words from

    {I,X,Y,Z} tensor {I,T}

on each of the two local sites.  The program exhausts commuting triples
A,B,C and words E anticommuting with all three, forms

    M=(-s_A A-s_B B-s_C C+s_A s_B s_C ABC)/2,
    H=sqrt(2/3) M + epsilon E/sqrt(3),

and tests the exceptional cubic relation exactly in the tensor-word algebra.

All coefficients are represented as Gaussian-integer multiples of sqrt(3)
and sqrt(6) after multiplying the residual by 216, so a reported zero is
exact.  Fixing s_A=+1 loses no solutions: simultaneous reversal of all three
signs negates M, while H -> -H preserves the cubic equation; both signs of E
are enumerated.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import sys
import time
from collections import defaultdict


# Pauli codes: 0=I, 1=X, 2=Y, 3=Z.  The phase is a Gaussian unit represented
# as (real, imaginary).
PAULI_PRODUCT = {
    (0, 0): ((1, 0), 0),
    (0, 1): ((1, 0), 1),
    (0, 2): ((1, 0), 2),
    (0, 3): ((1, 0), 3),
    (1, 0): ((1, 0), 1),
    (1, 1): ((1, 0), 0),
    (1, 2): ((0, 1), 3),
    (1, 3): ((0, -1), 2),
    (2, 0): ((1, 0), 2),
    (2, 1): ((0, -1), 3),
    (2, 2): ((1, 0), 0),
    (2, 3): ((0, 1), 1),
    (3, 0): ((1, 0), 3),
    (3, 1): ((0, 1), 2),
    (3, 2): ((0, -1), 1),
    (3, 3): ((1, 0), 0),
}

SiteWord = tuple[int, int]  # (Pauli code, transposition exponent)
PairWord = tuple[SiteWord, SiteWord]
TripleWord = tuple[SiteWord, SiteWord, SiteWord]
Gaussian = tuple[int, int]


def gaussian_multiply(a: Gaussian, b: Gaussian) -> Gaussian:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def site_multiply(a: SiteWord, b: SiteWord) -> tuple[Gaussian, SiteWord]:
    phase, pauli = PAULI_PRODUCT[(a[0], b[0])]
    return phase, (pauli, a[1] ^ b[1])


def word_multiply(
    a: tuple[SiteWord, ...], b: tuple[SiteWord, ...]
) -> tuple[Gaussian, tuple[SiteWord, ...]]:
    phase = (1, 0)
    output = []
    for left, right in zip(a, b):
        local_phase, local_word = site_multiply(left, right)
        phase = gaussian_multiply(phase, local_phase)
        output.append(local_word)
    return phase, tuple(output)


def commuting(a: PairWord, b: PairWord) -> int:
    phase_ab, word_ab = word_multiply(a, b)
    phase_ba, word_ba = word_multiply(b, a)
    if word_ab != word_ba:
        return 0
    if phase_ab == phase_ba:
        return 1
    if phase_ab == (-phase_ba[0], -phase_ba[1]):
        return -1
    return 0


def pair_product(a: PairWord, b: PairWord) -> tuple[Gaussian, PairWord]:
    phase, word = word_multiply(a, b)
    return phase, word  # type: ignore[return-value]


def word_trace(word: PairWord) -> int:
    result = 1
    for pauli, transposition_exponent in word:
        if pauli != 0:
            return 0
        result *= 3 if transposition_exponent == 0 else 1
    return result


def add_raw_term(
    raw: dict[PairWord, list[int]],
    word: PairWord,
    radical: int,
    coefficient: int,
    phase: Gaussian = (1, 0),
) -> None:
    # raw[word] stores real/imag coefficients of sqrt(3), then sqrt(6).
    slot = raw.setdefault(word, [0, 0, 0, 0])
    offset = 0 if radical == 3 else 2
    slot[offset] += coefficient * phase[0]
    slot[offset + 1] += coefficient * phase[1]
    if slot == [0, 0, 0, 0]:
        del raw[word]


def multiply_radicals(tags: tuple[int, int, int]) -> tuple[int, int]:
    """Return (integer factor, squarefree radical) for three tags in {3,6}."""
    product = tags[0] * tags[1] * tags[2]
    if product == 27:
        return (3, 3)
    if product == 54:
        return (3, 6)
    if product == 108:
        return (6, 3)
    if product == 216:
        return (6, 6)
    raise AssertionError(product)


def combine_pair_words(
    left: PairWord, middle: PairWord, right: PairWord
) -> tuple[Gaussian, PairWord]:
    phase1, product1 = pair_product(left, middle)
    phase2, product2 = pair_product(product1, right)
    return gaussian_multiply(phase1, phase2), product2


def raw_h_terms(
    a: PairWord,
    b: PairWord,
    c: PairWord,
    sign_b: int,
    sign_c: int,
    e: PairWord,
    sign_e: int,
) -> list[tuple[PairWord, int, int]]:
    # H=(sqrt(6) U + sqrt(3) V)/6.
    phase_ab, ab = pair_product(a, b)
    phase_abc, abc = pair_product(ab, c)
    phase_abc = gaussian_multiply(phase_ab, phase_abc)
    if phase_abc[1] != 0:
        raise AssertionError("commuting Hermitian product acquired imaginary phase")

    combined: dict[tuple[PairWord, int], int] = defaultdict(int)
    combined[(a, 6)] += -1
    combined[(b, 6)] += -sign_b
    combined[(c, 6)] += -sign_c
    combined[(abc, 6)] += sign_b * sign_c * phase_abc[0]
    combined[(e, 3)] += 2 * sign_e
    return [
        (word, radical, coefficient)
        for (word, radical), coefficient in combined.items()
        if coefficient
    ]


def trace_zero(terms: list[tuple[PairWord, int, int]]) -> bool:
    traces = {3: 0, 6: 0}
    for word, radical, coefficient in terms:
        traces[radical] += coefficient * word_trace(word)
    return traces[3] == 0 and traces[6] == 0


def embed_h1(word: PairWord) -> TripleWord:
    return (word[0], word[1], (0, 0))


def embed_h2(word: PairWord) -> TripleWord:
    return ((0, 0), word[0], word[1])


def cubic_residual(
    terms: list[tuple[PairWord, int, int]]
) -> dict[TripleWord, tuple[int, int, int, int]]:
    # Values store Gaussian coefficients of sqrt(3), sqrt(6) in 216*F.
    residual: dict[TripleWord, list[int]] = {}

    def add(
        word: TripleWord,
        radical: int,
        gaussian_coefficient: Gaussian,
    ) -> None:
        slot = residual.setdefault(word, [0, 0, 0, 0])
        offset = 0 if radical == 3 else 2
        slot[offset] += gaussian_coefficient[0]
        slot[offset + 1] += gaussian_coefficient[1]
        if slot == [0, 0, 0, 0]:
            del residual[word]

    embedded1 = [(embed_h1(w), r, c) for w, r, c in terms]
    embedded2 = [(embed_h2(w), r, c) for w, r, c in terms]

    for sequence, overall_sign in (
        ((embedded1, embedded2, embedded1), 1),
        ((embedded2, embedded1, embedded2), -1),
    ):
        for left, middle, right in itertools.product(*sequence):
            phase1, product1 = word_multiply(left[0], middle[0])
            phase2, output = word_multiply(product1, right[0])
            phase = gaussian_multiply(phase1, phase2)
            integer_factor, radical = multiply_radicals(
                (left[1], middle[1], right[1])
            )
            coefficient = (
                overall_sign
                * left[2]
                * middle[2]
                * right[2]
                * integer_factor
            )
            add(
                output,  # type: ignore[arg-type]
                radical,
                (coefficient * phase[0], coefficient * phase[1]),
            )

    # 216 * (H_1-H_2)/3 = 12 times the raw numerator of H.
    for word, radical, coefficient in embedded1:
        add(word, radical, (-12 * coefficient, 0))
    for word, radical, coefficient in embedded2:
        add(word, radical, (12 * coefficient, 0))

    return {word: tuple(value) for word, value in residual.items()}


def canonical_residual_bytes(
    residual: dict[TripleWord, tuple[int, int, int, int]]
) -> bytes:
    rows = []
    for word, coefficient in sorted(residual.items()):
        rows.append(repr((word, coefficient)).encode("ascii"))
    return b"\n".join(rows)


def main(output_path: str | None) -> int:
    start = time.monotonic()
    words: list[PairWord] = [
        ((q1, e1), (q2, e2))
        for q1, e1, q2, e2 in itertools.product(
            range(4), range(2), range(4), range(2)
        )
    ]
    identity = ((0, 0), (0, 0))
    nonidentity = [word for word in words if word != identity]

    commutation = {
        (a, b): commuting(a, b) for a in words for b in words
    }

    counters = defaultdict(int)
    best: dict | None = None
    solutions: list[dict] = []
    digest = hashlib.sha256()
    residual_cache: dict[
        tuple[tuple[PairWord, int, int], ...],
        tuple[tuple[int, int], bytes, bool],
    ] = {}

    for a, b, c in itertools.combinations(nonidentity, 3):
        if not (
            commutation[(a, b)] == 1
            and commutation[(a, c)] == 1
            and commutation[(b, c)] == 1
        ):
            continue
        counters["commuting_triples"] += 1
        eligible_e = [
            e
            for e in nonidentity
            if (
                commutation[(a, e)] == -1
                and commutation[(b, e)] == -1
                and commutation[(c, e)] == -1
            )
        ]
        if not eligible_e:
            continue
        counters["triples_with_anticommuting_e"] += 1

        for e in eligible_e:
            for sign_b, sign_c, sign_e in itertools.product((1, -1), repeat=3):
                counters["raw_candidates"] += 1
                terms = raw_h_terms(
                    a, b, c, sign_b, sign_c, e, sign_e
                )
                if not trace_zero(terms):
                    continue
                counters["trace_zero_candidates"] += 1
                terms_key = tuple(sorted(terms))
                cached = residual_cache.get(terms_key)
                if cached is None:
                    residual = cubic_residual(terms)
                    encoded = canonical_residual_bytes(residual)
                    score = (
                        len(residual),
                        sum(
                            sum(abs(x) for x in value)
                            for value in residual.values()
                        ),
                    )
                    residual_digest = hashlib.sha256(encoded).digest()
                    is_zero = not residual
                    residual_cache[terms_key] = (
                        score,
                        residual_digest,
                        is_zero,
                    )
                    counters["unique_trace_zero_h"] += 1
                else:
                    score, residual_digest, is_zero = cached
                    residual = (
                        cubic_residual(terms)
                        if best is None or score < tuple(best["score"])
                        else {}
                    )
                digest.update(residual_digest)
                digest.update(b"\0")
                if best is None or score < tuple(best["score"]):
                    if cached is not None and not residual:
                        residual = cubic_residual(terms)
                    best = {
                        "score": list(score),
                        "a": a,
                        "b": b,
                        "c": c,
                        "e": e,
                        "sign_b": sign_b,
                        "sign_c": sign_c,
                        "sign_e": sign_e,
                        "terms": terms,
                        "residual": [
                            {"word": word, "coefficient": coefficient}
                            for word, coefficient in sorted(residual.items())
                        ],
                    }
                if is_zero:
                    solutions.append(
                        {
                            "a": a,
                            "b": b,
                            "c": c,
                            "e": e,
                            "sign_b": sign_b,
                            "sign_c": sign_c,
                            "sign_e": sign_e,
                            "terms": terms,
                        }
                    )

    report = {
        "status": "exact_exhaustive_ansatz_search",
        "ansatz": "qubit-qutrit fixed-transposition majority reflection",
        "normalization": (
            "residual coefficients are exact Gaussian-integer multiples "
            "of sqrt(3) and sqrt(6) after scaling by 216"
        ),
        "word_count": len(words),
        "counters": dict(counters),
        "solution_count": len(solutions),
        "solutions": solutions,
        "best_nonzero_residual": best,
        "ordered_residual_digest_sha256": digest.hexdigest(),
        "elapsed_seconds": time.monotonic() - start,
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if output_path is not None:
        from pathlib import Path

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    return 0 if not solutions else 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.output))
