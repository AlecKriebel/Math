#!/usr/bin/env python3
"""Independent exact finite-cycle diagnostics, never a Brownian limit proof.

Compare a global first-arrival process on all walkers with a separate
order-filtered process which integrates the still-unfinished individual
visit orders at the global observation stopping time. Both use rational
absorbing-chain equations; no submitted implementation is imported.
"""
from collections import deque
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations, product
from math import factorial
from pathlib import Path
import hashlib
import json
import os
import sys

checks = 0
groups = {}


def check(value, name):
    global checks
    if not value:
        raise RuntimeError(name)
    checks += 1
    groups[name] = groups.get(name, 0) + 1


def linear_solve(matrix, rhs):
    n = len(rhs)
    a = [list(row) + [b] for row, b in zip(matrix, rhs)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            raise RuntimeError('singular exact absorbing-chain system')
        a[col], a[pivot] = a[pivot], a[col]
        divisor = a[col][col]
        a[col] = [v / divisor for v in a[col]]
        for row in range(n):
            if row != col and a[row][col]:
                multiple = a[row][col]
                a[row] = [v - multiple * w for v, w in zip(a[row], a[col])]
    return [a[r][-1] for r in range(n)]


def solve_reachable(initial, transitions, terminal):
    """Transition callback returns (probability,state); terminal returns F or None."""
    if terminal(initial) is not None:
        return terminal(initial), 0
    queue = deque([initial])
    seen = {initial}
    edges = {}
    while queue:
        state = queue.popleft()
        edges[state] = transitions(state)
        for probability, destination in edges[state]:
            if probability and terminal(destination) is None and destination not in seen:
                seen.add(destination)
                queue.append(destination)
    states = sorted(seen, key=repr)
    index = {state: n for n, state in enumerate(states)}
    matrix = [[F(0) for _ in states] for _ in states]
    rhs = [F(0) for _ in states]
    for state, row in index.items():
        matrix[row][row] = F(1)
        for probability, destination in edges[state]:
            boundary = terminal(destination)
            if boundary is None:
                matrix[row][index[destination]] -= probability
            else:
                rhs[row] += probability * boundary
    return linear_solve(matrix, rhs)[index[initial]], len(states)


@lru_cache(maxsize=None)
def next_query_probability(n, remaining, start, target):
    """Global killed-chain harmonic equations, not the endpoint-distance formula."""
    sites = [z for z in range(n) if z not in remaining]
    index = {z: i for i, z in enumerate(sites)}
    matrix = [[F(0) for _ in sites] for _ in sites]
    rhs = [F(0) for _ in sites]
    for z, row in index.items():
        matrix[row][row] = F(1)
        for destination in ((z - 1) % n, (z + 1) % n):
            if destination in remaining:
                rhs[row] += F(destination == target, 2)
            else:
                matrix[row][index[destination]] -= F(1, 2)
    return linear_solve(matrix, rhs)[index[start]]


@lru_cache(maxsize=None)
def unfinished_order_probability(n, order, start, phase):
    if phase == len(order):
        return F(1)
    remaining = tuple(sorted(order[phase:]))
    nxt = order[phase]
    return next_query_probability(n, remaining, start, nxt) * unfinished_order_probability(
        n, order, nxt, phase + 1)


def direct_global_ownership(n, starts, queries, desired):
    """All walkers continue; only global first visits record labels."""
    k = len(starts)
    query_index = {z: j for j, z in enumerate(queries)}
    complete = (1 << len(queries)) - 1
    fail = ('FAIL',)

    def terminal(state):
        if state == fail:
            return F(0)
        return F(1) if state[1] == complete else None

    def transitions(state):
        positions, mask = state
        out = []
        for i in range(k):
            for step in (-1, 1):
                new = (positions[i] + step) % n
                j = query_index.get(new)
                if j is not None and not mask & (1 << j) and desired[j] != i:
                    destination = fail
                else:
                    positions2 = positions[:i] + (new,) + positions[i + 1:]
                    mask2 = mask | (1 << j) if j is not None else mask
                    destination = (positions2, mask2)
                out.append((F(1, 2 * k), destination))
        return out

    return solve_reachable((tuple(starts), 0), transitions, terminal)


def filtered_order_global_race(n, starts, queries, desired, orders):
    """Constrain each walker's full order; compare global cumulative times.

    Product generators interleave every physical jump. On completion of the
    global ownership observation, integrate the unobserved suffixes by their
    individual killed-chain harmonic probabilities. This is the finite-state
    analogue of integrating complete individual hitting vectors over cones.
    """
    k = len(starts)
    m = len(queries)
    query_index = {z: j for j, z in enumerate(queries)}
    fail = ('FAIL',)

    def globally_seen(phases):
        return set().union(*(set(order[:phase]) for order, phase in zip(orders, phases)))

    def terminal(state):
        if state == fail:
            return F(0)
        positions, phases = state
        if len(globally_seen(phases)) != m:
            return None
        answer = F(1)
        for position, phase, order in zip(positions, phases, orders):
            answer *= unfinished_order_probability(n, order, position, phase)
        return answer

    def transitions(state):
        positions, phases = state
        seen = globally_seen(phases)
        out = []
        for i in range(k):
            for step in (-1, 1):
                new = (positions[i] + step) % n
                phase = phases[i]
                order = orders[i]
                if new in order[phase:]:
                    if new != order[phase] or (new not in seen and desired[query_index[new]] != i):
                        out.append((F(1, 2 * k), fail))
                        continue
                    phase += 1
                destination = (positions[:i] + (new,) + positions[i + 1:],
                               phases[:i] + (phase,) + phases[i + 1:])
                out.append((F(1, 2 * k), destination))
        return out

    return solve_reachable((tuple(starts), (0,) * k), transitions, terminal)


def model_checks():
    records = []
    fixtures = [(4, (0, 2), (1, 3)),
                (5, (0, 2), (1, 3)),
                (5, (0, 2), (1, 4)),
                (4, (0, 1, 2), (3,))]
    for n, starts, queries in fixtures:
        probability_sum = F(0)
        entries = []
        orders = tuple(permutations(queries))
        for desired in product(range(len(starts)), repeat=len(queries)):
            direct, states = direct_global_ownership(n, starts, queries, desired)
            filtered = F(0)
            filtered_states = 0
            for selected in product(orders, repeat=len(starts)):
                p, count = filtered_order_global_race(n, starts, queries, desired, selected)
                filtered += p
                filtered_states += count
            check(direct == filtered, 'full_joint_owner_probabilities_match')
            check(F(0) <= direct <= F(1), 'owner_probability_bounds')
            probability_sum += direct
            entries.append({'owner_vector_zero_based': desired, 'probability': str(direct),
                            'direct_transient_states': states,
                            'filtered_transient_states_total': filtered_states})
        check(probability_sum == 1, 'joint_owner_normalization')
        records.append({'cycle_sites': n, 'starts': starts, 'queries': queries,
                        'owner_entries': entries})
    return records


def independent_poisson_moment_checks():
    """Exact coefficient equality for arbitrary correlated ownership fields."""
    pieces = [F(1, 7), F(2, 7), F(4, 7)]
    patterns = [(0, 1, 2), (2, 2, 0), (1, 0, 1), (0, 0, 0)]
    masses = [F(1, 11), F(3, 11), F(5, 11), F(2, 11)]
    theta = [F(2, 3), F(5, 4), F(7, 3)]
    maximum = max(theta)
    moments = []
    survival_moments = []
    for m in range(8):
        moment = sum(weight * sum(width * theta[label] for width, label in zip(pieces, field)) ** m
                     for weight, field in zip(masses, patterns))
        survival = sum(weight * sum(width * (1 - theta[label] / maximum)
                                  for width, label in zip(pieces, field)) ** m
                       for weight, field in zip(masses, patterns))
        tensor = F(0)
        positive_tensor = F(0)
        for locations in product(range(len(pieces)), repeat=m):
            spatial_mass = F(1)
            for location in locations:
                spatial_mass *= pieces[location]
            joint_law = {}
            for weight, field in zip(masses, patterns):
                labels = tuple(field[location] for location in locations)
                joint_law[labels] = joint_law.get(labels, F(0)) + weight
            for labels, joint_probability in joint_law.items():
                value = F(1)
                positive_value = F(1)
                for label in labels:
                    value *= theta[label]
                    positive_value *= 1 - theta[label] / maximum
                tensor += spatial_mass * joint_probability * value
                positive_tensor += spatial_mass * joint_probability * positive_value
        check(tensor == moment, 'arbitrary_correlated_tensor_moments')
        check(positive_tensor == survival, 'poisson_query_positive_coefficients')
        moments.append(moment)
        survival_moments.append(survival)
        # coefficient of t^m in exp(-t T) sum_n (t T)^n E(1-Z/T)^n/n!
        coefficient = sum((-maximum) ** (m - n) * maximum ** n * survival_moments[n]
                          / (factorial(m - n) * factorial(n)) for n in range(m + 1))
        check(coefficient == (-1) ** m * moment / factorial(m),
              'positive_poisson_and_alternating_moment_series_identical')
    return {'nonuniform_piece_lengths': list(map(str, pieces)),
            'correlated_pattern_weights': list(map(str, masses)),
            'theta': list(map(str, theta)), 'maximum_degree': 7,
            'moment_values': list(map(str, moments))}


def substitution_controls():
    # Feasible two-target visit orders on the circle: p=(0,1/2), x=(1/4,3/4).
    # Walk 0 visits x0 then x1, walk 1 visits x1 then x0.
    increments = ((F(3), F(4)), (F(5), F(1)))
    orders = ((0, 1), (1, 0))
    physical = [[F(0), F(0)] for _ in increments]
    reset = [[F(0), F(0)] for _ in increments]
    for i, order in enumerate(orders):
        clock = F(0)
        for r, query in enumerate(order):
            clock += increments[i][r]
            physical[i][query] = clock
            reset[i][query] = increments[i][r]
    actual_owner = tuple(min(range(2), key=lambda i: physical[i][j]) for j in range(2))
    reset_owner = tuple(min(range(2), key=lambda i: reset[i][j]) for j in range(2))
    check(actual_owner == (0, 1) and reset_owner == (1, 0),
          'local_reset_clock_substitution_falsified')
    # On a cycle, a path starting outside three consecutive targets cannot
    # first reach the middle target without first reaching an outer target.
    impossible = next_query_probability(8, (1, 2, 3), 0, 2)
    check(impossible == 0, 'impossible_middle_first_order')
    # Each of the three separate one-target clocks is nondegenerate, so an
    # independently resampled triple would assign positive probability to
    # that impossible event. Such a substitution breaks within-walker dependence.
    # Singleton endpoint undercount is detected directly by harmonic mass.
    singleton = next_query_probability(8, (3,), 0, 3)
    check(singleton == 1, 'singleton_full_mass')
    return {'physical_hitting_times': [[str(v) for v in row] for row in physical],
            'reset_increments_mislabeled_as_times': [[str(v) for v in row] for row in reset],
            'actual_owner': actual_owner, 'wrong_reset_owner': reset_owner,
            'impossible_middle_first_probability': str(impossible),
            'singleton_probability': str(singleton)}


def main():
    begin = datetime.now(timezone.utc).isoformat()
    records = model_checks()
    moments = independent_poisson_moment_checks()
    controls = substitution_controls()
    root = Path(__file__).resolve().parent
    proof = root.parent / 'reference' / 'JOINT_LAW.md'
    result = {'schema': 'pr141-independent-probability-model-diagnostics/v1',
              'verdict': 'PASS_EXACT_FINITE_MODEL_DIAGNOSTICS',
              'scope': 'Finite-cycle exact diagnostics and an independent Poisson-query identity; no Brownian limit, quadrature, or priority result claimed.',
              'actual_pid': os.getpid(), 'started_utc': begin,
              'finished_utc': datetime.now(timezone.utc).isoformat(),
              'python': sys.version, 'optimized': bool(sys.flags.optimize),
              'checks': checks, 'groups': groups,
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'original_proof_sha256': hashlib.sha256(proof.read_bytes()).hexdigest(),
              'global_model_checks': records,
              'poisson_query_checks': moments, 'substitution_controls': controls}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
