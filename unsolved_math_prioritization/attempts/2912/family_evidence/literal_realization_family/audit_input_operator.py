#!/usr/bin/env python3
"""Reviewer authored READ-ONLY original-input closure operator.
Copies and byte-binds inputs as excluded foreign evidence. Never imports,
compiles or executes any candidate/historical helper. This is a content
integrity/read coverage check, not a scientific control or new attempt.
"""
from pathlib import Path
import hashlib,json,os,datetime
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
SNAP=AUDIT/"source_snapshot_v2"
MANIFEST=AUDIT/"snapshot_manifest_v2.json"
DIFF=AUDIT/"original_diff_v2.patch"
manifest=json.loads(MANIFEST.read_text())
expected_head="c772dc5b851ec91da9d46d534577609e5d3ca389"
expected_base="01358d66fc67d1c462bddf31c0d4ee5b120e6737"
assert manifest["head"]==expected_head and manifest["base"]==expected_base
assert len(manifest["files"])==18
copies=ROOT/"evidence"/"original_inputs"
copies.mkdir(exist_ok=True)
records=[]
for item in manifest["files"]:
    source=SNAP/item["path"]
    raw=source.read_bytes()
    assert len(raw)==item["size"]
    assert hashlib.sha256(raw).hexdigest()==item["sha256"]
    dst=copies/item["path"]
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_bytes(raw);dst.chmod(0o444)
    records.append({"source_path":str(source),"bound_copy":str(dst),"sha256":item["sha256"],"bytes":len(raw),"kind":"original_candidate_or_historical_input","excluded_from_reviewer_authorship":True,"executed":False,"mode":"0444"})
raw=DIFF.read_bytes()
assert len(raw)==75046
assert hashlib.sha256(raw).hexdigest()==manifest["diff_sha256"]
text=raw.decode()
blocks=text.split("diff --git ")[1:]
assert len(blocks)==19
checked=[]
for block in blocks:
    lines=block.splitlines(keepends=True)
    target=lines[0].strip().split(" b/",1)[1]
    if target=="unsolved_math_prioritization/QUEUE.md":
        assert "| 57 | 2912 / KP-4.36" in block and "| unsolved | 2/5 |" in block
        checked.append({"path":target,"kind":"one_queue_row_context_checked"})
    else:
        rel=target.removeprefix("unsolved_math_prioritization/attempts/2912/")
        assert lines[1].startswith("new file mode ")
        hunk=next(i for i,line in enumerate(lines) if line.startswith("@@ "))
        assert all(line.startswith("+") for line in lines[hunk+1:])
        added="".join(line[1:] for line in lines[hunk+1:]).encode()
        assert added==(SNAP/rel).read_bytes()
        checked.append({"path":target,"kind":"full_added_text_byte_equal_to_read_blob","sha256":hashlib.sha256(added).hexdigest()})
for source in (MANIFEST,DIFF):
    dst=copies/source.name;content=source.read_bytes();dst.write_bytes(content);dst.chmod(0o444)
    records.append({"source_path":str(source),"bound_copy":str(dst),"sha256":hashlib.sha256(content).hexdigest(),"bytes":len(content),"kind":"original_snapshot_or_diff_metadata","excluded_from_reviewer_authorship":True,"executed":False,"mode":"0444"})
report={"operator_pid":os.getpid(),"finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"head":expected_head,"base":expected_base,"original_18_files_bound":records,"full_19_path_diff_coverage":checked,"candidate_helper_executed":False,"old_helper_executed":False,"new_substantive_attempts":0,"audit_attempts":0,"scientific_assertion_count":0,"integrity_result":"PASS"}
(ROOT/"INPUT_CLOSURE_RECEIPT.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({"integrity_result":"PASS","original_files":18,"diff_paths":19,"diff_bytes":len(raw),"operator_pid":os.getpid(),"scientific_assertions":0,"new_substantive_attempts":0,"audit_attempts":0},indent=2))
