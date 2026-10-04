"""PR61 administrative checks only. Does not import or execute mathematical checkers."""
import ast,hashlib,json,pathlib,re,stat
ROOT=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
auth=json.loads((ROOT/"ORIGINAL_AUTHENTICATION.json").read_bytes())
assert auth["head"]=="b5a4829365f2a0bd5f42b7653c5cfacfa6b01d85"
assert auth["scientific_file_count"]==10
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
assert len(parts)==11
science=[]
for part in parts:
 lines=part.splitlines(keepends=True)
 path=lines[0].decode().strip().split(" b/",1)[1]
 if path=="unsolved_math_prioritization/QUEUE.md":
  old=[x for x in lines if x.startswith(b"-| 81 |")]
  new=[x for x in lines if x.startswith(b"+| 81 |")]
  assert len(old)==len(new)==1 and b"queued | 0/5" in old[0] and b"already_solved | 0/5" in new[0]
  q=json.loads((ROOT/"PR_QUEUE_SELECTED.json").read_bytes())
  assert new[0][1:].decode().rstrip("\n")==q["selected_new_patch_lines"][0]["text"]
  continue
 prefix="unsolved_math_prioritization/attempts/2725/"
 assert path.startswith(prefix) and b"new file mode 100644\n" in lines
 hunk=next(i for i,x in enumerate(lines) if x.startswith(b"@@"))
 body=b"".join(x[1:] for x in lines[hunk+1:] if x.startswith(b"+"))
 assert body==(ROOT/"original"/path[len(prefix):]).read_bytes(),path
 science.append(path)
assert len(science)==10
for p in ROOT.rglob("*.py"):ast.parse(p.read_bytes(),filename=str(p))
original=ROOT/"original"
proofsha=sha((original/"KNOWN_RESULT.md").read_bytes())
manifest=json.loads((original/"source_manifest.json").read_bytes())
summary=json.loads((original/"independent_review"/"review_summary.json").read_bytes())
receipt=json.loads((original/"independent_review"/"source_verification.json").read_bytes())
assert proofsha==summary["artifact_sha256"]==receipt["artifact_sha256"]
assert sha((original/"source_record.json").read_bytes())==manifest["source_record_sha256"]
assert sha((original/"independent_review"/"REVIEW.md").read_bytes())==summary["report_sha256"]
assert summary["substantive_attempts"]==0 and summary["recommended_status"]=="already_solved"
for line in (original/"SHA256SUMS").read_text().splitlines():
 digest,name=line.split(None,1);name=name.strip()
 assert pathlib.PurePosixPath(name).name==name
 assert sha((original/name).read_bytes())==digest
assert not list(original.rglob("*.py")), "no executable mathematical checker in original domain"
prior=(ROOT/"RAW_PRIOR_SQL_TEXT.txt").read_bytes()
assert prior==b"{}" and sha(prior)=="44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
assert json.loads((ROOT/"SELECTED_RAW_PRIOR.json").read_bytes()) is None
accounting=json.loads((ROOT/"SOURCE_ACCOUNTING.json").read_bytes())
assert accounting["prior_report"]["key_present"] is False and accounting["prior_report"]["upstream_flat_report_field_present"] is False
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
assert ready["ROOT_helpers_executed_by_preparer"] is False and ready["novelty_or_new_discovery_credit"]==0
with (ROOT/"BINDINGS.json").open("x") as f:
 json.dump({"schema":"pr60-original-science-bindings/v1","original_science":binding,"external_source_receipts":"SOURCE_ACCOUNTING.json; private inputs excluded and not required by ROOT custody helpers","ROOT_custody_claimed":False},f,sort_keys=True,indent=2);f.write("\n")
with (ROOT/"ADMINISTRATIVE_CONTROL_RESULT.json").open("x") as f:
 json.dump({"schema":"pr61-source-administrative-control/v1","status":"PASS_SOURCE_DIFF_RECEIPT_CONSISTENCY_ONLY","scientific_files":10,"diff_files":11,"complete_internal_command_caps_validated":caps,"current_outer_cap_included":False,"author_checker_imported_or_run":False,"new_mathematical_proof_or_review":False,"ROOT_helper_run":False},f,sort_keys=True,indent=2);f.write("\n")
print(json.dumps({"status":"PASS_SOURCE_DIFF_RECEIPT_CONSISTENCY_ONLY","scientific_files":10,"diff_files":11,"existing_actual_caps":len(caps),"historical_receipts_are_not_fresh_replays":True,"math_credit":0,"ROOT_helper_run":False},sort_keys=True))


