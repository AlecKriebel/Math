from pathlib import Path
import datetime,importlib.util,json,subprocess,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";sys.path.insert(0,str(D));from graphql_scoped_commit import gql
query='query($n:Int!){repository(owner:"AlecKriebel",name:"Math"){pullRequest(number:$n){state isDraft merged headRefOid mergeable mergeStateStatus mergedAt mergeCommit{oid parents(first:2){nodes{oid}} tree{oid}}}}}'
def read():return gql(query,{'n':789})['repository']['pullRequest']
g=json.loads((T/"FINAL_READINESS.json").read_text());expected_head=g["reviewed_head"]
p=read();assert p["state"]=="OPEN"and not p["isDraft"]and not p["merged"]and p["headRefOid"]==expected_head and p["mergeable"]=="MERGEABLE"and p["mergeStateStatus"]=="CLEAN"
spec=importlib.util.spec_from_file_location("pr789_premerge_fresh_eligibility",T/"publication_driver.py");driver=importlib.util.module_from_spec(spec);spec.loader.exec_module(driver)
original_save=driver.save
try:
 driver.save=lambda path,value: original_save(M/"FRESH_PREMERGE_ELIGIBILITY.json",value)
 driver.fresh_eligibility(g)
finally:driver.save=original_save
intent=M/"EXACT_HEAD_MERGE_INTENT.json";assert not intent.exists(),"A merge was already attempted; reconcile GET before any retry"
intent.write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"before":p,"command":["gh","pr","merge","789","--merge","--match-head-commit",p["headRefOid"]],"one_attempt":True},indent=2)+"\n")
r=subprocess.run(["gh","pr","merge","789","--merge","--match-head-commit",p["headRefOid"]],cwd=R,capture_output=True,text=True)
(M/"MERGE_STDOUT.txt").write_text(r.stdout);(M/"MERGE_STDERR.txt").write_text(r.stderr)
after=read();(M/"EXACT_HEAD_MERGE_RESPONSE.json").write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"CLI_returncode":r.returncode,"before":p,"after":after},indent=2)+"\n")
assert after["merged"]and after["headRefOid"]==p["headRefOid"]and after["mergeCommit"]and len(after["mergeCommit"]["parents"]["nodes"])==2
assert after["mergeCommit"]["parents"]["nodes"][1]["oid"]==p["headRefOid"]
print(json.dumps({"result":"MERGED_EXACT_APPROVED_HEAD","head":after["headRefOid"],"merge":after["mergeCommit"]["oid"],"parents":after["mergeCommit"]["parents"]["nodes"],"merged_at":after["mergedAt"],"CLI_returncode":r.returncode}))
