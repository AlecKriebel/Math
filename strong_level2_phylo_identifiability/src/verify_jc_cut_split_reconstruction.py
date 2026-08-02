#!/usr/bin/env python3
"""Exact certificate for generic JC cut-split reconstruction.

The finite calculation proves the only level-2-specific combinatorial input:
no nontrivial two-colouring of the incident ports of a cycle or theta blob is
displayed by every parent-choice switching.  Arbitrary port words reduce to
the enumerated run-compressed words.

The script also records exact five-by-five Fourier-flattening minors for the
two quartet topologies crossing a proposed split.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from sympy import Matrix, Rational

from enumerate_four_leaf_root_theta import build_network, valid_binary_strong
from enumerate_theta_orientation_cores import enumerate_cores
from generic_fourier_network import precompute_displayed_trees
from verify_jc_cycle_cross_generator_atlas import build_cycle_strong
from verify_jc_incoming_port_atlas import lift_network


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "jc_cut_split_reconstruction.json"

# A run-compressed word has at most one colour transition and one port per
# run.  If one colour occurs in only one run globally, a second representative
# from that run is retained by the singleton-doubling audit below.
WORDS_BY_LENGTH = {0: ((),), 1: ((0,), (1,)), 2: ((0, 1), (1, 0))}
BASE_WORDS = ((), (0,), (1,), (0, 1), (1, 0))


def build_cycle_root(counts):
    vertices = {"S": "S", "X": "X"}
    edges = []
    parents = []
    for side, count in enumerate(counts):
        chain = ["S"]
        for index in range(count):
            vertex = f"P{side}_{index}"
            vertices[vertex] = "T"
            parents.append(vertex)
            chain.append(vertex)
        chain.append("X")
        edges.extend(zip(chain, chain[1:]))
    parents.append("X")
    leaves = []
    for index, parent in enumerate(parents):
        leaf = f"L{index}"
        vertices[leaf] = "L"
        edges.append((parent, leaf))
        leaves.append(leaf)
    assert valid_binary_strong(vertices, tuple(edges))
    return {
        "vertices": vertices,
        "edges": tuple(edges),
        "leaves": tuple(leaves),
    }


def displayed_by_every_switching(network, colours):
    leaf_labels = {leaf: index for index, leaf in enumerate(network["leaves"])}
    side = frozenset(index for index, colour in enumerate(colours) if colour == 0)
    other = frozenset(range(len(colours))) - side
    assert len(side) >= 2 and len(other) >= 2
    _reticulations, trees = precompute_displayed_trees(
        network["vertices"], tuple(network["edges"]), leaf_labels
    )
    for _choice, selected, descendants in trees:
        if not any(descendants[index] in (side, other) for index in selected):
            return False
    return True


def theta_run_compressed_census():
    _raw, cores = enumerate_cores()
    occupancy_presentations = 0
    colourings = 0
    balanced = 0
    common = 0
    occupancy_by_core = Counter()

    for core_index, core in enumerate(cores):
        segment_count = len(core["directed_segments"])
        sink_count = sum(
            colour == "X" for colour in core["vertex_types"].values()
        )
        for counts in product(range(3), repeat=segment_count):
            vertices, edges, leaves = build_network(core, counts)
            if not valid_binary_strong(vertices, edges):
                continue
            network = lift_network(
                {"vertices": vertices, "edges": edges, "leaves": leaves}
            )
            occupancy_presentations += 1
            occupancy_by_core[core_index] += 1
            for words in product(*(WORDS_BY_LENGTH[count] for count in counts)):
                ordinary = tuple(colour for word in words for colour in word)
                for sink_colours in product((0, 1), repeat=sink_count):
                    for incoming_colour in (0, 1):
                        colours = ordinary + sink_colours + (incoming_colour,)
                        colourings += 1
                        counts_by_colour = Counter(colours)
                        if set(colours) != {0, 1} or min(
                            counts_by_colour.values()
                        ) < 2:
                            continue
                        balanced += 1
                        common += displayed_by_every_switching(network, colours)

    singleton_doubled = 0
    singleton_common = 0
    for core in cores:
        sink_count = sum(
            colour == "X" for colour in core["vertex_types"].values()
        )
        segment_count = len(core["directed_segments"])
        for base_words in product(BASE_WORDS, repeat=segment_count):
            for sink_colours in product((0, 1), repeat=sink_count):
                for incoming_colour in (0, 1):
                    occurrences = {0: [], 1: []}
                    for segment, word in enumerate(base_words):
                        for position, colour in enumerate(word):
                            occurrences[colour].append((segment, position))
                    for colour in tuple(sink_colours) + (incoming_colour,):
                        occurrences[colour].append(None)
                    if any(not occurrences[colour] for colour in (0, 1)):
                        continue
                    words = [list(word) for word in base_words]
                    changed = False
                    possible = True
                    for colour in (0, 1):
                        if len(occurrences[colour]) != 1:
                            continue
                        location = occurrences[colour][0]
                        if location is None:
                            possible = False
                            break
                        segment, position = location
                        words[segment].insert(position, colour)
                        changed = True
                    if not possible or not changed:
                        continue
                    words = tuple(tuple(word) for word in words)
                    counts = tuple(map(len, words))
                    vertices, edges, leaves = build_network(core, counts)
                    if not valid_binary_strong(vertices, edges):
                        continue
                    network = lift_network(
                        {"vertices": vertices, "edges": edges, "leaves": leaves}
                    )
                    colours = (
                        tuple(colour for word in words for colour in word)
                        + sink_colours
                        + (incoming_colour,)
                    )
                    assert set(colours) == {0, 1}
                    assert min(Counter(colours).values()) >= 2
                    singleton_doubled += 1
                    singleton_common += displayed_by_every_switching(
                        network, colours
                    )

    assert occupancy_presentations == 1512
    assert dict(occupancy_by_core) == {0: 648, 1: 576, 2: 144, 3: 144}
    assert colourings == 254400 and balanced == 251352
    assert singleton_doubled == 2232
    assert common == singleton_common == 0
    return {
        "run_compressed_occupancy_presentations": occupancy_presentations,
        "occupancy_presentations_by_core": dict(sorted(occupancy_by_core.items())),
        "run_compressed_colourings": colourings,
        "two_colours_at_least_twice": balanced,
        "singleton_run_doubled_colourings": singleton_doubled,
        "splits_displayed_by_every_switching": 0,
    }


def cycle_run_compressed_census():
    occupancy_presentations = 0
    colourings = 0
    balanced = 0
    common = 0
    for counts in product(range(3), repeat=2):
        if sum(counts) < 1:
            continue
        try:
            network = build_cycle_strong(counts)
        except AssertionError:
            continue
        occupancy_presentations += 1
        for words in product(*(WORDS_BY_LENGTH[count] for count in counts)):
            ordinary = tuple(colour for word in words for colour in word)
            for sink_colour, incoming_colour in product((0, 1), repeat=2):
                colours = ordinary + (sink_colour, incoming_colour)
                colourings += 1
                counts_by_colour = Counter(colours)
                if set(colours) != {0, 1} or min(counts_by_colour.values()) < 2:
                    continue
                balanced += 1
                common += displayed_by_every_switching(network, colours)

    singleton_doubled = 0
    singleton_common = 0
    for base_words in product(BASE_WORDS, repeat=2):
        for sink_colour, incoming_colour in product((0, 1), repeat=2):
            occurrences = {0: [], 1: []}
            for segment, word in enumerate(base_words):
                for position, colour in enumerate(word):
                    occurrences[colour].append((segment, position))
            for colour in (sink_colour, incoming_colour):
                occurrences[colour].append(None)
            if any(not occurrences[colour] for colour in (0, 1)):
                continue
            words = [list(word) for word in base_words]
            changed = False
            possible = True
            for colour in (0, 1):
                if len(occurrences[colour]) != 1:
                    continue
                location = occurrences[colour][0]
                if location is None:
                    possible = False
                    break
                segment, position = location
                words[segment].insert(position, colour)
                changed = True
            if not possible or not changed:
                continue
            words = tuple(tuple(word) for word in words)
            try:
                network = build_cycle_strong(tuple(map(len, words)))
            except AssertionError:
                continue
            colours = (
                tuple(colour for word in words for colour in word)
                + (sink_colour, incoming_colour)
            )
            assert set(colours) == {0, 1}
            assert min(Counter(colours).values()) >= 2
            singleton_doubled += 1
            singleton_common += displayed_by_every_switching(network, colours)

    assert occupancy_presentations == 8
    assert colourings == 96 and balanced == 54
    assert singleton_doubled == 24
    assert common == singleton_common == 0
    return {
        "run_compressed_occupancy_presentations": occupancy_presentations,
        "run_compressed_colourings": colourings,
        "two_colours_at_least_twice": balanced,
        "singleton_run_doubled_colourings": singleton_doubled,
        "splits_displayed_by_every_switching": 0,
    }


def theta_root_run_compressed_census():
    """Repeat the local lemma when the blob itself contains the root."""

    _raw, cores = enumerate_cores()
    occupancy_presentations = colourings = balanced = common = 0
    occupancy_by_core = Counter()
    for core_index, core in enumerate(cores):
        segment_count = len(core["directed_segments"])
        sink_count = sum(
            colour == "X" for colour in core["vertex_types"].values()
        )
        for counts in product(range(3), repeat=segment_count):
            vertices, edges, leaves = build_network(core, counts)
            if not valid_binary_strong(vertices, edges):
                continue
            network = {"vertices": vertices, "edges": edges, "leaves": leaves}
            occupancy_presentations += 1
            occupancy_by_core[core_index] += 1
            for words in product(*(WORDS_BY_LENGTH[count] for count in counts)):
                ordinary = tuple(colour for word in words for colour in word)
                for sink_colours in product((0, 1), repeat=sink_count):
                    colours = ordinary + sink_colours
                    colourings += 1
                    counts_by_colour = Counter(colours)
                    if set(colours) != {0, 1} or min(
                        counts_by_colour.values()
                    ) < 2:
                        continue
                    balanced += 1
                    common += displayed_by_every_switching(network, colours)

    singleton_doubled = singleton_common = 0
    for core in cores:
        sink_count = sum(
            colour == "X" for colour in core["vertex_types"].values()
        )
        segment_count = len(core["directed_segments"])
        for base_words in product(BASE_WORDS, repeat=segment_count):
            for sink_colours in product((0, 1), repeat=sink_count):
                occurrences = {0: [], 1: []}
                for segment, word in enumerate(base_words):
                    for position, colour in enumerate(word):
                        occurrences[colour].append((segment, position))
                for colour in sink_colours:
                    occurrences[colour].append(None)
                if any(not occurrences[colour] for colour in (0, 1)):
                    continue
                words = [list(word) for word in base_words]
                changed = False
                possible = True
                for colour in (0, 1):
                    if len(occurrences[colour]) != 1:
                        continue
                    location = occurrences[colour][0]
                    if location is None:
                        possible = False
                        break
                    segment, position = location
                    words[segment].insert(position, colour)
                    changed = True
                if not possible or not changed:
                    continue
                words = tuple(tuple(word) for word in words)
                vertices, edges, leaves = build_network(
                    core, tuple(map(len, words))
                )
                if not valid_binary_strong(vertices, edges):
                    continue
                network = {
                    "vertices": vertices,
                    "edges": edges,
                    "leaves": leaves,
                }
                colours = (
                    tuple(colour for word in words for colour in word)
                    + sink_colours
                )
                assert set(colours) == {0, 1}
                assert min(Counter(colours).values()) >= 2
                singleton_doubled += 1
                singleton_common += displayed_by_every_switching(
                    network, colours
                )

    assert occupancy_presentations == 1512
    assert dict(occupancy_by_core) == {0: 648, 1: 576, 2: 144, 3: 144}
    assert colourings == 127200 and balanced == 124368
    assert singleton_doubled == 2232
    assert common == singleton_common == 0
    return {
        "run_compressed_occupancy_presentations": occupancy_presentations,
        "occupancy_presentations_by_core": dict(sorted(occupancy_by_core.items())),
        "run_compressed_colourings": colourings,
        "two_colours_at_least_twice": balanced,
        "singleton_run_doubled_colourings": singleton_doubled,
        "splits_displayed_by_every_switching": 0,
    }


def cycle_root_run_compressed_census():
    occupancy_presentations = colourings = balanced = common = 0
    for counts in product(range(3), repeat=2):
        if sum(counts) < 1:
            continue
        try:
            network = build_cycle_root(counts)
        except AssertionError:
            continue
        occupancy_presentations += 1
        for words in product(*(WORDS_BY_LENGTH[count] for count in counts)):
            ordinary = tuple(colour for word in words for colour in word)
            for sink_colour in (0, 1):
                colours = ordinary + (sink_colour,)
                colourings += 1
                counts_by_colour = Counter(colours)
                if set(colours) != {0, 1} or min(counts_by_colour.values()) < 2:
                    continue
                balanced += 1
                common += displayed_by_every_switching(network, colours)

    singleton_doubled = singleton_common = 0
    for base_words in product(BASE_WORDS, repeat=2):
        for sink_colour in (0, 1):
            occurrences = {0: [], 1: []}
            for segment, word in enumerate(base_words):
                for position, colour in enumerate(word):
                    occurrences[colour].append((segment, position))
            occurrences[sink_colour].append(None)
            if any(not occurrences[colour] for colour in (0, 1)):
                continue
            words = [list(word) for word in base_words]
            changed = False
            possible = True
            for colour in (0, 1):
                if len(occurrences[colour]) != 1:
                    continue
                location = occurrences[colour][0]
                if location is None:
                    possible = False
                    break
                segment, position = location
                words[segment].insert(position, colour)
                changed = True
            if not possible or not changed:
                continue
            words = tuple(tuple(word) for word in words)
            try:
                network = build_cycle_root(tuple(map(len, words)))
            except AssertionError:
                continue
            colours = tuple(colour for word in words for colour in word) + (
                sink_colour,
            )
            assert set(colours) == {0, 1}
            assert min(Counter(colours).values()) >= 2
            singleton_doubled += 1
            singleton_common += displayed_by_every_switching(network, colours)

    assert occupancy_presentations == 8
    assert colourings == 48 and balanced == 16
    assert singleton_doubled == 20
    assert common == singleton_common == 0
    return {
        "run_compressed_occupancy_presentations": occupancy_presentations,
        "run_compressed_colourings": colourings,
        "two_colours_at_least_twice": balanced,
        "singleton_run_doubled_colourings": singleton_doubled,
        "splits_displayed_by_every_switching": 0,
    }


def wrong_split_flattening(true_side):
    rows = tuple(product(range(4), repeat=2))
    matrix = []
    for row in rows:
        line = []
        for column in rows:
            assignment = (row[0], row[1], column[0], column[1])
            if assignment[0] ^ assignment[1] ^ assignment[2] ^ assignment[3]:
                line.append(0)
                continue
            value = Fraction(1)
            for character in assignment:
                if character:
                    value *= Fraction(1, 2)
            internal_character = 0
            for position in true_side:
                internal_character ^= assignment[position]
            if internal_character:
                value *= Fraction(1, 2)
            line.append(Rational(value.numerator, value.denominator))
        matrix.append(line)
    return Matrix(matrix)


def crossing_tree_certificates():
    records = {}
    expected = {(0, 2): Rational(3, 1024), (0, 3): Rational(-3, 4096)}
    for true_side, expected_determinant in expected.items():
        matrix = wrong_split_flattening(true_side)
        determinant = matrix[:5, :5].det()
        assert matrix.rank() == 16 and determinant == expected_determinant
        name = "13|24" if true_side == (0, 2) else "14|23"
        records[name] = {
            "effective_pendant_and_internal_multipliers": "1/2",
            "flattening_split": "12|34",
            "full_exact_rank": 16,
            "upper_left_five_by_five_determinant": str(determinant),
        }
    return records


def generate_certificate():
    return {
        "status": {
            "local_common_switching_split_lemma": "PROVED",
            "generic_cut_split_rank_characterization": "PROVED",
            "generic_bridge_contraction_tree_reconstruction": "PROVED",
            "global_blob_tensor_factorization": "UNRESOLVED",
            "global_L1_classification": "UNRESOLVED",
        },
        "theta_root_compressed_two_colour_census": (
            theta_root_run_compressed_census()
        ),
        "cycle_root_compressed_two_colour_census": (
            cycle_root_run_compressed_census()
        ),
        "theta_compressed_two_colour_census": theta_run_compressed_census(),
        "cycle_compressed_two_colour_census": cycle_run_compressed_census(),
        "crossing_quartet_JC_fourier_flattenings": crossing_tree_certificates(),
        "cut_split_fourier_block_rank_bound": 4,
        "generic_non_cut_split_rank_lower_bound": 5,
        "conclusion": (
            "outside a proper algebraic exceptional set, a nontrivial leaf "
            "split is induced by a cut edge exactly when its JC pattern or "
            "Fourier flattening has rank at most four"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(json.dumps(generate_certificate(), sort_keys=True))
    if args.write_certificate:
        CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    else:
        assert certificate == json.loads(CERTIFICATE.read_text())
    print(json.dumps(certificate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
