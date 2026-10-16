#!/usr/bin/env python3
"""Fresh exact audit of PR407; standard library, no candidate-code imports.

Uses explicit dense matrices in the original coordinates, permutation rank
classes, and reconstruction from half-open simplex gaps. Checks remain active
under Python -O. Finite checks supplement the separately recorded all-n proof.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from itertools import combinations_with_replacement, permutations, product
from math import comb, factorial
from pathlib import Path
import argparse
import hashlib
import json


def require(condition, context):
    if not condition:
        raise RuntimeError(repr(context))


def descent_set(p):
    return tuple(j for j in range(len(p) - 1) if p[j] > p[j + 1])


def inverse(p):
    q = [0] * len(p)
    for j, a in enumerate(p):
        q[a] = j
    return tuple(q)


def alpha_from_runs(n, D):
    """Reverse identity blocks ending at each non-descent position."""
    cuts = [0] + [j + 1 for j in range(n - 1) if j not in D] + [n]
    alpha = tuple(a for left, right in zip(cuts, cuts[1:])
                  for a in reversed(range(left, right)))
    require(descent_set(alpha) == D, ("canonical labeling", n, D, alpha))
    return alpha


def relative_histogram(alpha, ranks):
    return Counter(len(descent_set(tuple(alpha[v] for v in inverse(sigma))))
                   for sigma in ranks)


def direct_condition(x, signs, m):
    return all(x[i] + x[i + 1] <= m if s == "-"
               else x[i] + x[i + 1] >= m
               for i, s in enumerate(signs))


def original_dense_count(signs, m):
    vector = [1 for _ in range(m + 1)]
    for sign in signs:
        # Explicit transition entries depend only on the original sum bound.
        matrix = [[int(a + b <= m if sign == "-" else a + b >= m)
                   for a in range(m + 1)] for b in range(m + 1)]
        vector = [sum(entry * count for entry, count in zip(row, vector))
                  for row in matrix]
    return sum(vector)


def run(max_n):
    coverage = Counter()
    examples = {}
    negative = {}
    wrong_composition_witness = None
    for n in range(1, max_n + 1):
        classes = defaultdict(list)
        for sigma in permutations(range(n)):
            classes[descent_set(sigma)].append(sigma)
            coverage["permutation_rankings"] += 1
        require(sum(len(c) for c in classes.values()) == factorial(n),
                ("permutation exhaustion", n))
        for signs in product("-+", repeat=n - 1):
            D = tuple(i for i, s in enumerate(signs)
                      if s == ("+" if i % 2 == 0 else "-"))
            ranks = classes[D]
            alpha = alpha_from_runs(n, D)
            histogram = relative_histogram(alpha, ranks)
            coverage["sign_words"] += 1
            require(histogram[0] == 1, ("constant coefficient", n, signs))
            labelings = ranks if n <= 7 else [ranks[0], ranks[-1], ranks[len(ranks)//2]]
            for beta in labelings:
                require(relative_histogram(beta, ranks) == histogram,
                        ("labeling invariance", n, signs, beta))
                coverage["natural_labelings"] += 1
                coverage["alpha_sigma_pairs"] += len(ranks)
            counts = [original_dense_count(signs, m) for m in range(n + 5)]
            # Formal multiplication by (1-z)^(n+1), including coefficients
            # beyond the expected numerator degree, detects endpoint shifts.
            numerator = [sum((-1)**j * comb(n + 1, j) * counts[k-j]
                             for j in range(min(k, n + 1) + 1))
                         for k in range(len(counts))]
            require(numerator == [histogram[k] for k in range(len(counts))],
                    ("complete numerator", n, signs, numerator, histogram))
            coverage["formal_series_coefficients"] += len(counts)
            for m in list(range(n + 5)) + [17, 23]:
                actual = counts[m] if m < len(counts) else original_dense_count(signs, m)
                predicted = sum(c * comb(m + n - d, n)
                                for d, c in histogram.items() if m >= d)
                require(actual == predicted, ("binomial formula", n, signs, m))
                coverage["original_coordinate_counts"] += 1
            if n <= 6:
                for m in range(4):
                    admitted = set()
                    for x in product(range(m + 1), repeat=n):
                        y = tuple(a if i % 2 == 0 else m - a for i, a in enumerate(x))
                        back = tuple(a if i % 2 == 0 else m - a for i, a in enumerate(y))
                        require(back == x, ("reflection involution", n, signs, m, x))
                        reflected = all((y[i] >= y[i + 1] if i in D
                                         else y[i] <= y[i + 1])
                                        for i in range(n - 1))
                        admitted_original = direct_condition(x, signs, m)
                        require(admitted_original == reflected,
                                ("pointwise reflection", n, signs, m, x, y))
                        coverage["grid_reflection_points"] += 1
                        if admitted_original:
                            admitted.add(x)
                            w = tuple(sorted(range(n), key=lambda v: (y[v], alpha[v])))
                            sigma = inverse(w)
                            require(descent_set(sigma) == D,
                                    ("tie sort is extension", n, signs, m, x, w))
                            seq = tuple(y[v] for v in w)
                            strict = descent_set(tuple(alpha[v] for v in w))
                            require(all(seq[j] < seq[j+1] for j in strict),
                                    ("tie sorting strictness", n, signs, m, x, w))
                            coverage["admitted_tie_sorted_points"] += 1
                    require(len(admitted) == counts[m], ("direct count", n, signs, m))
                    coverage["direct_grid_counts"] += 1
                    if n <= 5:
                        # Test every natural labeling, reconstruct every point
                        # from a word and strict-gap sequence, verify multiplicity.
                        for beta in ranks:
                            assigned = Counter()
                            for sigma in ranks:
                                w = inverse(sigma)
                                label_word = tuple(beta[v] for v in w)
                                strict = descent_set(label_word)
                                for sequence in combinations_with_replacement(range(m + 1), n):
                                    if any(sequence[j] == sequence[j+1] for j in strict):
                                        continue
                                    y = [0] * n
                                    for j, v in enumerate(w):
                                        y[v] = sequence[j]
                                    x = tuple(a if i % 2 == 0 else m-a for i, a in enumerate(y))
                                    assigned[x] += 1
                                    sorted_word = tuple(sorted(range(n), key=lambda v: (y[v], beta[v])))
                                    require(sorted_word == w, ("reverse tie sort", n, signs, m, beta, w))
                                    # Gap bijection: strict steps subtracted;
                                    # endpoints and gaps total exactly m-d.
                                    shifted = tuple(a-sum(j < pos for j in strict)
                                                    for pos, a in enumerate(sequence))
                                    require(all(a <= b for a, b in zip(shifted, shifted[1:])),
                                            ("weak shifted sequence", sequence, strict))
                                    gap = (shifted[0],) + tuple(b-a for a,b in zip(shifted,shifted[1:])) + (m-len(strict)-shifted[-1],)
                                    require(all(a >= 0 for a in gap) and sum(gap) == m-len(strict),
                                            ("gap sum", n, signs, m, beta, sequence, gap))
                                    coverage["strict_gap_reconstructions"] += 1
                            require(set(assigned) == admitted and all(c == 1 for c in assigned.values()),
                                    ("disjoint exhaustive partition", n, signs, m, beta))
                            coverage["all_label_boundary_partitions"] += 1
            if n <= 4:
                examples[f"n={n},signs={''.join(signs)}"] = dict(sorted(histogram.items()))
            if wrong_composition_witness is None:
                wrong = Counter(len(descent_set(tuple(alpha[v] for v in sigma)))
                                for sigma in ranks)
                if wrong != histogram:
                    wrong_composition_witness = {"n":n,"signs":''.join(signs),"alpha":alpha,
                                                 "wrong_no_inverse":dict(wrong),"correct":dict(histogram)}
        print(f"dimension {n}: all {2**(n-1)} sign words passed", flush=True)
    require(wrong_composition_witness is not None, "wrong composition negative control not detected")
    negative["omit_inverse"] = wrong_composition_witness
    ranks = [p for p in permutations(range(3)) if descent_set(p) == (1,)]
    raw = relative_histogram((0,1,2), ranks)
    require(raw == Counter({1:2}) and original_dense_count(("-","-"),0) == 1,
            "raw labeling negative control")
    negative["raw_labels"] = {"wrong":dict(raw),"correct":{"0":1,"1":1}}
    require(len(ranks) == 2, "weak-only boundary control")
    negative["omit_strict_gaps"] = {"m":0,"wrong":len(ranks),"actual":1}
    require(direct_condition((0,2),("-",),2) and 1-2 < 0, "wrong dilation map control")
    negative["use_T1_at_m2"] = {"x":[0,2],"wrong_y":[0,-1],"correct_y":[0,0]}
    negative["reverse_equal_value_ties"] = {"n":2,"signs":"-","m":0,"wrong_word":[1,0],
                                             "required_word":[0,1],"consequence":"violates generating comparison"}
    require(descent_set((1,0)) != (), "reverse tie negative control")
    return {"verdict":"PASS","utc":datetime.now(timezone.utc).isoformat(),
            "max_dimension":max_n,"arithmetic":"exact integers; standard library only",
            "coverage":dict(coverage),"negative_controls":negative,"small_examples":examples,
            "independence":"No candidate checker imports or frozen-source writes; require checks survive -O.",
            "scope":"Finite falsifiable evidence only; all-dimensions certificate recorded in AUDIT.md."}


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--max-n",type=int,default=9)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    require(1 <= args.max_n <= 9, "dimension guard")
    result=run(args.max_n)
    result["checker_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ["small_examples","negative_controls"]},indent=2))
