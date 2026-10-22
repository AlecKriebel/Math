"""Apply only the independently reviewed, same-ID description transport binding."""
from pathlib import Path
import datetime,hashlib,json,os,stat,sys,tempfile
F=Path(__file__).resolve().parent; A=F.parent; D=A.parent.parent; R=D/"service_resume_20261016"; REPO=D.parent
sys.path.insert(0,str(REPO/"zenodo_deposit_tool"));import zenodo as z

def read(p):return json.loads(p.read_text())
def need(c,s):
 if not c:raise RuntimeError(s)
def ident(p):
 b=p.read_bytes();return {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def write(p,value):
 fd,tmp=tempfile.mkstemp(prefix=".transport-",dir=p.parent)
 try:
  with os.fdopen(fd,"w") as stream:stream.write(value);stream.flush();os.fsync(stream.fileno())
  os.replace(tmp,p)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
def save(p,value):write(p,json.dumps(value,indent=2)+"\n")
def once(p,value):
 need(not p.exists(),"Preserve previous adoption evidence "+str(p));save(p,value)

cfg_path=R/"PR1094_SERVICE_CONFIG.json"; old_manifest=A/"preprint_v1_0/zenodo-deposit.json"; new_manifest=F/"zenodo-deposit-html-transport.json"; new_seal=F/"ROOT_TRANSPORT_SEAL.json"
need(read(D/"STATE.json")["next_pr"]==1094,"Ascending cursor")
addendum=read(F/"review01/ADOPTION_PLAN_RECHECK.json")
need(addendum["actionable_issues"]==0,"Independent adoption-plan clearance required")
for row in read(F/"review01/SEAL.json")["outputs"]:
 need(ident(F/"review01"/row["path"])=={k:row[k]for k in ("bytes","sha256")},"Original review output changed")
for name,row in read(F/"review01/SEAL.json")["input_pins"].items():need(ident(F/name)==row,"Reviewed input changed "+name)
need(cfg_path.read_bytes()==(F/"original_config.json").read_bytes(),"Original config changed")
need((R/"prepare_service_configs.py").read_bytes()==(F/"original_prepare_service_configs.py").read_bytes(),"Original generator changed")
need((F/"proposed_prepare_service_configs.py").read_text()==(F/"original_prepare_service_configs.py").read_text().replace("1094:'preprint_v1_0/zenodo-deposit.json'","1094:'publication_transport_20261017/zenodo-deposit-html-transport.json'",1),"Single generator literal only")
pins=read(F/"PROTECTED_BEFORE_PINS.json")
for row in pins:
 p=Path(row["absolute_path"])if "absolute_path"in row else A/row["path"]
 need(ident(p)=={k:row[k]for k in ("bytes","sha256")},"Protected bytes drift "+str(p))
 if "mode"in row:need(stat.S_IMODE(p.stat().st_mode)==row["mode"],"Protected mode drift")
old_data=read(old_manifest);new_data=read(new_manifest);expected=json.loads(json.dumps(old_data["metadata"]));needle=" n >= 1,";need(expected["description"].count(needle)==1,"Exactly one approved encoding occurrence");expected["description"]=expected["description"].replace(needle," n &gt;= 1,")
need(new_data["metadata"]==expected,"Only approved encoding may change")
metadata,files=z.load_manifest(new_manifest.resolve());oldmetadata,oldfiles=z.load_manifest(old_manifest.resolve())
need([(f["path"],f["name"],f["sha256"],f["size"])for f in files]==[(f["path"],f["name"],f["sha256"],f["size"])for f in oldfiles],"Same canonical files")
old_state_path,old_state=z.local_state(old_manifest.resolve(),"production");new_state_path,new_state=z.local_state(new_manifest.resolve(),"production")
need(old_state["id"]==23431313 and new_state is None,"Original known ID and new alias absent")
client=z.ZenodoClient("production",z.token_for("production"));remote=client.get(23431313);z.validate_record(remote,23431313);need(remote["submitted"]is False,"Draft must remain unpublished");norm=z.verify(remote,metadata,files);need(norm==[],"Exact wire metadata required")
old_cfg=read(cfg_path); seal={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"pr":1094,"head":old_cfg["head"],"status":"ROOT_READY_EXACT_HTML_TRANSPORT_ADOPTED","publication_ready":True,"actionable_issues":0,"whole_reviews_completed":2,"new_whole_review_credit":0,"scope":"Single lossless paragraph inequality encoding required by Zenodo; no paper, kit, proof, scope, source, credit or disclosure changes","source_final_seal":{"path":str((A/"FINAL_SEAL.json").relative_to(D)),**ident(A/"FINAL_SEAL.json")},"native_manifest":{"path":str(new_manifest.relative_to(D)),**ident(new_manifest)},"metadata_sha256":hashlib.sha256(json.dumps(metadata,sort_keys=True,separators=(",",":")).encode()).hexdigest(),"same_existing_production_id":23431313,"files":old_cfg["files"],"protected_pre_adoption_rows_verified":len(pins),"post_adoption_exception":"Only active service config row changes; exact original remains in original_config.json. Original 159 preprint files, historical final seal and native/driver bytes remain exact.","independent_review":{"original_seal":ident(F/"review01/SEAL.json"),"resolved_plan":ident(F/"review01/ADOPTION_PLAN_RECHECK.json")},"generator_new":ident(F/"proposed_prepare_service_configs.py"),"plan":ident(F/"ADOPTION_STATE_PATCH.json"),"priority_novelty_worldwide_openness":"UNKNOWN","external_service_read_only_before_adoption":True}
once(new_seal,seal)
cfg=json.loads(json.dumps(old_cfg));cfg.update(manifest=str(new_manifest.relative_to(D)),manifest_identity=ident(new_manifest),metadata_sha256=seal["metadata_sha256"],final_seal=str(new_seal.relative_to(D)),final_seal_identity=ident(new_seal))
once(F/"ADOPTION_INTENT.json",{"utc":seal["utc"],"id":23431313,"new_manifest":cfg["manifest"],"new_seal":cfg["final_seal"],"original_config":ident(cfg_path),"new_config_expected":cfg,"service_mutation":False})
z.save_state(new_state_path,{"manifest":str(new_manifest.resolve()),"environment":"production","id":23431313})
# Persist both the generator path and its authority, then the active config.
write(R/"prepare_service_configs.py",(F/"proposed_prepare_service_configs.py").read_text())
state=read(D/"STATE.json");state.setdefault("current_final_authorities",{})["1094"]=str(new_seal.relative_to(D));state.setdefault("native_transport_overrides",{})["1094"]={"source_manifest":str(old_manifest.relative_to(D)),"wire_manifest":str(new_manifest.relative_to(D)),"same_production_id":23431313,"semantic_change":False};save(D/"STATE.json",state)
save(cfg_path,cfg)
need(read(cfg_path)==cfg,"Config readback");need(read(D/"STATE.json")["current_final_authorities"]["1094"]==cfg["final_seal"],"STATE authority readback");need((R/"prepare_service_configs.py").read_bytes()==(F/"proposed_prepare_service_configs.py").read_bytes(),"Generator readback")
need(z.local_state(old_manifest.resolve(),"production")[1]==old_state,"Old alias preserved");need(z.local_state(new_manifest.resolve(),"production")[1]["id"]==23431313,"Same ID alias readback")
for row in pins:
 p=Path(row["absolute_path"])if "absolute_path"in row else A/row["path"]
 if p==cfg_path:continue
 need(ident(p)=={k:row[k]for k in ("bytes","sha256")},"Post-adoption protected drift")
remote=client.get(23431313);need(not remote["submitted"],"No publication during binding");need(z.verify(remote,metadata,files)==[],"Final exact wire readback")
once(F/"ROOT_ADOPTION_READBACK.json",{"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"PASS_ALL_BINDINGS_SAME_ID_READ_BACK","same_production_id":23431313,"submitted":False,"publication_ready":True,"whole_reviews_completed":2,"new_whole_review_credit":0,"actionable_issues":0,"protected_rows_unchanged":len(pins)-1,"config_original_preserved":ident(F/"original_config.json"),"config_current":ident(cfg_path),"generator_current":ident(R/"prepare_service_configs.py"),"state_authority":read(D/"STATE.json")["current_final_authorities"]["1094"],"remote_metadata_normalizations":[],"completion_percent":94})
print(json.dumps({"status":"ROOT_ADOPTION_PASS","id":23431313,"publication_ready":True}))
