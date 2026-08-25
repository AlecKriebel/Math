#!/usr/bin/env python3
"""Independent exact-rational replay of the K3P weak-class sharpness box.

This verifier deliberately does not import the cloud map builder or certifier and
does not consume their final Boolean.  Primitive rooted graphs and the rational
box data preserved in the frozen certificate determine the equality system.
All interval endpoints, inverses, residuals, and Neumann bounds below are exact
``fractions.Fraction`` values; there is no floating-point decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import os
import sys


# Exact certificates legitimately contain integers longer than Python's default
# defensive decimal-rendering limit.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
FROZEN = PROJECT / "input_frozen" / "k3p_cloud_artifacts"
SOURCE_CERT = FROZEN / "k3p_sharpness_krawczyk.json"
OUTPUT = HERE / "K3P_SHARPNESS_KRAWCZYK_CERTIFICATE.json"
DIM = 15
SECTORS = ("C", "G", "T")
CHARS = tuple((a, b, a ^ b) for a in range(4) for b in range(4))


def file_sha256(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def canonical_bytes(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def object_sha256(obj: object) -> str:
    return sha256(canonical_bytes(obj)).hexdigest()


def atomic_json(path: Path, obj: object) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q

    def __init__(self, lo: Q | int | str, hi: Q | int | str | None = None):
        a = Q(lo)
        b = a if hi is None else Q(hi)
        if a > b:
            raise ValueError(f"reversed interval: {a} > {b}")
        object.__setattr__(self, "lo", a)
        object.__setattr__(self, "hi", b)

    def __add__(self, other: object) -> "Interval":
        z = as_interval(other)
        return Interval(self.lo + z.lo, self.hi + z.hi)

    __radd__ = __add__

    def __neg__(self) -> "Interval":
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: object) -> "Interval":
        return self + (-as_interval(other))

    def __rsub__(self, other: object) -> "Interval":
        return as_interval(other) - self

    def __mul__(self, other: object) -> "Interval":
        z = as_interval(other)
        values = (self.lo * z.lo, self.lo * z.hi, self.hi * z.lo, self.hi * z.hi)
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def reciprocal(self) -> "Interval":
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError(f"interval contains zero: {self}")
        return Interval(1 / self.hi, 1 / self.lo)

    def __truediv__(self, other: object) -> "Interval":
        return self * as_interval(other).reciprocal()

    def max_abs(self) -> Q:
        return max(abs(self.lo), abs(self.hi))

    def contains_zero(self) -> bool:
        return self.lo <= 0 <= self.hi

    def strict_subset_of(self, other: "Interval") -> bool:
        return other.lo < self.lo and self.hi < other.hi

    def record(self) -> list[str]:
        return [str(self.lo), str(self.hi)]


def as_interval(value: object) -> Interval:
    return value if isinstance(value, Interval) else Interval(value)  # type: ignore[arg-type]


@dataclass(frozen=True)
class Dual:
    value: Interval
    deriv: tuple[Interval, ...]

    @staticmethod
    def constant(value: object, dim: int) -> "Dual":
        return Dual(as_interval(value), tuple(Interval(0) for _ in range(dim)))

    @staticmethod
    def variable(value: object, index: int, dim: int, scale: object = 1) -> "Dual":
        d = [Interval(0) for _ in range(dim)]
        d[index] = as_interval(scale)
        return Dual(as_interval(value), tuple(d))

    def __add__(self, other: object) -> "Dual":
        z = as_dual(other, len(self.deriv))
        return Dual(self.value + z.value, tuple(a + b for a, b in zip(self.deriv, z.deriv)))

    __radd__ = __add__

    def __neg__(self) -> "Dual":
        return Dual(-self.value, tuple(-x for x in self.deriv))

    def __sub__(self, other: object) -> "Dual":
        return self + (-as_dual(other, len(self.deriv)))

    def __rsub__(self, other: object) -> "Dual":
        return as_dual(other, len(self.deriv)) - self

    def __mul__(self, other: object) -> "Dual":
        z = as_dual(other, len(self.deriv))
        return Dual(
            self.value * z.value,
            tuple(a * z.value + self.value * b for a, b in zip(self.deriv, z.deriv)),
        )

    __rmul__ = __mul__


def as_dual(value: object, dim: int) -> Dual:
    return value if isinstance(value, Dual) else Dual.constant(value, dim)


@dataclass(frozen=True)
class NetworkSpec:
    name: str
    arcs: tuple[tuple[str, str], ...]
    retics: tuple[str, str]
    parent0: tuple[str, str]
    labels: tuple[tuple[str, int], ...]


W = NetworkSpec(
    "W",
    (("r", "S"), ("r", "L0"), ("S", "U"), ("S", "V"), ("U", "X"),
     ("V", "Z"), ("Z", "X"), ("U", "V"), ("Z", "L1"), ("X", "L2")),
    ("V", "X"),
    ("S", "Z"),
    (("L0", 0), ("L1", 1), ("L2", 2)),
)

WPRIME = NetworkSpec(
    "Wprime",
    (("r", "S"), ("r", "L0"), ("S", "U"), ("S", "X0"), ("V", "X0"),
     ("U", "X1"), ("V", "X1"), ("U", "V"), ("X0", "L1"), ("X1", "L2")),
    ("X0", "X1"),
    ("V", "V"),
    (("L0", 0), ("L1", 1), ("L2", 2)),
)


def topological_order(nodes: set[str], arcs: list[tuple[str, str]]) -> list[str]:
    indeg = {v: 0 for v in nodes}
    children = {v: [] for v in nodes}
    for u, v in arcs:
        indeg[v] += 1
        children[u].append(v)
    ready = sorted(v for v in nodes if indeg[v] == 0)
    order: list[str] = []
    while ready:
        u = ready.pop(0)
        order.append(u)
        for v in sorted(children[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
                ready.sort()
    if len(order) != len(nodes):
        raise AssertionError("primitive graph or switching is cyclic")
    return order


def build_map_terms(spec: NetworkSpec) -> tuple[tuple[tuple[tuple[int, ...], tuple[int, ...]], ...], ...]:
    """Build displayed-tree Fourier monomials from the primitive graph."""
    nodes = {x for arc in spec.arcs for x in arc}
    labels = dict(spec.labels)
    incoming = {r: [u for u, v in spec.arcs if v == r] for r in spec.retics}
    for r, ps in incoming.items():
        if len(ps) != 2:
            raise AssertionError((r, ps))
    outputs = []
    for chars in CHARS:
        coordinate_terms = []
        for bits in product((0, 1), repeat=2):
            selected = {
                r: (spec.parent0[j] if bits[j] else next(p for p in incoming[r] if p != spec.parent0[j]))
                for j, r in enumerate(spec.retics)
            }
            kept = [arc for arc in spec.arcs if arc[1] not in selected or arc[0] == selected[arc[1]]]
            children = {v: [] for v in nodes}
            for u, v in kept:
                children[u].append(v)
            descendant_mask: dict[str, int] = {}
            for v in reversed(topological_order(nodes, kept)):
                mask = (1 << labels[v]) if v in labels else 0
                for c in children[v]:
                    mask |= descendant_mask[c]
                descendant_mask[v] = mask
            factors = []
            for edge_index, arc in enumerate(spec.arcs):
                if arc not in kept:
                    continue
                mask = descendant_mask[arc[1]]
                sector = 0
                leaf_index = 0
                while mask:
                    if mask & 1:
                        sector ^= chars[leaf_index]
                    leaf_index += 1
                    mask >>= 1
                if sector:
                    factors.append(3 * edge_index + sector - 1)
            coordinate_terms.append((tuple(bits), tuple(factors)))
        outputs.append(tuple(coordinate_terms))
    return tuple(outputs)


MAP_TERMS = {W.name: build_map_terms(W), WPRIME.name: build_map_terms(WPRIME)}


def map_dual(spec: NetworkSpec, params: list[Dual]) -> list[Dual]:
    if len(params) != 32:
        raise AssertionError(len(params))
    dim = len(params[0].deriv)
    answer = []
    for terms in MAP_TERMS[spec.name]:
        value = Dual.constant(0, dim)
        for bits, factors in terms:
            term = Dual.constant(1, dim)
            for index in factors:
                term *= params[index]
            for j, bit in enumerate(bits):
                lam = params[30 + j]
                term *= lam if bit else (1 - lam)
            value += term
        answer.append(value)
    return answer


def matrix_inverse_and_det(matrix: list[list[Q]]) -> tuple[list[list[Q]], Q]:
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("matrix must be nonempty and square")
    aug = [row[:] + [Q(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    determinant = Q(1)
    for col in range(n):
        pivot = next((i for i in range(col, n) if aug[i][col]), None)
        if pivot is None:
            raise ZeroDivisionError(f"singular matrix at column {col}")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
            determinant = -determinant
        pv = aug[col][col]
        determinant *= pv
        aug[col] = [x / pv for x in aug[col]]
        for i in range(n):
            if i == col or not aug[i][col]:
                continue
            a = aug[i][col]
            aug[i] = [x - a * y for x, y in zip(aug[i], aug[col])]
    inverse = [row[n:] for row in aug]
    return inverse, determinant


def rank_and_pivot_columns(matrix: list[list[Q]]) -> tuple[int, list[int]]:
    a = [row[:] for row in matrix]
    m = len(a)
    n = len(a[0])
    row = 0
    pivots = []
    for col in range(n):
        pivot = next((i for i in range(row, m) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        pv = a[row][col]
        a[row] = [x / pv for x in a[row]]
        for i in range(m):
            if i != row and a[i][col]:
                c = a[i][col]
                a[i] = [x - c * y for x, y in zip(a[i], a[row])]
        pivots.append(col)
        row += 1
        if row == m:
            break
    return row, pivots


def interval_error_matrix(preconditioner: list[list[Q]], jacobian: list[list[Interval]]) -> list[list[Interval]]:
    n = len(preconditioner)
    return [
        [
            Interval(int(i == k))
            - sum((preconditioner[i][j] * jacobian[j][k] for j in range(n)), Interval(0))
            for k in range(n)
        ]
        for i in range(n)
    ]


def infinity_bound(matrix: list[list[Interval]]) -> Q:
    return max(sum((z.max_abs() for z in row), Q(0)) for row in matrix)


def matrix_record(matrix: list[list[Q | Interval]]) -> list[list[object]]:
    return [[z.record() if isinstance(z, Interval) else str(z) for z in row] for row in matrix]


ZERO_MONOMIAL = (0,) * DIM
Poly = dict[tuple[int, ...], Q]


def poly_add(a: Poly, b: Poly) -> Poly:
    out = dict(a)
    for monomial, coefficient in b.items():
        out[monomial] = out.get(monomial, Q(0)) + coefficient
        if not out[monomial]:
            del out[monomial]
    return out


def poly_scale(a: Poly, scale: Q) -> Poly:
    return {m: scale * c for m, c in a.items() if scale * c}


def poly_mul(a: Poly, b: Poly) -> Poly:
    out: Poly = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(x + y for x, y in zip(ma, mb))
            out[m] = out.get(m, Q(0)) + ca * cb
    return {m: c for m, c in out.items() if c}


def poly_one_minus(a: Poly) -> Poly:
    return poly_add({ZERO_MONOMIAL: Q(1)}, poly_scale(a, Q(-1)))


def map_polynomials(spec: NetworkSpec, params: list[Poly]) -> list[Poly]:
    answer = []
    for terms in MAP_TERMS[spec.name]:
        coordinate: Poly = {}
        for bits, factors in terms:
            term: Poly = {ZERO_MONOMIAL: Q(1)}
            for index in factors:
                term = poly_mul(term, params[index])
            for j, bit in enumerate(bits):
                term = poly_mul(term, params[30 + j] if bit else poly_one_minus(params[30 + j]))
            coordinate = poly_add(coordinate, term)
        answer.append(coordinate)
    return answer


def polynomial_record(poly: Poly) -> list[dict[str, object]]:
    records = []
    for monomial in sorted(poly):
        sparse_monomial = [[i, e] for i, e in enumerate(monomial) if e]
        records.append({"monomial": sparse_monomial, "coefficient": str(poly[monomial])})
    return records


def evaluate_poly_and_gradient(poly: Poly, point: list[Q]) -> tuple[Q, list[Q]]:
    value = Q(0)
    gradient = [Q(0) for _ in point]
    for monomial, coefficient in poly.items():
        term = coefficient
        for x, exponent in zip(point, monomial):
            term *= x ** exponent
        value += term
        for j, exponent in enumerate(monomial):
            if not exponent:
                continue
            d = coefficient * exponent
            for k, (x, e) in enumerate(zip(point, monomial)):
                d *= x ** (e - 1 if k == j else e)
            gradient[j] += d
    return value, gradient


def parameter_semantic(global_index: int) -> dict[str, object]:
    if not 0 <= global_index < 64:
        raise ValueError(global_index)
    side, local = (W, global_index) if global_index < 32 else (WPRIME, global_index - 32)
    if local < 30:
        edge_index, sector_index = divmod(local, 3)
        return {
            "global_index": global_index,
            "network": side.name,
            "local_index": local,
            "kind": "edge_eigenvalue",
            "edge_index": edge_index,
            "edge": list(side.arcs[edge_index]),
            "sector": SECTORS[sector_index],
        }
    retic_index = local - 30
    return {
        "global_index": global_index,
        "network": side.name,
        "local_index": local,
        "kind": "inheritance_probability",
        "reticulation": side.retics[retic_index],
        "parent0": side.parent0[retic_index],
    }


def direct_parameter_duals(
    centers: list[Q], pivots: list[int], y_center: list[Q], radius: Q, box: bool
) -> list[Dual]:
    pivot_map = {p: j for j, p in enumerate(pivots)}
    answer = []
    for i, center in enumerate(centers):
        if i not in pivot_map:
            answer.append(Dual.constant(center, DIM))
            continue
        j = pivot_map[i]
        y = Interval(y_center[j] - radius, y_center[j] + radius) if box else Interval(y_center[j])
        answer.append(Dual.variable(center * y, j, DIM, center))
    return answer


def equality_duals(
    centers: list[Q], pivots: list[int], y_center: list[Q], radius: Q, row_scales: list[Q], box: bool
) -> tuple[list[Dual], list[Dual]]:
    direct = direct_parameter_duals(centers, pivots, y_center, radius, box)
    qw = map_dual(W, direct[:32])
    qp = map_dual(WPRIME, direct[32:])
    equations = [row_scales[i] * (qw[i + 1] - qp[i + 1]) for i in range(DIM)]
    return equations, direct


def local_map_box(spec: NetworkSpec, direct_values: list[Interval]) -> tuple[list[Interval], list[list[Interval]]]:
    params = [Dual.variable(value, i, 32) for i, value in enumerate(direct_values)]
    outputs = map_dual(spec, params)[1:]
    return [z.value for z in outputs], [list(z.deriv) for z in outputs]


def physical_records(spec: NetworkSpec, values: list[Interval]) -> tuple[list[dict[str, object]], dict[str, object]]:
    records: list[dict[str, object]] = []

    def add(category: str, edge_index: int | None, label: str, interval: Interval) -> None:
        records.append({
            "category": category,
            "edge_index": edge_index,
            "edge": list(spec.arcs[edge_index]) if edge_index is not None else None,
            "expression": label,
            "interval": interval.record(),
            "strictly_positive": interval.lo > 0,
        })

    for edge_index in range(10):
        c, g, t = values[3 * edge_index: 3 * edge_index + 3]
        for sector, z in zip(SECTORS, (c, g, t)):
            add("edge_eigenvalue_lower", edge_index, sector, z)
            add("edge_eigenvalue_upper", edge_index, f"1-{sector}", 1 - z)
        add("transition_probability", edge_index, "p0=(1+C+G+T)/4", (1 + c + g + t) / 4)
        add("transition_probability", edge_index, "pC=(1+C-G-T)/4", (1 + c - g - t) / 4)
        add("transition_probability", edge_index, "pG=(1-C+G-T)/4", (1 - c + g - t) / 4)
        add("transition_probability", edge_index, "pT=(1-C-G+T)/4", (1 - c - g + t) / 4)
        add("strict_continuous_time", edge_index, "C-G*T", c - g * t)
        add("strict_continuous_time", edge_index, "G-C*T", g - c * t)
        add("strict_continuous_time", edge_index, "T-C*G", t - c * g)
    for j, lam in enumerate(values[30:]):
        records.append({
            "category": "inheritance_probability",
            "reticulation": spec.retics[j],
            "parent0": spec.parent0[j],
            "expression": "lambda",
            "interval": lam.record(),
            "strictly_positive": lam.lo > 0,
        })
        records.append({
            "category": "inheritance_probability",
            "reticulation": spec.retics[j],
            "parent0": spec.parent0[j],
            "expression": "1-lambda",
            "interval": (1 - lam).record(),
            "strictly_positive": (1 - lam).lo > 0,
        })
    failed = [r for r in records if not r["strictly_positive"]]
    minima: dict[str, dict[str, object]] = {}
    for category in sorted({str(r["category"]) for r in records}):
        candidates = [r for r in records if r["category"] == category]
        winner = min(candidates, key=lambda r: Q(r["interval"][0]))  # type: ignore[index]
        minima[category] = {
            "lower_bound": winner["interval"][0],  # type: ignore[index]
            "edge_index": winner.get("edge_index"),
            "expression": winner["expression"],
        }
    summary = {"all_strict": not failed, "failed_count": len(failed), "minimum_by_category": minima}
    return records, summary


def rank_certificate(
    spec: NetworkSpec,
    point_values: list[Q],
    box_values: list[Interval],
) -> dict[str, object]:
    _, point_jac_i = local_map_box(spec, [Interval(x) for x in point_values])
    _, box_jac = local_map_box(spec, box_values)
    point_jac = [[z.lo for z in row] for row in point_jac_i]
    rank, columns = rank_and_pivot_columns(point_jac)
    if rank != DIM:
        raise AssertionError(f"{spec.name} point rank is {rank}, not {DIM}")
    columns = columns[:DIM]
    point_minor = [[point_jac[i][j] for j in columns] for i in range(DIM)]
    box_minor = [[box_jac[i][j] for j in columns] for i in range(DIM)]
    inverse, determinant = matrix_inverse_and_det(point_minor)
    error = interval_error_matrix(inverse, box_minor)
    q = infinity_bound(error)
    if not q < 1:
        raise AssertionError(f"{spec.name} rank Neumann bound is not below one: {q}")
    return {
        "rank": rank,
        "selected_columns": columns,
        "selected_parameter_semantics": [parameter_semantic(j if spec is W else 32 + j) for j in columns],
        "point_determinant": str(determinant),
        "point_minor_matrix": matrix_record(point_minor),
        "point_inverse_preconditioner": matrix_record(inverse),
        "minor_interval_matrix": matrix_record(box_minor),
        "neumann_error_matrix": matrix_record(error),
        "neumann_infinity_bound": str(q),
        "uniformly_nonzero_on_box": q < 1,
        "proof": "If a selected minor A(y) were singular, A(y0)^(-1)A(y)=I-E would be singular; ||E||_infinity<1 makes I-E invertible by the Neumann lemma.",
    }


def main() -> int:
    frozen = json.loads(SOURCE_CERT.read_text(encoding="utf-8"))
    consumed_keys = (
        "center_rationals", "pivot_global_columns", "root_center_y", "box_radius",
        "row_scales", "edge_orders", "parameter_order",
    )
    missing = [key for key in consumed_keys if key not in frozen]
    if missing:
        raise AssertionError(f"frozen input missing keys: {missing}")
    centers = [Q(x) for x in frozen["center_rationals"]]
    pivots = [int(x) for x in frozen["pivot_global_columns"]]
    y_center = [Q(x) for x in frozen["root_center_y"]]
    radius = Q(frozen["box_radius"])
    row_scales = [Q(x) for x in frozen["row_scales"]]
    if not (len(centers) == 64 and len(pivots) == len(y_center) == len(row_scales) == DIM):
        raise AssertionError("unexpected rational data dimensions")
    if len(set(pivots)) != DIM or any(not 0 <= p < 64 for p in pivots) or radius <= 0:
        raise AssertionError("invalid pivot set or box radius")
    if frozen["edge_orders"] != {"W": [list(e) for e in W.arcs], "Wprime": [list(e) for e in WPRIME.arcs]}:
        raise AssertionError("frozen edge orders do not match independently encoded primitive graphs")

    point_equations, direct_point_dual = equality_duals(centers, pivots, y_center, radius, row_scales, False)
    box_equations, direct_box_dual = equality_duals(centers, pivots, y_center, radius, row_scales, True)
    f0 = [z.value.lo for z in point_equations]
    j0 = [[z.deriv[j].lo for j in range(DIM)] for z in point_equations]
    j_box = [list(z.deriv) for z in box_equations]
    preconditioner, det_j0 = matrix_inverse_and_det(j0)
    correction = [
        y_center[i] - sum((preconditioner[i][j] * f0[j] for j in range(DIM)), Q(0))
        for i in range(DIM)
    ]
    error = interval_error_matrix(preconditioner, j_box)
    contraction_q = infinity_bound(error)
    delta = Interval(-radius, radius)
    krawczyk = []
    for i in range(DIM):
        z = Interval(correction[i])
        for e in error[i]:
            z += e * delta
        krawczyk.append(z)
    box_intervals = [Interval(y - radius, y + radius) for y in y_center]
    inclusion_margins = [
        [str(krawczyk[i].lo - box_intervals[i].lo), str(box_intervals[i].hi - krawczyk[i].hi)]
        for i in range(DIM)
    ]
    strict_self_map = all(k.strict_subset_of(x) for k, x in zip(krawczyk, box_intervals))
    if not strict_self_map:
        raise AssertionError("Krawczyk operator is not a strict self-map")
    if not contraction_q < 1:
        raise AssertionError(f"preconditioned interval Jacobian bound is {contraction_q}")
    normalized_radius = max(
        max(abs(k.lo - y), abs(k.hi - y)) / radius for k, y in zip(krawczyk, y_center)
    )

    # Expand the same graph-derived system through an independent sparse-polynomial path.
    pivot_map = {p: j for j, p in enumerate(pivots)}
    direct_polys: list[Poly] = []
    for i, center in enumerate(centers):
        if i in pivot_map:
            exponent = [0] * DIM
            exponent[pivot_map[i]] = 1
            direct_polys.append({tuple(exponent): center})
        else:
            direct_polys.append({ZERO_MONOMIAL: center})
    qw_poly = map_polynomials(W, direct_polys[:32])
    qp_poly = map_polynomials(WPRIME, direct_polys[32:])
    equations_poly = [poly_scale(poly_add(qw_poly[i + 1], poly_scale(qp_poly[i + 1], Q(-1))), row_scales[i]) for i in range(DIM)]
    expanded_equations = [polynomial_record(p) for p in equations_poly]
    for i, poly in enumerate(equations_poly):
        value, gradient = evaluate_poly_and_gradient(poly, y_center)
        if value != f0[i] or gradient != j0[i]:
            raise AssertionError(f"expanded equality cross-check failed at row {i}")

    point_values = [z.value.lo for z in direct_point_dual]
    box_values = [z.value for z in direct_box_dual]
    w_rank = rank_certificate(W, point_values[:32], box_values[:32])
    wp_rank = rank_certificate(WPRIME, point_values[32:], box_values[32:])
    w_physical, w_physical_summary = physical_records(W, box_values[:32])
    wp_physical, wp_physical_summary = physical_records(WPRIME, box_values[32:])
    if not (w_physical_summary["all_strict"] and wp_physical_summary["all_strict"]):
        raise AssertionError("physical or continuous-time box inequality failed")

    qw_box = map_dual(W, direct_box_dual[:32])[1:]
    qp_box = map_dual(WPRIME, direct_box_dual[32:])[1:]
    common_enclosures = []
    for char, a, b in zip(CHARS[1:], qw_box, qp_box):
        intersection = Interval(max(a.value.lo, b.value.lo), min(a.value.hi, b.value.hi))
        common_enclosures.append({
            "character": list(char),
            "W": a.value.record(),
            "Wprime": b.value.record(),
            "intersection": intersection.record(),
        })

    free_parameters = []
    for i, value in enumerate(centers):
        if i not in pivot_map:
            entry = parameter_semantic(i)
            entry["frozen_value"] = str(value)
            free_parameters.append(entry)
    pivot_parameters = []
    for j, i in enumerate(pivots):
        entry = parameter_semantic(i)
        entry.update({
            "scaled_variable_index": j,
            "multiplicative_scale": str(centers[i]),
            "y_center": str(y_center[j]),
            "y_interval": box_intervals[j].record(),
            "direct_parameter_interval": box_values[i].record(),
        })
        pivot_parameters.append(entry)

    provenance_paths = [
        SOURCE_CERT,
        FROZEN / "sharpness_exact_maps.py",
        FROZEN / "certify_sharpness_krawczyk.py",
        FROZEN / "k3p_sharpness_ift_base.json",
        FROZEN / "k3p_sharpness_all_n.json",
        FROZEN / "k3p_rooting_censuses.json",
    ]
    provenance = {
        "frozen_inputs": [
            {"path": str(p.relative_to(PROJECT)), "bytes": p.stat().st_size, "sha256": file_sha256(p)}
            for p in provenance_paths
        ],
        "independent_verifier": {
            "path": str(Path(__file__).resolve().relative_to(PROJECT)),
            "bytes": Path(__file__).stat().st_size,
            "sha256": file_sha256(Path(__file__)),
            "python": sys.version,
            "dependencies": ["Python standard library only"],
        },
        "consumed_source_certificate_keys": list(consumed_keys),
        "explicitly_ignored_source_certificate_keys": sorted(set(frozen) - set(consumed_keys)),
        "missing_cloud_intermediate": "sharpness_relative_root.json is referenced by the cloud certifier but absent from input_frozen; all needed rational data were recovered from the frozen final certificate.",
    }
    all_pass = bool(
        strict_self_map and contraction_q < 1
        and w_rank["uniformly_nonzero_on_box"] and wp_rank["uniformly_nonzero_on_box"]
        and w_physical_summary["all_strict"] and wp_physical_summary["all_strict"]
    )
    certificate = {
        "schema": "k3p-sharpness-independent-exact-krawczyk-v2",
        "arithmetic": "exact rational closed intervals; Fraction operations are algebraically outward because endpoints are exact",
        "provenance": provenance,
        "primitive_networks": {
            W.name: {"arcs": [list(e) for e in W.arcs], "reticulations": list(W.retics), "parent0": list(W.parent0), "labels": [list(x) for x in W.labels]},
            WPRIME.name: {"arcs": [list(e) for e in WPRIME.arcs], "reticulations": list(WPRIME.retics), "parent0": list(WPRIME.parent0), "labels": [list(x) for x in WPRIME.labels]},
        },
        "map_term_sha256": {name: object_sha256(terms) for name, terms in MAP_TERMS.items()},
        "parameterization": {
            "direct_parameter_count": 64,
            "scaled_variable_count": DIM,
            "multiplicative_scales_for_pivots_and_values_for_frozen_parameters": [str(x) for x in centers],
            "direct_parameter_point": [str(x) for x in point_values],
            "direct_parameter_box": [x.record() for x in box_values],
            "pivot_global_columns": pivots,
            "pivot_parameters": pivot_parameters,
            "frozen_free_parameter_count": len(free_parameters),
            "frozen_free_parameters": free_parameters,
            "scaled_variable_center": [str(x) for x in y_center],
            "box_radius": str(radius),
            "box": [x.record() for x in box_intervals],
            "row_scales": [str(x) for x in row_scales],
        },
        "equality_system": {
            "output_order": [list(x) for x in CHARS[1:]],
            "definition": "F_i(y)=row_scale_i*(q_i(W;x_W(y))-q_i(Wprime;x_Wprime(y))), for the 15 nonconstant zero-sum K3P Fourier coordinates",
            "expanded_sparse_polynomials": expanded_equations,
            "expanded_sparse_polynomials_sha256": object_sha256(expanded_equations),
            "exact_center_residual": [str(x) for x in f0],
            "point_jacobian": matrix_record(j0),
            "point_jacobian_determinant": str(det_j0),
            "interval_jacobian": matrix_record(j_box),
        },
        "krawczyk": {
            "preconditioner_exact_inverse_of_point_jacobian": matrix_record(preconditioner),
            "corrected_center_term_y0_minus_YF0": [str(x) for x in correction],
            "error_matrix_I_minus_Y_J_box": matrix_record(error),
            "preconditioned_interval_jacobian_infinity_bound": str(contraction_q),
            "operator_intervals": [x.record() for x in krawczyk],
            "strict_inclusion_margins_left_right": inclusion_margins,
            "max_normalized_distance_from_box_center": str(normalized_radius),
            "strict_self_map": strict_self_map,
            "existence": strict_self_map,
            "uniqueness_in_box": strict_self_map and contraction_q < 1,
            "uniqueness_reason": "The strict Krawczyk inclusion gives a zero. The infinity bound below one makes every mean Jacobian on the convex box invertible, hence two distinct zeros cannot occur.",
        },
        "rank_15_minors": {W.name: w_rank, WPRIME.name: wp_rank},
        "physical_strict_continuous_time": {
            W.name: {"records": w_physical, "summary": w_physical_summary},
            WPRIME.name: {"records": wp_physical, "summary": wp_physical_summary},
        },
        "common_tensor_enclosures": common_enclosures,
        "conclusion": {
            "all_checks_pass": all_pass,
            "unique_common_parameter_root_in_box": strict_self_map and contraction_q < 1,
            "W_rank_15_throughout_box": w_rank["uniformly_nonzero_on_box"],
            "Wprime_rank_15_throughout_box": wp_rank["uniformly_nonzero_on_box"],
            "principal_K3P_domain_throughout_box": w_physical_summary["all_strict"] and wp_physical_summary["all_strict"],
            "strict_continuous_time_throughout_box": w_physical_summary["all_strict"] and wp_physical_summary["all_strict"],
            "local_geometric_consequence": "At the certified common tensor both 15-dimensional normalized maps are submersions into the 15-dimensional three-leaf Fourier space, so their images contain a common ambient-open regular germ.",
        },
    }
    if not all_pass:
        raise AssertionError("not all independently derived sharpness checks passed")
    atomic_json(OUTPUT, certificate)
    print(f"INDEPENDENT_K3P_KRAWCZYK_PASS {OUTPUT}")
    print(f"certificate_sha256={file_sha256(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
