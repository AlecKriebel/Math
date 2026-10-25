#!/usr/bin/env python3
"""Independent exact local-response regressions for B-REPAIR-NUMERIC-001.

Only rational arithmetic is used. Each interval has duration log(2), so an
integer pair rate k has survival 2^(-k). These bounded scalar checks supplement
the graph/measure proof and the separate raw-CTMC verifier; they do not assert
that an arbitrary signed hidden-history projector exists.
"""

if not __debug__:
    raise SystemExit("Verification requires assertions; optimized Python is unsupported.")

from fractions import Fraction as F


def survival(rate):
    return F(1, 2**rate)


def balanced_parent_word_test():
    # gamma=1/3; first-arm survivals over log(4) at rates 1,2.
    # Scaled by the positive child-pair entry mass.
    gamma = F(1, 3)
    w1, w2 = gamma**2 * F(1, 4), (1-gamma)**2 * F(1, 16)
    assert w1 == w2 == F(1, 36)

    # Swapping rates 3,4 preserves every local pair density derivative.
    for order in range(12):
        left = (-1)**order * (w1 * 3**(order+1) + w2 * 4**(order+1))
        right = (-1)**order * (w1 * 4**(order+1) + w2 * 3**(order+1))
        assert left == right

    # An actual earlier-parent anchor selects the first arm by the second
    # merger's support. At the start of this epoch, lambda_o=5.
    triple_left, triple_right = w1 * 3 * 5, w1 * 4 * 5
    assert triple_left - triple_right == F(-5, 36)
    assert triple_left != triple_right


def bypass_and_tree_join_test():
    # Initial route-1 co-occupancy includes a positive bypass contribution.
    route1_from_child, bypass, route2 = F(1, 10), F(1, 10), F(1, 7)
    route1 = route1_from_child + bypass
    observed_start_q = route1 + route2
    recovered_route1 = observed_start_q - route2
    assert recovered_route1 == route1
    assert recovered_route1 != route1_from_child  # rejects omitted bypass

    for ordinary_rate, arm2_rate, join_mass in ((2, 3, F(1, 20)),
                                               (5, 7, F(0))):
        route1 *= survival(ordinary_rate)
        route2 *= survival(arm2_rate)
        observed_q = route1 + route2
        observed_f = ordinary_rate * route1 + arm2_rate * route2
        recovered_route1 *= survival(ordinary_rate)
        recovered_route2 = observed_q - recovered_route1
        assert recovered_route2 == route2 > 0
        recovered_rate = (observed_f - ordinary_rate * recovered_route1) / recovered_route2
        assert recovered_rate == arm2_rate
        # At the ordinary tree join, all observed q jump belongs to route 1.
        observed_after_join_q = observed_q + join_mass
        recovered_route1 += observed_after_join_q - observed_q
        route1 += join_mass
        assert recovered_route1 == route1


def upper_reticulation_propagation_test():
    # Directly enumerate the four independent routing assignments of a pair
    # through an already recovered upper reticulation.
    incoming_mass, lower_arm_mass = F(1, 4), F(1, 8)
    for gamma in (F(1, 2), F(1, 3)):
        for rates in ((2, 4), (2, 2)):
            probabilities = (gamma, 1-gamma)
            known_q = F(0)
            known_f = F(0)
            for first_route in range(2):
                for second_route in range(2):
                    mass = incoming_mass * probabilities[first_route] * probabilities[second_route]
                    if first_route == second_route:
                        remaining = mass * survival(rates[first_route])
                        known_q += remaining
                        known_f += rates[first_route] * remaining
                    # Distinct routes remain separated and contribute zero.
            lower_q = lower_arm_mass * survival(3)
            observed_q, observed_f = known_q + lower_q, known_f + 3*lower_q
            reconstructed_q = observed_q - known_q
            assert reconstructed_q == lower_q > 0
            assert (observed_f - known_f) / reconstructed_q == 3

    # Negative control: treating the upper reticulation as one unchanged
    # ordinary population fails even positivity for this explicit case.
    actual_q = incoming_mass * F(5, 64) + lower_arm_mass * survival(3)
    false_ordinary_q = incoming_mass * survival(2)
    assert actual_q - false_ordinary_q < 0


if __name__ == "__main__":
    balanced_parent_word_test()
    bypass_and_tree_join_test()
    upper_reticulation_propagation_test()
    print("PASS: balanced-word separation, bypass/tree-join propagation, "
          "and upper-reticulation subtraction; negative controls rejected.")
