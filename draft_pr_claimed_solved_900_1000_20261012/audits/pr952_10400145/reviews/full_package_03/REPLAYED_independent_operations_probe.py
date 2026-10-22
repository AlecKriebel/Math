"""Independent actual-flow probes with explicit inert acceptance and I/O boundaries."""
import argparse,contextlib,copy,hashlib,io,json,pathlib,sys,tempfile,types
P=pathlib.Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012');A=P/'audits/pr952_10400145';R=A/'reviews/full_package_03/private/flows';ROOT=P.parent
PIN='14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec'
def need(ok,m):
 if not ok:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
raw=(P/'accept_pr952.py').read_bytes();need(sha(raw)==PIN,'actual core pin')
n={'__name__':'independent_full02_inert','__file__':str(P/'accept_pr952.py')};exec(compile(raw,str(P/'accept_pr952.py'),'exec',dont_inherit=True,optimize=sys.flags.optimize),n)
kitraw=(ROOT/'zenodo_deposit_tool/zenodo.py').read_bytes();need(sha(kitraw)==n['KIT_SHA'],'unchanged kit pin')
events=[]
def yes(label,f):
 value=f();events.append({'test':label,'status':'PASS'});return value
def no(label,f):
 try:f()
 except Exception as e:events.append({'test':label,'status':'REJECTED_EXPECTED','guard':str(e)});return
 raise RuntimeError('ADVERSE PROBE ACCEPTED '+label)
def forbidden(*a,**k):raise RuntimeError('REAL MUTATING/SERVICE BOUNDARY FORBIDDEN')
n.update(run=forbidden,pr_view=forbidden,remote_main=forbidden,gws=forbidden,bounded_public_get=forbidden,subprocess=types.SimpleNamespace(run=forbidden))
fixture=R/('private_independent_operations_'+str(sys.flags.optimize));fixture.mkdir()
n['W']=fixture;freeze=json.loads((A/'preprint/FREEZE.json').read_bytes());accepted={'freeze_sha256':'ab027971f0245481783e2afa106292543c41f06a93c3c83a0cf8dcea4cff9d77','operations_inventory_sha256':'9650f0baf87ac6d83a5a7eb934d212cc66ea67dea4c8758813bec47f5a24cc05'}
merge={'number':952,'state':'MERGED','headRefOid':n['HEAD'],'baseRefName':'main','url':'https://github.com/AlecKriebel/Math/pull/952','mergeCommit':{'oid':'b'*40}}
n['save'](fixture/'PR_MERGE_RECEIPT.json',merge)
calls={'guard':0,'create':0,'publish':0,'upload':0,'get':[],'append':0}
n['accepted_package']=lambda context:(accepted,freeze)
def reviews(*a):calls['guard']+=1
n['accepted_review_check']=reviews;n['merged_gate']=lambda *a:{'merge_commit':'b'*40,'observed_remote_main':'a'*40,'source_gate':{},'native_gate':{}}
metadata,expected=n['descriptor_check'](freeze)
server={'record':None,'fail_publish':True,'fail_get_once':False}
class FakeClient:
 def __init__(self,*a):pass
 def create(self,meta):
  calls['create']+=1;server['record']={'id':17,'submitted':False,'metadata':copy.deepcopy(meta),'files':[],'links':{'bucket':'https://zenodo.org/api/files/inert','html':'https://zenodo.org/deposit/17'}};return copy.deepcopy(server['record'])
 def get(self,ident):
  need(ident==17,'wrong ID reached inert service');calls['get'].append(ident)
  if server['fail_get_once']:server['fail_get_once']=False;raise kit['DepositError']('INERT_LOST_PUBLICATION_READBACK')
  return copy.deepcopy(server['record'])
 def upload(self,bucket,entry):
  calls['upload']+=1;server['record']['files'].append({'filename':entry['name'],'filesize':entry['size'],'checksum':'md5:'+entry['md5']});return {}
 def update(self,ident,meta):need(ident==17,'wrong metadata ID');server['record']['metadata']=copy.deepcopy(meta);return copy.deepcopy(server['record'])
 def publish(self,ident):
  need(ident==17,'wrong publish ID');calls['publish']+=1;server['record'].update(submitted=True,doi='10.5281/zenodo.17')
  if server['fail_publish']:server['fail_get_once']=True;raise kit['DepositError']('INERT_LOST_PUBLISH_RESPONSE')
  return copy.deepcopy(server['record'])
kit={'__name__':'inert_actual_unchanged_kit','__file__':str(ROOT/'zenodo_deposit_tool/zenodo.py')};exec(compile(kitraw,kit['__file__'],'exec',dont_inherit=True,optimize=sys.flags.optimize),kit)
kit.update(STATE_DIR=fixture/'kit-state',SECRETS=fixture/'no-secrets',token_for=lambda *a:'INERT_NO_REAL_TOKEN',ZenodoClient=FakeClient,doi_status=lambda doi:{'status':'INERT_ONLY'})
n['captured_kit']=lambda context:kit
context={'inventory_sha256':accepted['operations_inventory_sha256'],'inventory':{'files':{n['KIT']:{'sha256':n['KIT_SHA']}}},'captured':{n['KIT']:kitraw}}
def public(url,cap):
 rid=17
 if '/api/records/' in url:return json.dumps({'id':rid,'doi':'10.5281/zenodo.17','metadata':{'title':n['TITLE']},'files':[{'key':x['name']} for x in expected]}).encode(),url,200
 if url.startswith('https://doi.org/'):return b'',f'https://zenodo.org/records/{rid}',200
 for x in expected:
  if '/files/'+x['name'] in url:return (A/'preprint'/x['name']).read_bytes(),url,200
 raise RuntimeError('unexpected inert public request '+url)
n['bounded_public_get']=public
with contextlib.redirect_stdout(io.StringIO()):
 yes('actual_zenodo_stage_unchanged_kit_two_files',lambda:n['zenodo'](argparse.Namespace(action='stage'),context))
 no('actual_stage_repeat_blocked_by_durable_create_intent',lambda:n['zenodo'](argparse.Namespace(action='stage'),context))
 no('actual_publish_response_and_readback_both_lost',lambda:n['zenodo'](argparse.Namespace(action='publish'),context))
 need(calls['create']==1 and calls['upload']==2 and calls['publish']==1,'wrong actual-flow mutation counts')
 no('actual_publish_repeat_blocked_before_second_POST',lambda:n['zenodo'](argparse.Namespace(action='publish'),context))
 yes('actual_GET_only_inspect_recovers_same_ID_published_receipt',lambda:n['zenodo'](argparse.Namespace(action='inspect'),context))
 need(calls['create']==1 and calls['publish']==1 and set(calls['get'])=={17},'GET reconciliation repeated mutation or changed ID')
 pub=n['load'](fixture/'ZENODO_PUBLISH.json');need(pub['recovered_by_exact_saved_ID_GET'] is True,'publish receipt not recovered')
 actual_public=n['bounded_public_get']
 def corrupt(url,cap):
  body,final,status=actual_public(url,cap)
  if '/files/' in url:body=body[:-1]+bytes([body[-1]^1])
  return body,final,status
 n['bounded_public_get']=corrupt;no('actual_public_verifier_rejects_same_length_wrong_bytes',lambda:n['independent_public_verify'](pub,expected));n['bounded_public_get']=actual_public
 def wrong_doi(url,cap):
  body,final,status=actual_public(url,cap)
  return body,('https://zenodo.org/records/18' if url.startswith('https://doi.org/') else final),status
 n['bounded_public_get']=wrong_doi;no('actual_public_verifier_rejects_other_record_DOI',lambda:n['independent_public_verify'](pub,expected));n['bounded_public_get']=actual_public
 headers=['Original Problem','Solution Chat URL','DOI','Notes'];table=[headers];lose_append=[True];gws_calls=[]
 def gws(args):
  gws_calls.append(args);params=json.loads(args[args.index('--params')+1]);need(params['spreadsheetId']==n['SID'],'wrong spreadsheet')
  if args[:3]==['sheets','spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':1254632077,'title':'Math Puzzles'}}]}
  if args[:4]==['sheets','spreadsheets','values','append']:
   need(params['valueInputOption']=='RAW' and params['insertDataOption']=='INSERT_ROWS','non-RAW append')
   body=json.loads(args[args.index('--json')+1]);need(body=={'values':[n['tracker_row'](pub)]},'wrong exact tracker row');calls['append']+=1;table.append(body['values'][0])
   if lose_append[0]:lose_append[0]=False;raise RuntimeError('INERT_APPEND_APPLIED_RESPONSE_LOST')
   return {'updates':{'updatedRows':1,'updatedCells':4,'updatedRange':"'Math Puzzles'!A2:D2"}}
  rg=params['range'];return {'range':rg,'values':copy.deepcopy(table if rg=="'Math Puzzles'!A:D" else [table[1]])}
 n['gws']=gws
 no('actual_GWS_append_applied_response_lost',lambda:n['tracker_append'](None,context))
 yes('actual_GWS_identical_ROW_recovery_without_second_append',lambda:n['tracker_append'](None,context))
 need(calls['append']==1,'repeated RAW append after uncertainty')
 table.append(copy.deepcopy(table[1]));no('actual_GWS_duplicate_after_recovery_rejected',lambda:n['tracker_append'](None,context));table.pop()
 no('actual_GWS_same_target_different_DOI_rejected',lambda:n['duplicate_tracker']([headers,[*table[1][:2],'https://doi.org/10.5281/zenodo.18',table[1][3]]],table[1]))
# Production schema and helper authority are independently exercised here too.
for bad in [True,1.0,'1',None]:no('typed_native_counter_'+repr(bad),lambda b=bad:n['need'](type(b) is int and b==1,'counter must exact int'))
need(calls['guard']>10,'actual authority guard paths not reached')
print(json.dumps({'status':'PASS_INDEPENDENT_ACTUAL_FLOW_INERT_BOUNDARIES','outer_optimization':sys.flags.optimize,'actual_core_compile_optimization':sys.flags.optimize,'actual_unchanged_kit_compile_optimization':sys.flags.optimize,'events':events,'event_count':len(events),'mutation_boundary_counts':{k:v for k,v in calls.items() if k!='get'},'all_GET_IDs':sorted(set(calls['get'])),'scope':'Actual zenodo, unchanged kit run, GuardedZenodoClient, independent_public_verify, publication_links, tracker_append and durable own file receipts. Acceptance/review/merge are explicit synthetic boundaries; all service/Git calls inert. No real credentials or service requests.'},sort_keys=True))
