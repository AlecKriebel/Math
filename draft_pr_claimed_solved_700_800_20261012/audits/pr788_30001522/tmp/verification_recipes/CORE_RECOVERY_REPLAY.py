from pathlib import Path
import json,subprocess,datetime,hashlib,os
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp");P=T/"preprint"
r=subprocess.run(["python3","-I","-B",str(P/"source/verify_source.py"),"--expected-manifest-sha256","bdfe29cd2a46d035cda5d83a101775283125c17b1f432b0f0f0994b5ba0819ff","--pdf",str(P/"output/pdf/paper.pdf"),"--replay"],cwd="/",capture_output=True,text=True,timeout=300)
if r.returncode or r.stderr:raise RuntimeError(r.stdout+r.stderr)
got=json.loads(r.stdout);assert got["result"]=="PASS"and got["external_evidence_files_rehashed"]==0
inventory=json.loads((P/"PACKAGE_INVENTORY.json").read_text())
for row in inventory["files"]:
 b=(P/row["path"]).read_bytes();assert len(b)==row["bytes"]and hashlib.sha256(b).hexdigest()==row["sha256"]
receipt={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","restored_six_exact":True,"portable_core":got,"external_body_banks_lost":True,"historic_full76_receipt_preserved":True,"new_optional_external_custody_claimed":False,"old_unfinished_review_not_counted":True,"fresh_restarted_review":"/root/pr788_whole_preprint_round01_restarted"}
(T/"session-recovery/CORE_RECOVERY_REPLAY.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"result":"PASS","source_files":got["source_files"],"replayed_processes":len(got["finite_replay_processes"]),"restored_exact_six":True,"new_external_custody_count":0}))
