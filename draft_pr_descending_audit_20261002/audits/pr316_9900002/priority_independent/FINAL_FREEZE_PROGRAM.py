from pathlib import Path
import hashlib, json, datetime, stat, os

base = Path(__file__).resolve().parent
expected_first = {
    "SOURCE_ONLY_FIRST.md": "e9b3ceb53a44b9177ce4744e37a218011c3580fbdea9fbad08d917541026f537",
    "SOURCE_ONLY_FIRST_SHA256.txt": "776a00b7f75a506f628fafa5e2f2b26c58fc9747a43a2c184742b29ca2c79a20",
}
special = {"FREEZE_RECEIPT.json", "FINAL_VERIFY_RESULT.json", "FINAL_SHA256.json"}
def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def mode(path):
    return format(stat.S_IMODE(path.stat().st_mode), "03o")

started = utc()
for name, digest in expected_first.items():
    assert sha(base/name) == digest, f"Early frozen bytes changed: {name}"
early_checks = []
for line in (base/"SOURCE_ONLY_FIRST_SHA256.txt").read_text().splitlines():
    digest, filename = line.split(None, 1)
    path = Path(filename.strip())
    assert path.is_relative_to(base), "Early manifest escaped assigned folder"
    actual = sha(path)
    assert actual == digest, f"Early pin changed: {path}"
    early_checks.append({"path":str(path),"sha256":actual,"ok":True})
assert len(early_checks) == 24, f"Unexpected initial pin count: {len(early_checks)}"
with (base/"RESEARCH_LOG.md").open("a") as out:
    out.write("\n- "+utc()+"; completion100% of bounded priority audit: all24 first-stage pins plus original report/manifest hashes reverified. Final report and proof reread; actual local permission freeze now starts. Receipt records every previous/new mode, and final manifest pins all substantive artifacts. No first-priority certificate, Git mutation, outside contact, or publication.\n")
files = sorted(p for p in base.rglob("*") if p.is_file() and p.name not in special)
assert not any(p.is_symlink() for p in files), "Refusing unexpected evidence symlink"
before = [{"path":str(p),"bytes":p.stat().st_size,"sha256":sha(p),"previous_mode":mode(p)} for p in files]
transitions = []
for record in before:
    path = Path(record["path"])
    path.chmod(0o444)
    record["new_mode"] = mode(path)
    assert record["new_mode"] == "444"
    assert sha(path) == record["sha256"], f"Freeze changed content: {path}"
    transitions.append(record)
receipt = {
    "started_utc":started,
    "substantive_freeze_completed_utc":utc(),
    "scope_absolute_path":str(base),
    "meaning":"Local content/permissions evidence freeze, not publication",
    "first_stage_report_and_manifest_unchanged":expected_first,
    "all24_first_stage_pins_verified":early_checks,
    "permission_transitions":transitions,
    "explicit_644_to_444_count":sum(r["previous_mode"]=="644" for r in transitions),
    "already_444_count":sum(r["previous_mode"]=="444" for r in transitions),
    "receipt_and_final_manifest_modes":"Written within this operation and then444; not previously frozen content",
}
receipt_path = base/"FREEZE_RECEIPT.json"
receipt_path.write_text(json.dumps(receipt,indent=2)+"\n")
receipt_path.chmod(0o444)
verify = {
    "utc":utc(),
    "existing_artifact_count":len(files),
    "all_existing_content_hashes_match_pre_freeze":all(sha(Path(r["path"]))==r["sha256"] for r in before),
    "all_existing_files_mode444":all(mode(Path(r["path"]))=="444" for r in before),
    "all24_first_stage_pins_unchanged":all(sha(Path(r["path"]))==r["sha256"] for r in early_checks),
    "early_manifest_hash_unchanged":sha(base/"SOURCE_ONLY_FIRST_SHA256.txt")==expected_first["SOURCE_ONLY_FIRST_SHA256.txt"],
    "fresh_adversary_report_hash":sha(base/"slow_tail_adversary/report.md"),
}
assert all(verify[k] for k in ("all_existing_content_hashes_match_pre_freeze","all_existing_files_mode444","all24_first_stage_pins_unchanged","early_manifest_hash_unchanged"))
verify_path = base/"FINAL_VERIFY_RESULT.json"
verify_path.write_text(json.dumps(verify,indent=2)+"\n")
verify_path.chmod(0o444)
manifest_entries = [{"path":str(p),"bytes":p.stat().st_size,"sha256":sha(p),"mode":mode(p)}
                    for p in sorted(base.rglob("*")) if p.is_file() and p.name!="FINAL_SHA256.json"]
manifest_path = base/"FINAL_SHA256.json"
manifest_path.write_text(json.dumps({"utc":utc(),"excluded_self":str(manifest_path),"files":manifest_entries},indent=2)+"\n")
manifest_path.chmod(0o444)
for item in json.loads(manifest_path.read_text())["files"]:
    path=Path(item["path"])
    assert sha(path)==item["sha256"] and mode(path)==item["mode"]=="444"
print(json.dumps({
    "completed_utc":utc(),
    "manifest_entry_count":len(manifest_entries),
    "permission_change_count":receipt["explicit_644_to_444_count"],
    "all_first_stage_bytes_unchanged":True,
    "all_manifest_hashes_and_modes_verified":True,
    "named_sha256":{name:sha(base/name) for name in (
        "FINAL_PRIORITY_REPORT.md","SLOW_VARIATION_COROLLARY.md","FINAL_SHA256.json",
        "FREEZE_RECEIPT.json","FINAL_VERIFY_RESULT.json","SOURCE_ONLY_FIRST.md",
        "SOURCE_ONLY_FIRST_SHA256.txt")}
},indent=2))

