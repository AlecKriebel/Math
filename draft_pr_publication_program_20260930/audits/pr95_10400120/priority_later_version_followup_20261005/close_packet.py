from pathlib import Path
import json, hashlib, datetime, os, sys
P=Path(__file__).resolve().parent
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(f): return hashlib.sha256(f.read_bytes()).hexdigest()
def pin(f): return {"path":str(f.relative_to(P)),"bytes":f.stat().st_size,"sha256":sha(f)}
start=now()
checks=[]
for f in sorted((P/"processes").glob("retrieval_*.json")):
    r=json.loads(f.read_text()); b=(P/r["path"]).read_bytes()
    checks.append({"record":str(f.relative_to(P)),"check":"actual_response_byte_pin", "pass": len(b)==r["bytes"] and hashlib.sha256(b).hexdigest()==r["sha256"]})
    checks.append({"record":str(f.relative_to(P)),"check":"actual_pdf_classification", "pass":b.startswith(b"%PDF-")==r["PDF"]})
for f in sorted((P/"processes").glob("extract_*.json")):
    r=json.loads(f.read_text())
    checks.append({"record":str(f.relative_to(P)),"check":"source_execution_pin", "pass":sha(Path(r["argv"][2]))==r["source_sha256"] and sha(P/"retrieve_extract.py")==r["script_sha256"]})
    checks.append({"record":str(f.relative_to(P)),"check":"actual_extraction_exit_and_bytes", "pass":r["exit"]==0 and sha(Path(r["argv"][3]))==r["extraction_sha256"]})
for s in json.loads((P/"SOURCE_LEDGER.json").read_text())["sources"]:
    for r in s.get("files",[]):
        f=P/r["path"];checks.append({"record":s["id"],"check":"source_ledger_file_pin", "pass":f.stat().st_size==r["bytes"] and sha(f)==r["sha256"]})
for name in ["INPUT_MANIFEST.json","VERSION_COMPARISON_INPUTS.json"]:
    for r in json.loads((P/name).read_text())["inputs"]:
        f=Path(r["path"]);checks.append({"record":name,"path":str(f),"check":"external_input_stable", "pass":f.stat().st_size==r["bytes"] and sha(f)==r["sha256"]})
for r in json.loads((P/"adversarial_review/artifact_manifest.json").read_text())["files"]:
    f=P/"adversarial_review"/r["path_relative_to_adversarial_review"]
    checks.append({"record":"adversarial_review/artifact_manifest.json","path":r["path_relative_to_adversarial_review"],"check":"independent_adversary_closed_pin", "pass":f.stat().st_size==r["size_bytes"] and sha(f)==r["sha256"]})
if not all(c["pass"] for c in checks):
    (P/"INTEGRITY_CHECK.json").write_text(json.dumps({"UTC":now(),"operator_PID":os.getpid(),"checks":checks,"pass":False},indent=2)+"\n")
    raise SystemExit("Integrity check failed; no closure written")
(P/"INTEGRITY_CHECK.json").write_text(json.dumps({"UTC":now(),"operator_PID":os.getpid(),"checks":checks,"pass":True,"scope":"Custody/classification/process/source pins only. No new central mathematical computation."},indent=2)+"\n")
with (P/"RESEARCH_LOG.md").open("a") as f:
    f.write("- "+now()+" — Checkpoint 4 (100% bounded-audit completion): independent adversarial receipt integrated, report and source ledgers closed; actual response/extraction/input byte pins all verified. No earlier qualifying source example authenticated. Novelty/publication clearance remains false; direct Kuriya gap remains. Zero new central proof-search turns.\n")
(P/"processes/closure_integrity.json").write_text(json.dumps({"UTC_start":start,"UTC_finish":now(),"operator_PID":os.getpid(),"argv":sys.argv,"executed_script_sha256":sha(Path(__file__)),"checks_passed":len(checks),"exit":0,"result":"source/process/input pins all stable before closing manifest; output summary returned by actual tool transcript"},indent=2)+"\n")
excluded={"CLOSED_MANIFEST.json","CLOSURE.json"}
rows=[pin(f) for f in sorted(P.rglob("*")) if f.is_file() and str(f.relative_to(P)) not in excluded]
(P/"CLOSED_MANIFEST.json").write_text(json.dumps({"UTC":now(),"operator_PID":os.getpid(),"excluded":sorted(excluded),"files":rows},indent=2)+"\n")
bad=[]
for r in rows:
    f=P/r["path"]
    if f.stat().st_size!=r["bytes"] or sha(f)!=r["sha256"]:bad.append(r["path"])
if bad: raise SystemExit("Fresh closed-manifest verification failed: "+repr(bad))
c={"UTC":now(),"operator_PID":os.getpid(),"bounded_audit_complete":True,"bounded_audit_completion_percent":100,"original_author_effort":"2/5","new_central_proof_search_turns":0,"target_pair_recomputed":False,"new_source_pdfs":3,"earlier_qualifying_example_authenticated":False,"priority_clearance":False,"publication_clearance":False,"worldwide_novelty_established":False,"direct_priority_gap":"Kuriya2003 full text remains inaccessible/outside this bounded later-version task; Gang2019/HT2004 final text remain unread","report":pin(P/"REPORT.md"),"manifest":pin(P/"CLOSED_MANIFEST.json"),"manifest_members":len(rows),"fresh_manifest_verification_mismatches":bad,"integrity_checks":len(checks),"no_outreach_or_git_pr_service_ui_mutations":True}
(P/"CLOSURE.json").write_text(json.dumps(c,indent=2)+"\n")
print(json.dumps(c,indent=2))
