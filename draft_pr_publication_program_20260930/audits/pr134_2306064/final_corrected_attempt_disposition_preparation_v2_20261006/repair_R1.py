from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import difflib,json,os,shutil

S=Path(__file__).resolve().parent
A=S.parent
P=A/"final_corrected_attempt_disposition_preparation_20261006"
R=A/"final_disposition_postimage_adversary_20261006"
V=A/"corrected_attempt_preparation_20261006/corrected_attempt"
PID=os.getpid()
START=datetime.now(timezone.utc).isoformat()
CHECKS=0
def utc():return datetime.now(timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return {"bytes":len(b),"sha256":sha256(b).hexdigest()}
def ck(v,m):
 global CHECKS
 CHECKS+=1
 if not v:raise RuntimeError(m)
def js(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
def txt(p,s):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
def authenticate(root,h,count):
 p=root/"FINAL_MANIFEST.json";ck(pin(p)["sha256"]==h,"Input seal changed")
 m=json.loads(p.read_text());ck(m["member_count"]==count,"Input member count")
 for x in m["members"]:ck(pin(root/x["path"])=={k:x[k] for k in ["bytes","sha256"]},"Input body changed: "+x["path"])
 return m
ck(not (S/"corrected_attempt").exists(),"Successor already populated")
pm=authenticate(P,"85259c31a08a7c1fc389d22cc793d181ec446e4feeee542756cfe8cd8c6f8d72",85)
rm=authenticate(R,"34a3fe5449c1538d5fdd82b3fad6544408f83ff0e68c01ffa2fe798c3a4297cd",7)
rr=json.loads((R/"RESULT.json").read_text())
ck(rr["verdict"]=="FAIL_REPAIR_REQUIRED_SINGLE_REPLAY_RECEIPT_REFERENCE","Exact bounded fail verdict")
ck(len(rr["blocking_findings"])==1 and rr["blocking_findings"][0]["id"]=="R1","Exactly R1 required")
finding=rr["blocking_findings"][0]
ck(finding["required_value"]=="../../REPLAY_RESULTS.json" and finding["needs_diagnostic_rerun"] is False,"R1 scope")
for x in pm["members"]:
 dest=S/x["path"];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/x["path"],dest)
prov=S/"provenance";prov.mkdir()
for src,name in [
 (P/"FINAL_MANIFEST.json","PREDECESSOR_FINAL_MANIFEST.json"),
 (P/"CORRECTED_17_MANIFEST.json","PREDECESSOR_CORRECTED_17_MANIFEST.json"),
 (P/"REPORT.md","PREDECESSOR_REPORT.md"),
 (P/"RESULT.json","PREDECESSOR_RESULT.json"),
 (R/"REPORT.md","R1_FAIL_REVIEW_REPORT.md"),
 (R/"RESULT.json","R1_FAIL_REVIEW_RESULT.json"),
 (R/"FINAL_MANIFEST.json","R1_FAIL_REVIEW_FINAL_MANIFEST.json")
]:shutil.copyfile(src,prov/name)
summary_rel="corrected_attempt/review/review_summary.json"
summary=S/summary_rel
old_bytes=summary.read_bytes()
before=json.loads(old_bytes)
ck(before["replay_receipt"]=="../REPLAY_RESULTS.json","Exact old link")
old=b'"replay_receipt": "../REPLAY_RESULTS.json"'
new=b'"replay_receipt": "../../REPLAY_RESULTS.json"'
ck(old_bytes.count(old)==1,"Single exact byte replacement")
summary.write_bytes(old_bytes.replace(old,new,1))
after=json.loads(summary.read_bytes())
ck(after["replay_receipt"]=="../../REPLAY_RESULTS.json","New link value")
before.pop("replay_receipt");after.pop("replay_receipt")
ck(before==after,"No other summary JSON value changed")
target=(summary.parent/"../../REPLAY_RESULTS.json").resolve()
ck(target==S/"REPLAY_RESULTS.json" and target.is_file(),"Corrected link resolves")
ck(pin(target)["sha256"]=="c4627a4f18bbab5e38152cfe53d1674c41738f45fb4dbaf858f7f7d9e1bce9fc","Exact unchanged full receipt")

parent17=json.loads((P/"CORRECTED_17_MANIFEST.json").read_text())
operative=S/"corrected_attempt"
parentoperative=P/"corrected_attempt"
current_members={str(p.relative_to(operative)):pin(p) for p in operative.rglob("*") if p.is_file()}
parent_members={str(p.relative_to(parentoperative)):pin(p) for p in parentoperative.rglob("*") if p.is_file()}
ck(len(current_members)==17 and set(current_members)==set(parent_members),"Exactly same17 members")
changed17=[p for p in current_members if current_members[p]!=parent_members[p]]
ck(changed17==["review/review_summary.json"],"Only R1 postimage changed")
for rel in parent_members:
 if rel!="review/review_summary.json":ck(current_members[rel]==parent_members[rel],"Other postimage changed")
ck(current_members["CANDIDATE.md"]=={"bytes":16519,"sha256":"fd4240fdd20ec35bb429a3d6c439d04cd5f4429a8b86b4239380c62deb4588f6"},"Candidate exact unchanged")
ck(current_members["review/independent_checks.py"]["sha256"]=="4ccfb72d1f9e41c92eed9f26becd9ae1ece41f43718a74038bf993edf413686d","Checker exact unchanged")
receipts=[]
for x in pm["members"]:
 rel=x["path"]
 if rel in ["REPLAY_RESULTS.json","REPLAY_JOURNAL.jsonl","RETAINED_INDEPENDENT_EXERCISE.json"] or rel.startswith("runs/") or rel.startswith("retained_independent_runs/"):
  ck(pin(S/rel)=={k:x[k] for k in ["bytes","sha256"]},"Full original receipt/outputs changed")
  receipts.append({"path":rel,**pin(S/rel)})
# Only affected baseline diff changes; other11 baseline diffs stay byte-identical.
diff_rel="diffs_from_sealed_v2/review__review_summary.json.diff"
full_diff="".join(difflib.unified_diff((V/"review/review_summary.json").read_text().splitlines(keepends=True),summary.read_text().splitlines(keepends=True),fromfile="sealed_v2/review/review_summary.json",tofile="final_prepared_postimage/review/review_summary.json"))
txt(S/diff_rel,full_diff)
one_diff="".join(difflib.unified_diff((P/summary_rel).read_text().splitlines(keepends=True),summary.read_text().splitlines(keepends=True),fromfile="failed_stage/review/review_summary.json",tofile="successor/review/review_summary.json"))
one_path="repair_diffs/R1_review_summary_replay_reference.diff"
txt(S/one_path,one_diff)
for p in (P/"diffs_from_sealed_v2").iterdir():
 if p.name!="review__review_summary.json.diff":ck(pin(S/"diffs_from_sealed_v2"/p.name)==pin(p),"Unrelated diff changed")
for x in parent17["members"]:
 rel=x["path"]
 if rel=="review/review_summary.json":
  x["new_postimage"]=current_members[rel];x["diff"]=pin(S/diff_rel)
parent17.update({"schema":"pr134-final-qualified-disposition17/r1-successor","actual_writer_pid":PID,"utc":utc(),"status":"final-operative-disposition-postimages-preparation_only","predecessor_stage":str(P),"predecessor_seal":pin(P/"FINAL_MANIFEST.json"),"r1_fail_review_result":pin(R/"RESULT.json"),"successor_repair":"R1 replay_receipt ../REPLAY_RESULTS.json -> ../../REPLAY_RESULTS.json only","changed_from_predecessor_stage_count":1,"changed_from_predecessor_stage_paths":changed17,"new_diagnostic_runs_performed":False,"new_successor_consistency_review":"PENDING_NEW_INDEPENDENT_ADVERSARY"})
js(S/"CORRECTED_17_MANIFEST.json",parent17)

report="""# R1 successor disposition-stage preparation

Status: final-operative-disposition-postimages-preparation_only; R1 corrected and self-checked, NEW independent successor consistency review pending.

The sole operative17 change is corrected_attempt/review/review_summary.json: replay_receipt changes from ../REPLAY_RESULTS.json to ../../REPLAY_RESULTS.json. The repaired file-relative path resolves to the unchanged stage-root REPLAY_RESULTS.json, SHA-256 c4627a4f18bbab5e38152cfe53d1674c41738f45fb4dbaf858f7f7d9e1bce9fc. No other summary value, mathematical/disposition postimage, candidate, checker or full execution receipt changes.

The predecessor's85 sealed members and bounded FAIL review's7 sealed members remain untouched. The predecessor seal is85259c31a08a7c1fc389d22cc793d181ec446e4feeee542756cfe8cd8c6f8d72; the fail-review seal is34a3fe5449c1538d5fdd82b3fad6544408f83ff0e68c01ffa2fe798c3a4297cd. Their reports/results/seals are preserved by copies in provenance. The fail review identifies exactly R1 and explicitly requires no mathematical diagnostic rerun.

The candidate remains16519bytes/SHAfd4240fdd20ec35bb429a3d6c439d04cd5f4429a8b86b4239380c62deb4588f6; explicit-if checker remains SHA4ccfb72d1f9e41c92eed9f26becd9ae1ece41f43718a74038bf993edf413686d. Author/replay50840 and independent normal/optimized28722 with optimized false-guard rejection retain their full original bytes, PIDs and dates. No diagnostic is rerun or presented as a new successor execution.

Scientific disposition is unchanged: original literal target already_solved by the verified older1975 consequence; candidate mathematics PASS; whole historical subsumption not established; alternative polynomial novelty UNRESOLVED; express first named-answer priority UNVERIFIED. Scientific clearance is not global/service/publication approval. Closure URL/status, DOI and tracker stay null/false; actual native/author/global/closure work remains pending.

The affected sealed-v2 baseline diff and a single-field repair diff are refreshed, together with the17-manifest, stage result/report and enclosing seal. Nonblocking prose observations are intentionally untouched because the bounded instruction is only R1. Original effort1/5, substantive1,newproof0,no human review remain unchanged. No native/author/index/HEAD/PR/service writes or external individual communication occurred. All writes are confined to this new successor folder, which remains excluded from the current core checkpoint plan.

Bounded successor preparation100%; independent successor consistency clearance and all actual global/service actions remain pending.
"""
txt(S/"REPORT.md",report)
txt(S/"README.md","# R1-only frozen successor\n\nSee REPORT.md, CORRECTED_17_MANIFEST.json and repair_diffs/R1_review_summary_replay_reference.diff. Exactly one operative JSON link is repaired; all other17 content and all actual run receipts are unchanged. No diagnostics rerun. NEW independent successor review is pending; scientific outcome and unexecuted global/closure/publication limits remain unchanged. Older85-stage and7-review seals are preserved. This folder is excluded from the current core checkpoint plan.\n")
with (S/"PROCESS_JOURNAL.jsonl").open("a") as f:
 f.write(json.dumps({"utc":utc(),"actual_operator_pid":PID,"action":"R1_only_successor_repair","predecessor_members85_preserved":True,"review_members7_preserved":True,"one_postimage_changed":summary_rel,"old_value":"../REPLAY_RESULTS.json","new_value":"../../REPLAY_RESULTS.json","diagnostics_rerun":False},ensure_ascii=False)+"\n")
with (S/"RESEARCH_LOG.md").open("a") as f:
 f.write("\n- "+utc()+" (actual successor writer PID "+str(PID)+"): Corrected only R1 file-relative replay link in a new successor. Candidate/checker/full original receipts untouched, no rerun. Predecessor85 and review7 preserved; fresh successor review pending. Completion estimate:100% of bounded repair preparation; actual global/closure work pending.\n")
# Reauthenticate every sealed predecessor/review member after the repair.
authenticate(P,"85259c31a08a7c1fc389d22cc793d181ec446e4feeee542756cfe8cd8c6f8d72",85)
authenticate(R,"34a3fe5449c1538d5fdd82b3fad6544408f83ff0e68c01ffa2fe798c3a4297cd",7)
js(S/"R1_REPAIR_RECEIPT.json",{"actual_writer_pid":PID,"started_utc":START,"completed_utc":utc(),"metadata_checks_completed":CHECKS,"scope":"File identity/link resolution/one-field/diff consistency only, no mathematical diagnostics rerun","only_operative_postimage_change":summary_rel,"old_value":"../REPLAY_RESULTS.json","new_value":"../../REPLAY_RESULTS.json","resolved_target":str(target),"target_pin":pin(target),"repaired_summary":pin(summary),"new_candidate_hash_required":False,"candidate_unchanged":True,"checker_unchanged":True,"all_actual_run_receipts_unchanged":True,"receipt_members":receipts,"predecessor85_preserved":True,"review7_preserved":True,"new_consistency_adversary_pass_claimed":False})
oldresult=json.loads((P/"RESULT.json").read_text())
outcome=oldresult["scientific_outcome"]
result={**oldresult,"schema":"pr134-final-disposition-preparation-r1-successor/v1","actual_writer_pid":PID,"started_utc":START,"completed_utc":utc(),"completion_percent":100,"completion_scope":"Bounded R1-only successor preparation, no diagnostic rerun","corrected17_manifest":pin(S/"CORRECTED_17_MANIFEST.json"),"report":pin(S/"REPORT.md"),"predecessor_stage":str(P),"predecessor_result":pin(P/"RESULT.json"),"predecessor_seal":pin(P/"FINAL_MANIFEST.json"),"r1_fail_review_report":pin(R/"REPORT.md"),"r1_fail_review_result":pin(R/"RESULT.json"),"r1_fail_review_seal":pin(R/"FINAL_MANIFEST.json"),"repair_status":"R1_CORRECTED_SELF_CHECKED_AWAITING_NEW_ADVERSARY","changed_from_predecessor_stage":1,"changed_from_predecessor_paths":changed17,"actual_new_author_assertions_each":None,"new_author_or_independent_runs":False,"original_author_run_control_count_each_retained":50840,"original_independent_count_retained":28722,"all_original_actual_run_receipts_unchanged":True,"predecessor85_review7_unchanged":True,"r1_repair_receipt":pin(S/"R1_REPAIR_RECEIPT.json"),"new_successor_consistency_review":"PENDING_NEW_INDEPENDENT_ADVERSARY","scientific_outcome":outcome}
js(S/"RESULT.json",result)
allmembers=[{"path":str(p.relative_to(S)),**pin(p)} for p in sorted(S.rglob("*")) if p.is_file() and p!=S/"FINAL_MANIFEST.json"]
js(S/"FINAL_MANIFEST.json",{"schema":"pr134-final-disposition-postimages-r1-successor-seal/v1","actual_writer_pid":PID,"utc":utc(),"root":str(S),"status":"final-operative-disposition-postimages-preparation_only","self_excluded":True,"members":allmembers,"member_count":len(allmembers),"corrected17_manifest":pin(S/"CORRECTED_17_MANIFEST.json"),"predecessor85_seal":pin(P/"FINAL_MANIFEST.json"),"r1_fail_review7_seal":pin(R/"FINAL_MANIFEST.json"),"sole_operative17_change":summary_rel,"candidate_unchanged":True,"checker_and_all_actual_run_receipts_unchanged":True,"diagnostics_rerun":False,"new_successor_consistency_review":"PENDING_NEW_INDEPENDENT_ADVERSARY","scientific_outcome":outcome,"private_primary_bytes_copied":False,"excluded_from_current_core_checkpoint_plan":True})
for x in allmembers:ck(pin(S/x["path"])=={k:x[k] for k in ["bytes","sha256"]},"Final successor member drift")
print(json.dumps({"actual_pid":PID,"utc":utc(),"status":result["repair_status"],"operative17_changed_count":1,"candidate":pin(S/"corrected_attempt/CANDIDATE.md"),"summary":pin(summary),"replay_results":pin(target),"corrected17_manifest":pin(S/"CORRECTED_17_MANIFEST.json"),"report":pin(S/"REPORT.md"),"result":pin(S/"RESULT.json"),"manifest":pin(S/"FINAL_MANIFEST.json"),"members":len(allmembers),"new_diagnostic_runs":False,"predecessor85_and_review7_unchanged":True},indent=2))

