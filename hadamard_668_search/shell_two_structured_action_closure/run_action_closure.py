#!/usr/bin/env python3
"""Run the exact shell-two structured action closure, one image at a time."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import action_closure_common as common


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "output" / "production-v2"
DEFAULT_CERTIFICATE = HERE / "ACTION_CLOSURE_CERTIFICATE_V2.json"


def result_path(output: Path, index: int) -> Path:
    return output / f"image_{index:03d}.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--image-index",
        action="append",
        type=int,
        help="global image index; repeat to select several",
    )
    parser.add_argument(
        "--prepare-only",
        action="store_true",
        help="derive and print the frozen inputs and action manifest only",
    )
    parser.add_argument(
        "--write-certificate",
        action="store_true",
        help="write the tracked aggregate after all 84 results validate",
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        default=DEFAULT_CERTIFICATE,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = common.build_action_manifest()
    inputs = common.input_hashes()
    images = tuple(manifest["images"])
    print(
        "manifest="
        f"{manifest['semantic_sha256']} images={len(images)} "
        f"sources={len(inputs)}"
    )
    if args.prepare_only:
        print(json.dumps(manifest["source_orbit_counts"], sort_keys=True))
        return 0

    selected = (
        tuple(range(len(images)))
        if args.image_index is None
        else tuple(dict.fromkeys(args.image_index))
    )
    if any(index < 0 or index >= len(images) for index in selected):
        raise SystemExit("image index outside 0..83")
    args.output.mkdir(parents=True, exist_ok=True)

    pending = []
    results: dict[int, dict[str, object]] = {}
    for index in selected:
        path = result_path(args.output, index)
        if path.is_file():
            results[index] = common.validate_result(
                path,
                images[index],
                inputs,
                manifest["semantic_sha256"],
            )
            print(f"resume image={index:03d} status=VALID")
        else:
            pending.append(index)

    submodules = None
    if pending:
        common.f27.algebra.verify_pencil_algebra()
        submodules = common.f27.minimal_submodules()
        if len(submodules) != 56:
            raise AssertionError("F27 submodule census changed")
    for ordinal, index in enumerate(pending, start=1):
        image = images[index]
        print(
            f"start image={index:03d} id={image['image_id']} "
            f"pending={ordinal}/{len(pending)}",
            flush=True,
        )
        try:
            assert submodules is not None
            result = common.compute_image(
                image,
                inputs,
                manifest["semantic_sha256"],
                submodules,
            )
        except common.ConsecutiveSurvivor as discovery:
            alert_path = args.output / "CONSECUTIVE_SURVIVOR.json"
            common.atomic_json_write(alert_path, discovery.payload)
            print(
                "CONSECUTIVE_SURVIVOR="
                + common.canonical_json(discovery.payload),
                flush=True,
            )
            return 2
        path = result_path(args.output, index)
        common.atomic_json_write(path, result)
        results[index] = common.validate_result(
            path,
            image,
            inputs,
            manifest["semantic_sha256"],
        )
        print(
            f"done image={index:03d} "
            f"seconds={result['runtime']['elapsed_seconds']:.3f} "
            f"rss={common.current_rss_bytes()} "
            f"d2={common.aggregate_summaries([common.semantic_payload(result)])['raw_second_digit_survivor_occurrences']}",
            flush=True,
        )

    if args.write_certificate:
        all_results = []
        expected_paths = {
            result_path(args.output, index) for index in range(len(images))
        }
        actual_paths = set(args.output.glob("image_*.json"))
        if actual_paths != expected_paths:
            missing = sorted(str(path) for path in expected_paths - actual_paths)
            extra = sorted(str(path) for path in actual_paths - expected_paths)
            raise AssertionError(
                f"exact output set failed; missing={missing} extra={extra}"
            )
        for index, image in enumerate(images):
            all_results.append(
                common.validate_result(
                    result_path(args.output, index),
                    image,
                    inputs,
                    manifest["semantic_sha256"],
                )
            )
        certificate = common.build_certificate(
            manifest, inputs, all_results
        )
        common.atomic_json_write(args.certificate, certificate)
        print(
            f"certificate={args.certificate} "
            f"semantic_sha256={certificate['semantic_sha256']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
