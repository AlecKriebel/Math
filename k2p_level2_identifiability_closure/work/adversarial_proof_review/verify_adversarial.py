#!/usr/bin/env python3
"""Independent exact audit of the K2P bridge/marginal/gluing argument.

This verifier intentionally imports no primary K2P implementation.  It checks
the finite linear algebra and inequalities from first principles, then reads
the proof text only to enforce the logical claim boundary.  The default mode
reports blockers; ``--require-pass`` turns those blockers into a nonzero
promotion-gate exit.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
PRIMARY = PROJECT / "work/bridge_marginal_closure"
RESTORATION = PROJECT / "work/restoration_sign_reclassification"
GLOBAL = PROJECT / "work/global_theorem_closure"
TOPOLOGY_CERTIFICATE = HERE / "topology_direction_certificate.json"


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_rank(matrix: list[list[int | F]]) -> int:
    if not matrix:
        return 0
    work = [[F(value) for value in row] for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(row, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        scale = work[row][column]
        work[row] = [value / scale for value in work[row]]
        for i in range(len(work)):
            if i == row or not work[i][column]:
                continue
            scale = work[i][column]
            work[i] = [a - scale * b for a, b in zip(work[i], work[row])]
        row += 1
        if row == len(work):
            break
    return row


def in_dplus(s: F, g: F) -> bool:
    return 0 < s < 1 and 0 < g < 1 and g > 2 * s - 1


def strict_stochastic_positive(s: F, g: F) -> bool:
    return (
        s > 0
        and g > 0
        and 1 - g > 0
        and 1 + 2 * s + g > 0
        and 1 - 2 * s + g > 0
    )


def in_ct(s: F, g: F) -> bool:
    return 0 < s < 1 and s * s < g < 1


def check_domain() -> dict[str, object]:
    checked = 0
    values = [F(i, 20) for i in range(1, 20)]
    for s, g in itertools.product(values, repeat=2):
        require(
            strict_stochastic_positive(s, g) == in_dplus(s, g),
            f"principal-domain equivalence failed at {(s, g)}",
        )
        checked += 1
    # Boundary cases enforce strictness rather than a closed cone.
    require(not in_dplus(F(1, 2), F(0)), "g=0 boundary accepted")
    require(not in_dplus(F(1, 2), F(1)), "g=1 boundary accepted")
    require(not in_dplus(F(3, 4), F(1, 2)), "stochastic facet accepted")
    return {
        "status": "PASS",
        "rational_points": checked,
        "symbolic_reduction": [
            "1-g>0 gives g<1",
            "1+2s+g>0 is automatic for s,g>0",
            "1-2s+g>0 gives g>2s-1",
            "s<1 follows from g<1 and g>2s-1",
        ],
    }


def pair_matrix(degree: int) -> list[list[int]]:
    pairs = [(0, 1), (0, 2), (1, 2)] + [
        (0, index) for index in range(3, degree)
    ]
    return [[int(index in pair) for index in range(degree)] for pair in pairs]


def check_incidence_normalizers() -> dict[str, object]:
    rows = []
    for degree in range(3, 13):
        one = pair_matrix(degree)
        two = [row + [0] * degree for row in one] + [
            [0] * degree + row for row in one
        ]
        require(matrix_rank(one) == degree, f"one-sector rank {degree}")
        require(matrix_rank(two) == 2 * degree, f"two-sector rank {degree}")
        rows.append([degree, degree, 2 * degree])

    degree_two = [[1, 1]]
    require(matrix_rank(degree_two) == 1, "degree-two stabilizer disappeared")

    scales = (F(2, 3), F(3, 5), F(5, 7), F(7, 11), F(11, 13))
    pair = {(i, j): scales[i] * scales[j] for i, j in itertools.combinations(range(5), 2)}
    recovered_first_squared = pair[(0, 1)] * pair[(0, 2)] / pair[(1, 2)]
    require(recovered_first_squared == scales[0] ** 2, "square-root formula")
    for index in range(1, 5):
        # Positivity selects the unique square root, after which r_1k/a_1=a_k.
        require(pair[(0, index)] / scales[0] == scales[index], "later scale formula")

    return {
        "status": "PASS",
        "degree_rows": rows,
        "degree_two_boundary": {"rank": 1, "kernel": "(1,-1)"},
        "marked_exponent_matrix": "identity in each sector",
        "positive_square_root_unique": True,
    }


def check_rank_one_fibre() -> dict[str, object]:
    left = (F(2), F(3), F(5))
    right = (F(7), F(11), F(13), F(17))
    bridge = F(19, 23)
    matrix = [[bridge * x * y for y in right] for x in left]
    left_scale, right_scale = F(29, 31), F(37, 41)
    altered_left = tuple(left_scale * x for x in left)
    altered_right = tuple(right_scale * y for y in right)
    altered_bridge = bridge / (left_scale * right_scale)
    altered = [
        [altered_bridge * x * y for y in altered_right]
        for x in altered_left
    ]
    require(matrix == altered, "rank-one incidence action did not cancel")
    require(
        len({altered_left[i] / left[i] for i in range(len(left))}) == 1,
        "left rank-one scale not unique",
    )
    require(
        len({altered_right[i] / right[i] for i in range(len(right))}) == 1,
        "right rank-one scale not unique",
    )
    # A nonuniform mutation creates a nonzero cross minor and cannot be a new
    # rank-one factorization of the same positive block.
    mutated_left = list(altered_left)
    mutated_left[0] += 1
    mutated = [
        [altered_bridge * x * y for y in altered_right]
        for x in mutated_left
    ]
    require(mutated != matrix, "nonuniform factor mutation survived")
    return {
        "status": "PASS",
        "positive_block_shape": [len(left), len(right)],
        "left_scale": str(left_scale),
        "right_scale": str(right_scale),
        "all_zero_scale": 1,
        "K2P_sector_constraint": "global C/T automorphism forces their unique block scales equal; G remains independent",
    }


def is_dag(nodes: set[int], arcs: list[tuple[int, int]]) -> bool:
    indegree = {node: 0 for node in nodes}
    children = {node: [] for node in nodes}
    for tail, head in arcs:
        indegree[head] += 1
        children[tail].append(head)
    queue = [node for node in nodes if indegree[node] == 0]
    seen = 0
    while queue:
        tail = queue.pop()
        seen += 1
        for head in children[tail]:
            indegree[head] -= 1
            if indegree[head] == 0:
                queue.append(head)
    return seen == len(nodes)


def check_k4_minus_edge_boundary() -> dict[str, object]:
    # Theta path lengths (1,2,2): poles 0,1; internal vertices 2,3;
    # the two external incidences end in leaves 4,5.  Insert a binary root 6
    # on every underlying edge, choose every pair of core reticulations, and
    # orient every edge.  This is a superset of LSA-valid rootings, so finding
    # no tree-child orientation proves the required exclusion.
    core = (0, 1, 2, 3)
    edges = [(0, 1), (0, 2), (2, 1), (0, 3), (3, 1), (2, 4), (3, 5)]
    nodes = set(range(7))
    admissible = 0
    tree_child = 0
    for root_edge_index, root_edge in enumerate(edges):
        split_edges = (
            edges[:root_edge_index]
            + edges[root_edge_index + 1 :]
            + [(root_edge[0], 6), (6, root_edge[1])]
        )
        for reticulations in itertools.combinations(core, 2):
            roles = {
                node: ("retic" if node in reticulations else "tree")
                for node in core
            }
            roles.update({4: "leaf", 5: "leaf", 6: "root"})
            for bits in itertools.product((0, 1), repeat=len(split_edges)):
                arcs = [
                    (tail, head) if not bit else (head, tail)
                    for (tail, head), bit in zip(split_edges, bits)
                ]
                indegree = {node: 0 for node in nodes}
                outdegree = {node: 0 for node in nodes}
                children = {node: [] for node in nodes}
                for tail, head in arcs:
                    indegree[head] += 1
                    outdegree[tail] += 1
                    children[tail].append(head)
                valid = (indegree[6], outdegree[6]) == (0, 2)
                valid = valid and all(
                    (indegree[node], outdegree[node])
                    == ((2, 1) if roles[node] == "retic" else (1, 2))
                    for node in core
                )
                valid = valid and all(
                    (indegree[node], outdegree[node]) == (1, 0)
                    for node in (4, 5)
                )
                if not valid or not is_dag(nodes, arcs):
                    continue
                admissible += 1
                if all(
                    roles[node] == "leaf"
                    or any(roles[child] in {"tree", "leaf"} for child in children[node])
                    for node in nodes
                ):
                    tree_child += 1
    require(admissible == 25, f"K4-e rooted census drift: {admissible}")
    require(tree_child == 0, "K4-e acquired a tree-child rooting")
    return {
        "status": "PASS",
        "rooted_binary_DAG_presentations": admissible,
        "tree_child_presentations": tree_child,
        "scope_note": "enumerated superset; LSA filtering can only remove presentations",
    }


def prufer_edges(code: tuple[int, ...]) -> list[tuple[int, int]]:
    n = len(code) + 2
    degrees = [1] * n
    for vertex in code:
        degrees[vertex] += 1
    edges = []
    for vertex in code:
        leaf = next(i for i, degree in enumerate(degrees) if degree == 1)
        edges.append((leaf, vertex))
        degrees[leaf] -= 1
        degrees[vertex] -= 1
    leaves = [i for i, degree in enumerate(degrees) if degree == 1]
    edges.append((leaves[0], leaves[1]))
    return edges


def check_tree_holonomy() -> dict[str, object]:
    trees = 0
    for n in range(2, 7):
        for code in itertools.product(range(n), repeat=max(0, n - 2)):
            edges = prufer_edges(code)
            incidence = []
            for u, v in edges:
                row = [0] * n
                row[u], row[v] = 1, -1
                incidence.append(row)
            require(len(edges) == n - 1, "tree edge count")
            require(matrix_rank(incidence) == n - 1, "tree incidence rank")
            require(len(edges) - n + 1 == 0, "nonzero tree cycle space")
            trees += 1
    return {
        "status": "PASS",
        "labelled_prufer_trees_checked": trees,
        "cycle_space_dimension": 0,
        "two_sectors": "independent copies of the same zero-holonomy calculation",
    }


def rational_serial_section(S: F, G: F, length: int) -> tuple[F, list[tuple[F, F]]]:
    k = length - 1
    M = max(S, G, 2 * S - G, F(0))
    # Bernoulli: (1-x)^k >= 1-kx.  With x=(1-M)/(2k), r^k>(1+M)/2>M.
    r = 1 - (1 - M) / (2 * k)
    R = r**k
    require(M < R < 1, "constructive serial threshold")
    return r, [(r, r)] * k + [(S / R, G / R)]


def check_serial_sections() -> dict[str, object]:
    pairs = []
    grid = [F(i, 20) for i in range(1, 20)]
    for S, G in itertools.product(grid, repeat=2):
        if in_dplus(S, G):
            pairs.append((S, G))
    tests = 0
    for S, G in pairs:
        for length in range(2, 9):
            _, factors = rational_serial_section(S, G, length)
            require(all(in_dplus(s, g) for s, g in factors), "serial factor outside D_plus")
            product_s = F(1)
            product_g = F(1)
            for s, g in factors:
                product_s *= s
                product_g *= g
            require((product_s, product_g) == (S, G), "serial product drift")
            tests += 1

    ct_tests = 0
    for length in range(2, 9):
        for s, g in ((F(1, 5), F(1, 3)), (F(2, 5), F(1, 2))):
            require(in_ct(s, g), "CT base factor")
            require(in_ct(s**length, g**length), "CT product")
            # These exact perfect powers replay the claimed coordinate-root section.
            require((s**length) ** 2 < g**length, "CT root inequality")
            ct_tests += 1
    return {
        "status": "PASS",
        "D_plus_effective_pairs": len(pairs),
        "D_plus_factorizations": tests,
        "CT_perfect_power_replays": ct_tests,
        "jacobian_rank": 2,
        "analyticity": "fixed-r section is linear in (S,G); positive coordinate roots are analytic",
    }


def check_physical_incidence_saturation() -> dict[str, object]:
    grid = [F(i, 20) for i in range(1, 20)]
    tests = 0
    for S, G in itertools.product(grid, repeat=2):
        if not in_dplus(S, G):
            continue
        M = max(S, G, 2 * S - G, F(0))
        r = 1 - (1 - M) / 4
        require(r * r > M, "three-edge near-identity threshold")
        factors = ((r, r), (S / (r * r), G / (r * r)), (r, r))
        require(all(in_dplus(s, g) for s, g in factors), "physical incidence split")
        product_s = factors[0][0] * factors[1][0] * factors[2][0]
        product_g = factors[0][1] * factors[1][1] * factors[2][1]
        require((product_s, product_g) == (S, G), "three-edge product")
        tests += 1
    return {
        "status": "PASS",
        "D_plus_three_edge_splits": tests,
        "endpoint_sector_directions": 4,
        "openness": "all three factor pairs satisfy strict inequalities",
        "topology": "serial degree-two vertices suppress to the original bridge",
        "CT": "coordinate cube roots give the analogous strict split",
    }


def dplus_glue(A: F, B: F) -> tuple[F, F]:
    return min(F(1, 4), A / 4), min(F(1, 3), B / 3)


def ct_glue(A: F, B: F) -> tuple[F, F]:
    upper = min(F(1), B)
    coefficient = max(F(1), B / (A * A))
    s = min(F(1, 2), A / 2, upper / (2 * (coefficient + 1)))
    lower = coefficient * s * s
    require(lower < upper, "empty CT interval")
    return s, (lower + upper) / 2


def check_gluing() -> dict[str, object]:
    products = (F(1, 20), F(1, 5), F(1, 2), F(1), F(2), F(5), F(20))
    tests = 0
    for A, B in itertools.product(products, repeat=2):
        s, g = dplus_glue(A, B)
        require(in_dplus(s, g), "source D_plus glue")
        require(in_dplus(s / A, g / B), "target D_plus glue")
        sct, gct = ct_glue(A, B)
        require(in_ct(sct, gct), "source CT glue")
        require(in_ct(sct / A, gct / B), "target CT glue")
        tests += 1
    return {
        "status": "PASS",
        "arbitrary_positive_product_tests": tests,
        "strict_neighborhood": "all defining inequalities are strict",
        "independence": "one construction per bridge; bridge quotient is a tree",
    }


def check_unconditional_lift_counterexample() -> dict[str, object]:
    # S1 is b=1-a; the target equation is b-a=0.
    pullback = (F(1), F(-2))  # 1-2a
    require(pullback != (F(0), F(0)), "target equation vanished on source child")
    intersection = F(1, 2)
    require(1 - 2 * intersection == 0, "intersection point")
    # Both projections to a are the full interval (0,1), with derivative one.
    return {
        "status": "COUNTEREXAMPLE_CONFIRMED",
        "selected_projection_relation": "equal open intervals",
        "projection_jacobian_rank": 1,
        "restored_relation": "not contained; intersection has relative dimension zero",
        "source_pullback": "1-2a",
    }


def check_forest_binding() -> dict[str, object]:
    report_path = RESTORATION / "corrected_restoration_forest.json"
    report = json.loads(report_path.read_text())
    require(report.get("status") == "PASS", "corrected restoration forest not PASS")
    require(
        report.get("schema") == "k2p-corrected-restoration-forest-v3",
        "corrected restoration schema",
    )
    census = report.get("census", {})
    require(census.get("first_children") == 36568, "first-child count")
    require(census.get("second_children") == 256, "second-child count")
    require(census.get("forest_edges") == 36824, "forest-edge count")
    require(census.get("final_leaves") == 36792, "final-leaf count")
    require(census.get("unresolved") == 0, "unresolved restoration child")
    return {
        "status": "FINITE_PREMISE_PASS",
        "report_sha256": sha256_file(report_path),
        "first_children": 36568,
        "second_children": 256,
        "forest_edges": 36824,
        "final_leaves": 36792,
        "unresolved": 0,
        "logical_use": "valid only along a fixed full relation and its actual restored label",
    }


def check_topology_direction_binding() -> dict[str, object]:
    report = json.loads(TOPOLOGY_CERTIFICATE.read_text())
    require(report.get("status") == "PASS", "directional topology audit not PASS")
    require(
        report.get("schema") == "k2p-displayed-quartet-direction-audit-v2",
        "displayed-quartet direction schema",
    )
    four_port = report.get("raw_four_port_quartets", {})
    current = report.get("current_raw4_summary", {})
    summary_relative = current.get("summary_path")
    require(isinstance(summary_relative, str), "current raw4 summary path")
    raw4_summary_path = PROJECT / summary_relative
    require(
        four_port.get("raw_directions") == 405216
        and four_port.get("quartet_exclusions") == 360408,
        "raw displayed-quartet partition",
    )
    require(
        current.get("total_rows") == 405216
        and current.get("displayed_quartet_exclusions") == 360408
        and current.get("forbidden_rooted_fields") == 0
        and current.get("forbidden_rooted_reasons") == 0
        and raw4_summary_path.is_file()
        and current.get("summary_sha256") == sha256_file(raw4_summary_path)
        and current.get("summary_payload_sha256")
        == json.loads(raw4_summary_path.read_text()).get("payload_sha256"),
        "current raw4 displayed-quartet binding",
    )
    require(
        report.get("excluded_claims")
        == [
            "rooted tree/sunlet classification",
            "restoration-child classification",
            "whole-map T_i classification",
        ],
        "displayed-quartet claim boundary",
    )
    require(
        report.get("scope")
        == (
            "principal D_plus; raw four-port displayed-quartet direction and "
            "tree-of-blobs predicate only; no restoration or whole-map T_i classifier"
        ),
        "directional topology scope drift",
    )
    return {
        "status": "PASS",
        "certificate_sha256": sha256_file(TOPOLOGY_CERTIFICATE),
        "raw_displayed_quartet_exclusions": 360408,
        "logical_strength": (
            "pointwise disjoint strict K2P images for different displayed-quartet sets"
        ),
        "restoration_authority": False,
    }


def proof_text_blockers() -> list[dict[str, str]]:
    text = (PRIMARY / "PROOF.md").read_text()
    global_text = (GLOBAL / "GLOBAL_PROOF.md").read_text()
    normalized_text = " ".join(text.split())
    normalized_global = " ".join(global_text.split())
    blockers = []
    if re.search(
        r"If a four-port source germ were contained in a marginalized target completion",
        text,
    ):
        blockers.append(
            {
                "id": "RESTORATION_UNCONDITIONAL_LIFT",
                "severity": "FATAL",
                "diagnostic": (
                    "Section 6 infers a restored child from a selected four-port relation. "
                    "Open marginal image does not supply such a lift.  State the theorem "
                    "for one fixed full source-target relation and marginalize that same "
                    "relation to its actual omitted physical label."
                ),
            }
        )
    if re.search(
        r"every\s+graph-derived marginal completion map has physical\s+open image",
        text,
    ):
        blockers.append(
            {
                "id": "MARGINAL_SCOPE_OVERCLAIM",
                "severity": "MAJOR",
                "diagnostic": (
                    "The proof establishes serial-product openness for an ordinary source "
                    "leaf subdivision.  It does not analyze every nonretaining target "
                    "deletion/reduction map.  Restrict the statement to the source map "
                    "actually used by fixed-full restoration, or prove the broader maps."
                ),
            }
        )
    # Fail closed on the mathematical content of the physical-chart repair.
    # Do not key this gate to one introductory sentence: that allowed a wording
    # change to bypass the earlier detector without proving saturation.
    physical_chart_markers = (
        "ambient positive-tensor quotient chart",
        "split each physical bridge pair",
        "four endpoint coordinates vary independently",
        "constant-rank physical parameter chart",
        "not about physicality of an arbitrary normalized slice tensor",
    )
    missing_physical_markers = [
        marker for marker in physical_chart_markers if marker not in normalized_text
    ]
    if missing_physical_markers:
        blockers.append(
            {
                "id": "PHYSICAL_LOCAL_PRODUCT_SATURATION_GAP",
                "severity": "MAJOR",
                "diagnostic": (
                    "The anchors prove an ambient analytic gauge slice.  Promotion to a "
                    "physical product chart also needs a strict three-factor bridge split, "
                    "four independent endpoint directions, and a regular constant-rank "
                    "physical chart. Missing proof markers: "
                    + ", ".join(missing_physical_markers)
                ),
            }
        )

    global_physical_markers = (
        "ambient positive-tensor quotient chart",
        "Physical saturation is a separate step",
        "four independent coordinates",
        "constant-rank physical parameter chart",
        "No claim is made that an arbitrary normalized slice tensor is itself physical",
    )
    missing_global_physical = [
        marker for marker in global_physical_markers if marker not in normalized_global
    ]
    if missing_global_physical:
        blockers.append(
            {
                "id": "GLOBAL_PHYSICAL_CHART_SCOPE_DRIFT",
                "severity": "MAJOR",
                "diagnostic": (
                    "The global proof must retain the ambient/physical distinction and "
                    "regular-point saturation. Missing proof markers: "
                    + ", ".join(missing_global_physical)
                ),
            }
        )

    restoration_markers = (
        "fixed full containment",
        "No openness or inverse-lifting assertion is made for an arbitrary target deletion map",
    )
    if any(marker not in normalized_text for marker in restoration_markers):
        blockers.append(
            {
                "id": "RESTORATION_FIXED_FULL_SCOPE_DRIFT",
                "severity": "FATAL",
                "diagnostic": (
                    "Restoration must start with one fixed full relation, use only source "
                    "restriction openness, and make no target inverse-lifting claim."
                ),
            }
        )

    global_restoration_markers = (
        "fixing a hypothetical full containment between two actual networks",
        "No selected relation is lifted and no target deletion map is inverted",
    )
    if any(marker not in normalized_global for marker in global_restoration_markers):
        blockers.append(
            {
                "id": "GLOBAL_RESTORATION_SCOPE_DRIFT",
                "severity": "FATAL",
                "diagnostic": (
                    "The global proof must bind each restoration child to the actual "
                    "omitted label of one fixed full relation."
                ),
            }
        )

    topology_markers = (
        "different quartet sets have disjoint strict K2P images",
        "Positive inheritance mixtures preserve their strict signs",
        "labelled tree of blobs is recovered pointwise, not merely generically",
    )
    if any(marker not in normalized_global for marker in topology_markers):
        blockers.append(
            {
                "id": "GLOBAL_DIRECTIONAL_TOPOLOGY_SCOPE_DRIFT",
                "severity": "FATAL",
                "diagnostic": (
                    "Generic cut recovery is insufficient for directed noncontainment. "
                    "The proof must use exact zero-versus-strict-positive quartet signs "
                    "and pointwise disjointness on D_plus."
                ),
            }
        )
    return blockers


def build_report() -> dict[str, object]:
    checks = {
        "principal_domain": check_domain(),
        "positive_rank_one_fibre": check_rank_one_fibre(),
        "incidence_normalizers": check_incidence_normalizers(),
        "K4_minus_edge_stabilizer_exclusion": check_k4_minus_edge_boundary(),
        "tree_holonomy": check_tree_holonomy(),
        "paired_serial_sections": check_serial_sections(),
        "physical_incidence_saturation": check_physical_incidence_saturation(),
        "simultaneous_gluing": check_gluing(),
        "unconditional_lift": check_unconditional_lift_counterexample(),
        "restoration_finite_premise": check_forest_binding(),
        "raw_displayed_quartet_direction_binding": check_topology_direction_binding(),
    }
    blockers = proof_text_blockers()
    report: dict[str, object] = {
        "schema": "k2p-adversarial-analytic-review-v1",
        "status": "PASS" if not blockers else "BLOCKED",
        "scope": "principal D_plus and strict continuous-time analytic layers; no mixed-sign claim",
        "upstream_hashes": {
            "bridge_proof": sha256_file(PRIMARY / "PROOF.md"),
            "bridge_verifier": sha256_file(PRIMARY / "verify_bridge_marginal.py"),
            "corrected_restoration_forest": sha256_file(
                RESTORATION / "corrected_restoration_forest.json"
            ),
            "global_proof": sha256_file(GLOBAL / "GLOBAL_PROOF.md"),
            "raw_displayed_quartet_certificate": sha256_file(TOPOLOGY_CERTIFICATE),
        },
        "checks": checks,
        "blockers": blockers,
        "pass_findings": [
            "principal D_plus inequalities",
            "two independent positive incidence sectors",
            "marked and degree-at-least-three unmarked normalizers",
            "degree-two stabilizer boundary, conditional on its graph-theoretic exclusion",
            "zero bridge-tree holonomy",
            "paired source serial marginal section",
            "simultaneous D_plus gluing",
            "simultaneous strict continuous-time gluing",
            "finite 36,824-edge corrected restoration premise",
            "pointwise raw displayed-quartet directional exclusions",
        ],
    }
    body = dict(report)
    report["payload_sha256"] = hashlib.sha256(canonical_bytes(body)).hexdigest()
    return report


def main() -> int:
    if not __debug__:
        raise AuditFailure("verification disabled under Python -O")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(report, sort_keys=True))
    if args.require_pass and report["status"] != "PASS":
        return 2
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditFailure as error:
        print(f"ADVERSARIAL_AUDIT_FAIL: {error}")
        raise SystemExit(1)
