#!/usr/bin/env python3
"""Audit the small pinned OAI dependency closure; this is not a Lean checker.

Fetches immutable text sources into the effort's ignored sources directory and
records byte hashes, Git blob hashes, imports, and a placeholder token scan.
Only the OAI closure is fetched; Mathlib is an explicitly uninspected boundary.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import urllib.request

COMMIT = "adc7f1241b42e322a6451854ab7e4b4c146bf78a"
BASE = f"https://raw.githubusercontent.com/openai/math/{COMMIT}/"
ROOTS = [
    "lean/OAI/RingTheory/DirectFiniteness/FinitelyPresented.lean",
    "lean/ComparatorChallenges/KaplanskyFinitelyPresented.lean",
    "lean/ComparatorChallenges/KaplanskyFinitelyPresented.json",
    "lean/ComparatorChallenges/KaplanskyDirectFiniteness.lean",
    "lean/ComparatorChallenges/README.md",
    "lean/lean-toolchain",
    "lean/lakefile.lean",
    "lean/lake-manifest.json",
    "lean/README.md",
    "lean/formalization.yaml",
    "README.md",
    "preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/README.md",
]


def strip_comments(text: str) -> str:
    # Lean block comments nest. Preserve line boundaries for source locations.
    result, pos, depth = [], 0, 0
    while pos < len(text):
        if text.startswith("/-", pos):
            depth += 1
            result.extend("  ")
            pos += 2
        elif depth and text.startswith("-/", pos):
            depth -= 1
            result.extend("  ")
            pos += 2
        elif depth:
            result.append("\n" if text[pos] == "\n" else " ")
            pos += 1
        elif text.startswith("--", pos):
            end = text.find("\n", pos)
            if end == -1:
                result.extend(" " * (len(text) - pos))
                break
            result.extend(" " * (end - pos))
            pos = end
        else:
            result.append(text[pos])
            pos += 1
    if depth:
        raise ValueError("Unterminated block comment")
    return "".join(result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    effort = Path(__file__).resolve().parents[2]
    sources = effort / "sources" / "formal_adc7f124"
    out = Path(__file__).resolve().parent
    seen, queue, records, external, hits = set(), list(ROOTS), {}, set(), []
    stamp = dt.datetime.now(dt.timezone.utc).isoformat()

    def load(path: str) -> tuple[str, bytes]:
        dest = sources / path
        if args.fetch or not dest.exists():
            data = urllib.request.urlopen(BASE + path).read()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        else:
            data = dest.read_bytes()
        return path, data

    while queue:
        batch = sorted(set(queue) - seen)
        queue = []
        seen.update(batch)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            for path, data in pool.map(load, batch):
                records[path] = {
                    "path": path,
                    "url": BASE + path,
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "git_blob_sha1": hashlib.sha1(
                        b"blob " + str(len(data)).encode() + b"\0" + data
                    ).hexdigest(),
                    "observed_utc": stamp,
                }
                if not path.endswith(".lean"):
                    continue
                code = strip_comments(data.decode())
                for match in re.finditer(r"\b(sorry|axiom|admit|unsafe|implemented_by|native_decide)\b", code):
                    hits.append({"path": path, "line": code[:match.start()].count("\n") + 1,
                                 "token": match.group(0)})
                for imports in re.findall(r"^import\s+(.+)$", code, re.M):
                    for module in imports.split():
                        if module.startswith("OAI."):
                            queue.append("lean/" + module.replace(".", "/") + ".lean")
                        else:
                            external.add(module)
    ordered = [records[p] for p in sorted(records)]
    identity = hashlib.sha256("".join(
        record["path"] + " " + record["sha256"] + "\n" for record in ordered
    ).encode()).hexdigest()
    (out / "source_records.json").write_text(json.dumps(ordered, indent=2) + "\n")
    receipt = {
        "commit": COMMIT,
        "observed_utc": stamp,
        "unique_files": len(ordered),
        "total_bytes": sum(r["bytes"] for r in ordered),
        "source_list_sha256": identity,
        "external_import_boundary": sorted(external),
        "placeholder_scan_hits": hits,
        "scope": "Textual source scan only; no Lean elaboration, kernel or comparator check",
    }
    (out / "source_scan_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
