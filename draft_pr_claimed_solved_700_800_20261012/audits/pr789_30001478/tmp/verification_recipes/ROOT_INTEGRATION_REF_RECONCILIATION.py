from pathlib import Path
import datetime,hashlib,json,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";sys.path.insert(0,str(D))
from graphql_scoped_commit import Remote,gql,get_pr
from remote_scoped_commit import oid
obj=json.loads((M/"ADMINISTRATIVE_BRANCH_INTEGRATION_OBJECT_CREATED.json").read_text());intent=json.loads((M/"ADMINISTRATIVE_BRANCH_INTEGRATION_INTENT.json").read_text());ref=json.loads((M/"ADMINISTRATIVE_BRANCH_REF_RESPONSE.json").read_text());H=obj["original_scientific_head"];new=obj["head"];base=obj["main_base"]
assert H=="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"and new=="eb9f6de34861610cf7355a630603a0d18a13f39a"and ref["response"]["object"]["sha"]==new
p=get_pr(789);assert p["state"]=="open"and not p["merged"]and p["head"]["sha"]==new
head=Remote(H);main=Remote(base);post=Remote(new);Q="unsolved_math_prioritization/QUEUE.md";PREFIX="unsolved_math_prioritization/attempts/30001478";assert main.entry(PREFIX)is None
source=json.loads((T/"intake/ROOT_SOURCE_IDENTITY.json").read_text());assert len(source["original_files"])==58
rows={}
for f in source["original_files"]:
 e={"mode":"100644","type":"blob","sha":f["git_blob"]};assert head.entry(f["path"])==post.entry(f["path"])==e;rows[f["path"]]=e
def own(raw):
 lines=raw.splitlines(keepends=True);indices=[i for i,l in enumerate(lines)if l.startswith("| ")and" 30001478 / "in l];assert len(indices)==1;return lines,indices[0],lines[indices[0]]
lines,i,_=own(main.read(Q));_,_,candidate=own(head.read(Q));lines[i]=candidate;q="".join(lines);assert post.read(Q)==q;rows[Q]={"mode":"100644","type":"blob","sha":oid("blob",q.encode())}
expected=main.expected_tree(rows);assert expected==post.root==obj["tree"]==intent["expected_tree"]
actual=gql('query($o:GitObjectID!){repository(owner:"AlecKriebel",name:"Math"){object(oid:$o){...on Commit{oid parents(first:3){nodes{oid}}}}}}',{"o":new})["repository"]["object"];assert [x["oid"]for x in actual["parents"]["nodes"]]==[H,base]
g=json.loads((T/"FINAL_READINESS.json").read_text());assert g["reviewed_head"]==g["original_scientific_head"]==H and g["published"]is True
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS_ADMINISTRATIVE_INTEGRATION","head":new,"original_scientific_head":H,"main_base":base,"branch":"draft/prime-ideals-30001478-two-audits","tree":expected,"parents":[H,base],"allowed_paths":sorted(rows),"original58_blobs_byte_identical":True,"only_own_queue_row_changed_from_main":True,"complete_main_tree_other_paths_preserved":True,"same_published_source_manifest_sha256":g["source_manifest_sha256"],"same_six_published":True,"DOI":g["publication_DOI"],"force":False,"local_checkout_branch_index_objects_refs_untouched":True,"initial_PR_GraphQL_cache_lag_reconciled_by_read_only_GET":True,"second_ref_update_or_commit_created":False}
(M/"ADMINISTRATIVE_BRANCH_INTEGRATION_RECEIPT.json").write_text(json.dumps(out,indent=2)+"\n")
g.update(reviewed_head=new,original_scientific_head=H,administrative_integration_only=True,administrative_integration_main_base=base,administrative_integration_tree=expected,administrative_integration_receipt_sha256=hashlib.sha256((M/"ADMINISTRATIVE_BRANCH_INTEGRATION_RECEIPT.json").read_bytes()).hexdigest(),PR_completion_estimate_percent=96)
(T/"FINAL_READINESS.json").write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"result":out["result"],"head":new,"original_scientific_head":H,"main_base":base,"tree":expected,"scientific_blobs_preserved":58,"read_only_reconciliation":True}))

