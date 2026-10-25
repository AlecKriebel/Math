"""Exact small certificates for the Paper-B NMSC level-2 theorem.

The universal theorem is proved in the manuscript.  This module checks the
load-bearing formulas and graph tables with exact rational/symbolic arithmetic.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple
import json

import networkx as nx
import sympy as sp


@dataclass(frozen=True)
class Core:
    name: str
    arcs: Tuple[Tuple[str, str], ...]
    retics: Tuple[str, ...]
    sinks: Tuple[str, ...]
    repairs: Tuple[Tuple[int, ...], ...]


def load_cores(path: str | Path) -> Dict[str, Core]:
    raw = json.loads(Path(path).read_text())['cores']
    out: Dict[str, Core] = {}
    for name, rec in raw.items():
        out[name] = Core(
            name=name,
            arcs=tuple(tuple(x) for x in rec['arcs']),
            retics=tuple(rec['retics']),
            sinks=tuple(rec['sinks']),
            repairs=tuple(tuple(x) for x in rec['repairs']),
        )
    return out


def build_repaired_core(core: Core, repair: Sequence[int]) -> nx.MultiDiGraph:
    """Build the local raw strong expansion represented by one minimum repair.

    Each repaired segment is subdivided by a tree vertex with one sampled leaf.
    Every path-sink reticulation receives its compulsory sampled child.
    Edge keys retain parallel topological segments after suppression.
    """
    g = nx.MultiDiGraph()
    nodes = set(sum(([a, b] for a, b in core.arcs), []))
    for v in nodes:
        g.add_node(v, role='retic' if v in core.retics else 'tree')
    repair_set = set(repair)
    for i, (a, b) in enumerate(core.arcs):
        if i in repair_set:
            s = f'p{i}'
            leaf = f'L{i}'
            g.add_node(s, role='tree')
            g.add_node(leaf, role='leaf')
            g.add_edge(a, s, key=f'{i}a', segment=i)
            g.add_edge(s, b, key=f'{i}b', segment=i)
            g.add_edge(s, leaf, key=f'{i}L', segment=f'port{i}')
        else:
            g.add_edge(a, b, key=str(i), segment=i)
    for sink in core.sinks:
        leaf = f'C_{sink}'
        g.add_node(leaf, role='leaf')
        g.add_edge(sink, leaf, key=f'child_{sink}', segment='sink_child')
    return g


def is_local_tree_child(g: nx.MultiDiGraph) -> bool:
    for v, data in g.nodes(data=True):
        role = data.get('role')
        if role == 'leaf':
            continue
        children = [w for _, w, _ in g.out_edges(v, keys=True)]
        if not children:
            return False
        if not any(g.nodes[w].get('role') in {'tree', 'leaf'} for w in children):
            return False
        if role == 'retic' and len(children) != 1:
            return False
    return True


def is_local_strong_tree_child(g: nx.MultiDiGraph, source: str | None = 'S') -> bool:
    """Check the binary local strong criterion on a ported rooted core.

    Every tail of an edge into a reticulation must have two ordinary incident
    edges in the associated standard semi-directed topology.  The core source
    has one additional ordinary incoming boundary edge not stored in the local
    graph.
    """
    for r, data in g.nodes(data=True):
        if data.get('role') != 'retic':
            continue
        for pnode in set(g.predecessors(r)):
            # In the standard semi-directed reduction only edges whose head is
            # a reticulation retain an arrowhead.  Every incoming edge of this
            # tree tail, including an outgoing edge of another reticulation, is
            # ordinary; among outgoing edges, exclude only those entering a
            # reticulation.
            ordinary = g.in_degree(pnode)
            ordinary += sum(
                1 for _, v, _ in g.out_edges(pnode, keys=True)
                if g.nodes[v].get('role') != 'retic'
            )
            if source is not None and pnode == source:
                ordinary += 1  # distinguished incoming population boundary
            if ordinary < 2:
                return False
    return True


def repair_satisfies_domain(core: Core, repair: Sequence[int]) -> bool:
    """Require both rooted tree-childness and the semi-directed strong tail test."""
    graph = build_repaired_core(core, repair)
    return is_local_tree_child(graph) and is_local_strong_tree_child(graph)


def repair_is_minimal(core: Core, repair: Sequence[int]) -> bool:
    repair = tuple(sorted(repair))
    if not repair_satisfies_domain(core, repair):
        return False
    for size in range(len(repair)):
        for smaller in combinations(repair, size):
            if repair_satisfies_domain(core, smaller):
                return False
    return True


def enumerate_minimal_repairs(core: Core) -> Tuple[Tuple[int, ...], ...]:
    """Enumerate inclusion-minimal repairs from primitive core arcs.

    The enumeration does not consult ``core.repairs``.  It applies the two
    graph-domain predicates independently and retains precisely the subsets
    having no proper valid subset.
    """
    valid: List[Tuple[int, ...]] = []
    arc_ids = tuple(range(len(core.arcs)))
    for size in range(len(arc_ids) + 1):
        for repair in combinations(arc_ids, size):
            if not repair_satisfies_domain(core, repair):
                continue
            if any(set(smaller).issubset(repair) for smaller in valid):
                continue
            valid.append(repair)
    return tuple(valid)


def fixed_cut_coefficients(gamma, lam, D, u):
    gamma, lam, D, u = map(sp.sympify, (gamma, lam, D, u))
    a = gamma * (1 - gamma) * lam * sp.exp(-lam * u)
    c = gamma**2 * lam * sp.exp(-lam * D - 2 * lam * u)
    return sp.simplify(a), sp.simplify(c)


def fixed_cut_row(gamma, lam, D, delta, u):
    a, c = fixed_cut_coefficients(gamma, lam, D, u)
    e = sp.exp(-sp.sympify(lam) * sp.sympify(delta))
    return sp.Matrix([[sp.simplify(c * (1 - e)), sp.simplify(a + c * e)]])


def fixed_cut_det(gamma, lam, D, delta, u1, u2):
    m = sp.Matrix.vstack(
        fixed_cut_row(gamma, lam, D, delta, u1),
        fixed_cut_row(gamma, lam, D, delta, u2),
    )
    return sp.simplify(m.det())


def fixed_cut_expected_det(gamma, lam, D, delta, u1, u2):
    gamma, lam, D, delta, u1, u2 = map(sp.sympify, (gamma, lam, D, delta, u1, u2))
    return sp.simplify(
        (1 - sp.exp(-lam * delta))
        * gamma**3 * (1 - gamma) * lam**2 * sp.exp(-lam * D)
        * (sp.exp(-2 * lam * u1 - lam * u2) - sp.exp(-2 * lam * u2 - lam * u1))
    )


def routing_weights(m: int, gamma: Fraction) -> Dict[Tuple[int, ...], Fraction]:
    ans: Dict[Tuple[int, ...], Fraction] = {}
    for bits in product((0, 1), repeat=m):
        k = sum(bits)
        ans[bits] = gamma**k * (1 - gamma) ** (m - k)
    return ans


def marginal_routing_weights(m: int, selected: Sequence[int], gamma: Fraction) -> Dict[Tuple[int, ...], Fraction]:
    full = routing_weights(m, gamma)
    out: Dict[Tuple[int, ...], Fraction] = {}
    selected = tuple(selected)
    for bits, w in full.items():
        key = tuple(bits[i] for i in selected)
        out[key] = out.get(key, Fraction(0)) + w
    return out


def direct_routing_weights(r: int, gamma: Fraction) -> Dict[Tuple[int, ...], Fraction]:
    return routing_weights(r, gamma)


def pair_survival(gamma, lam1, lam2, u):
    gamma, lam1, lam2, u = map(sp.sympify, (gamma, lam1, lam2, u))
    return sp.simplify(
        2 * gamma * (1 - gamma)
        + gamma**2 * sp.exp(-lam1 * u)
        + (1 - gamma) ** 2 * sp.exp(-lam2 * u)
    )


def kingman_pair_survival(lam, u):
    """Two-block survival in one constant-rate Kingman population."""
    lam, u = map(sp.sympify, (lam, u))
    return sp.exp(-lam * u)


def equal_arm_routing_survival(gamma, lam, u):
    """Two-child survival after independent routing to equal-rate parents."""
    return pair_survival(gamma, lam, lam, u)


def survival_semigroup_defect(survival, u, v):
    """Return S(u+v)-S(u)S(v), zero for normalized one-rate survival."""
    survival = sp.sympify(survival)
    u, v = map(sp.sympify, (u, v))
    return sp.simplify(survival.subs(u, u + v) - survival * survival.subs(u, v))


def log_hazard_numerator(survival, u):
    """Return S S''-(S')^2, the negative numerator of log-hazard drift."""
    survival = sp.sympify(survival)
    u = sp.sympify(u)
    return sp.simplify(
        survival * sp.diff(survival, u, 2) - sp.diff(survival, u) ** 2
    )


def pair_moments(gamma: Fraction, lam1: Fraction, lam2: Fraction, max_k: int = 4) -> List[Fraction]:
    return [gamma**2 * lam1**k + (1 - gamma) ** 2 * lam2**k for k in range(1, max_k + 1)]


def recover_two_atom_rates(m: Sequence[Fraction]) -> Tuple[Fraction, Fraction]:
    """Recover unordered rates from m1..m4 using the order-two recurrence."""
    if len(m) < 4:
        raise ValueError('need four moments')
    m1, m2, m3, m4 = map(sp.Rational, m[:4])
    s1, s2 = sp.symbols('s1 s2')
    sol = sp.solve([sp.Eq(m3, s1*m2 - s2*m1), sp.Eq(m4, s1*m3 - s2*m2)], [s1, s2], dict=True)
    if len(sol) != 1:
        raise ValueError('non-generic recurrence')
    poly = sp.Poly(sp.Symbol('z')**2 - sol[0][s1]*sp.Symbol('z') + sol[0][s2], sp.Symbol('z'))
    roots = sp.solve(poly.as_expr(), sp.Symbol('z'))
    return tuple(sorted((Fraction(r.p, r.q) for r in roots)))  # type: ignore[return-value]


def triangle_forward(gamma, lam, Delta, u):
    gamma, lam, Delta, u = map(sp.sympify, (gamma, lam, Delta, u))
    return sp.simplify(
        gamma * (1 - gamma) * lam * sp.exp(-lam * u)
        + gamma**2 * lam * sp.exp(-lam * Delta - 2 * lam * u)
    )


def triangle_reverse(gamma, lam, Delta, u):
    gamma, lam, Delta, u = map(sp.sympify, (gamma, lam, Delta, u))
    return sp.simplify(gamma * lam * sp.exp(-lam * Delta - 2 * lam * u))


def exponential_curvature(f, u):
    """f f''-(f')^2: zero for one exponential, positive for two positive distinct exponents."""
    f = sp.sympify(f)
    u = sp.sympify(u)
    return sp.simplify(f * sp.diff(f, u, 2) - sp.diff(f, u) ** 2)


def biunary_kernel(gamma, lam, Delta):
    gamma, lam, Delta = map(sp.sympify, (gamma, lam, Delta))
    e = sp.exp(-lam * Delta)
    return sp.Matrix([[1 - gamma + gamma * e, gamma * (1 - e)], [0, 1]])


def biunary_kernel_from_route_enumeration(gamma, lam, Delta):
    """Independently enumerate split/join route outcomes for the bi-unary case."""
    gamma, lam, Delta = map(sp.sympify, (gamma, lam, Delta))
    route_weights = {"split": 1 - gamma, "join": gamma}
    survival_if_join = sp.exp(-lam * Delta)
    survival = route_weights["split"] + route_weights["join"] * survival_if_join
    merger = route_weights["join"] * (1 - survival_if_join)
    return sp.Matrix([[sp.simplify(survival), sp.simplify(merger)], [0, 1]])


def biunary_rate_word_kernel(gamma, rate_word):
    """Bi-unary Q6 kernel for a finite piecewise-constant donor rate word.

    ``rate_word`` is an ordered sequence of positive ``(duration, pair_rate)``
    pairs.  Q6 transfers this entire ordered word, not only one constant rate.
    """
    gamma = sp.sympify(gamma)
    pieces = tuple((sp.sympify(duration), sp.sympify(rate)) for duration, rate in rate_word)
    if not pieces:
        raise ValueError("the exposed donor rate word must be nonempty")
    hazard = sp.simplify(sum(duration * rate for duration, rate in pieces))
    survival_if_join = sp.exp(-hazard)
    return sp.Matrix(
        [
            [
                sp.simplify(1 - gamma + gamma * survival_if_join),
                sp.simplify(gamma * (1 - survival_if_join)),
            ],
            [0, 1],
        ]
    )


def biunary_rate_word_chamber_density(gamma, rate_word, chamber, u):
    """Merger density at local time ``u`` inside one donor-word chamber."""
    gamma = sp.sympify(gamma)
    pieces = tuple((sp.sympify(duration), sp.sympify(rate)) for duration, rate in rate_word)
    if not 0 <= chamber < len(pieces):
        raise IndexError("donor-word chamber is out of range")
    prefix_hazard = sp.simplify(
        sum(duration * rate for duration, rate in pieces[:chamber])
    )
    _, rate = pieces[chamber]
    return sp.simplify(gamma * rate * sp.exp(-prefix_hazard - rate * sp.sympify(u)))


OLD_PRINCIPAL_QUOTIENT_MOVES = (
    "Q1_parameter_free_suppression",
    "Q2_boundary_composition",
    "Q3_equal_rate_epoch_merger",
    "Q4_two_terminal_sample_unary_replacement",
    "Q5_parent_presentation_exchange",
    "Q6_biunary_sister_reversal",
    "Q7_labelled_isomorphism",
)
REPAIRED_PRINCIPAL_QUOTIENT_MOVES = OLD_PRINCIPAL_QUOTIENT_MOVES + (
    "Q8_preexposure_unary_fan_slide",
)


@dataclass(frozen=True)
class UnaryRoutingFan:
    """Typed stopping-port data for one pre-exposure routing fan.

    The stopping ports may occur at different times and need not form an
    antichain: they are the route-dependent first boundaries at which a second
    sampled block can be present.  Internal side entries exclude the module.
    """

    lower_boundary: Tuple[str, Fraction, str]
    reticulation_time: Fraction
    first_exposure_ports: Tuple[Tuple[str, Fraction, str, Fraction], ...]
    internal_unary_rates: Tuple[Tuple[str, Fraction], ...]
    maximum_internal_occupancy: int
    internal_sample_entries: Tuple[Tuple[str, str, Fraction], ...]


@dataclass(frozen=True)
class FanContinuationResponse:
    """Exact typed continuation rows, one for each stopped fan exit."""

    output_types: Tuple[str, ...]
    exit_rows: Tuple[Tuple[str, Tuple[Fraction, ...]], ...]


def build_preexposure_unary_fan(
    h: Fraction,
    gamma: Fraction,
    a: Fraction,
    d: Fraction,
    unary_rates: Mapping[str, Fraction],
) -> UnaryRoutingFan:
    h, gamma, a, d = map(Fraction, (h, gamma, a, d))
    rates = tuple(sorted((str(name), Fraction(rate)) for name, rate in unary_rates.items()))
    if not (0 < h < a < d):
        raise ValueError("pre-exposure fan requires 0 < h < a < d")
    if not (0 < gamma < 1):
        raise ValueError("inheritance probability must lie in (0,1)")
    if not rates or any(rate <= 0 for _, rate in rates):
        raise ValueError("every unary-arm rate must be positive")
    return UnaryRoutingFan(
        lower_boundary=("x", Fraction(0), "one-block"),
        reticulation_time=h,
        first_exposure_ports=(
            ("T", a, "first-exposure", gamma),
            ("S", d, "first-exposure", 1 - gamma),
        ),
        internal_unary_rates=rates,
        maximum_internal_occupancy=1,
        internal_sample_entries=(),
    )


def extend_fan_across_actual_exposure(fan: UnaryRoutingFan) -> UnaryRoutingFan:
    """The invalid extension through z's entry and the exposed S--T epoch."""
    ports = {name: (time, weight) for name, time, _, weight in fan.first_exposure_ports}
    a = ports["T"][0]
    d = ports["S"][0]
    return UnaryRoutingFan(
        lower_boundary=fan.lower_boundary,
        reticulation_time=fan.reticulation_time,
        first_exposure_ports=(("S", d, "first-exposure", Fraction(1)),),
        internal_unary_rates=fan.internal_unary_rates,
        maximum_internal_occupancy=2,
        internal_sample_entries=(("z", "T", a),),
    )


def is_safe_preexposure_unary_fan(fan: UnaryRoutingFan) -> bool:
    """Require one-block occupancy and stop before every sampled side entry."""
    if fan.maximum_internal_occupancy > 1 or fan.internal_sample_entries:
        return False
    if fan.lower_boundary[2] != "one-block":
        return False
    if not fan.first_exposure_ports:
        return False
    if any(kind != "first-exposure" for _, _, kind, _ in fan.first_exposure_ports):
        return False
    if any(time <= fan.reticulation_time for _, time, _, _ in fan.first_exposure_ports):
        return False
    weights = tuple(weight for _, _, _, weight in fan.first_exposure_ports)
    if any(weight <= 0 for weight in weights) or sum(weights, Fraction(0)) != 1:
        return False
    if not fan.internal_unary_rates or any(rate <= 0 for _, rate in fan.internal_unary_rates):
        return False
    return True


def private_side_support_start(fan: UnaryRoutingFan) -> Fraction:
    """First time at which any routed block can meet a sampled side block."""
    if not is_safe_preexposure_unary_fan(fan):
        raise ValueError("support start is defined only for a safe stopped fan")
    return min(time for _, time, _, _ in fan.first_exposure_ports)


def q1_q7_unary_fan_signature(fan: UnaryRoutingFan) -> tuple:
    """The old move list retains the routing event's raw time endpoint."""
    stopping_ports = tuple(
        sorted(fan.first_exposure_ports, key=lambda item: (item[1], item[0], item[2]))
    )
    return ("Q1-Q7", fan.lower_boundary, fan.reticulation_time, stopping_ports)


def scalar_separated_fan_continuation(fan: UnaryRoutingFan) -> FanContinuationResponse:
    """Identity exit response used when the stopping ports are scalar separated."""
    ports = tuple(
        sorted(fan.first_exposure_ports, key=lambda item: (item[1], item[0], item[2]))
    )
    output_types = tuple(
        f"{name}@{time}:{kind}" for name, time, kind, _ in ports
    )
    exit_rows = tuple(
        (
            name,
            tuple(Fraction(index == column) for column in range(len(ports))),
        )
        for index, (name, _, _, _) in enumerate(ports)
    )
    return FanContinuationResponse(output_types, exit_rows)


def canonical_reachable_observable_response(
    fan: UnaryRoutingFan,
    continuation: FanContinuationResponse,
) -> tuple:
    """Compose routing weights with exact future rows and remove null columns."""
    ports = tuple(
        sorted(fan.first_exposure_ports, key=lambda item: (item[1], item[0], item[2]))
    )
    rows = {name: tuple(map(Fraction, row)) for name, row in continuation.exit_rows}
    if set(rows) != {name for name, _, _, _ in ports}:
        raise ValueError("continuation rows must match the stopped fan exits")
    if not continuation.output_types:
        raise ValueError("continuation must expose at least one typed output column")
    if any(len(row) != len(continuation.output_types) for row in rows.values()):
        raise ValueError("continuation row width does not match its typed columns")
    composed: Dict[str, Fraction] = {}
    for name, _, _, weight in ports:
        for output_type, value in zip(continuation.output_types, rows[name]):
            composed[output_type] = composed.get(output_type, Fraction(0)) + weight * value
    return tuple(
        (output_type, value)
        for output_type, value in sorted(composed.items())
        if value != 0
    )


def fan_slide_quotient_signature(
    fan: UnaryRoutingFan,
    continuation: FanContinuationResponse,
) -> tuple:
    """Q8 signature: canonical composed response, excluding unary internals."""
    if not is_safe_preexposure_unary_fan(fan):
        raise ValueError("Q8 cannot cross sampled side entry or two-block exposure")
    frontier = tuple(
        (name, time, kind)
        for name, time, kind, _ in sorted(
            fan.first_exposure_ports,
            key=lambda item: (item[1], item[0], item[2]),
        )
    )
    response = canonical_reachable_observable_response(fan, continuation)
    return ("Q8", fan.lower_boundary, frontier, response)


def fan_slide_equivalent(
    left: UnaryRoutingFan,
    right: UnaryRoutingFan,
    left_continuation: FanContinuationResponse,
    right_continuation: FanContinuationResponse,
) -> bool:
    return fan_slide_quotient_signature(
        left, left_continuation
    ) == fan_slide_quotient_signature(right, right_continuation)


HIDDEN_FAN_CARRIERS = ("immediate", "delayed")
FIXED_LOCAL_SAMPLE_COUNT = 6


def _jsonable_tuple(value):
    """Convert nested exact labels to one totally ordered immutable value."""
    if isinstance(value, tuple):
        return tuple(_jsonable_tuple(item) for item in value)
    if isinstance(value, list):
        return tuple(_jsonable_tuple(item) for item in value)
    if isinstance(value, dict):
        return tuple(
            (str(key), _jsonable_tuple(item))
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        )
    if isinstance(value, Fraction):
        return ("Fraction", value.numerator, value.denominator)
    return value


def _colored_canonical_code(graph: nx.MultiDiGraph) -> str:
    """Exact colored-MultiDiGraph code used by the exposure sweep.

    The graphs have at most eleven vertices.  Exhausting permutations inside
    equal color classes is therefore both bounded and stronger than relying on
    a probabilistic graph hash.  Edge multiplicity and every observable edge
    color are included.
    """
    node_colors: Dict[str, str] = {}
    for node, data in graph.nodes(data=True):
        color = json.dumps(
            _jsonable_tuple(data.get("observable_color")),
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
        node_colors[node] = color
    if not node_colors:
        raise ValueError("cannot canonicalize an empty exposure-decorated graph")

    edge_color_by_arc = {
        (tail, head, key): json.dumps(
            _jsonable_tuple(data.get("observable_color")),
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
        for tail, head, key, data in graph.edges(keys=True, data=True)
    }
    # Exact color refinement sharply reduces the factorial blocks while the
    # final exhaustive search below remains a complete canonicalization.
    refined = dict(node_colors)
    while True:
        signatures = {}
        for node in graph:
            outgoing = tuple(sorted(
                (edge_color_by_arc[(tail, head, key)], refined[head])
                for tail, head, key in graph.out_edges(node, keys=True)
            ))
            incoming = tuple(sorted(
                (edge_color_by_arc[(tail, head, key)], refined[tail])
                for tail, head, key in graph.in_edges(node, keys=True)
            ))
            signatures[node] = json.dumps(
                (refined[node], incoming, outgoing),
                separators=(",", ":"),
            )
        old_cells = len(set(refined.values()))
        new_cells = len(set(signatures.values()))
        refined = signatures
        if new_cells == old_cells:
            break
    color_classes: Dict[str, List[str]] = {}
    for node, color in refined.items():
        color_classes.setdefault(color, []).append(node)
    ordered_colors = tuple(sorted(color_classes))
    blocks = [
        tuple(permutations(sorted(color_classes[color], key=str)))
        for color in ordered_colors
    ]
    best = None
    for block_order in product(*blocks):
        order = tuple(node for block in block_order for node in block)
        adjacency = []
        for tail in order:
            for head in order:
                cell_edges = tuple(sorted(
                    edge_color_by_arc[(tail, head, key)]
                    for key in graph.get_edge_data(tail, head, default={})
                ))
                adjacency.append(cell_edges)
        candidate = (
            tuple(node_colors[node] for node in order),
            tuple(adjacency),
        )
        if best is None or candidate < best:
            best = candidate
    return json.dumps(best, separators=(",", ":"), default=str)


def _colored_isomorphic(left: nx.MultiDiGraph, right: nx.MultiDiGraph) -> bool:
    node_match = nx.algorithms.isomorphism.categorical_node_match(
        "observable_color", None
    )
    edge_match = nx.algorithms.isomorphism.categorical_multiedge_match(
        "observable_color", None
    )
    return nx.algorithms.isomorphism.MultiDiGraphMatcher(
        left,
        right,
        node_match=node_match,
        edge_match=edge_match,
    ).is_isomorphic()


def _audit_colored_collision_representatives(
    rows: Sequence[Mapping],
    collision_groups: Mapping[str, Sequence[int]],
) -> tuple[tuple[int, int], ...]:
    """Check every nonrepresentative in every canonical collision group."""
    failures = []
    for indices in collision_groups.values():
        representative = rows[indices[0]]["normalized_graph"]
        for index in indices[1:]:
            if not _colored_isomorphic(
                representative,
                rows[index]["normalized_graph"],
            ):
                failures.append((indices[0], index))
    return tuple(failures)


def _canonicalize_transported_route_record(record: tuple) -> tuple:
    """Re-canonicalize the set-valued anchors in one transported outlet."""
    if len(record) != 6:
        raise ValueError("a transported Q8 route record has the wrong arity")
    return (
        record[0],
        tuple(sorted(record[1], key=str)),
        record[2],
        record[3],
        record[4],
        record[5],
    )


def _canonicalize_transported_q8_payload(payload: tuple) -> tuple:
    """Sort transported typed outlets while carrying their exact weights."""
    if tuple(field[0] for field in payload) != (
        "lower-sampled-role",
        "route-wise-first-positive-exposure-frontier",
        "continuation-column-classes",
        "composite-route-polynomial",
    ):
        raise ValueError("a transported Q8 payload has the wrong schema")
    route_records = tuple(
        _canonicalize_transported_route_record(record)
        for record in payload[1][1]
    )
    continuation_classes = tuple(payload[2][1])
    response = tuple(payload[3][1])
    if continuation_classes and continuation_classes[0][0] == "future-null-class":
        ordered_routes = tuple(sorted(route_records, key=repr))
        return (
            payload[0],
            (payload[1][0], ordered_routes),
            (
                payload[2][0],
                ((
                    "future-null-class",
                    ordered_routes[0],
                ),),
            ),
            (payload[3][0], response),
        )
    weight_by_class = dict(response)
    paired = tuple(sorted((
        (
            _canonicalize_transported_route_record(record),
            weight_by_class[class_label],
        )
        for class_label, record in continuation_classes
    ), key=lambda pair: repr(pair[0])))
    ordered_routes = tuple(record for record, _ in paired)
    rebuilt_classes = tuple(
        (f"outlet-class-{index}", record)
        for index, record in enumerate(ordered_routes)
    )
    rebuilt_response = tuple(
        (f"outlet-class-{index}", weight)
        for index, (_, weight) in enumerate(paired)
    )
    return (
        payload[0],
        (payload[1][0], ordered_routes),
        (payload[2][0], rebuilt_classes),
        (payload[3][0], rebuilt_response),
    )


def _canonicalize_transported_observable_value(transported):
    """Restore canonical set/pair order after a sampled-label transport."""
    if not isinstance(transported, tuple) or not transported:
        return transported
    if transported[0] in {
        "q8-behavior-derived-macro",
        "declared-q8-response",
    }:
        return (
            transported[0],
            _canonicalize_transported_q8_payload(transported[1]),
        )
    if transported[0] == "exposed-routing-event":
        support = transported[3]
        if support[0] != "positive-two-block-support":
            raise ValueError("an exposed event has the wrong support schema")
        support = (
            support[0],
            tuple(sorted(support[1], key=str)),
            *support[2:],
        )
        return (*transported[:3], support, *transported[4:])
    if transported[0] in {
        "observable-two-block-entry",
        "observable-incoming-parking-entry",
    }:
        return (
            transported[0],
            tuple(sorted(transported[1], key=str)),
            *transported[2:],
        )
    return transported


def _transport_observable_value(value, label_permutation: Mapping[str, str]):
    if isinstance(value, str):
        return label_permutation.get(value, value)
    if isinstance(value, tuple):
        transported = tuple(
            _transport_observable_value(item, label_permutation)
            for item in value
        )
        return _canonicalize_transported_observable_value(transported)
    if isinstance(value, list):
        return [
            _transport_observable_value(item, label_permutation)
            for item in value
        ]
    if isinstance(value, dict):
        return {
            key: _transport_observable_value(item, label_permutation)
            for key, item in value.items()
        }
    return value


def _transport_colored_graph(
    graph: nx.MultiDiGraph,
    label_permutation: Mapping[str, str],
) -> nx.MultiDiGraph:
    transported = graph.copy()
    for _, data in transported.nodes(data=True):
        data["observable_color"] = _transport_observable_value(
            data["observable_color"],
            label_permutation,
        )
    for _, _, _, data in transported.edges(keys=True, data=True):
        data["observable_color"] = _transport_observable_value(
            data["observable_color"],
            label_permutation,
        )
    return transported


def _exposed_time_tag(
    graph: nx.MultiDiGraph,
    reticulation: str,
    exposed_reticulations: Sequence[str],
) -> tuple:
    """Canonical symbolic event tag, preserving comparable exposure order."""
    exposed = set(exposed_reticulations)
    older = sum(
        other != reticulation and nx.has_path(graph, other, reticulation)
        for other in exposed
    )
    younger = sum(
        other != reticulation and nx.has_path(graph, reticulation, other)
        for other in exposed
    )
    return ("exposed-time", older, younger)


def _edge_observable_color(
    graph: nx.MultiDiGraph,
    tail: str,
    head: str,
    data: Mapping,
) -> tuple:
    segment = data.get("segment")
    tail_color = graph.nodes[tail].get("observable_color", ())
    head_color = graph.nodes[head].get("observable_color", ())
    if segment == "sink_child":
        return ("compulsory-child-incidence", str(head))
    if isinstance(segment, str) and segment.startswith("port"):
        return ("repaired-segment-sample-incidence", segment)
    if tail_color and tail_color[0] == "repair-port":
        return ("repaired-segment-lower-half", tail_color[1])
    if head_color and head_color[0] == "repair-port":
        return ("repaired-segment-upper-half", head_color[1])
    return ("primitive-segment",)


def build_exposure_decorated_raw_carrier(
    core: Core,
    repair: Sequence[int],
    exposed_reticulations: Sequence[str],
    hidden_carriers: Mapping[str, str],
) -> nx.MultiDiGraph:
    """Build one exact raw carrier over a repaired primitive core.

    ``immediate`` and ``delayed`` are deliberately distinct hidden unary
    placements.  They are retained by this raw graph and may be removed only
    by the stopped-fan normalization below.
    """
    if not repair_satisfies_domain(core, repair):
        raise ValueError("exposure carrier requires a valid minimal repair")
    graph = build_repaired_core(core, repair)
    exposed = tuple(sorted(set(exposed_reticulations)))
    if not set(exposed).issubset(core.retics):
        raise ValueError("exposure mask contains a non-reticulation")
    hidden = set(core.retics).difference(exposed)
    if set(hidden_carriers) != hidden:
        raise ValueError("hidden carrier choices must cover exactly the unexposed reticulations")
    if any(choice not in HIDDEN_FAN_CARRIERS for choice in hidden_carriers.values()):
        raise ValueError("unknown hidden unary carrier")
    sources = [node for node in graph if graph.in_degree(node) == 0]
    if len(sources) != 1:
        raise ValueError("a repaired core must have one incoming-boundary source")
    source = sources[0]
    for node, data in graph.nodes(data=True):
        if node in core.retics:
            if node in exposed:
                color = (
                    "reticulation",
                    "exposed",
                    _exposed_time_tag(graph, node, exposed),
                )
            else:
                color = (
                    "reticulation",
                    "unexposed-raw",
                    hidden_carriers[node],
                )
            data["reticulation_name"] = node
        elif node == source:
            color = ("source", "incoming-boundary")
        elif str(node).startswith("p") and str(node)[1:].isdigit():
            color = ("repair-port", f"segment-{str(node)[1:]}")
        elif str(node).startswith("L") and str(node)[1:].isdigit():
            color = ("repair-port-child", f"sample-anchor-{str(node)[1:]}")
        elif str(node).startswith("C_"):
            color = ("compulsory-reticulation-child", str(node)[2:])
        elif data.get("role") == "leaf":
            color = ("sampled-child",)
        else:
            color = ("core-tree-event",)
        data["observable_color"] = color
    for tail, head, _, data in graph.edges(keys=True, data=True):
        data["observable_color"] = _edge_observable_color(graph, tail, head, data)
    graph.graph.update(
        core_name=core.name,
        repair=tuple(sorted(repair)),
        exposed_reticulations=exposed,
    )
    return graph


def _hidden_generic_color(color: tuple) -> tuple:
    if len(color) >= 2 and color[:2] == ("reticulation", "unexposed-raw"):
        return ("reticulation", "unexposed")
    return color


def _frontier_profile(
    raw: nx.MultiDiGraph,
    frontier_node: str,
    component: Sequence[str],
) -> str:
    """Exact typed continuation-column class for one stopped route."""
    residual = raw.copy()
    residual.remove_nodes_from(component)
    for node, data in residual.nodes(data=True):
        color = _hidden_generic_color(tuple(data["observable_color"]))
        if node == frontier_node:
            color = ("marked-first-exposure-frontier", color)
        data["observable_color"] = color
    return _colored_canonical_code(residual)


def _frontier_descriptor(
    raw: nx.MultiDiGraph,
    tail: str,
    head: str,
    key: str,
    component: Sequence[str],
) -> tuple:
    color = _hidden_generic_color(tuple(raw.nodes[tail]["observable_color"]))
    source = next(node for node in raw if raw.in_degree(node) == 0)
    if color[0] == "repair-port":
        time_type = ("repair-anchor-event",)
    elif color[:2] == ("reticulation", "exposed"):
        time_type = color[2]
    elif color[0] == "source":
        time_type = ("incoming-boundary-event",)
    else:
        time_type = (
            "core-event-depth",
            nx.shortest_path_length(raw, source, tail),
        )
    component_set = set(component)
    side_incidence = tuple(sorted(
        (
            tuple(data["observable_color"]),
            _hidden_generic_color(tuple(raw.nodes[child]["observable_color"])),
        )
        for _, child, edge_key, data in raw.out_edges(tail, keys=True, data=True)
        if child not in component_set and not (child == head and edge_key == key)
    ))
    edge_color = tuple(raw[tail][head][key]["observable_color"])
    return (color, time_type, edge_color, side_incidence)


def _unexposed_components(raw: nx.MultiDiGraph) -> tuple[tuple[str, ...], ...]:
    hidden = [
        node
        for node, data in raw.nodes(data=True)
        if tuple(data.get("observable_color", ()))[:2]
        == ("reticulation", "unexposed-raw")
    ]
    if not hidden:
        return ()
    adjacency = nx.Graph()
    adjacency.add_nodes_from(hidden)
    hidden_set = set(hidden)
    for tail, head in raw.edges():
        if tail in hidden_set and head in hidden_set:
            adjacency.add_edge(tail, head)
    return tuple(
        tuple(sorted(component, key=str))
        for component in nx.connected_components(adjacency)
    )


def _component_route_polynomials(
    raw: nx.MultiDiGraph,
    component: Sequence[str],
    variable_order: Sequence[str],
    parent_bits: Sequence[int],
) -> Dict[Tuple[str, str, str], sp.Expr]:
    component_set = set(component)
    outgoing = [
        (tail, head, key)
        for tail, head, key in raw.edges(keys=True)
        if tail in component_set and head not in component_set
    ]
    if len(outgoing) != 1:
        raise ValueError("a maximal singleton-routing fan must have one lower boundary")
    lowest = outgoing[0][0]
    variable_index = {node: index for index, node in enumerate(variable_order)}
    bit_by_node = {node: bit for node, bit in zip(variable_order, parent_bits)}
    external: Dict[Tuple[str, str, str], sp.Expr] = {}

    def walk(node: str, mass: sp.Expr) -> None:
        incoming = sorted(raw.in_edges(node, keys=True), key=lambda edge: tuple(map(str, edge)))
        if len(incoming) != 2:
            raise ValueError("every routing event in a fan must be binary")
        gamma = sp.Symbol(f"g{variable_index[node]}")
        gamma_edge = bit_by_node[node]
        for index, (tail, head, key) in enumerate(incoming):
            factor = gamma if index == gamma_edge else 1 - gamma
            updated = sp.expand(mass * factor)
            if tail in component_set:
                walk(tail, updated)
            else:
                boundary = (tail, head, key)
                external[boundary] = sp.expand(
                    external.get(boundary, sp.Integer(0)) + updated
                )

    walk(lowest, sp.Integer(1))
    if sp.simplify(sum(external.values(), sp.Integer(0)) - 1) != 0:
        raise AssertionError("composed route polynomial is not stochastic")
    return external


def _macro_payload(
    raw: nx.MultiDiGraph,
    component: Sequence[str],
    retain_hidden: bool = False,
) -> tuple:
    """Canonical first-hit macro, quotienting exact future-null columns."""
    component = tuple(component)
    component_set = set(component)
    outgoing = [
        (tail, head, key)
        for tail, head, key in raw.edges(keys=True)
        if tail in component_set and head not in component_set
    ]
    if len(outgoing) != 1:
        raise ValueError("a stopped fan must have one lower child boundary")
    _, lower_child, lower_key = outgoing[0]
    lower_role = (
        _hidden_generic_color(tuple(raw.nodes[lower_child]["observable_color"])),
        tuple(raw[outgoing[0][0]][lower_child][lower_key]["observable_color"]),
    )
    boundary_edges = sorted(
        (
            (tail, head, key)
            for tail, head, key in raw.edges(keys=True)
            if tail not in component_set and head in component_set
        ),
        key=lambda edge: tuple(map(str, edge)),
    )
    profiles = {
        edge: _frontier_profile(raw, edge[0], component)
        for edge in boundary_edges
    }
    profile_labels = {
        profile: f"continuation-class-{index}"
        for index, profile in enumerate(sorted(set(profiles.values())))
    }
    frontier = tuple(sorted(
        (
            _frontier_descriptor(raw, tail, head, key, component),
            profile_labels[profiles[(tail, head, key)]],
        )
        for tail, head, key in boundary_edges
    ))
    candidates = []
    for variable_order in permutations(component):
        for parent_bits in product((0, 1), repeat=len(component)):
            route_polynomials = _component_route_polynomials(
                raw,
                component,
                variable_order,
                parent_bits,
            )
            response: Dict[str, sp.Expr] = {}
            for edge, polynomial in route_polynomials.items():
                label = profile_labels[profiles[edge]]
                response[label] = sp.expand(
                    response.get(label, sp.Integer(0)) + polynomial
                )
            response_tuple = tuple(
                (label, sp.srepr(sp.simplify(polynomial)))
                for label, polynomial in sorted(response.items())
                if sp.simplify(polynomial) != 0
            )
            candidate = (
                ("lower-child-role", lower_role),
                ("route-wise-first-exposure-frontier", frontier),
                (
                    "continuation-column-classes",
                    tuple(
                        (profile_labels[profile], profile)
                        for profile in sorted(profile_labels)
                    ),
                ),
                ("composite-route-polynomial", response_tuple),
            )
            candidates.append(candidate)
    payload = min(candidates, key=repr)
    if retain_hidden:
        hidden = tuple(sorted(
            tuple(raw.nodes[node]["observable_color"])[2]
            for node in component
        ))
        payload = payload + (("hidden-carrier-words", hidden),)
    return payload


def _path_observable_word(
    graph: nx.MultiDiGraph,
    path: Sequence[str],
) -> tuple:
    word = []
    for tail, head in zip(path, path[1:]):
        edge_colors = tuple(sorted(
            tuple(data["observable_color"])
            for data in graph.get_edge_data(tail, head).values()
        ))
        word.append((
            _hidden_generic_color(tuple(graph.nodes[tail]["observable_color"])),
            edge_colors,
        ))
    word.append((
        _hidden_generic_color(tuple(graph.nodes[path[-1]]["observable_color"])),
        (),
    ))
    return tuple(word)


def _lowest_common_ancestors(
    graph: nx.MultiDiGraph,
    left: str,
    right: str,
) -> tuple[str, ...]:
    common = (
        set(nx.ancestors(graph, left)).union({left})
        .intersection(set(nx.ancestors(graph, right)).union({right}))
    )
    lowest = [
        node
        for node in common
        if not any(
            other != node and nx.has_path(graph, node, other)
            for other in common
        )
    ]
    if not lowest:
        raise ValueError("frontier route and anchor have no common ancestor")
    return tuple(sorted(lowest, key=str))


def _anchor_support_word(
    raw: nx.MultiDiGraph,
    outlet: str,
    anchor: str,
) -> tuple:
    """Structural marked-support word for one outlet/repair-anchor pair."""
    common = _lowest_common_ancestors(raw, outlet, anchor)
    source = next(node for node in raw if raw.in_degree(node) == 0)
    records = []
    for ancestor in common:
        outlet_paths = tuple(sorted(
            _path_observable_word(raw, path)
            for path in nx.all_shortest_paths(raw, ancestor, outlet)
        ))
        anchor_paths = tuple(sorted(
            _path_observable_word(raw, path)
            for path in nx.all_shortest_paths(raw, ancestor, anchor)
        ))
        records.append((
            _hidden_generic_color(tuple(raw.nodes[ancestor]["observable_color"])),
            nx.shortest_path_length(raw, source, ancestor),
            outlet_paths,
            anchor_paths,
        ))
    return (
        tuple(raw.nodes[anchor]["observable_color"]),
        tuple(sorted(records)),
    )


def _structural_fan_elimination_certificate(
    raw: nx.MultiDiGraph,
    component: Sequence[str],
) -> dict:
    """Find a metric-support triangularization from labelled repair anchors.

    This is deliberately a structural possibility certificate.  It does not
    assert that a fixed finite continuation family computes the nullspace of
    the complete marked-law operator.
    """
    component = tuple(component)
    component_set = set(component)
    outlets = tuple(sorted(
        (
            (tail, head, key)
            for tail, head, key in raw.edges(keys=True)
            if tail not in component_set and head in component_set
        ),
        key=lambda edge: tuple(map(str, edge)),
    ))
    profiles = {
        outlet: _frontier_profile(raw, outlet[0], component)
        for outlet in outlets
    }
    classes = tuple(sorted(set(profiles.values())))
    anchors = tuple(sorted(
        node
        for node, data in raw.nodes(data=True)
        if tuple(data["observable_color"])[0] == "repair-port"
    ))
    anchor_words = {
        (outlet, anchor): _anchor_support_word(raw, outlet[0], anchor)
        for outlet in outlets
        for anchor in anchors
    }
    exclusive_candidates = []
    if len(outlets) == 2 and len(classes) == 2:
        for anchor in anchors:
            meetings = tuple(
                _lowest_common_ancestors(raw, outlet[0], anchor)
                for outlet in outlets
            )
            if any(len(nodes) != 1 for nodes in meetings):
                continue
            first_meeting, second_meeting = meetings[0][0], meetings[1][0]
            if first_meeting == second_meeting:
                continue
            if nx.has_path(raw, first_meeting, second_meeting):
                older_index, private_index = 0, 1
            elif nx.has_path(raw, second_meeting, first_meeting):
                older_index, private_index = 1, 0
            else:
                continue
            older_meeting = meetings[older_index][0]
            private_meeting = meetings[private_index][0]
            interval_path = tuple(nx.shortest_path(
                raw,
                older_meeting,
                private_meeting,
            ))
            if len(interval_path) < 2:
                continue
            exclusive_candidates.append({
                "anchor": tuple(raw.nodes[anchor]["observable_color"]),
                "anchor_node": anchor,
                "private_outlet_index": private_index,
                "excluded_outlet_index": older_index,
                "private_outlet": outlets[private_index],
                "excluded_outlet": outlets[older_index],
                "private_profile": profiles[outlets[private_index]],
                "excluded_profile": profiles[outlets[older_index]],
                "private_meeting": _hidden_generic_color(
                    tuple(raw.nodes[private_meeting]["observable_color"])
                ),
                "private_meeting_node": private_meeting,
                "excluded_reconvergence": _hidden_generic_color(
                    tuple(raw.nodes[older_meeting]["observable_color"])
                ),
                "excluded_reconvergence_node": older_meeting,
                "positive_length_path": interval_path,
                "positive_length_path_word": _path_observable_word(
                    raw,
                    interval_path,
                ),
                "strict_event_order_edge_count": len(interval_path) - 1,
                "private_anchor_support_word": anchor_words[
                    (outlets[private_index], anchor)
                ],
                "excluded_anchor_support_word": anchor_words[
                    (outlets[older_index], anchor)
                ],
            })
    exclusive_candidates.sort(
        key=lambda candidate: (
            candidate["private_outlet_index"],
            repr(candidate["anchor"]),
        )
    )
    exclusive_interval = (
        None if not exclusive_candidates else exclusive_candidates[0]
    )
    selected = (
        () if exclusive_interval is None
        else (exclusive_interval["anchor_node"],)
    )
    typed_first_outlet_anchors = []
    for outlet_index, outlet in enumerate(outlets):
        candidates = [
            candidate for candidate in exclusive_candidates
            if candidate["private_outlet_index"] == outlet_index
        ]
        if candidates:
            candidate = candidates[0]
            typed_first_outlet_anchors.append({
                "kind": "sampled-repair-first-exposure-anchor",
                "anchor": candidate["anchor"],
                "outlet": outlet,
                "outlet_profile": profiles[outlet],
                "exclusive_interval_path": candidate["positive_length_path"],
                "coverage": tuple(
                    int(index == outlet_index) for index in range(len(outlets))
                ),
            })
        else:
            tail, head, key = outlet
            typed_first_outlet_anchors.append({
                "kind": "typed-incoming-boundary-first-outlet",
                "anchor": _frontier_descriptor(raw, tail, head, key, component),
                "outlet": outlet,
                "outlet_profile": profiles[outlet],
                "exclusive_interval_path": (),
                "coverage": tuple(
                    int(index == outlet_index) for index in range(len(outlets))
                ),
            })
    failures = []
    if len(component) != 1:
        failures.append("fan crosses more than one hidden reticulation")
    if len(outlets) > 2:
        failures.append("fan has more than two typed outlets")
    if len(classes) != len(outlets):
        failures.append("future-null outlet columns remain in theorem-class carrier")
    if len(outlets) == 2 and (selected is None or exclusive_interval is None):
        failures.append(
            "no positive-length interval shared by one outlet and a repair anchor "
            "strictly before the other outlet reconverges"
        )
    if len(typed_first_outlet_anchors) != len(outlets):
        failures.append("not every typed first-exposure outlet has an anchor")
    typed_coverage = tuple(
        tuple(anchor["coverage"])
        for anchor in typed_first_outlet_anchors
    )
    if len(outlets) == 2 and typed_coverage != ((1, 0), (0, 1)):
        failures.append("typed first-exposure anchors do not cover both outlets")

    ordered_profiles = ()
    marked_cells = ()
    possibility_matrix = ()
    symbolic_transition = ()
    symbolic_determinant = None
    if not failures:
        if len(classes) == 1:
            ordered_profiles = classes
            marked_cells = (("unique-outlet-continuation",),)
            possibility_matrix = ((1,),)
            symbolic_transition = (("1",),)
            symbolic_determinant = "1"
        else:
            assert exclusive_interval is not None and selected is not None
            private_profile = exclusive_interval["private_profile"]
            other_profile = exclusive_interval["excluded_profile"]
            ordered_profiles = (private_profile, other_profile)
            anchor = selected[0]
            marked_cells = (
                (
                    "anchor-tagged-private-support-interval",
                    tuple(raw.nodes[anchor]["observable_color"]),
                    exclusive_interval["private_anchor_support_word"],
                    exclusive_interval["positive_length_path_word"],
                ),
                (
                    "survive-private-interval-then-upper-word",
                    tuple(raw.nodes[anchor]["observable_color"]),
                    exclusive_interval["excluded_anchor_support_word"],
                ),
            )
            possibility_matrix = ((1, 1), (0, 1))
            symbolic_transition = (
                ("1-exp(-lambda*delta)", "exp(-lambda*delta)"),
                ("0", "1"),
            )
            symbolic_determinant = "1-exp(-lambda*delta)>0"
    return {
        "status": "PASS" if not failures else "POTENTIAL_COUNTEREXAMPLE",
        "hidden_reticulations": component,
        "hidden_reticulation_count": len(component),
        "typed_outlet_count": len(outlets),
        "continuation_column_class_count": len(classes),
        "future_null_dimension": len(outlets) - len(classes),
        "available_sampled_repair_anchors": tuple(
            tuple(raw.nodes[anchor]["observable_color"])
            for anchor in anchors
        ),
        "selected_sampled_repair_anchors": () if selected is None else tuple(
            tuple(raw.nodes[anchor]["observable_color"])
            for anchor in selected
        ),
        "weight_separating_anchor_count": len(selected),
        "selected_first_outlet_anchors": tuple(typed_first_outlet_anchors),
        "typed_first_outlet_anchor_count": len(typed_first_outlet_anchors),
        "typed_outlet_coverage_matrix": typed_coverage,
        "one_typed_anchor_covers_both_outlets": any(
            sum(anchor["coverage"]) == len(outlets)
            for anchor in typed_first_outlet_anchors
        ),
        "exclusive_anchor_candidate_count_by_outlet": tuple(
            sum(
                candidate["private_outlet_index"] == outlet_index
                for candidate in exclusive_candidates
            )
            for outlet_index in range(len(outlets))
        ),
        "exclusive_positive_length_interval": exclusive_interval,
        "ordered_outlet_class_profiles": ordered_profiles,
        "marked_support_cells": marked_cells,
        "outlet_by_cell_possibility_matrix": possibility_matrix,
        "symbolic_merge_survive_transition": symbolic_transition,
        "symbolic_determinant": symbolic_determinant,
        "failures": tuple(failures),
    }


def normalize_exposure_decorated_carrier(raw: nx.MultiDiGraph) -> nx.MultiDiGraph:
    """Collapse every maximal unexposed one-block component to its Q8 macro."""
    components = _unexposed_components(raw)
    payloads = {component: _macro_payload(raw, component) for component in components}
    normalized = raw.copy()
    for component_index, component in enumerate(components):
        component_set = set(component)
        incoming = [
            (tail, head, key, dict(data))
            for tail, head, key, data in normalized.edges(keys=True, data=True)
            if tail not in component_set and head in component_set
        ]
        outgoing = [
            (tail, head, key, dict(data))
            for tail, head, key, data in normalized.edges(keys=True, data=True)
            if tail in component_set and head not in component_set
        ]
        normalized.remove_nodes_from(component)
        macro = f"q8-macro:{component_index}"
        normalized.add_node(
            macro,
            role="q8_macro",
            observable_color=("q8-first-exposure-macro", payloads[component]),
        )
        for index, (tail, _, _, data) in enumerate(incoming):
            normalized.add_edge(
                tail,
                macro,
                key=f"macro-in:{component_index}:{index}",
                observable_color=("macro-route-incidence", data["observable_color"]),
            )
        for index, (_, head, _, data) in enumerate(outgoing):
            normalized.add_edge(
                macro,
                head,
                key=f"macro-out:{component_index}:{index}",
                observable_color=("macro-lower-incidence", data["observable_color"]),
            )
    for _, data in normalized.nodes(data=True):
        data["observable_color"] = _hidden_generic_color(
            tuple(data["observable_color"])
        )
    return normalized


def exposure_decorated_signature(raw: nx.MultiDiGraph) -> str:
    return _colored_canonical_code(normalize_exposure_decorated_carrier(raw))


def exposure_decorated_isomorphic(
    left_raw: nx.MultiDiGraph,
    right_raw: nx.MultiDiGraph,
) -> bool:
    """Independent mapped-response check for a claimed normalized collision."""
    return _colored_isomorphic(
        normalize_exposure_decorated_carrier(left_raw),
        normalize_exposure_decorated_carrier(right_raw),
    )


def _sampled_leaf_nodes(graph: nx.MultiDiGraph) -> tuple[str, ...]:
    return tuple(sorted(
        node for node, data in graph.nodes(data=True)
        if data.get("role") == "leaf"
    ))


def _descendant_samples(
    graph: nx.MultiDiGraph,
    node: str,
) -> set[str]:
    descendants = set(nx.descendants(graph, node)).union({node})
    return {
        sample for sample in _sampled_leaf_nodes(graph)
        if sample in descendants
    }


def _side_samples(
    graph: nx.MultiDiGraph,
    node: str,
    downstream: str,
    focal: str,
) -> tuple[str, ...]:
    samples = set()
    for _, child, _ in graph.out_edges(node, keys=True):
        if child == downstream:
            continue
        samples.update(_descendant_samples(graph, child))
    samples.discard(focal)
    return tuple(sorted(samples))


def _lower_path_is_singleton(
    graph: nx.MultiDiGraph,
    path: Sequence[str],
    focal: str,
) -> tuple[bool, tuple]:
    side_entries = []
    for node, downstream in zip(path, path[1:]):
        if node == path[0]:
            continue
        side = _side_samples(graph, node, downstream, focal)
        if side:
            side_entries.append((node, side))
    return not side_entries, tuple(side_entries)


def _trace_first_exposure(
    graph: nx.MultiDiGraph,
    reticulation: str,
    parent: str,
    focal: str,
) -> dict:
    current = parent
    downstream = reticulation
    backward_path = [parent]
    while True:
        side = _side_samples(graph, current, downstream, focal)
        if side:
            return {
                "status": "first-positive-side-block",
                "frontier": current,
                "sample_anchors": side,
                "backward_path": tuple(backward_path),
            }
        if graph.nodes[current].get("role") == "retic":
            return {
                "status": "crosses-second-retic-before-exposure",
                "frontier": current,
                "sample_anchors": (),
                "backward_path": tuple(backward_path),
            }
        predecessors = tuple(sorted(set(graph.predecessors(current)), key=str))
        if not predecessors:
            return {
                "status": "incoming-boundary",
                "frontier": current,
                "sample_anchors": (),
                "backward_path": tuple(backward_path),
            }
        if len(predecessors) != 1:
            return {
                "status": "nonunary-route-before-exposure",
                "frontier": current,
                "sample_anchors": (),
                "backward_path": tuple(backward_path),
            }
        downstream, current = current, predecessors[0]
        backward_path.append(current)


def behavioral_lower_cone_guard(
    graph: nx.MultiDiGraph,
    path: Sequence[str],
    focal: str,
) -> tuple[bool, tuple]:
    """Reject assigned masks that cross a lower retic or sampled side entry."""
    lower_reticulations = tuple(
        node for node in path[1:-1]
        if graph.nodes[node].get("role") == "retic"
    )
    singleton, side_entries = _lower_path_is_singleton(graph, path, focal)
    reasons = (
        ("lower-reticulations", lower_reticulations),
        ("sampled-side-entries", side_entries),
    )
    return not lower_reticulations and singleton, reasons


def behaviorally_realizable_unary_fans(
    graph: nx.MultiDiGraph,
) -> tuple[tuple[dict, ...], tuple[dict, ...]]:
    """Derive stopped singleton fans from sampled-leaf occupancy.

    No exposure mask is supplied.  A hidden event is admitted only for a
    focal sampled lineage whose path reaches that lowest reticulation without
    another reachable sampled side block.  Each parental route is then stopped
    at its first positive side block, incoming boundary, or second reticulation.
    """
    reticulations = tuple(sorted(
        node for node, data in graph.nodes(data=True)
        if data.get("role") == "retic"
    ))
    accepted = []
    rejected = []
    for focal in _sampled_leaf_nodes(graph):
        ancestors = tuple(
            reticulation for reticulation in reticulations
            if nx.has_path(graph, reticulation, focal)
        )
        for reticulation in ancestors:
            paths = tuple(
                tuple(path)
                for path in nx.all_simple_paths(graph, reticulation, focal)
            )
            singleton_paths = []
            path_rejections = []
            for path in paths:
                admissible, reasons = behavioral_lower_cone_guard(
                    graph,
                    path,
                    focal,
                )
                if admissible:
                    singleton_paths.append(path)
                else:
                    path_rejections.append((path, reasons))
            if len(singleton_paths) != 1:
                crosses_lower_retic = any(
                    any(reason[0] == "lower-reticulations" and reason[1]
                        for reason in reasons)
                    for _, reasons in path_rejections
                )
                rejected.append({
                    "focal": focal,
                    "reticulation": reticulation,
                    "reason": (
                        "lower-reticulation-before-candidate"
                        if crosses_lower_retic
                        else "lower-cone-not-unique-singleton"
                    ),
                    "singleton_path_count": len(singleton_paths),
                    "path_rejections": tuple(path_rejections),
                })
                continue
            parents = tuple(sorted(set(graph.predecessors(reticulation)), key=str))
            routes = tuple(
                _trace_first_exposure(graph, reticulation, parent, focal)
                for parent in parents
            )
            if len(parents) != 2 or any(
                route["status"]
                in {
                    "crosses-second-retic-before-exposure",
                    "nonunary-route-before-exposure",
                }
                for route in routes
            ):
                rejected.append({
                    "focal": focal,
                    "reticulation": reticulation,
                    "reason": "route-not-stopped-before-next-routing-event",
                    "routes": routes,
                })
                continue
            accepted.append({
                "focal": focal,
                "reticulation": reticulation,
                "lower_path": singleton_paths[0],
                "maximum_internal_occupancy": 1,
                "internal_sample_entries": (),
                "parents": parents,
                "routes": routes,
            })
    return tuple(accepted), tuple(rejected)


def _observable_sample_label_maps(
    graph: nx.MultiDiGraph,
) -> tuple[dict[str, str], ...]:
    leaves = _sampled_leaf_nodes(graph)
    labels = tuple(f"sample-{index}" for index in range(len(leaves)))
    return tuple(
        dict(zip(leaves, assignment))
        for assignment in permutations(labels)
    )


def _generic_role(graph: nx.MultiDiGraph, node: str) -> str:
    if graph.in_degree(node) == 0:
        return "source"
    role = graph.nodes[node].get("role")
    if role == "leaf":
        return "sample"
    if role == "retic":
        return "retic"
    return "tree"


def _behavioral_path_word(
    graph: nx.MultiDiGraph,
    path: Sequence[str],
    sample_labels: Mapping[str, str],
) -> tuple:
    # Positive unary epoch boundaries are internal to Q8.  Their number,
    # metric placement, and rate word must not survive in the first-hit macro.
    observable_path = tuple(
        node for node in path
        if graph.nodes[node].get("role") != "unary"
    )
    return tuple(
        ("sample", sample_labels[node])
        if node in sample_labels
        else (_generic_role(graph, node),)
        for node in observable_path
    )


def _exact_time_tag(value) -> tuple:
    value = Fraction(value)
    return ("exact-time", value.numerator, value.denominator)


def _global_retained_event_order_tag(
    graph: nx.MultiDiGraph,
    node: str,
) -> tuple:
    """Global strict order type after deleting hidden clocks/unary fan words."""
    retained = []
    for candidate, data in graph.nodes(data=True):
        if graph.out_degree(candidate) == 0 or data.get("role") in {"unary", "macro"}:
            continue
        if data.get("role") == "retic" and _positive_two_block_support(
            graph,
            candidate,
        ) is None:
            continue
        retained.append(candidate)
    if "event_time" not in graph.nodes[node]:
        return (
            "global-retained-partial-order",
            sum(
                other != node and nx.has_path(graph, other, node)
                for other in retained
            ),
            sum(
                other != node and nx.has_path(graph, node, other)
                for other in retained
            ),
            len(retained),
        )
    ordered = tuple(sorted(
        retained,
        key=lambda candidate: Fraction(graph.nodes[candidate]["event_time"]),
        reverse=True,
    ))
    if len({graph.nodes[candidate]["event_time"] for candidate in ordered}) != len(ordered):
        raise AssertionError("retained event order is not temporally separated")
    return (
        "global-retained-strict-order",
        ordered.index(node),
        len(ordered),
    )


def _behavioral_route_records(
    graph: nx.MultiDiGraph,
    fan: Mapping,
    sample_labels: Mapping[str, str],
) -> tuple:
    frontiers = tuple(route["frontier"] for route in fan["routes"])
    records = []
    for route_index, route in enumerate(fan["routes"]):
        frontier = route["frontier"]
        time_order = (
            "frontier-time-order",
            sum(
                other != frontier and nx.has_path(graph, other, frontier)
                for other in frontiers
            ),
            sum(
                other != frontier and nx.has_path(graph, frontier, other)
                for other in frontiers
            ),
        )
        incidence = (
            "frontier-incidence",
            _generic_role(graph, frontier),
            graph.in_degree(frontier),
            graph.out_degree(frontier),
        )
        frontier_time = _global_retained_event_order_tag(graph, frontier)
        records.append((
            route["status"],
            tuple(sorted(sample_labels[sample] for sample in route["sample_anchors"])),
            time_order,
            frontier_time,
            incidence,
            _behavioral_path_word(graph, route["backward_path"], sample_labels),
        ))
    return tuple(records)


def _behavioral_macro_payload(
    graph: nx.MultiDiGraph,
    fan: Mapping,
    sample_labels: Mapping[str, str],
) -> tuple:
    ordered_route_records = _behavioral_route_records(graph, fan, sample_labels)
    typed_pairs = []
    for parent, record in zip(fan["parents"], ordered_route_records):
        parent_edges = tuple(
            data
            for tail, _, _, data in graph.in_edges(
                fan["reticulation"], keys=True, data=True
            )
            if tail == parent
        )
        if len(parent_edges) != 1:
            raise ValueError("typed fan parent does not determine one inheritance edge")
        weight = Fraction(parent_edges[0].get("inheritance_probability", Fraction(1, 2)))
        typed_pairs.append((record, weight))
    typed_pairs = tuple(sorted(typed_pairs, key=lambda pair: repr(pair[0])))
    route_records = tuple(record for record, _ in typed_pairs)
    if len(set(route_records)) != len(route_records):
        continuation_classes = (("future-null-class", route_records[0]),)
        response = ((
            "future-null-class",
            sp.srepr(sp.Rational(sum(weight for _, weight in typed_pairs))),
        ),)
    else:
        continuation_classes = tuple(
            (f"outlet-class-{index}", record)
            for index, record in enumerate(route_records)
        )
        response = tuple(
            (
                continuation_classes[index][0],
                sp.srepr(sp.Rational(weight.numerator, weight.denominator)),
            )
            for index, (_, weight) in enumerate(typed_pairs)
        )
    return (
        ("lower-sampled-role", sample_labels[fan["focal"]]),
        (
            "route-wise-first-positive-exposure-frontier",
            route_records,
        ),
        ("continuation-column-classes", continuation_classes),
        ("composite-route-polynomial", response),
    )


def _independent_behavioral_macro_payload(
    graph: nx.MultiDiGraph,
    fan: Mapping,
    sample_labels: Mapping[str, str],
) -> tuple:
    """Independent primitive-record construction of the same Q8 response."""
    frontiers = tuple(route["frontier"] for route in fan["routes"])
    records = []
    for route in fan["routes"]:
        frontier = route["frontier"]
        forced_order = (
            "frontier-time-order",
            sum(
                other != frontier and nx.has_path(graph, other, frontier)
                for other in frontiers
            ),
            sum(
                other != frontier and nx.has_path(graph, frontier, other)
                for other in frontiers
            ),
        )
        reduced_path = tuple(
            node for node in route["backward_path"]
            if graph.nodes[node].get("role") != "unary"
        )
        path_word = tuple(
            ("sample", sample_labels[node])
            if node in sample_labels
            else (_generic_role(graph, node),)
            for node in reduced_path
        )
        records.append((
            route["status"],
            tuple(sorted(sample_labels[sample] for sample in route["sample_anchors"])),
            forced_order,
            _global_retained_event_order_tag(graph, frontier),
            (
                "frontier-incidence",
                _generic_role(graph, frontier),
                graph.in_degree(frontier),
                graph.out_degree(frontier),
            ),
            path_word,
        ))
    typed_pairs = []
    for parent, record in zip(fan["parents"], records):
        matching_edges = tuple(
            data
            for tail, _, _, data in graph.in_edges(
                fan["reticulation"], keys=True, data=True
            )
            if tail == parent
        )
        if len(matching_edges) != 1:
            raise ValueError("independent typed parent-edge lookup is not unique")
        typed_pairs.append((
            record,
            Fraction(matching_edges[0].get("inheritance_probability", Fraction(1, 2))),
        ))
    typed_pairs = tuple(sorted(typed_pairs, key=lambda pair: repr(pair[0])))
    route_records = tuple(record for record, _ in typed_pairs)
    if len(set(route_records)) == 1:
        continuation_classes = (("future-null-class", route_records[0]),)
        response = ((
            "future-null-class",
            sp.srepr(sp.Rational(sum(weight for _, weight in typed_pairs))),
        ),)
    else:
        continuation_classes = tuple(
            (f"outlet-class-{index}", record)
            for index, record in enumerate(route_records)
        )
        response = tuple(
            (
                continuation_classes[index][0],
                sp.srepr(sp.Rational(weight.numerator, weight.denominator)),
            )
            for index, (_, weight) in enumerate(typed_pairs)
        )
    return (
        ("lower-sampled-role", sample_labels[fan["focal"]]),
        ("route-wise-first-positive-exposure-frontier", route_records),
        ("continuation-column-classes", continuation_classes),
        ("composite-route-polynomial", response),
    )


def _declared_primitive_quotient_graph(
    primitive_occupancy: nx.MultiDiGraph,
    state: Mapping,
    sample_labels: Mapping[str, str],
) -> nx.MultiDiGraph:
    """Declare Q7/Q8 orbits without invoking normalization or expected codes."""
    declared = primitive_occupancy.copy()
    hidden_by_reticulation = {
        fan["reticulation"]: fan for fan in state["hidden_fans"]
    }
    for node, data in declared.nodes(data=True):
        role = _generic_role(primitive_occupancy, node)
        if role == "sample":
            color = ("sample", sample_labels[node])
        elif node in hidden_by_reticulation:
            color = (
                "declared-q8-response",
                _independent_behavioral_macro_payload(
                    primitive_occupancy,
                    hidden_by_reticulation[node],
                    sample_labels,
                ),
            )
        else:
            color = _external_observable_color(
                primitive_occupancy,
                node,
                sample_labels,
            )
        data["observable_color"] = color
    for tail, head, _, data in declared.edges(keys=True, data=True):
        data["observable_color"] = _external_edge_observable_color(
            primitive_occupancy,
            tail,
            head,
            data,
        )
    return declared


def _declared_orbit_bucket(graph: nx.MultiDiGraph) -> tuple:
    node_profiles = tuple(sorted(
        (
            repr(_jsonable_tuple(data["observable_color"])),
            graph.in_degree(node),
            graph.out_degree(node),
        )
        for node, data in graph.nodes(data=True)
    ))
    return (graph.number_of_nodes(), graph.number_of_edges(), node_profiles)


def _enumerate_declared_primitive_orbits(
    configuration_records: Sequence[dict],
) -> tuple[tuple[dict, ...], int]:
    """Exact orbit enumeration by primitive colored MultiDiGraph mappings."""
    representatives: Dict[tuple, List[tuple[int, nx.MultiDiGraph]]] = {}
    witnesses = []
    orbit_count = 0
    for record_index, record in enumerate(configuration_records):
        graph = record["declared_quotient_graph"]
        bucket = _declared_orbit_bucket(graph)
        matched = None
        matched_mapping = None
        for orbit_id, representative in representatives.get(bucket, []):
            matcher = nx.algorithms.isomorphism.MultiDiGraphMatcher(
                representative,
                graph,
                node_match=nx.algorithms.isomorphism.categorical_node_match(
                    "observable_color",
                    None,
                ),
                edge_match=nx.algorithms.isomorphism.categorical_multiedge_match(
                    "observable_color",
                    None,
                ),
            )
            if matcher.is_isomorphic():
                matched = orbit_id
                matched_mapping = tuple(sorted(
                    (str(left), str(right))
                    for left, right in matcher.mapping.items()
                ))
                break
        if matched is None:
            matched = orbit_count
            orbit_count += 1
            representatives.setdefault(bucket, []).append((matched, graph))
            matched_mapping = tuple((str(node), str(node)) for node in graph)
        record["declared_primitive_orbit_id"] = matched
        witnesses.append({
            "record_index": record_index,
            "declared_primitive_orbit_id": matched,
            "primitive_automorphism_mapping": matched_mapping,
            "hidden_carrier_words_forgotten": True,
        })
    return tuple(witnesses), orbit_count


def _relative_label_orbit_audit(
    configuration_records: Sequence[dict],
) -> dict:
    """Exhaust all 6! relative label placements on reduced primitive records."""
    labels = tuple(f"sample-{index}" for index in range(FIXED_LOCAL_SAMPLE_COUNT))
    expected_groups: Dict[str, List[tuple[int, tuple[int, ...]]]] = {}
    placement_count = 0
    for record_index, record in enumerate(configuration_records):
        for permutation in permutations(range(FIXED_LOCAL_SAMPLE_COUNT)):
            transport = {
                labels[index]: labels[permutation[index]]
                for index in range(FIXED_LOCAL_SAMPLE_COUNT)
            }
            transported_expected = _transport_colored_graph(
                record["expected_graph"],
                transport,
            )
            code = _colored_canonical_code(transported_expected)
            expected_groups.setdefault(code, []).append((record_index, permutation))
            placement_count += 1
    failures = []
    collision_groups = 0
    primitive_mapping_checks = 0
    for entries in expected_groups.values():
        if len(entries) <= 1:
            continue
        collision_groups += 1
        representative_index, representative_permutation = entries[0]
        representative_transport = {
            labels[index]: labels[representative_permutation[index]]
            for index in range(FIXED_LOCAL_SAMPLE_COUNT)
        }
        representative = _transport_colored_graph(
            configuration_records[representative_index]["declared_quotient_graph"],
            representative_transport,
        )
        for record_index, permutation in entries[1:]:
            transport = {
                labels[index]: labels[permutation[index]]
                for index in range(FIXED_LOCAL_SAMPLE_COUNT)
            }
            declared = _transport_colored_graph(
                configuration_records[record_index]["declared_quotient_graph"],
                transport,
            )
            primitive_mapping_checks += 1
            if not _colored_isomorphic(representative, declared):
                failures.append({
                    "representative_record": representative_index,
                    "record": record_index,
                    "relative_permutation": permutation,
                })
    return {
        "fixed_sample_count": FIXED_LOCAL_SAMPLE_COUNT,
        "symmetric_group_order": len(tuple(permutations(labels))),
        "relative_label_placement_count": placement_count,
        "reduced_expected_signature_count": len(expected_groups),
        "relative_collision_group_count": collision_groups,
        "primitive_automorphism_mapping_checks": primitive_mapping_checks,
        "failures": tuple(failures),
    }


def _q8_weight_certificate(
    graph: nx.MultiDiGraph,
    state: Mapping,
    sample_labels: Mapping[str, str],
) -> tuple[dict, ...]:
    certificates = []
    for fan in state["hidden_fans"]:
        reticulation = fan["reticulation"]
        gamma = Fraction(graph.nodes[reticulation]["inheritance_probability"])
        actual = _behavioral_macro_payload(graph, fan, sample_labels)
        independent = _independent_behavioral_macro_payload(graph, fan, sample_labels)
        altered_graph = graph.copy()
        altered = Fraction(2, 5) if gamma not in {Fraction(2, 5), Fraction(3, 5)} else Fraction(1, 3)
        altered_graph.nodes[reticulation]["inheritance_probability"] = altered
        altered_edges = tuple(sorted(
            altered_graph.in_edges(reticulation, keys=True, data=True),
            key=lambda edge: tuple(map(str, edge[:3])),
        ))
        altered_edges[0][3]["inheritance_probability"] = altered
        altered_edges[1][3]["inheritance_probability"] = 1 - altered
        altered_response = _behavioral_macro_payload(
            altered_graph,
            fan,
            sample_labels,
        )
        complemented_graph = graph.copy()
        complemented_edges = tuple(sorted(
            complemented_graph.in_edges(reticulation, keys=True, data=True),
            key=lambda edge: tuple(map(str, edge[:3])),
        ))
        original_weights = tuple(
            Fraction(edge[3]["inheritance_probability"])
            for edge in complemented_edges
        )
        complemented_edges[0][3]["inheritance_probability"] = original_weights[1]
        complemented_edges[1][3]["inheritance_probability"] = original_weights[0]
        complemented_response = _behavioral_macro_payload(
            complemented_graph,
            fan,
            sample_labels,
        )
        parent_rename = {
            fan["parents"][0]: f"presentation-exchange:{fan['parents'][1]}",
            fan["parents"][1]: f"presentation-exchange:{fan['parents'][0]}",
        }
        renamed_graph = nx.relabel_nodes(graph, parent_rename, copy=True)
        renamed_fans, _ = behaviorally_realizable_unary_fans(renamed_graph)
        renamed_fan = next(
            candidate for candidate in renamed_fans
            if candidate["reticulation"] == reticulation
            and candidate["focal"] == fan["focal"]
        )
        renamed_response = _behavioral_macro_payload(
            renamed_graph,
            renamed_fan,
            sample_labels,
        )
        certificates.append({
            "gamma": gamma,
            "strictly_internal": 0 < gamma < 1,
            "actual_equals_independent_typed_response": actual == independent,
            "altered_gamma": altered,
            "different_nonexchange_weight_changes_response": actual != altered_response,
            "fixed_typed_outlet_complement_changes_response": (
                gamma == Fraction(1, 2) or actual != complemented_response
            ),
            "true_parent_presentation_relabel_preserves_response": (
                actual == renamed_response
            ),
            "typed_response": actual[-1][1],
        })
    return tuple(certificates)


def _normalizer_label_generator_audit(
    configuration_records: Sequence[dict],
    rows: Sequence[dict],
) -> dict:
    """Check the five adjacent generators whose closure is the full S6 action."""
    row_by_origin = {}
    for row in rows:
        origin = (
            row["core"],
            row["repair"],
            row["sample_attachment"],
            row["hidden_focal_samples"],
        )
        row_by_origin.setdefault(origin, row)
    labels = tuple(f"sample-{index}" for index in range(FIXED_LOCAL_SAMPLE_COUNT))
    failures = []
    audit_count = 0
    for record in configuration_records:
        origin = (
            record["core"],
            record["repair"],
            record["sample_attachment"],
            record["hidden_focal_samples"],
        )
        baseline = row_by_origin[origin]["normalized_graph"]
        for index in range(FIXED_LOCAL_SAMPLE_COUNT - 1):
            transport = {label: label for label in labels}
            transport[labels[index]] = labels[index + 1]
            transport[labels[index + 1]] = labels[index]
            transported_labels = {
                node: transport[label]
                for node, label in record["sample_labels"].items()
            }
            occupancy = _build_behavioral_occupancy_graph(
                record["core_object"],
                record["repair"],
                record["side_entry_reticulations"],
            )
            actual = _expand_actual_hidden_carriers(
                occupancy,
                {
                    reticulation: "immediate"
                    for reticulation in record["hidden_reticulations"]
                },
            )
            state = _derive_joint_occupancy_state(actual)
            normalized = _normalize_actual_joint_carrier(
                actual,
                state["hidden_fans"],
                transported_labels,
            )
            expected_transport = _transport_colored_graph(baseline, transport)
            audit_count += 1
            if (
                _colored_canonical_code(normalized)
                != _colored_canonical_code(expected_transport)
                or not _colored_isomorphic(normalized, expected_transport)
            ):
                failures.append({
                    "origin": origin,
                    "adjacent_transposition": (index, index + 1),
                })
    return {
        "adjacent_generator_count": FIXED_LOCAL_SAMPLE_COUNT - 1,
        "generated_group_order": len(tuple(permutations(labels))),
        "audit_count": audit_count,
        "failures": tuple(failures),
    }


def _behavioral_carrier_graph(
    graph: nx.MultiDiGraph,
    fan: Mapping,
    sample_labels: Mapping[str, str],
    carrier: str,
    *,
    normalized: bool,
    bake_internal_names: bool = False,
) -> nx.MultiDiGraph:
    """Backward-compatible one-fan wrapper around the joint construction."""
    return _behavioral_joint_carrier_graph(
        graph,
        (fan,),
        sample_labels,
        {fan["reticulation"]: carrier},
        normalized=normalized,
        bake_internal_names=bake_internal_names,
    )


def _behavioral_fan_interior_nodes(fan: Mapping) -> frozenset[str]:
    """Nodes strictly internal to a stopped pre-exposure routing fan.

    The sampled lower endpoint and each first-exposure frontier are boundary
    ports.  Everything between those ports is part of the replaceable unary
    routing module.  This definition makes compatibility a graph property,
    rather than an independently assigned exposure bit.
    """
    nodes = set(fan["lower_path"][:-1])
    for route in fan["routes"]:
        nodes.update(route["backward_path"][:-1])
    return frozenset(nodes)


def behaviorally_realizable_joint_configurations(
    graph: nx.MultiDiGraph,
) -> tuple[tuple[tuple[dict, ...], ...], tuple[dict, ...]]:
    """Enumerate all compatible joint hidden-fan configurations.

    Candidate fans first have to pass the sampled-reachability/occupancy
    derivation in :func:`behaviorally_realizable_unary_fans`.  Joint cases are
    then formed only from collections with disjoint replaceable interiors and
    distinct sampled lower boundary ports.  The empty collection is the fully
    exposed configuration.  No reticulation exposure mask is an input.
    """
    fans, rejected = behaviorally_realizable_unary_fans(graph)
    configurations = []
    joint_rejections = list(rejected)
    for size in range(len(fans) + 1):
        for candidate in combinations(fans, size):
            interiors = tuple(_behavioral_fan_interior_nodes(fan) for fan in candidate)
            reticulations = tuple(fan["reticulation"] for fan in candidate)
            focals = tuple(fan["focal"] for fan in candidate)
            overlap = tuple(
                sorted(interiors[left] & interiors[right], key=str)
                for left, right in combinations(range(size), 2)
                if interiors[left] & interiors[right]
            )
            if (
                len(set(reticulations)) != size
                or len(set(focals)) != size
                or overlap
            ):
                joint_rejections.append({
                    "reason": "joint-fan-interiors-not-disjoint",
                    "reticulations": reticulations,
                    "focals": focals,
                    "overlap": overlap,
                })
                continue
            configurations.append(tuple(sorted(
                candidate,
                key=lambda fan: (str(fan["focal"]), str(fan["reticulation"])),
            )))
    return tuple(configurations), tuple(joint_rejections)


def _behavioral_joint_carrier_graph(
    graph: nx.MultiDiGraph,
    hidden_fans: Sequence[Mapping],
    sample_labels: Mapping[str, str],
    carrier_by_reticulation: Mapping[str, str],
    *,
    normalized: bool,
    bake_internal_names: bool = False,
) -> nx.MultiDiGraph:
    """Color every simultaneously hidden fan by its raw word or Q8 response."""
    decorated = graph.copy()
    reticulations = tuple(
        node for node, data in graph.nodes(data=True)
        if data.get("role") == "retic"
    )
    hidden_by_reticulation = {
        fan["reticulation"]: fan for fan in hidden_fans
    }
    if len(hidden_by_reticulation) != len(hidden_fans):
        raise ValueError("a joint configuration repeats a routing event")
    if set(carrier_by_reticulation) != set(hidden_by_reticulation):
        raise ValueError("every and only hidden routing events need a carrier word")
    for node, data in decorated.nodes(data=True):
        role = _generic_role(graph, node)
        if role == "sample":
            color = ("sample", sample_labels[node])
        elif node in hidden_by_reticulation:
            fan = hidden_by_reticulation[node]
            if normalized:
                color = (
                    "q8-behavior-derived-macro",
                    _behavioral_macro_payload(graph, fan, sample_labels),
                )
            else:
                color = (
                    "hidden-routing-event-raw",
                    carrier_by_reticulation[node],
                )
        elif role == "retic":
            color = (
                "exposed-routing-event",
                sum(
                    other != node and nx.has_path(graph, other, node)
                    for other in reticulations
                ),
                sum(
                    other != node and nx.has_path(graph, node, other)
                    for other in reticulations
                ),
            )
        elif role == "source":
            color = ("source", "incoming-boundary")
        else:
            color = ("tree-event",)
        if bake_internal_names and role != "sample":
            color = color + (("internal-name", str(node)),)
        data["observable_color"] = color
    for _, _, _, data in decorated.edges(keys=True, data=True):
        data["observable_color"] = ("population-incidence",)
    return decorated


def _unique_reticulation_child(
    graph: nx.MultiDiGraph,
    reticulation: str,
) -> str:
    children = tuple(sorted(set(graph.successors(reticulation)), key=str))
    if len(children) != 1:
        raise ValueError(
            f"{reticulation!r} does not have one population child: {children!r}"
        )
    return children[0]


def _assign_strict_event_times(
    graph: nx.MultiDiGraph,
    *,
    reverse_incomparable_order: bool = False,
) -> None:
    """Assign distinct exact event times and contemporaneous sample time zero."""
    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("a temporal carrier must be acyclic")
    ordering_graph = nx.DiGraph(graph)
    if reverse_incomparable_order:
        reticulations = tuple(sorted((
            node for node, data in graph.nodes(data=True)
            if data.get("role") == "retic"
        ), key=str))
        incomparable = tuple(
            (left, right)
            for left, right in combinations(reticulations, 2)
            if not nx.has_path(ordering_graph, left, right)
            and not nx.has_path(ordering_graph, right, left)
        )
        if len(incomparable) > 1:
            raise ValueError("bounded order audit supports at most two reticulations")
        if incomparable:
            left, right = incomparable[0]
            baseline = tuple(nx.lexicographical_topological_sort(ordering_graph, key=str))
            baseline_older, baseline_younger = (
                (left, right)
                if baseline.index(left) < baseline.index(right)
                else (right, left)
            )
            ordering_graph.add_edge(baseline_younger, baseline_older)
            if not nx.is_directed_acyclic_graph(ordering_graph):
                raise AssertionError("incomparable retic precedence constraint made a cycle")
    topological = tuple(nx.lexicographical_topological_sort(ordering_graph, key=str))
    events = tuple(node for node in topological if graph.out_degree(node) > 0)
    event_count = len(events)
    for index, node in enumerate(events):
        graph.nodes[node]["event_time"] = Fraction(10 * (event_count - index), 1)
    for node in graph:
        if graph.out_degree(node) == 0:
            graph.nodes[node]["event_time"] = Fraction(0, 1)


def _add_explicit_two_block_support(
    graph: nx.MultiDiGraph,
    reticulation: str,
) -> None:
    """Add a sampled side entry below a reticulation, making exposure observable."""
    child = _unique_reticulation_child(graph, reticulation)
    edges = tuple(
        (key, dict(data))
        for key, data in graph.get_edge_data(reticulation, child).items()
    )
    if len(edges) != 1:
        raise ValueError("a reticulation child boundary must be a single raw arc")
    key, data = edges[0]
    graph.remove_edge(reticulation, child, key=key)
    entry = f"occupancy-entry:{reticulation}"
    companion = f"occupancy-sample:{reticulation}"
    graph.add_node(
        entry,
        role="tree",
        exposure_owner=reticulation,
    )
    graph.add_node(
        companion,
        role="leaf",
        exposure_owner=reticulation,
        companion_of=child,
    )
    graph.add_edge(reticulation, entry, key=f"exposure:{reticulation}:upper", **data)
    graph.add_edge(entry, child, key=f"exposure:{reticulation}:lower", **data)
    graph.add_edge(
        entry,
        companion,
        key=f"exposure:{reticulation}:sample",
        segment="observable-two-block-side-entry",
    )


def _add_incoming_parking_sample(
    graph: nx.MultiDiGraph,
    slot: str,
) -> None:
    sources = tuple(node for node in graph if graph.in_degree(node) == 0)
    if len(sources) != 1:
        raise ValueError("a parking scaffold needs one incoming source")
    old_source = sources[0]
    new_source = f"parking-entry:{slot}"
    sample = f"parking-sample:{slot}"
    graph.add_node(new_source, role="tree", parking_slot=slot)
    graph.add_node(sample, role="leaf", parking_slot=slot)
    graph.add_edge(
        new_source,
        old_source,
        key=f"parking:{slot}:continuation",
        segment="observable-parking-continuation",
    )
    graph.add_edge(
        new_source,
        sample,
        key=f"parking:{slot}:sample",
        segment="observable-parking-sample",
    )


def _build_behavioral_occupancy_graph(
    core: Core,
    repair: Sequence[int],
    side_entry_reticulations: Sequence[str],
    *,
    reverse_incomparable_order: bool = False,
) -> nx.MultiDiGraph:
    """Build one raw sampled-port configuration, before exposure is classified."""
    graph = build_repaired_core(core, repair)
    side_entries = set(side_entry_reticulations)
    if not side_entries.issubset(core.retics):
        raise ValueError("sampled side-entry set contains a nonreticulation")
    for reticulation in sorted(side_entries, key=str):
        _add_explicit_two_block_support(graph, reticulation)
    for reticulation in sorted(set(core.retics).difference(side_entries), key=str):
        _add_incoming_parking_sample(graph, f"retic-slot:{reticulation}")
    padding_count = FIXED_LOCAL_SAMPLE_COUNT - len(_sampled_leaf_nodes(graph))
    if padding_count < 0:
        raise AssertionError("local fixed-S scaffold is too small")
    for index in range(padding_count):
        _add_incoming_parking_sample(graph, f"common-padding:{index}")
    if len(_sampled_leaf_nodes(graph)) != FIXED_LOCAL_SAMPLE_COUNT:
        raise AssertionError("local carrier does not use the common fixed sampled set")
    for index, reticulation in enumerate(core.retics):
        gamma = Fraction(
            index + 1,
            index + 3,
        )
        graph.nodes[reticulation]["inheritance_probability"] = gamma
        incoming = tuple(sorted(
            graph.in_edges(reticulation, keys=True, data=True),
            key=lambda edge: tuple(map(str, edge[:3])),
        ))
        if len(incoming) != 2:
            raise AssertionError("binary reticulation lacks two inheritance edges")
        for edge_index, (_, _, _, data) in enumerate(incoming):
            data["inheritance_probability"] = (
                gamma if edge_index == 0 else 1 - gamma
            )
    _assign_strict_event_times(
        graph,
        reverse_incomparable_order=reverse_incomparable_order,
    )
    return graph


def _positive_two_block_support(
    graph: nx.MultiDiGraph,
    reticulation: str,
) -> dict | None:
    """Return an exact sampled-reachability witness, or ``None`` if singleton."""
    child = _unique_reticulation_child(graph, reticulation)
    leaves = tuple(sorted(
        node for node in _sampled_leaf_nodes(graph)
        if nx.has_path(graph, child, node)
    ))
    if len(leaves) < 2:
        return None
    candidates = tuple(
        node for node in nx.descendants(graph, child).union({child})
        if graph.out_degree(node) >= 2
        and len(tuple(
            leaf for leaf in leaves if nx.has_path(graph, node, leaf)
        )) >= 2
    )
    if not candidates:
        return None
    first_entry = max(
        candidates,
        key=lambda node: graph.nodes[node]["event_time"],
    )
    interval = Fraction(graph.nodes[reticulation]["event_time"]) - Fraction(
        graph.nodes[first_entry]["event_time"]
    )
    if interval <= 0:
        raise AssertionError("two-block support does not precede the routing event")
    return {
        "reticulation": reticulation,
        "first_side_entry": first_entry,
        "descendant_samples": leaves,
        "positive_interval": interval,
        "no_merger_survival": f"exp(-lambda*{interval})>0",
    }


def _derive_joint_occupancy_state(
    graph: nx.MultiDiGraph,
) -> dict:
    reticulations = tuple(sorted(
        node for node, data in graph.nodes(data=True)
        if data.get("role") == "retic"
    ))
    exposed_witnesses = {
        reticulation: _positive_two_block_support(graph, reticulation)
        for reticulation in reticulations
    }
    exposed = tuple(
        reticulation for reticulation in reticulations
        if exposed_witnesses[reticulation] is not None
    )
    fans, rejected = behaviorally_realizable_unary_fans(graph)
    hidden = tuple(sorted(
        {fan["reticulation"] for fan in fans},
        key=str,
    ))
    return {
        "hidden_reticulations": hidden,
        "exposed_reticulations": exposed,
        "hidden_fans": fans,
        "exposed_support_witnesses": tuple(
            exposed_witnesses[reticulation]
            for reticulation in exposed
        ),
        "behavioral_rejections": rejected,
    }


def _occupancy_sample_label_maps(
    graph: nx.MultiDiGraph,
) -> tuple[dict[str, str], ...]:
    """Permute one homogeneous observable label set over every sampled leaf."""
    return _observable_sample_label_maps(graph)


def _insert_positive_unary_chain(
    graph: nx.MultiDiGraph,
    tail: str,
    head: str,
    key: str,
    data: Mapping,
    *,
    owner: str,
    arm: str,
    count: int,
    carrier: str,
) -> None:
    tail_time = Fraction(graph.nodes[tail]["event_time"])
    head_time = Fraction(graph.nodes[head]["event_time"])
    if not tail_time > head_time:
        raise AssertionError("cannot subdivide a nonpositive temporal interval")
    graph.remove_edge(tail, head, key=key)
    nodes = []
    for index in range(count):
        node = f"unary:{owner}:{arm}:{index}:{carrier}"
        # The old-to-young interpolation is exact and strictly internal.
        event_time = tail_time - (tail_time - head_time) * Fraction(index + 1, count + 1)
        graph.add_node(
            node,
            role="unary",
            module_owner=owner,
            arm=arm,
            epoch_index=index,
            raw_carrier=carrier,
            event_time=event_time,
            population_rate=Fraction(2 + index + (carrier == "delayed"), 1),
        )
        nodes.append(node)
    chain = (tail, *nodes, head)
    for index, (left, right) in enumerate(zip(chain, chain[1:])):
        graph.add_edge(
            left,
            right,
            key=f"{key}:unary:{index}",
            **dict(data),
        )


def _separate_inserted_unary_times(graph: nx.MultiDiGraph) -> None:
    """Perturb arm words exactly so no two internal event clocks coincide."""
    groups: Dict[tuple, List[str]] = {}
    for node, data in graph.nodes(data=True):
        if data.get("role") == "unary":
            groups.setdefault(
                (data["module_owner"], data["arm"]),
                [],
            ).append(node)
    used = {
        Fraction(data["event_time"])
        for _, data in graph.nodes(data=True)
        if data.get("role") != "unary" and data.get("role") != "leaf"
    }
    nonunary_events = tuple(
        Fraction(data["event_time"])
        for node, data in graph.nodes(data=True)
        if graph.out_degree(node) > 0 and data.get("role") != "unary"
    )
    if len(set(nonunary_events)) != len(nonunary_events):
        raise AssertionError("nonunary routing/core event clocks coincide")
    for serial, group_key in enumerate(sorted(groups, key=repr)):
        nodes = tuple(sorted(
            groups[group_key],
            key=lambda node: graph.nodes[node]["epoch_index"],
        ))
        first, last = nodes[0], nodes[-1]
        external_parents = tuple(
            parent for parent in graph.predecessors(first)
            if graph.nodes[parent].get("role") != "unary"
        )
        external_children = tuple(
            child for child in graph.successors(last)
            if graph.nodes[child].get("role") != "unary"
        )
        if len(external_parents) != 1 or len(external_children) != 1:
            raise AssertionError("a unary arm word lacks two external boundaries")
        high = Fraction(graph.nodes[external_parents[0]]["event_time"])
        low = Fraction(graph.nodes[external_children[0]]["event_time"])
        if high <= low:
            raise AssertionError("a unary arm has nonpositive boundary length")
        count = len(nodes)
        denominator = 1009
        while True:
            epsilon = Fraction(serial + 1, denominator * (count + 1))
            candidates = tuple(
                high - (high - low) * (
                    Fraction(index + 1, count + 1) + epsilon
                )
                for index in range(count)
            )
            if (
                all(high > value > low for value in candidates)
                and len(set(candidates)) == count
                and not set(candidates).intersection(used)
            ):
                break
            denominator += 2
            if denominator > 100000:
                raise AssertionError("could not separate unary event clocks exactly")
        for node, value in zip(nodes, candidates):
            graph.nodes[node]["event_time"] = value
            used.add(value)


def _expand_actual_hidden_carriers(
    occupancy_graph: nx.MultiDiGraph,
    carrier_by_reticulation: Mapping[str, str],
) -> nx.MultiDiGraph:
    """Create genuinely different positive metric/topological raw fan words."""
    graph = occupancy_graph.copy()
    for reticulation, carrier in sorted(
        carrier_by_reticulation.items(),
        key=lambda item: str(item[0]),
    ):
        if carrier not in HIDDEN_FAN_CARRIERS:
            raise ValueError(f"unknown hidden carrier {carrier!r}")
        parents = tuple(sorted(
            graph.in_edges(reticulation, keys=True, data=True),
            key=lambda edge: tuple(map(str, edge[:3])),
        ))
        outgoing = tuple(graph.out_edges(reticulation, keys=True, data=True))
        if len(parents) != 2 or len(outgoing) != 1:
            raise ValueError("a hidden binary routing event needs two arms and one child")
        child = outgoing[0][1]
        low = Fraction(graph.nodes[child]["event_time"])
        high = min(Fraction(graph.nodes[parent]["event_time"]) for parent, _, _, _ in parents)
        fraction = Fraction(1, 3) if carrier == "immediate" else Fraction(2, 3)
        used_event_times = {
            Fraction(data["event_time"])
            for node, data in graph.nodes(data=True)
            if node != reticulation and graph.out_degree(node) > 0
            and data.get("role") != "unary"
        }
        candidate_time = low + fraction * (high - low)
        perturbation = 0
        while candidate_time in used_event_times:
            perturbation += 1
            adjusted_fraction = fraction + Fraction(perturbation, 1009)
            if adjusted_fraction >= 1:
                raise AssertionError("could not separate hidden routing clock")
            candidate_time = low + adjusted_fraction * (high - low)
        graph.nodes[reticulation]["event_time"] = candidate_time
        graph.nodes[reticulation]["raw_carrier"] = carrier
        count = 1 if carrier == "immediate" else 2
        for arm_index, (parent, _, key, data) in enumerate(parents):
            _insert_positive_unary_chain(
                graph,
                parent,
                reticulation,
                key,
                data,
                owner=reticulation,
                arm=f"upper-{arm_index}",
                count=count,
                carrier=carrier,
            )
        _, _, key, data = outgoing[0]
        _insert_positive_unary_chain(
            graph,
            reticulation,
            child,
            key,
            data,
            owner=reticulation,
            arm="lower",
            count=count,
            carrier=carrier,
        )
    _separate_inserted_unary_times(graph)
    for tail, head, _, data in graph.edges(keys=True, data=True):
        duration = Fraction(graph.nodes[tail]["event_time"]) - Fraction(
            graph.nodes[head]["event_time"]
        )
        if duration <= 0:
            raise AssertionError(f"nonpositive raw duration on {tail!r}->{head!r}")
        data["duration"] = duration
        data["population_rate"] = Fraction(
            graph.nodes[head].get("population_rate", 1)
        )
    return graph


def _observable_exposure_color(
    graph: nx.MultiDiGraph,
    reticulation: str,
    sample_labels: Mapping[str, str],
) -> tuple:
    witness = _positive_two_block_support(graph, reticulation)
    if witness is None:
        raise ValueError("an exposed role lacks positive two-block support")
    gamma = Fraction(graph.nodes[reticulation]["inheritance_probability"])
    reticulations = tuple(
        node for node, data in graph.nodes(data=True)
        if data.get("role") == "retic"
    )
    return (
        "exposed-routing-event",
        ("inheritance-probability", gamma.numerator, gamma.denominator),
        _global_retained_event_order_tag(graph, reticulation),
        (
            "positive-two-block-support",
            tuple(sorted(sample_labels[sample] for sample in witness["descendant_samples"])),
            "positive-length",
        ),
    )


def _external_observable_color(
    graph: nx.MultiDiGraph,
    node: str,
    sample_labels: Mapping[str, str],
) -> tuple:
    role = _generic_role(graph, node)
    if role == "sample":
        return ("sample", sample_labels[node])
    if role == "retic":
        return _observable_exposure_color(graph, node, sample_labels)
    if role == "source":
        return (
            "source",
            "incoming-boundary",
            _global_retained_event_order_tag(graph, node),
        )
    if graph.nodes[node].get("exposure_owner") is not None:
        side_samples = tuple(sorted(
            sample_labels[child]
            for child in graph.successors(node)
            if child in sample_labels
        ))
        return (
            "observable-two-block-entry",
            side_samples,
            _global_retained_event_order_tag(graph, node),
        )
    if graph.nodes[node].get("parking_slot") is not None:
        parked_samples = tuple(sorted(
            sample_labels[child]
            for child in graph.successors(node)
            if child in sample_labels
        ))
        return (
            "observable-incoming-parking-entry",
            parked_samples,
            _global_retained_event_order_tag(graph, node),
        )
    return (
        "tree-event",
        _global_retained_event_order_tag(graph, node),
    )


def _external_edge_observable_color(
    graph: nx.MultiDiGraph,
    tail: str,
    head: str,
    data: Mapping,
) -> tuple:
    if (
        graph.nodes[head].get("role") == "retic"
        and _positive_two_block_support(graph, head) is not None
    ):
        probability = Fraction(data["inheritance_probability"])
        return (
            "typed-inheritance-incidence",
            probability.numerator,
            probability.denominator,
        )
    return ("population-incidence",)


def _decorate_actual_raw_carrier(
    graph: nx.MultiDiGraph,
    hidden_fans: Sequence[Mapping],
    sample_labels: Mapping[str, str],
) -> nx.MultiDiGraph:
    decorated = graph.copy()
    hidden = {fan["reticulation"] for fan in hidden_fans}
    for node, data in decorated.nodes(data=True):
        role = _generic_role(graph, node)
        if role == "sample":
            color = ("sample", sample_labels[node])
        elif node in hidden:
            gamma = Fraction(data["inheritance_probability"])
            color = (
                "hidden-routing-event-raw",
                _exact_time_tag(data["event_time"]),
                ("positive-internal-rate",),
                ("inheritance-probability", gamma.numerator, gamma.denominator),
            )
        elif data.get("role") == "unary":
            color = (
                "positive-unary-epoch",
                _exact_time_tag(data["event_time"]),
                ("rate", Fraction(data["population_rate"]).numerator,
                 Fraction(data["population_rate"]).denominator),
            )
        else:
            color = _external_observable_color(graph, node, sample_labels)
        data["observable_color"] = color
    for tail, head, _, data in decorated.edges(keys=True, data=True):
        duration = Fraction(data["duration"])
        rate = Fraction(data["population_rate"])
        typed_weight = (
            ("inheritance-probability",)
            + (
                Fraction(data["inheritance_probability"]).numerator,
                Fraction(data["inheritance_probability"]).denominator,
            )
            if "inheritance_probability" in data
            else ("ordinary-population-edge",)
        )
        data["observable_color"] = (
            "positive-metric-population-epoch",
            (duration.numerator, duration.denominator),
            (rate.numerator, rate.denominator),
            typed_weight,
        )
    return decorated


def _normalize_actual_joint_carrier(
    raw: nx.MultiDiGraph,
    hidden_fans: Sequence[Mapping],
    sample_labels: Mapping[str, str],
) -> nx.MultiDiGraph:
    """Remove every disjoint raw fan interior and insert response macros."""
    normalized = raw.copy()
    interiors = {
        fan["reticulation"]: _behavioral_fan_interior_nodes(fan)
        for fan in hidden_fans
    }
    for left, right in combinations(interiors.values(), 2):
        if left & right:
            raise ValueError("simultaneous Q8 fan interiors overlap")
    boundary_records = []
    for fan in hidden_fans:
        reticulation = fan["reticulation"]
        component = interiors[reticulation]
        incoming = tuple(
            (tail, dict(data))
            for tail, head, _, data in raw.edges(keys=True, data=True)
            if tail not in component and head in component
        )
        outgoing = tuple(
            (head, dict(data))
            for tail, head, _, data in raw.edges(keys=True, data=True)
            if tail in component and head not in component
        )
        if len(incoming) != 2 or len(outgoing) != 1:
            raise ValueError("a stopped binary fan must have two upper and one lower ports")
        boundary_records.append((fan, incoming, outgoing[0][0]))
    normalized.remove_nodes_from(set().union(*interiors.values()) if interiors else set())
    for index, (fan, incoming, lower_child) in enumerate(boundary_records):
        macro = f"behavioral-q8-macro:{index}"
        normalized.add_node(
            macro,
            role="macro",
            observable_color=(
                "q8-behavior-derived-macro",
                _behavioral_macro_payload(raw, fan, sample_labels),
            ),
        )
        for route_index, (upper, _) in enumerate(incoming):
            normalized.add_edge(
                upper,
                macro,
                key=f"macro-upper:{index}:{route_index}",
                observable_color=("population-incidence",),
            )
        normalized.add_edge(
            macro,
            lower_child,
            key=f"macro-lower:{index}",
            observable_color=("population-incidence",),
        )
    macro_nodes = {node for node, data in normalized.nodes(data=True) if data.get("role") == "macro"}
    for node, data in normalized.nodes(data=True):
        if node not in macro_nodes:
            data["observable_color"] = _external_observable_color(
                normalized,
                node,
                sample_labels,
            )
    for tail, head, _, data in normalized.edges(keys=True, data=True):
        data["observable_color"] = _external_edge_observable_color(
            normalized,
            tail,
            head,
            data,
        )
    return normalized


def _independent_expected_joint_record(
    core: Core,
    repair: Sequence[int],
    side_entry_reticulations: Sequence[str],
    sample_labels: Mapping[str, str],
    *,
    reverse_incomparable_order: bool = False,
) -> tuple[nx.MultiDiGraph, nx.MultiDiGraph, dict, dict]:
    """Rebuild the reduced record from primitive arcs and occupancy support.

    This deliberately does not inspect, copy, recolor, or contract a generated
    raw carrier.  It is the independent target against which the simultaneous
    raw normalization is compared.
    """
    reference = _build_behavioral_occupancy_graph(
        core,
        repair,
        side_entry_reticulations,
        reverse_incomparable_order=reverse_incomparable_order,
    )
    if set(sample_labels) != set(_sampled_leaf_nodes(reference)):
        raise ValueError("independent target received the wrong sampled-lineage labels")
    state = _derive_joint_occupancy_state(reference)
    hidden_reticulations = tuple(state["hidden_reticulations"])
    expected = reference.copy()
    fan_by_reticulation = {
        fan["reticulation"]: fan for fan in state["hidden_fans"]
    }
    boundaries = []
    for reticulation in sorted(hidden_reticulations, key=str):
        incoming = tuple(
            tail for tail, _, _, _ in reference.in_edges(
                reticulation,
                keys=True,
                data=True,
            )
        )
        outgoing = tuple(
            head for _, head, _, _ in reference.out_edges(
                reticulation,
                keys=True,
                data=True,
            )
        )
        if len(incoming) != 2 or len(outgoing) != 1:
            raise AssertionError("primitive expected fan has the wrong boundary arity")
        boundaries.append((
            reticulation,
            incoming,
            outgoing[0],
            _independent_behavioral_macro_payload(
                reference,
                fan_by_reticulation[reticulation],
                sample_labels,
            ),
        ))
    expected.remove_nodes_from(hidden_reticulations)
    for index, (_, incoming, lower, payload) in enumerate(boundaries):
        macro = f"independent-response-macro:{index}"
        expected.add_node(
            macro,
            role="macro",
            observable_color=("q8-behavior-derived-macro", payload),
        )
        for route_index, upper in enumerate(incoming):
            expected.add_edge(
                upper,
                macro,
                key=f"expected-upper:{index}:{route_index}",
                observable_color=("population-incidence",),
            )
        expected.add_edge(
            macro,
            lower,
            key=f"expected-lower:{index}",
            observable_color=("population-incidence",),
        )
    macro_nodes = {node for node, data in expected.nodes(data=True) if data.get("role") == "macro"}
    for node, data in expected.nodes(data=True):
        if node not in macro_nodes:
            data["observable_color"] = _external_observable_color(
                expected,
                node,
                sample_labels,
            )
    for tail, head, _, data in expected.edges(keys=True, data=True):
        data["observable_color"] = _external_edge_observable_color(
            expected,
            tail,
            head,
            data,
        )

    skeleton = reference.copy()
    for node, data in skeleton.nodes(data=True):
        role = _generic_role(skeleton, node)
        if role == "sample":
            data["observable_color"] = ("sample", sample_labels[node])
        elif role == "retic":
            data["observable_color"] = ("retic",)
        elif role == "source":
            data["observable_color"] = ("source",)
        else:
            data["observable_color"] = ("tree",)
    for _, _, _, data in skeleton.edges(keys=True, data=True):
        data["observable_color"] = ("population-incidence",)
    return expected, skeleton, state, dict(sample_labels)


def _reinsert_entire_macro_collection(
    normalized: nx.MultiDiGraph,
) -> nx.MultiDiGraph:
    """Reinsert every anonymous reticulation using residual incidence only."""
    reinserted = normalized.copy()
    macros = tuple(sorted((
        node for node, data in reinserted.nodes(data=True)
        if tuple(data.get("observable_color", ()))[0]
        == "q8-behavior-derived-macro"
    ), key=str))
    boundaries = []
    for macro in macros:
        incoming = tuple(
            tail for tail, _, _, _ in reinserted.in_edges(
                macro,
                keys=True,
                data=True,
            )
        )
        outgoing = tuple(
            head for _, head, _, _ in reinserted.out_edges(
                macro,
                keys=True,
                data=True,
            )
        )
        if len(incoming) != 2 or len(outgoing) != 1:
            raise ValueError("a response macro has invalid reattachment arity")
        boundaries.append((macro, incoming, outgoing[0]))
    reinserted.remove_nodes_from(macros)
    for index, (_, incoming, lower) in enumerate(boundaries):
        reticulation = f"reinserted-routing-event:{index}"
        reinserted.add_node(
            reticulation,
            role="retic",
            observable_color=("retic",),
        )
        for route_index, upper in enumerate(incoming):
            reinserted.add_edge(
                upper,
                reticulation,
                key=f"reinserted-upper:{index}:{route_index}",
                observable_color=("population-incidence",),
            )
        reinserted.add_edge(
            reticulation,
            lower,
            key=f"reinserted-lower:{index}",
            observable_color=("population-incidence",),
        )
    for node, data in reinserted.nodes(data=True):
        color = tuple(data.get("observable_color", ()))
        if color and color[0] == "sample":
            continue
        role = data.get("role")
        if role == "retic":
            data["observable_color"] = ("retic",)
        elif reinserted.in_degree(node) == 0:
            data["observable_color"] = ("source",)
        else:
            data["observable_color"] = ("tree",)
    for _, _, _, data in reinserted.edges(keys=True, data=True):
        data["observable_color"] = ("population-incidence",)
    return reinserted


def _raw_carrier_validity_certificate(
    raw: nx.MultiDiGraph,
    hidden_fans: Sequence[Mapping],
) -> dict:
    suppressed = raw.copy()
    unary_nodes = tuple(
        node for node, data in suppressed.nodes(data=True)
        if data.get("role") == "unary"
    )
    for serial, node in enumerate(unary_nodes):
        incoming = tuple(suppressed.in_edges(node, keys=True, data=True))
        outgoing = tuple(suppressed.out_edges(node, keys=True, data=True))
        if len(incoming) != 1 or len(outgoing) != 1:
            raise AssertionError("raw unary epoch is not suppressible")
        parent = incoming[0][0]
        child = outgoing[0][1]
        suppressed.remove_node(node)
        suppressed.add_edge(
            parent,
            child,
            key=f"suppressed-unary:{serial}",
            segment="suppressed-positive-unary-word",
        )
    durations = tuple(
        Fraction(data["duration"])
        for _, _, _, data in raw.edges(keys=True, data=True)
    )
    reticulations = tuple(
        node for node, data in raw.nodes(data=True)
        if data.get("role") == "retic"
    )
    hidden_interiors = tuple(
        _behavioral_fan_interior_nodes(fan) for fan in hidden_fans
    )
    event_times = tuple(
        Fraction(data["event_time"])
        for node, data in raw.nodes(data=True)
        if raw.out_degree(node) > 0
    )
    suppressed_reticulations = tuple(
        node for node, data in suppressed.nodes(data=True)
        if data.get("role") == "retic"
    )
    binary_after_suppression = all(
        (
            suppressed.in_degree(node) == 2
            and suppressed.out_degree(node) == 1
        )
        if data.get("role") == "retic"
        else (
            suppressed.in_degree(node) == 1
            and suppressed.out_degree(node) == 0
        )
        if data.get("role") == "leaf"
        else (
            suppressed.out_degree(node) == 2
            and suppressed.in_degree(node) in {0, 1}
        )
        for node, data in suppressed.nodes(data=True)
    )
    undirected = nx.Graph(suppressed.to_undirected())
    maximum_blob_reticulations = max((
        sum(node in suppressed_reticulations for node in component)
        for component in nx.biconnected_components(undirected)
    ), default=0)
    inheritance_probabilities = tuple(
        Fraction(raw.nodes[node]["inheritance_probability"])
        for node in reticulations
    )
    inheritance_edge_pairs = tuple(
        tuple(
            Fraction(data["inheritance_probability"])
            for _, _, _, data in sorted(
                raw.in_edges(node, keys=True, data=True),
                key=lambda edge: tuple(map(str, edge[:3])),
            )
        )
        for node in reticulations
    )
    sampled_leaves = _sampled_leaf_nodes(raw)
    return {
        "rooted": sum(raw.in_degree(node) == 0 for node in raw) == 1,
        "acyclic": nx.is_directed_acyclic_graph(raw),
        "strict_positive_durations": bool(durations) and all(value > 0 for value in durations),
        "strict_temporal_separation": len(set(event_times)) == len(event_times),
        "binary_reticulations": all(
            raw.in_degree(node) == 2 and raw.out_degree(node) == 1
            for node in reticulations
        ),
        "binary_after_allowed_raw_unary_suppression": binary_after_suppression,
        "rooted_tree_child_after_unary_suppression": is_local_tree_child(suppressed),
        "strong_tail_after_unary_suppression": is_local_strong_tree_child(suppressed),
        "level_at_most_two_after_unary_suppression": maximum_blob_reticulations <= 2,
        "positive_population_rates": all(
            Fraction(data["population_rate"]) > 0
            for _, _, _, data in raw.edges(keys=True, data=True)
        ),
        "inheritance_probabilities_strictly_internal": all(
            0 < gamma < 1 for gamma in inheritance_probabilities
        ),
        "inheritance_edge_probabilities_strictly_internal": all(
            len(pair) == 2 and all(0 < weight < 1 for weight in pair)
            for pair in inheritance_edge_pairs
        ),
        "inheritance_edge_probabilities_sum_to_one": all(
            len(pair) == 2 and sum(pair, Fraction(0)) == 1
            for pair in inheritance_edge_pairs
        ),
        "inheritance_edges_agree_with_presentation_marker": all(
            len(pair) == 2
            and sorted(pair) == sorted((gamma, 1 - gamma))
            for gamma, pair in zip(
                inheritance_probabilities,
                inheritance_edge_pairs,
            )
        ),
        "fixed_sample_count": len(sampled_leaves) == FIXED_LOCAL_SAMPLE_COUNT,
        "contemporaneous_sampling": all(
            Fraction(raw.nodes[sample]["event_time"]) == 0
            for sample in sampled_leaves
        ),
        "all_sampled_leaves_retained": all(
            raw.out_degree(node) == 0
            for node in _sampled_leaf_nodes(raw)
        ),
        "simultaneous_fan_interiors_disjoint": all(
            not (left & right)
            for left, right in combinations(hidden_interiors, 2)
        ),
        "actual_unary_epoch_node_count": sum(
            data.get("role") == "unary" for _, data in raw.nodes(data=True)
        ),
    }


def _behavioral_expected_projection(
    graph: nx.MultiDiGraph,
    sample_labels: Mapping[str, str],
) -> nx.MultiDiGraph:
    expected = graph.copy()
    for node, data in expected.nodes(data=True):
        role = _generic_role(graph, node)
        data["observable_color"] = (
            ("sample", sample_labels[node])
            if role == "sample"
            else (role,)
        )
    for _, _, _, data in expected.edges(keys=True, data=True):
        data["observable_color"] = ("population-incidence",)
    return expected


def _recovered_projection(
    decorated: nx.MultiDiGraph,
) -> nx.MultiDiGraph:
    recovered = decorated.copy()
    for _, data in recovered.nodes(data=True):
        color = tuple(data["observable_color"])
        if color[0] in {"q8-behavior-derived-macro", "exposed-routing-event"}:
            projected = ("retic",)
        elif color[0] == "hidden-routing-event-raw":
            projected = ("retic",)
        elif color[0] == "tree-event":
            projected = ("tree",)
        elif color[0] == "source":
            projected = ("source",)
        elif color[0] == "sample":
            projected = color
        else:
            raise ValueError(f"unknown behavioral color {color!r}")
        data["observable_color"] = projected
    return recovered


def _behavioral_elimination_certificate(
    graph: nx.MultiDiGraph,
    fan: Mapping,
    sample_labels: Mapping[str, str],
) -> dict:
    parents = fan["parents"]
    focal = fan["focal"]
    candidate_samples = tuple(
        sample for sample in _sampled_leaf_nodes(graph)
        if sample != focal
    )
    exclusive = []
    for sample in candidate_samples:
        anchor_parents = tuple(set(graph.predecessors(sample)))
        if len(anchor_parents) != 1:
            continue
        anchor = anchor_parents[0]
        meetings = tuple(
            _lowest_common_ancestors(graph, parent, anchor)
            for parent in parents
        )
        if any(len(nodes) != 1 for nodes in meetings):
            continue
        first, second = meetings[0][0], meetings[1][0]
        if first == second:
            continue
        if nx.has_path(graph, first, second):
            older_index, private_index = 0, 1
        elif nx.has_path(graph, second, first):
            older_index, private_index = 1, 0
        else:
            continue
        older = meetings[older_index][0]
        private = meetings[private_index][0]
        interval = tuple(nx.shortest_path(graph, older, private))
        if len(interval) < 2:
            continue
        exclusive.append({
            "sample_anchor": sample_labels[sample],
            "private_outlet_index": private_index,
            "excluded_outlet_index": older_index,
            "positive_length_path_word": _behavioral_path_word(
                graph,
                interval,
                sample_labels,
            ),
            "strict_event_order_edge_count": len(interval) - 1,
        })
    exclusive.sort(key=repr)
    frontier_records = _behavioral_route_records(graph, fan, sample_labels)
    typed_anchors = tuple(
        (
            "sampled-first-side-block",
            anchors[0],
            frontier_records[index],
        )
        if anchors
        else (
            "typed-incoming-boundary",
            frontier_records[index],
        )
        for index, anchors in enumerate(
            tuple(record[1] for record in frontier_records)
        )
    )
    failures = []
    if fan["maximum_internal_occupancy"] != 1 or fan["internal_sample_entries"]:
        failures.append("derived cone is not internally singleton")
    if len(fan["routes"]) != 2:
        failures.append("derived fan does not have two routes")
    if len(set(frontier_records)) != 2:
        failures.append("behavior-derived frontier has a future-null outlet collision")
    if not exclusive:
        failures.append("no sampled anchor has a positive exclusive interval")
    if len(typed_anchors) != 2:
        failures.append("not both first exposure outlets are typed")
    return {
        "status": "PASS" if not failures else "POTENTIAL_COUNTEREXAMPLE",
        "focal_sample": sample_labels[focal],
        "hidden_reticulation_count": 1,
        "typed_outlet_count": len(fan["routes"]),
        "future_null_dimension": len(fan["routes"]) - len(set(frontier_records)),
        "weight_separating_anchor_count": 0 if not exclusive else 1,
        "typed_first_outlet_anchor_count": len(typed_anchors),
        "selected_first_outlet_anchors": typed_anchors,
        "typed_outlet_coverage_matrix": ((1, 0), (0, 1)),
        "exclusive_positive_length_interval": None if not exclusive else exclusive[0],
        "outlet_by_cell_possibility_matrix": ((1, 1), (0, 1)),
        "symbolic_merge_survive_transition": (
            ("1-exp(-lambda*delta)", "exp(-lambda*delta)"),
            ("0", "1"),
        ),
        "symbolic_determinant": "1-exp(-lambda*delta)>0",
        "failures": tuple(failures),
    }


def _audit_incomparable_reticulation_orders(
    core: Core,
    repair: Sequence[int],
    side_entry_reticulations: Sequence[str],
) -> dict | None:
    primitive = build_repaired_core(core, repair)
    incomparable_pairs = tuple(
        (left, right)
        for left, right in combinations(core.retics, 2)
        if not nx.has_path(primitive, left, right)
        and not nx.has_path(primitive, right, left)
    )
    if not incomparable_pairs:
        return None
    variants = []
    reticulation_orders = []
    for reverse in (False, True):
        occupancy = _build_behavioral_occupancy_graph(
            core,
            repair,
            side_entry_reticulations,
            reverse_incomparable_order=reverse,
        )
        sample_labels = dict(zip(
            _sampled_leaf_nodes(occupancy),
            tuple(f"sample-{index}" for index in range(len(_sampled_leaf_nodes(occupancy)))),
        ))
        expected, _, state, checked_labels = _independent_expected_joint_record(
            core,
            repair,
            side_entry_reticulations,
            sample_labels,
            reverse_incomparable_order=reverse,
        )
        hidden = tuple(state["hidden_reticulations"])
        actual = _expand_actual_hidden_carriers(
            occupancy,
            {reticulation: "immediate" for reticulation in hidden},
        )
        actual_state = _derive_joint_occupancy_state(actual)
        normalized = _normalize_actual_joint_carrier(
            actual,
            actual_state["hidden_fans"],
            checked_labels,
        )
        validity = _raw_carrier_validity_certificate(
            actual,
            actual_state["hidden_fans"],
        )
        normalized_code = _colored_canonical_code(normalized)
        expected_code = _colored_canonical_code(expected)
        if normalized_code != expected_code:
            raise AssertionError("incomparable-order raw normalization missed expected record")
        if not validity["strict_temporal_separation"]:
            raise AssertionError("incomparable-order raw carrier has tied event clocks")
        order = tuple(sorted(
            core.retics,
            key=lambda node: Fraction(occupancy.nodes[node]["event_time"]),
            reverse=True,
        ))
        reticulation_orders.append(order)
        variants.append({
            "reverse_incomparable_order": reverse,
            "reticulation_order": order,
            "derived_hidden_count": len(hidden),
            "derived_exposed_count": len(state["exposed_reticulations"]),
            "normalized_code": normalized_code,
            "independent_expected_code": expected_code,
            "strict_temporal_separation": True,
        })
    for left, right in incomparable_pairs:
        forward_sign = reticulation_orders[0].index(left) < reticulation_orders[0].index(right)
        reverse_sign = reticulation_orders[1].index(left) < reticulation_orders[1].index(right)
        if forward_sign == reverse_sign:
            raise AssertionError("the two bounded schedules do not reverse incomparable retics")
    return {
        "incomparable_pairs": incomparable_pairs,
        "variant_count": len(variants),
        "variants": tuple(variants),
    }


def enumerate_exposure_decorated_core_regression(
    cores: Mapping[str, Core],
) -> dict:
    """Exhaust the 36 behavior-derived joint exposure configurations.

    Every exposed role is realized by an explicit positive two-block sampled
    side entry.  Every hidden role is re-derived as a stopped singleton fan.
    All compatible sibling fans are normalized simultaneously.  Expected
    records are rebuilt independently from primitive arcs and sampled ports.
    """
    repair_count = 0
    structural_realizable_cone_count = 0
    joint_configuration_count = 0
    simultaneous_both_hidden_configuration_count = 0
    behavioral_rejections = []
    joint_compatibility_rejections = []
    configuration_records = []
    incomparable_order_audits = []
    per_core_joint_configuration_counts: Dict[str, int] = {}

    for core_name, core in sorted(cores.items()):
        repairs = enumerate_minimal_repairs(core)
        if repairs != core.repairs:
            raise AssertionError(f"{core_name}: primitive repair catalog drifted")
        repair_count += len(repairs)
        for repair in repairs:
            base_graph = build_repaired_core(core, repair)
            base_fans, base_rejected = behaviorally_realizable_unary_fans(base_graph)
            structural_realizable_cone_count += len(base_fans)
            behavioral_rejections.extend({
                "core": core_name,
                "repair": tuple(repair),
                **record,
            } for record in base_rejected)

            # Enumerate actual sampled side-entry port configurations first.
            # Only afterwards derive and deduplicate their exposure states.
            derived_configurations: Dict[tuple, dict] = {}
            for side_entry_count in range(len(core.retics) + 1):
                for side_entries in combinations(core.retics, side_entry_count):
                    occupancy = _build_behavioral_occupancy_graph(
                        core,
                        repair,
                        side_entries,
                    )
                    state = _derive_joint_occupancy_state(occupancy)
                    hidden = tuple(state["hidden_reticulations"])
                    exposed = tuple(state["exposed_reticulations"])
                    if set(hidden).intersection(exposed):
                        raise AssertionError("a routing event is both exposed and hidden")
                    if set(hidden).union(exposed) != set(core.retics):
                        behavioral_rejections.append({
                            "core": core_name,
                            "repair": tuple(repair),
                            "side_entry_reticulations": tuple(side_entries),
                            "reason": "sampled-port-configuration-leaves-unclassified-event",
                        })
                        continue
                    interiors = tuple(
                        _behavioral_fan_interior_nodes(fan)
                        for fan in state["hidden_fans"]
                    )
                    overlaps = tuple(
                        tuple(sorted(left & right, key=str))
                        for left, right in combinations(interiors, 2)
                        if left & right
                    )
                    if overlaps:
                        joint_compatibility_rejections.append({
                            "core": core_name,
                            "repair": tuple(repair),
                            "side_entry_reticulations": tuple(side_entries),
                            "reason": "joint-fan-interiors-not-disjoint",
                            "overlaps": overlaps,
                        })
                        continue
                    state_key = (hidden, exposed)
                    candidate = {
                        "side_entry_reticulations": tuple(side_entries),
                        "occupancy_graph": occupancy,
                        "state": state,
                    }
                    previous = derived_configurations.get(state_key)
                    if previous is None or len(side_entries) < len(
                        previous["side_entry_reticulations"]
                    ):
                        derived_configurations[state_key] = candidate

            configurations = tuple(
                derived_configurations[key]
                for key in sorted(derived_configurations, key=repr)
            )
            joint_configuration_count += len(configurations)
            per_core_joint_configuration_counts[core_name] = (
                per_core_joint_configuration_counts.get(core_name, 0)
                + len(configurations)
            )
            simultaneous_both_hidden_configuration_count += sum(
                len(configuration["state"]["hidden_reticulations"]) == 2
                for configuration in configurations
            )
            for configuration in configurations:
                order_audit = _audit_incomparable_reticulation_orders(
                    core,
                    repair,
                    configuration["side_entry_reticulations"],
                )
                if order_audit is not None:
                    incomparable_order_audits.append({
                        "core": core_name,
                        "repair": tuple(repair),
                        "side_entry_reticulations": configuration[
                            "side_entry_reticulations"
                        ],
                        **order_audit,
                    })

            for configuration in configurations:
                leaves = _sampled_leaf_nodes(configuration["occupancy_graph"])
                sample_labels = dict(zip(
                    leaves,
                    tuple(f"sample-{index}" for index in range(len(leaves))),
                ))
                expected, skeleton, state, checked_labels = (
                    _independent_expected_joint_record(
                        core,
                        repair,
                        configuration["side_entry_reticulations"],
                        sample_labels,
                    )
                )
                derived_hidden = tuple(state["hidden_reticulations"])
                derived_exposed = tuple(state["exposed_reticulations"])
                if (derived_hidden, derived_exposed) not in derived_configurations:
                    raise AssertionError("independent occupancy derivation changed state")
                reference = _build_behavioral_occupancy_graph(
                    core,
                    repair,
                    configuration["side_entry_reticulations"],
                )
                fan_certificates = tuple(
                    _behavioral_elimination_certificate(
                        reference,
                        fan,
                        checked_labels,
                    )
                    for fan in state["hidden_fans"]
                )
                macro_collection = tuple(sorted((
                    _behavioral_macro_payload(
                        reference,
                        fan,
                        checked_labels,
                    )
                    for fan in state["hidden_fans"]
                ), key=repr))
                weight_certificates = _q8_weight_certificate(
                    reference,
                    state,
                    checked_labels,
                )
                configuration_records.append({
                            "core": core_name,
                            "core_object": core,
                            "repair": tuple(repair),
                            "side_entry_reticulations": configuration[
                                "side_entry_reticulations"
                            ],
                            "sample_labels": checked_labels,
                            "sample_attachment": tuple(sorted(checked_labels.items())),
                            "hidden_reticulations": derived_hidden,
                            "exposed_reticulations": derived_exposed,
                            "hidden_focal_samples": tuple(sorted(
                                checked_labels[fan["focal"]]
                                for fan in state["hidden_fans"]
                            )),
                            "exposed_support_witnesses": state[
                                "exposed_support_witnesses"
                            ],
                            "fan_certificates": fan_certificates,
                            "q8_weight_certificates": weight_certificates,
                            "fixed_sampling_map": tuple(
                                (f"sample-{index}", f"taxon-{index}")
                                for index in range(FIXED_LOCAL_SAMPLE_COUNT)
                            ),
                            "macro_collection": macro_collection,
                            "declared_quotient_graph": (
                                _declared_primitive_quotient_graph(
                                    reference,
                                    state,
                                    checked_labels,
                                )
                            ),
                            "expected_graph": expected,
                            "expected_code": _colored_canonical_code(expected),
                            "expected_skeleton": skeleton,
                })

    declared_orbit_witnesses, declared_primitive_orbit_count = (
        _enumerate_declared_primitive_orbits(configuration_records)
    )
    relative_label_orbit_audit = _relative_label_orbit_audit(
        configuration_records
    )
    rows = []
    potential_counterexamples = []
    expected_by_code: Dict[str, List[tuple]] = {}
    for record in configuration_records:
        origin = (
            record["core"],
            record["repair"],
            record["sample_attachment"],
            record["hidden_focal_samples"],
        )
        expected_by_code.setdefault(record["expected_code"], []).append(origin)
        for certificate in record["fan_certificates"]:
            if certificate["status"] != "PASS":
                potential_counterexamples.append({
                    "origin": origin,
                    "failure": "fan elimination certificate failed",
                    "certificate": certificate,
                })

    for record in configuration_records:
        hidden_reticulations = record["hidden_reticulations"]
        carrier_words = tuple(product(
            HIDDEN_FAN_CARRIERS,
            repeat=len(hidden_reticulations),
        ))
        case_normalized_codes = set()
        case_raw_node_counts = set()
        origin = (
            record["core"],
            record["repair"],
            record["sample_attachment"],
            record["hidden_focal_samples"],
        )
        for carrier_word in carrier_words:
            carrier_by_reticulation = dict(zip(hidden_reticulations, carrier_word))
            occupancy = _build_behavioral_occupancy_graph(
                record["core_object"],
                record["repair"],
                record["side_entry_reticulations"],
            )
            actual = _expand_actual_hidden_carriers(
                occupancy,
                carrier_by_reticulation,
            )
            actual_state = _derive_joint_occupancy_state(actual)
            if set(actual_state["hidden_reticulations"]) != set(hidden_reticulations):
                potential_counterexamples.append({
                    "origin": origin,
                    "failure": "raw metric carrier changed behavior-derived hidden roles",
                })
            actual_fans = tuple(actual_state["hidden_fans"])
            raw = _decorate_actual_raw_carrier(
                actual,
                actual_fans,
                record["sample_labels"],
            )
            normalized = _normalize_actual_joint_carrier(
                actual,
                actual_fans,
                record["sample_labels"],
            )
            raw_code = _colored_canonical_code(raw)
            normalized_code = _colored_canonical_code(normalized)
            reinserted = _reinsert_entire_macro_collection(normalized)
            reinserted_code = _colored_canonical_code(reinserted)
            expected_skeleton_code = _colored_canonical_code(
                record["expected_skeleton"]
            )
            validity = _raw_carrier_validity_certificate(actual, actual_fans)
            if not all(
                value for key, value in validity.items()
                if key != "actual_unary_epoch_node_count"
            ):
                potential_counterexamples.append({
                    "origin": origin,
                    "failure": "invalid strict raw carrier",
                    "validity": validity,
                })
            if normalized_code != record["expected_code"] or not _colored_isomorphic(
                normalized,
                record["expected_graph"],
            ):
                potential_counterexamples.append({
                    "origin": origin,
                    "failure": "raw normalization misses independently rebuilt joint record",
                })
            if reinserted_code != expected_skeleton_code or not _colored_isomorphic(
                reinserted,
                record["expected_skeleton"],
            ):
                potential_counterexamples.append({
                    "origin": origin,
                    "failure": "entire macro collection does not reinsert to primitive skeleton",
                })
            case_normalized_codes.add(normalized_code)
            case_raw_node_counts.add(raw.number_of_nodes())
            rows.append({
                "core": record["core"],
                "repair": record["repair"],
                "sample_attachment": record["sample_attachment"],
                "fixed_sampling_map": record["fixed_sampling_map"],
                "hidden_focal_samples": record["hidden_focal_samples"],
                "derived_hidden_count": len(hidden_reticulations),
                "derived_exposed_count": len(record["exposed_reticulations"]),
                "actual_exposure_support_count": len(record["exposed_support_witnesses"]),
                "carrier_word": carrier_word,
                "raw_node_count": raw.number_of_nodes(),
                "raw_code": raw_code,
                "normalized_code": normalized_code,
                "independent_expected_code": record["expected_code"],
                "declared_primitive_orbit_id": record[
                    "declared_primitive_orbit_id"
                ],
                "reinserted_skeleton_code": reinserted_code,
                "independent_expected_skeleton_code": expected_skeleton_code,
                "expected_record_matches": tuple(
                    expected_by_code.get(normalized_code, ())
                ),
                "response_macro_collection": record["macro_collection"],
                "elimination_certificates": record["fan_certificates"],
                "q8_weight_certificates": record["q8_weight_certificates"],
                "raw_validity": validity,
                "raw_graph": raw,
                "normalized_graph": normalized,
                "independent_expected_graph": record["expected_graph"],
                "reinserted_graph": reinserted,
            })
        if len(case_normalized_codes) != 1:
            potential_counterexamples.append({
                "origin": origin,
                "failure": "positive immediate/delayed fan words survived simultaneous Q8",
            })
        if hidden_reticulations and len(case_raw_node_counts) < 2:
            potential_counterexamples.append({
                "origin": origin,
                "failure": "raw fan words are not genuinely topologically distinct",
            })

    label_generator_audit = _normalizer_label_generator_audit(
        configuration_records,
        rows,
    )
    if label_generator_audit["failures"]:
        potential_counterexamples.append({
            "failure": "normalizer is not equivariant under S6 generators",
            "details": label_generator_audit["failures"],
        })

    normalized_groups: Dict[str, List[int]] = {}
    raw_groups: Dict[str, List[int]] = {}
    for index, row in enumerate(rows):
        normalized_groups.setdefault(row["normalized_code"], []).append(index)
        raw_groups.setdefault(row["raw_code"], []).append(index)
    canonical_isomorphism_failures = list(
        _audit_colored_collision_representatives(rows, normalized_groups)
    )
    unacceptable_collisions = []
    unclassified_quotient_collisions = []
    declared_core_automorphism_group_count = 0
    declared_q8_carrier_group_count = 0
    q8_only_collision_pairs = 0
    normalized_collision_pairs = 0
    for indices in normalized_groups.values():
        declared_keys = {
            rows[index]["declared_primitive_orbit_id"] for index in indices
        }
        if len(declared_keys) != 1:
            unclassified_quotient_collisions.append(tuple(indices))
        origins = {
            (
                rows[index]["core"],
                rows[index]["repair"],
                rows[index]["sample_attachment"],
                rows[index]["hidden_focal_samples"],
            )
            for index in indices
        }
        if len(origins) > 1:
            declared_core_automorphism_group_count += 1
        if any(
            len({
                rows[index]["carrier_word"]
                for index in indices
                if (
                    rows[index]["core"],
                    rows[index]["repair"],
                    rows[index]["sample_attachment"],
                    rows[index]["hidden_focal_samples"],
                ) == origin
            }) > 1
            for origin in origins
        ):
            declared_q8_carrier_group_count += 1
        normalized_collision_pairs += len(indices) * (len(indices) - 1) // 2
        raw_multiplicities: Dict[str, int] = {}
        for index in indices:
            raw_code = rows[index]["raw_code"]
            raw_multiplicities[raw_code] = raw_multiplicities.get(raw_code, 0) + 1
        same_raw_pairs = sum(
            multiplicity * (multiplicity - 1) // 2
            for multiplicity in raw_multiplicities.values()
        )
        q8_only_collision_pairs += (
            len(indices) * (len(indices) - 1) // 2 - same_raw_pairs
        )
    if canonical_isomorphism_failures:
        unacceptable_collisions.extend(canonical_isomorphism_failures)
    normalized_codes_by_declared_key: Dict[int, set] = {}
    for row in rows:
        normalized_codes_by_declared_key.setdefault(
            row["declared_primitive_orbit_id"],
            set(),
        ).add(row["normalized_code"])
    unclassified_quotient_splits = tuple(
        (key, tuple(sorted(codes)))
        for key, codes in normalized_codes_by_declared_key.items()
        if len(codes) != 1
    )
    if unclassified_quotient_collisions or unclassified_quotient_splits:
        potential_counterexamples.append({
            "failure": "normalized collisions do not equal declared automorphism/Q8 orbits",
            "collision_groups": tuple(unclassified_quotient_collisions),
            "split_groups": unclassified_quotient_splits,
        })

    critical_route_rejections = tuple(
        rejection for rejection in behavioral_rejections
        if rejection.get("reason") == "route-not-stopped-before-next-routing-event"
    )
    if critical_route_rejections:
        potential_counterexamples.extend(critical_route_rejections)
    certificates = tuple(
        certificate
        for record in configuration_records
        for certificate in record["fan_certificates"]
    )
    if joint_configuration_count != 36:
        potential_counterexamples.append({
            "failure": "joint behavior-derived configuration catalog is incomplete",
            "observed": joint_configuration_count,
            "expected": 36,
        })
    expected_per_core = {
        "cycle": 4,
        "theta0": 4,
        "theta1": 4,
        "theta2": 16,
        "theta3": 8,
    }
    if per_core_joint_configuration_counts != expected_per_core:
        potential_counterexamples.append({
            "failure": "per-core joint configuration count drifted",
            "observed": dict(per_core_joint_configuration_counts),
            "expected": expected_per_core,
        })
    if relative_label_orbit_audit["failures"]:
        potential_counterexamples.append({
            "failure": "relative fixed-label collision lacks a primitive orbit mapping",
            "details": relative_label_orbit_audit["failures"],
        })
    return {
        "repair_count": repair_count,
        "fixed_sample_count": FIXED_LOCAL_SAMPLE_COUNT,
        "fixed_sampling_map": tuple(
            (f"sample-{index}", f"taxon-{index}")
            for index in range(FIXED_LOCAL_SAMPLE_COUNT)
        ),
        "structural_realizable_cone_count": structural_realizable_cone_count,
        "joint_configuration_count": joint_configuration_count,
        "per_core_joint_configuration_counts": dict(
            per_core_joint_configuration_counts
        ),
        "simultaneous_both_hidden_configuration_count": (
            simultaneous_both_hidden_configuration_count
        ),
        "incomparable_order_case_count": len(incomparable_order_audits),
        "incomparable_order_realization_count": sum(
            record["variant_count"] for record in incomparable_order_audits
        ),
        "fixed_label_configuration_count": len(configuration_records),
        "raw_joint_carrier_count": len(rows),
        "relative_label_orbit_audit": relative_label_orbit_audit,
        "normalizer_label_generator_audit": label_generator_audit,
        "raw_orbit_count": len(raw_groups),
        "normalized_signature_count": len(normalized_groups),
        "normalized_collision_pair_count": normalized_collision_pairs,
        "q8_only_collision_pair_count": q8_only_collision_pairs,
        "canonical_isomorphism_failures": tuple(canonical_isomorphism_failures),
        "unacceptable_collisions": tuple(unacceptable_collisions),
        "unclassified_quotient_collisions": tuple(unclassified_quotient_collisions),
        "unclassified_quotient_splits": unclassified_quotient_splits,
        "declared_core_automorphism_group_count": (
            declared_core_automorphism_group_count
        ),
        "declared_q8_carrier_group_count": declared_q8_carrier_group_count,
        "declared_primitive_orbit_count": declared_primitive_orbit_count,
        "declared_orbit_witnesses": declared_orbit_witnesses,
        "coverage_scope": (
            "fixed-(X,S,s) six-sample structural stopping/reattachment regression; "
            "all 6! relative label placements are exhausted on reduced records"
        ),
        "behaviorally_rejected_candidates": tuple(behavioral_rejections),
        "joint_compatibility_rejections": tuple(joint_compatibility_rejections),
        "critical_route_rejections": critical_route_rejections,
        "maximum_simultaneous_hidden_fans": max(
            (len(record["hidden_reticulations"]) for record in configuration_records),
            default=0,
        ),
        "maximum_hidden_reticulations_per_fan": max(
            (certificate["hidden_reticulation_count"] for certificate in certificates),
            default=0,
        ),
        "maximum_typed_outlets_per_fan": max(
            (certificate["typed_outlet_count"] for certificate in certificates),
            default=0,
        ),
        "maximum_weight_separating_anchors_per_fan": max(
            (certificate["weight_separating_anchor_count"] for certificate in certificates),
            default=0,
        ),
        "maximum_typed_first_outlet_anchors_per_fan": max(
            (certificate["typed_first_outlet_anchor_count"] for certificate in certificates),
            default=0,
        ),
        "maximum_future_null_dimension": max(
            (certificate["future_null_dimension"] for certificate in certificates),
            default=0,
        ),
        "potential_counterexamples": tuple(potential_counterexamples),
        "incomparable_order_audits": tuple(incomparable_order_audits),
        "configuration_records": tuple(configuration_records),
        "rows": tuple(rows),
    }


def exact_first_hit_composed_response(
    initial_weights: Sequence,
    transition_matrices: Sequence[sp.Matrix],
    continuation: sp.Matrix,
    output_types: Sequence[str],
) -> tuple:
    """Canonical response of a maximal nested fan, independent of contraction order."""
    current = sp.Matrix([[sp.sympify(value) for value in initial_weights]])
    if sp.simplify(sum(current) - 1) != 0:
        raise ValueError("initial first-hit weights must sum to one")
    for transition in transition_matrices:
        transition = sp.Matrix(transition)
        if current.cols != transition.rows:
            raise ValueError("nested first-hit dimensions do not compose")
        for row in range(transition.rows):
            if sp.simplify(sum(transition[row, column] for column in range(transition.cols)) - 1) != 0:
                raise ValueError("each nested first-hit transition row must sum to one")
        current = sp.simplify(current * transition)
    continuation = sp.Matrix(continuation)
    if current.cols != continuation.rows or continuation.cols != len(output_types):
        raise ValueError("continuation dimensions do not match first-hit frontier")
    response = sp.simplify(current * continuation)
    combined: Dict[str, sp.Expr] = {}
    for output_type, value in zip(output_types, list(response)):
        combined[output_type] = sp.simplify(
            combined.get(output_type, sp.Integer(0)) + value
        )
    return tuple(
        (output_type, value)
        for output_type, value in sorted(combined.items())
        if sp.simplify(value) != 0
    )


def nested_fan_first_hit_transport(
    outer_weights: Sequence,
    inner_weights: Sequence,
) -> tuple:
    """Flatten one nested exit before its first exposure; the other exits directly."""
    if len(outer_weights) != 2 or len(inner_weights) != 2:
        raise ValueError("bounded nested fixture uses two binary routing fans")
    outer = sp.Matrix([[sp.sympify(value) for value in outer_weights]])
    inner_left, inner_right = map(sp.sympify, inner_weights)
    transition = sp.Matrix(
        [[inner_left, inner_right, 0], [0, 0, 1]]
    )
    if sp.simplify(sum(outer) - 1) != 0 or sp.simplify(inner_left + inner_right - 1) != 0:
        raise ValueError("nested fan weights must be stochastic")
    return tuple(sp.simplify(value) for value in list(outer * transition))


def q1_q7_retention_certificate(fan: UnaryRoutingFan) -> dict:
    extended = extend_fan_across_actual_exposure(fan)
    return {
        "moves": OLD_PRINCIPAL_QUOTIENT_MOVES,
        "retained_time_by_move": tuple(
            (move, fan.reticulation_time) for move in OLD_PRINCIPAL_QUOTIENT_MOVES
        ),
        "retained_signature": q1_q7_unary_fan_signature(fan),
        "retained_reticulation_time": fan.reticulation_time,
        "whole_fan_is_two_terminal_corridor": len(fan.first_exposure_ports) == 1,
        "single_upper_extension_is_safe": is_safe_preexposure_unary_fan(extended),
        "extension_maximum_occupancy": extended.maximum_internal_occupancy,
        "extension_internal_sample_entries": extended.internal_sample_entries,
    }


def preexposure_complete_local_kernel(
    fan: UnaryRoutingFan,
    exposed_rate,
) -> dict:
    """Complete marked two-state kernel up to and beyond first exposure.

    The arbitrary symbolic continuation shows that equality of this boundary
    kernel composes with every common upper marked-history continuation.
    """
    if not is_safe_preexposure_unary_fan(fan):
        raise ValueError("local kernel requires a safely stopped unary fan")
    ports = {
        name: (time, weight)
        for name, time, _, weight in fan.first_exposure_ports
    }
    if set(ports) != {"T", "S"}:
        raise ValueError("strong-cycle fixture requires stopping ports T and S")
    a, gamma = ports["T"]
    d, other_weight = ports["S"]
    if gamma + other_weight != 1 or not a < d:
        raise ValueError("invalid strong-cycle stopping transport")
    lam = sp.sympify(exposed_rate)
    if lam.is_positive is False or lam == 0:
        raise ValueError("exposed rate must be positive")
    delta = sp.Rational((d - a).numerator, (d - a).denominator)
    gamma_symbolic = sp.Rational(gamma.numerator, gamma.denominator)
    u = sp.Symbol("u", positive=True)
    survival_exposed = sp.exp(-lam * delta)
    density = sp.simplify(gamma_symbolic * lam * sp.exp(-lam * u))
    survive = sp.simplify(1 - gamma_symbolic + gamma_symbolic * survival_exposed)
    merge = sp.simplify(gamma_symbolic * (1 - survival_exposed))
    kernel = sp.Matrix([[survive, merge], [0, 1]])
    c00, c01, c10, c11 = sp.symbols("c00 c01 c10 c11")
    arbitrary_upper = sp.Matrix([[c00, c01], [c10, c11]])
    return {
        "route_transport": sp.Matrix([[gamma_symbolic, 1 - gamma_symbolic]]),
        "marked_xz_density": density,
        "density_elapsed_support": (Fraction(0), d - a),
        "metric_support_start": private_side_support_start(fan),
        "no_merger_to_S": survive,
        "merged_before_S": merge,
        "state_kernel": kernel,
        "arbitrary_upper_continuation": sp.simplify(kernel * arbitrary_upper),
    }


def build_preexposure_strong_cycle_fixture(
    h: Fraction,
    a: Fraction = Fraction(3),
    d: Fraction = Fraction(5),
    r: Fraction = Fraction(7),
    gamma: Fraction = Fraction(1, 3),
    exposed_rate: Fraction = Fraction(2),
    unary_rates: Mapping[str, Fraction] | None = None,
) -> nx.MultiDiGraph:
    """Strict binary strong level-1 cycle with one pre-exposure routed block."""
    h, a, d, r, gamma, exposed_rate = map(
        Fraction, (h, a, d, r, gamma, exposed_rate)
    )
    if unary_rates is None:
        unary_rates = {"X-x": Fraction(5), "T-X": Fraction(7), "S-X": Fraction(11)}
    rates = {name: Fraction(rate) for name, rate in unary_rates.items()}
    if not (0 < h < a < d < r):
        raise ValueError("fixture requires 0 < h < a < d < r")
    if not (0 < gamma < 1) or exposed_rate <= 0 or any(rate <= 0 for rate in rates.values()):
        raise ValueError("fixture probabilities and rates must be positive")
    graph = nx.MultiDiGraph()
    for node, role, time in (
        ("R", "root", r),
        ("S", "tree", d),
        ("T", "tree", a),
        ("X", "retic", h),
        ("w", "leaf", Fraction(0)),
        ("z", "leaf", Fraction(0)),
        ("x", "leaf", Fraction(0)),
    ):
        graph.add_node(node, role=role, time=time)
    edge_data = (
        ("R", "S", "R-S", Fraction(13), None),
        ("R", "w", "R-w", Fraction(17), None),
        ("S", "T", "S-T", exposed_rate, None),
        ("S", "X", "S-X", rates["S-X"], 1 - gamma),
        ("T", "z", "T-z", Fraction(19), None),
        ("T", "X", "T-X", rates["T-X"], gamma),
        ("X", "x", "X-x", rates["X-x"], None),
    )
    for tail, head, key, rate, inheritance in edge_data:
        graph.add_edge(
            tail,
            head,
            key=key,
            rate=rate,
            inheritance=inheritance,
        )
    return graph


def is_level_one_fixture(graph: nx.MultiDiGraph) -> bool:
    if not nx.is_directed_acyclic_graph(graph):
        return False
    reticulations = {
        node for node, data in graph.nodes(data=True) if data.get("role") == "retic"
    }
    if not reticulations:
        return False
    simple = nx.Graph(graph)
    return all(
        len(reticulations.intersection(component)) <= 1
        for component in nx.biconnected_components(simple)
    )


def preexposure_unary_fan_certificate(
    h: Fraction = Fraction(1),
    h_prime: Fraction = Fraction(2),
) -> dict:
    a, d, r = Fraction(3), Fraction(5), Fraction(7)
    gamma, exposed_rate = Fraction(1, 3), Fraction(2)
    left_rates = {"X-x": Fraction(5), "T-X": Fraction(7), "S-X": Fraction(11)}
    right_rates = {"X-x": Fraction(23), "T-X": Fraction(29), "S-X": Fraction(31)}
    left_fan = build_preexposure_unary_fan(h, gamma, a, d, left_rates)
    right_fan = build_preexposure_unary_fan(h_prime, gamma, a, d, right_rates)
    left_graph = build_preexposure_strong_cycle_fixture(
        h, a, d, r, gamma, exposed_rate, left_rates
    )
    right_graph = build_preexposure_strong_cycle_fixture(
        h_prime, a, d, r, gamma, exposed_rate, right_rates
    )
    left_kernel = preexposure_complete_local_kernel(left_fan, exposed_rate)
    right_kernel = preexposure_complete_local_kernel(right_fan, exposed_rate)
    left_continuation = scalar_separated_fan_continuation(left_fan)
    right_continuation = scalar_separated_fan_continuation(right_fan)
    return {
        "left_graph": left_graph,
        "right_graph": right_graph,
        "left_fan": left_fan,
        "right_fan": right_fan,
        "left_kernel": left_kernel,
        "right_kernel": right_kernel,
        "left_continuation": left_continuation,
        "right_continuation": right_continuation,
        "complete_local_kernel_equal": left_kernel == right_kernel,
        "old_q1_q7_equal": q1_q7_unary_fan_signature(left_fan)
        == q1_q7_unary_fan_signature(right_fan),
        "q8_fan_slide_equal": fan_slide_equivalent(
            left_fan,
            right_fan,
            left_continuation,
            right_continuation,
        ),
        "left_q1_q7": q1_q7_retention_certificate(left_fan),
        "right_q1_q7": q1_q7_retention_certificate(right_fan),
    }


def build_stc_rank_one_nonbridge_fixture() -> nx.MultiDiGraph:
    """A strict binary repaired cycle producing an old rank-one false positive.

    Edges point from older to younger populations.  The port ``p`` has sampled
    side leaf ``z``; reticulation ``h`` has terminal child ``A``.  A second root
    child ``w`` makes the displayed fixture a complete rooted binary graph.
    """
    graph = nx.MultiDiGraph()
    for node, role, time in (
        ("root", "root", Fraction(5)),
        ("S", "tree", Fraction(4)),
        ("p", "tree", Fraction(3)),
        ("h", "retic", Fraction(1)),
        ("A", "leaf", Fraction(0)),
        ("z", "leaf", Fraction(0)),
        ("w", "leaf", Fraction(0)),
    ):
        graph.add_node(node, role=role, time=time)
    for index, (tail, head) in enumerate(
        (("root", "S"), ("root", "w"), ("S", "p"), ("S", "h"),
         ("p", "h"), ("p", "z"), ("h", "A"))
    ):
        graph.add_edge(tail, head, key=str(index))
    return graph


def is_rooted_binary_fixture(graph: nx.MultiDiGraph, root: str = "root") -> bool:
    """Validate the full binary degrees and strict time order of a fixture."""
    if root not in graph or graph.in_degree(root) != 0 or graph.out_degree(root) != 2:
        return False
    for node, data in graph.nodes(data=True):
        role = data.get("role")
        indegree, outdegree = graph.in_degree(node), graph.out_degree(node)
        if role == "root" and (node != root or indegree != 0 or outdegree != 2):
            return False
        if role == "tree" and (indegree != 1 or outdegree != 2):
            return False
        if role == "retic" and (indegree != 2 or outdegree != 1):
            return False
        if role == "leaf" and (indegree != 1 or outdegree != 0):
            return False
    return all(
        graph.nodes[tail]["time"] > graph.nodes[head]["time"]
        for tail, head, _ in graph.edges(keys=True)
    )


def rank_one_nonbridge_certificate(gamma=sp.Rational(1, 2), arm_survival=None):
    """Exact old-separator rows for the repaired-cycle false positive.

    The first one-block row comes from a merger below the reticulation and the
    second from a merger on one of two equal-rate arms.  Identity future columns
    deliberately give the strongest possible scalar test of their posteriors.
    """
    gamma = sp.sympify(gamma)
    if arm_survival is None:
        arm_survival = sp.Symbol("E", positive=True)
    arm_survival = sp.sympify(arm_survival)
    one_block_rows = sp.Matrix([
        [gamma, 1 - gamma],
        [gamma**2 * arm_survival, (1 - gamma) ** 2 * arm_survival],
    ])
    two_block_rows = sp.Matrix([[
        gamma**2 * arm_survival,
        gamma * (1 - gamma),
        gamma * (1 - gamma),
        (1 - gamma) ** 2 * arm_survival,
    ]])
    graph = build_stc_rank_one_nonbridge_fixture()
    simple = nx.Graph(graph)
    graph_bridges = {frozenset(edge) for edge in nx.bridges(simple)}
    retic_arm_is_bridge = frozenset(("p", "h")) in graph_bridges
    return {
        "graph": graph,
        "one_block_rows": one_block_rows,
        "two_block_rows": two_block_rows,
        "all_old_kernels_rank_one": one_block_rows.rank() == 1 and two_block_rows.rank() == 1,
        "no_cross_merger_strictly_before_port": graph.nodes["p"]["time"] > graph.nodes["h"]["time"],
        "retic_arm_is_graph_bridge": retic_arm_is_bridge,
    }


def side_free_suppressed_cycle() -> Core:
    """Primitive side-free parallel cycle before any strong repair is inserted."""
    return Core(
        name="sidefree_cycle",
        arcs=(("S", "X"), ("S", "X")),
        retics=("X",),
        sinks=("X",),
        repairs=(),
    )


def side_free_cycle_domain_certificate() -> dict:
    core = side_free_suppressed_cycle()
    graph = build_repaired_core(core, ())
    tree_child = is_local_tree_child(graph)
    strong = is_local_strong_tree_child(graph)
    return {
        "tree_child": tree_child,
        "strong_tail": strong,
        "combined_domain": tree_child and strong,
        "minimal_repairs": enumerate_minimal_repairs(core),
    }


def staggered_balance_certificate() -> dict:
    """Exact temporally separated posterior-balance suffix exchange.

    Time is measured in units of log(2), so a cumulative hazard H contributes
    the exact survival factor 2**(-H).
    """
    gamma = Fraction(1, 3)
    weight_1 = gamma**2 * Fraction(1, 2**9)
    weight_2 = (1 - gamma) ** 2 * Fraction(1, 2**11)
    split = 2 * gamma * (1 - gamma)
    v = sp.Symbol("v", nonnegative=True)
    w = sp.Rational(weight_1.numerator, weight_1.denominator)
    chambers = (
        # elapsed suffix interval, cumulative hazards, active rates
        ((0, 1), 3 * v, 3 * v, 3, 3),
        ((1, 2), 4 * v - 1, 3 * v, 4, 3),
        ((2, None), 4 * v - 1, 5 * v - 4, 4, 5),
    )
    chamber_checks = []
    for interval, hazard_a, hazard_b, rate_a, rate_b in chambers:
        survival_n = sp.Rational(split.numerator, split.denominator) + w * (
            2 ** (-hazard_a) + 2 ** (-hazard_b)
        )
        survival_prime = sp.Rational(split.numerator, split.denominator) + w * (
            2 ** (-hazard_b) + 2 ** (-hazard_a)
        )
        density_n = w * (
            rate_a * 2 ** (-hazard_a) + rate_b * 2 ** (-hazard_b)
        )
        density_prime = w * (
            rate_b * 2 ** (-hazard_b) + rate_a * 2 ** (-hazard_a)
        )
        chamber_checks.append({
            "interval": interval,
            "survival_difference": sp.simplify(survival_n - survival_prime),
            "density_difference": sp.simplify(density_n - density_prime),
        })
    schedules_n = (
        ((0, 1), (3, 3), (6, 4)),
        ((0, 2), (4, 3), (7, 5)),
    )
    schedules_prime = (
        ((0, 1), (3, 3), (7, 5)),
        ((0, 2), (4, 3), (6, 4)),
    )
    return {
        "gamma": gamma,
        "events": (3, 4, 6, 7),
        "weight_1": weight_1,
        "weight_2": weight_2,
        "split_mass": split,
        "one_block_route_mass": gamma + (1 - gamma),
        "chambers": tuple(chamber_checks),
        "schedules_n": schedules_n,
        "schedules_prime": schedules_prime,
        "identity_or_global_exchange": schedules_prime in (schedules_n, schedules_n[::-1]),
    }


def anchored_tagged_merger_masses() -> dict:
    """A physical side tag distinguishes the staggered exchanged suffixes.

    On the interval (6 log 2, 7 log 2), suffix A has merger mass 15/128
    and suffix B has mass 14/128 conditional on survival to the cut.  A later
    common anchor interval of rate six and length log 2 tags the physical arm.
    """
    balanced_weight = Fraction(1, 4608)
    suffix_a = Fraction(1, 2**3) - Fraction(1, 2**7)
    suffix_b = Fraction(1, 2**3) - Fraction(1, 2**6)
    anchor_join = 1 - Fraction(1, 2**6)
    tagged_n = balanced_weight * suffix_a * anchor_join
    tagged_prime = balanced_weight * suffix_b * anchor_join
    return {
        "suffix_a_interval_mass": suffix_a,
        "suffix_b_interval_mass": suffix_b,
        "anchor_join_mass": anchor_join,
        "untagged_n": balanced_weight * (suffix_a + suffix_b),
        "untagged_prime": balanced_weight * (suffix_b + suffix_a),
        "tagged_n": tagged_n,
        "tagged_prime": tagged_prime,
        "tagged_difference": tagged_n - tagged_prime,
    }


def anchored_route_separator_matrix(lam_p=2, lam_q=3, u_1=sp.Rational(1, 10), u_2=sp.Rational(1, 5)):
    """Triangular actual-suffix matrix separating PP, PQ, QP, QQ states."""
    lam_p, lam_q, u_1, u_2 = map(sp.sympify, (lam_p, lam_q, u_1, u_2))
    two_mergers_pp = lam_p**2 * sp.exp(-3 * lam_p * u_1) * sp.exp(-lam_p * (u_2 - u_1))
    one_pp = lam_p * sp.exp(-3 * lam_p * u_1)
    one_pq = lam_p * sp.exp(-lam_p * u_1)
    one_qq = lam_q * sp.exp(-lam_q * u_1)
    return sp.Matrix([
        [two_mergers_pp, one_pp, one_pp, one_pp],
        [0, one_pq, 0, 0],
        [0, 0, one_pq, 0],
        [0, 0, 0, one_qq],
    ])


EXPOSURE_LOSS_REPAIR_CASES = {
    ("theta0", (2, 3)): {
        "child_segment": 3,
        "typing_segment": 2,
        "typing_kind": "U-to-X-bypass-sibling-at-U",
        "label_triple": ("C_X", "L3", "L2"),
        "v_incoming": (("S", "1", 1), ("U", "4", 4)),
        "v_parent_incidences": (("S", "1", 1), ("U", "4", 4)),
        "v_outgoing": (("p3", "3a", 3),),
        "x_incoming": (("p2", "2b", 2), ("p3", "3b", 3)),
        "x_child_outlet": ("p3", "3b", 3),
        "x_bypass_outlet": ("p2", "2b", 2),
        "parent_change_order": ("physical-parent-0", "physical-parent-1"),
    },
    ("theta0", (3, 4)): {
        "child_segment": 3,
        "typing_segment": 4,
        "typing_kind": "nested-U-to-V-parent-arm",
        "label_triple": ("C_X", "L3", "L4"),
        "v_incoming": (("S", "1", 1), ("p4", "4b", 4)),
        "v_parent_incidences": (("S", "1", 1), ("p4", "4b", 4)),
        "v_outgoing": (("p3", "3a", 3),),
        "x_incoming": (("U", "2", 2), ("p3", "3b", 3)),
        "x_child_outlet": ("p3", "3b", 3),
        "x_bypass_outlet": ("U", "2", 2),
        "parent_change_order": ("physical-parent-0", "physical-parent-1"),
    },
    ("theta1", (2, 3)): {
        "child_segment": 2,
        "typing_segment": 3,
        "typing_kind": "first-U-to-V-parent-arm",
        "label_triple": ("C_X", "L2", "L3"),
        "v_incoming": (("p3", "3b", 3), ("U", "4", 4)),
        "v_parent_incidences": (("U", "4", 4), ("p3", "3b", 3)),
        "v_outgoing": (("p2", "2a", 2),),
        "x_incoming": (("S", "1", 1), ("p2", "2b", 2)),
        "x_child_outlet": ("p2", "2b", 2),
        "x_bypass_outlet": ("S", "1", 1),
        "parent_change_order": ("physical-parent-0", "physical-parent-1"),
    },
    ("theta1", (2, 4)): {
        "child_segment": 2,
        "typing_segment": 4,
        "typing_kind": "second-U-to-V-parent-arm",
        "label_triple": ("C_X", "L2", "L4"),
        "v_incoming": (("U", "3", 3), ("p4", "4b", 4)),
        "v_parent_incidences": (("U", "3", 3), ("p4", "4b", 4)),
        "v_outgoing": (("p2", "2a", 2),),
        "x_incoming": (("S", "1", 1), ("p2", "2b", 2)),
        "x_child_outlet": ("p2", "2b", 2),
        "x_bypass_outlet": ("S", "1", 1),
        "parent_change_order": ("physical-parent-0", "physical-parent-1"),
    },
}


def exposure_loss_observable_cells(
    p_x,
    q_v,
    child_rate,
    child_prefix,
    survived_child_weight,
    parent_rate_1,
    parent_rate_2,
    parent_prefix_1=0,
    parent_prefix_2=0,
    u=None,
) -> dict:
    """Exact scalar cells on the two sides of the exposure-loss breakpoint."""
    u = sp.Symbol("u", nonnegative=True) if u is None else sp.sympify(u)
    p_x, q_v = map(sp.sympify, (p_x, q_v))
    child_rate, child_prefix = map(sp.sympify, (child_rate, child_prefix))
    survived_child_weight = sp.sympify(survived_child_weight)
    parent_rate_1, parent_rate_2 = map(
        sp.sympify,
        (parent_rate_1, parent_rate_2),
    )
    parent_prefix_1, parent_prefix_2 = map(
        sp.sympify,
        (parent_prefix_1, parent_prefix_2),
    )
    if any(value.is_positive is False for value in (
        p_x,
        1 - p_x,
        q_v,
        1 - q_v,
        child_rate,
        survived_child_weight,
        parent_rate_1,
        parent_rate_2,
    )):
        raise ValueError("exposure-loss fixture parameters must be strictly positive")
    bypass = sp.simplify(1 - p_x)
    child_atom = sp.exp(-(child_prefix + child_rate * u))
    first_merger_density = sp.simplify(
        p_x * child_rate * child_atom
    )
    below_survival = sp.simplify(bypass + p_x * child_atom)
    split_atom = sp.simplify(
        2 * survived_child_weight * q_v * (1 - q_v)
    )
    parent_atom_1 = sp.simplify(
        survived_child_weight
        * q_v**2
        * sp.exp(-(parent_prefix_1 + parent_rate_1 * u))
    )
    parent_atom_2 = sp.simplify(
        survived_child_weight
        * (1 - q_v) ** 2
        * sp.exp(-(parent_prefix_2 + parent_rate_2 * u))
    )
    above_survival = sp.simplify(
        bypass + split_atom + parent_atom_1 + parent_atom_2
    )
    return {
        "u": u,
        "first_merger_density": first_merger_density,
        "below_survival": below_survival,
        "above_survival": above_survival,
    }


def _exact_graph_record(graph: nx.MultiDiGraph) -> tuple:
    nodes = tuple(sorted((
        (str(node), tuple(sorted((str(key), repr(value)) for key, value in data.items())))
        for node, data in graph.nodes(data=True)
    ), key=repr))
    edges = tuple(sorted((
        (
            str(tail),
            str(head),
            repr(key),
            tuple(sorted((str(name), repr(value)) for name, value in data.items())),
        )
        for tail, head, key, data in graph.edges(keys=True, data=True)
    ), key=repr))
    return nodes, edges


def recover_two_exponential_total_law(
    total_survival,
    scale,
    u,
) -> dict:
    """Invert a constant plus one/two positive exponentials from total-law moments.

    No latent component is supplied.  The constant is the analytic limit of
    the total observable survival, and the normalized moments are derivatives
    of the remaining total germ.
    """
    total_survival = sp.sympify(total_survival)
    scale = sp.sympify(scale)
    u = sp.sympify(u)
    constant = sp.simplify(sp.limit(total_survival, u, sp.oo))
    germ = sp.simplify(total_survival - constant)
    moments = tuple(
        sp.simplify((-1) ** order * sp.diff(germ, u, order).subs(u, 0) / scale)
        for order in range(4)
    )
    m0, m1, m2, m3 = moments
    determinant = sp.simplify(m0 * m2 - m1**2)
    if determinant == 0:
        rate = sp.simplify(m1 / m0)
        if rate.is_positive is False or m0.is_positive is False:
            raise ValueError("rank-one exponential germ is not strictly positive")
        return {
            "branch": "equal-rate",
            "constant": constant,
            "germ": germ,
            "moments": moments,
            "hankel_determinant": determinant,
            "components": ((rate, m0),),
            "reconstructed_total": sp.simplify(
                constant + scale * m0 * sp.exp(-rate * u)
            ),
        }
    sum_rates = sp.simplify((m0 * m3 - m1 * m2) / determinant)
    product_rates = sp.simplify((m1 * m3 - m2**2) / determinant)
    z = sp.Symbol("z_exposure_rate")
    rates = tuple(sorted(
        sp.solve(sp.Eq(z**2 - sum_rates * z + product_rates, 0), z),
        key=sp.default_sort_key,
    ))
    if len(rates) != 2 or rates[0] == rates[1]:
        raise ValueError("rank-two Prony recurrence did not yield two rates")
    rate_1, rate_2 = rates
    weight_1 = sp.simplify((rate_2 * m0 - m1) / (rate_2 - rate_1))
    weight_2 = sp.simplify((m1 - rate_1 * m0) / (rate_2 - rate_1))
    components = ((rate_1, weight_1), (rate_2, weight_2))
    reconstructed = sp.simplify(
        constant
        + scale * sum(
            weight * sp.exp(-rate * u) for rate, weight in components
        )
    )
    return {
        "branch": "unequal-rate",
        "constant": constant,
        "germ": germ,
        "moments": moments,
        "hankel_determinant": determinant,
        "sum_rates": sum_rates,
        "product_rates": product_rates,
        "components": components,
        "reconstructed_total": reconstructed,
    }


def _independent_exposure_loss_parameter_manifest(
    core_name: str,
    repair: Sequence[int],
    serial: int,
) -> dict:
    """Raw fixture manifest; the inverse routine never receives this object."""
    repair = tuple(repair)
    case = EXPOSURE_LOSS_REPAIR_CASES[(core_name, repair)]
    a = sp.Rational(2 + serial, 1)
    child_schedule = (
        (sp.Rational(1, 2), sp.Rational(2 + serial)),
        (sp.Rational(1, 3), sp.Rational(5 + serial)),
    )
    h_v = sp.simplify(a + sum(duration for duration, _ in child_schedule))
    parent_change_order = case["parent_change_order"]
    parent_schedule = (
        {
            "duration": sp.Rational(1, 4),
            "rates": (sp.Rational(3 + serial), sp.Rational(5 + serial)),
            "changed_parent": None,
        },
        {
            "duration": sp.Rational(1, 5),
            "rates": (sp.Rational(7 + serial), sp.Rational(5 + serial)),
            "changed_parent": parent_change_order[0],
        },
        {
            "duration": sp.Rational(1, 6),
            "rates": (sp.Rational(7 + serial), sp.Rational(11 + serial)),
            "changed_parent": parent_change_order[1],
        },
    )
    q_assignment = (sp.Rational(1, 3), sp.Rational(2, 3))
    p_x = sp.Rational(2, 5)
    return {
        "core": core_name,
        "repair": repair,
        "a": a,
        "h_v": h_v,
        "p_x": p_x,
        "q_assignment": q_assignment,
        "typed_q_assignment": tuple(
            (incidence[0], weight)
            for incidence, weight in zip(
                case["v_parent_incidences"],
                q_assignment,
            )
        ),
        "typed_x_assignment": (
            (case["x_child_outlet"][0], p_x),
            (case["x_bypass_outlet"][0], 1 - p_x),
        ),
        "child_schedule": child_schedule,
        "parent_schedule": parent_schedule,
        "equal_rate": sp.Rational(13 + serial),
        "direction_delta": sp.Rational(1, 4),
        "direction_rate": sp.Rational(17 + serial),
        "case": dict(case),
    }


def _compress_physical_rate_word(
    durations: Sequence,
    rates: Sequence,
) -> tuple:
    word = []
    for duration, rate in zip(durations, rates):
        duration, rate = map(sp.sympify, (duration, rate))
        if word and word[-1][1] == rate:
            word[-1] = (sp.simplify(word[-1][0] + duration), rate)
        else:
            word.append((duration, rate))
    return tuple(word)


def _generate_exposure_loss_observation(
    core: Core,
    manifest: Mapping,
) -> dict:
    """Generate only total marked laws and labelled anchor cells."""
    u = sp.Symbol(
        f"u_total_{manifest['core']}_{'_'.join(map(str, manifest['repair']))}",
        nonnegative=True,
    )
    p_x = manifest["p_x"]
    q_1, q_2 = manifest["q_assignment"]
    child_prefix = sp.Integer(0)
    current_time = manifest["a"]
    below = []
    for duration, rate in manifest["child_schedule"]:
        child_atom = sp.exp(-(child_prefix + rate * u))
        below.append({
            "start": current_time,
            "end": sp.simplify(current_time + duration),
            "total_survival": sp.simplify(1 - p_x + p_x * child_atom),
            "first_merger_density": sp.simplify(p_x * rate * child_atom),
        })
        current_time = sp.simplify(current_time + duration)
        child_prefix = sp.simplify(child_prefix + duration * rate)
    p_tilde = sp.simplify(p_x * sp.exp(-child_prefix))
    bypass = sp.simplify(1 - p_x)
    split = sp.simplify(2 * p_tilde * q_1 * q_2)
    parent_prefixes = [sp.Integer(0), sp.Integer(0)]
    above = []
    for chamber_index, chamber in enumerate(manifest["parent_schedule"]):
        rate_1, rate_2 = chamber["rates"]
        component_1 = sp.simplify(
            p_tilde * q_1**2
            * sp.exp(-(parent_prefixes[0] + rate_1 * u))
        )
        component_2 = sp.simplify(
            p_tilde * q_2**2
            * sp.exp(-(parent_prefixes[1] + rate_2 * u))
        )
        total = sp.simplify(bypass + split + component_1 + component_2)
        above.append({
            "start": current_time,
            "end": sp.simplify(current_time + chamber["duration"]),
            "total_survival": total,
            "anchor_cells": {
                "physical-parent-0": component_1,
                "physical-parent-1": component_2,
            },
            "changed_parent": chamber["changed_parent"],
        })
        current_time = sp.simplify(current_time + chamber["duration"])
        parent_prefixes[0] = sp.simplify(
            parent_prefixes[0] + chamber["duration"] * rate_1
        )
        parent_prefixes[1] = sp.simplify(
            parent_prefixes[1] + chamber["duration"] * rate_2
        )

    equal_observations = []
    for q in (sp.Rational(1, 3), sp.Rational(1, 2)):
        rate = manifest["equal_rate"]
        total = sp.simplify(
            bypass
            + 2 * p_tilde * q * (1 - q)
            + p_tilde * (q**2 + (1 - q) ** 2) * sp.exp(-rate * u)
        )
        equal_observations.append({
            "total_survival": total,
        })

    graph = build_repaired_core(core, manifest["repair"])
    timed_graph = graph.copy()
    _assign_strict_event_times(timed_graph)
    v_exposure_witness = _positive_two_block_support(timed_graph, "V")
    x_fans, _ = behaviorally_realizable_unary_fans(graph)
    x_fan = next(fan for fan in x_fans if fan["reticulation"] == "X")
    v_incoming_observations = tuple(sorted((
        (tail, str(key), data["segment"])
        for tail, _, key, data in graph.in_edges("V", keys=True, data=True)
    ), key=repr))
    v_outgoing_observations = tuple(sorted((
        (head, str(key), data["segment"])
        for _, head, key, data in graph.out_edges("V", keys=True, data=True)
    ), key=repr))
    x_incoming_observations = tuple(sorted((
        (tail, str(key), data["segment"])
        for tail, _, key, data in graph.in_edges("X", keys=True, data=True)
    ), key=repr))
    case = manifest["case"]
    if set(v_incoming_observations) != set(case["v_parent_incidences"]):
        raise AssertionError("physical V parent manifest disagrees with the raw graph")
    if set(x_incoming_observations) != set(case["x_incoming"]):
        raise AssertionError("physical X outlet manifest disagrees with the raw graph")
    typing_segment = manifest["case"]["typing_segment"]
    typing_port = f"p{typing_segment}"
    typing_label = f"L{typing_segment}"
    if graph.has_edge(typing_port, "X"):
        typing_kind = "U-to-X-bypass-sibling-at-U"
    elif graph.has_edge(typing_port, "V"):
        if manifest["core"] == "theta0":
            typing_kind = "nested-U-to-V-parent-arm"
        elif typing_segment == 3:
            typing_kind = "first-U-to-V-parent-arm"
        else:
            typing_kind = "second-U-to-V-parent-arm"
    else:
        raise AssertionError("typing anchor has no observable routing incidence")
    topology_cells = {
        "v_exposure_witness": v_exposure_witness,
        "v_incoming_observations": v_incoming_observations,
        "v_outgoing_observations": v_outgoing_observations,
        "physical_parent_incidences": {
            "physical-parent-0": case["v_parent_incidences"][0],
            "physical-parent-1": case["v_parent_incidences"][1],
        },
        "x_child_corridor_tail": case["x_child_outlet"][0],
        "typing_kind": typing_kind,
        "typing_label": typing_label,
        "label_triple": (
            "C_X",
            f"L{manifest['case']['child_segment']}",
            typing_label,
        ),
    }
    x_child_corridor_tail = topology_cells["x_child_corridor_tail"]
    if (
        case["x_child_outlet"] not in x_incoming_observations
        or not graph.has_edge(x_child_corridor_tail, "X")
    ):
        raise AssertionError("V child corridor does not enter the X routing fan")
    if case["x_bypass_outlet"] not in x_incoming_observations:
        raise AssertionError("X routing fan does not have one typed bypass arm")
    stored_x_macro = {
        "focal": x_fan["focal"],
        "parents": tuple(x_fan["parents"]),
        "child_corridor_tail": x_child_corridor_tail,
        "bypass_tail": case["x_bypass_outlet"][0],
        "incoming": x_incoming_observations,
        "outgoing": (("C_X", "child_X", "sink_child"),),
        "typed_weights": (
            (x_child_corridor_tail, p_x),
            (case["x_bypass_outlet"][0], 1 - p_x),
        ),
    }

    residual = graph.copy()
    residual.remove_node("C_X")
    residual.remove_node("X")
    residual_v_fans, _ = behaviorally_realizable_unary_fans(residual)
    residual_v_fan = next(
        fan for fan in residual_v_fans if fan["reticulation"] == "V"
    )
    residual.remove_node("V")
    residual.add_node("residual-q8:V", role="macro")
    for index, (tail, _, _) in enumerate(v_incoming_observations):
        residual.add_edge(tail, "residual-q8:V", key=f"macro-in:{index}")
    for index, (head, _, _) in enumerate(v_outgoing_observations):
        residual.add_edge("residual-q8:V", head, key=f"macro-out:{index}")

    direction_observation = triangle_forward(
        q_1,
        manifest["direction_rate"],
        manifest["direction_delta"],
        u,
    )
    return {
        "u": u,
        "p_x": p_x,
        "below_chambers": tuple(below),
        "above_chambers": tuple(above),
        "equal_rate_observations": tuple(equal_observations),
        "topology_cells": topology_cells,
        "stored_x_macro": stored_x_macro,
        "residual_q8_graph": residual,
        "residual_v_fan": residual_v_fan,
        "direction_observation": direction_observation,
        "direction_rate": manifest["direction_rate"],
        "direction_delta": manifest["direction_delta"],
    }


def _type_prony_components_from_anchor_cells(
    inversion: Mapping,
    anchor_cells: Mapping[str, sp.Expr],
    scale,
    u,
) -> dict:
    """Type physical routes from observable route-exclusive anchor germs.

    A total-law Prony atom can merge two physical routes when their rates are
    equal.  The separately marked anchor cells still expose each route's
    coefficient.  Recover those physical atoms directly and verify that their
    rate-grouped sum is exactly the independently recovered total-law
    decomposition.
    """
    typed = {}
    for physical_parent, anchor_cell in anchor_cells.items():
        anchor_cell = sp.sympify(anchor_cell)
        rate = sp.simplify(-sp.diff(anchor_cell, u) / anchor_cell)
        weight = sp.simplify(anchor_cell.subs(u, 0) / scale)
        if rate.is_positive is False or weight.is_positive is False:
            raise ValueError("anchor cell is not a positive exponential germ")
        if sp.simplify(
            scale * weight * sp.exp(-rate * u) - anchor_cell
        ) != 0:
            raise ValueError("anchor cell is not a single exponential germ")
        typed[physical_parent] = (rate, weight)

    grouped = {}
    for rate, weight in typed.values():
        grouped[rate] = sp.simplify(grouped.get(rate, 0) + weight)
    recovered_grouped = {
        sp.sympify(rate): sp.sympify(weight)
        for rate, weight in inversion["components"]
    }
    if grouped != recovered_grouped:
        raise ValueError("typed anchor atoms do not sum to the total-law Prony germ")
    return typed


def _inheritance_pair_from_sum_squares(sum_squares) -> tuple:
    """Recover the Bernoulli pair, retaining the double root at q=1/2."""
    sum_squares = sp.sympify(sum_squares)
    discriminant = sp.simplify(2 * sum_squares - 1)
    root = sp.simplify(sp.sqrt(discriminant))
    pair = tuple(sorted((
        sp.simplify((1 - root) / 2),
        sp.simplify((1 + root) / 2),
    ), key=sp.default_sort_key))
    if any(value.is_positive is False for value in pair):
        raise ValueError("total-law coefficient does not yield positive routes")
    if sp.simplify(sum(value**2 for value in pair) - sum_squares) != 0:
        raise ValueError("Bernoulli inversion does not recover the coefficient")
    return pair


def _recover_exposure_loss_record_from_total_laws(
    observation: Mapping,
) -> dict:
    """Recover E using total scalar laws; anchor cells only type atoms."""
    u = observation["u"]
    p_x = observation["p_x"]
    below_zero_atoms = tuple(
        sp.simplify(sp.limit(chamber["total_survival"], u, sp.oo))
        for chamber in observation["below_chambers"]
    )
    if len(set(below_zero_atoms)) != 1:
        raise ValueError("below-V bypass zero atom is not chamber-invariant")
    bypass = below_zero_atoms[0]
    child_rates = []
    child_durations = []
    for chamber in observation["below_chambers"]:
        germ = sp.simplify(chamber["total_survival"] - bypass)
        recovered_rate = sp.simplify(-sp.diff(germ, u) / germ)
        if sp.simplify(
            chamber["first_merger_density"] + sp.diff(
                chamber["total_survival"], u
            )
        ) != 0:
            raise ValueError("below-V density is not the derivative of survival")
        duration = sp.simplify(chamber["end"] - chamber["start"])
        child_rates.append(recovered_rate)
        child_durations.append(duration)
    h_candidates = tuple(
        chamber["start"]
        for chamber in observation["above_chambers"]
        if sp.simplify(
            sp.limit(chamber["total_survival"], u, sp.oo) - bypass
        ) > 0
    )
    if not h_candidates:
        raise ValueError("no positive zero-atom exposure breakpoint was observed")
    h_v = min(h_candidates)
    child_word = _compress_physical_rate_word(child_durations, child_rates)
    child_total_hazard = sp.simplify(sum(
        duration * rate for duration, rate in zip(child_durations, child_rates)
    ))
    p_tilde = sp.simplify(p_x * sp.exp(-child_total_hazard))

    inverted_chambers = []
    typed_chambers = []
    for chamber in observation["above_chambers"]:
        inversion = recover_two_exponential_total_law(
            chamber["total_survival"], p_tilde, u
        )
        if sp.simplify(
            inversion["reconstructed_total"] - chamber["total_survival"]
        ) != 0:
            raise ValueError("Prony inversion does not reconstruct total G_+")
        typed = _type_prony_components_from_anchor_cells(
            inversion,
            chamber["anchor_cells"],
            p_tilde,
            u,
        )
        inverted_chambers.append(inversion)
        typed_chambers.append(typed)

    first = inverted_chambers[0]
    if first["branch"] == "unequal-rate":
        square_roots = tuple(sorted((
            sp.simplify(sp.sqrt(weight))
            for _, weight in first["components"]
        ), key=sp.default_sort_key))
        if sp.simplify(sum(square_roots) - 1) != 0:
            raise ValueError("first above-V atom weights do not yield Bernoulli routes")
        inheritance_pair = square_roots
    else:
        sum_squares = first["components"][0][1]
        inheritance_pair = _inheritance_pair_from_sum_squares(sum_squares)

    durations = tuple(
        sp.simplify(chamber["end"] - chamber["start"])
        for chamber in observation["above_chambers"]
    )
    physical_rates = {
        parent: tuple(typed[parent][0] for typed in typed_chambers)
        for parent in ("physical-parent-0", "physical-parent-1")
    }
    parent_words = {
        parent: _compress_physical_rate_word(durations, rates)
        for parent, rates in physical_rates.items()
    }
    asynchronous_changes = tuple(
        sum(
            physical_rates[parent][index]
            != physical_rates[parent][index - 1]
            for parent in physical_rates
        )
        for index in range(1, len(durations))
    )
    if any(count != 1 for count in asynchronous_changes):
        raise ValueError("parent schedule is not strictly asynchronous")

    equal_recoveries = []
    for equal_observation in observation["equal_rate_observations"]:
        inversion = recover_two_exponential_total_law(
            equal_observation["total_survival"], p_tilde, u
        )
        if inversion["branch"] != "equal-rate":
            raise ValueError("equal-rate boundary did not enter the rank-one branch")
        sum_squares = inversion["components"][0][1]
        pair = _inheritance_pair_from_sum_squares(sum_squares)
        equal_recoveries.append({
            "branch": inversion["branch"],
            "rate": inversion["components"][0][0],
            "inheritance_pair": pair,
            "hankel_determinant": inversion["hankel_determinant"],
        })

    q_candidates = inheritance_pair
    forward_candidates = tuple(
        triangle_forward(
            q,
            observation["direction_rate"],
            observation["direction_delta"],
            u,
        )
        for q in q_candidates
    )
    reverse_candidates = tuple(
        triangle_reverse(
            q,
            observation["direction_rate"],
            observation["direction_delta"],
            u,
        )
        for q in q_candidates
    )
    forward_match = any(
        sp.simplify(observation["direction_observation"] - candidate) == 0
        for candidate in forward_candidates
    )
    reverse_match = any(
        sp.simplify(observation["direction_observation"] - candidate) == 0
        for candidate in reverse_candidates
    )
    if not forward_match or reverse_match:
        raise ValueError("triangle cell does not determine the direction quotient")

    typed_q_by_parent = {
        parent: sp.simplify(sp.sqrt(typed_chambers[0][parent][1]))
        for parent in ("physical-parent-0", "physical-parent-1")
    }
    if sp.simplify(sum(typed_q_by_parent.values()) - 1) != 0:
        raise ValueError("typed first-chamber coefficients do not yield route weights")
    typed_pair = tuple(sorted(
        typed_q_by_parent.values(),
        key=sp.default_sort_key,
    ))
    if typed_pair != inheritance_pair:
        raise ValueError("typed route weights disagree with the total-law inversion")

    topology = observation["topology_cells"]
    witness = topology["v_exposure_witness"]
    return {
        "h_v": h_v,
        "child_component": tuple(witness["descendant_samples"]),
        "parent_incidences": tuple(topology["v_incoming_observations"]),
        "child_incidence": tuple(topology["v_outgoing_observations"]),
        "inheritance_pair": inheritance_pair,
        "typed_inheritance_assignment": tuple(
            (
                topology["physical_parent_incidences"][parent][0],
                typed_q_by_parent[parent],
            )
            for parent in ("physical-parent-0", "physical-parent-1")
        ),
        "exposed_rate_words": {
            "child": tuple(child_word),
            "parent_1": parent_words["physical-parent-0"],
            "parent_2": parent_words["physical-parent-1"],
        },
        "child_chamber_rates": tuple(child_rates),
        "parent_chamber_rates": physical_rates,
        "repair_side_typing": {
            "kind": topology["typing_kind"],
            "labels": topology["label_triple"],
        },
        "direction_quotient": "forward-mod-parent-exchange",
        "zero_atom_breakpoint": {
            "below": bypass,
            "above": inverted_chambers[0]["constant"],
            "jump": sp.simplify(inverted_chambers[0]["constant"] - bypass),
        },
        "prony_chambers": tuple(inverted_chambers),
        "equal_rate_recoveries": tuple(equal_recoveries),
        "asynchronous_parent_boundary_changes": asynchronous_changes,
    }


def validate_stored_exposure_loss_record(record: Mapping) -> bool:
    """Semantic schema check; value correctness is audited against total laws."""
    required = {
        "h_v",
        "child_component",
        "parent_incidences",
        "child_incidence",
        "inheritance_pair",
        "typed_inheritance_assignment",
        "exposed_rate_words",
        "child_chamber_rates",
        "parent_chamber_rates",
        "repair_side_typing",
        "direction_quotient",
        "zero_atom_breakpoint",
        "prony_chambers",
        "equal_rate_recoveries",
        "asynchronous_parent_boundary_changes",
    }
    if not required.issubset(record):
        return False
    pair = tuple(map(sp.sympify, record["inheritance_pair"]))
    words = record["exposed_rate_words"]
    typed_assignment = tuple(record["typed_inheritance_assignment"])
    typed_values = tuple(sp.sympify(value) for _, value in typed_assignment)
    return (
        len(pair) == 2
        and all(value.is_positive for value in pair)
        and sp.simplify(sum(pair) - 1) == 0
        and len(typed_assignment) == 2
        and len({tail for tail, _ in typed_assignment}) == 2
        and {tail for tail, _ in typed_assignment}
        == {tail for tail, _, _ in record["parent_incidences"]}
        and all(value.is_positive for value in typed_values)
        and sp.simplify(sum(typed_values) - 1) == 0
        and tuple(sorted(typed_values, key=sp.default_sort_key))
        == tuple(sorted(pair, key=sp.default_sort_key))
        and set(words) == {"child", "parent_1", "parent_2"}
        and all(
            word
            and all(
                sp.sympify(duration).is_positive
                and sp.sympify(rate).is_positive
                for duration, rate in word
            )
            for word in words.values()
        )
        and len(record["parent_incidences"]) == 2
        and len(record["child_incidence"]) == 1
        and all(count == 1 for count in record["asynchronous_parent_boundary_changes"])
        and record["zero_atom_breakpoint"]["jump"].is_positive
    )


def _predict_exposure_loss_totals_from_record(
    record: Mapping,
    observation: Mapping,
) -> tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]]:
    """Forward-check a recovered record against the observable total cells."""
    u = observation["u"]
    p_x = observation["p_x"]
    topology = observation["topology_cells"]
    typed_weights = dict(record["typed_inheritance_assignment"])
    parent_0_tail = topology["physical_parent_incidences"][
        "physical-parent-0"
    ][0]
    parent_1_tail = topology["physical_parent_incidences"][
        "physical-parent-1"
    ][0]
    try:
        q_1 = typed_weights[parent_0_tail]
        q_2 = typed_weights[parent_1_tail]
    except KeyError as error:
        raise ValueError("typed inheritance weight misses a physical parent") from error
    child_predictions = []
    child_prefix = sp.Integer(0)
    if len(record["child_chamber_rates"]) != len(observation["below_chambers"]):
        raise ValueError("child chamber-rate record has the wrong length")
    child_durations = tuple(
        sp.simplify(chamber["end"] - chamber["start"])
        for chamber in observation["below_chambers"]
    )
    if _compress_physical_rate_word(
        child_durations,
        record["child_chamber_rates"],
    ) != tuple(record["exposed_rate_words"]["child"]):
        raise ValueError("child word is not the Q3 compression of its chambers")
    for duration, rate, chamber in zip(
        child_durations,
        record["child_chamber_rates"],
        observation["below_chambers"],
    ):
        child_predictions.append(sp.simplify(
            1 - p_x + p_x * sp.exp(-(child_prefix + rate * u))
        ))
        child_prefix = sp.simplify(child_prefix + duration * rate)
    p_tilde = sp.simplify(p_x * sp.exp(-child_prefix))
    split = sp.simplify(2 * p_tilde * q_1 * q_2)
    parent_prefixes = [sp.Integer(0), sp.Integer(0)]
    rates_1 = record["parent_chamber_rates"]["physical-parent-0"]
    rates_2 = record["parent_chamber_rates"]["physical-parent-1"]
    parent_predictions = []
    for index, chamber in enumerate(observation["above_chambers"]):
        duration = sp.simplify(chamber["end"] - chamber["start"])
        rate_1, rate_2 = rates_1[index], rates_2[index]
        parent_predictions.append(sp.simplify(
            1 - p_x + split
            + p_tilde * q_1**2 * sp.exp(-(parent_prefixes[0] + rate_1 * u))
            + p_tilde * q_2**2 * sp.exp(-(parent_prefixes[1] + rate_2 * u))
        ))
        parent_prefixes[0] = sp.simplify(parent_prefixes[0] + duration * rate_1)
        parent_prefixes[1] = sp.simplify(parent_prefixes[1] + duration * rate_2)
    return tuple(child_predictions), tuple(parent_predictions)


def exposure_loss_record_matches_observation(
    record: Mapping,
    observation: Mapping,
) -> bool:
    if not validate_stored_exposure_loss_record(record):
        return False
    if record["h_v"] != observation["above_chambers"][0]["start"]:
        return False
    topology = observation["topology_cells"]
    if tuple(record["parent_incidences"]) != tuple(
        topology["v_incoming_observations"]
    ):
        return False
    if tuple(record["child_incidence"]) != tuple(
        topology["v_outgoing_observations"]
    ):
        return False
    if tuple(record["child_component"]) != tuple(
        topology["v_exposure_witness"]["descendant_samples"]
    ):
        return False
    if record["repair_side_typing"]["kind"] != topology["typing_kind"]:
        return False
    if tuple(record["repair_side_typing"]["labels"]) != tuple(
        topology["label_triple"]
    ):
        return False
    if record["direction_quotient"] != "forward-mod-parent-exchange":
        return False
    durations = tuple(
        sp.simplify(chamber["end"] - chamber["start"])
        for chamber in observation["above_chambers"]
    )
    for parent, word_key in (
        ("physical-parent-0", "parent_1"),
        ("physical-parent-1", "parent_2"),
    ):
        if _compress_physical_rate_word(
            durations,
            record["parent_chamber_rates"][parent],
        ) != tuple(record["exposed_rate_words"][word_key]):
            return False
    try:
        child_predictions, parent_predictions = (
            _predict_exposure_loss_totals_from_record(
                record,
                observation,
            )
        )
    except (KeyError, TypeError, ValueError):
        return False
    return (
        len(child_predictions) == len(observation["below_chambers"])
        and len(parent_predictions) == len(observation["above_chambers"])
        and all(
            sp.simplify(prediction - chamber["total_survival"]) == 0
            for prediction, chamber in zip(
                child_predictions,
                observation["below_chambers"],
            )
        )
        and all(
            sp.simplify(prediction - chamber["total_survival"]) == 0
            for prediction, chamber in zip(
                parent_predictions,
                observation["above_chambers"],
            )
        )
    )


def exposure_loss_joint_bundle_matches(
    core: Core,
    manifest: Mapping,
    observation: Mapping,
    recovered_v_record: Mapping,
    stored_x_macro: Mapping,
) -> bool:
    """Check joint lift using only the residual and the two stored records."""
    try:
        reconstructed = _joint_restore_from_residual_records(
            observation["residual_q8_graph"],
            recovered_v_record,
            stored_x_macro,
        )
    except (KeyError, TypeError, ValueError, nx.NetworkXError):
        return False
    expected = _build_expected_exposure_decorated_graph(core, manifest)
    return _exact_graph_record(reconstructed) == _exact_graph_record(expected)


def _build_expected_exposure_decorated_graph(
    core: Core,
    manifest: Mapping,
) -> nx.MultiDiGraph:
    """Independent expected record from the frozen core/parameter manifest."""
    expected = build_repaired_core(core, manifest["repair"])
    q_1, q_2 = manifest["q_assignment"]
    expected.nodes["V"].update({
        "h_v": manifest["h_v"],
        "inheritance_pair": tuple(sorted((q_1, q_2), key=sp.default_sort_key)),
        "exposed_rate_words": {
            "child": _compress_physical_rate_word(
                tuple(duration for duration, _ in manifest["child_schedule"]),
                tuple(rate for _, rate in manifest["child_schedule"]),
            ),
            "parent_1": _compress_physical_rate_word(
                tuple(chamber["duration"] for chamber in manifest["parent_schedule"]),
                tuple(chamber["rates"][0] for chamber in manifest["parent_schedule"]),
            ),
            "parent_2": _compress_physical_rate_word(
                tuple(chamber["duration"] for chamber in manifest["parent_schedule"]),
                tuple(chamber["rates"][1] for chamber in manifest["parent_schedule"]),
            ),
        },
        "direction_quotient": "forward-mod-parent-exchange",
        "repair_side_typing": {
            "kind": manifest["case"]["typing_kind"],
            "labels": manifest["case"]["label_triple"],
        },
    })
    expected.nodes["X"].update({
        "p_x": manifest["p_x"],
        "typed_macro": True,
    })
    typed_q_assignment = dict(manifest["typed_q_assignment"])
    for tail, key, _ in manifest["case"]["v_parent_incidences"]:
        weight = typed_q_assignment[tail]
        expected[tail]["V"][key]["inheritance_probability"] = weight
    typed_x_assignment = dict(manifest["typed_x_assignment"])
    for tail, key, _ in manifest["case"]["x_incoming"]:
        weight = typed_x_assignment[tail]
        expected[tail]["X"][key]["inheritance_probability"] = weight
    return expected


def _joint_restore_from_residual_records(
    residual_q8_graph: nx.MultiDiGraph,
    stored_v_record: Mapping,
    stored_x_macro: Mapping,
) -> nx.MultiDiGraph:
    """Consume only residual Q8 + recovered E + stored typed X macro."""
    if not validate_stored_exposure_loss_record(stored_v_record):
        raise ValueError("joint lift requires a complete recovered V record")
    graph = residual_q8_graph.copy()
    graph.remove_node("residual-q8:V")
    graph.add_node(
        "V",
        role="retic",
        h_v=stored_v_record["h_v"],
        inheritance_pair=stored_v_record["inheritance_pair"],
        exposed_rate_words=stored_v_record["exposed_rate_words"],
        direction_quotient=stored_v_record["direction_quotient"],
        repair_side_typing=stored_v_record["repair_side_typing"],
    )
    typed_weights = dict(stored_v_record["typed_inheritance_assignment"])
    for tail, key, segment in stored_v_record["parent_incidences"]:
        graph.add_edge(
            tail,
            "V",
            key=key,
            segment=segment,
            inheritance_probability=typed_weights[tail],
        )
    for head, key, segment in stored_v_record["child_incidence"]:
        graph.add_edge("V", head, key=key, segment=segment)

    x_incoming_tails = {tail for tail, _, _ in stored_x_macro["incoming"]}
    x_weights = dict(stored_x_macro["typed_weights"])
    if (
        tuple(stored_x_macro["parents"]) != tuple(sorted(x_incoming_tails))
        or {
            stored_x_macro["child_corridor_tail"],
            stored_x_macro["bypass_tail"],
        } != x_incoming_tails
        or len(stored_x_macro["outgoing"]) != 1
        or stored_x_macro["focal"] != stored_x_macro["outgoing"][0][0]
        or stored_x_macro["focal"] != "C_X"
    ):
        raise ValueError("stored X macro has inconsistent focal/parent ports")
    graph.add_node(stored_x_macro["focal"], role="leaf")
    graph.add_node(
        "X",
        role="retic",
        p_x=x_weights[stored_x_macro["child_corridor_tail"]],
        typed_macro=True,
    )
    for tail, key, segment in stored_x_macro["incoming"]:
        graph.add_edge(
            tail,
            "X",
            key=key,
            segment=segment,
            inheritance_probability=x_weights[tail],
        )
    for head, key, segment in stored_x_macro["outgoing"]:
        graph.add_edge("X", head, key=key, segment=segment)
    return graph


def _exposure_loss_certificate_from_manifest(
    core_name: str,
    core: Core,
    manifest: Mapping,
) -> dict:
    repair = tuple(manifest["repair"])
    observation = _generate_exposure_loss_observation(core, manifest)
    recovered = _recover_exposure_loss_record_from_total_laws(observation)
    expected = _build_expected_exposure_decorated_graph(core, manifest)
    reconstructed = _joint_restore_from_residual_records(
        observation["residual_q8_graph"],
        recovered,
        observation["stored_x_macro"],
    )
    case = manifest["case"]
    expected_words = expected.nodes["V"]["exposed_rate_words"]
    expected_typed_v = tuple(manifest["typed_q_assignment"])
    expected_typed_x = dict(manifest["typed_x_assignment"])
    independent_expected_match = (
        recovered["h_v"] == manifest["h_v"]
        and recovered["inheritance_pair"]
        == tuple(sorted(manifest["q_assignment"], key=sp.default_sort_key))
        and recovered["exposed_rate_words"] == expected_words
        and tuple(recovered["parent_incidences"])
        == tuple(sorted(case["v_parent_incidences"], key=repr))
        and tuple(recovered["child_incidence"])
        == tuple(sorted(case["v_outgoing"], key=repr))
        and recovered["typed_inheritance_assignment"] == expected_typed_v
        and observation["stored_x_macro"]["incoming"]
        == tuple(sorted(case["x_incoming"], key=repr))
        and dict(observation["stored_x_macro"]["typed_weights"])
        == expected_typed_x
    )
    expected_equal_pairs = (
        (sp.Rational(1, 3), sp.Rational(2, 3)),
        (sp.Rational(1, 2), sp.Rational(1, 2)),
    )
    equal_boundary_cases_match = tuple(
        recovery["inheritance_pair"]
        for recovery in recovered["equal_rate_recoveries"]
    ) == expected_equal_pairs
    return {
        "core": core_name,
        "repair": repair,
        "manifest": manifest,
        "observation": observation,
        "recovered_v_record": recovered,
        "stored_x_macro": observation["stored_x_macro"],
        "zero_atom_breakpoint_positive": recovered[
            "zero_atom_breakpoint"
        ]["jump"].is_positive,
        "total_law_prony_exact": all(
            sp.simplify(
                chamber["reconstructed_total"]
                - observed["total_survival"]
            ) == 0
            for chamber, observed in zip(
                recovered["prony_chambers"],
                observation["above_chambers"],
            )
        ),
        "strict_asynchronous_parent_schedule": all(
            count == 1
            for count in recovered["asynchronous_parent_boundary_changes"]
        ),
        "first_prony_branch": recovered["prony_chambers"][0]["branch"],
        "equal_and_q_half_boundary_cases_match": equal_boundary_cases_match,
        "v_exposure_witness": observation["topology_cells"][
            "v_exposure_witness"
        ],
        "v_exposed_independently_witnessed": (
            set(observation["topology_cells"]["v_exposure_witness"][
                "descendant_samples"
            ])
            == {"C_X", f"L{case['child_segment']}"}
            and observation["topology_cells"]["v_exposure_witness"][
                "positive_interval"
            ] > 0
        ),
        "typing_kind": observation["topology_cells"]["typing_kind"],
        "label_triple": observation["topology_cells"]["label_triple"],
        "residual_v_becomes_q8": (
            observation["residual_v_fan"]["reticulation"] == "V"
        ),
        "record_matches_total_observation": exposure_loss_record_matches_observation(
            recovered,
            observation,
        ),
        "independent_expected_record_match": independent_expected_match,
        "joint_reattachment_order": (
            "restore-recovered-original-V",
            "reattach-stored-typed-X-macro",
        ),
        "joint_reattachment_exact": exposure_loss_joint_bundle_matches(
            core,
            manifest,
            observation,
            recovered,
            observation["stored_x_macro"],
        ),
        "expected_graph": expected,
        "reconstructed_graph": reconstructed,
    }


def exposure_loss_repair_certificate(
    core_name: str,
    core: Core,
    repair: Sequence[int],
    serial: int = 0,
) -> dict:
    manifest = _independent_exposure_loss_parameter_manifest(
        core_name,
        tuple(repair),
        serial,
    )
    return _exposure_loss_certificate_from_manifest(
        core_name,
        core,
        manifest,
    )


def _set_manifest_q_assignment(
    manifest: dict,
    q_assignment: Sequence,
) -> dict:
    q_assignment = tuple(map(sp.sympify, q_assignment))
    if (
        len(q_assignment) != 2
        or any(value.is_positive is False for value in q_assignment)
        or sp.simplify(sum(q_assignment) - 1) != 0
    ):
        raise ValueError("physical V inheritance weights must be positive and sum to one")
    manifest["q_assignment"] = q_assignment
    manifest["typed_q_assignment"] = tuple(
        (incidence[0], weight)
        for incidence, weight in zip(
            manifest["case"]["v_parent_incidences"],
            q_assignment,
        )
    )
    return manifest


def _equal_first_chamber_manifest(
    core_name: str,
    repair: Sequence[int],
    serial: int,
    q_assignment: Sequence,
) -> dict:
    manifest = _independent_exposure_loss_parameter_manifest(
        core_name,
        tuple(repair),
        serial,
    )
    first_rate = sp.Rational(3 + serial)
    parent_0_rate = sp.Rational(7 + serial)
    parent_1_rate = sp.Rational(11 + serial)
    _set_manifest_q_assignment(manifest, q_assignment)
    manifest["parent_schedule"] = (
        {
            "duration": sp.Rational(1, 4),
            "rates": (first_rate, first_rate),
            "changed_parent": None,
        },
        {
            "duration": sp.Rational(1, 5),
            "rates": (parent_0_rate, first_rate),
            "changed_parent": manifest["case"]["parent_change_order"][0],
        },
        {
            "duration": sp.Rational(1, 6),
            "rates": (parent_0_rate, parent_1_rate),
            "changed_parent": manifest["case"]["parent_change_order"][1],
        },
    )
    return manifest


def _equal_child_epoch_manifest(
    core_name: str,
    repair: Sequence[int],
    serial: int,
) -> dict:
    manifest = _independent_exposure_loss_parameter_manifest(
        core_name,
        tuple(repair),
        serial,
    )
    shared_rate = sp.Rational(5 + serial)
    manifest["child_schedule"] = (
        (sp.Rational(1, 2), shared_rate),
        (sp.Rational(1, 3), shared_rate),
    )
    return manifest


def enumerate_exposure_loss_certificates(cores: Mapping[str, Core]) -> dict:
    rows = tuple(
        exposure_loss_repair_certificate(
            core_name,
            cores[core_name],
            repair,
            serial,
        )
        for serial, (core_name, repair) in enumerate(
            EXPOSURE_LOSS_REPAIR_CASES
        )
    )
    equal_first_rows = []
    for case_index, (core_name, repair) in enumerate(
        EXPOSURE_LOSS_REPAIR_CASES
    ):
        for q_index, q_assignment in enumerate((
            (sp.Rational(1, 3), sp.Rational(2, 3)),
            (sp.Rational(1, 2), sp.Rational(1, 2)),
        )):
            manifest = _equal_first_chamber_manifest(
                core_name,
                repair,
                20 + 2 * case_index + q_index,
                q_assignment,
            )
            equal_first_rows.append(_exposure_loss_certificate_from_manifest(
                core_name,
                cores[core_name],
                manifest,
            ))
    equal_first_rows = tuple(equal_first_rows)

    equal_child_epoch_rows = tuple(
        _exposure_loss_certificate_from_manifest(
            core_name,
            cores[core_name],
            _equal_child_epoch_manifest(
                core_name,
                repair,
                60 + case_index,
            ),
        )
        for case_index, (core_name, repair) in enumerate(
            EXPOSURE_LOSS_REPAIR_CASES
        )
    )

    swapped_manifest = _independent_exposure_loss_parameter_manifest(
        "theta0",
        (2, 3),
        40,
    )
    _set_manifest_q_assignment(
        swapped_manifest,
        (sp.Rational(2, 3), sp.Rational(1, 3)),
    )
    swapped_physical_q_row = _exposure_loss_certificate_from_manifest(
        "theta0",
        cores["theta0"],
        swapped_manifest,
    )
    return {
        "repair_count": len(rows),
        "per_core_counts": {
            core_name: sum(row["core"] == core_name for row in rows)
            for core_name in ("theta0", "theta1")
        },
        "all_zero_atom_breakpoints_positive": all(
            row["zero_atom_breakpoint_positive"] for row in rows
        ),
        "all_total_law_prony_inversions_exact": all(
            row["total_law_prony_exact"] for row in rows
        ),
        "all_strict_asynchronous_schedules": all(
            row["strict_asynchronous_parent_schedule"] for row in rows
        ),
        "all_equal_and_q_half_boundaries_recovered": all(
            row["equal_and_q_half_boundary_cases_match"] for row in rows
        ),
        "all_v_exposure_witnesses_positive": all(
            row["v_exposed_independently_witnessed"] for row in rows
        ),
        "all_restrictions_turn_v_into_q8": all(
            row["residual_v_becomes_q8"] for row in rows
        ),
        "all_records_match_total_observations": all(
            row["record_matches_total_observation"] for row in rows
        ),
        "all_independent_expected_records_match": all(
            row["independent_expected_record_match"] for row in rows
        ),
        "all_joint_reattachments_exact": all(
            row["joint_reattachment_exact"] for row in rows
        ),
        "full_equal_first_chamber_count": len(equal_first_rows),
        "all_full_equal_first_chamber_records_exact": all(
            row["first_prony_branch"] == "equal-rate"
            and row["record_matches_total_observation"]
            and row["independent_expected_record_match"]
            and row["joint_reattachment_exact"]
            for row in equal_first_rows
        ),
        "full_equal_first_q_half_count": sum(
            row["manifest"]["q_assignment"]
            == (sp.Rational(1, 2), sp.Rational(1, 2))
            for row in equal_first_rows
        ),
        "equal_child_epoch_count": len(equal_child_epoch_rows),
        "all_equal_child_epochs_q3_compressed": all(
            len(row["recovered_v_record"]["exposed_rate_words"]["child"])
            == 1
            and row["record_matches_total_observation"]
            and row["independent_expected_record_match"]
            and row["joint_reattachment_exact"]
            for row in equal_child_epoch_rows
        ),
        "swapped_physical_q_assignment_exact": (
            swapped_physical_q_row["manifest"]["q_assignment"]
            == (sp.Rational(2, 3), sp.Rational(1, 3))
            and swapped_physical_q_row["record_matches_total_observation"]
            and swapped_physical_q_row["independent_expected_record_match"]
            and swapped_physical_q_row["joint_reattachment_exact"]
        ),
        "equal_first_chamber_rows": equal_first_rows,
        "equal_child_epoch_rows": equal_child_epoch_rows,
        "swapped_physical_q_row": swapped_physical_q_row,
        "rows": rows,
    }


def potential_lowest_reticulations(g: nx.MultiDiGraph) -> Tuple[str, ...]:
    retics=[v for v,d in g.nodes(data=True) if d.get('role')=='retic']
    out=[]
    simple=nx.DiGraph(g)
    for h in retics:
        if not any(h!=r and nx.has_path(simple,h,r) for r in retics):
            out.append(h)
    return tuple(sorted(out))


def sampled_leaf_descendants(g: nx.MultiDiGraph, start: str, forbidden: str | None = None) -> Tuple[str, ...]:
    simple=nx.DiGraph(g)
    if forbidden is not None and forbidden in simple:
        simple.remove_node(forbidden)
    if start not in simple:
        return ()
    desc=nx.descendants(simple,start)|{start}
    return tuple(sorted(v for v in desc if simple.nodes[v].get('role')=='leaf'))


def attachment_certificate_summary(g: nx.MultiDiGraph, h: str) -> dict:
    parents=sorted(set(g.predecessors(h)))
    child_leaves=sampled_leaf_descendants(g,h)
    side={p: sampled_leaf_descendants(g,p,forbidden=h) for p in parents}
    simple=nx.DiGraph(g)
    relation='incomparable'
    if len(parents)==2:
        if nx.has_path(simple,parents[0],parents[1]): relation=f'{parents[0]}-ancestor-{parents[1]}'
        elif nx.has_path(simple,parents[1],parents[0]): relation=f'{parents[1]}-ancestor-{parents[0]}'
    return {'reticulation':h,'parents':tuple(parents),'child_leaves':child_leaves,'side_leaves':side,'parent_relation':relation}

CORE_REATTACH_SIGNATURES = {
    # residual core role, parent role pair, parent incidence relation, child role
    ('cycle', 'X'): ('tree', ('tree-side-0', 'tree-side-1'), 'distinct-cycle-sides', 'sink-child'),
    ('theta0', 'X'): ('cycle:branch-retic-V', ('tree-U', 'residual-retic-V'), 'U-ancestor-of-V', 'sink-child-X'),
    ('theta1', 'X'): ('cycle:parallel-retic-V', ('source-S', 'residual-retic-V'), 'S-ancestor-of-V', 'sink-child-X'),
    ('theta2', 'X0'): ('cycle:sink-X1', ('tree-U', 'tree-V'), 'U-V-incomparable', 'sink-child-X0'),
    ('theta2', 'X1'): ('cycle:sink-X0', ('tree-U', 'tree-V'), 'U-V-incomparable', 'sink-child-X1'),
    ('theta3', 'X0'): ('cycle:sink-X1', ('source-S', 'tree-V'), 'S-ancestor-of-V', 'sink-child-X0'),
    ('theta3', 'X1'): ('cycle:sink-X0', ('tree-U', 'tree-V'), 'U-ancestor-of-V', 'sink-child-X1'),
}


def canonical_reattach_signature(core: str, lowest: str):
    rec = CORE_REATTACH_SIGNATURES[(core, lowest)]
    # Sort only the parent-presentation pair; retain incidence relation and child role.
    return (rec[0], tuple(sorted(rec[1])), rec[2], rec[3])


def decorated_word_signature(base_signature, words: Mapping[int, Sequence[Tuple[str, Fraction]]]):
    canon_words = tuple((seg, tuple(sorted(vals, key=lambda x: (x[1], x[0])))) for seg, vals in sorted(words.items()))
    return (base_signature, canon_words)


def sampling_initialization(sampling_map: Mapping[str, str]) -> Dict[str, Tuple[str, ...]]:
    pops: Dict[str, List[str]] = {}
    for lineage, taxon in sampling_map.items():
        pops.setdefault(taxon, []).append(lineage)
    return {taxon: tuple(sorted(labels)) for taxon, labels in sorted(pops.items())}


def terminal_rate_exposed(sampling_map: Mapping[str, str], taxon: str) -> bool:
    return sum(1 for x in sampling_map.values() if x == taxon) >= 2


def bridge_rank_one_matrix(prefix_scales: Sequence[Fraction], future: Sequence[Fraction]) -> sp.Matrix:
    return sp.Matrix([[sp.Rational(a.numerator, a.denominator) * sp.Rational(b.numerator, b.denominator) for b in future] for a in prefix_scales])


def temporal_gluing_consistent(local_times: Sequence[Mapping[str, Fraction]]) -> bool:
    seen: Dict[str, Fraction] = {}
    for rec in local_times:
        for key, val in rec.items():
            if key in seen and seen[key] != val:
                return False
            seen[key] = val
    return True
