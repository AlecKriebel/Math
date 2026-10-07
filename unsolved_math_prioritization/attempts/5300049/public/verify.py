#!/usr/bin/env python3
"""Deterministic exact sanity checks for the stated auxiliary examples.

Python 3 standard library only. No network, symbolic algebra, or numerical
Julia-set inference. These tests do not prove the original open question.
"""
from fractions import Fraction
from itertools import product
from math import isqrt
import argparse
import hashlib
import json
from pathlib import Path


def check_record_times():
    checked = selected = 0
    for n in range(1, 7):
        for a in product((-2, 0, 1, 3), repeat=n):
            checked += 1
            s = [0]
            for value in a:
                s.append(s[-1] + value)
            # A=3, b=1, c=1/2; scale all T-values by two.
            t = [2 * s[j] - j for j in range(n + 1)]
            records = []
            maximum = 0
            for j in range(1, n + 1):
                if t[j] > maximum:
                    records.append(j)
                    assert t[j] - maximum <= 5
                    assert all(2 * (s[j] - s[k]) >= j - k for k in range(j))
                    maximum = t[j]
            if s[n] >= n:
                selected += 1
                assert 5 * len(records) >= n
    return {"sequences": checked, "satisfying_average_hypothesis": selected,
            "max_length": 6, "A": 3, "b": 1, "c": "1/2"}


def dyadic_term(i):
    if i >= 4 and i & (i - 1) == 0:
        return 1 - i // 4
    return 1


def check_dyadic_sequence():
    total = 0
    records = []
    maximum = 0
    samples = []
    for n in range(1, 4097):
        total += dyadic_term(n)
        if n >= 4:
            m = n.bit_length() - 1
            assert total == n - (2 ** (m - 1) - 1)
            assert 2 * total >= n
        # c=1/4, A=1, b=1/2. Max record increment is 3.
        t = 4 * total - n
        if t > maximum:
            assert t - maximum <= 3
            records.append(n)
            maximum = t
        assert 3 * len(records) >= n
        if n >= 4 and n & (n - 1) == 0:
            assert Fraction(dyadic_term(n), n) == Fraction(1, n) - Fraction(1, 4)
            samples.append({"n": n, "S_n/n": str(Fraction(total, n)),
                            "a_n/n": str(Fraction(dyadic_term(n), n))})
    for cutoff in (1, 4, 16, 64):
        n = 4096
        tail = sum(-dyadic_term(i) for i in range(1, n + 1)
                   if dyadic_term(i) < -cutoff)
        assert Fraction(tail, n) >= Fraction(1, 4) - Fraction(1, n)
    return {"terms": 4096, "record_times_c_1_4": len(records), "samples": samples}


def vertex(word):
    n = len(word)
    try:
        k = word.index(1) + 1
    except ValueError:
        return Fraction(1)
    return 1 - Fraction(min(max(n - k, 0), k), k + 1)


def check_tree():
    checked = 0
    for n in range(1, 11):
        for w in product((0, 1), repeat=n):
            edge = abs(vertex(w) - vertex(w[:-1]))
            assert edge <= Fraction(2, n + 2)
            checked += 1
    for k in range(1, 65):
        for n in range(2 * k, 2 * k + 6):
            w = (0,) * (k - 1) + (1,) + (0,) * (n - k)
            assert vertex(w) == Fraction(1, k + 1)
        assert vertex((0,) * (2 * k)) == 1
    return {"edges": checked, "max_generation": 10,
            "eventual_endpoint_controls": 64, "uniform_bound": "2/(n+2)"}


def check_square_digit_counts():
    checked = 0
    for n in (32, 64, 128, 256, 512, 1024):
        for m in range(1, 13):
            positions = {k * k for k in range(1, isqrt(n + m) + 1)}
            exceptional = sum(any(j + t in positions for t in range(1, m + 1))
                              for j in range(n))
            assert exceptional <= m * (isqrt(n + m) + 1)
            checked += 1
    return {"window_count_tests": checked, "max_N": 1024, "max_window": 12}


def check_monomials():
    checked = 0
    for d in range(2, 11):
        for n in range(1, 11):
            # Derivative exponent of z in the chain rule:
            assert (d - 1) * sum(d ** j for j in range(n)) == d ** n - 1
            assert d ** n > 1
            checked += 1
    return {"integer_chain_rule_controls": checked}


def verify_manifest():
    root = Path(__file__).resolve().parent
    manifest = root / "SHA256SUMS"
    if not manifest.exists():
        return {"present": False}
    count = 0
    expected_names = set()
    for line in manifest.read_text().splitlines():
        digest, name = line.split("  ", 1)
        assert Path(name).name == name, "Manifest accepts only adjacent files."
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
        expected_names.add(name)
        count += 1
    actual_names = {p.name for p in root.iterdir() if p.is_file() and p.name != "SHA256SUMS"}
    assert actual_names == expected_names, (actual_names, expected_names)
    return {"present": True, "checked_files": count}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write deterministic verification.json")
    parser.add_argument("--check-manifest", action="store_true")
    args = parser.parse_args()
    result = {"schema_version": 1,
              "scope": "Finite exact checks of auxiliary lemmas; no solution or formal-proof certificate.",
              "record_times": check_record_times(),
              "dyadic_sequence": check_dyadic_sequence(),
              "abstract_tree": check_tree(),
              "square_digit_counts": check_square_digit_counts(),
              "monomials": check_monomials(), "passed": True}
    out = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        (Path(__file__).resolve().parent / "verification.json").write_text(out)
    print(out, end="")
    if args.check_manifest:
        print(json.dumps({"manifest": verify_manifest()}, sort_keys=True))


if __name__ == "__main__":
    main()
