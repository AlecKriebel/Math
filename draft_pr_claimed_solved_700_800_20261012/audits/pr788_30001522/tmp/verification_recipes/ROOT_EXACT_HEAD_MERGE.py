from pathlib import Path
import datetime,json,subprocess,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr788_30001522/tmp";M=T/"root-receipts";sys.path.insert(0,str(D));from graphql_scoped_commit import gql
query='query($n:Int!){repository(owner:"AlecKriebel",name:"Math"){pullRequest(number:$n){state isDraft merged headRefOid mergeable mergeStateStatus mergedAt mergeCommit{oid parents(first:2){nodes{oid}} tree{oid}}}}}'
def read():return gql(query,{'n':788})['repository']['pullRequest']
p=read();assert p["state"]=="OPEN"and not p["isDraft"]and not p["merged"]and p["headRefOid"]=="3412d5a074c3f3a03f75735a9ccf1755e172204a"and p["mergeable"]=="MERGEABLE"and p["mergeStateStatus"]=="CLEAN"
intent=M/"EXACT_HEAD_MERGE_INTENT.json";assert not intent.exists(),"A merge was already attempted; reconcile GET before any retry"
intent.write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"before":p,"command":["gh","pr","merge","788","--merge","--match-head-commit",p["headRefOid"]],"one_attempt":True},indent=2)+"\n")
r=subprocess.run(["gh","pr","merge","788","--merge","--match-head-commit",p["headRefOid"]],cwd=R,capture_output=True,text=True)
(M/"MERGE_STDOUT.txt").write_text(r.stdout);(M/"MERGE_STDERR.txt").write_text(r.stderr)
after=read();(M/"EXACT_HEAD_MERGE_RESPONSE.json").write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"CLI_returncode":r.returncode,"before":p,"after":after},indent=2)+"\n")
assert after["merged"]and after["headRefOid"]==p["headRefOid"]and after["mergeCommit"]and len(after["mergeCommit"]["parents"]["nodes"])==2
assert after["mergeCommit"]["parents"]["nodes"][1]["oid"]==p["headRefOid"]
print(json.dumps({"result":"MERGED_EXACT_ORIGINAL_HEAD","head":after["headRefOid"],"merge":after["mergeCommit"]["oid"],"parents":after["mergeCommit"]["parents"]["nodes"],"merged_at":after["mergedAt"],"CLI_returncode":r.returncode}))
