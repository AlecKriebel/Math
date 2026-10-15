"""AST-only counterexamples. Transport is simulated; all records are fixtures."""
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlsplit
import ast,copy,argparse,fcntl,gzip,hashlib,json,os,stat,subprocess,sys,shutil,types
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_descending_audit_20261002/audits/pr302_30003508';W=A/'publication_operations_adversary_02';D=A/'publication_preparation';REALF=A/'preprint_package_v02'
SA=W/'synthetic_fixture_A';F=SA/'preprint_package_v02';OUT=SA/'publication_actual';SG=SA/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json';OG=SA/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json';OM=SA/'REVISED_OPERATOR_MANIFEST.json';RV=SA/'publication_operations_adversary_02'
SA.mkdir();F.mkdir();OUT.mkdir();RV.mkdir()
def sh(b):return hashlib.sha256(b).hexdigest()
def fp(p):
 p=Path(p);assert p.is_file() and not p.is_symlink();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sh(b),mode=stat.S_IMODE(p.stat().st_mode))
def put(p,obj):Path(p).write_text(json.dumps(obj,indent=2)+'\n')
for p in REALF.iterdir():
 if p.is_file() and p.name in {Path(x['path']).name for x in json.loads((REALF/'SECOND_CANDIDATE_MANIFEST.json').read_bytes())['files']}|{'SECOND_CANDIDATE_MANIFEST.json'}:
  q=F/p.name;shutil.copyfile(p,q);q.chmod(stat.S_IMODE(p.stat().st_mode))
science=json.loads((A/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json').read_bytes());science['candidate_manifest']=fp(F/'SECOND_CANDIDATE_MANIFEST.json');newpins=[]
for row in science['closed_evidence_pins']:
 p=Path(row['path']);q=SA/p.relative_to(A);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);q.chmod(row['mode']);newpins.append(fp(q))
science['closed_evidence_pins']=newpins;science['synthetic_fixture_never_authority']=True;put(SG,science)
shutil.copyfile(D/'REVISED_OPERATOR_MANIFEST.json',OM)
for name in ('REPORT.md','READ_SCOPE.md','OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'):(RV/name).write_text('Synthetic complete-contract role for isolated tests; grants no authority.\n')
put(RV/'VERDICT.json',dict(mandatory_issues=[],nonmandatory_issues=[],publication_clearance=False,synthetic_fixture_never_authority=True))
ops=dict(status='PASS_PR302_REPAIRED_PUBLICATION_OPERATORS_AND_COMPLETE_EVIDENCE',original_PR=302,publication_operations_clearance=True,unresolved_material_issues=[],unresolved_nonmandatory_issues=[],science_gate=fp(SG),candidate_manifest=fp(F/'SECOND_CANDIDATE_MANIFEST.json'),operator_manifest=fp(OM),approved_operational_sources=json.loads(OM.read_bytes())['approved_operational_sources'],review_namespace=str(RV),closed_operations_evidence_pins=[fp(RV/n) for n in ('REPORT.md','READ_SCOPE.md','VERDICT.json','OUTPUT_MANIFEST.json','CLOSURE_SEAL.json')],approved_runtime_targets=[fp(Path(p).resolve()) for p in ('/opt/homebrew/bin/python3','/usr/bin/curl','/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws')],synthetic_fixture_never_authority=True)
put(OG,ops)
ns=dict(Path=Path,datetime=datetime,timezone=timezone,urlsplit=urlsplit,fcntl=fcntl,gzip=gzip,hashlib=hashlib,json=json,os=os,stat=stat,subprocess=subprocess,sys=sys,argparse=argparse,R=R,A=SA,D=D,F=F,OUT=OUT,OPERATORS=('publication_guard.py','run_zenodo_step.py','verify_public_record.py','append_tracker.py'),PYTHON='/opt/homebrew/bin/python3',CLI='/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws',KIT=R/'zenodo_deposit_tool/zenodo.py',SCIENCE_GATE=SG,OPERATIONS_GATE=OG,OPERATOR_MANIFEST=OM,ID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20',GID=1254632077)
AST_READS=[]
for source in ns['OPERATORS']:
 p=D/source;b=p.read_bytes();tree=ast.parse(b,filename=str(p));nodes=[]
 for node in tree.body:
  if isinstance(node,ast.FunctionDef):
   if node.name=='main':node.name={'run_zenodo_step.py':'zenodo_main','verify_public_record.py':'public_main','append_tracker.py':'tracker_main'}[source]
   nodes.append(node)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns)
 AST_READS.append(dict(source=fp(p),extracted_functions=[n.name for n in nodes],all_function_bodies_original_except_main_name=True,top_level_import_and_main_not_executed=True))
CASES=[]
def case(name,fn,want=True,detail=None):
 try:
  answer=fn();accepted=True;error=None
 except Exception as e:accepted=False;answer=None;error=dict(type=type(e).__name__,message=str(e))
 row=dict(name=name,expected_accept=want,accepted=accepted,expected_disposition_observed=accepted==want,error=error,detail=detail)
 CASES.append(row);print(json.dumps(row));return row
def mutation(p,fn,call):
 original=p.read_bytes();obj=json.loads(original);fn(obj);put(p,obj)
 try:return call()
 finally:p.write_bytes(original)
def mutate_guard(p,fn):
 saved=OG.read_bytes()
 def run():
  o=json.loads(OG.read_bytes());o['science_gate']=fp(SG);o['operator_manifest']=fp(OM);put(OG,o);return ns['clearance']()
 try:return mutation(p,fn,run)
 finally:OG.write_bytes(saved)
case('guard_complete_contract',lambda:ns['clearance']())
case('guard_production_ops_gate_absent',lambda: ns['clearance'].__globals__['load'](A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json'),False)
for name,key,value in [('science_empty','closed_evidence_pins',[]),('science_wrong_head','original_head','0'*40),('science_review_count','fresh_whole_package_reviews',1),('science_issues','unresolved_material_issues',['open'])]:case('guard_'+name,lambda k=key,v=value:mutate_guard(SG,lambda o:o.__setitem__(k,v)),False)
case('guard_science_duplicate',lambda:mutate_guard(SG,lambda o:o['closed_evidence_pins'].__setitem__(1,o['closed_evidence_pins'][0])),False)
case('guard_science_extra_pin_field',lambda:mutate_guard(SG,lambda o:o['closed_evidence_pins'][0].__setitem__('unreviewed',True)),False)
for key in ('approved_operational_sources','closed_operations_evidence_pins','approved_runtime_targets'):
 case('guard_empty_'+key,lambda k=key:mutation(OG,lambda o:o.__setitem__(k,[]),ns['clearance']),False)
 case('guard_duplicate_'+key,lambda k=key:mutation(OG,lambda o:o[k].__setitem__(1,o[k][0]),ns['clearance']),False)
case('guard_first_review_namespace',lambda:mutation(OG,lambda o:o.__setitem__('review_namespace',str(SA/'publication_operations_adversary_01')),ns['clearance']),False)
case('guard_wrong_manifest_registry_status',lambda:mutate_guard(OM,lambda o:o.__setitem__('status','changed')),False)
case('guard_missing_registry_source',lambda:mutate_guard(OM,lambda o:o['approved_operational_sources'].pop()),False)
case('guard_duplicate_registry_source',lambda:mutate_guard(OM,lambda o:o['approved_operational_sources'].__setitem__(1,o['approved_operational_sources'][0])),False)
for p in [D/n for n in ns['OPERATORS']]+[Path(x).resolve() for x in (ns['PYTHON'],'/usr/bin/curl',ns['CLI'])]:
 def changed_pin(path=p):
  original=ns['pin']
  def observed(q):
   row=original(q)
   if Path(q)==path:row['sha256']='0'*64
   return row
  ns['pin']=observed
  try:return ns['clearance']()
  finally:ns['pin']=original
 case('guard_changed_body_'+p.name,changed_pin,False,dict(synthetic_pin_provider_change=str(p),actual_file_unchanged=True))
# Complete positive inspected receipt and anonymous record, built from actual frozen bytes.
metadata=json.loads((F/'record_metadata.json').read_bytes());rid=123456789
published=dict(id=rid,doi='10.5281/zenodo.'+str(rid),doi_url='https://doi.org/10.5281/zenodo.'+str(rid),record_url='https://zenodo.org/records/'+str(rid),environment='production',state='published',title=metadata['title'],files=[dict(name=name,size=(F/name).stat().st_size,sha256=sh((F/name).read_bytes())) for name in ('spectral_tensor_consistency.pdf','spectral_tensor_verification.zip')],doi_resolution=dict(status='not_resolved',http_status=404),synthetic_fixture_never_authority=True)
remote_metadata=copy.deepcopy(metadata);remote_metadata['license']={'id':metadata['license']};remote_metadata['resource_type']={'type':metadata['upload_type'],'subtype':metadata['publication_type']};remote_metadata.pop('upload_type');remote_metadata.pop('publication_type');remote_metadata['doi']=published['doi']
record=dict(id=rid,doi=published['doi'],metadata=remote_metadata,files=[dict(key=x['name'],size=x['size'],checksum='md5:'+hashlib.md5((F/x['name']).read_bytes()).hexdigest(),links=dict(self='https://zenodo.org/api/records/'+str(rid)+'/files/'+x['name']+'/content')) for x in published['files']])
FAKE_OUTPUTS={}
class FixtureChild:
 def __init__(self,argv,**kwargs):
  assert kwargs['cwd']==R;self.pid=os.getpid();self.returncode=0;self.body=FAKE_OUTPUTS[tuple(argv)];self.stderr=b''
 def communicate(self,timeout=None):return self.body,self.stderr
 def kill(self):self.returncode=-9
fake_subprocess=types.SimpleNamespace(Popen=FixtureChild,PIPE=subprocess.PIPE,DEVNULL=subprocess.DEVNULL,TimeoutExpired=subprocess.TimeoutExpired)
ns['subprocess']=fake_subprocess
ns['sys']=types.SimpleNamespace(argv=[str(D/'run_zenodo_step.py')],executable=sys.executable,flags=sys.flags)
argv_inspect=[ns['PYTHON'],'-E','-B',str(ns['KIT']),'inspect',str(F/'zenodo-deposit.json'),'--check-doi']
FAKE_OUTPUTS[tuple(argv_inspect)]=json.dumps(published).encode()
_,inspect_native=ns['execute']('inspect_published',argv_inspect)
put(OUT/'inspect_published_receipt.json',published)
argv_record=ns['public_argv']('https://zenodo.org/api/records/'+str(rid));FAKE_OUTPUTS[tuple(argv_record)]=json.dumps(record).encode()
raw,record_native=ns['execute']('record',argv_record,OUT/'private_public_readback',parse_json=False)
file_rows=[]
for item in record['files']:
 name=item['key'];body=(F/name).read_bytes();argv=ns['public_argv'](item['links']['self']);FAKE_OUTPUTS[tuple(argv)]=body;_,native=ns['execute']('file_'+name,argv,OUT/'private_public_readback',parse_json=False)
 file_rows.append(dict(name=name,bytes=len(body),sha256=sh(body),md5=hashlib.md5(body).hexdigest(),entire_public_download_equals_reviewed_file=True,actual_anonymous_native_process=native))
# Clearly identify simulated native fields; they use the observed test-runner PID,
# not invented PIDs, and make no claim that transport children actually ran.
for parent,label in [(OUT/'private_processes','inspect_published'),(OUT/'private_public_readback','record')]+[(OUT/'private_public_readback','file_'+x['name']) for x in published['files']]:
 for leaf in ('request.json','execution.json'):
  p=parent/label/leaf;o=json.loads(p.read_bytes());o['synthetic_fixture_not_native_transport']=True;o['fixture_PID_is_actual_test_runner_not_transport_child']=True;put(p,o)
inspect_native=json.loads((OUT/'private_processes/inspect_published/execution.json').read_bytes());record_native=json.loads((OUT/'private_public_readback/record/execution.json').read_bytes())
for row in file_rows:row['actual_anonymous_native_process']=json.loads((OUT/'private_public_readback'/('file_'+row['name'])/'execution.json').read_bytes())
public=dict(UTC=datetime.now(timezone.utc).isoformat(),status='PASS_PUBLIC_RECORD_EXACT_METADATA_AND_BOTH_FULL_FILE_BYTES',record_id=rid,DOI=published['doi'],doi_url=published['doi_url'],record_url=published['record_url'],all_reviewed_metadata_fields_exact=True,public_schema_mapping=['license.id','resource_type.type','resource_type.subtype'],all_file_bytes=file_rows,actual_record_read=record_native,doi_resolution=published['doi_resolution'],no_individual_contacted=True,publication_state_confirmed_independently_of_resolver=True,synthetic_fixture_never_authority=True)
put(OUT/'PUBLIC_RECORD_VERIFICATION.json',public)
case('complete_inspected_evidence',ns['inspected_publication'])
case('complete_public_evidence_with_DOI404',lambda:ns['verify_public_evidence'](published))
for key,value in [('environment','sandbox'),('title','Wrong paper'),('files',[]),('doi','10.5281/zenodo.2'),('id',2),('state','draft')]:case('published_wrong_'+key,lambda k=key,v=value:mutation(OUT/'inspect_published_receipt.json',lambda o:o.__setitem__(k,v),ns['inspected_publication']),False)
case('public_thin_status_only',lambda:mutation(OUT/'PUBLIC_RECORD_VERIFICATION.json',lambda o:[o.pop(k) for k in list(o) if k not in ('status','record_id','DOI')],lambda:ns['verify_public_evidence'](published)),False)
for key,value in [('all_reviewed_metadata_fields_exact',False),('public_schema_mapping',[]),('all_file_bytes',[]),('record_id',2),('DOI','10.5281/zenodo.2'),('doi_resolution',{'status':'resolved'})]:case('public_wrong_'+key,lambda k=key,v=value:mutation(OUT/'PUBLIC_RECORD_VERIFICATION.json',lambda o:o.__setitem__(k,v),lambda:ns['verify_public_evidence'](published)),False)
case('public_corrupt_file_claim',lambda:mutation(OUT/'PUBLIC_RECORD_VERIFICATION.json',lambda o:o['all_file_bytes'][0].__setitem__('sha256','0'*64),lambda:ns['verify_public_evidence'](published)),False)
nw=OUT/'private_processes/inspect_published';execution=nw/'execution.json';request=nw/'request.json';started=nw/'started.json'
for key,value in [('actual_PID',None),('actual_launcher_PID',True),('cwd','/tmp'),('argv',['wrong']),('end_UTC','2026-10-05T00:00:00+00:00'),('start_UTC','2026-10-05T08:00:00'),('exit_code',1),('timed_out',True),('automatic_retry',True),('full_prelaunch_sources',[]),('full_prelaunch_approvals',[])]:case('native_wrong_'+key,lambda k=key,v=value:mutation(execution,lambda o:o.__setitem__(k,v),ns['inspected_publication']),False)
case('native_started_PID_disagrees',lambda:mutation(started,lambda o:o.__setitem__('actual_PID',os.getpid()+1),ns['inspected_publication']),False)
case('native_request_disagrees',lambda:mutation(request,lambda o:o.__setitem__('cwd','/tmp'),ns['inspected_publication']),False)
case('native_missing_source_pin',lambda:mutation(execution,lambda o:o['full_prelaunch_sources'].pop(),ns['inspected_publication']),False)
case('native_duplicate_source_pin',lambda:mutation(execution,lambda o:o['full_prelaunch_sources'].__setitem__(1,o['full_prelaunch_sources'][0]),ns['inspected_publication']),False)
case('native_logical_stdout_SHA_wrong',lambda:mutation(execution,lambda o:o['stdout'].__setitem__('logical_sha256','0'*64),ns['inspected_publication']),False)
case('native_binary_pin_wrong',lambda:mutation(execution,lambda o:o['resolved_executable'].__setitem__('sha256','0'*64),ns['inspected_publication']),False)
def alter_stream(path,body,fn):
 old=path.read_bytes();path.write_bytes(gzip.compress(body,mtime=0))
 try:return fn()
 finally:path.write_bytes(old)
case('native_stored_stdout_changed',lambda:alter_stream(nw/'stdout.bin.gz',b'{}',ns['inspected_publication']),False)
# Rewrite all consistent native/receipt stream pins for a corrupted remote record:
# this tests actual content comparison rather than merely stale-hash rejection.
def consistent_record_change(change):
 cw=OUT/'private_public_readback/record';saved={p:p.read_bytes() for p in (cw/'stdout.bin.gz',cw/'execution.json',OUT/'PUBLIC_RECORD_VERIFICATION.json')};o=copy.deepcopy(record);change(o);body=json.dumps(o).encode();stream=cw/'stdout.bin.gz';stream.write_bytes(gzip.compress(body,mtime=0));e=json.loads((cw/'execution.json').read_bytes());e['stdout']=dict(logical_bytes=len(body),logical_sha256=sh(body),stored=fp(stream));put(cw/'execution.json',e);p=json.loads((OUT/'PUBLIC_RECORD_VERIFICATION.json').read_bytes());p['actual_record_read']=e;put(OUT/'PUBLIC_RECORD_VERIFICATION.json',p)
 try:return ns['verify_public_evidence'](published)
 finally:
  for p,b in saved.items():p.write_bytes(b)
for label,fn in [('title',lambda o:o['metadata'].__setitem__('title','Changed')),('description',lambda o:o['metadata'].__setitem__('description','Changed')),('DOI',lambda o:o['metadata'].__setitem__('doi','10.5281/zenodo.2')),('record_id',lambda o:o.__setitem__('id',2)),('license',lambda o:o['metadata']['license'].__setitem__('id','other')),('file_checksum',lambda o:o['files'][0].__setitem__('checksum','md5:'+'0'*32)),('content_endpoint',lambda o:o['files'][0]['links'].__setitem__('self','https://zenodo.org/api/records/2/files/x/content'))]:case('consistent_raw_record_changed_'+label,lambda f=fn:consistent_record_change(f),False)
def consistent_download_change():
 name=published['files'][0]['name'];cw=OUT/'private_public_readback'/('file_'+name);saved={p:p.read_bytes() for p in (cw/'stdout.bin.gz',cw/'execution.json',OUT/'PUBLIC_RECORD_VERIFICATION.json')};body=(F/name).read_bytes()+b'x';stream=cw/'stdout.bin.gz';stream.write_bytes(gzip.compress(body,mtime=0));e=json.loads((cw/'execution.json').read_bytes());e['stdout']=dict(logical_bytes=len(body),logical_sha256=sh(body),stored=fp(stream));put(cw/'execution.json',e);p=json.loads((OUT/'PUBLIC_RECORD_VERIFICATION.json').read_bytes());p['all_file_bytes'][0]['actual_anonymous_native_process']=e;p['all_file_bytes'][0]['bytes']=len(body);p['all_file_bytes'][0]['sha256']=sh(body);p['all_file_bytes'][0]['md5']=hashlib.md5(body).hexdigest();put(OUT/'PUBLIC_RECORD_VERIFICATION.json',p)
 try:return ns['verify_public_evidence'](published)
 finally:
  for p,b in saved.items():p.write_bytes(b)
case('consistent_entire_download_corrupted',consistent_download_change,False)
case('complete_public_evidence_after_all_restorations',lambda:ns['verify_public_evidence'](published))
# Tracker end-to-end keeps the genuine guard and both stronger evidence functions;
# only the service transport endpoint is replaced with one explicit pure fixture.
original_execute=ns['execute'];original_acquire=ns['acquire'];TABLE=[['Original Problem','Solution Chat URL','DOI','Notes'],['Existing','','https://doi.org/10.5281/zenodo.1','prior']+['']*38+['AQ-preserved']];TRACK_CALLS=[];APPENDED=[];MODE={}
def tracker_execute(label,argv,capture_dir=None,parse_json=True):
 ns['clearance']();TRACK_CALLS.append(dict(label=label,argv=argv,synthetic_service=True));native=dict(actual_PID=os.getpid(),fixture_PID_is_actual_test_runner_not_transport_child=True)
 if label=='sheet_metadata':return dict(spreadsheetId=ns['ID'],sheets=[dict(properties=dict(sheetId=ns['GID'],title=MODE.get('tab','Math Puzzles'),gridProperties=dict(rowCount=1000,columnCount=43)))]),native
 if label=='all_rows_before':return dict(values=copy.deepcopy(TABLE)),native
 if label=='tracker_dry_run':
  if MODE.get('change_before_append'):
   p=OUT/'PUBLIC_RECORD_VERIFICATION.json';x=json.loads(p.read_bytes());x['all_reviewed_metadata_fields_exact']=False;put(p,x)
  return dict(synthetic_dry_run=True),native
 if label=='tracker_append':
  body=json.loads(argv[argv.index('--json')+1]);APPENDED.extend(body['values']);return dict(spreadsheetId=ns['ID'],updates=dict(updatedRows=1,updatedColumns=4,updatedCells=4,updatedRange="'Math Puzzles'!A3:D3")),native
 if label=='appended_row_readback':return dict(values=copy.deepcopy(APPENDED)),native
 if label=='all_rows_after':
  rows=copy.deepcopy(TABLE)+copy.deepcopy(APPENDED)
  if MODE.get('change_prior_AQ'):rows[1][42]='Changed'
  return dict(values=rows),native
 raise AssertionError('Unexpected synthetic service label '+label)
def tracker_fixture(mode=None,bad_public=None):
 TRACK_CALLS.clear();APPENDED.clear();MODE.clear();MODE.update(mode or {});saved=(OUT/'PUBLIC_RECORD_VERIFICATION.json').read_bytes()
 for name in ('TRACKER_ROW_REQUEST.json','TRACKER_COMPLETE.json'):
  p=OUT/name
  if p.exists():p.unlink()
 ns['execute']=tracker_execute;ns['acquire']=lambda:ns['clearance']()
 if bad_public:put(OUT/'PUBLIC_RECORD_VERIFICATION.json',bad_public)
 try:ns['tracker_main']();return dict(calls=TRACK_CALLS,appended=APPENDED)
 finally:
  ns['execute']=original_execute;ns['acquire']=original_acquire;(OUT/'PUBLIC_RECORD_VERIFICATION.json').write_bytes(saved)
case('tracker_complete_valid_chain_one_append',tracker_fixture)
assert sum(x['label']=='tracker_append' for x in TRACK_CALLS)==1
case('tracker_thin_public_before_any_service',lambda:tracker_fixture(bad_public={k:public[k] for k in ('status','record_id','DOI')}),False);assert TRACK_CALLS==[]
case('tracker_public_changes_immediately_before_append',lambda:tracker_fixture(dict(change_before_append=True)),False);assert not APPENDED
case('tracker_wrong_tab',lambda:tracker_fixture(dict(tab='Other')),False);assert not APPENDED
case('tracker_changed_prior_AQ_detected_after_one_append',lambda:tracker_fixture(dict(change_prior_AQ=True)),False);assert len(APPENDED)==1 and not (OUT/'TRACKER_COMPLETE.json').exists()
TABLE[1][42]='30003508 duplicate in AQ';case('tracker_duplicate_in_AQ',tracker_fixture,False);assert not APPENDED;TABLE[1][42]='AQ-preserved'
# Original immutable source and current23public body/mode readback.
initial=json.loads((W/'INITIAL_INPUTS.json').read_bytes())
for x in initial['sources']:assert fp(x['input']['path'])==x['input']
for x in initial['candidate_files']:assert fp(x['path'])==x
assert not (A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json').exists() and not (A/'publication_actual').exists()
results=dict(UTC=datetime.now(timezone.utc).isoformat(),actual_test_runner_PID=os.getpid(),status='COMPLETE_AST_ISOLATED_REPAIRED_CONTRACT_CHECKS',cases=CASES,case_count=len(CASES),unexpected_dispositions=[x for x in CASES if not x['expected_disposition_observed']],ast_sources=AST_READS,synthetic_guard_locations=dict(A=str(SA),F=str(F),OUT=str(OUT),science_gate=str(SG),operations_gate=str(OG),operator_manifest=str(OM)),guard_and_public_authentication_functions_not_bypassed=True,transport_is_synthetic_and_makes_no_native_or_service_claim=True,fixture_PIDs_are_observed_runner_PID_with_explicit_nontransport_labels=True,original_all23_public_and_source_inputs_unchanged=True,production_gate_and_OUT_absent=True,publication_clearance=False)
put(W/'ISOLATED_CASE_RESULTS.json',results)
assert not results['unexpected_dispositions'],results['unexpected_dispositions']
print(json.dumps(dict(status=results['status'],case_count=len(CASES),unexpected_dispositions=0,actual_test_runner_PID=os.getpid())))
