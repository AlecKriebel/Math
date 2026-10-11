"""Own-folder, genuine-process reproduction; no repository or external mutations."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import zipfile

A = Path(__file__).resolve().parent
P = A.parent / "publication_package_v3"
PRIVATE = A / "private"
PRIVATE.mkdir(exist_ok=False)
EXTRACT = PRIVATE / "extracted"
EXTRACT.mkdir()
SHA = lambda body: hashlib.sha256(body).hexdigest()
NOW = lambda: dt.datetime.now(dt.timezone.utc).isoformat()
def bind(path):
    body = path.read_bytes()
    return {"bytes": len(body), "sha256": SHA(body)}
source = Path(__file__).read_bytes()
(A / "PRELAUNCH_REPRODUCTION_SOURCE.py").write_bytes(source)
receipts = []
def run(name, argv, cwd=EXTRACT, expected=0):
    started = NOW()
    child = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.DEVNULL,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = child.communicate()
    record = {"name": name, "argv": list(map(str, argv)), "cwd": str(cwd),
              "child_pid": child.pid, "started_utc": started, "finished_utc": NOW(),
              "separately_instrumented_child_timestamps": False, "exit_code": child.returncode,
              "stdin_supplied": False}
    for label, body in (("stdout", out), ("stderr", err)):
        path = A / (name + "." + label + ".bin")
        path.write_bytes(body)
        record[label] = {"path": path.name, "bytes": len(body), "sha256": SHA(body)}
    receipts.append(record)
    (A / "COMMANDS.json").write_text(json.dumps(receipts, indent=2) + "\n")
    assert child.returncode == expected, record
    return out
pins = {name: bind(P / name) for name in ("even_strand_markov.tex", "even_strand_markov.pdf",
              "even-strand-markov-verification-v3.zip", "zenodo-deposit.json")}
expected_pins = json.loads((A.parent / "qualified_publication_20261004" /
                           "QUALIFIED_INPUT_PINS.json").read_text())["pins"]
assert pins == expected_pins
members = ["LICENSE-CODE.txt", "LICENSE-TEXT.md", "README.md", "SHA256SUMS",
           "SOURCE_QUALIFICATIONS.md", "VERIFICATION_RECORD.json", "build_verification_zip.py",
           "even_strand_markov.tex", "expected_results.json", "verify_even_calculus.py"]
with zipfile.ZipFile(P / "even-strand-markov-verification-v3.zip") as archive:
    assert archive.namelist() == members and archive.testzip() is None
    for member in archive.infolist():
        assert member.date_time == (1980, 1, 1, 0, 0, 0)
        assert member.external_attr >> 16 == 0o100644
        body = archive.read(member.filename)
        assert body == (P / member.filename).read_bytes()
        (EXTRACT / member.filename).write_bytes(body)
checksums = dict(row.split("  ", 1)[::-1] for row in (EXTRACT / "SHA256SUMS").read_text().splitlines())
assert set(checksums) == set(members) - {"SHA256SUMS"}
assert all(SHA((EXTRACT / name).read_bytes()) == digest for name, digest in checksums.items())
out = run("checker", ["/usr/bin/python3", "-E", "-B", "verify_even_calculus.py"])
assert out == (EXTRACT / "expected_results.json").read_bytes()
builder_out = run("builder", ["/usr/bin/python3", "-E", "-B", "build_verification_zip.py"])
rebuilt_zip = EXTRACT / "even-strand-markov-verification-v3.zip"
assert rebuilt_zip.read_bytes() == (P / rebuilt_zip.name).read_bytes()
REBUILD = PRIVATE / "rebuilt"
REBUILD.mkdir()
run("tectonic", ["/opt/homebrew/bin/tectonic", "-X", "compile", "--only-cached", "--untrusted",
                  "--keep-logs", "--outdir", str(REBUILD), str(EXTRACT / "even_strand_markov.tex")])
run("original_pdfinfo", ["/opt/homebrew/bin/pdfinfo", str(P / "even_strand_markov.pdf")])
run("rebuilt_pdfinfo", ["/opt/homebrew/bin/pdfinfo", str(REBUILD / "even_strand_markov.pdf")])
original_text = run("original_text", ["/opt/homebrew/bin/pdftotext", "-layout", str(P / "even_strand_markov.pdf"), "-"])
rebuilt_text = run("rebuilt_text", ["/opt/homebrew/bin/pdftotext", "-layout", str(REBUILD / "even_strand_markov.pdf"), "-"])
assert original_text == rebuilt_text
run("original_render", ["/opt/homebrew/bin/pdftoppm", "-r", "150", "-png", str(P / "even_strand_markov.pdf"), str(PRIVATE / "page")])
run("rebuilt_render", ["/opt/homebrew/bin/pdftoppm", "-r", "150", "-png", str(REBUILD / "even_strand_markov.pdf"), str(PRIVATE / "rebuilt-page")])
pages = sorted(PRIVATE.glob("page-*.png"))
assert len(pages) == 5
pixel_pins = {}
for page in pages:
    rebuilt = PRIVATE / ("rebuilt-" + page.name)
    assert page.read_bytes() == rebuilt.read_bytes()
    pixel_pins[page.name] = bind(page)
stress_source = (A / "independent_color_stress.py").read_bytes()
(A / "PRELAUNCH_STRESS_SOURCE.py").write_bytes(stress_source)
stress_out = run("independent_stress", ["/usr/bin/python3", "-E", "-B", str(A / "independent_color_stress.py")])
assert (A / "independent_color_stress.py").read_bytes() == stress_source
current = {name: bind(P / name) for name in pins}
assert current == pins
assert Path(__file__).read_bytes() == source
result = {"schema": "qualified-round2-genuine-reproduction/v1", "completed_utc": NOW(),
          "operator_pid": os.getpid(), "operator_version": sys.version, "input_pins": pins,
          "archive_members": {name: bind(EXTRACT / name) for name in members},
          "checker_output_exact": True, "diagnostic_result": json.loads(out),
          "rebuilt_archive_byte_identical": True, "PDF_source_text_correspondence": True,
          "five_rebuilt_page_pixels_byte_identical": True, "page_pins": pixel_pins,
          "inputs_unchanged": True, "visual_review": "pending personal inspection",
          "source_sha256": SHA(source), "priority_certified": False}
result["independent_stress"] = json.loads(stress_out)
(A / "REPRODUCTION.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
