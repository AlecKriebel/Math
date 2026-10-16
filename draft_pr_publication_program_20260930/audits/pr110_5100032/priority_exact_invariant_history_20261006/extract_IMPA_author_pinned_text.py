#!/usr/bin/env python3
from pathlib import Path,PurePosixPath
import zipfile,json,hashlib,os,datetime
w=Path(__file__).resolve().parent
t=json.loads((w/"private_sources/IMPA_author_tree.json").read_text())
known={r["path"]:r for r in t["tree"] if r["type"]=="blob"}
d=w/"private_review_materials/IMPA_author_pinned_text";d.mkdir(exist_ok=False)
rows=[]
with zipfile.ZipFile(w/"private_sources/IMPA_author_pinned.zip") as z:
 for x in z.infolist():
  ps=PurePosixPath(x.filename)
  if x.is_dir() or len(ps.parts)<2: continue
  r=str(PurePosixPath(*ps.parts[1:]))
  if not r.endswith((".tex",".bib",".md")): continue
  if ps.is_absolute() or ".." in ps.parts: raise ValueError("unsafe archive path")
  if r not in known: raise ValueError("unmatched inventory")
  b=z.read(x)
  oid=hashlib.sha1(("blob "+str(len(b))+"\0").encode()+b).hexdigest()
  if oid!=known[r]["sha"]: raise ValueError("Git blob mismatch "+r)
  dst=d/r;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
  rows.append({"path":r,"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"Git_blob_OID":oid})
expected={r for r in known if r.endswith((".tex",".bib",".md"))}
if {r["path"] for r in rows}!=expected: raise ValueError("incomplete selected extraction")
out={"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"actual_operator_PID":os.getpid(),"source_commit":"0b5b417fe2ba3185087979749bc8bcf8c702315d","source_commit_date":"2021-06-07T19:24:09Z","private_extraction_root":"private_review_materials/IMPA_author_pinned_text","count":len(rows),"body_rows":rows,"limitation":"Author repository source snapshot is not certified identical to the final July2021 book; compiled 000_main_impa.pdf byte-exact Git blob is truncated/invalid and cannot be read as a valid PDF. Official preview only15pages."}
(w/"IMPA_AUTHOR_SOURCE_CUSTODY.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"count":len(rows),"total_bytes":sum(r["bytes"] for r in rows),"all_Git_blob_pins_match":True}))

