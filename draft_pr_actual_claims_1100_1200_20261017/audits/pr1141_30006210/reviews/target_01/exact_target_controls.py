#!/usr/bin/env python3
"""Independent exact finite evidence, not a universal proof certificate.

Only Python's standard library is used. All mathematical comparisons use
integers or Fraction; no Python assert statement is used, so -O retains checks.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import platform
import sys


def require(condition, label):
    if not condition:
        raise RuntimeError("CONTROL FAILURE: " + label)


def evaluate(coefficients, masks, n):
    return tuple(sum(c * (-1 if (m & x).bit_count() % 2 else 1)
                     for c, m in zip(coefficients, masks))
                 for x in range(1 << n))


def normalized_influences(coefficients, masks, n, omit_constant=False):
    energy = sum(c*c for c, m in zip(coefficients, masks)
                 if not omit_constant or m != 0)
    if energy == 0:
        raise ValueError("nonzero full L2 norm is required")
    return tuple(Q(sum(c*c for c, m in zip(coefficients, masks) if m & (1 << i)),
                   energy) for i in range(n))


def square_resampling(values, i, flip_instead=False):
    energy_sum = sum(v*v for v in values)
    if not energy_sum:
        raise ValueError("nonzero full L2 norm is required")
    denominator = energy_sum * (1 if flip_instead else 2)
    return Q(sum(abs(v*v-values[x ^ (1 << i)]**2)
                 for x, v in enumerate(values)), denominator)


def endpoint_guards(mutation):
    masks = (0, 1)
    f, g = (1, 1), (1, -1)
    fv, gv = evaluate(f, masks, 1), evaluate(g, masks, 1)
    rho = normalized_influences(f, masks, 1,
                                omit_constant=mutation == "omit_constant")[0]
    require(rho == Q(1, 2), "full-mean denominator at d=1 endpoint")
    require(all(a*b == 0 for a, b in zip(fv, gv)), "endpoint disjointness")
    require(any(fv) and any(gv), "endpoint nonzeroness")
    a = square_resampling(fv, 0, flip_instead=mutation == "flip_resampling")
    require(a == 1, "resampling includes probability one-half of no change")
    require(a*a <= 4*rho*(1-rho), "square-density Fourier bound")
    if mutation == "nonstrict_old_endpoint":
        require(not (rho <= Q(1, 2) and all(a*b == 0 for a, b in zip(fv, gv))),
                "false nonstrict old endpoint rejected by explicit pair")
    try:
        normalized_influences((0, 0), masks, 1)
        rejected_zero = False
    except ValueError:
        rejected_zero = True
    if mutation == "accept_zero":
        rejected_zero = False
    require(rejected_zero, "zero polynomials cannot be normalized")
    constant = normalized_influences((7, 0), masks, 1)
    require(constant == (Q(0),), "nonzero constant has zero relative influence")
    # n=2, d=2: common zeros occupy one half of the cube.
    ff = (1, 1, 1, 1)  # (1+x1)(1+x2)
    gg = (1, -1, 1, -1)  # (1-x1)(1+x2)
    vm = (0, 1, 2, 3)
    ffv, ggv = evaluate(ff, vm, 2), evaluate(gg, vm, 2)
    union = sum(bool(a) or bool(b) for a, b in zip(ffv, ggv))
    require(union == 2, "common-zero boundary case")
    if mutation == "assume_partition":
        require(union == 4, "false assumption that disjoint supports cover cube")
    for d in (1, 2, 3, 17, 10**6):
        threshold, contrapositive = Q(1, 4096*d**8), Q(1, 1024*d**8)
        require(contrapositive == 4*threshold, "threshold strict slack")
        value_squared = 32**2 * d**8 * threshold
        if mutation == "constant_arithmetic":
            value_squared = 1
        require(value_squared == Q(1, 4), "final contradiction upper bound is 1/2")
    scales = (Q(-7, 3), Q(2, 11), Q(9))
    for scale in scales:
        sf = tuple(scale*c for c in f)
        require(normalized_influences(sf, masks, 1) == (Q(1, 2),),
                "nonzero real scaling invariance")
    return {"old_nonstrict_endpoint": "f=1+x1, g=1-x1, delta=1/2",
            "zero_normalization_rejected": True,
            "common_zero_fraction": "1/2",
            "exact_constant_checks_declared_d": [1, 2, 3, 17, 10**6]}


def coefficient_box(n, d):
    masks = tuple(m for m in range(1 << n) if m.bit_count() <= d)
    vertices = 1 << n
    groups = {}
    count = 0
    signed_count = 0
    max_l1_ratio = Q(0)
    for coefficients in itertools.product((-1, 0, 1), repeat=len(masks)):
        first = next((c for c in coefficients if c), 0)
        if first != 1:  # One representative modulo a global sign.
            continue
        count += 1
        energy = sum(c*c for c in coefficients)
        values = evaluate(coefficients, masks, n)
        require(sum(v*v for v in values) == vertices*energy, "Parseval exact")
        influences = normalized_influences(coefficients, masks, n)
        degree_weight = sum(m.bit_count()*c*c
                            for c, m in zip(coefficients, masks))
        require(sum(influences) == Q(degree_weight, energy),
                "Fourier total-influence identity")
        require(degree_weight <= d*energy, "degree-bound total influence")
        for i, rho in enumerate(influences):
            flip_square = sum((v-values[x ^ (1 << i)])**2
                              for x, v in enumerate(values))
            require(Q(flip_square, vertices*energy) == 4*rho,
                    "flip-energy and Fourier influence agree")
            plus_square = sum((v+values[x ^ (1 << i)])**2
                              for x, v in enumerate(values))
            require(Q(plus_square, vertices*energy) == 4*(1-rho),
                    "flip-sum energy includes constant coordinate")
            a = square_resampling(values, i)
            require(a*a <= 4*rho*(1-rho), "exact squared L1 bound")
            if rho and rho != 1:
                max_l1_ratio = max(max_l1_ratio, a*a/(4*rho*(1-rho)))
        support = sum(1 << x for x, v in enumerate(values) if v)
        require(support != 0, "nonzero Fourier vector has a nonempty support")
        delta = max(influences, default=Q(0))
        signed_count += min(values) < 0 < max(values)
        if support not in groups:
            groups[support] = {"count": 0, "delta": delta,
                               "coefficients": coefficients, "values": values}
        group = groups[support]
        group["count"] += 1
        if delta < group["delta"]:
            group.update(delta=delta, coefficients=coefficients, values=values)
    expected = (3**len(masks)-1)//2
    require(count == expected, "coefficient-box exhaustive count")
    unordered_support_pairs = 0
    unordered_poly_pairs = 0
    common_zero_pairs = 0
    min_delta = None
    witness = None
    full_support = (1 << vertices)-1
    mu_values = set()
    for sa, a in sorted(groups.items()):
        for sb, b in sorted(groups.items()):
            if sb < sa or sa & sb:
                continue
            unordered_support_pairs += 1
            unordered_poly_pairs += a["count"]*b["count"]
            common_zero_pairs += (sa | sb) != full_support
            pair_delta = max(a["delta"], b["delta"])
            require(pair_delta >= Q(1, 1024*d**8),
                    "claimed disjoint-support bound in finite coefficient box")
            require(pair_delta >= Q(1, 4*n*n),
                    "independent full-depth covariance bound")
            if d == 1:
                require(pair_delta == Q(1, 2), "affine classification endpoint")
            if min_delta is None or pair_delta < min_delta:
                min_delta = pair_delta
                witness = [list(a["coefficients"]), list(b["coefficients"])]
            # Choose h=1 on support(a), h=0 elsewhere, allowing common zeros.
            mu = Q(sa.bit_count(), vertices)
            afull = sum(x*x for x in a["values"])
            bfull = sum(x*x for x in b["values"])
            ehu = sum(Q(vertices*x*x, afull) for k, x in enumerate(a["values"])
                      if sa & (1 << k))/vertices
            ehv = sum(Q(vertices*x*x, bfull) for k, x in enumerate(b["values"])
                      if sa & (1 << k))/vertices
            require(ehu == 1 and ehv == 0, "separator multiplication identities")
            cov_u, cov_v = ehu-mu, ehv-mu
            require(abs(cov_u)+abs(cov_v) == 1,
                    "two covariance magnitudes sum to one with common zeros")
            mu_values.add(str(mu))
    require(unordered_support_pairs > 0, "nonvacuous disjoint-pair census")
    return {"n": n, "degree_bound": d, "coefficient_masks": masks,
            "coefficients": [-1, 0, 1], "sign_classes": count,
            "all_nonzero_coefficient_vectors": 2*count,
            "signed_value_sign_classes": signed_count,
            "distinct_nonempty_supports": len(groups),
            "unordered_disjoint_support_pairs": unordered_support_pairs,
            "unordered_disjoint_polynomial_sign_class_pairs": unordered_poly_pairs,
            "disjoint_support_pairs_with_common_zeros": common_zero_pairs,
            "minimum_pair_max_relative_influence": str(min_delta),
            "minimizer_coefficients_in_mask_order": witness,
            "max_squared_L1_bound_ratio": str(max_l1_ratio),
            "separator_means_seen": sorted(mu_values)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", choices=("omit_constant", "flip_resampling",
                        "nonstrict_old_endpoint", "accept_zero", "assume_partition",
                        "constant_arithmetic"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    guards = endpoint_guards(args.mutate)
    cases = [coefficient_box(n, d) for n, d in
             ((1, 1), (2, 1), (3, 1), (4, 1), (2, 2), (3, 2), (4, 2))]
    proof = Path(__file__).resolve().parents[2]/"inputs"/"PROOF.md"
    result = {"status": "PASS", "scope": "exact finite evidence; universal proof is written",
              "python_version": platform.python_version(), "optimized": not __debug__,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "proof_sha256": hashlib.sha256(proof.read_bytes()).hexdigest(),
              "endpoint_guards": guards, "coefficient_box_censuses": cases}
    rendered = json.dumps(result, indent=2)+"\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered)


if __name__ == "__main__":
    main()
