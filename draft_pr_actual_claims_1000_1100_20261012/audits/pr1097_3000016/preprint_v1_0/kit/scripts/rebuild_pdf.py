#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import argparse
import json
import os
import shutil
import subprocess
from common import KIT, inventory, fresh_output, sha, require

def main():
    p = argparse.ArgumentParser(description="Compile in a new external directory; canonical paper remains protected")
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()
    inventory()
    compiler = shutil.which("tectonic")
    require(compiler is not None, "Tectonic is required only for PDF regeneration")
    # The directory and every compiler child output are new and outside protected trees.
    out = fresh_output(args.out_dir, is_directory=True)
    shutil.copyfile(KIT / "paper.tex", out / "paper.tex")
    with (out / "compile.stdout.txt").open("xb") as stdout:
        with (out / "compile.stderr.txt").open("xb") as stderr:
            env = dict(os.environ)
            env["SOURCE_DATE_EPOCH"] = "1792022400"  # 2026-10-15 00:00:00 UTC
            run = subprocess.run([compiler, "-X", "compile", "--untrusted", "--only-cached", "--keep-logs", "--keep-intermediates", "--outdir", str(out), str(out / "paper.tex")],
                                 cwd=out, stdout=stdout, stderr=stderr, check=False, env=env)
    require(run.returncode == 0, "compiler failed; inspect external compile receipts")
    log = (out / "paper.log").read_text(errors="replace")
    require("Overfull" not in log, "overfull TeX box")
    require((out / "paper.pdf").is_file(), "compiler produced no PDF")
    print(json.dumps({"status": "PASS", "pdf_sha256": sha(out / "paper.pdf"),
                      "matches_distributed_pdf": sha(out / "paper.pdf") == sha(KIT / "paper.pdf"),
                      "byte_identity_scope": "Observed with the stated compiler/runtime; other TeX versions may differ"}, sort_keys=True))

if __name__ == "__main__":
    main()
