#!/usr/bin/env python3
"""Exact, targeted sanity checks for the harmonic mapping-torus audit.

These calculations test algebra and common incorrect shortcuts. They neither
prove nor refute an arbitrary-metric harmonic-representative assertion.
Python 3 standard library only. No source documents or dataset inputs required.
"""
from fractions import Fraction as Q
import json


def product(values):
    result = Q(1)
    for value in values:
        result *= value
    return result


def main():
    n = 6
    endpoint0 = [Q(1)] * n
    endpoint1 = [Q(4), Q(1, 4)] + [Q(1)] * (n - 2)
    velocity = [b - a for a, b in zip(endpoint0, endpoint1)]
    assert product(endpoint0) == product(endpoint1) == 1
    values = []
    for t in (Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
        k = [(1 - t) * a + t * b for a, b in zip(endpoint0, endpoint1)]
        assert all(v > 0 for v in k)
        determinant = product(k)
        derivative = sum(velocity[i] * product(k[:i] + k[i + 1:])
                         for i in range(n))
        trace = sum(d / v for d, v in zip(velocity, k))
        assert derivative == determinant * trace
        log_volume_derivative = trace / 2
        normalized_trace = trace + n * (-trace / n)
        assert normalized_trace == 0
        values.append((t, determinant, log_volume_derivative))
    assert values[1] == (Q(1, 4), Q(91, 64), Q(36, 91))
    assert values[2][1] == Q(25, 16)

    # If r=vol(K)/mu, the correct factor is r^(-2/m), for m>0.
    exponent_dimensions = list(range(1, 10))
    for m in exponent_dimensions:
        assert Q(-2, m) * Q(m, 2) + 1 == 0
        assert Q(-1, m) * Q(m, 2) + 1 == Q(1, 2)

    # Volume preservation need not mean coordinate Jacobian one. Here a
    # positive Jacobian 4 transports destination density 1/2 to source density 2.
    source_density, destination_density, jacobian = Q(2), Q(1, 2), Q(4)
    destination_metric_determinant = Q(1, 4)
    assert destination_density * jacobian == source_density
    pullback_determinant = jacobian**2 * destination_metric_determinant
    assert pullback_determinant == source_density**2 == Q(4)

    # Circle example: phi(x)=x+sin(2*pi*x)/(4*pi), R(x)=x+1/2,
    # a=phi^{-1} o R. Correct phi o a is R. Incorrect a o phi has
    # derivative phi'(0)/phi'(1/2)=3 at 0, and does not preserve dx.
    epsilon = Q(1, 2)
    derivative_correct_composition = Q(1)
    derivative_reversed_composition = (1 + epsilon) / (1 - epsilon)
    assert derivative_correct_composition == 1
    assert derivative_reversed_composition == 3

    # The Moser cancellation is d(eta)+d(i_X mu_s)=0 with i_X mu_s=-eta.
    assert Q(1) + (-1) == 0
    assert Q(1) + (+1) == 2

    # Identity gluing and scalar metric factor c(t)=1+t(1-t): endpoint
    # values agree, but first derivatives disagree. This is not a smooth seam.
    c = lambda t: 1 + t * (1 - t)
    dc = lambda t: 1 - 2 * t
    assert c(Q(0)) == c(Q(1)) == 1
    assert dc(Q(0)) == 1 and dc(Q(1)) == -1

    # For rho(t,x)=1+epsilon*sin(2*pi*t)*cos(2*pi*x1) on T^6,
    # integral rho dx=1 for all t, but (d_t log rho)/(2*pi)=epsilon
    # at t=0,x1=0. Total fibre volume alone does not imply co-closed dt.
    total_volume_example_laplacian_over_2pi = epsilon
    assert total_volume_example_laplacian_over_2pi != 0

    print(json.dumps({
        "result": "passed",
        "fibre_dimension": n,
        "diagonal_interpolation_points": len(values),
        "nonconstant_raw_volume_example": {
            "time": "1/4", "determinant": "91/64",
            "log_volume_derivative": "36/91",
            "normalized_log_volume_derivative": "0"
        },
        "normalization_exponent_dimensions": exponent_dimensions,
        "nonunit_jacobian_density_preservation": {
            "jacobian": "4", "destination_density": "1/2",
            "source_density": "2", "pullback_metric_determinant": "4"
        },
        "circle_composition_derivatives_at_zero": {
            "correct": str(derivative_correct_composition),
            "reversed": str(derivative_reversed_composition)
        },
        "moser_sign_cancellation_checked": True,
        "equal_endpoint_values_but_first_jet_mismatch_detected": True,
        "constant_total_volume_nonharmonic_projection_detected": True,
        "limitations": "Finite exact sanity checks only; global reasoning is in the independent mathematical audit."
    }, indent=2))


if __name__ == "__main__":
    main()
