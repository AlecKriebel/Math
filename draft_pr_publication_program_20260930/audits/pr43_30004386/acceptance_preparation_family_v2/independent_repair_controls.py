"""Handwritten independent V1/V2 correlations and byte controls; no proposed source execution."""
from pathlib import Path,PurePosixPath
import hashlib,json,datetime,os,stat,re,copy
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2];V1=A/'acceptance_preparation_family'
sha=lambda b:hashlib.sha256(b).hexdigest();checks=[];negatives=[]
def demand(ok,label):
    if not ok:raise ValueError(label)
    checks.append(label)
def typed(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(typed(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
    return a==b
def read(p):
    demand(p.is_file() and not p.is_symlink(),'Regular full source read '+p.relative_to(R).as_posix())
    return p.read_bytes()
production=['pr43_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']
new={n:read(H/n) for n in production};old={n:read(V1/n) for n in production}
required_deltas={'integrate_reviewed_partial.py':("snapshot_manifest_v2.json","snapshot_manifest.json"),'state_mirror_reconciliation.py':("PR43; source-status correction;","PR43 source-status correction;")}
for n in production:
    expected=old[n]
    if n in required_deltas:
        before,after=required_deltas[n];demand(expected.count(before.encode())==1,'Only one original defect token '+n);expected=expected.replace(before.encode(),after.encode(),1)
    demand(new[n]==expected,'Entire independent prescribed production delta '+n)
for n in ['DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json','SCIENTIFIC_SCOPE.json','EXPECTED_CURRENT_ADMIN.json','EXPECTED_WHOLE_VERDICT.json','EXPECTED_ROOT_WHOLE_REVIEW.json']:
    demand(read(H/n)==read(V1/n),'Entire unchanged scientific/draft byte body '+n)
# Filename correlation: the overlay's concrete source input exists and matches
# both the original_native guard and its exact prepared binding.
overlay_calls=re.findall(r"g\.load\(g\.A/'(snapshot_manifest[^']*\.json)'\)",new['integrate_reviewed_partial.py'].decode())
guard_calls=re.findall(r"(?:snapshot=load|snap=load)\(A/'(snapshot_manifest[^']*\.json)'\)",new['pr43_guards.py'].decode())
demand(overlay_calls==['snapshot_manifest.json'],'Exact actual overlay snapshot input')
demand(guard_calls==['snapshot_manifest.json','snapshot_manifest.json'],'Both guard original snapshot references agree')
snapshot=json.loads(read(A/overlay_calls[0]));demand(snapshot['schema']=='pr43-root-readonly-original-snapshot/v1' and len(snapshot['files'])==16 and len(snapshot['changed_paths'])==17,'Actual original snapshot schema16/17')
old_overlay=re.findall(r"g\.load\(g\.A/'(snapshot_manifest[^']*\.json)'\)",old['integrate_reviewed_partial.py'].decode())
demand(old_overlay==['snapshot_manifest_v2.json'] and not (A/old_overlay[0]).exists(),'Old defect reproduced by source correlation only, no helper execution')
for label,source in [('old_filename',new['integrate_reviewed_partial.py'].decode().replace('snapshot_manifest.json','snapshot_manifest_v2.json')),('invented_filename',new['integrate_reviewed_partial.py'].decode().replace('snapshot_manifest.json','invented_snapshot_manifest.json'))]:
    names=re.findall(r"g\.load\(g\.A/'([^']*snapshot[^']*\.json)'\)",source)
    demand(names!=overlay_calls or not all((A/name).is_file() for name in names),'Reject filename correlation mutant '+label);negatives.append(label)
# Scope correlation: compare literal dictionaries' source operands independently.
def scope(source,prefix):
    pattern=re.escape(prefix)+r"[^\n]*scope='([^']*)'"
    values=re.findall(pattern,source)
    demand(len(values)==1,'Exactly one literal scope assignment '+prefix)
    return values[0]
expected_scope=scope(new['pr43_guards.py'].decode(),'expected.update(')
written_scope=scope(new['state_mirror_reconciliation.py'].decode(),'proposal.update(')
demand(expected_scope==written_scope=='Incremental present accepted primary PR43 source-status correction; original0/5, no new proof turn or historical reconstruction.','Writer/guard complete literal scope equality')
demand(scope(old['state_mirror_reconciliation.py'].decode(),'proposal.update(')!=expected_scope,'Old defect reproduced as exact scope mismatch without execution')
for label,value in [('extra_semicolon',written_scope.replace('PR43 ','PR43; ',1)),('trailing_whitespace',written_scope+' '),('invented_turn',written_scope.replace('original0/5','original1/5')),('wrong_prior_status',written_scope.replace('source-status correction','new full resolution'))]:
    demand(value!=expected_scope,'Reject full scope mutant '+label);negatives.append(label)
inp=json.loads(read(H/'INPUT_BINDINGS.json'));oldinp=json.loads(read(V1/'INPUT_BINDINGS.json'))
operator=A/'capture_root_final_operation_v2.py';raw=read(operator);ref={'path':operator.relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw)}
demand(len(raw)==5113 and sha(raw)=='9376c9c2d972f3ae4950ddb6b46300c2cd1cc36db89bc6ced6627fe8801e71a4','Actual separately authored ROOT V2 source')
older=read(A/'capture_root_final_operation.py')
demand(raw==older.replace(b"A / 'acceptance_preparation_family'",b"A / 'acceptance_preparation_family_v2'",1),'Independent entire ROOT operator one-parent-literal delta')
expected=copy.deepcopy(oldinp);expected['pins'].pop('capture_root_final_operation.py');expected['pins']['capture_root_final_operation_v2.py']=ref;expected['root_capture_operator']=ref
demand(typed(inp,expected),'Entire typed INPUT differs only by exact two operator references')
draft=json.loads(read(H/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json'))
for key in ['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post']:
    demand(draft[key] is None,'Future actual ROOT reference stays null '+key)
for key in ['root_full_current_read_completed','root_full_whole_read_completed','root_acceptance_source_review_completed','independent_whole_current_pass','root_actual_PR42_predecessor_read_completed']:
    demand(draft[key] is False,'No future ROOT completion flag '+key)
for key in ['previous_mirror','previous_post','previous_root_post']:
    demand(inp['required_future_PR42_predecessor'][key] is None,'No fabricated actual42 handoff '+key)
refs=json.loads(read(H/'V1_SOURCE_REFERENCES.json'));demand(refs['files_count_including_literal_self']==len(refs['files'])==109,'All108+self old files individually pinned')
for z in refs['files']:
    p=R/z['path'];b=read(p);demand(len(b)==z['bytes'] and sha(b)==z['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'Whole old source member and permission preserved '+z['path'])
demand(sha(read(V1/'PREPARATION_MANIFEST.json'))=='4161032794d175f8e0cfc3b62b3d1567f172ca93abe590f43ef81576d6cd20f9','Old closure unchanged after new source authoring')
for mode in range(4096):demand((mode==0o444)==(mode in {0o444}),'Independent literal permission guard '+oct(mode))
private=H/'OWN_PRIVATE_MODE_PROBES';private.mkdir(exist_ok=False);observations=[]
for mode in [0o444,0o1444,0o2444,0o4444,0o644,0o777]:
    p=private/('mode_'+oct(mode));p.write_bytes(b'Own V2 mode probe before closure.\n');p.chmod(mode)
    actual=stat.S_IMODE(p.stat().st_mode);demand(actual==mode,'Genuine V2 filesystem special-mode observation '+oct(mode));observations.append({'path':p.relative_to(H).as_posix(),'observed_mode_before_closure':actual,'accepted_by_independent_literal_predicate':actual==0o444})
status=json.loads(read(H/'SOURCE_STATUS.json'))
# Clear copied V1 own-check/closure metadata until actual V2 checks and closure.
status.update(own_AST_only_syntax_checked_no_production_bytecode=None,own_control_demands=len(checks),actual_private_mode_observations_historical_before_closure=True,closed_source_all_files_literal0444=None,closure_parent_records_after_complete_capture=False)
(H/'SOURCE_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
record={'schema':'pr43-independent-adjacent-two-defect-source-controls/v2','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_child_pid':os.getpid(),'status':'PASS_SOURCE_ONLY_CORRELATIONS_AND_FULL_DELTA','checks':len(checks),'check_labels':checks,'negative_correlations':negatives,'permission_modes_checked':4096,'actual_V2_private_mode_observations':observations,'V1_original_nonexistent_snapshot_detected_without_execution':True,'V1_original_scope_mismatch_detected_without_execution':True,'five_production_delta_exactly_two_tokens':True,'all_original108_plus_self_unchanged':True,'all_other_scientific_and_draft_bytes_unchanged':True,'production_helpers_imported_compiled_executed':False,'V1_source_PASS_transferred':False,'future_ROOT_or_PR42_approval_claimed':False,'new_substantive_attempts':0,'audit_turns':0}
(H/'OWN_CONTROL_RESULTS.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:v for k,v in record.items() if k!='check_labels'}))
