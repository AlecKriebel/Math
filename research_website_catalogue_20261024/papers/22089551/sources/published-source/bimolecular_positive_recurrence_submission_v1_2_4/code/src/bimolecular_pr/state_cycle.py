"""Exact population-state witnesses supplied by weak reversibility.

The routines in this module are finite graph checks.  They expose the
elementary lifting used in the manuscript, but software checks are not a
substitute for the universal graph-theoretic proof.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable

from .network import Channel, Network, State, add, falling_factorial, subtract


@dataclass(frozen=True)
class StateCycleWitness:
    """A fired population transition followed by a lifted return path."""

    residual: State
    fired_channel: Channel
    return_channels: tuple[Channel, ...]
    states: tuple[State, ...]


def complex_return_path(network: Network, fired_channel: Channel) -> tuple[Channel, ...]:
    """Find a directed complex path from target back to source.

    Weak reversibility guarantees such a path for every genuine reaction.
    The search is deliberately local to the fired edge, so it also handles
    weakly reversible networks with multiple linkage classes.
    """
    if fired_channel not in network.channels:
        raise ValueError("the fired channel is not part of the network")
    if fired_channel.source == fired_channel.target:
        raise ValueError("a null self-channel is not a population transition")

    start = fired_channel.target
    goal = fired_channel.source
    predecessor: dict[tuple[int, ...], tuple[tuple[int, ...], Channel]] = {}
    seen = {start}
    queue = deque([start])

    while queue and goal not in seen:
        source = queue.popleft()
        for channel in network.channels:
            if channel.source != source or channel.source == channel.target:
                continue
            target = channel.target
            if target in seen:
                continue
            predecessor[target] = (source, channel)
            seen.add(target)
            queue.append(target)

    if goal not in seen:
        raise ValueError("the reaction edge has no directed complex return path")

    reverse_path: list[Channel] = []
    current = goal
    while current != start:
        previous, channel = predecessor[current]
        reverse_path.append(channel)
        current = previous
    return tuple(reversed(reverse_path))


def lifted_return_cycle(
    network: Network,
    state: State,
    fired_channel: Channel,
) -> StateCycleWitness:
    """Construct the population return cycle for one enabled reaction.

    If ``state = residual + fired_channel.source``, the same residual is
    added to every complex on a return path.  Consequently every path edge is
    enabled and the lifted path returns exactly to ``state``.
    """
    if len(state) != len(network.species) or any(value < 0 for value in state):
        raise ValueError("invalid population state")
    if falling_factorial(state, fired_channel.source) == 0:
        raise ValueError("the fired channel is disabled at the supplied state")

    residual = subtract(state, fired_channel.source)
    return_channels = complex_return_path(network, fired_channel)
    current = network.successor(state, fired_channel)
    states = [state, current]

    if current != add(residual, fired_channel.target):
        raise AssertionError("the post-jump residual was not preserved")

    expected_source = fired_channel.target
    for channel in return_channels:
        if channel.source != expected_source:
            raise AssertionError("the complex return path is not contiguous")
        expected_state = add(residual, channel.source)
        if current != expected_state:
            raise AssertionError("the lifted path changed its residual")
        if falling_factorial(current, channel.source) == 0:
            raise AssertionError("a lifted return channel is disabled")
        current = network.successor(current, channel)
        states.append(current)
        expected_source = channel.target

    if current != state or expected_source != fired_channel.source:
        raise AssertionError("the lifted path did not return to its initial state")
    return StateCycleWitness(
        residual=residual,
        fired_channel=fired_channel,
        return_channels=return_channels,
        states=tuple(states),
    )


def finite_transition_graph(
    network: Network,
    states: Iterable[State],
) -> dict[State, frozenset[State]]:
    """Return the population graph on a supplied finite closed state set."""
    state_set = frozenset(states)
    if not state_set:
        raise ValueError("the finite state set must be nonempty")
    adjacency: dict[State, frozenset[State]] = {}
    for state in state_set:
        successors = {
            network.successor(state, channel)
            for channel in network.enabled_channels(state)
        }
        outside = successors - state_set
        if outside:
            raise ValueError(
                f"the supplied state set is not closed; {state} reaches {sorted(outside)}"
            )
        adjacency[state] = frozenset(successors)
    return adjacency


def finite_reachability(
    adjacency: dict[State, frozenset[State]],
    initial: State,
) -> frozenset[State]:
    """Compute reachability in an explicit finite population graph."""
    if initial not in adjacency:
        raise ValueError("initial state is absent from the graph")
    seen = {initial}
    queue = deque([initial])
    while queue:
        current = queue.popleft()
        for successor in adjacency[current]:
            if successor not in seen:
                seen.add(successor)
                queue.append(successor)
    return frozenset(seen)


def finite_accessibility_is_symmetric(
    adjacency: dict[State, frozenset[State]],
) -> bool:
    """Check symmetry of accessibility on an explicit finite graph."""
    reachable = {
        state: finite_reachability(adjacency, state)
        for state in adjacency
    }
    return all(
        (target in reachable[source]) == (source in reachable[target])
        for source in adjacency
        for target in adjacency
    )
