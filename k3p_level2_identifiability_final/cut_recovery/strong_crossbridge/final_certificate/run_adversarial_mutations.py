#!/usr/bin/env python3
"""Subprocess-isolated mutation suite for the aggregate verifier."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
SINGLE = HERE / "SINGLE_MINOR_REPLAY.json"
UNIVERSE = HERE / "UNIVERSE_CERTIFICATE.json"
FINAL = HERE / "STRONG_CROSSBRIDGE_FINAL_CERTIFICATE.json"
VERIFIER = HERE / "verify_final_certificate.py"
REPORT = HERE / "ADVERSARIAL_MUTATION_REPORT.json"


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def changed_hash(value):
    return ("0" if value[0] != "0" else "1") + value[1:]


def run(single, universe, final):
    return subprocess.run(
        [
            sys.executable,
            str(VERIFIER),
            "--single",
            str(single),
            "--universe",
            str(universe),
            "--final",
            str(final),
            "--no-report",
        ],
        cwd=HERE,
        text=True,
        capture_output=True,
        check=False,
    )


def cases():
    result = []

    def add(kind, identifier, description, mutate):
        result.append((kind, identifier, description, mutate))

    add("single", "single_target_index", "change the first replay target index", lambda s: s["records"][0].__setitem__("target_index", 1))
    add("single", "single_descriptor", "change a replay descriptor hash", lambda s: s["records"][1].__setitem__("descriptor_sha256", changed_hash(s["records"][1]["descriptor_sha256"])))
    add("single", "single_polynomial_coefficient", "change an explicit reduced-polynomial coefficient", lambda s: s["records"][2]["minor"]["reduced_polynomial"][0].__setitem__(1, str(int(s["records"][2]["minor"]["reduced_polynomial"][0][1]) + 1)))
    add("single", "single_reduced_hash", "change a reduced-polynomial hash", lambda s: s["records"][3]["minor"].__setitem__("reduced_polynomial_sha256", changed_hash(s["records"][3]["minor"]["reduced_polynomial_sha256"])))
    add("single", "single_monomial", "change a positive monomial exponent", lambda s: s["records"][4]["minor"]["positive_monomial_exponent"].__setitem__(0, s["records"][4]["minor"]["positive_monomial_exponent"][0] + 1))
    add("single", "single_coordinate", "change a selected Fourier coordinate", lambda s: s["records"][5]["minor"]["coordinate_indices"].__setitem__(0, 1))
    add("single", "single_bernstein_numerator", "change a nonzero Bernstein numerator", lambda s: s["records"][6]["bernstein"]["nonzero_coefficients"][0].__setitem__("numerator", s["records"][6]["bernstein"]["nonzero_coefficients"][0]["numerator"] + 1))
    add("single", "single_bernstein_hash", "change the legacy ordered-numerator hash", lambda s: s["records"][7]["bernstein"].__setitem__("ordered_numerators_sha256", changed_hash(s["records"][7]["bernstein"]["ordered_numerators_sha256"])))
    add("single", "single_record_deletion", "delete a replay record", lambda s: s["records"].pop(8))
    add("single", "single_source_binding", "change a discovery-record byte binding", lambda s: s["source_record_bindings"][9].__setitem__("sha256", changed_hash(s["source_record_bindings"][9]["sha256"])))
    add("single", "single_residual_list", "remove a residual target", lambda s: s["residual_target_indices"].pop())
    add("single", "single_producer_hash", "change the producer source binding", lambda s: s["inputs"].__setitem__("producer_sha256", changed_hash(s["inputs"]["producer_sha256"])))

    add("universe", "universe_target_index", "change a direction index", lambda u: u["directions"][0].__setitem__("target_index", 1))
    add("universe", "universe_split", "change a labelled split", lambda u: u["directions"][1].__setitem__("old_split", [0, 1]))
    add("universe", "universe_order", "change a normalization order", lambda u: u["directions"][2].__setitem__("old_order", [0, 2, 1, 3]))
    add("universe", "universe_port_map", "change an old-to-normalized port map", lambda u: u["directions"][3]["old_to_normalized_port_map"].__setitem__(0, 3))
    add("universe", "universe_normalized_split", "change the normalized split", lambda u: u["directions"][4].__setitem__("normalized_split", [[0, 2], [1, 3]]))
    add("universe", "universe_signature_hash", "change a normalized-signature hash", lambda u: u["directions"][5].__setitem__("normalized_signatures_sha256", changed_hash(u["directions"][5]["normalized_signatures_sha256"])))
    add("universe", "universe_descriptor_hash", "change a normalized descriptor hash", lambda u: u["directions"][6].__setitem__("descriptor_sha256", changed_hash(u["directions"][6]["descriptor_sha256"])))
    add("universe", "universe_category", "move a direction to the wrong proof category", lambda u: u["directions"][7].__setitem__("certificate_category", "cyclic"))
    add("universe", "universe_row_deletion", "delete a normalized direction", lambda u: u["directions"].pop(8))
    add("universe", "universe_partition_overlap", "insert a signed-pair target into the single-minor partition", lambda u: u["partition"]["single_minor"].append(108))
    add("universe", "universe_automorphism_dependency", "claim an automorphism audit was used", lambda u: u["automorphism_audit"].__setitem__("used", True))
    add("universe", "universe_dummy_bug_status", "erase the record60 dummy-label supersession", lambda u: u["automorphism_audit"].__setitem__("known_record60_dummy_label_bug", "PASS"))

    add("final", "final_false_blocked", "downgrade a complete certificate to BLOCKED", lambda f: f.__setitem__("status", "BLOCKED"))
    add("final", "final_coverage_count", "change the 204-direction coverage count", lambda f: f["coverage"].__setitem__("target_directions", 203))

    def dependency_targets(final):
        final["dependencies"][1]["required_targets"].pop()
        final["dependencies_sha256"] = digest(final["dependencies"])

    add("final", "final_dependency_targets", "remove a signed-pair dependency target and rebind", dependency_targets)

    def dependency_artifact(final):
        artifact = final["dependencies"][1]["artifacts"][0]
        artifact["sha256"] = changed_hash(artifact["sha256"])
        final["dependencies_sha256"] = digest(final["dependencies"])

    add("final", "final_child_artifact_hash", "change a child proof byte hash and rebind", dependency_artifact)

    def dependency_status(final):
        final["dependencies"][2]["status"] = "BLOCKED"
        final["dependencies"][2]["reason"] = "mutated"
        final["dependencies_sha256"] = digest(final["dependencies"])

    add("final", "final_child_status", "falsify a child proof status and rebind", dependency_status)
    add("final", "final_blocked_list", "add a spurious blocked dependency", lambda f: f["blocked_dependencies"].append("cyclic"))
    add("final", "final_automorphism_flag", "claim automorphism transport in the final proof", lambda f: f["coverage"].__setitem__("automorphism_transport_used", True))
    add("final", "final_frozen_hash", "change the frozen primitive binding", lambda f: f["inputs"]["frozen_primitive"].__setitem__("sha256", changed_hash(f["inputs"]["frozen_primitive"]["sha256"])))
    add("final", "final_dependency_hash", "change only the aggregate dependency hash", lambda f: f.__setitem__("dependencies_sha256", changed_hash(f["dependencies_sha256"])))
    add("final", "final_partition_count", "change a category count", lambda f: f["coverage"]["partition_counts"].__setitem__("cyclic", 9))
    return result


def atomic_write(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main():
    baseline = run(SINGLE, UNIVERSE, FINAL)
    if baseline.returncode:
        raise RuntimeError(f"baseline failure: {baseline.stdout}{baseline.stderr}")
    base_single = json.loads(SINGLE.read_text())
    base_universe = json.loads(UNIVERSE.read_text())
    base_final = json.loads(FINAL.read_text())
    results = []
    with tempfile.TemporaryDirectory(prefix="mutation-", dir=HERE) as directory:
        root = Path(directory)
        for index, (kind, identifier, description, mutate) in enumerate(cases()):
            single = copy.deepcopy(base_single)
            universe = copy.deepcopy(base_universe)
            final = copy.deepcopy(base_final)
            if kind == "single":
                mutate(single)
                single["records_sha256"] = digest(single["records"])
            elif kind == "universe":
                mutate(universe)
                universe["directions_sha256"] = digest(universe["directions"])
            single_path = root / f"{index:03d}-single.json"
            universe_path = root / f"{index:03d}-universe.json"
            final_path = root / f"{index:03d}-final.json"
            single_path.write_text(json.dumps(single, indent=2, sort_keys=True) + "\n")
            universe_path.write_text(json.dumps(universe, indent=2, sort_keys=True) + "\n")
            final["inputs"]["single_minor_replay"]["sha256"] = file_hash(single_path)
            final["inputs"]["universe_certificate"]["sha256"] = file_hash(universe_path)
            final["dependencies"][0]["artifacts"][0]["sha256"] = file_hash(single_path)
            final["dependencies_sha256"] = digest(final["dependencies"])
            if kind == "final":
                mutate(final)
            final_path.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n")
            completed = run(single_path, universe_path, final_path)
            if completed.returncode == 0:
                raise AssertionError(f"mutation escaped: {identifier}")
            error = None
            if completed.stdout.strip():
                try:
                    error = json.loads(completed.stdout.strip().splitlines()[-1]).get("error")
                except json.JSONDecodeError:
                    error = completed.stdout.strip()[-500:]
            results.append(
                {
                    "id": identifier,
                    "surface": kind,
                    "description": description,
                    "rejected": True,
                    "verifier_error": error,
                }
            )
    report = {
        "schema": "k3p-strong-crossbridge-final-adversarial-mutations-v1",
        "status": "PASS",
        "baseline_passed": True,
        "inputs": {
            "single_sha256": file_hash(SINGLE),
            "universe_sha256": file_hash(UNIVERSE),
            "final_sha256": file_hash(FINAL),
            "verifier_sha256": file_hash(VERIFIER),
        },
        "mutation_count": len(results),
        "rejected_count": sum(record["rejected"] for record in results),
        "all_mutations_rejected": all(record["rejected"] for record in results),
        "mutations": results,
    }
    atomic_write(REPORT, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "mutation_count": report["mutation_count"],
                "rejected_count": report["rejected_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
