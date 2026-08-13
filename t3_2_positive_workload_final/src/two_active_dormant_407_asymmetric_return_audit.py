"""Independent exact audit of the frozen asymmetric hard-333 repair.

This module is claim-negative.  It replays one exact generalized-Family-II
template and the paid exact-return cycle that invalidates the fixed
``z_1**J`` base-step inequality in (7.16i) of the frozen theorem note.  It
does not modify or promote any analytic, pair-level, or global flag.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

import two_active_dormant_407_certificate as dormant


ROOT = Path(__file__).resolve().parents[1]
FROZEN_HASHES = {
    "theorem": "d7e3ba1548b8b5a3396f9b9aa5de458fd792039b10f780e57623696337ce64c7",
    "source": "098969ceeef5589a5a17f000901f43f168583015ac435de8c025add5c412e6a2",
    "tests": "ee51167d4948b8fff00d1ce4ae990d61aada1692656b1495d1e1e456359f8804",
}
FROZEN_PATHS = {
    "theorem": ROOT / "research_notes/two_active_dormant_407_resolvent_theorem.md",
    "source": ROOT / "src/two_active_dormant_407_certificate.py",
    "tests": ROOT / "tests/test_two_active_dormant_407_certificate.py",
}

VECTORS = {
    "0": (0, 0, 0),
    "U": (1, 0, 0),
    "2U": (2, 0, 0),
    "I": (0, 0, 1),
    "2I": (0, 0, 2),
    "UI": (1, 0, 1),
    "VI": (0, 1, 1),
}


def _file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _fire(
    state: tuple[int, int, int, int],
    source: str,
    target: str,
    paid: bool,
) -> tuple[int, int, int, int]:
    """Fire one normalized physical reaction in coordinates ``U,V,I,J``."""

    u, v, i, j = state
    source_vector = VECTORS[source]
    target_vector = VECTORS[target]
    if (
        u < source_vector[0]
        or v < source_vector[1]
        or i < source_vector[2]
    ):
        raise AssertionError(f"disabled source {source} at {state}")
    return (
        u + target_vector[0] - source_vector[0],
        v + target_vector[1] - source_vector[1],
        i + target_vector[2] - source_vector[2],
        j + int(paid),
    )


def _relative_state(
    state: tuple[int, int, int, int], n: int
) -> list[int]:
    u, v, i, j = state
    return [u, i, v - n, j]


def growth_word_states(n: int = 10**6) -> tuple[list[int], ...]:
    """A reachable no-service word taking ``(U,J)=(u,j)`` to ``(u+1,j+3)``."""

    word = (
        ("2U", "VI", False),
        ("I", "2I", True),
        ("VI", "2U", False),
        ("2U", "VI", True),
        ("2I", "UI", True),
        ("VI", "2U", False),
    )
    state = (2, n, 0, 0)
    states = [_relative_state(state, n)]
    for source, target, paid in word:
        state = _fire(state, source, target, paid)
        states.append(_relative_state(state, n))
    expected = (
        [2, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 2, 1, 1],
        [2, 1, 0, 1],
        [0, 2, 1, 2],
        [1, 1, 1, 3],
        [3, 0, 0, 3],
    )
    assert tuple(states) == expected
    return tuple(states)


def paid_exact_return_states(
    n: int = 10**6, u: int = 10, j: int = 7
) -> tuple[list[int], ...]:
    """The exact base return that increments only the paid counter ``J``."""

    word = (
        ("2U", "VI", False),
        ("2U", "VI", True),
        ("VI", "2U", False),
        ("VI", "2U", False),
    )
    state = (u, n, 0, j)
    states = [_relative_state(state, n)]
    for source, target, paid in word:
        state = _fire(state, source, target, paid)
        states.append(_relative_state(state, n))
    assert states[0] == [u, 0, 0, j]
    assert states[-1] == [u, 0, 0, j + 1]
    return tuple(states)


def first_nonself_cycle_probability(n: int, u: int) -> Fraction:
    """Lower bound from repeated simple proper self-macros.

    All rates are one.  At a no-fast base, a simple ``2U->VI->2U`` return
    may repeat arbitrarily.  This function gives the probability that the
    first outcome other than such a simple return is the exact paid return

        2U->VI, 2U->VI, VI->2U, VI->2U.

    Every other outcome is treated as failure, so this is a lower bound on
    the continuation mass relevant to the hostile audit.
    """

    if u < 6:
        raise ValueError("u must be at least six")
    base_proper = u * (u - 1)
    p_open = Fraction(base_proper, base_proper + 1)

    # After the first proper entry: (U,V,I)=(u-2,n+1,1).
    fast_1 = n + 1
    duplicate = (u - 2) * (u - 3)
    lower_paid_1 = u  # rates 0->I, I->2I, and UI->0
    total_1 = fast_1 + duplicate + lower_paid_1
    p_simple_return = p_open * Fraction(fast_1, total_1)

    # After the duplicate: (U,V,I)=(u-4,n+2,2).
    fast_2 = 2 * (n + 2)
    duplicate_2 = (u - 4) * (u - 5)
    lower_paid_2 = 2 * u - 3
    total_2 = fast_2 + duplicate_2 + lower_paid_2

    p_paid_exact_return = (
        p_open
        * Fraction(duplicate, total_1)
        * Fraction(fast_2, total_2)
        * Fraction(fast_1, total_1)
    )
    return p_paid_exact_return / (1 - p_simple_return)


def audit() -> dict[str, object]:
    observed_hashes = {
        name: _file_sha256(path) for name, path in FROZEN_PATHS.items()
    }
    assert observed_hashes == FROZEN_HASHES

    support_matches = tuple(
        row
        for row in dormant.generalized_support_templates()
        if set(row["proper"]) == {"2U", "VI"}
        and set(row["lower"]) == {"0", "I", "2I", "UI"}
    )
    physical_matches = tuple(
        row
        for row in dormant.generalized_normalized_rows()
        if set(row["proper"]) == {"2U", "VI"}
        and set(row["lower"]) == {"0", "I", "2I", "UI"}
    )
    assert len(support_matches) == 1
    assert len(physical_matches) == 6
    assert Counter(row["spectator_cap"] for row in physical_matches) == {
        0: 2,
        1: 2,
        2: 2,
    }

    probability_table = []
    previous = Fraction(0)
    for m in (10**3, 10**4, 10**5, 10**6):
        n = m**3
        u = m // 4
        probability = first_nonself_cycle_probability(n, u)
        assert probability > previous
        previous = probability
        probability_table.append(
            {
                "m": m,
                "n=m^3": n,
                "u=floor(m/4)": u,
                "probability": float(probability),
            }
        )
    assert previous > Fraction(999, 1000)

    certificate = dormant.certificate()
    flags = {
        name: certificate[name]
        for name in (
            "analytic_theorem_independently_audited",
            "pair_level_recurrence_certified",
            "global_t3_2_certified",
        )
    }
    assert flags == {
        "analytic_theorem_independently_audited": False,
        "pair_level_recurrence_certified": False,
        "global_t3_2_certified": False,
    }

    return {
        "audited_snapshot_sha256": observed_hashes,
        "exact_template": support_matches[0],
        "physical_rows": len(physical_matches),
        "spectator_cap_histogram": {"0": 2, "1": 2, "2": 2},
        "strong_orientations": {
            "proper": ["2U->VI", "VI->2U"],
            "lower": ["0->I", "I->2I", "2I->UI", "UI->0"],
            "rates": "all one",
        },
        "growth_word_states_U_I_R_J": growth_word_states(),
        "paid_exact_return_states_U_I_R_J": paid_exact_return_states(),
        "contracted_cycle_probability": probability_table,
        "asymptotic": (
            "for u=c*n^(1/3), q_n~u^4/(n+u^4)->1"
        ),
        "mark_ratio_on_exact_return": "Psi(endpoint)/Psi(start)=z1>1",
        "failed_display": "intended (7.16i), hence (7.16k)-(8.7) unproved",
        "scope": "proof failure, not a recurrence or T3-2 counterexample",
        "repair_case_split": {
            "reset": (
                "reset local J,I,R at every physical no-fast base return"
            ),
            "dominant_U4_over_n_event": "exact self-return; delete it",
            "remaining_d0_outward_rate": "O(U^3/n), with a service cut",
            "remaining_d1_outward_ratio": "O(U^2/n)=O(n^(-1/3))",
            "larger_proper_support": "fixed-probability strong cut per excursion",
            "required_missing_argument": (
                "second killed base resolvent for the perturbed nonself U-kernel"
            ),
        },
        "certification_flags": flags,
        "verdict": "FAIL-as-written",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
