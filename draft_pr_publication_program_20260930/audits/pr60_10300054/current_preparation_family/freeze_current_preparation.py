"""MIT licensed. Local preparation index, not a ROOT custody helper.
Saved observations end before installation; no process-completion fiction.
"""
import ast,datetime,hashlib,json,os,pathlib,stat
from binding_checks import verify_bindings
root=pathlib.Path(__file__).resolve().parent
assert not (root/"SOURCE.json").exists(),"historical seal must not be replaced"
cap=root/"captures"/"index_build_observations"; cap.mkdir(exist_ok=False)
operator=pathlib.Path(__file__).read_bytes(); (cap/"executed_operator.py").write_bytes(operator)
dependency=(root/"binding_checks.py").read_bytes()
(cap/"binding_checks_preverification.py").write_bytes(dependency)
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
for p in root.glob("*.py"): ast.parse(p.read_bytes(),filename=str(p))
verify_bindings(root)
bindings=json.loads((root/"BINDINGS.json").read_bytes())
assert len(bindings["original_science"])==17
for e in bindings["original_science"]:
 p=pathlib.Path(e["path"]); raw=p.read_bytes()
 assert len(raw)==e["bytes"] and hashlib.sha256(raw).hexdigest()==e["sha256"]
 assert stat.S_IMODE(p.stat().st_mode)==0o444
adj=(root.parent/"ROOT_SCIENTIFIC_ADJUDICATION_20261003.json").read_bytes()
assert hashlib.sha256(adj).hexdigest()=="f3c4abd127129cb2488921b23f95afe504791f6908c713cfd7d04fda34b1a0d5"
r=json.loads((root/"READY.json").read_bytes())
assert r["ROOT_helpers_executed_by_preparer"] is False and r["current_packet_ROOT_custody_claimed"] is False
assert r["paper_prepared"] is False and r["ROOT_actual_scientific_adjudication_bound"] is True
r["prepared_by_pid"]=os.getpid(); r["prepared_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
(root/"READY.json").write_text(json.dumps(r,sort_keys=True,indent=2)+"\n")
event={"status":"PASS_PRE_INDEX_ORIGINAL_BINDINGS_AND_HELPER_SYNTAX",
 "pid":os.getpid(),"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "original_objects":17,"ROOT_current_helper_run":False,"paper_prepared":False}
stdout=(json.dumps(event,sort_keys=True)+"\n").encode()
(cap/"stdout.bin").write_bytes(stdout); (cap/"stderr.bin").write_bytes(b"")
receipt={"schema":"pr60-index-build-pre-index-observations/v1",
 "actual_execution":True,"pid":os.getpid(),"started_utc":started,
 "observations_finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "operator_sha256":hashlib.sha256(operator).hexdigest(),
 "binding_checks_preverification_sha256":hashlib.sha256(dependency).hexdigest(),
 "dependency_unchanged":(root/"binding_checks.py").read_bytes()==dependency,
 "operator_capture_timing":"read at process start, not an external persisted prelaunch snapshot",
 "stdout":{"bytes":len(stdout),"sha256":hashlib.sha256(stdout).hexdigest()},
 "stderr":{"bytes":0,"sha256":hashlib.sha256(b"").hexdigest()},
 "scope":"source-binding/syntax observations before final index installation",
 "process_completion_recorded":False,"ROOT_helper_run":False,"math_or_paper_certification":False}
(cap/"CAPTURE.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
print(stdout.decode(),end="",flush=True)
for p in root.rglob("*"):
 assert not p.is_symlink(),str(p)
 if p.is_dir(): os.chmod(p,0o755)
 elif p.is_file(): os.chmod(p,0o444); assert p.stat().st_nlink==1
 else: raise AssertionError(str(p))
os.chmod(root,0o755)
files=[]
for p in sorted(root.rglob("*")):
 if p.is_file():
  raw=p.read_bytes(); files.append({"path":p.relative_to(root).as_posix(),"bytes":len(raw),
  "sha256":hashlib.sha256(raw).hexdigest(),"full_mode_07777":format(stat.S_IMODE(p.stat().st_mode),"04o"),"nlink":1})
dirs=[{"path":".","full_mode_07777":"0755"}]+[
 {"path":p.relative_to(root).as_posix(),"full_mode_07777":"0755"} for p in sorted(root.rglob("*")) if p.is_dir()]
index={"schema":"pr60-operative-current-fixed-SOURCE/v1",
 "utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "self_indexed":False,"self_full_mode_07777":"0444","self_nlink":1,
 "ROOT_current_helpers_executed":False,"current_packet_ROOT_custody_claimed":False,
 "ROOT_scientific_adjudication_bound":True,"files":files,"directories":dirs}
with (root/"SOURCE.json").open("xb") as f:
 f.write((json.dumps(index,sort_keys=True,indent=2)+"\n").encode()); f.flush(); os.fsync(f.fileno())
os.chmod(root/"SOURCE.json",0o444)
# No output or mutation of indexed files follows installation.
