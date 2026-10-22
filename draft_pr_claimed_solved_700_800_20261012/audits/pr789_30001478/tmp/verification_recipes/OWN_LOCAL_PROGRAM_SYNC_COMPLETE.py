from pathlib import Path
import datetime,hashlib,json,stat,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";sys.path.insert(0,str(D));from graphql_scoped_commit import Remote
old=json.loads((M/"LOCAL_PROGRAM_MIRROR_SYNC_V4.json").read_text());receipt=json.loads((M/"COMPLETE_CHECKPOINT_RECEIPT.json").read_text());remote=Remote(receipt["commit"]);new=[];payloads=[]
for row in old["only_own6text_mirrors"]:
 p=R/row["path"];assert stat.S_ISREG(p.lstat().st_mode)and not p.is_symlink()and p.stat().st_nlink==1
 raw=remote.read(row["path"]).encode();assert hashlib.sha256(p.read_bytes()).hexdigest()==row["sha256"]or p.read_bytes()==raw,"Unexpected own local edits; preserve"
 payloads.append((p,raw));new.append({"path":row["path"],"sha256":hashlib.sha256(raw).hexdigest()})
for p,raw in payloads:p.write_bytes(raw)
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","commit":receipt["commit"],"only_own6text_mirrors":new,"old_own6hashes_authenticated":True,"unrelated_working_changes_index_Git_objects_and_refs_untouched":True}
(M/"LOCAL_PROGRAM_MIRROR_SYNC_COMPLETE.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps({"result":"PASS","own_mirrors":6,"source_commit":receipt["commit"]}))

