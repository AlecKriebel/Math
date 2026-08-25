#!/usr/bin/env python3
"""Verify the one-sentence full-map certificate reseal and its fail-closed gates."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEFAULT_OUTPUT = HERE / "full_map_reseal_audit.json"
CURRENT_DOMAIN = (
    "the full open unit cube in edge-sector and inheritance variables; "
    "therefore also its physical D_plus subset"
)
LEGACY_DOMAIN = "0<every edge-sector and inheritance variable<1 (hence D_plus)"
FAMILIES = {
    "raw4": {
        "path": PROJECT
        / "work/adversarial_proof_review/raw4_tree_sunlet_full_map_certificate.json",
        "schema": "k2p-raw4-tree-sunlet-full-map-truth-v1",
        "sign_count": 8,
        "legacy_file_sha256": (
            "2195c2c469decc9377c85b5432cdbf5e89d07e7a26a7c547e7760fcef20aa21c"
        ),
    },
    "theta2": {
        "path": PROJECT
        / "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json",
        "schema": "k2p-theta2-tree-sunlet-full-map-truth-v1",
        "sign_count": 85,
        "legacy_file_sha256": (
            "0928eb4061d74d39250360036c024a8c1c63b4e2474f7d17975fcfd326c29dd7"
        ),
        # The strict-triangle canonicalizer hardening changed the atlas bytes,
        # but an independent regeneration left all 2,528 truth rows and all 85
        # sign polynomials unchanged.  Record that provenance-only rebind
        # explicitly so the historical byte reconstruction remains exact.
        "current_atlas_sha256": (
            "37e9b7910f7723c146a87ae2f60dfb62529b1a3e4866ccd72d65dc4efda923ad"
        ),
        "legacy_atlas_sha256": (
            "5b9e03653cc6960bf341fcbe7e63ffd10226d0f6a56441012212c6e3b2a26483"
        ),
    },
}


class ResealFailure(RuntimeError):
    """A certificate, historical reconstruction, or mutation gate failed."""


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        suffix = "" if detail is None else f":{detail}"
        raise ResealFailure(f"{code}{suffix}")


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def pretty_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def sha_object(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sign_payloads(document: dict[str, Any]) -> list[dict[str, Any]]:
    records = document.get("sign_certificates")
    require(isinstance(records, dict), "SIGN_RECORDS_MISSING")
    result: list[dict[str, Any]] = []
    for key in sorted(records):
        row = records[key]
        require(isinstance(row, dict), "SIGN_RECORD_INVALID", key)
        sign = row.get("sign")
        require(isinstance(sign, dict), "SIGN_PAYLOAD_INVALID", key)
        result.append(sign)
    return result


def validate_document(
    document: dict[str, Any],
    *,
    schema: str,
    sign_count: int,
    current_atlas_sha256: str | None = None,
) -> None:
    claimed = document.get("payload_sha256")
    body = {key: value for key, value in document.items() if key != "payload_sha256"}
    require(claimed == sha_object(body), "TOP_SEAL_FAIL")
    require(document.get("schema") == schema, "SCHEMA_FAIL")
    if current_atlas_sha256 is not None:
        require(
            document.get("inputs", {}).get("atlas_sha256")
            == current_atlas_sha256,
            "CURRENT_ATLAS_BINDING_FAIL",
        )
    signs = sign_payloads(document)
    require(len(signs) == sign_count, "SIGN_CENSUS_FAIL", len(signs))
    for ordinal, sign in enumerate(signs):
        nested = sign.get("certificate_sha256")
        body = {key: value for key, value in sign.items() if key != "certificate_sha256"}
        require(nested == sha_object(body), "NESTED_SEAL_FAIL", ordinal)
        require(sign.get("domain") == CURRENT_DOMAIN, "DOMAIN_TEXT_FAIL", ordinal)


def reseal_document(document: dict[str, Any]) -> None:
    document.pop("payload_sha256", None)
    document["payload_sha256"] = sha_object(document)


def reconstruct_legacy(
    document: dict[str, Any], *, legacy_atlas_sha256: str | None = None
) -> dict[str, Any]:
    legacy = copy.deepcopy(document)
    if legacy_atlas_sha256 is not None:
        legacy["inputs"]["atlas_sha256"] = legacy_atlas_sha256
    for sign in sign_payloads(legacy):
        sign["domain"] = LEGACY_DOMAIN
        sign.pop("certificate_sha256", None)
        sign["certificate_sha256"] = sha_object(sign)
    reseal_document(legacy)
    return legacy


def mutation_rows(
    document: dict[str, Any], *, schema: str, sign_count: int, family: str
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    arbitrary = copy.deepcopy(document)
    arbitrary_sign = sign_payloads(arbitrary)[0]
    arbitrary_sign["domain"] = "arbitrary resealed domain"
    arbitrary_sign.pop("certificate_sha256", None)
    arbitrary_sign["certificate_sha256"] = sha_object(arbitrary_sign)
    reseal_document(arbitrary)

    stale_nested = copy.deepcopy(document)
    sign_payloads(stale_nested)[0]["domain"] = "stale nested seal"
    reseal_document(stale_nested)

    stale_top = copy.deepcopy(document)
    stale_top_sign = sign_payloads(stale_top)[0]
    stale_top_sign["domain"] = "stale top seal"
    stale_top_sign.pop("certificate_sha256", None)
    stale_top_sign["certificate_sha256"] = sha_object(stale_top_sign)

    for name, candidate, expected in (
        ("fully_resealed_arbitrary_domain", arbitrary, "DOMAIN_TEXT_FAIL"),
        ("stale_nested_seal", stale_nested, "NESTED_SEAL_FAIL"),
        ("stale_top_seal", stale_top, "TOP_SEAL_FAIL"),
    ):
        try:
            validate_document(candidate, schema=schema, sign_count=sign_count)
        except ResealFailure as error:
            diagnostic = str(error)
            require(expected in diagnostic, "MUTATION_WRONG_REJECTION", diagnostic)
            rows.append(
                {
                    "family": family,
                    "mutation": name,
                    "status": "REJECTED",
                    "diagnostic": diagnostic,
                }
            )
        else:
            raise ResealFailure(f"MUTATION_SURVIVED:{family}:{name}")
    return rows


def main() -> int:
    if not __debug__:
        raise ResealFailure("FULL_MAP_RESEAL_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    family_rows: dict[str, dict[str, Any]] = {}
    mutations: list[dict[str, str]] = []
    for family, specification in FAMILIES.items():
        path = specification["path"]
        document = json.loads(path.read_text(encoding="utf-8"))
        validate_document(
            document,
            schema=specification["schema"],
            sign_count=specification["sign_count"],
            current_atlas_sha256=specification.get("current_atlas_sha256"),
        )
        legacy = reconstruct_legacy(
            document,
            legacy_atlas_sha256=specification.get("legacy_atlas_sha256"),
        )
        legacy_bytes = pretty_bytes(legacy)
        require(
            sha_bytes(legacy_bytes) == specification["legacy_file_sha256"],
            "LEGACY_BYTE_RECONSTRUCTION_FAIL",
            family,
        )
        family_rows[family] = {
            "current_file_sha256": sha_bytes(path.read_bytes()),
            "current_payload_sha256": document["payload_sha256"],
            "legacy_file_sha256": specification["legacy_file_sha256"],
            "legacy_payload_sha256": legacy["payload_sha256"],
            "sign_certificate_count": specification["sign_count"],
            "exact_changed_leaf_census": {
                "domain": specification["sign_count"],
                "certificate_sha256": specification["sign_count"],
                "inputs.atlas_sha256": int(
                    "legacy_atlas_sha256" in specification
                ),
                "payload_sha256": 1,
                "total": 2 * specification["sign_count"]
                + 1
                + int("legacy_atlas_sha256" in specification),
            },
            "all_other_leaves_identical": True,
            "legacy_bytes_reconstructed_exactly": True,
        }
        mutations.extend(
            mutation_rows(
                document,
                schema=specification["schema"],
                sign_count=specification["sign_count"],
                family=family,
            )
        )

    report: dict[str, Any] = {
        "schema": "k2p-full-map-domain-reseal-audit-v1",
        "status": "PASS",
        "current_domain": CURRENT_DOMAIN,
        "legacy_domain": LEGACY_DOMAIN,
        "families": family_rows,
        "mutation_count": len(mutations),
        "mutation_survivors": 0,
        "mutations": mutations,
    }
    report["payload_sha256"] = sha_object(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(pretty_bytes(report))
    print(
        json.dumps(
            {
                "status": "PASS",
                "families": len(family_rows),
                "mutations": len(mutations),
                "payload_sha256": report["payload_sha256"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ResealFailure as error:
        raise SystemExit(f"FULL_MAP_RESEAL_FAIL:{error}") from error
