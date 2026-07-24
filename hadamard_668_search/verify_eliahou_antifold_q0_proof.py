#!/usr/bin/env python3
"""Verify the packaged long-q=0 anti-fold UNSAT certificate.

The default audit is dependency-free and checks the certificate metadata,
artifact sizes and hashes, and the complete DIMACS shape.  With ``--full``
it also decompresses the binary DRAT proof to a regular temporary file and
invokes an external ``drat-trim`` executable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROOF_DIR = ROOT / "output" / "antifold42_q0_proof"
CERTIFICATE_PATH = PROOF_DIR / "certificate.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_dimacs(path: Path, variables: int, clauses: int) -> None:
    seen_header = False
    seen_clauses = 0
    largest_variable = 0
    with path.open("rt", encoding="ascii") as source:
        for line_number, line in enumerate(source, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("c"):
                continue
            if stripped.startswith("p"):
                assert not seen_header, "duplicate DIMACS header"
                assert stripped == f"p cnf {variables} {clauses}"
                seen_header = True
                continue
            assert seen_header, f"clause before header at line {line_number}"
            literals = [int(word) for word in stripped.split()]
            assert literals and literals[-1] == 0
            assert 0 not in literals[:-1]
            largest_variable = max(
                largest_variable,
                *(abs(literal) for literal in literals[:-1]),
            )
            seen_clauses += 1
    assert seen_header
    assert seen_clauses == clauses, (seen_clauses, clauses)
    assert largest_variable == variables, (largest_variable, variables)


def audit_metadata() -> dict:
    certificate = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    assert certificate["schema"] == (
        "eliahou-antifold42-q0-drat-certificate-v1"
    )
    assert certificate["checker"]["status"] == "VERIFIED"
    assert certificate["formula"]["q_block"] == "L"
    assert certificate["formula"]["q_index"] == 0
    assert certificate["formula"]["profile"] is None

    cnf_record = certificate["artifacts"]["cnf"]
    cnf_path = PROOF_DIR / cnf_record["path"]
    assert cnf_path.stat().st_size == cnf_record["bytes"]
    assert sha256(cnf_path) == cnf_record["sha256"]
    audit_dimacs(
        cnf_path,
        cnf_record["variables"],
        cnf_record["clauses"],
    )

    proof_record = certificate["artifacts"]["proof"]
    proof_path = PROOF_DIR / proof_record["compressed_path"]
    assert proof_path.stat().st_size == proof_record["compressed_bytes"]
    assert sha256(proof_path) == proof_record["compressed_sha256"]
    return certificate


def replay_full(
    certificate: dict,
    drat_trim: str,
    zstd: str,
    keep_raw: Path | None,
) -> None:
    cnf_path = PROOF_DIR / certificate["artifacts"]["cnf"]["path"]
    proof_record = certificate["artifacts"]["proof"]
    compressed_path = PROOF_DIR / proof_record["compressed_path"]

    if keep_raw is None:
        temporary = tempfile.TemporaryDirectory(
            prefix="antifold42-q0-proof-"
        )
        raw_path = Path(temporary.name) / "antifold_00.drat"
    else:
        temporary = None
        raw_path = keep_raw.resolve()
        raw_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.run(
            [zstd, "-d", "-f", str(compressed_path), "-o", str(raw_path)],
            check=True,
        )
        assert raw_path.is_file()
        assert raw_path.stat().st_size == proof_record["raw_bytes"]
        assert sha256(raw_path) == proof_record["raw_sha256"]
        completed = subprocess.run(
            [drat_trim, str(cnf_path), str(raw_path)],
            check=False,
        )
        assert completed.returncode == 0, (
            f"drat-trim returned {completed.returncode}"
        )
    finally:
        if temporary is not None:
            temporary.cleanup()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--full",
        action="store_true",
        help="decompress and independently replay the binary DRAT proof",
    )
    parser.add_argument(
        "--drat-trim",
        help="path to drat-trim (required for --full unless it is on PATH)",
    )
    parser.add_argument(
        "--zstd",
        help="path to zstd (defaults to the executable on PATH)",
    )
    parser.add_argument(
        "--keep-raw",
        type=Path,
        help="retain the 276 MB decompressed proof at this exact path",
    )
    return parser.parse_args()


def resolve_executable(explicit: str | None, name: str) -> str:
    candidate = explicit or shutil.which(name)
    if candidate is None:
        raise SystemExit(f"{name} is required for --full")
    return candidate


def main() -> None:
    args = parse_args()
    certificate = audit_metadata()
    if args.full:
        replay_full(
            certificate,
            resolve_executable(args.drat_trim, "drat-trim"),
            resolve_executable(args.zstd, "zstd"),
            args.keep_raw,
        )
    print(
        "anti-fold q=0 certificate audit passed "
        f"({'full DRAT replay' if args.full else 'hash and DIMACS audit'})"
    )


if __name__ == "__main__":
    main()
