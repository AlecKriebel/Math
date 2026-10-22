"""Independent fake transports exercise unmodified production logic; no service access.
Only remap filesystem constants into isolated world. Every dependency was read first.
Large immutable payload captures use hard links; pinned originals are never modified.
"""
from pathlib import Path
import contextlib,copy,datetime,hashlib,importlib.util,io,json,os,shutil,subprocess,sys,urllib.error,urllib.request
from unittest.mock import patch
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
A=R.parent/'existing_publication_batch_b1_plus1198'
W=R/'private'/('world_'+('OO' if sys.flags.optimize==2 else 'O' if sys.flags.optimize else 'normal'))
W.mkdir(parents=True,exist_ok=False)
def check(condition,message):
 if not condition:raise RuntimeError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
P=json.loads((A/'PROPOSAL.json').read_bytes());PB=(A/'PROPOSAL.json').read_bytes()
index={}
for name,digest in P['input_pins'].items():
 src=A/name;dst=W/name;dst.parent.mkdir(parents=True,exist_ok=True)
 if src.suffix=='.py':shutil.copyfile(src,dst)
 else:os.link(src,dst)
 index.setdefault(digest,src)
for name in ['PROPOSAL.json','ops_core.py']:
 if not (W/name).exists():shutil.copyfile(A/name,W/name)
original_write=Path.write_bytes
# Avoid allocating another PDF per fake call; preserve exact captured bytes/path.
def compact_write(path,data):
 if path.is_relative_to(W) and path.suffix in {'.bin','.stdout'} and len(data)>4096:
  digest=sha(data);src=index.get(digest)
  if src is not None and src!=path:
   os.link(src,path);return len(data)
  result=original_write(path,data);index[digest]=path;return result
 return original_write(path,data)
sys.path.insert(0,str(A))
with patch('subprocess.run',side_effect=RuntimeError('Import process')),patch('urllib.request.urlopen',side_effect=RuntimeError('Import network')):
 spec=importlib.util.spec_from_file_location('independently_reviewed_runner',A/'append_reviewed_rows.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
 import ops_core as core
 runner.load_numeric()
runner.HERE=W;runner.PLAN=W/'PROPOSAL.json';runner.HELPER=W/'frozen/reconcile_existing_row.py'
basekeys,intrakeys=runner.clearance_keys(P)
ready={'ready_for_execution':True,'reviewed_plan_sha256':sha(PB),'reviewed_runner_sha256':sha((A/'append_reviewed_rows.py').read_bytes()),'reviewed_core_sha256':runner.CORE_SHA,'approved_semantic_clearance_keys':basekeys,'approved_intrabatch_clearance_keys':intrakeys}
for key,role in [('root_action_acceptance','root_action_adoption'),('fresh_independent_action_review','independent_action_review')]:
 obj={'MOCK_ONLY':True,'action_review_accepted':True,'plan_sha256':sha(PB),'runner_sha256':ready['reviewed_runner_sha256'],'core_sha256':runner.CORE_SHA,'row_count':16,'new_publications':0,'native_write_attempt_limit':1,'approved_semantic_clearance_keys':basekeys,'approved_intrabatch_clearance_keys':intrakeys,role:True}
 name=key+'.json';(W/name).write_text(json.dumps(obj));ready[key]={'accepted':True,'path':name,'sha256':sha((W/name).read_bytes())}
runner.READINESS=W/'READINESS.json';runner.READINESS.write_text(json.dumps(ready));readybytes=runner.READINESS.read_bytes()
BASE=json.loads((A/'private_readonly/ledger_preparation02/02.stdout').read_bytes())['valueRanges'][0]['valueRange']['values'];SHEET=P['preparation_ledger']['sheet_metadata']
GETS={};PRS={}
for i in P['items']:
 if i['pr']!=1198:
  GETS[i['registry_url']]=(A/i['fresh_registry_path'],200,i['registry_url'])
  GETS['https://doi.org/'+i['doi']]=(None,200,i['reviewed_doi_final_url'])
  GETS[i['selected_source']['url']]=(A/i['selected_source']['reviewed_path'],200,i['selected_source']['url'])
 else:
  for name,url in [('record','https://zenodo.org/api/records/23165876'),('concept_record','https://zenodo.org/api/records/23127198'),('version_registry','https://api.datacite.org/dois/'+i['version_doi']),('concept_registry','https://api.datacite.org/dois/'+i['concept_doi'])]:GETS[url]=(A/'private_inputs/fresh'/('pr1198_'+name+'.json'),200,url)
  GETS['https://doi.org/'+i['concept_doi']]=(None,200,'https://zenodo.org/records/23165876')
  GETS['https://doi.org/'+i['version_doi']]=(None,404,'https://doi.org/'+i['version_doi'])
  import urllib.parse
  for f in i['expected_payloads']:
   u='https://zenodo.org/api/records/23165876/files/'+urllib.parse.quote(f['name'],safe='')+'/content';GETS[u]=(A/'private_inputs/p1198/private_sources'/f['name'],200,u)
 for bind in i['pr_bindings']:PRS[bind['pr']]=(A/'private_readonly/preparation01'/('pr'+str(bind['pr'])+'_live.stdout')).read_bytes()
class Response:
 def __init__(self,data,status,url):self.data=data;self.status=status;self.url=url;self.headers={'Content-Type':'application/octet-stream'}
 def __enter__(self):return self
 def __exit__(self,*a):pass
 def read(self):return self.data
class World:
 def __init__(self,name,issue=None):
  self.name=name;self.issue=issue;self.rows=copy.deepcopy(BASE);self.writes=0;self.gets=[];self.prs=[];self.cli=[];self.fsyncs=0;self.before_writes_fsyncs=None;self.case=W/'private_action'/name
  if issue in {'bare_arxiv_duplicate','bare_arxiv_pdf_duplicate'}:self.rows.append(['Already entered paper','','https://arxiv.org/'+('abs/1712.09148' if issue=='bare_arxiv_duplicate' else 'pdf/1712.09148v1'),''])
  if issue=='new_author':self.rows.append(['Unreviewed row','','','Cao'])
  if issue=='new_catalog43':self.rows.append(['Different row','','','']+['']*38+['30005421'])
  if issue=='new_source':self.rows.append(['Different row','','','OWR-8415354-004'])
  if issue=='new_concept':self.rows.append(['Different row','','','https://zenodo.org/records/23127199'])
 def urlopen(self,request,timeout=None):
  check(request.get_method()=='GET','NonGET request');check(request.get_header('User-agent')==core.UA,'Missing UA');url=request.full_url;check(url in GETS,'Unscheduled GET '+url)
  path,status,final=GETS[url];data=path.read_bytes() if path else b'fake resolver body';self.gets.append(url)
  if self.issue=='unknown1198' and url=='https://zenodo.org/api/records/23165876':
   obj=json.loads(data);obj['unreviewed_unknown_field']={'x':1};data=json.dumps(obj).encode()
  if self.issue=='advance1198' and url=='https://doi.org/10.5281/zenodo.23127198':final='https://zenodo.org/records/99999999'
  if self.issue=='unknown_registry' and url==P['items'][0]['registry_url']:
   obj=json.loads(data);obj['message']['unreviewed_reference']='altered';data=json.dumps(obj).encode()
  if self.issue=='pdf_changed' and url==P['items'][0]['selected_source']['url']:data+=b'x'
  if self.issue=='http403' and url==P['items'][0]['registry_url']:status=403
  if self.issue=='version200' and url=='https://doi.org/10.5281/zenodo.23165876':status=200
  if status!=200:raise urllib.error.HTTPError(url,status,'fake HTTP',{},io.BytesIO(data))
  return Response(data,status,final)
 def process(self,command,capture_output=False):
  if command[:2]==['gh','api']:
   n=int(command[2].rsplit('/',1)[1]);check(n in PRS,'Unexpected PR');self.prs.append(n);raw=PRS[n]
   if self.issue=='pr1176_body' and n==1176:
    v=json.loads(raw);v['body']=(v.get('body') or '')+' changed';raw=json.dumps(v).encode()
   return subprocess.CompletedProcess(command,0,raw,b'')
  check(command[:3]==['gws','sheets','spreadsheets'],'Unexpected externalprocess')
  parts=command[3:command.index('--params')];params=json.loads(command[command.index('--params')+1]);check(params['spreadsheetId']==runner.BOOK,'Wrong workbook');self.cli.append(parts)
  if parts==['get']:
   sheet=copy.deepcopy(SHEET)
   if self.issue=='metadata_drift' and len(self.cli)>=4:sheet['gridProperties']['rowCount']+=1
   obj={'spreadsheetId':runner.BOOK,'sheets':[{'properties':sheet}]}
  elif parts==['values','batchGetByDataFilter']:
   body=json.loads(command[command.index('--json')+1]);check(body['dataFilters']==[{'gridRange':{'sheetId':runner.GID}}],'Filter not numeric/full');check(body['majorDimension']=='ROWS','Wrong dimension');rows=copy.deepcopy(self.rows)
   if self.issue=='formula' and body['valueRenderOption']=='FORMULA':rows[1][0]='=HYPERLINK("x")'
   obj={'spreadsheetId':runner.BOOK,'valueRanges':[{'dataFilters':body['dataFilters'],'valueRange':{'range':"'Math Puzzles'!A1:AQ"+str(SHEET['gridProperties']['rowCount']),'majorDimension':'ROWS','values':rows}}]}
  elif parts==['batchUpdate']:
   check(self.case.exists() and (self.case/'INTENT.json').is_file() and (self.case/'WRITE_ATTEMPTED.json').is_file(),'Nondurable write');self.before_writes_fsyncs=self.fsyncs;check(self.fsyncs>=12,'Missing fsync durability');self.writes+=1;check(self.writes==1,'Write retry')
   body=json.loads(command[command.index('--json')+1]);check(body==json.loads((self.case/'INTENT.json').read_bytes())['request'],'Intent/request mismatch')
   check(len(body['requests'])==1,'Multiple requests');append=body['requests'][0]['appendCells'];check(append['sheetId']==runner.GID and append['fields']=='userEnteredValue','Bad append target/fields')
   added=[]
   for row in append['rows']:
    check(len(row['values'])==4,'Wrong number cells');values=[]
    for c in row['values']:check(set(c)=={'userEnteredValue'} and set(c['userEnteredValue'])=={'stringValue'},'Nonliteral cell');values.append(c['userEnteredValue']['stringValue'])
    added.append(values)
   check(added==[i['row'] for i in P['items']],'Rows changed');self.rows+=added
   if self.issue=='unknown_write':return subprocess.CompletedProcess(command,1,b'',b'unknown outcome after accepted fake write')
   if self.issue=='malformed_write':return subprocess.CompletedProcess(command,0,b'not JSON',b'')
   if self.issue=='old43':self.rows[1]+=['']*(43-len(self.rows[1]));self.rows[1][42]='changed'
   if self.issue=='gap':self.rows.insert(len(BASE),[])
   if self.issue=='reverse':self.rows[-16:]=self.rows[-16:][::-1]
   if self.issue=='duplicate':self.rows.append(copy.deepcopy(self.rows[-1]))
   obj={'spreadsheetId':runner.BOOK,'replies':[{}] if self.issue!='bad_reply' else [{'bad':True}]}
  else:raise RuntimeError('Unexpected command '+str(parts))
  return subprocess.CompletedProcess(command,0,json.dumps(obj).encode(),b'')
def execute(name,issue=None,mode='--execute-reviewed'):
 world=World(name,issue);runner.CASE=world.case;runner.READINESS.write_bytes(readybytes);error=None;output=io.StringIO();original_fsync=os.fsync
 def fsync(fd):world.fsyncs+=1;return original_fsync(fd)
 original_durable=None
 # Use unmodified verify_inputs/publication/clearance/numeric functions, not stubs.
 with patch('subprocess.run',side_effect=world.process),patch('urllib.request.urlopen',side_effect=world.urlopen),patch('os.fsync',side_effect=fsync),patch.object(Path,'write_bytes',new=compact_write),contextlib.redirect_stdout(output):
  try:runner.main(mode)
  except BaseException as ex:error=type(ex).__name__+': '+str(ex)
  oldwrites=world.writes
  if world.case.exists():
   try:runner.main('--execute-reviewed')
   except core.GateError as ex:check('Existing actionCASE' in str(ex),'Wrong rerun rejection')
   else:raise RuntimeError('Rerun accepted')
   check(world.writes==oldwrites,'Rerun attempted write')
 result={'name':name,'issue':issue,'mode':mode,'error':error,'get_calls':len(world.gets),'pr_calls':len(world.prs),'gws_calls':world.cli,'write_attempts':world.writes,'case_exists':world.case.exists(),'fsyncs_before_write':world.before_writes_fsyncs,'receipt_exists':(world.case/'RECONCILIATION.json').exists(),'all_publication_logic_executed':len(world.gets)==54 and len(world.prs)==17}
 (W/(name+'_execution.json')).write_text(json.dumps(result,indent=2)+'\n');(W/(name+'_stdout.txt')).write_text(output.getvalue())
 return result
results=[]
for name,issue,expected_write,expected_receipt in [('baseline',None,1,True),('bare_arxiv_duplicate','bare_arxiv_duplicate',1,True),('bare_arxiv_pdf_duplicate','bare_arxiv_pdf_duplicate',1,True),('new_author','new_author',0,False),('new_catalog43','new_catalog43',0,False),('new_source','new_source',0,False),('new_concept','new_concept',0,False),('unknown1198','unknown1198',0,False),('advance1198','advance1198',0,False),('unknown_registry','unknown_registry',0,False),('pdf_changed','pdf_changed',0,False),('pr1176_body','pr1176_body',0,False),('http403','http403',0,False),('version200','version200',0,False),('formula','formula',0,False),('metadata_drift','metadata_drift',0,False),('unknown_write','unknown_write',1,False),('malformed_write','malformed_write',1,False),('old43','old43',1,False),('gap','gap',1,False),('reverse','reverse',1,False),('duplicate','duplicate',1,False),('bad_reply','bad_reply',1,False)]:
 result=execute(name,issue);check(result['write_attempts']==expected_write and result['receipt_exists']==expected_receipt,'Unexpected control result '+repr(result));results.append(result)
result=execute('readonly',mode='--readonly-preflight');check(result['write_attempts']==0 and not result['case_exists'] and result['error'] is None,'Readonly wrote/failed');results.append(result)
# Actual readiness-false rejection, with no provider access.
runner.READINESS=A/'READINESS.json';runner.CASE=W/'private_action/readiness_false'
with patch('subprocess.run',side_effect=RuntimeError('Unexpected service call')),patch('urllib.request.urlopen',side_effect=RuntimeError('Unexpected GET')):
 try:runner.main('--execute-reviewed')
 except core.GateError as ex:check('Not ready' in str(ex),'False readiness wrong failure')
 else:raise RuntimeError('Actual false readiness accepted')
# Pure identity function controls are explicitly distinguished from full main runs.
park=next(i for i in P['items'] if i['pr']==1058)
identity=[]
for text in ['https://arxiv.org/abs/1712.09148','https://arxiv.org/pdf/1712.09148v1','https://doi.org/10.48550/arXiv.1712.09148','https://arxiv.org/abs/1712.09148v1']:
 hits=core.identity_hits([P['schema'],['Existing result','',text,'']],park);identity.append({'text':text,'hits':hits})
check([bool(x['hits']) for x in identity]==[False,False,True,False],'Alias counterexample not reproduced')
retry=[]
for sequence in [[429,502,200],[503,504,200],[429,429,429],[403],[404],[500]]:
 calls=[];delays=[]
 def get(request,timeout=None):
  check(request.get_method()=='GET','Retry not GET');status=sequence[len(calls)];calls.append(status)
  if status==200:return Response(b'ok',status,'https://example.invalid/')
  raise urllib.error.HTTPError(request.full_url,status,'fake',{},io.BytesIO(b'error'))
 err=None
 with patch('urllib.request.urlopen',side_effect=get),patch('time.sleep',side_effect=delays.append):
  try:core.read_url('https://example.invalid/',W/'retry'/str(len(retry)),'r')
  except core.GateError as ex:err=str(ex)
 check(calls==sequence,'Retry count/status drift');retry.append({'sequence':calls,'delays':delays,'error':err})
# Narrow Springer canonicalization, no network involved.
doi='10.1007/s00031-020-09589-x';u='https://link.springer.com/article/'+doi+'?error=cookies_not_supported&code=ead1103a-cef4-497c-bb6c-628a9dda5656';v=u.replace('ead1103a','9ad1103a')
check(core.resolver_identity(u,doi)==core.resolver_identity(v,doi),'UUID canonicalization failed')
for bad in [v+'&unknown=1',v+'&code=ead1103a-cef4-497c-bb6c-628a9dda5656',v.replace('https://','http://'),v.replace('link.springer.com','evil.invalid'),v+'#x',v.replace('09589-x','09589-y'),v.replace('cookies_not_supported','other_error')]:check(core.resolver_identity(bad,doi)==bad,'Overbroad canonicalization')
check(not (A/'private_action/action01').exists(),'Production case created');check(json.loads((A/'READINESS.json').read_bytes())['ready_for_execution'] is False,'Production readiness changed')
summary={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'optimization':sys.flags.optimize,'status':'HOLD_REPRODUCED_MISSING_ARXIV_ALIAS','production_case_absent':True,'production_readiness_false':True,'real_external_calls':0,'real_service_writes':0,'full_actual_runner_cases':results,'pure_identity_controls':identity,'pure_retry_controls':retry,'source_replacements':'Only isolated HERE/PLAN/HELPER/CASE/READINESS constants; production algorithms and frozen hashes unmodified; synthetic approval JSON is MOCK_ONLY.','large_capture_storage':'Hard links retain exact payload bytes without allocating repeated PDFs.'}
(R/('CONTROLS_'+('OO' if sys.flags.optimize==2 else 'O' if sys.flags.optimize else 'normal')+'.json')).write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({'status':summary['status'],'optimization':sys.flags.optimize,'full_cases':len(results),'writes_real':0,'counterexample_full_gates':results[1]['all_publication_logic_executed']}))
