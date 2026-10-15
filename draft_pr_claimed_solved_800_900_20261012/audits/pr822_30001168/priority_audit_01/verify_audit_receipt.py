#!/usr/bin/env python3
"""Check saved audit metadata and retained-source hashes; not a priority proof."""
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    base = Path(__file__).resolve().parent
    decision = json.loads((base / "DECISION.json").read_text())
    require(decision["problem_id"] == 30001168, "wrong problem")
    require(decision["worldwide_firstness_certified"] is False, "unsupported firstness")
    require(decision["current_openness_certified"] is False, "unsupported openness")
    require(decision["novel_discovery_eligibility_certified"] is False, "unsupported novelty")
    require(decision["published_construction_plus_standard_tools_and_round_bound_yields_qualitative_negative"] is True,
            "classical construction disposition missing")
    require(decision["n_ge_4_restriction_resolved_or_counted"] is False, "scope drift")
    require(decision["adjacent_problem30001169_resolved_or_counted"] is False, "adjacent scope drift")
    public_count = 0
    for path in base.rglob("*.json"):
        if "private_sources" not in path.relative_to(base).parts:
            json.loads(path.read_text())
            public_count += 1
    manifest = json.loads((base / "CORPUS_MANIFEST.json").read_text())
    for row in manifest["files"]:
        path = (base / row["relative_private_path"]).resolve()
        require(path.is_relative_to(base / "private_sources"), "source escapes private folder")
        require(path.is_file(), "missing source: " + str(path))
        data = path.read_bytes()
        require(len(data) == row["bytes"], "byte-count mismatch: " + str(path))
        require(hashlib.sha256(data).hexdigest() == row["sha256"], "hash mismatch: " + str(path))
    for label in ("record", "author_proof"):
        row = decision["inputs"][label]
        path = Path(row["path"])
        data = path.read_bytes()
        expected_hash = row.get("file_sha256", row.get("sha256"))
        require(len(data) == row["bytes"], "input bytes changed: " + label)
        require(hashlib.sha256(data).hexdigest() == expected_hash, "input hash changed: " + label)
    public_manifest_path = base / "PUBLIC_MANIFEST.json"
    if public_manifest_path.exists():
        public_manifest = json.loads(public_manifest_path.read_text())
        for row in public_manifest["files"]:
            path = (base / row["relative_public_path"]).resolve()
            require(path.is_relative_to(base), "public path escapes audit folder")
            require("private_sources" not in path.relative_to(base).parts, "raw source in public manifest")
            data = path.read_bytes()
            require(len(data) == row["bytes"], "public bytes changed: " + str(path))
            require(hashlib.sha256(data).hexdigest() == row["sha256"], "public hash changed: " + str(path))
    print(json.dumps({"status": "receipt_metadata_and_hashes_pass", "public_json_files": public_count,
                      "retained_private_files": len(manifest["files"]),
                      "meaning": "Integrity and scope metadata only; not a worldwide priority or novelty certificate."},
                     sort_keys=True))


if __name__ == "__main__":
    main()
