"""Claim-neutral certificate for the nested-entry one-active obstruction.

The finite assertions here refute a uniform old-debt service probability.
They do not assert recurrence or transience of the displayed CTMC.
"""

from __future__ import annotations

from fractions import Fraction

import global_atlas_interface_closure as closure
import one_active_phase_shape as phase_shape
import stoichiometric_gate_feasibility as feasibility


PAIR = (
    closure.mask(("0", "AC")),
    closure.mask(("2A", "2B", "AB", "BC")),
)

ORIENTED_EDGES = (
    ("0", "AC"),
    ("AC", "0"),
    ("BC", "AB"),
    ("AB", "2B"),
    ("2B", "2A"),
    ("2A", "BC"),
)

DEBT_HISTORY = (
    ("0", "AC"),
    ("0", "AC"),
    ("0", "AC"),
    ("2A", "BC"),
    ("AB", "2B"),
    ("2B", "2A"),
    ("AC", "0"),
    ("AC", "0"),
)


def vector(name: str) -> tuple[int, int, int]:
    return closure.COMPLEXES[closure.NAME_TO_INDEX[name]]


def apply_history(
    initial_c: int,
) -> tuple[tuple[int, int, int], int]:
    """Apply the displayed path and the reflected C-debt update."""

    state = [0, 0, initial_c]
    debt = 0
    for source, target in DEBT_HISTORY:
        y = vector(source)
        z = vector(target)
        assert all(state[index] >= y[index] for index in range(3))
        delta = tuple(z[index] - y[index] for index in range(3))
        state = [state[index] + delta[index] for index in range(3)]
        if delta[2] == 1:
            debt += 1
        elif delta[2] == -1:
            debt = max(debt - 1, 0)
        else:
            assert delta[2] == 0
    return tuple(state), debt


def second_birth_before_exit_probability(
    c: int,
    alpha: Fraction,
    beta: Fraction,
) -> Fraction:
    """Exact race probability from (A,B,C)=(1,0,c)."""

    return alpha / (alpha + beta * c)


def leading_activation_coefficient(
    alpha: Fraction,
    beta: Fraction,
    kappa_4: Fraction,
) -> Fraction:
    """Coefficient gamma in P(activate | primary birth)=gamma/C^2+O(C^-3).

    Propensities use falling factorials.  The first rare race creates A=2;
    the second fires 2A->BC before an AC death.
    """

    return alpha * kappa_4 / (beta * beta)


def quadratic_trace_coefficient(
    gamma: Fraction,
    first_loss_moment: Fraction,
    second_loss_moment: Fraction,
) -> Fraction:
    """Formal leading coefficient of E[C_next^2-C^2].

    If the activated excursion has limiting fractional loss Y in [0,1],
    this is gamma E[-2Y+Y^2], which is strictly negative whenever
    E[Y]>0.
    """

    return gamma * (-2 * first_loss_moment + second_loss_moment)


def certificate() -> dict[str, object]:
    feasible = feasibility.feasible_failing_descriptors(PAIR)
    c_axis = tuple(
        descriptor
        for descriptor in feasible
        if descriptor.weight == (0, 0, 1)
        and descriptor.caps[0] == 0
        and descriptor.caps[1] == 0
    )
    assert PAIR in phase_shape.candidate_pairs()
    assert c_axis
    assert apply_history(10) == ((0, 0, 12), 2)

    # A representative rational-rate calculation.  This only checks the
    # algebraic sign conditional on a nonzero limiting fractional loss.
    gamma = leading_activation_coefficient(
        Fraction(1), Fraction(1), Fraction(1)
    )
    formal = quadratic_trace_coefficient(
        gamma, Fraction(1, 2), Fraction(1, 3)
    )
    assert formal < 0

    return {
        "claim_scope": (
            "exact support/path and inverse-C service obstruction; "
            "full base-trace recurrence remains analytic"
        ),
        "pair": closure.pair_payload(PAIR),
        "orientation": ORIENTED_EDGES,
        "active_coordinate": "C",
        "debt_history": DEBT_HISTORY,
        "history_endpoint_from_C10": apply_history(10),
        "uniform_old_debt_service_probability": False,
        "leading_activation_order": "C^-2 per primary birth",
        "stopped_network_trace_certified": True,
        "global_recurrence_certified": False,
    }


if __name__ == "__main__":
    print(certificate())
