"""Bounded PR195 mathematical-clearance checkpoint; Root separately moves MAIN."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent
PREFIX="draft_pr_publication_program_20260930/";CASE=PREFIX+"audits/pr195_30004601/"
PRIOR=A/"intake_checkpoint_preparation_01/checkpoint_intake01";QUEUE="unsolved_math_prioritization/QUEUE.md"
MUTABLE={PREFIX+x for x in ["CURRENT_PROGRESS.json","CURRENT_PROGRESS.md","RESEARCH_LOG.md"]}|{CASE+x for x in ["CURRENT_CASE_STATUS.json","RESEARCH_LOG.md"]}
def read(p):return json.loads(Path(p).read_bytes())
def encode(j):return (json.dumps(j,indent=2)+"\n").encode()
def pin(b):return {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def save(p,b):
 with p.open("xb") as f:f.write(b)
 p.chmod(0o444)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load():
 path=A/"intake_checkpoint_preparation_01/prepare_intake_checkpoint.py"
 assert pin(path.read_bytes())=={"bytes":17138,"sha256":"35ffe71e114b1d2b20a0130626a68ed39bdb61cc98294612e0cd09a641992bd2"}
 sp=importlib.util.spec_from_file_location("approved195_lowlevel",path);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
 c,h=v.load();h.m.TREE_CACHE_PATH=A/"SCIENCE_PRIVATE_TREE_CACHE.json";return v,c,h
QUEUE_REVIEW_PINS={'ROOT_SCIENCE_REVIEWED_QUEUE_01.json': {'bytes': 1655, 'sha256': 'd80468b91a49b93f430d6f8b8aee918b779ffb4c921617b5d279f279dd060aee'}, 'ROOT_SCIENCE_QUEUE_OBSERVATION_01.json': {'bytes': 1452, 'sha256': '8d2f9571e49fe5792cb033841305f533545f29f82195a2581c9945ea5751f1c4'}, 'ROOT_SCIENCE_FOREIGN_QUEUE_DIFF_01.diff': {'bytes': 1382, 'sha256': '990b07f908269544b8f52653ccbb44cfbace346440c531821be7217dcabd9f97'}}
def inputs():
 out={}
 for dirname in ["polar_syzygy_audit_01","generic_initial_source_audit_01","exact_reproduction_audit_01"]:
  folder=A/dirname;allow=read(folder/"SAFE_ALLOWLIST.json")
  for name in allow["files"]:
   file=folder/name;assert file.is_file() and not file.is_symlink() and file.stat().st_mode&0o777==0o444
   out[CASE+dirname+"/"+name]=file.read_bytes()
 gate=(A/"ROOT_MATHEMATICAL_GATE_01.json").read_bytes()
 assert pin(gate)=={"bytes":7426,"sha256":"c033bcd68a3ce4809ba40916b48a5c4ad9734fa3aad07f9e6e7c60d13e1306c0"}
 g=json.loads(gate);assert g["mathematical_clearance"] is True and len(g["three_new_independent_audit_families"])==3
 for dirname,review in g["three_new_independent_audit_families"].items():
  for name,x in review["safe_files"].items():assert pin(out[CASE+dirname+"/"+name])==x
 out[CASE+"ROOT_MATHEMATICAL_GATE_01.json"]=gate
 for name,x in QUEUE_REVIEW_PINS.items():
  b=(A/name).read_bytes();assert pin(b)==x;out[CASE+name]=b
 for name in ["ROOT_POLAR_AUDIT_ACCEPTANCE_01.json","ROOT_GENERIC_INITIAL_SOURCE_ACCEPTANCE_01.json","ROOT_INTAKE_HELPER_AUTHENTICATION_01.json"]:
  out[CASE+name]=(A/name).read_bytes()
 for name in ["PREPARATION.json","ROOT_PRE_MOVE_VERIFICATION.json","INTAKE_CHECKPOINT_ACCEPTANCE.json"]:
  out[CASE+"intake_checkpoint_preparation_01/checkpoint_intake01/"+name]=(PRIOR/name).read_bytes()
 out[CASE+"science_checkpoint_02/checkpoint_math195.py"]=Path(__file__).read_bytes()
 return g,out
def baseline(c,h,current):
 r=read(PRIOR/"PREPARATION.json");a=read(PRIOR/"INTAKE_CHECKPOINT_ACCEPTANCE.json")
 assert a["accepted"] is True and a["checkpoint_commit"]==r["commit"]=="43b91eb9b9274d997fe94a25fe7cf69a1ca8857d"
 assert a["every_selected_identity_checked_at_actual_observed_MAIN"] is True and a["selected_files"]==len(r["selected_files"])==1307
 assert a["selected_map_sha256"]==r["selected_map_sha256"]==c.selected_digest(r["selected_files"])
 assert (a["fully_completed_count"],a["published_count"],a["last_completed_PR"])==(41,25,193)
 assert c.selected_current(h,a["main_observed"],r["selected_files"],r["tree"])==a["actual_tree"]
 main=h.api("git/ref/heads/main")["object"]["sha"]
 assert h.api("compare/"+r["commit"]+"..."+main)["status"] in ["identical","ahead"]
 gate=read(A/"ROOT_SCIENCE_REVIEWED_QUEUE_01.json")
 assert pin((A/"ROOT_SCIENCE_REVIEWED_QUEUE_01.json").read_bytes())==QUEUE_REVIEW_PINS["ROOT_SCIENCE_REVIEWED_QUEUE_01.json"]
 assert gate["historical_checkpoint_main"]==a["main_observed"] and gate["historical_queue_pin"]==r["selected_files"][QUEUE] and gate["Root_full_diff_read"] is True and gate["all_other1306_selected_identities_unchanged"] is True and gate["QUEUE_overlay_authorized"] is False and gate["unchanged_own_problem_ids"]==[30004563,30004601]
 old=h.body_at(QUEUE,a["main_observed"]);new=h.body_at(QUEUE,gate["observed_main"]);assert c.byte_pin(old)==gate["historical_queue_pin"] and c.byte_pin(new)==gate["current_queue_pin"]
 before=old.decode().splitlines(keepends=True);after=new.decode().splitlines(keepends=True);assert len(before)==len(after)
 def rid(line):
  cells=line.split("|");v=cells[2].strip().split() if len(cells)>3 else []
  return int(v[0]) if v and v[0].isdigit() else None
 delta=[{"problem_id":rid(x),"before":x,"after":y} for x,y in zip(before,after) if x!=y]
 assert delta==gate["exact_changed_lines"] and [x["problem_id"] for x in delta]==gate["changed_foreign_problem_ids"] and all(x["problem_id"] not in [30004563,30004601] and x["problem_id"]==rid(x["after"]) for x in delta)
 for pid in [30004563,30004601]:
  row=[x for x in before if rid(x)==pid];assert len(row)==1 and row==[x for x in after if rid(x)==pid]
 inherited={**r["selected_files"],QUEUE:gate["current_queue_pin"]}
 assert c.selected_current(h,gate["observed_main"],inherited,gate["observed_tree"])==gate["observed_tree"]
 assert h.api("compare/"+r["commit"]+"..."+gate["observed_main"])["status"] in ["identical","ahead"]
 if current:c.selected_current(h,main,inherited,gate["observed_tree"])
 return inherited,main
def overlay(c,h,parent,stamp):
 g,out=inputs();case=read(A/"intake_checkpoint_preparation_01/CASE_BASELINE20.json")
 case.update(UTC=stamp,status="MATHEMATICS_CLEARED_DEEP_PRIORITY_AUDIT_ACTIVE",case_percent=45,mathematical_result_valid=True,mathematical_clearance=True,independent_mathematical_audit_families_complete=3,independent_mathematical_audit_active=False,mathematical_gate="ROOT_MATHEMATICAL_GATE_01.json",mathematical_gate_sha256=pin((A/"ROOT_MATHEMATICAL_GATE_01.json").read_bytes())["sha256"],priority_audit_active=True,priority_audit_complete=False,remaining_required_steps="Complete deep priority audit; qualified publication only if supported; prepare package and successive NEW whole-package reviews; actual publication/tracker/originalHEAD-safe merge/factual MAIN acceptance.")
 out[CASE+"CURRENT_CASE_STATUS.json"]=encode(case)
 p=json.loads(h.body_at(PREFIX+"CURRENT_PROGRESS.json",parent))
 assert (p["current_PR"],p["fully_completed_count"],p["published_count"],p["last_completed_PR"])==(195,41,25,193)
 p.setdefault("historical_current_case_snapshots",[]).append({"UTC":stamp,"PR":195,"prior_phase":20,"values":{k:v for k,v in p.items() if k.startswith("current_")}})
 p.update(UTC=stamp,updated_UTC=stamp,current_PR_workflow_percent=45,current_workflow_estimate_percent=45,current_status=case["status"],current_mathematical_clearance=True,current_mathematics_cleared=True,current_mathematical_result_valid=True,current_independent_mathematical_audit_active=False,current_independent_mathematical_audit_families_complete=3,current_mathematical_gate="audits/pr195_30004601/ROOT_MATHEMATICAL_GATE_01.json",current_priority_audit_active=True,current_priority_clearance=False,current_priority_audit_complete=False,current_remaining_required_steps=case["remaining_required_steps"],remaining_current_step="Complete current195 deep priority audit; paper/publication/merge remain pending.",next_step="Complete195 priority audit before paper/package preparation; no196 intake.",program_snapshot_semantics="PR195 mathematics cleared by3NEW independent families and Root exact read-only reproductions; deep priority audit active and unresolved.41completed/25published,last193;cursor195/conditional196/advancefalse,broader goal active.",program_snapshot_authority_condition="Mathematical45 checkpoint postimage effective only after actual true-parent/fullscope/all-current-identities acceptance. No priority,publication or next-intake authority.")
 assert p["advance_to_next_PR_authorized_now"] is False and p["current_completed"] is False
 out[PREFIX+"CURRENT_PROGRESS.json"]=encode(p)
 note="\n"+stamp+" — PR195 mathematical45% checkpoint: corrected second-variable conjecture disproved by characteristic-zero seven-plane arrangement, cutoff8/degree7 largest-variablex3 generator.3NEW independent families CLEANPASS,Root reports/sources/full30safe hashes/read-only verifiers authenticated. Genericity is algebraic,not sampled; ambient4polars distinguished from restricted arrangement Jacobian. Historical novelty/priority unestablished; deep priority audit active, no paper/package/publication/tracker/merge clearance.41completed/25published,last193;cursor195/advancefalse; broader goal active.\n"
 for name in [CASE+"RESEARCH_LOG.md",PREFIX+"CURRENT_PROGRESS.md",PREFIX+"RESEARCH_LOG.md"]:out[name]=h.body_at(name,parent)+note.encode()
 return out
def selected(c,base,out):
 assert QUEUE not in out
 for name,b in out.items():
  assert name.startswith(CASE) or name in MUTABLE
  if name in base and name not in MUTABLE:assert c.byte_pin(b)==base[name]
 return {**base,**{name:c.byte_pin(b) for name,b in out.items()}}
def message(digest):return "Record PR195 mathematical45 clearance; priority pending;41completed/25published\n\nPR195 scientific selected-map SHA256: "+digest
def original(h):
 p=h.api("pulls/195");assert p["head"]["sha"]=="e776a961293116775fed2cb2a3019d577b84c04a" and p["state"]=="open" and p["draft"] is True and p["merged"] is False
def prepare(v,c,h,gen):
 base,parent=baseline(c,h,True);original(h);stamp=now();out=overlay(c,h,parent,stamp);expected=selected(c,base,out);dest=D/gen;dest.mkdir(exist_ok=False)
 pt=h.api("git/commits/"+parent)["tree"]["sha"];tree=h.api("git/trees","POST",{"base_tree":pt,"tree":[{"path":n,"mode":"100644","type":"blob","content":b.decode()} for n,b in sorted(out.items())]})
 co=h.api("git/commits","POST",{"tree":tree["sha"],"parents":[parent],"message":message(c.selected_digest(expected))});h.m.m.h.warm_selected_directories([pt,tree["sha"]],expected)
 r={"UTC":stamp,"expected_main":parent,"parent_tree":pt,"tree":tree["sha"],"commit":co["sha"],"selected_files":expected,"selected_map_sha256":c.selected_digest(expected),"overlay_paths":sorted(out),"changed_paths":sorted(n for n,x in expected.items() if h.lookup(pt,n)!=("100644","blob",x["git_blob"])),"MAIN_moved":False}
 save(dest/"PREPARATION.json",encode(r));v.verify_object(c,h,r,expected,message(c.selected_digest(expected)));assert h.api("git/ref/heads/main")["object"]["sha"]==parent;print(json.dumps({k:r[k] for k in ["expected_main","commit","tree"]}|{"selected":len(expected),"changed":len(r["changed_paths"])}))
def accept(v,c,h,gen):
 r=read(D/gen/"PREPARATION.json");base,main=baseline(c,h,False);out=overlay(c,h,r["expected_main"],r["UTC"]);expected=selected(c,base,out);assert r["overlay_paths"]==sorted(out);v.verify_object(c,h,r,expected,message(c.selected_digest(expected)))
 assert h.api("compare/"+r["commit"]+"..."+main)["status"] in ["identical","ahead"]
 tree=c.selected_current(h,main,expected,r["tree"])
 for name,b in out.items():assert h.body_at(name,main)==b
 assert c.byte_pin(h.body_at(QUEUE,main))==base[QUEUE];original(h)
 a={"UTC":now(),"PR":195,"accepted":True,"status":"ACTUAL_PR195_MATHEMATICAL45_FULL_SCOPE_ALL_CURRENT_IDENTITIES_ACCEPTED","checkpoint_commit":r["commit"],"sole_parent":r["expected_main"],"main_observed":main,"actual_tree":tree,"selected_files":len(expected),"selected_map_sha256":c.selected_digest(expected),"every_selected_identity_checked_at_actual_observed_MAIN":True,"all_output_bodies_verified":True,"mathematical_clearance":True,"priority_clearance":False,"publication_ready":False,"fully_completed_count":41,"published_count":25,"last_completed_PR":193,"case_percent":45,"QUEUE_native_PR_unchanged":True,"next_numeric_intake_cursor":195,"advance_to_next_PR_authorized_now":False,"goal_complete":False}
 save(D/gen/"ACCEPTANCE.json",encode(a));print(json.dumps(a))
if __name__=="__main__":
 assert sys.dont_write_bytecode
 v,c,h=load();{"prepare":prepare,"accept":accept}[sys.argv[1]](v,c,h,sys.argv[2])
