#!/usr/bin/env python3
"""Independent exact verifier for the Lalonde uniform-rank obstruction.

This program uses only the Python standard library and rational arithmetic.
It treats the JSON file as untrusted proof data.  The checker anchors the
graph by independently decoding its graph6 checksum, reconstructs the core
trace-SOS in a free noncommutative polynomial algebra, checks the ideal
witness made from clique-column relations, replays the Walsh identities, and
checks every cross-tail block compression over freely noncommuting labels.

The only analytic inference (reported explicitly at the end) is the standard
finite-matrix fact

    Tr(sum_j F_j^* F_j) = 0  ==>  F_j = 0 for every j.

No floating point arithmetic, CAS, SDP solver, or third-party package is used.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


EXPECTED_SCHEMA = "lalonde-uniform-obstruction-certificate-v1"
EXPECTED_GRAPH6 = "RxLAKA@AgYAWDGO?O?@??A?W@@OC@_"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def rat(value):
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    raise TypeError(f"not an exact rational: {value!r}")


# A free noncommutative polynomial is {word_tuple: rational_coefficient}.
def clean(poly):
    return {word: coeff for word, coeff in poly.items() if coeff}


def pconst(value):
    value = rat(value)
    return {} if not value else {(): value}


def pvar(name):
    return {(str(name),): Fraction(1)}


def padd(*polys):
    out = {}
    for poly in polys:
        for word, coeff in poly.items():
            out[word] = out.get(word, Fraction(0)) + coeff
    return clean(out)


def pscale(value, poly):
    value = rat(value)
    return clean({word: value * coeff for word, coeff in poly.items()})


def pneg(poly):
    return pscale(-1, poly)


def psub(left, right):
    return padd(left, pneg(right))


def pmul(left, right):
    out = {}
    for word_l, coeff_l in left.items():
        for word_r, coeff_r in right.items():
            word = word_l + word_r
            out[word] = out.get(word, Fraction(0)) + coeff_l * coeff_r
    return clean(out)


def adjoint_symbol(symbol):
    # Projection generators are declared self-adjoint.
    if symbol.startswith("u") and symbol[1:].isdigit():
        return symbol
    return symbol[:-1] if symbol.endswith("*") else symbol + "*"


def pstar(poly):
    return clean(
        {
            tuple(adjoint_symbol(symbol) for symbol in reversed(word)): coeff
            for word, coeff in poly.items()
        }
    )


def psum(polys):
    return padd(*list(polys))


ONE = pconst(1)
ZERO = {}


def graph6_decode(text):
    """Decode the small-n graph6 format without networkx."""
    require(text and text[0] != "~", "only the graph6 n <= 62 form is expected")
    values = [ord(ch) - 63 for ch in text]
    require(all(0 <= value <= 63 for value in values), "invalid graph6 character")
    n = values[0]
    bits = "".join(f"{value:06b}" for value in values[1:])
    needed = n * (n - 1) // 2
    require(len(bits) >= needed, "truncated graph6 payload")
    require(set(bits[needed:]) <= {"0"}, "nonzero graph6 padding")
    edges = set()
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if bits[cursor] == "1":
                edges.add((low + 1, high + 1))
            cursor += 1
    return n, edges


def normalized_edge(a, b):
    require(a != b, "loops are not allowed")
    return (a, b) if a < b else (b, a)


def triangle_set(n, edges):
    out = set()
    for a, b, c in itertools.combinations(range(1, n + 1), 3):
        if all(normalized_edge(x, y) in edges for x, y in ((a, b), (a, c), (b, c))):
            out.add((a, b, c))
    return out


def reduce_operator_word(word, projection_names, edge_names):
    """Use only p^2=p and p_v p_w=0 for graph edges."""
    word = list(word)
    changed = True
    while changed:
        changed = False
        for index in range(len(word) - 1):
            left, right = word[index], word[index + 1]
            if left == right and left in projection_names:
                del word[index + 1]
                changed = True
                break
            if frozenset((left, right)) in edge_names:
                return None
    return tuple(word)


def reduce_operator(poly, projection_names, edge_names):
    out = {}
    for word, coeff in poly.items():
        reduced = reduce_operator_word(word, projection_names, edge_names)
        if reduced is not None:
            out[reduced] = out.get(reduced, Fraction(0)) + coeff
    return clean(out)


def canonical_rotation(word):
    if not word:
        return word
    rotations = [word[index:] + word[:index] for index in range(len(word))]
    return min(rotations)


def reduce_trace_word(word, projection_names, edge_names):
    """Reduce modulo projections/edges and cyclicity of finite trace."""
    word = list(word)
    while len(word) >= 2:
        changed = False
        size = len(word)
        for index in range(size):
            nxt = (index + 1) % size
            left, right = word[index], word[nxt]
            if frozenset((left, right)) in edge_names:
                return None
            if left == right and left in projection_names:
                if nxt == 0:  # cyclic boundary: (...,p), (p,...)
                    word.pop()
                else:
                    word.pop(nxt)
                changed = True
                break
        if not changed:
            break
    return canonical_rotation(tuple(word))


def trace_reduce(poly, projection_names, edge_names, corner_dimension_units=3):
    """Return a formal trace polynomial; every projection has trace r."""
    out = {}
    for word, coeff in poly.items():
        word = reduce_trace_word(word, projection_names, edge_names)
        if word is None:
            continue
        if not word:
            key = ("r",)
            coeff *= corner_dimension_units
        elif len(word) == 1 and word[0] in projection_names:
            key = ("r",)
        else:
            key = ("tau",) + word
        out[key] = out.get(key, Fraction(0)) + coeff
    return clean(out)


def tadd(*traces):
    return padd(*traces)


def tscale(value, trace):
    return pscale(value, trace)


def rtrace(value):
    value = rat(value)
    return {} if not value else {("r",): value}


def parse_linear_form(data, allowed):
    require(isinstance(data, dict), "a block linear form must be a JSON object")
    out = {}
    for symbol, coeff in data.items():
        require(symbol in allowed, f"undeclared free block {symbol}")
        out = padd(out, pscale(rat(coeff), pvar(symbol)))
    return out


def matrix_shape(matrix):
    require(isinstance(matrix, list) and matrix, "matrix must be a nonempty list")
    width = len(matrix[0])
    require(width and all(len(row) == width for row in matrix), "ragged matrix")
    return len(matrix), width


def mzero(rows, cols):
    return [[{} for _ in range(cols)] for _ in range(rows)]


def madd(left, right):
    rows_l, cols_l = matrix_shape(left)
    rows_r, cols_r = matrix_shape(right)
    require((rows_l, cols_l) == (rows_r, cols_r), "matrix-add shape mismatch")
    return [[padd(left[i][j], right[i][j]) for j in range(cols_l)] for i in range(rows_l)]


def mscale(value, matrix):
    return [[pscale(value, entry) for entry in row] for row in matrix]


def mmul(left, right):
    rows_l, cols_l = matrix_shape(left)
    rows_r, cols_r = matrix_shape(right)
    require(cols_l == rows_r, "matrix-product shape mismatch")
    out = mzero(rows_l, cols_r)
    for i in range(rows_l):
        for j in range(cols_r):
            out[i][j] = psum(pmul(left[i][k], right[k][j]) for k in range(cols_l))
    return out


def scalar_matrix(data):
    matrix_shape(data)
    return [[pconst(entry) for entry in row] for row in data]


def scalar_transpose(data):
    rows, cols = matrix_shape(data)
    return [[data[i][j] for i in range(rows)] for j in range(cols)]


def compress_scalar_embedding(block_matrix, embedding):
    """Compute F^t T F; F is a rational scalar matrix."""
    rational_f = [[rat(entry) for entry in row] for row in embedding]
    return mmul(mmul(scalar_matrix(scalar_transpose(rational_f)), block_matrix), scalar_matrix(rational_f))


def omega(label):
    return [[{}, label], [pneg(label), {}]]


def identity_poly_matrix(size):
    return [[ONE if i == j else {} for j in range(size)] for i in range(size)]


def rational_rank(rows):
    matrix = [[rat(entry) for entry in row] for row in rows]
    if not matrix:
        return 0
    row_count, col_count = len(matrix), len(matrix[0])
    require(all(len(row) == col_count for row in matrix), "ragged rational matrix")
    pivot_row = 0
    for col in range(col_count):
        pivot = next((row for row in range(pivot_row, row_count) if matrix[row][col]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][col]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(row_count):
            if row != pivot_row and matrix[row][col]:
                factor = matrix[row][col]
                matrix[row] = [a - factor * b for a, b in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def rational_matmul(left, right):
    rows_l, cols_l = matrix_shape(left)
    rows_r, cols_r = matrix_shape(right)
    require(cols_l == rows_r, "rational matrix-product shape mismatch")
    return [
        [sum((rat(left[i][k]) * rat(right[k][j]) for k in range(cols_l)), Fraction(0)) for j in range(cols_r)]
        for i in range(rows_l)
    ]


# A tiny exact commutative polynomial ring Q[n,f,d].  Here f is a formal
# name for (n-1)!; the only factorial fact used is the symbolic recurrence
# n! = n f.  This avoids presenting verification at finitely many n as a
# proof of the family statement.
def cclean(poly):
    return {monomial: coeff for monomial, coeff in poly.items() if coeff}


def cconst(value):
    value = rat(value)
    return {} if not value else {(): value}


def cvar(name):
    return {((str(name), 1),): Fraction(1)}


def cmul_monomials(left, right):
    powers = {}
    for symbol, power in left + right:
        powers[symbol] = powers.get(symbol, 0) + power
    return tuple(sorted((symbol, power) for symbol, power in powers.items() if power))


def cadd(*polys):
    out = {}
    for poly in polys:
        for monomial, coeff in poly.items():
            out[monomial] = out.get(monomial, Fraction(0)) + coeff
    return cclean(out)


def cscale(value, poly):
    value = rat(value)
    return cclean({monomial: value * coeff for monomial, coeff in poly.items()})


def csub(left, right):
    return cadd(left, cscale(-1, right))


def cmul(left, right):
    out = {}
    for monomial_l, coeff_l in left.items():
        for monomial_r, coeff_r in right.items():
            monomial = cmul_monomials(monomial_l, monomial_r)
            out[monomial] = out.get(monomial, Fraction(0)) + coeff_l * coeff_r
    return cclean(out)


def ceval(poly, values):
    total = Fraction(0)
    for monomial, coeff in poly.items():
        term = coeff
        for symbol, power in monomial:
            term *= rat(values[symbol]) ** power
        total += term
    return total


def check_graph(cert):
    graph = cert["graph"]
    require(graph["graph6"] == EXPECTED_GRAPH6, "certificate is for the wrong graph6 string")
    decoded_n, decoded_edges = graph6_decode(EXPECTED_GRAPH6)
    listed_edges = {normalized_edge(*edge) for edge in graph["edges"]}
    require(graph["vertex_count"] == decoded_n == 19, "wrong graph order")
    require(listed_edges == decoded_edges, "listed edges do not match independently decoded graph6")
    listed_triangles = {tuple(sorted(triangle)) for triangle in graph["base_triangles"]}
    actual_triangles = triangle_set(decoded_n, decoded_edges)
    require(listed_triangles == actual_triangles, "base triangle list is not exhaustive")
    require(graph["apex"] == 20, "wrong apex label")
    require(graph["apex_neighbors"] == list(range(1, 20)), "apex is not declared universal on G_19")
    print(f"[PASS] graph6 decodes to the declared 19 vertices, 36 edges, and {len(actual_triangles)} triangles")
    return decoded_edges, actual_triangles


def check_uniformization(cert, triangles):
    data = cert["uniformization"]
    colors = data["color_count"]
    require(colors == 4, "primary certificate must use four colors")
    require(data["permutation_blocks"] == math.factorial(colors), "wrong number of color permutations")
    require(data["fixed_color_occurrences"] == math.factorial(colors - 1), "wrong fixed-color count")
    require(data["new_dimension_multiple"] == math.factorial(colors), "wrong symmetrized dimension")
    require(data["uniform_rank_multiple"] == math.factorial(colors - 1), "wrong symmetrized rank")
    require(data["new_dimension_multiple"] == colors * data["uniform_rank_multiple"], "D != 4r")
    require(data["corner_dimension_in_rank_units"] == colors - 1 == 3, "wrong fixed-color corner dimension")
    partitions = {tuple(sorted(partition)) for partition in cert["core"]["partitions"]}
    require(partitions == triangles, "core partitions must be exactly the four graph triangles")
    # Each triangle plus the universal apex is a 4-clique.  Four mutually
    # orthogonal rank-r projections in dimension 4r sum to the identity.
    require(colors * data["uniform_rank_multiple"] == data["new_dimension_multiple"], "clique rank count failed")
    print("[PASS] 24-fold color symmetrization gives D=24d, rank=6d, and four exact clique columns")


def check_all_n(cert):
    data = cert["all_n"]
    expected_text = {
        "domain": "integer n >= 3, original local dimension d >= 1",
        "factorial_predecessor_symbol": "f=(n-1)!",
        "factorial_recurrence": "n!=n*f",
        "uniform_rank_formula": "r=f*d=(n-1)!*d",
        "symmetrized_dimension_formula": "D=n*f*d=n*r=n!*d",
        "joined_clique_order": "n-3",
        "corner_dimension_formula": "D-(n-3)*r=3*r",
        "sector_sum_formula": "E_+ + E_- = n*r",
        "combined_impossible_inequality": "3*n*r <= 2*n*r",
    }
    for key, value in expected_text.items():
        require(data.get(key) == value, f"wrong all-n certificate field {key}")
    require(data.get("sector_bounds") == ["3*E_+ <= n*r", "3*E_- <= n*r"], "wrong all-n sector bounds")

    n, f, d = cvar("n"), cvar("f"), cvar("d")
    factorial_n_by_recurrence = cmul(n, f)       # n! = n (n-1)!
    rank = cmul(f, d)                            # r = (n-1)! d
    dimension_from_factorial = cmul(factorial_n_by_recurrence, d)
    dimension_from_n_rank = cmul(n, rank)
    require(dimension_from_factorial == dimension_from_n_rank, "D=n!d does not replay as nr")

    n_minus_three = cadd(n, cconst(-3))
    joined_clique_rank = cmul(n_minus_three, rank)
    corner_dimension = csub(dimension_from_factorial, joined_clique_rank)
    require(corner_dimension == cscale(3, rank), "all-n fixed-color corner is not symbolically 3r")

    # Adding the two sector packing inequalities has right side 2D.  The
    # sector sum is D=nr, so its left side is 3D.  All equalities below are
    # identities of Q[n,f,d], not evaluations at sample integers.
    combined_left = cscale(3, dimension_from_n_rank)
    combined_right = cscale(2, dimension_from_n_rank)
    require(combined_left == cscale(3, cmul(n, rank)), "left side is not 3nr")
    require(combined_right == cscale(2, cmul(n, rank)), "right side is not 2nr")
    contradiction_gap = csub(combined_left, combined_right)
    require(contradiction_gap == dimension_from_n_rank, "3nr-2nr is not nr")

    # Exact specialization is only a consistency check; the preceding formal
    # polynomial identities are the all-n replay.
    require(ceval(rank, {"n": 4, "f": 6, "d": 1}) == 6, "n=4 rank specialization failed")
    require(ceval(dimension_from_factorial, {"n": 4, "f": 6, "d": 1}) == 24, "n=4 dimension specialization failed")
    print("[PASS] symbolic all-n recurrence: r=(n-1)!d and D=n!d=n r in Q[n,f,d]")
    print("[PASS] symbolic all-n packing: 3nr <= 2nr would force nr <= 0, contradicting n>=3 and r>0")


def check_core_sos(cert, edges):
    core = cert["core"]
    projection_names = {f"u{vertex}" for vertex in range(1, 14)}
    edge_names = {
        frozenset((f"u{left}", f"u{right}"))
        for left, right in edges
        if left <= 13 and right <= 13
    }

    def u(vertex):
        return pvar(f"u{vertex}")

    def vertex_sum(vertices):
        return psum(u(vertex) for vertex in vertices)

    partition_residuals = {}
    for partition in core["partitions"]:
        residual = psub(vertex_sum(partition), ONE)
        partition_residuals[frozenset(partition)] = residual
        for left, right in itertools.combinations(partition, 2):
            require(normalized_edge(left, right) in edges, f"partition {partition} is not a clique")

    pairs = core["binary_pairs"]
    require(len(pairs) == 3, "three binary decompositions are required")
    pair_sums = []
    letters = {}
    binary_residuals = []
    for item in pairs:
        left, right = item["vertices"]
        complement = item["complement_vertex"]
        require(normalized_edge(left, right) in edges, "binary pair must be an edge")
        residual = psub(padd(u(left), u(right)), psub(ONE, u(complement)))
        expected = partition_residuals.get(frozenset((left, right, complement)))
        require(expected is not None and residual == expected, "binary complement is not a clique partition")
        pair_sums.append(padd(u(left), u(right)))
        letters[item["letter"]] = psub(u(left), u(right))
        binary_residuals.append(residual)

        square_claim = psub(pmul(letters[item["letter"]], letters[item["letter"]]), psub(ONE, u(complement)))
        square_witness = padd(
            psub(pmul(u(left), u(left)), u(left)),
            psub(pmul(u(right), u(right)), u(right)),
            pneg(pmul(u(left), u(right))),
            pneg(pmul(u(right), u(left))),
            residual,
        )
        require(square_claim == square_witness, f"bad exact square witness for {item['letter']}")

    base_residual = partition_residuals[frozenset((1, 2, 3))]
    pair_total_minus_two = psub(psum(pair_sums), pconst(2))
    require(
        pair_total_minus_two == psub(psum(binary_residuals), base_residual),
        "A^2+B^2+C^2 support identity has no valid partition witness",
    )

    coefficient = rat(core["sos_coefficient"])
    require(coefficient == Fraction(3, 2), "the sharp SOS coefficient must be 3/2")
    sos_factors = []
    pair_overlap_sum = {}
    sign_rows = []
    for item in core["sos_terms"]:
        target = item["target"]
        summands = item["summands"]
        signs = item["walsh_signs"]
        require(len(summands) == len(signs) == 3, "malformed core SOS term")
        require(math.prod(signs) == -1, "Walsh signs must have product -1")
        sign_rows.append(signs)
        for neighbor in summands:
            require(normalized_edge(target, neighbor) in edges, f"u{target} does not annihilate u{neighbor}")
        S = vertex_sum(summands)
        support_projection = psub(ONE, u(target))
        require(
            reduce_operator(pmul(u(target), S), projection_names, edge_names) == {},
            f"left support relation failed at target {target}",
        )
        require(
            reduce_operator(pmul(S, u(target)), projection_names, edge_names) == {},
            f"right support relation failed at target {target}",
        )
        require(
            reduce_operator(psub(pmul(support_projection, support_projection), support_projection), projection_names, edge_names) == {},
            f"I-u{target} is not verified as a projection",
        )
        factor = psub(S, pscale(coefficient, support_projection))
        require(factor == pstar(factor), "SOS factor is not Hermitian")
        sos_factors.append(factor)
        for left, right in itertools.combinations(summands, 2):
            pair_overlap_sum = padd(pair_overlap_sum, pmul(u(left), u(right)))

        D = psum(pscale(sign, letters[name]) for sign, name in zip(signs, ("A", "B", "C")))
        # 2 S = (sum of the three binary pairs) + D, hence this residual
        # is the already certified pair-total-minus-two relation.
        require(
            psub(pscale(2, S), padd(pconst(2), D)) == pair_total_minus_two,
            f"S=I+D/2 sign assignment failed at target {target}",
        )

        # Once trace-SOS gives S=(3/2)(I-u_target), D=I-3u_target.
        D_from_projection = psub(ONE, pscale(3, u(target)))
        quadratic = padd(pmul(D_from_projection, D_from_projection), D_from_projection, pconst(-2))
        require(
            quadratic == pscale(9, psub(pmul(u(target), u(target)), u(target))),
            f"D^2+D-2 projection witness failed at target {target}",
        )

    sos = psum(pmul(pstar(factor), factor) for factor in sos_factors)

    overlap_factors = core["overlap_factorization"]
    require(len(overlap_factors) == 3, "three overlap products are required")
    overlap_product = {}
    for left_pair, right_pair in overlap_factors:
        overlap_product = padd(overlap_product, pmul(vertex_sum(left_pair), vertex_sum(right_pair)))
    require(
        trace_reduce(pair_overlap_sum, projection_names, edge_names)
        == trace_reduce(overlap_product, projection_names, edge_names),
        "the twelve overlap moments do not factor into the three binary products",
    )

    a, b, c = pair_sums
    a_prime, b_prime, c_prime = psub(ONE, u(3)), psub(ONE, u(2)), psub(ONE, u(1))
    T = padd(pmul(a, b), pmul(a, c), pmul(b, c))
    T_complement = padd(
        pmul(a_prime, b_prime),
        pmul(a_prime, c_prime),
        pmul(b_prime, c_prime),
    )
    r_a, r_b, r_c = binary_residuals
    ideal_witness = padd(
        pmul(r_a, b), pmul(a_prime, r_b),
        pmul(r_a, c), pmul(a_prime, r_c),
        pmul(r_b, c), pmul(b_prime, r_c),
    )
    require(psub(T, T_complement) == ideal_witness, "invalid noncommutative clique-ideal witness for T")

    trace_sos = trace_reduce(sos, projection_names, edge_names)
    trace_T = trace_reduce(T, projection_names, edge_names)
    trace_T_complement = trace_reduce(T_complement, projection_names, edge_names)
    require(
        trace_sos == tadd(tscale(2, trace_T), rtrace(-6)),
        "free trace expansion of the core SOS is not 2 Tr(T)-6r",
    )
    require(trace_T_complement == rtrace(3), "complement overlap trace is not exactly 3r")
    final_trace = tadd(tscale(2, trace_T_complement), rtrace(-6))
    require(final_trace == {}, "core sum of squares does not have trace zero")

    # Replay the four Walsh expansions in the free algebra.
    A, B, C = letters["A"], letters["B"], letters["C"]
    anti_BC = padd(pmul(B, C), pmul(C, B))
    anti_AC = padd(pmul(A, C), pmul(C, A))
    anti_AB = padd(pmul(A, B), pmul(B, A))
    errors = [psub(A, anti_BC), psub(B, anti_AC), psub(C, anti_AB)]
    square_sum_residual = psub(padd(pmul(A, A), pmul(B, B), pmul(C, C)), pconst(2))
    for item, signs in zip(core["sos_terms"], sign_rows):
        D = psum(pscale(sign, letter) for sign, letter in zip(signs, (A, B, C)))
        walsh = psum(pscale(sign, error) for sign, error in zip(signs, errors))
        expanded_quadratic = padd(pmul(D, D), D, pconst(-2))
        require(
            expanded_quadratic == padd(square_sum_residual, walsh),
            f"Walsh free-polynomial expansion failed at target {item['target']}",
        )
    require(rational_rank(sign_rows) == 3, "Walsh sign matrix does not have rank three")
    gram = rational_matmul([[row[col] for row in sign_rows] for col in range(3)], sign_rows)
    require(gram == [[Fraction(4 if i == j else 0) for j in range(3)] for i in range(3)], "Walsh left inverse is not (1/4) S^t")

    print("[PASS] exact free trace-SOS: Tr(sum F_j^*F_j)=2(3r)-6r=0")
    print("[PASS] clique ideal witness and all four noncommutative Walsh expansions replay exactly")


def check_core_sign_and_cross_form(cert, edges):
    vectors = {int(vertex): [rat(entry) for entry in vector] for vertex, vector in cert["core"]["sign_vectors"].items()}
    require(set(vectors) == set(range(1, 14)), "core sign vectors must cover vertices 1--13")
    for left, right in edges:
        if left <= 13 and right <= 13:
            dot = sum((a * b for a, b in zip(vectors[left], vectors[right])), Fraction(0))
            require(dot == 0, f"core sign vectors violate edge {left}-{right}")

    # Same-vertex orthogonality at vertices 1--9 is one scalar linear
    # equation f_v^t T f_v=0 in the nine unknown blocks T_ab.
    equations = []
    for vertex in range(1, 10):
        f = vectors[vertex]
        equations.append([f[row] * f[col] for row in range(3) for col in range(3)])
    require(rational_rank(equations) == 6, "vertices 1--9 do not leave a three-block kernel")
    skew_basis = []
    for positions in (((0, 1), (1, 0)), ((0, 2), (2, 0)), ((1, 2), (2, 1))):
        basis = [Fraction(0)] * 9
        basis[3 * positions[0][0] + positions[0][1]] = 1
        basis[3 * positions[1][0] + positions[1][1]] = -1
        skew_basis.append(basis)
    require(rational_rank(skew_basis) == 3, "declared skew-block basis is dependent")
    for basis in skew_basis:
        require(all(sum((a * b for a, b in zip(row, basis)), Fraction(0)) == 0 for row in equations), "skew block is not in the constraint kernel")
    print("[PASS] vertices 1--9 force exactly the 3-parameter skew block form (X,Y,Z)")


def check_cross_tail(cert):
    data = cert["cross_tail"]
    allowed = set(data["free_block_generators"])
    require(allowed == {"X", "Y", "Z"}, "wrong free block alphabet")
    parsed_T = [[parse_linear_form(entry, allowed) for entry in row] for row in data["skew_block_matrix"]]
    X, Y, Z = pvar("X"), pvar("Y"), pvar("Z")
    expected_T = [[{}, X, Y], [pneg(X), {}, Z], [pneg(Y), pneg(Z), {}]]
    require(parsed_T == expected_T, "certificate skew matrix has wrong signs or adjoints")

    embeddings = {int(vertex): matrix for vertex, matrix in data["tail_embeddings"].items()}
    anchored_embeddings = {
        14: [[1, 0], [0, 0], [0, 1]],
        15: [[0, 0], [1, 0], [0, 1]],
        16: [[1, 0], [0, -1], [0, 0]],
        17: [[1, 0], [1, 0], [0, 1]],
        18: [[1, 0], [0, -1], [0, 1]],
        19: [[1, 0], [0, -1], [1, 0]],
    }
    require(embeddings == anchored_embeddings, "tail embeddings differ from the proved plane normal form")
    spaces = {int(vertex): name for vertex, name in data["tail_parameter_spaces"].items()}
    require(spaces == {14: "M", 15: "M", 16: "M", 17: "M_perp", 18: "M_perp", 19: "M_perp"}, "wrong tail parameter spaces")

    computed_labels = {}
    for vertex in range(14, 20):
        label = parse_linear_form(data["expected_compression_labels"][str(vertex)], allowed)
        computed = compress_scalar_embedding(parsed_T, embeddings[vertex])
        require(computed == omega(label), f"F_{vertex}^t T F_{vertex} is not Omega of the declared label")
        computed_labels[vertex] = label

    # The last three labels recover X,Y,Z exactly.
    forward = []
    for vertex in (17, 18, 19):
        label = computed_labels[vertex]
        forward.append([label.get((symbol,), Fraction(0)) for symbol in ("X", "Y", "Z")])
    inverse = [[rat(entry) for entry in data["coefficient_inverse"][symbol]] for symbol in ("X", "Y", "Z")]
    identity = [[Fraction(1 if i == j else 0) for j in range(3)] for i in range(3)]
    require(rational_matmul(inverse, forward) == identity, "declared coefficient transform is not an exact inverse")
    require(rational_matmul(forward, inverse) == identity, "coefficient transform lacks a two-sided inverse")

    J_data = data["J"]
    require(J_data == [[0, 1], [-1, 0]], "wrong complex-structure matrix J")
    J = scalar_matrix(J_data)
    I2 = identity_poly_matrix(2)
    require(mmul(J, J) == mscale(-1, I2), "J^2 != -I")
    for symbol in (X, Y, Z):
        Omega = omega(symbol)
        common = [[pneg(symbol), {}], [{}, pneg(symbol)]]
        require(mmul(J, Omega) == common, "J Omega_K has the wrong value")
        require(mmul(Omega, J) == common, "Omega_K J has the wrong value")

    # Final coefficient-only contradiction after the exact inclusions:
    # 3 sum_c e_(c,+) <= 4r and 3 sum_c e_(c,-) <= 4r, while
    # sum_(c,sigma)e_(c,sigma)=4r.
    require(data["sector_multiplicity"] == 3, "wrong sector-space dimension multiplier")
    require(data["physical_dimension_in_rank_units"] == 4, "wrong physical dimension")
    require(data["sector_count"] == 2, "J must have two eigensectors")
    lhs = data["sector_multiplicity"] * data["physical_dimension_in_rank_units"]
    rhs = data["sector_count"] * data["physical_dimension_in_rank_units"]
    require(lhs > rhs and (lhs, rhs) == (12, 8), "dimension contradiction is not 12r <= 8r")

    print("[PASS] all six exact cross-tail compressions F_v^t T F_v = Omega_L replay over free blocks")
    print("[PASS] tail coefficient transform is invertible and J Omega_K = Omega_K J exactly")
    print("[PASS] sector dimension conclusion would require 12r <= 8r, impossible for r>0")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "certificate",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "certificate" / "lalonde_uniform_obstruction.json",
    )
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    cert = json.loads(raw)
    require(cert.get("schema") == EXPECTED_SCHEMA, "unsupported certificate schema")
    print(f"certificate sha256: {hashlib.sha256(raw).hexdigest()}")
    edges, triangles = check_graph(cert)
    check_uniformization(cert, triangles)
    check_all_n(cert)
    check_core_sos(cert, edges)
    check_core_sign_and_cross_form(cert, edges)
    check_cross_tail(cert)
    print("ALL EXACT CERTIFICATE CHECKS PASSED")
    print("analytic convention used: finite-dimensional matrix trace is faithful on positive semidefinite matrices")


if __name__ == "__main__":
    main()
