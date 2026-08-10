#!/usr/bin/env python3
"""Replay the clean-room full-boundary atlas into this audit directory.

The loaded implementation was independently written under
``reviews/local_relations`` and imports none of the primary or historical
decorated-atlas modules.  This driver redirects every generated certificate
to the present read/write scope, records the exact implementation hash, and
then regenerates the requested p=4 and p=5 screens from graph templates.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "cleanroom_engine.py"
CERT = HERE / "certificates" / "verified"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_cleanroom():
    text = SOURCE.read_text()
    forbidden = (
        "import primary",
        "from primary",
        "import decorated_atlas",
        "from decorated_atlas",
        "independent.decorated_atlas",
    )
    hits = [needle for needle in forbidden if needle in text]
    if hits:
        raise AssertionError(("clean-room implementation imports forbidden producer code", hits))
    spec = importlib.util.spec_from_file_location("incoming_boundary_cleanroom", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load clean-room atlas")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.CERT = CERT
    CERT.mkdir(parents=True, exist_ok=True)
    return module


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ports", type=int, choices=(4, 5), required=True)
    parser.add_argument("--equal-audit", action="store_true")
    args = parser.parse_args()

    implementation_hash = sha256(SOURCE)
    module = load_cleanroom()
    outgoing = args.ports - 1
    census = module.census_only()
    screen = module.screen_size(outgoing)
    equal = module.equal_audit(outgoing) if args.equal_audit else None
    implementation_hash_after = sha256(SOURCE)
    if implementation_hash_after != implementation_hash:
        raise AssertionError((
            "clean-room source changed during replay",
            implementation_hash,
            implementation_hash_after,
        ))
    write_json(CERT / "cleanroom_census.json", census)
    manifest = {
        "schema": "incoming-boundary-cleanroom-replay-v1",
        "port_count": args.ports,
        "implementation_path": str(SOURCE.relative_to(HERE.parents[1])),
        "implementation_sha256": implementation_hash,
        "implementation_sha256_after": implementation_hash_after,
        "implementation_stable_during_replay": True,
        "forbidden_import_scan": "PASS",
        "census_body_sha256": census["body_sha256"],
        "screen_body_sha256": screen["body_sha256"],
        "equal_audit_body_sha256": equal["body_sha256"] if equal else None,
    }
    write_json(CERT / f"replay_manifest_p{args.ports}.json", manifest)
    print(json.dumps({"manifest": manifest, "screen": screen, "equal": equal}, sort_keys=True))


if __name__ == "__main__":
    main()
