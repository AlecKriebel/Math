#!/usr/bin/env python3
"""Targeted live mutations of the two formerly missing triangle guards."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
OUTPUT = HERE / "canonicalizer_completeness_mutation_certificate.json"


def sha_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_mutation(name, old, new):
    source = ATLAS.read_text()
    if source.count(old) != 1:
        raise SystemExit(f"MUTATION_SITE_FAIL:{name}:{source.count(old)}")
    with tempfile.TemporaryDirectory(prefix=f"k2p-canonicalizer-{name}-") as temporary:
        mutated = Path(temporary) / "k2p_atlas_core.py"
        mutated.write_text(source.replace(old, new))
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(HERE / "canonicalizer_audit.py"),
                "--semantic-only",
                "--atlas",
                str(mutated),
            ],
            cwd=PROJECT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if completed.returncode == 0:
            raise SystemExit(f"MUTATION_SURVIVED:{name}:{completed.stdout[-1000:]}")
        return {
            "name": name,
            "rejected": True,
            "exit_code": completed.returncode,
            "diagnostic_tail": completed.stdout[-500:],
            "mutated_atlas_sha256": sha_file(mutated),
        }


def main():
    if not __debug__:
        raise SystemExit("CANONICALIZER_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    results = [
        run_mutation(
            "accept_nonordinary_split_heads",
            "if not valid or len(headed)!=2 or headed[0]!=headed[1]:continue",
            "if not valid or len(headed)!=2:continue",
        ),
        run_mutation(
            "erase_without_marking_selected_triangle",
            "kind='forgotten_triangle_edge' if forget else 'edge',",
            "kind='edge',",
        ),
    ]
    report = {
        "schema": "k2p-canonicalizer-completeness-mutations-v1",
        "status": "PASS",
        "mutations": results,
        "rejected": len(results),
        "survived": 0,
        "atlas_sha256": sha_file(ATLAS),
        "auditor_sha256": sha_file(HERE / "canonicalizer_audit.py"),
    }
    payload = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("K2P_CANONICALIZER_MUTATIONS_PASS rejected=2 survived=0")


if __name__ == "__main__":
    main()
