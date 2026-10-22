"""Offline F01 regression: execute actual coordinator and actual kit.run.
Only release-authentication/live-preflight dependencies are replaced by explicit
synthetic valid inputs. In-memory clients make real external mutation impossible.
This is an operational control test, not a substitute for release authentication.
"""
from pathlib import Path
import copy,datetime,hashlib,importlib.util,json,tempfile
from unittest.mock import patch
REPO=Path('/Users/alec/Documents/Math');A=Path(__file__).resolve().parent
SOURCE=REPO/'draft_pr_actual_outcomes_1200_1300_20261017/_local/run_pr1241_deposit.py'
def need(c,m):
 if not c:raise RuntimeError(m)
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def case(name,legacy=False,normalization_at=0,mutate_summary=None,stage_id=77,state_id=77,published=False,lost=False,unconfirmed=False,prior_intent=False,stale_inspect=False):
 with tempfile.TemporaryDirectory(prefix='pr1241-f01-') as tmp:
  p=Path(tmp);coord=load('f01_coord_'+name,SOURCE);kit=load('f01_kit_'+name,REPO/'zenodo_deposit_tool/zenodo.py');coord.P=p
  manifest=json.loads((A/'publication/zenodo-deposit.json').read_text())
  if legacy:manifest['metadata']['description']=manifest['metadata']['description'].replace("Farb's",'Farb\u2019s').replace("Horowitz's",'Horowitz\u2019s').replace("Ferudun's",'Ferudun\u2019s')
  manifest['files']=[{'path':'paper.pdf'},{'path':'verification.zip'}];(p/'paper.pdf').write_bytes(b'offline PDF fixture');(p/'verification.zip').write_bytes(b'offline ZIP fixture');write(p/'zenodo-deposit.json',manifest)
  metadata,files=kit.load_manifest(p/'zenodo-deposit.json');events=[]
  summary={'environment':'production','title':metadata['title'],'id':stage_id,'state':'ready_to_publish','metadata_normalizations':[],'files':[{'name':f['name'],'size':f['size'],'sha256':f['sha256']} for f in files]};write(p/'STAGE_RECEIPT.json',summary)
  if stale_inspect:write(p/'STAGE_INSPECT.json',{**summary,'id':999,'state':'published'})
  if prior_intent:write(p/'PUBLISH_INTENT.json',{'id':77})
  class Client:
   def __init__(self):self.submitted=published;self.gets=0
   def get(self,record_id):
    events.append('GET_'+str(record_id));self.gets+=1;m=copy.deepcopy(metadata)
    if normalization_at and self.gets>=normalization_at:m['description']=m['description'].replace('\u2019',"'")
    return {'id':77,'submitted':self.submitted,'doi':'10.5281/zenodo.77','metadata':m,'files':[{'filename':f['name'],'filesize':f['size'],'checksum':'md5:'+f['md5']} for f in files]}
   def publish(self,record_id):
    events.append('PUBLISH_POST_'+str(record_id))
    if not unconfirmed:self.submitted=True
    if lost or unconfirmed:raise kit.DepositError('Simulated lost response')
    return {'id':77,'submitted':True}
  client=Client();real_run=kit.run
  def run(args):
   d=real_run(args,client=client)
   if mutate_summary and args.command=='inspect':mutate_summary(d)
   return d
  kit.run=run;gate={'metadata_sha256':sha(p/'zenodo-deposit.json'),'pdf_sha256':sha(p/'paper.pdf'),'verification_zip_sha256':sha(p/'verification.zip')}
  state={'manifest':str(p/'zenodo-deposit.json'),'environment':'production','id':state_id}
  result={'case':name,'events':events,'fixture_legacy_curly_description':legacy,'live_network_calls':0}
  with patch.object(coord,'authenticate_release',return_value=gate),patch.object(coord,'live_preflight',side_effect=lambda:events.append('READONLY_LIVE_PREFLIGHT')),patch.object(kit,'local_state',return_value=(p/'kit-state.json',state)),patch.object(kit,'save_state'),patch.object(kit,'doi_status',return_value={'status':'resolved'}):
   try:d=coord.execute('publish',kit);result.update(completed=True,state=d['state'],recovered=d.get('recovered_after_publish_error',False))
   except Exception as e:result.update(completed=False,error=type(e).__name__+': '+str(e))
   if unconfirmed:
    posts_before=sum(e.startswith('PUBLISH_POST') for e in events)
    try:coord.execute('publish',kit)
    except Exception as e:result['second_attempt_refused']=str(e)
    else:raise RuntimeError('Unconfirmed attempt retried')
    result['retry_extra_posts']=sum(e.startswith('PUBLISH_POST') for e in events)-posts_before
  result.update(publish_posts=sum(e.startswith('PUBLISH_POST') for e in events),publication_receipt=(p/'PUBLICATION_RECEIPT.json').exists(),fresh_inspect_saved=(p/'STAGE_INSPECT.json').exists(),intent_saved=(p/'PUBLISH_INTENT.json').exists())
  return result
results=[case('exact_ASCII_no_saved_inspect'),case('stale_saved_inspect_replaced_by_fresh',stale_inspect=True),case('F01_legacy_normalized_before_inspect',legacy=True,normalization_at=1),case('F01_normalization_after_exact_inspect_before_POST',legacy=True,normalization_at=2),case('already_published_readonly_recovery',published=True),case('lost_POST_response_readonly_recovered',lost=True),case('unconfirmed_POST_no_second_attempt',unconfirmed=True),case('prior_intent_unpublished_refused',prior_intent=True),case('different_known_state_ID_refused',state_id=78),case('invalid_stage_ID_refused',stage_id=True)]
for name,mutation in [('missing_inspect_exactness',lambda d:d.pop('metadata_normalizations')),('nonexact_inspect',lambda d:d.update(metadata_normalizations=[{'field':'description'}])),('inspect_wrong_ID',lambda d:d.update(id=78)),('inspect_wrong_state',lambda d:d.update(state='unknown')),('inspect_wrong_files',lambda d:d.update(files=[])),('inspect_wrong_environment',lambda d:d.update(environment='sandbox')),('inspect_wrong_title',lambda d:d.update(title='other'))]:results.append(case(name,mutate_summary=mutation))
for i in [0,1]:need(results[i]['completed'] and results[i]['publish_posts']==1 and results[i]['fresh_inspect_saved'],'Positive fresh-inspection control failed')
for i in [2,3,7,8,9,*range(10,len(results))]:need(not results[i]['completed'] and results[i]['publish_posts']==0,'Negative condition published: '+results[i]['case'])
need(results[4]['completed'] and results[4]['publish_posts']==0,'Published recovery mutated')
need(results[5]['completed'] and results[5]['publish_posts']==1 and results[5]['recovered'],'Lost response not recovered once')
need(not results[6]['completed'] and results[6]['publish_posts']==1 and results[6]['retry_extra_posts']==0,'Unconfirmed POST retried')
report={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','coordinator_sha256':sha(SOURCE),'kit_sha256':sha(REPO/'zenodo_deposit_tool/zenodo.py'),'test_sha256':sha(Path(__file__)),'count':len(results),'results':results,'limits':'Synthetic release authentication and live preflights only; actual kit.run, exact verifier, coordinator execute/intent/receipt paths used with in-memory client. Zero real network/mutation. R2 authenticated separately; new full reviewer still required.'}
write(A/'COORDINATOR_F01_REGRESSION.json',report);print(json.dumps({k:report[k] for k in ['status','count','coordinator_sha256','kit_sha256']}))
