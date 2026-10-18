#!/usr/bin/env python3
"""Finite exact stress tests; no network, imports of submitted code or mutation.

All probabilities use fractions. This is supporting verification of identities,
not a substitute for the asymptotic argument in DERIVATION.md.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path

COUNTS = defaultdict(int)
SAMPLES = []


def check(condition, group):
    if not condition:
        raise AssertionError(group)
    COUNTS[group] += 1


def plus(dist, x, p):
    if p:
        dist[x] += p


def homogeneous(q, n, start=0):
    dist = {start: F(1)}
    for _ in range(n):
        nxt = defaultdict(F)
        for x, w in dist.items():
            plus(nxt, x + 1, w * q)
            plus(nxt, x - 1, w * (1 - q))
        dist = dict(nxt)
    return dist


def lazy(q, n):
    a = q * (1 - q)
    dist = {0: F(1)}
    for _ in range(n):
        nxt = defaultdict(F)
        for x, w in dist.items():
            for step, p in ((-1, a), (0, 1 - 2 * a), (1, a)):
                plus(nxt, x + step, w * p)
        dist = dict(nxt)
    return dist


def killed_gap(q, n, d):
    if d == 0:
        return F(0)
    a = q * (1 - q)
    dist = {d: F(1)}
    for _ in range(n):
        nxt = defaultdict(F)
        for x, w in dist.items():
            for step, p in ((-1, a), (0, 1 - 2 * a), (1, a)):
                if x + step > 0:
                    plus(nxt, x + step, w * p)
        dist = dict(nxt)
    return sum(dist.values(), F(0))


def reflection_tests():
    for q in map(F, (F(1, 1000), F(1, 5), F(1, 2), F(4, 5), F(999, 1000))):
        for n in range(17):
            p = lazy(q, n)
            for d in range(1, 8):
                s = killed_gap(q, n, d)
                direct = sum((p.get(j, F(0)) for j in range(1 - d, d + 1)), F(0))
                check(s == direct, "lazy_reflection_exact")
                if d > n:
                    check(s == 1, "pre_meeting_finite_speed")


def coordinates(starts, n):
    return sorted({(t, x + d) for t in range(n) for x in starts
                   for d in range(-t, t + 1, 2)})


def environments(coords, law):
    for picks in product(range(len(law)), repeat=len(coords)):
        env, weight = {}, F(1)
        for c, i in zip(coords, picks):
            p, w = law[i]
            env[c] = p
            weight *= w
        yield env, weight


def kernel(env, start, n, radius=None, v=F(0)):
    dist = {start: F(1)}
    for t in range(n):
        nxt = defaultdict(F)
        for x, w in dist.items():
            p = env[t, x]
            for step, probability in ((1, p), (-1, 1 - p)):
                z = x + step
                if radius is None or abs(z - start - v * (t + 1)) <= radius:
                    plus(nxt, z, w * probability)
        dist = dict(nxt)
    return dist


def l1(a, b):
    return sum((abs(a.get(x, F(0)) - b.get(x, F(0)))
                for x in a.keys() | b.keys()), F(0))


LAWS = [
    ("near_arrows_symmetric", ((F(1, 100), F(1, 2)), (F(99, 100), F(1, 2)))),
    ("biased_two_atom_elliptic", ((F(1, 20), F(2, 3)), (F(4, 5), F(1, 3)))),
    ("deterministic_elliptic", ((F(3, 4), F(1)),)),
    ("excluded_arrow_boundary", ((F(0), F(1, 2)), (F(1), F(1, 2)))),
]


def coalescence_tests():
    for label, law in LAWS:
        q = sum((p * w for p, w in law), F(0))
        for n in range(1, 4):
            for d in (1, 2):
                starts = (0, 2 * d)
                expectation = F(0)
                total = F(0)
                for env, weight in environments(coordinates(starts, n), law):
                    expectation += weight * l1(kernel(env, 0, n), kernel(env, 2 * d, n))
                    total += weight
                survival = killed_gap(q, n, d)
                check(total == 1, "coalescence_environment_weights")
                check(expectation <= 2 * survival, "quenched_kernel_coalescence_L1")
                SAMPLES.append({"law": label, "steps": n, "half_gap": d,
                                "expected_kernel_L1": str(expectation),
                                "twice_nonmeeting_probability": str(2 * survival)})


def coarse(dist, length, align):
    out = defaultdict(F)
    for x, w in dist.items():
        plus(out, (F(x) - align) // length, w)
    return dict(out)


def mix(mu, kernels):
    out = defaultdict(F)
    for x, w in mu.items():
        for y, p in kernels[x].items():
            plus(out, y, w * p)
    return dict(out)


def strip_tests():
    starts = (-4, -2, 0, 2, 4)
    measures = ({x: F(i + 1, 15) for i, x in enumerate(starts)}, {0: F(1)})
    for n in (1, 2, 4):
        coords = coordinates(starts, n)
        for radius in (1, 2, 3):
            for v in (F(-2, 3), F(0), F(3, 5)):
                strip = {c: (F(c[1]) - v * c[0]) // radius for c in coords}
                indices = sorted(set(strip.values()))
                env = {c: (F(1, 100), F(3, 10), F(99, 100))[(c[0] + c[1]) % 3]
                       for c in coords}
                base = {x: kernel(env, x, n, radius, v) for x in starts}
                for x in starts:
                    overlap = sum(k * radius - radius - 1 <= x <= (k + 1) * radius + radius + 1
                                  for k in indices)
                    check(overlap <= 6, "strip_overlap_at_most_six")
                for mu in measures:
                    weights = {k: sum((p for x, p in mu.items()
                                      if k * radius - radius - 1 <= x <= (k + 1) * radius + radius + 1), F(0))
                               for k in indices}
                    check(sum(weights.values(), F(0)) <= 6, "sum_influence_weights")
                    check(sum((w * w for w in weights.values()), F(0)) <= 6 * max(weights.values()),
                          "sum_squared_influence_weights")
                    base_mix = mix(mu, base)
                    for k in indices:
                        for replacement in (F(1, 1000), F(999, 1000)):
                            altered = {c: replacement if strip[c] == k else p for c, p in env.items()}
                            changed = {x: kernel(altered, x, n, radius, v) for x in starts}
                            for x in starts:
                                if not k * radius - radius - 1 <= x <= (k + 1) * radius + radius + 1:
                                    check(base[x] == changed[x], "strip_exact_zero_influence_outside_J")
                            alt_mix = mix(mu, changed)
                            check(l1(base_mix, alt_mix) <= 2 * weights[k], "killed_kernel_strip_oscillation")
                            for length in (F(3, 2), F(2), F(3), F(11)):
                                for align in (F(-2), F(0), F(1, 3)):
                                    a = coarse(base_mix, length, align)
                                    b = coarse(alt_mix, length, align)
                                    check(l1(a, b) <= 2 * weights[k], "real_cell_coarsening_oscillation")
                                    target = {0: F(1)}
                                    check(abs(l1(a, target) - l1(b, target)) <= 2 * weights[k],
                                          "F_dagger_strip_oscillation")
                    # Positivity, exact killed mass, and restoration of the unrestricted kernel.
                    full = mix(mu, {x: kernel(env, x, n) for x in starts})
                    lost = 1 - sum(base_mix.values(), F(0))
                    check(all(full.get(y, F(0)) >= p for y, p in base_mix.items()), "killed_kernel_domination")
                    check(l1(full, base_mix) == lost, "exact_lost_mass_L1")
                    for length in (F(3, 2), F(2), F(11)):
                        a, b = coarse(full, length, F(1, 3)), coarse(base_mix, length, F(1, 3))
                        check(abs(l1(a, {0: F(1)}) - l1(b, {0: F(1)})) <= lost,
                              "restoration_F_difference")


def replacement(mu, alpha, length, align):
    old_cells, alpha_cells = coarse(mu, length, align), coarse(alpha, length, align)
    out = {}
    for x, p in alpha.items():
        c = (F(x) - align) // length
        out[x] = old_cells.get(c, F(0)) * p / alpha_cells[c]
    return out


def transfer_tests():
    n, old_steps = 2, 2
    starts = (-2, 0, 2)
    for label, law in LAWS[:2]:
        q = sum((p * w for p, w in law), F(0))
        alpha = homogeneous(q, old_steps)
        total_alpha = homogeneous(q, n + old_steps)
        worlds = [(w, {x: kernel(env, x, n) for x in starts})
                  for env, w in environments(coordinates(starts, n), law)]
        for length in (F(1), F(2), F(3), F(5)):
            for align in (F(-2), F(0), F(1, 3)):
                for mu in ({-2: F(1, 2), 0: F(1, 3), 2: F(1, 6)}, {0: F(1)}):
                    replacement_mu = replacement(mu, alpha, length, align)
                    old_L1 = l1(coarse(mu, length, align), coarse(alpha, length, align))
                    check(l1(replacement_mu, alpha) == old_L1, "within_cell_replacement_identity_N")
                    pair_bound = F(0)
                    alpha_cells = coarse(alpha, length, align)
                    for x, px in mu.items():
                        c = (F(x) - align) // length
                        for y, py in alpha.items():
                            if (F(y) - align) // length == c:
                                pair_bound += px * py / alpha_cells[c] * 2 * killed_gap(q, n, abs(x - y) // 2)
                    replacement_error = sum((w * l1(mix(mu, ks), mix(replacement_mu, ks))
                                             for w, ks in worlds), F(0))
                    check(replacement_error <= pair_bound, "replacement_M_exact_coalescent_bound")
                    for target_length in (F(1), F(3, 2), F(3), F(7)):
                        for target_align in (F(-1), F(1, 3)):
                            target = coarse(total_alpha, target_length, target_align)
                            full = F(0)
                            annealed_old_error = F(0)
                            translate_bound = F(0)
                            for w, ks in worlds:
                                full += w * l1(coarse(mix(mu, ks), target_length, target_align), target)
                                annealed_old_error += w * l1(coarse(mix(alpha, ks), target_length, target_align), target)
                                for x, px in alpha.items():
                                    local_target = coarse(homogeneous(q, n, x), target_length, target_align)
                                    translate_bound += w * px * l1(coarse(ks[x], target_length, target_align), local_target)
                            check(annealed_old_error <= translate_bound, "translated_jensen_O")
                            check(full <= old_L1 + pair_bound + translate_bound, "full_conditional_mean_P")


def parameter_tests():
    eta, kappa, old_radius, length, cell = F(1, 32), F(1, 32), F(3, 8), F(3, 4), F(5, 16)
    variance_exponent = eta + F(1, 2) - 2 * old_radius
    check(variance_exponent == F(-7, 32), "exact_exponents")
    check(-2 * kappa - variance_exponent == F(5, 32), "exact_exponents")
    check(cell - length / 2 == F(-1, 16), "exact_exponents")
    check(old_radius - F(1, 2) < -kappa, "exact_exponents")
    check(cell > F(1, 4), "auxiliary_scale_G_margin")


def main():
    reflection_tests()
    coalescence_tests()
    strip_tests()
    transfer_tests()
    parameter_tests()
    here = Path(__file__)
    result = {"schema": "pr239-independent-exact-coalescence-strip-checks-v1",
              "all_passed": True, "assertions": sum(COUNTS.values()),
              "counts": dict(sorted(COUNTS.items())), "coalescence_samples": SAMPLES,
              "source": {"bytes": here.stat().st_size,
                         "sha256": hashlib.sha256(here.read_bytes()).hexdigest()},
              "scope": "Finite exact stress tests. No asymptotic proof, novelty certificate, external action, or repository acceptance inferred.",
              "excluded_boundary_note": "Arrow-law finite coupling test is deliberately outside 0<p<1 a.s.; no concentration theorem is asserted for it."}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
