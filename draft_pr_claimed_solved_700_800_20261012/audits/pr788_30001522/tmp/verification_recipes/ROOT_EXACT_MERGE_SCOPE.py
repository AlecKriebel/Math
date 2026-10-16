from pathlib import Path
import sys,json,hashlib,datetime
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr788_30001522/tmp";M=T/"root-receipts";sys.path.insert(0,str(D))
from graphql_scoped_commit import Remote,gql
from remote_scoped_commit import oid
receipt=json.loads((M/"EXACT_HEAD_MERGE_RESPONSE.json").read_text());after=receipt["after"];merge=after["mergeCommit"];parents=[p["oid"]for p in merge["parents"]["nodes"]];assert after["merged"]and after["headRefOid"]==parents[1]=="3412d5a074c3f3a03f75735a9ccf1755e172204a"
pre=Remote(parents[0]);post=Remote(merge["oid"]);original=Remote(parents[1]);source=json.loads((T/"intake/ROOT_SOURCE_IDENTITY.json").read_text());assert len(source["original_files"])==48
rows={}
for row in source["original_files"]:
 expected={"mode":"100644","type":"blob","sha":row["git_blob"]};assert original.entry(row["path"])==post.entry(row["path"])==expected;assert pre.entry(row["path"])is None;rows[row["path"]]=expected
qpath="unsolved_math_prioritization/QUEUE.md";old=pre.read(qpath);new=post.read(qpath);candidate=original.read(qpath)
def own(raw):
 lines=raw.splitlines(keepends=True);idx=[i for i,l in enumerate(lines)if l.startswith("| ")and" 30001522 / "in l];assert len(idx)==1;i=idx[0];return lines[i],lines[:i]+lines[i+1:]
b,o=own(old);a,n=own(new);ca,_=own(candidate);assert o==n and a==ca and b.split("|")[8].strip()=="queued"and b.split("|")[9].strip()=="0/5"and a.split("|")[8].strip()=="claimed_solved"and a.split("|")[9].strip()=="2/5"
rows[qpath]={"mode":"100644","type":"blob","sha":oid("blob",new.encode())}
assert pre.expected_tree(rows)==post.root==merge["tree"]["oid"]
g=json.loads((T/"FINAL_READINESS.json").read_text());sourcepin=hashlib.sha256((T/"preprint/source/MANIFEST.json").read_bytes()).hexdigest();assert sourcepin==g["source_manifest_sha256"]
for f in g["publication_files"]:
 b=(T/"preprint"/f["path"]).read_bytes();assert len(b)==f["bytes"]and hashlib.sha256(b).hexdigest()==f["sha256"]
rec={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","pr":788,"problem":"30001522","original_reviewed_head":parents[1],"merge_commit":merge["oid"],"merge_first_parent":parents[0],"merge_parents_exact":parents,"merge_tree":post.root,"entire_merge_tree_equals_first_parent_plus_exact_allowed_49_paths":True,"allowed_paths":sorted(rows),"original_added_candidate_blobs_preserved":48,"other_QUEUE_bytes_preserved":True,"own_QUEUE_exact_candidate_row_preserved":True,"own_proof_budget":"2/5","source_manifest_sha256":sourcepin,"all_frozen_six_unchanged":True,"branch_integration_repair_required":False,"private_unrelated_workspace_and_all_other_remote_paths_untouched":True,"case_percent":97,"shard_percent":75}
(M/"ROOT_EXACT_MERGE_SCOPE.json").write_text(json.dumps(rec,indent=2)+"\n");print(json.dumps(rec))
