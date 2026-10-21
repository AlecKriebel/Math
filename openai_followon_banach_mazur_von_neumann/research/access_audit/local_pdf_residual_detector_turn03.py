#!/usr/bin/env python3
"""Bounded local identity check for the saved unresolved first-page records.

This exact saved source is authored before execution, unlike the earlier
regenerated detector preservation. No root or output path has a private default.
Only the two first physical pages of each selected PDF are eligible for text
extraction, low-resolution rendering, and installed English OCR. Raw extracted
text is held in memory and discarded. Per-path metadata belongs in ignored local
storage; the receipt deliberately contains no research-file paths.
"""

import argparse
import collections
import concurrent.futures
import hashlib
import json
import math
import os
import re
import shutil
import stat
import subprocess
import tempfile
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path


def signals(value):
    normal = unicodedata.normalize("NFKC", value).lower()
    words = re.sub(r"[^a-z0-9]+", " ", normal).strip()
    compact = re.sub(r"\s+", "", normal)
    return {
        "target_title": "banach mazur stability of von neumann algebras" in words,
        "author_name": "jean roydor" in words or "roydor jean" in words,
        "target_doi": "10.1142/s1793525321500151" in compact,
    }


def diagnostic_category(stderr):
    text = stderr.lower()
    if "password" in text:
        return "password_required"
    if any(term in text for term in ["xref", "syntax error", "document stream",
                                     "trailer dictionary", "not a pdf file"]):
        return "pdf_parser_error"
    return "unspecified_tool_error"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--scan", type=Path, required=True,
                        help="Saved original scan JSON; select only its 49 unresolved byte groups")
    parser.add_argument("--tmp-root", type=Path, required=True,
                        help="Project-local ignored temporary image directory")
    parser.add_argument("--metadata", type=Path, required=True,
                        help="Ignored local per-path derived output")
    parser.add_argument("--receipt", type=Path, required=True,
                        help="Path-free aggregate receipt output")
    parser.add_argument("--total-cap", type=float, default=180)
    parser.add_argument("--per-pdf-cap", type=float, default=8)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--expected-count", type=int, default=49)
    args = parser.parse_args()
    if (not math.isfinite(args.total_cap) or not math.isfinite(args.per_pdf_cap)
            or not 0 < args.total_cap <= 180 or not 0 < args.per_pdf_cap <= 8
            or not 1 <= args.workers <= 6):
        parser.error("Require finite total cap <=180, per-PDF cap <=8, and 1..6 workers")
    started = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    overall_deadline = start + args.total_cap
    detector_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    root = args.root.resolve()
    temporary_parent = args.tmp_root.resolve()
    temporary_parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix="fresh-run-", dir=temporary_parent))
    original_bytes = args.scan.read_bytes()
    original = json.loads(original_bytes)
    selected = [record for record in original["header_records"]
                if record["status"] in ["no_first_page_text", "extraction_failed"]]
    if (len(selected) != args.expected_count
            or len({record["sha256"] for record in selected}) != args.expected_count):
        parser.error("Residual source count or uniqueness differs from the specified saved scope")
    if any(not re.fullmatch(r"[0-9a-f]{64}", record["sha256"]) for record in selected):
        parser.error("Residual SHA-256 values must be lowercase hexadecimal hashes")
    tools = {name: shutil.which(name)
             for name in ["pdftotext", "pdfinfo", "pdftoppm", "tesseract"]}
    if not all(tools.values()):
        parser.error("Required tools must already be installed; this script installs nothing")
    environment = os.environ.copy()
    environment["OMP_THREAD_LIMIT"] = "1"
    versions = {}
    for name, argument in [("pdftotext", "-v"), ("pdfinfo", "-v"),
                           ("pdftoppm", "-v"), ("tesseract", "--version")]:
        result = subprocess.run([tools[name], argument], capture_output=True,
                                text=True, timeout=min(4, max(0.001, overall_deadline - time.monotonic())),
                                env=environment)
        versions[name] = (result.stdout + result.stderr).splitlines()[0]

    def inspect(source):
        file_start = time.monotonic()
        deadline = min(overall_deadline, file_start + args.per_pdf_cap)
        record = {"path": source["path"], "original_sha256": source["sha256"],
                  "prior_status": source["status"], "stages": {}, "images": [],
                  "candidate": False}
        image_paths = []

        def remaining():
            left = deadline - time.monotonic()
            if left <= 0:
                raise TimeoutError("per_pdf_or_overall_deadline")
            return left

        def run(command):
            return subprocess.run(command, capture_output=True, text=True,
                                  timeout=remaining(), env=environment)

        def record_text(stage, result):
            facts = {"exit_code": result.returncode,
                     "character_count": len(result.stdout.strip()),
                     "signals": signals(result.stdout)}
            if result.returncode:
                facts["diagnostic_category"] = diagnostic_category(result.stderr)
            record["stages"][stage] = facts
            record["candidate"] |= any(facts["signals"].values())
            return result.returncode == 0 and bool(result.stdout.strip())

        try:
            path = Path(source["path"])
            path.resolve().relative_to(root)
            remaining()
            if not stat.S_ISREG(path.stat().st_mode):
                record["status"] = "not_regular_file"
                return record
            digest = hashlib.sha256()
            with path.open("rb") as file:
                while True:
                    remaining()
                    chunk = file.read(1024 * 1024)
                    if not chunk:
                        break
                    digest.update(chunk)
            current_hash = digest.hexdigest()
            record["current_sha256"] = current_hash
            if current_hash != source["sha256"]:
                record["status"] = "source_hash_changed"
                return record

            info = run([tools["pdfinfo"], str(path)])
            metadata_signals = signals(info.stdout)
            pages = re.search(r"^Pages:\s+(\d+)", info.stdout, re.M)
            page_count = int(pages.group(1)) if pages else None
            record["page_count"] = page_count
            record["stages"]["pdfinfo"] = {"exit_code": info.returncode,
                                             "signals": metadata_signals}
            record["candidate"] |= any(metadata_signals.values())
            if info.returncode:
                category = diagnostic_category(info.stderr)
                record["stages"]["pdfinfo"]["diagnostic_category"] = category
                if category == "password_required":
                    record["status"] = "password_required_no_attempt_to_unlock"
                    return record

            page2_ok = False
            if page_count == 1:
                record["stages"]["page2_text"] = {"status": "no_second_page"}
            else:
                result = run([tools["pdftotext"], "-f", "2", "-l", "2",
                              "-layout", str(path), "-"])
                page2_ok = record_text("page2_text", result)
            if record["candidate"]:
                record["status"] = "candidate_requires_complete_primary_text_check"
                return record

            last_page = 1 if page_count == 1 or page2_ok else 2
            prefix = temporary / source["sha256"]
            render = run([tools["pdftoppm"], "-f", "1", "-l", str(last_page),
                          "-scale-to", "1100", "-gray", "-png", str(path), str(prefix)])
            record["stages"]["render"] = {"exit_code": render.returncode,
                                            "requested_pages": last_page,
                                            "maximum_pixel_dimension": 1100}
            if render.returncode:
                record["stages"]["render"]["diagnostic_category"] = diagnostic_category(render.stderr)
            image_paths = sorted(temporary.glob(source["sha256"] + "-*.png"))
            page1_ok = False
            page2_ocr_ok = False
            for image_path in image_paths:
                page_match = re.search(r"-(\d+)\.png$", image_path.name)
                physical_page = int(page_match.group(1)) if page_match else None
                if physical_page not in [1, 2]:
                    continue
                record["images"].append({"path": str(image_path),
                                          "page": physical_page,
                                          "bytes": image_path.stat().st_size})
                result = run([tools["tesseract"], str(image_path), "stdout",
                              "-l", "eng", "--psm", "11"])
                readable = record_text("page" + str(physical_page) + "_ocr", result)
                if physical_page == 1:
                    page1_ok = readable
                else:
                    page2_ocr_ok = readable
            if record["candidate"]:
                record["status"] = "candidate_requires_complete_primary_text_check"
            elif page1_ok and (page_count == 1 or page2_ok or page2_ocr_ok):
                record["status"] = "first_two_page_identity_checked_no_match"
            elif page1_ok or page2_ok or page2_ocr_ok:
                record["status"] = "partially_checked_no_match"
            elif not image_paths:
                record["status"] = "render_failed_no_readable_first_two_pages"
            else:
                record["status"] = "rendered_but_ocr_empty_or_failed"
        except (TimeoutError, subprocess.TimeoutExpired):
            record["status"] = "per_pdf_or_total_timeout"
        except ValueError:
            record["status"] = "scope_error"
        except Exception as error:
            record["status"] = "execution_error"
            record["error_type"] = type(error).__name__
        finally:
            record["elapsed_seconds"] = round(time.monotonic() - file_start, 3)
            # A timed-out renderer may already have written an incomplete image.
            # The fresh run directory prevents stale images from entering evidence.
            try:
                listed = {image["path"] for image in record["images"]}
                for generated in sorted(temporary.glob(source["sha256"] + "-*.png")):
                    if str(generated) not in listed:
                        page_match = re.search(r"-(\d+)\.png$", generated.name)
                        record["images"].append({
                            "path": str(generated),
                            "page": int(page_match.group(1)) if page_match else None,
                            "bytes": generated.stat().st_size,
                            "ocr_attempted": False,
                        })
                # Retain images only for unresolved or actual candidate identities.
                retained = record.get("status") != "first_two_page_identity_checked_no_match"
                for image in record["images"]:
                    image["retained"] = retained
                    if not retained:
                        try:
                            Path(image["path"]).unlink(missing_ok=True)
                        except OSError as error:
                            image["retained"] = True
                            image["cleanup_error_type"] = type(error).__name__
            except OSError as error:
                record["image_accounting_error_type"] = type(error).__name__
        return record

    records = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(inspect, source) for source in selected]
        for future in concurrent.futures.as_completed(futures):
            records.append(future.result())
    records.sort(key=lambda item: item["original_sha256"])
    elapsed = round(time.monotonic() - start, 3)
    counts = dict(collections.Counter(record["status"] for record in records))
    metadata = {
        "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": elapsed, "root": str(root), "temporary_image_root": str(temporary),
        "original_scan_sha256": hashlib.sha256(original_bytes).hexdigest(),
        "expected_unique_count": args.expected_count, "recorded_unique_count": len(records),
        "prior_status_counts": dict(collections.Counter(record["status"] for record in selected)),
        "status_counts": counts, "candidate_count": sum(record["candidate"] for record in records),
        "caps": {"total_seconds": args.total_cap, "per_pdf_seconds": args.per_pdf_cap,
                 "workers": args.workers}, "tool_versions": versions, "records": records,
    }
    args.metadata.write_text(json.dumps(metadata, indent=2) + "\n")
    receipt = {key: value for key, value in metadata.items()
               if key not in ["root", "temporary_image_root", "records"]}
    receipt.update({
        "detector_filename": Path(__file__).name,
        "detector_sha256": detector_hash,
        "metadata_sha256": hashlib.sha256(args.metadata.read_bytes()).hexdigest(),
        "method": "Only saved unresolved byte hashes; current hash verification; metadata/page2 text; first1-2 page low-resolution render; installed English sparse-text OCR; raw text discarded; no fuzzy matching or OCR completeness claim",
        "render_scale_to_pixels": 1100, "ocr_language": "eng", "ocr_psm": 11,
        "limits": "No global absence conclusion; exact OCR can miss damaged/small/non-English/poorly segmented text; blank or failed extraction remains unresolved; no password unlocking or installation; ordinary local filesystem calls are cooperative and not forcibly interrupted by the subprocess deadline",
        "complete_article_access_established": False,
    })
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"elapsed_seconds": elapsed, "recorded_unique_count": len(records),
                      "status_counts": counts, "candidate_count": metadata["candidate_count"]}, indent=2))


if __name__ == "__main__":
    main()
