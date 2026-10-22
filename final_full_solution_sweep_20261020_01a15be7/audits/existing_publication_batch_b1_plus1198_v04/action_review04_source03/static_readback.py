from pathlib import Path
import json,hashlib,gzip,stat,types,datetime
R=Path("/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7")
A=R/"audits/existing_publication_batch_b1_plus1198_v04/actor01";S=A/"private/sourceprep03";F=A/"private/focused03"
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def check(e):
 p=Path(e["path"]);b=p.read_bytes();s=p.stat();need(not p.is_symlink(),"symlink")
 need(len(b)==e["bytes"]and sha(b)==e["sha256"],"filebytes "+str(p))
 if "mode"in e:need(stat.S_IMODE(s.st_mode)==e["mode"],"mode")
 if "mtime_ns"in e:need(s.st_mtime_ns==e["mtime_ns"],"mtime")
 return b
final=json.loads((A/"PREPARATION03_FINAL_SEAL.json").read_text())
check(final["initial_seal"])
for e in final["additional_closure_files"]:check(e)
pub=json.loads((A/"PREPARATION03_MANIFEST.json").read_text());priv=json.loads(check(pub["private_manifest"]))
for e in priv["files"]:check(e)
for e in pub["source_entries"]:check({**e,"path":str(S/e["path"])})
for e in json.loads((F/"INPUTS.json").read_text())["input_pins"]:check(e)
shared=json.loads((S/"SHARED_INPUTS.json").read_text())
for e in shared.values():check(e)
core=types.ModuleType("inert_identity_primitives");raw=(S/"ops_core.py").read_bytes();exec(compile(raw,str(S/"ops_core.py"),"exec",optimize=0),core.__dict__)
plan=json.loads((S/"PROPOSAL.json").read_text());old=json.loads((A/"PROPOSAL.json").read_text())
need(core.typed_equal(plan["items"],old["items"])and core.typed_equal(plan["semantic_lead_clearances"],old["semantic_lead_clearances"])and core.typed_equal(plan["intrabatch_lead_clearances"],old["intrabatch_lead_clearances"]),"science changed")
adopt=json.loads((A/"ROOT_SEMANTIC43_PROPOSAL_ADOPTION.json").read_text())
need(core.typed_equal(plan["account_semantic_decisions"],adopt["decisions"]),"43decision transfer")
ref=json.loads((A/"private/OWNED_FIXTURE_REFERENCE.json").read_text());owned=[]
for e in ref["files"]:owned+=json.loads(check(e))
need(len(owned)==197 and 23165876 not in [x["id"]for x in owned],"owned197/external1198")
by={x["id"]:x for x in owned};items={x["pr"]:x for x in plan["items"]}
for d in adopt["decisions"]:
 item=items[d["pr"]];record=by[d["record_id"]]
 need(sha(core.canonical(record))==d["complete_raw_sha256"],"whole record hash")
 need(sha(core.canonical(record["metadata"]))==d["complete_metadata_sha256"],"whole metadata hash")
 need(d["target_doi"]==item["doi"]and d["target_four_cell_canonical_sha256"]==sha(core.canonical(item["row"]))and d["target_43_column_row_sha256"]==core.row_sha(item["row"]),"target hash")
prs=[p for x in plan["items"]for p in x["associated_prs"]];forms=[]
for p in prs:
 for t in [f"PULL\u2003REQUEST : #000{p}",f"PR:\u2002#00{p}",f"https://github.com/AlecKriebel/Math/pull/000{p}",f"ＰＲ # {p}"]:
  need(p in core.associated_pr_numbers_in_text(t),"missedPR");forms.append(t)
need(core.associated_pr_numbers_in_text("PR10070; bare1007; PR1007.5; wordingPR1007")=={10070},"nearPR false")
# Independent full archive decoding: no claimant validation routine executed.
results=json.loads((F/"RESULTS.json").read_text());blobs={};nf=nd=nb=0;cases=[]
for c in results["case_results"]:
 receipt=c["custody"];ip=Path(receipt["inventory"]);need(sha(ip.read_bytes())==receipt["inventory_sha256"],"inventory")
 inv=json.loads(ip.read_text());need(len(inv["files"])==receipt["files"]and len(inv["directories"])==receipt["directories"],"counts")
 names=set()
 for e in inv["files"]:
  rel=Path(e["relative"]);need(not rel.is_absolute()and ".."not in rel.parts and e["relative"]not in names,"unsafe/duplicate");names.add(e["relative"])
  path=Path(e["blob"])
  if str(path)not in blobs:
   need(path.stat().st_size==e["blob_bytes"]and sha(path.read_bytes())==e["blob_sha256"],"gzip container")
   h=hashlib.sha256();n=0
   with gzip.open(path,"rb")as f:
    for b in iter(lambda:f.read(65536),b""):h.update(b);n+=len(b)
   blobs[str(path)]=(n,h.hexdigest())
  need(blobs[str(path)]==(e["bytes"],e["sha256"]),"gzip content")
  need(type(e["mode"])is int and type(e["mtime_ns"])is int,"metadata")
 for e in inv["directories"]:need(type(e["mode"])is int and type(e["mtime_ns"])is int,"directory metadata")
 ce=next(e for e in inv["files"]if e["relative"]=="CASE_RESULT.json")
 data=json.loads(gzip.decompress(Path(ce["blob"]).read_bytes()))
 need(data["control_outcome"]=="PASS"and not data["real_external_attempts"]and not data["provider_infrastructure_errors"],"preparer case notpass")
 nf+=len(inv["files"]);nd+=len(inv["directories"]);nb+=sum(e["bytes"]for e in inv["files"]);cases.append({"name":c["name"],"status":data["actor_status"],"inventory_sha256":receipt["inventory_sha256"]})
print(json.dumps({"at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_manifest_sha256":sha((S/"SOURCE_MANIFEST.json").read_bytes()),"private_manifest_members":len(priv["files"]),"all108sharedpins":len(shared),"full_owned_records":len(owned),"exact_record_target_decisions":len(adopt["decisions"]),"literal_rows":len(items),"associatedPRs":len(prs),"independentPRgrammar_checks":len(forms)+1,"decoded_cases":len(cases),"verified_files":nf,"directory_metadata":nd,"unique_gzip_blobs":len(blobs),"regular_bytes_represented":nb,"unique_uncompressed_bytes":sum(x[0]for x in blobs.values()),"physical_restore_performed":False,"real_external_calls":0,"cases":cases},indent=2))

