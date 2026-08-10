"""Finite certificate for a shell-Poisson corrector sign reversal.

The top linkage is the unit-rate reversible pair

    2A <-> B + C,

and the lower linkage is the unit-rate directed cycle

    0 -> A + B -> A -> 2B -> 0.

For one finite top shell this module constructs the conditioned product-
Poisson stationary law, evaluates ``g = L_R F``, solves

    Q_T chi = bar(g) - g,       pi(chi) = 0,

by the exact birth--death conductance recurrence, and evaluates ``L_R chi``
at a specified state.  Decimal arithmetic is used only for square roots and
logarithms in the shell entropy.  The finite state-space recurrences and
propensities are otherwise exact.

This is a local calculation about one proposed corrector normalization.  It
does not assert recurrence or nonrecurrence of the reaction network, and it
does not rule out a different shell-dependent additive gauge for ``chi``.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from hashlib import sha256
import json


Vector = tuple[int, int, int]
State = tuple[int, int, int]
Invariant = tuple[int, int]
Edge = tuple[str, str]

ZERO = "0"
A = "A"
TWO_B = "2B"
AB = "AB"

COMPLEXES: dict[str, Vector] = {
    ZERO: (0, 0, 0),
    A: (1, 0, 0),
    TWO_B: (0, 2, 0),
    AB: (1, 1, 0),
}

LOWER_CYCLE: tuple[Edge, ...] = (
    (ZERO, AB),
    (AB, A),
    (A, TWO_B),
    (TWO_B, ZERO),
)

DEFAULT_PRECISION = 90
EXPECTED_CERTIFICATE_SHA256 = (
    "cede254774e6ae78bb3712c5d48ace13f95c7474a008fbc7e2cbe5aba605f89d"
)


@dataclass(frozen=True)
class ShellSolution:
    """Stationary law and mean-zero Poisson solution on one top fiber."""

    invariant: Invariant
    states: tuple[State, ...]
    stationary: tuple[Decimal, ...]
    g: tuple[Decimal, ...]
    average_g: Decimal
    chi: tuple[Decimal, ...]
    edge_gradients: tuple[Decimal, ...]
    max_poisson_residual: Decimal


def invariant(state: State) -> Invariant:
    """Return the two invariants U=A+2B and V=A+2C."""

    a, b, c = state
    return a + 2 * b, a + 2 * c


def _reaction_vector(edge: Edge) -> Vector:
    source = COMPLEXES[edge[0]]
    target = COMPLEXES[edge[1]]
    return tuple(target[i] - source[i] for i in range(3))


def _add(state: State, vector: Vector) -> State:
    return tuple(state[i] + vector[i] for i in range(3))


def _falling_propensity(state: State, source: Vector) -> int:
    result = 1
    for population, count in zip(state, source):
        if population < count:
            return 0
        if count == 1:
            result *= population
        elif count == 2:
            result *= population * (population - 1)
    return result


def _entropy_term(value: Decimal) -> Decimal:
    if not value:
        return Decimal(1)
    return value * (value.ln() - Decimal(1)) + Decimal(1)


def entropy_center(q: Invariant) -> tuple[Decimal, Decimal, Decimal]:
    """Continuous entropy center on the ``2A <-> B+C`` fiber."""

    u, v = map(Decimal, q)
    if u and v:
        discriminant = u * u + Decimal(14) * u * v + v * v
        a = (discriminant.sqrt() - u - v) / Decimal(6)
    else:
        a = Decimal(0)
    return a, (u - a) / Decimal(2), (v - a) / Decimal(2)


def shell_entropy(q: Invariant) -> Decimal:
    return sum((_entropy_term(value) for value in entropy_center(q)), Decimal(0))


def _states(q: Invariant) -> tuple[State, ...]:
    u, v = q
    if u < 0 or v < 0 or (u - v) % 2:
        raise ValueError(f"empty top fiber for invariant {q}")
    return tuple(
        (a, (u - a) // 2, (v - a) // 2)
        for a in range(u % 2, min(u, v) + 1, 2)
    )


def _stationary_law(states: tuple[State, ...]) -> tuple[Decimal, ...]:
    """Unit-rate conditioned product-Poisson law via detailed balance."""

    weights = [Decimal(1)]
    for a, b, c in states[:-1]:
        # The next state has (A,B,C)=(a+2,b-1,c-1).
        ratio = Decimal(b * c) / Decimal((a + 2) * (a + 1))
        weights.append(weights[-1] * ratio)
    total = sum(weights, Decimal(0))
    return tuple(weight / total for weight in weights)


def _lower_drift_values(
    q: Invariant,
    states: tuple[State, ...],
) -> tuple[Decimal, ...]:
    base = shell_entropy(q)
    terms: list[tuple[Vector, Decimal]] = []
    for edge in LOWER_CYCLE:
        source = COMPLEXES[edge[0]]
        jump = _reaction_vector(edge)
        dq = jump[0] + 2 * jump[1], jump[0] + 2 * jump[2]
        target_q = q[0] + dq[0], q[1] + dq[1]
        terms.append((source, shell_entropy(target_q) - base))
    return tuple(
        sum(
            (
                Decimal(_falling_propensity(state, source)) * increment
                for source, increment in terms
            ),
            Decimal(0),
        )
        for state in states
    )


def solve_shell(q: Invariant) -> ShellSolution:
    """Solve the stationary mean-zero Poisson equation on one fiber."""

    states = _states(q)
    stationary = _stationary_law(states)
    g = _lower_drift_values(q, states)
    average = sum(
        (probability * value for probability, value in zip(stationary, g)),
        Decimal(0),
    )
    forcing = tuple(average - value for value in g)

    # In increasing-A order, lambda moves a -> a+2 by BC -> 2A and mu moves
    # a -> a-2 by 2A -> BC.
    birth = tuple(Decimal(b * c) for _, b, c in states)
    death = tuple(Decimal(a * (a - 1)) for a, _, _ in states)
    size = len(states)
    mode = max(range(size), key=stationary.__getitem__)

    # edge_gradients[k] = chi[k] - chi[k-1] for k >= 1.  The left-tail and
    # right-tail conductance recurrences avoid subtracting tiny probabilities.
    edge_gradients = [Decimal(0) for _ in states]
    left_cumulative = Decimal(0)
    for index in range(mode):
        if index == 0:
            left_cumulative = forcing[index]
        else:
            left_cumulative = (
                forcing[index]
                + death[index] / birth[index - 1] * left_cumulative
            )
        edge_gradients[index + 1] = left_cumulative / birth[index]

    right_cumulative = Decimal(0)
    for index in range(size - 1, mode, -1):
        if index == size - 1:
            right_cumulative = forcing[index]
        else:
            right_cumulative = (
                forcing[index]
                + birth[index] / death[index + 1] * right_cumulative
            )
        edge_gradients[index] = -right_cumulative / death[index]

    chi = [Decimal(0) for _ in states]
    for index in range(1, size):
        chi[index] = chi[index - 1] + edge_gradients[index]
    chi_mean = sum(
        (probability * value for probability, value in zip(stationary, chi)),
        Decimal(0),
    )
    chi = [value - chi_mean for value in chi]

    residuals: list[Decimal] = []
    for index in range(size):
        q_chi = Decimal(0)
        if index + 1 < size:
            q_chi += birth[index] * (chi[index + 1] - chi[index])
        if index:
            q_chi += death[index] * (chi[index - 1] - chi[index])
        residuals.append(abs(q_chi - forcing[index]))

    return ShellSolution(
        invariant=q,
        states=states,
        stationary=stationary,
        g=g,
        average_g=average,
        chi=tuple(chi),
        edge_gradients=tuple(edge_gradients),
        max_poisson_residual=max(residuals, default=Decimal(0)),
    )


def _chi_at(
    q: Invariant,
    state: State,
    cache: dict[Invariant, ShellSolution],
) -> Decimal:
    solution = cache.get(q)
    if solution is None:
        solution = solve_shell(q)
        cache[q] = solution
    parity = q[0] % 2
    index = (state[0] - parity) // 2
    if index < 0 or index >= len(solution.states):
        raise ValueError(f"state {state} does not lie on fiber {q}")
    if solution.states[index] != state:
        raise ValueError(f"state {state} does not lie on fiber {q}")
    return solution.chi[index]


def _decimal_string(value: Decimal, places: int = 60) -> str:
    return format(value, f".{places}f")


def finite_counterexample(
    n: int = 4,
    precision: int = DEFAULT_PRECISION,
) -> dict[str, object]:
    """Return the deterministic finite-shell sign-reversal calculation."""

    if n < 2:
        raise ValueError("n must be at least two")
    with localcontext() as context:
        context.prec = precision

        stationary_center = (n**3, n, n**5)
        q = invariant(stationary_center)
        evaluation_state = (
            n,
            (q[0] - n) // 2,
            (q[1] - n) // 2,
        )

        cache: dict[Invariant, ShellSolution] = {}
        base_solution = solve_shell(q)
        cache[q] = base_solution
        base_chi = _chi_at(q, evaluation_state, cache)

        contributions: list[dict[str, object]] = []
        lower_corrector_drift = Decimal(0)
        lower_propensity = 0
        for edge in LOWER_CYCLE:
            source = COMPLEXES[edge[0]]
            rate = _falling_propensity(evaluation_state, source)
            lower_propensity += rate
            jump = _reaction_vector(edge)
            target_state = _add(evaluation_state, jump)
            target_q = invariant(target_state)
            increment = _chi_at(target_q, target_state, cache) - base_chi
            contribution = Decimal(rate) * increment
            lower_corrector_drift += contribution
            contributions.append(
                {
                    "edge": f"{edge[0]}->{edge[1]}",
                    "source_propensity": rate,
                    "chi_increment": _decimal_string(increment),
                    "drift_contribution": _decimal_string(contribution),
                }
            )

        a, b, c = evaluation_state
        top_propensity = a * (a - 1) + b * c
        corrected_drift = base_solution.average_g + lower_corrector_drift
        maximum_residual = max(
            solution.max_poisson_residual for solution in cache.values()
        )

        return {
            "n": n,
            "stationary_center": list(stationary_center),
            "invariant": list(q),
            "evaluation_state": list(evaluation_state),
            "base_fiber_size": len(base_solution.states),
            "stationary_average_g": _decimal_string(base_solution.average_g),
            "lower_corrector_drift": _decimal_string(lower_corrector_drift),
            "corrected_drift": _decimal_string(corrected_drift),
            "top_propensity": top_propensity,
            "lower_propensity": lower_propensity,
            "top_to_lower_propensity_ratio": _decimal_string(
                Decimal(top_propensity) / Decimal(lower_propensity)
            ),
            "reaction_contributions": contributions,
            "maximum_poisson_residual": format(maximum_residual, ".6E"),
        }


def asymptotic_fields() -> dict[str, object]:
    """Analytic asymptotic fields associated with the certified family."""

    return {
        "stationary_center": ["N^3", "N", "N^5"],
        "invariant": ["N^3+2N", "N^3+2N^5"],
        "evaluation_state": [
            "N",
            "(N^3+N)/2",
            "N^5+(N^3-N)/2",
        ],
        "stationary_average_g": "-(1+o(1)) N^4 log N",
        "dominant_2B_corrector_increment": "(5+o(1)) log N / N^2",
        "lower_corrector_drift": "(5/4+o(1)) N^4 log N",
        "corrected_drift": "(1/4+o(1)) N^4 log N",
        "top_propensity": "(1/2+o(1)) N^8",
        "lower_propensity": "(1/4+o(1)) N^6",
        "top_to_lower_propensity_ratio": "(2+o(1)) N^2",
        "status": (
            "recorded analytic expansion of the exact conductance recurrence; "
            "the finite Decimal certificate is the machine-checked claim"
        ),
    }


def certificate() -> dict[str, object]:
    payload: dict[str, object] = {
        "claim_scope": (
            "finite canonical mean-zero shell-Poisson corrector calculation; "
            "no recurrence or nonrecurrence claim and no claim against other gauges"
        ),
        "top_linkage": ["2A->BC", "BC->2A"],
        "lower_cycle": [f"{source}->{target}" for source, target in LOWER_CYCLE],
        "rates": "all unit",
        "poisson_equation": "Q_T chi = stationary_average_g - g",
        "normalization": "stationary mean of chi equals zero on every shell",
        "finite_counterexample": finite_counterexample(),
        "asymptotic_family": asymptotic_fields(),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = sha256(encoded).hexdigest()
    return payload


def self_test() -> None:
    result = certificate()
    finite = result["finite_counterexample"]
    assert isinstance(finite, dict)
    assert Decimal(finite["stationary_average_g"]) < 0
    assert Decimal(finite["lower_corrector_drift"]) > 0
    assert Decimal(finite["corrected_drift"]) > 0
    assert finite["top_propensity"] > 20 * finite["lower_propensity"]
    assert Decimal(finite["maximum_poisson_residual"]) < Decimal("1e-75")
    assert result["certificate_sha256"] == EXPECTED_CERTIFICATE_SHA256


if __name__ == "__main__":
    self_test()
    print(json.dumps(certificate(), indent=2, sort_keys=True))
