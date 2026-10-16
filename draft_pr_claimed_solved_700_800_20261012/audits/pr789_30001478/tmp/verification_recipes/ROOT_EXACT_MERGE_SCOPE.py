from pathlib import Path
import datetime,hashlib,json,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";sys.path.insert(0,str(D))
from graphql_scoped_commit import Remote,gql
from remote_scoped_commit import oid
H="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a";g=json.loads((T/"FINAL_READINESS.json").read_text())
receipt=json.loads((M/"EXACT_HEAD_MERGE_RESPONSE.json").read_text());after=receipt["after"];merge=after["mergeCommit"];parents=[p["oid"]for p in merge["parents"]["nodes"]]
assert after["merged"]and after["headRefOid"]==parents[1]==g["reviewed_head"]
pre=Remote(parents[0]);post=Remote(merge["oid"]);original=Remote(H);source=json.loads((T/"intake/ROOT_SOURCE_IDENTITY.json").read_text());assert len(source["original_files"])==58 and source["reviewed_head"]==H
rows={}
for row in source["original_files"]:
 expected={"mode":"100644","type":"blob","sha":row["git_blob"]};assert original.entry(row["path"])==post.entry(row["path"])==expected
 assert pre.entry(row["path"])is None,"Preexisting own scientific prefix; reconcile"
 rows[row["path"]]=expected
qpath="unsolved_math_prioritization/QUEUE.md";old=pre.read(qpath);new=post.read(qpath);candidate=original.read(qpath)
def own(raw):
 lines=raw.splitlines(keepends=True);idx=[i for i,l in enumerate(lines)if l.startswith("| ")and" 30001478 / "in l];assert len(idx)==1;i=idx[0];return lines[i],lines[:i]+lines[i+1:]
b,o=own(old);a,n=own(new);ca,_=own(candidate);assert o==n and a==ca and a.split("|")[8].strip()=="claimed_solved"and a.split("|")[9].strip()=="1/5"
assert (b.split("|")[8].strip(),b.split("|")[9].strip())in[("queued","0/5"),("claimed_solved","1/5")]
rows[qpath]={"mode":"100644","type":"blob","sha":oid("blob",new.encode())}
assert pre.expected_tree(rows)==post.root==merge["tree"]["oid"]
integrated=parents[1]!=H
if integrated:
 r=json.loads((M/"ADMINISTRATIVE_BRANCH_INTEGRATION_RECEIPT.json").read_text())
 assert r["head"]==parents[1]and r["original_scientific_head"]==H
 head=Remote(r["head"]);base=Remote(r["main_base"])
 target={}
 for row in source["original_files"]:
  assert base.entry(row["path"])is None
  target[row["path"]]={"mode":"100644","type":"blob","sha":row["git_blob"]}
 oldq=base.read(qpath);oldrow,others=own(oldq);_,origothers=own(candidate)
 lines=oldq.splitlines(keepends=True);idx=next(i for i,l in enumerate(lines)if l.startswith("| ")and" 30001478 / "in l);lines[idx]=ca
 iq="".join(lines);target[qpath]={"mode":"100644","type":"blob","sha":oid("blob",iq.encode())}
 assert base.expected_tree(target)==head.root and head.read(qpath)==iq
 actual=gql('query($o:GitObjectID!){repository(owner:"AlecKriebel",name:"Math"){object(oid:$o){...on Commit{oid parents(first:3){nodes{oid}}}}}}',{"o":r["head"]})["repository"]["object"]
 assert [x["oid"]for x in actual["parents"]["nodes"]]==[H,r["main_base"]]
sourcepin=hashlib.sha256((T/"preprint/source/MANIFEST.json").read_bytes()).hexdigest();assert sourcepin==g["source_manifest_sha256"]=="b20f39f39a33b18822cff51850f8b5b220e139af4d7badec23a7f5a7e17805aa"
for f in g["publication_files"]:
 raw=(T/"preprint"/f["path"]).read_bytes();assert len(raw)==f["bytes"]and hashlib.sha256(raw).hexdigest()==f["sha256"]
rec={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","pr":789,"problem":"30001478","original_reviewed_head":H,"approved_merged_head":parents[1],"merge_commit":merge["oid"],"merge_first_parent":parents[0],"merge_parents_exact":parents,"merge_tree":post.root,"entire_merge_tree_equals_first_parent_plus_exact_allowed_59_paths":True,"allowed_paths":sorted(rows),"original_added_candidate_blobs_preserved":58,"other_QUEUE_bytes_preserved":True,"own_QUEUE_exact_candidate_row_preserved":True,"own_proof_budget":"1/5","source_manifest_sha256":sourcepin,"all_frozen_six_unchanged":True,"branch_integration_repair_required":integrated,"private_unrelated_workspace_and_all_other_remote_paths_untouched":True,"case_percent":97,"shard_percent":83}
(M/"ROOT_EXACT_MERGE_SCOPE.json").write_text(json.dumps(rec,indent=2)+"\n");print(json.dumps(rec))

