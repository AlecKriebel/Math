"""MIT licensed. Source/provenance consistency only; no mathematical certification."""
import hashlib,json,pathlib,stat
def digest(data): return hashlib.sha256(data).hexdigest()
def pin_check(e):
    p=pathlib.Path(e["path"])
    assert not p.is_symlink() and p.is_file(),str(p)
    raw=p.read_bytes()
    assert len(raw)==e["bytes"] and digest(raw)==e["sha256"],str(p)
    assert stat.S_IMODE(p.stat().st_mode)==int(e["full_mode_07777"],8),str(p)
    assert p.stat().st_nlink==e["nlink"]==1,str(p)
    return raw
def family_check(e):
    root=pathlib.Path(e["path"]); index=json.loads(pin_check(e["index_pin"]))
    source_files=index["files"]
    entries=source_files if isinstance(source_files,list) else [dict(v,path=k) for k,v in source_files.items()]
    indexed={x["path"] for x in entries}
    assert len(indexed)==len(entries)
    excluded=set(e["excluded_fixed_metadata"])
    actual_files=set(); actual_dirs={"."}
    assert not root.is_symlink() and stat.S_IMODE(root.stat().st_mode)==0o755
    for p in root.rglob("*"):
        assert not p.is_symlink(),str(p)
        rel=p.relative_to(root).as_posix()
        if p.is_dir():
            actual_dirs.add(rel); assert stat.S_IMODE(p.stat().st_mode)==0o755
        elif p.is_file():
            actual_files.add(rel); assert stat.S_IMODE(p.stat().st_mode)==0o444 and p.stat().st_nlink==1
        else: raise AssertionError(str(p))
    assert actual_files==indexed|excluded,(str(root),"file topology changed")
    assert not indexed&excluded,(str(root),"excluded metadata indexed")
    assert len(actual_files)==e["files_including_index"]
    assert len(actual_dirs)==e["directories_including_root"]
    d=index["directories"]
    dirnames={(x["path"] if isinstance(x,dict) else x) for x in d} if isinstance(d,list) else set(d)
    assert actual_dirs==dirnames,(str(root),"directory topology changed")
    for x in entries:
        p=root/x["path"]; raw=p.read_bytes()
        assert len(raw)==x["bytes"] and digest(raw)==x["sha256"],str(p)
        mode=x.get("full_mode_07777",x.get("mode_07777",x.get("mode",x.get("full_mode"))))
        mode=int(mode,8) if isinstance(mode,str) else mode
        assert stat.S_IMODE(p.stat().st_mode)==mode==0o444,str(p)
    for p in actual_dirs:
        value=(next(x["full_mode_07777"] for x in d if isinstance(x,dict) and x["path"]==p) if isinstance(d[0],dict) else index["directory_full_mode"]) if isinstance(d,list) else d[p]
        mode=int(value,8) if isinstance(value,str) else value
        assert stat.S_IMODE((root/p).stat().st_mode)==mode==0o755
    return len(actual_files)
def verify_bindings(root):
    root=pathlib.Path(root)
    st=json.loads((root/"STATUS.json").read_bytes())
    b=json.loads((root/"BINDINGS.json").read_bytes())
    ev=json.loads((root/"ROOT_EVIDENCE.json").read_bytes())
    assert st["operative_disposition"]=="already_solved" and st["original_budget"]=="0/5"
    assert st["substantive_proof_attempts"]==0 and st["budget"]==5
    assert st["new_mathematical_attempts"]==st["audit_editorial_increment"]==st["new_contribution_credit"]==0
    assert st["full_target_answered_by_attributed_theorem"] is True
    assert st["imported_existence_independently_reconstructed"] is False
    assert st["paper_prepared"] is False and st["DOI_or_upload"] is False and st["priority_or_novelty_claim"] is False
    assert st["native_Git_PR_acceptance_mutation"] is False
    assert st["ROOT_current_helpers_executed_by_preparer"] is False and st["current_packet_ROOT_custody_claimed"] is False
    assert st["ROOT_current_scientific_approval_claimed"] is True
    assert b["head"]==st["original_head"]=="b5a4829365f2a0bd5f42b7653c5cfacfa6b01d85"
    assert len(b["original_science"])==10
    for x in b["original_science"]+b["audited_in_place"]+b["ROOT_actual_capture_files"]: pin_check(x)
    totals=[family_check(x) for x in b["whole_family_bindings"]]
    assert totals==[175,24,37]
    raw=pin_check(ev["ROOT_scientific_record"]); adj=json.loads(raw)
    assert digest(raw)==st["ROOT_scientific_adjudication_sha256"]=="99a48b3c7236057a4abddc3112fd0e257d71e73e8d8d0d08c5dd39c0be39fdff"
    assert adj["actual_writer_pid"]==95096 and adj["utc"]=="2026-10-03T19:05:03.198132+00:00"
    assert adj["scientific_verdict"]=="VALID_ATTRIBUTED_ALREADY_SOLVED_NEGATIVE_ANSWER"
    assert adj["status"]=="already_solved" and adj["original_budget"]=="0/5"
    assert adj["new_attempts"]==adj["audit_attempts"]==adj["novelty_credit"]==0
    assert adj["native_acceptance_completed"] is False and adj["paper_DOI_tracker"] is False
    assert adj["full_imported_construction_independently_recertified"] is False
    qual=(root/"PROOF_PRECISION_QUALIFICATION.md").read_text()
    assert "U(2)/SO(2)" in qual and "pi2 is Z" in qual and "pi2(U(2))=0" in qual
    assert "time mesh" in qual and "2epsilon/Delta t" in qual
    scope=(root/"CURRENT_SCIENTIFIC_SCOPE.md").read_text()
    assert "attributed imports" in scope and "No newly reviewed publisher" in scope
    assert "time mesh" in scope and "U(2)/SO(2)" in scope
    acc=ev["typed_prior_accounting"]
    assert acc["raw_report_key_present"] is False and acc["raw_upstream_key"]=="KP-1.66"
    assert acc["selected_raw_value"] is None and acc["upstream_flat_report_field_present"] is False
    assert acc["SQL_storage_type"]=="text" and acc["SQL_exact_text_bytes"]==2 and acc["SQL_exact_text_literal"]=="{}"
    assert acc["SQL_exact_text_sha256"]=="44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
    assert acc["SQL_empty_object_is_missing_report_join_fallback"] is True
    assert acc["original_prior_report_json_present_dict_placeholder"] is True
    assert acc["original_turn_ledger_present"] is False and acc["original_executable_math_checker_present"] is False
    assert acc["new_math_attempts"]==acc["audit_editorial_increment"]==0
    assert ev["mode_chronology"]["current_original_close"]["full_mode_07777"]=="0444"
    pin_check(ev["mode_chronology"]["current_original_close"])
    ops=ev["actual_custody_captures"]
    assert [x["pid"] for x in ops]==[91483,91487,91951,91953,92189,92194,92415]
    assert ev["actual_scientific_writer_capture"]["pid"]==95096
    for x in ops+[ev["actual_scientific_writer_capture"]]:
        p=pathlib.Path(x["capture_path"]); c=json.loads(p.read_bytes())
        assert c["actual_execution"] is True and c["completed"] is True and c["exit_code"]==0
        assert c["pid"]==x["pid"] and c["started_utc"]==x["started_utc"] and c["finished_utc"]==x["finished_utc"]
        for stream in ("stdout","stderr"):
            raw=(p.parent/c[stream]["path"]).read_bytes()
            assert len(raw)==c[stream]["bytes"] and digest(raw)==c[stream]["sha256"]
        assert c["stderr"]["bytes"]==0
        assert digest((p.parent/"prelaunch_operator.py").read_bytes())==c["operator_sha256"]
    assert not any(p.suffix in (".pdf",".png",".jpg") or p.name.endswith(".layout.txt") for p in root.rglob("*") if p.is_file())
    return {"original_files":10,"bound_family_files":totals,"actual_ROOT_custody_operations":7,
            "actual_ROOT_scientific_writer_pid":95096,"qualified_scientific_adjudication_bound":True,
            "imported_existence_reconstructed":False,"current_ROOT_helper_execution":False,
            "new_math_or_review_credit":0,"paper_prepared":False}
