from fractions import Fraction as Q
from itertools import product
import unittest

from residual_pair_certificate import (
    FastRates,
    SlowRates,
    certified_generator,
    certified_riccati,
    choose_weights,
    direct_generator,
    direct_riccati,
    workload_coefficients,
)


DIRECTED_EDGES = ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1))


def strong_masks() -> tuple[int, ...]:
    masks = []
    for mask in range(1, 1 << len(DIRECTED_EDGES)):
        adjacency = {vertex: set() for vertex in range(3)}
        for edge_index, (source, target) in enumerate(DIRECTED_EDGES):
            if mask & (1 << edge_index):
                adjacency[source].add(target)
        strong = True
        for start in range(3):
            reached = {start}
            frontier = [start]
            while frontier:
                source = frontier.pop()
                for target in adjacency[source] - reached:
                    reached.add(target)
                    frontier.append(target)
            strong &= len(reached) == 3
        if strong:
            masks.append(mask)
    return tuple(masks)


class ResidualPairCertificate(unittest.TestCase):
    def test_directed_cycles_and_full_graph(self) -> None:
        examples = (
            (
                FastRates(Q(0), Q(1), Q(1), Q(0), Q(0), Q(1)),
                SlowRates(Q(0), Q(1), Q(1), Q(0), Q(0), Q(1)),
            ),
            (
                FastRates(Q(2), Q(3), Q(5), Q(7), Q(11), Q(13)),
                SlowRates(Q(2), Q(3), Q(5), Q(7), Q(11), Q(13)),
            ),
            (
                FastRates(Q(1), Q(0), Q(0), Q(1), Q(1), Q(0)),
                SlowRates(Q(1), Q(0), Q(0), Q(1), Q(1), Q(0)),
            ),
        )
        for fast, slow in examples:
            lam, rho = choose_weights(fast, slow)
            coeff = workload_coefficients(fast, slow, lam, rho)
            for state in product(range(7), repeat=3):
                self.assertEqual(
                    direct_generator(state, fast, slow, coeff),
                    certified_generator(state, coeff),
                )
                self.assertEqual(
                    direct_riccati(state, fast),
                    certified_riccati(state, fast),
                )

    def test_positive_weights_and_strict_drift_coefficients(self) -> None:
        fast = FastRates(Q(0), Q(2), Q(0), Q(3), Q(5), Q(7))
        slow = SlowRates(Q(2), Q(0), Q(0), Q(3), Q(5), Q(7))
        lam, rho = choose_weights(fast, slow)
        coeff = workload_coefficients(fast, slow, lam, rho)
        for key in ("p_a", "p_b", "p_c", "c_2", "c_bc", "d_a", "d_c"):
            self.assertGreater(coeff[key], 0)

    def test_all_strong_orientation_pairs(self) -> None:
        masks = strong_masks()
        self.assertEqual(len(masks), 18)
        for fast_mask in masks:
            fast_values = tuple(
                Q(index + 1) if fast_mask & (1 << index) else Q(0)
                for index in range(6)
            )
            fast = FastRates(*fast_values)
            for slow_mask in masks:
                slow_values = tuple(
                    Q(7 - index) if slow_mask & (1 << index) else Q(0)
                    for index in range(6)
                )
                slow = SlowRates(*slow_values)
                lam, rho = choose_weights(fast, slow)
                coeff = workload_coefficients(fast, slow, lam, rho)
                for key in (
                    "p_a",
                    "p_b",
                    "p_c",
                    "c_2",
                    "c_bc",
                    "d_a",
                    "d_c",
                ):
                    self.assertGreater(coeff[key], 0)
                for state in product(range(3), repeat=3):
                    self.assertEqual(
                        direct_generator(state, fast, slow, coeff),
                        certified_generator(state, coeff),
                    )
                    self.assertEqual(
                        direct_riccati(state, fast),
                        certified_riccati(state, fast),
                    )
