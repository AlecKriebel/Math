from pathlib import Path
import hashlib,json,datetime
base=Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
checks=[]
for path in sorted((base/"receipts").glob("*.json")):
    r=json.loads(path.read_text())
    assert isinstance(r["pid"],int) and r["pid"]>0
    assert isinstance(r["argv"],list) and r["argv"]
    assert r["exit_code"]==0, (path,r["exit_code"])
    for name in ["stdout","stderr"]:
        s=r[name]; data=Path(s["private_path"]).read_bytes()
        assert len(data)==s["bytes"] and hashlib.sha256(data).hexdigest()==s["sha256"],(path,name)
    checks.append({"receipt":str(path.relative_to(base)),"pid":r["pid"],"exit_code":r["exit_code"],"both_stream_hashes_verified":True})
first=json.loads((base/"FIRST_CONCLUSION.json").read_text())
assert hashlib.sha256((base/"FIRST_CONCLUSION.md").read_bytes()).hexdigest()==first["markdown_sha256"]
root=base.parent/"attributed_prior_result_preparation_20261004"
root_manifest=json.loads((root/"MANIFEST.json").read_text())
root_checks=[]
for row in root_manifest["files"]:
    data=(root/row["path"]).read_bytes()
    ok=len(data)==row["bytes"] and hashlib.sha256(data).hexdigest()==row["sha256"]
    root_checks.append({**row,"pin_matches_at_final_check":ok})
    assert ok,row["path"]
result={"utc":now,"receipt_count_checked":len(checks),"receipts":checks,"first_conclusion_hash_still_matches":True,"reviewed_root_packet_pins":root_checks,"scope":"integrity/source-custody checks; no candidate diagnostics rerun and no universal proof inferred from computation"}
(base/"INTEGRITY_CHECKS.json").write_text(json.dumps(result,indent=2)+"\n")
files=[]
for path in sorted(base.rglob("*")):
    if not path.is_file() or path.name=="MANIFEST.json" or path.name=="manifest_finalize.json":continue
    data=path.read_bytes()
    files.append({"path":str(path.relative_to(base)),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
manifest={"schema":"pr65-independent-final-adversary-manifest/v1","utc":now,"files":files,"excluded_bookkeeping":["MANIFEST.json itself","receipts/manifest_finalize.json is produced after this snapshot; kept separately"],"full_primary_bodies_and_renderings_external_private":True,"completion_percent":100,"original_proof_search_turns_added":0}
(base/"MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps({"utc":now,"manifested_files":len(files),"instrumented_receipts_checked":len(checks),"both_stream_hashes_verified":True,"root_packet_pins_match":True,"completion_percent":100}))
