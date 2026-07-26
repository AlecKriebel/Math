"""Deterministically construct the exact anchored order-12 k=4 parent CNF."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import tempfile
from pathlib import Path
from typing import Sequence

from .encoding import build_k4_encoding


SCHEMA = "gamma-theta-order12-k4-parent-cnf-v1"
SOURCE_PATHS = (
    "src/synthesis_k4/__init__.py",
    "src/synthesis_k4/encoding.py",
    "src/synthesis_k4/generate.py",
    "math/lemmas/order12_k4_synthesis_target.md",
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".partial",
        dir=path.parent,
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _source_manifest() -> tuple[tuple[str, int, str], ...]:
    campaign = Path(__file__).resolve().parents[2]
    records: list[tuple[str, int, str]] = []
    for relative in SOURCE_PATHS:
        path = campaign / relative
        if not path.is_file():
            raise ValueError(f"missing source {relative}")
        records.append((relative, path.stat().st_size, sha256_file(path)))
    return tuple(records)


def _assert_distinct_paths(
    output: Path, manifest: Path, sources: Sequence[Path]
) -> tuple[Path, Path]:
    resolved_output = output.resolve(strict=False)
    resolved_manifest = manifest.resolve(strict=False)
    if resolved_output == resolved_manifest:
        raise ValueError("CNF and manifest paths collide")
    for source in sources:
        resolved_source = source.resolve(strict=True)
        if resolved_output == resolved_source or resolved_manifest == resolved_source:
            raise ValueError("an output path aliases a trusted source")
        for candidate in (output, manifest):
            try:
                if os.path.samefile(candidate, source):
                    raise ValueError("an output path aliases a trusted source")
            except FileNotFoundError:
                pass
    try:
        if os.path.samefile(output, manifest):
            raise ValueError("CNF and manifest paths collide")
    except FileNotFoundError:
        pass
    return resolved_output, resolved_manifest


def generate(
    *,
    output: Path,
    manifest: Path,
    mode: str = "full",
) -> dict[str, object]:
    """Install a deterministic CNF and a byte-binding JSON manifest."""

    modes = {
        "base": (False, False),
        "bank": (True, False),
        "full": (True, True),
    }
    if mode not in modes:
        raise ValueError("mode must be base, bank, or full")
    source_records = _source_manifest()
    campaign = Path(__file__).resolve().parents[2]
    sources = tuple(campaign / relative for relative, _, _ in source_records)
    output, manifest = _assert_distinct_paths(output, manifest, sources)

    bank, breaker = modes[mode]
    encoding = build_k4_encoding(
        include_coloring_bank=bank,
        include_signature_breaker=breaker,
    )
    payload = encoding.cnf.dimacs_bytes()
    _atomic_write(output, payload)
    installed_sha = sha256_file(output)
    if installed_sha != sha256_bytes(payload):
        raise ValueError("installed CNF bytes changed")

    source_set_payload = "".join(
        f"{relative} {size} {digest}\n"
        for relative, size, digest in source_records
    ).encode("ascii")
    invocation = [
        "/usr/bin/env",
        f"PYTHONPATH={campaign / 'src'}",
        sys.executable,
        "-m",
        "synthesis_k4.generate",
        "--mode",
        mode,
        "--output",
        str(output),
        "--manifest",
        str(manifest),
    ]
    result: dict[str, object] = {
        "schema": SCHEMA,
        "schema_version": 1,
        "claim_status": "NO_MATHEMATICAL_CLAIM",
        "claim_boundary": (
            "Formula construction is not a SAT result and does not exclude "
            "the order-12 parameter-four slice."
        ),
        "order": 12,
        "parameter": 4,
        "graph_encoded_by_edges": "H=complement(G)",
        "connected_graphs_only": True,
        "mode": mode,
        "complete_anchored_coloring_bank": bank,
        "outer_signature_breaker": breaker,
        "variable_count": encoding.cnf.variable_count,
        "clause_count": len(encoding.cnf.clauses),
        "literal_count": encoding.cnf.literal_count,
        "cnf_path": str(output),
        "cnf_size_bytes": len(payload),
        "cnf_sha256": installed_sha,
        "clause_families": [
            {
                "name": record.name,
                "first_clause_zero_based": record.first_clause,
                "clause_count": record.clause_count,
                "literal_count": record.literal_count,
            }
            for record in encoding.clause_families
        ],
        "source_manifest": [
            {"path": relative, "size": size, "sha256": digest}
            for relative, size, digest in source_records
        ],
        "source_set_sha256": sha256_bytes(source_set_payload),
        "python_executable": sys.executable,
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "working_directory": str(campaign),
        "normalized_invocation": invocation,
    }
    _atomic_write(
        manifest,
        (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("base", "bank", "full"), default="full")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    result = generate(
        output=arguments.output,
        manifest=arguments.manifest,
        mode=arguments.mode,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

