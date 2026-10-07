#!/usr/bin/env python3
"""Faithful parameterized regeneration of the original Documents detector.

Provenance: reconstructed from this agent's actual 2026-10-07 execution source.
Changed only fixed root/inventory/output bindings into required CLI arguments,
wrapped execution in main(), exposed original caps as CLI defaults with finite-positive
argument checks, resolved the supplied root, and reduced terminal output to
aggregate status. Selection, initial PDF magic test, whole-
byte SHA-256 deduplication, matching, queue/cap behavior, and saved accounting
are preserved. This saved version has not been run against research PDFs.

The original cap limits scheduling, not total wall time: already submitted
first-page extraction/metadata jobs finish after scheduling stops. An eligible
path must be lexically and physically within the explicitly supplied root.
Inventory exclusions belong to inventory_pdf_paths.py. Do not publish derived
inventories or per-path scan records; they can contain unrelated local paths.
"""

import argparse
import concurrent.futures
import hashlib
import json
import math
import re
import subprocess
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

TITLE = re.compile(r"banach\s*[-–—−]?\s*mazur\s+stability\s+of\s+von\s+neumann\s+algebras", re.I)
DOI = re.compile(r"10\s*\.\s*1142\s*/\s*s1793525321500151", re.I)
AUTHOR = re.compile(r"jean\s+roydor|roydor\s*,\s*jean", re.I)


def inspect_first_page(path, digest, size, per_pdf_cap):
    record = {"path": str(path), "sha256": digest, "bytes": size}
    try:
        result = subprocess.run(
            ["pdftotext", "-f", "1", "-l", "1", "-layout", str(path), "-"],
            capture_output=True, text=True, timeout=per_pdf_cap)
        record["extraction_exit_code"] = result.returncode
        text = unicodedata.normalize("NFKC", result.stdout)
        text = re.sub(r"\s+", " ", text)
        record["first_page_char_count"] = len(text)
        record["target_title"] = bool(TITLE.search(text))
        record["target_doi"] = bool(DOI.search(text))
        record["author_name"] = bool(AUTHOR.search(text))
        if result.returncode:
            record["status"] = "extraction_failed"
        elif not text.strip():
            record["status"] = "no_first_page_text"
        else:
            record["status"] = "header_scanned"
        if record["target_title"] or record["target_doi"] or record["author_name"]:
            info = subprocess.run(["pdfinfo", str(path)], capture_output=True,
                                  text=True, timeout=per_pdf_cap)
            pages = re.search(r"^Pages:\s+(\d+)", info.stdout, re.M)
            record["page_count"] = int(pages.group(1)) if pages else None
            record["match"] = True
        else:
            record["match"] = False
    except subprocess.TimeoutExpired:
        record.update(status="timeout", match=False)
    except Exception as error:
        record.update(status="error", error_type=type(error).__name__, match=False)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True,
                        help="Explicitly authorized research root")
    parser.add_argument("--inventory", type=Path, required=True,
                        help="JSON list from the preserved inventory step")
    parser.add_argument("--output", type=Path, required=True,
                        help="Local ignored derived metadata destination")
    parser.add_argument("--time-cap", type=float, default=180)
    parser.add_argument("--per-pdf-cap", type=float, default=8)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    if (not math.isfinite(args.time_cap) or not math.isfinite(args.per_pdf_cap)
            or args.time_cap <= 0 or args.per_pdf_cap <= 0 or args.workers <= 0):
        parser.error("Caps must be finite and positive; worker count must be positive")
    root = args.root.resolve()
    paths = [Path(item) for item in json.loads(args.inventory.read_text())
             if item.startswith(str(root) + "/")]
    start = time.monotonic()
    started = datetime.now(timezone.utc).isoformat()
    results, duplicates, errors, unscanned = [], [], [], []
    seen, pending = {}, {}
    hashed = 0
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=args.workers)
    try:
        for index, path in enumerate(paths):
            if time.monotonic() - start >= args.time_cap:
                unscanned.extend(str(item) for item in paths[index:])
                break
            try:
                path.resolve().relative_to(root)
                with path.open("rb") as file:
                    magic = file.read(5)
                    if magic != b"%PDF-":
                        errors.append({"path": str(path), "status": "not_pdf_magic"})
                        continue
                    hasher = hashlib.sha256()
                    hasher.update(magic)
                    for chunk in iter(lambda: file.read(1024 * 1024), b""):
                        hasher.update(chunk)
                digest = hasher.hexdigest()
                size = path.stat().st_size
                hashed += 1
            except Exception as error:
                errors.append({"path": str(path), "status": "read_or_scope_error",
                               "error_type": type(error).__name__})
                continue
            if digest in seen:
                duplicates.append({"path": str(path), "canonical_path": seen[digest],
                                   "sha256": digest})
                continue
            seen[digest] = str(path)
            future = pool.submit(inspect_first_page, path, digest, size, args.per_pdf_cap)
            pending[future] = str(path)
            while len(pending) >= 60:
                done, _ = concurrent.futures.wait(
                    pending, return_when=concurrent.futures.FIRST_COMPLETED, timeout=1)
                for future in done:
                    results.append(future.result())
                    pending.pop(future)
                if time.monotonic() - start >= args.time_cap:
                    break
            done = [future for future in pending if future.done()]
            for future in done:
                results.append(future.result())
                pending.pop(future)
        for future in concurrent.futures.as_completed(pending):
            results.append(future.result())
    finally:
        pool.shutdown(wait=True)
    counts = {}
    for record in results:
        counts[record["status"]] = counts.get(record["status"], 0) + 1
    matches = [record for record in results if record.get("match")]
    record = {
        "started_utc": started,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(time.monotonic() - start, 2),
        "root": str(root), "time_cap_seconds": args.time_cap,
        "per_pdf_timeout_seconds": args.per_pdf_cap, "thread_count": args.workers,
        "method": "SHA-256 exact-byte deduplication; PDF magic check; first physical PDF page only via pdftotext, normalized whitespace, exact target title or DOI or Jean Roydor author-name match; no raw unrelated text retained",
        "inventoried_pdf_filenames": len(paths), "hashed_pdf_paths": hashed,
        "unique_pdf_byte_hashes": len(seen), "exact_duplicate_paths": len(duplicates),
        "unique_header_status_counts": counts, "candidate_count": len(matches),
        "candidate_records": matches, "pre_extraction_errors": errors,
        "unscanned_count": len(unscanned), "unscanned_paths": unscanned,
        "header_records": results, "duplicates": duplicates,
    }
    args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({key: record[key] for key in [
        "elapsed_seconds", "inventoried_pdf_filenames", "hashed_pdf_paths",
        "unique_pdf_byte_hashes", "exact_duplicate_paths", "unique_header_status_counts",
        "candidate_count", "unscanned_count"]}, indent=2))


if __name__ == "__main__":
    main()
