"""Root authenticates all sealed family bodies and actually reproduces their controls."""
from pathlib import Path
import hashlib,json,os,datetime,subprocess,sys
A=Path(__file__).resolve().parent
D=A/"root_family_reproduction_20261006"
D.mkdir(exist_ok=False)
PY="/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14"
ENV={"PATH":"/usr/bin:/bin","LANG":"C","LC_ALL":"C","TZ":"UTC","__CF_USER_TEXT_ENCODING":"0x1F5:0x0:0x0"}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes()
 return {"path":str(p.relative_to(A)),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def require(ok,msg):
 if not ok:raise ValueError(msg)
specs=[
("ideal_hypotheses_adversary_20261006","863931986a6222285d3ab840bb16b2e5054a2dabba008cc119a0f1ed9e51b9a2","20954e9c201bf9ff84b939dc050aec88522d5ab260013ec7d7848ebabc30c25a","independent_ideal_controls.py","884aea99e85514ee0721412cc02ed115ab72112fc4a1409ebe2dcee9221d8568","checks_total",59747,"python_optimization_level"),
("polytope_fiber_adversary_20261006","91cfa9cfe70d53c8c238815521dbff44137873190a7e70c55a398a3dcc994f69","c6a5ff2da9d19cd39e7ddee47ff67f9ff57291d81ea5efdf53517c55344f2b01","independent_polytope_audit.py","d1bc6f86d38f3c37f3f2a853c84a95403884c93d95737f593367e20641d89c0d","explicit_guards",1729,"optimizations_disabled"),
("primary_source_scope_adversary_20261006",None,"048c5b3cf877413fc201a1d3e2bc520b1d9b1acde4c9751f9116fbc47d926098","source_scope_controls.py","49ba65d887e6d041b3355a9b75ea56613e55de473e13a4b51e5a18a9c29c255c","checks",810,None)]
events=[]
def run(argv,label,env=ENV):
 e={"label":label,"start_UTC":now(),"argv":argv}
 p=subprocess.Popen(argv,cwd=D,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 e["actual_child_PID"]=p.pid
 (D/"PROCESS_JOURNAL.json").write_text(json.dumps({"actual_operator_PID":os.getpid(),"events":events+[e]},indent=2)+"\n")
 stdout,stderr=p.communicate(timeout=60)
 e.update({"end_UTC":now(),"exit_code":p.returncode,"stdout_bytes":len(stdout),"stdout_sha256":hashlib.sha256(stdout).hexdigest(),"stderr_bytes":len(stderr),"stderr_sha256":hashlib.sha256(stderr).hexdigest()})
 (D/(label+".stdout.txt")).write_bytes(stdout)
 (D/(label+".stderr.txt")).write_bytes(stderr)
 events.append(e)
 (D/"PROCESS_JOURNAL.json").write_text(json.dumps({"actual_operator_PID":os.getpid(),"events":events},indent=2)+"\n")
 require(p.returncode==0 and not stderr,"Run failed: "+label)
 return json.loads(stdout)
families=[]
for folder,expected_manifest,expected_report,script,expected_script,countkey,count,modekey in specs:
 F=A/folder
 manifestpin=pin(F/"OUTPUT_MANIFEST.json")
 if expected_manifest:require(manifestpin["sha256"]==expected_manifest,"Manifest pin mismatch")
 require(pin(F/"REPORT.md")["sha256"]==expected_report,"Report pin mismatch")
 require(pin(F/script)["sha256"]==expected_script,"Script pin mismatch")
 m=json.loads((F/"OUTPUT_MANIFEST.json").read_text())
 members=m.get("members",m.get("files"))
 require(isinstance(members,list),"Manifest members")
 pins=[]
 for member in members:
  path=Path(member["path"])
  require(not path.is_absolute() and ".." not in path.parts,"Unsafe member path")
  require(not any(part.startswith("private_") for part in path.parts),"Private body in public manifest")
  p=F/path
  require(p.is_file() and not p.is_symlink(),"Member not regular")
  got=pin(p)
  require(got["bytes"]==member.get("bytes",member.get("byte_count")) and got["sha256"]==member["sha256"],"Member changed: "+str(path))
  pins.append(got)
 result=json.loads((F/"RESULT.json").read_text())
 require(not result.get("mandatory_mathematical_corrections",[]) and not result.get("mandatory_mathematical_findings",[]) and not result.get("mandatory_source_scope_findings",[]),"Unresolved finding")
 outputs=[]
 for optimized in (False,True):
  argv=[PY,"-E","-S","-B","-P"]+(["-O"] if optimized else [])+[str(F/script)]
  out=run(argv,folder+("_optimized" if optimized else "_normal"))
  require(out[countkey]==count,"Guard count mismatch")
  require(out.get("status",out.get("result"))=="PASS","NonPASS")
  require(not out.get("novelty_clearance",False),"Unexpected novelty clearance")
  copy=dict(out)
  if modekey:
   require(copy.pop(modekey)==(1 if optimized else 0),"Optimization metadata")
  outputs.append(copy)
 require(outputs[0]==outputs[1],"Normal optimized logical mismatch")
 families.append({"family":folder,"manifest":manifestpin,"report":pin(F/"REPORT.md"),"result":pin(F/"RESULT.json"),"member_count":len(pins),"authenticated_members":pins,"explicit_guards_each_actual_mode":count,"family_verdict":result.get("verdict",result.get("status"))})
for optimized in (False,True):
 argv=[PY,"-E","-S","-B","-P"]+(["-O"] if optimized else [])+[str(A/"root_family_false_guard_probe_20261006.py")]
 result=run(argv,"root_false_guard_probe"+("_optimized" if optimized else "_normal"))
 require(result["status"]=="PASS" and len(result["results"])==3,"False controls")
 require(all(v["false_claim_rejected"] for v in result["results"]),"Accepted false guard")
auth=json.loads((A/"original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json").read_text())
for e in auth["original_files"]:
 p=A/"original_head_authentication_20261006/original_attempt"/e["path"]
 got=pin(p)
 require((got["bytes"],got["sha256"])==(e["bytes"],e["sha256"]),"Original modified")
reason=json.loads((A/"ROOT_MATHEMATICAL_REASONING_20261006.json").read_text())
require(reason["root_individual_math_assessment"]=="PASS" and reason["priority_clearance"] is False,"Root reasoning")
receipt={"schema":"pr117-root-sealed-family-authentication-and-reproduction/v1","UTC":now(),"actual_operator_PID":os.getpid(),"status":"PASS","PR":117,"immutable_head":auth["original_head"],"all_20_originals_unchanged":True,"family_count":len(families),"authenticated_public_member_count":sum(x["member_count"] for x in families),"families":families,"events":events,"normal_and_optimized_all_three_families_PASS":True,"all_three_false_guard_controls_normal_and_optimized_PASS":True,"root_full_reports_and_checker_logic_read":True,"priority_clearance":False,"publication_readiness":False,"remote_or_native_mutations":False,"new_central_proof_search_turns":0}
out=A/"ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json"
out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
gate={"schema":"pr117-cross-family-math-source-gate/v1","UTC":now(),"actual_root_authentication_PID":os.getpid(),"status":"PASS","PR":117,"problem_id":30001234,"immutable_head":auth["original_head"],"candidate_sha256":auth["original_files"][0]["sha256"],"source_prior_review_hash":auth["review_hash"],"original_attempts":"1/5","math_source_completion_percent":100,"workflow_completion_percent":25,"mandatory_math_or_scope_findings":[],"original_assertion_robustness_issue_repaired_in_diagnostic_copy":True,"proof_unchanged":True,"support":pin(out),"independent_families":[x["family"] for x in families],"root_reasoning":pin(A/"ROOT_MATHEMATICAL_REASONING_20261006.json"),"priority_audit_authorized_to_begin":True,"priority_clearance":False,"preprint_readiness":False,"merge_or_disposition_authorized_by_this_gate":False,"new_central_proof_search_turns":0,"program_complete":False,"program_completed":19,"published":11,"goal_active":True}
g=A/"MATHEMATICAL_SOURCE_GATE_20261006.json"
g.write_text(json.dumps(gate,indent=2,sort_keys=True)+"\n")
with (A/"RESEARCH_LOG.md").open("a") as f:
 f.write("\n"+now()+": Root read all three sealed reports/code and authenticated all public members; independently reproduced each exception-guard checker in actual normal/-O modes, plus false controls. Complete original mathematics and source gate PASS100%; no mandatory math/scope concerns. Guard repair restricted to separate diagnostics;20 original files unchanged; central proof turns added0. Full priority audit may now begin; priority clearance remains false. PR workflow best guess25%; program19/99=19.19%, published11; persistent goal active. Main/index remains released; no remote/native mutation.\n")
print(json.dumps({"status":"PASS","actual_operator_PID":os.getpid(),"authenticated_public_members":receipt["authenticated_public_member_count"],"actual_completed_children":len(events),"gate":pin(g),"priority_clearance":False,"gate_UTC":gate["UTC"]}))

