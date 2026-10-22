"""Cached-only, untrusted TeX rebuild into a fresh audit-owned folder."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess

OWN = Path(__file__).resolve().parent
PACKAGE = OWN.parent / "publication_package_v1"


def main():
    out = OWN / "tex_rebuild"
    out.mkdir(exist_ok=False)
    tmp = out / "tmp"
    tmp.mkdir()
    source = PACKAGE / "focal_inverse_area_product.tex"
    if hashlib.sha256(source.read_bytes()).hexdigest() != "963ff712d79aeb471fa22b56d36ac49d62cd3af3cf0090b339e4d5f19f871bca":
        raise RuntimeError("TeX pin changed")
    argv = ["/opt/homebrew/bin/tectonic", "--only-cached", "--untrusted", "--keep-logs", "--outdir", str(out), str(source)]
    env = dict(os.environ)
    env["TMPDIR"] = str(tmp)
    p = subprocess.run(argv, cwd=OWN, env=env, capture_output=True, text=True, timeout=60)
    record = {"utc":datetime.now(timezone.utc).isoformat(),"argv":argv,"cwd":str(OWN),"TMPDIR":str(tmp),"exit":p.returncode,"stdout":p.stdout,"stderr":p.stderr,"source_sha256":hashlib.sha256(source.read_bytes()).hexdigest()}
    (out / "build_run.json").write_text(json.dumps(record,indent=2)+"\n")
    if p.returncode:
        print(json.dumps({"status":"BUILD_FAILED","record":record},indent=2))
        raise SystemExit(1)
    rebuilt = out / "focal_inverse_area_product.pdf"
    extraction = []
    for pdf in (PACKAGE / "focal_inverse_area_product.pdf", rebuilt):
        command = ["/opt/homebrew/bin/pdftotext", "-layout", str(pdf), "-"]
        t = subprocess.run(command,cwd=OWN,capture_output=True,text=True,timeout=60)
        extraction.append({"argv":command,"exit":t.returncode,"stdout":t.stdout,"stderr":t.stderr})
        if t.returncode:
            raise RuntimeError("extraction failed")
    if extraction[0]["stdout"] != extraction[1]["stdout"]:
        raise RuntimeError("Rebuilt PDF text differs")
    (out / "text_comparison.json").write_text(json.dumps({"extractions":extraction,"equal":True},indent=2)+"\n")
    summary = {"status":"PASS","build":"cached-only untrusted", "pdf_text":"identical", "rebuilt_pdf_sha256":hashlib.sha256(rebuilt.read_bytes()).hexdigest(),"rebuilt_pdf_bytes":rebuilt.stat().st_size}
    (out / "SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,sort_keys=True))


if __name__ == "__main__":
    main()
