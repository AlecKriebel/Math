#!/usr/bin/env python3
"""Independent exact graph diagnostics using signed cyclic words and edge sets.

No imports or reads of original PR checkers. These finite checks support the
universal derivation saved in FIRST_CONCLUSION; they do not replace it.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform
import sys


P_WORD = (-1, -2, 3, 1, -3, 2)
T_WORD = (-1, 2, -3, 1, -2, 3)


def renamed(word):
    names = {}
    result = []
    for token in word:
        chord = abs(token)
        if chord not in names:
            names[chord] = len(names) + 1
        result.append(names[chord] * (1 if token > 0 else -1))
    return tuple(result)


def cyclic_key(word):
    if not word:
        return ()
    return min(renamed(word[k:] + word[:k]) for k in range(len(word)))


P_KEY, T_KEY = cyclic_key(P_WORD), cyclic_key(T_WORD)


def arc_tokens(word, chord):
    """Scan the cyclic word, beginning after the positive token (tail)."""
    tail = word.index(chord)
    walk = word[tail + 1:] + word[:tail]
    head = walk.index(-chord)
    return frozenset(walk[:head])


def intersection_graph(word):
    chords = sorted({abs(t) for t in word})
    arcs = {c: arc_tokens(word, c) for c in chords}
    edges = set()
    for c, d in combinations(chords, 2):
        alternating = (d in arcs[c]) != (-d in arcs[c])
        reverse_alternating = (c in arcs[d]) != (-c in arcs[d])
        assert alternating == reverse_alternating
        if alternating:
            forward = d in arcs[c]
            reverse = c in arcs[d]
            assert forward != reverse, (word, c, d)
            edges.add((c, d) if forward else (d, c))
    return frozenset(edges)


def is_cycle(edges, triple):
    x, y, z = triple
    return ((x, y) in edges and (y, z) in edges and (z, x) in edges) or (
        (y, x) in edges and (z, y) in edges and (x, z) in edges)


def count_cycles(edges, vertices):
    return sum(is_cycle(edges, triple) for triple in combinations(vertices, 3))


def completions(edges, vertices):
    absent = [(a, b) for a, b in combinations(vertices, 2)
              if (a, b) not in edges and (b, a) not in edges]
    for bits in product((0, 1), repeat=len(absent)):
        yield frozenset(set(edges) | {
            ((b, a) if bit else (a, b)) for (a, b), bit in zip(absent, bits)})


def pairings(positions):
    if not positions:
        yield ()
        return
    first = positions[0]
    for i in range(1, len(positions)):
        second = positions[i]
        remaining = positions[1:i] + positions[i + 1:]
        for rest in pairings(remaining):
            yield ((first, second),) + rest


def directed_words(n):
    for pairs in pairings(tuple(range(2 * n))):
        for directions in product((1, -1), repeat=n):
            word = [None] * (2 * n)
            for chord, ((left, right), direction) in enumerate(zip(pairs, directions), 1):
                word[left] = direction * chord
                word[right] = -direction * chord
            yield tuple(word)


def arrow_subsets(word):
    vertices = sorted({abs(t) for t in word})
    p_sets, t_sets = [], []
    for triple in combinations(vertices, 3):
        selected = frozenset(triple)
        restricted = tuple(t for t in word if abs(t) in selected)
        key = cyclic_key(restricted)
        if key == P_KEY:
            p_sets.append(triple)
        elif key == T_KEY:
            t_sets.append(triple)
    return p_sets, t_sets


def bound(n):
    return Fraction(n * (n * n - 1), 24)


def floor_bound(n):
    value = bound(n)
    return value.numerator // value.denominator


def strong_bound(n):
    return Fraction(n * (n * n - 4), 24) if n % 2 == 0 else Fraction(floor_bound(n))


def pattern_checks():
    p_edges = intersection_graph(P_WORD)
    t_edges = intersection_graph(T_WORD)
    assert p_edges == frozenset({(3, 1), (1, 2)})
    assert t_edges == frozenset({(1, 3), (3, 2), (2, 1)})
    assert len(p_edges) == 2 and len(t_edges) == 3
    assert P_KEY != T_KEY
    results = {}
    for name, word in [("P", P_WORD), ("T", T_WORD)]:
        automorphisms = sum(renamed(word[k:] + word[:k]) == renamed(word)
                            for k in range(len(word)))
        rotated_cases = 0
        for k in range(len(word)):
            rotated = word[k:] + word[:k]
            assert intersection_graph(rotated) == intersection_graph(word)
            assert cyclic_key(rotated) == cyclic_key(word)
            rotated_cases += 1
        reverse = tuple(reversed(word))
        assert intersection_graph(reverse) == frozenset((b, a) for a, b in intersection_graph(word))
        cycle_values = [count_cycles(e, (1, 2, 3))
                        for e in completions(intersection_graph(word), (1, 2, 3))]
        expectation = Fraction(sum(cycle_values), len(cycle_values))
        assert expectation == (Fraction(1, 2) if name == "P" else Fraction(1))
        results[name] = {
            "signed_word": word,
            "edges": sorted(intersection_graph(word)),
            "cyclic_automorphisms": automorphisms,
            "rotations_checked": rotated_cases,
            "completion_cycle_counts": cycle_values,
            "expectation": str(expectation),
        }
    assert results["P"]["cyclic_automorphisms"] == 1
    assert results["T"]["cyclic_automorphisms"] == 3
    return results


def formal_chord_checks():
    results = []
    local_histogram = Counter()
    for n in range(5):
        words = 0
        sign_assignments = 0
        completions_checked = 0
        max_abs_value = Fraction(0)
        max_weight = Fraction(0)
        p_occurrences = 0
        t_occurrences = 0
        distinct_keys = set()
        for word in directed_words(n):
            words += 1
            distinct_keys.add(cyclic_key(word))
            vertices = tuple(range(1, n + 1))
            graph = intersection_graph(word)
            assert intersection_graph(tuple(reversed(word))) == frozenset((b, a) for a, b in graph)
            p_sets, t_sets = arrow_subsets(word)
            p_occurrences += len(p_sets)
            t_occurrences += len(t_sets)
            weight = Fraction(len(p_sets), 2) + len(t_sets)
            max_weight = max(max_weight, weight)
            cycle_values = []
            for completion in completions(graph, vertices):
                completions_checked += 1
                c = count_cycles(completion, vertices)
                assert c <= strong_bound(n), (word, completion, c, strong_bound(n))
                cycle_values.append(c)
            expectation = Fraction(sum(cycle_values), len(cycle_values))
            assert weight <= expectation <= strong_bound(n), (word, weight, expectation)
            for triple in p_sets:
                induced = frozenset((a, b) for a, b in graph if a in triple and b in triple)
                assert len(induced) == 2
                local = [is_cycle(e, triple) for e in completions(induced, triple)]
                assert Fraction(sum(local), len(local)) == Fraction(1, 2)
            for triple in t_sets:
                induced = frozenset((a, b) for a, b in graph if a in triple and b in triple)
                assert len(induced) == 3 and is_cycle(induced, triple)
            for signs in product((-1, 1), repeat=n):
                sign_assignments += 1
                signed_sum = Fraction(0)
                for collection, coefficient in [(p_sets, Fraction(1, 2)), (t_sets, Fraction(1))]:
                    for triple in collection:
                        sign_product = 1
                        for chord in triple:
                            sign_product *= signs[chord - 1]
                        signed_sum += coefficient * sign_product
                assert abs(signed_sum) <= weight <= expectation <= strong_bound(n)
                max_abs_value = max(max_abs_value, abs(signed_sum))
            if n == 3:
                name = "P" if p_sets else "T" if t_sets else "other"
                local_histogram[(name, len(graph), str(expectation))] += 1
        results.append({
            "n": n,
            "rooted_unlabeled_chord_words": words,
            "cyclic_isomorphism_classes": len(distinct_keys),
            "sign_assignments_checked": sign_assignments,
            "completion_tournaments_checked": completions_checked,
            "P_subset_occurrences": p_occurrences,
            "T_subset_occurrences": t_occurrences,
            "maximum_absolute_formal_evaluation": str(max_abs_value),
            "maximum_unsigned_weight": str(max_weight),
            "floor_bound": floor_bound(n),
            "parity_refined_bound": str(strong_bound(n)),
        })
    return {"sizes": results, "three_chord_local_histogram": [
        {"type": key[0], "fixed_edges": key[1], "cyclic_probability": key[2], "count": count}
        for key, count in sorted(local_histogram.items())]}


def tournament_checks():
    results = []
    for n in range(7):
        vertices = tuple(range(1, n + 1))
        tournaments = 0
        observed_max = 0
        maximizers = 0
        cycle_histogram = Counter()
        for edges in completions(frozenset(), vertices):
            tournaments += 1
            c = count_cycles(edges, vertices)
            degrees = [sum((v, w) in edges for w in vertices if w != v) for v in vertices]
            assert sum(degrees) == n * (n - 1) // 2
            transitive_by_sources = sum(d * (d - 1) // 2 for d in degrees)
            assert c == n * (n - 1) * (n - 2) // 6 - transitive_by_sources
            centered_identity = bound(n) - sum((Fraction(d) - Fraction(n - 1, 2)) ** 2 for d in degrees) / 2
            assert c == centered_identity
            assert c <= floor_bound(n)
            assert c <= strong_bound(n)
            if n % 2 == 0:
                assert strong_bound(n).denominator == 1
            cycle_histogram[c] += 1
            if c > observed_max:
                observed_max, maximizers = c, 1
            elif c == observed_max:
                maximizers += 1
        assert observed_max == strong_bound(n)
        results.append({
            "n": n,
            "tournaments_checked": tournaments,
            "observed_maximum_cycles": observed_max,
            "maximizers": maximizers,
            "cycle_histogram": dict(sorted(cycle_histogram.items())),
            "floor_bound": floor_bound(n),
            "parity_refined_bound": str(strong_bound(n)),
        })
    return results


def main():
    source = Path(__file__).resolve()
    result = {
        "status": "PASS",
        "implementation": "signed cyclic words; frozenset directed edges; direct cycle predicates; exact Fraction arithmetic",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "pattern_checks": pattern_checks(),
        "formal_chord_checks": formal_chord_checks(),
        "tournament_checks": tournament_checks(),
        "scope": "finite diagnostics only; universal result follows from FIRST_CONCLUSION derivation; imported knot bridge not checked here",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
