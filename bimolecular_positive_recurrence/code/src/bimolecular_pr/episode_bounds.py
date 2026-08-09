from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class EnvelopeBranch:
    branch: str
    maximizer: Fraction


def scalar_envelope_branch(q: Fraction, M: Fraction) -> EnvelopeBranch:
    if q <= 0:
        raise ValueError("q must be positive")
    if M >= -Fraction(1, 1) / q:
        return EnvelopeBranch("endpoint", Fraction(1))
    return EnvelopeBranch("interior", -Fraction(1, 1) / (q * M))


def propagate_symbolic(branches: list[tuple[Fraction, Fraction]]) -> list[EnvelopeBranch]:
    """Classify each exact (q,M) scalar-envelope branch."""
    return [scalar_envelope_branch(q, M) for q, M in branches]


def episode_continuation_probability(source_probability: Fraction, conditional_edge_probability: Fraction) -> Fraction:
    if not (0 <= source_probability <= 1 and 0 < conditional_edge_probability <= 1):
        raise ValueError("invalid probability")
    return source_probability * conditional_edge_probability


def target_following_path_probability(
    phases: list[tuple[Fraction, Fraction]],
) -> Fraction:
    """Exact probability of following every designated edge in a path.

    Each phase is ``(source_probability, conditional_edge_probability)``.
    The empty list is the length-zero path and has probability one.
    """
    probability = Fraction(1)
    for source_probability, conditional_edge_probability in phases:
        probability *= episode_continuation_probability(
            source_probability,
            conditional_edge_probability,
        )
    return probability
