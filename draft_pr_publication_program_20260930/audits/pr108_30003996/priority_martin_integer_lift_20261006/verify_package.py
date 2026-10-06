import json, pathlib, hashlib; p=pathlib.Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr108_30003996/priority_martin_integer_lift_20261006"); errors=[]; m=json.loads((p/"SOURCE_MANIFEST.json").read_text()); scope=json.loads((p/"READ_SCOPE.json").read_text()); v=json.loads((p/"VERDICT.json").read_text()); files=list(p.glob("*.json")); [json.loads(f.read_text()) for f in files]; checks=0
for item in m["sources"]+scope["items"]:
    b=pathlib.Path(item["path"]).read_bytes(); checks+=1
    if ("bytes" in item and len(b)!=item["bytes"]) or hashlib.sha256(b).hexdigest()!=item["sha256"]: errors.append("pin mismatch "+item["path"])
for item in m["raw_material_manifest"]:
    b=(p/item["path"]).read_bytes(); checks+=1
    if item.get("snapshot_semantics"): b=b[:item["bytes"]]
    if len(b)!=item["bytes"] or hashlib.sha256(b).hexdigest()!=item["sha256"]: errors.append("private pin mismatch "+item["path"])
if hashlib.sha256((p.parent/"repaired_diagnostics_v1/PROOF.md").read_bytes()).hexdigest()!=v["candidate_proof_sha256"]: errors.append("candidate moved")
if (p/".gitignore").read_text().splitlines()[0]!="private/": errors.append("private exclusion missing")
receipts=json.loads((p/"SEARCH_RECEIPTS.json").read_text())
if len(receipts["calls"])!=18: errors.append("search receipt count")
if v["status_accounting"]["added_central_proof_turns"]!=0: errors.append("budget status")
if m["disk_bytes"]>350*1024*1024: errors.append("disk cap")
if errors: raise RuntimeError(errors)
print(json.dumps({"manifest_pin_checks":checks,"json_files_valid":len(files),"search_calls":18,"candidate_sha256":v["candidate_proof_sha256"],"disk_bytes":sum(q.stat().st_size for q in p.rglob("*") if q.is_file()),"errors":errors}))
(p/'PACKAGE_CHECK.json').write_text(json.dumps({'utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'manifest_pin_checks':checks,'valid_json_files':len(files),'search_calls':18,'candidate_pinned':True,'errors':errors},indent=2)+'\n')

