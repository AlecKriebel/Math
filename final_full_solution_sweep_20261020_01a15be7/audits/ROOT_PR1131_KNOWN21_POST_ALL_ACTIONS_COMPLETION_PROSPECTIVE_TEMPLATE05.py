"""Inactive completion recipe21; bind all three ROOT pins only after actual four-action success."""
from pathlib import Path
import json,hashlib,base64,datetime,os
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
P=R/'audits/pr1131_30005455';E=P/'known23592692_operations21_preparation01'
D=P/'root_actual21_known23592692_actions01';RT=P/'operations19/runtime'
ACT=P/'root_actual21_known23592692_activation01';AUTH=P/'known23592692_operations21_authority01'
ID=23592692;CONCEPT=23592691;OWNER=1789874
CONTRACT_SHA=ACTUAL21_CONTRACT_SHA_LITERAL
SOURCE21_SHA=ACTUAL21_SOURCE_MANIFEST_SHA_LITERAL
ENTRY21_SHA=ACTUAL21_ENTRY_SHA_LITERAL
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda v:json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)),'bytes':len(b),'sha256':H(b)}
def exact_file(p,h):
 b=p.read_bytes();assert H(b)==h;return b
def utc(s):
 t=datetime.datetime.fromisoformat(s.replace('Z','+00:00'));assert t.tzinfo is not None and t.utcoffset()==datetime.timedelta(0);return t
contractp=AUTH/'ROOT_EXECUTION_ADOPTION21.json'
contract=json.loads(exact_file(contractp,CONTRACT_SHA))
assert contract['schema']=='ROOT-known23592692-execution21-1' and contract['id']==ID
for k in ['approved_for_actions','new_whole21_review_adopted','full_original_known_create_and_six_history_accepted','old_source19_20_joint_science_reused_unchanged','known_create_only','future_create_allowance_zero']:
 assert contract[k]is True
assert contract['source21_sha256']==SOURCE21_SHA and contract['entry21_sha256']==ENTRY21_SHA
exact_file(E/'source21/SOURCE_MANIFEST21.json',SOURCE21_SHA)
entryraw=exact_file(E/'entry21.py',ENTRY21_SHA)
controllerraw=exact_file(E/'native_step21.py',contract['native_controller21_sha256'])
parent_templatep=R/'audits/ROOT_ACTUAL21_KNOWN_ONLY_SEPARATE_ACTION_FULL_NATIVE_PARENT_PROSPECTIVE_TEMPLATE03.py'
exact_file(parent_templatep,'0cd02ddf5cc23928aed3e2fc6ac98904512bd40369b25d01522902af33093771')
source=json.loads((E/'source21/SOURCE_MANIFEST21.json').read_bytes())
assert set(q.name for q in(E/'source21').iterdir())==set(source)|{'SOURCE_MANIFEST21.json'}
for name,spec in source.items():
 b=(E/'source21'/name).read_bytes();assert spec=={'bytes':len(b),'sha256':H(b)}
data=json.loads((E/'source21/DATA_CONTRACT21.json').read_bytes())
assert data['id']==ID and data['concept']==CONCEPT and data['owner']==OWNER
assert len(data['historical_runtime'])==6
evidence=[pin(contractp),pin(E/'source21/SOURCE_MANIFEST21.json'),pin(E/'entry21.py')]
for name,spec in data['historical_runtime'].items():
 b=(RT/name).read_bytes();assert len(b)==spec['bytes']and H(b)==spec['sha256'];evidence.append(pin(RT/name))
firstp=Path(data['first_response']['path']);first=firstp.read_bytes()
assert len(first)==data['first_response']['bytes']and H(first)==data['first_response']['sha256']=='509e46d778614c1cf7ec0709cd75b571333ee5814927b53a123f2eaa596eddff'
custodyp=P/'operations19/source/custody18.py';custodyraw=exact_file(custodyp,'a0890e56df45eb963a29b031d1f360a5cf16df86b1cd0f3a4a33fc245c12069c')
custody={'__file__':str(custodyp),'__name__':'ROOT_COMPLETION_KNOWN21_AUTHENTICATED_CUSTODY','_OPS18_VERIFIED':True}
exec(compile(custodyraw,str(custodyp),'exec',dont_inherit=True,optimize=0),custody)
initial=custody['loads'](first);legacy=initial['response']
assert initial['kind']=='create'and initial['requested_or_known_id']==ID
assert type(legacy['id'])is int and legacy['id']==ID and legacy['submitted']is False and legacy['files']==[]
assert legacy['conceptrecid']==str(CONCEPT) and legacy['owner']==OWNER
assert legacy['metadata']['prereserve_doi']['doi']=='10.5281/zenodo.'+str(ID)
evidence.append(pin(firstp))
known=json.loads((RT/'CREATE_RETURNED_KNOWN_ID.json').read_bytes());assert known['id']==ID
assert known['original_response']['pin']['sha256']==H(first)

expected_programs={'git':('/opt/homebrew/Cellar/git/2.38.2/bin/git','2caa5a792b58b0d09d3e0cba7034eeac4fc2a678812e583a8f68a6d2e07183e0'),'gh':('/opt/homebrew/Cellar/gh/2.85.0/bin/gh','91f6e182bce24da56581ab999088c55ae0216309af19bc6167bbc4396c3f4ea5'),'gws':('/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws','0f27b8b0815bf09cdf95da48d3c604f05ceb8f16bf5c9f0ba355b1f957cdd47e')}
actions=['stage-known','publish','verify-public','ledger'];parsed={};previous=None
for action in actions:
 expected_argv=[action,'--expected-pr-head','9601e1e768c94522bc8ad105db4dfae4770bad75','--deposit-id',str(ID),'--clearance-sha256',contract['ROOT19_sha256'],'--root21-clearance-sha256',contract['ROOT21_sha256'],'--compat20-clearance-sha256',contract['compatibility20_authority_sha256']]
 entryp=E/'entry21.py';helperp=E/'native_step21.py';helperh=contract['native_controller21_sha256']
 inner_program='from pathlib import Path;import hashlib;p=Path('+repr(str(entryp))+');b=p.read_bytes();\nif hashlib.sha256(b).hexdigest()!='+repr(ENTRY21_SHA)+':raise RuntimeError("entry21 changed")\nn={"__file__":str(p),"__name__":"checked_actual_known21"};exec(compile(b,str(p),"exec",dont_inherit=True,optimize=0),n);n["main"]('+repr(expected_argv)+')'
 expected_inner_command=['/opt/homebrew/bin/python3','-I','-S','-B','-c',inner_program]
 outer_program="from pathlib import Path;import hashlib;p=Path("+repr(str(helperp))+");b=p.read_bytes();assert hashlib.sha256(b).hexdigest()=="+repr(helperh)+";n={'__file__':str(p),'__name__':'ROOT_checked_actual_known21_helper'};exec(compile(b,str(p),'exec',dont_inherit=True,optimize=0),n);n['main'](['--action',"+repr(action)+",'--root-contract-sha256',"+repr(CONTRACT_SHA)+"])"
 expected_outer_command=['/opt/homebrew/bin/python3','-I','-S','-B','-c',outer_program]
 intent=json.loads((D/(action+'.intent.json')).read_bytes())
 ex=json.loads((D/(action+'.exit.json')).read_bytes())
 ob=(D/(action+'.stdout.bin')).read_bytes();eb=(D/(action+'.stderr.bin')).read_bytes()
 assert ex['returncode']==0 and ex['complete_native_return']is True and ex['error']is None and eb==b''
 assert ex['stdout']=={'bytes':len(ob),'sha256':H(ob)}and ex['stderr']=={'bytes':len(eb),'sha256':H(eb)}
 assert ex['native_command']==intent['native_command']==expected_inner_command and intent['attempt_limit']==1
 assert intent['argv']==expected_argv
 for interpretation in [intent['interpreter'],ex['interpreter']]:
  assert interpretation['path']=='/opt/homebrew/bin/python3'and Path(interpretation['resolved_path']).resolve()==Path('/opt/homebrew/bin/python3').resolve()
  assert interpretation['sha256']=='b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf'
 assert intent['known_id']==ID and intent['future_create_allowance']==0 and intent['ROOT_execution_sha256']==CONTRACT_SHA
 result=json.loads(ob);assert result==json.loads((D/(action+'.parsed.json')).read_bytes())
 parsed[action]=result
 evidence.extend(pin(D/(action+suffix))for suffix in ['.intent.json','.exit.json','.stdout.bin','.stderr.bin','.parsed.json'])
 outerp=ACT/('ROOT_'+action+'_ORIGINAL_PARENT_NATIVE.json');outer=json.loads(outerp.read_bytes())
 assert outer['returncode']==0 and outer['error']is None and outer['complete_native_return']is True and outer['successful_native_return']is True
 assert outer['stream_snapshot_may_be_incomplete_and_descendant_may_continue']is False
 assert outer['physical_raw_stream_custody_saved_before_parse']is True and outer['ROOT_contract_sha256']==CONTRACT_SHA
 assert outer['known_id']==ID and outer['future_create_allowance']==0 and outer['action']==action
 assert outer['helper_sha256']==contract['native_controller21_sha256']and outer['argv']==expected_outer_command
 assert outer['interpreter_sha256']=='b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf'
 outer_ob=base64.b64decode(outer['stdout_base64'],validate=True);outer_eb=base64.b64decode(outer['stderr_base64'],validate=True)
 assert outer_eb==b''
 for role,b in [('stdout',outer_ob),('stderr',outer_eb)]:
  q=outer['physical_streams'][role];path=Path(q['path']);assert path.parent==ACT and path.read_bytes()==b
  assert q['bytes_at_snapshot']==len(b)and q['sha256_at_snapshot']==H(b);evidence.append(pin(path))
 summary=json.loads(outer_ob)
 assert summary['action']==action and summary['known_id']==ID and summary['native_returncode']==0 and summary['automatic_next_action']is False
 assert summary['transport']==str(D)
 start=utc(outer['before']);end=utc(outer['after'])
 assert start<=utc(ex['started_at'])<=utc(ex['finished_at'])<=end and(previous is None or previous<=start)
 previous=end
 envpin=outer['native_environment_preflight'];envp=Path(envpin['path']);raw=envp.read_bytes()
 assert len(raw)==envpin['bytes']and H(raw)==envpin['sha256'];env=json.loads(raw)
 assert env['at']==outer['before']and env['action']==action and env['ROOT_contract_sha256']==CONTRACT_SHA
 assert env['native_command']==outer['argv']and env['effective_PATH']==outer['effective_PATH']
 assert env['resolved_native_programs']==outer['resolved_native_programs']and env['same_environment_supplied_before_helper_preparation']is True
 for name,(expected_path,expected_hash)in expected_programs.items():
  v=env['resolved_native_programs'][name]
  assert Path(v['resolved_path']).resolve()==Path(expected_path).resolve()and v['sha256']==expected_hash
 evidence.extend([pin(outerp),pin(envp)])

doi='10.5281/zenodo.'+str(ID);url='https://zenodo.org/records/'+str(ID)
assert parsed['stage-known']['id']==parsed['publish']['id']==ID
assert parsed['stage-known']['state']=='ready_to_publish'and parsed['publish']['state']=='published'
public=parsed['verify-public'];ledger=parsed['ledger']
assert public['record']==ID and public['doi']==doi and public['metadata_verified']is True
assert public['doi_status']==200 and public['doi_destination']==url
expected=[{'name':'finite-warm-thresholds.pdf','bytes':91613,'sha256':'42c5c632de7e942df6b7c407fb95d877a165281f215e4aa7d1dfa862b08b2157','md5':'845715d7fffb5aba43baddb039692933'},{'name':'finite-warm-thresholds-source-and-verification.zip','bytes':211840,'sha256':'e92f6fa13245686525a0dd8fc4c5327bd03e58a1f02ae7dcae918668c16c5fee','md5':'513e0c50bc16dfe669473fb83695dbca'}]
for payload in expected:
 local_payload=(P/'operations/proposed/preprint'/payload['name']).read_bytes()
 assert len(local_payload)==payload['bytes']and H(local_payload)==payload['sha256']and hashlib.md5(local_payload).hexdigest()==payload['md5']
assert sorted(public['files'],key=lambda x:x['name'])==sorted(expected,key=lambda x:x['name'])
assert public['native_target_verified']['record']==ID and public['native_target_verified']['concept']==CONCEPT and public['native_target_verified']['owner']==OWNER
assert ledger['record']==ID and ledger['row']==287 and ledger['verified']is True and type(ledger['new_row'])is bool
certs={}
for name in ['RESUME_STAGE_VERIFIED.json','ZENODO_STAGE_VERIFIED.json','ZENODO_PUBLISH_VERIFIED.json','LEDGER_VERIFIED.json']:
 p=RT/name;v=json.loads(p.read_bytes());assert v['certification_approval_sha256']==data['ROOT19_sha256']
 provenance=v['additional_source21_policy']
 assert provenance['source21_sha256']==SOURCE21_SHA and provenance['entry21_sha256']==ENTRY21_SHA
 assert provenance['ROOT21_sha256']==contract['ROOT21_sha256']and provenance['compatibility20_authority_sha256']==contract['compatibility20_authority_sha256']
 assert provenance['known_id']==ID and provenance['first_return_sha256']==H(first)
 certs[name]=v;evidence.append(pin(p))
lv=certs['LEDGER_VERIFIED.json']
assert lv['row']==287 and lv['record']==ID and lv['read_back_exact']is True and lv['unique_target_family']is True and lv['all_other_rows_and_full_raw_metadata_preserved']is True
assert type(lv['new_row'])is bool and lv['new_row']is ledger['new_row']
append_new=ledger['new_row'];append_names=['LEDGER_APPEND_INTENT.json','LEDGER_APPEND_RESPONSE.json','LEDGER_APPEND_ACKNOWLEDGED.json']
if append_new:
 assert all((RT/name).is_file()for name in append_names)
 append_intent,append_response,append_ack=[json.loads((RT/name).read_bytes())for name in append_names]
 assert append_intent['record']==ID and append_ack['record']==ID
 assert append_intent['before_rows']==286 and len(append_intent['before_snapshot']['values'])==286
 assert append_intent['values']==lv['values']and append_intent['operation']==append_ack['operation']=='spreadsheets.batchUpdate.appendCells'
 assert append_intent['spreadsheet_id']==append_ack['spreadsheet_id']==ledger['spreadsheet_id']
 assert append_intent['sheet_id']==append_ack['sheet_id']==ledger['sheet_id']
 assert append_intent['request']=={'requests':[{'appendCells':{'sheetId':ledger['sheet_id'],'rows':[{'values':[{'userEnteredValue':{'stringValue':cell}}for cell in lv['values']]}],'fields':'userEnteredValue'}}],'includeSpreadsheetInResponse':True,'responseIncludeGridData':False}
 evidence.extend(pin(RT/name)for name in append_names)
else:
 assert not any((RT/name).exists()for name in append_names),'Existing literal NOOP must not conceal an unexplained own append history'

statep=Path('/Users/alec/Documents/Math/.zenodo-state/fde2539c673adf9f640aa7c1-production.json')
state=json.loads(statep.read_bytes())
assert state['id']==ID and state['environment']=='production'and state['manifest']==str(P/'operations/proposed/preprint/zenodo-deposit.json')
assert sum(q.name=='WRITE_stage_create_INTENT.json'for q in RT.iterdir())==1
assert len(list(RT.glob('WRITE_stage_upload_*_INTENT.json')))==2
assert (RT/'WRITE_stage_update_INTENT.json').is_file()and (RT/'WRITE_publish_publish_INTENT.json').is_file()
n={'__file__':str(E/'entry21.py'),'__name__':'ROOT_FINAL1131_KNOWN21_LOCAL_CHECK'}
exec(compile(entryraw,str(E/'entry21.py'),'exec',dont_inherit=True,optimize=0),n)
argv=['ledger','--expected-pr-head','9601e1e768c94522bc8ad105db4dfae4770bad75','--deposit-id',str(ID),'--clearance-sha256',data['ROOT19_sha256'],'--root21-clearance-sha256',contract['ROOT21_sha256'],'--compat20-clearance-sha256',contract['compatibility20_authority_sha256']]
m,base_argv,policy,guard=n['prepare'](argv)
assert base_argv==['ledger','--expected-pr-head','9601e1e768c94522bc8ad105db4dfae4770bad75','--deposit-id',str(ID),'--clearance-sha256',data['ROOT19_sha256']]
args=m.argparse.Namespace(action='ledger',expected_pr_head='9601e1e768c94522bc8ad105db4dfae4770bad75',deposit_id=ID,clearance_sha256=data['ROOT19_sha256'],operations_sha256=data['source19_sha256'])
m.bind_runtime();m.ACTION_ARGS=args;m.ACTION='ledger';m.bind_state();assert guard.known(ID)==ID
m.state_exact(ID);m.runtime_exact();m.local_context(args,'ledger');policy.check()
if append_new:
 assert append_ack['request_sha256']==m.c.digest(append_intent['request'])and append_ack['response_sha256']==m.c.digest(append_response)
 assert append_intent['before_sha256']==m.c.digest(append_intent['before_snapshot']['values'])
 guard.snapshot(append_intent['before_snapshot'],ID,'ledger');m.SHEET_POLICY.append_response(append_response,append_intent['before_snapshot'])
checks={k:True for k in ['all_four_separate_known21_native_actions_complete','sole_original_known_create_no_second_record','all_six_original_history_files_preserved','same_canonical_manifest_truthful_known_state','phase_specific_one_use_mutation_authorization','fresh_final_native_metadata_and_public_payloads_verified','DOI200_exact_destination','unique_ledger287_fullprefix43','finalsource21_base19_20_runtime_certificates_reverified','merged_PR_final_head_verified_at_every_action']}
v={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':1131,'problem_id':'30005455','title':'A sharp forest bound and an improved whisker bound for finite WARM graphs','doi':doi,'record':ID,'concept':CONCEPT,'owner':OWNER,'url':url,'complete':True,'merge_commit':'67915a3df87d3bdd19be74ac04b1a39fd0ce89f3','integrated_head':'9601e1e768c94522bc8ad105db4dfae4770bad75','ledger_row':287,'ledger_new_row':append_new,'ledger_new_four_literal_cells':lv['values'],'canonical_manifest':str((P/'operations/proposed/preprint/zenodo-deposit.json').relative_to(R)),'canonical_manifest_sha256':'0ca12e07eee0ed88da4f94b82a2404eed4341aaa1f08f9100ecb630014fed6fe','qualified_theorem':'Finite simple undirected loopless WARM graphs; fixed positive integer initial counts. Arbitrary positive vertex rates: surviving edges form a forest for alpha>4/3, strict sharp via triangle. Equal rates: surviving components have diameter at most3 for alpha>=17/4. Weighted odd-cycle instability alpha>sec^2(pi/(2m)).','scope_limits':'No stochastic equality alpha=4/3, sharp whisker interval, infinite graphs or arbitrary real/zero counts claim. Published stochastic support/convergence and earlier bounds credited.','priority':'Two independent bounded primary-source audits found no earlier exact universal improved bounds in inspected sources. No exhaustive worldwide priority or historical firstness certification.','ai_and_preprint_disclosures':'Extensive AI research, proof development, computation, literature investigation, manuscript preparation and adversarial auditing. Unrefereed preprint, no formal independent human peer review or proof-assistant certification.','actual_effect_counts':{'new_deposition_POST':1,'PDF_PUT':1,'source_ZIP_PUT':1,'metadata_PUT':1,'publication_POST':1,'atomic_ledger_append':int(append_new)},'public_download_payloads':expected,'doi_destination':url,'required_native_checks':checks,'scientific_and_base_whole_review_adoption':pin(P/'ROOT_FINAL_JOINT_WHOLE20_SCIENTIFIC_SOURCE_AND_ACTION_REVIEW_ADOPTION.json'),'actual_ROOT_execution_adoption':pin(contractp),'original_known_create_fact':pin(RT/'CREATE_RETURNED_KNOWN_ID.json'),'known21_source_manifest':pin(E/'source21/SOURCE_MANIFEST21.json'),'evidence':evidence,'history_limits':'Earlier pre-create failures and the consumed exact missing-parent reconstruction remain preserved. The sole actual create returned known23592692 then stopped because canonical languages and UI languages were both absent. Its complete tagged first response and all six original runtime files are retained unchanged. Source21 is explicitly modified execution policy, independently reviewed and separately adopted: exact authenticated same-buffer transformations, narrow absent-language UI projection, exact historical predicate exception, exclusive truthful known-state installation, permanent create prohibition and phase-specific one-use write capabilities. No unknown write outcome, retry or second record is authorized. Old Source20 completion recipe and stage action are superseded. Failed models, original custody and bounded review limitations remain recorded.','no_GitHub_release_or_duplicate_record_created':True,'overall_percent':97}
out=R/'PR1131_PUBLICATION_VERIFICATION.json'
with out.open('x')as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps({'complete':True,'path':str(out),'sha256':H(out.read_bytes()),'doi':doi,'record':ID,'ledger_row':287}))
