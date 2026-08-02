#!/usr/bin/env python3
"""Exact all-threshold audit of the 600-point dual golden orbit.

Start with the 120 vectors of squared norm 16 in Z[sqrt(5)] used by the
golden H4 search.  Enumerate the 600 K4s in their positive
4+4*sqrt(5) relation graph.  For a K4 Q, this file stores the scaled centroid

    p_Q = sum(v for v in Q) = 4 * actual_centroid(Q).

All 600 sums are distinct and have squared norm 112+48*sqrt(5).  Their 30
pair-product values are audited as possible diameter thresholds.

At five low thresholds, frozen five-colorings of the full equality-relation
graph eliminate every subset.  At every other threshold, a complete CEGAR
search proves that no admissible set can induce minimum equality-degree five.
Every admissible threshold graph is consequently 4-degenerate and hence
five-colorable.  The search is reduced to one vertex by four exact root
reflections whose action is verified to be transitive on the 600 points.

Only the Python standard library is used.  The frozen colorings are checked
edge by edge; no SAT solver is needed to replay the certificate.
"""

from __future__ import annotations

import functools
import hashlib
import itertools
from dataclasses import dataclass
from typing import Iterable, Iterator, Sequence


Quadratic = tuple[int, int]  # a+b*sqrt(5), positive real embedding
Point = tuple[Quadratic, Quadratic, Quadratic, Quadratic]


def qadd(x: Quadratic, y: Quadratic) -> Quadratic:
    return x[0] + y[0], x[1] + y[1]


def qsub(x: Quadratic, y: Quadratic) -> Quadratic:
    return x[0] - y[0], x[1] - y[1]


def qmul(x: Quadratic, y: Quadratic) -> Quadratic:
    return x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def qsign(x: Quadratic) -> int:
    """Exact sign of a+b*sqrt(5)."""
    a, b = x
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return 1 if a > 0 else -1
    comparison = a * a - 5 * b * b
    assert comparison != 0
    return (1 if a > 0 else -1) * ((comparison > 0) - (comparison < 0))


def qcompare(x: Quadratic, y: Quadratic) -> int:
    return qsign(qsub(x, y))


def qdot(x: Point, y: Point) -> Quadratic:
    answer = (0, 0)
    for a, b in zip(x, y):
        answer = qadd(answer, qmul(a, b))
    return answer


def point_sum(points: Iterable[Point]) -> Point:
    result = [(0, 0)] * 4
    for point in points:
        for coordinate in range(4):
            result[coordinate] = qadd(result[coordinate], point[coordinate])
    return tuple(result)  # type: ignore[return-value]


def permutation_parity(permutation: Sequence[int]) -> int:
    return sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    ) % 2


def golden_vectors_scaled_by_four() -> list[Point]:
    """Reconstruct the exact 120-vector golden system from first principles."""
    points: list[Point] = []
    zero = (0, 0)
    for coordinate in range(4):
        for sign in (-1, 1):
            point = [zero] * 4
            point[coordinate] = (4 * sign, 0)
            points.append(tuple(point))  # type: ignore[arg-type]
    for signs in itertools.product((-1, 1), repeat=4):
        points.append(tuple((2 * sign, 0) for sign in signs))  # type: ignore[arg-type]

    base: Point = ((0, 0), (2, 0), (1, 1), (-1, 1))
    for permutation in itertools.permutations(range(4)):
        if permutation_parity(permutation):
            continue
        permuted = tuple(base[permutation[i]] for i in range(4))
        nonzero = [i for i, value in enumerate(permuted) if value != zero]
        for signs in itertools.product((-1, 1), repeat=3):
            point = list(permuted)
            for coordinate, sign in zip(nonzero, signs):
                a, b = point[coordinate]
                point[coordinate] = sign * a, sign * b
            points.append(tuple(point))  # type: ignore[arg-type]

    answer = sorted(set(points))
    assert len(answer) == 120
    assert {qdot(point, point) for point in answer} == {(16, 0)}
    return answer


def dot_table(points: Sequence[Point]) -> list[list[Quadratic]]:
    result = [[(0, 0)] * len(points) for _ in points]
    for i, point in enumerate(points):
        result[i][i] = qdot(point, point)
        for j in range(i):
            result[i][j] = result[j][i] = qdot(point, points[j])
    return result


def relation_masks(
    table: Sequence[Sequence[Quadratic]], target: Quadratic
) -> tuple[int, ...]:
    return tuple(
        sum(1 << j for j in range(len(table))
            if j != i and table[i][j] == target)
        for i in range(len(table))
    )


def compatibility_masks(
    table: Sequence[Sequence[Quadratic]], threshold: Quadratic
) -> tuple[int, ...]:
    return tuple(
        sum(1 << j for j in range(len(table))
            if j != i and qsign(qsub(table[i][j], threshold)) >= 0)
        for i in range(len(table))
    )


def enumerate_k4s(adjacency: Sequence[int]) -> list[tuple[int, int, int, int]]:
    """Enumerate every K4 once in increasing vertex order."""
    result: list[tuple[int, int, int, int]] = []
    n = len(adjacency)
    for a in range(n):
        later_a = adjacency[a] & ~((1 << (a + 1)) - 1)
        while later_a:
            b_bit = later_a & -later_a
            later_a ^= b_bit
            b = b_bit.bit_length() - 1
            common = adjacency[a] & adjacency[b] & ~((1 << (b + 1)) - 1)
            while common:
                c_bit = common & -common
                common ^= c_bit
                c = c_bit.bit_length() - 1
                choices = (adjacency[a] & adjacency[b] & adjacency[c]
                           & ~((1 << (c + 1)) - 1))
                while choices:
                    d_bit = choices & -choices
                    choices ^= d_bit
                    result.append((a, b, c, d_bit.bit_length() - 1))
    assert result == sorted(set(result))
    return result


def dual_centroid_orbit() -> tuple[list[Point], list[tuple[int, int, int, int]], list[Point]]:
    roots = golden_vectors_scaled_by_four()
    root_table = dot_table(roots)
    positive_relation = relation_masks(root_table, (4, 4))
    k4s = enumerate_k4s(positive_relation)
    assert len(k4s) == 600
    centroids = [point_sum(roots[i] for i in clique) for clique in k4s]
    assert len(set(centroids)) == 600
    assert {qdot(point, point) for point in centroids} == {(112, 48)}
    return roots, k4s, centroids


THRESHOLDS: tuple[Quadratic, ...] = (
    (-112, -48), (-104, -48), (-100, -44), (-88, -40), (-84, -36),
    (-76, -36), (-72, -32), (-60, -28), (-56, -24), (-44, -20),
    (-40, -16), (-32, -16), (-28, -12), (-16, -8), (-12, -4),
    (0, 0), (12, 4), (16, 8), (28, 12), (32, 16), (40, 16),
    (44, 20), (56, 24), (60, 28), (72, 32), (76, 36), (84, 36),
    (88, 40), (100, 44), (104, 48),
)


EXPECTED_RELATION_DEGREES = (
    1, 4, 12, 24, 12, 4, 24, 24, 32, 24, 12, 24, 28, 24, 24,
    54, 24, 24, 28, 24, 12, 24, 32, 24, 24, 4, 12, 24, 12, 4,
)


EXPECTED_COMPATIBILITY_DEGREES = (
    599, 598, 594, 582, 558, 546, 542, 518, 494, 462, 438, 426,
    402, 374, 350, 326, 272, 248, 224, 196, 172, 160, 136, 104,
    80, 56, 52, 40, 16, 4,
)


# Full-relation five-color certificates at the only thresholds not eliminated
# by the compatible-core search.  Vertices use the deterministic K4 order
# returned by enumerate_k4s; each character is a color in {0,...,4}.
FULL_RELATION_COLORINGS: dict[int, str] = {
    2: "244433333333341443343323333223333303330311111111113331131111222113322332323222224211240100320222222112111211112111233011333001131131103003031300000020033002222233333322321110010010000100203202232111111111131110422230003311300101003000033300332000000000300111130000041010222222222222222222221111111111100111111112113111143322113222111112221222221221220302243433011313211411112111111111121210022200000002200002002221211111322121222100000000000001010000000000200002200020002233322002200032233000000000110000011000111132122310200112002212022122000211212122322303122200020000110001111110000112012110001000",
    3: "424222024204222222222200000000220002000011122212202222021121240024000444414444142121122122224242111121211111114111020000002000032220000424424434324242432330000024434440402222222222212120000000000302222132120000444240222222233222222322322220332232333220000232004334322222014010010444014101401111111111111111111101111000000001101010111114411144111111110000000000000000000000011112130122120013444244443433343411433311121211111111111100000332330030303330333333333333333333330000040334300304400322331222311333311333110104140022432303331111011111414111011111011103303310340303113321113113333331133033413133",
    6: "000000000000000000000000000000000000000000000000000000000000000000000100000000100000000001000000001000000000000000000022021210212101221000330111101111011110000101111011110000211112011320444404444122220222202024030331111101122111110121101144111110111101144111220111111211404334444444443443342333322222332232232303033442224444234223333333333333333333334444444444222444244422222222222222222222333334433433333333343333333313333333333321441222221222122111111111111111111111114444444414444144444422222222232221223222002243334422413121113333333333333332222244232344244313441244222223212331112222224233331411",
    7: "000000000000000000000000000000000000000000000000000000000000000000101100001010100000001011000010101000000000000000000022022222222202222111111111111111111114404414141044440203212111033130444404444022220333300024111112222222222122122222222222221222222222222022221141121211444444444444444444443333303333333333333304033030330444343333043331101114143413334444444444223444444433333332232243233333111411111411141411111111111113111313111122222222222222222222111221122211112111114424444444442444444423222332233222233322400341114232411121224333333333431433333344443444444444442344333333333332332333334413131412",
    8: "024130414021323324200412313402410212203423301021032041311302234314231004321134224212030412314432014314203031414421030401214301430244321102131043241003302411420331120024330423123310442302042303211423433201410343223103421010412341020012342031033141204031042231144431001422104313142414320302410441334110234202342120324240434302304123014301404230142324014301234021132341410202140044022141321024340424203021314401232313002423142431304040142012133241030324312340414242132141320424021134040233214141230301242041031430301240211332021003134301220231124011312420314013240342141030302114104300344402433231432204",
}


EXPECTED_COLORING_DIGESTS = {
    2: "ced569a0d96eb4fa340e6346f779fbd3d305ce9bbe562e7dfde6819907ef1f1b",
    3: "314347bed87686f429dea4d7154fed2030788d03929511d2feb715de2f9abb01",
    6: "71fe9ac7e86f55f0953e3ebb91cdb81770c63db091fdb923789b4efff79d7eb8",
    7: "3dedc81f06e5881c16c9a7f85a224ce7856087abec33d3d7e7c09024eae10729",
    8: "10d26dddfd0fa4a85f3cf301491af5417c717a4292e84a2045b32740495f4f3b",
}


def verify_coloring(adjacency: Sequence[int], encoded: str) -> None:
    assert len(encoded) == len(adjacency)
    assert set(encoded) <= set("01234")
    colors = tuple(map(int, encoded))
    for i, neighbors in enumerate(adjacency):
        while neighbors:
            bit = neighbors & -neighbors
            neighbors ^= bit
            j = bit.bit_length() - 1
            assert colors[i] != colors[j]


# These four norm-16 roots generate a transitive reflection action on the
# centroid orbit.  The checker reconstructs their permutations exactly.
REFLECTION_ROOTS: tuple[Point, ...] = (
    ((4, 0), (0, 0), (0, 0), (0, 0)),
    ((1, 1), (1, -1), (0, 0), (2, 0)),
    ((2, 0), (2, 0), (2, 0), (2, 0)),
    ((2, 0), (2, 0), (2, 0), (-2, 0)),
)


def reflect(point: Point, root: Point) -> Point:
    """Reflect in root^perp, using root.root=16 exactly."""
    assert qdot(root, root) == (16, 0)
    product = qdot(point, root)
    result: list[Quadratic] = []
    for coordinate, root_coordinate in zip(point, root):
        correction = qmul(product, root_coordinate)
        assert correction[0] % 8 == correction[1] % 8 == 0
        result.append((
            coordinate[0] - correction[0] // 8,
            coordinate[1] - correction[1] // 8,
        ))
    return tuple(result)  # type: ignore[return-value]


def reflection_permutations(
    points: Sequence[Point], table: Sequence[Sequence[Quadratic]]
) -> tuple[tuple[int, ...], ...]:
    index = {point: i for i, point in enumerate(points)}
    assert len(index) == len(points)
    permutations = tuple(
        tuple(index[reflect(point, root)] for point in points)
        for root in REFLECTION_ROOTS
    )
    for permutation in permutations:
        assert len(set(permutation)) == len(points)
        # An independent exact check that the induced permutation preserves
        # every pair-product relation used below.
        for i in range(len(points)):
            for j in range(i):
                assert table[permutation[i]][permutation[j]] == table[i][j]

    reached = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for permutation in permutations:
            image = permutation[vertex]
            if image not in reached:
                reached.add(image)
                stack.append(image)
    assert len(reached) == len(points) == 600
    return permutations


def clique_subsets(mask: int, size: int, compatibility: Sequence[int]) -> Iterator[int]:
    """Yield all compatible subsets of the requested size, as bit masks."""
    def search(chosen: int, candidates: int, remaining: int) -> Iterator[int]:
        if remaining == 0:
            yield chosen
            return
        if candidates.bit_count() < remaining:
            return
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            yield from search(
                chosen | bit,
                candidates & compatibility[vertex],
                remaining - 1,
            )
    return search(0, mask, size)


@dataclass(frozen=True)
class CoreSearchResult:
    core: int | None
    seed_count: int
    search_nodes: int
    maximum_chosen_size: int


def find_compatible_five_core(
    relation: Sequence[int], compatibility: Sequence[int]
) -> CoreSearchResult:
    """Search exhaustively for a compatible induced subgraph of min degree 5.

    Transitivity lets vertex 0 represent an arbitrary vertex of a putative
    core.  We enumerate five compatible relation-neighbors of 0.  At a
    recursive state S, choose a deficient vertex v in S.  Any extending core
    must supply exactly ``5-deg_S(v)`` vertices from its still-compatible
    relation-neighbors; all such compatible choices are branched on.  Thus a
    negative result is complete, not heuristic.
    """
    n = len(relation)
    all_vertices = (1 << n) - 1
    search_nodes = 0
    seed_count = 0
    maximum_chosen_size = 0
    failed: set[tuple[int, int]] = set()

    def search(chosen: int, candidates: int) -> int | None:
        nonlocal search_nodes, maximum_chosen_size
        search_nodes += 1
        maximum_chosen_size = max(maximum_chosen_size, chosen.bit_count())
        deficits: list[tuple[int, int, int, int]] = []
        work = chosen
        while work:
            bit = work & -work
            work ^= bit
            vertex = bit.bit_length() - 1
            needed = 5 - (relation[vertex] & chosen).bit_count()
            if needed > 0:
                available = relation[vertex] & candidates
                if available.bit_count() < needed:
                    return None
                deficits.append((
                    available.bit_count() - needed,
                    available.bit_count(),
                    -needed,
                    vertex,
                ))
        if not deficits:
            return chosen
        state = chosen, candidates
        if state in failed:
            return None
        failed.add(state)

        _, _, neg_needed, vertex = min(deficits)
        needed = -neg_needed
        available = relation[vertex] & candidates
        for addition in clique_subsets(available, needed, compatibility):
            next_candidates = candidates & ~addition
            work = addition
            while work:
                bit = work & -work
                work ^= bit
                next_candidates &= compatibility[bit.bit_length() - 1]
            result = search(chosen | addition, next_candidates)
            if result is not None:
                return result
        return None

    for neighbors in clique_subsets(relation[0], 5, compatibility):
        seed_count += 1
        chosen = 1 | neighbors
        candidates = all_vertices & ~chosen
        work = chosen
        while work:
            bit = work & -work
            work ^= bit
            candidates &= compatibility[bit.bit_length() - 1]
        core = search(chosen, candidates)
        if core is not None:
            return CoreSearchResult(core, seed_count, search_nodes,
                                    maximum_chosen_size)
    return CoreSearchResult(None, seed_count, search_nodes, maximum_chosen_size)


def spectrum(table: Sequence[Sequence[Quadratic]]) -> tuple[Quadratic, ...]:
    values = {table[i][j] for i in range(len(table)) for j in range(i)}
    return tuple(sorted(values, key=functools.cmp_to_key(qcompare)))


def verify() -> None:
    roots, k4s, points = dual_centroid_orbit()
    assert len(roots) == 120 and len(k4s) == len(points) == 600
    assert hashlib.sha256(repr(k4s).encode()).hexdigest() == (
        "8413e79e674829660270ea05ef60dbfbb5598c6baa1e523243b010b2b9288517"
    )
    assert hashlib.sha256(repr(points).encode()).hexdigest() == (
        "62ce256266c0d737a9cd3f5c1386539fad1e0fe9c68058824b4305712872c752"
    )
    table = dot_table(points)
    assert spectrum(table) == THRESHOLDS
    reflection_permutations(points, table)

    results: list[tuple[int, Quadratic, int, int, str, int, int, int]] = []
    for index, threshold in enumerate(THRESHOLDS):
        relation = relation_masks(table, threshold)
        compatibility = compatibility_masks(table, threshold)
        relation_degrees = {mask.bit_count() for mask in relation}
        compatibility_degrees = {mask.bit_count() for mask in compatibility}
        assert relation_degrees == {EXPECTED_RELATION_DEGREES[index]}
        assert compatibility_degrees == {EXPECTED_COMPATIBILITY_DEGREES[index]}

        if index in FULL_RELATION_COLORINGS:
            encoded = FULL_RELATION_COLORINGS[index]
            assert hashlib.sha256(encoded.encode()).hexdigest() == EXPECTED_COLORING_DIGESTS[index]
            verify_coloring(relation, encoded)
            results.append((index, threshold, relation[0].bit_count(),
                            compatibility[0].bit_count(), "full-5-coloring",
                            0, 0, 0))
            continue

        core_result = find_compatible_five_core(relation, compatibility)
        assert core_result.core is None
        results.append((index, threshold, relation[0].bit_count(),
                        compatibility[0].bit_count(), "no-compatible-5-core",
                        core_result.seed_count, core_result.search_nodes,
                        core_result.maximum_chosen_size))

    print("dual golden 600-point all-threshold exact audit passed")
    print("centroids=600 norm_squared=(112,48) thresholds=30 symmetry_orbit=600")
    print("idx threshold relation_degree compatibility_degree method seeds nodes max_chosen")
    for row in results:
        print(*row)
    print("non_5_colorable_admissible_threshold_graphs=0")


def main() -> None:
    verify()


if __name__ == "__main__":
    main()
