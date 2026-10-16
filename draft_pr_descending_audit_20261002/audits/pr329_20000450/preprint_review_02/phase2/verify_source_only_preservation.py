#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import stat
import subprocess

HERE=Path(__file__).resolve().parent; N=HERE.parent
original=json.loads((N/"SOURCE_ONLY_FREEZE.json").read_text())
results=[]
for row in original["objects_before_manifest_creation"]:
    p=N/row["path"]
    current_mode=format(stat.S_IMODE(p.stat().st_mode),"04o")
    out={"path":row["path"],"mode_unchanged":current_mode==row["mode_octal"]}
    if row["type"]=="file":
        if row["path"]=="RESEARCH_LOG.md":
            prefix=(HERE/"source_only_log_prefix.md").read_bytes()
            out["frozen_prefix_sha_matches"]=hashlib.sha256(prefix).hexdigest()==row["sha256"]
            out["current_log_is_append_only"]=p.read_bytes().startswith(prefix)
        else:
            out["body_unchanged"]=hashlib.sha256(p.read_bytes()).hexdigest()==row["sha256"]
    assert all(v for k,v in out.items() if k!="path"),out
    results.append(out)
assert hashlib.sha256((N/"SOURCE_ONLY_FREEZE.json").read_bytes()).hexdigest()=="858dc31c2ce1f49d3e2c4dfc59d13c76c2d36cb3011954e7ecf6129a1a3c7637"
utc=subprocess.run(["/bin/date","-u","+%Y-%m-%dT%H:%M:%SZ"],capture_output=True,check=True).stdout.decode().strip()
out={"utc":utc,"status":"all source-only file bodies and modes preserved; research log append-only with exact frozen prefix separately preserved","source_only_manifest_body_unchanged":True,"checks":results}
(HERE/"source_only_preservation_check.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"utc":utc,"status":out["status"],"checked_original_objects":len(results)},indent=2))
