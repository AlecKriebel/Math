#!/usr/bin/env python3
"""Close this family alone; parent runs --verify after child exit with receipt outside the family."""
import hashlib, json, os, stat, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/"SELF_MANIFEST.json"
def inventory():
    files=[];dirs=["."]
    for p in sorted(ROOT.rglob("*")):
        assert not p.is_symlink(),str(p)
        if p.is_dir(): dirs.append(str(p.relative_to(ROOT)))
        elif p.is_file() and p!=MANIFEST:
            b=p.read_bytes()
            files.append({"path":str(p.relative_to(ROOT)),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"mode":format(stat.S_IMODE(p.stat().st_mode),"04o")})
        else: assert p==MANIFEST
    return files,dirs
if "--verify" not in sys.argv:
    assert not MANIFEST.exists()
    for p in ROOT.rglob("*"):
        if p.is_file(): p.chmod(0o444)
    files,dirs=inventory()
    out={"schema":"pr47-gauge-family-self-only-closed-manifest/v1",
         "root":str(ROOT),"original_head":"487327b2412c436ae69e8c52bf353a9a1fb7594e",
         "self_excluded":"SELF_MANIFEST.json","files":files,"directories":dirs,
         "file_count_excluding_self":len(files),"all_payload_full_modes":"0444",
         "foreign_body_policy":"No foreign PDFs, text, OCR, source pixels, headers, raw network caches, SQL, or access credentials retained.",
         "post_child_exit_verify_required":True}
    MANIFEST.write_text(json.dumps(out,indent=2)+"\n");MANIFEST.chmod(0o444)
else: out=json.loads(MANIFEST.read_text())
files,dirs=inventory()
assert files==out["files"]
assert dirs==out["directories"]
assert all(f["mode"]=="0444" for f in files)
assert stat.S_IMODE(MANIFEST.stat().st_mode)==0o444
for p in ROOT.rglob("*"):
    if p.is_file(): assert p.suffix.lower() not in [".pdf",".png",".jpg",".jpeg",".webp",".gif",".pyc",".sql",".sqlite"]
print(json.dumps({"verified":True,"root":str(ROOT),"file_count_excluding_self":len(files),"files_with_self":len(files)+1,"directory_count":len(dirs),"all_files_mode_0444":True,"no_foreign_body_extensions":True,"self_manifest_sha256":hashlib.sha256(MANIFEST.read_bytes()).hexdigest()},indent=2))
