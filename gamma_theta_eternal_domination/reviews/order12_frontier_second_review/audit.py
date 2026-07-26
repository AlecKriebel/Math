#!/usr/bin/env python3
"""Independent, solver-free audit of the frozen order-12 frontier note."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
import math
from pathlib import Path
import subprocess
import tempfile


CAMPAIGN = Path(__file__).resolve().parents[2]

TARGET = "math/lemmas/order12_frontier.md"
TARGET_SHA256 = "adb27204d33feb47933f2a4b1e381485b2e1b80c22b56a67b18586c4933c2b75"

EXPECTED_FILES = {
    TARGET: TARGET_SHA256,
    "instances/order12_k4_connected_parent/instance.cnf":
        "adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac",
    "instances/order12_k4_connected_doublelex/instance.cnf":
        "14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7",
    "certificates/order12_k4_doublelex_seed0_lrat/proof/"
    "proof.normalized.rup.bdrat":
        "2741335a5ed9af769f0db4bd0c03a70e414d0568681d5b8261a5667ed30b6686",
    "certificates/order12_k4_doublelex_seed0_lrat/proof/"
    "proof.converted.lrat":
        "0e04eb639a3f7f7d335126d56040abb4ef11e8548770262c316a608390659263",
    "reviews/order12_k4_doublelex_lrat_hostile_0814a4f4/REVIEW.md":
        "fb95934b5d5acd75c9f6deb9142be3b903900f5abd02a5cc21d9884788f38395",
    "reviews/order12_k4_doublelex_lrat_hostile_0814a4f4/"
    "hostile-evidence.json":
        "2651f9d286582c068fb872acf862b82c4d4ab8e5fc07f6b99825b9335dd40b63",
    "math/lemmas/order12_k4_synthesis_target.md":
        "5421357c5095113ac598afa22fa5a4e3623ef19d3c3a7a348b6c6c9a29945671",
    "reviews/order12_k4_synthesis_target_hostile_review.md":
        "119b9038b160cf9e85f56056578a3b33decf08c83cd40df071e89f35be1fea35",
    "math/lemmas/order12_k4_doublelex.md":
        "d5be9b6373d7aa7c49dec32c18c6202698b35fe05a1f58b2b97dcc98d9114a76",
    "reviews/order12_k4_doublelex_hostile_review.md":
        "4cf3c5012a8b0ecfdcbad82c0fd2c283c2aebbd3396eaba9b232902956f86d8f",
    "reviews/order12_k4_doublelex_conditional_implication_audit/REVIEW.md":
        "6768b18569877b0e83c70ba1dea2c2caf332ee69c1477b2eca635f2d3f69925d",
    "math/lemmas/order12_k3_exclusion.md":
        "b6010d6f365a62845e24666603f6417d87f14c37876e3406dc2a7c6b6ee91ae4",
    "results/order12_k3_exclusion_acceptance.json":
        "f6224392eed348519ab898eaccfe96d223f874b280165cc49d48d3f587dbf2a3",
    "reviews/order12_k3_exclusion_hostile_review.md":
        "ed4df8f2f0ec52198fda5240c0ef98c39184e58a3b62e6b97caa093e2640b3bd",
    "reviews/order12_k3_exclusion_second_review.md":
        "48fbe860d7ce2f22a28bd61fc95c27114662115bf37dfd656d9aec560b72050f",
    "math/reductions.md":
        "d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13",
    "reviews/reductions_hostile_review.md":
        "6798b33ad14adc660b69792ee74ed31be4afeb5c2bab4659b29d7b650090c159",
    "math/lemmas/half_order_exclusion.md":
        "5d5e054305d97bf8e40f84073abd5236c6d726d66205b5e309ccfe39dd7d5f50",
    "reviews/half_order_exclusion_hostile_review.md":
        "41d76e6d5295db5924d3bc2b0181ac42519c4592fa6b071dbdd8c28c817b5aa2",
    "math/lemmas/simplicial_neighborhood_reduction.md":
        "87cdebc4177bf7703a53892f84d436c0a52eb5444a6b0ac14663284c0351b25a",
    "reviews/simplicial_neighborhood_reduction_hostile/REVIEW.md":
        "2c8553a28affd20ce44cedb1f860e218b1f6c175f5aec7cb8bb0c8bccb7ac821",
    "math/lemmas/leaf_support_reduction.md":
        "802907a01c27043dfa1348a1c8e97e142769238cb62c9064e946573dfba93517",
    "reviews/leaf_support_reduction_hostile/REVIEW.md":
        "8966eae9933cd1f952295a11004d00fc73d8f7f30eee003a2e3f53513008728c",
    "literature/sources/mmv2022.pdf":
        "e1a5c6bb4fb4767c3d91a5e848872d26d97d3f0df284142a1b885ad720a20edf",
    "literature/sources/mmv2022_src/EternalDomination.tex":
        "e77618dcf06b4e65d6b622e993eed4307238de49d4f395da920044bb6dfd9a45",
    "literature/sources/henning_schiermeyer_yeo_2011_p12.pdf":
        "418199b3a9f9c92974046a6c92b0b11b24cdec51e034f5aa23168c4bdfbb4285",
    "literature/status.md":
        "61ae2e2a67991bef928894a09ee452196d2834035934456b262cc983f75ba9c4",
}


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> object:
    def unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
        output: dict[str, object] = {}
        for key, value in pairs:
            if key in output:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            output[key] = value
        return output

    return json.loads(path.read_text(), object_pairs_hook=unique_pairs)


def parse_dimacs(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    if not payload.endswith(b"\n"):
        raise ValueError(f"{path} has no final newline")
    lines = payload.decode("ascii").splitlines()
    header = lines[0].split()
    if len(header) != 4 or header[:2] != ["p", "cnf"]:
        raise ValueError(f"bad DIMACS header in {path}")
    variables, declared_clauses = map(int, header[2:])
    literal_count = 0
    maximum_variable = 0
    for number, line in enumerate(lines[1:], start=2):
        tokens = [int(token) for token in line.split()]
        if not tokens or tokens[-1] != 0 or 0 in tokens[:-1]:
            raise ValueError(f"bad clause terminator at {path}:{number}")
        clause = tokens[:-1]
        if not clause:
            raise ValueError(f"input formula contains empty clause at {path}:{number}")
        literal_count += len(clause)
        maximum_variable = max(maximum_variable, *(abs(x) for x in clause))
    if len(lines) - 1 != declared_clauses:
        raise ValueError(f"declared/actual clause mismatch in {path}")
    if maximum_variable > variables:
        raise ValueError(f"variable bound exceeded in {path}")
    return {
        "bytes": len(payload),
        "sha256": sha256(payload).hexdigest(),
        "variables": variables,
        "clauses": declared_clauses,
        "literals": literal_count,
        "maximum_variable": maximum_variable,
    }


def independent_doublelex_suffix() -> bytes:
    edge = {
        pair: index
        for index, pair in enumerate(combinations(range(12), 2), start=1)
    }
    clauses: list[tuple[int, ...]] = []
    for left_anchor, right_anchor in ((0, 1), (1, 2), (2, 3)):
        for first_difference in range(8):
            for prefix in product((0, 1), repeat=first_difference):
                literals: list[int] = []
                for coordinate, bit in enumerate(prefix):
                    outer = coordinate + 4
                    left = edge[(left_anchor, outer)]
                    right = edge[(right_anchor, outer)]
                    literals.extend((left, right) if bit == 0 else (-left, -right))
                outer = first_difference + 4
                literals.extend(
                    (-edge[(left_anchor, outer)], edge[(right_anchor, outer)])
                )
                clauses.append(tuple(literals))
    if len(clauses) != 765 or sum(map(len, clauses)) != 10_758:
        raise AssertionError("independent DoubleLex census is wrong")
    return b"".join(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in clauses
    )


def audit_doublelex_binding() -> dict[str, object]:
    parent_path = CAMPAIGN / "instances/order12_k4_connected_parent/instance.cnf"
    doublelex_path = (
        CAMPAIGN / "instances/order12_k4_connected_doublelex/instance.cnf"
    )
    parent = parent_path.read_bytes()
    doublelex = doublelex_path.read_bytes()
    parent_lines = parent.splitlines(keepends=True)
    doublelex_lines = doublelex.splitlines(keepends=True)
    if parent_lines[1:] != doublelex_lines[1:len(parent_lines)]:
        raise ValueError("DoubleLex body does not have exact parent body prefix")
    actual_suffix = b"".join(doublelex_lines[len(parent_lines):])
    expected_suffix = independent_doublelex_suffix()
    if actual_suffix != expected_suffix:
        raise ValueError("DoubleLex suffix differs from independent reconstruction")
    return {
        "parent_body_is_exact_prefix": True,
        "suffix_byte_identical_to_independent_reconstruction": True,
        "suffix_bytes": len(actual_suffix),
        "suffix_clauses": len(actual_suffix.splitlines()),
        "suffix_literals": sum(
            len(line.split()) - 1 for line in actual_suffix.decode("ascii").splitlines()
        ),
        "suffix_sha256": sha256(actual_suffix).hexdigest(),
    }


def run_json_probe(relative_path: str) -> dict[str, object]:
    completed = subprocess.run(
        ["python3", relative_path],
        cwd=CAMPAIGN,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if completed.returncode != 0 or completed.stderr:
        raise RuntimeError(
            f"probe failed: {relative_path}; rc={completed.returncode}; "
            f"stderr={completed.stderr!r}"
        )
    parsed = json.loads(completed.stdout)
    return {
        "returncode": completed.returncode,
        "status": parsed.get("status") or parsed.get("verdict"),
        "solver_invoked": parsed.get("solver_invoked", False),
        "output_sha256": parsed.get("output_sha256")
        or parsed.get("modes", {}).get("full", {}).get("sha256"),
        "clean_room_byte_equal": parsed.get(
            "permanent_instance", {}
        ).get("clean_room_byte_equal"),
        "all_move_attacks_unoccupied": parsed.get(
            "all_move_attacks_unoccupied"
        ),
        "mutation_kills": parsed.get("mutation_kills"),
    }


def audit_certificate() -> dict[str, object]:
    certificate_path = (
        CAMPAIGN / "certificates/order12_k4_doublelex_seed0_lrat/certificate.json"
    )
    certificate = load_json(certificate_path)
    assert isinstance(certificate, dict)
    expected_records = {
        "formula": EXPECTED_FILES[
            "instances/order12_k4_connected_doublelex/instance.cnf"
        ],
        "normalized_binary_rup": EXPECTED_FILES[
            "certificates/order12_k4_doublelex_seed0_lrat/proof/"
            "proof.normalized.rup.bdrat"
        ],
        "converted_lrat": EXPECTED_FILES[
            "certificates/order12_k4_doublelex_seed0_lrat/proof/"
            "proof.converted.lrat"
        ],
    }
    record_checks: dict[str, object] = {}
    for key, expected_hash in expected_records.items():
        record = certificate[key]
        assert isinstance(record, dict)
        actual_path = Path(str(record["path"]))
        if not actual_path.is_absolute():
            actual_path = CAMPAIGN / actual_path
        actual_hash = file_sha256(actual_path)
        actual_size = actual_path.stat().st_size
        if actual_hash != expected_hash or record["sha256"] != expected_hash:
            raise ValueError(f"certificate hash mismatch for {key}")
        if record["size_bytes"] != actual_size:
            raise ValueError(f"certificate size mismatch for {key}")
        record_checks[key] = {
            "sha256": actual_hash,
            "bytes": actual_size,
            "certificate_binding_matches": True,
        }

    phases = certificate["phase_resources"]
    assert isinstance(phases, dict)
    phase_checks: dict[str, object] = {}
    for name in (
        "normalizer",
        "normalized_forward_rup",
        "backward_lrat_conversion_rup",
        "lrat_check",
    ):
        phase = phases[name]
        assert isinstance(phase, dict)
        child = phase["child"]
        assert isinstance(child, dict)
        if not phase["passed"] or child["exit_code"] != 0:
            raise ValueError(f"certificate phase failed: {name}")
        stderr_path = Path(str(child["stderr_path"]))
        stdout_path = Path(str(child["stdout_path"]))
        if stderr_path.stat().st_size != 0:
            raise ValueError(f"nonempty certificate stderr: {name}")
        stdout = stdout_path.read_text()
        if name == "normalizer":
            marker = "s NORMALIZED"
        elif name == "lrat_check":
            marker = "c VERIFIED"
        else:
            marker = "s VERIFIED"
            if "0 RAT lemmas" not in stdout:
                raise ValueError(f"RAT count not zero: {name}")
        if marker not in stdout:
            raise ValueError(f"missing verification marker: {name}")
        phase_checks[name] = {
            "passed": True,
            "exit_code": 0,
            "stderr_empty": True,
            "verification_marker": marker,
            "zero_rat_lemmas": (
                True
                if name in ("normalized_forward_rup", "backward_lrat_conversion_rup")
                else None
            ),
        }

    evidence = load_json(
        CAMPAIGN
        / "reviews/order12_k4_doublelex_lrat_hostile_0814a4f4/"
        "hostile-evidence.json"
    )
    assert isinstance(evidence, dict)
    if evidence["verdict"] != "ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_ONLY":
        raise ValueError("unexpected exact-CNF hostile verdict")
    if (
        evidence["transfer_to_graph_exclusion"]
        != "OUT_OF_SCOPE_SEPARATE_AUDIT_REQUIRED"
    ):
        raise ValueError("hostile evidence improperly claims graph transfer")

    return {
        "certificate_status": certificate["status"],
        "claim_boundary": certificate["claim_boundary"],
        "dimacs_census": certificate["dimacs_census"],
        "records": record_checks,
        "phase_transcripts": phase_checks,
        "independent_hostile_verdict": evidence["verdict"],
        "hostile_scope_transfer_to_graph_exclusion": evidence[
            "transfer_to_graph_exclusion"
        ],
    }


def fresh_lrat_replay() -> dict[str, object]:
    checker = CAMPAIGN / "tools/drat_trim_2023_05_22/lrat-check"
    formula = CAMPAIGN / "instances/order12_k4_connected_doublelex/instance.cnf"
    lrat = (
        CAMPAIGN
        / "certificates/order12_k4_doublelex_seed0_lrat/proof/"
        "proof.converted.lrat"
    )
    completed = subprocess.run(
        [str(checker), str(formula), str(lrat)],
        cwd=CAMPAIGN,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    lines = [
        line
        for line in completed.stdout.splitlines()
        if line and not line.startswith("c verification time =")
    ]
    if (
        completed.returncode != 0
        or completed.stderr
        or lines.count("c VERIFIED") != 1
    ):
        raise RuntimeError(
            "fresh LRAT replay failed: "
            f"rc={completed.returncode}, stderr={completed.stderr!r}, lines={lines!r}"
        )
    return {
        "checker_sha256": file_sha256(checker),
        "exit_code": completed.returncode,
        "stderr_empty": completed.stderr == "",
        "verified_marker_count": lines.count("c VERIFIED"),
        "stdout_lines": lines,
        "solver_invoked": False,
    }


def extract_pdf_text(path: Path) -> str:
    with tempfile.TemporaryDirectory(prefix="order12-frontier-citation-") as temp:
        destination = Path(temp) / "source.txt"
        completed = subprocess.run(
            [
                "gs",
                "-q",
                "-dNOPAUSE",
                "-dBATCH",
                "-sDEVICE=txtwrite",
                f"-sOutputFile={destination}",
                str(path),
            ],
            check=False,
            capture_output=True,
            timeout=60,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"Ghostscript extraction failed for {path}")
        return destination.read_bytes().decode("utf-8", errors="replace")


def audit_literature() -> dict[str, object]:
    mmv_tex = (
        CAMPAIGN / "literature/sources/mmv2022_src/EternalDomination.tex"
    ).read_text()
    mmv_checks = {
        "one_guard_unoccupied_attack_definition": (
            "the attacker selects a vertex $v$ on which there is no guard"
            in mmv_tex
            and "moving a guard on a neighbour of $v$ to $v$" in mmv_tex
        ),
        "observation_5_6_source_statement": (
            "Our computer search yields the following observation." in mmv_tex
            and "There are no counterexample to the $\\gamma-\\theta$ "
            "conjecture of order $n \\leq 11$." in mmv_tex
        ),
        "table7_orders_10_11_present": (
            "11716571" in mmv_tex and "1006700565" in mmv_tex
        ),
        "56_55_0_summary_present": (
            "We found $56$ graphs" in mmv_tex
            and "$55$ graphs with $\\alpha=\\gamma^\\infty<\\theta$" in mmv_tex
            and "none with $\\gamma=\\gamma^\\infty<\\theta$" in mmv_tex
        ),
    }
    if not all(mmv_checks.values()):
        raise ValueError(f"MMV source check failed: {mmv_checks}")

    hsy_text = extract_pdf_text(
        CAMPAIGN / "literature/sources/henning_schiermeyer_yeo_2011_p12.pdf"
    )
    hsy_checks = {
        "mccuaig_shepherd_theorem_attribution": (
            "Theorem 1 (McCuaig and Shepherd [12])" in hsy_text
        ),
        "seven_exception_scope": (
            "except for seven exceptional" in hsy_text
            and "F4 ∪ F7" in hsy_text
        ),
        "one_order4_exception": "F4 = {C4}" in hsy_text,
        "six_order7_exceptions": "The six graphs in the family F7" in hsy_text,
        "two_fifths_bound": "γ(G) ≤ 2n/5" in hsy_text,
    }
    if not all(hsy_checks.values()):
        raise ValueError(f"HSY source check failed: {hsy_checks}")

    target_text = (CAMPAIGN / TARGET).read_text()
    boundary_checks = {
        "published_lower_order_premise_named": (
            "through-order-\\(11\\) premise is the published exhaustive "
            "computation" in target_text
        ),
        "campaign_limit_through_order9_named": (
            "independently\n"
            "enumerates all connected graphs only through order \\(9\\)"
            in target_text
        ),
        "orders10_11_not_campaign_reproduced": (
            "has not\n"
            "reproduced the original all-graph coverage at orders \\(10\\) "
            "and \\(11\\)" in target_text
        ),
        "not_campaign_only_frontier": (
            "not a campaign-only proof-certificate enumeration through "
            "order \\(12\\)" in target_text
        ),
        "final_conditional_reporting_language": (
            "explicitly conditional on the published lower-order computation"
            in target_text
        ),
    }
    if not all(boundary_checks.values()):
        raise ValueError(f"published/campaign boundary check failed: {boundary_checks}")

    return {
        "mmv2022_official_pdf_sha256": EXPECTED_FILES[
            "literature/sources/mmv2022.pdf"
        ],
        "mmv2022_official_tex_checks": mmv_checks,
        "henning_schiermeyer_yeo_official_pdf_sha256": EXPECTED_FILES[
            "literature/sources/henning_schiermeyer_yeo_2011_p12.pdf"
        ],
        "henning_schiermeyer_yeo_text_checks": hsy_checks,
        "published_vs_campaign_boundary_checks": boundary_checks,
    }


def audit_case_coverage() -> dict[str, object]:
    acceptance = load_json(
        CAMPAIGN / "results/order12_k3_exclusion_acceptance.json"
    )
    assert isinstance(acceptance, dict)
    complete = acceptance["complete_slice_proof"]
    assert isinstance(complete, dict)
    if (
        acceptance["claim_id"] != "C-035"
        or acceptance["verdict"]
        != "ACCEPT_CERTIFIED_FINITE_ORDER12_PARAMETER3_EXCLUSION"
        or complete["disconnected_case_explicitly_covered"] is not True
        or complete["first_review_verdict"]
        != "ACCEPT_COMPLETE_ORDER12_K3_EXCLUSION"
        or complete["second_review_verdict"] != "ACCEPT_NO_BLOCKER"
    ):
        raise ValueError("C-035 acceptance gate does not match expected scope")

    remaining = [k for k in range(13) if k >= 3 and 12 >= 2 * k + 1]
    if remaining != [3, 4, 5]:
        raise AssertionError(f"wrong order-12 parameter list: {remaining}")
    k5_minimum_order = math.ceil(5 * 5 / 2)
    if k5_minimum_order != 13:
        raise AssertionError("wrong McCuaig-Shepherd k=5 arithmetic")

    reductions = (CAMPAIGN / "math/reductions.md").read_text()
    simplicial = (
        CAMPAIGN / "math/lemmas/simplicial_neighborhood_reduction.md"
    ).read_text()
    half_order = (
        CAMPAIGN / "math/lemmas/half_order_exclusion.md"
    ).read_text()
    logical_source_checks = {
        "component_additivity_and_counterexample_component": (
            "Additivity over components" in reductions
            and "then a connected counterexample\nexists" in reductions
        ),
        "minimum_parameter_k_at_least_3": (
            "**Corollary 11 (minimum parameter).**  Every counterexample has"
            in reductions
            and "\\gamma^\\infty(G)\\geq3" in reductions
        ),
        "minimum_counterexample_connected_no_simplicial_delta2": (
            "Every minimum-order counterexample" in simplicial
            and "is connected and has no simplicial vertex" in simplicial
            and "minimum degree is at least two" in simplicial
        ),
        "connected_half_order_strict": (
            "k<\\frac n2" in half_order and "n\\geq 2k+1" in half_order
        ),
    }
    if not all(logical_source_checks.values()):
        raise ValueError(f"logical dependency text check failed: {logical_source_checks}")

    return {
        "published_no_counterexample_through_11_makes_order12_minimal": True,
        "component_additivity_then_makes_order12_counterexample_connected": True,
        "order12_integral_parameters_after_k_ge_3_and_n_ge_2k_plus_1": remaining,
        "k3": {
            "claim": acceptance["claim"],
            "verdict": acceptance["verdict"],
            "disconnected_case_explicitly_covered": True,
            "branches": complete["exhaustive_connected_template_branches"],
        },
        "k4": {
            "connected_exclusion_from_C037_C045_and_exact_D_UNSAT": True,
            "disconnected_case_handled_by_minimality_and_published_lower_order_premise": True,
        },
        "k5": {
            "minimum_order_from_ceil_5k_over_2": k5_minimum_order,
            "order12_impossible": 12 < k5_minimum_order,
            "dependencies": [
                "minimum counterexample connected",
                "simplicial reduction gives minimum degree at least two",
                "McCuaig-Shepherd with exceptions only at orders 4 and 7",
                "published absence through order 11",
            ],
        },
        "logical_source_checks": logical_source_checks,
        "coverage_complete": True,
    }


def main() -> int:
    target_before = file_sha256(CAMPAIGN / TARGET)
    if target_before != TARGET_SHA256:
        raise ValueError("frozen target hash mismatch before audit")

    file_bindings: dict[str, object] = {}
    for relative, expected in EXPECTED_FILES.items():
        path = CAMPAIGN / relative
        actual = file_sha256(path)
        if actual != expected:
            raise ValueError(
                f"hash mismatch for {relative}: expected {expected}, got {actual}"
            )
        file_bindings[relative] = {
            "sha256": actual,
            "bytes": path.stat().st_size,
            "matches_expected": True,
        }

    parent_census = parse_dimacs(
        CAMPAIGN / "instances/order12_k4_connected_parent/instance.cnf"
    )
    doublelex_census = parse_dimacs(
        CAMPAIGN / "instances/order12_k4_connected_doublelex/instance.cnf"
    )
    if parent_census != {
        "bytes": 3_992_947,
        "sha256": EXPECTED_FILES[
            "instances/order12_k4_connected_parent/instance.cnf"
        ],
        "variables": 18_381,
        "clauses": 114_742,
        "literals": 1_180_016,
        "maximum_variable": 18_381,
    }:
        raise ValueError(f"unexpected parent census: {parent_census}")
    if doublelex_census != {
        "bytes": 4_030_657,
        "sha256": EXPECTED_FILES[
            "instances/order12_k4_connected_doublelex/instance.cnf"
        ],
        "variables": 18_381,
        "clauses": 115_507,
        "literals": 1_190_774,
        "maximum_variable": 18_381,
    }:
        raise ValueError(f"unexpected DoubleLex census: {doublelex_census}")

    evidence = {
        "schema": "gamma-theta-order12-frontier-second-review-evidence-v1",
        "target": {
            "path": TARGET,
            "sha256": target_before,
            "frozen_hash_matches": True,
        },
        "verdict": "ACCEPT_ORDER12_FRONTIER_WITH_EXPLICIT_PUBLISHED_PREMISE",
        "blocking_defects": [],
        "omissions": [],
        "file_bindings": file_bindings,
        "exact_model": {
            "parent_census": parent_census,
            "doublelex_census": doublelex_census,
            "doublelex_binding": audit_doublelex_binding(),
            "constructor_probe": run_json_probe(
                "reviews/order12_k4_synthesis_target_hostile_probe.py"
            ),
            "doublelex_probe": run_json_probe(
                "reviews/order12_k4_doublelex_hostile_probe.py"
            ),
        },
        "exact_unsat_certificate": audit_certificate(),
        "fresh_lrat_replay": fresh_lrat_replay(),
        "literature": audit_literature(),
        "case_coverage": audit_case_coverage(),
        "scope": {
            "proved_through_order": 12,
            "published_lower_order_premise_required": True,
            "campaign_only_all_graph_coverage_through_order12": False,
            "claim_for_order13_or_larger": False,
            "universal_conjecture_resolved": False,
        },
        "solver_invoked": False,
    }

    target_after = file_sha256(CAMPAIGN / TARGET)
    if target_after != target_before:
        raise ValueError("frozen target changed during audit")
    evidence["target"]["unchanged_during_audit"] = True
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
