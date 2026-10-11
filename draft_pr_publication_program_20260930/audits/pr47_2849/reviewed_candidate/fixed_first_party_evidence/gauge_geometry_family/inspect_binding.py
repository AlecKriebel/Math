#!/usr/bin/env python3
"""Independently bind every candidate byte and the entire diff to original Git objects."""
from pathlib import Path
import hashlib, json, re, subprocess
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
REPO=AUDIT.parents[2]
HEAD="487327b2412c436ae69e8c52bf353a9a1fb7594e"
BASE="c6975ca76f9f667f1250ba403d0e6da2aafe14d0"
SNAP=AUDIT/"source_snapshot"
def git(*args):
    r=subprocess.run(["git",*args],cwd=REPO,stdin=subprocess.DEVNULL,capture_output=True,check=True)
    assert r.stderr==b""
    return r.stdout
manifest=json.loads((AUDIT/"snapshot_manifest.json").read_text())
diff=git("diff","--no-ext-diff","--no-textconv","--binary",BASE,HEAD,"--")
assert diff==(AUDIT/"original_git_commands/whole_diff/stdout.bin").read_bytes()
entries=[]
for f in manifest["files"]:
    b=(SNAP/f["relative_path"]).read_bytes()
    original=git("show",HEAD+":"+f["path"])
    assert original==b
    assert hashlib.sha256(b).hexdigest()==f["sha256"]
    entries.append({"path":f["relative_path"],"bytes":len(b),"sha256":f["sha256"],"original_git_object":f["git_object"],"byte_equal":True})
blocks=[b for b in re.split(rb"(?=^diff --git )",diff,flags=re.M) if b]
assert len(blocks)==17 and len(entries)==16
for b in blocks:
    header=b.splitlines()[0].decode()
    if "/attempts/2849/" in header:
        name=header.split(" b/")[1].split("/attempts/2849/",1)[1]
        lines=b.splitlines(keepends=True)
        added=b"".join(line[1:] for line in lines if line.startswith(b"+") and not line.startswith(b"+++"))
        assert added==(SNAP/name).read_bytes()
turns=json.loads((SNAP/"turns.json").read_text()); assert turns["count"]==len(turns["attempts"])==1
assert json.loads((SNAP/"prior_report.json").read_text()) is None
out={"head":HEAD,"base":BASE,"file_count":len(entries),"all_16_added_hunks_byte_equal":True,
     "diff_files":17,"diff_bytes":len(diff),"diff_sha256":hashlib.sha256(diff).hexdigest(),
     "files":entries,"turns_format":"single JSON object, not JSONL","turn_count":1,
     "prior_report_literal_null":True,"source_first_record_sha256":hashlib.sha256((ROOT/"SOURCE_FIRST.md").read_bytes()).hexdigest()}
(ROOT/"BINDING_RESULTS.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
