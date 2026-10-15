"""Second-review hostile controls; source-captured helpers, all transports mocked.
Fixture plumbing from round1 is reused only after independent complete source review.
New cases target different schema, stale-source, normalization and state boundaries.
"""
import copy,datetime,hashlib,io,json,os,shutil,subprocess,sys,types
from pathlib import Path
R=Path(__file__).absolute().parent; A=R.parent.parent
base=A/'reviews/whole_package_round1/operations_controls.py'
n={'__file__':str(base),'__name__':'fixture_plumbing_only'}
exec(compile(base.read_bytes(),str(base),'exec'),n)
# Every fixture and every fake receipt is redirected into round2's ignored tmp.
n['R']=R;n['LIVE']=A;n['T']=R/'tmp'/('FAKE_FIXTURE_OPT' if sys.flags.optimize else 'FAKE_FIXTURE_NORMAL')
T=n['T']
if T.exists():shutil.rmtree(T)
T.mkdir(parents=True,exist_ok=True)
F=n['Fixture'];DOI=n['DOI'];NOW=n['NOW'];jbytes=n['jbytes'];load=n['load']
checks=[]
REJECTIONS=(ValueError,OSError,subprocess.CalledProcessError,TypeError,KeyError)
def need(v,label):
 if not v:raise RuntimeError(label)
def ok(label,fn):
 fn();checks.append({'case':label,'outcome':'PASS'})
def reject(label,fn):
 try:fn()
 except REJECTIONS as e:
  checks.append({'case':label,'outcome':'REJECTED','exception':type(e).__name__});return
 raise RuntimeError('HOSTILE ACCEPTED: '+label)
def restore_case(f,label,path,mut):
 p=f.a/path;b=p.read_bytes();f.mutate_json(path,mut)
 try:reject(label,f.inputs)
 finally:p.write_bytes(b)
f=F();ok('legitimate_exact_fake_receipts_accepted',f.inputs)
for label,num,mut in [
 ('round1_chain_must_begin_at_null',1,lambda x:x.update(previous_report_sha256='f'*64)),
 ('round2_optional_bool_is_not_zero_count',2,lambda x:x.update(optional_findings=False)),
 ('round2_nonempty_findings_with_zero_counts',2,lambda x:x.update(findings=['unwaived'])),
 ('round2_gate_pin_cannot_be_omitted',2,lambda x:x['gate_bindings'].pop('PRIORITY_GATE_ACCEPTANCE.json')),
 ('round2_publication_extra_pin_is_not_exact_ten',2,lambda x:x['publication_files'].update(extra={'bytes':0,'sha256':'0'*64})),
 ('round2_nonUTC_completion',2,lambda x:x.update(completed_utc='2026-10-15T00:00:00-07:00')),
 ('round2_start_after_end',2,lambda x:x.update(started_utc=(NOW-datetime.timedelta(minutes=30)).isoformat())),
]:
 q=F();q.repin_report(num,mut);reject(label,q.inputs)
for label,path,mut in [
 ('accepted_extra_eleventh_file','ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x['files'].update(extra={'bytes':0,'sha256':'0'*64})),
 ('accepted_helper_missing_tracker','ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x['helper_sha256'].pop('record_tracker.py')),
 ('accepted_file_boolean_size','ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x['files']['requirements.txt'].update(bytes=True)),
 ('accepted_review_optional_unresolved','ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x['whole_package_review_rounds'][1].update(optional_findings=1)),
 ('accepted_report_path_traversal','ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x['whole_package_review_rounds'][1].update(report_path='reviews/../VERDICT.json')),
 ('final_acceptance_precedes_gate','PUBLICATION_FINAL_ACCEPTANCE.json',lambda x:x.update(created_utc=(NOW-datetime.timedelta(days=2)).isoformat())),
 ('receipt_wrong_environment','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x.update(environment='sandbox')),
 ('receipt_not_saved','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x.update(receipt_saved=False)),
 ('receipt_duplicate_files','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x.update(files=[x['files'][0],x['files'][0]])),
 ('receipt_file_extra_metadata_changes_exact_binding','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x['files'][0].update(md5='0'*32)),
 ('receipt_http_bool_is_not_200','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x['doi_resolution'].update(http_status=True)),
 ('receipt_naive_time','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x.update(verified_utc='2026-10-15T00:00:00')),
 ('benign_kit_normalization_requires_reconciliation','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x.update(metadata_normalizations=[{'field':'description','kind':'plain_text_html_entities'}])),
]:restore_case(f,label,path,mut)
for value in ['10.5281/zenodo.0','10.5281/zenodo.01','10.5281/zenodo.+1','10.5281/zenodo.1\n','10.5281/zenodo.1/','https://doi.org/'+DOI]:reject('invalid_doi_'+repr(value),lambda value=value:f.h.valid_doi(value))
inputs=f.inputs();validation=inputs['validation']
# Replace every source category after capture, with a harmless byte change.
for relative in ['ACCEPTED_PUBLICATION_INPUTS.json','PUBLICATION_FINAL_ACCEPTANCE.json','PRIORITY_GATE_ACCEPTANCE.json','record_tracker.py','ZENODO_POST_PUBLICATION_INSPECTION.json','reviews/fake2/VERDICT.json','publication/satoh_filtration_verification.zip']:
 p=f.a/relative;b=p.read_bytes();p.write_bytes(b+b'\n')
 reject('pre_dispatch_rehash_'+relative,lambda:f.h.recheck_sources(validation));p.write_bytes(b)
# Capture API reads must reject a linked parent as well as final symlinks.
linked=f.root/'linked-audit';linked.symlink_to(f.a,target_is_directory=True)
reject('regular_capture_linked_ancestor',lambda:f.h.regular_bytes(linked/'SCOPE_AND_SNAPSHOT.json'))
# A stale bytecode cache must not execute through the tracker dependency loader.
import importlib._bootstrap_external
p=f.a/'prepare_integration.py';s=p.stat();cached=f.a/'__pycache__'/('prepare_integration.'+sys.implementation.cache_tag+'.pyc');cached.parent.mkdir()
cached.write_bytes(importlib._bootstrap_external._code_to_timestamp_pyc(compile("raise RuntimeError('STALE BYTECODE EXECUTED')",str(p),'exec'),int(s.st_mtime),s.st_size))
ok('tracker_source_loader_ignores_matching_timestamp_stale_pyc',lambda:load(f.a/'record_tracker.py','round2_stale_cache_probe'))
# Exact metadata compatibility and a benign normalization accepted by the kit,
# then independently rejected above by current publication gates.
kit=load(A.parents[2]/'zenodo_deposit_tool/zenodo.py','round2_kit_no_main')
REJECTIONS=REJECTIONS+(kit.DepositError,)
metadata,files=kit.load_manifest(f.a/'publication/zenodo-deposit.json')
remote={'metadata':copy.deepcopy(metadata),'files':[{'filename':x['name'],'filesize':x['size'],'checksum':'md5:'+x['md5']}for x in files]}
ok('kit_exact_metadata_and_binary_md5_size',lambda:need(kit.verify(remote,metadata,files)==[],'metadata exactness'))
import html
remote['metadata']['description']=html.escape(metadata['description'],quote=False)
ok('kit_entity_escaping_is_explicit_normalization',lambda:need(kit.verify(remote,metadata,files)==[{'field':'description','kind':'plain_text_html_entities'}],'expected entity normalization'))
remote['metadata']['title']='altered';reject('kit_title_change_not_normalized',lambda:kit.verify(remote,metadata,files))
# Queue preservation includes CRLF, UTF-8, NUL unrelated bytes and no last newline.
row=inputs['snapshot']['queue_row'];cells=row.split('|');cells[8]=' queued ';cells[9]=' 0/5 ';cells[11]=' '
queue=b'prefix\x00\xff\r\n'+('|'.join(cells)+'\r\n').encode()+b'no-final-newline\xc3\xa9'
patched,patch=f.h.patch_queue(queue,DOI,row)
ok('queue_only_three_cells_with_binary_unselected_bytes',lambda:need(patched.startswith(b'prefix\x00\xff\r\n')and patched.endswith(b'no-final-newline\xc3\xa9')and patch['changed_cells']==['Status','Turns','Findings'],'queue byte loss'))
for label,mut in [('existing_findings',lambda c:c.__setitem__(11,' existing ')),('turns_changed',lambda c:c.__setitem__(9,' 1/5 ')),('source_cell_changed',lambda c:c.__setitem__(7,' 2019 '))]:
 c=cells.copy();mut(c);reject('queue_reject_'+label,lambda c=c:f.h.patch_queue('|'.join(c).encode(),DOI,row))
# Stale and malformed sticky intents must block even when DOI is absent.
for label,payload in [('wrong_schema',{'schema':'wrong'}),('wrong_row',None),('wrong_validation',None)]:
 q=F();ready=q.ready();q.final_gate('tracker',ready['publication_validation'])
 intent={'schema':'pr681-tracker-intent-v1','spreadsheet_id':q.tr.ID,'sheet_id':q.tr.GID,'doi':DOI,'row':ready['row'],'publication_validation':copy.deepcopy(ready['publication_validation'])}
 if payload is not None:intent=payload
 elif label=='wrong_row':intent['row']=ready['row'][:-1]
 else:intent['publication_validation']['deposit_metadata_sha256']='0'*64
 n['write'](q.a/'TRACKER_UNCONFIRMED.json',intent)
 reject('sticky_tracker_'+label,lambda:q.tr.append_once(ready));need(q.append_count==0,'intent failure dispatched')
q=F();ready=q.ready();q.final_gate('tracker',ready['publication_validation']);(q.a/'TRACKER_UNCONFIRMED.json').write_text('{malformed')
reject('sticky_tracker_malformed_json',lambda:q.tr.append_once(ready));need(q.append_count==0,'malformed dispatched')
q=F();ready=q.ready();q.final_gate('tracker',ready['publication_validation']);(q.a/'TRACKER_UNCONFIRMED.json').symlink_to(q.a/'SCOPE_AND_SNAPSHOT.json')
reject('sticky_tracker_symlink',lambda:q.tr.append_once(ready));need(q.append_count==0,'linked intent dispatched')
q=F();ready=q.ready();variant=ready['row'].copy();variant[2]='DOI: '+DOI+'/'
q.values.extend([variant,ready['row']]);reject('global_doi_uniqueness_includes_case_prefix_slash_variants',lambda:q.tr.append_once(ready));need(q.append_count==0,'duplicate dispatched')
q=F();ready=q.ready();variant=ready['row'].copy();variant[1]='unexpected-chat';q.values.append(variant)
reject('existing_doi_wrong_solution_chat_no_overwrite',lambda:q.tr.append_once(ready));need(q.append_count==0,'changed row dispatched')
# Intercept response after a mock append to challenge parser and sticky state.
for label,mutation in [('row_range_leading_zero',lambda x:x['updates'].update(updatedRange="'Math Puzzles'!A02:D02")),('count_boolean',lambda x:x['updates'].update(updatedRows=True)),('wrong_spreadsheet',lambda x:x.update(spreadsheetId='wrong')),('wrong_data',lambda x:x['updates']['updatedData'].update(values=[['wrong']]))]:
 q=F();ready=q.ready();q.final_gate('tracker',ready['publication_validation']);original=q.tr.call
 def call(resource,method,params,body=None,original=original,mutation=mutation):
  x=original(resource,method,params,body)
  if method=='append':mutation(x)
  return x
 q.tr.call=call;reject('append_response_'+label,lambda:q.tr.append_once(ready));need(q.append_count==1 and (q.a/'TRACKER_UNCONFIRMED.json').exists(),'missing sticky marker')
 # Exact remote row can be read back without a second dispatch.
 q.tr.call=original;receipt=q.tr.append_once(ready)
 ok('readonly_reconcile_'+label,lambda:need(q.append_count==1 and receipt['already_present'],'append repeated'))
# Full exact main in toy repository: real local Git objects and capsule replays;
# gh/gws and all Git network/push operations stay mocked by the audited adapter.
q=F();q.init_git();receipt=q.integration(False)
ok('complete_isolated_dry_integration_preserves_toy_refs_index_objects',lambda:need(q.git_snapshot()==q.git_initial and q.push_count==0,'toy git changed'))
prepared=json.loads((q.a/'INTEGRATION_PREPARED_RECEIPT.json').read_bytes())
ok('public_confirmation_observation_distinct_from_integration_time',lambda:need(prepared['publication_validation']['publication_confirmed_utc']!=prepared['integration_prepared_utc'],'time conflation'))
# Mutation of advertised main only on final pre-push read must stop dispatch.
q=F();q.init_git();q.final_gate('integration');real=q.h.remote_oid;count=[0]
def advancing(ref):
 if ref=='refs/heads/main':
  count[0]+=1
  if count[0]>=3:return 'f'*40
 return real(ref)
q.h.remote_oid=advancing
reject('fresh_main_advanced_at_final_dispatch_guard',lambda:q.integration(True));need(q.push_count==0 and not(q.a/'INTEGRATION_PUSH_INTENT.json').exists(),'stale main pushed')
# Unapproved transport and shallow repository exit before any object mutation.
q=F();q.init_git();reject('Git_writes_require_isolation',lambda:q.h.git('hash-object','-w','--stdin',input=b'x'))
for value in ['file:///tmp/remote.git','https://github.com/Other/Math.git','https://github.com/AlecKriebel/Math.git\nhttps://evil.invalid/repo']:
 original=q.h.git;q.h.git=lambda *a,input=None,value=value:value.encode()+b'\n'
 reject('unreviewed_transport_'+value,lambda:q.h.origin_url(push=True));q.h.git=original
# Execute successful ordinary mocked push, then stale/ambiguous dispatch blocks.
q=F();q.init_git();q.final_gate('integration');receipt=q.integration(True)
ok('ordinary_push_exact_url_durable_intent_and_second_readback',lambda:need(q.push_count==1 and receipt['pushed'] and receipt['remote_branch_head_verified'] and q.git_snapshot()==q.git_initial,'push control failed'))
reject('confirmed_push_cannot_redispatch',lambda:q.integration(True));need(q.push_count==1,'duplicate push')
q=F();q.init_git();q.final_gate('integration');q.push_mode='lost'
reject('lost_push_keeps_durable_intent',lambda:q.integration(True));reject('lost_push_no_automatic_redispatch',lambda:q.integration(True));need(q.push_count==1,'lost push retry')
print(json.dumps({'schema':'pr681-round2-operations-controls-v1','status':'PASS','mode':'optimized'if sys.flags.optimize else'normal','count':len(checks),'checks':checks,'fake_fixture_root':str(T),'fixture_plumbing_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'mock_dispatches':n['DISPATCHES'],'live_cloud_github_tracker_network_writes':0,'helper_sha256':json.loads((A/'WHOLE_PACKAGE_REVIEW_INPUTS.json').read_bytes())['helper_sha256']},indent=2,sort_keys=True))
