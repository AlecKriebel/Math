from pathlib import Path
import datetime,hashlib,json,sys,stat
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";sys.path.insert(0,str(D));from graphql_scoped_commit import Remote
old=json.loads((D/"audits/pr788_30001522/tmp/root-receipts/LOCAL_PROGRAM_MIRROR_SYNC.json").read_text());receipt=json.loads((M/"INTAKE_CHECKPOINT_RECEIPT.json").read_text());remote=Remote(receipt["commit"]);rows=[]
for row in old["only_own5text_mirrors"]:
 path=R/row["path"];assert stat.S_ISREG(path.lstat().st_mode)and not path.is_symlink()and path.stat().st_nlink==1;b=path.read_bytes();raw=remote.read(row["path"]).encode();assert hashlib.sha256(b).hexdigest()==row["sha256"]or b==raw,"Local own mirror changed; preserve it"
 path.write_bytes(raw);rows.append({"path":row["path"],"sha256":hashlib.sha256(raw).hexdigest()})
case=D/"audits/pr789_30001478/RESEARCH_LOG.md";raw=remote.read(case.relative_to(R).as_posix()).encode();assert raw.startswith(case.read_bytes()),"Local case log changed";case.write_bytes(raw);rows.append({"path":case.relative_to(R).as_posix(),"sha256":hashlib.sha256(raw).hexdigest()})
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","commit":receipt["commit"],"only_own6text_mirrors":rows,"previous_old5hashes_authenticated":True,"new_case_initial_log_prefix_preserved":True,"unrelated_working_changes_index_Git_objects_and_refs_untouched":True}
(M/"LOCAL_PROGRAM_MIRROR_SYNC.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps({"result":"PASS","own_text_mirrors":len(rows),"source_commit":receipt["commit"],"local_branch_checkout_index_untouched":True}))
