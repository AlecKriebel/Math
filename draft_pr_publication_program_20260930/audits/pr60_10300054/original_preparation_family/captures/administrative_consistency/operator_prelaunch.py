"""PR60 administrative checks only. Does not import or execute mathematical checkers."""
import ast,hashlib,json,pathlib,re,stat
ROOT=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
auth=json.loads((ROOT/"ORIGINAL_AUTHENTICATION.json").read_bytes())
assert auth["head"]=="1e762651b698c1fb519901bd924c5bd3717cc5ef"
assert auth["scientific_file_count"]==17
binding=[]
for e in auth["scientific_files"]:
 p=ROOT/e["local_path"];b=p.read_bytes()
 assert len(b)==e["bytes"] and sha(b)==e["sha256"]
 assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==e["git_blob_sha1"]
 assert stat.S_IMODE(p.stat().st_mode)==0o444
 binding.append({"path":e["local_path"],"bytes":len(b),"sha256":sha(b),"full_mode_07777":"0444","git_blob_sha1":e["git_blob_sha1"],"git_mode":"100644"})
diff=(ROOT/"FULL_PR_DIFF.patch").read_bytes()
parts=re.split(br"(?=^diff --git )",diff,flags=re.M)
parts=[p for p in parts if p]
assert len(parts)==18
science=[]
for part in parts:
 lines=part.splitlines(keepends=True)
 path=lines[0].decode().strip().split(" b/",1)[1]
 if path=="unsolved_math_prioritization/QUEUE.md":
  old=[x for x in lines if x.startswith(b"-| 76 |")]
  new=[x for x in lines if x.startswith(b"+| 76 |")]
  assert len(old)==len(new)==1 and b"queued | 0/5" in old[0] and b"unsolved | 1/5" in new[0]
  q=json.loads((ROOT/"PR_QUEUE_SELECTED.json").read_bytes())
  assert new[0][1:].decode().rstrip("\n")==q["selected_lines"][0]["text"]
  continue
 prefix="unsolved_math_prioritization/attempts/10300054/"
 assert path.startswith(prefix) and b"new file mode 100644\n" in lines
 hunk=next(i for i,x in enumerate(lines) if x.startswith(b"@@"))
 body=b"".join(x[1:] for x in lines[hunk+1:] if x.startswith(b"+"))
 assert body==(ROOT/"original"/path[len(prefix):]).read_bytes(),path
 science.append(path)
assert len(science)==17
for p in ROOT.rglob("*.py"):ast.parse(p.read_bytes(),filename=str(p))
original=ROOT/"original"
proofsha=sha((original/"OBSTRUCTION.md").read_bytes())
ver=json.loads((original/"verification.json").read_bytes())
prov=json.loads((original/"provenance.json").read_bytes())
summary=json.loads((original/"independent_review"/"review_summary.json").read_bytes())
assert proofsha==ver["artifact_sha256"]==prov["artifact_sha256"]==summary["artifact_sha256"]
assert sha((original/"verify.py").read_bytes())==summary["submitted_verifier_sha256"]
assert sha((original/"independent_review"/"REVIEW.md").read_bytes())==summary["report_sha256"]
assert ver["assertions"]==61 and summary["independent_exact_assertions"]==209
turns=json.loads((original/"turns.json").read_bytes())
assert turns["substantive_proof_attempts"]==1 and turns["budget"]==5 and turns["turns"][0]["outcome"]=="unsolved"
prior=(ROOT/"RAW_PRIOR_SQL_TEXT.txt").read_bytes()
assert len(prior)==988 and sha(prior)=="8c2af2f7b8875c20b01084f20ad9315d65aac38588f9ddff36943868c802b2c4"
assert json.loads(prior)==json.loads((ROOT/"SELECTED_RAW_PRIOR.json").read_bytes())
caps=[]
for p in sorted((ROOT/"captures").rglob("CAPTURE.json")):
 obj=json.loads(p.read_bytes())
 for name in ["stdout","stderr"]:
  stream=p.parent/obj[name].get("path",name+".bin");b=stream.read_bytes()
  assert len(b)==obj[name]["bytes"] and sha(b)==obj[name]["sha256"],str(p)
 assert obj["actual_execution"] is True and isinstance(obj["pid"],int)
 caps.append({"path":p.relative_to(ROOT).as_posix(),"pid":obj["pid"],"exit_code":obj["exit_code"]})
# This operator's outer CAPTURE is written after completion and is not in caps yet.
ready=json.loads((ROOT/"READY.json").read_bytes())
assert ready["ROOT_helpers_executed_by_preparer"] is False and ready["full_target_resolved"] is False
with (ROOT/"BINDINGS.json").open("x") as f:
 json.dump({"schema":"pr60-original-science-bindings/v1","original_science":binding,"external_source_receipts":"SOURCE_ACCOUNTING.json; private inputs excluded and not required by ROOT custody helpers","ROOT_custody_claimed":False},f,sort_keys=True,indent=2);f.write("\n")
with (ROOT/"ADMINISTRATIVE_CONTROL_RESULT.json").open("x") as f:
 json.dump({"schema":"pr60-source-administrative-control/v1","status":"PASS_SOURCE_DIFF_RECEIPT_CONSISTENCY_ONLY","scientific_files":17,"diff_files":18,"complete_internal_command_caps_validated":caps,"current_outer_cap_included":False,"author_checker_imported_or_run":False,"new_mathematical_proof_or_review":False,"ROOT_helper_run":False},f,sort_keys=True,indent=2);f.write("\n")
print(json.dumps({"status":"PASS_SOURCE_DIFF_RECEIPT_CONSISTENCY_ONLY","scientific_files":17,"diff_files":18,"existing_actual_caps":len(caps),"historical_receipts_are_not_fresh_replays":True,"math_credit":0,"ROOT_helper_run":False},sort_keys=True))

