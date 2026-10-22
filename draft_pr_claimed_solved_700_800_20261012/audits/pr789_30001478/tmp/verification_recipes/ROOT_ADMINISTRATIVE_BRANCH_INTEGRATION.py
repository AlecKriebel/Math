"""Create one exact-scoped two-parent administrative integration on the existing PR branch, without local Git writes."""
from pathlib import Path
import base64,datetime,hashlib,importlib.util,json,sys,urllib.parse
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";sys.path.insert(0,str(D))
from graphql_scoped_commit import Remote,gql,get_pr,head_oid
from remote_scoped_commit import api,oid
H="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a";BRANCH="draft/prime-ideals-30001478-two-audits";Q="unsolved_math_prioritization/QUEUE.md";PREFIX="unsolved_math_prioritization/attempts/30001478"
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+"\n")
def own(raw):
 lines=raw.splitlines(keepends=True);hits=[i for i,l in enumerate(lines)if l.startswith("| ")and" 30001478 / "in l];assert len(hits)==1;return lines,hits[0],lines[hits[0]]
assert not(M/"ADMINISTRATIVE_BRANCH_INTEGRATION_INTENT.json").exists(),"Existing integration intent: inspect known object/ref before retry"
assert hashlib.sha256((T/"publication_driver.py").read_bytes()).hexdigest()=="a02c7910936f6d871fc760af4f5f41005f2ca055dc7cc99e84913a0893a47f96"
spec=importlib.util.spec_from_file_location("pr789_approved_integration_gate",T/"publication_driver.py");d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d);g,inv=d.gate()
assert g["reviewed_head"]==g["original_scientific_head"]==H and g["actual_whole_preprint_rounds"]==4 and g["published"]is True
pub=json.loads((T/"publication/PUBLISH_RECEIPT.json").read_text());sheet=json.loads((T/"publication/SHEET_VERIFICATION.json").read_text());assert pub["state"]=="published"and pub["doi"]==sheet["doi"]=="10.5281/zenodo.23423736"and sheet["result"]=="PASS"
p=gql('query{repository(owner:"AlecKriebel",name:"Math"){pullRequest(number:789){state isDraft merged headRefOid headRefName baseRefName mergeable mergeStateStatus headRepository{nameWithOwner}}}}')["repository"]["pullRequest"]
assert p["state"]=="OPEN"and not p["isDraft"]and not p["merged"]and p["headRefOid"]==H and p["headRefName"]==BRANCH and p["baseRefName"]=="main"and p["headRepository"]["nameWithOwner"]=="AlecKriebel/Math"and p["mergeable"]=="CONFLICTING"and p["mergeStateStatus"]=="DIRTY"
head=Remote(H);mainbase=head_oid();main=Remote(mainbase);assert main.entry(PREFIX)is None
parent=gql('query($o:GitObjectID!){repository(owner:"AlecKriebel",name:"Math"){object(oid:$o){...on Commit{parents(first:3){nodes{oid}}}}}}',{"o":H})["repository"]["object"]["parents"]["nodes"];assert len(parent)==1
_,_,baseline=own(Remote(parent[0]["oid"]).read(Q));_,_,candidate=own(head.read(Q));qlines,qi,mainrow=own(main.read(Q))
assert baseline.split("|")[8].strip()=="queued"and baseline.split("|")[9].strip()=="0/5"and candidate.split("|")[8].strip()=="claimed_solved"and candidate.split("|")[9].strip()=="1/5"
assert mainrow in[baseline,candidate],"Do not overwrite concurrent own problem changes"
source=json.loads((T/"intake/ROOT_SOURCE_IDENTITY.json").read_text());assert source["reviewed_head"]==H and len(source["original_files"])==58
assert hashlib.sha256((T/"intake/ROOT_SOURCE_IDENTITY.json").read_bytes()).hexdigest()=="92c0b6666f23bcab7624a7801d79247d8dc9a3d01333da8a300d2328da75db70"
rows={}
for f in source["original_files"]:
 e={"mode":"100644","type":"blob","sha":f["git_blob"]};assert head.entry(f["path"])==e and main.entry(f["path"])is None;rows[f["path"]]=e
qlines[qi]=candidate;qraw="".join(qlines).encode();qsha=oid("blob",qraw);rows[Q]={"mode":"100644","type":"blob","sha":qsha};expected=main.expected_tree(rows)
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
save(M/"ADMINISTRATIVE_BRANCH_INTEGRATION_INTENT.json",{"utc":stamp,"original_scientific_head":H,"main_base":mainbase,"existing_branch":BRANCH,"expected_tree":expected,"parents":[H,mainbase],"exact_allowed_paths":sorted(rows),"same_original_blobs":58,"only_own_QUEUE_row":True,"no_force_or_local_Git_writes":True,"DOI":pub["doi"]})
blob=api("git/blobs","POST",{"content":base64.b64encode(qraw).decode(),"encoding":"base64"});assert blob["sha"]==qsha
tree=api("git/trees","POST",{"base_tree":main.root,"tree":[dict(path=path,**entry)for path,entry in rows.items()]});assert tree["sha"]==expected
commit=api("git/commits","POST",{"message":"Integrate current main administratively for audited PR789 while preserving all 58 scientific files","tree":expected,"parents":[H,mainbase]});newhead=commit["sha"];assert commit["tree"]["sha"]==expected and [x["sha"]for x in commit["parents"]]==[H,mainbase]
save(M/"ADMINISTRATIVE_BRANCH_INTEGRATION_OBJECT_CREATED.json",{"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"head":newhead,"original_scientific_head":H,"main_base":mainbase,"tree":expected,"parents":[H,mainbase],"branch_ref_update_not_yet_confirmed":True})
current=get_pr(789);assert current["head"]["sha"]==H and current["state"]=="open"and not current["merged"],"Concurrent PR drift: known integration object saved but no ref update"
response=api("git/refs/heads/"+urllib.parse.quote(BRANCH,safe="/"),"PATCH",{"sha":newhead,"force":False},check=False)
confirmed=get_pr(789);save(M/"ADMINISTRATIVE_BRANCH_REF_RESPONSE.json",{"response":response,"confirmed_PR":confirmed})
assert confirmed["head"]["sha"]==newhead and confirmed["state"]=="open"and not confirmed["merged"],"Reference outcome requires known-ID reconciliation; never force"
post=Remote(newhead);assert post.root==expected and post.read(Q)=="".join(qlines)
for f in source["original_files"]:assert post.entry(f["path"])==rows[f["path"]]
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS_ADMINISTRATIVE_INTEGRATION","head":newhead,"original_scientific_head":H,"main_base":mainbase,"branch":BRANCH,"tree":expected,"parents":[H,mainbase],"allowed_paths":sorted(rows),"original58_blobs_byte_identical":True,"only_own_queue_row_changed_from_main":True,"complete_main_tree_other_paths_preserved":True,"same_published_source_manifest_sha256":inv["source_manifest_sha256"],"same_six_published":True,"DOI":pub["doi"],"force":False,"local_checkout_branch_index_objects_refs_untouched":True}
save(M/"ADMINISTRATIVE_BRANCH_INTEGRATION_RECEIPT.json",out)
g.update(reviewed_head=newhead,original_scientific_head=H,administrative_integration_only=True,administrative_integration_main_base=mainbase,administrative_integration_tree=expected,administrative_integration_receipt_sha256=hashlib.sha256((M/"ADMINISTRATIVE_BRANCH_INTEGRATION_RECEIPT.json").read_bytes()).hexdigest(),PR_completion_estimate_percent=96)
save(T/"FINAL_READINESS.json",g)
print(json.dumps({"result":out["result"],"head":newhead,"original_scientific_head":H,"main_base":mainbase,"tree":expected,"same_scientific_files":58,"only_own_Q_row":True,"local_branch":"main"}))

