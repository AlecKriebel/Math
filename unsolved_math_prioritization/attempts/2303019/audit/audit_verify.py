#!/usr/bin/env python3
"""Recheck the frozen input and replay finite controls; not a proof verifier.

Usage: python3 audit_verify.py [--publication PATH]
Writes JSON to stdout only. Never changes the publication input directory.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

EXPECTED_MANIFEST = "d21cc63288ee27d315269164446384790c89bda4338c91d3e567e39193f9d822"
EXPECTED_COUNTS = {
    "all_rotation_grid_representatives": 30912,
    "compact_disk_kernel_bound": 10395,
    "geometric_tail": 100,
    "grid_point_has_integral_index": 30912,
    "latest_overwrite_sign": 524288,
    "local_sign_constant": 2,
    "oscillation_margin": 100,
    "overwrite_support": 1048576,
    "overwrite_telescoping": 262144,
    "positive_affine_normalization": 201,
    "positive_oscillation_gap": 3,
    "real_boundary_range": 1048576,
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inspect_input(root):
    manifest_bytes = (root / "MANIFEST.sha256").read_bytes()
    assert sha(manifest_bytes) == EXPECTED_MANIFEST, "Frozen manifest differs"
    hashes = {}
    for line in manifest_bytes.decode("utf-8").splitlines():
        expected, name = line.split(maxsplit=1)
        assert Path(name).name == name, "Unexpected manifest path"
        actual = sha((root / name).read_bytes())
        assert actual == expected, "Frozen payload differs: " + name
        hashes[name] = actual
    assert len(hashes) == 8, "Unexpected payload count"
    return {"manifest_sha256": EXPECTED_MANIFEST, "payload_sha256": hashes}

def main():
    base = Path(__file__).resolve().parent.parent
    default = base / "publication" if (base / "publication").is_dir() else base
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publication", type=Path, default=default)
    args = parser.parse_args()
    root = args.publication.resolve()
    before = inspect_input(root)
    run = subprocess.run(
        [sys.executable, str(root / "controls.py")],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert run.stderr == b"", "Unexpected control stderr"
    assert run.stdout == (root / "validation.json").read_bytes(), "Replay differs"
    replay = json.loads(run.stdout)
    assert replay["result"] == "PASS"
    assert replay["checks"] == EXPECTED_COUNTS
    assert replay["total_assertions"] == sum(EXPECTED_COUNTS.values()) == 2956209
    after = inspect_input(root)
    assert before == after, "Frozen input changed during replay"
    result = {
        "result": "PASS",
        "problem_id": 2303019,
        "scope": "frozen-input integrity and finite-control replay only",
        "universal_proof_machine_verified": False,
        "before": before,
        "after": after,
        "frozen_input_unchanged": True,
        "control_replay_byte_identical": True,
        "control_families": len(EXPECTED_COUNTS),
        "total_assertions": replay["total_assertions"],
        "control_counts": replay["checks"],
        "replay_sha256": sha(run.stdout),
    }
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
