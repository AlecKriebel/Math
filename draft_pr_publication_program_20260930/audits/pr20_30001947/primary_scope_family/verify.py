"""Read-only integrity checks for this source audit. No network or Git operations."""

import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


own = Path(__file__).resolve().parent
audit = own.parent
snapshot = audit / "source_snapshot"
manifest = json.loads((audit / "snapshot_manifest.json").read_text())
assert manifest["head"] == "7914dfa8c2ddf0efb784a29accc8a05b5a24a690"
assert len(manifest["files"]) == 10
for row in manifest["files"]:
    path = snapshot / row["path"]
    assert digest(path) == row["sha256"], row["path"]
    assert path.stat().st_size == row["bytes"], row["path"]

scope_seal = json.loads((own / "SCOPE_SEAL.json").read_text())
assert digest(own / "SCOPE_SEAL.md") == scope_seal["sha256"]
readiness = json.loads((snapshot / "readiness.json").read_text())
review = json.loads((snapshot / "review/review_summary.json").read_text())
assert digest(snapshot / "SOURCE_STATUS.md") == readiness["reviewed_sha256"]
assert digest(snapshot / "SOURCE_STATUS.md") == review["reviewed_sha256"]
assert digest(snapshot / "review/REVIEW.md") == review["review_sha256"]
assert readiness["budget"]["used_substantive_attempts"] == 1
assert readiness["budget"]["maximum_substantive_attempts"] == 5
assert len((snapshot / "turns.jsonl").read_text().splitlines()) == 1

local_manifest = json.loads((own / "MANIFEST.json").read_text())
for row in local_manifest["files"]:
    path = own / row["path"]
    assert digest(path) == row["sha256"], row["path"]
    assert path.stat().st_size == row["bytes"], row["path"]
listed = {row["path"] for row in local_manifest["files"]}
actual = {
    str(path.relative_to(own))
    for path in own.rglob("*")
    if path.is_file()
    and "tmp" not in path.relative_to(own).parts
    and "__pycache__" not in path.relative_to(own).parts
    and path.name != "MANIFEST.json"
}
assert listed == actual, (listed - actual, actual - listed)

# Optional local cache checks. The ignored foreign cache is not needed to verify
# committed first-party artifacts, but when present its receipt hashes are checked.
cache = own / "tmp/primary_sources"
old_source_names = {
    "owr-2011-56.pdf": "owr_author.pdf",
    "friedman-arxiv.pdf": "2witt_v1.pdf",
    "goresky-pardon-wu.pdf": "gp1989.pdf",
    "friedman-stratwitt.pdf": "stratwitt_current.pdf",
}
for row in json.loads((snapshot / "source_checksums.json").read_text()):
    path = cache / old_source_names[row["file"]]
    if path.exists():
        assert digest(path) == row["sha256"], row["file"]
        assert path.stat().st_size == row["bytes"], row["file"]
checked = 0
for row in json.loads((own / "SOURCE_LEDGER.json").read_text())["receipts"]:
    stem = "owr2011_56" if row["id"] == "OWR" else row["id"]
    candidates = [cache / (stem + extension) for extension in (".pdf", ".html", ".json")]
    present = [path for path in candidates if path.is_file()]
    if present:
        assert any(digest(path) == row["sha256"] for path in present), row["id"]
        checked += 1

print(
    "PASS: ten frozen inputs, original scope seal, note/review digest links, "
    f"first-party audit manifest, and {checked} locally present source receipts. "
    "Original substantive attempts remain 1/5; this audit adds zero."
)
