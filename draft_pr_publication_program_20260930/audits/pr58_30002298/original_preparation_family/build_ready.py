from pathlib import Path
import datetime,hashlib,json,os,stat
from packet_common import HERE,source_check
assert not (HERE/"INDEX.json").exists() and not (HERE/"READY.json").exists() and not (HERE/"SELF_MANIFEST.json").exists()
controls=source_check(True)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (HERE/"RESEARCH_LOG.md").open("a") as stream:
    stream.write("\n"+now+" —100% original SOURCE preparation;0% mathematical-discovery credit. Actual checker25015 exited0 with273 source checks and19 then-completed captures; its genuine completed supervisor capture adds the20th. Exact17 scientific files, source joins,0/5 empty attempt ledger, three private historical receipts, old/final metadata-only snapshot relation and separate successful queue retry are complete. Two ENOSPC capture domains remain explicitly incomplete with surviving bytes, not fabricated PIDs/times. Full fixed-payload mode/topology inventory and READY follow. ROOT-only closure/readback remain unexecuted; no accepted math/priority verdict or native/Git/remote/paper action.\n")
paths=sorted(x for x in HERE.rglob("*") if x.is_file())
for x in [HERE,*HERE.rglob("*")]:
    assert not x.is_symlink()
    if x.is_dir():x.chmod(0o755)
for x in paths:x.chmod(0o444)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[{"path":x.relative_to(HERE).as_posix(),"bytes":x.stat().st_size,"sha256":digest(x),"mode":format(stat.S_IMODE(x.stat().st_mode),"04o")} for x in paths]
dirs=sorted("." if x==HERE else x.relative_to(HERE).as_posix() for x in [HERE,*HERE.rglob("*")] if x.is_dir())
idx={"schema":"pr58-original-prepared-index/v1","created_UTC":now,"scope":"Fixed SOURCE payload excluding INDEX, READY and future absent-only SELF_MANIFEST","full_mode_mask":"07777","files":rows,"directories":dirs,"root_approval":False}
(HERE/"INDEX.json").write_text(json.dumps(idx,indent=2)+"\n");(HERE/"INDEX.json").chmod(0o444)
ready={"schema":"pr58-original-source-ready/v1","status":"SOURCE_READY_UNCLOSED","created_UTC":now,"manifest_absent_at_handoff":True,"root_approval":False,"new_math_verdict_credit":False,"new_priority_verdict_credit":False,"native_acceptance":False,"index_sha256":digest(HERE/"INDEX.json"),"report_sha256":digest(HERE/"REPORT.md"),"authentication_sha256":digest(HERE/"ORIGINAL_AUTHENTICATION.json"),"accounting_sha256":digest(HERE/"SOURCE_ACCOUNTING.json"),"science_index_sha256":digest(HERE/"SCIENCE_INDEX.json"),"reproduction_sha256":digest(HERE/"REPRODUCTION.json"),"failure_observations_sha256":digest(HERE/"ACTUAL_FAILURE_OBSERVATIONS.json"),"fixed_payload_files":len(rows),"fixed_payload_bytes":sum(x["bytes"] for x in rows),"prepared_files":len(rows)+2,"directories":len(dirs),"original_scientific_bodies":17,"original_author_recommended_status":"already_solved","original_used_substantive_attempts":0,"original_attempt_limit":5,"original_JSONL_entries":0,"generic_original_response_count_supplied":False,"new_route_increment":False,"preparation_completion_percent":100,"mathematical_discovery_credit_percent":0,"actual_SOURCE_verifier_child_pid":25015,"actual_SOURCE_verifier_assertions":273,"complete_actual_captures":20,"incomplete_failed_capture_domains":2,"primary_corpus_copies_included":False,"ROOT_closer_execution":"UNEXECUTED","ROOT_reader_execution":"UNEXECUTED","ROOT_closer_argv":["/usr/bin/python3","-B",str(HERE/"ROOT_close_source.py"),"--root-only-close-after-reading"],"ROOT_reader_argv_template":["/usr/bin/python3","-B",str(HERE/"ROOT_read_closed_source.py"),"--root-only-read-after-close","ACTUAL_RETURNED_SELF_MANIFEST_SHA256"],"qualification":"Original SOURCE custody only; author already_solved recommendation is not current acceptance. No future ROOT reading/closure or native/Git/paper/DOI authority."}
(HERE/"READY.json").write_text(json.dumps(ready,indent=2)+"\n");(HERE/"READY.json").chmod(0o444)
from packet_common import prepared_check
prepared_check(False)
print(json.dumps({"status":"SOURCE_READY_UNCLOSED","actual_preparer_freezer_pid":os.getpid(),"utc":now,"prepared_files":len(rows)+2,"fixed_payload_bytes":ready["fixed_payload_bytes"],"all_prepared_bytes":sum(x.stat().st_size for x in HERE.rglob("*") if x.is_file()),"ready_sha256":digest(HERE/"READY.json"),"index_sha256":digest(HERE/"INDEX.json"),"report_sha256":digest(HERE/"REPORT.md"),"manifest_absent":not (HERE/"SELF_MANIFEST.json").exists(),"ROOT_helpers_executed":False}))
