"""Claim-neutral algebra for the exact relative-resistance equality chain.

The network is

    0 <-> B+C,
    B -> A -> A+B -> 2B -> B.

The executable freezes two identities used by the analytic base-trace
calculation:

* ``Q=C-A-B`` changes only at ``A->A+B`` and ``2B->B``;
* on the random clock ``u=int B(t) dt``, the A-coordinate is exactly an
  immigration--death chain.

It is not a numerical proof of the singular perturbation theorem and it
does not certify a support-pair or T3-2 recurrence claim.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from math import factorial


REACTION_DELTAS = {
    "0->BC": (0, 1, 1),
    "BC->0": (0, -1, -1),
    "B->A": (1, -1, 0),
    "A->AB": (0, 1, 0),
    "AB->2B": (-1, 1, 0),
    "2B->B": (0, -1, 0),
}

EXPECTED_PAYLOAD_SHA256 = (
    "1f7371556dd69667bebceffcf5aff703733a1152c979442e1006abea6cca1d39"
)


def q_increment(delta: tuple[int, int, int]) -> int:
    """Increment of ``Q=C-A-B`` for one reaction vector."""

    da, db, dc = delta
    return dc - da - db


def a_increment(delta: tuple[int, int, int]) -> int:
    return delta[0]


def a_clock_jump_probabilities(
    population: int,
    kappa_up: Fraction = Fraction(1),
    kappa_down: Fraction = Fraction(1),
) -> tuple[Fraction, Fraction]:
    """Up/down probabilities at the next A-changing reaction.

    In physical time the two A-changing hazards are
    ``kappa_up*B`` and ``kappa_down*A*B``.  Their common B factor cancels.
    """

    if population < 1:
        raise ValueError("the killed A-clock formula requires A >= 1")
    kappa_up = Fraction(kappa_up)
    kappa_down = Fraction(kappa_down)
    denominator = kappa_up + kappa_down * population
    return kappa_up / denominator, kappa_down * population / denominator


def a_ceiling_probability(
    ceiling: int,
    kappa_up: Fraction = Fraction(1),
    kappa_down: Fraction = Fraction(1),
) -> Fraction:
    """Exact ``P_1(T_ceiling<T_0)`` for the A-clock birth-death chain."""

    if ceiling < 2:
        raise ValueError("ceiling must be at least two")
    ratio = Fraction(kappa_down, kappa_up)
    denominator = sum(
        (ratio**j * factorial(j) for j in range(ceiling)),
        Fraction(),
    )
    return Fraction(1, 1) / denominator


def a_ceiling_factorial_bound(
    ceiling: int,
    kappa_up: Fraction = Fraction(1),
    kappa_down: Fraction = Fraction(1),
) -> Fraction:
    """The last-term factorial upper bound for ``a_ceiling_probability``."""

    if ceiling < 2:
        raise ValueError("ceiling must be at least two")
    return Fraction(kappa_up, kappa_down) ** (ceiling - 1) / factorial(
        ceiling - 1
    )


def leading_powered_drift_sign(phi: Fraction) -> int:
    """Sign of the leading powered-factorial coefficient ``phi-1``."""

    phi = Fraction(phi)
    if not 0 < phi < 1:
        raise ValueError("the Feynman--Kac moment must lie in (0,1)")
    return -1


def stopped_power_scaling(power: int) -> dict[str, int]:
    """Powers of N in the clean stopped-episode bookkeeping.

    The trigger has probability order ``N^-1``.  A successful endpoint
    loses a fixed fraction of C, hence changes ``F^power`` by order
    ``N^power log(N)^power``.  Every failed endpoint has only a bounded
    population overshoot, so its positive powered cost is one derivative,
    or order ``N^(power-1) log(N)^power``.  Multiplication by the trigger
    probability leaves a one-power strict gap.
    """

    if power < 1:
        raise ValueError("power must be positive")
    return {
        "successful_expected_power": power - 1,
        "failed_positive_expected_power": power - 2,
        "strict_power_gap": 1,
    }


def certificate() -> dict[str, object]:
    q_deltas = {
        label: q_increment(delta) for label, delta in REACTION_DELTAS.items()
    }
    a_deltas = {
        label: a_increment(delta) for label, delta in REACTION_DELTAS.items()
    }
    payload = {
        "scope": "exact algebra and boundary-tail regression only",
        "supports": [["0", "BC"], ["B", "A", "AB", "2B"]],
        "orientation": [
            "0->BC",
            "BC->0",
            "B->A",
            "A->AB",
            "AB->2B",
            "2B->B",
        ],
        "q_coordinate": "C-A-B",
        "q_increments": q_deltas,
        "a_increments": a_deltas,
        "a_clock_generator": "k1*(a->a+1)+k3*a*(a->a-1)",
        "activation_resistance": 1,
        "nonactivation_positive_resistance": 2,
        "stopped_fourth_power_scaling": stopped_power_scaling(4),
        "local_base_trace_analytic_theorem_certified": False,
        "pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return {**payload, "payload_sha256": sha256(encoded).hexdigest()}


def main() -> None:
    result = certificate()
    assert result["payload_sha256"] == EXPECTED_PAYLOAD_SHA256
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
