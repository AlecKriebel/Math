#!/usr/bin/env python3
"""Preserved, parameterized first-page detector; this file has not rerun the scan.

Provenance: faithfully regenerated from the inline Python tool-call source used
for the Desktop scan on 2026-10-07. This is not a byte-identical saved copy of that
ephemeral source. The companion desktop_detector_provenance.md records its scope.

Differences from the inline source:
* Required CLI arguments replace the private inventory, output, and root paths.
  Multiple explicitly supplied roots are supported; inventory entries are selected
  once, using lexical containment, then checked against the corresponding real root.
* PATH resolution / optional CLI arguments replace the two machine-specific tool
  paths. Timing and worker constants are configurable with their original defaults.
* The scan is wrapped in a function and invoked through argparse; mutable state is
  function-local rather than global. Tool availability / arguments are validated.
* The output uses a roots list and a privacy-neutral scope description. The original
  matching, directory exclusions, byte-hash deduplication, first-page-only reads,
  candidate metadata, cooperative deadline checks, and aggregate accounting remain.

The deadline is cooperative, as in the original: a blocking filesystem read is
not forcibly interrupted. Subprocesses use bounded timeouts. This detector reads
PDF bytes for hashing, but extracts text from page 1 only and stores no unrelated
extracted text. Candidate paths and metadata are saved only to the requested file.
"""

import argparse
import concurrent.futures
import datetime
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import threading
import time
import unicodedata


EXCLUDED_COMPONENTS = {
    ".git", "node_modules", "credentials", "communications", "private",
    ".cache", "cache", "tmp", "temp", "build", "dist", "generated",
    "__pycache__",
}


def canonical(value):
    return re.sub(
        r"[^a-z0-9]+", " ", unicodedata.normalize("NFKC", value).lower()
    ).strip()


def scan(args):
    with open(args.inventory) as handle:
        all_paths = json.load(handle)
    if not isinstance(all_paths, list):
        raise ValueError("Inventory must be a JSON list of path strings.")

    # Preserve the original lexical selection before any realpath validation.
    root_pairs = [
        (os.path.abspath(os.path.expanduser(root)),
         os.path.realpath(os.path.expanduser(root)))
        for root in args.root
    ]
    paths = []
    path_roots = []
    for path in all_paths:
        if not isinstance(path, str):
            continue
        for lexical_root, real_root in root_pairs:
            if path.startswith(lexical_root.rstrip(os.sep) + os.sep):
                paths.append(path)
                path_roots.append(real_root)
                break

    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    start = time.monotonic()
    deadline = start + args.budget_seconds
    lock = threading.Lock()
    next_index = 0
    results = {}
    hashes = {}
    candidates = []

    def worker():
        nonlocal next_index
        while True:
            with lock:
                if next_index >= len(paths) or time.monotonic() >= deadline:
                    return
                index = next_index
                next_index += 1
            path = paths[index]
            root = path_roots[index]
            result = {"status": "unscanned"}
            try:
                real = os.path.realpath(path)
                if os.path.commonpath([root, real]) != root:
                    result = {
                        "status": "excluded", "reason": "realpath_outside_root"
                    }
                elif any(
                    component.lower() in EXCLUDED_COMPONENTS
                    for component in os.path.relpath(real, root).split(os.sep)[:-1]
                ):
                    result = {
                        "status": "excluded",
                        "reason": "excluded_directory_component",
                    }
                elif not os.path.isfile(real):
                    result = {
                        "status": "failed", "stage": "file_validation",
                        "reason": "not_regular_file",
                    }
                else:
                    digest = hashlib.sha256()
                    with open(real, "rb") as handle:
                        while True:
                            if time.monotonic() >= deadline:
                                raise TimeoutError("overall_budget")
                            chunk = handle.read(1024 * 1024)
                            if not chunk:
                                break
                            digest.update(chunk)
                    sha = digest.hexdigest()
                    with lock:
                        original = hashes.get(sha)
                        if original is None:
                            hashes[sha] = index
                    if original is not None:
                        result = {
                            "status": "duplicate", "sha256": sha,
                            "canonical_index": original,
                        }
                    else:
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            raise TimeoutError("overall_budget")
                        run = subprocess.run(
                            [args.pdftotext, "-f", "1", "-l", "1", "-enc",
                             "UTF-8", real, "-"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            timeout=min(args.per_pdf_timeout_seconds, remaining),
                        )
                        if run.returncode != 0:
                            result = {
                                "status": "failed",
                                "stage": "first_page_extraction",
                                "reason": "pdftotext_nonzero",
                                "exit_code": run.returncode, "sha256": sha,
                            }
                        else:
                            text = run.stdout.decode("utf-8", errors="replace")
                            norm = canonical(text)
                            title_match = (
                                "banach mazur stability of von neumann algebras"
                                in norm
                            )
                            author_match = bool(
                                re.search(r"\bjean\s+roydor\b", norm)
                            )
                            doi_match = (
                                "10.1142/s1793525321500151"
                                in re.sub(
                                    r"\s+", "",
                                    unicodedata.normalize("NFKC", text).lower(),
                                )
                            )
                            result = {
                                "status": "scanned", "sha256": sha,
                                "first_page_text_empty": not bool(text.strip()),
                            }
                            if title_match or author_match or doi_match:
                                candidate = {
                                    "path": path, "realpath": real,
                                    "sha256": sha,
                                    "matches": {
                                        "exact_target_title_normalized": title_match,
                                        "jean_roydor": author_match,
                                        "target_doi": doi_match,
                                    },
                                    "first_page_character_count": len(text),
                                    "first_page_indicators": {
                                        "slides_or_talk": bool(re.search(
                                            r"\b(cirm|slides|workshop|lecture|talk|conference)\b",
                                            norm,
                                        )),
                                        "completely_bounded": "completely bounded" in norm,
                                        "arxiv": "arxiv" in norm,
                                    },
                                    "complete_target_text_established": False,
                                }
                                try:
                                    info = subprocess.run(
                                        [args.pdfinfo, real],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        timeout=min(
                                            args.metadata_timeout_seconds,
                                            max(0.05, deadline - time.monotonic()),
                                        ),
                                    )
                                    if info.returncode == 0:
                                        metadata = {}
                                        for line in info.stdout.decode(
                                            "utf-8", errors="replace"
                                        ).splitlines():
                                            if line.startswith("Pages:"):
                                                metadata["page_count"] = int(
                                                    line.split(":", 1)[1].strip()
                                                )
                                            elif line.startswith("Title:"):
                                                metadata["pdf_title"] = (
                                                    line.split(":", 1)[1].strip()
                                                )
                                        candidate["pdf_metadata"] = metadata
                                except Exception:
                                    candidate["pdf_metadata_status"] = (
                                        "unavailable_within_budget"
                                    )
                                with lock:
                                    candidates.append(candidate)
                                print(json.dumps({"candidate": candidate}), flush=True)
                            del text, norm, run
            except subprocess.TimeoutExpired:
                result = {
                    "status": "failed", "stage": "first_page_extraction",
                    "reason": "per_file_timeout",
                }
            except TimeoutError:
                result = {"status": "unscanned", "reason": "overall_budget"}
            except Exception as error:
                result = {
                    "status": "failed", "stage": "file_or_extraction",
                    "reason": type(error).__name__,
                }
            with lock:
                results[index] = result

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(worker) for _ in range(args.workers)]
        for future in futures:
            future.result()
    for index in range(len(paths)):
        if index not in results:
            results[index] = {"status": "unscanned", "reason": "overall_budget"}

    counts = {
        status: sum(result["status"] == status for result in results.values())
        for status in ["scanned", "duplicate", "failed", "unscanned", "excluded"]
    }
    dedup_scanned = dedup_failed = dedup_unscanned = 0
    for result in results.values():
        if result["status"] == "duplicate":
            status = results[result["canonical_index"]]["status"]
            if status == "scanned":
                dedup_scanned += 1
            elif status == "failed":
                dedup_failed += 1
            else:
                dedup_unscanned += 1

    record = {
        "started_utc": started,
        "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "roots": [real_root for _, real_root in root_pairs],
        "inventory": args.inventory,
        "total_inventory_paths_for_root": len(paths),
        "unique_byte_hashes_obtained": len(hashes),
        "counts": counts,
        "files_covered_by_successful_first_page_scan": counts["scanned"] + dedup_scanned,
        "duplicate_coverage": {
            "of_scanned": dedup_scanned, "of_failed": dedup_failed,
            "of_unscanned": dedup_unscanned,
        },
        "empty_first_pages": sum(
            result.get("first_page_text_empty", False) for result in results.values()
        ),
        "candidates": sorted(candidates, key=lambda candidate: candidate["path"]),
        "failures": [
            {"path": paths[index], **{
                key: value for key, value in result.items() if key != "sha256"
            }}
            for index, result in results.items() if result["status"] == "failed"
        ],
        "method": {
            "scope": (
                "Only supplied inventory entries lexically within explicitly supplied "
                "roots; corresponding realpaths verified within those roots; excluded "
                "directory components enforced."
            ),
            "content_read": (
                "First page only through pdftotext -f 1 -l 1 -enc UTF-8, in memory; "
                "unrelated text neither printed nor stored."
            ),
            "matching": (
                "NFKC, lowercase, nonalphanumeric/whitespace tolerant exact title; "
                "Jean Roydor; exact target DOI with whitespace removed."
            ),
            "deduplication": (
                "Whole-file SHA-256 bytes, first page extracted once per byte-unique PDF."
            ),
            "metadata": "pdfinfo title and page count only for matching candidates.",
            "budget_seconds": args.budget_seconds,
            "per_pdf_timeout_seconds": args.per_pdf_timeout_seconds,
            "workers": args.workers,
        },
        "source_access_gate": (
            "Unsatisfied: first-page candidates alone do not establish complete "
            "target article retrieval/read."
        ),
        "bounded_scan_completion_percent": (
            round(100 * (len(paths) - counts["unscanned"]) / len(paths), 2)
            if paths else 100
        ),
        "mandatory_complete_article_retrieval_read_percent": 0,
    }
    # Exclusive creation preserves the original no-overwrite behavior.
    with open(args.output, "x") as handle:
        json.dump(record, handle, indent=2)
        handle.write("\n")
    print(json.dumps({
        "output": args.output, "elapsed_seconds": record["elapsed_seconds"],
        "total": len(paths), "unique_byte_hashes": len(hashes), "counts": counts,
        "files_covered_by_successful_first_page_scan": (
            record["files_covered_by_successful_first_page_scan"]
        ),
        "empty_first_pages": record["empty_first_pages"],
        "candidate_count": len(candidates),
    }), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", required=True, help="JSON list of supplied PDF paths")
    parser.add_argument("--output", required=True, help="New metadata JSON file; never overwritten")
    parser.add_argument("--root", required=True, action="append", help="Explicitly authorized root; repeatable")
    parser.add_argument("--pdftotext", default=shutil.which("pdftotext"))
    parser.add_argument("--pdfinfo", default=shutil.which("pdfinfo"))
    parser.add_argument("--budget-seconds", type=float, default=115)
    parser.add_argument("--per-pdf-timeout-seconds", type=float, default=4)
    parser.add_argument("--metadata-timeout-seconds", type=float, default=1.5)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    if (
        not args.pdftotext or not args.pdfinfo
        or shutil.which(args.pdftotext) is None
        or shutil.which(args.pdfinfo) is None
    ):
        parser.error("pdftotext and pdfinfo must be on PATH or supplied explicitly")
    time_limits = (
        args.budget_seconds, args.per_pdf_timeout_seconds, args.metadata_timeout_seconds
    )
    if args.workers < 1 or not all(
        math.isfinite(value) and value > 0 for value in time_limits
    ):
        parser.error("Workers must be positive; timeout values must be finite and positive")
    scan(args)


if __name__ == "__main__":
    main()
