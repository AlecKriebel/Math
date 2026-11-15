#!/usr/bin/env python3
"""Independent exact finite-expression checks in the infinite free word algebra.

No product is projected to a bounded quotient. Bounds select test inputs only.
No third-party dependencies and no source/review file reads.
"""
from collections import Counter
from datetime import datetime, timezone
from functools import lru_cache
from itertools import product
import hashlib
import json
from pathlib import Path
import time


def words(bound):
    return ["".join(w) for n in range(bound + 1)
            for w in product("eo", repeat=n)]


def parity(w):
    return w.count("o") & 1


def sign(n):
    return -1 if n & 1 else 1


class Algebra:
    def __init__(self, p):
        assert p in (2, 3, 5)
        self.p = p

    def add(self, out, key, coefficient):
        coefficient = (out.get(key, 0) + coefficient) % self.p
        if coefficient:
            out[key] = coefficient
        else:
            out.pop(key, None)

    def scale(self, expression, scalar):
        return {k: (c * scalar) % self.p for k, c in expression.items()
                if (c * scalar) % self.p}

    def difference(self, a, b):
        out = dict(a)
        for k, c in b.items():
            self.add(out, k, -c)
        return out

    @lru_cache(None)
    def h_delta(self, w):
        out = {}
        # All assignments of positions to left (1) and right (0).
        for mask in range(1 << len(w)):
            left, right = [], []
            prior_right_odd = 0
            inversions = 0
            for index, letter in enumerate(w):
                if mask & (1 << index):
                    left.append(letter)
                    if letter == "o":
                        inversions += prior_right_odd
                else:
                    right.append(letter)
                    if letter == "o":
                        prior_right_odd += 1
            self.add(out, ("".join(left), "".join(right)), sign(inversions))
        return out

    @staticmethod
    def h_s(w):
        q = w.count("o")
        return sign(len(w) + q * (q - 1) // 2), w[::-1]

    @staticmethod
    def b_mul(a, b):
        u, i = a
        v, j = b
        return sign(i * parity(v)), (u + v, (i + j) & 1)

    @lru_cache(None)
    def b_delta(self, a, bad=False):
        w, i = a
        out = {}
        for (u, v), c in self.h_delta(w).items():
            shift = 0 if bad else parity(v)
            self.add(out, ((u, (i + shift) & 1), (v, i)), c)
        return out

    def b_s(self, a):
        w, i = a
        c, reverse = self.h_s(w)
        group = (i + parity(w)) & 1
        return c * sign(group * parity(w)), (reverse, group)

    def generator_delta(self, a):
        # Independent construction from Delta(e), Delta(o), Delta(g), expanded
        # by ordinary multiplication. No unshuffle or parity-of-right formula.
        w, i = a
        unit, g = ("", 0), ("", 1)
        out = {(unit, unit): 1}
        for letter in w:
            x = (letter, 0)
            generator = {(x, unit): 1, (g if letter == "o" else unit, x): 1}
            out = self.tensor_product_b(out, generator)
        if i:
            out = self.tensor_product_b(out, {(g, g): 1})
        return out

    def generator_antipode(self, a):
        # Independent anti-algebra expansion from S(e)=-e, S(o)=og, S(g)=g.
        w, i = a
        current = ("", i)
        coefficient = 1
        for letter in w[::-1]:
            value = ("e", 0) if letter == "e" else ("o", 1)
            scalar = -1 if letter == "e" else 1
            c, current = self.b_mul(current, value)
            coefficient *= scalar * c
        return {current: coefficient % self.p}

    def tensor_product_b(self, a, b):
        # Ordinary tensor product: component products introduce their own
        # bosonized signs, but there is no additional Koszul tensor sign.
        out = {}
        for (a1, a2), ca in a.items():
            for (b1, b2), cb in b.items():
                c1, ab1 = self.b_mul(a1, b1)
                c2, ab2 = self.b_mul(a2, b2)
                self.add(out, (ab1, ab2), ca * cb * c1 * c2)
        return out

    def tensor_product_h(self, a, b, graded=True):
        out = {}
        for (u1, u2), ca in a.items():
            for (v1, v2), cb in b.items():
                c = sign(parity(u2) * parity(v1)) if graded else 1
                self.add(out, (u1 + v1, u2 + v2), ca * cb * c)
        return out

    def iterated_delta(self, a, bosonized, side):
        delta = self.b_delta if bosonized else self.h_delta
        out = {}
        for (u, v), c in delta(a).items():
            if side == "left":
                for (u1, u2), c2 in delta(u).items():
                    self.add(out, (u1, u2, v), c * c2)
            else:
                for (v1, v2), c2 in delta(v).items():
                    self.add(out, (u, v1, v2), c * c2)
        return out

    def counit(self, a, bosonized, side):
        delta = self.b_delta if bosonized else self.h_delta
        out = {}
        for (u, v), c in delta(a).items():
            evaluated, retained = (u, v) if side == "left" else (v, u)
            w = evaluated[0] if bosonized else evaluated
            if not w:
                self.add(out, retained, c)
        return out

    def convolution(self, a, bosonized, side, bad=False):
        delta = self.b_delta(a, bad) if bosonized else self.h_delta(a)
        antipode = self.b_s if bosonized else self.h_s
        out = {}
        for (u, v), c in delta.items():
            if side == "left":
                cs, u = antipode(u)
            else:
                cs, v = antipode(v)
            if bosonized:
                cm, uv = self.b_mul(u, v)
            else:
                cm, uv = 1, u + v
            self.add(out, uv, c * cs * cm)
        return out


def printable(expression):
    return [{"basis": k, "coefficient": c}
            for k, c in sorted(expression.items())]


def run(p):
    a = Algebra(p)
    counts = Counter()

    def equal(label, lhs, rhs):
        counts[label] += 1
        if lhs != rhs:
            raise AssertionError((p, label, printable(lhs), printable(rhs)))

    h6, h4, h3 = words(6), words(4), words(3)
    b6 = [(w, i) for w in h6 for i in (0, 1)]
    b4 = [(w, i) for w in h4 for i in (0, 1)]
    b3 = [(w, i) for w in h3 for i in (0, 1)]
    unit = ("", 0)
    for w in h6:
        equal("H_coassociativity", a.iterated_delta(w, False, "left"),
              a.iterated_delta(w, False, "right"))
        target = {"": 1} if not w else {}
        for side in ("left", "right"):
            equal("H_counit_" + side, a.counit(w, False, side), {w: 1})
            equal("H_antipode_" + side,
                  a.convolution(w, False, side), target)
    for x in b6:
        equal("B_unit_left", {a.b_mul(unit, x)[1]: a.b_mul(unit, x)[0] % p}, {x: 1})
        equal("B_unit_right", {a.b_mul(x, unit)[1]: a.b_mul(x, unit)[0] % p}, {x: 1})
        equal("B_coassociativity", a.iterated_delta(x, True, "left"),
              a.iterated_delta(x, True, "right"))
        equal("B_independent_generator_delta", a.b_delta(x), a.generator_delta(x))
        c_s, sx = a.b_s(x)
        equal("B_independent_generator_antipode", {sx: c_s % p},
              a.generator_antipode(x))
        target = {unit: 1} if not x[0] else {}
        for side in ("left", "right"):
            equal("B_counit_" + side, a.counit(x, True, side), {x: 1})
            equal("B_antipode_" + side,
                  a.convolution(x, True, side), target)
    for u in h4:
        for v in h4:
            equal("H_graded_delta_multiplicativity", a.h_delta(u + v),
                  a.tensor_product_h(a.h_delta(u), a.h_delta(v)))
            if p == 2:
                equal("H_char2_ordinary_delta_multiplicativity", a.h_delta(u + v),
                      a.tensor_product_h(a.h_delta(u), a.h_delta(v), graded=False))
            c_uv, s_uv = a.h_s(u + v)
            c_u, s_u = a.h_s(u)
            c_v, s_v = a.h_s(v)
            equal("H_graded_antipode_antimultiplicativity", {s_uv: c_uv % p},
                  {s_v + s_u: c_u * c_v * sign(parity(u) * parity(v)) % p})
    max_binary_output_length = 0
    for x in b4:
        for y in b4:
            cxy, xy = a.b_mul(x, y)
            max_binary_output_length = max(max_binary_output_length, len(xy[0]))
            equal("B_delta_multiplicativity", a.scale(a.b_delta(xy), cxy),
                  a.tensor_product_b(a.b_delta(x), a.b_delta(y)))
            equal("B_counit_multiplicativity", {"scalar": (cxy * (not xy[0])) % p},
                  {"scalar": int(not x[0] and not y[0])})
            c_sxy, sxy = a.b_s(xy)
            c_sx, sx = a.b_s(x)
            c_sy, sy = a.b_s(y)
            c_rev, rev = a.b_mul(sy, sx)
            equal("B_antipode_antimultiplicativity", {sxy: cxy * c_sxy % p},
                  {rev: c_sx * c_sy * c_rev % p})
    max_triple_output_length = 0
    for x in b3:
        for y in b3:
            for z in b3:
                cxy, xy = a.b_mul(x, y)
                c_left, xyz_left = a.b_mul(xy, z)
                cyz, yz = a.b_mul(y, z)
                c_right, xyz_right = a.b_mul(x, yz)
                max_triple_output_length = max(max_triple_output_length, len(xyz_left[0]))
                equal("B_associativity", {xyz_left: cxy * c_left % p},
                      {xyz_right: cyz * c_right % p})

    # An explicit odd-odd control, predicted in reconstruction.md before coding.
    odd = ("o", 0)
    c_square, square = a.b_mul(odd, odd)
    bad_multiplicativity_residual = a.difference(
        a.scale(a.b_delta(square, bad=True), c_square),
        a.tensor_product_b(a.b_delta(odd, bad=True), a.b_delta(odd, bad=True)))
    expected_residual = {} if p == 2 else {(("o", 0), ("o", 0)): (-2) % p}
    equal("negative_control_expected_multiplicativity_residual",
          bad_multiplicativity_residual, expected_residual)
    bad_antipode_left = a.convolution(odd, True, "left", bad=True)
    bad_antipode_right = a.convolution(odd, True, "right", bad=True)
    expected_antipode_residual = {("o", 0): 1, ("o", 1): 1}
    equal("negative_control_expected_antipode_left_residual",
          bad_antipode_left, expected_antipode_residual)
    equal("negative_control_expected_antipode_right_residual",
          bad_antipode_right, expected_antipode_residual)
    assert bool(bad_multiplicativity_residual) == (p != 2)
    assert bad_antipode_left and bad_antipode_right
    assert max_binary_output_length == 8 and max_triple_output_length == 9
    # Sanity checks that the model did not silently impose an exterior relation
    # or commute the even and odd letters.
    assert square == ("oo", 0) and square != unit
    assert a.b_mul(("e", 0), odd)[1] != a.b_mul(odd, ("e", 0))[1]
    return {
        "field": f"F_{p}", "status": "PASS", "checks": dict(sorted(counts.items())),
        "total_equalities": sum(counts.values()),
        "max_binary_output_word_length": max_binary_output_length,
        "max_associativity_output_word_length": max_triple_output_length,
        "negative_control": {
            "mutation": "omit parity(v) in left group exponent of Delta_B",
            "input": ["o", 0],
            "multiplicativity_residual_left_minus_right": printable(bad_multiplicativity_residual),
            "antipode_left_residual": printable(bad_antipode_left),
            "antipode_right_residual": printable(bad_antipode_right),
            "multiplicativity_detection_expected": p != 2,
            "antipode_detection_expected": True,
        },
    }


def main():
    started = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()
    result = {
        "started_utc": started,
        "model": "infinite free associative graded Hopf algebra on e even, o odd",
        "arithmetic": "exact integer coefficient operations reduced modulo field characteristic",
        "bounds": {"unary_word_length": 6, "binary_each_word_length": 4,
                   "associativity_each_word_length": 3},
        "input_basis_counts": {"H_unary": 127, "B_unary": 254,
                               "H_binary_each": 31, "B_binary_each": 62,
                               "B_associativity_each": 30},
        "output_truncation": False,
        "fields": [run(p) for p in (2, 3, 5)],
        "limitations": "Finite basis tests support conventions only; no infinite theorem or topological claim is certified.",
    }
    result["completed_utc"] = datetime.now(timezone.utc).isoformat()
    result["elapsed_seconds"] = round(time.perf_counter() - start, 6)
    result["checker_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["total_equalities"] = sum(f["total_equalities"] for f in result["fields"])
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
