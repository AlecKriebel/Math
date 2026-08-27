#!/usr/bin/env python3
"""Referee-only diagnostic for the first full parameter-transport mutant."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent / "package"
RUNNER = (
    PACKAGE
    / "work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py"
)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    runner = load("referee_parameter_runner", RUNNER)
    verifier = runner.import_path("referee_parameter_verifier", runner.VERIFY_PATH)
    relation_path = runner.HERE / "probe_relation_parameter_transports.jsonl.gz"
    triangle = runner.find(relation_path, lambda row: row["relation"] == "triangle")

    def mutate(row):
        action = next(
            item
            for item in row["edge_actions"]
            if item["mode"] == "ordinary_triangle_local_section"
        )
        action["mode"] = "paired_K2P_product"
        action["s_action"] = action["g_action"] = "match_products"

    with tempfile.TemporaryDirectory(prefix="referee-parameter-triangle-") as temporary:
        root = Path(temporary) / "mutant"
        runner.copy_clean_certificate_tree(root)
        ledger_key = "probe_relations"
        ledger_name = verifier.LEDGER_KEYS[ledger_key]
        ledger = root / ledger_name
        rewritten = root / f".{ledger_name}.mutant"
        metadata = runner.rewrite_complete_ledger(
            ledger,
            rewritten,
            triangle["occurrence_id"],
            mutate,
            verifier,
        )
        os.replace(rewritten, ledger)
        certificate_path = root / "parameter_transport_certificate.json"
        certificate = json.loads(certificate_path.read_text())
        certificate["ledgers"][ledger_key].update(metadata)
        certificate_path.write_bytes(runner.canonical_bytes(certificate) + b"\n")
        mutant_certificate = runner.reseal_certificate(certificate_path, ledger_key)
        verifier.validate_directory(root)
        result, runtime = runner.invoke_production_verifier(root, 1200.0)
        print(
            json.dumps(
                {
                    "returncode": result.returncode,
                    "runtime_seconds": runtime,
                    "stdout": result.stdout,
                    "mutated_ledger_sha256": metadata["sha256"],
                    "mutated_certificate_payload_sha256": mutant_certificate[
                        "payload_sha256"
                    ],
                    "free_bytes_after": os.statvfs(root).f_bavail
                    * os.statvfs(root).f_frsize,
                },
                indent=2,
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
