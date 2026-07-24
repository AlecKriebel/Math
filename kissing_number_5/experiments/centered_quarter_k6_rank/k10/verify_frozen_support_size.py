#!/usr/bin/env python3
"""Verify the exact frozen-K9 orbit size and minimum K10 gluing work."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE.parent / "k9" / "direct_k9_triangle_extension.json"
CORE_PATH = HERE / "estimate_frozen_support_core.cpp"
CERTIFICATE_PATH = HERE / "frozen_support_size.json"
EDGE_KEY = (
    "edge_color_indices_01_02_03_04_05_06_07_08_12_13_14_15_16_17_"
    "18_23_24_25_26_27_28_34_35_36_37_38_45_46_47_48_56_57_58_"
    "67_68_78"
)


def parse_core_output(output: str) -> dict[str, object]:
    result: dict[str, object] = {
        "orbit_size_distribution": {},
        "automorphism_size_distribution": {},
    }
    orbit_sizes = result["orbit_size_distribution"]
    automorphisms = result["automorphism_size_distribution"]
    assert isinstance(orbit_sizes, dict) and isinstance(automorphisms, dict)
    for line in output.splitlines():
        fields = line.split()
        assert fields
        if fields[0] == "orbit_size":
            assert len(fields) == 3
            orbit_sizes[int(fields[1])] = int(fields[2])
        elif fields[0] == "automorphism_size":
            assert len(fields) == 3
            automorphisms[int(fields[1])] = int(fields[2])
        else:
            assert len(fields) == 2
            result[fields[0]] = int(fields[1])
    return result


def run_core(representatives: list[tuple[int, ...]]) -> dict[str, object]:
    compiler = shutil.which("c++")
    assert compiler is not None
    payload = [str(len(representatives))]
    for representative in representatives:
        assert len(representative) == 36
        assert all(0 <= color < 7 for color in representative)
        payload.append(" ".join(map(str, representative)))
    with tempfile.TemporaryDirectory() as directory:
        executable = Path(directory) / "estimate_frozen_support"
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
        "kissing5.centered_quarter_k10_frozen_k9_support_size.v1"
    )
    assert certificate["source_k9_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()
    assert certificate["source_k9_sha256"] == (
        "b0ead73d99ea050a002a36bfd78f549348d37d19244c147228bee26ad692b148"
    )
    core_hash = hashlib.sha256(CORE_PATH.read_bytes()).hexdigest()
    assert certificate["estimation_core_sha256"] == core_hash
    assert core_hash == (
        "429f25da8ed861281a52c84bca56c88ed485ae22e5b52a2361d4960842addc48"
    )

    representatives = [tuple(atom[EDGE_KEY]) for atom in source["atoms"]]
    assert len(representatives) == 51
    observed = run_core(representatives)
    expected = {
        "k9_orbits": 51,
        "labeled_k9_support": 16057440,
        "orbit_size_distribution": {90720: 1, 181440: 12, 362880: 38},
        "automorphism_size_distribution": {1: 38, 2: 12, 4: 1},
        "minimum_k10_color_trials": 112402080,
        "packed_support_bytes_at_16_per_pattern": 256919040,
    }
    assert observed == expected

    exact_counts = certificate["exact_counts"]
    assert exact_counts == {
        "k9_orbits": 51,
        "labeled_k9_support": 16057440,
        "orbit_size_distribution": {
            "90720": 1,
            "181440": 12,
            "362880": 38,
        },
        "automorphism_size_distribution": {
            "1": 38,
            "2": 12,
            "4": 1,
        },
        "minimum_k10_color_trials": 112402080,
        "packed_support_bytes_at_16_per_pattern": 256919040,
    }
    assert exact_counts["minimum_k10_color_trials"] == (
        7 * exact_counts["labeled_k9_support"]
    )
    assert "no obstruction claimed" in certificate["status"]

    return {
        "status": "PASS",
        "scope": "exact size estimate only; full K10 gluing skipped",
        "labeled_k9_support": observed["labeled_k9_support"],
        "minimum_k10_color_trials": observed["minimum_k10_color_trials"],
        "packed_support_mib_at_16_bytes": (
            observed["packed_support_bytes_at_16_per_pattern"] / 2**20
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
