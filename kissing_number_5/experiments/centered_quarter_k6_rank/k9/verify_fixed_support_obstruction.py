#!/usr/bin/env python3
"""Exact verifier for nonextension of the frozen K8 support to K9.

The Python wrapper authenticates and parses the rational certificates.  Its
exhaustive finite core is self-contained C++20 using only the standard
library; the compact three-bit encoding is exact.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE.parent / "k8" / "direct_k8_triangle_extension.json"
CORE_PATH = HERE / "fixed_support_core.cpp"
CERTIFICATE_PATH = HERE / "fixed_support_obstruction.json"
EDGE_KEY = (
    "edge_color_indices_01_02_03_04_05_06_07_12_13_14_15_16_17_"
    "23_24_25_26_27_34_35_36_37_45_46_47_56_57_67"
)


def parse_core_output(output: str) -> dict[str, object]:
    result: dict[str, object] = {
        "orbit_size_distribution": {},
        "overlap_group_size_distribution": {},
    }
    orbit_sizes = result["orbit_size_distribution"]
    group_sizes = result["overlap_group_size_distribution"]
    assert isinstance(orbit_sizes, dict) and isinstance(group_sizes, dict)
    for line in output.splitlines():
        fields = line.split()
        assert fields
        if fields[0] == "orbit_size":
            assert len(fields) == 3
            orbit_sizes[int(fields[1])] = int(fields[2])
        elif fields[0] == "group_size":
            assert len(fields) == 3
            group_sizes[int(fields[1])] = int(fields[2])
        else:
            assert len(fields) == 2
            result[fields[0]] = int(fields[1])
    return result


def run_core(representatives: list[tuple[int, ...]]) -> dict[str, object]:
    compiler = shutil.which("c++")
    assert compiler is not None
    payload = [str(len(representatives))]
    for representative in representatives:
        assert len(representative) == 28
        assert all(0 <= color < 7 for color in representative)
        payload.append(" ".join(map(str, representative)))
    with tempfile.TemporaryDirectory() as directory:
        executable = Path(directory) / "fixed_support_core"
        compile_result = subprocess.run(
            [
                compiler,
                "-std=c++20",
                "-O3",
                "-DNDEBUG",
                str(CORE_PATH),
                "-o",
                str(executable),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        assert compile_result.returncode == 0, compile_result.stderr
        run_result = subprocess.run(
            [str(executable)],
            input="\n".join(payload) + "\n",
            check=False,
            capture_output=True,
            text=True,
        )
        assert run_result.returncode == 0, run_result.stderr
    return parse_core_output(run_result.stdout)


def verify() -> dict[str, object]:
    source_bytes = SOURCE_PATH.read_bytes()
    source = json.loads(source_bytes)
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    assert certificate["schema"] == (
        "kissing5.centered_quarter_k9_fixed_k8_support_obstruction.v1"
    )
    assert certificate["source_k8_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()
    assert certificate["source_k8_sha256"] == (
        "9499977c14f3de72cd0b55d83872a645f2727f120182d010967832106b65b195"
    )
    core_hash = hashlib.sha256(CORE_PATH.read_bytes()).hexdigest()
    assert certificate["enumeration_core_sha256"] == core_hash
    assert core_hash == (
        "5b143b369ad57f63a646848d74dec19341e478f13ee109d4bd51da8f8789b728"
    )

    representatives = [tuple(atom[EDGE_KEY]) for atom in source["atoms"]]
    weights = [Q(atom["weight"]) for atom in source["atoms"]]
    assert len(representatives) == len(weights) == 51
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    observed = run_core(representatives)
    expected_observed = {
        "k8_orbits": 51,
        "labeled_k8_support": 1824480,
        "orbit_size_distribution": {10080: 1, 20160: 10, 40320: 40},
        "k7_overlap_keys": 1635480,
        "overlap_group_size_distribution": {
            1: 1506960,
            2: 97020,
            3: 15960,
            4: 11340,
            6: 3360,
            8: 630,
            24: 210,
        },
        "compatible_ordered_k8_face_pairs": 2502360,
        "pre_support_k9_color_trials": 17516520,
        "support_compatible_labeled_k9": 0,
    }
    assert observed == expected_observed

    enumeration = certificate["enumeration"]
    assert enumeration == {
        "method": (
            "join two labeled supported K8 faces over their common labeled "
            "K7 face, try all seven colors on the remaining edge, and check "
            "the other seven K8 faces"
        ),
        "k8_orbits": 51,
        "labeled_k8_support": 1824480,
        "orbit_size_distribution": {
            "10080": 1,
            "20160": 10,
            "40320": 40,
        },
        "k7_overlap_keys": 1635480,
        "overlap_group_size_distribution": {
            "1": 1506960,
            "2": 97020,
            "3": 15960,
            "4": 11340,
            "6": 3360,
            "8": 630,
            "24": 210,
        },
        "compatible_ordered_k8_face_pairs": 2502360,
        "pre_support_k9_color_trials": 17516520,
        "support_compatible_labeled_k9": 0,
        "rank_at_most_five_k9_orbits": 0,
    }

    assert weights[26] == Q(
        255486062818504206996978464985143047480098887,
        47175701418398322017174301773892000000000000000,
    )
    target_pairing = -9 * weights[26]
    assert target_pairing == -Q(
        766458188455512620990935394955429142440296661,
        15725233806132774005724767257964000000000000000,
    )
    farkas = certificate["farkas_certificate"]
    assert farkas["dual_vector"] == "-e_26"
    assert farkas["column_pairings"] == []
    assert Q(farkas["target_pairing"]) == target_pairing < 0

    return {
        "status": "PASS",
        "scope": "particular frozen 51-orbit K8 distribution only",
        "labeled_k8_support": observed["labeled_k8_support"],
        "k9_trials_after_k7_join": observed[
            "pre_support_k9_color_trials"
        ],
        "support_compatible_labeled_k9": observed[
            "support_compatible_labeled_k9"
        ],
        "farkas_target_pairing": str(target_pairing),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
