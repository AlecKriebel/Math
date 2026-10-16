from pathlib import Path
import datetime,hashlib,json
here=Path("draft_pr_actual_claims_1000_1100_20261012/audits/pr1064_30001073/finalization/terminal_admin_20261014").resolve()
audit=here.parent.parent
package=audit/"preprint_v1_0"
def require(c,m):
 if not c:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def match(p,r):
 return p.is_file() and not p.is_symlink() and p.stat().st_size==r["bytes"] and hashlib.sha256(p.read_bytes()).hexdigest()==r["sha256"]
def rec(p,root):
 b=p.read_bytes();return {"path":p.relative_to(root).as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
inventory=load(here/"CHANGE_INVENTORY.json")
allowed={r["path"]:r for r in inventory["modified"]}
baseline=load(here/"INPUT_PINS.json")["records"]
initial=load(here/"INPUT_PINS_INITIAL_BOUNDARY.json")["records"]
require((len(allowed),len(baseline),len(initial))==(9,494,422),"unexpected preserved boundary")
by_path={r["path"]:r for r in baseline};changed=[]
whole=load(audit/"reviews/package_03/INPUT_CUSTODY.json")["files"]
require(len(whole)==467 and all(by_path[r["path"]]==r for r in whole),"whole03 input boundary not retained")
for r in baseline:
 p=audit/r["path"]
 if match(p,r):
  require(r["path"] not in allowed,"authorized change unexpectedly absent");continue
 require(r["path"] in allowed,"unauthorized change "+r["path"])
 row=allowed[r["path"]]
 require(r==row["before"] and match(audit/row["preserved_path"],r),"immediate before differs "+r["path"])
 require(match(p,row["after"]),"current after differs "+r["path"]);changed.append(r["path"])
require(set(changed)==set(allowed),"changed set differs")
for r in initial:require(by_path.get(r["path"])==r,"initial expanded boundary rebind")
before=load(here/"BEFORE_PINS.json")["entries"]
for r in before:require(match(here/r["preserved_path"],r),"before mismatch")
current=load(here/"FINAL_CURRENT_PINS.json")["records"]
require(len(current)==204,"current count differs")
for r in current:require(match(package/r["path"],r),"current package mismatch "+r["path"])
actual={p.relative_to(package).as_posix() for p in package.rglob("*") if p.is_file() and not {"tmp","__pycache__"}.intersection(p.relative_to(package).parts)}
require(actual=={r["path"] for r in current},"current package set differs")
stages=load(here/"PRIOR_STAGE_RECEIPTS.json")["stages"];resolutions=0
for stage in stages:
 if "records" in stage:
  require(len(stage["records"])==stage["count"],"stage count differs")
  for r in stage["records"]:
   require(match(audit/r["resolved_path"],r),"historical resolution differs "+r["resolved_path"]);resolutions+=1
 else:
  seal=audit/stage["stage"];rows=load(seal)["entries"]
  require(len(rows)==stage["count"],"historical output count differs")
  for r in rows:require(match(seal.parent/r["path"],r),"historical output differs");resolutions+=1
copies=load(package/"COPY_MAP.json")["copies"]
old=load(here/"before/preprint_v1_0/COPY_MAP.json")["copies"]
require(len(copies)==163 and copies[:122]==old,"old122 maps changed")
require(load(package/"SAFE_INPUT_PINS.json")["records"]==copies,"SAFE map differs")
for r in copies:require(match(audit/r["source_path"],r) and match(package/r["package_path"],r),"copy/source differs "+r["source_path"])
selections=load(package/"TERMINAL_SELECTION_LEDGER.json")["records"]
require(len(selections)==70 and sum(r["included"] for r in selections)==41,"selection count differs")
included={r["source_path"] for r in copies[122:]}
for r in selections:
 require(match(audit/r["source_path"],r),"selection source differs")
 require((r["source_path"] in included)==r["included"],"selection decision differs")
 require(isinstance(r["reason"],str) and r["reason"],"selection lacks reason")
protected=load(here/"PROTECTED_BYTE_RECEIPT.json")["explicit_protected"]
require(len(protected)==20,"protected count differs")
for r in protected:require(match(audit/r["path"],r),"protected semantic file differs")
metadata=load(package/"metadata.json")
require(all(load(package/n)["metadata"]==metadata for n in ["publication/zenodo.json","publication/release_metadata.json","publication/zenodo-deposit.json"]),"metadata differs")
additions=inventory["added_package_files"];require(len(additions)==46,"addition count differs")
for r in additions:require(match(audit/r["path"],r),"added file differs")
commands=[json.loads(s) for s in (here/"EXECUTIONS.jsonl").read_text().splitlines()]
require(len(commands)==481 and all((r["returncode"]==0)==r["expected_success"] for r in commands),"original commands differ")
result={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"pass":True,"resumption_scope":"Existing terminal candidate; no candidate edits or new whole review.","initial_boundary":len(initial),"immediate_boundary":len(baseline),"authorized_changes":changed,"unchanged_boundary_records":len(baseline)-len(changed),"exact_before_files":len(before),"current_package_files":len(current),"historical_stages":len(stages),"historical_record_resolutions":resolutions,"old_copy_map_records_unchanged":len(old),"current_source_equal_copies":len(copies),"terminal_selection_records":len(selections),"new_copies":len(included),"individual_omissions":sum(not r["included"] for r in selections),"protected_semantic_records":len(protected),"metadata_objects_equal":True,"original_command_receipts_consistent":len(commands),"paper_pdf":rec(package/"paper.pdf",package),"support_zip":rec(package/"support.zip",package)}
print(json.dumps(result,indent=2))
