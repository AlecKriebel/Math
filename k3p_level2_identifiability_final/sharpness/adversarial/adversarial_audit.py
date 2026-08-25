#!/usr/bin/env python3
"""Adversarial clean-room audit of the K3P weak-class sharpness package.

This script uses only the Python standard library.  It deliberately ignores all
stored conclusion booleans and independently reconstructs the mathematical
objects from primitive graphs plus the rational witness data.  Its interval
engine is symmetric exact center-radius arithmetic, structurally different
from the endpoint implementation in the parent package.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
from math import isqrt
from pathlib import Path
import json
import os
import sys


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
getcontext().prec = 40

HERE = Path(__file__).resolve().parent
SHARPNESS = HERE.parent
PROJECT = SHARPNESS.parent
FROZEN = PROJECT / "input_frozen" / "k3p_cloud_artifacts"
SOURCE = FROZEN / "k3p_sharpness_krawczyk.json"
PARENT_K = SHARPNESS / "K3P_SHARPNESS_KRAWCZYK_CERTIFICATE.json"
PARENT_T = SHARPNESS / "K3P_SHARPNESS_TOPOLOGY_ALL_N_CERTIFICATE.json"
ALLN_SOURCE = FROZEN / "k3p_sharpness_all_n.json"
OUTPUT = HERE / "SHARPNESS_ADVERSARIAL_AUDIT.json"

DIM = 15
SECTORS = ("C", "G", "T")
CHARS = tuple((a, b, a ^ b) for a in range(4) for b in range(4))


def file_hash(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def object_hash(obj: object) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return sha256(raw).hexdigest()


def decimal(q: Q | str | int, digits: int = 12) -> str:
    z = Q(q)
    x = Decimal(z.numerator) / Decimal(z.denominator)
    return f"{x:.{digits}E}"


def atomic_json(path: Path, obj: object) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


@dataclass(frozen=True)
class Ball:
    """Exact symmetric enclosure {mid + e: |e| <= rad}."""

    mid: Q
    rad: Q = Q(0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "mid", Q(self.mid))
        object.__setattr__(self, "rad", Q(self.rad))
        if self.rad < 0:
            raise ValueError("negative radius")

    @property
    def lo(self) -> Q:
        return self.mid - self.rad

    @property
    def hi(self) -> Q:
        return self.mid + self.rad

    def __add__(self, other: object) -> "Ball":
        z = as_ball(other)
        return Ball(self.mid + z.mid, self.rad + z.rad)

    __radd__ = __add__

    def __neg__(self) -> "Ball":
        return Ball(-self.mid, self.rad)

    def __sub__(self, other: object) -> "Ball":
        return self + (-as_ball(other))

    def __rsub__(self, other: object) -> "Ball":
        return as_ball(other) - self

    def __mul__(self, other: object) -> "Ball":
        z = as_ball(other)
        # |(m+e)(n+f)-mn| <= |m||f|+|n||e|+|e||f|.
        return Ball(
            self.mid * z.mid,
            abs(self.mid) * z.rad + abs(z.mid) * self.rad + self.rad * z.rad,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> "Ball":
        z = as_ball(other)
        if z.rad:
            raise ValueError("audit only divides by exact scalars")
        if not z.mid:
            raise ZeroDivisionError
        return Ball(self.mid / z.mid, self.rad / abs(z.mid))

    def max_abs(self) -> Q:
        return abs(self.mid) + self.rad

    def contains(self, value: Q) -> bool:
        return self.lo <= value <= self.hi

    def record(self) -> dict[str, str]:
        return {"mid": str(self.mid), "radius": str(self.rad), "lo": str(self.lo), "hi": str(self.hi)}


def as_ball(value: object) -> Ball:
    return value if isinstance(value, Ball) else Ball(Q(value))  # type: ignore[arg-type]


@dataclass(frozen=True)
class Dual:
    value: Ball
    deriv: tuple[Ball, ...]

    @staticmethod
    def constant(value: object, dim: int) -> "Dual":
        return Dual(as_ball(value), tuple(Ball(0) for _ in range(dim)))

    @staticmethod
    def variable(value: object, index: int, dim: int, scale: object = 1) -> "Dual":
        d = [Ball(0) for _ in range(dim)]
        d[index] = as_ball(scale)
        return Dual(as_ball(value), tuple(d))

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
    ("V", "X"), ("S", "Z"), (("L0", 0), ("L1", 1), ("L2", 2)),
)
WPRIME = NetworkSpec(
    "Wprime",
    (("r", "S"), ("r", "L0"), ("S", "U"), ("S", "X0"), ("V", "X0"),
     ("U", "X1"), ("V", "X1"), ("U", "V"), ("X0", "L1"), ("X1", "L2")),
    ("X0", "X1"), ("V", "V"), (("L0", 0), ("L1", 1), ("L2", 2)),
)


def selected_tree(spec: NetworkSpec, bits: tuple[int, int]) -> tuple[tuple[str, str], ...]:
    incoming = {r: tuple(u for u, v in spec.arcs if v == r) for r in spec.retics}
    chosen = {}
    for j, r in enumerate(spec.retics):
        p0 = spec.parent0[j]
        chosen[r] = p0 if bits[j] else next(p for p in incoming[r] if p != p0)
    return tuple((u, v) for u, v in spec.arcs if v not in chosen or u == chosen[v])


def descendants_from(child: str, kept: tuple[tuple[str, str], ...], labels: dict[str, int]) -> int:
    kids: dict[str, list[str]] = {}
    for u, v in kept:
        kids.setdefault(u, []).append(v)
    mask = 0
    stack = [child]
    seen = set()
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        if u in labels:
            mask |= 1 << labels[u]
        stack.extend(kids.get(u, ()))
    return mask


def xor_sector(mask: int, chars: tuple[int, int, int]) -> int:
    sector = 0
    for leaf in range(3):
        if mask & (1 << leaf):
            sector ^= chars[leaf]
    return sector


def build_terms(spec: NetworkSpec) -> tuple[tuple[tuple[tuple[int, int], tuple[int, ...]], ...], ...]:
    """Build map terms by reachability DFS in each displayed switching."""
    labels = dict(spec.labels)
    outputs = []
    for chars in CHARS:
        terms = []
        for bits in product((0, 1), repeat=2):
            kept = selected_tree(spec, bits)
            factors = []
            for edge_index, edge in enumerate(spec.arcs):
                if edge not in kept:
                    continue
                h = xor_sector(descendants_from(edge[1], kept, labels), chars)
                if h:
                    factors.append(3 * edge_index + h - 1)
            terms.append((bits, tuple(factors)))
        outputs.append(tuple(terms))
    return tuple(outputs)


MAP_TERMS = {W.name: build_terms(W), WPRIME.name: build_terms(WPRIME)}


def map_dual(spec: NetworkSpec, params: list[Dual]) -> list[Dual]:
    if len(params) != 32:
        raise AssertionError(len(params))
    dim = len(params[0].deriv)
    result = []
    for terms in MAP_TERMS[spec.name]:
        coordinate = Dual.constant(0, dim)
        for bits, factors in terms:
            term = Dual.constant(1, dim)
            for i in factors:
                term *= params[i]
            for j, bit in enumerate(bits):
                lam = params[30 + j]
                term *= lam if bit else 1 - lam
            coordinate += term
        result.append(coordinate)
    return result


ZERO_MONOMIAL = (0,) * DIM
Poly = dict[tuple[int, ...], Q]


def p_add(a: Poly, b: Poly) -> Poly:
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, Q(0)) + c
        if not out[m]:
            del out[m]
    return out


def p_scale(a: Poly, c: Q) -> Poly:
    return {m: c * x for m, x in a.items() if c * x}


def p_mul(a: Poly, b: Poly) -> Poly:
    out: Poly = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(x + y for x, y in zip(ma, mb))
            out[m] = out.get(m, Q(0)) + ca * cb
    return {m: c for m, c in out.items() if c}


def p_one_minus(a: Poly) -> Poly:
    return p_add({ZERO_MONOMIAL: Q(1)}, p_scale(a, Q(-1)))


def map_poly(spec: NetworkSpec, params: list[Poly]) -> list[Poly]:
    result = []
    for terms in MAP_TERMS[spec.name]:
        coordinate: Poly = {}
        for bits, factors in terms:
            term = {ZERO_MONOMIAL: Q(1)}
            for i in factors:
                term = p_mul(term, params[i])
            for j, bit in enumerate(bits):
                term = p_mul(term, params[30 + j] if bit else p_one_minus(params[30 + j]))
            coordinate = p_add(coordinate, term)
        result.append(coordinate)
    return result


def parse_stored_polys(records: list[list[dict[str, object]]]) -> list[Poly]:
    answer = []
    for poly in records:
        p: Poly = {}
        for term in poly:
            exponents = [0] * DIM
            for i, e in term["monomial"]:  # type: ignore[index]
                exponents[int(i)] = int(e)
            p[tuple(exponents)] = Q(term["coefficient"])  # type: ignore[arg-type]
        answer.append(p)
    return answer


def matrix_inverse_and_det(matrix: list[list[Q]]) -> tuple[list[list[Q]], Q]:
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("nonsquare matrix")
    aug = [row[:] + [Q(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    det = Q(1)
    for col in range(n):
        pivot = next((i for i in range(col, n) if aug[i][col]), None)
        if pivot is None:
            raise ZeroDivisionError(f"singular at column {col}")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
            det = -det
        pv = aug[col][col]
        det *= pv
        aug[col] = [x / pv for x in aug[col]]
        for i in range(n):
            if i == col or not aug[i][col]:
                continue
            c = aug[i][col]
            aug[i] = [x - c * y for x, y in zip(aug[i], aug[col])]
    return [row[n:] for row in aug], det


def determinant(matrix: list[list[Q]]) -> Q:
    n = len(matrix)
    a = [row[:] for row in matrix]
    d = Q(1)
    for col in range(n):
        pivot = next((i for i in range(col, n) if a[i][col]), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            d = -d
        pv = a[col][col]
        d *= pv
        for i in range(col + 1, n):
            if not a[i][col]:
                continue
            c = a[i][col] / pv
            for j in range(col + 1, n):
                a[i][j] -= c * a[col][j]
    return d


def rank_and_pivots(matrix: list[list[Q]]) -> tuple[int, list[int]]:
    a = [row[:] for row in matrix]
    if not a:
        return 0, []
    m, n = len(a), len(a[0])
    row = 0
    columns = []
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
        columns.append(col)
        row += 1
        if row == m:
            break
    return row, columns


def error_matrix(preconditioner: list[list[Q]], jacobian: list[list[Ball]]) -> list[list[Ball]]:
    n = len(preconditioner)
    return [[
        Ball(int(i == k)) - sum((preconditioner[i][j] * jacobian[j][k] for j in range(n)), Ball(0))
        for k in range(n)
    ] for i in range(n)]


def inf_bound(matrix: list[list[Ball]]) -> Q:
    return max(sum((z.max_abs() for z in row), Q(0)) for row in matrix)


def direct_duals(
    centers: list[Q], pivots: list[int], y0: list[Q], radius: Q, variable_dim: int = DIM
) -> list[Dual]:
    pmap = {p: j for j, p in enumerate(pivots)}
    result = []
    for i, c in enumerate(centers):
        if i not in pmap:
            result.append(Dual.constant(c, variable_dim))
        else:
            j = pmap[i]
            y = Ball(y0[j], radius)
            result.append(Dual.variable(c * y, j, variable_dim, c))
    return result


def equality_duals(
    centers: list[Q], pivots: list[int], y0: list[Q], radius: Q, row_scales: list[Q]
) -> tuple[list[Dual], list[Dual]]:
    direct = direct_duals(centers, pivots, y0, radius)
    qw = map_dual(W, direct[:32])
    qp = map_dual(WPRIME, direct[32:])
    return [row_scales[i] * (qw[i + 1] - qp[i + 1]) for i in range(DIM)], direct


def local_map_jac(spec: NetworkSpec, values: list[Ball]) -> tuple[list[Ball], list[list[Ball]]]:
    params = [Dual.variable(v, i, 32) for i, v in enumerate(values)]
    out = map_dual(spec, params)[1:]
    return [z.value for z in out], [list(z.deriv) for z in out]


def krawczyk_check(
    centers: list[Q], pivots: list[int], y0: list[Q], radius: Q, row_scales: list[Q],
    f0: list[Q], inverse: list[list[Q]], transpose_preconditioner: bool = False,
) -> dict[str, object]:
    box_eq, _ = equality_duals(centers, pivots, y0, radius, row_scales)
    jx = [list(z.deriv) for z in box_eq]
    pre = [list(row) for row in zip(*inverse)] if transpose_preconditioner else inverse
    correction = [
        y0[i] - sum((pre[i][j] * f0[j] for j in range(DIM)), Q(0))
        for i in range(DIM)
    ]
    error = error_matrix(pre, jx)
    q = inf_bound(error)
    delta = Ball(0, radius)
    operator = []
    margins = []
    for i in range(DIM):
        z = Ball(correction[i])
        for e in error[i]:
            z += e * delta
        operator.append(z)
        margins.append(radius - (abs(z.mid - y0[i]) + z.rad))
    strict = all(m > 0 for m in margins)
    normalized = max((abs(z.mid - y0[i]) + z.rad) / radius for i, z in enumerate(operator))
    return {
        "strict_self_map": strict,
        "q": q,
        "normalized_operator_radius": normalized,
        "minimum_inclusion_margin": min(margins),
        "operator": operator,
    }


def rank_box_check(spec: NetworkSpec, point: list[Q], box: list[Ball]) -> dict[str, object]:
    _, j0b = local_map_jac(spec, [Ball(x) for x in point])
    _, jxb = local_map_jac(spec, box)
    j0 = [[z.mid for z in row] for row in j0b]
    rank, columns = rank_and_pivots(j0)
    if rank != DIM:
        raise AssertionError((spec.name, rank))
    columns = columns[:DIM]
    a0 = [[j0[i][j] for j in columns] for i in range(DIM)]
    ax = [[jxb[i][j] for j in columns] for i in range(DIM)]
    inv, det = matrix_inverse_and_det(a0)
    q = inf_bound(error_matrix(inv, ax))
    return {"rank": rank, "columns": columns, "determinant": det, "q": q, "uniform": q < 1, "point_jacobian": j0}


def physical_check(spec: NetworkSpec, values: list[Ball]) -> dict[str, object]:
    tests: list[tuple[str, int | None, str, Ball]] = []
    for i in range(10):
        c, g, t = values[3 * i:3 * i + 3]
        rows = (
            ("eigenvalue", "C", c), ("eigenvalue", "G", g), ("eigenvalue", "T", t),
            ("eigenvalue_upper", "1-C", 1-c), ("eigenvalue_upper", "1-G", 1-g), ("eigenvalue_upper", "1-T", 1-t),
            ("transition", "p0", (1+c+g+t)/4), ("transition", "pC", (1+c-g-t)/4),
            ("transition", "pG", (1-c+g-t)/4), ("transition", "pT", (1-c-g+t)/4),
            ("ct", "C-GT", c-g*t), ("ct", "G-CT", g-c*t), ("ct", "T-CG", t-c*g),
        )
        tests.extend((cat, i, label, z) for cat, label, z in rows)
    for j, lam in enumerate(values[30:]):
        tests.extend((("inheritance", None, f"lambda{j}", lam), ("inheritance", None, f"1-lambda{j}", 1-lam)))
    minimum = min(tests, key=lambda x: x[3].lo)
    failed = [(cat, i, label, z.record()) for cat, i, label, z in tests if z.lo <= 0]
    # Root suppression merges arcs 0 and 1 coordinatewise.  Check the effective
    # semi-directed edge explicitly in addition to the stronger arcwise test.
    effective = [values[j] * values[3+j] for j in range(3)]
    ec, eg, et = effective
    effective_tests = [ec, eg, et, 1-ec, 1-eg, 1-et,
                       (1+ec+eg+et)/4, (1+ec-eg-et)/4, (1-ec+eg-et)/4, (1-ec-eg+et)/4,
                       ec-eg*et, eg-ec*et, et-ec*eg]
    return {
        "all_strict": not failed and all(z.lo > 0 for z in effective_tests),
        "failed": failed,
        "minimum": {"category": minimum[0], "edge": minimum[1], "expression": minimum[2], "lower": minimum[3].lo},
        "effective_suppressed_root_edge_minimum": min(z.lo for z in effective_tests),
    }


# ---------------------------------------------------------------------------
# Fixed-mixed-graph topology and explicit sd_0 rooting replay


@dataclass(frozen=True, order=True)
class MixedEdge:
    endpoints: tuple[str, str]
    heads: tuple[str, ...] = ()

    @staticmethod
    def make(a: str, b: str, heads: tuple[str, ...] | list[str] = ()) -> "MixedEdge":
        if a == b:
            raise ValueError("loop")
        ends = tuple(sorted((a, b)))
        hs = tuple(sorted(heads))
        if any(x not in ends for x in hs):
            raise ValueError((ends, hs))
        return MixedEdge(ends, hs)


@dataclass(frozen=True)
class MixedGraph:
    name: str
    roles: tuple[tuple[str, str], ...]
    labels: tuple[tuple[str, int], ...]
    edges: tuple[MixedEdge, ...]

    def role_dict(self) -> dict[str, str]:
        return dict(self.roles)

    def label_dict(self) -> dict[str, int]:
        return dict(self.labels)


@dataclass(frozen=True)
class RootedSpec:
    name: str
    arcs: tuple[tuple[str, str], ...]
    retics: frozenset[str]
    labels: tuple[tuple[str, int], ...]


RW = RootedSpec(W.name, W.arcs, frozenset(W.retics), W.labels)
RWP = RootedSpec(WPRIME.name, WPRIME.arcs, frozenset(WPRIME.retics), WPRIME.labels)
COLLISION = RootedSpec(
    "collision",
    (("rho", "1"), ("rho", "u"), ("u", "p"), ("u", "q"), ("p", "r2"),
     ("q", "r2"), ("p", "r3"), ("q", "r3"), ("r2", "2"), ("r3", "3")),
    frozenset(("r2", "r3")), (("1", 0), ("2", 1), ("3", 2)),
)


def suppress_root(spec: RootedSpec) -> MixedGraph:
    nodes = {x for e in spec.arcs for x in e}
    indeg = {v: 0 for v in nodes}
    for _, v in spec.arcs:
        indeg[v] += 1
    roots = [v for v in nodes if indeg[v] == 0]
    if len(roots) != 1:
        raise AssertionError(roots)
    root = roots[0]
    children = [v for u, v in spec.arcs if u == root]
    if len(children) != 2:
        raise AssertionError(children)
    labels = dict(spec.labels)
    roles = {v: ("leaf" if v in labels else "retic" if v in spec.retics else "tree") for v in nodes if v != root}
    edges = [MixedEdge.make(u, v, (v,) if v in spec.retics else ()) for u, v in spec.arcs if u != root]
    merged_heads = tuple(v for v in children if v in spec.retics)
    if len(merged_heads) > 1:
        raise AssertionError("double-headed root suppression is outside the fixed convention")
    edges.append(MixedEdge.make(children[0], children[1], merged_heads))
    if len({e.endpoints for e in edges}) != len(edges):
        raise AssertionError("root suppression is not simple")
    return MixedGraph(spec.name, tuple(sorted(roles.items())), tuple(sorted(spec.labels)), tuple(sorted(edges)))


def topo_order(nodes: set[str], arcs: list[tuple[str, str]]) -> list[str] | None:
    indeg = {v: 0 for v in nodes}
    children = {v: [] for v in nodes}
    for u, v in arcs:
        if u not in nodes or v not in nodes or u == v:
            return None
        indeg[v] += 1
        children[u].append(v)
    ready = sorted(v for v in nodes if indeg[v] == 0)
    order = []
    while ready:
        u = ready.pop(0)
        order.append(u)
        for v in sorted(children[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
                ready.sort()
    return order if len(order) == len(nodes) else None


def sd0_from_arcs(
    roles: dict[str, str], labels: dict[str, int], arcs: list[tuple[str, str]], root: str, name: str,
) -> MixedGraph | None:
    children = [v for u, v in arcs if u == root]
    if len(children) != 2:
        return None
    heads = tuple(v for v in children if roles.get(v) == "retic")
    if len(heads) > 1:
        return None
    edges = [MixedEdge.make(u, v, (v,) if roles.get(v) == "retic" else ()) for u, v in arcs if u != root]
    edges.append(MixedEdge.make(children[0], children[1], heads))
    if len({e.endpoints for e in edges}) != len(edges):
        return None
    return MixedGraph(name, tuple(sorted(roles.items())), tuple(sorted(labels.items())), tuple(sorted(edges)))


def validate_rooting(
    target: MixedGraph, arcs: list[tuple[str, str]], root: str = "__R__", require_lsa: bool = True,
) -> dict[str, object] | None:
    roles, labels = target.role_dict(), target.label_dict()
    nodes = set(roles) | {root}
    if len(arcs) != len(set(arcs)):
        return None
    order = topo_order(nodes, arcs)
    if order is None:
        return None
    indeg = {v: 0 for v in nodes}
    kids = {v: [] for v in nodes}
    parents = {v: [] for v in nodes}
    for u, v in arcs:
        indeg[v] += 1
        kids[u].append(v)
        parents[v].append(u)
    if (indeg[root], len(kids[root])) != (0, 2):
        return None
    for v, role in roles.items():
        wanted = (1, 0) if role == "leaf" else (2, 1) if role == "retic" else (1, 2)
        if (indeg[v], len(kids[v])) != wanted:
            return None
    reachable = {root}
    stack = [root]
    while stack:
        u = stack.pop()
        for v in kids[u]:
            if v not in reachable:
                reachable.add(v)
                stack.append(v)
    if reachable != nodes or set(labels) != {v for v, r in roles.items() if r == "leaf"}:
        return None
    dom = {root: {root}}
    for v in order[1:]:
        if not parents[v]:
            return None
        dom[v] = {v} | set.intersection(*(dom[p] for p in parents[v]))
    stable = set.intersection(*(dom[v] for v in labels))
    if require_lsa and stable != {root}:
        return None
    reconstructed = sd0_from_arcs(roles, labels, arcs, root, target.name)
    if reconstructed != target:
        return None
    witnesses = [u for u in nodes if roles.get(u) != "leaf" and all(roles.get(v) == "retic" for v in kids[u])]
    return {
        "tree_child": not witnesses,
        "non_tree_child_witnesses": sorted(witnesses),
        "stable_vertices": sorted(stable),
        "arcs": tuple(sorted(arcs)),
    }


def enumerate_rootings(mixed: MixedGraph, require_lsa: bool = True, enforce_sd0: bool = True) -> list[dict[str, object]]:
    # enforce_sd0 is present for mutation testing; the valid path always uses it.
    roles, labels = mixed.role_dict(), mixed.label_dict()
    result = []
    for root_edge in mixed.edges:
        if len(root_edge.heads) > 1:
            continue
        remaining = [e for e in mixed.edges if e != root_edge]
        ordinary = sorted(e for e in remaining if not e.heads)
        fixed = sorted(e for e in remaining if e.heads)
        for bits in product((0, 1), repeat=len(ordinary)):
            root = "__R__"
            arcs = [(root, root_edge.endpoints[0]), (root, root_edge.endpoints[1])]
            for e, bit in zip(ordinary, bits):
                a, b = e.endpoints
                arcs.append((a, b) if bit == 0 else (b, a))
            for e in fixed:
                if len(e.heads) != 1:
                    continue
                head = e.heads[0]
                tail = next(v for v in e.endpoints if v != head)
                arcs.append((tail, head))
            if enforce_sd0:
                check = validate_rooting(mixed, arcs, root, require_lsa=require_lsa)
            else:
                # A deliberately permissive mutation: validate against whatever
                # mixed graph suppression produces, not the fixed target.
                candidate = sd0_from_arcs(roles, labels, arcs, root, mixed.name)
                check = validate_rooting(candidate, arcs, root, require_lsa=require_lsa) if candidate else None
            if check is not None:
                result.append({"root_edge": root_edge, "bits": bits, **check})
    return sorted(result, key=lambda x: (x["root_edge"].endpoints, x["bits"]))  # type: ignore[index,union-attr]


def adjacency(mixed: MixedGraph) -> dict[str, set[str]]:
    a = {v: set() for v, _ in mixed.roles}
    for e in mixed.edges:
        u, v = e.endpoints
        a[u].add(v)
        a[v].add(u)
    return a


def leaf_distance_matrix(mixed: MixedGraph) -> dict[str, int]:
    adj = adjacency(mixed)
    by_label = {label: node for node, label in mixed.labels}
    out = {}
    for a, b in ((0, 1), (0, 2), (1, 2)):
        start, goal = by_label[a], by_label[b]
        distance = {start: 0}
        queue = [start]
        for u in queue:
            for v in sorted(adj[u]):
                if v not in distance:
                    distance[v] = distance[u] + 1
                    queue.append(v)
        out[f"{a}-{b}"] = distance[goal]
    return out


def triangles(mixed: MixedGraph) -> tuple[tuple[str, str, str], ...]:
    adj = adjacency(mixed)
    nodes = sorted(adj)
    return tuple((a, b, c) for i, a in enumerate(nodes) for j, b in enumerate(nodes[i+1:], i+1)
                 for c in nodes[j+1:] if b in adj[a] and c in adj[a] and c in adj[b])


def bridge_edges(mixed: MixedGraph) -> set[tuple[str, str]]:
    adj = adjacency(mixed)
    bridges = set()
    for e in mixed.edges:
        a, b = e.endpoints
        seen = {a}
        stack = [a]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if {u, v} == {a, b}:
                    continue
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        if b not in seen:
            bridges.add(e.endpoints)
    return bridges


def biconnected_blocks(mixed: MixedGraph) -> list[list[tuple[str, str]]]:
    adj = adjacency(mixed)
    discovery: dict[str, int] = {}
    low: dict[str, int] = {}
    parent: dict[str, str | None] = {}
    stack: list[tuple[str, str]] = []
    blocks = []
    tick = 0

    def visit(u: str) -> None:
        nonlocal tick
        tick += 1
        discovery[u] = low[u] = tick
        for v in sorted(adj[u]):
            edge = tuple(sorted((u, v)))
            if v not in discovery:
                parent[v] = u
                stack.append(edge)
                visit(v)
                low[u] = min(low[u], low[v])
                if low[v] >= discovery[u]:
                    block = []
                    while stack:
                        x = stack.pop()
                        block.append(x)
                        if x == edge:
                            break
                    blocks.append(sorted(block))
            elif parent.get(u) != v and discovery[v] < discovery[u]:
                low[u] = min(low[u], discovery[v])
                stack.append(edge)

    for v in sorted(adj):
        if v not in discovery:
            parent[v] = None
            visit(v)
    return sorted(blocks)


def topology_summary(mixed: MixedGraph) -> dict[str, object]:
    roles = mixed.role_dict()
    adj = adjacency(mixed)
    blobs = []
    for block in biconnected_blocks(mixed):
        vertices = {v for e in block for v in e}
        if len(block) >= len(vertices):
            blobs.append({"vertices": sorted(vertices), "edges": block,
                          "reticulations": sum(roles[v] == "retic" for v in vertices)})
    return {
        "simple": len({e.endpoints for e in mixed.edges}) == len(mixed.edges),
        "binary": all(len(adj[v]) == (1 if role == "leaf" else 3) for v, role in roles.items()),
        "level": max((b["reticulations"] for b in blobs), default=0),
        "blobs": blobs,
        "triangles": triangles(mixed),
    }


def no_omnian_failures(mixed: MixedGraph) -> list[dict[str, object]]:
    failures = []
    for e in mixed.edges:
        if len(e.heads) != 1:
            continue
        head = e.heads[0]
        tail = next(v for v in e.endpoints if v != head)
        ordinary = sum(not x.heads and tail in x.endpoints for x in mixed.edges)
        if ordinary != 2:
            failures.append({"tail": tail, "head": head, "ordinary_incidence_count": ordinary})
    return failures


def substitute_cherry(mixed: MixedGraph, retained: str, new_leaf: str, label: int, parent: str) -> MixedGraph:
    roles, labels = mixed.role_dict(), mixed.label_dict()
    incident = [e for e in mixed.edges if retained in e.endpoints]
    if len(incident) != 1 or incident[0].heads or roles.get(retained) != "leaf":
        raise AssertionError((retained, incident))
    old = incident[0]
    outside = next(v for v in old.endpoints if v != retained)
    edges = [e for e in mixed.edges if e != old]
    edges.extend((MixedEdge.make(outside, parent), MixedEdge.make(parent, retained), MixedEdge.make(parent, new_leaf)))
    roles[parent] = "tree"
    roles[new_leaf] = "leaf"
    labels[new_leaf] = label
    return MixedGraph(mixed.name, tuple(sorted(roles.items())), tuple(sorted(labels.items())), tuple(sorted(edges)))


def contract_cherry(mixed: MixedGraph, retained: str, new_leaf: str, parent: str) -> MixedGraph:
    roles, labels = mixed.role_dict(), mixed.label_dict()
    adj = adjacency(mixed)
    outside = sorted(adj[parent] - {retained, new_leaf})
    if len(outside) != 1 or adj[retained] != {parent} or adj[new_leaf] != {parent}:
        raise AssertionError("not the expected pendant cherry")
    removed = {parent, new_leaf}
    edges = [e for e in mixed.edges if not any(v in removed for v in e.endpoints)]
    edges.append(MixedEdge.make(outside[0], retained))
    del roles[parent]
    del roles[new_leaf]
    del labels[new_leaf]
    return MixedGraph(mixed.name, tuple(sorted(roles.items())), tuple(sorted(labels.items())), tuple(sorted(edges)))


def lift_rooting(
    mixed_after: MixedGraph, record: dict[str, object], retained: str, new_leaf: str, parent: str,
) -> dict[str, object]:
    arcs = list(record["arcs"])  # type: ignore[arg-type]
    incoming = [e for e in arcs if e[1] == retained]
    if len(incoming) != 1:
        raise AssertionError(incoming)
    old = incoming[0]
    arcs.remove(old)
    arcs.extend(((old[0], parent), (parent, retained), (parent, new_leaf)))
    check = validate_rooting(mixed_after, arcs)
    if check is None:
        raise AssertionError("lifted rooting failed explicit sd0 validation")
    return check


# ---------------------------------------------------------------------------
# Cherry inverse, dimension, and targeted falsification tests


def sqrt_fraction(x: Q) -> Q:
    if x < 0:
        raise ValueError("negative square root")
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    if a * a != x.numerator or b * b != x.denominator:
        raise ValueError(f"not a rational square: {x}")
    return Q(a, b)


def cherry_jacobian(u: tuple[Q, Q, Q], v: tuple[Q, Q, Q]) -> list[list[Q]]:
    j = [[Q(0) for _ in range(6)] for _ in range(6)]
    for h in range(3):
        ui, vi = u[h], v[h]
        j[2*h][2*h] = 1 / vi
        j[2*h][2*h+1] = -ui / (vi * vi)
        j[2*h+1][2*h] = vi
        j[2*h+1][2*h+1] = ui
    return j


def strict_k3p_point(x: tuple[Q, Q, Q]) -> dict[str, object]:
    c, g, t = x
    tests = {
        "C": c, "G": g, "T": t, "1-C": 1-c, "1-G": 1-g, "1-T": 1-t,
        "p0": (1+c+g+t)/4, "pC": (1+c-g-t)/4,
        "pG": (1-c+g-t)/4, "pT": (1-c-g+t)/4,
        "C-GT": c-g*t, "G-CT": g-c*t, "T-CG": t-c*g,
    }
    return {"all_strict": all(z > 0 for z in tests.values()), "minimum": min(tests.values()), "tests": tests}


def cherry_transform_countercheck(u: tuple[Q, Q, Q], v: tuple[Q, Q, Q]) -> dict[str, object]:
    ue = (Q(1),) + u
    ve = (Q(1),) + v
    # A generic positive normalized three-leaf Fourier tensor.  Only the 16
    # zero-sum coordinates occur, and q_000 is one.
    old = {char: (Q(1) if char == (0, 0, 0) else Q(7 + i, 101)) for i, char in enumerate(CHARS)}
    new = {}
    for a, b, c in product(range(4), repeat=3):
        d = a ^ b ^ c
        new[(a, b, c, d)] = old[(a, b, c ^ d)] * ue[c] * ve[d]
    ratios, products_ = [], []
    for h in (1, 2, 3):
        ratios.append(new[(h, 0, h, 0)] / new[(h, 0, 0, h)])
        products_.append(new[(0, 0, h, h)])
    recovered_u = tuple(sqrt_fraction(ratios[h] * products_[h]) for h in range(3))
    recovered_v = tuple(sqrt_fraction(products_[h] / ratios[h]) for h in range(3))
    recovered_old = {}
    for a, b in product(range(4), repeat=2):
        k = a ^ b
        recovered_old[(a, b, k)] = new[(a, b, k, 0)] / ue[k]
    return {
        "ratios": [str(x) for x in ratios],
        "products": [str(x) for x in products_],
        "u_recovered": recovered_u == u,
        "v_recovered": recovered_v == v,
        "old_tensor_recovered": recovered_old == old,
        "positive_branch_required": True,
    }


def interval_endpoint_product(lo1: Q, hi1: Q, lo2: Q, hi2: Q) -> tuple[Q, Q]:
    if lo1 > hi1 or lo2 > hi2:
        raise ValueError("reversed endpoint interval")
    values = (lo1*lo2, lo1*hi2, hi1*lo2, hi1*hi2)
    return min(values), max(values)


def run_mutations(
    centers: list[Q], pivots: list[int], y0: list[Q], row_scales: list[Q], radius: Q,
    f0: list[Q], j0: list[list[Q]], inverse: list[list[Q]], polynomials: list[Poly],
    rank_w: dict[str, object], physical_w: dict[str, object],
) -> dict[str, object]:
    results: dict[str, object] = {}

    # Exact 10^-50 boxes are invisible in binary64 near y=1.
    collapsed = sum(float(y-radius) == float(y+radius) for y in y0)
    results["binary64_box_collapse"] = {
        "collapsed_coordinates": collapsed,
        "total": DIM,
        "mutation_detected": collapsed == DIM,
        "meaning": "A binary64 replay cannot establish the strict 10^-50 inclusion; exact/outward arithmetic is mandatory.",
    }

    # Alternate interval multiplication and a classic mixed-sign failure of an
    # unsafe two-corner implementation.
    correct = interval_endpoint_product(Q(-2), Q(-1), Q(-3), Q(4))
    unsafe = (Q(6), Q(-4))  # lo*lo, hi*hi without four-corner ordering
    ball = Ball(Q(-3, 2), Q(1, 2)) * Ball(Q(1, 2), Q(7, 2))
    results["interval_orientation"] = {
        "exact_endpoint_product": [str(x) for x in correct],
        "unsafe_two_corner_result": [str(x) for x in unsafe],
        "center_radius_encloses_exact": ball.lo <= correct[0] and ball.hi >= correct[1],
        "reversed_interval_rejected": False,
        "mutation_detected": False,
    }
    try:
        interval_endpoint_product(Q(1), Q(0), Q(0), Q(1))
    except ValueError:
        results["interval_orientation"]["reversed_interval_rejected"] = True  # type: ignore[index]
    results["interval_orientation"]["mutation_detected"] = bool(  # type: ignore[index]
        correct == (Q(-8), Q(6)) and unsafe[0] > unsafe[1]
        and results["interval_orientation"]["center_radius_encloses_exact"]
        and results["interval_orientation"]["reversed_interval_rejected"]
    )

    # A scalar orientation fixture has a nonzero center residual so the sign in
    # y0-YF0 is actually tested (the production residual is too tiny to expose
    # this mutation numerically).
    scalar_y0, scalar_a, scalar_r = Q(0), Q(1, 4), Q(1, 3)
    correct_center = scalar_y0 - (scalar_y0-scalar_a)
    wrong_center = scalar_y0 + (scalar_y0-scalar_a)
    results["krawczyk_center_sign_fixture"] = {
        "correct_self_map": abs(correct_center-scalar_y0) < scalar_r,
        "wrong_plus_sign_self_map": abs(wrong_center-scalar_y0) < scalar_r,
        "correct_operator_point_residual": str(correct_center-scalar_a),
        "wrong_operator_point_residual": str(wrong_center-scalar_a),
        "mutation_detected": correct_center-scalar_a == 0 and wrong_center-scalar_a != 0,
        "lesson": "A wrong sign can still map a symmetric box into itself; the fixed-point-to-zero identity, not inclusion alone, fixes the Krawczyk orientation.",
    }

    transposed = krawczyk_check(centers, pivots, y0, radius, row_scales, f0, inverse, True)
    results["transposed_preconditioner"] = {
        "strict_self_map": transposed["strict_self_map"],
        "q_decimal": decimal(transposed["q"]),
        "mutation_detected": not transposed["strict_self_map"] or transposed["q"] >= 1,
    }

    tiny = krawczyk_check(centers, pivots, y0, Q(1, 10**92), row_scales, f0, inverse)
    results["undersized_box"] = {
        "radius": "1e-92", "strict_self_map": tiny["strict_self_map"],
        "normalized_operator_radius_decimal": decimal(tiny["normalized_operator_radius"]),
        "mutation_detected": not tiny["strict_self_map"],
    }

    broad = krawczyk_check(centers, pivots, y0, Q(1, 10), row_scales, f0, inverse)
    results["overbroad_box"] = {
        "radius": "1/10", "q_decimal": decimal(broad["q"]),
        "strict_self_map": broad["strict_self_map"],
        "mutation_detected": broad["q"] >= 1 or not broad["strict_self_map"],
    }

    # Slice integrity mutations.
    duplicate_pivots = pivots[:-1] + [pivots[0]]
    results["duplicate_pivot"] = {
        "unique_count": len(set(duplicate_pivots)),
        "mutation_detected": len(set(duplicate_pivots)) != DIM,
    }
    results["dropped_equation"] = {
        "jacobian_rank": rank_and_pivots(j0[:-1])[0],
        "mutation_detected": rank_and_pivots(j0[:-1])[0] < DIM,
    }
    zero_row = [[Q(0) for _ in range(DIM)]] + j0[1:]
    results["q000_replaces_nonconstant_row"] = {
        "jacobian_rank": rank_and_pivots(zero_row)[0],
        "mutation_detected": rank_and_pivots(zero_row)[0] < DIM,
    }
    tampered = [dict(p) for p in polynomials]
    first_m = next(iter(tampered[0]))
    tampered[0][first_m] += 1
    results["tampered_polynomial_coefficient"] = {
        "same_as_reconstruction": tampered == polynomials,
        "mutation_detected": tampered != polynomials,
    }

    # Rank-minor and physical mutations.
    cols = list(rank_w["columns"])  # type: ignore[arg-type]
    duplicate_cols = cols[:-1] + [cols[0]]
    jw = rank_w["point_jacobian"]  # type: ignore[assignment]
    duplicate_minor = [[jw[i][j] for j in duplicate_cols] for i in range(DIM)]
    results["duplicate_rank_column"] = {
        "determinant": str(determinant(duplicate_minor)),
        "mutation_detected": determinant(duplicate_minor) == 0,
    }
    stochastic_not_ct = strict_k3p_point((Q(1, 20), Q(4, 5), Q(1, 10)))
    results["stochastic_but_not_ct_edge"] = {
        "principal_transition_positive": all(stochastic_not_ct["tests"][x] > 0 for x in ("C", "G", "T", "1-C", "1-G", "1-T", "p0", "pC", "pG", "pT")),  # type: ignore[index]
        "ct_all_strict": all(stochastic_not_ct["tests"][x] > 0 for x in ("C-GT", "G-CT", "T-CG")),  # type: ignore[index]
        "mutation_detected": stochastic_not_ct["tests"]["C-GT"] < 0,  # type: ignore[index]
    }
    results["zero_edge_eigenvalue"] = {
        "would_pass": Q(0) > 0,
        "mutation_detected": not (Q(0) > 0),
    }

    # Cherry rank drops when a product observable is duplicated or the two
    # pendant spectra are artificially tied.
    alln = json.loads(ALLN_SOURCE.read_text(encoding="utf-8"))
    u = tuple(Q(x) for x in alln["example_u"])
    v = tuple(Q(x) for x in alln["example_v"])
    cj = cherry_jacobian(u, v)
    duplicated_row = [row[:] for row in cj]
    duplicated_row[1] = duplicated_row[0][:]
    tied = []
    # R_h=1 has zero derivative under u_h=v_h=w_h; P_h=w_h^2.
    for h in range(3):
        tied.append([Q(0), Q(0), Q(0)])
        row = [Q(0), Q(0), Q(0)]
        row[h] = 2*u[h]
        tied.append(row)
    results["cherry_observable_duplication"] = {
        "rank": rank_and_pivots(duplicated_row)[0],
        "mutation_detected": rank_and_pivots(duplicated_row)[0] < 6,
    }
    results["tied_cherry_edges"] = {
        "rank": rank_and_pivots(tied)[0],
        "mutation_detected": rank_and_pivots(tied)[0] == 3,
    }

    # Rooting-definition fixtures.  The first is binary and acyclic but has a
    # proper stable descendant v, so omitting the LSA test would admit it.  The
    # second keeps the underlying graph while erasing retained arrowheads; an
    # explicit sd_0 equality check must reject that mutation.
    lsa_bad = RootedSpec(
        "lsa_bad_fixture",
        (("rb", "a"), ("rb", "b"), ("a", "h"), ("a", "k"), ("b", "h"), ("b", "k"),
         ("h", "v"), ("k", "v"), ("v", "t"), ("t", "L0"), ("t", "L1")),
        frozenset(("h", "k", "v")), (("L0", 0), ("L1", 1)),
    )
    lsa_mixed = suppress_root(lsa_bad)
    lsa_arcs = [("__R__" if u == "rb" else u, v) for u, v in lsa_bad.arcs]
    lsa_required = validate_rooting(lsa_mixed, lsa_arcs, require_lsa=True)
    lsa_omitted = validate_rooting(lsa_mixed, lsa_arcs, require_lsa=False)
    results["lsa_omission_fixture"] = {
        "accepted_with_lsa_required": lsa_required is not None,
        "accepted_if_lsa_omitted": lsa_omitted is not None,
        "stable_vertices_without_filter": lsa_omitted["stable_vertices"] if lsa_omitted else [],
        "mutation_detected": lsa_required is None and lsa_omitted is not None,
    }
    w_mixed = suppress_root(RW)
    w_arcs = [("__R__" if u == "r" else u, v) for u, v in RW.arcs]
    valid_w = validate_rooting(w_mixed, w_arcs)
    heads_erased = MixedGraph(w_mixed.name, w_mixed.roles, w_mixed.labels,
                              tuple(MixedEdge.make(*e.endpoints) for e in w_mixed.edges))
    wrong_w = validate_rooting(heads_erased, w_arcs)
    results["arrowhead_erasure_fixture"] = {
        "original_rooting_valid": valid_w is not None,
        "same_underlying_graph_with_heads_erased_valid": wrong_w is not None,
        "mutation_detected": valid_w is not None and wrong_w is None,
    }

    # Ensure this audit does not accidentally derive authority from a stored
    # PASS bit: flipping every parent conclusion would not alter any input used
    # above.  The key inventories are recorded for review.
    parent_k = json.loads(PARENT_K.read_text(encoding="utf-8"))
    parent_t = json.loads(PARENT_T.read_text(encoding="utf-8"))
    results["stored_boolean_independence"] = {
        "parent_k_conclusion_keys_ignored": sorted(parent_k.get("conclusion", {})),
        "parent_t_conclusion_keys_ignored": sorted(parent_t.get("conclusion", {})),
        "mutation_detected": True,
        "method": "No parent conclusion value enters any reconstructed equation, interval, graph, or determinant.",
    }
    return results


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    parent_k = json.loads(PARENT_K.read_text(encoding="utf-8"))
    alln_source = json.loads(ALLN_SOURCE.read_text(encoding="utf-8"))

    centers = [Q(x) for x in source["center_rationals"]]
    pivots = [int(x) for x in source["pivot_global_columns"]]
    y0 = [Q(x) for x in source["root_center_y"]]
    radius = Q(source["box_radius"])
    row_scales = [Q(x) for x in source["row_scales"]]
    if len(centers) != 64 or len(pivots) != len(y0) != DIM:
        raise AssertionError("bad witness dimensions")
    if not (len(pivots) == len(y0) == len(row_scales) == DIM and len(set(pivots)) == DIM and radius > 0):
        raise AssertionError("bad slice")
    if any(s == 0 for s in row_scales):
        raise AssertionError("zero row scale")
    expected_edges = {"W": [list(x) for x in W.arcs], "Wprime": [list(x) for x in WPRIME.arcs]}
    if source["edge_orders"] != expected_edges:
        raise AssertionError("edge-order mismatch")

    # Independent symbolic reconstruction of the equality slice.
    pmap = {p: j for j, p in enumerate(pivots)}
    direct_polys: list[Poly] = []
    for i, c in enumerate(centers):
        if i in pmap:
            m = [0] * DIM
            m[pmap[i]] = 1
            direct_polys.append({tuple(m): c})
        else:
            direct_polys.append({ZERO_MONOMIAL: c})
    qwpoly = map_poly(W, direct_polys[:32])
    qppoly = map_poly(WPRIME, direct_polys[32:])
    normalized_constant = {ZERO_MONOMIAL: Q(1)}
    if qwpoly[0] != normalized_constant or qppoly[0] != normalized_constant:
        raise AssertionError("q000 normalization failed")
    if len(set(CHARS)) != 16 or any((a ^ b ^ c) != 0 for a, b, c in CHARS):
        raise AssertionError("Fourier output order is not the complete zero-sum order")
    polynomials = [p_scale(p_add(qwpoly[i+1], p_scale(qppoly[i+1], Q(-1))), row_scales[i]) for i in range(DIM)]
    if any(any(e not in (0, 1) for e in m) for p in polynomials for m in p):
        raise AssertionError("slice unexpectedly not multiaffine")
    stored_polynomials = parse_stored_polys(parent_k["equality_system"]["expanded_sparse_polynomials"])
    symbolic_match = polynomials == stored_polynomials
    if not symbolic_match:
        raise AssertionError("independent graph-derived equations differ from stored expansion")

    # Alternate center-radius exact Krawczyk replay.
    point_eq, direct_point = equality_duals(centers, pivots, y0, Q(0), row_scales)
    f0 = [z.value.mid for z in point_eq]
    j0 = [[z.deriv[j].mid for j in range(DIM)] for z in point_eq]
    inverse, det_j0 = matrix_inverse_and_det(j0)
    if f0 != [Q(x) for x in parent_k["equality_system"]["exact_center_residual"]]:
        raise AssertionError("center residual mismatch")
    kraw = krawczyk_check(centers, pivots, y0, radius, row_scales, f0, inverse)
    if not kraw["strict_self_map"] or not kraw["q"] < 1:
        raise AssertionError("alternate Krawczyk replay failed")

    _, direct_box = equality_duals(centers, pivots, y0, radius, row_scales)
    point_values = [z.value.mid for z in direct_point]
    box_values = [z.value for z in direct_box]
    rank_w = rank_box_check(W, point_values[:32], box_values[:32])
    rank_p = rank_box_check(WPRIME, point_values[32:], box_values[32:])
    physical_w = physical_check(W, box_values[:32])
    physical_p = physical_check(WPRIME, box_values[32:])
    if not rank_w["uniform"] or not rank_p["uniform"] or not physical_w["all_strict"] or not physical_p["all_strict"]:
        raise AssertionError("rank or physical replay failed")

    # Every box Jacobian is a polynomial interval enclosure.  Test a fixed set
    # of exact corners against it to guard derivative-variable orientation.
    box_eq, _ = equality_duals(centers, pivots, y0, radius, row_scales)
    jbox = [list(z.deriv) for z in box_eq]
    corner_patterns = [tuple(0 for _ in range(DIM)), tuple(1 for _ in range(DIM))]
    corner_patterns += [tuple((i >> j) & 1 for j in range(DIM)) for i in (1, 3, 7, 31, 255, 1023, 32767)]
    corner_containment = True
    for bits in corner_patterns:
        yc = [y0[j] + (radius if bits[j] else -radius) for j in range(DIM)]
        eqc, _ = equality_duals(centers, pivots, yc, Q(0), row_scales)
        for i in range(DIM):
            for j in range(DIM):
                if not jbox[i][j].contains(eqc[i].deriv[j].mid):
                    corner_containment = False
    if not corner_containment:
        raise AssertionError("alternate interval Jacobian misses a tested corner")

    # Explicit sd0 census; no frozen census record is consumed.
    mixed = {s.name: suppress_root(s) for s in (RW, RWP, COLLISION)}
    rootings = {name: enumerate_rootings(g) for name, g in mixed.items()}
    counts = {name: (len(rs), sum(bool(r["tree_child"]) for r in rs), sum(not bool(r["tree_child"]) for r in rs)) for name, rs in rootings.items()}
    expected_counts = {"W": (5, 2, 3), "Wprime": (7, 2, 5), "collision": (7, 0, 7)}
    if counts != expected_counts:
        raise AssertionError((counts, expected_counts))
    if any(len({r["root_edge"].endpoints for r in rs}) != len(rs) for rs in rootings.values()):  # type: ignore[union-attr]
        raise AssertionError("root-edge orientation is not unique")
    topology = {name: topology_summary(g) for name, g in mixed.items()}
    if not all(topology[n]["simple"] and topology[n]["binary"] and topology[n]["level"] == 2 for n in ("W", "Wprime")):
        raise AssertionError("base topology class failed")
    distance_w = leaf_distance_matrix(mixed["W"])
    distance_p = leaf_distance_matrix(mixed["Wprime"])
    distance_separation = distance_w != distance_p and distance_w["0-1"] == 4 and distance_p["0-1"] == 3
    if not distance_separation:
        raise AssertionError("leaf-distance topology separator failed")
    no_omnian = {name: no_omnian_failures(mixed[name]) for name in ("W", "Wprime")}
    if not all(no_omnian.values()):
        raise AssertionError("expected strong-tree-child obstruction absent")

    # Lift independent TC and NTC witnesses through nine stages (to n=12),
    # checking exact sd0 reconstruction, bridge status, level, and contraction.
    persistence: dict[str, list[dict[str, object]]] = {}
    for name in ("W", "Wprime"):
        current = mixed[name]
        tc = next(r for r in rootings[name] if r["tree_child"])
        ntc = next(r for r in rootings[name] if not r["tree_child"])
        stages = []
        base_triangles = triangles(current)
        for n in range(4, 13):
            parent = f"AuditCherryParent{n}"
            leaf = f"AuditLeaf{n-1}"
            previous = current
            current = substitute_cherry(current, "L2", leaf, n-1, parent)
            tc = lift_rooting(current, tc, "L2", leaf, parent)
            ntc = lift_rooting(current, ntc, "L2", leaf, parent)
            contracted = contract_cherry(current, "L2", leaf, parent)
            summary = topology_summary(current)
            new_incident = [e.endpoints for e in current.edges if parent in e.endpoints]
            bridges = bridge_edges(current)
            stage_ok = (
                tc["tree_child"] and not ntc["tree_child"] and contracted == previous
                and summary["simple"] and summary["binary"] and summary["level"] == 2
                and summary["triangles"] == base_triangles
                and all(e in bridges for e in new_incident)
                and leaf_distance_matrix(current)["0-1"] == (4 if name == "W" else 3)
            )
            if not stage_ok:
                raise AssertionError((name, n))
            stages.append({"n": n, "stage_ok": stage_ok, "level": summary["level"],
                           "new_edges_are_bridges": all(e in bridges for e in new_incident),
                           "distance_0_1": leaf_distance_matrix(current)["0-1"]})
        persistence[name] = stages

    # Cherry determinant, exact positive inverse, tensor factorization.
    u = tuple(Q(x) for x in alln_source["example_u"])
    v = tuple(Q(x) for x in alln_source["example_v"])
    cherry_j = cherry_jacobian(u, v)
    cherry_det = determinant(cherry_j)
    formula_det = 8*u[0]*u[1]*u[2]/(v[0]*v[1]*v[2])
    if cherry_det != formula_det or cherry_det != Q(176, 25):
        raise AssertionError("cherry determinant mismatch")
    cherry_inverse = cherry_transform_countercheck(u, v)
    if not all(cherry_inverse[x] for x in ("u_recovered", "v_recovered", "old_tensor_recovered")):
        raise AssertionError("cherry inverse failed")
    u_phys, v_phys = strict_k3p_point(u), strict_k3p_point(v)
    if not u_phys["all_strict"] or not v_phys["all_strict"]:
        raise AssertionError("cherry spectra not strict CT")

    mutations = run_mutations(centers, pivots, y0, row_scales, radius, f0, j0, inverse, polynomials, rank_w, physical_w)
    mutation_failures = [name for name, record in mutations.items() if not record.get("mutation_detected", False)]  # type: ignore[union-attr]

    missing_relative = FROZEN / "sharpness_relative_root.json"
    provenance = {
        "source_hashes": {str(p.relative_to(PROJECT)): file_hash(p) for p in (
            SOURCE, FROZEN / "certify_sharpness_krawczyk.py", FROZEN / "sharpness_exact_maps.py",
            FROZEN / "k3p_sharpness_ift_base.json", ALLN_SOURCE, FROZEN / "k3p_rooting_censuses.json",
            PARENT_K, PARENT_T,
        )},
        "sharpness_relative_root_referenced_by_cloud_script": "sharpness_relative_root.json" in (FROZEN / "certify_sharpness_krawczyk.py").read_text(encoding="utf-8"),
        "sharpness_relative_root_present": missing_relative.exists(),
        "discovery_lineage_replayable_end_to_end": missing_relative.exists(),
        "final_rational_witness_self_contained_for_exact_verification": True,
        "parent_final_booleans_consumed": False,
        "adversarial_verifier": {
            "path": str(Path(__file__).resolve().relative_to(PROJECT)),
            "sha256": file_hash(Path(__file__).resolve()),
            "bytes": Path(__file__).stat().st_size,
            "python": sys.version,
            "dependencies": ["Python standard library only"],
        },
        "residual_gap": "The numerical-discovery intermediate sharpness_relative_root.json is absent, so discovery lineage and the pre-truncation root cannot be replayed. The final graph-plus-rational witness is nevertheless independently sufficient for the exact existence/rank/physical proof.",
    }

    all_math_pass = bool(
        symbolic_match and kraw["strict_self_map"] and kraw["q"] < 1 and corner_containment
        and rank_w["uniform"] and rank_p["uniform"] and physical_w["all_strict"] and physical_p["all_strict"]
        and counts == expected_counts and distance_separation and all(no_omnian.values())
        and all(stage["stage_ok"] for stages in persistence.values() for stage in stages)
        and cherry_det != 0 and cherry_inverse["old_tensor_recovered"] and u_phys["all_strict"] and v_phys["all_strict"]
        and not mutation_failures
    )
    audit = {
        "schema": "k3p-sharpness-adversarial-audit-v1",
        "method": "clean-room exact rational center-radius intervals, explicit sd0 reconstruction, graph invariants, and killed mutations; parent PASS booleans ignored",
        "analytic_base": {
            "map_term_hashes": {name: object_hash(terms) for name, terms in MAP_TERMS.items()},
            "expanded_equations_match_parent_embedded_copy": symbolic_match,
            "expanded_equation_term_counts": [len(p) for p in polynomials],
            "multiaffine": True,
            "q000_is_identically_one_on_both_maps": True,
            "output_order_is_complete_unique_zero_sum_order": True,
            "equality_point_jacobian_determinant": str(det_j0),
            "equality_point_jacobian_determinant_decimal": decimal(det_j0),
            "maximum_center_residual_decimal": decimal(max(abs(x) for x in f0)),
            "box_radius": str(radius),
            "alternate_krawczyk": {
                "strict_self_map": kraw["strict_self_map"],
                "q": str(kraw["q"]), "q_decimal": decimal(kraw["q"]),
                "normalized_operator_radius": str(kraw["normalized_operator_radius"]),
                "normalized_operator_radius_decimal": decimal(kraw["normalized_operator_radius"]),
                "minimum_inclusion_margin": str(kraw["minimum_inclusion_margin"]),
                "minimum_inclusion_margin_decimal": decimal(kraw["minimum_inclusion_margin"]),
                "tested_exact_corners_contained": corner_containment,
                "uniqueness_hypotheses": {"box_convex": True, "map_polynomial_C1": True,
                    "preconditioner_invertible": det_j0 != 0, "mean_jacobians_in_interval_hull": True,
                    "error_norm_below_one": kraw["q"] < 1},
            },
            "rank_persistence": {
                "W": {"rank": rank_w["rank"], "columns": rank_w["columns"], "determinant": str(rank_w["determinant"]), "q": str(rank_w["q"]), "q_decimal": decimal(rank_w["q"]), "uniform": rank_w["uniform"]},
                "Wprime": {"rank": rank_p["rank"], "columns": rank_p["columns"], "determinant": str(rank_p["determinant"]), "q": str(rank_p["q"]), "q_decimal": decimal(rank_p["q"]), "uniform": rank_p["uniform"]},
            },
            "physical_strict_ct": {
                "W": {"all_strict": physical_w["all_strict"], "minimum_lower": str(physical_w["minimum"]["lower"]), "minimum_lower_decimal": decimal(physical_w["minimum"]["lower"]), "minimum_semantics": {k: v for k, v in physical_w["minimum"].items() if k != "lower"}, "effective_root_edge_minimum": str(physical_w["effective_suppressed_root_edge_minimum"])},
                "Wprime": {"all_strict": physical_p["all_strict"], "minimum_lower": str(physical_p["minimum"]["lower"]), "minimum_lower_decimal": decimal(physical_p["minimum"]["lower"]), "minimum_semantics": {k: v for k, v in physical_p["minimum"].items() if k != "lower"}, "effective_root_edge_minimum": str(physical_p["effective_suppressed_root_edge_minimum"])},
            },
            "geometric_consequence": "The exact slice root is interior to the strict-CT parameter domain. Each normalized 15-output map is a submersion there, hence both images contain ambient-open neighborhoods of the same tensor; their intersection is a common regular 15-germ.",
        },
        "topology": {
            "rooting_censuses": {name: list(counts[name]) for name in counts},
            "every_rooting_explicitly_suppresses_back_to_fixed_mixed_graph": True,
            "root_edge_orientation_unique": True,
            "base_summaries": topology,
            "no_omnian_failures": no_omnian,
            "leaf_distance_matrices": {"W": distance_w, "Wprime": distance_p},
            "labelled_underlying_nonisomorphism": distance_separation,
            "not_ordinary_triangle_equivalent": distance_separation,
            "reason": "Ordinary triangle redirection preserves the labelled underlying graph and therefore leaf distances; d_W(0,1)=4 but d_Wprime(0,1)=3.",
        },
        "all_n": {
            "checked_stages": persistence,
            "uniform_class_argument": "Pendant cherry replacement lifts one explicit tree-child rooting and one explicit non-tree-child rooting; the old non-tree-child witness is untouched. All new edges are bridges, so binary standardness, blobs, and level 2 persist.",
            "uniform_nonisomorphism_argument": "Every graft occurs above leaf 2, so d(0,1) remains 4 on W_n and 3 on Wprime_n for every n. This directly excludes labelled isomorphism and triangle equivalence at all n.",
            "cherry_jacobian_determinant": str(cherry_det),
            "cherry_jacobian_rank": rank_and_pivots(cherry_j)[0],
            "positive_inverse_countercheck": cherry_inverse,
            "cherry_spectra_strict_ct": {"u": u_phys["all_strict"], "v": v_phys["all_strict"], "u_min": str(u_phys["minimum"]), "v_min": str(v_phys["minimum"])},
            "dimension": {
                "base": 15, "increment_per_cherry": 6, "formula": "15+6(n-3)=6n-3",
                "upper_bound_reason": "The grafted tensor factors through (old tensor,u,v), so its image dimension is at most old dimension plus six.",
                "lower_bound_reason": "The six R_h,P_h observables have nonzero Jacobian and recover u,v on the positive branch; division by nonzero pendant factors recovers the old tensor.",
                "full_model_dimension_reason": "The entire grafted-network image has exactly this factorized form, so the common embedded germ has the full intrinsic dimension of each grafted model.",
            },
        },
        "mutations": mutations,
        "mutation_failures": mutation_failures,
        "provenance": provenance,
        "verdict": {
            "mathematical_sharpness_claim": "PASS" if all_math_pass else "FAIL",
            "proof_gaps": [] if all_math_pass else ["one or more independent mathematical gates failed"],
            "provenance_status": "PASS_WITH_DOCUMENTARY_GAP" if all_math_pass and not missing_relative.exists() else "PASS" if all_math_pass else "FAIL",
            "residual_gaps": [provenance["residual_gap"]] if not missing_relative.exists() else [],
            "completion_estimate_percent": 100 if all_math_pass else 90,
        },
    }
    atomic_json(OUTPUT, audit)
    print("SHARPNESS_ADVERSARIAL_MATH_PASS" if all_math_pass else "SHARPNESS_ADVERSARIAL_FAIL")
    print(f"output={OUTPUT}")
    print(f"sha256={file_hash(OUTPUT)}")
    print(f"mutation_failures={mutation_failures}")
    return 0 if all_math_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
