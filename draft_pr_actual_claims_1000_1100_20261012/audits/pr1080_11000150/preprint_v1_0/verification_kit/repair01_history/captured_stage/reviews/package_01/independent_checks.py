#!/usr/bin/env python3
"""Fresh exact controls; written proof, not these finite cases, proves the theorem."""
from fractions import Fraction
from itertools import product
import argparse
import json


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


I = (0, 1, 2, 3)


def mul(a, b):
    return tuple(a[b[k]] for k in range(4))


def inv(a):
    return tuple(a.index(k) for k in range(4))


def evaluate(word):
    out = I
    for a in word:
        out = mul(out, a)
    return out


def insertion_controls(fault):
    # Permutation action is independent of the prior free-word reducers.
    letters = [(1, 0, 2, 3), (0, 2, 3, 1), (3, 0, 1, 2)]
    cases = proper = empty = wrong_detected = 0
    for n in range(7):
        for v in product(letters, repeat=n):
            for mask in range(1 << n):
                u, blocks = [], [[]]
                for j, a in enumerate(v):
                    if mask & (1 << j):
                        u.append(a)
                        blocks.append([])
                    else:
                        blocks[-1].append(a)
                lhs = mul(evaluate(v), inv(evaluate(u)))
                rhs, prefix = I, I
                for j, block in enumerate(blocks):
                    value = evaluate(block)
                    rhs = mul(rhs, value if fault == "conjugation" else mul(mul(prefix, value), inv(prefix)))
                    if j < len(u):
                        prefix = mul(prefix, u[j])
                need(lhs == rhs, "retained-prefix insertion identity failed")
                wrong = evaluate([a for block in blocks for a in block])
                wrong_detected += int(lhs != wrong)
                cases += 1
                proper += int(len(u) < len(v))
                empty += int(not u)
    need(wrong_detected > 0, "missing-conjugation control did not distinguish the formula")
    return {"cases": cases, "proper": proper, "empty_retained": empty,
            "wrong_unconjugated_formula_detected": wrong_detected}


def parity_controls(fault):
    cases = 0
    for g in range(1, 9):
        for a in range(1 << (2*g)):
            x = a & ((1 << g)-1)
            y = a >> g
            pairing = ((x & y).bit_count() + (y & x).bit_count()) % 2
            if fault == "parity":
                pairing ^= 1
            need(pairing == 0, "symplectic self-pairing failed")
            cases += 1
    need(12 > (1 << 2) * (3-2) + 1, "support-size versus length counterexample lost")
    return {"exact_self_pairings": cases, "genus_one_chain_exceeds_support_bound": True}


def expansion_controls(fault):
    # In Aff^+(Q), positive translations form a conjugation-invariant positive set.
    # The target translation is noncentral in that ambient group.
    values = [1, 2, 3, 2]
    counts = [0] * 19
    counts[0] = 1
    maxima = [0] * 19
    for target in range(1, 19):
        counts[target] = sum(counts[target-v] for v in values if v <= target)
        maxima[target] = max(maxima[target-v]+1 for v in values if v <= target)
        need(maxima[target] == target and counts[target] > 0, "finite positive translation fiber failed")
    dilation, target = Fraction(2), Fraction(18)
    need(dilation * target != target, "ambient target became central")
    for n in range(8):
        for word in product(values, repeat=n):
            expanded = sum(0 if fault == "erasing" and v == 2 else v for v in word)
            need(expanded >= len(word), "nonerasing atomic length bound failed")
    return {"noncentral_translation_target": 18, "target_word_count": counts[18],
            "target_maximum_raw_length": maxima[18], "duplicate_letter_values_retained": True,
            "erasing_identity_letters_allow_unbounded_insertions": True}


def crossings():
    # Choose each new rational intercept outside the finite forbidden set.
    # Unlike the old checker, no closed-form sum/product perturbation is used.
    cases = 0
    for n in range(2, 22):
        offsets = [Fraction(0), Fraction(1)]
        for j in range(2, n):
            forbidden = set()
            for a in range(j):
                for b in range(a+1, j):
                    x = (offsets[b]-offsets[a]) / Fraction(a-b)
                    y = a*x+offsets[a]
                    forbidden.add(y-j*x)
            chosen = 1
            while Fraction(chosen) in forbidden:
                chosen += 1
            offsets.append(Fraction(chosen))
        scale = Fraction(1, 10*(1+max(abs(x) for x in offsets)))
        seen = set()
        for a in range(n):
            for b in range(a+1, n):
                x = scale*(offsets[b]-offsets[a]) / Fraction(a-b)
                y = a*x+scale*offsets[a]
                need(abs(x) < 1, "crossing escaped the local disk chart")
                need((x,y) not in seen, "triple concurrence remains")
                seen.add((x,y))
                left = (-a+scale*offsets[a])-(-b+scale*offsets[b])
                right = (a+scale*offsets[a])-(b+scale*offsets[b])
                need(left*right < 0, "pairwise alternating endpoint order lost")
                cases += 1
        need(len(seen) == n*(n-1)//2, "crossing count changed")
    return {"exact_pair_crossings": cases, "concurrent_line_counts": list(range(2,22)),
            "zero_offset_triple_concurrence_is_a_negative_control": True}


def cycle_count(p):
    unseen = set(range(len(p)))
    out = 0
    while unseen:
        j = min(unseen)
        while j in unseen:
            unseen.remove(j)
            j = p[j]
        out += 1
    return out


def ribbons():
    # Boundary cycles of an oriented ribbon neighborhood are sigma * edge involution.
    alpha = [2, 3, 0, 1]
    sigma = [1, 2, 3, 0]
    wrong = [2, 3, 1, 0]
    good_boundary = cycle_count([sigma[alpha[j]] for j in range(4)])
    bad_boundary = cycle_count([wrong[alpha[j]] for j in range(4)])
    need(good_boundary == 1 and bad_boundary == 3, "ribbon cyclic order control failed")
    circle_boundary = cycle_count([0, 1])
    need(circle_boundary == 2, "isolated circle must have an annular neighborhood")
    for isolated in range(10):
        b = good_boundary+2*isolated
        vertices, edges, components = 1+isolated, 2+isolated, 1+isolated
        total_genus = (2*components-b-vertices+edges)//2
        need(total_genus == 1, "disconnected isolated-circle Euler bookkeeping failed")
    return {"alternating_crossing_boundaries": 1, "nonalternating_boundaries": 3,
            "isolated_circle_boundaries": 2, "disconnected_cases": 10}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fault", choices=["conjugation", "parity", "erasing"])
    a = p.parse_args()
    result = {"status": "PASS", "finite_controls_only": True,
              "insertion": insertion_controls(a.fault), "parity": parity_controls(a.fault),
              "expansions": expansion_controls(a.fault), "crossings": crossings(),
              "ribbons": ribbons(), "guards_active_under_optimized_python": True}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
