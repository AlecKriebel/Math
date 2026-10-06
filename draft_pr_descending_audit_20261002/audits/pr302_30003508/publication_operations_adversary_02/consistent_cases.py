"""Fresh focused coupled-record/source and kit state/POST counterexamples."""
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlsplit,quote
from urllib.request import HTTPRedirectHandler,Request,build_opener
from urllib.error import HTTPError,URLError
import ast,argparse,copy,fcntl,gzip,hashlib,html,http.client,json,os,re,stat,subprocess,sys,tempfile,types
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_descending_audit_20261002/audits/pr302_30003508';W=A/'publication_operations_adversary_02';D=A/'publication_preparation';SA=W/'synthetic_fixture_A';F=SA/'preprint_package_v02';OUT=SA/'publication_actual';SG=SA/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json';OG=SA/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json';OM=SA/'REVISED_OPERATOR_MANIFEST.json'
ns=dict(Path=Path,datetime=datetime,timezone=timezone,urlsplit=urlsplit,fcntl=fcntl,gzip=gzip,hashlib=hashlib,json=json,os=os,stat=stat,subprocess=subprocess,sys=sys,argparse=argparse,R=R,A=SA,D=D,F=F,OUT=OUT,OPERATORS=('publication_guard.py','run_zenodo_step.py','verify_public_record.py','append_tracker.py'),PYTHON='/opt/homebrew/bin/python3',CLI='/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws',KIT=R/'zenodo_deposit_tool/zenodo.py',SCIENCE_GATE=SG,OPERATIONS_GATE=OG,OPERATOR_MANIFEST=OM)
for source in ns['OPERATORS']:
 tree=ast.parse((D/source).read_bytes(),filename=str(D/source));defs=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name!='main'];exec(compile(ast.Module(body=defs,type_ignores=[]),str(D/source),'exec'),ns)
CASES=[]
def put(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def case(name,fn,want=False):
 try:fn();accepted=True;error=None
 except Exception as e:accepted=False;error=dict(type=type(e).__name__,message=str(e))
 row=dict(name=name,expected_accept=want,accepted=accepted,error=error,expected_disposition_observed=accepted==want);CASES.append(row);print(json.dumps(row))
def coupled_native(change):
 cw=OUT/'private_processes/inspect_published';paths=(cw/'request.json',cw/'execution.json',cw/'started.json');saved={p:p.read_bytes() for p in paths};request=json.loads(saved[paths[0]]);native=json.loads(saved[paths[1]]);started=json.loads(saved[paths[2]]);change(request,native,started)
 for p,o in zip(paths,(request,native,started)):put(p,o)
 try:return ns['inspected_publication']()
 finally:
  for p,b in saved.items():p.write_bytes(b)
def both_set(key,value):
 def modify(q,e,s):q[key]=value;e[key]=value
 return modify
for key,value in [('full_prelaunch_sources',[]),('full_prelaunch_approvals',[]),('actual_launcher_PID',None),('cwd','/tmp'),('argv',['/usr/bin/curl','wrong']),('resolved_executable',{}),('resolved_caller_interpreter',{}),('automatic_retry',True)]:case('coupled_native_'+key,lambda k=key,v=value:coupled_native(both_set(k,v)))
def duplicate_source(q,e,s):q['full_prelaunch_sources'][1]=q['full_prelaunch_sources'][0];e['full_prelaunch_sources']=copy.deepcopy(q['full_prelaunch_sources'])
case('coupled_duplicate_source',lambda:coupled_native(duplicate_source))
def no_kit(q,e,s):q['full_prelaunch_sources']=[x for x in q['full_prelaunch_sources'] if x['input']['path']!=str(ns['KIT'])];e['full_prelaunch_sources']=copy.deepcopy(q['full_prelaunch_sources'])
case('coupled_missing_kit',lambda:coupled_native(no_kit))
def timezonefree(q,e,s):q['requested_UTC']='2026-10-05T08:00:00';e['requested_UTC']=q['requested_UTC']
case('coupled_timezonefree',lambda:coupled_native(timezonefree))
def archived_source_changed():
 cw=OUT/'private_processes/inspect_published';q=json.loads((cw/'request.json').read_bytes());p=Path(q['full_prelaunch_sources'][0]['stored_full_source']['path']);old=p.read_bytes();p.chmod(0o644);p.write_bytes(gzip.compress(b'unrelated source',mtime=0));p.chmod(0o444)
 def modify(q,e,s):q['full_prelaunch_sources'][0]['stored_full_source']=ns['pin'](p);e['full_prelaunch_sources']=copy.deepcopy(q['full_prelaunch_sources'])
 try:return coupled_native(modify)
 finally:p.chmod(0o644);p.write_bytes(old);p.chmod(0o444)
case('coupled_archive_pin_recomputed_but_full_source_wrong',archived_source_changed)
def archived_approval_changed():
 cw=OUT/'private_processes/inspect_published';q=json.loads((cw/'request.json').read_bytes());p=Path(q['full_prelaunch_approvals'][0]['stored_full_source']['path']);old=p.read_bytes();p.chmod(0o644);p.write_bytes(gzip.compress(b'{}',mtime=0));p.chmod(0o444)
 def modify(q,e,s):q['full_prelaunch_approvals'][0]['stored_full_source']=ns['pin'](p);e['full_prelaunch_approvals']=copy.deepcopy(q['full_prelaunch_approvals'])
 try:return coupled_native(modify)
 finally:p.chmod(0o644);p.write_bytes(old);p.chmod(0o444)
case('coupled_approval_pin_recomputed_but_full_bytes_wrong',archived_approval_changed)
case('complete_inspected_chain_after_coupled_restorations',ns['inspected_publication'],True)
published=json.loads((OUT/'inspect_published_receipt.json').read_bytes());case('complete_public_chain_after_coupled_restorations',lambda:ns['verify_public_evidence'](published),True)
# Extract all repository kit definitions without executing the main or imports.
kit=R/'zenodo_deposit_tool/zenodo.py';kns=dict(Path=Path,argparse=argparse,hashlib=hashlib,html=html,http=http,json=json,os=os,re=re,sys=sys,tempfile=tempfile,datetime=datetime,timezone=timezone,HTTPError=HTTPError,URLError=URLError,HTTPRedirectHandler=HTTPRedirectHandler,Request=Request,build_opener=build_opener,quote=quote,urlsplit=urlsplit,ROOT=R,STATE_DIR=SA/'synthetic_kit_state',SECRETS=SA/'NEVER_READ_CREDENTIALS',BASES={'production':'https://zenodo.org','sandbox':'https://sandbox.zenodo.org'},MAX_FILES=100,MAX_BYTES=50*1024**3,CHUNK=1024*1024,USER_AGENT='Math-Zenodo-Deposit-Tool/1.0',MAX_RESPONSE_BYTES=1024*1024)
tree=ast.parse(kit.read_bytes(),filename=str(kit));nodes=[x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))];exec(compile(ast.Module(body=nodes,type_ignores=[]),str(kit),'exec'),kns)
kns['doi_status']=lambda doi:dict(status='not_resolved',http_status=404,synthetic_resolver=True)
metadata,files=kns['load_manifest'](F/'zenodo-deposit.json');rid=published['id'];place=kns['state_path']((F/'zenodo-deposit.json').resolve(),'production');state=dict(manifest=str((F/'zenodo-deposit.json').resolve()),environment='production',id=rid)
class MockClient:
 def __init__(self,mode='normal',submitted=False):self.mode=mode;self.posts=0;self.gets=0;self.submitted=submitted
 def deposit(self):return dict(id=rid,submitted=self.submitted,doi=published['doi'],metadata=copy.deepcopy(metadata),files=[dict(filename=x['name'],filesize=x['size'],checksum=x['md5']) for x in files])
 def get(self,id):
  assert id==rid;self.gets+=1
  if self.mode=='unconfirmed_after_POST' and self.posts:raise kns['DepositError']('mock unavailable readback')
  d=self.deposit()
  if self.mode=='wrong_metadata':d['metadata']['title']='Changed'
  if self.mode=='wrong_checksum':d['files'][0]['checksum']='0'*32
  return d
 def publish(self,id):
  assert id==rid;self.posts+=1;self.submitted=True
  if self.mode in ('lost_POST_response','unconfirmed_after_POST'):raise kns['DepositError']('mock lost response')
CLIENT_OBSERVATIONS=[]
def kit_case(mode='normal',confirm=rid,submitted=False,wantposts=1):
 kns['save_state'](place,state);client=MockClient(mode,submitted);args=argparse.Namespace(manifest=F/'zenodo-deposit.json',sandbox=False,command='publish',confirm_id=confirm)
 try:return kns['run'](args,client)
 finally:
  CLIENT_OBSERVATIONS.append(dict(mode=mode,confirm_id=confirm,initial_submitted=submitted,synthetic_publish_POSTs=client.posts,synthetic_GETs=client.gets));assert client.posts==wantposts
case('kit_normal_exactly_one_POST',kit_case,True)
case('kit_lost_POST_response_confirmed_one_POST',lambda:kit_case('lost_POST_response'),True)
case('kit_lost_POST_response_unconfirmed_stops_after_one_POST',lambda:kit_case('unconfirmed_after_POST'))
case('kit_already_published_zero_POST',lambda:kit_case(submitted=True,wantposts=0),True)
case('kit_wrong_confirm_zero_POST',lambda:kit_case(confirm=rid+1,wantposts=0))
case('kit_wrong_metadata_zero_POST',lambda:kit_case('wrong_metadata',wantposts=0))
case('kit_wrong_checksum_zero_POST',lambda:kit_case('wrong_checksum',wantposts=0))
initial=json.loads((W/'INITIAL_INPUTS.json').read_bytes())
for x in initial['sources']:assert ns['pin'](x['input']['path'])==x['input']
for x in initial['candidate_files']:assert ns['pin'](x['path'])==x
assert not (A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json').exists() and not (A/'publication_actual').exists()
result=dict(UTC=datetime.now(timezone.utc).isoformat(),actual_test_runner_PID=os.getpid(),case_count=len(CASES),cases=CASES,unexpected_dispositions=[x for x in CASES if not x['expected_disposition_observed']],kit_client_observations=CLIENT_OBSERVATIONS,all_transport_and_DOI_observations_are_synthetic=True,full_guard_and_native_evidence_checks_used=True,source_and_all23_public_unchanged=True,publication_clearance=False)
put(W/'CONSISTENT_CASE_RESULTS.json',result);assert not result['unexpected_dispositions'];print(json.dumps(dict(actual_test_runner_PID=os.getpid(),case_count=len(CASES),unexpected_dispositions=0)))
