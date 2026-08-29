#!/usr/bin/env python3
"""Build the content inventory for the external Tectonic PDF resource cache."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import stat
import sys


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
REPRO = PROJECT / "reproducibility"
if str(REPRO) not in sys.path:
    sys.path.insert(0, str(REPRO))

from release_common import (  # noqa: E402
    atomic_write,
    canonical_json_bytes,
    refuse_optimized_python,
    require,
    sha256_bytes,
    sha256_file,
)


DEFAULT_BUNDLE_URL = "https://relay.fullyjustified.net/default_bundle_v33.tar"
DEFAULT_BUNDLE_DIGEST = (
    "6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c"
)
DEFAULT_OUTPUT = HERE / "TECTONIC_CACHE_MANIFEST.json"


def inventory(cache_root: Path, *, bundle_url: str, bundle_digest: str) -> dict:
    cache_root = cache_root.resolve()
    require(cache_root.is_dir() and not cache_root.is_symlink(),
            ("Tectonic cache root must be a real directory", str(cache_root)))
    rows = []
    for path in sorted(cache_root.rglob("*")):
        relative = path.relative_to(cache_root).as_posix()
        metadata = path.lstat()
        require(not stat.S_ISLNK(metadata.st_mode),
                ("Tectonic cache symlink forbidden", relative))
        if stat.S_ISDIR(metadata.st_mode):
            continue
        require(stat.S_ISREG(metadata.st_mode),
                ("Tectonic cache nonregular object forbidden", relative))
        rows.append({
            "path": relative,
            "bytes": metadata.st_size,
            "sha256": sha256_file(path),
        })
    rows.sort(key=lambda row: row["path"])
    require(rows, "empty Tectonic cache inventory")
    pointer_name = bundle_url.replace(":", ",58,").replace("/", ",47,")
    pointer_path = f"bundles/hashes/{pointer_name}"
    pointer = cache_root / pointer_path
    require(pointer.is_file() and pointer.read_text(encoding="ascii").strip() == bundle_digest,
            ("Tectonic bundle hash pointer", pointer_path, bundle_digest))
    manifest = {
        "schema": "k3p-tectonic-cache-manifest-v1",
        "bundle_url": bundle_url,
        "bundle_digest": bundle_digest,
        "cache_layout": "contents of the Tectonic per-user cache root",
        "bundle_hash_pointer": pointer_path,
        "file_count": len(rows),
        "total_bytes": sum(row["bytes"] for row in rows),
        "files": rows,
    }
    manifest["payload_sha256"] = sha256_bytes(canonical_json_bytes(manifest))
    return manifest


def main(argv: list[str] | None = None) -> int:
    refuse_optimized_python()
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-root", type=Path, required=True)
    parser.add_argument("--bundle-url", default=DEFAULT_BUNDLE_URL)
    parser.add_argument("--bundle-digest", default=DEFAULT_BUNDLE_DIGEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    value = inventory(
        args.cache_root,
        bundle_url=args.bundle_url,
        bundle_digest=args.bundle_digest,
    )
    atomic_write(
        args.output.resolve(),
        (json.dumps(value, indent=2, sort_keys=True) + "\n").encode(),
    )
    print(json.dumps({
        "status": "PASS",
        "output": str(args.output.resolve()),
        "file_count": value["file_count"],
        "total_bytes": value["total_bytes"],
        "payload_sha256": value["payload_sha256"],
    }, sort_keys=True))
    print("K3P_TECTONIC_CACHE_MANIFEST_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
