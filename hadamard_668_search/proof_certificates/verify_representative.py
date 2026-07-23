#!/usr/bin/env python3
"""Regenerate CNFs and check the pinned representative DRAT proofs."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
DEFAULT_MANIFEST = HERE / "representative" / "manifest.json"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def _verify_case(
    name: str,
    record: dict,
    drat_trim: Path,
    temporary: Path,
) -> None:
    artifact = REPOSITORY / record["artifact"]
    artifact_sha256 = _sha256(artifact)
    if artifact_sha256 != record["artifact_sha256"]:
        raise ValueError(
            f"{name}: artifact checksum changed: {artifact_sha256}"
        )
    cnf = temporary / f"{name}.cnf"
    metadata = temporary / f"{name}.metadata.json"
    command = [
        sys.executable,
        str(HERE / "export_seed_frontier_cnf.py"),
        "--artifact",
        str(artifact),
        "--result-index",
        str(record["artifact_result_index"]),
        "--propagation",
        record["propagation"],
        "--output",
        str(cnf),
        "--metadata",
        str(metadata),
    ]
    exported = subprocess.run(
        command, cwd=REPOSITORY, text=True, capture_output=True
    )
    if exported.returncode:
        raise ValueError(
            f"{name}: exporter failed:\n{exported.stdout}{exported.stderr}"
        )
    observed_metadata = json.loads(metadata.read_text(encoding="utf-8"))
    checks = {
        "cnf_sha256": _sha256(cnf),
        "cnf_bytes": cnf.stat().st_size,
        "variables": observed_metadata["variables"],
        "clauses": observed_metadata["clauses"],
        "compression": observed_metadata["compression"],
    }
    for field, observed in checks.items():
        if observed != record[field]:
            raise ValueError(
                f"{name}: regenerated {field} is {observed!r}, "
                f"expected {record[field]!r}"
            )

    compressed = HERE / record["proof"]
    if _sha256(compressed) != record["proof_gzip_sha256"]:
        raise ValueError(f"{name}: compressed proof checksum changed")
    if compressed.stat().st_size != record["proof_gzip_bytes"]:
        raise ValueError(f"{name}: compressed proof size changed")
    proof = temporary / f"{name}.drat"
    with gzip.open(compressed, "rb") as source, proof.open("wb") as destination:
        shutil.copyfileobj(source, destination)
    if _sha256(proof) != record["proof_raw_sha256"]:
        raise ValueError(f"{name}: raw proof checksum changed")
    if proof.stat().st_size != record["proof_raw_bytes"]:
        raise ValueError(f"{name}: raw proof size changed")

    checked = subprocess.run(
        [str(drat_trim), str(cnf), str(proof)],
        cwd=REPOSITORY,
        text=True,
        capture_output=True,
    )
    if checked.returncode or "s VERIFIED" not in checked.stdout:
        raise ValueError(
            f"{name}: drat-trim failed:\n{checked.stdout}{checked.stderr}"
        )
    print(
        f"PASS {name}: regenerated {record['variables']} variables / "
        f"{record['clauses']} clauses; DRAT VERIFIED"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest", type=Path, default=DEFAULT_MANIFEST
    )
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument(
        "--case",
        action="append",
        dest="cases",
        help="case name; repeat as needed (default: every manifest case)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = json.loads(args.manifest.read_text(encoding="utf-8"))
        records = payload["cases"]
        selected = args.cases or list(records)
        unknown = set(selected) - set(records)
        if unknown:
            raise ValueError(f"unknown cases: {sorted(unknown)}")
        if not args.drat_trim.is_file():
            raise ValueError(f"drat-trim not found: {args.drat_trim}")
        with tempfile.TemporaryDirectory(
            prefix="hadamard-668-proof-check-"
        ) as directory:
            temporary = Path(directory)
            for name in selected:
                _verify_case(name, records[name], args.drat_trim, temporary)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"RESULT: {len(selected)} representative proof(s) verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
