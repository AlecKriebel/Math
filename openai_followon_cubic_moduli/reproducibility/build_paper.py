"""Export the standalone source in a clean directory; no third-party Python packages.

Requires Tectonic 0.16.9 (or a compatible version). Example:
  python3 reproducibility/build_paper.py --output rebuilt.pdf
The PDF creation timestamp can vary; compare text as well as source hashes.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    source = project / "main.tex"
    scratch_parent = project / "reproducibility" / "tmp"
    scratch_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="cubic-preprint-", dir=scratch_parent) as location:
        scratch = Path(location)
        shutil.copyfile(source, scratch / "main.tex")
        result = subprocess.run(
            ["tectonic", "--keep-logs", "main.tex"],
            cwd=scratch, text=True, capture_output=True)
        log = (scratch / "main.log").read_text() if (scratch / "main.log").exists() else ""
        if result.returncode or "undefined" in log.lower():
            raise RuntimeError(result.stdout + result.stderr + log)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(scratch / "main.pdf", args.output)
    receipt = {
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "compiler": subprocess.check_output(["tectonic", "--version"], text=True).strip(),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "pdf_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
        "bytes": args.output.stat().st_size,
        "clean_build_exit": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "undefined_reference": False,
    }
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
