#!/usr/bin/env python3
"""Read-only candidate audit; all mutations stay in this review's private scratch."""
import collections
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
DELIVERY = AUDIT / "preprint_v1_0"
KIT = DELIVERY / "verification_kit"
REPO = AUDIT.parents[2]
sys.dont_write_bytecode = True


def require(value, message):
    if not value:
        raise RuntimeError(message)


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check(p, row):
    require(p.is_file() and not p.is_symlink(), "missing/nonregular: " + str(p))
    require(p.stat().st_size == row["bytes"] and digest(p) == row["sha256"], "pin mismatch: " + str(p))


def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2) + "\n")


RECEIPTS = []


def run(argv, cwd, expected=0, label=None, timeout=180):
    p = subprocess.run([str(v) for v in argv], cwd=cwd, capture_output=True, text=True, timeout=timeout)
    row = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "label": label, "argv": [str(v) for v in argv], "cwd": str(cwd),
           "exit_code": p.returncode, "expected_success": expected == 0,
           "stdout": p.stdout, "stderr": p.stderr}
    RECEIPTS.append(row)
    with (HERE / "REPRODUCTION_RECEIPTS.jsonl").open("a") as f:
        f.write(json.dumps(row) + "\n")
    require((p.returncode == 0) == (expected == 0), "unexpected command result: " + str(argv) + ": " + p.stderr[-1200:])
    return p


def history_and_archive():
    frozen = json.loads((HERE / "FROZEN_INPUTS.json").read_text())
    for r in frozen["files"]:
        check(AUDIT / r["path"], r)
    stage = json.loads((KIT / "REPAIR01_STAGE_COPIES.json").read_text())
    for r in stage["files"]:
        check(KIT / r["destination"], r)
        check(AUDIT / r["source_snapshot"], r)
        require((KIT / r["destination"]).read_bytes() == (AUDIT / r["source_snapshot"]).read_bytes(), "stage source mismatch")
    h = json.loads((KIT / "REPAIR01_HISTORY_RESOLUTION.json").read_text())
    groups = collections.defaultdict(list)
    dispositions = collections.Counter()
    for r in h["references"]:
        groups[(r["stage"], r["inventory"])].append(r)
        dispositions[r["disposition"]] += 1
        if r["disposition"] == "exact_captured_stage_or_canonical_copy":
            check(KIT / r["destination"], r)
        else:
            require(r["disposition"] == "omitted" and bool(r["reason"]), "unexplained history omission")
    for (stage_name, inv), rs in groups.items():
        data = json.loads((AUDIT / inv).read_text())["files"]
        prefix = Path(inv).parent.as_posix() + "/" if inv.endswith("/OUTPUT_PINS.json") else ""
        expected = {(prefix + r["path"], r["bytes"], r["sha256"]) for r in data}
        actual = {(r["original_path"], r["bytes"], r["sha256"]) for r in rs}
        require(len(actual) == len(rs) and expected == actual, "history inventory incomplete: " + stage_name)
        require(h["inventory_counts"][stage_name] == len(rs), "history count mismatch")
    ledger = json.loads((KIT / "COPY_EXCLUSION_LEDGER.json").read_text())
    original_copies = omissions = 0
    for r in ledger["files"]:
        check(AUDIT / r["path"], r)
        if r["disposition"] == "byte_identical_copy":
            check(KIT / r["destination"], r)
            original_copies += 1
        else:
            require(r["disposition"] == "omitted" and bool(r["reason"]), "initial omission")
            omissions += 1
    historical = 0
    for r in ledger["historical_pin_references"]:
        node = json.loads((KIT / r["receipt"]).read_text())
        for key in r["json_location"].split("/")[1:]:
            key = key.replace("~1", "/").replace("~0", "~")
            node = node[int(key)] if isinstance(node, list) else node[key]
        require(isinstance(node, dict) and node["sha256"] == r["sha256"], "historical receipt pointer mismatch")
        require(r["historical_reference"] in node.values(), "historical reference mismatch")
        if r["disposition"] == "hash_identical_canonical_copy":
            require(digest(KIT / r["destination"]) == r["sha256"], "historical copy mismatch")
        else:
            require(r["disposition"] == "omitted" and bool(r["reason"]), "historical omission")
        historical += 1
    native = json.loads((DELIVERY / "metadata.json").read_text())
    wrapper = json.loads((DELIVERY / "deposit_metadata.json").read_text())
    require((DELIVERY / "metadata.json").read_bytes() == (KIT / "metadata.json").read_bytes(), "native bare bytes")
    require(set(wrapper) == {"metadata", "files"} and wrapper["metadata"] == native, "native wrapper metadata")
    require(wrapper["files"] == [{"path": "preprint.pdf", "name": "preprint.pdf"}, {"path": "verification_kit.zip", "name": "verification_kit.zip"}], "attachments")
    require((DELIVERY / "preprint.tex").read_bytes() == (KIT / "preprint.tex").read_bytes(), "paper source copy")
    require((DELIVERY / "research_metadata.json").read_bytes() == (KIT / "research_metadata.json").read_bytes(), "custom historic copy")
    require("At the bounded-repair checkpoint on 2026-10-14" in native["notes"] and "had been" in native["notes"], "dated notes")
    names = json.loads((KIT / "ALLOWLIST.json").read_text())["members"]
    require(names == sorted(set(names)), "allowlist")
    filebytes = io.BytesIO()
    with zipfile.ZipFile(filebytes, "w", compression=zipfile.ZIP_STORED) as z:
        for name in names:
            r = zipfile.ZipInfo("verification_kit/" + name, (2026, 10, 14, 0, 0, 0))
            r.create_system = 3
            r.external_attr = 0o100644 << 16
            r.compress_type = zipfile.ZIP_STORED
            r.flag_bits = 0
            z.writestr(r, (KIT / name).read_bytes())
    require(filebytes.getvalue() == (DELIVERY / "verification_kit.zip").read_bytes(), "independent CLOSED ZIP differs")
    with zipfile.ZipFile(DELIVERY / "verification_kit.zip") as z:
        require(z.testzip() is None and z.comment == b"", "ZIP CRC/comment")
        require(z.namelist() == ["verification_kit/" + n for n in names], "ZIP member order")
        for f, name in zip(z.infolist(), names):
            require(not f.is_dir() and f.date_time == (2026,10,14,0,0,0) and f.compress_type == 0 and f.create_system == 3 and f.external_attr == 0o100644 << 16, "ZIP header")
            require(z.read(f) == (KIT / name).read_bytes(), "ZIP member bytes")
    save("CUSTODY_AND_ARCHIVE_RESULTS.json", {"status": "PASS", "all_frozen_files_unchanged": len(frozen["files"]), "source_equal_stage_copies": len(stage["files"]), "historical_resolutions": len(h["references"]), "resolution_groups": {s: len(rs) for (s, inv), rs in groups.items()}, "resolution_dispositions": dict(dispositions), "initial_ledger_files": len(ledger["files"]), "initial_copies": original_copies, "initial_omissions": omissions, "historical_json_pointers_checked": historical, "archive_members": len(names), "independent_closed_zip_bytes_equal": True, "native_bare_objects_byte_equal_wrapper_metadata_object_equal": True, "pdf_sha256": digest(DELIVERY/"preprint.pdf"), "archive_sha256": digest(DELIVERY/"verification_kit.zip")})


def reseal_member(kit, name):
    # A coherent adversarial mutation in SCRATCH, not a tool for candidate resealing.
    p = kit / "MANIFEST.json"
    data = json.loads(p.read_text())
    for r in data["files"]:
        if r["path"] == name:
            r.update(bytes=(kit/name).stat().st_size, sha256=digest(kit/name))
            break
    else:
        raise RuntimeError("mutation member absent")
    p.write_text(json.dumps(data, indent=2) + "\n")


def runtime():
    (HERE / "private").mkdir(exist_ok=True)
    (HERE / "REPRODUCTION_RECEIPTS.jsonl").write_text("")
    with tempfile.TemporaryDirectory(dir=HERE / "private", prefix="clean-") as temp:
        base = Path(temp)
        with zipfile.ZipFile(DELIVERY/"verification_kit.zip") as z:
            z.extractall(base)
        kit = base/"verification_kit"
        for opt in (False, True):
            prefix = [sys.executable, "-I", "-B"] + (["-O"] if opt else [])
            for script in ("verify.py", "run_checks.py", "fault_checks.py", "output_guard_checks.py"):
                run(prefix+[script], kit, label=("optimized:" if opt else "normal:")+script)
            out = base/("rebuilt-O.zip" if opt else "rebuilt.zip")
            run(prefix+["build_archive.py", "--output", out], kit, label="documented rebuild")
            require(out.read_bytes() == (DELIVERY/"verification_kit.zip").read_bytes(), "rebuild byte mismatch")
            run(prefix+["verify.py", "--require-binding", "--binding", DELIVERY/"EXTERNAL_BINDING.json", "--pdf", DELIVERY/"preprint.pdf", "--archive", out], kit, label="strict relocated binding")
            out.unlink()
            run(prefix+["verify.py", "--require-binding"], kit, expected=1, label="absent required binding")
            # Bootstrap leaf and parent aliases, even with identical bytes.
            bootstrap = kit/"MANIFEST.json"
            original = bootstrap.read_bytes()
            target = base/"identical-manifest.json"
            target.write_bytes(original)
            bootstrap.unlink(); bootstrap.symlink_to(target)
            run(prefix+["verify.py"], kit, expected=1, label="identical bootstrap symlink")
            bootstrap.unlink(); bootstrap.write_bytes(original); target.unlink()
            # Coherently update the internal digest, retaining a wrong scope/disclosure.
            p=kit/"metadata.json"; old=p.read_bytes(); data=json.loads(old)
            data["description"]=data["description"].replace("unrefereed", "refereed")
            p.write_text(json.dumps(data)); reseal_member(kit,"metadata.json")
            run(prefix+["verify.py"], kit, expected=1, label="coherent native scope/disclosure mutation")
            p.write_bytes(old)
            (kit/"MANIFEST.json").write_bytes(original)
            # Coherent false author metadata must also be rejected.
            data=json.loads(old); data["creators"][0]["orcid"]="0000-0000-0000-0000"
            p.write_text(json.dumps(data)); reseal_member(kit,"metadata.json")
            run(prefix+["verify.py"], kit, expected=1, label="coherent native author mutation")
            p.write_bytes(old); (kit/"MANIFEST.json").write_bytes(original)
            # A valid present adjacent binding is checked; use exact delivery files.
            for name in ("EXTERNAL_BINDING.json","metadata.json","research_metadata.json","deposit_metadata.json","CURRENT_STATUS_REPAIR01.json","README.md","preprint.tex","preprint.pdf","verification_kit.zip"):
                os.link(DELIVERY/name, base/name)
            run(prefix+["verify.py"], kit, label="valid adjacent binding strict")
            # Swap only the binding, leaving hard-linked canonical files untouched.
            binding=base/"EXTERNAL_BINDING.json"; binding.unlink(); bad=json.loads((DELIVERY/binding.name).read_text()); bad["pdf"]["sha256"]="0"*64
            binding.write_text(json.dumps(bad))
            run(prefix+["verify.py"], kit, expected=1, label="present binding false PDF digest")
            for name in ("EXTERNAL_BINDING.json","metadata.json","research_metadata.json","deposit_metadata.json","CURRENT_STATUS_REPAIR01.json","README.md","preprint.tex","preprint.pdf","verification_kit.zip"):
                (base/name).unlink()
            run(prefix+["verify.py"], kit, label="restored clean verifier")
        compiled=base/"compiled"; compiled.mkdir()
        run(["tectonic","--outdir",compiled,"preprint.tex"],kit,label="real clean standalone Tectonic compile",timeout=240)
        require((compiled/"preprint.pdf").is_file(), "no compiled PDF")
        run(["pdfinfo",compiled/"preprint.pdf"],kit,label="clean compiled PDF information")
        shutil.copyfile(compiled/"preprint.pdf",HERE/"private/clean_compiled.pdf")
        save("CLEAN_COMPILE_PINS.json",{"source_sha256":digest(kit/"preprint.tex"),"pdf_sha256":digest(compiled/"preprint.pdf"),"bytes":(compiled/"preprint.pdf").stat().st_size,"delivered_pdf_byte_equal":(compiled/"preprint.pdf").read_bytes()==(DELIVERY/"preprint.pdf").read_bytes(),"byte_identity_not_required_by_contract":True})
    run([sys.executable,"-I","-B",REPO/"zenodo_deposit_tool/zenodo.py","check",DELIVERY/"deposit_metadata.json"],REPO,label="actual repository entirely local native manifest check")
    for opt in (False,True):
        prefix=[sys.executable,"-I","-B"]+(["-O"] if opt else [])
        p=run(prefix+[HERE/"independent_checks.py"],HERE,label="fresh independent mathematical controls")
        save("INDEPENDENT_RESULTS_OPTIMIZED.json" if opt else "INDEPENDENT_RESULTS.json",json.loads(p.stdout))
        for fault in ("conjugation","erasing","parity"):
            run(prefix+[HERE/"independent_checks.py",fault],HERE,expected=1,label="fresh mathematical fault:"+fault)
    require(json.loads((HERE/"INDEPENDENT_RESULTS.json").read_text())==json.loads((HERE/"INDEPENDENT_RESULTS_OPTIMIZED.json").read_text()),"independent normal/O mismatch")
    save("REPRODUCTION_SUMMARY.json",{"status":"PASS","commands":len(RECEIPTS),"expected_rejections":sum(r["exit_code"]!=0 for r in RECEIPTS),"all_documented_python_commands_normal_and_optimized":True,"fresh_independent_math_results_normal_and_optimized_equal":True,"candidate_bytes_unchanged":True,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat()})


if __name__=="__main__":
    history_and_archive()
    runtime()
    history_and_archive()
    print(json.dumps({"status":"PASS","commands":len(RECEIPTS)}))
