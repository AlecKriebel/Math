#!/usr/bin/env python3
"""Fresh tiny-fixture package controls; reads candidate but never mutates it."""
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile

OWN = Path(__file__).resolve().parent
ROOT = OWN.parents[2] / "work/pr872_revision_r1"
PORTABLE = ROOT / "publication_20261015/verification_package"
INDEX_PIN = "09b94f08b7b30f4657bd0ed18f6c2ef86c58aec4ab1813badd12078c9cf36444"
START_PIN = "bf4b7f54267ec12bf3ed14bd8ae7410e2e3497943249bdc320bd8108fc9fc9aa"
OUTER_PIN = "02d511d2c24414615006dd1e97e134061c65888955f534c25d1c12e4edc4d8be"
OUTER_START = "57b78a4813329b5964f94879b3fbff796d2e0d1e1298f3889b804117ec06d8fe"


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


need(sha((PORTABLE / "verify_package.py").read_bytes()) == START_PIN, "startup pin")
need(sha((PORTABLE / "check_originals.py").read_bytes()) == "7e5980d58b749c2e017e860b6f8874267b86833e468d2c287330eaa0cf194318", "original checker startup pin")
need(sha((ROOT / "verify_current_publication.py").read_bytes()) == OUTER_START, "outer startup pin")
need(sha((PORTABLE / "package_index.json").read_bytes()) == INDEX_PIN, "index pin")
need(sha((ROOT / "PUBLICATION_MANIFEST.json").read_bytes()) == OUTER_PIN, "outer pin")
api = runpy.run_path(str(PORTABLE / "verify_package.py"))
original_api = runpy.run_path(str(PORTABLE / "check_originals.py"))
records = []


def reject(label, action, reason):
    try:
        action()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        need(reason in str(exc), label + ": wrong rejection " + str(exc))
        records.append({"test": label, "status": "EXPECTED_REJECTION", "reason": str(exc)})
    else:
        raise RuntimeError(label + ": accepted")


def row(path, raw=b""):
    return {"path": path, "bytes": len(raw), "sha256": sha(raw)}


def cli(root, pin, full=False, extra=None):
    command = [sys.executable, "-I", "-S", "-B"] + (["-O"] if sys.flags.optimize else [])
    command += [str(PORTABLE / "verify_package.py"), pin, "--root", str(root)]
    if full:
        command += ["--full"]
    command += extra or []
    return subprocess.run(command, cwd=OWN, capture_output=True, timeout=15)


def cli_reject(label, proc, reason):
    need(proc.returncode == 1 and not proc.stderr, label + ": wrong process status")
    data = json.loads(proc.stdout)
    need(data.get("status") == "REJECTED" and reason in data["reason"], label + ": wrong process reason")
    records.append({"test": label, "status": "EXPECTED_REJECTION", "reason": data["reason"], "exit_code": 1})


for raw in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}', b'{"x":1e9999}'):
    reject("strict-json-" + raw.decode(), lambda raw=raw: api["strict_json"](raw), "JSON")
for path in ("../escape", "/absolute", "a//b", "a/./b", "a\\b", "a:b", "a\x00b", "a/../b", "a\nb"):
    reject("safe-path-" + repr(path), lambda path=path: api["safe_name"](path), "path")
reject("duplicate-inventory", lambda: api["rows_map"]([row("a"), row("a")]), "duplicate")
reject("parent-collision", lambda: api["rows_map"]([row("a"), row("a/b")]), "collision")
for size in (True, -1, api["MAX_FILE"] + 1, 1.5):
    r = row("a"); r["bytes"] = size
    reject("bad-size-" + str(size), lambda r=r: api["rows_map"]([r]), "byte count")
big = [{"path": str(i), "bytes": api["MAX_FILE"], "sha256": "0" * 64} for i in range(3)]
reject("total-size", lambda: api["rows_map"](big), "size limit")

with tempfile.TemporaryDirectory(prefix="tiny-controls-", dir=OWN) as td:
    temp = Path(td)
    tiny = temp / "tiny"; (tiny / "root_evidence").mkdir(parents=True)
    payloads = {"verify_package.py": b"# dummy, never executed\n", "check_originals.py": b"# dummy\n", "root_evidence/SOURCE_MANIFEST.json": b"{}\n"}
    for name, raw in payloads.items():
        (tiny / name).write_bytes(raw)
    good = {"schema": "random-property-t-verification-v1", "problem_id": "30006628", "files": [row(n, b) for n, b in payloads.items()]}

    def setindex(raw):
        (tiny / "package_index.json").write_bytes(raw)
        return sha(raw)

    goodraw = json.dumps(good).encode()
    pin = setindex(goodraw)
    need(cli(tiny, pin).returncode == 0, "tiny positive")
    records.append({"test": "tiny-positive-closed-inventory", "status": "PASS"})
    cli_reject("external-index-pin", cli(tiny, "0" * 64), "external index pin mismatch")
    for label, raw, reason in [
        ("resealed-duplicate-key", goodraw[:-1] + b',"schema":"random-property-t-verification-v1"}', "duplicate JSON key"),
        ("resealed-nonfinite", goodraw[:-1] + b',"extra":1e9999}', "nonfinite JSON number"),
        ("resealed-unsafe-path", goodraw.replace(b'"check_originals.py"', b'"../check_originals.py"'), "unsafe relative path"),
        ("resealed-duplicate-row", json.dumps({**good, "files": good["files"] + [good["files"][0]]}).encode(), "duplicate inventory path"),
    ]:
        cli_reject(label, cli(tiny, setindex(raw)), reason)
    pin = setindex(goodraw)
    (tiny / "extra").mkdir()
    cli_reject("extra-empty-directory", cli(tiny, pin), "unlisted directory")
    (tiny / "extra").rmdir()
    (tiny / "extra.txt").write_bytes(b"x")
    cli_reject("extra-file", cli(tiny, pin), "unlisted file")
    (tiny / "extra.txt").unlink()
    (tiny / "check_originals.py").unlink()
    cli_reject("missing-file", cli(tiny, pin), "missing inventory file")
    external = temp / "external.py"; external.write_bytes(payloads["check_originals.py"])
    (tiny / "check_originals.py").symlink_to(external)
    cli_reject("internal-leaf-alias", cli(tiny, pin), "nonregular inventory entry")
    (tiny / "check_originals.py").unlink()
    os.mkfifo(tiny / "check_originals.py")
    cli_reject("internal-fifo-no-hang", cli(tiny, pin), "nonregular inventory entry")
    (tiny / "check_originals.py").unlink(); (tiny / "check_originals.py").write_bytes(payloads["check_originals.py"])
    (tiny / "root_evidence").rename(temp / "stored")
    (tiny / "root_evidence").symlink_to(temp / "stored", target_is_directory=True)
    cli_reject("internal-directory-alias", cli(tiny, pin), "nonregular inventory entry")
    (tiny / "root_evidence").unlink(); (temp / "stored").rename(tiny / "root_evidence")
    # Screen declared size before read and forbid regular-file confusion with FIFO/leaf aliases.
    reject("bounded-read-small-limit", lambda: api["read_regular"](external, limit=1), "size limit")
    reject("pinned-size-before-read", lambda: api["read_regular"](external, expected_size=999), "byte count mismatch")
    fifo = temp / "fifo"; os.mkfifo(fifo)
    reject("direct-fifo", lambda: api["read_regular"](fifo), "nonregular input")
    alias = temp / "alias"; alias.symlink_to(external)
    reject("direct-leaf-alias", lambda: api["read_regular"](alias), "nonregular input")
    # The full authentic small package is about 1 MB, not the optional large source corpora.
    copied = temp / "copied"; shutil.copytree(PORTABLE, copied)
    marker = temp / "executed-marker"
    (copied / "check_originals.py").write_text("from pathlib import Path\nPath(" + repr(str(marker)) + ").write_text('executed')\n")
    cli_reject("changed-inner-code-before-execution", cli(copied, INDEX_PIN, full=True), "byte count mismatch")
    need(not marker.exists(), "changed inner code executed")
    records[-1]["marker_absent"] = True
    # Optional input preflight rejects a FIFO without reading any large source.
    _, members, _ = original_api["original_inputs"](PORTABLE)
    sources = {"catalog": fifo, "problems": external, "reports": external, "pdf_dir": temp}
    reject("optional-source-fifo-preflight", lambda: original_api["supplied_inputs"](members, sources), "nonregular input")
    sources["catalog"] = alias
    reject("optional-source-leaf-alias-preflight", lambda: original_api["supplied_inputs"](members, sources), "nonregular input")
    sources["catalog"] = external
    reject("optional-source-wrong-size-preflight", lambda: original_api["supplied_inputs"](members, sources), "byte count mismatch")

result = {"status": "PASS", "mode": "optimized" if sys.flags.optimize else "normal", "tests": len(records), "records": records,
          "candidate_changed": False, "large_source_replay": False, "disposable_fixtures_removed": True}
print(json.dumps(result, sort_keys=True, indent=2))
