"""Adversarial bookkeeping probes for the pinned frequency-block lemma.

These finite quadrature probes are not mathematical verification of the
frequency-block theorem.  They optimize admissible output-dependent
coefficient phases and test for obvious growth in several elementary input
families.  The accompanying audit gives the exact analytic checks.
Run with Python 3; no third-party dependencies are required.
"""

import cmath
import json
import math
import random
from pathlib import Path


def gaussian_derivative_window(z, xi, d, q=1.0):
    sigma = 3.0 * q
    g = math.exp(-z * z / (2.0 * sigma)) / math.sqrt(2.0 * math.pi * sigma)
    g1 = -z / sigma * g
    g2 = (z * z / sigma**2 - 1.0 / sigma) * g
    g3 = (3.0 * z / sigma**2 - z**3 / sigma**3) * g
    return cmath.exp(1j * xi * z) * (g3 + 3j * xi * g2 - 3.0 * xi**2 * g1 - 1j * xi**3 * g) / d**3


def coefficient_probe(d, node_count, scale_count, family, frequency_count=32):
    h = 1.0 / (4.0 * d)
    radius = node_count // 2
    indices = list(range(-radius, radius + 1))
    scales = [2.0**k for k in range(scale_count)]
    xis = [(-2.0 * d + (f + 0.5) * 4.0 * d / frequency_count) for f in range(frequency_count)]
    measure_weight = 4.0 / frequency_count
    rng = random.Random(825231)
    a1 = {}
    a2 = {}
    for j in indices:
        for l in indices:
            if family == "constant":
                a1[j, l] = a2[j, l] = 1.0
            elif family == "chirp":
                alpha = 1.5 * d
                a1[j, l] = cmath.exp(-1j * alpha * (j + l) * h)
                a2[j, l] = cmath.exp(-1j * alpha * l * h)
            else:
                a1[j, l] = rng.choice((-1.0, 1.0))
                a2[j, l] = rng.choice((-1.0, 1.0))
    kernels = {}
    for k, scale in enumerate(scales):
        for f, xi in enumerate(xis):
            for node_sum in range(-3 * radius, 3 * radius + 1):
                kernels[k, f, node_sum] = gaussian_derivative_window(node_sum * h / scale, xi, d) / scale
    norm_product = ((h**2 * node_count**2)**(1.0 / 3.0))**2
    output_power_sum = 0.0
    coefficient_square_sum_max = 0.0
    for i in indices:
        for j in indices:
            values = []
            for k in range(scale_count):
                for f in range(frequency_count):
                    values.append(h * sum(a1[j, l] * a2[l, i] * kernels[k, f, i + j + l] for l in indices))
            square_sum = measure_weight * sum(abs(t)**2 for t in values)
            maximum = max(abs(t) for t in values)
            denominator = max(math.sqrt(square_sum), maximum)
            if denominator:
                # mu_{ij,k}(xi) = conjugate(T_{ij,k}(xi))/denominator.
                # Both the coefficient supremum and total square integral
                # in the finite quadrature menu are then bounded by one.
                output = square_sum / denominator
                coefficient_square_sum_max = max(coefficient_square_sum_max, square_sum / denominator**2)
                output_power_sum += h**2 * output**1.5
    return {
        "D": d,
        "nodes_per_coordinate": node_count,
        "scales": scale_count,
        "family": family,
        "frequency_midpoints": frequency_count,
        "mesh": h,
        "optimized_output_norm_ratio": output_power_sum**(2.0 / 3.0) / norm_product,
        "max_coefficient_square_sum": coefficient_square_sum_max,
        "caveat": "Finite midpoint quadrature, not a certified continuum counterexample search.",
    }


def covariance_probe():
    # Sigma/s = [[2 theta,-theta],[-theta,3]].
    # The covariance majorant is 4 diag(theta,1); its difference has
    # determinant theta*(2-theta)>0.  Evaluate limiting and edge values.
    return [{
        "theta": theta,
        "positive_minor_1": 2.0 * theta,
        "positive_minor_2": theta * (2.0 - theta),
        "gaussian_density_majorant_constant": 4.0 / math.sqrt(6.0 - theta),
    } for theta in (1.0 / 16.0, 1.0 / 256.0, 1.0 / 65536.0)]


def main():
    probes = []
    for d, node_count, scale_count in ((1, 17, 1), (1, 33, 4), (2, 33, 4), (4, 33, 4)):
        for family in ("constant", "chirp", "random_sign"):
            probes.append(coefficient_probe(d, node_count, scale_count, family))
    result = {"covariance": covariance_probe(), "frequency_block": probes}
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
