from fractions import Fraction
import unittest

from claim_neutral_regressions import (
    fast_neutral_channels,
    fast_neutral_jump_mass,
    fast_neutral_jump_tail,
    fast_neutral_pretrace_hazards,
    fast_neutral_race,
    immigration_death_channels,
    immigration_death_drift,
    is_pairwise_reversible,
    lex_drain_cost_truncation,
    lex_joint_box_size,
    lex_jump_increments,
    lex_switch_cdf_truncation,
    lex_switch_mass,
    lex_switch_tail,
    lex_switch_time_truncation,
    poisson_markov_tail_bound,
    poisson_tight_radius,
    poisson_unnormalised_weight,
    shell_edge_resistance,
    shell_partial_invariant_mass,
    shell_probabilities,
    shell_reversible_weight,
    shell_service_margin,
)


class ShellDependentDriftRegression(unittest.TestCase):
    def test_every_shell_has_strict_but_nonuniform_margin(self) -> None:
        for level in (1, 2, 10, 1_000):
            up, down = shell_probabilities(level)
            self.assertEqual(up + down, 1)
            self.assertEqual(down - up, Fraction(1, 2 * level + 1))
            self.assertGreater(shell_service_margin(level), 0)
        self.assertLess(shell_service_margin(1_000), shell_service_margin(10))

    def test_exact_null_recurrence_certificate(self) -> None:
        self.assertEqual(
            shell_reversible_weight(0),
            shell_reversible_weight(1) * shell_probabilities(1)[1],
        )
        for level in range(1, 40):
            self.assertEqual(
                shell_reversible_weight(level),
                Fraction(1, level) + Fraction(1, level + 1),
            )
            self.assertEqual(shell_edge_resistance(level), level + 1)
            up, _ = shell_probabilities(level)
            _, next_down = shell_probabilities(level + 1)
            self.assertEqual(
                shell_reversible_weight(level) * up,
                shell_reversible_weight(level + 1) * next_down,
            )
        self.assertGreater(shell_partial_invariant_mass(100), Fraction(10))
        self.assertGreater(
            shell_partial_invariant_mass(1_000),
            shell_partial_invariant_mass(100),
        )


class LexicographicCostRegression(unittest.TestCase):
    def test_switch_distribution_and_finite_switch_time(self) -> None:
        for start in (1, 3, 11):
            cutoff = 100
            mass = sum(
                (lex_switch_mass(start, level) for level in range(start, cutoff + 1)),
                Fraction(),
            )
            self.assertEqual(mass, lex_switch_cdf_truncation(start, cutoff))
            self.assertEqual(mass + lex_switch_tail(start, cutoff + 1), 1)
            self.assertEqual(lex_switch_time_truncation(start, cutoff), mass)
            self.assertLess(lex_switch_time_truncation(start, cutoff), 1)

    def test_lex_descent_hides_harmonic_drain_cost(self) -> None:
        self.assertGreater(
            lex_drain_cost_truncation(1, 10_000),
            lex_drain_cost_truncation(1, 100),
        )
        self.assertGreater(lex_drain_cost_truncation(1, 10_000), Fraction(8))
        self.assertEqual(lex_joint_box_size(50), 101)
        self.assertTrue(
            all(abs(component) <= 1 for jump in lex_jump_increments() for component in jump)
        )


class TightInfiniteEnvironmentRegression(unittest.TestCase):
    def test_poisson_environment_is_tight_with_infinite_support(self) -> None:
        channels = immigration_death_channels()
        self.assertTrue(is_pairwise_reversible(channels))
        self.assertTrue(all(channel.molecularity <= 1 for channel in channels))
        self.assertLess(immigration_death_drift(2), 0)
        self.assertGreater(poisson_unnormalised_weight(250), 0)
        birth, death = channels
        for population in range(20):
            left = poisson_unnormalised_weight(population) * birth.propensity((population,))
            right = poisson_unnormalised_weight(population + 1) * death.propensity(
                (population + 1,)
            )
            self.assertEqual(left, right)

        epsilon = Fraction(1, 100)
        radius = poisson_tight_radius(epsilon)
        self.assertEqual(radius, 100)
        self.assertLess(poisson_markov_tail_bound(radius), epsilon)
        self.assertGreater(poisson_unnormalised_weight(radius + 1), 0)


class FastNeutralCRNRegression(unittest.TestCase):
    def test_fast_jump_cost_grows_while_physical_duration_stays_fixed(self) -> None:
        channels = fast_neutral_channels()
        self.assertTrue(is_pairwise_reversible(channels))
        self.assertEqual({channel.linkage for channel in channels}, {0, 1})
        self.assertTrue(all(channel.molecularity <= 1 for channel in channels))

        for shell in (1, 10, 10_000):
            race = fast_neutral_race(shell)
            self.assertEqual(race.fast_hazard, shell)
            self.assertEqual(race.expected_fast_jumps, shell)
            self.assertEqual(race.expected_physical_time, 1)
            for a_population in (0, shell // 2, shell):
                hazards = fast_neutral_pretrace_hazards(
                    a_population,
                    shell - a_population,
                )
                self.assertEqual(hazards, (Fraction(shell), Fraction(1)))

    def test_exact_geometric_reaction_count(self) -> None:
        shell = 17
        cutoff = 30
        mass = sum(
            (fast_neutral_jump_mass(shell, jumps) for jumps in range(cutoff + 1)),
            Fraction(),
        )
        self.assertEqual(mass + fast_neutral_jump_tail(shell, cutoff + 1), 1)


if __name__ == "__main__":
    unittest.main()
