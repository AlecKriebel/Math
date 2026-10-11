import datetime,hashlib,json,pathlib,stat
HERE=pathlib.Path(__file__).absolute().parent
EXPECTED=pathlib.Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr58_30002298/original_preparation_family")
assert HERE==EXPECTED
def sha(b):return hashlib.sha256(b).hexdigest()
def js(rel):return json.loads((HERE/rel).read_bytes())
def mode(p):return format(stat.S_IMODE(p.stat().st_mode),"04o")
def topology():
    assert all(not x.is_symlink() for x in [HERE,*HERE.parents,*HERE.rglob("*")])
    return sorted(x.relative_to(HERE).as_posix() for x in HERE.rglob("*") if x.is_file()),sorted("." if x==HERE else x.relative_to(HERE).as_posix() for x in [HERE,*HERE.rglob("*")] if x.is_dir())
def source_check(include_preparation_capture=True):
    checks=0
    def ck(v):
        nonlocal checks
        assert v
        checks+=1
    a=js("ORIGINAL_AUTHENTICATION.json");s=js("SOURCE_ACCOUNTING.json");q=js("QUEUE_SOURCE_AUTHENTICATION.json");replay=js("REPRODUCTION.json")
    ck(a["original_head"]=="465d771ec1ddc91877e8d9db51ed59aea1b0d97d")
    ck(a["github_base_oid"]=="c6975ca76f9f667f1250ba403d0e6da2aafe14d0" and a["actual_merge_base_oid"]=="60292bed09f59236aa192cb17aa138f7b4750e1a")
    ck(a["original_science_file_count"]==17 and a["complete_diff_file_count"]==18 and a["local_object_check_actual_exit"]==128)
    diff=(HERE/"FULL_PR_DIFF.patch").read_bytes();ck(len(diff)==a["full_diff"]["bytes"]==86772 and sha(diff)==a["full_diff"]["sha256"])
    ck(diff==(HERE/"captures/full_original_diff/stdout.bin").read_bytes())
    ck({x.relative_to(HERE/"original").as_posix() for x in (HERE/"original").rglob("*") if x.is_file()}=={x["relative_path"] for x in a["original_science_files"]})
    idx=js("SCIENCE_INDEX.json");ck(idx["original_science_files"]==17 and len(idx["files"])==17)
    for row in a["original_science_files"]:
        body=(HERE/"original"/row["relative_path"]).read_bytes()
        ck(len(body)==row["bytes"] and sha(body)==row["sha256"])
        ck(hashlib.sha1(b"blob "+str(len(body)).encode()+b"\0"+body).hexdigest()==row["git_blob_sha1"])
    for row in idx["files"]:
        body=(HERE/row["path"]).read_bytes();ck(len(body)==row["bytes"] and sha(body)==row["sha256"])
    metadata=json.loads((HERE/"captures/api_pr_metadata/stdout.bin").read_bytes())
    ck(metadata["head"]["sha"]==a["original_head"] and metadata["base"]["sha"]==a["github_base_oid"] and metadata["draft"] and metadata["state"]=="open")
    compare=json.loads((HERE/"captures/actual_merge_base/stdout.bin").read_bytes())
    ck(compare["merge_base_commit"]["sha"]==a["actual_merge_base_oid"])
    commit=json.loads((HERE/"captures/head_commit/stdout.bin").read_bytes());ck(commit["sha"]==a["original_head"] and commit["tree"]["sha"]==a["root_tree"])
    trees={}
    for capname in ["root_tree","tree_unsolved_math_prioritization","tree_attempts","tree_30002298","review_tree"]:
        tree=json.loads((HERE/"captures"/capname/"stdout.bin").read_bytes());ck(not tree["truncated"])
        body=b""
        for entry in sorted(tree["tree"],key=lambda x:(x["path"]+("/" if x["type"]=="tree" else "")).encode()):
            body+=entry["mode"].lstrip("0").encode()+b" "+entry["path"].encode()+b"\0"+bytes.fromhex(entry["sha"])
        ck(hashlib.sha1(b"tree "+str(len(body)).encode()+b"\0"+body).hexdigest()==tree["sha"]);trees[capname]=tree
    ck(trees["root_tree"]["sha"]==commit["tree"]["sha"])
    for parent,name,child in [("root_tree","unsolved_math_prioritization","tree_unsolved_math_prioritization"),("tree_unsolved_math_prioritization","attempts","tree_attempts"),("tree_attempts","30002298","tree_30002298"),("tree_30002298","review","review_tree")]:
        ck(next(x for x in trees[parent]["tree"] if x["path"]==name)["sha"]==trees[child]["sha"])
    for row in a["original_science_files"]:
        parts=row["relative_path"].split("/");tree=trees["review_tree" if len(parts)==2 else "tree_30002298"]
        ck(next(x for x in tree["tree"] if x["path"]==parts[-1])["sha"]==row["git_blob_sha1"])
    changed=json.loads((HERE/"captures/changed_files/stdout.bin").read_bytes())
    ck(len(changed)==18 and {x["filename"] for x in changed}=={x["repository_path"] for x in a["original_science_files"]}|{"unsolved_math_prioritization/QUEUE.md"})
    ck(q["selected_head_queue_literal"]==s["original_draft_proposed_queue_literal"][1:])
    ck((HERE/"captures/head_queue_literal_retry/stdout.bin").read_text().splitlines()==[q["selected_head_queue_literal"]])
    ck(q["queue_blob_sha1_in_authenticated_tree"]==next(x for x in trees["tree_unsolved_math_prioritization"]["tree"] if x["path"]=="QUEUE.md")["sha"]==a["original_queue_destination_blob_sha1"])
    wrapper=js("original/source_record.json");ck(wrapper["record"]==json.loads(s["SQL_selected_row"]["payload_literal"]))
    ck(s["original_record_typed_equal_to_raw_and_SQL"] and s["raw_report_key_present"] is False and "raw_report_value" not in s)
    ck(s["SQL_selected_row"]["report_is_SQL_NULL"] is False and s["SQL_selected_row"]["report_literal"]=="{}")
    ck(wrapper["research_result_for_code"] is None and s["archived_wrapper_research_result_for_code_value"] is None)
    ck(not (HERE/"original/prior_report.json").exists() and not (HERE/"original/status.json").exists())
    ck(s["original_status_json_present"] is False and s["archived_separate_prior_report_file_present"] is False)
    ck(s["native_state_key_present"] is False and "native_state_selected" not in s)
    ck(s["original_draft_proposes"]=={"Status":"already_solved","Turns":"0/5"})
    ready=js("original/readiness.json");ck(ready["used_substantive_attempts"]==s["original_used_substantive_attempts"]==0 and ready["maximum_substantive_attempts"]==s["original_maximum_substantive_attempts"]==5)
    ck((HERE/"original/turns.jsonl").read_bytes()==b"" and s["original_turn_log_entry_count"]==0 and s["original_turn_log_entries"]==[])
    ck(s["generic_original_response_count_supplied"] is False and s["new_response_or_route_increment"] is False)
    old=(HERE/"original/review/source_snapshot.md").read_bytes();current=(HERE/"original/SOURCE_STATUS.md").read_bytes()
    ck(sha(old)==ready["reviewed_mathematical_snapshot_sha256"]=="457559b700340e08ab2402629685c961b15327f74a21a354be198c561fd601e0")
    ck(sha(current)==ready["artifact_sha256"]=="fc9b927d0755ca48a61e4d2e90f5189c9d896e00a417ff8f1c10ec880bc8ec3e")
    ck(old.replace(b"Separate adversarial review is pending.",b"Separate adversarial source and mathematical review passed; see [the report](review/REVIEW.md).")==current)
    failures=js("ACTUAL_FAILURE_OBSERVATIONS.json");ck(failures["actual_tool_exit_code"]==1 and failures["missing_PID_and_UTC_evidence_not_reconstructed"])
    missing={"queue_authentication","head_queue_literal"};complete=0
    for d in (HERE/"captures").iterdir():
        if d.name in missing:
            ck(not (d/"CAPTURE.json").exists());continue
        if d.name=="preparation_check" and not include_preparation_capture:continue
        cap=json.loads((d/"CAPTURE.json").read_bytes())
        ck(cap["schema"]=="pr58-original-actual-command-capture/v1" and type(cap["child_pid"]) is int and cap["child_pid"]>0 and cap["ROOT_approval"] is False)
        ck(cap["exit_code"]==(128 if d.name=="local_original_object" else 0))
        ck(datetime.datetime.fromisoformat(cap["utc_start"])<=datetime.datetime.fromisoformat(cap["utc_end"]))
        op=(d/"operator_prelaunch.py").read_bytes();ck(len(op)==cap["operator"]["bytes"] and sha(op)==cap["operator"]["sha256"] and op==(HERE/"capture_command.py").read_bytes())
        ck(cap["operator_unchanged_after"] and cap["sources_unchanged_after"])
        for row in cap["sources"]:
            b=pathlib.Path(row["saved"]).read_bytes();ck(len(b)==row["bytes"] and sha(b)==row["sha256"] and b==pathlib.Path(row["original"]).read_bytes())
        for channel in ["stdout","stderr"]:
            b=(d/(channel+".bin")).read_bytes();ck(len(b)==cap[channel]["bytes"] and sha(b)==cap[channel]["sha256"])
        complete+=1
    for job in replay["jobs"]:
        cap=json.loads(pathlib.Path(job["capture"]).read_bytes());ck(job["actual_child_pid"]==cap["child_pid"] and job["actual_operator_pid"]==cap["operator_pid"] and job["argv"]==cap["argv"] and job["utc_start"]==cap["utc_start"] and job["utc_end"]==cap["utc_end"])
        written=pathlib.Path(job["written_receipt"]["path"]).read_bytes();reference=pathlib.Path(job["exact_original_reference"]["path"]).read_bytes()
        ck(written==reference and sha(written)==job["written_receipt"]["sha256"] and len(written)==job["written_receipt"]["bytes"])
        out=json.loads(written);ck(out["status"]=="PASS" and out["exact_assertions"]==job["exact_assertions"] and job["new_mathematical_independence"] is False and job["code_hashes_proof"] is False)
        stdout=pathlib.Path(job["capture"]).with_name("stdout.bin").read_bytes();ck((stdout==written)==job["stdout_full_written_receipt"])
    ck(replay["new_math_verdict_credit"] is False and replay["new_priority_verdict_credit"] is False and replay["root_approval"] is False)
    return {"source_checks":checks,"complete_actual_captures":complete,"incomplete_failed_capture_domains":2,"original_scientific_bodies":17}
def prepared_check(closed=False):
    idx=js("INDEX.json");ready=js("READY.json")
    assert idx["schema"]=="pr58-original-prepared-index/v1" and ready["schema"]=="pr58-original-source-ready/v1"
    assert ready["index_sha256"]==sha((HERE/"INDEX.json").read_bytes())
    for key,name in [("report_sha256","REPORT.md"),("authentication_sha256","ORIGINAL_AUTHENTICATION.json"),("accounting_sha256","SOURCE_ACCOUNTING.json"),("science_index_sha256","SCIENCE_INDEX.json"),("reproduction_sha256","REPRODUCTION.json"),("failure_observations_sha256","ACTUAL_FAILURE_OBSERVATIONS.json")]:assert ready[key]==sha((HERE/name).read_bytes())
    assert ready["manifest_absent_at_handoff"] and ready["root_approval"] is False and ready["new_math_verdict_credit"] is False
    assert ready["original_used_substantive_attempts"]==0 and ready["original_attempt_limit"]==5 and ready["original_JSONL_entries"]==0 and ready["new_route_increment"] is False
    files,dirs=topology();expected={x["path"] for x in idx["files"]}|{"INDEX.json","READY.json"}
    if closed:expected.add("SELF_MANIFEST.json")
    assert set(files)==expected and len(files)==len(expected) and dirs==idx["directories"]
    assert len(idx["files"])==ready["fixed_payload_files"] and sum(x["bytes"] for x in idx["files"])==ready["fixed_payload_bytes"]<1000000
    for row in idx["files"]:
        file=HERE/row["path"];b=file.read_bytes();assert len(b)==row["bytes"] and sha(b)==row["sha256"] and mode(file)==row["mode"]=="0444"
    for name in ["INDEX.json","READY.json"]:assert mode(HERE/name)=="0444"
    for rel in dirs:assert mode(HERE if rel=="." else HERE/rel)=="0755"
    controls=source_check(True)
    cap=js("captures/preparation_check/CAPTURE.json");out=json.loads((HERE/"captures/preparation_check/stdout.bin").read_bytes())
    assert out["status"]=="PASS_ORIGINAL_SOURCE_CHECKS_ONLY" and out["actual_verifier_pid"]==cap["child_pid"]
    assert out["source_checks"]>0 and controls["complete_actual_captures"]==out["complete_actual_captures"]+1
    return idx,ready,controls
