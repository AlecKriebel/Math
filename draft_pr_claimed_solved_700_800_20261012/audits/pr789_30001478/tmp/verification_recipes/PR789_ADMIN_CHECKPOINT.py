from pathlib import Path
import contextlib,datetime,io,json,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";sys.path.insert(0,str(D))
from graphql_scoped_commit import Remote,head_oid,commit_updates
plan=json.loads((T/"ADMIN_CHECKPOINT_PLAN.json").read_text());phase=plan["phase"];assert phase.replace("_","").isalnum();receiptpath=M/(phase+"_CHECKPOINT_RECEIPT.json");assert not receiptpath.exists(),"Existing checkpoint receipt; inspect rather than duplicate"
g=json.loads((T/"FINAL_READINESS.json").read_text());assert g["result"]=="PASS"and g["pr"]==789
updates={}
for name in["root-receipts","verification_recipes","publication"]:
 for p in(T/name).rglob("*"):
  if p.is_file():
   assert not p.is_symlink();updates[p.relative_to(R).as_posix()]=p.read_bytes()
for n in["FINAL_READINESS.json","publication_driver.py","TRACKER_SCOPE.json","ADMIN_CHECKPOINT_PLAN.json"]:
 p=T/n;updates[p.relative_to(R).as_posix()]=p.read_bytes()
for folder in [T/"whole_preprint_round03",T/"admin_scope/packet"]:
 if not(folder/"MANIFEST.json").exists():continue
 entries=json.loads((folder/"MANIFEST.json").read_text())["files"]
 if isinstance(entries,dict):entries=[dict(path=n,**v)for n,v in entries.items()]
 for item in entries+[{"path":"MANIFEST.json"}]:
  p=folder/item["path"];assert p.name==item["path"]and p.is_file()and not p.is_symlink()and p.stat().st_nlink==1
  updates[p.relative_to(R).as_posix()]=p.read_bytes()
now=datetime.datetime.now(datetime.timezone.utc).isoformat();entry="\n## "+now+" — "+plan["heading"]+"\n\n"+plan["notes"]+"\n\nCase "+str(plan["case_percent"])+"%; shard "+str(plan["shard_percent"])+"%.\n"
for retry in range(3):
 r=Remote(head_oid());u=dict(updates)
 for n in["RESEARCH_LOG.md","audits/pr789_30001478/RESEARCH_LOG.md"]:u[D.name+"/"+n]=r.read(D.name+"/"+n)+entry
 state=json.loads(r.read(D.name+"/STATE.json"));assert len(state["processed"])==10;state.update(updated_at=now,current_pr=789,current_stage=plan["heading"],overall_completion_estimate_percent=plan["shard_percent"]);u[D.name+"/STATE.json"]=json.dumps(state,indent=2)+"\n"
 log=r.read(D.name+"/checkpoint_receipts.jsonl")
 for n in plan["previous_receipts"]:
  prev=json.loads((M/n).read_text())
  if not any(json.loads(l).get("commit")==prev["commit"]for l in log.splitlines()if l):log+=json.dumps(prev)+"\n"
 u[D.name+"/checkpoint_receipts.jsonl"]=log
 captured=io.StringIO()
 with contextlib.redirect_stdout(captured):receipt=commit_updates(r,u,plan["message"])
 (M/(phase+"_CHECKPOINT_RAW.txt")).write_text(captured.getvalue())
 if receipt:break
else:raise RuntimeError("Three main races; no checkpoint confirmation")
receiptpath.write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"commit":receipt["commit"],"phase":phase,"case_percent":plan["case_percent"],"shard_percent":plan["shard_percent"]}))
