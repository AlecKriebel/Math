"""MIT licensed. Source/evidence consistency only, not a mathematical proof."""
import ast,hashlib,json,pathlib,stat
root=pathlib.Path(__file__).resolve().parent
st=json.loads((root/"STATUS.json").read_bytes())
b=json.loads((root/"BINDINGS.json").read_bytes())
ev=json.loads((root/"ROOT_EVIDENCE.json").read_bytes())
assert st["operative_disposition"]=="already_solved"
assert st["substantive_proof_attempts"]==0 and st["budget"]==5
assert st["audit_editorial_increment"]==st["new_contribution_credit"]==0
assert st["paper_prepared"] is False and st["native_Git_PR_acceptance_mutation"] is False
assert st["ROOT_current_helpers_executed_by_preparer"] is False
assert st["ROOT_current_scientific_approval_claimed"] is True
assert b["head"]==st["original_head"]=="465d771ec1ddc91877e8d9db51ed59aea1b0d97d"
assert len(b["original_science"])==17
for e in b["original_science"]+b["audited_in_place"]+b["ROOT_actual_capture_files"]:
 p=pathlib.Path(e["path"]); raw=p.read_bytes()
 assert len(raw)==e["bytes"] and hashlib.sha256(raw).hexdigest()==e["sha256"],e["path"]
for e in b["original_science"]:
 assert stat.S_IMODE(pathlib.Path(e["path"]).stat().st_mode)==0o444
adj=pathlib.Path(root.parent/"ROOT_SCIENTIFIC_ADJUDICATION_20261003.json")
raw=adj.read_bytes()
assert hashlib.sha256(raw).hexdigest()==st["ROOT_scientific_adjudication_sha256"]
a=json.loads(raw)
assert a["disposition"]=="already_solved" and a["original_budget"]=="0/5"
assert a["audit_increment"]==0 and a["native_acceptance_completed"] is False
acc=ev["typed_prior_accounting"]
assert acc["raw_report_key_present"] is False and acc["SQL_report_is_NULL"] is False
assert acc["SQL_report_literal"]=="{}" and acc["wrapper_field_present"] is True
assert acc["wrapper_field_value"] is None and acc["original_turn_log_entries"]==0
assert len(ev["actual_custody_captures"])==6
for e in ev["actual_custody_captures"]:
 p=pathlib.Path(e["capture_path"]); c=json.loads(p.read_bytes())
 assert c["actual_execution"] is True and c["exit_code"]==0 and c["pid"]==e["pid"]
 for stream in ("stdout","stderr"):
  raw=(p.parent/c[stream]["path"]).read_bytes()
  assert len(raw)==c[stream]["bytes"] and hashlib.sha256(raw).hexdigest()==c[stream]["sha256"]
for p in root.glob("ROOT_*.py"): ast.parse(p.read_bytes(),filename=str(p))
assert not any(p.suffix in (".pdf",".png",".jpg") or p.name.endswith(".layout.txt") for p in root.rglob("*") if p.is_file())
print(json.dumps({"status":"PASS_OPERATIVE_PREPARATION_CONSISTENCY_ONLY",
 "original17_unchanged":True,"actual_ROOT_capture_pairs":3,
 "scientific_adjudication_bound":True,"ROOT_current_helpers_executed":False,
 "native_mutation":False,"new_math_or_review_credit":0,"paper_prepared":False},sort_keys=True))
