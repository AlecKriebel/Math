"""After completed whole04 only: replace the sole known unpublished draft's exact old ZIP, never create a record."""
from pathlib import Path
import argparse,datetime,hashlib,importlib.util,json,stat,urllib.request,uuid
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");P=T/"preprint";U=T/"publication";M=T/"root-receipts";OLD=T/"package_versions/v3_review03"
def need(v,m):
 if not v:raise RuntimeError(m)
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+"\n")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
need(sha(T/"publication_driver.py")=="a02c7910936f6d871fc760af4f5f41005f2ca055dc7cc99e84913a0893a47f96","Approved production driver pin differs before import")
spec=importlib.util.spec_from_file_location("pr789_approved_v4_known_draft",T/"publication_driver.py");d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
g,inv=d.gate()
need(g["actual_whole_preprint_rounds"]==4 and g["final_current_round_clean"]is True and g["reviewed_head"]=="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a","Completed exact four-round final gate required")
need(inv["source_manifest_sha256"]=="b20f39f39a33b18822cff51850f8b5b220e139af4d7badec23a7f5a7e17805aa","Wrong V4 source")
need((U/"READINESS_AT_PUBLICATION_V4.json").read_bytes()==(T/"FINAL_READINESS.json").read_bytes(),"Exact final V4 publication snapshot required")
need((M/"WHOLE04_V4_READY_CHECKPOINT_RECEIPT.json").exists(),"Completed scoped prepublication checkpoint required")
need(not(U/"PUBLICATION_INTENT.json").exists()and not(U/"PUBLISH_RECEIPT.json").exists(),"Publication already attempted; reconcile without mutations")
intent=U/"V4_ZIP_REPLACEMENT_INTENT.json";need(not intent.exists(),"Replacement was attempted; use read-only known-ID reconciliation before any retry")
oldsave=d.save
try:
 d.save=lambda p,v:oldsave(M/"FRESH_V4_PRE_REPLACEMENT_ELIGIBILITY.json",v)
 d.fresh_eligibility(g)
finally:d.save=oldsave
z=d.load_tool();manifest=(P/"zenodo-deposit.json").resolve();place,state=z.local_state(manifest,"production")
need(state is not None and state["id"]==23423736,"The sole known draft state is required; no create fallback")
client=z.ZenodoClient("production",z.token_for("production"))
def prohibit_create(*args,**kwargs):raise RuntimeError("A second deposition creation is prohibited")
client.create=prohibit_create
dep=client.get(23423736);z.validate_record(dep,23423736);need(dep["submitted"]is False,"Only unpublished23423736 may be repaired")
metadata,files=z.load_manifest(manifest);oldmeta,oldfiles=z.load_manifest((OLD/"zenodo-deposit.json").resolve())
need(all(dep["metadata"].get(k)==v for k,v in metadata.items()),"Existing canonical metadata must exactly match every V4 supplied field")
remote=z.server_files(dep);need(set(remote)=={"paper.pdf","source-and-verification.zip"},"Exact known two-file inventory required")
for e in oldfiles:need(z.matching_file(remote[e["name"]],e),"Existing draft differs from the preserved exact V3 files")
oldzip=next(e for e in oldfiles if e["name"]=="source-and-verification.zip");newzip=next(e for e in files if e["name"]=="source-and-verification.zip");paper=next(e for e in files if e["name"]=="paper.pdf")
need(oldzip["sha256"]=="5a6ebbfa082458149a633e13b5ae0f5b7dccb04aca90cfd43771fc75f7a2568a"and oldzip["size"]==338686,"Old V3 ZIP identity")
need(newzip["sha256"]=="9dfb13a945de2fe4d088eef8cd86ca1f9ecdb75b87162285a8fa4b7c1aab94b6"and newzip["size"]==338683 and z.matching_file(remote["paper.pdf"],paper),"New V4 ZIP and unchanged PDF identity")
approved_bucket=dep["links"]["bucket"]
raw_get,raw_update,raw_upload=client.get,client.update,client.upload
upload_attempts=0
def only_known_get(record_id):
 need(type(record_id)is int and record_id==23423736,"Refusing a different record ID before GET or stage mutation")
 result=raw_get(record_id);z.validate_record(result,23423736);return result
def only_known_update(record_id,requested_metadata):
 need(type(record_id)is int and record_id==23423736 and requested_metadata==metadata,"Refusing different record or metadata before PUT")
 return raw_update(record_id,requested_metadata)
def only_approved_ZIP_upload(bucket,entry):
 global upload_attempts
 need(bucket==approved_bucket and entry==newzip,"Refusing a different bucket, file, or PDF upload")
 approved_path=P/"source-and-verification.zip";info=approved_path.lstat()
 need(Path(entry["path"])==approved_path and stat.S_ISREG(info.st_mode)and info.st_nlink==1 and info.st_size==338683 and sha(approved_path)==newzip["sha256"],"Frozen approved ZIP path or bytes differ before upload")
 need(upload_attempts==0,"Only one replacement ZIP upload attempt is authorized")
 upload_attempts+=1
 return raw_upload(bucket,entry)
client.get,client.update,client.upload=only_known_get,only_known_update,only_approved_ZIP_upload
fid=remote["source-and-verification.zip"]["id"];need(type(fid)is str and str(uuid.UUID(fid))==fid,"Exact canonical file UUID required")
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
save(intent,{"utc":stamp,"known_record_id":23423736,"submitted":False,"only_file_removed":"source-and-verification.zip","old_file_id":fid,"old_size":oldzip["size"],"old_md5":oldzip["md5"],"old_sha256":oldzip["sha256"],"replacement_size":newzip["size"],"replacement_sha256":newzip["sha256"],"unchanged_PDF_sha256":paper["sha256"],"source_manifest_sha256":inv["source_manifest_sha256"],"readiness_sha256":sha(T/"FINAL_READINESS.json"),"creation_requests_prohibited":True,"official_DELETE_API":"https://developers.zenodo.org/#deposition-files"})
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):raise RuntimeError("Unexpected redirect; no authorization forwarded")
url="https://zenodo.org/api/deposit/depositions/23423736/files/"+fid
request=urllib.request.Request(url,method="DELETE",headers={"Authorization":"Bearer "+client.token,"Accept":"application/json","User-Agent":"Math-independent-research/1.0"})
try:
 with urllib.request.build_opener(NoRedirect).open(request,timeout=90)as response:
  status=response.status;body=response.read(4096)
except Exception:
 raise RuntimeError("Known-file removal outcome unconfirmed; reconcile draft23423736 with GET before any retry")from None
need(status==204 and body==b"","Unexpected removal response; reconcile known draft without repeating DELETE")
save(U/"V4_ZIP_DELETION_RECEIPT.json",{"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"record_id":23423736,"file_id":fid,"only_file":"source-and-verification.zip","HTTP_status":204,"empty_body":True,"PDF_not_mutated":True})
dep=client.get(23423736);z.validate_record(dep,23423736);need(dep["submitted"]is False and set(z.server_files(dep))=={"paper.pdf"}and z.matching_file(z.server_files(dep)["paper.pdf"],paper),"Known draft after removal differs")
# The unchanged tool sees an existing state and uploads only its missing ZIP.
out=z.run(argparse.Namespace(command="stage",manifest=manifest,sandbox=False),client=client)
need(out["id"]==23423736 and out["state"]=="ready_to_publish"and out["metadata_normalizations"]==[]and upload_attempts==1,"Canonical same-ID staging did not verify exactly")
save(U/"STAGE_RECEIPT.json",out)
save(M/"KNOWN_DRAFT_RESUMED_V4.json",{"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","record_id":23423736,"deposition_creations_total":1,"published":False,"removed_old_unpublished_ZIPs":1,"uploaded_new_ZIPs":1,"PDF_bytes_unchanged":True,"all_supplied_metadata_exact":True,"metadata_normalizations":[],"current_source_manifest_sha256":inv["source_manifest_sha256"],"original_upload_tool_unchanged":True,"case_adapter_used":False})
print(json.dumps({"result":"SAME_KNOWN_DRAFT_READY","id":23423736,"state":out["state"],"metadata_normalizations":[],"creations_total":1,"published":False}))

