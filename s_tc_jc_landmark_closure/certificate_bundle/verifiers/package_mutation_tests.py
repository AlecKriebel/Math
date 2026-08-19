#!/usr/bin/env python3
"""Mutation-sensitive checks for the curated bundle's finite-universe index.

This runs only in the disposable copy created by ``run_gate.py``.  Every
mutation is restored byte-for-byte before the next check.
"""

from __future__ import annotations

import gzip
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / "verifiers/verify_certificate_bundle.py"


def load_verifier():
    spec = importlib.util.spec_from_file_location("bundle_integrity", VERIFY_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expect_rejection(name: str, action) -> None:
    try:
        action()
    except (AssertionError, OSError, EOFError):
        return
    raise AssertionError(f"mutation was not rejected: {name}")


def mutate_index(transform) -> None:
    path = ROOT / "atlas/ATLAS_INDEX.csv.gz"
    original = path.read_bytes()
    try:
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            lines = handle.readlines()
        changed = transform(lines)
        with path.open("wb") as raw:
            with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as out:
                out.write("".join(changed).encode("utf-8"))
        load_verifier().verify_counts(ROOT)
    finally:
        path.write_bytes(original)


def main() -> None:
    verifier = load_verifier()
    mutations = 0

    expect_rejection("delete_decorated_relation", lambda: mutate_index(lambda lines: lines[:-1]))
    mutations += 1
    expect_rejection("duplicate_decorated_relation", lambda: mutate_index(lambda lines: lines + [lines[-1]]))
    mutations += 1

    def reversed_direction(lines):
        row = lines[1].replace("source_precedes_target", "target_precedes_source", 1)
        return [lines[0], row, *lines[2:]]

    expect_rejection("reverse_source_target", lambda: mutate_index(reversed_direction))
    mutations += 1

    certificate = ROOT / "primary/certificates/core_universe.json"
    original = certificate.read_bytes()
    try:
        certificate.write_bytes(original + b"\n")
        expect_rejection("alter_certificate_bytes", lambda: verifier.verify_manifest(ROOT))
        mutations += 1
    finally:
        certificate.write_bytes(original)

    manifest = ROOT / "ACTIVE_MANIFEST.json"
    original = manifest.read_bytes()
    try:
        manifest.write_bytes(original.replace(b'"version": "1.1.5"', b'"version": "0.0.0"', 1))

        def check_version():
            payload = verifier.verify_manifest(ROOT)
            assert payload["version"] == "1.1.5", "bundle version"

        expect_rejection("alter_bundle_version", check_version)
        mutations += 1
    finally:
        manifest.write_bytes(original)

    verifier.verify_manifest(ROOT)
    verifier.verify_counts(ROOT)
    print(f'{{"mutations_rejected": {mutations}, "status": "VERIFIED"}}')


if __name__ == "__main__":
    main()
