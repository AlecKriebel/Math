from pathlib import Path
import hashlib
OWN=Path(__file__).resolve().parent
old=(OWN/'PROPOSED_accept_pr952.py').read_bytes()
if hashlib.sha256(old).hexdigest()!='07d1088bcbf8a81c71f15f5f096fcced98e4638244eb794df7efffcd0783688b':raise RuntimeError('old authenticated proposal pin')
(OWN/'HISTORICAL_PROPOSAL04_LOG_GAP_accept_pr952.py').write_bytes(old)
s=(OWN/'build_proposal.py').read_text()
start=s.index('def local_atomic_json(');end=s.index('    name=path.relative_to(ROOT)',start)
s=s[:start]+'''def local_atomic_json(path,value,expected_pin):
    path=Path(path);need(path in (P/'CURRENT_STATE.json',P/'inventory.json'),'only two local JSON bookkeeping paths')
    raw=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\\\\n').encode()
    return local_atomic_bytes(path,raw,expected_pin)


def local_atomic_bytes(path,raw,expected_pin):
    """One durable file replacement; fresh semantic reconciliation on retry.

    This is neither a cross-file transaction nor an adversarial multiwriter CAS.
    """
    path=Path(path);need(path in (P/'CURRENT_STATE.json',P/'inventory.json',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md'),'only four required local finalization paths')
    need(type(raw) is bytes and len(raw)<=8*1024*1024,'local byte output schema/cap')
    validate_pin(expected_pin)
    need(fingerprint(read_regular(path,pin=expected_pin))==expected_pin,'local input changed before atomic write')
    if fingerprint(raw)==expected_pin:return False
''' +s[end:]
pos=s.index('def reconcile_local_finalization(')
s=s[:pos]+'''def local_final_log(raw,record):
    """Preserve every unrelated byte and exactly one approved-outcome marker.

    The marker time is the actual reconciliation call time, never the original
    publication record time. An old unmarked narrative remains historical text.
    """
    need(type(raw) is bytes,'local log byte schema')
    token=b'PR952-LOCAL-COMPLETION';prefix=token+b'-V1 '
    keys=('pr','problem_id','outcome','original_pr_head','merge_commit','merged_base','doi','record_url','tracker_range','native_ledger_commit','accepted_freeze_sha256','clean_final_review_manifest_sha256')
    approved={key:record[key] for key in keys}
    approved_sha256=sha(json.dumps(approved,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode())
    markers=[]
    for line in raw.splitlines(keepends=True):
        if token not in line:continue
        need(line.startswith(prefix) and line.endswith(b'\\\\n'),'malformed local completion marker framing')
        marker=strict_json(line[len(prefix):-1])
        need(type(marker) is dict and set(marker)=={'schema','reconciled_utc','workflow_completion_estimate_percent','approved_outcome','approved_sha256'},'malformed local completion marker schema')
        need(marker['schema']=='pr952-local-completion-v1' and type(marker['workflow_completion_estimate_percent']) is int and marker['workflow_completion_estimate_percent']==100,'local completion marker schema/progress')
        utc(marker['reconciled_utc'])
        need(exact(marker['approved_outcome'],approved) and marker['approved_sha256']==approved_sha256,'local completion marker conflicts with approved outcome')
        canonical=prefix+json.dumps(marker,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()+b'\\\\n'
        need(line==canonical,'noncanonical local completion marker')
        markers.append(marker)
    need(len(markers)<=1,'duplicate local completion markers')
    if markers:return raw,markers[0]
    marker={'schema':'pr952-local-completion-v1','reconciled_utc':utc_now(),'workflow_completion_estimate_percent':100,'approved_outcome':approved,'approved_sha256':approved_sha256}
    utc(marker['reconciled_utc'])
    addition=prefix+json.dumps(marker,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()+b'\\\\n'
    return raw+(b'\\\\n' if raw and not raw.endswith(b'\\\\n') else b'')+addition,marker


''' +s[pos:]
s=s.replace("    desired_inventory,index=local_final_inventory(inventory,record)","    desired_inventory,index=local_final_inventory(inventory,record)\n    log_paths={'project_log':P/'RESEARCH_LOG.md','audit_log':A/'RESEARCH_LOG.md'}\n    log_before={role:read_regular(path) for role,path in log_paths.items()}\n    log_desired={role:local_final_log(raw,record) for role,raw in log_before.items()}")
s=s.replace("    before={'state':fingerprint(state_raw),'inventory':fingerprint(inventory_raw)}", "    before={'state':fingerprint(state_raw),'inventory':fingerprint(inventory_raw),**{role:fingerprint(raw) for role,raw in log_before.items()}}")
s=s.replace("    accepted_review_check(accepted,freeze,context)\n    if advancing:","    accepted_review_check(accepted,freeze,context)\n    save(W/'LOCAL_FINALIZATION_RECEIPT.json',{**plan,'confirmed':False,'phase':'RECONCILING_FOUR_REQUIRED_LOCAL_FILES'})\n    if advancing:")
a=s.index("    accepted_review_check(accepted,freeze,context)\n    receipt={**plan");b=s.index('    return actual_state,receipt',a)
s=s[:a]+'''    # Each log is reconciled even if state/inventory were already completed.
    # The canonical confirmed receipt is written only after all four readbacks.
    log_changed={}
    for role,path in log_paths.items():
        desired,marker=log_desired[role]
        log_changed[role]=local_atomic_bytes(path,desired,before[role])
    actual_logs={role:read_regular(path) for role,path in log_paths.items()}
    for role,raw in actual_logs.items():
        need(raw==log_desired[role][0] and local_final_log(raw,record)[0]==raw,'required local log completion readback')
    need(read_regular(P/'CURRENT_STATE.json')==actual_state_raw and read_regular(P/'inventory.json')==actual_inventory_raw,'local state/inventory changed during log reconciliation')
    accepted_review_check(accepted,freeze,context)
    receipt={**plan,'completed_utc':utc_now(),'confirmed':True,'local_state_and_inventory_consistent':True,'both_research_logs_confirmed':True,'state_changed':state_changed,'inventory_changed':inventory_changed,'log_changed':log_changed,'log_markers':{role:log_desired[role][1] for role in log_paths},'after':{'state':fingerprint(actual_state_raw),'inventory':fingerprint(actual_inventory_raw),**{role:fingerprint(raw) for role,raw in actual_logs.items()}},'next_pr':actual_state.get('active_pr')}
    numbered_receipt('LOCAL_FINALIZATION_READBACK',receipt);save(W/'LOCAL_FINALIZATION_RECEIPT.json',receipt)
    need(exact(load(W/'LOCAL_FINALIZATION_RECEIPT.json'),receipt),'canonical local completion receipt exact readback')
''' +s[b:]
a=s.index("    if not local_receipt['target_already_completed']:");b=s.index("    print(json.dumps({'PR952':record",a)
s=s[:a]+s[b:]
(OWN/'build_proposal.py').write_text(s)
