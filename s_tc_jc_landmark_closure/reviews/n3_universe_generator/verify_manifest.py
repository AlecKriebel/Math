#!/usr/bin/env python3
"""Fast fail-closed semantic and hash check for the n3 universe package."""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def stream_digest(path: Path) -> tuple[int, str]:
    count = 0
    digest = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for line in handle:
            count += 1
            digest.update(line)
    return count, digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    manifest = HERE / "MANIFEST.sha256"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        path = (HERE / relative).resolve()
        require(path.is_file(), f"manifest input missing: {relative}")
        require(sha256(path) == expected, f"manifest hash mismatch: {relative}")

    certificate = json.loads((HERE / "n3_universe_certificate.json").read_text())
    require(certificate["status"] == "VERIFIED", "certificate is not VERIFIED")
    require(all(certificate["checks"].values()), "one universe check is false")
    require(certificate["counts"] == {
        "canonical_merged_relations": 10466,
        "descriptor_cache": 393,
        "marginalized_incoming_completions": 1983,
        "raw_necessary_relations": 10826,
        "selected_incoming_completions": 831,
        "source_supports": 8,
    }, "theorem counts changed")
    require(certificate["independence"]["primary_modules_imported"] == [],
            "primary module import declared")

    raw_count, raw_digest = stream_digest(HERE / "n3_normalized_raw_relations.jsonl.gz")
    merged_count, merged_digest = stream_digest(HERE / "n3_normalized_merged_relations.jsonl.gz")
    require(raw_count == 10826, "raw normalized stream count changed")
    require(merged_count == 10466, "merged normalized stream count changed")
    require(raw_digest == certificate["hashes"]["raw_stream_sha256"],
            "raw normalized stream content changed")
    require(merged_digest == certificate["hashes"]["merged_stream_sha256"],
            "merged normalized stream content changed")
    require(certificate["hashes"]["independent_raw_multiset_sha256"]
            == certificate["hashes"]["primary_raw_multiset_sha256"],
            "raw claim comparison is unequal")
    require(certificate["hashes"]["independent_merged_multiset_sha256"]
            == certificate["hashes"]["primary_merged_multiset_sha256"],
            "merged claim comparison is unequal")

    source = (HERE / "generate_universe.py").read_text(encoding="utf-8")
    require("from primary" not in source and "import primary" not in source,
            "generator imports a primary module")
    require("generate_completions()" in source and "source_support_candidates()" in source,
            "independent grammar entry points missing")
    print(json.dumps({
        "status": "VERIFIED",
        "raw": raw_count,
        "merged": merged_count,
        "raw_multiset_sha256": certificate["hashes"]["independent_raw_multiset_sha256"],
        "merged_multiset_sha256": certificate["hashes"]["independent_merged_multiset_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FALSE: {exc}", file=sys.stderr)
        raise

