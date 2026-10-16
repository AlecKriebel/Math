"""Read-only integrity checks for the independent recent priority audit.

Run from any directory. Does not download sources, alter files, or contact people.
Third-party bytes are inventoried privately and are excluded from public artifacts.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = json.loads((BASE / "AUTHORED_MANIFEST.json").read_text())
    inventory = json.loads((BASE / "SOURCE_INVENTORY.json").read_text())
    search = json.loads((BASE / "SEARCH_LOG.json").read_text())
    failures: list[str] = []
    for item in manifest["files"]:
        name = item["path"]
        if name.startswith("private_reading/"):
            failures.append(f"Third-party/private file in public manifest: {name}")
        path = BASE / name
        if not path.is_file():
            failures.append(f"Missing authored artifact: {name}")
        elif path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]:
            failures.append(f"Authored artifact changed: {name}")
    for item in inventory["private_inventory"]:
        path = BASE / item["path"]
        if not path.is_file() or path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]:
            failures.append(f"Private evidence changed: {item['path']}")
    for item in search["batches"]:
        path = BASE / item["private_receipt"]
        if not path.is_file() or digest(path) != item["receipt_sha256"]:
            failures.append(f"Search receipt changed: {item['batch']}")
    if sum(len(batch["queries"]) for batch in search["batches"]) != search["query_count"]:
        failures.append("Search count mismatch")
    status = json.loads((BASE / "STATUS.json").read_text())
    target = BASE / status["frozen_target"]["relative_path"]
    if digest(target) != status["frozen_target"]["sha256"]:
        failures.append("Frozen target changed")
    print(json.dumps({
        "passed": not failures,
        "authored_files_checked": len(manifest["files"]),
        "private_evidence_files_checked": len(inventory["private_inventory"]),
        "search_batches_checked": len(search["batches"]),
        "queries_checked": search["query_count"],
        "full_priority_coverage_found": False,
        "novelty_certified": False,
        "failures": failures,
    }, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
