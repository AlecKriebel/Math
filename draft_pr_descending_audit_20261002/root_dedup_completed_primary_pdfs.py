from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
P=Path("draft_pr_descending_audit_20261002");R=P.parent;j=P/"ROOT_PRIVATE_SOURCE_DEDUP_20261003_1835.jsonl";sha=lambda b:hashlib.sha256(b).hexdigest();rows=[]
for A in sorted((P/"audits").glob("pr*")):
 n=int(A.name.split("_")[0][2:])
 if not 368<=n<=388:continue
 candidates=[p for p in sorted(A.rglob("*")) if p.is_file() and not p.is_symlink() and p.suffix.lower()==".pdf" and any("private" in k or k in {"tmp","raw_sources"} for k in p.relative_to(A).parts) and "sources_effective_review" not in p.parts]
 tracked=set(subprocess.check_output(["git","ls-files","-z","--",str(A)],cwd=R).split(b"\0"));canonical={}
 for p in candidates:
  if str(p).encode() in tracked:continue
  b=p.read_bytes();h=sha(b)
  if h not in canonical:canonical[h]=p;continue
  c=canonical[h]
  if p.stat().st_ino==c.stat().st_ino:continue
  row={"utc":datetime.now(timezone.utc).isoformat(),"target":str(p),"canonical":str(c),"bytes":len(b),"sha256":h,"state":"PREPARED_EXACT_CANONICAL_VERIFIED"}
  with j.open("a") as f:f.write(json.dumps(row)+"\n");f.flush();os.fsync(f.fileno())
  temp=p.with_name(p.name+".root_dedup_pending");assert not temp.exists();os.link(c,temp);os.replace(temp,p);assert p.read_bytes()==b and p.stat().st_ino==c.stat().st_ino
  row["state"]="COMPLETE_EXACT_BYTES_PRESERVED"
  with j.open("a") as f:f.write(json.dumps(row)+"\n");f.flush();os.fsync(f.fileno())
  rows.append(row)
o={"utc":datetime.now(timezone.utc).isoformat(),"scope":"Only completed own PR388–368 untracked private/tmp/raw_sources exact-duplicate PDFs; shared sources_effective_review runtime entire tree excluded; every byte/path remains; no active/public/foreign change","files":len(rows),"logical_duplicate_bytes":sum(x["bytes"] for x in rows),"journal":str(j)}
(P/"ROOT_PRIVATE_SOURCE_DEDUP_20261003_1835.json").write_text(json.dumps(o,indent=2)+"\n");print(json.dumps(o))
