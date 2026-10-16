#!/usr/bin/env python3
"""Independent contract models and actual private filesystem fixtures; no candidate load."""
import copy
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat

P=Path(__file__).resolve().parent;A=P.parent;R=A.parents[2];V=A/'acceptance_preparation_family_v2'
SHA=lambda b:hashlib.sha256(b).hexdigest()
CHECKS=[]
HEAD='292b95ca601f166e6d246e609cf7ed5ca5653e25'
def require(value):
    if not value:raise ValueError('Independent specification rejected fixture')
def same(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
def check(label,operation,expect,kind):
    try:operation();got=True
    except (ValueError,KeyError,TypeError,StopIteration):got=False
    require(got is expect)
    CHECKS.append({'name':label,'observed_admission':got,'expected_admission':expect,'kind':kind,'status':'PASS_OWN_MODEL_OR_FIXTURE'})
def clock(value):
    require(type(value) is str and value and value==value.strip())
    try:c=dt.datetime.fromisoformat(value[:-1]+'+00:00' if value.endswith('Z') else value)
    except (TypeError,ValueError):raise ValueError('bad clock')
    require(c.tzinfo is not None and c.utcoffset()==dt.timedelta(0));return c
def ref(value):
    require(type(value) is dict and set(value)=={'path','bytes','sha256'})
    require(type(value['bytes']) is int and value['bytes']>=0)
    n=value['path'];require(type(n) is str and n and '\\' not in n and '\0' not in n)
    q=PurePosixPath(n);require(not q.is_absolute() and q.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(q.parts))
    require(type(value['sha256']) is str and re.fullmatch('[0-9a-f]{64}',value['sha256']))
def derive(before,remote,when):
    require(type(before) is dict and type(before['items']) is list and len(before['items'])==180)
    numbers=[z['number'] for z in before['items']]
    require(all(type(z) is int for z in numbers) and len(set(numbers))==180 and numbers.count(41)==1)
    require(type(before['completed_count']) is int and before['completed_count']==30 and sum(z.get('stage')=='complete' for z in before['items'])==30)
    for k,v in {'number':41,'state':'MERGED','isDraft':False,'headRefOid':HEAD,'headRefName':'dot/math-9700035','baseRefName':'main'}.items():require(same(remote[k],v))
    require(type(remote['mergeCommit']) is dict and set(remote['mergeCommit'])=={'oid'} and type(remote['mergeCommit']['oid']) is str and re.fullmatch('[0-9a-f]{40}',remote['mergeCommit']['oid']))
    require(clock(remote['mergedAt'])<=clock(when)<=dt.datetime.now(dt.timezone.utc))
    after=copy.deepcopy(before);item=next(z for z in after['items'] if z['number']==41)
    require(item.get('stage')!='complete')
    item.update(stage='complete',outcome='unsolved_accepted_partial',queue_status='unsolved',audited_head=HEAD,merge_commit=remote['mergeCommit']['oid'],merged_at=remote['mergedAt'],workflow_completion_estimate_percent=100,original_attempts='2/5',new_substantive_attempts=0,cumulative_attempts='2/5',paper_or_new_doi_or_tracker=False)
    require(sum(z.get('stage')=='complete' for z in after['items'])==31)
    after.update(updated_at_utc=when,last_checkpoint_utc=when,completed_count=31,program_completion_estimate_percent=31/180*100,completion_estimate_percent=31/180*100,current_pr=42)
    return after
def put(name,obj):
    target=P/name;require(not target.exists());target.write_text(json.dumps(obj,indent=2)+'\n')

# Complete actual current native inventory is only a dated observed before fixture.
# Every hypothetical after value is explicitly artificial, never future runtime authority.
before_path=R/'draft_pr_publication_program_20260930/inventory.json'
before_raw=before_path.read_bytes();before=json.loads(before_raw)
before_ref={'path':before_path.relative_to(R).as_posix(),'bytes':len(before_raw),'sha256':SHA(before_raw),'worktree_mode':stat.S_IMODE(before_path.stat().st_mode)}
remote={'number':41,'state':'MERGED','isDraft':False,'headRefOid':HEAD,'headRefName':'dot/math-9700035','baseRefName':'main','mergeCommit':{'oid':'a'*40},'mergedAt':'2026-10-02T23:00:00Z'}
when='2026-10-02T23:00:05+00:00'
good=derive(before,remote,when)
put('INVENTORY_FIXTURE_BEFORE.json',before)
put('INVENTORY_FIXTURE_EXPECTED_ARTIFICIAL_AFTER.json',good)
check('S1_full180_typed_baseline',lambda:require(same(derive(before,remote,when),good)),True,'complete inventory model')
mutants=[('program100',lambda z:z.update(program_completion_estimate_percent=100)),('completion100',lambda z:z.update(completion_estimate_percent=100)),('programnull',lambda z:z.update(program_completion_estimate_percent=None)),('programbool',lambda z:z.update(program_completion_estimate_percent=True)),('missing_program',lambda z:z.pop('program_completion_estimate_percent')),('root_clock_missing',lambda z:z.pop('updated_at_utc')),('root_clock_null',lambda z:z.update(updated_at_utc=None)),('clock_invalid',lambda z:z.update(last_checkpoint_utc='bad')),('clock_different_valid_UTC',lambda z:z.update(updated_at_utc='2026-10-02T23:00:06Z')),('extra_authority',lambda z:z.update(human_peer_review_asserted=True)),('bool_completed',lambda z:z.update(completed_count=True)),('float_completed',lambda z:z.update(completed_count=31.0)),('wrong_current_pr',lambda z:z.update(current_pr=41)),('changed_unselected',lambda z:z['items'][0].update(unrequested=True)),('reordered_items',lambda z:z['items'].reverse())]
for label,mutate in mutants:
    wrong=copy.deepcopy(good);mutate(wrong)
    check('S1_reject_'+label,lambda w=wrong:require(same(w,good)),False,'complete typed inventory equality')
for label,value in [('null',None),('bool',False),('float',100.0),('wrong',99)]:
    wrong=copy.deepcopy(good);next(z for z in wrong['items'] if z['number']==41)['workflow_completion_estimate_percent']=value
    check('S1_reject_workflow_'+label,lambda w=wrong:require(same(w,good)),False,'complete typed selected workflow')
for label,remote_change,final_clock in [('merge_after_final',{'mergedAt':'2026-10-02T23:00:06Z'},when),('future_final',{},'2999-01-01T00:00:00Z'),('naive_final',{},'2026-10-02T23:00:05'),('nonUTC_final',{},'2026-10-02T16:00:05-07:00'),('padded_final',{},' '+when),('bool_merge_oid',{'mergeCommit':{'oid':True}},when),('extra_merge_key',{'mergeCommit':{'oid':'a'*40,'url':'forged'}},when),('bool_draft',{'isDraft':0},when)]:
    altered=copy.deepcopy(remote);altered.update(remote_change)
    check('S1_clock_remote_reject_'+label,lambda r=altered,c=final_clock:derive(before,r,c),False,'constructor typed actual merge/clock domain')

scope=json.loads((V/'SCIENTIFIC_SCOPE.json').read_bytes())
common=['preparation_manifest_sha256','final_plan','final_plan_sha256','final_receipt','final_receipt_sha256','final_manifest','final_manifest_sha256','reconciliation_capture','reconciliation_capture_sha256','previous_mirror','previous_mirror_sha256','previous_post','previous_post_sha256','fresh_preimage','fresh_preimage_sha256','root_bindings','root_bindings_sha256']
pins={name:('b'*64 if name.endswith('sha256') else 'artificial/'+name+'.json') for name in common}
science={'full_problem_solved':False,'partial_valid':True,'novelty_claimed':False,'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'verification_attempts_added':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'paper_or_new_doi_or_tracker':False}
accept={'schema':'pr41-accepted-qualified-conditional-partial/v1','utc':when,**science,**pins,'pr':41,'id':9700035,'problem_id':9700035,'problem_number':'AMR-096-0035','queue_status':'unsolved','outcome':'unsolved_accepted_partial_merged','original_head':HEAD,'original_base':'c6975ca76f9f667f1250ba403d0e6da2aafe14d0','merge_commit':'a'*40,'merge_tree':'c'*40,'merge_parents':['d'*40,HEAD],'merged_at':remote['mergedAt'],'remote_state':'MERGED','remote_isDraft':False,'canonical_scientific_artifact_sha256':'464af6d259f9275ca9f0056567f5301bc228465fa0ddaf2faece0920cab6bd7c','source_record_sha256':'d86ee1dc749ef5b9a0446109fb6f0278246cf3584f36aa70205b5bc6c683782f','original_ledger_sha256':'bd0a82165c3ac81f7a7d35ace164f20ecb87e6b73a9155815e4eecac655a2549','substantive_attempts_used':2,'substantive_attempt_limit':5,'native_historical_events_inferred':False,'historical_metadata_archival_only':True,'workflow_completion_estimate_percent':100,'full_resolution_completion_estimate_percent':0,'scientific_scope':scope}
audit={**copy.deepcopy(accept),'canonical_manifest_sha256':'e'*64,'canonical_manifest_entries':558}
check('S2_complete_canonical_baseline',lambda:require(same(copy.deepcopy(accept),accept)),True,'complete all-field artificial receipt')
check('S2_exact_audit_two_extensions',lambda:require(same(copy.deepcopy(audit),audit)),True,'complete all-field artificial audit')
for label,mutate in [('peer_review',lambda z:z.update(human_peer_review_asserted=True)),('solved',lambda z:z.update(solved=True)),('missing_null',lambda z:z.pop('current_model')),('bool_budget',lambda z:z.update(original_substantive_attempts=True)),('float_budget',lambda z:z.update(original_substantive_attempts=2.0)),('numeric_false',lambda z:z.update(full_problem_solved=0)),('nested_peer_review',lambda z:z['scientific_scope'].update(human_peer_review_asserted=True)),('wrong_merge',lambda z:z.update(merge_commit='f'*40)),('extra_reference_authority',lambda z:z.update(root_override=True)),('workflowfloat',lambda z:z.update(workflow_completion_estimate_percent=100.0))]:
    for kind,expected in [('canonical',accept),('audit',audit)]:
        wrong=copy.deepcopy(expected);mutate(wrong)
        check('S2_'+kind+'_reject_'+label,lambda w=wrong,e=expected:require(same(w,e)),False,'complete derived receipt schema/value/type')
check('S2_canonical_reject_audit_extensions',lambda:require(same(audit,accept)),False,'audit-only keyset distinction')
check('S2_audit_reject_missing_extensions',lambda:require(same(accept,audit)),False,'audit-only keyset distinction')
put('COMPLETE_ACCEPTANCE_FIXTURE_ARTIFICIAL.json',{'canonical':accept,'audit':audit,'fields_count':len(accept),'all_values_artificial_not_runtime_approval':True})

inputs=json.loads((V/'INPUT_BINDINGS.json').read_bytes())
whole_ref={k:inputs['whole_observed_only'][k] for k in ['path','bytes','sha256']}
root_ref=inputs['root_whole_observed']
root_expected=json.loads((V/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json').read_bytes())
root_expected.update(status='ROOT_APPROVED_CLOSED_WHOLE_EVIDENCE',created_utc=when,root_full_current_read_completed=True,root_full_whole_read_completed=True,independent_whole_current_pass=True,whole_manifest=whole_ref,root_whole_inspection=root_ref)
def root_guard(value):
    ref(value['whole_manifest']);ref(value['root_whole_inspection'])
    require(same(value,root_expected));require(clock(value['created_utc'])<=dt.datetime.now(dt.timezone.utc))
check('S2_ROOT_exact_completed_schema_fixture',lambda:root_guard(copy.deepcopy(root_expected)),True,'artificial typed ROOT fixture, never approval')
for label,mutate in [('extra_authority',lambda z:z.update(human_peer_review_asserted=True)),('missing_created',lambda z:z.pop('created_utc')),('false_rootflag',lambda z:z.update(root_full_current_read_completed=False)),('numeric_rootflag',lambda z:z.update(root_full_current_read_completed=1)),('extra_whole_reference',lambda z:z['whole_manifest'].update(full_problem_solved=True)),('extra_root_reference',lambda z:z['root_whole_inspection'].update(size=z['root_whole_inspection']['bytes'])),('bool_reference_bytes',lambda z:z['whole_manifest'].update(bytes=True)),('negative_reference_bytes',lambda z:z['whole_manifest'].update(bytes=-1)),('wrong_reference_hash',lambda z:z['whole_manifest'].update(sha256='bad')),('escaping_reference',lambda z:z['whole_manifest'].update(path='../escape.json'))]:
    wrong=copy.deepcopy(root_expected);mutate(wrong)
    check('S2_ROOT_reject_'+label,lambda w=wrong:root_guard(w),False,'complete ROOT schema and exact3-key reference domain')
put('ROOT_BINDING_FIXTURE_ARTIFICIAL.json',root_expected)

# Read real private file stat modes rather than merely masking invented integers.
fixture=P/'private_actual_mode_fixtures';fixture.mkdir(exist_ok=False)
mode_rows=[]
def frozen_file(q):
    require(q.is_file() and not q.is_symlink())
    require(stat.S_IMODE(q.stat().st_mode)==0o444)
for mode in [0o444,0o644,0o400,0o440,0o2444,0o4444,0o1444]:
    q=fixture/('mode_'+format(mode,'04o')+'.bin');q.write_bytes(b'Independent private permission fixture.\n');q.chmod(mode)
    observed=stat.S_IMODE(q.stat().st_mode);require(observed==mode)
    mode_rows.append({'path':q.relative_to(P).as_posix(),'bytes':len(q.read_bytes()),'sha256':SHA(q.read_bytes()),'actual_observed_permission_mode':observed,'actual_observed_mode_octal':format(observed,'04o')})
    check('S3_actual_file_mode_'+format(mode,'04o'),lambda p=q:frozen_file(p),mode==0o444,'actual private regular file stat.S_IMODE')
bundle=P/'private_actual_bundle_fixture';bundle.mkdir(exist_ok=False)
names=['PREPARATION_MANIFEST.json','member.json','FINAL_MANIFEST.json','ROOT_REVIEWED_SCOPE.json','ROOT_FINAL_RECONCILIATION.json','MANIFEST.json']
for n in names:(bundle/n).write_text('{}\n');(bundle/n).chmod(0o444)
def frozen_bundle():
    for n in names:frozen_file(bundle/n)
check('S3_actual_all_members_and_self_baseline',frozen_bundle,True,'actual bundle including all literal self names')
for n in names:
    q=bundle/n;unchanged=q.read_bytes();q.chmod(0o644)
    check('S3_actual_permission_only_reject_'+n,frozen_bundle,False,'actual member/self mode bound with unchanged bytes')
    require(q.read_bytes()==unchanged);q.chmod(0o444)
target=fixture/'mode_0444.bin';symlink=fixture/'transient_symlink';symlink.symlink_to(target.name)
check('S3_actual_symlink_rejected',lambda:frozen_file(symlink),False,'actual private symlink boundary')
symlink.unlink()
# Preserve the extra empty-directory fixture explicitly in this audit closure.
empty=bundle/'intentional_empty_extra_directory';empty.mkdir()
def exact_without_extra_dir():
    dirs={q.relative_to(bundle).as_posix() for q in bundle.rglob('*') if q.is_dir()}
    require(dirs==set())
check('topology_actual_extra_empty_directory_rejected',exact_without_extra_dir,False,'private exact topology expectation')

guard=(V/'pr41_guards.py').read_text();integration=(V/'integrate_reviewed_partial.py').read_text();mirror=(V/'state_mirror_reconciliation.py').read_text();post_source=(V/'verify_post_acceptance.py').read_text();sealer=(V/'seal_final_evidence.py').read_text()
for name,present in [('complete_inventory_constructor','def derive_inventory' in guard),('inventory_finalizer', 'g.derive_inventory(before_inv,observation,now)' in integration),('inventory_mirror',"inventory_guard(g.load(g.A/'integration_inventory_before.json'),inv,retained_remote,final['utc'])" in mirror),('inventory_post','g.equal(inventory,g.derive_inventory(' in post_source),('accepted_complete','require(equal(o,expected)' in guard),('ROOT_complete','Complete typed external ROOT bindings schema/value equality required' in guard),('references_exact',"set(obj)=={'path','bytes','sha256'}" in guard),('mode_full','stat.S_IMODE(regular(base,n).stat().st_mode)==0o444' in guard),('final_modes','a.final_manifest_sha256,2,frozen=True)' in guard),('preparation_modes',"manifest(HERE,'PREPARATION_MANIFEST.json',a.preparation_manifest_sha256,frozen=True)" in guard),('current_modes',"manifest(C,'MANIFEST.json',CURRENT_SHA,547,frozen=True)" in guard),('whole_modes',"frozen_files(w,authored+foreign,'FIRST_PARTY_MANIFEST.json')" in guard),('accepted_modes','frozen=True' in mirror),('sealer_after_freeze','count=2,frozen=True)' in sealer)]:
    check('source_callsite_'+name,lambda ok=present:require(ok),True,'full manual source review corroborated by literal occurrence')

result={'schema':'pr41-independent-v2-source-finite-contract-falsification/v1','status':'PASS_OWN_MODELS_AND_ACTUAL_PRIVATE_FILESYSTEM_FIXTURES','actual_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'checks_count':len(CHECKS),'checks':CHECKS,'full_canonical_acceptance_fixture_fields':len(accept),'before_inventory_dated_observation':before_ref,'actual_mode_rows_at_testing':mode_rows,'special_modes_were_actually_observed':True,'private_fixture_files_frozen0444_only_at_final_audit_closure':True,'intentional_empty_directories':['private_actual_bundle_fixture/intentional_empty_extra_directory'],'transient_symlink_removed_after_recorded_rejection':True,'models_and_after_receipts_are_artificial':True,'candidate_helpers_imported_compiled_or_executed':False,'future_runtime_PASS_claimed':False,'scientific_reexecution_claimed':False,'native_Git_remote_mutations':False}
put('FINITE_SPECIFICATION_RESULT.json',result)
print(json.dumps({k:result[k] for k in ['status','actual_pid','checks_count','full_canonical_acceptance_fixture_fields','special_modes_were_actually_observed','candidate_helpers_imported_compiled_or_executed','future_runtime_PASS_claimed']},indent=2))
