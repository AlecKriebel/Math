#!/usr/bin/env python3
"""Read only released exact PR329 snapshot attempt scope, no queue access."""
import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
manifest=json.loads((root/"evidence/candidate_full/inputs/snapshot_manifest.json").read_text())
records=[r for r in manifest["files"] if r["path"].startswith("unsolved_math_prioritization/attempts/20000450/")]
assert len(records)==21
out=root/"evidence/original_pr_scope"
out.mkdir(exist_ok=False)
rows=[]
for record in records:
    source=root.parent/"snapshot"/record["path"]
    data=source.read_bytes()
    assert len(data)==record["bytes"] and hashlib.sha256(data).hexdigest()==record["sha256"]
    rel=record["path"].split("attempts/20000450/",1)[1]
    target=out/rel
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    row={"relative_path":rel,"bytes":len(data),"sha256":record["sha256"],"source":str(source)}
    rows.append(row);print(json.dumps(row))
(out/"OWN_COPY_INVENTORY.json").write_text(json.dumps(rows,indent=2)+"\n")
