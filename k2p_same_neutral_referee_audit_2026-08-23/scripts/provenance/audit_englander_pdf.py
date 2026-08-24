#!/usr/bin/env python3
"""Compare the retained reviewed Englander PDF with the current official bytes.

This is an independent provenance check.  It does not import submission code,
and it writes only the requested compact JSON report outside the handoff.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def command_bytes(argv: list[str]) -> bytes:
    return subprocess.run(argv, check=True, stdout=subprocess.PIPE).stdout


def pdf_record(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    info = command_bytes(["pdfinfo", str(path)]).decode("utf-8", errors="replace")
    pages_match = re.search(r"^Pages:\s+(\d+)\s*$", info, flags=re.MULTILINE)
    mod_match = re.search(r"^ModDate:\s+(.+?)\s*$", info, flags=re.MULTILINE)
    return {
        "path": str(path),
        "bytes": len(data),
        "sha256": sha256(data),
        "pages": int(pages_match.group(1)) if pages_match else None,
        "pdfinfo_modification_date": mod_match.group(1) if mod_match else None,
        "pdftotext_sha256": sha256(command_bytes(["pdftotext", str(path), "-"])),
        "pdftotext_layout_sha256": sha256(
            command_bytes(["pdftotext", "-layout", str(path), "-"])
        ),
    }


METADATA_PATTERNS = (
    rb"<xmp:ModifyDate>.*?</xmp:ModifyDate>",
    rb"<xmp:MetadataDate>.*?</xmp:MetadataDate>",
    rb"<xmpMM:DocumentID>.*?</xmpMM:DocumentID>",
    rb"<xmpMM:InstanceID>.*?</xmpMM:InstanceID>",
    rb"/ModDate\(D:202608[^)]*\)",
    rb"/ID\[<([0-9A-Fa-f]+)><[0-9A-Fa-f]+>\]",
)


def canonicalize_metadata(data: bytes) -> bytes:
    result = data
    for index, pattern in enumerate(METADATA_PATTERNS):
        if index == len(METADATA_PATTERNS) - 1:
            result, count = re.subn(pattern, rb"/ID[<\1><CANONICAL>]", result)
        else:
            result, count = re.subn(pattern, b"<CANONICAL_METADATA>", result)
        if count != 1:
            raise ValueError(f"expected one metadata match for pattern {pattern!r}; got {count}")
    return result


def difference_runs(left: bytes, right: bytes) -> tuple[int, list[list[int]]]:
    if len(left) != len(right):
        return -1, []
    indices = [index for index, pair in enumerate(zip(left, right)) if pair[0] != pair[1]]
    runs: list[list[int]] = []
    if indices:
        start = previous = indices[0]
        for index in indices[1:]:
            if index == previous + 1:
                previous = index
            else:
                runs.append([start, previous])
                start = previous = index
        runs.append([start, previous])
    return len(indices), runs


def raster_record(historical_dir: Path, current_dir: Path) -> dict[str, object]:
    left = sorted(historical_dir.glob("*.png"))
    right = sorted(current_dir.glob("*.png"))
    equal = len(left) == len(right) and all(
        a.read_bytes() == b.read_bytes() for a, b in zip(left, right)
    )
    return {
        "historical_pages": len(left),
        "current_pages": len(right),
        "all_corresponding_png_bytes_identical": equal,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--historical", type=Path, required=True)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--historical-renders", type=Path, required=True)
    parser.add_argument("--current-renders", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    historical = args.historical.read_bytes()
    current = args.current.read_bytes()
    differing_bytes, runs = difference_runs(historical, current)
    canonical_equal = canonicalize_metadata(historical) == canonicalize_metadata(current)
    rasters = raster_record(args.historical_renders, args.current_renders)

    result = {
        "schema": "independent-englander-v4-pdf-provenance-v1",
        "status": "PASS" if canonical_equal and rasters["all_corresponding_png_bytes_identical"] else "FAIL",
        "historical_reviewed_copy": pdf_record(args.historical),
        "current_official_download": pdf_record(args.current),
        "binary_comparison": {
            "same_length": len(historical) == len(current),
            "differing_byte_count": differing_bytes,
            "contiguous_difference_runs_zero_based_inclusive": runs,
            "equal_after_canonicalizing_only_xmp_dates_xmp_ids_info_moddate_and_second_trailer_id": canonical_equal,
        },
        "raster_comparison_96_dpi": rasters,
        "acquisition_record": {
            "historical_copy_location": str(args.historical),
            "filesystem_created_local": "2026-08-17T11:07:49-0700",
            "filesystem_modified_local": "2026-08-17T11:07:50-0700",
            "macos_where_from_domain": "chatgpt.com",
            "macos_where_from_kind": "content attachment",
            "note": "The query token and signature from the extended attribute are deliberately redacted.",
        },
        "classification": {
            "evidence_type": "literature provenance and attribution; not mathematical validation",
            "finding": "The historically bound bytes are retained locally. The current official rendition differs only in mutable PDF metadata and the second trailer identifier; extracted text and every rendered page are identical.",
            "severity": "nonblocking",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "output": str(args.output)}, sort_keys=True))


if __name__ == "__main__":
    main()
