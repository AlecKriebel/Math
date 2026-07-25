#!/usr/bin/env python3
"""Independent exact audit of the 12-antipodal-line ADE reduction.

Only the Python standard library is used.  All linear algebra is performed
with Fraction.  For every 12-line subset of the canonical A5, D5, and
D4+A1 root-line sets, the program:

* determines its exact rank;
* for every full-rank subset chooses five independent selected roots;
* enumerates all {-1,0,1} pairings with those roots;
* reconstructs the unique ambient vector exactly;
* keeps precisely the norm-two vectors pairing in {-1,0,1} with all
  twelve selected roots.

The last step enumerates the relevant dual shell even if the five roots
chosen for coordinates are not a primitive lattice basis.

The rank-four D4 case is treated separately in R4 plus a one-dimensional
orthogonal complement, followed by an exact compatibility-clique check.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from typing import Iterable, Sequence


Vector = tuple[int, ...]
Matrix = tuple[tuple[Fraction, ...], ...]


def dot(
    left: Sequence[Fraction | int],
    right: Sequence[Fraction | int],
    weights: Sequence[int],
) -> Fraction:
    return sum(
        Fraction(weight) * Fraction(x) * Fraction(y)
        for x, y, weight in zip(left, right, weights)
    )


def canonical_a(rank: int) -> tuple[tuple[Vector, ...], tuple[int, ...]]:
    """Line representatives e_i-e_j for A_rank in R^(rank+1)."""

    roots = []
    for i, j in combinations(range(rank + 1), 2):
        root = [0] * (rank + 1)
        root[i] = 1
        root[j] = -1
        roots.append(tuple(root))
    return tuple(roots), (1,) * (rank + 1)


def canonical_d(rank: int) -> tuple[tuple[Vector, ...], tuple[int, ...]]:
    """Line representatives e_i-e_j and e_i+e_j for D_rank."""

    roots = []
    for i, j in combinations(range(rank), 2):
        minus = [0] * rank
        minus[i] = 1
        minus[j] = -1
        roots.append(tuple(minus))
        plus = [0] * rank
        plus[i] = 1
        plus[j] = 1
        roots.append(tuple(plus))
    return tuple(roots), (1,) * rank


def canonical_d4_a1() -> tuple[tuple[Vector, ...], tuple[int, ...]]:
    """D4 plus an A1 coordinate whose metric coefficient is two."""

    d4, _ = canonical_d(4)
    lifted = tuple(root + (0,) for root in d4)
    return lifted + ((0, 0, 0, 0, 1),), (1, 1, 1, 1, 2)


def matrix_rank(rows: Iterable[Sequence[Fraction | int]]) -> int:
    work = [list(map(Fraction, row)) for row in rows]
    if not work:
        return 0
    width = len(work[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def inverse(matrix: Sequence[Sequence[Fraction | int]]) -> Matrix:
    size = len(matrix)
    work = [
        list(map(Fraction, row))
        + [Fraction(int(i == j)) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            row for row in range(column, size) if work[row][column]
        )
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [value / scale for value in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(work[row], work[column])
            ]
    return tuple(
        tuple(work[row][size + column] for column in range(size))
        for row in range(size)
    )


def mat_vec(
    matrix: Sequence[Sequence[Fraction | int]],
    vector: Sequence[Fraction | int],
) -> tuple[Fraction, ...]:
    return tuple(
        sum(Fraction(value) * Fraction(entry) for value, entry in zip(row, vector))
        for row in matrix
    )


def quadratic(
    vector: Sequence[Fraction | int],
    matrix: Sequence[Sequence[Fraction | int]],
) -> Fraction:
    image = mat_vec(matrix, vector)
    return sum(Fraction(x) * y for x, y in zip(vector, image))


def independent_masks(
    roots: Sequence[Vector],
    rank: int,
) -> set[int]:
    result = set()
    for indices in combinations(range(len(roots)), rank):
        if matrix_rank(roots[index] for index in indices) == rank:
            result.add(sum(1 << index for index in indices))
    return result


def first_basis(
    selected: tuple[int, ...],
    rank: int,
    basis_masks: set[int],
) -> tuple[int, ...] | None:
    for indices in combinations(selected, rank):
        mask = sum(1 << index for index in indices)
        if mask in basis_masks:
            return indices
    return None


def candidate_bad_masks(
    roots: Sequence[Vector],
    weights: Sequence[int],
    basis: tuple[int, ...],
) -> tuple[int, ...]:
    """Return one bad-line mask for every norm-two pairing vector."""

    basis_roots = tuple(roots[index] for index in basis)
    gram = tuple(
        tuple(dot(left, right, weights) for right in basis_roots)
        for left in basis_roots
    )
    gram_inverse = inverse(gram)

    # If alpha=sum_j d_j basis_j, then H d=((basis_i,alpha))_i.
    root_coordinates = []
    for root in roots:
        pairings = tuple(dot(base, root, weights) for base in basis_roots)
        root_coordinates.append(mat_vec(gram_inverse, pairings))

    allowed = {Fraction(-1), Fraction(0), Fraction(1)}
    bad_masks = []
    for pairing_vector in product((-1, 0, 1), repeat=len(basis)):
        if quadratic(pairing_vector, gram_inverse) != 2:
            continue
        bad_mask = 0
        for index, coordinates in enumerate(root_coordinates):
            pairing = sum(
                Fraction(value) * coordinate
                for value, coordinate in zip(pairing_vector, coordinates)
            )
            if pairing not in allowed:
                bad_mask |= 1 << index
        bad_masks.append(bad_mask)
    return tuple(bad_masks)


def audit_full_rank_subsets(
    name: str,
    roots: Sequence[Vector],
    weights: Sequence[int],
    rank: int = 5,
) -> dict[str, object]:
    basis_masks = independent_masks(roots, rank)
    cache: dict[tuple[int, ...], tuple[int, ...]] = {}
    distribution: Counter[int] = Counter()
    maximum = -1
    maximizers: list[tuple[int, ...]] = []
    rank_deficient: list[tuple[int, ...]] = []

    for selected in combinations(range(len(roots)), 12):
        basis = first_basis(selected, rank, basis_masks)
        if basis is None:
            rank_deficient.append(selected)
            continue
        if basis not in cache:
            cache[basis] = candidate_bad_masks(roots, weights, basis)
        selected_mask = sum(1 << index for index in selected)
        count = sum(
            not (bad_mask & selected_mask)
            for bad_mask in cache[basis]
        )
        distribution[count] += 1
        if count > maximum:
            maximum = count
            maximizers = [selected]
        elif count == maximum:
            maximizers.append(selected)

    return {
        "name": name,
        "subsets": sum(distribution.values()) + len(rank_deficient),
        "full_rank": sum(distribution.values()),
        "rank_deficient": tuple(rank_deficient),
        "distribution": dict(sorted(distribution.items())),
        "maximum": maximum,
        "maximizers": tuple(maximizers),
        "basis_cache_size": len(cache),
    }


def d4_projected_candidates(
    selected: tuple[int, ...] | None = None,
) -> tuple[
    tuple[tuple[Fraction, ...], Fraction], ...
]:
    """Return (basis pairings, projected norm) for admissible D4 vectors."""

    roots, weights = canonical_d(4)
    if selected is None:
        selected = tuple(range(len(roots)))
    basis_masks = independent_masks(roots, 4)
    basis = first_basis(selected, 4, basis_masks)
    assert basis is not None
    basis_roots = tuple(roots[index] for index in basis)
    gram = tuple(
        tuple(dot(left, right, weights) for right in basis_roots)
        for left in basis_roots
    )
    gram_inverse = inverse(gram)
    coordinates = []
    for root in roots:
        pairings = tuple(dot(base, root, weights) for base in basis_roots)
        coordinates.append(mat_vec(gram_inverse, pairings))

    allowed = {Fraction(-1), Fraction(0), Fraction(1)}
    result = []
    for pairing_vector in product((-1, 0, 1), repeat=4):
        norm = quadratic(pairing_vector, gram_inverse)
        if norm > 2:
            continue
        if all(
            sum(
                Fraction(value) * coordinate
                for value, coordinate in zip(pairing_vector, root_coordinates)
            )
            in allowed
            for index, root_coordinates in enumerate(coordinates)
            if index in selected
        ):
            result.append((tuple(map(Fraction, pairing_vector)), norm))
    return tuple(result)


def audit_rank4_d4_eleven_lines() -> dict[str, object]:
    roots, weights = canonical_d(4)
    distributions = []
    for omitted in range(len(roots)):
        selected = tuple(index for index in range(len(roots)) if index != omitted)
        projected = d4_projected_candidates(selected)
        distribution = Counter(norm for _, norm in projected)
        if distribution != {
            Fraction(0): 1,
            Fraction(1): 24,
            Fraction(2): 2,
        }:
            raise AssertionError((omitted, distribution))

        basis = first_basis(
            selected,
            4,
            independent_masks(roots, 4),
        )
        assert basis is not None
        basis_roots = tuple(roots[index] for index in basis)
        expected_missing_pairings = {
            tuple(
                Fraction(sign) * dot(roots[omitted], base, weights)
                for base in basis_roots
            )
            for sign in (-1, 1)
        }
        observed_norm_two = {
            pairing_vector
            for pairing_vector, norm in projected
            if norm == 2
        }
        if observed_norm_two != expected_missing_pairings:
            raise AssertionError("unexpected norm-two projected candidate")
        distributions.append(
            {str(key): value for key, value in sorted(distribution.items())}
        )
    return {
        "omissions": len(distributions),
        "distributions": tuple(distributions),
    }


def character_support_distribution(
    roots: Sequence[Vector],
    weights: Sequence[int],
    simple_roots: Sequence[Vector],
) -> dict[int, int]:
    """Support sizes on root lines of nonzero L -> F2 characters."""

    gram = tuple(
        tuple(dot(left, right, weights) for right in simple_roots)
        for left in simple_roots
    )
    gram_inverse = inverse(gram)
    coordinates = []
    for root in roots:
        pairings = tuple(dot(base, root, weights) for base in simple_roots)
        root_coordinates = mat_vec(gram_inverse, pairings)
        if any(value.denominator != 1 for value in root_coordinates):
            raise AssertionError("a root has nonintegral simple-root coordinates")
        coordinates.append(tuple(int(value) for value in root_coordinates))

    distribution: Counter[int] = Counter()
    for character in product((0, 1), repeat=len(simple_roots)):
        if not any(character):
            continue
        support = sum(
            sum(
                bit * coordinate
                for bit, coordinate in zip(character, root_coordinates)
            )
            % 2
            for root_coordinates in coordinates
        )
        distribution[support] += 1
    return dict(sorted(distribution.items()))


def audit_r11_character_bounds() -> dict[str, object]:
    a4, a4_weights = canonical_a(4)
    d4, d4_weights = canonical_d(4)
    a4_simple = tuple(
        tuple(
            1 if coordinate == index
            else -1 if coordinate == index + 1
            else 0
            for coordinate in range(5)
        )
        for index in range(4)
    )
    d4_simple = (
        (1, -1, 0, 0),
        (0, 1, -1, 0),
        (0, 0, 1, -1),
        (0, 0, 1, 1),
    )
    a4_distribution = character_support_distribution(
        a4,
        a4_weights,
        a4_simple,
    )
    d4_distribution = character_support_distribution(
        d4,
        d4_weights,
        d4_simple,
    )
    if a4_distribution != {4: 5, 6: 10}:
        raise AssertionError(a4_distribution)
    if d4_distribution != {6: 12, 8: 3}:
        raise AssertionError(d4_distribution)

    cover_lower_bounds = {
        d: d * (5 - d)
        for d in (1, 2, 3)
    }
    if cover_lower_bounds != {1: 4, 2: 6, 3: 6}:
        raise AssertionError(cover_lower_bounds)
    if any(value <= 3 for value in cover_lower_bounds.values()):
        raise AssertionError("rank-four defect contradiction is too weak")

    # Exact number of antipodal lines in the norm-two dual shell for every
    # rank-five ADE type having at least eight root lines.
    dual_shell_lines = {
        "A5": 15,
        "D5": 20,
        "D4+A1": 13,
        "A4+A1": 11,
        "A3+A2": 9,
        # A3+2A1 has 8 root lines and 12 cross-component lines:
        # 6 norm-one A3* vectors times 2*2 minimal A1* choices gives
        # 24 oriented, hence 12 antipodal, cross vectors.
        "A3+2A1": 20,
    }
    if max(dual_shell_lines.values()) != 20:
        raise AssertionError(dual_shell_lines)
    return {
        "A4_character_support": a4_distribution,
        "D4_character_support": d4_distribution,
        "cover_lower_bounds": cover_lower_bounds,
        "dual_shell_lines": dual_shell_lines,
    }


def maximum_clique(adjacency: Sequence[int]) -> tuple[int, int]:
    """Exact bitset branch-and-bound; return size and one clique mask."""

    best_mask = 0
    popcount = lambda value: bin(value).count("1")

    def expand(clique: int, candidates: int) -> None:
        nonlocal best_mask
        if popcount(clique) + popcount(candidates) <= popcount(best_mask):
            return
        while candidates:
            if popcount(clique) + popcount(candidates) <= popcount(best_mask):
                return
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            new_clique = clique | bit
            if popcount(new_clique) > popcount(best_mask):
                best_mask = new_clique
            expand(new_clique, candidates & adjacency[vertex])

    expand(0, (1 << len(adjacency)) - 1)
    return popcount(best_mask), best_mask


def audit_rank4_d4() -> dict[str, object]:
    projected = d4_projected_candidates()
    norm_distribution = Counter(norm for _, norm in projected)
    if set(norm_distribution) != {Fraction(0), Fraction(1)}:
        raise AssertionError(f"unexpected D4 projected norms: {norm_distribution}")

    roots, weights = canonical_d(4)
    basis = first_basis(
        tuple(range(len(roots))),
        4,
        independent_masks(roots, 4),
    )
    assert basis is not None
    basis_roots = tuple(roots[index] for index in basis)
    gram = tuple(
        tuple(dot(left, right, weights) for right in basis_roots)
        for left in basis_roots
    )
    gram_inverse = inverse(gram)

    expected_projected_vectors = []
    for coordinate in range(4):
        for sign in (-1, 1):
            vector = [Fraction(0)] * 4
            vector[coordinate] = Fraction(sign)
            expected_projected_vectors.append(tuple(vector))
    expected_projected_vectors.extend(
        tuple(Fraction(sign, 2) for sign in signs)
        for signs in product((-1, 1), repeat=4)
    )
    expected_pairings = {
        tuple(dot(vector, base, weights) for base in basis_roots)
        for vector in expected_projected_vectors
    }
    observed_pairings = {
        pairing_vector
        for pairing_vector, norm in projected
        if norm == 1
    }
    if observed_pairings != expected_pairings:
        raise AssertionError("the projected shell is not the 24-cell")

    # Candidate is (basis-pairing vector for p, symbolic height).
    # Heights are ±sqrt(2) for p=0 and ±1 for projected norm one.
    candidates: list[tuple[tuple[Fraction, ...], str | int]] = []
    for pairing_vector, norm in projected:
        if norm == 0:
            candidates.extend(
                ((pairing_vector, "+sqrt2"), (pairing_vector, "-sqrt2"))
            )
        elif norm == 1:
            candidates.extend(((pairing_vector, 1), (pairing_vector, -1)))

    scaled_colors = {
        Fraction(-3, 2),
        Fraction(-1),
        Fraction(-1, 2),
        Fraction(0),
        Fraction(1),
    }

    def compatible(
        left: tuple[tuple[Fraction, ...], str | int],
        right: tuple[tuple[Fraction, ...], str | int],
    ) -> bool:
        left_pairing, left_height = left
        right_pairing, right_height = right
        projected_inner = sum(
            Fraction(x) * y
            for x, y in zip(left_pairing, mat_vec(gram_inverse, right_pairing))
        )
        if isinstance(left_height, str) or isinstance(right_height, str):
            # Opposite poles have inner product -2 (a forbidden thirteenth
            # antipodal pair); a pole and a norm-one candidate have irrational
            # inner product ±sqrt(2), outside the quarter grid.
            return False
        return projected_inner + left_height * right_height in scaled_colors

    adjacency = [0] * len(candidates)
    for i, j in combinations(range(len(candidates)), 2):
        if compatible(candidates[i], candidates[j]):
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    clique_number, clique_mask = maximum_clique(adjacency)

    # Same-height norm-one subgraph: compatibility is exactly p.q in {-1,0}.
    same_sign_indices = [
        index
        for index, (_, height) in enumerate(candidates)
        if height == 1
    ]
    compressed = [0] * len(same_sign_indices)
    for ii, i in enumerate(same_sign_indices):
        for jj, j in enumerate(same_sign_indices):
            if ii != jj and (adjacency[i] >> j) & 1:
                compressed[ii] |= 1 << jj
    same_sign_number, _ = maximum_clique(compressed)

    unseen = set(range(len(compressed)))
    component_sizes = []
    while unseen:
        seed = unseen.pop()
        component = {seed}
        frontier = [seed]
        while frontier:
            vertex = frontier.pop()
            neighbors = {
                index
                for index in unseen
                if (compressed[vertex] >> index) & 1
            }
            unseen.difference_update(neighbors)
            component.update(neighbors)
            frontier.extend(neighbors)
        component_sizes.append(len(component))
        for i, j in combinations(component, 2):
            if not ((compressed[i] >> j) & 1):
                raise AssertionError("a same-height component is not complete")
    component_sizes.sort()

    return {
        "projected_norm_distribution": {
            str(key): value for key, value in sorted(norm_distribution.items())
        },
        "candidate_count": len(candidates),
        "clique_number": clique_number,
        "same_height_clique_number": same_sign_number,
        "same_height_component_sizes": tuple(component_sizes),
        "clique_indices": tuple(
            index
            for index in range(len(candidates))
            if (clique_mask >> index) & 1
        ),
    }


def self_test() -> dict[str, object]:
    a5, a5_weights = canonical_a(5)
    d5, d5_weights = canonical_d(5)
    d4a1, d4a1_weights = canonical_d4_a1()
    if (len(a5), len(d5), len(d4a1)) != (15, 20, 13):
        raise AssertionError("canonical root-line counts are wrong")
    for roots, weights in (
        (a5, a5_weights),
        (d5, d5_weights),
        (d4a1, d4a1_weights),
    ):
        if any(dot(root, root, weights) != 2 for root in roots):
            raise AssertionError("a canonical root does not have norm two")

    results = {
        "A5": audit_full_rank_subsets("A5", a5, a5_weights),
        "D5": audit_full_rank_subsets("D5", d5, d5_weights),
        "D4+A1": audit_full_rank_subsets(
            "D4+A1",
            d4a1,
            d4a1_weights,
        ),
        "D4_rank4": audit_rank4_d4(),
        "D4_rank4_eleven": audit_rank4_d4_eleven_lines(),
        "r11_character_bounds": audit_r11_character_bounds(),
    }

    expected = {
        "A5": (455, 455, 0, 6),
        "D5": (125970, 125965, 5, 16),
        "D4+A1": (13, 12, 1, 2),
    }
    for name, (subsets, full_rank, deficient, maximum) in expected.items():
        result = results[name]
        observed = (
            result["subsets"],
            result["full_rank"],
            len(result["rank_deficient"]),
            result["maximum"],
        )
        if observed != (subsets, full_rank, deficient, maximum):
            raise AssertionError((name, observed))
    d4_result = results["D4_rank4"]
    if d4_result["projected_norm_distribution"] != {"0": 1, "1": 24}:
        raise AssertionError(d4_result)
    if d4_result["candidate_count"] != 50:
        raise AssertionError(d4_result)
    if d4_result["same_height_clique_number"] != 8:
        raise AssertionError(d4_result)
    if d4_result["same_height_component_sizes"] != (8, 8, 8):
        raise AssertionError(d4_result)
    if d4_result["clique_number"] != 16:
        raise AssertionError(d4_result)
    d4_eleven = results["D4_rank4_eleven"]
    if d4_eleven["omissions"] != 12:
        raise AssertionError(d4_eleven)
    r11 = results["r11_character_bounds"]
    if r11["cover_lower_bounds"] != {1: 4, 2: 6, 3: 6}:
        raise AssertionError(r11)
    return results


def main() -> None:
    results = self_test()
    for name in ("A5", "D5", "D4+A1"):
        result = results[name]
        print(
            f"{name}: subsets={result['subsets']}, "
            f"full_rank={result['full_rank']}, "
            f"rank_deficient={len(result['rank_deficient'])}, "
            f"max_shell={result['maximum']}, "
            f"distribution={result['distribution']}"
        )
    d4 = results["D4_rank4"]
    print(
        "D4 rank4: "
        f"projected={d4['projected_norm_distribution']}, "
        f"candidates={d4['candidate_count']}, "
        f"same-height clique={d4['same_height_clique_number']}, "
        f"same-height components={d4['same_height_component_sizes']}, "
        f"full clique={d4['clique_number']}"
    )
    d4_eleven = results["D4_rank4_eleven"]
    print(
        "D4 rank4 with 11 core lines: "
        f"omissions={d4_eleven['omissions']}, "
        "projected={'0': 1, '1': 24, '2': 2}"
    )
    r11 = results["r11_character_bounds"]
    print(
        "r11 defect audit: "
        f"A4 characters={r11['A4_character_support']}, "
        f"D4 characters={r11['D4_character_support']}, "
        f"cover bounds={r11['cover_lower_bounds']}, "
        f"max dual-shell lines={max(r11['dual_shell_lines'].values())}"
    )
    print("PASS: exact ADE core-shell enumeration")


if __name__ == "__main__":
    main()
