#!/usr/bin/env python3
"""Run bounded or complete exact Walsh ranges for the mod-4 quadratic lift."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import subprocess
import tempfile

import numpy as np

import verify_long_block_exact_triage as triage


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "mod4_quadratic_walsh.cpp"
CERTIFICATE = HERE / "MOD4_WALSH_CENSUS.json"
MAGIC = b"H668M4Q1"


def write_model(path: Path, case_number: int) -> dict[str, object]:
    metadata, arrays = triage.derive_mod4_anf(case_number)
    constant, linear, quadratic = arrays
    with path.open("wb") as output:
        output.write(MAGIC)
        output.write(struct.pack("<II", 57, 20))
        for equation in range(20):
            constant_word = int(constant[equation])
            linear_word = sum(
                int(linear[equation, coordinate]) << coordinate
                for coordinate in range(57)
            )
            output.write(struct.pack("<QQ", constant_word, linear_word))
            adjacency = [0] * 57
            for left in range(57):
                for right in range(left + 1, 57):
                    if quadratic[equation, left, right]:
                        adjacency[left] |= 1 << right
                        adjacency[right] |= 1 << left
            output.write(struct.pack("<" + "Q" * 57, *adjacency))
    payload = path.read_bytes()
    return {
        **metadata,
        "binary_model_bytes": len(payload),
        "binary_model_sha256": hashlib.sha256(payload).hexdigest(),
    }


def compile_engine(destination: Path) -> None:
    subprocess.run(
        [
            "clang++",
            "-O3",
            "-DNDEBUG",
            "-std=c++20",
            "-Wall",
            "-Wextra",
            "-pedantic",
            str(SOURCE),
            "-o",
            str(destination),
        ],
        check=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        default="1,2,6,14",
        help="comma-separated canonical cases (default: 1,2,6,14)",
    )
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument(
        "--stop",
        type=int,
        default=1 << 16,
        help="exclusive Walsh-combination stop (default: bounded 2^16)",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="run all 2^20 combinations for each selected case",
    )
    parser.add_argument(
        "--write-certificate",
        action="store_true",
        help="write the aggregate payload to MOD4_WALSH_CENSUS.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases = tuple(int(value) for value in args.cases.split(",") if value)
    if not cases or any(case not in triage.CASES for case in cases):
        raise ValueError("cases must lie in 1,...,20")
    start = 0 if args.full else args.start
    stop = (1 << 20) if args.full else args.stop
    if not 0 <= start <= stop <= 1 << 20:
        raise ValueError("invalid Walsh range")

    results = []
    with tempfile.TemporaryDirectory(prefix="h668_mod4_walsh_") as temporary:
        temporary_path = Path(temporary)
        engine = temporary_path / "mod4_walsh"
        compile_engine(engine)
        for case_number in cases:
            model = temporary_path / f"case_{case_number}.bin"
            metadata = write_model(model, case_number)
            completed = subprocess.run(
                [str(engine), str(model), str(start), str(stop)],
                check=True,
                capture_output=True,
                text=True,
            )
            walsh = json.loads(completed.stdout)
            if walsh["common_zeros"] is not None:
                common_zeros = int(walsh["common_zeros"])
                walsh["effective_bits_removed"] = (
                    57 - math.log2(common_zeros)
                )
            results.append(
                {
                    "case": case_number,
                    "q_index": metadata["q_index"],
                    "anf_sha256": metadata["anf_sha256"],
                    "binary_model_bytes": metadata["binary_model_bytes"],
                    "binary_model_sha256": metadata[
                        "binary_model_sha256"
                    ],
                    "walsh": walsh,
                }
            )

    payload: dict[str, object] = {
        "schema": "h668-mod4-quadratic-walsh-census-v1",
        "cases": list(cases),
        "range": [start, stop],
        "complete_pencil": start == 0 and stop == 1 << 20,
        "affine_domain": {
            "free_coordinates": 57,
            "points": str(1 << 57),
            "weight_constraint": (
                "odd parity only; exact weight 39 is not imposed"
            ),
        },
        "interpretation": (
            "common_zeros is the exact mod-4 relaxation count inside the "
            "21-equation mod-2 affine slice, not a weight-39 census"
        ),
        "results": results,
    }
    semantic = json.loads(json.dumps(payload))
    for result in semantic["results"]:
        result["walsh"].pop("seconds", None)
        result["walsh"].pop("combinations_per_second", None)
    payload["semantic_sha256"] = triage.compact_hash(semantic)
    if args.write_certificate:
        CERTIFICATE.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n"
        )
        print(f"WROTE {CERTIFICATE}")
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
