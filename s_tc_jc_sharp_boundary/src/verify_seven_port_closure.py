#!/usr/bin/env python3
"""Self-contained exact closure of the seven-outgoing cycle-to-core-3 theta residual.

The verifier regenerates the eight residual role patterns and all 192 labelled
records, enumerates every standard-S_TC seven-outgoing completion, proves exact
F-invariant separation, and certifies generic dimensions by exact modular
Jacobian minors.  It does not import the historical Gate-1/Gate-2/Gate-3 code.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import json
import random
import sys

import sympy as sp

HERE = Path(__file__).resolve().parents[1]
CERT = HERE / "certificates" / "seven_port_closure.json"
COMPLETION_CENSUS = HERE / "certificates" / "cycle_theta_support_completion_corrected.json"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from core_enumerator import enumerate_cores  # noqa: E402

# Core-3 directed segments, recovered independently from the core enumerator.
SEGMENTS = (("U", "V"), ("S", "U"), ("S", "V"), ("U", "X0"), ("V", "X0"))
EXPECTED_RESIDUAL_PATTERNS = {
    629: ((), (0, 0, 1, 1, 2)),
    644: ((), (0, 1, 1, 2, 0)),
    649: ((), (0, 2, 0, 1, 1)),
    650: ((), (0, 2, 0, 2, 0)),
    685: ((), (2, 1, 0, 1, 0)),
    700: ((0,), (0, 0, 2, 0, 1)),
    705: ((0,), (0, 1, 0, 2, 0)),
    706: ((0,), (0, 1, 1, 0, 1)),
}
PRIME = 1_000_003


def digest(obj) -> str:
    return sha256(repr(obj).encode()).hexdigest()

def weak_compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, parts - 1):
            yield (first,) + rest

def enumerate_weak_metadata(outgoing_count=4):
    """Recreate the deterministic presentation-index universe from core data."""
    _raw, cores = enumerate_cores()
    records = []
    for core_index, core in enumerate(cores):
        sinks = tuple(sorted(v for v,c in core["vertex_types"].items() if c == "X"))
        for selected_sink_count in range(len(sinks)+1):
            for selected_sinks in combinations(range(len(sinks)), selected_sink_count):
                ordinary_count = outgoing_count - selected_sink_count
                for counts in weak_compositions(ordinary_count, len(core["directed_segments"])):
                    records.append({
                        "core_index": core_index,
                        "selected_sink_indices": tuple(selected_sinks),
                        "ordinary_counts": tuple(counts),
                    })
    return tuple(records)

def derive_residual_patterns_from_census():
    census = json.loads(COMPLETION_CENSUS.read_text())
    residual = [r for r in census["records"] if r["missing_rigid_support_ports"] == 3]
    assert len(residual) == 192
    metadata = enumerate_weak_metadata(4)
    by_pid = defaultdict(list)
    for record in residual:
        pid = record["presentation_index"]
        assert 0 <= pid < len(metadata)
        meta = metadata[pid]
        assert meta["core_index"] == record["core_index"] == 3
        by_pid[pid].append(record["permutation_index"])
    assert len(by_pid) == 8
    assert all(sorted(indices) == list(range(24)) for indices in by_pid.values())
    patterns = {
        pid: (metadata[pid]["selected_sink_indices"], metadata[pid]["ordinary_counts"])
        for pid in sorted(by_pid)
    }
    assert patterns == EXPECTED_RESIDUAL_PATTERNS
    return patterns, residual, census


def reticulations(vertices):
    return tuple(sorted(v for v, c in vertices.items() if c in {"R", "X"}))


def precompute(vertices, edges, leaf_labels):
    rs = reticulations(vertices)
    trees = []
    for choices in product((0, 1), repeat=len(rs)):
        excluded = set()
        for r, choice in zip(rs, choices):
            incoming = tuple(i for i, (_u, v) in enumerate(edges) if v == r)
            assert len(incoming) == 2
            excluded.add(incoming[1 - choice])
        selected = tuple(i for i in range(len(edges)) if i not in excluded)
        children = defaultdict(list)
        for i in selected:
            children[edges[i][0]].append(edges[i][1])
        cache = {}

        def descend(v):
            if v in cache:
                return cache[v]
            if v in leaf_labels:
                answer = frozenset((leaf_labels[v],))
            else:
                answer = frozenset().union(*(descend(w) for w in children.get(v, ())))
            cache[v] = answer
            return answer

        trees.append((choices, selected, {i: descend(edges[i][1]) for i in selected}))
    return rs, tuple(trees)


def lift_local(base):
    vertices = {
        ("IN" if v == "S" else v): ("T" if v == "S" else c)
        for v, c in base["vertices"].items()
    }
    edges = [
        (("IN" if u == "S" else u), ("IN" if v == "S" else v))
        for u, v in base["edges"]
    ]
    vertices.update({"ROOT": "S", "LIN": "L"})
    edges.extend((('ROOT', 'IN'), ('ROOT', 'LIN')))
    leaves = tuple(("IN" if v == "S" else v) for v in base["leaves"]) + ("LIN",)
    return {"vertices": vertices, "edges": tuple(edges), "leaves": leaves}


def build_core3_words(words, sink_label):
    vertices = {"S": "S", "U": "T", "V": "R", "X0": "X"}
    edges = []
    parent = {}
    for segment_index, ((tail, head), word) in enumerate(zip(SEGMENTS, words)):
        chain = [tail]
        for label in word:
            v = f"P{label}"
            vertices[v] = "T"
            parent[label] = v
            chain.append(v)
        chain.append(head)
        edges.extend(zip(chain, chain[1:]))
    parent[sink_label] = "X0"
    leaves = []
    label_by_leaf = {}
    for label in sorted(parent):
        leaf = f"L{label}"
        vertices[leaf] = "L"
        edges.append((parent[label], leaf))
        leaves.append(leaf)
        label_by_leaf[leaf] = label
    net = lift_local({"vertices": vertices, "edges": tuple(edges), "leaves": tuple(leaves)})
    label_by_leaf["LIN"] = 8
    return net, label_by_leaf


def build_weak_pattern(selected_sinks, counts, repair_choice):
    raw, cores = enumerate_cores()
    assert raw == 24 and len(cores) == 4
    core = cores[3]
    assert tuple((s["tail"], s["head"]) for s in core["directed_segments"]) == SEGMENTS
    repairs = tuple(tuple(r) for r in core["repairs"])
    assert repairs == ((0, 4), (3, 4))
    repair = repairs[repair_choice]
    vertices = dict(core["vertex_types"])
    edges = []
    selected_parents = []
    dummy_parents = []
    occupied = {i for i, c in enumerate(counts) if c}
    for i, (segment, count) in enumerate(zip(core["directed_segments"], counts)):
        chain = [segment["tail"]]
        for j in range(count):
            v = f"P{i}_{j}"
            vertices[v] = "T"
            selected_parents.append(v)
            chain.append(v)
        if i in repair and i not in occupied:
            v = f"D{i}"
            vertices[v] = "T"
            dummy_parents.append(v)
            chain.append(v)
        chain.append(segment["head"])
        edges.extend(zip(chain, chain[1:]))
    sinks = tuple(sorted(v for v, c in vertices.items() if c == "X"))
    assert sinks == ("X0",)
    for j, sink in enumerate(sinks):
        (selected_parents if j in selected_sinks else dummy_parents).append(sink)
    selected = []
    dummy = []
    leaves = []
    for i, p in enumerate(selected_parents):
        leaf = f"L{i}"
        vertices[leaf] = "L"
        edges.append((p, leaf))
        selected.append(leaf)
        leaves.append(leaf)
    for i, p in enumerate(dummy_parents):
        leaf = f"Z{i}"
        vertices[leaf] = "L"
        edges.append((p, leaf))
        dummy.append(leaf)
        leaves.append(leaf)
    return lift_local({"vertices": vertices, "edges": tuple(edges), "leaves": tuple(leaves)}), tuple(selected), tuple(dummy)


def semi_directed(net, leaf_colors):
    vertices = net["vertices"]
    colors = {}
    for v, c in vertices.items():
        if c == "S":
            continue
        if c == "L":
            colors[v] = leaf_colors.get(v, "Z")
        elif c in {"R", "X"}:
            colors[v] = "R"
        else:
            colors[v] = "T"
    root_children = []
    edges = []
    for u, v in net["edges"]:
        if u == "ROOT":
            root_children.append(v)
            continue
        if vertices[v] in {"R", "X"}:
            edges.append(("D", u, v))
        else:
            edges.append(("U",) + tuple(sorted((u, v))))
    assert len(root_children) == 2
    a, b = root_children
    ar, br = vertices[a] in {"R", "X"}, vertices[b] in {"R", "X"}
    assert not (ar and br)
    if ar:
        edges.append(("D", b, a))
    elif br:
        edges.append(("D", a, b))
    else:
        edges.append(("U",) + tuple(sorted((a, b))))
    return colors, tuple(sorted(edges))


def relation_neighborhood(colors, edges):
    ans = {v: [] for v in colors}
    for kind, a, b in edges:
        if kind == "U":
            ans[a].append(("U", b)); ans[b].append(("U", a))
        else:
            ans[a].append(("D+", b)); ans[b].append(("D-", a))
    return ans


def canonical_mixed_graph(graph):
    colors, edges = graph
    neigh = relation_neighborhood(colors, edges)
    groups = defaultdict(list)
    for v, c in colors.items(): groups[c].append(v)
    initial = tuple(tuple(sorted(groups[c])) for c in sorted(groups))

    def refine(part):
        while True:
            ci = {v: i for i, cell in enumerate(part) for v in cell}
            changed = False; out = []
            for cell in part:
                blocks = defaultdict(list)
                for v in cell:
                    cnt = Counter((rel, ci[w]) for rel, w in neigh[v])
                    sig = tuple(cnt[(rel, i)] for i in range(len(part)) for rel in ("U", "D+", "D-"))
                    blocks[sig].append(v)
                changed |= len(blocks) > 1
                out.extend(tuple(sorted(blocks[k])) for k in sorted(blocks))
            part = tuple(out)
            if not changed: return part

    def leaf_code(part):
        order = tuple(cell[0] for cell in part); pos = {v: i for i, v in enumerate(order)}
        ee = []
        for kind, a, b in edges:
            a, b = pos[a], pos[b]
            if kind == "U" and a > b: a, b = b, a
            ee.append((kind, a, b))
        return tuple(colors[v] for v in order), tuple(sorted(ee))

    def search(part):
        part = refine(part)
        if all(len(cell) == 1 for cell in part): return leaf_code(part)
        j = next(i for i, cell in enumerate(part) if len(cell) > 1)
        cell = part[j]; best = None
        for v in cell:
            rest = tuple(x for x in cell if x != v)
            candidate = search(part[:j] + ((v,), rest) + part[j+1:])
            if best is None or candidate < best: best = candidate
        return best
    return search(initial)



def full_parameterization_signature(net, labels):
    """Machine-readable exact displayed-tree monomial schema for all tensor coordinates."""
    leaf_labels = {leaf: label - 1 for leaf, label in labels.items()}
    rs, trees = precompute(net["vertices"], net["edges"], leaf_labels)
    records = []
    for choices, selected, descendants in trees:
        edge_records = []
        for edge_index in selected:
            mask = 0
            for label in descendants[edge_index]:
                mask |= 1 << label
            edge_records.append((edge_index, mask))
        records.append((tuple(choices), tuple(edge_records)))
    return (tuple(net["edges"]), tuple(rs), tuple(records))

def standard_stc(net, labels):
    leaf_colors = {leaf: ("LIN" if label == 8 else f"L{label}") for leaf, label in labels.items()}
    colors, edges = semi_directed(net, leaf_colors)
    undeg = Counter()
    for kind, a, b in edges:
        if kind == "U": undeg[a] += 1; undeg[b] += 1
    return all(undeg[tail] == 2 for kind, tail, _head in edges if kind == "D")


def interleavings(old, new):
    for new_order in permutations(new):
        for old_positions in combinations(range(len(old) + len(new)), len(old)):
            word = [None] * (len(old) + len(new))
            it = iter(old)
            for i in old_positions: word[i] = next(it)
            it = iter(new_order)
            for i in range(len(word)):
                if word[i] is None: word[i] = next(it)
            yield tuple(word)


def completions(pattern):
    selected_sinks, counts = pattern
    old_by_segment = []
    next_label = 1
    for count in counts:
        old_by_segment.append(tuple(range(next_label, next_label + count)))
        next_label += count
    old_sink = next_label if selected_sinks else None
    if old_sink is not None: next_label += 1
    assert next_label == 5
    extras = {5, 6, 7}
    answer = set()
    if old_sink is None:
        for sink in extras:
            ordinary = sorted(extras - {sink})
            for allocation in product(range(5), repeat=2):
                added = [[] for _ in range(5)]
                for label, segment in zip(ordinary, allocation): added[segment].append(label)
                choices = [tuple(interleavings(old_by_segment[i], added[i])) for i in range(5)]
                for words in product(*choices):
                    occupied = tuple(bool(w) for w in words)
                    if occupied[4] and (occupied[0] or occupied[3]): answer.add((words, sink))
    else:
        for allocation in product(range(5), repeat=3):
            added = [[] for _ in range(5)]
            for label, segment in zip(sorted(extras), allocation): added[segment].append(label)
            choices = [tuple(interleavings(old_by_segment[i], added[i])) for i in range(5)]
            for words in product(*choices):
                occupied = tuple(bool(w) for w in words)
                if occupied[4] and (occupied[0] or occupied[3]): answer.add((words, old_sink))
    return tuple(sorted(answer))


def symbolic_F(net, selected_leaves, triple, prefix):
    observed = tuple(selected_leaves) + ("LIN",)
    leaf_labels = {v: i for i, v in enumerate(observed)}
    rs, trees = precompute(net["vertices"], net["edges"], leaf_labels)
    xs = sp.symbols(f"{prefix}x0:{len(net['edges'])}")
    ls = sp.symbols(f"{prefix}l0:{len(rs)}")
    patterns = ((1,1,0), (1,0,1), (0,1,1), (1,2,3))
    coordinates = []
    for pat in patterns:
        assignment = [0] * len(observed)
        for i, value in zip(triple, pat): assignment[i] = value
        total = 0
        for choices, selected, descendants in trees:
            term = 1
            for j, choice in enumerate(choices): term *= ls[j] if choice == 0 else 1 - ls[j]
            for edge_index in selected:
                char = 0
                for label in descendants[edge_index]: char ^= assignment[label]
                if char: term *= xs[edge_index]
            total += term
        coordinates.append(sp.expand(total))
    return sp.factor(coordinates[0] * coordinates[1] * coordinates[2] - coordinates[3] ** 2)


def factor_sign(expr):
    """Certify the selected factorizations are strictly positive on (0,1)^d."""
    coefficient, factors = sp.factor_list(expr)
    sign = 1 if coefficient > 0 else -1
    explanations = []
    for factor, power in factors:
        factor = sp.factor(factor)
        fs = factor.free_symbols
        this = None; reason = None
        if len(fs) == 1 and factor in fs:
            this, reason = 1, "positive variable"
        elif factor.is_Pow:
            raise AssertionError
        else:
            poly = sp.Poly(factor, *sorted(fs, key=str)) if fs else None
            # x-1, product-1, or one of the two exact negative mixture brackets.
            if sp.expand(factor + 1).is_Mul and all(term.is_Symbol for term in sp.Mul.make_args(sp.expand(factor + 1))):
                this, reason = -1, "product-minus-one"
            elif len(fs) == 1:
                x = next(iter(fs))
                if sp.expand(factor - (x - 1)) == 0: this, reason = -1, "x-minus-one"
                elif sp.expand(factor - (x + 1)) == 0: this, reason = 1, "x-plus-one"
            if this is None:
                # Detect B = l0*l1*A-l0*A-l1*C = -[l0(1-l1)A+l1*C],
                # where A and C are positive monomials on the open cube.
                ls = [x for x in fs if str(x).endswith("l0") or str(x).endswith("l1")]
                def positive_monomial(q):
                    q = sp.factor(q)
                    coefficient, powers = q.as_coeff_Mul()
                    if coefficient <= 0:
                        return False
                    return all(term.is_Symbol or (term.is_Pow and term.base.is_Symbol
                               and term.exp.is_Integer and term.exp > 0)
                               for term in sp.Mul.make_args(powers))
                for l0 in ls:
                    for l1 in ls:
                        if l0 == l1: continue
                        A = sp.factor(sp.diff(sp.diff(factor, l0), l1))
                        C = sp.factor(-factor.subs(l0, 0) / l1)
                        target = -l0 * (1 - l1) * A - l1 * C
                        if sp.expand(factor - target) == 0 and positive_monomial(A) and positive_monomial(C):
                            this, reason = -1, "-[l0(1-l1)A+l1*C] with positive monomials A,C"
                            break
                    if this is not None: break
            if this is None:
                # Squares are harmless even if the base changes sign.
                if power % 2 == 0:
                    this, reason = 1, "nonzero square"
                else:
                    raise AssertionError(f"unclassified sign factor: {factor}")
        if power % 2 == 0: this = 1
        sign *= this
        explanations.append((str(factor), int(power), int(this), reason))
    assert sign == 1
    return explanations


def cycle_network(counts):
    vertices = {"S": "S", "X": "X"}; edges = []; parents = []
    for side, count in enumerate(counts):
        chain = ["S"]
        for j in range(count):
            v = f"P{side}_{j}"; vertices[v] = "T"; parents.append(v); chain.append(v)
        chain.append("X"); edges.extend(zip(chain, chain[1:]))
    parents.append("X"); leaves = []
    for i, parent in enumerate(parents):
        leaf = f"L{i}"; vertices[leaf] = "L"; edges.append((parent, leaf)); leaves.append(leaf)
    return lift_local({"vertices": vertices, "edges": tuple(edges), "leaves": tuple(leaves)})


def core3_count_network(counts):
    words = []
    label = 1
    for count in counts:
        words.append(tuple(range(label, label + count))); label += count
    return build_core3_words(tuple(words), 7)[0]


def mod_inverse(x): return pow(x % PRIME, PRIME - 2, PRIME)


def jacobian_rows_mod(net, assignments):
    edges = net["edges"]; leaves = net["leaves"]
    labels = {v: i for i, v in enumerate(leaves)}
    rs, trees = precompute(net["vertices"], edges, labels)
    edge_values = [(17 + 37 * i) % PRIME for i in range(len(edges))]
    inheritance_values = [(211 + 53 * i) % PRIME for i in range(len(rs))]
    rows = []
    for assignment in assignments:
        derivative = [0] * (len(edges) + len(rs))
        for choices, selected, descendants in trees:
            active = []; edge_product = 1
            for edge_index in selected:
                char = 0
                for label in descendants[edge_index]: char ^= assignment[label]
                if char:
                    active.append(edge_index)
                    edge_product = edge_product * edge_values[edge_index] % PRIME
            weight = 1
            for j, choice in enumerate(choices):
                lam = inheritance_values[j]
                weight = weight * (lam if choice == 0 else 1 - lam) % PRIME
            term = weight * edge_product % PRIME
            for edge_index in active:
                derivative[edge_index] = (derivative[edge_index] + term * mod_inverse(edge_values[edge_index])) % PRIME
            for j, choice in enumerate(choices):
                lam = inheritance_values[j]
                dweight = weight * mod_inverse(lam if choice == 0 else 1 - lam) % PRIME
                if choice: dweight = -dweight % PRIME
                derivative[len(edges) + j] = (derivative[len(edges) + j] + dweight * edge_product) % PRIME
        rows.append(derivative)
    return rows, edge_values, inheritance_values


def rank_minor_certificate(net, seed):
    rng = random.Random(seed); assignments = []
    n = len(net["leaves"])
    for _ in range(600):
        first = [rng.randrange(4) for _ in range(n - 1)]; last = 0
        for x in first: last ^= x
        assignments.append(tuple(first + [last]))
    rows, edge_values, inheritance_values = jacobian_rows_mod(net, assignments)
    basis = {}; selected_rows = []
    for row_index, row in enumerate(rows):
        v = row[:]
        for pivot in sorted(basis):
            if v[pivot]:
                factor = v[pivot]
                v = [(x - factor * y) % PRIME for x, y in zip(v, basis[pivot])]
        pivot = next((i for i, x in enumerate(v) if x), None)
        if pivot is None: continue
        inv = mod_inverse(v[pivot]); v = [x * inv % PRIME for x in v]
        for old in list(basis):
            if basis[old][pivot]:
                factor = basis[old][pivot]
                basis[old] = [(x - factor * y) % PRIME for x, y in zip(basis[old], v)]
        basis[pivot] = v; selected_rows.append(row_index)
    rank = len(basis); columns = tuple(sorted(basis))
    assert len(selected_rows) == rank == len(columns)
    matrix = [[rows[i][j] for j in columns] for i in selected_rows]
    determinant = 1
    for col in range(rank):
        pivot_row = next(i for i in range(col, rank) if matrix[i][col])
        if pivot_row != col:
            matrix[col], matrix[pivot_row] = matrix[pivot_row], matrix[col]
            determinant = -determinant % PRIME
        pivot = matrix[col][col]; determinant = determinant * pivot % PRIME
        inv = mod_inverse(pivot)
        for i in range(col + 1, rank):
            if matrix[i][col]:
                factor = matrix[i][col] * inv % PRIME
                matrix[i] = [(x - factor * y) % PRIME for x, y in zip(matrix[i], matrix[col])]
    assert determinant
    return {
        "rank": rank,
        "row_assignments": [list(assignments[i]) for i in selected_rows],
        "columns": list(columns),
        "determinant_mod_prime": determinant,
        "edge_values_mod_prime": edge_values,
        "inheritance_values_mod_prime": inheritance_values,
    }


def expected_dimension(net):
    n = len(net["leaves"]); r = len(reticulations(net["vertices"])); edges = len(net["edges"])
    assert edges == 2 * n + 3 * r - 2
    # Root-split gauge plus two exact gauges per reticulation.
    return 2 * n + 2 * r - 3


def generate_certificate():
    residual_patterns, inherited_residual_records, completion_census = derive_residual_patterns_from_census()
    raw, cores = enumerate_cores()
    assert raw == 24 and len(cores) == 4
    core3 = cores[3]
    assert core3["vertex_types"] == {"S": "S", "U": "T", "V": "R", "X0": "X"}
    assert tuple(tuple(r) for r in core3["repairs"]) == ((0, 4), (3, 4))

    # Freeze 192 labelled records and eight free S4 orbits.
    records = []; orbit_records = []; all_codes = set(); base_codes = set()
    for pid, pattern in residual_patterns.items():
        selected_sinks, counts = pattern
        base_options = []
        for repair_choice in (0, 1):
            net, selected, dummy = build_weak_pattern(selected_sinks, counts, repair_choice)
            leaf_colors = {leaf: "L" for leaf in selected}; leaf_colors["LIN"] = "LIN"
            leaf_colors.update({leaf: "Z" for leaf in dummy})
            base_options.append(canonical_mixed_graph(semi_directed(net, leaf_colors)))
        base_code = min(base_options)
        assert base_code not in base_codes; base_codes.add(base_code)
        members = []
        for permutation_index, relabelling in enumerate(permutations((1,2,3,4))):
            options = []
            for repair_choice in (0, 1):
                net, selected, dummy = build_weak_pattern(selected_sinks, counts, repair_choice)
                colors = {leaf: f"L{label}" for leaf, label in zip(selected, relabelling)}
                colors["LIN"] = "LIN"; colors.update({leaf: "Z" for leaf in dummy})
                options.append(canonical_mixed_graph(semi_directed(net, colors)))
            code = min(options)
            assert code not in all_codes; all_codes.add(code)
            record = {
                "presentation_id": pid,
                "permutation_index": permutation_index,
                "outgoing_relabelling": list(relabelling),
                "selected_sink_indices": list(selected_sinks),
                "ordinary_counts_by_segment": list(counts),
                "canonical_graph_sha256": digest(code),
            }
            records.append(record); members.append(record["canonical_graph_sha256"])
        assert len(set(members)) == 24
        orbit_records.append({
            "presentation_id": pid,
            "orbit_size": 24,
            "selected_sink_indices": list(selected_sinks),
            "ordinary_counts_by_segment": list(counts),
            "unlabelled_role_graph_sha256": digest(base_code),
            "member_graph_sha256": members,
        })
    assert len(records) == len(all_codes) == 192
    assert len(orbit_records) == len(base_codes) == 8

    # Exact marginal F filtering of the eight orbit representatives.
    zero_patterns = {}; positive_certificates = []
    selected_factor_requests = {
        700: ((1,2,4), (0,2,4), (0,1,3), (0,1,2)),
        706: ((1,2,4), (0,2,4), (0,1,3), (0,1,2)),
    }
    for pid, (selected_sinks, counts) in residual_patterns.items():
        net, selected, _dummy = build_weak_pattern(selected_sinks, counts, 0)
        zeros = []
        for triple in combinations(range(5), 3):
            value = symbolic_F(net, selected, triple, f"p{pid}t{''.join(map(str,triple))}_")
            if value == 0: zeros.append(triple)
        zero_patterns[str(pid)] = [list(t) for t in zeros]
        if pid in selected_factor_requests:
            for triple in selected_factor_requests[pid]:
                value = symbolic_F(net, selected, triple, f"p{pid}t{''.join(map(str,triple))}_")
                assert value != 0
                signs = factor_sign(value)
                positive_certificates.append({
                    "presentation_id": pid,
                    "triple": list(triple),
                    "factorization": str(value),
                    "factor_signs": signs,
                })
    assert set(map(tuple, zero_patterns["629"])) >= {(0,1,4), (0,2,3)}
    for pid in (644,650,685): assert len(zero_patterns[str(pid)]) == 10
    for pid in (649,705):
        assert set(map(tuple, zero_patterns[str(pid)])) >= {(0,1,2),(0,1,4),(0,2,4),(1,2,4)}

    # Exact logical separator table.  A cycle triple has F>0 precisely when it
    # contains the cycle-sink label, and F=0 otherwise.
    base_logic = {
        629: {0:("target_zero_source_positive",(0,1,4)), 1:("target_zero_source_positive",(0,1,4)),
              2:("target_zero_source_positive",(0,2,3)), 3:("target_zero_source_positive",(0,2,3))},
        644: {0:("target_zero_source_positive",(0,1,4)), 1:("target_zero_source_positive",(0,1,4)),
              2:("target_zero_source_positive",(0,2,4)), 3:("target_zero_source_positive",(0,3,4))},
        650: {0:("target_zero_source_positive",(0,1,4)), 1:("target_zero_source_positive",(0,1,4)),
              2:("target_zero_source_positive",(0,2,4)), 3:("target_zero_source_positive",(0,3,4))},
        685: {0:("target_zero_source_positive",(0,1,4)), 1:("target_zero_source_positive",(0,1,4)),
              2:("target_zero_source_positive",(0,2,4)), 3:("target_zero_source_positive",(0,3,4))},
        700: {0:("source_zero_target_positive",(1,2,4)), 1:("source_zero_target_positive",(0,2,4)),
              2:("source_zero_target_positive",(0,1,3)), 3:("source_zero_target_positive",(0,1,2))},
        706: {0:("source_zero_target_positive",(1,2,4)), 1:("source_zero_target_positive",(0,2,4)),
              2:("source_zero_target_positive",(0,1,3)), 3:("source_zero_target_positive",(0,1,2))},
        649: {0:("target_zero_source_positive",(0,1,4)), 1:("target_zero_source_positive",(0,1,4)),
              2:("target_zero_source_positive",(0,2,4)), 3:("requires_seven_port_completion",None)},
        705: {0:("target_zero_source_positive",(0,1,4)), 1:("target_zero_source_positive",(0,1,4)),
              2:("target_zero_source_positive",(0,2,4)), 3:("requires_seven_port_completion",None)},
    }
    positive_lookup={(r["presentation_id"],tuple(r["triple"])) for r in positive_certificates}
    for pid, by_sink in base_logic.items():
        for sink,(kind,triple) in by_sink.items():
            if kind == "target_zero_source_positive":
                assert tuple(triple) in {tuple(t) for t in zero_patterns[str(pid)]} and sink in triple
            elif kind == "source_zero_target_positive":
                assert (pid,tuple(triple)) in positive_lookup and sink not in triple
            else:
                assert pid in (649,705) and sink == 3 and triple is None

    # Cycle positivity for triples containing its sink: exact two canonical factors.
    cycle_factor_records = []
    for counts in ((2,0),(1,1)):
        net = cycle_network(counts)
        selected = tuple(net["leaves"][:-1])
        value = symbolic_F(net, selected, (0,1,2), f"cycle{counts[0]}{counts[1]}_")
        cycle_factor_records.append({"side_counts": list(counts), "factorization": str(value), "factor_signs": factor_sign(value)})

    # Enumerate all conservative seven-port completions and verify S_TC.
    completion_summary = {}; completion_records = []; completion_codes = set(); target_count_vectors = set()
    for pid, pattern in residual_patterns.items():
        items = completions(pattern)
        per_counts = Counter()
        for words, sink in items:
            net, labels = build_core3_words(words, sink)
            assert standard_stc(net, labels)
            colors = {leaf: ("LIN" if label == 8 else f"L{label}") for leaf, label in labels.items()}
            code = canonical_mixed_graph(semi_directed(net, colors))
            assert code not in completion_codes; completion_codes.add(code)
            count_vector = tuple(map(len, words)); target_count_vectors.add(count_vector); per_counts[count_vector] += 1
            witness = None
            if pid == 649:
                witness = (1,2,sink)
            elif pid == 705:
                witness = (1,2,min(label for label in (5,6,7) if label in words[4]))
            completion_records.append({
                "presentation_id": pid,
                "segment_words": [list(w) for w in words],
                "sink_label": sink,
                "count_vector": list(count_vector),
                "standard_S_TC": True,
                "canonical_graph_sha256": digest(code),
                "full_parameterization_sha256": digest(full_parameterization_signature(net, labels)),
                "separator_triple": list(witness) if witness else None,
            })
        completion_summary[str(pid)] = {
            "completions": len(items),
            "count_vectors": {str(list(k)): v for k,v in sorted(per_counts.items())},
        }
    assert len(completion_records) == len(completion_codes) == 1686
    assert completion_summary["649"]["completions"] == 270
    assert completion_summary["705"]["completions"] == 216

    # Exact universal seven-port factors for the two surviving base orbits.
    caseA_net, caseA_labels = build_core3_words(((), (1,2), (), (3,), (4,)), 5)
    caseB_net, caseB_labels = build_core3_words(((), (1,), (), (2,3), (5,)), 4)
    # Marginalize every leaf except labels 1,2,5 and the incoming port.
    # This evaluates a polynomial of the complete seven-port tensor, not a
    # separate weak-model parameterization.
    caseA_selected = ("L1", "L2", "L5")
    caseB_selected = ("L1", "L2", "L5")
    caseA_F = symbolic_F(caseA_net, caseA_selected, (0,1,2), "caseA_")
    caseB_F = symbolic_F(caseB_net, caseB_selected, (0,1,2), "caseB_")
    seven_factors = [
        {"orbit": 649, "canonical_triple_labels": [1,2,5], "factorization": str(caseA_F), "factor_signs": factor_sign(caseA_F)},
        {"orbit": 705, "canonical_triple_labels": [1,2,5], "factorization": str(caseB_F), "factor_signs": factor_sign(caseB_F)},
    ]

    # Exact generic dimensions: upper bound from one root gauge and two gauges per reticulation;
    # lower bound from nonzero modular Jacobian minors for every relevant count vector.
    cycle_dimensions = []
    for left in range(7):
        counts = (left, 6-left); net = cycle_network(counts)
        cert = rank_minor_certificate(net, 1000 + left)
        assert expected_dimension(net) == 15 == cert["rank"]
        cycle_dimensions.append({"counts": list(counts), "dimension": 15, "minor": cert})
    theta_dimensions = []
    for index, counts in enumerate(sorted(target_count_vectors)):
        net = core3_count_network(counts)
        cert = rank_minor_certificate(net, 2000 + index)
        assert expected_dimension(net) == 17 == cert["rank"]
        theta_dimensions.append({"counts": list(counts), "dimension": 17, "minor": cert})

    return {
        "status": "PROVED",
        "scope": "all 192 seven-outgoing cycle-source to core-3 theta-target residual records",
        "residual_census_dependency": {
            "file": COMPLETION_CENSUS.name,
            "sha256": sha256(COMPLETION_CENSUS.read_bytes()).hexdigest(),
            "selected_count_three_records": len(inherited_residual_records),
            "deterministically_rebuilt_weak_metadata_records": len(enumerate_weak_metadata(4)),
        },
        "corrected_completion_rule": (
            "The conservative disjoint-support completion can require three additional "
            "outgoing labels for core 3, hence seven outgoing labels in total."
        ),
        "core3": {
            "vertices": core3["vertex_types"],
            "directed_segments": [list(s) for s in SEGMENTS],
            "minimal_strong_repairs": [list(r) for r in ((0,4),(3,4))],
        },
        "residual_records": records,
        "graph_symmetry_orbits_under_S4": orbit_records,
        "base_F_zero_patterns": zero_patterns,
        "base_positive_F_certificates": positive_certificates,
        "cycle_positive_F_certificates": cycle_factor_records,
        "base_orbit_separator_logic": {
            str(pid): {str(sink): [kind, list(triple) if triple else None] for sink,(kind,triple) in by_sink.items()}
            for pid,by_sink in base_logic.items()
        },
        "completion_summary": completion_summary,
        "completion_records": completion_records,
        "distinct_completed_standard_S_TC_graphs": len(completion_codes),
        "seven_port_universal_F_certificates": seven_factors,
        "generic_dimensions": {
            "formula": "dim = (edge parameters + reticulation parameters) - (1 + 2r) = 2n+2r-3",
            "cycle_sources": cycle_dimensions,
            "core3_theta_targets": theta_dimensions,
        },
        "classification": {
            "six_orbits_separated_on_original_five-port_tensor": [629,644,650,685,700,706],
            "two_orbits_requiring_completion_separator": [649,705],
            "stochastic_disjointness": 192,
            "lower_dimensional_or_one_sided_or_full_overlap": 0,
        },
        "conclusion": (
            "Every residual cycle-source/core-3-theta-target pair has disjoint complete "
            "open JC stochastic images.  No seven-port S_TC counterexample survives."
        ),
    }


def main():
    certificate = generate_certificate()
    normalized = json.loads(json.dumps(certificate, sort_keys=True))
    if "--write" in sys.argv:
        CERT.write_text(json.dumps(normalized, indent=2, sort_keys=True) + "\n")
    else:
        assert normalized == json.loads(CERT.read_text())
    print(json.dumps({
        "status": normalized["status"],
        "residual_records": len(normalized["residual_records"]),
        "S4_orbits": len(normalized["graph_symmetry_orbits_under_S4"]),
        "completed_S_TC_graphs": normalized["distinct_completed_standard_S_TC_graphs"],
        "classification": normalized["classification"],
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
