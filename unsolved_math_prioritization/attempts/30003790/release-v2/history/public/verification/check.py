#!/usr/bin/env python3
"""Small deterministic controls for RESULT.md. No external data or packages."""
import cmath
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import random


def sinc(x):
    return math.sin(x) / x if x else 1.0


def check_slice():
    b = Q(1, 4)
    widths = [Q(1, 5), Q(1, 20), Q(1, 100), Q(1, 1000)]
    rows = []
    for h in widths:
        variance = b * b / 3 + h * h / 12
        span = 2 * b + h
        oriented = 2 * (1 - sinc(float(b)) * sinc(float(h) / 2))
        projector = 1 - sinc(2 * float(b)) * sinc(float(h))
        assert variance > b * b / 3 and span > 2 * b
        assert oriented > 0 and projector > 0
        rows.append(dict(h=str(h), latent_span=str(span), variance=str(variance),
                         oriented_loss=oriented, projector_loss=projector))
    # Independent midpoint integration of the two-dimensional conditional rectangle.
    n, h = 180, 0.08
    ts = [(-h / 2 + (i + .5) * h / n) - (-float(b) + (j + .5) * 2 * float(b) / n)
          for i in range(n) for j in range(n)]
    mean_cos = sum(math.cos(t) for t in ts) / len(ts)
    mean_sin2 = sum(math.sin(t) ** 2 for t in ts) / len(ts)
    e_oriented = abs(2 * (1 - mean_cos) - 2 * (1 - sinc(float(b)) * sinc(h / 2)))
    e_projector = abs(2 * mean_sin2 - (1 - sinc(2 * float(b)) * sinc(h)))
    assert e_oriented < 2e-6 and e_projector < 2e-6
    return dict(rows=rows, limiting_oriented_loss=2 * (1 - sinc(float(b))),
                limiting_projector_loss=1 - sinc(2 * float(b)),
                quadrature_points=len(ts), quadrature_errors=[e_oriented, e_projector],
                note="Quadrature is a numerical control; the exact formulas are proved in RESULT.md.")


def check_guard():
    rng = random.Random(30003790)
    dirs = [(Q(1), Q(0)), (Q(0), Q(1)), (Q(3, 5), Q(4, 5)),
            (Q(-3, 5), Q(4, 5)), (Q(5, 13), Q(-12, 13))]
    for a in dirs:
        assert a[0] ** 2 + a[1] ** 2 == 1
    cases = 0
    max_ratio = Q(0)
    for lam in [Q(1), Q(1, 2), Q(1, 7), Q(1, 50)]:
        for _ in range(35):
            records = []
            for i in range(30):
                radius = Q(rng.randrange(1, 101), 10)
                u, a = rng.choice(dirs), rng.choice(dirs)
                z = (radius * u[0], radius * u[1])
                proxy = abs(a[0] * z[0] + a[1] * z[1])
                d = proxy + lam * radius
                assert lam * radius <= d <= (1 + lam) * radius
                records.append((d, i, radius))
            for k in [1, 3, 8, 17, 30]:
                euclidean_k = sorted(r[2] for r in records)[k - 1]
                chosen = sorted(records)[:k]
                chosen_radius = max(r[2] for r in chosen)
                assert chosen_radius <= (1 + lam) / lam * euclidean_k
                max_ratio = max(max_ratio, chosen_radius / euclidean_k)
                cases += 1
    # Without a guard a far orthogonal point beats a close tangential point.
    unguarded = [(Q(1), Q(1)), (Q(0), Q(100))]
    assert min(unguarded)[1] == 100
    return dict(exact_order_statistic_cases=cases, max_selected_to_euclidean_ratio=str(max_ratio),
                unguarded_selected_radius=100, unguarded_euclidean_nearest_radius=1)


def check_chernoff_and_rates():
    rows = []
    for n in [20, 50, 100, 200]:
        k = math.isqrt(n)
        p = 2 * k / n
        tail = sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k))
        bound = math.exp(-k / 4)
        assert tail <= bound
        rows.append(dict(n=n, k=k, exact_binomial_tail=tail, chernoff_bound=bound))
    exponents = []
    for d in [1, 2, 5, 20]:
        alpha, beta = Q(1, 2), Q(1, 4 * d)
        radius_exponent = (alpha - 1) / d + beta
        assert radius_exponent == -Q(1, 4 * d)
        exponents.append(dict(d=d, radius_exponent=str(radius_exponent),
                              lipschitz_squared_bias_exponent=str(2 * radius_exponent)))
    return dict(binomial_checks=rows, exact_rate_exponents=exponents)


def check_deconvolution():
    # Known Gaussian convolution identity, with a nonconstant signed weight.
    zs, probs, weights, sigma = [-.5, .25, 1.0], [.2, .5, .3], [-2., 1., .4], .3
    max_error = 0
    for u in [-8., -2., 0., .5, 4.]:
        clean = sum(p * w * cmath.exp(1j * u * z) for p, w, z in zip(probs, weights, zs))
        observed = sum(p * w * cmath.exp(1j * u * z - sigma ** 2 * u ** 2 / 2)
                       for p, w, z in zip(probs, weights, zs))
        recovered = observed / math.exp(-sigma ** 2 * u ** 2 / 2)
        max_error = max(max_error, abs(recovered - clean))
    assert max_error < 1e-13
    bounds = []
    for n in [100, 10000, 1000000, 100000000]:
        u = math.sqrt(math.log(n) / (2 * sigma ** 2))
        bound = u * math.exp(sigma ** 2 * u ** 2) / (math.pi * n)
        assert abs(bound - u / (math.pi * math.sqrt(n))) < 1e-12
        bounds.append(dict(n=n, cutoff=u, stochastic_l2_bound_M1=bound))
    assert all(a['stochastic_l2_bound_M1'] > b['stochastic_l2_bound_M1']
               for a, b in zip(bounds, bounds[1:]))
    return dict(characteristic_identity_max_error=max_error, bounds=bounds,
                note="The discrete identity control does not test the L2-density hypothesis; no numerical deconvolution theorem is claimed.")


def check_pilot():
    # Exact finite control: F(t)=2t, p(t)=F(t)+bounded deterministic perturbation.
    delta, h, m = Q(1, 20), Q(1, 7), Q(2)
    cells = {}
    for i in range(-100, 101):
        t = Q(i, 100)
        f = m * t
        p = f + (delta if i % 2 else -delta)
        cell = p // h
        cells.setdefault(cell, []).append(t)
    bound = (h + 2 * delta) / m
    observed = max(max(ts) - min(ts) for ts in cells.values())
    assert observed <= bound
    return dict(cells=len(cells), max_latent_width=str(observed), exact_upper_bound=str(bound))


def check_flat_jet():
    # d/dt [P(1/t) exp(-1/t^2)] corresponds to [-u^2 P'(u)+2u^3P(u)].
    p = {0: 1}
    degrees = []
    for _ in range(12):
        q = {}
        for degree, coefficient in p.items():
            if degree:
                q[degree + 1] = q.get(degree + 1, 0) - degree * coefficient
            q[degree + 3] = q.get(degree + 3, 0) + 2 * coefficient
        p = {k: v for k, v in q.items() if v}
        degrees.append(max(p))
    assert degrees == [3 * j for j in range(1, 13)]
    b = .5
    discrepancy = math.exp(-1 / (b * b))
    assert discrepancy > 0
    return dict(derivative_polynomial_degrees=degrees, fixed_width=b, discrepancy=discrepancy,
                note="All-order flatness is proved by the polynomial-times-exponential induction, not by these 12 checks.")


def main():
    result = dict(problem_id="30003790", status="PASS", scope="Scoped algebraic and finite controls only",
                  slice=check_slice(), guard=check_guard(), chernoff_rates=check_chernoff_and_rates(),
                  deconvolution=check_deconvolution(), pilot=check_pilot(), flat_jet=check_flat_jet())
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
