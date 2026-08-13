#!/usr/bin/env python3
"""Fast exact verifier for the completed proof-first local calculations.

Standard library only.  The verifier does not import the discovery engine,
does not enumerate topology spaces, and deliberately excludes the unfinished
five-port TT-separated case.  It reconstructs six explicit minimal-support
graphs, enumerates at most four displayed trees per graph, checks the stated
Fourier identities and factorizations as sparse integer polynomials, and
computes exact rational Jacobian-minor certificates at one interior point.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from itertools import permutations, product
import json
from operator import xor
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "completed_certificate.json"

Monomial = tuple[int, ...]
Poly = dict[Monomial, int]


def padd(left: Poly, right: Poly, scale: int = 1) -> Poly:
    answer = dict(left)
    for monomial, coefficient in right.items():
        value = answer.get(monomial, 0) + scale * coefficient
        if value:
            answer[monomial] = value
        else:
            answer.pop(monomial, None)
    return answer


def pneg(value: Poly) -> Poly:
    return {monomial: -coefficient for monomial, coefficient in value.items()}


def pscale(value: Poly, scalar: int) -> Poly:
    return {monomial: scalar * coefficient for monomial, coefficient in value.items() if scalar * coefficient}


def pmul(left: Poly, right: Poly) -> Poly:
    answer: Poly = {}
    for a, ca in left.items():
        for b, cb in right.items():
            monomial = tuple(x + y for x, y in zip(a, b))
            answer[monomial] = answer.get(monomial, 0) + ca * cb
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def ppow(value: Poly, exponent: int, variables: int) -> Poly:
    answer = pconst(1, variables)
    for _ in range(exponent):
        answer = pmul(answer, value)
    return answer


def pconst(value: int, variables: int) -> Poly:
    return {} if value == 0 else {(0,) * variables: value}


def pvar(index: int, variables: int) -> Poly:
    exponent = [0] * variables
    exponent[index] = 1
    return {tuple(exponent): 1}


@dataclass(frozen=True)
class Core:
    name: str
    segments: tuple[tuple[str, str], ...]
    path_sinks: tuple[str, ...]


CORES = {
    "cycle": Core("cycle", (("S", "X"), ("S", "X")), ("X",)),
    "TR-separated": Core(
        "TR-separated",
        (("S", "U"), ("S", "V"), ("U", "X0"), ("V", "X0"), ("U", "V")),
        ("X0",),
    ),
    "TR-nested": Core(
        "TR-nested",
        (("S", "U"), ("S", "X0"), ("V", "X0"), ("U", "V"), ("U", "V")),
        ("X0",),
    ),
    "TT-nested": Core(
        "TT-nested",
        (("S", "U"), ("S", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V")),
        ("X0", "X1"),
    ),
}


@dataclass(frozen=True)
class Model:
    name: str
    core: Core
    repair: tuple[int, ...]
    edges: tuple[tuple[str, str], ...]
    labels: tuple[str, ...]
    reticulation_parents: tuple[tuple[str, tuple[tuple[str, str], tuple[str, str]]], ...]
    variable_names: tuple[str, ...]
    variable_index: dict[str, int]

    @property
    def variables(self) -> int:
        return len(self.variable_names)


def edge_name(edge: tuple[str, str]) -> str:
    return "x_" + "_".join(edge)


def build_model(name: str, core_name: str, repair: tuple[int, ...]) -> Model:
    core = CORES[core_name]
    edges: list[tuple[str, str]] = [("S", "L_I")]
    labels = ["I"]
    for index, (tail, head) in enumerate(core.segments):
        if index in repair:
            middle = f"P{index}"
            label = f"R{index}"
            edges.extend(((tail, middle), (middle, head), (middle, f"L_{label}")))
            labels.append(label)
        else:
            edges.append((tail, head))
    for sink in core.path_sinks:
        label = f"K_{sink}"
        edges.append((sink, f"L_{label}"))
        labels.append(label)

    incoming: dict[str, list[tuple[str, str]]] = {}
    for edge in edges:
        incoming.setdefault(edge[1], []).append(edge)
    retics = tuple(sorted(
        (node, tuple(sorted(parents)))
        for node, parents in incoming.items()
        if len(parents) == 2
    ))
    names = tuple(sorted([edge_name(edge) for edge in edges] + [f"l_{node}" for node, _ in retics]))
    return Model(
        name=name,
        core=core,
        repair=repair,
        edges=tuple(edges),
        labels=tuple(labels),
        reticulation_parents=retics,
        variable_names=names,
        variable_index={value: index for index, value in enumerate(names)},
    )


MODELS = {
    "cycle": build_model("cycle", "cycle", (0,)),
    "TR-separated-short": build_model("TR-separated-short", "TR-separated", (2, 3)),
    "TR-separated-long": build_model("TR-separated-long", "TR-separated", (3, 4)),
    "TR-nested": build_model("TR-nested", "TR-nested", (2, 3)),
    "TT-nested-short": build_model("TT-nested-short", "TT-nested", (2,)),
    "TT-nested-long": build_model("TT-nested-long", "TT-nested", (4,)),
}


def var(model: Model, name: str) -> Poly:
    return pvar(model.variable_index[name], model.variables)


def one_minus(model: Model, name: str) -> Poly:
    return padd(pconst(1, model.variables), var(model, name), -1)


def minus_one(model: Model, name: str) -> Poly:
    return padd(var(model, name), pconst(1, model.variables), -1)


def displayed(model: Model):
    retics = model.reticulation_parents
    for bits in product((0, 1), repeat=len(retics)):
        active = set(model.edges)
        weight = pconst(1, model.variables)
        for (node, (first, second)), bit in zip(retics, bits):
            inheritance = f"l_{node}"
            if bit == 0:
                active.remove(second)
                weight = pmul(weight, var(model, inheritance))
            else:
                active.remove(first)
                weight = pmul(weight, one_minus(model, inheritance))
        yield tuple(sorted(active)), weight


def descendants(active: tuple[tuple[str, str], ...], start: str) -> frozenset[str]:
    children: dict[str, list[str]] = {}
    for tail, head in active:
        children.setdefault(tail, []).append(head)
    answer: set[str] = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node.startswith("L_"):
            answer.add(node[2:])
        else:
            stack.extend(children.get(node, ()))
    return frozenset(answer)


def fourier(model: Model, characters: tuple[int, ...]) -> Poly:
    if len(characters) != len(model.labels) or reduce(xor, characters, 0):
        raise ValueError((model.labels, characters))
    assignment = dict(zip(model.labels, characters))
    total: Poly = {}
    for active, weight in displayed(model):
        term = weight
        for edge in active:
            character = 0
            for label in descendants(active, edge[1]):
                character ^= assignment[label]
            if character:
                term = pmul(term, var(model, edge_name(edge)))
        total = padd(total, term)
    return total


COLOUR_MAPS = tuple((0, *row) for row in permutations((1, 2, 3)))


def colour_canon(row: tuple[int, ...]) -> tuple[int, ...]:
    return min(tuple(mapping[value] for value in row) for mapping in COLOUR_MAPS)


REPS4 = tuple(sorted({
    colour_canon(row)
    for row in product(range(4), repeat=4)
    if reduce(xor, row, 0) == 0
}))


def coordinates4(model: Model) -> tuple[Poly, ...]:
    if len(model.labels) != 4:
        raise ValueError(model.name)
    return tuple(fourier(model, row) for row in REPS4)


def coordinates4_order(model: Model, order: tuple[str, ...]) -> tuple[Poly, ...]:
    if set(order) != set(model.labels) or len(order) != 4:
        raise ValueError((model.name, order, model.labels))
    answer = []
    for row in REPS4:
        assignment = dict(zip(order, row))
        answer.append(fourier(model, tuple(assignment[label] for label in model.labels)))
    return tuple(answer)


def qsum(q: tuple[Poly, ...], terms: tuple[tuple[int, int], ...]) -> Poly:
    answer: Poly = {}
    for coefficient, index in terms:
        answer = padd(answer, q[index], coefficient)
    return answer


def qmonomial(q: tuple[Poly, ...], indices: tuple[int, ...]) -> Poly:
    answer = pconst(1, len(next(iter(q[0]), ())))
    # q[0] is the constant polynomial and still carries the exponent width.
    variables = len(next(iter(q[0])))
    answer = pconst(1, variables)
    for index in indices:
        answer = pmul(answer, q[index])
    return answer


def qrelation(q: tuple[Poly, ...], terms: tuple[tuple[int, tuple[int, ...]], ...]) -> Poly:
    answer: Poly = {}
    for coefficient, indices in terms:
        answer = padd(answer, qmonomial(q, indices), coefficient)
    return answer


L_SEP = (
    ((1, 9), (-1, 10), (-1, 12), (1, 13)),
    ((1, 9), (-1, 10), (1, 12), (-1, 13)),
    ((1, 9), (1, 10), (-1, 12), (-1, 13)),
)
L_NESTED = (
    ((-1, 9), (-1, 10), (1, 12), (1, 13)),
    ((-1, 9), (1, 10), (-1, 12), (1, 13)),
    ((-1, 9), (1, 10), (1, 12), (-1, 13)),
)
C_TR = (
    (1, (3, 7, 8)), (1, (4, 6, 8)),
    (-1, (1, 8, 14)), (-1, (3, 6, 11)),
)
C_TT = (
    (1, (2, 7, 8)), (1, (4, 5, 8)),
    (-1, (1, 8, 11)), (-1, (2, 5, 14)),
)
H_TR_SEP_LONG = (
    (1, (0, 9, 10)), (-1, (0, 9, 12)),
    (-2, (0, 10, 13)), (2, (0, 12, 13)),
    (-2, (1, 8, 9)), (1, (1, 8, 10)),
    (1, (1, 8, 12)), (2, (1, 8, 13)),
    (-2, (1, 11, 14)), (2, (2, 6, 9)),
    (-1, (2, 6, 10)), (-1, (2, 6, 12)),
    (-2, (2, 6, 13)), (2, (2, 7, 14)),
    (1, (3, 5, 10)), (-1, (3, 5, 12)),
    (2, (4, 6, 11)), (-2, (4, 7, 8)),
)


def product_of(model: Model, factors: tuple[Poly, ...], scalar: int = 1) -> Poly:
    answer = pconst(scalar, model.variables)
    for factor in factors:
        answer = pmul(answer, factor)
    return answer


def power_var(model: Model, name: str, exponent: int) -> Poly:
    return ppow(var(model, name), exponent, model.variables)


def exact_value(poly: Poly, point: tuple[Fraction, ...]) -> Fraction:
    total = Fraction(0)
    for monomial, coefficient in poly.items():
        term = Fraction(coefficient)
        for exponent, value in zip(monomial, point):
            term *= value ** exponent
        total += term
    return total


def derivative_value(poly: Poly, variable: int, point: tuple[Fraction, ...]) -> Fraction:
    total = Fraction(0)
    for monomial, coefficient in poly.items():
        exponent = monomial[variable]
        if not exponent:
            continue
        term = Fraction(coefficient * exponent)
        for index, (power, value) in enumerate(zip(monomial, point)):
            term *= value ** (power - 1 if index == variable else power)
        total += term
    return total


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    size = len(matrix)
    work = [row[:] for row in matrix]
    answer = Fraction(1)
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        work[column] = [entry / value for entry in work[column]]
        for row in range(column + 1, size):
            factor = work[row][column]
            if factor:
                work[row] = [a - factor * b for a, b in zip(work[row], work[column])]
    return answer


def rank_minor(model: Model, coordinates: tuple[Poly, ...]) -> dict:
    point = tuple(Fraction(index + 2, index + 7) for index in range(model.variables))
    matrix = [
        [derivative_value(coordinate, column, point) for column in range(model.variables)]
        for coordinate in coordinates
    ]
    work = [row[:] for row in matrix]
    row_ids = list(range(len(work)))
    pivot_rows: list[int] = []
    pivot_columns: list[int] = []
    row = 0
    for column in range(model.variables):
        pivot = next((candidate for candidate in range(row, len(work)) if work[candidate][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        row_ids[row], row_ids[pivot] = row_ids[pivot], row_ids[row]
        value = work[row][column]
        work[row] = [entry / value for entry in work[row]]
        for candidate in range(len(work)):
            if candidate == row:
                continue
            factor = work[candidate][column]
            if factor:
                work[candidate] = [a - factor * b for a, b in zip(work[candidate], work[row])]
        pivot_rows.append(row_ids[row])
        pivot_columns.append(column)
        row += 1
        if row == len(work):
            break
    minor = [[matrix[r][c] for c in pivot_columns] for r in pivot_rows]
    det = determinant(minor)
    if not det:
        raise AssertionError((model.name, pivot_rows, pivot_columns))
    return {
        "rank_at_point": len(pivot_rows),
        "interpretation": "exact lower bound for generic rank; no upper-rank claim",
        "point": {name: fraction_text(value) for name, value in zip(model.variable_names, point)},
        "minor_coordinate_rows": ["".join(map(str, REPS4[index])) for index in pivot_rows],
        "minor_parameter_columns": [model.variable_names[index] for index in pivot_columns],
        "minor_determinant": fraction_text(det),
    }


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def completed_payload() -> dict:
    q = {name: coordinates4(model) for name, model in MODELS.items() if len(model.labels) == 4}

    identities = {
        "TR-separated-short::L_sep_0": not qsum(q["TR-separated-short"], L_SEP[0]),
        "TR-nested::L_nested_0": not qsum(q["TR-nested"], L_NESTED[0]),
        "TR-nested::C_TR": not qrelation(q["TR-nested"], C_TR),
        "TT-nested-short::L_nested_0": not qsum(q["TT-nested-short"], L_NESTED[0]),
        "TT-nested-short::C_TT": not qrelation(q["TT-nested-short"], C_TT),
        "TT-nested-long::L_nested_0": not qsum(q["TT-nested-long"], L_NESTED[0]),
        "TR-separated-long::H_in_order_(I,R3,K_X0,R4)": not qrelation(
            coordinates4_order(
                MODELS["TR-separated-long"],
                ("I", "R3", "K_X0", "R4"),
            ),
            H_TR_SEP_LONG,
        ),
    }
    if not all(identities.values()):
        raise AssertionError(identities)

    long_tr = MODELS["TR-separated-long"]
    q_long_tr = q["TR-separated-long"]
    rhs_a = product_of(long_tr, (
        var(long_tr, "l_V"), var(long_tr, "x_P3_L_R3"), var(long_tr, "x_P4_L_R4"),
        var(long_tr, "x_P4_V"), var(long_tr, "x_S_L_I"), var(long_tr, "x_S_U"),
        var(long_tr, "x_U_X0"), var(long_tr, "x_V_P3"), var(long_tr, "x_X0_L_K_X0"),
        minus_one(long_tr, "l_X0"), minus_one(long_tr, "x_U_P4"),
    ), scalar=2)
    bracket = padd(
        padd(
            pmul(pmul(var(long_tr, "l_V"), var(long_tr, "x_P4_V")), var(long_tr, "x_V_P3")),
            pmul(pmul(var(long_tr, "l_V"), var(long_tr, "x_S_V")), var(long_tr, "x_V_P3")),
            -1,
        ),
        padd(pmul(var(long_tr, "x_S_V"), var(long_tr, "x_V_P3")), pconst(1, long_tr.variables), -1),
    )
    rhs_b = product_of(long_tr, (
        var(long_tr, "l_X0"), var(long_tr, "x_P3_L_R3"), var(long_tr, "x_P3_X0"),
        var(long_tr, "x_P4_L_R4"), var(long_tr, "x_S_L_I"), var(long_tr, "x_S_U"),
        var(long_tr, "x_U_P4"), var(long_tr, "x_X0_L_K_X0"), bracket,
    ), scalar=-2)
    rhs_c = product_of(long_tr, (
        var(long_tr, "x_P3_L_R3"), var(long_tr, "x_P4_L_R4"), var(long_tr, "x_S_L_I"),
        var(long_tr, "x_S_V"), var(long_tr, "x_U_P4"), var(long_tr, "x_U_X0"),
        var(long_tr, "x_V_P3"), var(long_tr, "x_X0_L_K_X0"),
        minus_one(long_tr, "l_V"), minus_one(long_tr, "l_X0"), minus_one(long_tr, "x_S_U"),
    ), scalar=-2)
    sep_rhs = (rhs_a, rhs_b, rhs_c)
    contrast_factorizations = {}
    for index, rhs in enumerate(sep_rhs):
        lhs = qsum(q_long_tr, L_SEP[index])
        good = lhs == rhs
        contrast_factorizations[f"TR-separated-long::L_sep_{index}"] = good
        if not good:
            raise AssertionError((index, padd(lhs, rhs, -1)))
    # The nested contrasts occur in reverse order with the opposite sign.
    for index, rhs in enumerate(reversed(sep_rhs)):
        lhs = qsum(q_long_tr, L_NESTED[index])
        good = lhs == pneg(rhs)
        contrast_factorizations[f"TR-separated-long::L_nested_{index}"] = good
        if not good:
            raise AssertionError(("nested", index, padd(lhs, pneg(rhs), -1)))

    long_tt = MODELS["TT-nested-long"]
    q_long_tt = q["TT-nested-long"]
    rhs_ctr = product_of(long_tt, (
        var(long_tt, "l_X0"), power_var(long_tt, "x_P4_L_R4", 2), power_var(long_tt, "x_S_L_I", 2),
        var(long_tt, "x_S_U"), var(long_tt, "x_S_X0"), var(long_tt, "x_U_V"),
        var(long_tt, "x_U_X1"), power_var(long_tt, "x_V_P4", 2), var(long_tt, "x_V_X0"),
        power_var(long_tt, "x_X0_L_K_X0", 2), var(long_tt, "x_X1_L_K_X1"),
        minus_one(long_tt, "l_X0"), minus_one(long_tt, "l_X1"),
        minus_one(long_tt, "x_S_U"), minus_one(long_tt, "x_U_V"),
        padd(pmul(var(long_tt, "x_S_U"), var(long_tt, "x_U_V")), pconst(1, long_tt.variables), -1),
    ))
    rhs_ctt = product_of(long_tt, (
        var(long_tt, "l_X1"), power_var(long_tt, "x_P4_L_R4", 2), var(long_tt, "x_P4_X1"),
        power_var(long_tt, "x_S_L_I", 2), power_var(long_tt, "x_S_U", 2), var(long_tt, "x_U_V"),
        var(long_tt, "x_U_X1"), var(long_tt, "x_V_P4"), var(long_tt, "x_V_X0"),
        var(long_tt, "x_X0_L_K_X0"), power_var(long_tt, "x_X1_L_K_X1", 2),
        minus_one(long_tt, "l_X0"), minus_one(long_tt, "l_X1"),
        minus_one(long_tt, "x_U_V"), minus_one(long_tt, "x_V_P4"),
        padd(pmul(var(long_tt, "x_U_V"), var(long_tt, "x_V_P4")), pconst(1, long_tt.variables), -1),
    ))
    cubic_factorizations = {
        "TT-nested-long::C_TR": qrelation(q_long_tt, C_TR) == rhs_ctr,
        "TT-nested-long::C_TT": qrelation(q_long_tt, C_TT) == rhs_ctt,
    }
    if not all(cubic_factorizations.values()):
        raise AssertionError(cubic_factorizations)

    witness_point = lambda model: tuple(Fraction(index + 2, index + 7) for index in range(model.variables))
    cross_nonzero = {
        "TR-nested::C_TT": fraction_text(exact_value(qrelation(q["TR-nested"], C_TT), witness_point(MODELS["TR-nested"]))),
        "TT-nested-short::C_TR": fraction_text(exact_value(qrelation(q["TT-nested-short"], C_TR), witness_point(MODELS["TT-nested-short"]))),
    }
    if any(value == "0" for value in cross_nonzero.values()):
        raise AssertionError(cross_nonzero)

    rank_rows = {
        name: rank_minor(MODELS[name], q[name])
        for name in (
            "TR-separated-short", "TR-separated-long", "TR-nested",
            "TT-nested-short", "TT-nested-long",
        )
    }
    # The three-port JC orbit tensor has four nonconstant coordinates, so this
    # nonzero rank-four certificate is also an exact rank upper/lower match.
    cycle = MODELS["cycle"]
    cycle_rows = tuple(
        fourier(cycle, row)
        for row in product(range(4), repeat=3)
        if reduce(xor, row, 0) == 0
    )
    # Use an ad-hoc version of rank_minor because REPS4 labels do not apply.
    point = tuple(Fraction(index + 2, index + 7) for index in range(cycle.variables))
    cycle_matrix = [[derivative_value(poly, c, point) for c in range(cycle.variables)] for poly in cycle_rows]
    # Exact rank by elimination; no minor labels needed beyond the value.
    work = [row[:] for row in cycle_matrix]
    rank = 0
    columns = len(work[0])
    for column in range(columns):
        pivot = next((r for r in range(rank, len(work)) if work[r][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        value = work[rank][column]
        work[rank] = [x / value for x in work[rank]]
        for r in range(len(work)):
            if r != rank and work[r][column]:
                factor = work[r][column]
                work[r] = [a - factor * b for a, b in zip(work[r], work[rank])]
        rank += 1
    if rank != 4:
        raise AssertionError(("cycle rank", rank))

    return {
        "schema": 1,
        "scope": "completed cycle and four-port minimum-support calculations only; five-port TT-separated and uniform local containment excluded",
        "coordinate_order": ["".join(map(str, row)) for row in REPS4],
        "identities": identities,
        "strict_factorization_equalities": {
            **contrast_factorizations,
            **cubic_factorizations,
        },
        "strict_sign_reason": {
            "TR-separated-long contrasts": "all three L_sep pullbacks are >0 and all three L_nested pullbacks are <0 on 0<x,lambda<1; the only composite bracket is x_VP3*(lambda_V*x_P4V+(1-lambda_V)*x_SV)-1<0",
            "TT-nested-long cubics": "both C_TR and C_TT pullbacks are <0 because their positive monomial is multiplied by two inheritance factors (lambda-1) and three edge/product factors (x-1)",
        },
        "cross_cubic_nonzero_exact_witnesses": cross_nonzero,
        "jacobian_certificates": rank_rows,
        "cycle_rank": {
            "rank_at_point": rank,
            "exact_generic_rank": 4,
            "upper_bound": "four nonconstant normalized three-port JC orbit coordinates",
        },
        "excluded_claims": [
            "no upper-rank certificate for any four-port model",
            "no five-port TT-separated classification",
            "no exhaustive labelled-port or target-completion theorem",
            "no uniform local containment theorem",
            "no global identifiability theorem",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write the deterministic checked certificate")
    args = parser.parse_args()
    payload = completed_payload()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.write:
        CERTIFICATE.write_text(rendered)
        print(f"WROTE {CERTIFICATE}")
        return
    if not CERTIFICATE.exists():
        raise SystemExit(f"missing {CERTIFICATE}; run with --write once")
    if CERTIFICATE.read_text() != rendered:
        raise SystemExit("certificate mismatch")
    print("VERIFIED: completed proof-first cycle/four-port calculations")


if __name__ == "__main__":
    main()
