#!/usr/bin/env python3
"""Reproduce a bundle after strict integrity verification.

The bundle contains original/ and sealed review directories at
reviews/measure_ordinal and reviews/continuity_core. This program writes no
bundle files and does not generate a manifest or certify a mathematical proof.
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys

sys.dont_write_bytecode = True
from integrity import load_json, require, verify_bundle


def typed_equal(actual, expected):
    if type(actual) is not type(expected):
        return False
    if type(actual) is dict:
        return set(actual) == set(expected) and all(
            typed_equal(actual[key], expected[key]) for key in actual)
    if type(actual) is list:
        return len(actual) == len(expected) and all(
            typed_equal(a, b) for a, b in zip(actual, expected))
    return actual == expected


def run_json(root, relative, optimized=False, historical=False):
    program = root / relative
    # -E ignores PYTHONOPTIMIZE; the historical assertion program is always
    # launched without -O and checks __debug__ before executing its source.
    command = [sys.executable, "-E", "-B"]
    if optimized:
        command.append("-O")
    if historical:
        require(not optimized, "historical assertions must run normally")
        command += ["-c", "import runpy,sys\nif not __debug__: raise RuntimeError('assertions disabled')\nrunpy.run_path(sys.argv[1],run_name='__main__')", str(program)]
    else:
        command.append(str(program))
    environment = dict(os.environ)
    # The original verifier starts its own density-check child without -E.
    # Removing this variable ensures that child's assertions also execute.
    environment.pop("PYTHONOPTIMIZE", None)
    proc = subprocess.run(command, cwd=root, text=True, capture_output=True,
                          env=environment)
    require(proc.returncode == 0, "replay failed: %s\n%s" % (relative, proc.stderr))
    return json.loads(proc.stdout), proc.stdout


def reproduce(root, manifest_name="FILES.json"):
    integrity = verify_bundle(root, manifest_name)
    root = pathlib.Path(root).resolve()
    old, _ = run_json(root, "original/verify_public_packet.py", historical=True)
    require(type(old.get("public_files_verified")) is int and
            old["public_files_verified"] == 10, "historical file count mismatch")
    require(type(old.get("finite_identity_checks")) is int and
            old["finite_identity_checks"] == 4240, "historical identity count mismatch")
    replays = {}
    for family in ("measure_ordinal", "continuity_core"):
        relative = "reviews/%s/independent_controls.py" % family
        normal, normal_bytes = run_json(root, relative)
        optimized, optimized_bytes = run_json(root, relative, optimized=True)
        require(normal_bytes == optimized_bytes and typed_equal(normal, optimized),
                "normal/optimized output mismatch: " + family)
        require(normal.get("status") == "PASS", "control status failed: " + family)
        if family == "measure_ordinal":
            expected = load_json(root / "reviews/measure_ordinal/INDEPENDENT_CONTROLS.json")["runs"][0]["stdout"]
            counts = {"exact_finite_checks": 10128, "formal_association_cases": 1728,
                      "exact_convergent_block_color_run_cases": 400,
                      "tail_scale_cases": 1950, "exact_gaussian_density_form_cases": 243,
                      "density_wrong_scale_cases_rejected": 192}
        else:
            expected = load_json(root / "reviews/continuity_core/INDEPENDENT_CONTROLS.normal.json")
            counts = {"finite_words": 19531, "individual_partition_membership_tests": 312496,
                      "nonincreasing_core_words": 462, "all_grid_partitions": 16,
                      "rational_labels": 5, "maximum_finite_word_length": 6,
                      "distinct_coordinate_free_hull_cover_cases": 326,
                      "exact_adjoint_identity_checks": 7203,
                      "zero_time_norm_bound_checks": 384,
                      "properness_geometric_bound_checks": 24}
        for key, value in counts.items():
            require(type(normal.get(key)) is int and normal[key] == value,
                    "exact integer count mismatch: " + family + "/" + key)
        require(typed_equal(normal, expected), "sealed control output mismatch: " + family)
        replays[family] = normal
    return {"integrity": integrity, "historical_normal_mode_only": old,
            "guarded_family_controls_normal_optimized_identical": replays,
            "scope": "Byte integrity and bounded controls; the analytic paper and written reconstructions remain essential."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=pathlib.Path)
    parser.add_argument("--manifest", default="FILES.json")
    args = parser.parse_args()
    try:
        print(json.dumps(reproduce(args.root, args.manifest), indent=2, sort_keys=True))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, "reproduction failure: %s\n" % exc)
