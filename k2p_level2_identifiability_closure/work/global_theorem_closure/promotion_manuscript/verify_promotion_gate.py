#!/usr/bin/env python3
"""Fail-closed verifier for promotion of the K2P theorem manuscript.

This verifier performs byte-hash checks on the frozen proof inputs and then
requires a completely populated full-probe placeholder.  It deliberately
exits nonzero until the final corrected one-/two-port probe package is frozen.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STRICT_JSON_DIR = ROOT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import StrictJSONError, decode_json_document  # noqa: E402

MANUSCRIPT = HERE / "K2P_SAME_PROMOTION_MANUSCRIPT.md"
PLACEHOLDER = HERE / "PROBE_PROMOTION_PLACEHOLDER.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_ARTIFACTS = {"primary", "independent_replay", "mutation_report"}
EXPECTED_LEDGERS = {
    "one_port",
    "two_port_parent_inventory",
    "two_port",
    "exact_transport",
    "parent_restriction",
    "separation_proof_registry",
}
EXPECTED_PASS_GATES = {
    "independent_primitive_176_anchor_reconstruction",
    "all_site_cartesian_coverage",
    "exact_relation_precedence",
    "quartet_algebra_replay",
    "whole_map_Ti_algebra_replay",
    "transport_replay",
    "parent_restriction_replay",
    "reverse_order_coverage",
    "global_triangle_coherence",
    "mutation_suite",
}
EXPECTED_ZERO_GATES = {
    "cycles",
    "incoherent_transport_restrictions",
    "missing_generated_children",
    "missing_parent_bindings",
    "multiple_parent_bindings",
    "non_isomorphism_or_triangle_survivors",
    "unresolved_records",
    "wrong_parent_bindings",
}
EXPECTED_PROBE_ARTIFACT_VALUES = {
    "primary": {
        "path": "work/probe_coherence_corrected/probe_coherence_certificate.json",
        "file_sha256": "aef621cdefb7a892b396ae993b35d4582faa6d617a90e975d067aed2f9a53554",
        "payload_sha256": "29927d40fcb7b9f3436c9c93f3ec797d2c7b4539ad518c6de94e5ea9efd3ab50",
        "status": "PASS",
    },
    "independent_replay": {
        "path": "work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit_certificate.json",
        "file_sha256": "68d323419270209ee795e0b98b52045cdaf120f21046c4a232207fd838443319",
        "payload_sha256": "cdf6fbec365ebc7f2b9ea66f766c850caf0b88ea56a827a4623dac5d84c05b82",
        "status": "PASS",
    },
    "mutation_report": {
        "path": "work/global_proof_adversary/probe_full_audit/independent_probe_mutation_report.json",
        "file_sha256": "d75c348e905d4d4749e9b6835abb25cb42aac24d10a0c91b5ecb64443fe07a7a",
        "payload_sha256": "0339224d8ea0204c6881dd17dd7fc1a78d931abf8961a89f6b36de4cbd46eab0",
        "status": "PASS",
    },
}
EXPECTED_LEDGER_HASHES = {
    "one_port": "d5fa13d38731bff2403eeb4e4d9e139566c4983b09d30553c6260eaac64c5c90",
    "two_port_parent_inventory": "673112e949e08dce0bdbd690be647dd97d0899c2bb12121b4a16ed7a62dba3f8",
    "two_port": "10f0afcab77f2d61cecfc36d723c6f32065c304ac088b0b8ecf12dfc867fbf9d",
    "exact_transport": "6bc8e88feac2bee68491287775f078e8e5474bf930961a7390967c9fd350044d",
    "parent_restriction": "5d1e6c2fe38d31f6304a76886ec37829215b88c8b179f5b23596d49d37ceeb38",
    "separation_proof_registry": "057783503b1ad7b3c55c14a1cc643db4851c9e42e00595b789b7d6b6d069acfe",
}
EXPECTED_CENSUS = {
    "one_port_directed_rows": 29_964,
    "two_port_directed_rows": 544_571,
    "terminal_hash_root": "7868fed6f8e0c10fcb9740da8ffdcb7f64ea68939c99cba6f364da4cfd90bf50",
    "terminal_census": {
        "anchors": 176,
        "anchor_classes": 39,
        "one_port": {
            "displayed_quartet_mismatch": 27_758,
            "equality_relation_classes": 469,
            "equality_survivors": 2_107,
            "full_map_Ti_strict_sign": 99,
            "isomorphic": 1_915,
            "triangle": 192,
        },
        "two_port": {
            "displayed_quartet_mismatch": 511_266,
            "equality_survivors": 32_729,
            "full_map_Ti_strict_sign": 576,
            "isomorphic": 30_969,
            "triangle": 1_760,
        },
    },
}


FROZEN = {
    "work/domain_rooting_closure/domain_rooting_certificate.json": (
        "4e38beb68062deae8f83cd265daacbef8c5d3f6d73ce25ef47a54828b658d450",
        "01d03c01482ba1f4f0e43d03c3defbff35bc10a97f8b19412ce96e4ce8025328",
    ),
    "work/bridge_marginal_closure/certificate.json": (
        "9231a7b78c13e54b745eba68926276a6551c6c3512d6a85746baba6613c1aacf",
        "5abc19f857a02c712d1386b53bf1ecea18ec31db852cb31b24ea7dde688630ee",
    ),
    "work/global_proof_adversary/component_scale_certificate.json": (
        "c763bcc32af83a7b7605d4f5821d7c27ebb27ad6938d584d28bbd1e96a97d4eb",
        "a5df3fa09c48a372fb1f51acc4471e8c7cada13641deeca6cb6b09a75cb24465",
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz": (
        "7cf3f953fca695d612387143818843650498f84f55cf0a776f90c9afdd95eef6",
        None,
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_summary.json": (
        "7fe22084b0037bd29674baa72683be2673a7f247f300422432c9857f47ad3da1",
        "92880c7655e6e6d906c0d6dbe2089043289c7496d1d9883a3fdc69f4de2bd331",
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_independent_replay.json": (
        "610748d793db9c9045d0eec416f4ea97c54bc4fa4467fe69029fb06fa7db1602",
        "6364abb6c504b511700f2256ab044640ae89a1dbba62e6447e73c252e2d8d5bc",
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz": (
        "8d821c2000da5cf2647913cbdb42f8a42dfeb6826b8b76be49d91d78ebaf9998",
        None,
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_mutations.json": (
        "6475e37d2ec15eafc3650f387d8d4543268963c6794e3dfd90376d01741f23db",
        "94b2f2f90ab77eee454bdbf1c5f81b3be8fd0f89d24b45a15bfed6e92f59a04c",
    ),
    "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_ledger.jsonl.gz": (
        "805fc7f5a3de9dad2c63a210208075cf19910cf811ffd08878f32782ce71b659",
        None,
    ),
    "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_summary.json": (
        "a714cf5b96591832eca83405daec42557bf7da787bf4b6656c19584b726f7973",
        "bdf85d7d02d7a4540da2e9357c948a9e0b30aa799940240323c9d2821d4738d4",
    ),
    "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_independent_replay.json": (
        "cd503f97e4fc0aacb52e04fa02358c95cca099d1b0117e7b7133b0913814d2cd",
        "6a3902aaee5f58a0dd45ed1a65d8e5f27cc8bdda6c3999422437f52482256de5",
    ),
    "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_mutations.json": (
        "07f51fe0d5a28cd673cf782478c4a024e38ff7c729cf7a1e5cdafa4b53a4fac5",
        "6395c6a79540fb05fe10fc54b55bf446d09023e2c6107148926a9c8f6848ac80",
    ),
    "work/restoration_sign_reclassification/corrected_restoration_forest.json": (
        "396d1970af17b5e90c3f1b00ceab1b810816e93ec68a566bd0479f05c722793f",
        "c4e5502d6bb774b426477ef3b289140e81dc16bf061261ccf3562d5de02cb2e3",
    ),
    "work/restoration_sign_reclassification/corrected_restoration_replay_certificate.json": (
        "d74cc01341f405732c6ff62558ca3afff705c15cdf9a6f16dcc6ccd7636749c4",
        "2e190fa1ea877545ace1706c3ae3a423f44cfecc4bc2bba32033c46d109657b0",
    ),
    "work/restoration_sign_reclassification/corrected_restoration_mutation_certificate.json": (
        "ee3a66c72e730b75baea5041bdd42e62de6b8bc561cc0ed6ac1665f3a06dd6ee",
        "13f21d037e6d6fa127e80ed73d0b746c0d00fd67bc3d22de7a75b3959c0d5dbf",
    ),
    "work/cycle_three_port_closure/promotion/cycle_base_authoritative.jsonl.gz": (
        "7bfb6c99ffff43993fe12c7f2625be83dbeb590faac5178961398331368d69a2",
        None,
    ),
    "work/cycle_three_port_closure/promotion/cycle_full_authoritative.jsonl.gz": (
        "6e170c814b95fa7900e9cf24bcb6594a72f8399456614e9da7c0e5a1593d3506",
        None,
    ),
    "work/cycle_three_port_closure/promotion/cycle_promotion_certificate.json": (
        "126ad1dd1aa753b578779fe01c12d26df2f5939abc1e02b5c4b8ccc275867adc",
        "7a7f6757ea4aae3be5e7e1e599d4807e050df999828dc810ae30b443957c8b09",
    ),
    "work/final_theorem_release/triangle_sunlet_certificate.json": (
        "b81a6cf8da1380f6a682ba6042f6f429ce5d6a47ba0cf62e9c9d8de1b4158885",
        "6fd43ae6d38629277c047d3888e970cdab51f4805dce36d71b2430095c1e1aa6",
    ),
    "work/adversarial_proof_review/probe_input_contract.json": (
        "5e6e955db206a0c2b5f520a67fd2fdedcedcdef88d466a7c8e436108a77fac24",
        "e12f0fb912f74fe7b00412619e6a33b28bdeb641a2ddf524fd577d552a856470",
    ),
    "work/adversarial_proof_review/probe_input_independent_verification.json": (
        "842bc64b8fa5ddc2949a5420ea19d3360406a60032012865e4e4a2727f8677dd",
        "d3494abd1ce609824d08816347af514ed8d8ffa280dfc5c8866a6db55578ea12",
    ),
    "work/weak_sharpness_closure/weak_sharpness_certificate.json": (
        "e66c78a0aeab990b4dc448f4f064b37e1e15ecbff75a5f472bf116d4464378bd",
        "dfecd30ea217810a902add48350025e5f00dfa1255718783df790a9c7e1a5182",
    ),
    "work/weak_sharpness_audit/audit_certificate.json": (
        "cfd8d3a2ebc7431d141cac6ebe943e25730eb086fbc84b52833a40bee40a5d52",
        "848cc69e28e3cbd8bc1ab7bbad82b0c3e240354079e95965b433c423edc2d8c5",
    ),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pending_paths(value: Any, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, str) and "__PENDING_" in value:
        found.append(path)
    elif isinstance(value, dict):
        for key, child in value.items():
            found.extend(pending_paths(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(pending_paths(child, f"{path}[{index}]"))
    return found


def fail(message: str) -> None:
    print(f"PROMOTION_BLOCKED: {message}", file=sys.stderr)
    raise SystemExit(1)


def verify_json_payload(path: Path, expected: str) -> None:
    try:
        payload = decode_json_document(
            path.read_bytes(), label=path.name, require_object=True
        )
    except (OSError, StrictJSONError) as exc:
        fail(f"cannot read JSON payload from {path}: {exc}")
    actual = payload.get("payload_sha256")
    if actual != expected:
        fail(f"payload hash field mismatch for {path}: {actual!r} != {expected!r}")


def checked_repo_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError:
        fail(f"artifact path escapes repository: {relative}")
    return path


def verify_frozen_inputs() -> None:
    for relative, (expected_file, expected_payload) in FROZEN.items():
        path = checked_repo_path(relative)
        if not path.is_file():
            fail(f"frozen input missing: {relative}")
        actual = sha256_file(path)
        if actual != expected_file:
            fail(f"frozen input byte hash mismatch: {relative}")
        if expected_payload is not None:
            verify_json_payload(path, expected_payload)


def main() -> None:
    allowed_arguments = {"--frozen-only"}
    unexpected = set(sys.argv[1:]) - allowed_arguments
    if unexpected:
        fail("unexpected command-line argument(s): " + ", ".join(sorted(unexpected)))

    if "--frozen-only" in sys.argv[1:]:
        verify_frozen_inputs()
        print(
            json.dumps(
                {"frozen_inputs_verified": len(FROZEN), "status": "PASS_FROZEN_ONLY"},
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return

    manuscript_text = MANUSCRIPT.read_text(encoding="utf-8")
    try:
        placeholder = decode_json_document(
            PLACEHOLDER.read_bytes(), label=PLACEHOLDER.name, require_object=True
        )
    except (OSError, StrictJSONError) as error:
        fail(f"cannot read JSON payload from {PLACEHOLDER}: {error}")

    pending = pending_paths(placeholder)
    if "__PENDING_" in manuscript_text:
        pending.append("manuscript")
    if pending:
        fail("unfilled probe values at " + ", ".join(pending))

    if placeholder.get("promotion_status") != "PASS":
        fail("probe promotion_status is not PASS")
    if placeholder.get("schema") != "k2p-full-probe-promotion-placeholder-v1":
        fail("unexpected probe placeholder schema")

    input_contract = placeholder.get("frozen_input_contract", {})
    if input_contract != {
        "file_sha256": "5e6e955db206a0c2b5f520a67fd2fdedcedcdef88d466a7c8e436108a77fac24",
        "path_records": 176,
        "payload_sha256": "e12f0fb912f74fe7b00412619e6a33b28bdeb641a2ddf524fd577d552a856470",
    }:
        fail("frozen probe-input contract fields drifted")

    if set(placeholder.get("artifacts", {})) != EXPECTED_ARTIFACTS:
        fail("probe artifact set is incomplete or has unexpected members")
    if set(placeholder.get("bound_ledgers", {})) != EXPECTED_LEDGERS:
        fail("probe ledger set is incomplete or has unexpected members")
    if set(placeholder.get("required_pass_gates", {})) != EXPECTED_PASS_GATES:
        fail("required pass-gate set is incomplete or has unexpected members")
    if set(placeholder.get("required_zero_gates", {})) != EXPECTED_ZERO_GATES:
        fail("required zero-gate set is incomplete or has unexpected members")
    if placeholder["artifacts"] != EXPECTED_PROBE_ARTIFACT_VALUES:
        fail("probe artifact identities drifted from the promoted freeze")
    if placeholder.get("census") != EXPECTED_CENSUS:
        fail("probe census or combined ordered root drifted")

    for key, value in placeholder.get("required_pass_gates", {}).items():
        if value != "PASS":
            fail(f"pass gate {key} is {value!r}, expected 'PASS'")

    for key, value in placeholder.get("required_zero_gates", {}).items():
        if type(value) is not int or value != 0:
            fail(f"zero gate {key} is {value!r}, expected integer 0")

    census = placeholder.get("census", {})
    for key in ("one_port_directed_rows", "two_port_directed_rows"):
        value = census.get(key)
        if type(value) is not int or value <= 0:
            fail(f"census field {key} must be a positive integer")
    if not isinstance(census.get("terminal_census"), dict) or not census["terminal_census"]:
        fail("terminal_census must be a populated object")
    if not HEX64.fullmatch(str(census.get("terminal_hash_root", ""))):
        fail("terminal_hash_root is not a lowercase SHA-256")

    for name, artifact in placeholder.get("artifacts", {}).items():
        if artifact.get("status") != "PASS":
            fail(f"probe artifact {name} status is not PASS")
        for field in ("file_sha256", "payload_sha256"):
            if not HEX64.fullmatch(str(artifact.get(field, ""))):
                fail(f"probe artifact {name} has invalid {field}")
        path = checked_repo_path(str(artifact.get("path", "")))
        if not path.is_file():
            fail(f"probe artifact {name} missing: {path}")
        actual = sha256_file(path)
        if actual != artifact["file_sha256"]:
            fail(f"probe artifact {name} byte hash mismatch")
        verify_json_payload(path, artifact["payload_sha256"])

    for name, ledger in placeholder.get("bound_ledgers", {}).items():
        expected = str(ledger.get("file_sha256", ""))
        if not HEX64.fullmatch(expected):
            fail(f"probe ledger {name} has invalid file_sha256")
        path = checked_repo_path(str(ledger.get("path", "")))
        if not path.is_file():
            fail(f"probe ledger {name} missing: {path}")
        if sha256_file(path) != expected:
            fail(f"probe ledger {name} byte hash mismatch")
        if expected != EXPECTED_LEDGER_HASHES[name]:
            fail(f"probe ledger {name} hash drifted from the promoted freeze")

    verify_frozen_inputs()

    print(
        json.dumps(
            {
                "frozen_inputs_verified": len(FROZEN),
                "probe_artifacts_verified": 3,
                "probe_ledgers_verified": len(placeholder["bound_ledgers"]),
                "required_pass_gates": len(placeholder["required_pass_gates"]),
                "required_zero_gates": len(placeholder["required_zero_gates"]),
                "status": "PASS",
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
