"""MIT licensed. Local index construction; not a ROOT custody helper.
The saved observation capture ends before final index installation. It does
not pretend to record process completion or certify scientific approval.
"""
import ast,datetime,hashlib,json,os,pathlib,stat
root=pathlib.Path(__file__).resolve().parent
assert not (root/"SOURCE.json").exists(),"do not overwrite a historical seal"
cap=root/"captures"/"index_build_observations"; cap.mkdir(exist_ok=False)
operator=pathlib.Path(__file__).read_bytes()
(cap/"executed_operator.py").write_bytes(operator)
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
messages=[]
for p in root.glob("*.py"): ast.parse(p.read_bytes(),filename=str(p))
bindings=json.loads((root/"BINDINGS.json").read_bytes())
for e in bindings["original_science"]:
 p=root/e["path"]; b=p.read_bytes()
 assert len(b)==e["bytes"] and hashlib.sha256(b).hexdigest()==e["sha256"]
 assert stat.S_IMODE(p.stat().st_mode)==int(e["full_mode_07777"],8)
assert len(bindings["original_science"])==17
r=json.loads((root/"READY.json").read_bytes())
assert r["ROOT_helpers_executed_by_preparer"] is False
assert r["full_target_resolved"] is False and r["new_mathematical_attempts"]==0
for p in sorted((root/"captures").rglob("CAPTURE.json")):
 rec=json.loads(p.read_bytes())
 for label in ["stdout","stderr"]:
  body=(p.parent/rec[label].get("path",label+".bin")).read_bytes()
  assert len(body)==rec[label]["bytes"] and hashlib.sha256(body).hexdigest()==rec[label]["sha256"]
messages.append({"status":"PASS_PRE_INDEX_SOURCE_BINDINGS_AND_HELPER_SYNTAX",
 "pid":os.getpid(),"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "original_objects":17,"ROOT_helper_run":False,"mathematical_approval":False})
stdout=("".join(json.dumps(m,sort_keys=True)+"\n" for m in messages)).encode()
(cap/"stdout.bin").write_bytes(stdout); (cap/"stderr.bin").write_bytes(b"")
receipt={"schema":"pr60-original-index-build-pre-index-observations/v1",
 "actual_execution":True,"pid":os.getpid(),"started_utc":started,
 "observations_finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "operator_sha256":hashlib.sha256(operator).hexdigest(),
 "operator_capture_timing":"read at process start; not an externally persisted prelaunch capture",
 "stdout":{"bytes":len(stdout),"sha256":hashlib.sha256(stdout).hexdigest()},
 "stderr":{"bytes":0,"sha256":hashlib.sha256(b"").hexdigest()},
 "scope":"Source bindings, all actual stream receipts and syntax checks before index installation",
 "process_completion_recorded":False,"ROOT_helper_run":False,
 "math_or_compiler_certification":False}
(cap/"CAPTURE.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
print(stdout.decode(),end="",flush=True)
for p in root.rglob("*"):
 assert not p.is_symlink(),str(p)
 if p.is_dir(): os.chmod(p,0o755)
 elif p.is_file(): os.chmod(p,0o444)
 else: raise AssertionError(str(p))
os.chmod(root,0o755)
files=[]
for p in sorted(root.rglob("*")):
 if p.is_file():
  b=p.read_bytes(); files.append({"path":p.relative_to(root).as_posix(),
  "bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),
  "full_mode_07777":format(stat.S_IMODE(p.stat().st_mode),"04o")})
dirs=[{"path":".","full_mode_07777":"0755"}]+[
 {"path":p.relative_to(root).as_posix(),"full_mode_07777":"0755"}
 for p in sorted(root.rglob("*")) if p.is_dir()]
index={"schema":"pr60-original-preparation-fixed-source/v1",
 "utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "self_indexed":False,"self_full_mode_07777":"0444",
 "ROOT_helpers_executed":False,"ROOT_custody_claimed":False,
 "files":files,"directories":dirs}
with (root/"SOURCE.json").open("xb") as f:
 f.write((json.dumps(index,sort_keys=True,indent=2)+"\n").encode()); f.flush(); os.fsync(f.fileno())
os.chmod(root/"SOURCE.json",0o444)
# No output or indexed-file mutation follows installation.

