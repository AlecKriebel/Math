#!/usr/bin/env python3
"""Build a reproducible source-free author ZIP from an explicit allowlist."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

FILES = ["README.md", "RESEARCH_REPORT.md", "RESEARCH_LOG.md", "TARGET_REVIEW.json",
         "SOURCE_METADATA.json", "PRIOR_ATTEMPT_CHECK.json", "EXACT_CERTIFICATES.json",
         "NUMERIC_RESULTS.json", "NUMERIC_SUMMARY.json", "search_numeric.py",
         "verify_release.py", "test_verifier.py", "freeze.py"]
ROOT = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    output = args.output.resolve()
    if output.parent == ROOT:
        raise ValueError("ZIP must be outside the source package")
    manifest = {"schema": 1, "files": {}}
    for name in FILES:
        p = ROOT / name
        if not p.is_file() or p.is_symlink():
            raise ValueError("missing file or symlink: " + name)
        b = p.read_bytes()
        manifest["files"][name] = {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    (ROOT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True)+"\n")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in sorted(FILES + ["MANIFEST.json"]):
            item = zipfile.ZipInfo(name, date_time=(2000,1,1,0,0,0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.create_system = 3
            item.external_attr = 0o100644 << 16
            z.writestr(item, (ROOT/name).read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    b = output.read_bytes()
    print(json.dumps({"filename":output.name,"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),
                      "files":len(FILES)+1}, sort_keys=True))


if __name__ == "__main__":
    main()
