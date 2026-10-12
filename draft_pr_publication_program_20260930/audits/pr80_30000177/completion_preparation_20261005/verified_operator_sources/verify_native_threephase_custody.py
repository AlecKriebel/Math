"""Verify preserved actual evidence; no Git/service or scientific-file mutation."""
import datetime,gzip,hashlib,json,os,re,stat,sys
from pathlib import Path
if sys.flags.optimize:raise RuntimeError('Optimization forbidden')
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr80_30000177';F=Path(__file__).parent;E=F/'process_evidence'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 assert p.is_file() and not p.is_symlink() and p.resolve()==p and p.is_relative_to(R)
 b=p.read_bytes();return {'path':str(p.relative_to(R)),'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(p.stat().st_mode)}
def load(p):return json.loads(p.read_bytes())
groups={'actual_window':10,'native_merge':181,'merge_reconciliation':58,'native_accept':154,'native_checkpoint':668}
labels=['ROOT_actual_final_ACK_capacity_constraints','ROOT_actual_workspace_window_gate','ROOT_actual_renewed_ACK_capacity_constraints','ROOT_actual_workspace_window_gate_after_capacity_recovery','ROOT_actual_native_merge','ROOT_merge_reconciliation_fresh_GitHub_state','ROOT_actual_readonly_merge_reconciliation','ROOT_actual_native_accept','ROOT_actual_native_checkpoint']
for group,count in groups.items():
 actual={int(p.name[len(group)+1:]) for p in E.iterdir() if re.fullmatch(re.escape(group)+r'_\d+',p.name)}
 assert actual==set(range(1,count+1)),(group,actual,count)
 labels += [group+'_'+str(n) for n in range(1,count+1)]
assert len(labels)==len(set(labels))==1080
expected_fail={'ROOT_actual_workspace_window_gate':5097,'ROOT_actual_native_merge':11452}
records=[];raw_total=0;stored_total=0;source_total=0
for label in labels:
 d=E/label;x=load(d/'result.json');rq=load(d/'request.json');start=load(d/'process_started.json');end=load(d/'process_completed.json')
 assert x['label']==rq['label']==label and x['argv']==rq['argv'] and x['cwd']==rq['cwd']==str(R)
 assert x['retained_sources_prelaunch']==rq['retained_sources_prelaunch'] and x['requested_at_UTC']==rq['requested_at_UTC']
 assert x['actual_PID']==start['actual_PID']==end['actual_PID'] and x['exit_code']==end['exit_code']==(1 if label in expected_fail else 0)
 assert x['start_UTC']==start['start_UTC']==end['start_UTC'] and x['end_UTC']==end['end_UTC']
 if label in expected_fail:assert x['actual_PID']==expected_fail[label]
 streams={}
 for k in ('stdout','stderr'):
  p=Path(x[k+'_path']);assert p.parent==d and p.name==k+'.bin.gz';b=p.read_bytes();st=x[k+'_storage'];raw=gzip.decompress(b)
  assert st['storage_codec']=='gzip' and len(b)==st['storage_bytes'] and sha(b)==st['storage_sha256']
  assert len(raw)==x[k+'_bytes']==end[k+'_bytes']==st['logical_bytes'] and sha(raw)==x[k+'_sha256']==end[k+'_sha256']==st['logical_sha256']
  raw_total+=len(raw);stored_total+=len(b);streams[k]=raw
 sources=[]
 for item in x['retained_sources_prelaunch']:
  p=Path(item['retained_path']);assert p.parent==d;b=p.read_bytes();raw=gzip.decompress(b)
  assert item['storage_codec']=='gzip' and len(b)==item['storage_bytes'] and sha(b)==item['storage_sha256'] and len(raw)==item['bytes']==item['logical_bytes'] and sha(raw)==item['sha256']==item['logical_sha256']
  source_total+=len(raw);sources.append({'source_path':item['path'],'bytes':len(raw),'sha256':sha(raw)})
 if label.startswith(('native_merge_','native_accept_','native_checkpoint_')):
  required={'capture.py':'25eb431b1849b8abcfb44443a3792b7241a5ddd4d0d0399e7f712c46ac6ce626','native_integrate.py':'20d7995baf499388708b59becf1e5953760bf51d3f9042ac5fd36029f42f8cd8','ROOT_NATIVE_PLAN_WORKSPACE_REPAIR_V2_FINAL_20261005.json':'054843655c4a57844f49d1312a096f8bc000e8e93240f426aa6c7f677b2f9014','ROOT_EXCLUSIVE_PR80_PUBLICATION_INTEGRATION_ACK.json':'52ec5feb319771932f05569e28a3f1c8ba4b1e040e6b58ed0e8a2461e739c81a'}
  mapped={Path(item['source_path']).name:item['sha256'] for item in sources}
  assert all(mapped.get(k)==v for k,v in required.items())
 if label in expected_fail:
  assert not streams['stdout']
  expected=b'Insufficient durable capacity before mutation' if label.endswith('window_gate') else b'GitHub merged-head readback failed'
  assert expected in streams['stderr']
 records.append({'label':label,'actual_PID':x['actual_PID'],'exit_code':x['exit_code'],'start_UTC':x['start_UTC'],'end_UTC':x['end_UTC'],'result':pin(d/'result.json'),'stdout_bytes':x['stdout_bytes'],'stdout_sha256':x['stdout_sha256'],'stderr_bytes':x['stderr_bytes'],'stderr_sha256':x['stderr_sha256']})
receipts=[A/('ROOT_NATIVE_'+n+'_RECEIPT_20261004.json') for n in ('MERGE','ACCEPTANCE','CHECKPOINT')];values=[load(p) for p in receipts]
assert [x['commit'] for x in values]==['3804c6bbc5890529da417e9d9202b2be1c15330f','3e229327d4afeaef717b4103db54a52c19eb352b','bf5374af9e60e7343c848e1fac16ddc7bcf53319']
for p,label,value in zip(receipts,['ROOT_actual_readonly_merge_reconciliation','ROOT_actual_native_accept','ROOT_actual_native_checkpoint'],values):
 x=load(E/label/'result.json');assert x['exit_code']==0 and x['actual_PID']==value['actual_PID'] and gzip.decompress(Path(x['stdout_path']).read_bytes())==p.read_bytes()
 assert value['status']=='COMMITTED_PUSHED_INDEPENDENTLY_READ_BACK' and value['original_budget']=='1/5' and value['new_central_proof_search_turns']==0
 assert value['known_held_foreign_file_count']==19084 and value['index_empty'] is True
plan=load(A/'ROOT_NATIVE_PLAN_WORKSPACE_REPAIR_V2_FINAL_20261005.json');assert values[2]['committed_paths']==sorted(plan['checkpoint_files']) and len(values[2]['committed_paths'])==144
assert values[1]['parent']==values[0]['commit'] and values[2]['parent']==values[1]['commit']
assert values[0]['reconciliation']['failed_original_child_PID']==11452 and values[0]['reconciliation']['original_push_PID']==12002 and values[0]['reconciliation']['no_merge_push_commit_stage_or_PR_mutation_repeated'] is True
result={'schema':'pr80-preserved-native-operation-custody/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_verification_PID':os.getpid(),'status':'ALL1080_SELECTED_ACTUAL_CAPTURE_RECORDS_FULLSTREAM_SOURCE_LIFECYCLE_AND_PHASE_CHAIN_VERIFIED','actual_complete_record_count':1080,'completed_inner_children':1071,'outer_capture_count':9,'expected_preserved_failures':expected_fail,'unexpected_failures':[],'groups':groups,'full_logical_stdout_stderr_bytes':raw_total,'stored_stdout_stderr_bytes':stored_total,'retained_source_logical_bytes_verified':source_total,'phase_receipts':[pin(p) for p in receipts],'records':records,'scope':'Preserved completed process evidence and explicit native phase chain only; no fresh live service/Git state is inferred after writer release. Publication/tracker fullstream custody is separately verified in ROOT_PUBLICATION_OPERATION_CUSTODY_20261005.json. This verification performs no Git/service or scientific-file mutation. Private fullstream bodies stay local; only hashes/counts/PIDs/record pins are in this authored record.','original_budget':'1/5','new_central_proof_search_turns':0}
p=A/'ROOT_NATIVE_OPERATION_CUSTODY_20261005.json'
with p.open('x') as stream:stream.write(json.dumps(result,indent=2)+'\n');stream.flush();os.fsync(stream.fileno())
assert load(p)==result
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
