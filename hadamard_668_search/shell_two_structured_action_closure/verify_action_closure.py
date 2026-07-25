#!/usr/bin/env python3
"""Verify the tracked 84-image structured action-closure certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import action_closure_common as common


HERE = Path(__file__).resolve().parent
PINNED_CERTIFICATE = HERE / "ACTION_CLOSURE_CERTIFICATE_V2.json"
DEFAULT_OUTPUT = HERE / "output" / "production-v2"


def result_path(output: Path, index: int) -> Path:
    return output / f"image_{index:03d}.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate", type=Path, default=PINNED_CERTIFICATE
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="also validate the exact production output set",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--full",
        action="store_true",
        help="rerun every exact family enumeration and compare all records",
    )
    return parser.parse_args()


def load_and_verify_certificate(path: Path) -> tuple[
    dict[str, object],
    dict[str, object],
    dict[str, str],
]:
    if not path.is_file():
        raise AssertionError(f"pinned certificate is missing: {path}")
    stored = json.loads(path.read_text(encoding="utf-8"))
    semantic = stored.pop("semantic_sha256")
    if common.compact_hash(stored) != semantic:
        raise AssertionError("certificate semantic digest failed")
    stored["semantic_sha256"] = semantic
    if stored["schema"] != common.CERTIFICATE_SCHEMA:
        raise AssertionError("certificate schema changed")
    manifest = common.build_action_manifest()
    inputs = common.input_hashes()
    if stored["inputs"] != inputs:
        raise AssertionError("frozen transitive source hashes changed")
    if common.json_normalize(stored["action_manifest"]) != (
        common.json_normalize(manifest)
    ):
        raise AssertionError("frozen action manifest changed")
    if stored["action_manifest_sha256"] != manifest["semantic_sha256"]:
        raise AssertionError("action manifest digest changed")
    if int(stored["image_count"]) != common.EXPECTED_IMAGE_COUNT:
        raise AssertionError("certificate does not cover 84 images")
    if tuple(stored["family_names"]) != common.ALL_FAMILY_NAMES:
        raise AssertionError("certificate family list changed")
    records = tuple(stored["records"])
    images = tuple(manifest["images"])
    if len(records) != len(images):
        raise AssertionError("certificate record count changed")
    for index, (record, image) in enumerate(zip(records, images)):
        if common.compact_hash(record) != (
            stored["record_semantic_sha256"][index]
        ):
            raise AssertionError(f"embedded record {index} digest failed")
        common.validate_semantic_result(
            record, image, inputs, manifest["semantic_sha256"]
        )
    regenerated = common.build_certificate(manifest, inputs, records)
    if common.json_normalize(regenerated) != common.json_normalize(stored):
        raise AssertionError("certificate aggregate replay changed")
    if stored["status"] != "EXHAUSTIVE_NO_CONSECUTIVE_SURVIVOR":
        raise AssertionError("certificate status is not exhaustive")
    return stored, manifest, inputs


def verify_live(
    output: Path,
    certificate: dict[str, object],
    manifest: dict[str, object],
    inputs: dict[str, str],
) -> None:
    images = tuple(manifest["images"])
    expected = {
        result_path(output, index) for index in range(len(images))
    }
    actual = set(output.glob("image_*.json"))
    if actual != expected:
        raise AssertionError(
            f"live output set changed: missing={sorted(expected-actual)} "
            f"extra={sorted(actual-expected)}"
        )
    records = []
    for index, image in enumerate(images):
        result = common.validate_result(
            result_path(output, index),
            image,
            inputs,
            manifest["semantic_sha256"],
        )
        records.append(common.semantic_payload(result))
    if common.json_normalize(records) != common.json_normalize(
        certificate["records"]
    ):
        raise AssertionError("live results differ from tracked certificate")


def verify_full(
    certificate: dict[str, object],
    manifest: dict[str, object],
    inputs: dict[str, str],
) -> None:
    common.f27.algebra.verify_pencil_algebra()
    submodules = common.f27.minimal_submodules()
    for index, image in enumerate(manifest["images"]):
        regenerated = common.compute_image(
            image,
            inputs,
            manifest["semantic_sha256"],
            submodules,
        )
        if common.json_normalize(common.semantic_payload(regenerated)) != (
            common.json_normalize(certificate["records"][index])
        ):
            raise AssertionError(f"full replay changed image {index}")
        print(f"full image={index:03d} status=PASS", flush=True)


def main() -> int:
    args = parse_args()
    certificate, manifest, inputs = load_and_verify_certificate(
        args.certificate
    )
    if args.live:
        verify_live(args.output, certificate, manifest, inputs)
    if args.full:
        verify_full(certificate, manifest, inputs)
    summaries = certificate["summaries"]
    print(
        f"images={certificate['image_count']} "
        f"d2_raw={summaries['raw_second_digit_survivor_occurrences']} "
        f"d2_c6_unique="
        f"{summaries['unique_c6_rotation_classes_of_second_digit_survivors']} "
        f"d3={summaries['consecutive_through_digit_3_survivors']} "
        f"semantic_sha256={certificate['semantic_sha256']} status=PASS"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
