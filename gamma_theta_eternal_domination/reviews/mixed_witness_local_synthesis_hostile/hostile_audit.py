#!/usr/bin/env python3
"""Independent hostile audit of the mixed-witness bounded synthesis.

This checker deliberately does not import the search program.  It rebuilds
the labeled graph universes, domination/independence tests, one-guard safe
kernels, and base-cube search from the literal definitions.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[2]
SOURCE = (
    CAMPAIGN
    / "math/working/mixed_witness_local_synthesis"
    / "mixed_witness_local_synthesis.py"
)
RESULT_DIR = CAMPAIGN / "results/mixed_witness_local_synthesis"

LABELS_8 = ("a", "b", "c", "x0", "x1", "x2", "x3", "w")
S_VERTICES = (0, 1, 2)
T_VERTICES = (7, 4, 5)

FIXED_EDGES = frozenset(
    {
        (0, 3),
        (0, 4),
        (2, 4),
        (1, 5),
        (2, 5),
        (1, 6),
        (3, 5),
        (3, 6),
        (4, 6),
    }
)
FIXED_NONEDGES = frozenset(
    {
        (0, 1),
        (0, 2),
        (1, 2),
        (3, 4),
        (4, 5),
        (5, 6),
        (4, 7),
        (5, 7),
    }
)
POSITIVE = (
    (3, 0),
    (4, 0),
    (4, 2),
    (5, 1),
    (5, 2),
    (6, 1),
)
NEGATIVE = (
    (3, 1),
    (3, 2),
    (4, 1),
    (5, 0),
    (6, 0),
    (6, 2),
)


def bits(vertices: tuple[int, ...] | list[int]) -> int:
    answer = 0
    for vertex in vertices:
        answer |= 1 << vertex
    return answer


S_STATE = bits(list(S_VERTICES))
T_STATE = bits(list(T_VERTICES))


def direct_swap(attacked: int, guard: int) -> int:
    return (S_STATE & ~(1 << guard)) | (1 << attacked)


POSITIVE_STATES = tuple(direct_swap(*pair) for pair in POSITIVE)
NEGATIVE_STATES = tuple(direct_swap(*pair) for pair in NEGATIVE)


def labels(order: int) -> tuple[str, ...]:
    return LABELS_8 if order == 8 else LABELS_8 + ("y",)


def unknown_pairs(order: int) -> tuple[tuple[int, int], ...]:
    return tuple(
        pair
        for pair in itertools.combinations(range(order), 2)
        if pair not in FIXED_EDGES and pair not in FIXED_NONEDGES
    )


def rows_for_mask(order: int, mask: int) -> tuple[int, ...]:
    rows = [1 << vertex for vertex in range(order)]
    for left, right in FIXED_EDGES:
        rows[left] |= 1 << right
        rows[right] |= 1 << left
    for index, (left, right) in enumerate(unknown_pairs(order)):
        if mask & (1 << index):
            rows[left] |= 1 << right
            rows[right] |= 1 << left
    return tuple(rows)


def covered(rows: tuple[int, ...], state: int) -> int:
    answer = 0
    remaining = state
    while remaining:
        singleton = remaining & -remaining
        remaining ^= singleton
        answer |= rows[singleton.bit_length() - 1]
    return answer


def dominates(rows: tuple[int, ...], state: int) -> bool:
    return covered(rows, state) == (1 << len(rows)) - 1


def is_independent(rows: tuple[int, ...], state: int) -> bool:
    remaining = state
    while remaining:
        singleton = remaining & -remaining
        remaining ^= singleton
        vertex = singleton.bit_length() - 1
        if rows[vertex] & remaining:
            return False
    return True


def exact_alpha(rows: tuple[int, ...]) -> int:
    order = len(rows)
    for size in range(order, 0, -1):
        for vertices in itertools.combinations(range(order), size):
            if is_independent(rows, bits(list(vertices))):
                return size
    raise AssertionError("empty graph has positive order")


def exact_gamma(rows: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    order = len(rows)
    for size in range(1, order + 1):
        for vertices in itertools.combinations(range(order), size):
            if dominates(rows, bits(list(vertices))):
                return size, vertices
    raise AssertionError("the full vertex set dominates")


def has_independent_four(rows: tuple[int, ...]) -> bool:
    for vertices in itertools.combinations(range(len(rows)), 4):
        if is_independent(rows, bits(list(vertices))):
            return True
    return False


def has_small_dominator(rows: tuple[int, ...]) -> bool:
    order = len(rows)
    for size in (1, 2):
        for vertices in itertools.combinations(range(order), size):
            if dominates(rows, bits(list(vertices))):
                return True
    return False


def is_connected(rows: tuple[int, ...]) -> bool:
    reached = 1
    while True:
        expanded = reached
        for vertex, row in enumerate(rows):
            if reached & (1 << vertex):
                expanded |= row
        if expanded == reached:
            return reached == (1 << len(rows)) - 1
        reached = expanded


def forced_unknown(
    order: int,
    masks: list[int],
) -> dict[str, list[list[str]]]:
    names = labels(order)
    edges: list[list[str]] = []
    nonedges: list[list[str]] = []
    if masks:
        for index, (left, right) in enumerate(unknown_pairs(order)):
            flag = 1 << index
            if all(mask & flag for mask in masks):
                edges.append([names[left], names[right]])
            if all(not mask & flag for mask in masks):
                nonedges.append([names[left], names[right]])
    return {"edges": edges, "nonedges": nonedges}


def triple_states(order: int) -> tuple[int, ...]:
    return tuple(
        bits(list(vertices))
        for vertices in itertools.combinations(range(order), 3)
    )


def legal_successors(
    rows: tuple[int, ...],
    state: int,
    attacked: int,
) -> tuple[int, ...]:
    answer: list[int] = []
    occupied = state
    attacked_bit = 1 << attacked
    while occupied:
        guard_bit = occupied & -occupied
        occupied ^= guard_bit
        guard = guard_bit.bit_length() - 1
        if rows[guard] & attacked_bit:
            answer.append((state ^ guard_bit) | attacked_bit)
    return tuple(answer)


def safe_kernel(
    rows: tuple[int, ...],
    size: int,
    banned: frozenset[int] = frozenset(),
) -> tuple[frozenset[int], tuple[int, ...], int]:
    """Synchronous greatest fixed point, rebuilt from literal obligations."""
    order = len(rows)
    active = {
        bits(list(vertices))
        for vertices in itertools.combinations(range(order), size)
        if bits(list(vertices)) not in banned
        and dominates(rows, bits(list(vertices)))
    }
    initial = len(active)
    waves: list[int] = []
    while active:
        doomed: set[int] = set()
        frozen = frozenset(active)
        for state in frozen:
            for attacked in range(order):
                if state & (1 << attacked):
                    continue
                if not any(
                    successor in frozen
                    for successor in legal_successors(rows, state, attacked)
                ):
                    doomed.add(state)
                    break
        if not doomed:
            break
        waves.append(len(doomed))
        active.difference_update(doomed)
    return frozenset(active), tuple(waves), initial


def check_family(
    rows: tuple[int, ...],
    family: frozenset[int],
    size: int,
    banned: frozenset[int] = frozenset(),
) -> int:
    if not family:
        raise AssertionError("expected nonempty family")
    obligations = 0
    for state in family:
        assert state.bit_count() == size
        assert state not in banned
        assert dominates(rows, state)
        for attacked in range(len(rows)):
            if state & (1 << attacked):
                continue
            obligations += 1
            if not any(
                successor in family
                for successor in legal_successors(rows, state, attacked)
            ):
                raise AssertionError((state, attacked))
    return obligations


def response_pattern(
    rows: tuple[int, ...],
    family: frozenset[int],
    pairs: tuple[tuple[int, int], ...],
) -> tuple[str, ...]:
    names = labels(len(rows))
    return tuple(
        f"{names[guard]}->{names[attacked]}"
        for attacked, guard in pairs
        if rows[guard] & (1 << attacked)
        and direct_swap(attacked, guard) in family
    )


def pattern_key(pattern: tuple[str, ...]) -> str:
    return "|".join(pattern) if pattern else "<none>"


def mask_digest(masks: list[int]) -> str:
    payload = ",".join(str(mask) for mask in masks).encode()
    return hashlib.sha256(payload).hexdigest()


def family_digest(family: frozenset[int]) -> str:
    payload = ",".join(str(state) for state in sorted(family)).encode()
    return hashlib.sha256(payload).hexdigest()


def cube_paths() -> tuple[tuple[int, ...], ...]:
    paths: list[tuple[int, ...]] = []
    for image in itertools.permutations(T_VERTICES):
        interior: list[int] = []
        for subset in range(1, 7):
            state_vertices = [
                image[index] if subset & (1 << index) else source
                for index, source in enumerate(S_VERTICES)
            ]
            interior.append(bits(state_vertices))
        paths.append(tuple(interior))
    return tuple(paths)


CUBE_PATHS = cube_paths()


def base_count(family: frozenset[int]) -> int:
    return sum(all(state in family for state in path) for path in CUBE_PATHS)


def independent_nonbase_cegar(
    rows: tuple[int, ...],
    greatest: frozenset[int],
) -> tuple[bool, int, int]:
    """Lexicographic CEGAR, without the search program's frequency heuristic."""
    kernels: dict[frozenset[int], frozenset[int]] = {
        frozenset(): greatest
    }
    answers: dict[frozenset[int], bool] = {}
    maximum_depth = 0

    def kernel(banned: frozenset[int]) -> frozenset[int]:
        nonlocal maximum_depth
        maximum_depth = max(maximum_depth, len(banned))
        if banned not in kernels:
            kernels[banned] = safe_kernel(rows, 3, banned)[0]
        return kernels[banned]

    def visit(banned: frozenset[int]) -> bool:
        if banned in answers:
            return answers[banned]
        family = kernel(banned)
        if S_STATE not in family or T_STATE not in family:
            answers[banned] = False
            return False
        live = [
            path
            for path in CUBE_PATHS
            if all(state in family for state in path)
        ]
        if not live:
            answers[banned] = True
            return True
        branch = min(live)
        answer = any(visit(banned | {state}) for state in sorted(branch))
        answers[banned] = answer
        return answer

    found = visit(frozenset())
    return found, len(kernels), maximum_depth


def graph6_encode(rows: tuple[int, ...]) -> str:
    order = len(rows)
    stream: list[int] = []
    for right in range(1, order):
        for left in range(right):
            stream.append(int(bool(rows[left] & (1 << right))))
    while len(stream) % 6:
        stream.append(0)
    body = "".join(
        chr(
            63
            + sum(
                stream[offset + bit] << (5 - bit)
                for bit in range(6)
            )
        )
        for offset in range(0, len(stream), 6)
    )
    return chr(order + 63) + body


def graph6_decode(value: str) -> tuple[int, ...]:
    order = ord(value[0]) - 63
    stream: list[int] = []
    for char in value[1:]:
        datum = ord(char) - 63
        stream.extend((datum >> shift) & 1 for shift in range(5, -1, -1))
    rows = [1 << vertex for vertex in range(order)]
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if stream[cursor]:
                rows[left] |= 1 << right
                rows[right] |= 1 << left
            cursor += 1
    return tuple(rows)


def mask_of_rows(rows: tuple[int, ...]) -> int:
    order = len(rows)
    mask = 0
    for pair in FIXED_EDGES:
        assert rows[pair[0]] & (1 << pair[1])
    for pair in FIXED_NONEDGES:
        assert not rows[pair[0]] & (1 << pair[1])
    for index, (left, right) in enumerate(unknown_pairs(order)):
        if rows[left] & (1 << right):
            mask |= 1 << index
    return mask


def states_from_labels(
    order: int,
    records: list[list[str]],
) -> frozenset[int]:
    inverse = {name: vertex for vertex, name in enumerate(labels(order))}
    return frozenset(
        bits([inverse[name] for name in record])
        for record in records
    )


def audit_special_graphs(expected9: dict[str, object]) -> dict[str, object]:
    exemplar = expected9["disjunctive_negative_response_probe"]["exemplar"]
    hc_value = exemplar["graph6"]
    hc_rows = graph6_decode(hc_value)
    assert len(hc_rows) == 9
    assert graph6_encode(hc_rows) == hc_value
    assert mask_of_rows(hc_rows) == exemplar["mask"] == 39588
    hc_gamma, hc_witness = exact_gamma(hc_rows)
    hc_alpha = exact_alpha(hc_rows)
    hc_greatest, _, _ = safe_kernel(hc_rows, 3)
    assert (hc_gamma, hc_alpha, len(hc_greatest)) == (3, 3, 39)
    assert check_family(hc_rows, hc_greatest, 3) == 39 * 6
    hc_all_banned = safe_kernel(
        hc_rows, 3, frozenset(NEGATIVE_STATES)
    )[0]
    assert not hc_all_banned
    hc_single: dict[str, dict[str, object]] = {}
    names = labels(9)
    computed_by_digest: dict[str, frozenset[int]] = {}
    for attacked, guard in NEGATIVE:
        state = direct_swap(attacked, guard)
        family = safe_kernel(hc_rows, 3, frozenset({state}))[0]
        assert family
        assert state not in family
        check_family(hc_rows, family, 3, frozenset({state}))
        digest = family_digest(family)
        computed_by_digest[digest] = family
        hc_single[f"{names[guard]}->{names[attacked]}"] = {
            "size": len(family),
            "sha256": digest,
        }
    stored = exemplar["safe_families_by_sha256"]
    assert set(stored) == set(computed_by_digest)
    for digest, record in stored.items():
        stored_family = states_from_labels(9, record["states"])
        assert stored_family == computed_by_digest[digest]
        assert record["size"] == len(stored_family)
        assert record["literal_attack_obligations"] == check_family(
            hc_rows, stored_family, 3
        )

    stress = expected9["post_setup_near_countermodel"]
    hd_value = stress["graph6"]
    hd_rows = graph6_decode(hd_value)
    assert graph6_encode(hd_rows) == hd_value == "HDzruf]"
    hd_gamma, hd_witness = exact_gamma(hd_rows)
    hd_alpha = exact_alpha(hd_rows)
    hd_two = safe_kernel(hd_rows, 2)[0]
    hd_safe, hd_waves, hd_initial = safe_kernel(
        hd_rows, 3, frozenset(NEGATIVE_STATES)
    )
    assert (hd_gamma, hd_alpha) == (2, 3)
    assert not hd_two
    assert len(hd_safe) == 46
    assert check_family(
        hd_rows, hd_safe, 3, frozenset(NEGATIVE_STATES)
    ) == 276
    assert set(hd_witness) == {0, 4}
    stored_hd = states_from_labels(9, stress["family_states"])
    assert stored_hd == hd_safe
    computed_lists: dict[str, list[str]] = {}
    for attacked in range(3, 9):
        computed_lists[names[attacked]] = [
            names[guard]
            for guard in S_VERTICES
            if hd_rows[guard] & (1 << attacked)
            and direct_swap(attacked, guard) in hd_safe
        ]
    assert computed_lists == stress["family_lists_at_S"]
    assert stress["safe_greatest_family_initial_size"] == hd_initial
    assert tuple(stress["safe_greatest_family_deletion_waves"]) == hd_waves

    return {
        "HCxrs`c": {
            "mask": 39588,
            "gamma": hc_gamma,
            "gamma_witness": list(hc_witness),
            "alpha": hc_alpha,
            "greatest_family_size": len(hc_greatest),
            "all_six_banned_kernel_size": len(hc_all_banned),
            "single_ban_families": hc_single,
            "stored_distinct_families_exactly_matched": True,
        },
        "HDzruf]": {
            "gamma": hd_gamma,
            "gamma_witness": list(hd_witness),
            "alpha": hd_alpha,
            "two_guard_safe_kernel_size": len(hd_two),
            "three_guard_exact_list_kernel_size": len(hd_safe),
            "initial_size": hd_initial,
            "deletion_waves": list(hd_waves),
            "literal_obligations": 276,
            "stored_family_exactly_matched": True,
            "family_lists_at_S": computed_lists,
        },
    }


def audit_order(order: int) -> dict[str, object]:
    expected = json.loads(
        (RESULT_DIR / f"order{order}.json").read_text(encoding="utf-8")
    )
    checkpoint = json.loads(
        (RESULT_DIR / f"order{order}.checkpoint.json").read_text(
            encoding="utf-8"
        )
    )
    unknown = unknown_pairs(order)
    expected_masks = 1 << len(unknown)
    assert len(FIXED_EDGES & FIXED_NONEDGES) == 0
    assert len(unknown) == (11 if order == 8 else 19)
    assert (
        len(FIXED_EDGES) + len(FIXED_NONEDGES) + len(unknown)
        == order * (order - 1) // 2
    )

    counters: Counter[str] = Counter()
    gamma_masks: list[int] = []
    required_masks: list[int] = []
    unrestricted_masks: list[int] = []
    disjunctive_masks: list[int] = []
    family_size_hist: Counter[str] = Counter()
    positive_hist: Counter[str] = Counter()
    negative_hist: Counter[str] = Counter()
    base_hist: Counter[str] = Counter()
    single_unavoidable_hist: Counter[str] = Counter()
    exact_initial_hist: Counter[str] = Counter()
    exact_wave_hist: Counter[str] = Counter()
    max_positive = -1
    closest: list[int] = []
    base_calls = 0
    base_max_calls = 0
    base_max_depth = 0
    base_counterexamples: list[int] = []
    required_unrestricted: list[int] = []
    required_positive_hist: Counter[str] = Counter()
    required_max_positive = -1
    required_closest: list[int] = []
    required_extinction: Counter[str] = Counter()

    direct = (S_STATE,) + POSITIVE_STATES
    required = direct + (T_STATE,)
    all_positive_names = response_pattern(
        rows_for_mask(order, 0),
        frozenset(POSITIVE_STATES),
        POSITIVE,
    )
    # The edge condition in response_pattern suppresses optional positive
    # edges only in malformed universes; all six are fixed here.
    assert len(all_positive_names) == 6

    for mask in range(expected_masks):
        counters["masks_examined"] += 1
        rows = rows_for_mask(order, mask)
        direct_dominates = all(dominates(rows, state) for state in direct)
        if direct_dominates:
            counters["reference_and_six_positive_states_dominate"] += 1
        if has_independent_four(rows):
            continue
        counters["alpha_equals_3"] += 1
        if direct_dominates:
            counters[
                "reference_and_six_positive_states_dominate_and_alpha_equals_3"
            ] += 1
        if not dominates(rows, S_STATE):
            continue
        counters["reference_state_dominates"] += 1
        if has_small_dominator(rows):
            continue
        counters["gamma_alpha_equals_3"] += 1
        gamma_masks.append(mask)
        assert is_connected(rows)

        required_here = all(dominates(rows, state) for state in required)
        if required_here:
            counters["all_required_states_dominate"] += 1
            required_masks.append(mask)

        greatest, _, _ = safe_kernel(rows, 3)
        if greatest:
            counters["unrestricted_eternal_equality"] += 1
            unrestricted_masks.append(mask)
            assert S_STATE in greatest and T_STATE in greatest
            counters["literal_families_checked"] += 1
            counters["literal_attack_obligations_checked"] += check_family(
                rows, greatest, 3
            )
            positive = response_pattern(rows, greatest, POSITIVE)
            negative = response_pattern(rows, greatest, NEGATIVE)
            if len(positive) == 6:
                counters["unrestricted_contains_all_positive_swaps"] += 1
            family_size_hist[str(len(greatest))] += 1
            positive_hist[pattern_key(positive)] += 1
            negative_hist[pattern_key(negative)] += 1
            base_hist[str(base_count(greatest))] += 1
            if len(positive) > max_positive:
                max_positive = len(positive)
                closest = [mask]
            elif len(positive) == max_positive:
                closest.append(mask)

            individually_avoidable = True
            individually_unavoidable: list[str] = []
            names = labels(order)
            for attacked, guard in NEGATIVE:
                negative_state = direct_swap(attacked, guard)
                single = safe_kernel(
                    rows, 3, frozenset({negative_state})
                )[0]
                if single:
                    counters["literal_families_checked"] += 1
                    counters["literal_attack_obligations_checked"] += (
                        check_family(
                            rows,
                            single,
                            3,
                            frozenset({negative_state}),
                        )
                    )
                else:
                    individually_avoidable = False
                    individually_unavoidable.append(
                        f"{names[guard]}->{names[attacked]}"
                    )
            single_unavoidable_hist[
                pattern_key(tuple(individually_unavoidable))
            ] += 1

            nonbase, calls, depth = independent_nonbase_cegar(
                rows, greatest
            )
            base_calls += calls
            base_max_calls = max(base_max_calls, calls)
            base_max_depth = max(base_max_depth, depth)
            if nonbase:
                base_counterexamples.append(mask)
        else:
            individually_avoidable = False

        exact, waves, initial = safe_kernel(
            rows, 3, frozenset(NEGATIVE_STATES)
        )
        exact_initial_hist[str(initial)] += 1
        exact_wave_hist[str(len(waves))] += 1
        if exact:
            counters["exact_safe_family_nonempty"] += 1
            counters["literal_families_checked"] += 1
            counters["literal_attack_obligations_checked"] += check_family(
                rows, exact, 3, frozenset(NEGATIVE_STATES)
            )
        elif greatest and individually_avoidable:
            disjunctive_masks.append(mask)
        if exact and all(state in exact for state in required):
            counters["exact_realizations"] += 1

        if required_here:
            if greatest:
                required_unrestricted.append(mask)
                positive = response_pattern(rows, greatest, POSITIVE)
                required_positive_hist[pattern_key(positive)] += 1
                if len(positive) > required_max_positive:
                    required_max_positive = len(positive)
                    required_closest = [mask]
                elif len(positive) == required_max_positive:
                    required_closest.append(mask)
            profile = (
                f"initial={initial};waves="
                + ",".join(str(item) for item in waves)
            )
            required_extinction[profile] += 1

    counters["base_cegar_fixed_points"] = base_calls
    counters["base_counterexamples"] = len(base_counterexamples)
    expected_counts = expected["coverage"]["counts"]
    actual_counts = {
        key: counters.get(key, 0)
        for key in expected_counts
    }
    count_differences = {
        key: {
            "expected": expected_counts.get(key),
            "independent": actual_counts.get(key, 0),
        }
        for key in sorted(set(expected_counts) | set(actual_counts))
        if expected_counts.get(key, 0) != actual_counts.get(key, 0)
    }

    assert gamma_masks == expected["gamma_alpha_frontier"]["masks"]
    assert required_masks == expected[
        "required_state_domination_frontier"
    ]["masks"]
    assert unrestricted_masks == expected[
        "unrestricted_eternal_frontier"
    ]["masks"]
    assert disjunctive_masks == expected[
        "disjunctive_negative_response_probe"
    ]["joint_but_no_singleton_unavoidable_masks"]
    assert mask_digest(gamma_masks) == expected[
        "gamma_alpha_frontier"
    ]["mask_list_sha256"]
    assert mask_digest(required_masks) == expected[
        "required_state_domination_frontier"
    ]["mask_list_sha256"]
    assert mask_digest(unrestricted_masks) == expected[
        "unrestricted_eternal_frontier"
    ]["mask_list_sha256"]
    assert forced_unknown(order, gamma_masks) == expected[
        "gamma_alpha_frontier"
    ]["forced_unknown_adjacencies"]
    assert forced_unknown(order, required_masks) == expected[
        "required_state_domination_frontier"
    ]["forced_unknown_adjacencies"]
    assert forced_unknown(order, unrestricted_masks) == expected[
        "unrestricted_eternal_frontier"
    ]["forced_unknown_adjacencies"]
    assert forced_unknown(order, closest) == expected[
        "unrestricted_eternal_frontier"
    ]["closest_forced_unknown_adjacencies"]
    assert dict(family_size_hist) == expected[
        "unrestricted_eternal_frontier"
    ]["family_size_histogram"]
    assert dict(positive_hist) == expected[
        "unrestricted_eternal_frontier"
    ]["positive_pattern_histogram"]
    assert dict(negative_hist) == expected[
        "unrestricted_eternal_frontier"
    ]["negative_pattern_histogram"]
    assert dict(base_hist) == expected[
        "unrestricted_eternal_frontier"
    ]["greatest_family_base_ordering_count_histogram"]
    assert max_positive == expected["unrestricted_eternal_frontier"][
        "max_positive_swaps_present_out_of_6"
    ]
    assert closest == expected["unrestricted_eternal_frontier"][
        "closest_masks"
    ]
    assert dict(single_unavoidable_hist) == checkpoint[
        "single_negative_unavoidable_histogram"
    ]
    assert dict(exact_initial_hist) == expected[
        "exact_safe_fixed_point"
    ]["initial_state_count_histogram"]
    assert dict(exact_wave_hist) == expected["exact_safe_fixed_point"][
        "deletion_wave_count_histogram"
    ]
    assert required_unrestricted == expected[
        "required_state_domination_frontier"
    ]["unrestricted_eternal_masks"]
    assert dict(required_positive_hist) == expected[
        "required_state_domination_frontier"
    ]["unrestricted_positive_pattern_histogram"]
    assert required_max_positive == expected[
        "required_state_domination_frontier"
    ]["maximum_positive_swaps_surviving_closure_out_of_6"]
    assert required_closest == expected[
        "required_state_domination_frontier"
    ]["closest_masks_after_closure"]
    assert dict(required_extinction) == expected[
        "required_state_domination_frontier"
    ]["exact_safe_extinction_profile_histogram"]
    assert not base_counterexamples
    assert not expected["proper_family_base_ordering_falsifier"][
        "counterexamples"
    ]
    assert checkpoint["next_mask"] == checkpoint["stop_mask"] == expected_masks
    assert checkpoint["counts"] == expected_counts
    assert checkpoint["gamma_alpha_masks"] == gamma_masks
    assert checkpoint["required_dominating_masks"] == required_masks
    assert checkpoint["unrestricted_eternal_masks"] == unrestricted_masks
    assert (
        checkpoint["joint_but_not_singleton_unavoidable_masks"]
        == disjunctive_masks
    )
    assert checkpoint["exact_masks"] == []

    return {
        "order": order,
        "unknown_edge_count": len(unknown),
        "mask_count": expected_masks,
        "all_mask_bits_covered_once": True,
        "independent_counts": actual_counts,
        "count_differences_from_published": count_differences,
        "mask_digests": {
            "gamma_alpha": mask_digest(gamma_masks),
            "required_states_dominate": mask_digest(required_masks),
            "unrestricted_eternal": mask_digest(unrestricted_masks),
        },
        "exact_mask_lists_match": True,
        "exact_histograms_match": True,
        "forced_adjacency_diagnostics_match": True,
        "all_gamma_alpha_frontier_graphs_connected": True,
        "exact_list_safe_kernel_nonempty": counters[
            "exact_safe_family_nonempty"
        ],
        "exact_realizations": counters["exact_realizations"],
        "base_orderability": {
            "graphs": len(unrestricted_masks),
            "independent_lexicographic_cegar_fixed_points": base_calls,
            "published_frequency_cegar_fixed_points": expected_counts[
                "base_cegar_fixed_points"
            ],
            "maximum_independent_calls_per_graph": base_max_calls,
            "maximum_independent_banned_depth": base_max_depth,
            "counterexamples": base_counterexamples,
        },
        "checkpoint_exactly_matches_results_and_lists": True,
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    expected_hashes = {
        "source": "d2e565eeaae4f04cdace53e08657cdaaf84b51bec83e7fe23822aaee77640c4d",
        "order8.json": "ae752b8aaf6b2cad693c1183d22d42ce04160b4ece2a58324f3d57615f7481a5",
        "order8.log": "a0b16aac03e74af7707cdfd1419fd70ddc2c50644cb8ff3a02a2cb958d8c8636",
        "order8.checkpoint.json": "5d134503c84d907046d848e04857adf90f6798dc8c5bb11c112f98b37ad0db4a",
        "order9.json": "45ce01d4ef36b1d90e5bb593506976897edeaa972921407ddd4108dbb10609c1",
        "order9.log": "38cc12c99a748f30683d2eac39b2b52672d35d582bb5404bfa0472ba27810837",
        "order9.checkpoint.json": "5a50aa1939753e0b15089a954519bb25be88dccb18a5272391653af227d052f6",
    }
    artifact_paths = {
        "source": SOURCE,
        **{
            name: RESULT_DIR / name
            for name in expected_hashes
            if name != "source"
        },
    }
    actual_hashes = {
        name: sha256(path)
        for name, path in artifact_paths.items()
    }
    assert actual_hashes == expected_hashes
    order8 = audit_order(8)
    order9 = audit_order(9)
    expected9 = json.loads(
        (RESULT_DIR / "order9.json").read_text(encoding="utf-8")
    )
    special = audit_special_graphs(expected9)
    evidence = {
        "verdict": "PASS_WITH_ONE_NONMATHEMATICAL_REPRODUCIBILITY_ERRATUM",
        "commit_audited": "a997ced3",
        "independence": (
            "No import from the synthesis source; graph universe, exact "
            "gamma/alpha, synchronous safe kernel, literal transition "
            "checker, lexicographic base-cube CEGAR, and graph6 replay were "
            "implemented independently."
        ),
        "artifact_hashes": actual_hashes,
        "orders": {
            "8": order8,
            "9": order9,
        },
        "special_graphs": special,
        "model_checks": {
            "attacks_only_unoccupied": True,
            "exactly_one_guard_replaced": True,
            "move_requires_graph_edge": True,
            "every_family_state_dominates_full_graph": True,
            "six_negative_states_banned_from_family_not_graph": True,
            "proper_families_covered_by_greatest_safe_kernel": True,
        },
        "erratum": {
            "claim": (
                "NOTE section 8 says a completed-checkpoint resume "
                "reproduced identical output bytes."
            ),
            "finding": (
                "A completed resume regenerates completed_at, so output "
                "bytes and SHA-256 differ unless both finalizations happen "
                "in the same timestamp second. The mathematical content is "
                "unchanged after removing completed_at."
            ),
            "severity": "minor; no mathematical or coverage impact",
        },
        "scope_clarification": {
            "location": "NOTE section 3 count table",
            "finding": (
                "The row 'nonempty safe family after all six negative "
                "swaps are banned: 0' is true only inside the "
                "gamma=alpha=3 frontier. Read literally over all labeled "
                "masks it is false, as the same note's HDzruf] gamma=2 "
                "stress graph has a 46-state such kernel."
            ),
            "recommended_wording": (
                "gamma=alpha=3 and nonempty safe family after all six "
                "negative swaps are banned"
            ),
            "severity": "minor wording ambiguity; no mathematical impact",
        },
    }
    output = Path(__file__).with_name("hostile-evidence.json")
    output.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "verdict": evidence["verdict"],
        "order8_exact": order8["exact_realizations"],
        "order9_exact": order9["exact_realizations"],
        "order8_count_differences": order8[
            "count_differences_from_published"
        ],
        "order9_count_differences": order9[
            "count_differences_from_published"
        ],
        "evidence": str(output),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
