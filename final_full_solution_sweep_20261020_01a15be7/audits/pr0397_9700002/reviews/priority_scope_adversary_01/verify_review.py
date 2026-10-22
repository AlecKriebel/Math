#!/usr/bin/env python3
"""Read-only verification of this review's seal, frozen inputs and source custody."""
import hashlib
import json
from pathlib import Path
import scope_priority_controls


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    folder = Path(__file__).resolve().parent
    effort = folder.parents[3]
    audit = folder.parents[1]
    seal = json.loads((folder / "MANIFEST.json").read_text())
    assert set(seal["files"]) == {p.name for p in folder.iterdir()
                                 if p.is_file() and p.name != "MANIFEST.json"}
    for name, rec in seal["files"].items():
        path = folder / name
        assert path.stat().st_size == rec["bytes"] and digest(path) == rec["sha256"], name

    inp = json.loads((folder / "INPUT_PROVENANCE.json").read_text())
    assert digest(effort / inp["source_snapshot_relative_to_effort"]) == inp["source_snapshot_sha256"]
    assert digest(folder / inp["duplicate_check_receipt"]) == inp["duplicate_check_receipt_sha256"]
    for rec in inp["files"]:
        path = audit / rec["path"]
        data = path.read_bytes()
        git_blob = hashlib.sha1(("blob " + str(len(data)) + "\0").encode() + data).hexdigest()
        assert len(data) == rec["bytes"] and digest(path) == rec["sha256"]
        assert git_blob == rec["git_blob"]

    private_source_count = 0
    for rec in json.loads((folder / "ACCESS_LEDGER.json").read_text()):
        if rec["access"] == "complete_body":
            path = effort / rec["private_path"]
            assert path.resolve().is_relative_to((effort / "private/pr0397_priority_scope").resolve())
            assert path.stat().st_size == rec["bytes"] and digest(path) == rec["sha256"]
            private_source_count += 1

    query = json.loads((folder / "PUBLIC_ZENODO_QUERY_CHECKS.json").read_text())
    for rec in query["valid_requests"]:
        assert rec["status"] == 200 and rec["total"] == 0
        path = effort / "private/pr0397_priority_scope" / ("zenodo_query_" + rec["raw_sha256"] + ".json")
        assert digest(path) == rec["raw_sha256"]

    assert scope_priority_controls.run() == json.loads((folder / "SCOPE_PRIORITY_CONTROLS.json").read_text())
    print(json.dumps({"all_passed": True, "authored_files": len(seal["files"]),
                      "original_inputs": len(inp["files"]),
                      "private_source_bodies": private_source_count,
                      "public_Zenodo_queries": len(query["valid_requests"]),
                      "scope_priority_controls": 32}, sort_keys=True))


if __name__ == "__main__":
    main()
