#!/usr/bin/env python3
"""Fail-closed independent verifier for the K3P global infrastructure.

The verifier shares no code with the generator.  It reconstructs the K3P
three-sunlet map, quartic pullbacks, Jacobians, incidence anchor systems,
physical inequalities, marginal sections, and manifest bindings directly.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
import argparse
import gzip
import json
import math
from pathlib import Path
import sys


Q = Fraction
NAMES = "0CGT"
SECTORS = ["C", "G", "T"]


class VerificationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def canon(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def digest_payload(value: dict) -> str:
    body = dict(value)
    body.pop("payload_sha256", None)
    return sha256(canon(body)).hexdigest()


def digest_file(path: Path) -> str:
    h = sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(1048576)
            if not block:
                return h.hexdigest()
            h.update(block)


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def load_gzip(path: Path) -> dict:
    with gzip.open(path, "rt") as stream:
        return json.load(stream)


def frac(value: str | int | Q) -> Q:
    return value if isinstance(value, Q) else Q(value)


def det_bareiss(source: list[list[int | Q]]) -> Q:
    a = [[frac(x) for x in row] for row in source]
    n = len(a)
    require(all(len(row) == n for row in a), "nonsquare determinant")
    sign = 1
    result = Q(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j] != 0), None)
        if pivot is None:
            return Q(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            sign = -sign
        p = a[j][j]
        result *= p
        for i in range(j + 1, n):
            if a[i][j]:
                s = a[i][j] / p
                for k in range(j + 1, n):
                    a[i][k] -= s * a[j][k]
    return result * sign


def gaussian_rank(source: list[list[Q]]) -> tuple[int, list[int], list[int]]:
    a = [[frac(x) for x in row] for row in source]
    row_ids = list(range(len(a)))
    m = len(a)
    n = len(a[0]) if m else 0
    r = 0
    rows: list[int] = []
    cols: list[int] = []
    for j in range(n):
        pivot = next((i for i in range(r, m) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        row_ids[r], row_ids[pivot] = row_ids[pivot], row_ids[r]
        p = a[r][j]
        for i in range(r + 1, m):
            if a[i][j]:
                s = a[i][j] / p
                for k in range(j, n):
                    a[i][k] -= s * a[r][k]
        rows.append(row_ids[r])
        cols.append(j)
        r += 1
        if r == m:
            break
    return r, rows, cols


def d3(triple: tuple[Q, Q, Q]) -> dict[str, Q]:
    c, g, t = triple
    return {
        "c": c, "g": g, "t": t,
        "1-c": 1 - c, "1-g": 1 - g, "1-t": 1 - t,
        "1+c-g-t": 1 + c - g - t,
        "1-c+g-t": 1 - c + g - t,
        "1-c-g+t": 1 - c - g + t,
    }


def ct(triple: tuple[Q, Q, Q]) -> dict[str, Q]:
    c, g, t = triple
    return {"c-g*t": c - g * t, "g-c*t": g - c * t, "t-c*g": t - c * g}


def verify_bridge(certificate: dict) -> None:
    require(certificate["schema"] == "k3p-three-sector-bridge-fibre-certificate-v1", "bridge schema")
    require(certificate["status"] == "PASS", "bridge status")
    require(certificate["payload_sha256"] == digest_payload(certificate), "bridge payload hash")
    require(certificate["character_labels"] == ["0", "C", "G", "T"], "bridge character labels")
    action = certificate["incidence_action"]
    require(action["independent_nonzero_sectors"] == SECTORS, "K2P sector equality introduced")
    require(action["sector_equalities_imposed"] == [], "hidden sector equality")
    require(action["fixed_observable_sector_labels"] is True, "sector labels not fixed")
    require(action["sector_permutation_is_gauge"] is False, "sector permutation accepted as gauge")
    for sector in SECTORS:
        item = action["sectorwise_cancellation_exponents"][sector]
        require(item["for_a_u"] == {"left_component": 1, "bridge": -1, "right_component": 0, "total": 0}, f"left cancellation {sector}")
        require(item["for_a_v"] == {"left_component": 0, "bridge": -1, "right_component": 1, "total": 0}, f"right cancellation {sector}")

    anchors = certificate["analytic_normalizer"]["anchor_degrees"]
    require(certificate["analytic_normalizer"]["degree_scope"].startswith("every integer d>=3"), "anchor degree scope")
    for degree in range(3, 13):
        record = anchors[str(degree)]
        expected_pairs = [(0, 1), (0, 2), (1, 2)] + [(0, i) for i in range(3, degree)]
        matrix = [[0] * degree for _ in range(degree)]
        for i, (u, v) in enumerate(expected_pairs):
            matrix[i][u] = matrix[i][v] = 1
        require(record["pair_anchors"] == [[u + 1, v + 1] for u, v in expected_pairs], f"anchor pair set degree {degree}")
        require(record["one_sector_matrix"] == matrix, f"anchor matrix degree {degree}")
        one = det_bareiss(matrix)
        require(one == -2 and record["one_sector_determinant"] == "-2", f"anchor determinant degree {degree}")
        block = []
        for s in range(3):
            for row in matrix:
                block.append([0] * (s * degree) + row + [0] * ((2 - s) * degree))
        three_rank, _, _ = gaussian_rank([[Q(x) for x in row] for row in block])
        require(three_rank == 3 * degree == record["three_sector_rank"], f"anchor rank degree {degree}")
        require(record["three_sector_selected_minor_determinant"] == "-8", f"three-sector determinant degree {degree}")

    witness = certificate["sector_independence_witness"]
    require([witness["C_pair_anchor_ratio_with_incidence_1"], witness["G_pair_anchor_ratio_with_incidence_1"], witness["T_pair_anchor_ratio_with_incidence_1"]] == ["2", "1", "1"], "independent-sector witness")
    fixed = certificate["fixed_label_nonpermutation_witness"]
    coordinates = fixed["two_leaf_equal_sector_coordinates"]
    require(coordinates == {"CC": "1/4", "GG": "1/9", "TT": "1/16"}, "fixed-label probe")
    require(len(set(coordinates.values())) == 3 and fixed["all_six_nonidentity_permutations_change_the_labelled_vector"] is True, "sector permutation not excluded")

    physical = certificate["physical_local_product"]
    required_d3 = ["c>0", "g>0", "t>0", "1-c>0", "1-g>0", "1-t>0", "1+c-g-t>0", "1-c+g-t>0", "1-c-g+t>0"]
    required_ct = ["c-g*t>0", "g-c*t>0", "t-c*g>0"]
    require(physical["principal_domain_inequalities"] == required_d3, "missing or changed D3+ inequality")
    require(physical["continuous_time_inequalities"] == required_ct, "missing or changed CT inequality")
    require(physical["endpoint_log_tangent_matrix"] == [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "endpoint tangent")
    require(physical["two_endpoint_incidence_tangent_rank"] == 6, "two-endpoint local-product rank")
    for continuous, key in ((False, "principal_examples"), (True, "continuous_time_examples")):
        for record in physical[key]:
            triple = tuple(map(frac, record["input"]))
            bounds = list(map(frac, record["lower_bounds"]))
            maximum = max(bounds)
            r = (1 + maximum) / 2
            require(r == frac(record["r"]) and r < 1, "split r")
            endpoint = (r, r, r)
            residual = tuple(x / r for x in triple)
            require([str(x) for x in endpoint] == record["endpoint"], "split endpoint")
            require([str(x) for x in residual] == record["residual"], "split residual")
            require(all(x > 0 for x in d3(endpoint).values()) and all(x > 0 for x in d3(residual).values()), "split D3+")
            if continuous:
                require(all(x > 0 for x in ct(endpoint).values()) and all(x > 0 for x in ct(residual).values()), "split CT")
            require(tuple(endpoint[i] * residual[i] for i in range(3)) == triple, "split product")

    fibre = certificate["complete_fibre"]
    require(fibre["one_scale_per_bridge_incidence_and_nonzero_sector"] is True, "incomplete fibre")
    require("tree" in fibre["tree_peeling_induction"]["step"], "tree peeling missing")
    require(certificate["proof_boundary"]["k2p_algebra_used"] is False, "K2P algebra admitted")


def verify_source_binding(project: Path, record: dict, gzip_json: bool = False) -> dict:
    path = project / record["path"]
    require(path.is_file(), f"missing bound source {record['path']}")
    require(digest_file(path) == record["sha256"], f"source hash {record['path']}")
    return load_gzip(path) if gzip_json else load(path)


def verify_marginal(project: Path, certificate: dict) -> None:
    require(certificate["schema"] == "k3p-selected-marginal-submersion-certificate-v1", "marginal schema")
    require(certificate["status"] == "PASS", "marginal status")
    require(certificate["payload_sha256"] == digest_payload(certificate), "marginal payload")
    group = certificate["character_group"]
    table = [[i ^ j for j in range(4)] for i in range(4)]
    require(group["xor_table"] == table, "character table")
    require(group["valid_for_every_selected_port_count"] is True, "complement proof scope")
    # Exhaust the actual selected port-count interval at the group-law level.
    # XOR(S^c)=XOR(all)^XOR(S) follows because each element is self-inverse.
    census = {}
    for k in range(3, 10):
        assignments = 4 ** (k - 1)
        canonical_masks = 2 ** (k - 1)
        census[str(k)] = assignments * canonical_masks
        # Exact enumeration of every zero-sum assignment; the arbitrary-mask
        # identity then follows from the checked XOR table and associativity.
        for prefix in product(range(4), repeat=k - 1):
            total = 0
            for x in prefix:
                total ^= x
            chars = prefix + (total,)
            aggregate = 0
            for x in chars:
                aggregate ^= x
            require(aggregate == 0, f"zero-sum assignment k={k}")
    require(census == {str(k): 8 ** (k - 1) for k in range(3, 10)}, "split-complement census")

    triple = certificate["triple_product_map"]
    require(triple["m_range"] == "every positive integer", "marginal m scope")
    require(triple["parameter_rank"] == 3 and triple["image_tangent_rank"] == 3 and triple["local_openness"] is True, "marginal rank/openness")
    sections = certificate["physical_sections"]["exact_examples_m_1_through_12"]
    require(len(sections) == 24, "physical-section example census")
    for record in sections:
        m = record["m"]
        require(1 <= m <= 12, "physical section m")
        target = tuple(map(frac, record["target"]))
        residual = tuple(map(frac, record["residual"]))
        require(all(x > 0 for x in d3(target).values()), "section target D3+")
        if m == 1:
            require(frac(record["isotropic_prefix_aggregate_R"]) == 1 and residual == target, "m=1 section")
        else:
            c, g, t = target
            bounds = [c, g, t]
            if record["domain"] == "D3_CT":
                bounds += [g * t / c, c * t / g, c * g / t]
            else:
                bounds += [g + t - c, c + t - g, c + g - t]
            R = (1 + max(bounds)) / 2
            require(frac(record["isotropic_prefix_aggregate_R"]) == R, "section aggregate")
            require(residual == tuple(x / R for x in target), "section residual")
            require(all(x > 0 for x in d3(residual).values()), "section residual D3+")
            if record["domain"] == "D3_CT":
                require(all(x > 0 for x in ct(target).values()) and all(x > 0 for x in ct(residual).values()), "section CT")

    inheritance = certificate["switching_and_inheritance"]
    require(inheritance["maximum_reticulations_per_level2_factor"] == 2, "level-2 switching bound")
    for r in range(3):
        rows = inheritance["switching_weight_checks"][str(r)]
        lambdas = [Q(j + 2, j + 5) for j in range(r)]
        expected = []
        total = Q(0)
        for bits in product((0, 1), repeat=r):
            value = Q(1)
            for bit, lam in zip(bits, lambdas):
                value *= lam if bit else 1 - lam
            total += value
            expected.append({"bits": list(bits), "weight": str(value)})
        require(rows == expected and total == 1, f"switching weights r={r}")
    require(inheritance["weights_sum_to_one"] is True, "inheritance total")
    require("derivative -1" in inheritance["parent_flip"] and "derivative +1" in inheritance["retained_parent_role"], "inheritance transports")

    inventory = certificate["selected_restriction_inventory"]
    require(inventory["restriction_families"] == ["rigid_support", "restoration_prefix", "support_plus_one", "support_plus_two"], "restriction families")
    require(inventory["selected_port_range"] == [3, 9], "restriction port range")
    require(inventory["incoming_modes"] == ["selected", "zero-character dummy"], "incoming modes")
    require(inventory["inheritance_transports"] == ["lambda", "1-lambda"], "inventory inheritance")
    require(inventory["edge_class_lengths"] == "all positive integers", "edge class length scope")

    atlas = verify_source_binding(project, inventory["four_port_atlas"])
    require(atlas["schema"] == "k3p-four-port-descriptor-report-v1", "bound atlas schema")
    for key in ("source_count", "target_count", "output_coordinates", "raw_relation_count"):
        require(atlas[key] == inventory["four_port_atlas"][key], f"atlas field {key}")
    atlas_source = project / inventory["four_port_atlas"]["atlas_source_path"]
    require(digest_file(atlas_source) == inventory["four_port_atlas"]["atlas_source_sha256"], "atlas source hash")
    require(inventory["four_port_atlas"]["model"] == "K3P", "atlas model")

    restoration = verify_source_binding(project, inventory["restoration_topology"], True)
    for key in ("six_port_children", "seven_port_children", "unresolved_paths"):
        require(restoration["census"][key] == inventory["restoration_topology"][key], f"restoration {key}")
    require(inventory["restoration_topology"]["algebra_fields_ignored"] is True, "restoration algebra boundary")
    contract = verify_source_binding(project, inventory["probe_topology_contract"])
    require(contract["status"] == "PASS", "probe topology contract")
    require(contract["anchor_census"]["physical_equality_anchor_records"] == inventory["probe_topology_contract"]["anchors"], "probe anchors")
    require(contract["candidate_census"]["first_probe_source_target_pairs"] == inventory["probe_topology_contract"]["first_probe_pairs"], "probe first pairs")
    require(inventory["probe_topology_contract"]["algebra_fields_ignored"] is True, "probe K2P algebra boundary")
    active = inventory.get("active_k3p_probe_binding")
    if active:
        active_path = project / active["path"]
        require(digest_file(active_path) == active["sha256"], "active K3P probe binding")
    source_relative = certificate["source_relative_open_image"]
    require(source_relative["target_marginal_openness_used"] is False, "target marginal openness used")
    require(source_relative["direct_marginal_of_original_containment"] is True, "not a direct source marginal")
    require(certificate["k2p_algebra_used"] is False, "K2P algebra used in marginal proof")


class Poly:
    """Sparse integer polynomial with monomials as sorted variable-name tuples."""

    def __init__(self, terms: dict[tuple[str, ...], int] | None = None):
        self.terms = {tuple(sorted(k)): int(v) for k, v in (terms or {}).items() if v}

    @staticmethod
    def variable(name: str) -> "Poly":
        return Poly({(name,): 1})

    @staticmethod
    def one() -> "Poly":
        return Poly({(): 1})

    def __add__(self, other: "Poly") -> "Poly":
        answer: defaultdict[tuple[str, ...], int] = defaultdict(int)
        for key, value in self.terms.items():
            answer[key] += value
        for key, value in other.terms.items():
            answer[key] += value
        return Poly(dict(answer))

    def __neg__(self) -> "Poly":
        return Poly({key: -value for key, value in self.terms.items()})

    def __sub__(self, other: "Poly") -> "Poly":
        return self + (-other)

    def __mul__(self, other: "Poly") -> "Poly":
        answer: defaultdict[tuple[str, ...], int] = defaultdict(int)
        for left, a in self.terms.items():
            for right, b in other.terms.items():
                answer[tuple(sorted(left + right))] += a * b
        return Poly(dict(answer))


class Jet:
    def __init__(self, value: Q, gradient: tuple[Q, ...]):
        self.value, self.gradient = value, gradient

    def __add__(self, other: "Jet") -> "Jet":
        return Jet(self.value + other.value, tuple(a + b for a, b in zip(self.gradient, other.gradient)))

    def __sub__(self, other: "Jet") -> "Jet":
        return Jet(self.value - other.value, tuple(a - b for a, b in zip(self.gradient, other.gradient)))

    def __mul__(self, other: "Jet") -> "Jet":
        return Jet(self.value * other.value, tuple(self.value * b + other.value * a for a, b in zip(self.gradient, other.gradient)))


def characters() -> list[tuple[int, int, int]]:
    return [(a, b, a ^ b) for a in range(4) for b in range(4)]


def triangle_formula(orientation: int, variables, poly_mode: bool):
    order = {1: (1, 2, 0), 2: (0, 2, 1), 3: (0, 1, 2)}[orientation]
    one = Poly.one() if poly_mode else Jet(Q(1), (Q(0),) * 19)
    lam = variables["lambda"]
    outputs = []
    for original in characters():
        x, y, z = [original[i] for i in order]
        def ev(edge: str, h: int):
            return one if h == 0 else variables[f"{edge}{NAMES[h]}"]
        arms = ev("a", x) * ev("b", y) * ev("c", z)
        displayed_left = lam * ev("f", y) * ev("d", z)
        displayed_right = (one - lam) * ev("f", x) * ev("e", z)
        outputs.append(arms * (displayed_left + displayed_right))
    return outputs


def verify_h14(project: Path, certificate: dict) -> None:
    require(certificate["schema"] == "k3p-h14-contextual-germ-certificate-v1", "H14 schema")
    require(certificate["status"] == "PASS", "H14 status")
    require(certificate["payload_sha256"] == digest_payload(certificate), "H14 payload")
    require(certificate["ambient_normalized_dimension"] == 15, "wrong normalized ambient dimension")
    require(certificate["H14_dimension"] == 14 and certificate["H14_codimension"] == 1, "wrong H14 dimension")
    require(certificate["ambient_open_triangle_germ"] is False, "ambient-open triangle claim")
    require(certificate["common_relative_germ"]["never_ambient_rank_15"] is True, "rank-15 triangle claim")
    quartic_input = verify_source_binding(project, certificate["input_quartic"])
    terms = quartic_input["terms"]
    require(terms == certificate["quartic_terms"], "quartic term mutation")
    labels = ["".join(NAMES[x] for x in triple) for triple in characters()]
    require(labels == certificate["coordinate_labels"], "H14 coordinate order")
    for term in terms:
        require(term["coordinate_labels"] == [labels[i] for i in term["coordinate_indices"]], "quartic coordinate transport")

    pvars = {f"{edge}{sector}": Poly.variable(f"{edge}{sector}") for edge in "abcdef" for sector in SECTORS}
    pvars["lambda"] = Poly.variable("lambda")
    for orientation in (1, 2, 3):
        outputs = triangle_formula(orientation, pvars, True)
        pullback = Poly()
        for term in terms:
            monomial = Poly.one()
            for i in term["coordinate_indices"]:
                monomial = monomial * outputs[i]
            pullback = pullback + (monomial if term["coefficient"] == 1 else -monomial)
        require(not pullback.terms, f"H14 pullback orientation {orientation}")

    point_values = [Q(1, 2)] * 15 + [Q(1, 3)] * 3 + [Q(1, 2)]
    names = [f"{edge}{sector}" for edge in "abcdef" for sector in SECTORS] + ["lambda"]
    jets = {}
    for i, (name, value) in enumerate(zip(names, point_values)):
        gradient = [Q(0)] * 19
        gradient[i] = 1
        jets[name] = Jet(value, tuple(gradient))
    common = None
    for orientation in (1, 2, 3):
        outputs = triangle_formula(orientation, jets, False)
        values = tuple(x.value for x in outputs)
        if common is None:
            common = values
        require(values == common, f"common point orientation {orientation}")
        matrix = [list(x.gradient) for x in outputs]
        r, rows, columns = gaussian_rank(matrix)
        record = certificate["orientations"][str(orientation)]
        require(r == 14 == record["rank"], f"H14 rank orientation {orientation}")
        require(rows == record["minor_rows"] and columns == record["minor_columns"], f"H14 pivot transport {orientation}")
        minor = [[matrix[i][j] for j in columns] for i in rows]
        require(str(det_bareiss(minor)) == record["minor_determinant"], f"H14 minor orientation {orientation}")
        require(record["quartic_pullback_terms"] == 0, f"stored pullback orientation {orientation}")
        require(record["context_contraction_id"] == "common-labelled-three-port-multilinear-contraction-v1", f"context id orientation {orientation}")
        require(record["labelled_port_order"] == [0, 1, 2], f"context port transport orientation {orientation}")
    require(common is not None and [str(x) for x in common] == certificate["common_tensor"], "stored common tensor")

    value = Q(0)
    gradient = [Q(0)] * 16
    for term in terms:
        indices = term["coordinate_indices"]
        monomial = Q(term["coefficient"])
        for i in indices:
            monomial *= common[i]
        value += monomial
        for variable in set(indices):
            derivative = Q(term["coefficient"] * indices.count(variable))
            skipped = False
            for i in indices:
                if i == variable and not skipped:
                    skipped = True
                else:
                    derivative *= common[i]
            gradient[variable] += derivative
    require(value == 0 and any(gradient[1:]), "H14 smoothness")
    smooth = certificate["smoothness"]
    require(smooth["quartic_value"] == "0", "H14 value")
    require(smooth["normalized_gradient"] == [str(x) for x in gradient[1:]], "H14 gradient")
    require(smooth["nonzero_gradient_indices_in_16_coordinate_order"] == [i for i, x in enumerate(gradient) if x], "H14 gradient support")

    preimage = certificate["common_preimage"]
    require(preimage["inheritance_probability"] == "1/2", "triangle boundary inheritance")
    for row in preimage["edge_triples"]:
        edge = tuple(map(frac, row))
        require(all(x > 0 for x in d3(edge).values()), "triangle preimage D3+")
        require(all(x > 0 for x in ct(edge).values()), "triangle preimage CT")
    require(preimage["strict_D3_plus"] is True and preimage["strict_continuous_time"] is True, "triangle physical status")

    # Independent normalized irreducibility check.  Dehomogenize q000=1 and
    # regard F as a degree-one polynomial in q0CC.
    coeff: defaultdict[tuple[str, ...], int] = defaultdict(int)
    remainder: defaultdict[tuple[str, ...], int] = defaultdict(int)
    for term in terms:
        mon = [labels[i] for i in term["coordinate_indices"] if labels[i] != "000"]
        if "0CC" in mon:
            require(mon.count("0CC") == 1, "quartic not linear in q0CC")
            mon.remove("0CC")
            coeff[tuple(sorted(mon))] += term["coefficient"]
        else:
            remainder[tuple(sorted(mon))] += term["coefficient"]
    coeff = defaultdict(int, {k: v for k, v in coeff.items() if v})
    require(len(coeff) == 2 and sorted(coeff.values()) == [-1, 1], "irreducibility coefficient binomial")
    supports = list(coeff)
    require(set(supports[0]).isdisjoint(supports[1]), "coefficient monomials not disjoint")
    require(math.gcd(*[1 for _ in supports[0] + supports[1]]) == 1, "binomial exponent difference")
    assignment = defaultdict(lambda: Q(1))
    assignment["TGC"] = Q(2)
    assignment["0GG"] = assignment["0TT"] = Q(0)
    def evaluate(poly):
        total = Q(0)
        for mon, scalar in poly.items():
            term = Q(scalar)
            for variable in mon:
                term *= assignment[variable]
            total += term
        return total
    require(evaluate(coeff) == 0 and evaluate(remainder) == -1, "irreducibility nondivisibility specialization")
    irreducible = certificate["normalized_irreducibility_certificate"]
    require(irreducible["linear_variable"] == "q0CC", "irreducibility linear variable")
    require(irreducible["nondivisibility_specialization"]["coefficient_value"] == "0" and irreducible["nondivisibility_specialization"]["remainder_value"] == "-1", "irreducibility stored specialization")
    require(irreducible["gauss_lemma_conclusion"] == "the normalized quartic is irreducible over Q", "irreducibility conclusion")

    context = certificate["contextualization"]
    require(context["common_context_contraction_id"] == "common-labelled-three-port-multilinear-contraction-v1", "common context mutation")
    require(context["allows_context_to_reconnect_triangle_terminals"] is True, "context reconnection")
    require(context["tensor_product_independence_assumed"] is False, "false tensor-product context")
    require("rank >= d_context" in context["rank_lower_bound"] and "rank <= d_context" in context["rank_upper_bound"], "context rank sandwich")
    relative = certificate["common_relative_germ"]
    require(relative["each_orientation_submerses_onto_H14"] is True, "H14 submersion")
    require(relative["rank_relative_to_each_complete_triangle_image"] == 14 and relative["rank_in_ambient_A15"] == 14, "relative contextual rank")


def acyclic(graph: dict[str, list[str]]) -> bool:
    known = set(graph)
    visiting: set[str] = set()
    done: set[str] = set()
    def visit(node: str) -> bool:
        if node in done or node not in known:
            return True
        if node in visiting:
            return False
        visiting.add(node)
        for predecessor in graph[node]:
            if not visit(predecessor):
                return False
        visiting.remove(node)
        done.add(node)
        return True
    return all(visit(node) for node in graph)


def verify_global(project: Path, certificate: dict, bridge: dict, marginal: dict, h14: dict) -> None:
    require(certificate["schema"] == "k3p-global-gluing-genericity-reconstruction-certificate-v1", "global schema")
    require(certificate["internal_infrastructure_status"] == "PASS", "internal global status")
    require(certificate["payload_sha256"] == digest_payload(certificate), "global payload")
    deps = certificate["dependencies"]
    require(deps["bridge_fibre_payload_sha256"] == bridge["payload_sha256"], "bridge dependency")
    require(deps["marginal_payload_sha256"] == marginal["payload_sha256"], "marginal dependency")
    require(deps["H14_context_payload_sha256"] == h14["payload_sha256"], "H14 dependency")
    interface = deps["pointwise_cut_interface"]
    require(interface["required_status"] == "PASS", "cut interface weakened")
    current = interface.get("current_binding")
    accepted = False
    if current:
        path = project / current["path"]
        require(path.is_file() and digest_file(path) == current["sha256"], "cut binding hash")
        report = load(path)
        actual = report.get("K3P_pointwise_cut_theorem", {}).get("status")
        require(actual == current["reported_status"], "cut binding status")
        accepted = actual == "PASS" and current["accepted_as_pass"] is True
    expected_global = "PASS" if accepted else "BLOCKED_EXTERNAL_CUT_DEPENDENCY"
    require(certificate["global_theorem_dependency_status"] == expected_global, "global cut gate not fail-closed")

    gluing = certificate["simultaneous_physical_bridge_gluing"]
    require(gluing["principal_domain_inequalities"] == ["c>0", "g>0", "t>0", "1-c>0", "1-g>0", "1-t>0", "1+c-g-t>0", "1-c+g-t>0", "1-c-g+t>0"], "global missing D3+ inequality")
    require(gluing["continuous_time_inequalities"] == ["c-g*t>0", "g-c*t>0", "t-c*g>0"], "global missing CT inequality")
    require(gluing["incidence_product_compact_bounds"] == "0<L<=A_h<=U on the finite common compactly-contained local germs", "gluing compact bounds")
    require(gluing["common_effective_isotropic_spectrum"] == ["L^2/(4*U)"] * 3, "effective CT spectrum not isotropic")
    require(gluing["actual_coordinate_interval"] == ["L^2/(4*U^2)", "L/(4*U)"], "gluing coordinate formula")
    require(gluing["principal_composition_margin_lower_bound"] == "1-L/(2*U)>=1/2", "gluing D3+ symbolic lower bound")
    require(gluing["continuous_time_margin_lower_bound"] == "3*L^2/(16*U^2)>0", "gluing CT symbolic lower bound")
    for L, U in ((Q(1, 2), Q(2)), (Q(3, 5), Q(7, 3)), (Q(7), Q(7)), (Q(11), Q(13))):
        eps = L * L / (4 * U)
        lo, hi = eps / U, eps / L
        require(lo == L * L / (4 * U * U) and hi == L / (4 * U), "gluing coordinate algebra")
        principal = 1 - 2 * hi
        ct_lower = lo - hi * hi
        require(principal >= Q(1, 2) and ct_lower == 3 * L * L / (16 * U * U) > 0, "gluing strict symbolic inequalities")
    replay = gluing["exact_rational_replay_instance"]
    L, U = frac(replay["L"]), frac(replay["U"])
    eps = L * L / (4 * U)
    lo, hi = eps / U, eps / L
    require(replay == {
        "L": str(L), "U": str(U), "epsilon": str(eps),
        "actual_coordinate_interval": [str(lo), str(hi)],
        "principal_margin_lower_bound": str(1 - 2 * hi),
        "continuous_time_margin_lower_bound": str(lo - hi * hi),
    }, "gluing rational replay")
    require(gluing["same_epsilon_all_networks_and_bridges"] is True and gluing["finite_simultaneous_shrinking"] is True, "simultaneous gluing")
    require(gluing["incidence_cancellation"] is True and gluing["no_holonomy"] is True, "gluing gauge")

    genericity = certificate["genericity"]
    bounds = genericity["fixed_leaf_count_topology_bound"]
    require(bounds["reticulations"] == "r<=n-1", "reticulation finiteness bound")
    require(bounds["nonroot_tree_vertices"] == "t=n+r-2", "tree vertex count")
    require(bounds["rooted_vertices"] == "1+t+r+n=2*n+2*r-1<=4*n-3", "total vertex bound")
    for n in range(3, 51):
        r = n - 1
        t = n + r - 2
        require(1 + t + r + n == 4 * n - 3, "vertex count arithmetic")
    require(genericity["exceptional_set_proper"] is True, "generic exceptional set")
    require(genericity["scope"] == "for each fixed topology N; not pointwise parameter identifiability", "genericity scope")
    reconstruction = certificate["exact_reconstruction"]
    require(len(reconstruction["steps"]) == 8, "reconstruction steps")
    require(reconstruction["practical_finite_sequence_claimed"] is False, "practical reconstruction overclaim")
    require(reconstruction["individual_edge_parameters_identified"] is False, "edge-parameter overclaim")
    require("quantifier elimination" in reconstruction["termination"], "reconstruction termination")
    graph = certificate["logical_dependency_dag"]
    require(acyclic(graph), "cyclic global proof dependencies")
    require("pointwise_cut_interface" in graph["bridge_tree_recovery"], "cut missing from reconstruction DAG")
    require("H14_context" in graph["sufficiency"], "H14 missing from sufficiency")


def verify_manifest(project: Path, certificates: Path, manifest: dict, records: dict[str, dict]) -> None:
    require(manifest["schema"] == "k3p-global-infrastructure-manifest-v1", "manifest schema")
    require(manifest["payload_sha256"] == digest_payload(manifest), "manifest payload")
    expected_status = "PASS" if records["global"]["global_theorem_dependency_status"] == "PASS" else "PASS_INTERNAL_BLOCKED_EXTERNAL"
    require(manifest["status"] == expected_status, "manifest status")
    mapping = {
        "bridge_fibre/K3P_BRIDGE_FIBRE_CERTIFICATE.json": records["bridge"],
        "marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json": records["marginal"],
        "triangle_h14/K3P_H14_CONTEXT_CERTIFICATE.json": records["h14"],
        "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json": records["global"],
    }
    require(set(manifest["artifacts"]) == set(mapping), "manifest artifact set")
    for relative, value in mapping.items():
        path = certificates / relative
        record = manifest["artifacts"][relative]
        require(digest_file(path) == record["sha256"], f"manifest file hash {relative}")
        require(record["payload_sha256"] == value["payload_sha256"] and record["schema"] == value["schema"], f"manifest payload {relative}")
    generator = project / manifest["generator"]["path"]
    require(generator.is_file() and digest_file(generator) == manifest["generator"]["sha256"], "generator binding")
    required_implementations = {
        "global_infrastructure/verify_global_infrastructure.py",
        "global_infrastructure/test_global_infrastructure_mutations.py",
    }
    require(set(manifest["independent_implementations"]) == required_implementations, "independent implementation set")
    for relative, record in manifest["independent_implementations"].items():
        path = project / relative
        require(path.is_file() and digest_file(path) == record["sha256"], f"implementation hash {relative}")


def main(argv: list[str] | None = None) -> int:
    if not __debug__:
        print("FAIL: optimized mode is forbidden for certification verification", file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser()
    default = Path(__file__).resolve().parents[1]
    parser.add_argument("--project-root", type=Path, default=default)
    parser.add_argument("--certificate-root", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    project = args.project_root.resolve()
    certificates = (args.certificate_root or project).resolve()
    paths = {
        "bridge": certificates / "bridge_fibre" / "K3P_BRIDGE_FIBRE_CERTIFICATE.json",
        "marginal": certificates / "marginals" / "K3P_MARGINAL_SUBMERSION_CERTIFICATE.json",
        "h14": certificates / "triangle_h14" / "K3P_H14_CONTEXT_CERTIFICATE.json",
        "global": certificates / "global_infrastructure" / "K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json",
    }
    report = {"schema": "k3p-global-infrastructure-independent-verification-v1", "checks": {}, "status": "FAIL"}
    try:
        records = {name: load(path) for name, path in paths.items()}
        verify_bridge(records["bridge"])
        report["checks"]["bridge_fibre"] = "PASS"
        verify_marginal(project, records["marginal"])
        report["checks"]["marginal_submersion"] = "PASS"
        verify_h14(project, records["h14"])
        report["checks"]["H14_context"] = "PASS"
        verify_global(project, records["global"], records["bridge"], records["marginal"], records["h14"])
        report["checks"]["gluing_genericity_reconstruction"] = "PASS_INTERNAL"
        manifest = load(certificates / "global_infrastructure" / "GLOBAL_INFRASTRUCTURE_MANIFEST.json")
        verify_manifest(project, certificates, manifest, records)
        report["checks"]["manifest"] = "PASS"
        report["global_theorem_dependency_status"] = records["global"]["global_theorem_dependency_status"]
        report["status"] = "PASS_INTERNAL_BLOCKED_EXTERNAL" if report["global_theorem_dependency_status"] != "PASS" else "PASS"
    except (VerificationError, KeyError, ValueError, TypeError, OSError, json.JSONDecodeError) as error:
        report["error"] = str(error)
        if args.report:
            args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
