#!/usr/bin/env python3
"""Parameterized regeneration of the follow-up binary signature check.

The original inspected only paths with a pre-extraction error in the Documents
scan. This preserves its first-1,024-byte classification and status counts;
required CLI arguments replace fixed ignored-project input/output paths. No
file body is stored or printed. The regenerated implementation was not rerun.
"""

import argparse
import collections
import json
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scan", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True,
                        help="Explicitly authorized research root")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    scan = json.loads(args.scan.read_text())
    records = []
    for item in scan["pre_extraction_errors"]:
        path = Path(item["path"])
        try:
            # Added scope recheck for the reusable script; the original input
            # list came solely from the already scope-checked detector.
            path.resolve().relative_to(root)
            with path.open("rb") as file:
                prefix = file.read(1024)
            if b"%PDF-" in prefix:
                status = "pdf_header_after_prefix"
            elif prefix.startswith(b"version https://git-lfs.github.com/spec/v1"):
                status = "git_lfs_pointer"
            elif not prefix:
                status = "empty_file"
            else:
                status = "no_pdf_header_in_first_1024_bytes"
            records.append({"path": str(path), "status": status,
                            "bytes": path.stat().st_size})
        except (OSError, ValueError) as error:
            records.append({"path": str(path), "status": "read_error",
                            "error_type": type(error).__name__})
    output = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "method": "Binary header first1024 bytes only; classify PDF signature/LFS pointer/empty file without saving content",
        "counts": dict(collections.Counter(item["status"] for item in records)),
        "records": records,
    }
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output["counts"]))


if __name__ == "__main__":
    main()
