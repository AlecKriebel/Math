#!/usr/bin/env python3
"""Bind and independently replay the complete C7 side-exhaustion bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_ID = "ramsey55_automorphism7_side_model_exhaustion_bundle_checker_v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verified(output: str) -> bool:
    return "VERIFIED" in output and "NOT VERIFIED" not in output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing to overwrite output")
    started = time.monotonic()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if (
        plan.get("schema")
        != "ramsey55.automorphism7_side_model_exhaustion_plan.v1"
        or plan.get("status") != "PREREGISTERED"
    ):
        raise SystemExit("wrong plan")
    outputs = {
        name: ROOT / relative for name, relative in plan["outputs"].items()
    }
    if any(not path.is_file() for path in outputs.values()):
        raise FileNotFoundError("planned artifact missing")
    metadata = json.loads(outputs["metadata"].read_text(encoding="utf-8"))
    structural = json.loads(
        outputs["structural_check"].read_text(encoding="utf-8")
    )
    proof_result = json.loads(
        outputs["proof_result"].read_text(encoding="utf-8")
    )
    generator = ROOT / plan["generator"]["path"]
    checker = ROOT / plan["checker"]["path"]
    tests = ROOT / plan["tests"]["path"]
    pipeline = ROOT / plan["proof_pipeline"]["path"]
    source_pins_valid = (
        sha256_file(generator) == plan["generator"]["sha256"]
        and sha256_file(checker) == plan["checker"]["sha256"]
        and sha256_file(tests) == plan["tests"]["sha256"]
        and sha256_file(pipeline) == plan["proof_pipeline"]["sha256"]
    )
    artifact_binding_valid = (
        structural.get("valid") is True
        and structural.get("model_list_sha256")
        == sha256_file(outputs["models"])
        and structural.get("cnf_sha256") == sha256_file(outputs["cnf"])
        and metadata.get("model_list_sha256")
        == sha256_file(outputs["models"])
        and metadata.get("cnf_sha256") == sha256_file(outputs["cnf"])
        and proof_result.get("status") == "CERTIFIED_UNSAT"
        and proof_result.get("cnf_sha256") == sha256_file(outputs["cnf"])
        and proof_result.get("proof_sha256") == sha256_file(outputs["drat"])
        and proof_result.get("lrat_sha256") == sha256_file(outputs["lrat"])
        and proof_result.get("drat_trim_valid") is True
        and proof_result.get("lrat_check_valid") is True
    )
    drat_trim = Path(plan["toolchain"]["drat_trim"]["path"])
    lrat_check = Path(plan["toolchain"]["lrat_check"]["path"])
    with tempfile.TemporaryDirectory(
        prefix="automorphism7-side-exhaustion-replay-",
        dir=args.output.parent,
    ) as temporary_directory:
        regenerated = Path(temporary_directory) / "regenerated.lrat"
        drat = subprocess.run(
            [
                str(drat_trim),
                str(outputs["cnf"]),
                str(outputs["drat"]),
                "-I",
                "-L",
                str(regenerated),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=int(
                plan["proof_pipeline"]["proof_check_time_limit_seconds"]
            ),
        )
        drat_valid = (
            drat.returncode == 0
            and verified(drat.stdout + drat.stderr)
            and regenerated.is_file()
        )
        regenerated_sha256 = (
            sha256_file(regenerated) if regenerated.is_file() else None
        )
        lrat_exact = (
            drat_valid
            and regenerated.read_bytes() == outputs["lrat"].read_bytes()
        )
    lrat = subprocess.run(
        [str(lrat_check), str(outputs["cnf"]), str(outputs["lrat"])],
        capture_output=True,
        text=True,
        check=False,
        timeout=int(plan["proof_pipeline"]["proof_check_time_limit_seconds"]),
    )
    lrat_valid = lrat.returncode == 0 and verified(lrat.stdout + lrat.stderr)
    retained_bytes = sum(path.stat().st_size for path in outputs.values())
    exact_cover_cap = int(
        plan["storage_gate"]["full_design_exact_cover_cap_bytes"]
    )
    valid = (
        source_pins_valid
        and artifact_binding_valid
        and drat_valid
        and lrat_valid
        and lrat_exact
        and retained_bytes <= exact_cover_cap
    )
    result = {
        "checker": CHECKER_ID,
        "valid": valid,
        "evidence_label": "COMPLETE SIDE-MODEL COVER, DRAT AND LRAT REPLAYED",
        "conclusion": (
            "The 191,394 listed assignments are exactly all satisfying "
            "assignments of the 30-variable C7 side formula."
        ),
        "claim_boundary": (
            "This certifies the side formula only. The global order-7 "
            "conclusion additionally needs the pair quotient and every pair "
            "shard certificate."
        ),
        "source_pins_valid": source_pins_valid,
        "artifact_binding_valid": artifact_binding_valid,
        "model_count": structural["model_count"],
        "all_listed_models_satisfy": structural[
            "all_listed_models_satisfy"
        ],
        "cnf_reconstruction_exact": structural["cnf_reconstruction_exact"],
        "model_list_sha256": sha256_file(outputs["models"]),
        "cnf_sha256": sha256_file(outputs["cnf"]),
        "drat_sha256": sha256_file(outputs["drat"]),
        "drat_bytes": outputs["drat"].stat().st_size,
        "drat_trim_valid": drat_valid,
        "lrat_sha256": sha256_file(outputs["lrat"]),
        "lrat_bytes": outputs["lrat"].stat().st_size,
        "regenerated_lrat_sha256": regenerated_sha256,
        "regenerated_lrat_exact": lrat_exact,
        "lrat_check_valid": lrat_valid,
        "retained_bundle_bytes": retained_bytes,
        "exact_cover_cap_bytes": exact_cover_cap,
        "cap_passed": retained_bytes <= exact_cover_cap,
        "structural_check_sha256": sha256_file(outputs["structural_check"]),
        "proof_result_sha256": sha256_file(outputs["proof_result"]),
        "plan_sha256": sha256_file(args.plan),
        "runtime_seconds": time.monotonic() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
