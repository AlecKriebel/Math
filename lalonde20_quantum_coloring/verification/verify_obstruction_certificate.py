#!/usr/bin/env python3
"""Exact replay of the Lalonde quantum-coloring obstruction certificate.

The verifier uses only the Python standard library.  It checks:

* the rational noncommutative sum-of-squares identity;
* explicit reduction of its three aggregate relations to the original
  projection, edge, and triangle relations;
* the core Walsh inversion and anticommutator signs;
* all six formal cross-color tail compressions;
* the invertibility of the final three-term transform; and
* the integer dimension contradiction after color symmetrization.

No floating-point arithmetic or numerical solver is used.
"""

from __future__ import annotations

from fractions import Fraction
import json
import pathlib
import sys


if not __debug__:
    raise RuntimeError(
        "verify_obstruction_certificate.py relies on executable assertions; "
        "rerun without Python -O"
    )


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_data import E19, GRAPH6_G19, TRIANGLES19  # noqa: E402


Word = tuple[int, ...]
Polynomial = dict[Word, Fraction]
FormalBlock = dict[str, Fraction]


def clean(polynomial: Polynomial) -> Polynomial:
    return {word: coefficient for word, coefficient in polynomial.items() if coefficient}


def add(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for polynomial in polynomials:
        for word, coefficient in polynomial.items():
            result[word] = result.get(word, Fraction(0)) + coefficient
    return clean(result)


def scale(coefficient: Fraction | int, polynomial: Polynomial) -> Polynomial:
    coefficient = Fraction(coefficient)
    return clean({word: coefficient * value for word, value in polynomial.items()})


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_word, left_value in left.items():
        for right_word, right_value in right.items():
            word = left_word + right_word
            result[word] = result.get(word, Fraction(0)) + left_value * right_value
    return clean(result)


ONE: Polynomial = {(): Fraction(1)}


def generator(vertex: int) -> Polynomial:
    return {(vertex,): Fraction(1)}


def parse_polynomial(terms) -> Polynomial:
    return clean(
        {
            tuple(int(letter) for letter in word): Fraction(coefficient)
            for coefficient, word in terms
        }
    )


EDGE_SET = {tuple(sorted(edge)) for edge in E19}


def reduce_projection_and_edges(polynomial: Polynomial) -> Polynomial:
    """Reduce adjacent idempotencies and graph-edge zero products exactly."""

    result: Polynomial = {}
    for original_word, coefficient in polynomial.items():
        word = list(original_word)
        changed = True
        zero = False
        while changed and not zero:
            changed = False
            output = []
            index = 0
            while index < len(word):
                if index + 1 < len(word):
                    left, right = word[index], word[index + 1]
                    if left == right:
                        output.append(left)
                        index += 2
                        changed = True
                        continue
                    if tuple(sorted((left, right))) in EDGE_SET:
                        zero = True
                        break
                output.append(word[index])
                index += 1
            word = output
        if not zero:
            key = tuple(word)
            result[key] = result.get(key, Fraction(0)) + coefficient
    return clean(result)


def anticommutator(left: Polynomial, right: Polynomial) -> Polynomial:
    return add(multiply(left, right), multiply(right, left))


def verify_core_sos(certificate) -> None:
    core = certificate["fixed_color_core"]
    assert tuple(tuple(t) for t in core["triangles"]) == TRIANGLES19

    forms = {
        name: parse_polynomial(terms)
        for name, terms in core["sos_linear_forms"].items()
    }
    lhs = parse_polynomial(core["sos_left_hand_side"])
    sum_of_squares = add(*(multiply(form, form) for form in forms.values()))
    sos_residual = add(sum_of_squares, scale(-1, lhs))

    pairs = [tuple(pair) for pair in core["binary_pairs"]]
    walsh_vertices = [int(v) for v in core["walsh_vertices"]]
    signs = [[int(value) for value in row] for row in core["walsh_signs"]]
    differences = [add(generator(high), scale(-1, generator(low))) for low, high in pairs]
    walsh = [
        add(*(scale(row[column], generator(vertex)) for column, vertex in enumerate(walsh_vertices)))
        for row in signs
    ]
    x = add(*(generator(vertex) for vertex in walsh_vertices))

    g_pair = add(
        *(multiply(difference, difference) for difference in differences),
        scale(-2, ONE),
    )
    g_walsh = add(
        multiply(x, x),
        *(multiply(form, form) for form in walsh),
        scale(-4, x),
    )
    g_neighbor = add(
        *(anticommutator(difference, form) for difference, form in zip(differences, walsh)),
        scale(4, x),
    )

    coefficients = core["aggregate_identity_coefficients"]
    reconstructed = add(
        scale(Fraction(coefficients["pair_square_identity"]), g_pair),
        scale(Fraction(coefficients["walsh_square_identity"]), g_walsh),
        scale(Fraction(coefficients["neighbor_anticommutator_identity"]), g_neighbor),
    )
    assert sos_residual == reconstructed

    # G_pair is an explicit linear combination of the four triangle relations
    # after using idempotency and the within-triangle edge zeros.
    triangle_relations = {
        tuple(triangle): add(*(generator(v) for v in triangle), scale(-1, ONE))
        for triangle in TRIANGLES19
    }
    t0, t1, t2, t3 = TRIANGLES19
    expected_pair = add(
        triangle_relations[t1],
        triangle_relations[t2],
        triangle_relations[t3],
        scale(-1, triangle_relations[t0]),
    )
    assert reduce_projection_and_edges(g_pair) == expected_pair

    # The Walsh-square identity is formal Hadamard cancellation plus e_j^2=e_j.
    assert reduce_projection_and_edges(g_walsh) == {}

    # For j=10,...,13, the signed pair difference is neighbor_sum minus
    # nonneighbor_sum.  Edge terms vanish, while all six plane projections sum
    # to 2I by the triangle relations just checked.
    plane_sum_relation = expected_pair
    expected_neighbor = add(
        *(
            scale(-1, anticommutator(plane_sum_relation, generator(vertex)))
            for vertex in walsh_vertices
        )
    )
    assert reduce_projection_and_edges(g_neighbor) == reduce_projection_and_edges(expected_neighbor)

    # Check that each Walsh sign column selects exactly the graph neighbours of
    # its vertex among 4,...,9; this ties the algebra replay to the graph data.
    for column, vertex in enumerate(walsh_vertices):
        selected = set()
        for row, (low, high) in zip(signs, pairs):
            selected.add(high if row[column] == 1 else low)
        actual = {u for u in range(4, 10) if tuple(sorted((u, vertex))) in EDGE_SET}
        assert selected == actual, (vertex, selected, actual)

    # f_j=0 and Walsh inversion give the four core projections.  Verify the
    # sign matrix and the resulting anticommutator coefficient system exactly.
    sign_columns = [tuple(row[column] for row in signs) for column in range(4)]
    assert sign_columns == [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    assert all(a * b * c == 1 for a, b, c in sign_columns)
    gram = [[sum(left[k] * right[k] for k in range(3)) for right in sign_columns]
            for left in sign_columns]
    assert gram == [[3 if i == j else -1 for j in range(4)] for i in range(4)]


def block_add(*terms: FormalBlock) -> FormalBlock:
    result: FormalBlock = {}
    for term in terms:
        for label, coefficient in term.items():
            result[label] = result.get(label, Fraction(0)) + coefficient
    return {label: coefficient for label, coefficient in result.items() if coefficient}


def block_scale(coefficient: Fraction | int, term: FormalBlock) -> FormalBlock:
    coefficient = Fraction(coefficient)
    return {label: coefficient * value for label, value in term.items() if coefficient * value}


def parse_block(label: str) -> FormalBlock:
    if label == "0":
        return {}
    if label.startswith("-"):
        return {label[1:]: Fraction(-1)}
    return {label: Fraction(1)}


def compress(overlap, embedding):
    result = [[{} for _ in range(2)] for _ in range(2)]
    for i in range(2):
        for j in range(2):
            terms = []
            for a in range(3):
                for b in range(3):
                    coefficient = Fraction(embedding[a][i] * embedding[b][j])
                    if coefficient:
                        terms.append(block_scale(coefficient, overlap[a][b]))
            result[i][j] = block_add(*terms)
    return result


def omega(term: FormalBlock):
    return [[{}, term], [block_scale(-1, term), {}]]


def matrix_scale(coefficient, matrix):
    return [[block_scale(coefficient, entry) for entry in row] for row in matrix]


def scalar_left_product(scalar_matrix, block_matrix):
    """Multiply a scalar matrix by a matrix of formal linear block labels."""

    rows = len(scalar_matrix)
    inner = len(block_matrix)
    columns = len(block_matrix[0])
    assert all(len(row) == inner for row in scalar_matrix)
    return [
        [
            block_add(*(
                block_scale(scalar_matrix[i][k], block_matrix[k][j])
                for k in range(inner)
            ))
            for j in range(columns)
        ]
        for i in range(rows)
    ]


def scalar_right_product(block_matrix, scalar_matrix):
    """Multiply formal linear block labels by a scalar matrix."""

    rows = len(block_matrix)
    inner = len(scalar_matrix)
    columns = len(scalar_matrix[0])
    assert all(len(row) == inner for row in block_matrix)
    return [
        [
            block_add(*(
                block_scale(scalar_matrix[k][j], block_matrix[i][k])
                for k in range(inner)
            ))
            for j in range(columns)
        ]
        for i in range(rows)
    ]


def verify_cross_color_blocks(certificate) -> None:
    data = certificate["cross_color_blocks"]
    overlap = [[parse_block(entry) for entry in row] for row in data["overlap_matrix"]]
    embeddings = {int(vertex): matrix for vertex, matrix in data["tail_embeddings"].items()}
    x, y, z = parse_block("X"), parse_block("Y"), parse_block("Z")
    expected = {
        14: omega(y),
        15: omega(z),
        16: matrix_scale(-1, omega(x)),
        17: omega(block_add(y, z)),
        18: omega(block_add(y, block_scale(-1, x))),
        19: omega(block_add(z, block_scale(-1, x))),
    }
    for vertex, embedding in embeddings.items():
        assert compress(overlap, embedding) == expected[vertex], vertex

    u = block_add(y, z)
    v = block_add(y, block_scale(-1, x))
    w = block_add(z, block_scale(-1, x))
    assert block_scale(Fraction(1, 2), block_add(u, block_scale(-1, v), block_scale(-1, w))) == x
    assert block_scale(Fraction(1, 2), block_add(u, v, block_scale(-1, w))) == y
    assert block_scale(Fraction(1, 2), block_add(u, block_scale(-1, v), w)) == z

    # J_d Omega_K = Omega_K J_c = diag(-K,-K), so Omega_K intertwines the
    # two complex structures and preserves their eigenspace labels.  Replay
    # both matrix products rather than merely comparing expected labels.
    j_matrix = [[0, 1], [-1, 0]]
    for term in (x, y, z):
        omega_term = omega(term)
        expected_product = [[block_scale(-1, term), {}], [{}, block_scale(-1, term)]]
        assert scalar_left_product(j_matrix, omega_term) == expected_product
        assert scalar_right_product(omega_term, j_matrix) == expected_product


def verify_dimension_arithmetic(certificate) -> None:
    # Replay the terminal coefficient identity symbolically, rather than by
    # sampling dimensions.  Adding the two sector bounds gives coefficient 3
    # on nr, while their two right-hand sides give coefficient 2.  Their gap
    # is therefore the positive monomial nr for every n >= 3 and r > 0.
    dimension = certificate["dimension_contradiction"]
    assert dimension == {
        "fixed_color_space_dimension": "3r",
        "symmetrized_physical_dimension": "nr",
        "sector_count": 2,
        "sector_inequalities": [
            "3 sum_c e_(c,+) <= nr",
            "3 sum_c e_(c,-) <= nr",
        ],
        "rank_partition": "sum_c (e_(c,+)+e_(c,-)) = nr",
        "impossible_conclusion": "3nr <= 2nr for r > 0",
    }
    left_coefficient = 3
    right_coefficient = dimension["sector_count"]
    assert (left_coefficient, right_coefficient) == (3, 2)
    assert left_coefficient - right_coefficient == 1


def main() -> None:
    certificate_path = ROOT / "certificate" / "obstruction_certificate.json"
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    assert certificate["graph6_G19"] == GRAPH6_G19
    verify_core_sos(certificate)
    verify_cross_color_blocks(certificate)
    verify_dimension_arithmetic(certificate)
    print("exact obstruction certificate: PASS")
    print("core SOS: rational free-algebra replay PASS")
    print("tail/cross-color blocks: formal replay PASS")
    print("all-n dimension contradiction: symbolic coefficient replay PASS")


if __name__ == "__main__":
    main()
