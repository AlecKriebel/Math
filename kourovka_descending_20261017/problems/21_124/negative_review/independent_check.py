#!/usr/bin/env python3
"""Independent exact audit, with no imports from the author's checkers.

Cover characters are computed after contracting a spanning tree and solving
the rational cocycle equations. Affine quotient examples come from independent
4-by-4 unitriangular matrix products. All arithmetic is exact.
"""
from fractions import Fraction as F
from itertools import permutations, product
from math import gcd, lcm
from pathlib import Path
import argparse
import datetime
import hashlib
import json

LETTERS = "abct"


def inverse_perm(p):
    q = [None] * len(p)
    for i, x in enumerate(p):
        q[x] = i
    return tuple(q)


def relators(k):
    return [(4, 1, -4, -1),
            (4, 2, -4) + (-1,) * k + (-2,),
            (4, 3, -4, 2, 1, -2, -1, -3)]


def walk(word, v, moves):
    edges = {}
    for letter in word:
        g = abs(letter) - 1
        if letter > 0:
            edge = (v, g)
            v = moves[g][v]
            sign = 1
        else:
            v = inverse_perm(moves[g])[v]
            edge = (v, g)
            sign = -1
        edges[edge] = edges.get(edge, 0) + sign
    return v, edges


def nullspace(equations, width):
    rows = [[F(x) for x in row] for row in equations]
    pivots = []
    next_row = 0
    for column in range(width):
        found = next((j for j in range(next_row, len(rows))
                      if rows[j][column]), None)
        if found is None:
            continue
        rows[next_row], rows[found] = rows[found], rows[next_row]
        scale = rows[next_row][column]
        rows[next_row] = [x / scale for x in rows[next_row]]
        for j in range(len(rows)):
            if j != next_row and rows[j][column]:
                scale = rows[j][column]
                rows[j] = [x - scale * y for x, y in
                           zip(rows[j], rows[next_row])]
        pivots.append(column)
        next_row += 1
        if next_row == len(rows):
            break
    free = [j for j in range(width) if j not in pivots]
    out = []
    for column in free:
        vector = [F(0)] * width
        vector[column] = F(1)
        for j, pivot in enumerate(pivots):
            vector[pivot] = -rows[j][column]
        assert all(sum(x * y for x, y in zip(row, vector)) == 0
                   for row in equations)
        out.append(vector)
    return out, len(pivots)


def cover_characters(k, moves, include_witness=False):
    n = len(moves[0])
    seen = {0}
    todo = [0]
    tree = set()
    while todo:
        v = todo.pop(0)
        for g in range(4):
            for letter in (g + 1, -g - 1):
                w, edge = walk((letter,), v, moves)
                if w not in seen:
                    seen.add(w)
                    todo.append(w)
                    tree.add(next(iter(edge)))
    assert len(seen) == n, "Disconnected action is outside this test."
    assert len(tree) == n - 1
    variables = [(v, g) for v in range(n) for g in range(4)
                 if (v, g) not in tree]
    equations = []
    for v in range(n):
        for word in relators(k):
            end, edges = walk(word, v, moves)
            assert end == v, (k, n, v, word, end)
            equations.append([edges.get(e, 0) for e in variables])
    characters, rank = nullspace(equations, len(variables))
    visibility = []
    witness = None
    for v in range(n):
        e, w = 1, moves[0][v]
        while w != v:
            w = moves[0][w]
            e += 1
        end, chain = walk((1,) * e, v, moves)
        assert end == v
        for character in characters:
            value = sum(chain.get(edge, 0) * weight
                        for edge, weight in zip(variables, character))
            if value:
                visibility.append({"vertex": v, "a_power": e})
                if include_witness and witness is None:
                    factor = lcm(*(weight.denominator for weight in character))
                    weights = {edge: int(weight * factor)
                               for edge, weight in zip(variables, character)}
                    for base in range(n):
                        for word in relators(k):
                            _, chain2 = walk(word, base, moves)
                            assert sum(weights.get(edge, 0) * x
                                       for edge, x in chain2.items()) == 0
                    witness = {"weights_by_vertex_abct":
                               [[weights.get((base, g), 0) for g in range(4)]
                                for base in range(n)],
                               "vertex": v, "a_power": e,
                               "evaluation": int(value * factor)}
                break
    out = {"degree": n, "tree_edges": len(tree), "variables": len(variables),
           "relator_rank_Q": rank, "b1_Q": len(characters),
           "a_visible": visibility}
    if witness:
        out["explicit_integral_character"] = witness
    return out


def matrix_product(a, b, modulus=None):
    n = len(a)
    result = [[sum(a[i][h] * b[h][j] for h in range(n))
               for j in range(n)] for i in range(n)]
    return result if modulus is None else [[x % modulus for x in r] for r in result]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def unitriangular_inverse(a, p):
    n = len(a)
    nilpotent = [[(a[i][j] - int(i == j)) % p for j in range(n)] for i in range(n)]
    term, out = identity(n), identity(n)
    for exponent in range(1, n):
        term = matrix_product(term, nilpotent, p)
        out = [[(out[i][j] + (-1) ** exponent * term[i][j]) % p
                for j in range(n)] for i in range(n)]
    assert matrix_product(a, out, p) == identity(n)
    return out


def affine_cover(k, p):
    assert gcd(k, p) == 1
    matrices = [identity(4) for _ in range(4)]
    matrices[0][0][2] = pow(k, -1, p)
    matrices[1][1][2] = 1
    matrices[1][2][3] = 1
    matrices[2][1][3] = pow(k, -1, p)
    matrices[3][0][1] = 1
    for word in relators(k):
        total = identity(4)
        for letter in word:
            a = matrices[abs(letter) - 1]
            if letter < 0:
                a = unitriangular_inverse(a, p)
            total = matrix_product(total, a, p)
        assert total == identity(4)
    points = list(product(range(p), repeat=3))
    labels = {v: i for i, v in enumerate(points)}
    moves = []
    for matrix in matrices:
        backwards = unitriangular_inverse(matrix, p)
        perm = []
        for xyz in points:
            v = xyz + (1,)
            image = tuple(sum(backwards[i][j] * v[j] for j in range(4)) % p
                          for i in range(3))
            perm.append(labels[image])
        moves.append(tuple(perm))
    result = cover_characters(k, moves)
    assert not result["a_visible"]
    result.update(k=k, p=p, right_permutations=[list(x) for x in moves])
    return result


def scalar_product(a, b):
    return sum(x * y for x, y in zip(a, b))


def matvec(a, x):
    return [scalar_product(row, x) for row in a]


def transpose(a):
    return [list(x) for x in zip(*a)]


def convexity_checks():
    count = 0
    equality_count = 0
    for n in range(1, 5):
        for perm in permutations(range(n)):
            for signs in product((-1, 1), repeat=n):
                b = [[signs[i] * int(j == perm[i]) for j in range(n)] for i in range(n)]
                for t in ([int(i == j) for i in range(n)] for j in range(n)):
                    bt, bit = matvec(b, t), matvec(transpose(b), t)
                    for k in range(3, 9):
                        coefficients = [F(k - 2, k), F(1, k), F(1, k)]
                        vectors = [t, bt, bit]
                        s = [sum(coefficients[j] * vectors[j][i] for j in range(3))
                             for i in range(n)]
                        deficit = scalar_product(t, t) - scalar_product(s, s)
                        pair_sum = sum(coefficients[i] * coefficients[j] *
                                       sum((x - y) ** 2 for x, y in
                                           zip(vectors[i], vectors[j]))
                                       for i in range(3) for j in range(i + 1, 3))
                        assert deficit == pair_sum
                        assert deficit >= 0
                        assert (deficit == 0) == (bt == t)
                        equality_count += deficit == 0
                        count += 1
    return {"exact_signed_permutation_vector_parameter_cases": count,
            "equality_cases_exactly_B_fixed": equality_count}


def affine_multiply(x, y):
    shift = [a + b for a, b in zip(x[0], matvec(x[1], y[0]))]
    return shift, matrix_product(x[1], y[1])


def affine_inverse(x):
    linear_inverse = transpose(x[1])
    return ([-a for a in matvec(linear_inverse, x[0])], linear_inverse)


def boundary_affine_witnesses():
    definitions = [
        (1, [([-1, -1], identity(2)), ([0, 0], [[0, -1], [1, 0]]),
             ([0, 0], [[-1, 0], [0, -1]]), ([1, 0], identity(2))]),
        (2, [([-1], [[1]]), ([0], [[-1]]), ([0], [[-1]]), ([1], [[1]])])]
    out = []
    for k, images in definitions:
        n = len(images[0][0])
        neutral = ([0] * n, identity(n))
        evaluations = []
        for word in relators(k):
            total = neutral
            for letter in word:
                image = images[abs(letter) - 1]
                if letter < 0:
                    image = affine_inverse(image)
                total = affine_multiply(total, image)
            assert total == neutral
            evaluations.append(total)
        assert images[0] != neutral
        out.append({"k": k, "dimension": n, "generator_images_abct": images,
                    "all_relators_identity": True})
    return out


def explicit_cellular_witness(k, n, cshift, a_weights, t_weights):
    moves = [tuple(range(n)), tuple((i + 1) % n for i in range(n)),
             tuple((i + cshift) % n for i in range(n)), tuple(range(n))]
    weights = {(v, g): [a_weights[v], 0, 0, t_weights[v]][g]
               for v in range(n) for g in range(4)}
    evaluations = []
    for v in range(n):
        for word in relators(k):
            end, chain = walk(word, v, moves)
            assert end == v
            value = sum(weights[edge] * count for edge, count in chain.items())
            assert value == 0
            evaluations.append(value)
    _, a_loop = walk((1,), 0, moves)
    value = sum(weights[e] * x for e, x in a_loop.items())
    assert value == 1
    return {"k": k, "relator_evaluations": evaluations,
            "specified_a_loop_evaluation": value,
            "tree_contracted_homology": cover_characters(k, moves)}


def cyclic_quotient_checks():
    counts = []
    for k in range(3, 9):
        checked = 0
        rotating_a = 0
        for n in range(1, 6):
            for a, b, c, t in product(range(n), repeat=4):
                if (k * a) % n or gcd(n, gcd(a, gcd(b, gcd(c, t)))) != 1:
                    continue
                moves = [tuple((i + shift) % n for i in range(n))
                         for shift in (a, b, c, t)]
                answer = cover_characters(k, moves)
                assert not answer["a_visible"], (k, n, a, b, c, t, answer)
                checked += 1
                rotating_a += a != 0
        counts.append({"k": k, "connected_cyclic_quotient_characters_checked": checked,
                       "nontrivial_a_linear_action": rotating_a})
    return counts


def normal_core_boundary_cover():
    """The regular D8 cover independently tests a^2 in the normal core."""
    generators = [(0, 1, 3, 2), (1, 0, 2, 3), (2, 3, 0, 1), (0, 1, 2, 3)]
    multiply = lambda x, y: tuple(x[y[i]] for i in range(4))
    neutral = tuple(range(4))
    elements, seen = [neutral], {neutral}
    cursor = 0
    while cursor < len(elements):
        x = elements[cursor]
        cursor += 1
        for g in generators:
            new = multiply(x, g)
            if new not in seen:
                seen.add(new)
                elements.append(new)
    assert len(elements) == 8
    labels = {x: i for i, x in enumerate(elements)}
    moves = [tuple(labels[multiply(x, g)] for x in elements) for g in generators]
    result = cover_characters(4, moves, True)
    assert any(x == {"vertex": 0, "a_power": 2} for x in result["a_visible"])
    result["regular_quotient_order"] = 8
    result["right_permutations_abct"] = [list(x) for x in moves]
    result["scope"] = "Normal core does not contain a, but contains a^2 with nonzero rational homology."
    return result


def input_hashes():
    base = Path(__file__).resolve().parent.parent
    names = ["negative_geometric/FINITE_HOLONOMY_FILTER.md",
             "negative_geometric/check_covers.py", "negative_geometric/cover_results.json",
             "negative_geometric/search_small_covers.py", "negative_geometric/small_cover_search.json",
             "priority/SOURCE_CONTRACT.md", "priority/sources/delage2602.08759v3.html",
             "priority/sources/wu_ye2504.14192v2.html"]
    return {name: {"sha256": hashlib.sha256((base / name).read_bytes()).hexdigest(),
                   "bytes": (base / name).stat().st_size} for name in names}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("independent_results.json"))
    args = parser.parse_args()
    frozen = input_hashes()
    nonnormal_moves = [(0, 1, 3, 2), (1, 0, 2, 3), (2, 3, 0, 1), (0, 1, 2, 3)]
    nonnormal = cover_characters(4, nonnormal_moves, True)
    assert nonnormal["a_visible"] == [{"vertex": 0, "a_power": 1},
                                      {"vertex": 1, "a_power": 1}]
    assert nonnormal["relator_rank_Q"] == 6
    results = {
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "method": "Independent standard-library exact computations; spanning-tree contraction and rational cocycle nullspace, plus 4x4 unitriangular matrix checks",
        "inputs": frozen,
        "convexity_identity": convexity_checks(),
        "affine_boundary_counterexamples": boundary_affine_witnesses(),
        "author_boundary_cocycles": [
            explicit_cellular_witness(1, 4, 2, [1, 0, -1, 0], [0, 0, 1, 1]),
            explicit_cellular_witness(2, 2, 1, [1, -1], [0, 2])],
        "unitriangular_affine_covers": [affine_cover(k, p) for k, p in
                                        [(3, 2), (4, 3), (5, 2), (5, 3)]],
        "abelian_cyclic_quotient_tests": cyclic_quotient_checks(),
        "nonnormal_boundary_counterexample": nonnormal,
        "normal_core_boundary_counterexample": normal_core_boundary_cover(),
        "bounded_computations_are_not_general_proofs": True,
        "result": "PASS exact bounded checks; theoretical scope audited separately in AUDIT.md"}
    assert input_hashes() == frozen, "Input changed during independent run."
    args.output.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"result": results["result"], "output": str(args.output),
                      "cyclic_quotient_cases": sum(x["connected_cyclic_quotient_characters_checked"]
                                                   for x in results["abelian_cyclic_quotient_tests"]),
                      "convexity_cases": results["convexity_identity"]}, indent=2))


if __name__ == "__main__":
    main()
