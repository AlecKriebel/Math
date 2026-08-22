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
        "file_sha256": "93de7b0dd3aa581bdf12288eae8cb9ac42f20a9d9bb3eab35eee8ef9a759d390",
        "payload_sha256": "674853fa730c4f54b9ba264d539a51591c8b926ad444195e68df086c26f83825",
        "status": "PASS",
    },
    "independent_replay": {
        "path": "work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit_certificate.json",
        "file_sha256": "47f527dd56ce355d911c44ebc55e24a1e9c7f14f379810902b49ae068261e74f",
        "payload_sha256": "4492860febc84f4530f67fa50f684ca34fde7c6fc2c6b3ccf906d88d275ac540",
        "status": "PASS",
    },
    "mutation_report": {
        "path": "work/global_proof_adversary/probe_full_audit/independent_probe_mutation_report.json",
        "file_sha256": "b0df0584163150c9a823b4e364b8ee46c196ae8abb28fdca4d3d5893a97bfea7",
        "payload_sha256": "58006ed7b6677c055b5cdd7249857dc2f752fb3db9cfbcc5bbe5e0a26e31875f",
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
        "d9b19cde1e9d0544d8c1674ace662b050301313858c1b9bdc857af29c64804d6",
        "ce8f4e6860675e36238b8351458875bd46de0507df34f6729e34b20170e02acd",
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz": (
        "431dac8898ad2a724d12c200687de1b377723e302214a79a11a03524a4084b96",
        None,
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_summary.json": (
        "515d6fea22d8388ab13c68066d0a57164b96baa684bf24b8f6da7da21bf6726c",
        "8154acc38ad58b49e4f0f5b34f6fdb9999c0392dd947f91bc6017d8e2ab8d5cf",
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_independent_replay.json": (
        "d44705d2266aa1360acec19cdb8bf0fea648fc9c029ae96adb437a04ad5cce10",
        "0e167e742907394a77a0eab1614366e2460b86b13241577ad25e902822241ea8",
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz": (
        "0a1818655429d60660c1ed87f3fbe412701f386b081562b3a4caa54079069f1d",
        None,
    ),
    "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_mutations.json": (
        "449228fa4013234280434495e5c79468750de2785d5a2a2a8ad7d91bbdcae3a7",
        "88bd552f75c87d0b084ab6a9fa09421ef16867b274a2be25b513ff9fdf9f010d",
    ),
    "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_ledger.jsonl.gz": (
        "805fc7f5a3de9dad2c63a210208075cf19910cf811ffd08878f32782ce71b659",
        None,
    ),
    "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_summary.json": (
        "5c0c7c091982b3ce235f0380eeb6e4531419bf7d3dcbfe44b9535f1b0e122086",
        "480c27d82924bbf12adf1357f9e3bc216d1818dce68d061bb134f387e9737194",
    ),
    "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_independent_replay.json": (
        "ed57b46c5e05a73f08a26afc99ae1bd5f0076e941b2da7ac411ecc52f3b63e58",
        "2fa46fd0ca70dbe00e8231686bfd790f57d76d9a33ddc4b07cffaa72e3b07e8b",
    ),
    "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_mutations.json": (
        "c1c8012941ac58ae3f01a890caaa9e9ad05e8342d11a41d8a911de18dc3e6775",
        "5fce45398dc5f3ad948078ec5b66583d28e3af2cf3991f4f0931c0bfaf332e77",
    ),
    "work/restoration_sign_reclassification/corrected_restoration_forest.json": (
        "43bd2be5e7626a954fc4fa4cf45e8d0e6483c947ddc9cba80f2b1a13351bc3a8",
        "0a3df52751ba38d7e6d4d118ee7068a98b7be7897d0aa732e96a74d7523a88bf",
    ),
    "work/restoration_sign_reclassification/corrected_restoration_replay_certificate.json": (
        "24fa2e61f60610a8b24c4107ec7f866278f0cc671ca203d7aaa40a37bea291dd",
        "36c89ff9729e049a374a9fead8488f7a90e62c617d17e242aca5d340faeb164a",
    ),
    "work/restoration_sign_reclassification/corrected_restoration_mutation_certificate.json": (
        "7513e55df67bc9d3adbbe3fe9e20b2557beb733abb29b73cbdaabc5103d890ca",
        "5d2733443767fbd1fecbe6cd2723f3f463e0afdb0404f970994dcf9b968d6348",
    ),
    "work/cycle_three_port_closure/promotion/cycle_base_authoritative.jsonl.gz": (
        "d6209dc605c9f3a3459c129d741c6b788f26dcf989afe828d8a720833bfd49da",
        None,
    ),
    "work/cycle_three_port_closure/promotion/cycle_full_authoritative.jsonl.gz": (
        "cc73d0eaf3f39939c255c8f86915093e58159eca37c147ae2854d430f1fcb2f7",
        None,
    ),
    "work/cycle_three_port_closure/promotion/cycle_promotion_certificate.json": (
        "b560fdf0545c36d576a4cdaf24af9984f6f7231180f20f6927121a57bf816a7a",
        "df5e3966822af65e2341660bf3f607ff3635d69d3e5a89854afaef308727f2f1",
    ),
    "work/final_theorem_release/triangle_sunlet_certificate.json": (
        "b81a6cf8da1380f6a682ba6042f6f429ce5d6a47ba0cf62e9c9d8de1b4158885",
        "6fd43ae6d38629277c047d3888e970cdab51f4805dce36d71b2430095c1e1aa6",
    ),
    "work/adversarial_proof_review/probe_input_contract.json": (
        "7f686ae99dd5e6dafc1c04396b711d294a0bddd6a25574f9ea809b831ad7b377",
        "579919ca13204ddf959b3a159e4849b69c05ac87861eba2221659ec45bd73f38",
    ),
    "work/adversarial_proof_review/probe_input_independent_verification.json": (
        "54de1bef73e76fc82132ef3f0250a0579ea401274a302ed4d8fbd015c9e8a053",
        "96d14bae9b20646abfe64b85a7ac0f61377182f75479031f621ea0dbe2096fce",
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
        "file_sha256": "7f686ae99dd5e6dafc1c04396b711d294a0bddd6a25574f9ea809b831ad7b377",
        "path_records": 176,
        "payload_sha256": "579919ca13204ddf959b3a159e4849b69c05ac87861eba2221659ec45bd73f38",
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
