#!/usr/bin/env python3
"""Independent whole-helper offline controls. Never invokes real service/Git CLIs."""
import ast, copy, datetime as real_datetime, hashlib, importlib.util, json, os
from pathlib import Path
import py_compile, runpy, shutil, socket, subprocess, sys, types, urllib.request, http.client
O=Path(__file__).resolve().parent
R=O.parents[2]
A=R/'audits/pr1156_30003650'
DEPS=['publication_check.py','sweep_io.py','checkpoint.py','audits/pr0399_30001179/ops_binding.py','audits/pr0399_30001179/prepublication_check.py','../zenodo_deposit_tool/zenodo.py']
H='audits/pr1156_30003650/reconcile_external_ledger_v3.py'
P='audits/pr1156_30003650/LEDGER_RECONCILIATION_PLAN.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()

def snapshot():
 root=O/'private/snapshot/research';root.mkdir(parents=True,exist_ok=True)
 for rel in DEPS+[H,P,'raw/pr1156/zenodo_23350364.json']:
  dst=root/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/rel,dst)
 plan=json.loads((R/P).read_text())
 pr=next(p for p in json.loads((R/'rest_inventory.json').read_text())['pull_requests'] if p['number']==1156)
 (root/'rest_inventory.json').write_text(json.dumps({'pull_requests':[pr]}))
 for f in plan['existing_publication']['files']:
  n='raw/pr1156/payload_'+f['sha256']+'.bin';shutil.copyfile(R/n,root/n)
 return root

CASES={
 'valid_append':('pass',1), 'already_exact':('pass',0),
 'project_shadow_and_pyc':('pass',1),'lost_response':('fail',1),'lost_response_recovery':('pass',0),
 'prior_intent_missing_row':('fail',0),'partial_intent':('fail',0),'exclusive_race':('fail',0),
 'immediate_concurrent_row':('fail',0),'immediate_target_row':('fail',0),
 'postappend_extra_row':('fail',1),'postappend_prefix_change':('fail',1),
 'postappend_duplicate':('fail',1),'postappend_missing':('fail',1),
 'preappend_pr_head':('fail',0),'preappend_pr_base':('fail',0),'preappend_pr_body':('fail',0),
 'preappend_pr_state':('fail',0),'preappend_pr_merged':('fail',0),'preappend_pr_draft':('fail',0),
 'expired':('fail',0),'time_reversal':('fail',0),
 'account_wrong':('fail',0),'account_partial':('fail',0),'account_repeat':('fail',0),
 'account_inexact':('fail',0),'account_changed_total':('fail',0),'account_foreign_next':('fail',0),
 'account_loop':('fail',0),'account_files_object':('fail',0),'account_missing_metadata':('fail',0),
 'account_checksum':('fail',0),'account_keyword':('fail',0),'account_encoded_concept':('fail',0),
 'account_short_alias':('fail',0),'account_files_url':('fail',0),'account_pagination':('pass',1),
 'ledger_concept_col0':('fail',0),'ledger_encoded_col1':('fail',0),'ledger_url_col3':('fail',0),
 'ledger_short_alias':('fail',0),'ledger_late_alias':('fail',0),'ledger_lookalike':('fail',0),
 'schema_extra_cell':('fail',0),'schema_header':('fail',0),'sheet_wrong_gid':('fail',0),
 'sheet_wrong_id':('fail',0),'read_wrong_range':('fail',0),'read_wrong_dimension':('fail',0),
 'provider_metadata':('fail',0),'provider_concept':('fail',0),'provider_file':('fail',0),
 'provider_payload':('fail',0),'provider_unpublished':('fail',0),'doi_foreign':('fail',0),
 'response_wrong_sheet':('fail',1),'response_wrong_cells':('fail',1),'response_wrong_row':('fail',1),
 'response_extra_column':('fail',1),'response_wrong_values':('fail',1),
 'acceptance_wrong_sha':('fail',0),'acceptance_not_ready':('fail',0),'acceptance_changed_plan':('fail',0),
 'acceptance_changed_helper':('fail',0),'dependency_changed':('fail',0),'dependency_symlink':('fail',0),
 'dependency_inventory':('fail',0),'review_changed':('fail',0),
 # Probes test boundary assumptions, not advertised required guard expectations.
 'probe_account_top_level_identity':('pass',1),
 'probe_account_record_id':('pass',1),'probe_account_parent_id':('pass',1),
 'probe_account_pids_doi':('pass',1),'probe_plan_read_hash_race':('pass',1),
 'dependency_changes_after_snapshot':('pass',1),'acceptance_missing':('fail',0),
 'lost_response_then_retry':('pass',1),
 'probe_response_update_sheet':('pass',1),'probe_response_echo_range':('pass',1),
 'probe_response_echo_dimension':('pass',1),
 'probe_already_row_after_expiry':('pass',0),
 'probe_already_row_added_unrelated':('pass',0),
 'probe_provider_duplicate_file_key':('pass',1),
}

def worker(name):
 fixture=O/'private/cases'/((str(sys.flags.optimize))+'_'+name)
 fixture.parent.mkdir(parents=True,exist_ok=True)
 if fixture.exists():shutil.rmtree(fixture)
 shutil.copytree(O/'private/snapshot',fixture)
 root=fixture/'research';audit=root/'audits/pr1156_30003650';hp=root/H
 plan=json.loads((root/P).read_text());row=plan['proposed_row'];schema=plan['schema_columns']
 historical=json.loads((root/'rest_inventory.json').read_text())['pull_requests'][0]
 pr={'number':1156,'head':{'sha':plan['head']},'base':{'sha':plan['base']},'body':historical['body'],'state':'open','merged':False,'draft':False}
 provider=json.loads((root/'raw/pr1156/zenodo_23350364.json').read_text())
 before=[schema,['https://example.test/problem','','https://doi.org/10.5281/zenodo.1000','Unrelated result']]
 known={'id':23408971,'metadata':{'title':'Known positive control'},'files':[]}
 account=[known];intent=audit/'LEDGER_RECONCILIATION_INTENT.json'
 if name in {'already_exact','lost_response_recovery','probe_already_row_after_expiry','probe_already_row_added_unrelated'}:before.append(row)
 if name in {'prior_intent_missing_row','lost_response_recovery'}:intent.write_text(json.dumps({'unknown':True}))
 if name=='partial_intent':intent.write_text('{')
 if name=='account_wrong':account=[{**known,'id':1}]
 if name=='account_checksum':account.append({'id':123,'metadata':{},'files':[{'checksum':plan['existing_publication']['files'][0]['checksum']}]})
 if name=='account_keyword':account.append({'id':123,'metadata':{'title':'CP Plus rank'},'files':[]})
 if name=='account_encoded_concept':account.append({'id':123,'metadata':{'identifier':'10.5281%2fzenodo.23350363'},'files':[]})
 if name=='account_short_alias':account.append({'id':123,'metadata':{'identifier':'https://shortdoi.org/abc'},'files':[]})
 if name=='account_files_url':account.append({'id':123,'metadata':{},'files':[{'url':'https://zenodo.org/records/23350363/files/a.pdf'}]})
 if name=='account_files_object':known['files']={}
 if name=='account_missing_metadata':del known['metadata']
 if name=='probe_account_record_id':account.append({'id':23350364,'metadata':{'title':'Uninformative'},'files':[]})
 if name=='probe_account_parent_id':account.append({'id':123,'parent':{'id':'23350363'},'metadata':{'title':'Uninformative'},'files':[]})
 if name=='probe_account_pids_doi':account.append({'id':123,'pids':{'doi':{'identifier':'10.5281/zenodo.23350364'}},'metadata':{'title':'Uninformative'},'files':[]})
 if name=='probe_account_top_level_identity':account.append({'id':123,'doi':'10.5281/zenodo.23350364','conceptrecid':'23350363','metadata':{'title':'Uninformative title'},'files':[]})
 if name=='account_pagination':account.append({'id':123,'metadata':{'title':'Unrelated'},'files':[]})
 cases_cells={'ledger_concept_col0':(0,'https://doi.org/10.5281/zenodo.23350363'), 'ledger_encoded_col1':(1,'10.5281%252fzenodo.23350364'),'ledger_url_col3':(3,'https://zenodo.org/api/records/23350363'), 'ledger_short_alias':(0,'10/abc'),'ledger_lookalike':(3,'https://notzenodo.org/records/23350364')}
 if name in cases_cells:idx,value=cases_cells[name];before[1][idx]=value
 if name=='ledger_late_alias':before[1]=['https://doi.org/10.5281/zenodo.23350364','','','https://shortdoi.org/abc']
 if name=='schema_extra_cell':before[1].append('bad')
 if name=='schema_header':before[0]=['Wrong',*schema[1:]]
 if name=='provider_metadata':provider['metadata']['title']='Changed title'
 if name=='provider_concept':provider['conceptrecid']='23350362'
 if name=='provider_file':provider['files'][0]['checksum']='md5:'+'0'*32
 if name=='provider_unpublished':provider['submitted']=False
 if name=='probe_provider_duplicate_file_key':provider['files'].append(copy.deepcopy(provider['files'][0]))
 acceptance={'dependency_pins':{rel:SHA((root/rel).read_bytes()) for rel in DEPS},'ready_for_existing_publication_record':True,'helper_sha256':SHA(hp.read_bytes()),'plan_sha256':SHA((root/P).read_bytes()),'review_pins':[]}
 if name=='acceptance_not_ready':acceptance['ready_for_existing_publication_record']=False
 if name=='acceptance_changed_helper':acceptance['helper_sha256']='0'*64
 if name=='acceptance_changed_plan':acceptance['plan_sha256']='0'*64
 if name=='dependency_inventory':acceptance['dependency_pins'].pop(DEPS[-1])
 if name=='dependency_changed':(root/'sweep_io.py').write_text('raise RuntimeError("unreviewed source executed")\n')
 if name=='dependency_symlink':
  dep=root/'sweep_io.py';body=dep.read_bytes();dep.unlink();(root/'other.py').write_bytes(body);dep.symlink_to(root/'other.py')
 if name=='review_changed':
  (audit/'review.txt').write_text('changed');acceptance['review_pins']=[{'path':'review.txt','sha256':'0'*64}]
 ab=json.dumps(acceptance).encode();(audit/'ROOT_LEDGER_REVIEW03_ACCEPTANCE.json').write_bytes(ab)
 if name=='acceptance_missing':(audit/'ROOT_LEDGER_REVIEW03_ACCEPTANCE.json').unlink()
 if name=='probe_plan_read_hash_race':
  accepted_plan_bytes=(root/P).read_bytes();mutated=copy.deepcopy(plan)
  row=mutated['proposed_row'];row[3]+=' UNREVIEWED ROW MARKER'
  (root/P).write_text(json.dumps(mutated))
 accepted_sha='0'*64 if name=='acceptance_wrong_sha' else SHA(ab)
 events=[];reads=0;pr_reads=0;account_reads=0;appends=0;rows=copy.deepcopy(before);mock_mutations=[]
 def command(args,**kwargs):
  nonlocal reads,pr_reads,appends,rows
  events.append({'kind':'cli','args':args})
  if args[0]=='git':
   if args[-1:] == ['--show-current']:out='main\n'
   elif 'remote' in args and 'get-url' in args:out='https://github.com/AlecKriebel/Math.git\n'
   else:raise RuntimeError('OFFLINE unexpected Git command')
  elif args[:2]==['gh','api']:
   if args[-1].endswith('/pulls/1156'):
    pr_reads+=1;live=copy.deepcopy(pr)
    if pr_reads==2 and name.startswith('preappend_pr_'):
     prop=name.removeprefix('preappend_pr_')
     if prop in {'head','base'}:live[prop]['sha']='f'*40
     elif prop=='body':live[prop]+=' changed'
     elif prop=='state':live[prop]='closed'
     else:live[prop]=not live[prop]
    out=json.dumps(live)
   elif args[-1].endswith('/git/ref/heads/main'):out=json.dumps({'object':{'sha':'b'*40}})
   else:raise RuntimeError('OFFLINE unexpected GitHub command')
  elif args[:4]==['gws','sheets','spreadsheets','get']:
   info={'spreadsheetId':plan['spreadsheet_id'],'sheets':[{'properties':{'sheetId':1254632077,'title':'Math Puzzles'}}]}
   if name=='sheet_wrong_gid':info['sheets'][0]['properties']['sheetId']=3
   if name=='sheet_wrong_id':info['spreadsheetId']='foreign'
   out=json.dumps(info)
  elif args[:5]==['gws','sheets','spreadsheets','values','get']:
   reads+=1
   if reads==2 and name=='exclusive_race':intent.write_text('{"other_process":true}')
   if reads==2 and name=='immediate_concurrent_row':rows.append(['other','','',''])
   if reads==2 and name=='immediate_target_row':rows.append(row)
   if reads==2 and name=='probe_already_row_added_unrelated':rows.append(['other','','',''])
   data={'range':"'Math Puzzles'!A1:AQ999",'majorDimension':'ROWS','values':rows}
   if name=='read_wrong_range':data['range']="'Math Puzzles'!A1:D999"
   if name=='read_wrong_dimension':data['majorDimension']='COLUMNS'
   out=json.dumps(data)
  elif args[:5]==['gws','sheets','spreadsheets','values','append']:
   appends+=1;mock_mutations.append('offline GWS append')
   params=json.loads(args[args.index('--params')+1]);payload=json.loads(args[args.index('--json')+1])
   if params!={'spreadsheetId':plan['spreadsheet_id'],'range':plan['range'],'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True} or payload!={'majorDimension':'ROWS','values':[row]}:raise RuntimeError('Unexpected append request')
   rows.append(row);rn=len(rows)
   response={'spreadsheetId':plan['spreadsheet_id'],'tableRange':f"'Math Puzzles'!A1:D{rn-1}",'updates':{'spreadsheetId':plan['spreadsheet_id'],'updatedCells':4,'updatedRows':1,'updatedColumns':4,'updatedRange':f"'Math Puzzles'!A{rn}:D{rn}",'updatedData':{'range':f"'Math Puzzles'!A{rn}:D{rn}",'majorDimension':'ROWS','values':[row]}}}
   if name=='probe_response_update_sheet':response['updates']['spreadsheetId']='foreign'
   if name=='probe_response_echo_range':response['updates']['updatedData']['range']="'Wrong Sheet'!A999:D999"
   if name=='probe_response_echo_dimension':response['updates']['updatedData']['majorDimension']='COLUMNS'
   if name in {'lost_response','lost_response_then_retry'}:raise subprocess.CalledProcessError(1,args,output='',stderr='offline lost response')
   if name=='postappend_extra_row':rows.append(['other','','',''])
   if name=='postappend_prefix_change':rows[1][0]='changed'
   if name=='postappend_duplicate':rows.append(row)
   if name=='postappend_missing':rows.pop()
   if name=='response_wrong_sheet':response['spreadsheetId']='foreign'
   if name=='response_wrong_cells':response['updates']['updatedCells']=5
   if name=='response_wrong_row':response['updates']['updatedRange']="'Math Puzzles'!A999:D999"
   if name=='response_extra_column':response['updates']['updatedColumns']=5
   if name=='response_wrong_values':response['updates']['updatedData']['values']=[row+['extra']]
   out=json.dumps(response)
  else:raise RuntimeError('OFFLINE unexpected command '+repr(args))
  return subprocess.CompletedProcess(args,0,out if kwargs.get('text') else out.encode(),'' if kwargs.get('text') else b'')
 def check_output(args,**kwargs):return command(args,**kwargs).stdout
 class Response:
  status=200;url=''
  def __init__(self,body,url=''):self.body=body;self.url=url
  def read(self,*args):return self.body
  def __enter__(self):return self
  def __exit__(self,*args):pass
 def urlopen(request,**kwargs):
  url=request.full_url;events.append({'kind':'public_GET','url':url})
  if url=='https://zenodo.org/api/records/23350364':return Response(json.dumps(provider).encode(),url)
  if url==row[2]:return Response(b'', 'https://foreign.test/records/23350364' if name=='doi_foreign' else 'https://zenodo.org/records/23350364')
  for f in plan['existing_publication']['files']:
   actual=next(x for x in provider['files'] if x['key']==f['name'])
   if url==actual['links']['self']:
    b=(root/'raw/pr1156'/('payload_'+f['sha256']+'.bin')).read_bytes()
    if name=='provider_payload':b=b'altered'
    return Response(b,url)
  raise RuntimeError('OFFLINE unexpected public URL '+url)
 class HTTPSConnection:
  def __init__(self,host,**kwargs):
   if host!='zenodo.org':raise RuntimeError('OFFLINE foreign account host')
  def putrequest(self,method,path):
   self.path=path
   if method!='GET' or not path.startswith('/api/user/records?'):raise RuntimeError('OFFLINE forbidden authenticated method/path')
   events.append({'kind':'account_GET','path':path})
  def putheader(self,*args):pass
  def endheaders(self):pass
  def send(self,*args):raise RuntimeError('OFFLINE forbidden HTTP body')
  def close(self):pass
  def getresponse(self):
   nonlocal account_reads
   account_reads+=1;records=account;total=len(account);links={}
   if name in {'account_pagination','account_changed_total'}:
    if account_reads==1:records=account[:1];links={'next':'https://zenodo.org/api/user/records?page=2'};total=2
    else:records=account[1:];total=3 if name=='account_changed_total' else 2
   if name=='account_partial':total+=1
   if name=='account_repeat':records=[*account,*account];total=2
   if name=='account_inexact':total={'value':len(account),'relation':'gte'}
   if name=='account_foreign_next':links={'next':'https://foreign.test/api/user/records'}
   if name=='account_loop':links={'next':'https://zenodo.org/api/user/records?q=&size=25'}
   return Response(json.dumps({'hits':{'total':total,'hits':records},'links':links}).encode())
 class Clock(real_datetime.datetime):
  ticks=0
  @classmethod
  def now(cls,tz=None):
   cls.ticks+=1;base=real_datetime.datetime(2026,10,22,tzinfo=real_datetime.timezone.utc)
   if name in {'expired','probe_already_row_after_expiry'}:return base+real_datetime.timedelta(seconds=181 if cls.ticks>=3 else 0)
   if name=='time_reversal':return base-real_datetime.timedelta(seconds=1 if cls.ticks>=3 else 0)
   return base
 def deny(*args,**kwargs):raise RuntimeError('OFFLINE blocked unmocked external operation')
 subprocess.run=command;subprocess.check_output=check_output;subprocess.Popen=deny
 socket.socket=deny;socket.create_connection=deny;http.client.HTTPSConnection=HTTPSConnection;urllib.request.urlopen=urlopen
 real_datetime.datetime=Clock
 os.environ['ZENODO_TOKEN']='OFFLINE_DUMMY_NEVER_TRANSMITTED';os.environ.pop('ZENODO_SANDBOX_TOKEN',None)
 if name=='exclusive_race':
  original_open=os.open
  def race_open(path,flags,*args,**kwargs):
   if Path(path)==intent and flags&os.O_EXCL:intent.write_text('{"other_process":true}')
   return original_open(path,flags,*args,**kwargs)
  os.open=race_open
 if name in {'probe_plan_read_hash_race','dependency_changes_after_snapshot'}:
  original_read_bytes=Path.read_bytes
  def racing_read_bytes(path):
   result=original_read_bytes(path)
   if name=='probe_plan_read_hash_race' and path==audit/'ROOT_LEDGER_REVIEW03_ACCEPTANCE.json':(root/P).write_bytes(accepted_plan_bytes)
   if name=='dependency_changes_after_snapshot' and path==root/'../zenodo_deposit_tool/zenodo.py':(root/'sweep_io.py').write_text('raise RuntimeError("UNREVIEWED MUTATED SOURCE EXECUTED")\n')
   return result
  Path.read_bytes=racing_read_bytes
 if name=='project_shadow_and_pyc':
  for module in ['sweep_io','checkpoint','zenodo','ops_binding','publication_check','pr1156_account_reader_final']:
   poison=types.ModuleType(module);poison.__getattr__=lambda n:(_ for _ in ()).throw(RuntimeError('POISON MODULE USED'));sys.modules[module]=poison
  shadow=root/'shadow';shadow.mkdir();sys.path.insert(0,str(shadow))
  for module in ['sweep_io','checkpoint','zenodo','ops_binding','publication_check']:
   src=shadow/(module+'.py');src.write_text('raise RuntimeError("SHADOW SOURCE OR PYC EXECUTED")\n');py_compile.compile(str(src),doraise=True)
 sys.argv=[str(hp),'--acceptance-sha256',accepted_sha]
 from contextlib import redirect_stdout
 import io
 captured=io.StringIO();error=None
 try:
  with redirect_stdout(captured):runpy.run_path(str(hp),run_name='__main__')
 except BaseException as exc:error=type(exc).__name__+': '+str(exc)
 first_error=None
 if name=='lost_response_then_retry':
  first_error=error;error=None
  try:
   with redirect_stdout(captured):runpy.run_path(str(hp),run_name='__main__')
  except BaseException as exc:error=type(exc).__name__+': '+str(exc)
 receipt_path=audit/'LEDGER_PUBLICATION_VERIFICATION.json';receipt=json.loads(receipt_path.read_text()) if receipt_path.exists() else None
 result={'case':name,'optimization':sys.flags.optimize,'outcome':'fail' if error else 'pass','error':error,'first_error':first_error,'mock_append_count':appends,'intent_exists':intent.exists(),'receipt':receipt,'events':events,'real_external_side_effects':0,'fixture_root':str(root)}
 expected=CASES[name];result['expected_outcome']=expected[0];result['expected_append_count']=expected[1];result['expectations_met']=result['outcome']==expected[0] and appends==expected[1]
 print(json.dumps(result))
 # Full receipts are returned above; each fresh fixture is disposable, source snapshot retained.
 shutil.rmtree(fixture)

if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='--worker':worker(sys.argv[2])
 else:
  snapshot();results=[]
  for mode in [[],['-O'],['-OO']]:
   for name in CASES:
    completed=subprocess.run([sys.executable,*mode,str(Path(__file__).resolve()),'--worker',name],capture_output=True,text=True,check=True)
    value=json.loads(completed.stdout);results.append(value)
  (O/'OFFLINE_CONTROL_RESULTS.json').write_text(json.dumps({'scope':'Exact copied helper and dependencies; mocked CLI and full network; zero real external side effects','results':results,'all_expectations_met':all(v['expectations_met'] for v in results)},indent=2)+'\n')
  print(json.dumps({'controls':len(results),'all_expectations_met':all(v['expectations_met'] for v in results),'unexpected':[{'case':v['case'],'optimization':v['optimization'],'outcome':v['outcome'],'error':v['error'],'mock_append_count':v['mock_append_count']} for v in results if not v['expectations_met']]},indent=2))
