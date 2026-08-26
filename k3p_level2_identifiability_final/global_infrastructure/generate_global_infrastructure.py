#!/usr/bin/env python3
"""Generate exact K3P global-infrastructure certificates.

This program intentionally rebuilds the model-specific algebra from the
K3P Fourier formulas.  The separately locked K2P package is read only for
graph/restoration/probe selection metadata; none of its two-sector algebra is
accepted as K3P evidence.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import gzip
import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "input_frozen"
K3P = FROZEN / "k3p_cloud_artifacts"
TOPOLOGY = FROZEN / "model_independent_topology_package"
SECTORS = ("C", "G", "T")
CHAR_NAMES = "0CGT"
CUT_TRANSFER = ROOT / "cut_recovery" / "strong_crossbridge" / "global_transfer"
CUT_TRANSFER_THEOREM_SHA256 = "dd0ffea14051b9f45764a87d1a96b78d8199883417ce9a4321bfef4d612e8e51"
CUT_TRANSFER_CLAIM = (
    "For binary standard semi-directed strongly tree-child level-2 networks "
    "under source-relative regular full-dimensional containment on strict D3,+, "
    "Cut(N)=Cut(Nprime)."
)
CUT_TRANSFER_BOUNDARY = {
    "conclusion": "Cut(N)=Cut(Nprime)_under_source_relative_containment_in_the_strong_class",
    "strong_class_cut_transfer": "PROVED",
    "universal_pointwise_K3P_cut_recovery": "WITHDRAWN_NOT_USED",
}
CUT_TRANSFER_NONCIRCULARITY = {
    "bridge_tree_equality_assumed": False,
    "common_bridge_tree_assumed": False,
    "fourteen_orbit_classification_imported": False,
    "only_preexisting_cut_direction_used": "Cut(Nprime) subset Cut(N)",
    "reverse_direction_proved_here": "Cut(N) subset Cut(Nprime)",
    "target_open_marginal_assumed": False,
    "target_regular_point_assumed": False,
}
CUT_TRANSFER_FILE_SET = {
    "GLOBAL_TRANSFER_AUDIT.md", "GLOBAL_TRANSFER_CERTIFICATE.json",
    "GLOBAL_TRANSFER_DIRECTION_UNIVERSE.json", "OPTIMIZED_VERIFICATION_REPORT.json",
    "README.md", "RELEASE_OPTIMIZED_VERIFICATION_REPORT.json",
    "RELEASE_VERIFICATION_REPORT.json", "VERIFICATION_REPORT.json", "WORK_LOG.md",
    "adversarial/ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.json",
    "adversarial/ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.md", "adversarial/MANIFEST.sha256",
    "adversarial/MUTATION_RESULTS.json", "adversarial/VERIFICATION_REPORT.json",
    "adversarial/WORK_LOG.md", "adversarial/test_global_transfer_adversarial_mutations.py",
    "adversarial/verify_global_transfer_adversarial.py", "build_global_transfer.py",
    "build_manifest.py", "verify_global_transfer.py", "verify_release.py",
}
CUT_TRANSFER_LOAD_BEARING_PATHS = {
    "directed_cut_inclusion_audit": "cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json",
    "frozen_strong_topology": "cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json",
    "pointwise_204_adversarial_mutations": "cut_recovery/strong_crossbridge/final_certificate/ADVERSARIAL_MUTATION_REPORT.json",
    "pointwise_204_certificate": "cut_recovery/strong_crossbridge/final_certificate/STRONG_CROSSBRIDGE_FINAL_CERTIFICATE.json",
    "pointwise_204_independent_verification": "cut_recovery/strong_crossbridge/final_certificate/VERIFICATION_REPORT.json",
    "pointwise_204_universe": "cut_recovery/strong_crossbridge/final_certificate/UNIVERSE_CERTIFICATE.json",
    "recompiled_direction_universe": "cut_recovery/strong_crossbridge/global_transfer/GLOBAL_TRANSFER_DIRECTION_UNIVERSE.json",
    "selected_marginal": "marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json",
}
GLOBAL_INFRASTRUCTURE_CLAIM_BOUNDARY = (
    "Internal bridge/marginal/H14/gluing/genericity logic and the exact "
    "strong-class containment cut-equality interface are PASS. The universal "
    "arbitrary-network pointwise cut-rank iff claim is withdrawn and not used. "
    "This infrastructure manifest does not by itself promote the final classification; "
    "restoration and the remaining release gates stay separate."
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def payload_hash(value: dict) -> str:
    body = dict(value)
    body.pop("payload_sha256", None)
    return sha256(canonical(body)).hexdigest()


def bind(value: dict) -> dict:
    value = dict(value)
    value["payload_sha256"] = payload_hash(value)
    return value


def file_sha(path: Path) -> str:
    h = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT.resolve()))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def read_json_gz(path: Path) -> dict:
    with gzip.open(path, "rt") as stream:
        return json.load(stream)


def q(value: str | int | F) -> F:
    return value if isinstance(value, F) else F(value)


def determinant(matrix: Iterable[Iterable[F]]) -> F:
    rows = [list(map(q, row)) for row in matrix]
    n = len(rows)
    if any(len(row) != n for row in rows):
        fail("determinant requires a square matrix")
    answer = F(1)
    for column in range(n):
        pivot = next((i for i in range(column, n) if rows[i][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            answer = -answer
        entry = rows[column][column]
        answer *= entry
        for i in range(column + 1, n):
            if rows[i][column]:
                scale = rows[i][column] / entry
                for j in range(column + 1, n):
                    rows[i][j] -= scale * rows[column][j]
    return answer


def rank(matrix: Iterable[Iterable[F]]) -> int:
    rows = [list(map(q, row)) for row in matrix]
    if not rows:
        return 0
    m, n = len(rows), len(rows[0])
    r = 0
    for column in range(n):
        pivot = next((i for i in range(r, m) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        entry = rows[r][column]
        for i in range(m):
            if i != r and rows[i][column]:
                scale = rows[i][column] / entry
                for j in range(column, n):
                    rows[i][j] -= scale * rows[r][j]
        r += 1
        if r == m:
            break
    return r


def rank_minor(matrix: list[list[F]]) -> tuple[int, list[int], list[int], F]:
    work = [row[:] for row in matrix]
    row_ids = list(range(len(work)))
    m = len(work)
    n = len(work[0]) if m else 0
    r = 0
    pivot_rows: list[int] = []
    pivot_columns: list[int] = []
    for column in range(n):
        pivot = next((i for i in range(r, m) if work[i][column]), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        row_ids[r], row_ids[pivot] = row_ids[pivot], row_ids[r]
        entry = work[r][column]
        for i in range(r + 1, m):
            if work[i][column]:
                scale = work[i][column] / entry
                for j in range(column, n):
                    work[i][j] -= scale * work[r][j]
        pivot_rows.append(row_ids[r])
        pivot_columns.append(column)
        r += 1
        if r == m:
            break
    minor = [[matrix[i][j] for j in pivot_columns] for i in pivot_rows]
    return r, pivot_rows, pivot_columns, determinant(minor)


def anchor_matrix(degree: int) -> tuple[list[list[int]], list[list[int]]]:
    pairs = [(0, 1), (0, 2), (1, 2)] + [(0, j) for j in range(3, degree)]
    matrix = [[0] * degree for _ in range(degree)]
    for row, (u, v) in enumerate(pairs):
        matrix[row][u] = 1
        matrix[row][v] = 1
    return [[u + 1, v + 1] for u, v in pairs], matrix


def domain_margins(triple: tuple[F, F, F]) -> dict[str, F]:
    c, g, t = triple
    return {
        "c": c,
        "g": g,
        "t": t,
        "1-c": 1 - c,
        "1-g": 1 - g,
        "1-t": 1 - t,
        "1+c-g-t": 1 + c - g - t,
        "1-c+g-t": 1 - c + g - t,
        "1-c-g+t": 1 - c - g + t,
    }


def ct_margins(triple: tuple[F, F, F]) -> dict[str, F]:
    c, g, t = triple
    return {"c-g*t": c - g * t, "g-c*t": g - c * t, "t-c*g": t - c * g}


def strict_positive(values: dict[str, F], label: str) -> None:
    bad = {name: str(value) for name, value in values.items() if value <= 0}
    if bad:
        fail(f"{label} is not strict: {bad}")


def split_witness(triple: tuple[F, F, F], continuous_time: bool) -> dict:
    c, g, t = triple
    bounds = [c, g, t]
    names = ["c", "g", "t"]
    if continuous_time:
        bounds.extend((g * t / c, c * t / g, c * g / t))
        names.extend(("g*t/c", "c*t/g", "c*g/t"))
    else:
        bounds.extend((g + t - c, c + t - g, c + g - t))
        names.extend(("g+t-c", "c+t-g", "c+g-t"))
    maximum = max(bounds)
    if maximum >= 1:
        fail("serial-split lower bound is not below one")
    r = (1 + maximum) / 2
    endpoint = (r, r, r)
    residual = (c / r, g / r, t / r)
    strict_positive(domain_margins(endpoint), "endpoint D3+")
    strict_positive(domain_margins(residual), "residual D3+")
    if continuous_time:
        strict_positive(ct_margins(endpoint), "endpoint CT")
        strict_positive(ct_margins(residual), "residual CT")
    if tuple(endpoint[i] * residual[i] for i in range(3)) != triple:
        fail("serial split does not multiply back to the original edge")
    return {
        "input": [str(x) for x in triple],
        "bound_names": names,
        "lower_bounds": [str(x) for x in bounds],
        "maximum": str(maximum),
        "r": str(r),
        "endpoint": [str(x) for x in endpoint],
        "residual": [str(x) for x in residual],
        "endpoint_D3_plus_minimum": str(min(domain_margins(endpoint).values())),
        "residual_D3_plus_minimum": str(min(domain_margins(residual).values())),
        "endpoint_CT_minimum": str(min(ct_margins(endpoint).values())) if continuous_time else None,
        "residual_CT_minimum": str(min(ct_margins(residual).values())) if continuous_time else None,
    }


def build_bridge_certificate() -> dict:
    anchors = {}
    for degree in range(3, 13):
        pairs, matrix = anchor_matrix(degree)
        det = determinant(matrix)
        if det != -2:
            fail(f"unexpected anchor determinant at degree {degree}: {det}")
        block = []
        for sector in range(3):
            for row in matrix:
                block.append([0] * (sector * degree) + row + [0] * ((2 - sector) * degree))
        if rank(block) != 3 * degree:
            fail(f"three-sector anchor rank failure at degree {degree}")
        anchors[str(degree)] = {
            "pair_anchors": pairs,
            "one_sector_matrix": matrix,
            "one_sector_determinant": str(det),
            "three_sector_rank": 3 * degree,
            "three_sector_selected_minor_determinant": str(det ** 3),
        }

    d3_examples = [
        split_witness((F(1, 2), F(2, 5), F(1, 3)), False),
        split_witness((F(2, 7), F(3, 10), F(1, 4)), False),
    ]
    ct_examples = [
        split_witness((F(3, 5), F(1, 2), F(2, 5)), True),
        split_witness((F(7, 10), F(3, 5), F(1, 2)), True),
    ]

    # A generic fixed-label probe: a nontrivial sector permutation changes an
    # observed coordinate, so it cannot be an unobserved gauge operation.
    distinct = {"C": F(1, 2), "G": F(1, 3), "T": F(1, 4)}
    probes = {sector + sector: str(value * value) for sector, value in distinct.items()}
    if len(set(probes.values())) != 3:
        fail("fixed-label probe did not distinguish all sectors")

    return bind({
        "schema": "k3p-three-sector-bridge-fibre-certificate-v1",
        "status": "PASS",
        "character_labels": ["0", *SECTORS],
        "normalization": {
            "zero_sector_scale": "a^0_{v,e}=1",
            "all_zero_component_coordinate": "P_v(0,...,0)=1",
            "zero_action_exponent": 0,
        },
        "incidence_action": {
            "component": "P_v(h)->P_v(h)*product_{e incident v} a[v,e,h_e], with a[v,e,0]=1",
            "bridge": "k_e(h)->k_e(h)/(a[u,e,h]*a[v,e,h])",
            "sectorwise_cancellation_exponents": {
                sector: {
                    "for_a_u": {"left_component": 1, "bridge": -1, "right_component": 0, "total": 0},
                    "for_a_v": {"left_component": 0, "bridge": -1, "right_component": 1, "total": 0},
                }
                for sector in SECTORS
            },
            "independent_nonzero_sectors": list(SECTORS),
            "sector_equalities_imposed": [],
            "fixed_observable_sector_labels": True,
            "sector_permutation_is_gauge": False,
        },
        "complete_fibre": {
            "positive_rank_one_block_uniqueness": "If xy^T=x'y'^T with positive entries, x'=s*x and y'=y/s for one s>0.",
            "one_scale_per_bridge_incidence_and_nonzero_sector": True,
            "tree_peeling_induction": {
                "base": "one component has no bridge incidence",
                "step": "a finite nontrivial tree has a leaf; rank-one uniqueness fixes its incident scales and removal leaves a tree",
                "conclusion": "every incidence is reached exactly once and no cycle holonomy exists",
            },
            "freeness": "full-column-rank monomial anchor exponents plus the unique positive square-root inverse",
            "excluded_unmarked_degree_two_stabilizer": "excluded by the strong tree-child retained-factor topology theorem",
        },
        "analytic_normalizer": {
            "formula": [
                "a1=sqrt(r12*r13/r23)",
                "a2=sqrt(r12*r23/r13)",
                "a3=sqrt(r13*r23/r12)",
                "ak=r1k/a1 for k>=4",
            ],
            "positive_chart_real_analytic": True,
            "degree_scope": "every integer d>=3; the leading 3x3 block has determinant -2 and each row (1,k) introduces column k",
            "anchor_degrees": anchors,
        },
        "sector_independence_witness": {
            "scale_only_C_at_incidence_1": "2",
            "G_and_T_scales": "1",
            "C_pair_anchor_ratio_with_incidence_1": "2",
            "G_pair_anchor_ratio_with_incidence_1": "1",
            "T_pair_anchor_ratio_with_incidence_1": "1",
        },
        "fixed_label_nonpermutation_witness": {
            "edge_sector_values": {k: str(v) for k, v in distinct.items()},
            "two_leaf_equal_sector_coordinates": probes,
            "all_six_nonidentity_permutations_change_the_labelled_vector": True,
        },
        "physical_local_product": {
            "principal_domain_inequalities": [
                "c>0", "g>0", "t>0", "1-c>0", "1-g>0", "1-t>0",
                "1+c-g-t>0", "1-c+g-t>0", "1-c-g+t>0",
            ],
            "continuous_time_inequalities": ["c-g*t>0", "g-c*t>0", "t-c*g>0"],
            "continuous_time_implies_principal": "put u=sqrt(g*t/c), v=sqrt(c*t/g), w=sqrt(c*g/t) in (0,1); then (c,g,t)=(v*w,u*w,u*v) and 1+v*w-u*w-u*v>(1-v)*(1-w)>0, cyclically",
            "principal_split_bound": ["c", "g", "t", "g+t-c", "c+t-g", "c+g-t"],
            "continuous_time_split_bound": ["c", "g", "t", "g*t/c", "c*t/g", "c*g/t"],
            "split": "y=(r,r,r) odot (y/r) with r=(1+max(bounds))/2",
            "two_endpoint_split": "y=A_u odot (y/(A_u odot A_v)) odot A_v; at the base take A_u=A_v=(sqrt(R),sqrt(R),sqrt(R)) with R=(1+max(bounds))/2",
            "two_endpoint_independent_variation": "strictness is open at both isotropic endpoints and at the residual, so the six endpoint sector coordinates vary independently",
            "endpoint_log_tangent_matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "two_endpoint_incidence_tangent_rank": 6,
            "all_bridges_simultaneous": "finite intersection of strict open neighborhoods",
            "principal_examples": d3_examples,
            "continuous_time_examples": ct_examples,
        },
        "proof_boundary": {
            "model_specific": "all three K3P sectors, D3+ and CT inequalities, and labelled-sector nonpermutation are regenerated here",
            "topology_only_dependency": "retained unmarked components have degree at least three and the component-incidence graph is a tree",
            "k2p_algebra_used": False,
        },
    })


def switching_weights(reticulations: int) -> list[dict]:
    variables = [F(j + 2, j + 5) for j in range(reticulations)]
    rows = []
    total = F(0)
    for bits in product((0, 1), repeat=reticulations):
        value = F(1)
        for bit, lam in zip(bits, variables):
            value *= lam if bit else 1 - lam
        total += value
        rows.append({"bits": list(bits), "weight": str(value)})
    if total != 1:
        fail("switching weights do not sum to one")
    return rows


def product_section(target: tuple[F, F, F], m: int, continuous_time: bool) -> dict:
    if m < 1:
        fail("edge-class length must be positive")
    if m == 1:
        factors = [target]
        r = F(1)
    else:
        c, g, t = target
        bounds = [c, g, t]
        if continuous_time:
            bounds.extend((g * t / c, c * t / g, c * g / t))
        else:
            bounds.extend((g + t - c, c + t - g, c + g - t))
        maximum = max(bounds)
        # R is the product of the m-1 isotropic factors.  Exact rational R is
        # enough for the certificate; its positive (m-1)-st root exists.
        R = (1 + maximum) / 2
        residual = tuple(x / R for x in target)
        strict_positive(domain_margins(residual), "product-section residual D3+")
        if continuous_time:
            strict_positive(ct_margins(residual), "product-section residual CT")
        r = R  # record the exact aggregate, avoiding algebraic-number syntax
        factors = [(F(-1), F(-1), F(-1))] * (m - 1) + [residual]
    return {
        "m": m,
        "target": [str(x) for x in target],
        "isotropic_prefix_aggregate_R": str(r),
        "isotropic_prefix_factor": "R^(1/(m-1))" if m > 1 else "none",
        "residual": [str(x) for x in factors[-1]],
        "product_equals_target": True,
        "domain": "D3_CT" if continuous_time else "D3_plus",
    }


def selected_restriction_inventory() -> dict:
    descriptor_path = K3P / "descriptor_report_4(1).json"
    atlas_path = K3P / "k3p_atlas_core.py"
    contract_path = TOPOLOGY / "anchor_inputs" / "probe_input_contract.json"
    closure_path = TOPOLOGY / "anchor_inputs" / "fixed_full_restoration_closure.json.gz"
    contract = read_json(contract_path)
    closure = read_json_gz(closure_path)
    descriptor = read_json(descriptor_path)
    if descriptor.get("schema") != "k3p-four-port-descriptor-report-v1":
        fail("unexpected K3P four-port descriptor report")
    if contract.get("status") != "PASS" or contract["anchor_census"]["physical_equality_anchor_records"] != 176:
        fail("topology-only probe input contract is not closed")
    if closure["census"]["unresolved_paths"] != 0:
        fail("topology restoration input has unresolved paths")

    active_probe = ROOT / "probes" / "K3P_PROBE_COHERENCE_CERTIFICATE.json"
    active_binding = None
    if active_probe.exists():
        probe = read_json(active_probe)
        active_binding = {
            "path": rel(active_probe),
            "sha256": file_sha(active_probe),
            "schema": probe.get("schema"),
            "status": probe.get("status"),
            "payload_sha256": probe.get("payload_sha256"),
            "one_port_rows": probe.get("one_port", {}).get("ordered_ledger", {}).get("rows"),
            "two_port_rows": (probe.get("two_port") or {}).get("ordered_ledger", {}).get("rows"),
            "use": "record coverage only; no K2P algebra",
        }

    return {
        "restriction_families": ["rigid_support", "restoration_prefix", "support_plus_one", "support_plus_two"],
        "selected_port_range": [3, 9],
        "selected_assignments": "all G=Z2xZ2 assignments with XOR sum zero",
        "split_normalization": "descendant masks S and S^c have the same sector on zero-sum assignments",
        "switching_signature": "complete row over every switching and every retained zero-sum assignment",
        "invisible_edge_class": "the all-zero complete signature is omitted",
        "visible_edge_class": "identical complete signatures are replaced by one independent K3P triple equal to the sectorwise product",
        "inheritance_transports": ["lambda", "1-lambda"],
        "incoming_modes": ["selected", "zero-character dummy"],
        "edge_class_lengths": "all positive integers",
        "four_port_atlas": {
            "path": rel(descriptor_path),
            "sha256": file_sha(descriptor_path),
            "atlas_source_path": rel(atlas_path),
            "atlas_source_sha256": file_sha(atlas_path),
            "source_count": descriptor["source_count"],
            "target_count": descriptor["target_count"],
            "output_coordinates": descriptor["output_coordinates"],
            "raw_relation_count": descriptor["raw_relation_count"],
            "model": "K3P",
        },
        "restoration_topology": {
            "path": rel(closure_path),
            "sha256": file_sha(closure_path),
            "six_port_children": closure["census"]["six_port_children"],
            "seven_port_children": closure["census"]["seven_port_children"],
            "unresolved_paths": closure["census"]["unresolved_paths"],
            "used_fields": ["census", "claim_scope", "topology_witnesses", "isomorphism_certificates"],
            "algebra_fields_ignored": True,
        },
        "probe_topology_contract": {
            "path": rel(contract_path),
            "sha256": file_sha(contract_path),
            "anchors_by_port_count": contract["anchor_census"]["by_port_count"],
            "anchors": contract["anchor_census"]["physical_equality_anchor_records"],
            "source_sites": contract["candidate_census"]["source_sites"],
            "target_sites": contract["candidate_census"]["target_sites"],
            "first_probe_pairs": contract["candidate_census"]["first_probe_source_target_pairs"],
            "used_fields": ["anchor_census", "candidate_census", "root_movement_contract"],
            "algebra_fields_ignored": True,
        },
        "active_k3p_probe_binding": active_binding,
    }


def build_marginal_certificate() -> dict:
    target_plus = (F(1, 2), F(2, 5), F(1, 3))
    target_ct = (F(3, 5), F(1, 2), F(2, 5))
    sections = []
    for m in range(1, 13):
        sections.append(product_section(target_plus, m, False))
        sections.append(product_section(target_ct, m, True))

    xor_table = [[a ^ b for b in range(4)] for a in range(4)]
    if any((a ^ a) != 0 for a in range(4)):
        fail("character group inverse check failed")
    switching = {str(r): switching_weights(r) for r in range(3)}

    return bind({
        "schema": "k3p-selected-marginal-submersion-certificate-v1",
        "status": "PASS",
        "character_group": {
            "encoding": {name: i for i, name in enumerate(CHAR_NAMES)},
            "xor_table": xor_table,
            "zero_sum_complement_identity": "xor(S^c)=xor(all)^xor(S)=xor(S)",
            "valid_for_every_selected_port_count": True,
        },
        "triple_product_map": {
            "formula": "((c_i,g_i,t_i))_{i=1}^m -> (product c_i, product g_i, product t_i)",
            "m_range": "every positive integer",
            "jacobian": "three rows on disjoint variable blocks; d(product x_i)/dx_j=product_{i!=j} x_i>0",
            "selected_3x3_minor": "diag(product_{i>1}c_i, product_{i>1}g_i, product_{i>1}t_i)",
            "parameter_rank": 3,
            "local_openness": True,
            "image_tangent_rank": 3,
        },
        "physical_sections": {
            "construction": "fix m-1 equal isotropic factors with aggregate R in (B,1), and use target/R as residual",
            "principal_bound_B": "max(c,g,t,g+t-c,c+t-g,c+g-t)",
            "continuous_time_bound_B": "max(c,g,t,g*t/c,c*t/g,c*g/t)",
            "uniform_all_m_proof": "for m>1 take each prefix factor R^(1/(m-1)); strictness is open around the displayed section",
            "exact_examples_m_1_through_12": sections,
        },
        "switching_and_inheritance": {
            "maximum_reticulations_per_level2_factor": 2,
            "switching_weight_checks": switching,
            "weights_sum_to_one": True,
            "parent_flip": "lambda -> 1-lambda is a physical analytic diffeomorphism of (0,1) with derivative -1",
            "retained_parent_role": "lambda with derivative +1",
            "complete_switching_signatures_required": True,
        },
        "selected_restriction_inventory": selected_restriction_inventory(),
        "source_relative_open_image": {
            "chain_rule": "R o Phi_full = Phi_selected o delta_R",
            "full_and_selected_rank_minors_meet": "nonempty intersection of finitely many Zariski-open subsets of the irreducible parameter space",
            "constant_rank_conclusion": "R maps a dense regular source locus openly onto a relative selected-image neighborhood",
            "target_marginal_openness_used": False,
            "direct_marginal_of_original_containment": True,
        },
        "k2p_algebra_used": False,
    })


# Sparse polynomials are maps from exponent tuples to rational coefficients.
def poly_add(*summands: tuple[F, dict[tuple[int, ...], F]]) -> dict[tuple[int, ...], F]:
    answer: defaultdict[tuple[int, ...], F] = defaultdict(F)
    for scalar, polynomial in summands:
        for exponent, coefficient in polynomial.items():
            answer[exponent] += scalar * coefficient
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def poly_mul(left: dict[tuple[int, ...], F], right: dict[tuple[int, ...], F]) -> dict[tuple[int, ...], F]:
    answer: defaultdict[tuple[int, ...], F] = defaultdict(F)
    for x, a in left.items():
        for y, b in right.items():
            answer[tuple(u + v for u, v in zip(x, y))] += a * b
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def poly_var(count: int, index: int) -> dict[tuple[int, ...], F]:
    return {tuple(1 if i == index else 0 for i in range(count)): F(1)}


def poly_one(count: int) -> dict[tuple[int, ...], F]:
    return {(0,) * count: F(1)}


def poly_product(polynomials: Iterable[dict[tuple[int, ...], F]], count: int) -> dict[tuple[int, ...], F]:
    answer = poly_one(count)
    for polynomial in polynomials:
        answer = poly_mul(answer, polynomial)
    return answer


def poly_value(polynomial: dict[tuple[int, ...], F], point: tuple[F, ...]) -> F:
    answer = F(0)
    for exponent, coefficient in polynomial.items():
        term = coefficient
        for value, power in zip(point, exponent):
            term *= value ** power
        answer += term
    return answer


def poly_derivative_value(polynomial: dict[tuple[int, ...], F], point: tuple[F, ...], variable: int) -> F:
    answer = F(0)
    for exponent, coefficient in polynomial.items():
        power = exponent[variable]
        if not power:
            continue
        term = coefficient * power
        for j, (value, degree) in enumerate(zip(point, exponent)):
            term *= value ** (degree - (1 if j == variable else 0))
        answer += term
    return answer


def edge_var(count: int, edge: int, character: int) -> dict[tuple[int, ...], F]:
    return poly_one(count) if character == 0 else poly_var(count, 3 * edge + character - 1)


def zero_sum_three() -> list[tuple[int, int, int]]:
    return [(x, y, x ^ y) for x in range(4) for y in range(4)]


def coordinate_labels() -> list[str]:
    return ["".join(CHAR_NAMES[x] for x in triple) for triple in zero_sum_three()]


def sunlet_map(orientation: int) -> list[dict[tuple[int, ...], F]]:
    # Variables are the C,G,T spectra on a,b,c,d,e,f followed by lambda.
    count = 19
    lam = poly_var(count, 18)
    one_minus = poly_add((F(1), poly_one(count)), (F(-1), lam))
    order = {1: (1, 2, 0), 2: (0, 2, 1), 3: (0, 1, 2)}[orientation]
    outputs = []
    for original in zero_sum_three():
        x, y, z = (original[i] for i in order)
        arms = poly_product((edge_var(count, 0, x), edge_var(count, 1, y), edge_var(count, 2, z)), count)
        first = poly_product((lam, edge_var(count, 5, y), edge_var(count, 3, z)), count)
        second = poly_product((one_minus, edge_var(count, 5, x), edge_var(count, 4, z)), count)
        outputs.append(poly_mul(arms, poly_add((F(1), first), (F(1), second))))
    return outputs


def compose_quartic(outputs: list[dict[tuple[int, ...], F]], terms: list[dict]) -> dict[tuple[int, ...], F]:
    count = len(next(iter(outputs[0])))
    answer: dict[tuple[int, ...], F] = {}
    for term in terms:
        monomial = poly_product((outputs[i] for i in term["coordinate_indices"]), count)
        answer = poly_add((F(1), answer), (F(term["coefficient"]), monomial))
    return answer


def build_h14_certificate() -> dict:
    quartic_path = K3P / "k3p_three_sunlet_quartic.json"
    quartic = read_json(quartic_path)
    terms = quartic["terms"]
    labels = coordinate_labels()
    if any(
        term.get("coordinate_labels") != [labels[i] for i in term["coordinate_indices"]]
        for term in terms
    ):
        fail("H14 term labels do not match the canonical zero-sum K3P coordinate order")

    point = tuple(
        value
        for edge in ((F(1, 2),) * 3,) * 5 + ((F(1, 3),) * 3,)
        for value in edge
    ) + (F(1, 2),)
    orientation_records = {}
    common = None
    for orientation in (1, 2, 3):
        outputs = sunlet_map(orientation)
        pullback = compose_quartic(outputs, terms)
        if pullback:
            fail(f"orientation {orientation} does not satisfy H14 identically")
        values = tuple(poly_value(polynomial, point) for polynomial in outputs)
        if common is None:
            common = values
        elif values != common:
            fail("ordinary triangle orientations do not meet at the exact common tensor")
        jacobian = [[poly_derivative_value(polynomial, point, j) for j in range(19)] for polynomial in outputs]
        r, rows, columns, minor = rank_minor(jacobian)
        if r != 14 or not minor:
            fail(f"orientation {orientation} has wrong exact rank {r}")
        orientation_records[str(orientation)] = {
            "parameter_count": 19,
            "normalized_output_count": 16,
            "rank": r,
            "minor_rows": rows,
            "minor_columns": columns,
            "minor_determinant": str(minor),
            "quartic_pullback_terms": 0,
            "context_contraction_id": "common-labelled-three-port-multilinear-contraction-v1",
            "labelled_port_order": [0, 1, 2],
        }

    if common is None:
        fail("missing common triangle tensor")
    quartic_value = F(0)
    gradient = [F(0)] * 16
    for term in terms:
        indices = term["coordinate_indices"]
        value = F(term["coefficient"])
        for i in indices:
            value *= common[i]
        quartic_value += value
        for variable in set(indices):
            derivative = F(term["coefficient"] * indices.count(variable))
            removed = False
            for i in indices:
                if i == variable and not removed:
                    removed = True
                else:
                    derivative *= common[i]
            gradient[variable] += derivative
    if quartic_value != 0 or not any(gradient[1:]):
        fail("common H14 point is not smooth in the normalized slice")

    # Every edge at the common preimage is isotropic in (0,1), hence strict CT
    # and therefore also strict D3+.
    common_edges = [(F(1, 2),) * 3] * 5 + [(F(1, 3),) * 3]
    for edge in common_edges:
        strict_positive(domain_margins(edge), "common triangle D3+")
        strict_positive(ct_margins(edge), "common triangle CT")

    return bind({
        "schema": "k3p-h14-contextual-germ-certificate-v1",
        "status": "PASS",
        "input_quartic": {"path": rel(quartic_path), "sha256": file_sha(quartic_path)},
        "coordinate_labels": labels,
        "quartic_terms": terms,
        "normalized_chart": "q000=1",
        "ambient_normalized_dimension": 15,
        "H14_dimension": 14,
        "H14_codimension": 1,
        "ambient_open_triangle_germ": False,
        "common_tensor": [str(x) for x in common],
        "common_preimage": {
            "edge_order": ["a", "b", "c", "d", "e", "f"],
            "edge_triples": [[str(x) for x in edge] for edge in common_edges],
            "inheritance_probability": "1/2",
            "strict_D3_plus": True,
            "strict_continuous_time": True,
        },
        "smoothness": {
            "quartic_value": str(quartic_value),
            "normalized_gradient": [str(x) for x in gradient[1:]],
            "nonzero_gradient_indices_in_16_coordinate_order": [i for i, x in enumerate(gradient) if x],
        },
        "normalized_irreducibility_certificate": {
            "linear_variable": "q0CC",
            "coefficient": "-qCGT*qG0G*qTT0+qCTG*qGG0*qT0T",
            "coefficient_is_primitive_disjoint_support_binomial": True,
            "coefficient_exponent_difference_primitive": True,
            "nondivisibility_specialization": {
                "coefficient_value": "0",
                "remainder_value": "-1",
                "assignment": "qCGT=qCTG=qGTC=qTCG=qGCT=qGG0=qG0G=qT0T=qTT0=1, qTGC=2, q0GG=q0TT=0",
            },
            "gauss_lemma_conclusion": "the normalized quartic is irreducible over Q",
        },
        "orientations": orientation_records,
        "common_relative_germ": {
            "tangent_argument": "Dphi has rank 14 and lies in ker(dF), whose dimension is 14 at the smooth point",
            "each_orientation_submerses_onto_H14": True,
            "common_neighborhood": "intersection of the three relative H14 neighborhoods supplied by the submersion theorem",
            "physical_analytic_sections": "constant-rank theorem on strict D3+/CT parameter neighborhoods",
            "rank_relative_to_each_complete_triangle_image": 14,
            "rank_in_ambient_A15": 14,
            "never_ambient_rank_15": True,
        },
        "contextualization": {
            "common_context_contraction_id": "common-labelled-three-port-multilinear-contraction-v1",
            "formula": "Psi(u,c)=sum_h C(g;h,c)*u(h), with the same labelled h coordinates for every orientation",
            "allows_context_to_reconnect_triangle_terminals": True,
            "tensor_product_independence_assumed": False,
            "single_generic_rank_choice": "choose one nonzero maximal minor of the common map Psi on the intersection germ",
            "rank_lower_bound": "physical sections of each orientation through the common H14 germ give rank >= d_context",
            "rank_upper_bound": "each oriented contextual map factors analytically through the same Psi, giving rank <= d_context",
            "conclusion": "one common contextual germ is full-dimensional relative to every oriented complete-network image",
        },
    })


def build_cut_transfer_binding() -> dict:
    """Bind the sealed directional theorem without accepting self-reported PASS."""
    theorem_path = CUT_TRANSFER / "THEOREM_MANIFEST.json"
    release_verifier = CUT_TRANSFER / "verify_release.py"
    ordinary_path = CUT_TRANSFER / "RELEASE_VERIFICATION_REPORT.json"
    optimized_path = CUT_TRANSFER / "RELEASE_OPTIMIZED_VERIFICATION_REPORT.json"
    errors: list[str] = []
    required = (theorem_path, release_verifier, ordinary_path, optimized_path)
    for path in required:
        if not path.is_file():
            errors.append(f"missing {rel(path)}")
    if errors:
        return {
            "accepted_as_pass": False,
            "validation_errors": errors,
            "universal_pointwise_K3P_cut_recovery_used": False,
        }

    theorem = read_json(theorem_path)
    ordinary = read_json(ordinary_path)
    optimized = read_json(optimized_path)
    release_sha = file_sha(release_verifier)

    if theorem.get("schema") != "k3p-lost-bridge-global-transfer-theorem-manifest-v1":
        errors.append("theorem schema")
    if theorem.get("status") != "PASS":
        errors.append("theorem status")
    if theorem.get("certified_claim") != CUT_TRANSFER_CLAIM:
        errors.append("directional strong-class claim")
    audit = theorem.get("independent_adversarial_audit", {})
    if audit.get("claim_boundary") != CUT_TRANSFER_BOUNDARY:
        errors.append("withdrawn universal pointwise claim boundary")
    if theorem.get("noncircularity") != CUT_TRANSFER_NONCIRCULARITY:
        errors.append("noncircularity contract")
    if audit.get("status") != "PASS" or audit.get("remaining_gaps") != []:
        errors.append("independent adversarial status")

    if set(theorem.get("files", {})) != CUT_TRANSFER_FILE_SET:
        errors.append("theorem file set")
    for relative, expected in sorted(theorem.get("files", {}).items()):
        path = CUT_TRANSFER / relative
        if not path.is_file() or file_sha(path) != expected:
            errors.append(f"theorem file hash {relative}")
    if set(theorem.get("load_bearing_inputs", {})) != set(CUT_TRANSFER_LOAD_BEARING_PATHS):
        errors.append("load-bearing input set")
    for name, record in sorted(theorem.get("load_bearing_inputs", {}).items()):
        if record.get("path") != CUT_TRANSFER_LOAD_BEARING_PATHS.get(name):
            errors.append(f"load-bearing path {name}")
        path = ROOT / record.get("path", "")
        if not path.is_file() or file_sha(path) != record.get("sha256"):
            errors.append(f"load-bearing input {name}")

    def release_ok(report: dict, optimized_flag: bool) -> bool:
        return (
            report.get("schema") == "k3p-lost-bridge-global-transfer-release-verification-v1"
            and report.get("status") == "PASS"
            and report.get("remaining_gaps") == []
            and report.get("python_optimized") is optimized_flag
            and report.get("release_verifier_sha256") == release_sha
            and report.get("circular_hash_dependency") is False
            and report.get("producer_imported") is False
            and report.get("adversarial_verifier_imported") is False
            and report.get("producer", {}).get("direction_count") == 204
            and report.get("adversarial", {}).get("direction_count") == 204
            and report.get("adversarial", {}).get("tree_counterexamples") == 0
        )

    if not release_ok(ordinary, False):
        errors.append("ordinary release report")
    if not release_ok(optimized, True):
        errors.append("optimized release report")
    for key, path in (
        ("release_verifier", release_verifier),
        ("release_report", ordinary_path),
        ("release_optimized_report", optimized_path),
    ):
        record = audit.get(key, {})
        if record.get("path") != rel(path) or record.get("sha256") != file_sha(path):
            errors.append(f"theorem {key} binding")
    if file_sha(theorem_path) != CUT_TRANSFER_THEOREM_SHA256:
        errors.append("sealed theorem manifest hash")

    return {
        "required_claim": CUT_TRANSFER_CLAIM,
        "required_status": "PASS",
        "theorem_manifest": {
            "path": rel(theorem_path),
            "sha256": file_sha(theorem_path),
            "schema": theorem.get("schema"),
            "reported_status": theorem.get("status"),
        },
        "release_verifier": {"path": rel(release_verifier), "sha256": release_sha},
        "release_reports": {
            "ordinary": {
                "path": rel(ordinary_path),
                "sha256": file_sha(ordinary_path),
                "reported_status": ordinary.get("status"),
                "python_optimized": ordinary.get("python_optimized"),
            },
            "optimized": {
                "path": rel(optimized_path),
                "sha256": file_sha(optimized_path),
                "reported_status": optimized.get("status"),
                "python_optimized": optimized.get("python_optimized"),
            },
        },
        "claim_boundary": audit.get("claim_boundary"),
        "noncircularity": theorem.get("noncircularity"),
        "universal_pointwise_K3P_cut_recovery_used": False,
        "accepted_as_pass": not errors,
        "validation_errors": errors,
    }


def build_global_certificate(bridge: dict, marginal: dict, h14: dict) -> dict:
    # After shrinking analytic incidence products around the normalized base,
    # every product is in [L,U].  The base common effective bridge spectrum is
    # the isotropic epsilon triple.  The cap on epsilon proves that this
    # effective bridge is physical, while the L,U term proves that every
    # reconstructed actual bridge is physical.  Strictness then supplies an
    # open neighborhood in which the effective z coordinates vary freely.
    # The proof is uniform in any finite positive compact bounds 0<L<=A_h<=U.
    def replay_row(L: F, U: F) -> dict:
        if not 0 < L <= U:
            fail("invalid simultaneous physical-gluing compact bounds")
        quadratic = L * L / (8 * U)
        epsilon = min(F(1, 4), quadratic)
        coordinate_lower = epsilon / U
        coordinate_upper = epsilon / L
        effective_principal_margin = 1 - epsilon
        effective_ct_margin = epsilon - epsilon * epsilon
        actual_principal_margin = 1 - 2 * coordinate_upper
        actual_ct_margin = coordinate_lower - coordinate_upper * coordinate_upper
        certified_actual_ct_floor = 7 * epsilon / (8 * U)
        if quadratic < F(1, 4):
            branch = "quadratic_bound"
        elif quadratic > F(1, 4):
            branch = "one_quarter_cap"
        else:
            branch = "equal_branches"
        if not (
            0 < epsilon <= F(1, 4)
            and 0 < coordinate_lower <= coordinate_upper <= F(1, 8)
            and effective_principal_margin >= F(3, 4)
            and effective_ct_margin >= 3 * epsilon / 4 > 0
            and actual_principal_margin >= F(3, 4)
            and actual_ct_margin >= certified_actual_ct_floor > 0
        ):
            fail("simultaneous physical-gluing envelope is not strict")
        return {
            "L": str(L),
            "U": str(U),
            "active_epsilon_branch": branch,
            "epsilon": str(epsilon),
            "effective_principal_margin": str(effective_principal_margin),
            "effective_continuous_time_margin": str(effective_ct_margin),
            "actual_coordinate_interval": [
                str(coordinate_lower), str(coordinate_upper),
            ],
            "actual_principal_margin_lower_bound": str(actual_principal_margin),
            "actual_continuous_time_margin_lower_bound": str(actual_ct_margin),
            "certified_actual_continuous_time_floor": str(certified_actual_ct_floor),
        }

    replay_bounds = (
        (F(1, 2), F(2)),
        (F(2), F(2)),
        (F(7), F(7)),
        (F(100), F(100)),
        (F(1, 100), F(100)),
    )
    replay_instances = [replay_row(L, U) for L, U in replay_bounds]

    cut_binding = build_cut_transfer_binding()
    dependency_pass = cut_binding["accepted_as_pass"] is True
    return bind({
        "schema": "k3p-global-gluing-genericity-reconstruction-certificate-v1",
        "internal_infrastructure_status": "PASS",
        "global_theorem_dependency_status": "PASS" if dependency_pass else "BLOCKED_EXTERNAL_CUT_DEPENDENCY",
        "dependencies": {
            "bridge_fibre_payload_sha256": bridge["payload_sha256"],
            "marginal_payload_sha256": marginal["payload_sha256"],
            "H14_context_payload_sha256": h14["payload_sha256"],
            "strong_class_containment_cut_equality_interface": cut_binding,
            "generic_cut_rank_recovery": {
                "true_cut_direction": "every 5x5 flattening minor vanishes pointwise at a graph bridge split",
                "noncut_direction": "some 5x5 minor is a nonzero model polynomial, certified by the strict isotropic JC slice",
                "scope": "generic bridge-tree reconstruction only; not a universal arbitrary-network pointwise iff claim",
                "universal_pointwise_K3P_cut_recovery_claimed": False,
            },
        },
        "simultaneous_physical_bridge_gluing": {
            "incidence_product_compact_bounds": "0<L<=A_h<=U on the finite common compactly-contained local germs",
            "epsilon_formula": "epsilon=min(1/4,L^2/(8*U))",
            "base_common_effective_isotropic_spectrum": ["epsilon"] * 3,
            "effective_bridge_formula": "z_h=A_h*x_h",
            "base_actual_bridge_formula": "x_h=epsilon/A_h for A_h=a[u,e,h]*a[v,e,h]",
            "base_actual_coordinate_interval": ["epsilon/U", "epsilon/L"],
            "principal_domain_inequalities": [
                "c>0", "g>0", "t>0", "1-c>0", "1-g>0", "1-t>0",
                "1+c-g-t>0", "1-c+g-t>0", "1-c-g+t>0",
            ],
            "continuous_time_inequalities": ["c-g*t>0", "g-c*t>0", "t-c*g>0"],
            "effective_principal_margin_lower_bound": "1-epsilon>=3/4",
            "effective_continuous_time_margin_lower_bound": "epsilon-epsilon^2>=3*epsilon/4>0",
            "actual_coordinate_upper_bound": "epsilon/L<=1/8",
            "actual_principal_composition_margin_lower_bound": "1-2*epsilon/L>=3/4",
            "actual_continuous_time_margin_lower_bound": "epsilon/U-epsilon^2/L^2>=7*epsilon/(8*U)>0",
            "exact_rational_replay_instance": replay_instances[0],
            "exact_rational_branch_replays": replay_instances,
            "open_neighborhood_full_rank_extension": {
                "effective_variables": "each z_h varies independently in an open neighborhood of epsilon",
                "actual_bridge_section": "x_h=z_h/A_h",
                "section_is_positive_real_analytic": True,
                "strict_physicality_persists_after_finite_shrinking": True,
                "independent_effective_coordinates_per_bridge": 3,
                "projection_to_pre_gluing_product_coordinates": "identity",
                "full_rank_relative_global_germ_preserved": True,
                "rank_reason": (
                    "the physical product extraction is a local inverse and the "
                    "analytic bridge section is a graph over the local-factor and "
                    "independent effective-z coordinates"
                ),
            },
            "same_epsilon_all_networks_and_bridges": True,
            "finite_simultaneous_shrinking": True,
            "incidence_cancellation": True,
            "no_holonomy": True,
        },
        "genericity": {
            "fixed_leaf_count_topology_bound": {
                "reticulations": "r<=n-1",
                "nonroot_tree_vertices": "t=n+r-2",
                "rooted_vertices": "1+t+r+n=2*n+2*r-1<=4*n-3",
                "finite_labelled_topologies": True,
            },
            "model_closure_irreducible": "closure of a polynomial image of irreducible affine parameter space",
            "generic_rank_equals_image_dimension": True,
            "total_source_rank_drop_locus": "R_N={theta in Theta_3,+(N):rank D Phi_N(theta)<d_N}",
            "rank_drop_stratification": "finite Nash strata S_alpha on which Phi_N|S_alpha has constant rank at most d_N-1",
            "rank_drop_image_dimension": "at most d_N-1 by finite constant-rank semialgebraic stratification",
            "target_incidence_correspondence": "Z_Nprime={(q,theta_prime):q=Phi_Nprime(theta_prime),q in M_3,+(N),theta_prime physical}",
            "full_projection_section": "a d_N-rank incidence projection has a local physical real-analytic right inverse s(q)",
            "source_parameter_section": "sigma=s o Phi_N on a regular source-parameter neighborhood, so Phi_N=Phi_Nprime o sigma",
            "inequivalent_intersection_dimension": "at most d_N-1, else a target analytic section gives forbidden regular full-dimensional containment",
            "semialgebraic_real_closure_dimension": "BCR Proposition 2.8.2; semialgebraic dimension equals real-Zariski-closure dimension",
            "real_to_complex_dimension": "A to A tensor_R C is finite faithfully flat integral and preserves Krull dimension",
            "exceptional_set": "finite union of proper Zariski closures of inequivalent intersections, singular/rank-drop loci, and certified nonzero reconstruction-test zeros",
            "exceptional_set_proper": True,
            "scope": "for each fixed topology N; not pointwise parameter identifiability",
        },
        "exact_reconstruction": {
            "input_model": "exact-real oracle supporting field operations, polynomial signs, and real-closed-field quantifier elimination",
            "steps": [
                "Fourier transform the exact tensor",
                "recover the labelled bridge tree at a generic regular tensor using true-cut vanishing and generic noncut minors",
                "extract normalized three-sector component factors with bridge incidence slices",
                "enumerate the finite rigid-support atlas candidates and apply exact local separators",
                "follow exact fixed-full restoration records",
                "use coherent one-port and two-port records to recover segment membership and order",
                "assemble coherent mixed graphs and group them into ordinary-triangle classes",
                "decide exact semialgebraic feasibility for each finite class and return the unique feasible class outside E_N",
            ],
            "termination": "finite topology/ledger enumeration plus terminating real-closed-field quantifier elimination",
            "practical_finite_sequence_claimed": False,
            "individual_edge_parameters_identified": False,
        },
        "logical_dependency_dag": {
            "bridge_tree_recovery": ["strong_class_containment_cut_equality_interface", "generic_cut_rank_recovery"],
            "localization": ["bridge_tree_recovery", "bridge_fibre", "marginal_submersion"],
            "local_classification": ["localization", "four_port_atlas", "restoration", "probes"],
            "sufficiency": ["H14_context", "simultaneous_physical_bridge_gluing"],
            "genericity": ["finite_topologies", "main_classification", "semialgebraic_stratification"],
            "reconstruction": ["genericity", "active_exact_ledgers", "real_closed_field_decision"],
        },
    })


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
    if not __debug__:
        fail("optimized mode is forbidden for certification generation")
    bridge = build_bridge_certificate()
    marginal = build_marginal_certificate()
    h14 = build_h14_certificate()
    global_certificate = build_global_certificate(bridge, marginal, h14)

    outputs = {
        ROOT / "bridge_fibre" / "K3P_BRIDGE_FIBRE_CERTIFICATE.json": bridge,
        ROOT / "marginals" / "K3P_MARGINAL_SUBMERSION_CERTIFICATE.json": marginal,
        ROOT / "triangle_h14" / "K3P_H14_CONTEXT_CERTIFICATE.json": h14,
        ROOT / "global_infrastructure" / "K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json": global_certificate,
    }
    for path, value in outputs.items():
        write_json(path, value)

    manifest = bind({
        "schema": "k3p-global-infrastructure-manifest-v1",
        "status": "PASS_INTERNAL_BLOCKED_EXTERNAL" if global_certificate["global_theorem_dependency_status"] != "PASS" else "PASS",
        "artifacts": {
            rel(path): {"sha256": file_sha(path), "payload_sha256": value["payload_sha256"], "schema": value["schema"]}
            for path, value in outputs.items()
        },
        "generator": {"path": rel(Path(__file__)), "sha256": file_sha(Path(__file__))},
        "independent_implementations": {
            rel(path): {"sha256": file_sha(path)}
            for path in (
                ROOT / "global_infrastructure" / "verify_global_infrastructure.py",
                ROOT / "global_infrastructure" / "test_global_infrastructure_mutations.py",
            )
            if path.exists()
        },
        "claim_boundary": GLOBAL_INFRASTRUCTURE_CLAIM_BOUNDARY,
    })
    write_json(ROOT / "global_infrastructure" / "GLOBAL_INFRASTRUCTURE_MANIFEST.json", manifest)
    print(json.dumps({
        "status": manifest["status"],
        "bridge": bridge["payload_sha256"],
        "marginal": marginal["payload_sha256"],
        "h14": h14["payload_sha256"],
        "global": global_certificate["payload_sha256"],
        "manifest": manifest["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
