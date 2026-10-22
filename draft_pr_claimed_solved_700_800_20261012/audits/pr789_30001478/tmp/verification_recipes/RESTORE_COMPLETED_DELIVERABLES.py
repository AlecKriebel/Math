from pathlib import Path
import datetime,hashlib,json,sys,urllib.request,urllib.parse
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";sys.path.insert(0,str(D));from graphql_scoped_commit import Remote,head_oid
W=D/"final_delivery";W.mkdir(exist_ok=True);remote=Remote(head_oid())
cases=[(718,"30004324",23331395),(742,"30005356",23357263),(764,"30005453",23408971),(765,"30005613",23410944),(778,"30001054",23414444),(781,"4600024",23416806),(786,"30001223",23418581),(788,"30001522",23422039)]
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"purpose":"Restore exact already-published authored PDF deliverables after old RAM mounts disappeared; no PR or mathematical/priority re-review or mutation.","main_identity_commit":remote.parent,"papers":[]}
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Math-artifact-custody/1.0"}),timeout=90)as f:return f.read(),f.status,f.url
for pr,problem,rid in cases:
 accraw=remote.read("unsolved_math_prioritization/attempts/"+problem+"/acceptance.json").encode();acc=json.loads(accraw)
 assert acc["doi"]=="10.5281/zenodo."+str(rid)
 rows=acc.get("publication_files")
 if rows is None:
  binding=acc["final_readiness"];graw=remote.read(binding["path"]).encode();assert hashlib.sha256(graw).hexdigest()==binding["sha256"];rows=json.loads(graw)["publication_files"]
 wanted=[x for x in rows if x["path"].endswith(".pdf")];assert len(wanted)==1
 expected=wanted[0];target=W/("pr"+str(pr)+"-paper.pdf")
 if target.exists():
  raw=target.read_bytes();assert len(raw)==expected["bytes"]and hashlib.sha256(raw).hexdigest()==expected["sha256"];url="existing independently bound exact copy";status=None
 else:
  record_raw,rs,ru=get("https://zenodo.org/api/records/"+str(rid));record=json.loads(record_raw);assert record["id"]==rid and record["metadata"]["doi"]==acc["doi"]
  files=[x for x in record["files"]if x["key"].endswith(".pdf")];assert len(files)==1 and"/"not in files[0]["key"]
  raw,status,url=get("https://zenodo.org/records/"+str(rid)+"/files/"+urllib.parse.quote(files[0]["key"])+"?download=1")
  assert raw.startswith(b"%PDF-")and len(raw)==expected["bytes"]and hashlib.sha256(raw).hexdigest()==expected["sha256"]
  target.write_bytes(raw)
 out["papers"].append({"pr":pr,"problem":problem,"doi":acc["doi"],"record_id":rid,"path":str(target),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"native_acceptance_sha256":hashlib.sha256(accraw).hexdigest(),"public_HTTP_status":status,"public_final_url":url,"original_delivery_bytes_restored":True})
(W/"RESTORATION_RECEIPT.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"result":"PASS","papers_restored":len(out["papers"]),"bytes":sum(x["bytes"]for x in out["papers"]),"no_PR_reprocessing":True}))
