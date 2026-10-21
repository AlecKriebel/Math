#!/usr/bin/env python3
"""Exact finite controls for the Agugliaro literature implication.

These controls do not prove the CM existence or Hodge comparison theorems.
They check the elementary arithmetic, representation, and group steps of REPORT.md.
Python 3 standard library only. No network or repository mutation.
"""
from fractions import Fraction
from itertools import combinations, product
from math import prod
import argparse
import json
from pathlib import Path


def trim(a):
    a = list(a)
    while len(a) > 1 and not a[-1]:
        a.pop()
    return a


def mul(a, b, p=None):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return trim([x % p for x in c] if p else c)


def rem(a, b, p):
    a, b = trim([x % p for x in a]), trim([x % p for x in b])
    while a != [0] and len(a) >= len(b):
        k = len(a) - len(b)
        v = a[-1] * pow(b[-1], -1, p) % p
        for j, x in enumerate(b):
            a[j + k] = (a[j + k] - v * x) % p
        a = trim(a)
    return a


def sub(a, b, p):
    return trim([((a[i] if i < len(a) else 0) -
                  (b[i] if i < len(b) else 0)) % p
                 for i in range(max(len(a), len(b)))])


def gcd_poly(a, b, p):
    while b != [0]:
        a, b = b, rem(a, b, p)
    inv = pow(a[-1], -1, p)
    return [(x * inv) % p for x in a]


def powmod(a, k, f, p):
    out = [1]
    while k:
        if k & 1:
            out = rem(mul(out, a, p), f, p)
        a = rem(mul(a, a, p), f, p)
        k //= 2
    return out


def prime_factors(n):
    return [d for d in range(2, n + 1)
            if n % d == 0 and all(d % e for e in range(2, d))]


def irreducible(f, p):
    n = len(f) - 1
    x = [0, 1]
    if sub(powmod(x, p ** n, f, p), x, p) != [0]:
        return False
    return all(gcd_poly(f, sub(powmod(x, p ** (n // d), f, p), x, p), p)
               == [1] for d in prime_factors(n))


def first_irreducible(n, p):
    for a in product(range(p), repeat=n):
        if a[0] and irreducible(list(a) + [1], p):
            return list(a) + [1]
    raise AssertionError("Irreducible polynomial not found")


def trial_irreducible(f, p):
    """Separate small-degree control: trial every possible monic proper factor.

    This deliberately does not call the Rabin test, gcd, powmod, or rem above.
    """
    for d in range(1, (len(f) - 1) // 2 + 1):
        for coeff in product(range(p), repeat=d):
            divisor = list(coeff) + [1]
            a = [x % p for x in f]
            for k in reversed(range(len(a) - d)):
                lead = a[k + d]
                for j in range(d + 1):
                    a[k + j] = (a[k + j] - lead * divisor[j]) % p
            if all(x == 0 for x in a[:d]):
                return False
    return True


def rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][c]
        a[r] = [x / v for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                v = a[i][c]
                a[i] = [x - v * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def orbit(g, plus):
    return [tuple(1 if i in ix else -1 for i in range(g))
            for ix in combinations(range(g), plus)]


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def generated(gens):
    identity = tuple(range(len(gens[0])))
    seen, todo = {identity}, [identity]
    while todo:
        h = todo.pop()
        for s in gens:
            sh = compose(s, h)
            if sh not in seen:
                seen.add(sh)
                todo.append(sh)
    return seen


def cycle(n, indices):
    a = list(range(n))
    for i, j in zip(indices, indices[1:] + indices[:1]):
        a[i] = j
    return tuple(a)


def eval_poly(a, x):
    out = 0
    for c in reversed(a):
        out = out * x + c
    return out


def field_witness():
    # R = Q[X]/P. Absolute degree 6; p=3; Q0=Q(i).
    f3 = first_irreducible(6, 3)
    f11 = first_irreducible(5, 11)
    f13 = first_irreducible(2, 13)
    target = {3: f3, 11: mul([0, 1], f11, 11)}
    target[13] = f13
    for j in range(4):
        target[13] = mul(target[13], [-j, 1], 13)
    modulus = prod(target)
    base, spacing = [1], 1_000_000
    for j in range(1, 7):
        base = mul(base, [-j * spacing, 1])
    p = base[:]
    for k in range(6):
        delta = sum(((target[q][k] - base[k]) % q) * (modulus // q) *
                    pow(modulus // q, -1, q) for q in target) % modulus
        if delta > modulus // 2:
            delta -= modulus
        p[k] += delta
    assert all([c % q for c in p] == target[q] for q in target)
    # Exact intermediate-value isolation at 12 integral endpoints.
    intervals = []
    for j in range(1, 7):
        lo, hi = j * spacing - spacing // 4, j * spacing + spacing // 4
        a, b = eval_poly(p, lo), eval_poly(p, hi)
        assert a * b < 0
        intervals.append({"left": lo, "right": hi,
                          "left_sign": 1 if a > 0 else -1,
                          "right_sign": 1 if b > 0 else -1})
    # The stated factors are squarefree: irreducible factors have degree > 1,
    # and the explicit linear factors have distinct roots.
    assert irreducible(f3, 3) and irreducible(f11, 11) and irreducible(f13, 13)
    assert trial_irreducible(f3, 3) and trial_irreducible(f11, 11)
    assert trial_irreducible(f13, 13)
    assert irreducible([1, 0, 1], 3)  # Q(i) is inert at 3.
    reducible_control = mul([1, 1, 1], [2, 0, 0, 0, 1], 3)
    assert not irreducible(reducible_control, 3)
    assert not trial_irreducible(reducible_control, 3)
    return {"coefficient_order": "constant first", "polynomial": p,
            "p": 3, "imaginary_quadratic": "Q(i)",
            "mod_3_irreducible_degree_6": f3,
            "mod_11_irreducible_degree_5": f11,
            "mod_13_irreducible_degree_2": f13,
            "factor_types": {"3": [6], "11": [5, 1], "13": [2, 1, 1, 1, 1]},
            "irreducibility_controls": "Rabin and separate exhaustive trial division; reducible negative fixture rejected",
            "isolating_intervals": intervals}


def run():
    results = {"schema": "pr799-agugliaro-adversarial-controls-v1"}
    ranks = []
    for g in (4, 6, 8):
        o = orbit(g, g // 2 + 1)
        assert rank(o) == g
        ranks.append({"g": g, "signature_sum": 2, "orbit_size": len(o), "rank": rank(o)})
    # These controls reject both unjustified shortcuts about sign vectors.
    assert rank(orbit(6, 3)) == 5
    assert rank(orbit(6, 6)) == 1
    assert rank(orbit(2, 2)) == 1
    results["sign_orbit_ranks"] = ranks
    results["negative_sign_controls"] = {"g6_balanced_rank": 5,
                                          "g6_constant_rank": 1,
                                          "g2_sum2_constant_rank": 1}
    local = []
    for g in (4, 6, 8):
        # In the fixed Q0 block, exactly g/2 embeddings have low slope.
        # Choosing one low-slope embedding globally fixes all conjugate choices.
        for chosen_low in range(g):
            first_block_selected = sum((i == chosen_low) if i < g // 2
                                       else (i != chosen_low) for i in range(g))
            signature_sum = 2 * first_block_selected - g
            assert abs(signature_sum) == 2
            local.append({"g": g, "unique_low_choice": chosen_low,
                          "first_block_h10": first_block_selected,
                          "signature_sum": signature_sum})
    results["local_to_global_signature_checks"] = local
    o = orbit(6, 4)
    tested = 0
    for d in product(range(-2, 3), repeat=6):
        orthogonal = all(sum(x * y for x, y in zip(d, s)) == 0 for s in o)
        assert orthogonal == (d == (0,) * 6)
        tested += 1
    results["weight_relation_control"] = {"vectors_tested": tested,
                                           "only_common_orthogonal_vector": [0] * 6}
    c6 = cycle(6, list(range(6)))
    t03 = cycle(6, [0, 3])
    c5 = cycle(6, [1, 2, 3, 4, 5])
    bad = len(generated([c6, t03]))
    repaired = len(generated([c6, t03, c5]))
    assert bad == 24 and repaired == 720
    results["group_controls"] = {"six_cycle_plus_opposite_transposition_order": bad,
                                  "with_five_cycle_order": repaired,
                                  "S6_order": 720}
    results["field_witness"] = field_witness()
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--compare", type=Path)
    args = parser.parse_args()
    result = run()
    if args.compare:
        assert result == json.loads(args.compare.read_text()), "Results changed"
        print("PASS: all exact controls; stored results reproduced")
    elif args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("PASS: all exact controls; wrote", args.output)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
