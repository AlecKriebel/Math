#!/usr/bin/env python3
"""Gate-0 audit and replacement of the Phase-IV local interface.

The earlier finite-SCC certificate did not encode target retention.  Phase V
uses a stronger exact object: a designated complex path.  Along that path the
residual is constant, each designated source is literally present, every
conditional edge probability is positive, episode length is bounded by the
number of complexes, and physical duration is uniformly bounded.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import sys
from typing import Sequence

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT))

from src.generator import Reaction  # type: ignore  # noqa:E402
from phase5_source_flag_closure.src.episode_library import (  # type: ignore  # noqa:E402
    EpisodePath,
    lifted_path_states,
)
from phase5_source_flag_closure.src.target_source_residual import (  # type: ignore  # noqa:E402
    aggregate_source_rates,
    increment_ratio,
    nontrivial_reactions,
    residual,
)


@dataclass(frozen=True, slots=True)
class LiftedPathAudit:
    phases: int
    jump_bound: int
    min_conditional_edge_probability: Fraction
    max_coordinate_overshoot: int
    physical_time_bound_coefficient: Fraction


def audit_lifted_path(
    reactions: Sequence[Reaction], residual_vector: Sequence[int], path: EpisodePath
) -> LiftedPathAudit:
    rs = nontrivial_reactions(reactions)
    if not rs:
        raise ValueError("no jump reactions")
    states = lifted_path_states(residual_vector, path)
    rates = aggregate_source_rates(rs)
    phases = [path.start] + [step.target for step in path.steps]
    if len(states) != len(phases):
        raise AssertionError("state/phase mismatch")
    for x, t in zip(states, phases):
        if residual(x, t) != tuple(residual_vector):
            raise AssertionError("designated path changed the residual")
        if t not in rates:
            raise AssertionError("carried target has no nontrivial outgoing edge")
    for x, step in zip(states, path.steps):
        chosen = rs[step.reaction_index]
        if chosen.source != step.source or chosen.target != step.target:
            raise AssertionError("designated reaction index mismatch")
        if not chosen.enabled(x):
            raise AssertionError("target-following reaction is not enabled")
        if increment_ratio(x, step.source, chosen.source) != 1:
            raise AssertionError("designated edge has nonzero residual reward")
        if step.conditional_edge_probability <= 0:
            raise AssertionError("designated edge probability is not positive")

    min_q = min(
        (step.conditional_edge_probability for step in path.steps),
        default=Fraction(1),
    )
    kappa_min = min(r.rate for r in rs)
    jump_bound = path.jump_bound
    # At every phase the current target is enabled, hence at least one edge
    # of rate >= kappa_min has propensity factor >=1.
    physical_coefficient = Fraction(jump_bound, 1) / kappa_min
    return LiftedPathAudit(
        phases=len(phases),
        jump_bound=jump_bound,
        min_conditional_edge_probability=min_q,
        max_coordinate_overshoot=2 * jump_bound,
        physical_time_bound_coefficient=physical_coefficient,
    )


def self_test() -> None:
    reactions = (
        Reaction((0, 0), (1, 1), Fraction(2)),
        Reaction((1, 1), (0, 1), Fraction(3)),
        Reaction((0, 1), (0, 0), Fraction(5)),
    )
    from phase5_source_flag_closure.src.episode_library import shortest_designated_path

    path = shortest_designated_path(reactions, (0, 0), (0, 1))
    cert = audit_lifted_path(reactions, (100, 0), path)
    assert cert.jump_bound == 3
    assert cert.physical_time_bound_coefficient == Fraction(3, 2)


if __name__ == "__main__":
    self_test()
    print("bounded_defect_full_audit.py self-test: OK")
