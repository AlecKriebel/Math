"""Owned read-only extraction of the user-provided primary; no ROOT approval."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

base = Path(__file__).resolve().parent
cache = base / "private_inputs"
cache.mkdir(exist_ok=False)
pdf = Path("/Users/alec/Downloads/Some-New-Results-on-Geometric-Transversals.pdf")
def pin(p):
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest(),
        full_mode_07777=format(stat.S_IMODE(p.stat().st_mode),"04o"))
source = pin(pdf)
assert source["bytes"] == 596169
captures = []
for label, argv in [
    ("pdfinfo", ["/opt/homebrew/bin/pdfinfo", str(pdf)]),
    ("pdftotext", ["/opt/homebrew/bin/pdftotext", "-layout", str(pdf), "-"]),
]:
    out = cache / (label+".stdout.bin")
    err = cache / (label+".stderr.bin")
    pre = dict(controller_pid=os.getpid(), utc=datetime.now(timezone.utc).isoformat(),
        argv=argv, source_pdf=source, executable=pin(Path(argv[0])),
        operator_source=pin(Path(__file__)), ROOT_custody=False)
    (cache / (label+".PRELAUNCH.json")).write_text(json.dumps(pre,indent=2,sort_keys=True)+"\n")
    (cache / (label+".PRELAUNCH_SOURCE.py")).write_bytes(Path(__file__).read_bytes())
    with out.open("wb") as stdout, err.open("wb") as stderr:
        child = subprocess.Popen(argv, stdout=stdout, stderr=stderr)
        code = child.wait()
    cap = dict(prelaunch=pre, child_pid=child.pid, exit_code=code,
        end_utc=datetime.now(timezone.utc).isoformat(), stdout=pin(out), stderr=pin(err))
    (cache / (label+".CAPTURE.json")).write_text(json.dumps(cap,indent=2,sort_keys=True)+"\n")
    captures.append(cap)
    if code:
        raise SystemExit(code)
pages = (cache / "pdftotext.stdout.bin").read_text().split("\f")
assert len(pages) == 31 and not pages[-1].strip()
page_index = []
for i, page in enumerate(pages[:-1],1):
    p = cache / ("page_%02d.txt" % i)
    p.write_text(page)
    page_index.append(dict(pdf_page_index=i-1, printed_page=673+i, body=pin(p)))
assert pin(pdf) == source
receipt = dict(schema="pr18-user-provided-full-article-extraction/v1",
    actual_operator_pid=os.getpid(), utc=datetime.now(timezone.utc).isoformat(),
    source=source, pages=30, page_index=page_index, captures=captures,
    ROOT_approval=False, extraction_does_not_imply_personal_reading=True,
    private_inputs_not_redistributed=True, no_new_attempt_or_audit_credit=True)
(base / "EXTRACTION_RECEIPT.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
print(json.dumps(dict(pid=os.getpid(), source=source, pages=30,
    captures=[dict(child_pid=c["child_pid"], exit_code=c["exit_code"],
        stdout_bytes=c["stdout"]["bytes"], stderr_bytes=c["stderr"]["bytes"])
        for c in captures]),indent=2,sort_keys=True))
