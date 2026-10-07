#!/usr/bin/env python3
"""Reproduce finite algebra checks and standalone PDF; no geometric certificate."""
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
EPOCH = "1791347194"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    sums = json.loads((ROOT / "SHA256SUMS.json").read_text())
    for name, wanted in sums.items():
        path = ROOT / name
        if not path.is_file() or digest(path) != wanted:
            raise SystemExit(f"Source hash mismatch: {name}")
    compiler = shutil.which("tectonic")
    if not compiler:
        raise SystemExit("Tectonic is required on PATH; verified version is 0.16.9.")
    version = subprocess.check_output([compiler, "--version"], text=True).strip()
    with tempfile.TemporaryDirectory(prefix="k3-moduli-reproduce-") as raw:
        work = Path(raw)
        shutil.copy2(ROOT / "main.tex", work / "main.tex")
        shutil.copytree(ROOT / "checks", work / "checks")
        for code, result in [
            ("verify_local_spin_pairing.py", "local_spin_pairing_certificate.json"),
            ("verify_graph_signs.py", "graph_sign_certificate.json"),
        ]:
            subprocess.run([os.sys.executable, str(work / "checks" / code)],
                           cwd=work, check=True, capture_output=True, text=True)
            actual = json.loads((work / "checks" / result).read_text())
            expected = json.loads((ROOT / "checks" / result).read_text())
            if actual != expected:
                raise SystemExit(f"Certificate mismatch: {result}")
        signs = subprocess.check_output(
            [os.sys.executable, str(work / "checks" / "check_finite_sign_identities.py")],
            cwd=work, text=True).strip()
        if signs != "All 32 + 1600 + 79 finite sign checks passed.":
            raise SystemExit("Unexpected parity-check output")
        env = os.environ.copy()
        env["SOURCE_DATE_EPOCH"] = EPOCH
        env["FORCE_SOURCE_DATE"] = "1"
        build = subprocess.run([compiler, "--keep-logs", "main.tex"],
                               cwd=work, env=env, capture_output=True, text=True)
        if build.returncode:
            raise SystemExit(build.stdout + build.stderr)
        log = (work / "main.log").read_text(errors="replace")
        if "Overfull" in log or "undefined" in log.lower():
            raise SystemExit("Build has an overfull box or undefined reference")
        out = ROOT / "reproduced"
        out.mkdir(exist_ok=True)
        shutil.copy2(work / "main.pdf", out / "paper.pdf")
        report = {"python": platform.python_version(), "compiler": version,
                  "SOURCE_DATE_EPOCH": EPOCH, "source_files_verified": len(sums),
                  "finite_checks": "all passed", "pdf_sha256": digest(out / "paper.pdf"),
                  "scope": "source integrity, finite algebra and compilation only"}
        (out / "reproduction.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
