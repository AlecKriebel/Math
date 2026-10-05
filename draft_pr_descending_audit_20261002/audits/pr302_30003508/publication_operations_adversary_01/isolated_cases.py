"""Pure AST-isolated counterexamples. No service module is imported or called.

Synthetic service/native dictionaries below are explicitly mock observations;
they contain no invented process IDs. Actual execution custody is separate.
"""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote
import __future__, ast, contextlib, copy, gzip, hashlib, html, io, json, os, re, stat, sys

W=Path(__file__).resolve().parent; A=W.parent; D=A/'publication_preparation'; F=A/'preprint_package_v02'
R=Path('/Users/alec/Documents/Math')
INITIAL=json.loads((W/'INITIAL_INPUTS.json').read_bytes())
def require(ok,msg):
 if not ok: raise RuntimeError(msg)
def real_pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
for row in INITIAL['inputs']:require(real_pin(row['input']['path'])==row['input'],'Reviewed input changed')
for row in INITIAL['all_23_candidate_files']:require(real_pin(row['path'])==row,'Candidate changed')
def function(path,name,glob):
 tree=ast.parse(Path(path).read_bytes(),filename=str(path));nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name]
 require(len(nodes)==1,'Unique AST definition required')
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec',flags=__future__.annotations.compiler_flag),glob)
 return glob[name]
metadata=json.loads((F/'record_metadata.json').read_bytes())
manifest=json.loads((F/'SECOND_CANDIDATE_MANIFEST.json').read_bytes())
payloads={n:(F/n).read_bytes() for n in ['spectral_tensor_consistency.pdf','spectral_tensor_verification.zip']}
RID=12345678; DOI='10.5281/zenodo.'+str(RID)
published=dict(id=RID,environment='production',state='published',doi=DOI,doi_url='https://doi.org/'+DOI,record_url='https://zenodo.org/records/'+str(RID),title=metadata['title'],files=[dict(name=n,size=len(b),sha256=hashlib.sha256(b).hexdigest()) for n,b in payloads.items()],doi_resolution=dict(status='not_resolved',http_status=404))
results=[]
def record(name,observed,details):
 results.append(dict(name=name,observed=observed,details=details,synthetic_inputs_and_transport=True,no_network_or_service_execution=True))

# Guard contract counterexamples: the actual original function, only mock load/pin.
for variant in ['baseline','empty_evidence','changed_guard_source','changed_zenodo_operator','changed_public_verifier','changed_tracker_operator']:
 seen=[];clear=dict(status='PASS_PR302_REVISED_PREPRINT_AFTER_TWO_FRESH_WHOLE_PACKAGE_REVIEWS',original_PR=302,original_head='eb6e0e999521d84a65f9857d338cad76b84d30db',original_status='claimed_solved',unresolved_material_issues=[],unresolved_nonmandatory_issues=[],fresh_whole_package_reviews=2,publication_clearance=True,candidate_manifest=real_pin(F/'SECOND_CANDIDATE_MANIFEST.json'),closed_evidence_pins=[])
 def fake_load(p):
  p=Path(p)
  if p.name=='ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json':return copy.deepcopy(clear)
  if p.name=='SECOND_CANDIDATE_MANIFEST.json':return copy.deepcopy(manifest)
  if p.name=='zenodo-deposit.json':return json.loads((F/p.name).read_bytes())
  if p.name=='record_metadata.json':return copy.deepcopy(metadata)
  raise RuntimeError('Unexpected pure load')
 def fake_pin(p):
  p=Path(p);seen.append(str(p)); r=real_pin(p)
  changed={'changed_guard_source':'publication_guard.py','changed_zenodo_operator':'run_zenodo_step.py','changed_public_verifier':'verify_public_record.py','changed_tracker_operator':'append_tracker.py'}.get(variant)
  if p.name==changed:r['sha256']='0'*64
  return r
 glob=dict(sys=sys,A=A,F=F,R=R,require=require,load=fake_load,pin=fake_pin)
 function(D/'publication_guard.py','clearance',glob)()
 record('guard_'+variant,'ACCEPTED',dict(all_pin_calls=seen,operator_pin_calls=[x for x in seen if str(D) in x],no_actual_clearance_file_created=True,required_gap='Mandatory accepted operator/evidence pin contract absent' if variant!='baseline' else None))

class SyntheticPath:
 def __init__(self,value,pending=False):self.value=value;self.pending=pending
 def __truediv__(self,other):return SyntheticPath(self.value+'/'+str(other),self.pending)
 def __str__(self):return self.value
 def exists(self):return self.pending and self.value.endswith('/private_processes/tracker_append')

# The tracker main is extracted alone; every write and transport is memory-only.
def tracker_case(variant):
 calls=[];writes={};prior=[['Original Problem','Solution Chat URL','DOI','Notes']+['']*38+['Extra AQ heading'],['Earlier problem','','https://doi.org/10.example/prior','Earlier note']+['']*38+['AQ preserved value']]
 pub=copy.deepcopy(published);public=dict(status='PASS_PUBLIC_RECORD_EXACT_METADATA_AND_BOTH_FULL_FILE_BYTES',record_id=RID,DOI=DOI)
 if variant=='public_wrong_id':public['record_id']=RID+1
 if variant=='public_wrong_doi':public['DOI']='10.5281/zenodo.999'
 if variant=='published_wrong_title':pub['title']='Completely different paper'
 if variant=='published_sandbox_environment':pub['environment']='sandbox'
 if variant=='published_missing_files':pub['files']=[]
 if variant=='public_corrupt_retained_file_evidence':public['all_file_bytes']=[dict(name='unrelated.pdf',sha256='0'*64,bytes=1)]
 if variant=='duplicate_problem_in_AQ':prior[1][-1]='duplicate target 30003508'
 if variant=='duplicate_doi_in_AQ':prior[1][-1]=DOI
 if variant=='duplicate_title_in_AQ':prior[1][-1]=metadata['title']
 if variant=='wrong_header':prior[0][3]='Renamed header'
 targetrow=None
 def fake_load(p):
  if str(p).endswith('inspect_published_receipt.json'):return pub
  if str(p).endswith('PUBLIC_RECORD_VERIFICATION.json'):return public
  if str(p).endswith('record_metadata.json'):return metadata
  raise RuntimeError('Unexpected synthetic tracker load')
 def fake_execute(label,argv):
  nonlocal targetrow
  calls.append(dict(label=label,argv=argv))
  if label=='sheet_metadata':
   props=dict(sheetId=1254632077,title='Math Puzzles',gridProperties=dict(columnCount=43,rowCount=1000))
   if variant=='wrong_tab':props['title']='Other tab'
   if variant=='wrong_gid':props['sheetId']=1254632078
   return dict(spreadsheetId='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20',sheets=[dict(properties=props)]),dict(actual_PID=None,synthetic=True)
  if label=='all_rows_before':return dict(values=copy.deepcopy(prior)),dict(actual_PID=None,synthetic=True)
  if label in ('tracker_dry_run','tracker_append'):
   body=json.loads(argv[argv.index('--json')+1]);targetrow=body['values'][0]
   return dict(spreadsheetId='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20',updates=dict(updatedRows=1,updatedColumns=4,updatedCells=4,updatedRange="'Math Puzzles'!A3:D3")),dict(actual_PID=None,synthetic=True)
  if label=='appended_row_readback':return dict(values=[targetrow]),dict(actual_PID=None,synthetic=True)
  if label=='all_rows_after':
   after=copy.deepcopy(prior)+[targetrow]
   if variant=='changed_prior_AQ_after':after[1][-1]='Changed AQ value'
   return dict(values=after),dict(actual_PID=None,synthetic=True)
  raise RuntimeError('Unexpected synthetic tracker call')
 glob=dict(acquire=lambda:object(),load=fake_load,OUT=SyntheticPath('/SYNTHETIC_ONLY/publication_actual',variant=='uncertain_append_marker'),F=F,require=require,pin=lambda p:dict(sha256='0f27b8b0815bf09cdf95da48d3c604f05ceb8f16bf5c9f0ba355b1f957cdd47e'),execute=fake_execute,CLI='SYNTHETIC_PINNED_GWS',ID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20',GID=1254632077,json=json,write=lambda p,x:writes.update({str(p):copy.deepcopy(x)}),utc=lambda:'SYNTHETIC_TIME_NOT_AN_OBSERVATION',clearance=lambda:None)
 glob['identity']=function(D/'run_zenodo_step.py','identity',glob)
 fn=function(D/'append_tracker.py','main',glob);exception=None
 try:
  with contextlib.redirect_stdout(io.StringIO()):fn()
 except Exception as exc:exception=str(exc)
 completion=next((v for k,v in writes.items() if k.endswith('/TRACKER_COMPLETE.json')),None)
 expected_accept=variant in ['valid','public_status_only_without_full_evidence','public_corrupt_retained_file_evidence','published_wrong_title','published_sandbox_environment','published_missing_files']
 require((exception is None)==expected_accept,'Unexpected tracker fixture disposition: '+variant+' '+str(exception))
 require(not expected_accept or completion is not None,'Missing synthetic completion')
 record('tracker_'+variant,'ACCEPTED' if exception is None else 'REJECTED',dict(exception=exception,calls=calls,synthetic_completion=completion,actual_append_mock_reached=any(x['label']=='tracker_append' for x in calls),required_gap='Thin public/published receipts trusted without full evidence binding' if expected_accept and variant!='valid' else None,prior_43_columns_scanned=True))
for v in ['valid','public_status_only_without_full_evidence','public_corrupt_retained_file_evidence','published_wrong_title','published_sandbox_environment','published_missing_files','public_wrong_id','public_wrong_doi','duplicate_problem_in_AQ','duplicate_doi_in_AQ','duplicate_title_in_AQ','wrong_header','wrong_tab','wrong_gid','uncertain_append_marker','changed_prior_AQ_after']:tracker_case(v)

# Actual verifier comparison logic with fully in-memory anonymous responses.
for variant in ['valid_DOI_404_separate','metadata_title_changed','metadata_description_changed','wrong_public_id','wrong_public_doi','extra_file','wrong_content_url','wrong_full_file_bytes','wrong_remote_checksum']:
 remote=copy.deepcopy(metadata);remote['license']=dict(id=metadata['license']);remote['resource_type']=dict(type=metadata['upload_type'],subtype=metadata['publication_type']);remote['doi']=DOI
 rec=dict(id=RID,doi=DOI,metadata=remote,files=[dict(key=n,size=len(b),checksum='md5:'+hashlib.md5(b).hexdigest(),links=dict(self='https://zenodo.org/api/records/'+str(RID)+'/files/'+n+'/content')) for n,b in payloads.items()]);calls=[];writes={}
 if variant=='metadata_title_changed':remote['title']='Another title'
 if variant=='metadata_description_changed':remote['description']+='changed'
 if variant=='wrong_public_id':rec['id']=RID+1
 if variant=='wrong_public_doi':rec['doi']='10.5281/zenodo.999'
 if variant=='extra_file':rec['files'].append(dict(key='extra.txt'))
 if variant=='wrong_content_url':rec['files'][0]['links']['self']='https://zenodo.org/api/records/999/files/spectral_tensor_consistency.pdf/content'
 if variant=='wrong_remote_checksum':rec['files'][0]['checksum']='md5:'+'0'*32
 def fake_fetch(label,url):
  calls.append(dict(label=label,url=url))
  if label=='record':b=json.dumps(rec).encode()
  else:
   name=label.removeprefix('file_');b=payloads[name]
   if variant=='wrong_full_file_bytes':b=b+b'X'
  return b,dict(synthetic=True,actual_PID=None)
 glob=dict(acquire=lambda:object(),OUT=SyntheticPath('/SYNTHETIC_ONLY/publication_actual'),load=lambda p:copy.deepcopy(published) if str(p).endswith('inspect_published_receipt.json') else metadata,F=F,require=require,fetch=fake_fetch,json=json,hashlib=hashlib,sha=lambda b:hashlib.sha256(b).hexdigest(),clearance=lambda:None,utc=lambda:'SYNTHETIC_TIME_NOT_AN_OBSERVATION',write=lambda p,x:writes.update({str(p):copy.deepcopy(x)}))
 glob['identity']=function(D/'run_zenodo_step.py','identity',glob);fn=function(D/'verify_public_record.py','main',glob);exception=None
 try:
  with contextlib.redirect_stdout(io.StringIO()):fn()
 except Exception as exc:exception=str(exc)
 require((exception is None)==(variant=='valid_DOI_404_separate'),'Unexpected verifier fixture disposition')
 record('public_'+variant,'ACCEPTED' if exception is None else 'REJECTED',dict(exception=exception,calls=calls,doi_resolver_not_publication_gate=True,all_metadata_descriptor_count=len(metadata)))

# Repository kit irreversible-action logic with a fake client and memory state.
kit=R/'zenodo_deposit_tool/zenodo.py'
prepared=[dict(path=F/n,name=n,size=len(b),md5=hashlib.md5(b).hexdigest(),sha256=hashlib.sha256(b).hexdigest()) for n,b in payloads.items()]
for variant in ['correct_publish','wrong_confirm_id','already_published','lost_publish_reply_confirmed','lost_publish_reply_unconfirmed','wrong_readback_id','metadata_diff_before_publish','checksum_diff_before_publish','create_reply_unknown','stage_conflicting_extra_file']:
 calls=[];saved=[];state=dict(manifest=str(F/'zenodo-deposit.json'),environment='production',id=RID)
 def deposit(submitted=False):return dict(id=RID,submitted=submitted,metadata=copy.deepcopy(metadata),doi=DOI,files=[dict(filename=x['name'],filesize=x['size'],checksum='md5:'+x['md5']) for x in prepared],links=dict(bucket='https://zenodo.org/api/files/SYNTHETIC_BUCKET'))
 first=deposit(variant=='already_published')
 if variant=='metadata_diff_before_publish':first['metadata']['title']='Changed'
 if variant=='checksum_diff_before_publish':first['files'][0]['checksum']='md5:'+'0'*32
 if variant=='stage_conflicting_extra_file':first['files'].append(dict(filename='extra.txt',filesize=1,checksum='md5:'+'0'*32))
 glob=dict(Path=Path,hashlib=hashlib,html=html,re=re,quote=quote,datetime=datetime,timezone=timezone,BASES=dict(production='https://zenodo.org',sandbox='https://sandbox.zenodo.org'),save_state=lambda p,x:saved.append(copy.deepcopy(x)),load_manifest=lambda p:(copy.deepcopy(metadata),copy.deepcopy(prepared)),local_state=lambda p,e:(SyntheticPath('/SYNTHETIC_ONLY/state'),None if variant=='create_reply_unknown' else copy.deepcopy(state)),doi_status=lambda doi:dict(status='not_resolved',http_status=404))
 for name in ['DepositError','server_files','matching_file','validate_record','verify','public_doi_url','published_summary','run']:function(kit,name,glob)
 Error=glob['DepositError']
 class FakeClient:
  def get(self,rid):
   calls.append(('get',rid))
   if sum(x[0]=='get' for x in calls)==1:return copy.deepcopy(first)
   if variant=='lost_publish_reply_unconfirmed':raise Error('SYNTHETIC unavailable readback')
   item=deposit(True)
   if variant=='wrong_readback_id':item['id']=RID+1
   return item
  def publish(self,rid):
   calls.append(('publish',rid))
   if variant.startswith('lost_publish_reply'):raise Error('SYNTHETIC lost POST response')
   return deposit(True)
  def create(self,meta):calls.append(('create',None));raise Error('SYNTHETIC unknown create response')
  def upload(self,bucket,entry):calls.append(('upload',entry['name']));return {}
  def update(self,rid,meta):calls.append(('update',rid));return {}
 class Args:pass
 args=Args();args.manifest=F/'zenodo-deposit.json';args.sandbox=False;args.command='stage' if variant in ['create_reply_unknown','stage_conflicting_extra_file'] else 'publish';args.confirm_id=RID+1 if variant=='wrong_confirm_id' else RID
 exception=None;summary=None
 try:summary=glob['run'](args,FakeClient())
 except Exception as exc:exception=str(exc)
 expected=variant in ['correct_publish','already_published','lost_publish_reply_confirmed']
 require((exception is None)==expected,'Unexpected kit fixture disposition '+variant)
 publish_count=sum(x[0]=='publish' for x in calls);require(publish_count<=1,'Second publication POST in mock')
 if variant in ['wrong_confirm_id','already_published','metadata_diff_before_publish','checksum_diff_before_publish','create_reply_unknown','stage_conflicting_extra_file']:require(publish_count==0,'Unexpected POST in rejected/old case')
 record('kit_'+variant,'ACCEPTED' if exception is None else 'REJECTED_WITHOUT_AUTOMATIC_RETRY',dict(exception=exception,calls=calls,publish_POST_count=publish_count,summary=summary,saved_state_count=len(saved),public_DOI_status_distinct=True))

for row in INITIAL['inputs']:require(real_pin(row['input']['path'])==row['input'],'Reviewed input changed after tests')
for row in INITIAL['all_23_candidate_files']:require(real_pin(row['path'])==row,'Candidate changed after tests')
out=dict(schema='pr302-prepared-publication-operator-AST-counterexamples/v1',UTC=datetime.now(timezone.utc).isoformat(),actual_test_runner_PID=os.getpid(),fixture_count=len(results),all_cases_completed=True,results=results,original_four_sources_and_23_candidate_files_unchanged=True,no_service_module_import_or_network_call=True,no_actual_clearance_file_created=True,no_Git_PR_native_or_control_mutation=True)
with (W/'ISOLATED_CASE_RESULTS.json').open('x') as f:json.dump(out,f,indent=2,ensure_ascii=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status='ALL_ISOLATED_CASES_COMPLETED',actual_PID=os.getpid(),cases=len(results),required_gaps=['operator/evidence guard contract','tracker full public-evidence binding']),indent=2))
