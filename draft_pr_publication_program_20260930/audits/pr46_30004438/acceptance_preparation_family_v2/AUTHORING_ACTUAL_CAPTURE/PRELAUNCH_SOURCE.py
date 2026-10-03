"""Own literal V2 source authoring; never import/compile/run proposed production."""
from pathlib import Path
import datetime as dt, difflib, hashlib, json, os
H = Path(__file__).resolve().parent
A = H.parent
V = A / 'acceptance_preparation_family'
R = A.parents[2]
NAMES = ['pr46_guards.py','seal_final_evidence.py','capture_root_final_operation.py',
 'integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']

def sha(raw): return hashlib.sha256(raw).hexdigest()
def put(path, raw):
    with path.open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
def enc(obj): return (json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False)+'\n').encode()
def change(text, before, after, count=1):
    assert text.count(before) == count, ('Literal replacement count', before, text.count(before), count)
    return text.replace(before, after)

OWNERSHIP = '''PROGRAM_LOG = B / 'RESEARCH_LOG.md'
ADDITIONAL_OWNED_MUTATION_PATHS = {PROGRAM_LOG.relative_to(R).as_posix()}
OWNED_OPERATIONAL_LOGS = [('root_problem', A / 'ROOT_RESEARCH_LOG.md'), ('program', PROGRAM_LOG)]


def owned_mutation_path(name):
    relative(name)
    return (name in NATIVE or name in ADDITIONAL_OWNED_MUTATION_PATHS
        or name.startswith(K.relative_to(R).as_posix()+'/')
        or name.startswith(A.relative_to(R).as_posix()+'/'))


def protected_foreign_paths(paths):
    require(type(paths) is list and all(type(n) is str for n in paths)
        and paths==sorted(set(paths)), 'Exact sorted ROOT protected foreign path list')
    for name in paths:
        require(not owned_mutation_path(name), 'Owned mutation path cannot be protected foreign')
    return paths


def operational_log_note(clock):
    return ('\\n## '+clock+' — PR46 actual accepted credited known-result source correction\\n\\n'
        'Workflow100%; scientific discovery0%; original0/5,new0,audit0. Actual MERGED original-head/tree checked. '
        'Program36/180=20%; one present native mirror remains. No paper/newDOI/tracker/release.\\n')


def owned_log_append_check(pre):
    foreign_check(pre)
    record=load(A/'integration_log_append_receipt.json')
    keyset(record,{'schema','utc','logs','note','source_preparation_did_not_append'},'Exact owned operational log receipt')
    required(record,{'schema':'pr46-actual-owned-operational-log-append/v1',
        'source_preparation_did_not_append':True},'Actual owned log append, not source preparation')
    final=load(A/'integration_finalization.json');note=operational_log_note(final['utc'])
    require(record['note']==note,'Exact derived operational log append')
    require(utc_clock(final['utc'],'Actual finalization')<=utc_clock(record['utc'],'Actual owned append')
        <=dt.datetime.now(dt.timezone.utc),'Actual operational append chronology')
    require(type(record['logs']) is list and len(record['logs'])==2,'Exactly two actual appended operational logs')
    for row,(label,path) in zip(record['logs'],OWNED_OPERATIONAL_LOGS):
        keyset(row,{'log','before','retained_preimage','after','before_worktree_mode','after_worktree_mode'},'Complete owned operational append row')
        name=path.relative_to(R).as_posix();require(row['log']==name and owned_mutation_path(name),'Exact owned log destination')
        before=exact_reference(row['before']);retained=exact_reference(row['retained_preimage']);after=exact_reference(row['after'])
        require(before['path']==after['path']==name and retained['path']==(A/'integration_log_preimages'/(label+'.bin')).relative_to(R).as_posix(),'Exact retained log paths')
        raw=regular(R,retained['path']).read_bytes();check(R,[retained,after])
        require(len(raw)==before['bytes'] and sha(raw)==before['sha256'] and regular(R,name).read_bytes()==raw+note.encode(),'Exact preserved whole log prefix plus reviewed append')
        require(type(row['before_worktree_mode']) is int and row['before_worktree_mode']==row['after_worktree_mode']
            and 0<=row['before_worktree_mode']<=0o7777
            and stat.S_IMODE(path.stat().st_mode)==row['after_worktree_mode'],'Full owned log mode preserved')
    return record


def source_repair_basis():
    record=load(HERE/'SOURCE_REPAIR_BINDINGS.json')
    required(record,{'schema':'pr46-acceptance-source-v2-repair-bindings/v1',
        'status':'COMPLETED_REJECTED_V1_ADVERSE_BINDINGS','closed_adverse_binding_completed':True,
        'superseded_v1_manifest_sha256':'d97fb190b4b20a2566a1415130e4b7729cb1f8377f8b823e0fd0b263a3315dab',
        'future_acceptance_approved':False,'production_imported_compiled_executed':False},'Actual adverse source history, not approval')
    refs=rows(record['complete_first_party_refs']);check(R,refs)
    for row in refs:
        require(type(row['full_mode']) is int and stat.S_IMODE(regular(R,row['path']).stat().st_mode)==row['full_mode'],'Complete rejected-source evidence full mode')
    v=A/'acceptance_preparation_family';manifest(v,'PREPARATION_MANIFEST.json',record['superseded_v1_manifest_sha256'],166,frozen=True)
    require(equal(load(v/'PREPARATION_MANIFEST.json'),load(HERE/'EXPECTED_REJECTED_V1_MANIFEST.json')),'Entire rejected V1 source closure')
    adverse=regular(R,record['closed_adverse_manifest']['path']);am=load(adverse)
    require(sha(adverse.read_bytes())==record['closed_adverse_manifest']['sha256'] and adverse.parent==A/'acceptance_source_adversary_family','Exact closed adverse family')
    rr=rows(am['files']);require(am['self_excluded']==[adverse.name] and type(am['files_count']) is int and am['files_count']==len(rr),'Adverse self-only closure')
    check(adverse.parent,rr);exact(adverse.parent,{z['path'] for z in rr}|{adverse.name});frozen_files(adverse.parent,rr,adverse.name)
    require(equal(load(R/record['closed_adverse_verdict']['path']),load(HERE/'EXPECTED_REJECTED_V1_ADVERSE_VERDICT.json')),'Entire final adverse verdict')
    require(equal(load(R/record['root_complete_adverse_inspection']['path']),load(HERE/'EXPECTED_ROOT_REJECTED_V1_INSPECTION.json')),'Entire genuine ROOT adverse read')
    return [{'path':row['path'],'bytes':row['bytes'],'sha256':row['sha256']} for row in refs]


'''

def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
    old=parse_manifest=json.loads((V/'PREPARATION_MANIFEST.json').read_bytes())
    assert sha((V/'PREPARATION_MANIFEST.json').read_bytes())=='d97fb190b4b20a2566a1415130e4b7729cb1f8377f8b823e0fd0b263a3315dab' and old['files_count']==166
    put(H/'EXPECTED_REJECTED_V1_MANIFEST.json',(V/'PREPARATION_MANIFEST.json').read_bytes())
    inherited=['INPUT_BINDINGS.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json','SCIENTIFIC_SCOPE.json','EXPECTED_NATIVE_TRANSITION.json','ROOT_POST_CONTRACT.json']
    inherited += [p.name for p in V.glob('EXPECTED_*.json')]
    for name in sorted(set(inherited)):
        put(H/name,(V/name).read_bytes())
    changes=[]
    for name in NAMES:
        original=(V/name).read_text();text=original
        text='"""V2 SOURCE ONLY: rejected V1 S1 repaired; independent clean SOURCE audit remains required."""\n'+text if not text.startswith('#!') else text.replace('\n','\n"""V2 SOURCE ONLY: rejected V1 S1 repaired; independent clean SOURCE audit remains required."""\n',1)
        # The exact helper family changes with the V2 anchor; no old source is executed.
        if name=='capture_root_final_operation.py':
            text=change(text,"A / 'acceptance_preparation_family'","A / 'acceptance_preparation_family_v2'")
        if name=='pr46_guards.py':
            text=change(text,'def foreign_capture(fresh):',OWNERSHIP+'def foreign_capture(fresh):')
            text=change(text,"    foreign_paths=fresh['protected_foreign_tracked_paths'];require(type(foreign_paths) is list and all(type(n) is str for n in foreign_paths) and foreign_paths==sorted(set(foreign_paths)),'Exact sorted ROOT protected foreign path list')\n    for n in foreign_paths:\n        relative(n);require(n not in NATIVE and not n.startswith(K.relative_to(R).as_posix()+'/') and not n.startswith(A.relative_to(R).as_posix()+'/'),'Foreign exception outside exact owned/native scope')","    protected_foreign_paths(fresh['protected_foreign_tracked_paths'])")
            text=change(text,"    paths=fresh['protected_foreign_tracked_paths'];require(type(paths) is list and paths==sorted(set(paths)),'Exact ROOT-declared sorted protected foreign paths')\n    for n in paths:\n        relative(n);require(n not in NATIVE and not n.startswith(K.relative_to(R).as_posix()+'/') and not n.startswith(A.relative_to(R).as_posix()+'/'),'Protected foreign path outside all owned/native scope required')","    paths=protected_foreign_paths(fresh['protected_foreign_tracked_paths'])")
            text=change(text,"    fresh=load(R/pre['fresh_preimage']);paths=fresh['protected_foreign_tracked_paths'];rr=pre['foreign_logs'];require([z['path'] for z in rr]==paths,'Exact protected ROOT declared foreign identities');check(R,rr)","    fresh=load(R/pre['fresh_preimage']);paths=protected_foreign_paths(fresh['protected_foreign_tracked_paths']);rr=pre['foreign_logs'];require([z['path'] for z in rr]==paths,'Exact protected ROOT declared foreign identities');check(R,rr)")
            text=change(text,"sm.parent not in {C,HERE,A/'current_whole_adversary_family',A/'current_source_adversary_family_v2'}","sm.parent not in {C,HERE,A/'acceptance_preparation_family',A/'acceptance_source_adversary_family',A/'current_whole_adversary_family',A/'current_source_adversary_family_v2'}")
            text=change(text,"approved,rp=root_binding_input(root_bindings,root_bindings_sha256);inputs=load(HERE/'INPUT_BINDINGS.json');refs=[]","approved,rp=root_binding_input(root_bindings,root_bindings_sha256);inputs=load(HERE/'INPUT_BINDINGS.json');refs=source_repair_basis()")
        if name=='integrate_reviewed_partial.py':
            text=change(text,"    note='\\n## '+now+' — PR46 actual accepted credited known-result source correction\\n\\nWorkflow100%; scientific discovery0%; original0/5,new0,audit0. Actual MERGED original-head/tree checked. Program36/180=20%; one present native mirror remains. No paper/newDOI/tracker/release.\\n'","    note=g.operational_log_note(now)")
            text=change(text,"    for name,f in [('root_problem',g.A/'ROOT_RESEARCH_LOG.md'),('program',g.B/'RESEARCH_LOG.md')]:","    for name,f in g.OWNED_OPERATIONAL_LOGS:")
            text=change(text,"previous=f.read_bytes(); before_pin=g.pin(f)","previous=f.read_bytes(); before_pin=g.pin(f); before_mode=g.stat.S_IMODE(f.stat().st_mode)")
            text=change(text,"g.write(f,previous+note.encode()); log_receipt.append({'log':f.relative_to(g.R).as_posix(),'before':before_pin,'retained_preimage':g.pin(logdir/(name+'.bin')),'after':g.pin(f)})","g.write(f,previous+note.encode()); f.chmod(before_mode); log_receipt.append({'log':f.relative_to(g.R).as_posix(),'before':before_pin,'retained_preimage':g.pin(logdir/(name+'.bin')),'after':g.pin(f),'before_worktree_mode':before_mode,'after_worktree_mode':g.stat.S_IMODE(f.stat().st_mode)})")
            text=change(text,"g.dump(g.A/'integration_log_append_receipt.json',{'utc':g.stamp(),'logs':log_receipt,'note':note,'source_preparation_did_not_append':True},exclusive=True)","g.dump(g.A/'integration_log_append_receipt.json',{'schema':'pr46-actual-owned-operational-log-append/v1','utc':g.stamp(),'logs':log_receipt,'note':note,'source_preparation_did_not_append':True},exclusive=True)\n    g.owned_log_append_check(pre)")
        if name=='state_mirror_reconciliation.py':
            text=change(text,'    return pre,canonical','    g.owned_log_append_check(pre)\n    return pre,canonical')
        if name=='verify_post_acceptance.py':
            text=change(text,"g.accepted_invariants(acceptance,pins,pre); g.foreign_check(pre)","g.accepted_invariants(acceptance,pins,pre); g.foreign_check(pre); g.owned_log_append_check(pre)")
            text=change(text,"'paper_or_new_doi_or_tracker':False},exclusive=True)","'paper_or_new_doi_or_tracker':False,'owned_operational_log_appends_exact':True,'protected_foreign_paths_exclude_owned_program_log':True},exclusive=True)")
        put(H/name,text.encode())
        changes.extend(difflib.unified_diff(original.splitlines(True),text.splitlines(True),fromfile='closed_v1/'+name,tofile='operative_v2/'+name))
    put(H/'S1_SCOPED_OWNERSHIP_REPAIR.patch',''.join(changes).encode())
    post=json.loads((H/'ROOT_POST_CONTRACT.json').read_bytes());post['required_ROOT_complete_keyset'].append('owned_operational_log_appends_exact');post['required_completed_values']['owned_operational_log_appends_exact']=True;post['required_entire_post_values'].update(owned_operational_log_appends_exact=True,protected_foreign_paths_exclude_owned_program_log=True)
    post['required_complete_inspections'].append('S1 V2: exact program RESEARCH_LOG.md is an owned operational append destination and is rejected from every protected-foreign list before mutation. Every unrelated program/audit/other tracked path remains protected. Exactly two operational log destinations have retained complete prefix bytes, exact derived append text and full mode preservation, verified after finalize and again before mirror/post. No whole-program exclusion. The actual 22-key ROOT post includes this complete owned-log inspection.')
    (H/'ROOT_POST_CONTRACT.json').write_bytes(enc(post))
    scope=json.loads((H/'SCIENTIFIC_SCOPE.json').read_bytes());scope['exact_remaining_gaps']=['New clean V2 acceptance SOURCE adversary, ROOT complete source/predecessor review and independently fresh actual acceptance authority'];(H/'SCIENTIFIC_SCOPE.json').write_bytes(enc(scope))
    plan=json.loads((H/'DRAFT_FINAL_PLAN.json').read_bytes());plan['scientific_scope']=scope;(H/'DRAFT_FINAL_PLAN.json').write_bytes(enc(plan))
    native=json.loads((H/'EXPECTED_NATIVE_TRANSITION.json').read_bytes());native['additional_owned_mutation_paths']=['draft_pr_publication_program_20260930/RESEARCH_LOG.md'];native['unrelated_program_paths_remain_protected']=True;native['exact_owned_log_prefix_append_and_modes_required']=True;(H/'EXPECTED_NATIVE_TRANSITION.json').write_bytes(enc(native))
    put(H/'SOURCE_REPAIR_BINDINGS.json',enc({'schema':'pr46-acceptance-source-v2-repair-bindings/v1','status':'PENDING_ACTUAL_CLOSED_ADVERSE_ROOT_BINDINGS','closed_adverse_binding_completed':False,'superseded_v1_manifest_sha256':'d97fb190b4b20a2566a1415130e4b7729cb1f8377f8b823e0fd0b263a3315dab','closed_adverse_manifest':None,'closed_adverse_verdict':None,'root_complete_adverse_inspection':None,'complete_first_party_refs':[],'future_acceptance_approved':False,'production_imported_compiled_executed':False}))
    put(H/'OWNERSHIP_WRITE_INVENTORY.json',enc({'schema':'pr46-source-v2-exact-write-scope/v1','source_only':True,'additional_owned_tracked_body_paths':['draft_pr_publication_program_20260930/RESEARCH_LOG.md'],'owned_operational_logs':['draft_pr_publication_program_20260930/audits/pr46_30004438/ROOT_RESEARCH_LOG.md','draft_pr_publication_program_20260930/RESEARCH_LOG.md'],'native_body_writes':['unsolved_math_prioritization/QUEUE.md','draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/history.jsonl','unsolved_math_prioritization/state.json'],'canonical_writes':'unsolved_math_prioritization/attempts/30004438/','audit_receipts_captures_retained_preimages_and_final_publication':'draft_pr_publication_program_20260930/audits/pr46_30004438/','lock_open_without_body_write':'draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/tmp/root-accepted-state.lock','lock_creation_only_if_untracked_absent':True,'complete_program_exclusion':False,'canonical_overlay_payload_count':955,'accepted_payload_count':957,'immutable_operative_originals':8,'current_administration_objects':4,'original_substantive_attempts':0,'original_source_verification_responses':1,'new_substantive_attempts':0,'audit_turns':0,'paper_or_new_doi_or_tracker':False}))
    put(H/'SOURCE_STATUS.json',enc({'schema':'pr46-acceptance-source-v2-status/v1','status':'REPAIRED_S1_PENDING_GENUINE_CLOSED_ADVERSE_BINDINGS_AND_PRIVATE_CONTROLS','preparation_completion_percent':35,'actual_acceptance_completion_percent':0,'discovery_credit_percent':0,'production_imported_compiled_executed':False,'future_acceptance_approved':False,'whole_binding_completed':True,'closed_adverse_binding_completed':False,'original_substantive_attempts':0,'original_source_verification_responses':1,'new_substantive_attempts':0,'audit_turns':0}))
    print(json.dumps({'status':'AUTHORED_V2_SOURCE_ONLY_S1_REPAIR','actual_pid':os.getpid(),'production_imported_compiled_executed':False,'future_acceptance_approved':False,'closed_adverse_bound':False,'source_files':NAMES},sort_keys=True))

if __name__=='__main__': main()
