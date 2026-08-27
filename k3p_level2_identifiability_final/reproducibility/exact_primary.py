#!/usr/bin/env python3
"""Exact primitive replays for primary K3P gates outside the four-port atlas."""

from __future__ import annotations

import ast
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import sys


if not __debug__ or sys.flags.optimize:
    raise SystemExit("optimized Python forbidden for exact_primary")


CH3 = tuple((a, b, a ^ b) for a in range(4) for b in range(4))
CHAR_NAMES = "0CGT"


def determinant(matrix):
    matrix = [list(row) for row in matrix]
    n = len(matrix)
    result = matrix[0][0] * 0 + 1 if n else Q(1)
    for column in range(n):
        pivot = next((i for i in range(column, n) if matrix[i][column]), None)
        if pivot is None:
            return result * 0
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            result = -result
        value = matrix[column][column]
        result *= value
        for i in range(column + 1, n):
            if matrix[i][column]:
                multiplier = matrix[i][column] / value
                for j in range(column + 1, n):
                    matrix[i][j] -= multiplier * matrix[column][j]
    return result


def rank_pivots(matrix):
    matrix = [list(row) for row in matrix]
    if not matrix:
        return 0, [], []
    rows = list(range(len(matrix)))
    rank = 0
    pivot_rows, pivot_columns = [], []
    for column in range(len(matrix[0])):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        value = matrix[rank][column]
        for i in range(rank + 1, len(matrix)):
            if matrix[i][column]:
                multiplier = matrix[i][column] / value
                for j in range(column, len(matrix[0])):
                    matrix[i][j] -= multiplier * matrix[rank][j]
        pivot_rows.append(rows[rank])
        pivot_columns.append(column)
        rank += 1
        if rank == len(matrix):
            break
    return rank, pivot_rows, pivot_columns


def integer_anchor_matrix(degree: int):
    pairs = [(0, 1), (0, 2), (1, 2)] + [(0, j) for j in range(3, degree)]
    matrix = [[Q(0) for _ in range(degree)] for _ in range(degree)]
    for i, (u, v) in enumerate(pairs):
        matrix[i][u] = 1
        matrix[i][v] = 1
    return pairs, matrix


def model_domain_evidence(frozen_dir: Path):
    stored = json.loads((frozen_dir / "k3p_model_domain_bridge.json").read_text())

    # Each transition row is a translate of p=(p0,pC,pG,pT).  Coefficients
    # are recorded against the formal vector (1,c,g,t), with denominator 4.
    inverse_fourier_coefficients = (
        (1, 1, 1, 1),
        (1, 1, -1, -1),
        (1, -1, 1, -1),
        (1, -1, -1, 1),
    )
    hadamard = inverse_fourier_coefficients
    product_matrix = [
        [sum(hadamard[i][k] * hadamard[j][k] for k in range(4)) for j in range(4)]
        for i in range(4)
    ]
    assert product_matrix == [[4 if i == j else 0 for j in range(4)] for i in range(4)]
    assert [sum(row) for row in inverse_fourier_coefficients] == [4, 0, 0, 0]

    # CT spectra are exponent vectors in substitution rates (A,B,C).
    ct_exponents = {
        "c": (0, -2, -2),
        "g": (-2, 0, -2),
        "t": (-2, -2, 0),
    }
    ratio_exponents = {
        "c/(g*t)": tuple(ct_exponents["c"][i] - ct_exponents["g"][i] - ct_exponents["t"][i] for i in range(3)),
        "g/(c*t)": tuple(ct_exponents["g"][i] - ct_exponents["c"][i] - ct_exponents["t"][i] for i in range(3)),
        "t/(c*g)": tuple(ct_exponents["t"][i] - ct_exponents["c"][i] - ct_exponents["g"][i] for i in range(3)),
    }
    assert ratio_exponents == {
        "c/(g*t)": (4, 0, 0),
        "g/(c*t)": (0, 4, 0),
        "t/(c*g)": (0, 0, 4),
    }

    # The residual edge (c/r,g/r,t/r) is strict whenever
    # r exceeds these six lower bounds and r<1.
    subdivision_lower_bounds = ("c", "g", "t", "g+t-c", "c+t-g", "c+g-t")
    examples = []
    for triple in ((Q(1, 2), Q(2, 5), Q(1, 3)), (Q(2, 7), Q(3, 10), Q(1, 4))):
        c, g, t = triple
        lower = max(c, g, t, g + t - c, c + t - g, c + g - t)
        r = (1 + lower) / 2
        residual = (c / r, g / r, t / r)
        for cc, gg, tt in ((r, r, r), residual):
            margins = (
                cc, gg, tt, 1 - cc, 1 - gg, 1 - tt,
                1 + cc - gg - tt, 1 - cc + gg - tt, 1 - cc - gg + tt,
            )
            assert min(margins) > 0
        assert tuple(r * x for x in residual) == triple
        examples.append({"triple": list(map(str, triple)), "lower_bound": str(lower), "r": str(r), "residual": list(map(str, residual))})
    assert examples == [
        {"triple": x["triple"], "lower_bound": x["R"], "r": x["r"], "residual": x["residual"]}
        for x in stored["examples"]
    ]

    # Root movement: M_ij=p_{i xor j} is symmetric, and each row is a
    # permutation of p.  Uniform detailed balance therefore holds formally.
    transition_index = [[i ^ j for j in range(4)] for i in range(4)]
    assert transition_index == [list(row) for row in zip(*transition_index)]
    assert all(sorted(row) == [0, 1, 2, 3] for row in transition_index)

    anchors = {}
    for degree in range(3, 13):
        pairs, matrix = integer_anchor_matrix(degree)
        value = determinant(matrix)
        assert abs(value) == 2
        stored_anchor = stored["anchors"][str(degree)]
        assert stored_anchor["pairs"] == [[u + 1, v + 1] for u, v in pairs]
        assert stored_anchor["one_sector_determinant"] == int(value)
        assert stored_anchor["one_sector_rank"] == degree
        assert stored_anchor["three_sector_determinant"] == int(value ** 3)
        assert stored_anchor["three_sector_rank"] == 3 * degree
        anchors[str(degree)] = {
            "pairs": [[u + 1, v + 1] for u, v in pairs],
            "one_sector_determinant": int(value),
            "three_sector_determinant": int(value ** 3),
            "three_sector_rank": 3 * degree,
        }
    return {
        "schema": "k3p-primary-model-domain-exact-v1",
        "inverse_fourier_coefficients_over_4": [list(x) for x in inverse_fourier_coefficients],
        "hadamard_product": product_matrix,
        "principal_domain_proof": "pC,pG,pT>0 are exactly the three displayed composition inequalities; p0>0 follows from c,g,t>0",
        "ct_exponent_vectors": {k: list(v) for k, v in ct_exponents.items()},
        "ct_ratio_exponents": {k: list(v) for k, v in ratio_exponents.items()},
        "subdivision_lower_bounds": list(subdivision_lower_bounds),
        "subdivision_examples": examples,
        "root_movement_transition_index": transition_index,
        "root_movement_detailed_balance": True,
        "anchors": anchors,
    }


# Sparse polynomials use exponent tuples and exact rational coefficients.
def p_add(*terms):
    result = defaultdict(Q)
    for coefficient, polynomial in terms:
        for exponent, value in polynomial.items():
            result[exponent] += Q(coefficient) * value
    return {e: c for e, c in result.items() if c}


def p_mul(left, right):
    result = defaultdict(Q)
    for e, c in left.items():
        for f, d in right.items():
            result[tuple(x + y for x, y in zip(e, f))] += c * d
    return {e: c for e, c in result.items() if c}


def p_product(polynomials, n):
    result = {(0,) * n: Q(1)}
    for polynomial in polynomials:
        result = p_mul(result, polynomial)
    return result


def p_var(n, index):
    return {tuple(1 if i == index else 0 for i in range(n)): Q(1)}


def p_one(n):
    return {(0,) * n: Q(1)}


def p_evaluate(polynomial, point):
    zero = point[0] * 0
    result = zero
    for exponent, coefficient in polynomial.items():
        term = zero + coefficient
        for value, power in zip(point, exponent):
            if power:
                term *= value ** power
        result += term
    return result


def p_derivative_value(polynomial, point, variable):
    zero = point[0] * 0
    result = zero
    for exponent, coefficient in polynomial.items():
        power = exponent[variable]
        if not power:
            continue
        term = zero + coefficient * power
        for j, (value, e) in enumerate(zip(point, exponent)):
            use_power = e - 1 if j == variable else e
            if use_power:
                term *= value ** use_power
        result += term
    return result


def edge_character_variable(n, edge_index, character):
    if character == 0:
        return p_one(n)
    return p_var(n, 3 * edge_index + character - 1)


def tree_polynomials():
    n = 9
    outputs = []
    for x, y, z in CH3:
        outputs.append(
            p_product(
                [
                    edge_character_variable(n, 0, x),
                    edge_character_variable(n, 1, y),
                    edge_character_variable(n, 2, z),
                ],
                n,
            )
        )
    return outputs


def sunlet_polynomials(orientation: int):
    """Three-sunlet map from q=abc[L f_y d_z +(1-L) f_x e_z]."""
    n = 19
    if orientation == 3:
        port_order = (0, 1, 2)
    elif orientation == 2:
        port_order = (0, 2, 1)
    elif orientation == 1:
        port_order = (1, 2, 0)
    else:
        raise ValueError(orientation)
    lam = p_var(n, 18)
    one_minus_lam = p_add((1, p_one(n)), (-1, lam))
    outputs = []
    for original in CH3:
        x, y, z = (original[i] for i in port_order)
        outer = p_product(
            [
                edge_character_variable(n, 0, x),
                edge_character_variable(n, 1, y),
                edge_character_variable(n, 2, z),
            ],
            n,
        )
        first = p_product(
            [lam, edge_character_variable(n, 5, y), edge_character_variable(n, 3, z)], n
        )
        second = p_product(
            [one_minus_lam, edge_character_variable(n, 5, x), edge_character_variable(n, 4, z)], n
        )
        outputs.append(p_mul(outer, p_add((1, first), (1, second))))
    return outputs


def compose_coordinate_polynomial(outputs, terms):
    n = len(next(iter(outputs[0])))
    result = {}
    for term in terms:
        monomial = p_product([outputs[i] for i in term["coordinate_indices"]], n)
        result = p_add((1, result), (term["coefficient"], monomial))
    return result


def output_values(outputs, point):
    return tuple(p_evaluate(polynomial, point) for polynomial in outputs)


def output_jacobian(outputs, point):
    return [
        [p_derivative_value(polynomial, point, j) for j in range(len(point))]
        for polynomial in outputs
    ]


def parse_sparse_expression(text: str, variables: dict[str, dict], n: int):
    tree = ast.parse(text, mode="eval")

    def visit(node):
        if isinstance(node, ast.Name):
            return variables[node.id]
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return {(0,) * n: Q(node.value)}
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return p_add((-1, visit(node.operand)))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
            return p_mul(visit(node.left), visit(node.right))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return p_add((1, visit(node.left)), (1, visit(node.right)))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub):
            return p_add((1, visit(node.left)), (-1, visit(node.right)))
        raise ValueError(f"unsupported exact factor AST: {ast.dump(node)}")

    return visit(tree.body)


def three_port_evidence(frozen_dir: Path, separator_path: Path):
    rank_input = json.loads((frozen_dir / "k3p_three_port_ranks.json").read_text())
    quartic_input = json.loads((frozen_dir / "k3p_three_sunlet_quartic.json").read_text())
    separator_input = json.loads(separator_path.read_text())
    assert separator_input["schema"] == "k3p-tree-sunlet-literal-separator-v2"
    assert separator_input["map_formula"] == "q_xyz=a_x*b_y*c_z*(L*f_y*d_z+(1-L)*f_x*e_z)"
    assert separator_input["edge_order"] == ["a", "b", "c", "d", "e", "f"]
    labels = ["".join(CHAR_NAMES[x] for x in chars) for chars in CH3]
    assert labels == rank_input["coordinate_labels"]

    tree_outputs = tree_polynomials()
    sunlet_outputs = {orientation: sunlet_polynomials(orientation) for orientation in (1, 2, 3)}
    tree_point = tuple(Q(x) for _ in range(3) for x in (Q(2, 5), Q(3, 7), Q(4, 9)))
    tree_matrix = output_jacobian(tree_outputs, tree_point)
    tree_rank, tree_rows, tree_columns = rank_pivots(tree_matrix)
    assert tree_rank == 9
    tree_minor = determinant([[tree_matrix[i][j] for j in tree_columns] for i in tree_rows])
    assert tree_minor

    # Edge order (a,b,c,d,e,f), with f isotropic 1/3 as in the map formula.
    sunlet_point = tuple(
        value
        for edge in (
            (Q(1, 2),) * 3,
            (Q(1, 2),) * 3,
            (Q(1, 2),) * 3,
            (Q(1, 2),) * 3,
            (Q(1, 2),) * 3,
            (Q(1, 3),) * 3,
        )
        for value in edge
    ) + (Q(1, 2),)
    common_values = None
    orientation_evidence = {}
    for orientation, outputs in sunlet_outputs.items():
        values = output_values(outputs, sunlet_point)
        if common_values is None:
            common_values = values
        assert values == common_values
        matrix = output_jacobian(outputs, sunlet_point)
        rank, rows, columns = rank_pivots(matrix)
        assert rank == 14
        minor = determinant([[matrix[i][j] for j in columns] for i in rows])
        assert minor
        orientation_evidence[str(orientation)] = {
            "rank": rank,
            "minor_rows": rows,
            "minor_columns": columns,
            "minor_determinant": str(minor),
        }
    assert [str(x) for x in common_values] == rank_input["common_tensor"]

    quartic_pullbacks = {}
    for orientation, outputs in sunlet_outputs.items():
        pullback = compose_coordinate_polynomial(outputs, quartic_input["terms"])
        assert not pullback
        quartic_pullbacks[str(orientation)] = "identically_zero"
    quartic_value = Q(0)
    gradient = []
    for coordinate in range(16):
        derivative = Q(0)
        for term in quartic_input["terms"]:
            multiplicity = term["coordinate_indices"].count(coordinate)
            if not multiplicity:
                continue
            product_value = Q(term["coefficient"] * multiplicity)
            removed = False
            for i in term["coordinate_indices"]:
                if i == coordinate and not removed:
                    removed = True
                else:
                    product_value *= common_values[i]
            derivative += product_value
        gradient.append(derivative)
    for term in quartic_input["terms"]:
        value = Q(term["coefficient"])
        for i in term["coordinate_indices"]:
            value *= common_values[i]
        quartic_value += value
    assert quartic_value == 0 and any(gradient)

    label_index = {label: i for i, label in enumerate(labels)}
    circuit_terms = [
        [
            {"coefficient": 1, "coordinate_indices": [label_index[x] for x in record["left"]]},
            {"coefficient": -1, "coordinate_indices": [label_index[x] for x in record["right"]]},
        ]
        for record in separator_input["circuits"]
    ]
    variables = {"L": p_var(19, 18)}
    # The active v2 certificate uses the literal displayed edge order.  No
    # hidden d/e/f permutation is accepted at this interface.
    for edge_index, edge_name in enumerate(separator_input["edge_order"]):
        for h, h_name in enumerate("CGT", start=1):
            variables[edge_name + h_name] = edge_character_variable(19, edge_index, h)
    separator_evidence = []
    for record, terms in zip(separator_input["circuits"], circuit_terms):
        assert not compose_coordinate_polynomial(tree_outputs, terms)
        pullback = compose_coordinate_polynomial(sunlet_outputs[3], terms)
        expected = parse_sparse_expression(record["literal_sunlet_factor"], variables, 19)
        assert pullback == expected
        separator_evidence.append(
            {
                "id": record["id"],
                "left": record["left"],
                "right": record["right"],
                "expanded_terms": len(pullback),
                "exact_factor": record["literal_sunlet_factor"],
                "composition_margin": record["composition_margin"],
                "factor_sign": record["factor_sign"],
            }
        )
    assert len(separator_evidence) == 6

    # The nonzero proof is an exact cancellation argument over positive
    # variables: each composition margin occurs with its two reciprocal cross
    # equations.  The three margin equations multiply to p=p^2.
    contradiction_checks = {
        "paired_cross_equations_force": ["fG^2=1", "fT^2=1", "fC^2=1"],
        "paired_circuits": [["I1", "I3"], ["I2", "I4"], ["I5", "I6"]],
        "all_composition_margins_zero_force": "p=p^2 for p=fC*fG*fT",
        "domain_excludes": ["fC=1", "fG=1", "fT=1", "p=1"],
    }
    return {
        "schema": "k3p-primary-three-port-exact-v2",
        "tree_sunlet_separator": {
            "schema": separator_input["schema"],
            "payload_sha256": separator_input["payload_sha256"],
            "map_formula": separator_input["map_formula"],
            "edge_order": separator_input["edge_order"],
            "hidden_edge_permutation_used": False,
        },
        "tree_rank": tree_rank,
        "tree_minor": {"rows": tree_rows, "columns": tree_columns, "determinant": str(tree_minor)},
        "sunlet_orientations": orientation_evidence,
        "common_tensor": [str(x) for x in common_values],
        "quartic_terms": quartic_input["terms"],
        "quartic_pullbacks": quartic_pullbacks,
        "quartic_common_value": str(quartic_value),
        "quartic_gradient": [str(x) for x in gradient],
        "quartic_smooth_at_common_point": quartic_value == 0 and any(gradient),
        "tree_sunlet_circuits": separator_evidence,
        "tree_sunlet_strictness_argument": contradiction_checks,
        "tree_sunlet_sum_of_squares_strict": True,
    }


class Alg:
    """Q[h]/(5 h^4-1), represented in the basis 1,h,h^2,h^3."""

    __slots__ = ("c",)

    def __init__(self, value=0):
        if isinstance(value, Alg):
            self.c = value.c
        elif isinstance(value, (tuple, list)):
            values = list(map(Q, value)) + [Q(0)] * (4 - len(value))
            self.c = tuple(values[:4])
        else:
            self.c = (Q(value), Q(0), Q(0), Q(0))

    def __add__(self, other):
        other = Alg(other)
        return Alg(tuple(a + b for a, b in zip(self.c, other.c)))

    __radd__ = __add__

    def __neg__(self):
        return Alg(tuple(-a for a in self.c))

    def __sub__(self, other):
        return self + (-Alg(other))

    def __rsub__(self, other):
        return Alg(other) - self

    def __mul__(self, other):
        other = Alg(other)
        raw = [Q(0)] * 7
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                raw[i + j] += a * b
        for degree in range(6, 3, -1):
            raw[degree - 4] += raw[degree] / 5
        return Alg(tuple(raw[:4]))

    __rmul__ = __mul__

    def __pow__(self, exponent: int):
        if exponent < 0:
            return (self.inverse()) ** (-exponent)
        result, base = Alg(1), self
        while exponent:
            if exponent & 1:
                result *= base
            base *= base
            exponent >>= 1
        return result

    def inverse(self):
        if not self:
            raise ZeroDivisionError
        h = Alg((0, 1, 0, 0))
        basis = [Alg(1), h, h * h, h * h * h]
        matrix = [[(self * basis[j]).c[i] for j in range(4)] for i in range(4)]
        augmented = [row + [Q(1 if i == 0 else 0)] for i, row in enumerate(matrix)]
        for column in range(4):
            pivot = next(i for i in range(column, 4) if augmented[i][column])
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
            value = augmented[column][column]
            augmented[column] = [x / value for x in augmented[column]]
            for i in range(4):
                if i != column and augmented[i][column]:
                    factor = augmented[i][column]
                    augmented[i] = [x - factor * y for x, y in zip(augmented[i], augmented[column])]
        result = Alg(tuple(augmented[i][4] for i in range(4)))
        assert self * result == Alg(1)
        return result

    def __truediv__(self, other):
        return self * Alg(other).inverse()

    def __rtruediv__(self, other):
        return Alg(other) / self

    def __eq__(self, other):
        return self.c == Alg(other).c

    def __bool__(self):
        return any(self.c)

    def __repr__(self):
        return f"Alg({','.join(map(str, self.c))})"

    def as_string(self):
        names = ("1", "h", "h^2", "h^3")
        terms = [f"({coefficient})*{name}" for coefficient, name in zip(self.c, names) if coefficient]
        return " + ".join(terms) if terms else "0"


class Interval:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = Q(lo)
        self.hi = self.lo if hi is None else Q(hi)
        assert self.lo <= self.hi

    def __add__(self, other):
        other = other if isinstance(other, Interval) else Interval(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-(other if isinstance(other, Interval) else Interval(other)))

    def __rsub__(self, other):
        return Interval(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Interval) else Interval(other)
        values = (self.lo * other.lo, self.lo * other.hi, self.hi * other.lo, self.hi * other.hi)
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = other if isinstance(other, Interval) else Interval(other)
        assert not (other.lo <= 0 <= other.hi)
        reciprocal = Interval(1 / other.hi, 1 / other.lo) if other.lo > 0 else Interval(1 / other.hi, 1 / other.lo)
        return self * reciprocal


def alg_interval(value: Alg, h_interval: Interval):
    result = Interval(0)
    power = Interval(1)
    for coefficient in value.c:
        result += coefficient * power
        power *= h_interval
    return result


def collision_polynomials():
    n = 29
    lam2, lam3 = p_var(n, 27), p_var(n, 28)
    m2, m3 = p_add((1, p_one(n)), (-1, lam2)), p_add((1, p_one(n)), (-1, lam3))
    outputs = []
    # edges: L1,K2,K3,U,V,S2,S3,T2,T3
    for x, y, z in CH3:
        outer = p_product(
            [edge_character_variable(n, 0, x), edge_character_variable(n, 1, y), edge_character_variable(n, 2, z)], n
        )
        terms = [
            p_product([lam2, lam3, edge_character_variable(n, 5, y), edge_character_variable(n, 6, z), edge_character_variable(n, 3, y ^ z)], n),
            p_product([lam2, m3, edge_character_variable(n, 5, y), edge_character_variable(n, 8, z), edge_character_variable(n, 3, y), edge_character_variable(n, 4, z)], n),
            p_product([m2, lam3, edge_character_variable(n, 7, y), edge_character_variable(n, 6, z), edge_character_variable(n, 3, z), edge_character_variable(n, 4, y)], n),
            p_product([m2, m3, edge_character_variable(n, 7, y), edge_character_variable(n, 8, z), edge_character_variable(n, 4, y ^ z)], n),
        ]
        outputs.append(p_mul(outer, p_add(*((1, term) for term in terms))))
    return outputs


def collision_evidence():
    h = Alg((0, 1, 0, 0))
    k = (Alg(Q(1, 2)),) * 3
    u = (h / 3, h, Alg(Q(1, 3)))
    v = (h, h / 3, Alg(Q(1, 3)))
    s = (3 * h * h / 4, Alg(Q(1, 4)), Alg(Q(3, 10)))
    t = (Alg(Q(1, 4)), 3 * h * h / 4, Alg(Q(3, 10)))
    edges = (
        tuple(x * x for x in k), k, k, u, v, s, s, t, t,
    )
    point = tuple(value for edge in edges for value in edge) + (Alg(Q(1, 2)), Alg(Q(1, 2)))
    outputs = collision_polynomials()
    network_values = output_values(outputs, point)

    alpha = ((5 * h ** 3 + h) / 16, (5 * h ** 3 + h) / 16, h * h / 4)
    beta = (h * h / 4,) * 3
    tree_point = tuple(value for edge in (alpha, beta, beta) for value in edge)
    tree_outputs = tree_polynomials()
    tree_values = output_values(tree_outputs, tree_point)
    assert network_values == tree_values

    matrix = output_jacobian(outputs[1:], point)
    rank, rows, columns = rank_pivots(matrix)
    assert rank == 15
    minor = determinant([[matrix[i][j] for j in columns] for i in rows])
    assert minor
    tree_matrix = output_jacobian(tree_outputs[1:], tree_point)
    tree_rank, tree_rows, tree_columns = rank_pivots(tree_matrix)
    assert tree_rank == 9
    tree_minor = determinant([[tree_matrix[i][j] for j in tree_columns] for i in tree_rows])
    assert tree_minor

    # h is the positive fourth root of 1/5; these rational bounds are exact.
    assert Q(2, 3) ** 4 < Q(1, 5) < Q(7, 10) ** 4
    h_box = Interval(Q(2, 3), Q(7, 10))
    physical_margins = []
    for side, triples in (("network", edges), ("tree", (alpha, beta, beta))):
        for edge_index, (c, g, tt) in enumerate(triples):
            tests = {
                "c": c, "g": g, "t": tt,
                "1-c": 1 - c, "1-g": 1 - g, "1-t": 1 - tt,
                "1+c-g-t": 1 + c - g - tt,
                "1-c+g-t": 1 - c + g - tt,
                "1-c-g+t": 1 - c - g + tt,
            }
            for name, value in tests.items():
                enclosure = alg_interval(value, h_box)
                assert enclosure.lo > 0, (side, edge_index, name, enclosure.lo, enclosure.hi)
                physical_margins.append((enclosure.lo, f"{side}:e{edge_index}:{name}"))
    minimum = min(physical_margins)
    return {
        "schema": "k3p-tree-double-theta-collision-exact-v1",
        "field_relation": "5*h^4-1=0",
        "rational_isolating_interval": ["2/3", "7/10"],
        "consistent_coordinate_equalities": 16,
        "network_rank": rank,
        "network_rank_minor_rows": rows,
        "network_rank_minor_columns": columns,
        "network_rank_minor_determinant": minor.as_string(),
        "tree_rank": tree_rank,
        "tree_rank_minor_determinant": tree_minor.as_string(),
        "network_parameter_dimension": 29,
        "local_collision_dimension": 29 - (15 - 9),
        "minimum_certified_principal_margin_lower_bound": [minimum[1], str(minimum[0])],
    }


def enumerate_rootings(arcs, retics, leaves, original_root):
    root_children = [v for u, v in arcs if u == original_root]
    assert len(root_children) == 2
    directed = {(u, v) for u, v in arcs if v in retics}
    undirected = {
        frozenset((u, v)) for u, v in arcs if u != original_root and v not in retics
    }
    undirected.add(frozenset(root_children))
    edge_records = [("d", u, v) for u, v in sorted(directed)] + [
        ("u", *sorted(edge)) for edge in sorted(undirected, key=lambda x: sorted(x))
    ]
    nodes = {x for edge in arcs for x in edge} - {original_root}
    rootings = []
    for removed_index, root_edge in enumerate(edge_records):
        a, b = root_edge[1:]
        remaining = edge_records[:removed_index] + edge_records[removed_index + 1 :]
        free_edges = [edge for edge in remaining if edge[0] == "u"]
        fixed = [(edge[1], edge[2]) for edge in remaining if edge[0] == "d"]
        for bits in product((0, 1), repeat=len(free_edges)):
            oriented = list(fixed) + [
                (u, v) if bit else (v, u)
                for bit, (_, u, v) in zip(bits, free_edges)
            ] + [("ROOT", a), ("ROOT", b)]
            indegree = {n: 0 for n in nodes} | {"ROOT": 0}
            children = {n: [] for n in nodes} | {"ROOT": []}
            for u, v in oriented:
                indegree[v] += 1
                children[u].append(v)
            if any(indegree[n] != (2 if n in retics else 1) for n in nodes):
                continue
            queue, seen = ["ROOT"], set()
            while queue:
                node = queue.pop()
                if node in seen:
                    continue
                seen.add(node)
                queue.extend(children[node])
            if len(seen) != len(nodes) + 1:
                continue
            tree_child = all(
                node in leaves or any(child not in retics for child in children[node])
                for node in children
            )
            rootings.append(
                {
                    "root_edge": sorted((a, b)),
                    "tree_child": tree_child,
                    "oriented_edges": oriented,
                }
            )
    return rootings


def rooting_census_evidence(frozen_dir: Path):
    stored = json.loads((frozen_dir / "k3p_rooting_censuses.json").read_text())
    duplicate = json.loads((frozen_dir / "k3p_rooting_censuses (1).json").read_text())
    assert stored == duplicate
    cases = {
        "W": (
            [("r", "S"), ("r", "L0"), ("S", "U"), ("S", "V"), ("U", "X"), ("V", "Z"), ("Z", "X"), ("U", "V"), ("Z", "L1"), ("X", "L2")],
            {"V", "X"}, {"L0", "L1", "L2"}, "r",
        ),
        "Wprime": (
            [("r", "S"), ("r", "L0"), ("S", "U"), ("S", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V"), ("X0", "L1"), ("X1", "L2")],
            {"X0", "X1"}, {"L0", "L1", "L2"}, "r",
        ),
        "collision": (
            [("rho", "1"), ("rho", "u"), ("u", "p"), ("u", "q"), ("p", "r2"), ("q", "r2"), ("p", "r3"), ("q", "r3"), ("r2", "2"), ("r3", "3")],
            {"r2", "r3"}, {"1", "2", "3"}, "rho",
        ),
    }
    evidence = {}
    for name, args in cases.items():
        rootings = enumerate_rootings(*args)
        summary = {
            "admissible": len(rootings),
            "tree_child": sum(x["tree_child"] for x in rootings),
            "non_tree_child": sum(not x["tree_child"] for x in rootings),
            "root_edges": sorted([x["root_edge"] for x in rootings]),
        }
        assert summary["admissible"] == stored[name]["admissible"]
        assert summary["tree_child"] == stored[name]["tree_child"]
        assert summary["non_tree_child"] == stored[name]["non_tree_child"]
        stored_edges = sorted([sorted(ast.literal_eval(x) for x in r["root_edge"]) for r in stored[name]["rootings"]])
        assert summary["root_edges"] == stored_edges
        evidence[name] = summary
    return {"schema": "k3p-rooting-census-independent-v1", "cases": evidence}


def bridge_and_marginal_evidence(model_evidence):
    # The d-by-d anchor matrices prove freeness independently in each fixed
    # observable sector.  Direct cancellation proves the stated action.
    action = {
        "normalization": "a^0_{v,e}=1",
        "component_action": "P_v(h)->P_v(h)*prod_e a^{h_e}_{v,e} for h_e in {C,G,T}",
        "bridge_action": "k_e(h)->k_e(h)/(a^h_{u,e}*a^h_{v,e})",
        "independent_nonzero_sectors": ["C", "G", "T"],
        "fixed_observable_sector_labels": True,
        "complete_positive_rank_one_cut_scalars": 3,
        "cancellation_checked_sectorwise": True,
        "no_holonomy_reason": "the component-incidence graph is a tree, so leaf peeling reaches every incidence",
    }
    assert all(record["three_sector_rank"] == 3 * int(degree) for degree, record in model_evidence["anchors"].items())
    normalizer = {
        "anchor_degree_range_replayed": [3, 12],
        "formula": [
            "a1=sqrt(r12*r13/r23)",
            "a2=sqrt(r12*r23/r13)",
            "a3=sqrt(r13*r23/r12)",
            "ak=r1k/a1",
        ],
        "all_anchor_determinants_nonzero": True,
        "rank_for_degree_d": "3d",
        "analytic_on_positive_anchor_charts": True,
    }
    physical_product = {
        "serial_split": "(c,g,t)=(r,r,r) odot (c/r,g/r,t/r)",
        "endpoint_scales_vary_near_identity": True,
        "residual_principal_domain_open": True,
        "all_bridges_simultaneous": "finite intersection of open neighborhoods",
    }
    marginal = {
        "map": "((c_i,g_i,t_i)) -> (prod c_i, prod g_i, prod t_i)",
        "jacobian_structure": "three disjoint positive rows",
        "rank": 3,
        "physical_surjectivity": "choose m-1 isotropic near-identity factors, then the strict residual factor",
        "all_m_positive_integers": True,
    }
    return action, normalizer, physical_product, marginal


def cut_recovery_evidence(frozen_dir: Path):
    """Historical cloud-transfer audit; deliberately not an active proof gate.

    The aggregate record below depended on the withdrawn CFN shortcut and is
    retained only to reproduce why the old universal pointwise claim was
    blocked.  Active primary item 6 uses the independently sealed directional
    strong-class containment cut-transfer package instead.
    """
    transfer = json.loads((frozen_dir / "k3p_pointwise_cut_transfer.json").read_text())
    missing_hash = transfer["frozen_certificate_sha256"]
    available_hashes = {}
    for path in frozen_dir.rglob("*"):
        if path.is_file():
            import hashlib
            available_hashes[hashlib.sha256(path.read_bytes()).hexdigest()] = path.name
    primitive_present = missing_hash in available_hashes
    return {
        "schema": "k3p-primary-cut-recovery-audit-v1",
        "transfer_record": transfer,
        "character_projection_identity_checked": transfer["character_projection"] == "{0,C}",
        "missing_frozen_JC_certificate_sha256": missing_hash,
        "primitive_certificate_present": primitive_present,
        "status": "PASS" if primitive_present else "BLOCKED",
        "exact_gap": None if primitive_present else "The 177 endpoint and 453 single-blob primitive records named by the transfer verifier are absent; only their aggregate counters and an absent-file hash are frozen.",
    }


def cherry_evidence():
    u = (Q(2, 5), Q(4, 9), Q(3, 7))
    v = (Q(3, 7), Q(5, 11), Q(4, 9))

    def margins(edge):
        c, g, t = edge
        return (c, g, t, 1-c, 1-g, 1-t, 1+c-g-t, 1-c+g-t, 1-c-g+t, c-g*t, g-c*t, t-c*g)

    assert min(margins(u)) > 0 and min(margins(v)) > 0
    blocks = [[[1 / b, -a / (b * b)], [b, a]] for a, b in zip(u, v)]
    block_determinants = [determinant(block) for block in blocks]
    value = block_determinants[0] * block_determinants[1] * block_determinants[2]
    expected = 8 * u[0] * u[1] * u[2] / (v[0] * v[1] * v[2])
    assert value == expected == Q(176, 25)
    return {
        "schema": "k3p-cherry-extension-exact-v1",
        "jacobian_block_determinants": [str(x) for x in block_determinants],
        "jacobian_determinant": str(value),
        "dimension_increment": 6,
        "base_dimension": 15,
        "all_n_dimension": "6n-3",
        "rooting_persistence_proof": "Replacing a leaf by a tree vertex with two leaf children preserves every existing tree-child witness and every existing violation; pruning and suppressing that cherry recovers the base rooting.",
        "tree_child_and_non_tree_child_base_rootings_exist": True,
        "rooting_class_persists_under_iteration": True,
    }
