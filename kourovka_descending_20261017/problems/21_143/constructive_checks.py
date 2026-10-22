#!/usr/bin/env python3
"""Exact, finite sanity checks for constructive-route obstruction families.

This is not an automaticity decision procedure.  Proofs of the universal
claims are in approach_constructive.md.  No floating-point arithmetic is used.
Run: python3 constructive_checks.py
"""

from bisect import bisect_right
from datetime import datetime, timezone
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import re


def canonical(points):
    points = sorted(set(points))
    out = []
    for p in points:
        out.append(p)
        while len(out) >= 3:
            (a, b), (c, d), (e, f) = out[-3:]
            if (d - b) * (e - c) != (f - d) * (c - a):
                break
            out.pop(-2)
    return tuple(out)


def evaluate(f, t):
    i = max(0, min(len(f) - 2, bisect_right([p[0] for p in f], t) - 1))
    (a, b), (c, d) = f[i:i + 2]
    return b + (t - a) * (d - b) / (c - a)


def inverse(f):
    return tuple((b, a) for a, b in f)


def compose(f, g):
    """Return f after g, i.e. f(g(t))."""
    gi = inverse(g)
    cuts = {a for a, _ in g} | {evaluate(gi, a) for a, _ in f}
    return canonical((t, evaluate(f, evaluate(g, t))) for t in cuts)


IDENTITY = ((Q(0), Q(0)), (Q(1), Q(1)))
X0 = tuple((Q(a), Q(b)) for a, b in [
    (0, 0), (Q(1, 2), Q(1, 4)), (Q(3, 4), Q(1, 2)), (1, 1)])
X1 = tuple((Q(a), Q(b)) for a, b in [
    (0, 0), (Q(1, 2), Q(1, 2)), (Q(3, 4), Q(5, 8)),
    (Q(7, 8), Q(3, 4)), (1, 1)])
GENERATORS = {"x": X0, "X": inverse(X0), "y": X1, "Y": inverse(X1)}


def word_map(word):
    """Composition convention: f_(uv) = f_u after f_v.

    Algebraic right multiplication remains concatenation of words.  This
    convention is selected by checking the stated finite presentation.
    """
    ans = IDENTITY
    for a in word:
        ans = compose(ans, GENERATORS[a])
    return ans


def nf_member(word):
    if re.search(r"xX|Xx|yY|Yy", word):
        return False
    return re.search(r"[yY]x+y|[yY]xx+Y", word) is None


def abelian(word):
    return word.count("x") - word.count("X"), word.count("y") - word.count("Y")


def l1(u, v):
    return sum(abs(a - b) for a, b in zip(u, v))


def dyadic_depth(t):
    d = t.denominator
    assert d > 0 and d & (d - 1) == 0
    return d.bit_length() - 1


def max_break_depth(f):
    return max((dyadic_depth(a) for a, _ in f[1:-1]), default=0)


def infinite_generator(index):
    assert index >= 1
    return "X" * (index - 1) + "y" + "x" * (index - 1)


def asynchronous_quotient_distance(u, v):
    """Exact discrete monotone matching distance in the l1 quotient.

    This is a lower bound for the corresponding Cayley-graph matching
    distance.  Horizontal, vertical and diagonal steps are allowed.
    """
    up = [abelian(u[:i]) for i in range(len(u) + 1)]
    vp = [abelian(v[:j]) for j in range(len(v) + 1)]
    best = [[None] * len(vp) for _ in up]
    for i in range(len(up)):
        for j in range(len(vp)):
            cost = l1(up[i], vp[j])
            preds = []
            if i:
                preds.append(best[i - 1][j])
            if j:
                preds.append(best[i][j - 1])
            if i and j:
                preds.append(best[i - 1][j - 1])
            best[i][j] = max(cost, min(preds)) if preds else cost
    return best[-1][-1]


def main():
    assert all(compose(g, inverse(g)) == IDENTITY for g in GENERATORS.values())
    # Two standard finite defining relators, in the convention of the report.
    def inv(w):
        return w.swapcase()[::-1]
    def comm(a, b):
        return inv(a) + inv(b) + a + b
    relators = [comm("y", "xyXX"), comm("y", "xxyXXX")]
    assert all(word_map(r) == IDENTITY for r in relators)

    gs = []
    for n in range(1, 65):
        u = "y" + "x" * n
        v = "x" * n + "y" + "X" * (n + 1) + "y" + "x" * (n + 1)
        assert nf_member(u) and nf_member(v)
        assert word_map(u + "y") == word_map(v)
        assert len(v) - len(u) == 2 * n + 3
        assert l1(abelian(u), abelian(v[:2 * n + 3])) == n + 2
        row = {"n": n, "u_length": len(u), "v_length": len(v),
               "length_gap": len(v) - len(u), "synchronous_lower_bound": n + 2}
        if n <= 20:
            a = asynchronous_quotient_distance(u, v)
            assert 2 * a >= n + 2
            expected = 2 if n <= 2 else (n + 4) // 2
            assert a == expected
            row["exact_discrete_asynchronous_l1_distance"] = a
        gs.append(row)

    index = []
    for n in range(1, 65):
        # b^n -> b^n #^(n+1) b under right multiplication by y^-1.
        left = "X" * n + "Y"
        right = inv(infinite_generator(n + 1)) + "X" * n
        assert word_map(left) == word_map(right)
        index.append({"n": n, "u_symbol_length": n,
                      "v_symbol_length": 2 * n + 2, "length_gap": n + 2})

    depths = []
    for i in range(1, 65):
        f = word_map(infinite_generator(i))
        d = max_break_depth(f)
        assert d == i + 2
        depths.append({"index": i, "binary_index_length": i.bit_length(),
                       "expanded_word_length": 2 * i - 1,
                       "max_breakpoint_depth": d,
                       "generator_word_length_lower_bound": i})

    # Check the elementary point-depth estimate used in the proof on a grid.
    checked_points = 0
    for depth in range(1, 12):
        for k in range(1, 2 ** depth, 2):
            t = Q(k, 2 ** depth)
            for g in GENERATORS.values():
                assert dyadic_depth(evaluate(g, t)) <= depth + 1
                checked_points += 1

    # Exhaustive short words independently test the global breakpoint bound.
    short_words = 0
    for n in range(6):
        for letters in product("xXyY", repeat=n):
            w = "".join(letters)
            assert max_break_depth(word_map(w)) <= n + 2
            short_words += 1

    result = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "arithmetic": "fractions.Fraction; exact rational PL composition",
        "claim_scope": "finite checks of parametric formulas, not automaticity",
        "all_checks_passed": True,
        "finite_presentation_relators_checked": relators,
        "gs_family": gs,
        "unary_index_family": index,
        "binary_index_depth_family": depths,
        "dyadic_generator_point_checks": checked_points,
        "exhaustive_words_through_length_5": short_words,
    }
    target = Path(__file__).with_name("constructive_check_results.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"all_checks_passed": True, "output": str(target),
                      "gs_family_n": [1, 64], "index_family_n": [1, 64],
                      "depth_family_i": [1, 64], "point_checks": checked_points,
                      "short_words": short_words}, indent=2))


if __name__ == "__main__":
    main()
