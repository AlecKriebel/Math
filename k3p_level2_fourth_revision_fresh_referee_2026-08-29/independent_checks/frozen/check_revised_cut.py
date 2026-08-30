#!/usr/bin/env python3
"""Referee-authored checks of the revised noncut handoff.

This file imports no reviewed-package module and reads no stored certificate.
It independently enumerates the full balanced-word universe and derives the
displayed-tree wrong-flattening minor from the K3P Fourier tree formula.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path

import sympy as sp


FAMILIES = (
    ("cycle", 2, 1),
    ("theta_TR_nested", 5, 1),
    ("theta_TR_separated", 5, 1),
    ("theta_TT_nested", 6, 2),
    ("theta_TT_separated", 6, 2),
)


def weak_compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for remainder in weak_compositions(total - first, parts - 1):
            yield (first, *remainder)


def run_lengths(word: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    answer: list[list[int]] = []
    for value in word:
        if not answer or answer[-1][0] != value:
            answer.append([value, 1])
        else:
            answer[-1][1] += 1
    return tuple((colour, length) for colour, length in answer)


def disposition(words: tuple[tuple[int, ...], ...], extras: tuple[int, ...]) -> str:
    run_rows = tuple(run_lengths(word) for word in words)
    if any(len(row) >= 3 for row in run_rows):
        return "three_run_path_obstruction"
    representatives = [colour for row in run_rows for colour, _length in row]
    counts = Counter((*representatives, *extras))
    if min(counts[0], counts[1]) >= 2:
        return "direct_palette"
    singleton = [colour for colour in (0, 1) if counts[colour] == 1]
    if len(singleton) != 1:
        raise RuntimeError(("unbalanced reduction", words, extras, counts))
    colour = singleton[0]
    matching_runs = [
        length
        for row in run_rows
        for value, length in row
        if value == colour
    ]
    if colour in extras or len(matching_runs) != 1 or matching_runs[0] < 2:
        raise RuntimeError(("invalid singleton doubling", words, extras, colour))
    return "singleton_doubled_palette"


def enumerate_words() -> dict[str, object]:
    total = Counter()
    records = []
    for family, segment_count, sink_count in FAMILIES:
        for nonroot in (False, True):
            extra_count = sink_count + int(nonroot)
            observed = Counter()
            closed_form = 0
            for active_count in range(4, 9):
                segment_letters = active_count - extra_count
                composition_count = comb(
                    segment_letters + segment_count - 1,
                    segment_count - 1,
                )
                closed_form += composition_count * (
                    2**active_count - 2 * active_count - 2
                )
                for lengths in weak_compositions(segment_letters, segment_count):
                    for letters in product((0, 1), repeat=segment_letters):
                        offset = 0
                        words = []
                        for length in lengths:
                            words.append(tuple(letters[offset : offset + length]))
                            offset += length
                        for extras in product((0, 1), repeat=extra_count):
                            counts = Counter((*letters, *extras))
                            if min(counts[0], counts[1]) < 2:
                                continue
                            observed[disposition(tuple(words), extras)] += 1
            observed_total = sum(observed.values())
            if observed_total != closed_form:
                raise RuntimeError(("closed-form mismatch", family, nonroot))
            total.update(observed)
            records.append({
                "family": family,
                "role": "nonroot" if nonroot else "root",
                "balanced_closed_form": closed_form,
                "counts": dict(sorted(observed.items())),
            })
    expected = {
        "direct_palette": 544_350,
        "singleton_doubled_palette": 34_304,
        "three_run_path_obstruction": 229_988,
    }
    if dict(sorted(total.items())) != expected or sum(total.values()) != 808_642:
        raise RuntimeError(("word census", total))
    if disposition(((1, 0, 1), (0,)), (0,)) != "three_run_path_obstruction":
        raise RuntimeError("101 mutation survived")
    if disposition(((0, 0), (1,)), (1,)) != "singleton_doubled_palette":
        raise RuntimeError("singleton-duplication mutation survived")
    return {
        "families_and_root_roles": records,
        "totals": {"balanced_total": 808_642, **expected},
        "closed_form": (
            "sum over m=4..8 of C(m-e+s-1,s-1)"
            "*(2^m-2m-2), summed over five families and both root roles"
        ),
    }


def quartet_minor() -> dict[str, object]:
    p = sp.symbols("p0:4", positive=True)
    u = sp.symbols("u", positive=True)

    def xor(values: tuple[int, ...]) -> int:
        result = 0
        for value in values:
            result ^= value
        return result

    def coordinate(row: tuple[int, int], column: tuple[int, int]):
        # Wrong flattening 02|13; the displayed quartet split is 01|23.
        h = (row[0], column[0], row[1], column[1])
        if xor(h) != 0:
            return sp.Integer(0)
        value = sp.Integer(1)
        for index, character in enumerate(h):
            if character:
                value *= p[index]
        if h[0] ^ h[1]:
            value *= u
        return value

    selected_rows = ((0, 0), (1, 1), (1, 0), (2, 0), (3, 0))
    selected_columns = ((0, 0), (1, 1), (1, 0), (2, 0), (3, 0))
    matrix = sp.Matrix([
        [coordinate(row, column) for column in selected_columns]
        for row in selected_rows
    ])
    determinant = sp.factor(matrix.det())
    expected = sp.factor(p[0] ** 4 * p[1] ** 4 * p[2] * p[3] * (1 - u**2))
    if sp.expand(determinant - expected) != 0:
        raise RuntimeError(("five-by-five determinant", determinant, expected))
    sample = matrix.subs({p[0]: sp.Rational(2, 3), p[1]: sp.Rational(3, 5),
                          p[2]: sp.Rational(4, 7), p[3]: sp.Rational(5, 8),
                          u: sp.Rational(7, 9)})
    if sample.rank() < 5 or sample.det() <= 0:
        raise RuntimeError("strict displayed-tree sample failed")
    return {
        "selected_wrong_flattening_rows_02": [list(row) for row in selected_rows],
        "selected_wrong_flattening_columns_13": [list(row) for row in selected_columns],
        "five_by_five_determinant": str(determinant),
        "strict_positive_for": "0<p0,p1,p2,p3,u<1",
        "exact_sample_rank": sample.rank(),
        "exact_sample_determinant": str(sample.det()),
    }


def main() -> None:
    if not __debug__:
        raise SystemExit("optimized Python forbidden")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    report = {
        "schema": "k3p-second-revision-referee-revised-cut-check-v1",
        "status": "PASS",
        "independence": {
            "package_modules_imported": False,
            "stored_certificates_read": False,
            "word_count_has_independent_closed_form": True,
            "minor_derived_from_fourier_tree_formula": True,
        },
        "balanced_words": enumerate_words(),
        "displayed_tree_minor": quartet_minor(),
    }
    raw = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_bytes(raw)
    print(json.dumps({
        "status": report["status"],
        "balanced_words": report["balanced_words"]["totals"]["balanced_total"],
        "output_sha256": hashlib.sha256(raw).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
