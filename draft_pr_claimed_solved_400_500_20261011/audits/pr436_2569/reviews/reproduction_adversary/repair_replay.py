#!/usr/bin/env python3
"""Reuse the exact original replay/fault harness on separate repaired copies."""
import importlib.util
import json
from pathlib import Path
import shutil
import sys

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]


def main():
    spec = importlib.util.spec_from_file_location("original_replay", HERE / "reproduce.py")
    replay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(replay)
    repaired = HERE / "repaired_verification"
    provenance = json.loads((repaired / "REPAIR_PROVENANCE.json").read_text())
    replay.PRIVATE = CASE / "private_sources/reproduction_adversary/repair_run"
    replay.HERE = replay.PRIVATE

    def repaired_fixture(name):
        folder = replay.PRIVATE / "fixtures" / name
        if folder.exists():
            raise RuntimeError(f"Refusing to overwrite repaired fixture {name}")
        shutil.copytree(replay.SOURCE, folder)
        for script, _ in replay.SCRIPTS.values():
            data = (repaired / script).read_bytes()
            expected = next(row["repaired_sha256"] for row in provenance["scripts"] if row["path"] == script)
            if replay.digest(data) != expected:
                raise RuntimeError("Repaired code hash mismatch")
            (folder / script).write_bytes(data)
        return folder

    replay.fixture = repaired_fixture
    replay.main()
    result = json.loads((replay.PRIVATE / "EXECUTION_RESULTS.json").read_text())
    # The shared harness records original-family labels. State the repair and actual private location.
    result["record_type"] = "repaired_verification_execution_results"
    result["repair_provenance_sha256"] = replay.digest((repaired / "REPAIR_PROVENANCE.json").read_bytes())
    result["baseline_original_runs"] = result.pop("baseline_original_runs")
    for rec in [result["environment"], *result["baseline_original_runs"], *result["meaningful_fault_controls"]]:
        rec["raw_record"] = rec["raw_record"].replace("reproduction_adversary/raw/", "reproduction_adversary/repair_run/raw/")
    result["baseline_runs_use_repaired_scripts"] = True
    result["all_repaired_baselines_byte_identical"] = all(
        row["exit_code"] == 0 and row["byte_equal_historical"] and row["fields_equal_historical"]
        for row in result["baseline_original_runs"])
    result["all_meaningful_faults_rejected_in_both_modes"] = all(
        row["fault_rejected"] for row in result["meaningful_fault_controls"])
    result["proof_search_turns_added"] = 0
    (HERE / "REPAIRED_EXECUTION_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    if not result["all_repaired_baselines_byte_identical"] or not result["all_meaningful_faults_rejected_in_both_modes"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
