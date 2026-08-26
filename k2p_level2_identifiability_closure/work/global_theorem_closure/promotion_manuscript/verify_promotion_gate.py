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
        "file_sha256": "53d1ac1e6a14637f547c031a6e8031d3d3cc49630518f31339813031089e0bfc",
        "payload_sha256": "5d71b11dfef66fa3ef33cb52078baa10becb6f08f56edb94902bf82be6e4548b",
        "status": "PASS",
    },
    "independent_replay": {
        "path": "work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit_certificate.json",
        "file_sha256": "74cd1dfb4d6c38dfe73b8bb3c76d29b22eb5f8ab8ca80a9d56bc376ec5d0fa0d",
        "payload_sha256": "095d7cfa4a2f8bc54e56f8fbc2e44f184ba8af75e4135f31f9db5b0c3ff444e2",
        "status": "PASS",
    },
    "mutation_report": {
        "path": "work/global_proof_adversary/probe_full_audit/independent_probe_mutation_report.json",
        "file_sha256": "70fd78df07220d7ab27ba477ed584f3ba1c5cc45a96cd4d4ffdb5d1a34b1325a",
        "payload_sha256": "1b2126eda8036dbb75ed861b3536ed9db0f651c8399cbb85cb8c43d2cf39a110",
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
        "77d3881e7f7d5f90d71339968e3268c5780a0cd51e893e476aac040200e49064",
        "02013c3a0d9456c97d64ae06fd20b241057bfdb437f07acea4f15437860b8416",
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz": (
        "c6cd9d6b5b09371565fd3e58ff9ab3cd7266b6231b153d43f9d1e886af8eae27",
        None,
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_summary.json": (
        "31bb6cf9e363fa4435e1d5a5e4d6d589440b926afd049844eb010b59f04c1436",
        "3a49bfeeb244cba84cf2e42e2acf296f112d1586c5e17f40e2d2872722c3c988",
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_independent_replay.json": (
        "1a4ac5c5ab5f86228f9e59c62a9021547907a9d6238e1171a7074f49506a8c66",
        "dfed35eab33dcc9983b38c8cedb79ed90b12c8a5cf04b58d251637b3fb2f1191",
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz": (
        "0a1818655429d60660c1ed87f3fbe412701f386b081562b3a4caa54079069f1d",
        None,
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_mutations.json": (
        "db6d4e6c8986db20ca623724981d2d4f39f6ff0ccf5d70e708190c1e09a86d4a",
        "eec4a56b20faa3239044db49796fa724d60a5412a8d6e89a92db5d81e9656385",
    ),
    "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_ledger.jsonl.gz": (
        "805fc7f5a3de9dad2c63a210208075cf19910cf811ffd08878f32782ce71b659",
        None,
    ),
    "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_summary.json": (
        "cf4ee4c23068cbc644474ad0161510a99106d3235f28e722fd3340b5bbbb3fdb",
        "c89dd764f7c66831db7f6a092fedf666a20f3594ef03647de3e85b5fbf04d0e8",
    ),
    "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_independent_replay.json": (
        "dd02a752b2ce41628039d2f6da6fdab77f2a8ffd73b8cd80e2968790dbbf3150",
        "7e4283fe726083927b14d483d55644e2892a311b0179aa70d4766576c66ab545",
    ),
    "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_mutations.json": (
        "ec2c6ec092539048b4e7ab9d9cfea01caa985d0f35cae74ca56732dc4cfe4c84",
        "5663b87d3f09eaac5e89db69ac5a1cf6069b308abf9bc4242650d0897ded1ff7",
    ),
    "work/restoration_sign_reclassification/corrected_restoration_forest.json": (
        "bcf91bf433c71056d1e27871dd15fe532f9ae1cc4ad79eb2373eae57071ee427",
        "be81d13f8f51dc49030e569bf31939a7c3bb915c3dff1f91455416761eeeb772",
    ),
    "work/restoration_sign_reclassification/corrected_restoration_replay_certificate.json": (
        "42be6b0c4d85aa58b336caebbdefd10a0af0ce4234a0482e65c7b5a68d1e6430",
        "e32668fd0b1bc6d59fc7fde6a3bb25e934e8e4c77aa65ee4f024978d07ddda4f",
    ),
    "work/restoration_sign_reclassification/corrected_restoration_mutation_certificate.json": (
        "9379094aa0bd6a90c906d82ca441bccee00fa0b10b13d34645c5ca9c3bff9161",
        "9f31f9688a587d79d35c24114d4a0693463486f254f0ee4892b99494d707c909",
    ),
    "work/cycle_three_port_closure/promotion/cycle_base_authoritative.jsonl.gz": (
        "abb209def72a61971b7f2fd8b1f3b7fb1a1a7d2e79b8dc2985feb04736a44437",
        None,
    ),
    "work/cycle_three_port_closure/promotion/cycle_full_authoritative.jsonl.gz": (
        "76860c09fe8fc26887e6db275ca4d200bc7c3168cfe66a505789926f1c0d273b",
        None,
    ),
    "work/cycle_three_port_closure/promotion/cycle_promotion_certificate.json": (
        "9fa7dbb121108f778395405cbc866cccc78d9766c4ca12c86aaa24caa899bd50",
        "26482f277889f3667841614b34dad8cfa68bb3ea2041d4847c9f06d8b82e6590",
    ),
    "work/final_theorem_release/triangle_sunlet_certificate.json": (
        "b81a6cf8da1380f6a682ba6042f6f429ce5d6a47ba0cf62e9c9d8de1b4158885",
        "6fd43ae6d38629277c047d3888e970cdab51f4805dce36d71b2430095c1e1aa6",
    ),
    "work/adversarial_proof_review/probe_input_contract.json": (
        "71d8596c5e0fa5804f5a1d938423ba9802f4d11783ef0e9d0f45a0453f0aff22",
        "39eb12e3dccf102d0550017cc7374ac1ab22c7065e52c900bea2205d07e4e14f",
    ),
    "work/adversarial_proof_review/probe_input_independent_verification.json": (
        "7aab53c560117a4e0260b0c63905fa5d6e60c384d0f01d7f986ddb75911c0107",
        "4a29f3e7c5e925820b2df39a7a53d29b1a7f672776af9604c2489dbb908a8e36",
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
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
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
    placeholder = json.loads(PLACEHOLDER.read_text(encoding="utf-8"))

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
        "file_sha256": "71d8596c5e0fa5804f5a1d938423ba9802f4d11783ef0e9d0f45a0453f0aff22",
        "path_records": 176,
        "payload_sha256": "39eb12e3dccf102d0550017cc7374ac1ab22c7065e52c900bea2205d07e4e14f",
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
