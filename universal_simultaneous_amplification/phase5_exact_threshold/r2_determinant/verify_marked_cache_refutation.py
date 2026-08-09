#!/usr/bin/env python3
"""Independent exact verifier for the eight-vertex marked-cache refutation.

Two implementations are used.

* A full 1,016-state labelled active chain is built directly from the pin
  replacement rule.
* A separate two-label orbit chain is built from canonical representatives.

Both implementations uniformly symmetrize words with fixed pin counts over
QQ.  They agree on the negative q=1 marked-cache comparison and on the
positive inverse-rank comparison for the same pair of pin multisets.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import comb


LabelledState = tuple[int, int]
Orbit = tuple[int, int, int]
Operator = list[dict[int, F]]


def pin_targets(n: int, pin: int, source: int) -> list[tuple[int, F]]:
    if source == pin:
        return [(target, F(1, n - 1)) for target in range(n) if target != pin]
    return [(pin, F(1))]


def labelled_states(n: int) -> list[LabelledState]:
    return [
        (cache, target)
        for target in range(n)
        for cache in range(1, 1 << n)
        if not (cache >> target) & 1
    ]


def labelled_pin_operator(
    n: int, pin: int, states: list[LabelledState]
) -> Operator:
    index = {state: position for position, state in enumerate(states)}
    operator: Operator = []
    for cache, target in states:
        rank = cache.bit_count()
        row: dict[int, F] = {}

        def add(new_cache: int, new_target: int, mass: F) -> None:
            position = index[(new_cache, new_target)]
            row[position] = row.get(position, F(0)) + mass

        for sample, mass in pin_targets(n, pin, target):
            add(cache | (1 << sample), target, mass / 2)
        for source in range(n):
            if not (cache >> source) & 1:
                continue
            removed = cache & ~(1 << source)
            for sample, mass in pin_targets(n, pin, source):
                add(removed | (1 << sample), source, mass / (2 * rank))
        assert sum(row.values(), F(0)) == 1
        operator.append(row)
    return operator


def orbit_states(n: int) -> list[Orbit]:
    ordinary = n - 2
    answer = []
    for mask in range(4):
        marked = mask.bit_count()
        for target_type in range(2):
            if (mask >> target_type) & 1:
                continue
            for ordinary_count in range(ordinary + 1):
                if marked + ordinary_count:
                    answer.append((mask, ordinary_count, target_type))
        for ordinary_count in range(ordinary):
            if marked + ordinary_count:
                answer.append((mask, ordinary_count, 2))
    return answer


def representative(state: Orbit, n: int) -> tuple[frozenset[int], int]:
    mask, ordinary_count, target_type = state
    cache = {label for label in range(2) if (mask >> label) & 1}
    if target_type == 2:
        target = 2
        cache.update(range(3, 3 + ordinary_count))
    else:
        target = target_type
        cache.update(range(2, 2 + ordinary_count))
    assert target not in cache and cache
    assert max(cache | {target}) < n
    return frozenset(cache), target


def orbit_of(cache: frozenset[int], target: int) -> Orbit:
    mask = sum(1 << label for label in cache if label < 2)
    ordinary_count = sum(label >= 2 for label in cache)
    target_type = target if target < 2 else 2
    return mask, ordinary_count, target_type


def orbit_pin_operator(n: int, pin: int, states: list[Orbit]) -> Operator:
    index = {state: position for position, state in enumerate(states)}
    operator: Operator = []
    for state in states:
        cache, target = representative(state, n)
        rank = len(cache)
        row: dict[int, F] = {}

        def add(new_cache: frozenset[int], new_target: int, mass: F) -> None:
            position = index[orbit_of(new_cache, new_target)]
            row[position] = row.get(position, F(0)) + mass

        for sample, mass in pin_targets(n, pin, target):
            add(cache | {sample}, target, mass / 2)
        for source in cache:
            removed = cache - {source}
            for sample, mass in pin_targets(n, pin, source):
                add(removed | {sample}, source, mass / (2 * rank))
        assert sum(row.values(), F(0)) == 1
        operator.append(row)
    return operator


def apply(operator: Operator, vector: list[F]) -> list[F]:
    return [
        sum((mass * vector[target] for target, mass in row.items()), F(0))
        for row in operator
    ]


def dot(row: list[F], column: list[F]) -> F:
    return sum((x * y for x, y in zip(row, column)), F(0))


def fixed_count_controls(
    left: Operator, right: Operator, reward: list[F], total: int
) -> list[list[F]]:
    """Return controls indexed by the number of left-pin occurrences."""

    previous = [reward]
    for time in range(1, total + 1):
        current = []
        for left_count in range(time + 1):
            value = [F(0)] * len(reward)
            if left_count:
                image = apply(left, previous[left_count - 1])
                scale = F(left_count, time)
                value = [x + scale * y for x, y in zip(value, image)]
            if left_count < time:
                image = apply(right, previous[left_count])
                scale = F(time - left_count, time)
                value = [x + scale * y for x, y in zip(value, image)]
            current.append(value)
        previous = current
    return previous


def labelled_initial(n: int, states: list[LabelledState]) -> list[F]:
    N = n - 1
    return [F(cache.bit_count(), n * N * 2 ** (N - 1)) for cache, _ in states]


def orbit_initial(n: int, states: list[Orbit]) -> list[F]:
    N = n - 1
    ordinary = n - 2
    answer = []
    for mask, ordinary_count, target_type in states:
        rank = mask.bit_count() + ordinary_count
        orbit_size = (
            ordinary * comb(ordinary - 1, ordinary_count)
            if target_type == 2
            else comb(ordinary, ordinary_count)
        )
        answer.append(F(orbit_size * rank, n * N * 2 ** (N - 1)))
    assert sum(answer, F(0)) == 1
    return answer


def rank_of_labelled(state: LabelledState) -> int:
    return state[0].bit_count()


def rank_of_orbit(state: Orbit) -> int:
    return state[0].bit_count() + state[1]


def quotient_row_audit() -> None:
    for n in range(3, 6):
        full_states = labelled_states(n)
        full_index = {state: position for position, state in enumerate(full_states)}
        reduced_states = orbit_states(n)
        reduced_index = {
            state: position for position, state in enumerate(reduced_states)
        }
        representatives: dict[Orbit, list[int]] = {
            state: [] for state in reduced_states
        }
        for position, (cache, target) in enumerate(full_states):
            cache_set = frozenset(
                vertex for vertex in range(n) if (cache >> vertex) & 1
            )
            representatives[orbit_of(cache_set, target)].append(position)

        for pin in range(2):
            full = labelled_pin_operator(n, pin, full_states)
            reduced = orbit_pin_operator(n, pin, reduced_states)
            for orbit, source_positions in representatives.items():
                aggregate_rows = []
                for source in source_positions:
                    aggregate = [F(0)] * len(reduced_states)
                    for target, mass in full[source].items():
                        cache, vertex = full_states[target]
                        cache_set = frozenset(
                            label for label in range(n) if (cache >> label) & 1
                        )
                        aggregate[reduced_index[orbit_of(cache_set, vertex)]] += mass
                    aggregate_rows.append(aggregate)
                assert all(row == aggregate_rows[0] for row in aggregate_rows)
                expected = [F(0)] * len(reduced_states)
                for target, mass in reduced[reduced_index[orbit]].items():
                    expected[target] = mass
                assert aggregate_rows[0] == expected
            assert len(full_index) == len(full_states)
    print("PASS (EXACT): independent orbit quotient matches labelled rows, n=3..5")


NEGATIVE_MARKED = -F(
    5097841855133683116602026973677867709383649499615439175346534343452763341123776494668866115269,
    2209253741490523003907776625044372951761360171795984893713024521622498836480000000000000000000000000,
)

POSITIVE_INVERSE_RANK = F(
    25801268944756526477036175355372435803145464088958168680881355283347745154642235159793307444839,
    131839524215120724870881810531207252023269575469496114714332239142007603200000000000000000000000000,
)


def witness_values(
    n: int,
    states,
    left: Operator,
    right: Operator,
    initial: list[F],
    rank_function,
    include_cdf: bool = True,
) -> tuple[F, F, list[F]]:
    N = n - 1
    marked_reward = [F(N - rank_function(state), N - 1) for state in states]
    inverse_reward = [F(1, rank_function(state)) for state in states]
    marked = fixed_count_controls(left, right, marked_reward, 26)
    inverse = fixed_count_controls(left, right, inverse_reward, 26)
    marked_difference = dot(initial, marked[14]) - dot(initial, marked[13])
    inverse_difference = dot(initial, inverse[14]) - dot(initial, inverse[13])

    cdf = []
    if include_cdf:
        for cutoff in range(1, N):
            reward = [F(rank_function(state) <= cutoff) for state in states]
            controls = fixed_count_controls(left, right, reward, 26)
            cdf.append(dot(initial, controls[14]) - dot(initial, controls[13]))
    return marked_difference, inverse_difference, cdf


def bernstein_controls(cdf: list[F]) -> list[F]:
    degree = len(cdf) - 1
    return [
        sum(
            (
                cdf[power] * F(comb(control, power), comb(degree, power))
                for power in range(control + 1)
            ),
            F(0),
        )
        for control in range(degree + 1)
    ]


def refutation_audit() -> None:
    n = 8
    full_states = labelled_states(n)
    full_left = labelled_pin_operator(n, 0, full_states)
    full_right = labelled_pin_operator(n, 1, full_states)
    full_values = witness_values(
        n,
        full_states,
        full_left,
        full_right,
        labelled_initial(n, full_states),
        rank_of_labelled,
        include_cdf=False,
    )

    reduced_states = orbit_states(n)
    reduced_left = orbit_pin_operator(n, 0, reduced_states)
    reduced_right = orbit_pin_operator(n, 1, reduced_states)
    reduced_values = witness_values(
        n,
        reduced_states,
        reduced_left,
        reduced_right,
        orbit_initial(n, reduced_states),
        rank_of_orbit,
    )
    assert full_values[:2] == reduced_values[:2]

    marked_difference, inverse_difference, cdf = reduced_values
    assert marked_difference == NEGATIVE_MARKED < 0
    assert inverse_difference == POSITIVE_INVERSE_RANK > 0
    assert [1 if value > 0 else -1 for value in cdf] == [1, -1, -1, -1, -1, -1]

    controls = bernstein_controls(cdf)
    assert all(value > 0 for value in controls[:-1])
    assert controls[-1] == 6 * marked_difference < 0
    print("EXACTLY REFUTED: all-order marked-cache/PGF Schur order")
    print(f"FULL LABELLED STATES: {len(full_states)}")
    print(f"q=1 marked-cache difference: {marked_difference}")
    print(f"inverse-rank difference on same witness: {inverse_difference}")
    print("OPEN: the integrated inverse-rank standard-sector sign")


if __name__ == "__main__":
    quotient_row_audit()
    refutation_audit()
