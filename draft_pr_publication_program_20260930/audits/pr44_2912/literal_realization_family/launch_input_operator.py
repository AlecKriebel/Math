#!/usr/bin/env python3
"""Reviewer authored operator launcher with a sealed prelaunch input closure."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time,datetime
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
operator=ROOT/"audit_input_operator.py"
inputs=[AUDIT/"snapshot_manifest_v2.json",AUDIT/"original_diff_v2.patch"]
manifest=json.loads(inputs[0].read_text())
inputs.extend(AUDIT/"source_snapshot_v2"/f["path"] for f in manifest["files"])
def bind(path):
    raw=path.read_bytes()
    return {"path":str(path),"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw)}
closure={"schema":"self_only_reviewer_operator_closure/v1","prelaunch_utc":stamp(),"launcher_pid":os.getpid(),"operator":bind(operator),"launcher":bind(Path(__file__).resolve()),"explicit_foreign_inputs":[bind(p) for p in inputs],"foreign_input_authorship":"excluded","foreign_helpers_executed":False,"scientific_execution":False,"new_substantive_attempts":0,"audit_attempts":0,"argv":[sys.executable,str(operator)],"cwd":str(ROOT),"runtime":sys.version,"execution_scope":"reviewer-owned closure operator and standard-library only; foreign files treated as bytes/text"}
p=ROOT/"INPUT_OPERATOR_PRELAUNCH.json";p.write_text(json.dumps(closure,indent=2)+"\n");p.chmod(0o444)
start=stamp();before=time.monotonic()
proc=subprocess.Popen([sys.executable,str(operator)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdout,stderr=proc.communicate(timeout=40)
for name,data in (("input_operator.stdout",stdout),("input_operator.stderr",stderr)):
    p=ROOT/name;p.write_bytes(data);p.chmod(0o444)
record={"schema":"reviewer_operator_run/v1","launcher_pid":os.getpid(),"child_pid":proc.pid,"started_utc":start,"finished_utc":stamp(),"elapsed_monotonic_seconds":time.monotonic()-before,"exit_code":proc.returncode,"prelaunch_sha256":hashlib.sha256((ROOT/"INPUT_OPERATOR_PRELAUNCH.json").read_bytes()).hexdigest(),"operator_source_sha256":hashlib.sha256(operator.read_bytes()).hexdigest(),"stdout":bind(ROOT/"input_operator.stdout"),"stderr":bind(ROOT/"input_operator.stderr"),"new_substantive_attempts":0,"audit_attempts":0,"scientific_assertion_count":0,"candidate_helper_execution":False,"historical_helper_execution":False}
p=ROOT/"INPUT_OPERATOR_RUN.json";p.write_text(json.dumps(record,indent=2)+"\n");p.chmod(0o444)
print(json.dumps(record,indent=2))
if proc.returncode:sys.exit(proc.returncode)
