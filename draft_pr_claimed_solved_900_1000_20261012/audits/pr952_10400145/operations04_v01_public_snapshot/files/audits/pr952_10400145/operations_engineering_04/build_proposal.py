from pathlib import Path
import hashlib,difflib
OWN=Path(__file__).resolve().parent;base=(OWN/'BASE_accept_pr952.py').read_bytes()
if hashlib.sha256(base).hexdigest()!='888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8':raise RuntimeError('base pin')
s=base.decode();pos=s.index('def finalize(args,context):')
helpers='''def local_final_record(existing,expected):
    """Retain a same-outcome record, including its original time/extra metadata."""
    need(type(existing) is dict and type(existing.get('utc')) is str,'local final record schema/time')
    utc(existing['utc'])
    need(all(name in existing and exact(existing[name],value) for name,value in expected.items() if name!='utc'),'local completed outcome conflicts with approved publication')
    return existing


def local_final_inventory(inventory,record):
    need(type(inventory) is list and all(type(item) is dict and type(item.get('number')) is int for item in inventory),'local inventory list/strict PR identity')
    numbers=[item['number'] for item in inventory]
    need(len(numbers)==len(set(numbers)),'duplicate local inventory PR identity')
    matches=[i for i,item in enumerate(inventory) if item['number']==PR]
    need(len(matches)==1,'exactly one target inventory item required')
    index=matches[0];item=inventory[index]
    need(item.get('headRefOid')==HEAD and item.get('baseRefName')=='main' and item.get('url')==f'https://github.com/AlecKriebel/Math/pull/{PR}','local target inventory exact head/main/URL')
    entries=item.get('entries')
    need(type(entries) is list and len(entries)==1 and type(entries[0]) is dict and type(entries[0].get('id')) is str and entries[0]['id']==KEY,'local target inventory exact single problem identity')
    desired={'disposition':record['outcome'],'doi':record['doi'],'tracker_range':record['tracker_range'],'merge_commit':record['merge_commit'],'native_ledger_commit':record['native_ledger_commit'],'accepted_freeze_sha256':record['accepted_freeze_sha256'],'original_pr_head':HEAD,'problem_id':KEY,'record_url':record['record_url']}
    need(type(item.get('disposition')) is str and item['disposition'] in ('pending_audit','claimed_solved',record['outcome']),'conflicting/malformed inventory disposition')
    for name,value in desired.items():
        if name in item and name!='disposition':need(exact(item[name],value),'conflicting/malformed inventory publication field: '+name)
    if 'outcome' in item:need(exact(item['outcome'],record['outcome']),'conflicting inventory outcome')
    result=copy.deepcopy(inventory);result[index].update(desired)
    need(all(exact(item,result[i]) for i,item in enumerate(inventory) if i!=index),'unrelated inventory item changed')
    return result,index


def local_final_state(state,record):
    need(type(state) is dict,'local state object')
    for name in ('eligible_prs','completed_prs','published_prs'):
        rows=state.get(name);need(type(rows) is list and all(type(x) is int for x in rows) and len(rows)==len(set(rows)),'local state strict unique '+name)
    need(state['eligible_prs'] and PR in state['eligible_prs'],'target eligible and nonzero denominator')
    rows=state.get('completed_results');need(type(rows) is list and all(type(x) is dict and type(x.get('pr')) is int and type(x.get('outcome')) is str for x in rows),'local completed result identities')
    ids=[x['pr'] for x in rows];need(len(ids)==len(set(ids)) and set(ids)==set(state['completed_prs']),'local completion lists inconsistent/duplicate')
    published={x['pr'] for x in rows if x['outcome']=='accepted_merged_preprint_published'}
    need(set(state['published_prs'])==published,'local published list inconsistent')
    active=state.get('active_pr');need(active is None or (type(active) is int and 1<=active<=1000),'local active PR identity/type')
    matches=[x for x in rows if x['pr']==PR]
    if matches:
        local_final_record(matches[0],record)
        need(active!=PR,'completed target still active: explicit state reconciliation required')
    else:need(active in (PR,None) or active>PR,'another earlier active research target')
    return bool(matches),active is not None and active>PR


def local_atomic_json(path,value,expected_pin):
    """Replace one local JSON file atomically after exact observed-input checks.

    The two-file operation is intentionally reconciled from fresh approved
    outcome on retry, rather than replaying stale whole-state snapshots.
    """
    path=Path(path);need(path in (P/'CURRENT_STATE.json',P/'inventory.json'),'only two local bookkeeping paths')
    validate_pin(expected_pin)
    need(fingerprint(read_regular(path,pin=expected_pin))==expected_pin,'local input changed before atomic write')
    raw=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\\n').encode()
    need(len(raw)<=8*1024*1024,'local JSON output cap')
    if fingerprint(raw)==expected_pin:return False
    name=path.relative_to(ROOT).as_posix();need(safe(name),'local atomic output name')
    directory_flags=os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_NONBLOCK
    directory=os.open(ROOT,directory_flags);temporary=None
    try:
        parts=name.split('/')
        for part in parts[:-1]:
            child=os.open(part,directory_flags,dir_fd=directory);os.close(directory);directory=child
        info=os.stat(parts[-1],dir_fd=directory,follow_symlinks=False)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink==1 and stat.S_IMODE(info.st_mode) in (0o600,0o644),'local target regular single-link mode')
        temporary='.pr952-finalize-'+parts[-1]+'-'+os.urandom(12).hex()+'.tmp'
        fd=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_NONBLOCK,stat.S_IMODE(info.st_mode),dir_fd=directory)
        with os.fdopen(fd,'wb') as stream:
            os.fchmod(stream.fileno(),stat.S_IMODE(info.st_mode))
            stream.write(raw);stream.flush();os.fsync(stream.fileno())
        read_regular(path,pin=expected_pin)
        os.replace(temporary,parts[-1],src_dir_fd=directory,dst_dir_fd=directory);temporary=None
        os.fsync(directory)
        need(fingerprint(read_regular(path))==fingerprint(raw),'local atomic exact readback')
        return True
    finally:
        if temporary is not None:
            try:os.unlink(temporary,dir_fd=directory)
            except FileNotFoundError:pass
        os.close(directory)


def reconcile_local_finalization(accepted,freeze,record,context):
    state_raw=read_regular(P/'CURRENT_STATE.json');inventory_raw=read_regular(P/'inventory.json')
    state=strict_json(state_raw);inventory=strict_json(inventory_raw)
    desired_inventory,index=local_final_inventory(inventory,record)
    already,later=local_final_state(state,record)
    desired_state=copy.deepcopy(state);skipped=[];selected=None
    advancing=not already and not later
    if not already:
        completed=sorted([*state['completed_results'],copy.deepcopy(record)],key=lambda x:x['pr'])
        desired_state.update(utc=utc_now(),completed_results=completed,completed_prs=[x['pr'] for x in completed],published_prs=[x['pr'] for x in completed if x['outcome']=='accepted_merged_preprint_published'],shard_completion_estimate_percent=100*len(completed)/len(state['eligible_prs']))
        if advancing:
            skipped,selected=gate_next(inventory)
            desired_state.update(active_pr=selected['number'] if selected else None,active_problem_id=selected['problem_id'] if selected else None,next_pr=selected['number'] if selected else None,active_pr_completion_estimate_percent=0,phase='post_PR952_status_only_gate')
            for name in ['active_original_head','original_candidate_turns','review_families','priority_families','publication_disposition','priority_status','full_package_reviews','active_candidate_revision','active_freeze_sha256','active_package_manifest_sha256','new_priority_research_positive_turns','known_effort_positive_turns','new_mechanism_status','portable_release_tooling']:
                desired_state.pop(name,None)
            if selected:desired_state['active_original_head']=selected['headRefOid']
    # Re-run all semantic conflict checks before either local file is changed.
    need(local_final_state(desired_state,record)[0],'proposed local completion missing')
    need(exact(local_final_inventory(desired_inventory,record)[0],desired_inventory),'proposed inventory not idempotent')
    before={'state':fingerprint(state_raw),'inventory':fingerprint(inventory_raw)}
    plan={'utc':utc_now(),'pr':PR,'original_pr_head':HEAD,'accepted_freeze_sha256':accepted['freeze_sha256'],'approved_outcome':{k:record[k] for k in ('doi','merge_commit','native_ledger_commit','tracker_range','outcome')},'before':before,'target_already_completed':already,'later_active_preserved':later,'status_only_gate_run':advancing,'blind_external_retry_permitted':False}
    numbered_receipt('LOCAL_FINALIZATION_PLAN',plan)
    accepted_review_check(accepted,freeze,context)
    if advancing:
        gate={'utc':utc_now(),'skipped':skipped,'next_eligible':selected,'math_source_read':False,'ascending_range':[953,1000]}
        numbered_receipt('LOCAL_FINALIZATION_STATUS_GATES',gate);save(W/'POST_PR952_STATUS_GATES.json',gate)
    # Inventory first; retries also repair the legacy state-first partial window.
    inventory_changed=local_atomic_json(P/'inventory.json',desired_inventory,before['inventory']) if not exact(desired_inventory,inventory) else False
    state_changed=local_atomic_json(P/'CURRENT_STATE.json',desired_state,before['state']) if not exact(desired_state,state) else False
    actual_state_raw=read_regular(P/'CURRENT_STATE.json');actual_inventory_raw=read_regular(P/'inventory.json')
    actual_state=strict_json(actual_state_raw);actual_inventory=strict_json(actual_inventory_raw)
    need(exact(actual_state,desired_state) and exact(actual_inventory,desired_inventory),'local finalization changed during exact readback')
    need(local_final_state(actual_state,record)[0] and exact(local_final_inventory(actual_inventory,record)[0],actual_inventory),'local finalization incomplete after writes')
    accepted_review_check(accepted,freeze,context)
    receipt={**plan,'completed_utc':utc_now(),'confirmed':True,'local_state_and_inventory_consistent':True,'state_changed':state_changed,'inventory_changed':inventory_changed,'after':{'state':fingerprint(actual_state_raw),'inventory':fingerprint(actual_inventory_raw)},'next_pr':actual_state.get('active_pr')}
    numbered_receipt('LOCAL_FINALIZATION_READBACK',receipt);save(W/'LOCAL_FINALIZATION_RECEIPT.json',receipt)
    return actual_state,receipt


'''
s=s[:pos]+helpers+s[pos:]
s=s.replace("    save(W/'PUBLICATION_FINAL_VERIFICATION.json',native_result);save(W/'PUBLICATION_RECORD.json',record)", "    if (W/'PUBLICATION_RECORD.json').exists():record=local_final_record(load(W/'PUBLICATION_RECORD.json'),record)\n    else:save(W/'PUBLICATION_RECORD.json',record,exclusive=True)\n    save(W/'PUBLICATION_FINAL_VERIFICATION.json',native_result)")
start=s.index("    state=load(P/'CURRENT_STATE.json');inventory=load(P/'inventory.json')",s.index('def finalize(args,context):'));end=s.index('\n\ndef readonly_preflight(',start)
s=s[:start]+'''    state,local_receipt=reconcile_local_finalization(accepted,freeze,record,context)
    if not local_receipt['target_already_completed']:
        for path in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
            with path.open('a') as stream:stream.write(f"\\n{utc_now()} — PR952 workflow100%; shard {state['shard_completion_estimate_percent']:.2f}%. Actual main merge {merge['mergeCommit']['oid']}; DOI {publication['doi']}; tracker {tracker['updated_range']}; native {native['commit']}. Exact local readbacks verified; original declared1/5 retained separately, historical native count UNKNOWN, zero new author proof responses.\\n")
    print(json.dumps({'PR952':record,'next_pr':state.get('active_pr'),'local_finalization':local_receipt}))
''' +s[end:]
compile(s,str(OWN/'PROPOSED_accept_pr952.py'),'exec');(OWN/'PROPOSED_accept_pr952.py').write_text(s)
(OWN/'PROPOSED.patch').write_text(''.join(difflib.unified_diff(base.decode().splitlines(keepends=True),s.splitlines(keepends=True),fromfile='a/draft_pr_claimed_solved_900_1000_20261012/accept_pr952.py',tofile='b/draft_pr_claimed_solved_900_1000_20261012/accept_pr952.py')))
print(hashlib.sha256(s.encode()).hexdigest())
