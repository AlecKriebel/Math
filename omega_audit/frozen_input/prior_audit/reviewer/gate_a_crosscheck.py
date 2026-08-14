#!/usr/bin/env python3
"""Reviewer-A cross-check for Gate A, independent of project graph/model code.

The script reads only the two machine-readable network certificates.  It
implements a second mixed-graph reduction/isomorphism/rooting calculation and
direct displayed-tree JC evaluation.  It intentionally imports no module from
``src`` or ``AUDIT/INDEPENDENT_IMPLEMENTATION``.
"""

from __future__ import annotations

import itertools
import json
import math
import sys
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OMEGA = ROOT / "certificates" / "jc_omega_move.json"
THETA = ROOT / "certificates" / "theta_pair_networks.json"


@dataclass(frozen=True)
class QBeta:
    """Element c+d*beta modulo 43337075*b^2-36083110*b+7336259."""

    c: F = F(0)
    d: F = F(0)

    @staticmethod
    def make(value):
        return value if isinstance(value, QBeta) else QBeta(F(value), F(0))

    def __add__(self, other):
        other = self.make(other)
        return QBeta(self.c + other.c, self.d + other.d)

    __radd__ = __add__

    def __neg__(self):
        return QBeta(-self.c, -self.d)

    def __sub__(self, other):
        return self + (-self.make(other))

    def __rsub__(self, other):
        return self.make(other) - self

    def __mul__(self, other):
        other = self.make(other)
        # beta^2 = (36083110*beta-7336259)/43337075.
        dd = self.d * other.d
        return QBeta(
            self.c * other.c - dd * F(7336259, 43337075),
            self.c * other.d + self.d * other.c + dd * F(36083110, 43337075),
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.make(other)
        conjugate = QBeta(other.c + other.d * F(36083110, 43337075), -other.d)
        norm = other * conjugate
        assert norm.d == 0 and norm.c != 0
        return self * QBeta(conjugate.c / norm.c, conjugate.d / norm.c)

    def __rtruediv__(self, other):
        return self.make(other) / self

    def __bool__(self):
        return bool(self.c or self.d)


def bidegrees(arcs):
    indeg, outdeg = defaultdict(int), defaultdict(int)
    for u, v in arcs:
        outdeg[u] += 1
        indeg[v] += 1
        indeg[u] += 0
        outdeg[v] += 0
    return dict(indeg), dict(outdeg)


def dag(vertices, arcs):
    indeg = {v: 0 for v in vertices}
    children = defaultdict(list)
    for u, v in arcs:
        indeg[v] += 1
        children[u].append(v)
    queue = deque(v for v in vertices if indeg[v] == 0)
    count = 0
    while queue:
        u = queue.popleft()
        count += 1
        for v in children[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return count == len(vertices)


def rooted_valid(root, arcs, labels):
    vertices = {x for edge in arcs for x in edge}
    indeg, outdeg = bidegrees(arcs)
    if (indeg[root], outdeg[root]) != (0, 2) or not dag(vertices, arcs):
        return False
    for v in vertices:
        wanted = (1, 0) if v in labels else ((0, 2) if v == root else None)
        if wanted is not None and (indeg[v], outdeg[v]) != wanted:
            return False
        if wanted is None and (indeg[v], outdeg[v]) not in ((1, 2), (2, 1)):
            return False
    children = defaultdict(list)
    for u, v in arcs:
        children[u].append(v)
    for removed in vertices - {root} - set(labels):
        seen = {root}
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in children[u]:
                if v != removed and v not in seen:
                    seen.add(v)
                    queue.append(v)
        if not (seen & set(labels)):
            return False
    return True


def rooted_tree_child(root, arcs, labels):
    indeg, outdeg = bidegrees(arcs)
    children = defaultdict(list)
    for u, v in arcs:
        children[u].append(v)
    good_child = set(labels) | {
        v for v in indeg if (indeg[v], outdeg[v]) == (1, 2)
    }
    return all(any(v in good_child for v in children[u]) for u in outdeg if outdeg[u])


def edge(u, v, head=None):
    assert u != v and (head is None or head in (u, v))
    return (frozenset((u, v)), head)


def normalize_edges(edges):
    # These examples never create competing arrowheads on a parallel pair.
    by_ends = defaultdict(set)
    for ends, head in edges:
        if head is not None:
            by_ends[ends].add(head)
        else:
            by_ends[ends]
    answer = []
    for ends, heads in by_ends.items():
        if len(heads) > 1:
            answer.append((ends, tuple(sorted(heads))))
        else:
            answer.append((ends, next(iter(heads)) if heads else None))
    return answer


def suppress(edges, vertex):
    incident = [e for e in edges if vertex in e[0]]
    assert len(incident) == 2
    (ends1, head1), (ends2, head2) = incident
    u = next(iter(ends1 - {vertex}))
    v = next(iter(ends2 - {vertex}))
    kept = [e for e in edges if e not in incident]
    if u != v:
        surviving_heads = [h for h in (head1, head2) if h in (u, v)]
        assert len(surviving_heads) <= 1
        kept.append(edge(u, v, surviving_heads[0] if surviving_heads else None))
    return normalize_edges(kept)


def reduce_standard(root, arcs, labels):
    indeg, outdeg = bidegrees(arcs)
    retics = {v for v in indeg if (indeg[v], outdeg[v]) == (2, 1)}
    mixed = [edge(u, v, v if v in retics else None) for u, v in arcs]
    mixed = suppress(mixed, root)
    while True:
        degree = Counter(x for ends, _head in mixed for x in ends)
        candidates = sorted(v for v, d in degree.items() if d == 2 and v not in labels)
        if not candidates:
            break
        mixed = suppress(mixed, candidates[0])
    return mixed


def edge_signature(edges, mapping=None):
    mapping = mapping or {}
    tokens = []
    for ends, head in edges:
        u, v = sorted(mapping.get(x, x) for x in ends)
        mapped_head = mapping.get(head, head) if head is not None else None
        tokens.append((u, v, mapped_head))
    return sorted(tokens)


def isomorphic(left_edges, left_labels, right_edges, right_labels):
    lvertices = {x for e, _h in left_edges for x in e}
    rvertices = {x for e, _h in right_edges for x in e}
    lbylabel = {label: vertex for vertex, label in left_labels.items()}
    rbylabel = {label: vertex for vertex, label in right_labels.items()}
    fixed = {lbylabel[label]: rbylabel[label] for label in lbylabel}
    lint = sorted(lvertices - set(left_labels))
    rint = sorted(rvertices - set(right_labels))
    target = edge_signature(right_edges)
    for perm in itertools.permutations(rint):
        mapping = fixed | dict(zip(lint, perm))
        if edge_signature(left_edges, mapping) == target:
            return True
    return False


def local_strong_violations(edges, labels):
    incident = defaultdict(list)
    for e in edges:
        for v in e[0]:
            incident[v].append(e)
    bad = []
    for v, adjacent in incident.items():
        if v in labels:
            continue
        outgoing = sum(head is not None and head != v for _ends, head in adjacent)
        undirected = sum(head is None for _ends, head in adjacent)
        if outgoing and undirected != 2:
            bad.append((v, outgoing, undirected))
    return sorted(bad)


def all_rootings(edges, labels):
    answers = []
    for split_index, split in enumerate(edges):
        ends, _head = split
        a, b = sorted(ends)
        remaining = edges[:split_index] + edges[split_index + 1 :]
        undirected_indices = [i for i, (_ends, head) in enumerate(remaining) if head is None]
        for bits in itertools.product((0, 1), repeat=len(undirected_indices)):
            choices = dict(zip(undirected_indices, bits))
            root = "__R__"
            arcs = [(root, a), (root, b)]
            for i, (pair, head) in enumerate(remaining):
                u, v = sorted(pair)
                if head is not None:
                    arcs.append((v if head == u else u, head))
                else:
                    arcs.append((u, v) if choices[i] == 0 else (v, u))
            if rooted_valid(root, arcs, labels):
                answers.append((tuple(sorted(ends)), rooted_tree_child(root, arcs, labels)))
    return answers


def cycle_lengths(edges):
    adjacency = defaultdict(set)
    for ends, _head in edges:
        u, v = tuple(ends)
        adjacency[u].add(v)
        adjacency[v].add(u)
    cycles = set()

    def canon(path):
        variants = []
        for seq in (path, list(reversed(path))):
            variants.extend(tuple(seq[i:] + seq[:i]) for i in range(len(seq)))
        return min(variants)

    for start in sorted(adjacency):
        def visit(u, path):
            for v in adjacency[u]:
                if v == start and len(path) >= 3:
                    cycles.add(canon(path))
                elif v not in path and v >= start:
                    visit(v, path + [v])
        visit(start, [start])
    return sorted(map(len, cycles))


def descendants(active, labels):
    children = defaultdict(list)
    for _name, u, v in active:
        children[u].append(v)
    memo = {}

    def visit(v):
        if v in memo:
            return memo[v]
        if v in labels:
            result = frozenset((labels[v],))
        else:
            result = frozenset().union(*(visit(w) for w in children.get(v, ())))
        memo[v] = result
        return result

    return {name: visit(v) for name, _u, v in active}


def jc_coordinate(named_arcs, labels, incoming, params, lambdas, assignment):
    total = QBeta() if any(isinstance(v, QBeta) for v in params.values()) else F(0)
    retics = sorted(incoming)
    for choices in itertools.product((0, 1), repeat=len(retics)):
        chosen = {r: incoming[r][bit] for r, bit in zip(retics, choices)}
        excluded = {name for r in retics for name in incoming[r] if name != chosen[r]}
        active = [arc for arc in named_arcs if arc[0] not in excluded]
        below = descendants(active, labels)
        term = QBeta.make(1) if isinstance(total, QBeta) else F(1)
        for r, bit in zip(retics, choices):
            lam = lambdas[r]
            term *= lam if bit == 0 else (1 - lam)
        for name, _u, _v in active:
            char = 0
            for label in below[name]:
                char ^= assignment[label - 1]
            if char:
                term *= params[name]
        total += term
    return total


def determinant(matrix):
    matrix = [list(row) for row in matrix]
    one = QBeta.make(1) if any(isinstance(x, QBeta) for row in matrix for x in row) else F(1)
    answer = one
    for j in range(len(matrix)):
        pivot = next(i for i in range(j, len(matrix)) if matrix[i][j])
        if pivot != j:
            matrix[j], matrix[pivot] = matrix[pivot], matrix[j]
            answer = -answer
        value = matrix[j][j]
        answer *= value
        for k in range(j, len(matrix)):
            matrix[j][k] /= value
        for i in range(j + 1, len(matrix)):
            value = matrix[i][j]
            for k in range(j, len(matrix)):
                matrix[i][k] -= value * matrix[j][k]
    return answer


def theta_fourier_check(theta):
    named = [(name, u, v) for u, v, name in theta["internal_arcs"] + theta["pendant_arcs"]]
    incoming = theta["reticulation_incoming_choices"]
    half = F(1, 2)
    source = {
        "rA": F(2, 3), "rC": F(3, 4), "AB": F(3, 5), "BC": half,
        "CD": F(9, 20), "DE": F(2, 5), "AF": half, "EF": F(1, 3),
        "pB": F(1, 5), "pD": half, "pF": half, "pE": F(3, 8),
    }
    beta = QBeta(F(0), F(1))
    beta_lo, beta_hi = F(441, 1250), F(3529, 10000)
    discriminant = 36083110**2 - 4 * 43337075 * 7336259
    assert math.isqrt(discriminant) ** 2 != discriminant
    polynomial = lambda value: 43337075 * value * value - 36083110 * value + 7336259
    assert polynomial(beta_lo) > 0 > polynomial(beta_hi)
    assert beta_hi < F(20678, 2 * 24835)  # AB is positive and below one.
    assert beta_lo > F(10339, 53010)      # AF is below one.
    assert beta_lo > F(3, 20)             # pB is below one.
    target = {
        "rA": QBeta.make(F(2, 3)), "rC": QBeta.make(F(3, 4)),
        "AB": 24835 * beta / (20678 - 24835 * beta), "BC": QBeta.make(half),
        "CD": QBeta.make(F(9934, 12215)), "DE": QBeta.make(F(171, 775)),
        "AF": QBeta.make(10339) / (53010 * beta), "EF": QBeta.make(half),
        "pB": QBeta.make(F(3, 20)) / beta, "pD": QBeta.make(half),
        "pF": QBeta.make(F(1767, 4832)), "pE": QBeta.make(F(31, 190)),
    }
    lambdas_r = {"C": half, "F": half}
    lambdas_q = {"C": QBeta.make(half), "F": QBeta.make(half)}
    assignments = [(a, b, c, a ^ b ^ c) for a, b, c in itertools.product(range(4), repeat=3)]
    source_coords = [jc_coordinate(named, theta["source_leaf_labels"], incoming, source, lambdas_r, a) for a in assignments]
    target_coords = [jc_coordinate(named, theta["target_leaf_labels"], incoming, target, lambdas_q, a) for a in assignments]
    source_q = [QBeta.make(x) for x in source_coords]
    assert source_q == target_coords

    reps = (
        (0, 0, 1, 1), (0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 2, 3),
        (1, 0, 0, 1), (1, 0, 1, 0), (1, 0, 2, 3), (1, 1, 0, 0),
    )
    source_free = ("pD", "DE", "pE", "EF", "pF", "CD", "AB", "pB")
    target_free = ("pD", "DE", "AF", "AB", "pF", "CD", "pE", "pB")

    def jacobian(labels, params, lambdas, free):
        columns = []
        for name in free:
            low, high = dict(params), dict(params)
            zero = QBeta.make(0) if isinstance(params[name], QBeta) else F(0)
            one = QBeta.make(1) if isinstance(params[name], QBeta) else F(1)
            low[name], high[name] = zero, one
            columns.append([
                jc_coordinate(named, labels, incoming, high, lambdas, a)
                - jc_coordinate(named, labels, incoming, low, lambdas, a)
                for a in reps
            ])
        return [list(row) for row in zip(*columns)]

    source_minor = determinant(jacobian(theta["source_leaf_labels"], source, lambdas_r, source_free))
    target_minor = determinant(jacobian(theta["target_leaf_labels"], target, lambdas_q, target_free))
    assert source_minor and target_minor
    return {
        "all_parameters_strictly_in_JC_Theta0": True,
        "beta_isolating_interval": [str(beta_lo), str(beta_hi)],
        "minimal_polynomial_irreducible_over_Q": True,
        "complete_zero_sum_coordinate_equalities": len(assignments),
        "source_rank8_minor_nonzero": bool(source_minor),
        "source_rank8_minor": str(source_minor),
        "target_rank8_minor_nonzero": bool(target_minor),
        "target_rank8_minor": {"constant": str(target_minor.c), "linear": str(target_minor.d)},
    }


def theta_invariant_pullbacks(theta):
    """Rebuild and annihilate the six inherited JC equations generically."""
    named = [(name, u, v) for u, v, name in theta["internal_arcs"] + theta["pendant_arcs"]]
    incoming = theta["reticulation_incoming_choices"]
    edge_names = [name for name, _u, _v in named]
    edge_symbols = sp.symbols(" ".join(f"x_{name}" for name in edge_names))
    params = dict(zip(edge_names, edge_symbols))
    lambda_c, lambda_f = sp.symbols("lambda_C lambda_F")
    lambdas = {"C": lambda_c, "F": lambda_f}
    reps = (
        (0, 0, 1, 1), (0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 2, 3),
        (1, 0, 0, 1), (1, 0, 1, 0), (1, 0, 2, 3), (1, 1, 0, 0),
        (1, 1, 1, 1), (1, 1, 2, 2), (1, 2, 0, 3), (1, 2, 1, 2),
        (1, 2, 2, 1), (1, 2, 3, 0),
    )

    counts = {}
    for side, labels in (("source", theta["source_leaf_labels"]), ("target", theta["target_leaf_labels"])):
        coords = [jc_coordinate(named, labels, incoming, params, lambdas, a) for a in reps]
        A, B, C, D, E, Fv, G, H, J, K, L, M, N, O = coords
        equations = (
            J - K - M + N,
            J - A * H - B * Fv + C * E,
            G * L - E * N,
            L**2 - B * E * H,
            B * M - D * L - B**2 * Fv + B * C * E,
            B * E * O - B * G * H - C * E * L + D * E * H,
        )
        reduced = [sp.factor(value) for value in equations]
        assert reduced == [0] * 6
        counts[side] = len(reduced)
    return {
        "six_generic_pullbacks_zero_on_each_side": counts,
        "positive_locus_upper_dimension": 8,
        "upper_dimension_reason": "On B*E != 0, five coordinates reconstruct rationally and L^2=B*E*H.",
    }


def unpack_omega(data):
    answer = {}
    for name, model in data["root_models"].items():
        net = data["network_encodings"][str(model["census_index"])]
        labels = dict(zip(net["leaves_in_port_order"], model["port_labels"]))
        answer[name] = (net["root"], [tuple(x) for x in net["arcs_in_parameter_order"]], labels)
    return answer


def omega_fourier_check(data, networks):
    coordinates = {}
    minors = {}
    reps = (
        (0, 0, 1, 1), (0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 2, 3),
        (1, 0, 0, 1), (1, 0, 1, 0), (1, 0, 2, 3), (1, 1, 0, 0),
        (1, 1, 1, 1), (1, 1, 2, 2), (1, 2, 0, 3), (1, 2, 1, 2),
        (1, 2, 2, 1), (1, 2, 3, 0),
    )
    rows = (0, 1, 2, 3, 4, 5, 6, 7, 9)
    for name, (_root, arcs, labels) in networks.items():
        values = [F(x) for x in data["exact_common_points"][name]]
        assert all(0 < value < 1 for value in values)
        named = [(f"e{i}", u, v) for i, (u, v) in enumerate(arcs)]
        indeg, outdeg = bidegrees(arcs)
        retics = sorted(v for v in indeg if (indeg[v], outdeg[v]) == (2, 1))
        incoming = {r: [edge_name for edge_name, _u, v in named if v == r] for r in retics}
        params = {f"e{i}": value for i, value in enumerate(values[:12])}
        lambdas = dict(zip(retics, values[12:]))
        assignments = [(a, b, c, a ^ b ^ c) for a, b, c in itertools.product(range(4), repeat=3)]
        coordinates[name] = [jc_coordinate(named, labels, incoming, params, lambdas, a) for a in assignments]

        columns = data["dimension_and_rank"]["N16_columns" if "N16" in name else "N26_columns"]
        derivative_columns = []
        for column in columns:
            low_params, high_params = dict(params), dict(params)
            low_lambdas, high_lambdas = dict(lambdas), dict(lambdas)
            if column < 12:
                low_params[f"e{column}"], high_params[f"e{column}"] = F(0), F(1)
            else:
                retic = retics[column - 12]
                low_lambdas[retic], high_lambdas[retic] = F(0), F(1)
            derivative_columns.append([
                jc_coordinate(named, labels, incoming, high_params, high_lambdas, reps[row])
                - jc_coordinate(named, labels, incoming, low_params, low_lambdas, reps[row])
                for row in rows
            ])
        minor = determinant(list(map(list, zip(*derivative_columns))))
        expected = F(data["dimension_and_rank"]["rank_nine_minors"][name])
        assert minor == expected != 0
        minors[name] = str(minor)
    base = coordinates["N16_source"]
    assert all(value == base for value in coordinates.values())
    return {
        "all_parameters_strictly_in_JC_Theta0": True,
        "complete_zero_sum_coordinate_equalities": len(base),
        "all_four_points_equal": True,
        "rank9_minors": minors,
    }


def graph_record(root, arcs, labels):
    assert rooted_valid(root, arcs, labels)
    mixed = reduce_standard(root, arcs, labels)
    rootings = all_rootings(mixed, labels)
    return {
        "edges": edge_signature(mixed),
        "cycles": cycle_lengths(mixed),
        "local_violations": local_strong_violations(mixed, labels),
        "admissible_rootings": len(rootings),
        "tree_child_rootings": sum(tree_child for _edge, tree_child in rootings),
        "all_rootings_tree_child": all(tree_child for _edge, tree_child in rootings),
    }, mixed


def main():
    omega = json.loads(OMEGA.read_text())
    theta = json.loads(THETA.read_text())
    omega_networks = unpack_omega(omega)
    records, mixed = {}, {}
    for name, (root, arcs, labels) in omega_networks.items():
        records[name], mixed[name] = graph_record(root, arcs, labels)
    omega_iso = {
        pair: isomorphic(mixed[left], omega_networks[left][2], mixed[right], omega_networks[right][2])
        for pair, left, right in (
            ("N16_source__N16_target", "N16_source", "N16_target"),
            ("N26_source__N26_target", "N26_source", "N26_target"),
            ("N16_source__N26_source", "N16_source", "N26_source"),
            ("N16_target__N26_target", "N16_target", "N26_target"),
        )
    }

    theta_named_arcs = [(u, v) for u, v, _name in theta["internal_arcs"] + theta["pendant_arcs"]]
    theta_records, theta_mixed = {}, {}
    for name, labels in (("source", theta["source_leaf_labels"]), ("target", theta["target_leaf_labels"])):
        theta_records[name], theta_mixed[name] = graph_record("rho", theta_named_arcs, labels)

    result = {
        "omega_graphs": records,
        "omega_isomorphism": omega_iso,
        "omega_exact_JC_point": omega_fourier_check(omega, omega_networks),
        "theta_graphs": theta_records,
        "theta_standard_isomorphic": isomorphic(
            theta_mixed["source"], theta["source_leaf_labels"],
            theta_mixed["target"], theta["target_leaf_labels"],
        ),
        "theta_exact_JC_point": theta_fourier_check(theta),
        "theta_generic_invariants": theta_invariant_pullbacks(theta),
    }
    print(json.dumps(result, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"FAIL: {type(error).__name__}: {error}", file=sys.stderr)
        raise
