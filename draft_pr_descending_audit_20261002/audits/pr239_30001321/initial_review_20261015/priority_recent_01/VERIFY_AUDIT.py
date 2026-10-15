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
    expected_authored = {
        str(path.relative_to(BASE))
        for path in BASE.rglob("*")
        if path.is_file()
        and not path.is_relative_to(BASE / "private_reading")
        and path != BASE / "AUTHORED_MANIFEST.json"
    }
    declared_authored = {item["path"] for item in manifest["files"]}
    if expected_authored != declared_authored:
        failures.append("Authored manifest is not the complete authored file set")
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
    historical_seals = list((BASE / "revision_history").glob("*/AUTHORED_MANIFEST.json"))
    for historical_seal in historical_seals:
        historical_manifest = json.loads(historical_seal.read_text())
        for item in historical_manifest["files"]:
            path = historical_seal.parent / item["path"]
            if not path.is_file() or path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]:
                failures.append(f"Historical sealed artifact changed: {path.relative_to(BASE)}")
    print(json.dumps({
        "passed": not failures,
        "authored_files_checked": len(manifest["files"]),
        "private_evidence_files_checked": len(inventory["private_inventory"]),
        "search_batches_checked": len(search["batches"]),
        "queries_checked": search["query_count"],
        "historical_seals_checked": len(historical_seals),
        "full_priority_coverage_found": False,
        "novelty_certified": False,
        "failures": failures,
    }, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
