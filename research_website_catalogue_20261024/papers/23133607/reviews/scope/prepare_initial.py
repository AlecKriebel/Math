#!/usr/bin/env python3
"""Own source/core byte custody and ordinary four-page PDF views only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat
import subprocess
import sys

A = Path(__file__).resolve().parent
S = A.parents[1] / "sources"
P = A.parents[3]
CORE = P / "verification/supported-cycle-focal-independent-code-audit-sol-20261115/ACTUAL623_QUALIFIED_CORE.json"


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def pin(p):
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "SHA256": hashlib.sha256(b).hexdigest()}


def prepare():
    need(pin(S/"SOURCE_READY.json")["SHA256"] == "34854844ee902600ec563d89501d3878fa303915e9ac1442929feaffef7ec816", "original READY")
    need(pin(S/"SOURCE_READY_SEAL.json")["SHA256"] == "e3175bda643f60efb02575f4bbdefd0f67a5ea89c85a5b7d055d92b80447f012", "original source seal")
    r = json.loads((S/"SOURCE_READY.json").read_bytes())
    m = json.loads((S/"SOURCE_READY_MANIFEST.json").read_bytes())
    files, dirs = [], []
    for p in sorted(S.rglob("*")):
        mode = p.lstat().st_mode
        need(not stat.S_ISLNK(mode), "source symlink")
        if stat.S_ISDIR(mode):
            dirs.append(p.relative_to(S).as_posix())
        else:
            need(stat.S_ISREG(mode), "source special file")
            files.append(pin(p))
    terminals = ["SOURCE_READY_CLOSURE.json","SOURCE_READY_MANIFEST.json","SOURCE_READY_SEAL.json"]
    need(len(files)==97 and len(m["files"])==94 and len(dirs)==9, "97=94+3 whole source files/9dirs")
    need(sorted(Path(e["path"]).relative_to(S).as_posix() for e in files)==sorted([e["path"] for e in m["files"]]+terminals), "exact original source namespace")
    need(dirs==m["directories"], "all original directories")
    for e in m["files"]:
        q = pin(S/e["path"])
        need(q["bytes"]==e["bytes"] and q["SHA256"]==e["SHA256"], "whole original source payload")
    pdf = Path(r["selected_actual_PDF"]["path"])
    tex = Path(r["controlling_TeX"]["extracted_path"])
    need(pin(pdf)["SHA256"]=="9152374e115103db5703b830d9ac45d7e0d9043be5635e1c30243a4023eac626", "actual four-page PDF")
    need(pin(tex)["SHA256"]=="7fc0709331c475b86eff8ee4388f828ae82d3f9b82ba4f272467d2901618efbe" and len(tex.read_bytes().splitlines())==267, "all controlling267 TeX lines")
    need(r["additional_controlling_TeX_sources"]==[] and r["embedded_PDFs"]==[] and len(r["actual_standalone_readers"])==1, "whole controlling manuscript set")
    need(pin(CORE)["bytes"]==13162 and pin(CORE)["SHA256"]=="0f285e35daa206f53aa931946c4bcc6c5b01ae6b4b59a231a861b0a6fe11d104", "root-qualified core contract")
    core = json.loads(CORE.read_bytes())
    need(core["original17_plus_sole_authorized405b_checkpoint"] is True and core["all18_original_unchanged_claim"] is False, "qualified not18original distinction")
    actual_core = []
    for entry in core["files"]:
        p = Path(entry["path"])
        need(p.is_relative_to(P), "core project boundary, no website read")
        actual = pin(p)
        need(actual["bytes"]==entry["bytes"] and actual["SHA256"]==entry["SHA256"], "actual root-qualified core bytes")
        actual_core.append(actual)
    need(len(actual_core)==18 and core["actual_checkpoint_SHA256"]=="405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0", "17 original plus authorized checkpoint")
    (A/"CORE_BINDINGS.json").write_text(json.dumps({"UTC":datetime.now(timezone.utc).isoformat(),"whole_root_contract_binding":pin(CORE),"whole_original_root_contract":core,"actual_byreference_core_files":actual_core,"qualification":"17 original inputs plus sole authorized405b checkpoint helper, not18original unchanged","actual_code_programmes_read_or_executed":False,"generated_caches_opaque_no_immutability_claim":True,"no_duplicate_core_corpus_created":True},indent=2)+"\n")
    (A/"SOURCE_INPUT_MANIFEST.json").write_text(json.dumps({"UTC":datetime.now(timezone.utc).isoformat(),"source_root":str(S),"complete_source_files":files,"exact_complete_source_directories":dirs,"source_payload_count":94,"source_complete_files_including_three_exact_terminals":97,"source_exact_terminals":terminals,"root140_gate":"CLOSED","prior_record140_scientific_body_or_opinion_read":False},indent=2)+"\n")
    (A/"rasters").mkdir(exist_ok=False)
    runs=[]
    for command in [["pdftotext","-layout",str(pdf),str(A/"published-pdf-text.txt")],["pdftoppm","-r","120","-f","1","-l","4","-png",str(pdf),str(A/"rasters/page")],["pdfinfo",str(pdf)]]:
        start=datetime.now(timezone.utc).isoformat()
        result=subprocess.run(command,capture_output=True,text=True)
        runs.append({"actual_command":command,"UTC_started":start,"UTC_completed":datetime.now(timezone.utc).isoformat(),"exit_code":result.returncode,"stdout":result.stdout,"stderr":result.stderr})
        need(result.returncode==0,"ordinary Poppler derivative")
    images=[pin(p) for p in sorted((A/"rasters").glob("page-*.png"))]
    need(len(images)==4,"four fresh own individual rasters")
    (A/"MANUSCRIPT_DERIVATION_RECEIPTS.json").write_text(json.dumps({"actual_PDF":pin(pdf),"actual_controlling_TeX":pin(tex),"actual_ordinary_Poppler_runs":runs,"fresh_own_rasters":images,"scientific_execution":False,"source_or_core_programmes_executed":[]},indent=2)+"\n")
    with (A/"RESEARCH_LOG.md").open("a") as f:
        f.write("\n"+datetime.now(timezone.utc).isoformat()+" —10%: Whole97 original source files/9dirs authenticated, actual qualified17+authorized405b core bound byreference with no caches claim. Four fresh own page rasters/text generated by ordinary Poppler only. Full4PDF/267TeX/4raster reading and independent reconstruction next before code/results/archive/foreign. No primaryGET or scientific execution; root140 CLOSED.\n")
    print(json.dumps({"source_files":97,"source_directories":9,"PDF_pages":4,"TeX_lines":267,"fresh_rasters":4,"qualified_core_originals":17,"separately_authorized_checkpoint":1,"source_or_core_scientific_execution":False,"root140_gate":"CLOSED"}))


if __name__ == "__main__":
    if sys.argv[1:] != ["--prepare"]:
        raise SystemExit("Inert by default; --prepare authenticates custody and creates ordinary own manuscript views only")
    prepare()
