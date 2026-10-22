from pathlib import Path
from unittest.mock import patch
import argparse,contextlib,copy,datetime,hashlib,importlib.util,io,json,shutil,types
R=Path(__file__).resolve().parent;freeze=json.loads((R/'INPUT_FREEZE.json').read_text());A=Path(freeze['root']);REPO=Path('/Users/alec/Documents/Math');W=R/'scratch_local/coordinator';W.mkdir(exist_ok=True)
COORD=Path(freeze['external_readonly_inputs'][2]['path']);KIT=Path(freeze['external_readonly_inputs'][0]['path'])
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def need(c,m):
 if not c:raise RuntimeError(m)
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def case(label,remote_mutation=None,mutation_get=1,legacy=None,initial_published=False,prior_intent=False,post_mode='success',summary_mutation=None,state_change=None,stage_change=None,stale=False,retry=False):
 p=W/label;p.mkdir(exist_ok=True);kit=load('ind_kit_'+label,KIT);c=load('ind_coord_'+label,COORD);c.P=p
 doc=json.loads((A/'publication/zenodo-deposit.json').read_text());doc['files']=[{'path':'paper.pdf'},{'path':'archive.zip'}];(p/'paper.pdf').write_bytes(b'synthetic exact pdf');(p/'archive.zip').write_bytes(b'synthetic exact zip')
 if legacy=='curly':doc['metadata']['description']=doc['metadata']['description'].replace("Farb's",'Farb\u2019s').replace("Horowitz's",'Horowitz\u2019s').replace("Ferudun's",'Ferudun\u2019s')
 if legacy=='plaintext':doc['metadata']['description']='plain A & B < 3'
 if legacy=='nullcreator':doc['metadata']['creators'][0].pop('affiliation')
 write(p/'zenodo-deposit.json',doc);meta,files=kit.load_manifest(p/'zenodo-deposit.json');stage={'environment':'production','title':meta['title'],'state':'ready_to_publish','id':981,'metadata_normalizations':[],'files':[{k:f[k] for k in ('name','size','sha256')} for f in files]}
 if stage_change:stage_change(stage)
 write(p/'STAGE_RECEIPT.json',stage)
 if prior_intent:write(p/'PUBLISH_INTENT.json',{'id':981,'policy':'prior uncertain attempt'})
 if stale:write(p/'STAGE_INSPECT.json',{**stage,'id':999,'metadata_normalizations':[{'field':'description'}]})
 state={'manifest':str((p/'zenodo-deposit.json').resolve()),'environment':'production','id':981}
 if state_change:state_change(state)
 kit.STATE_DIR=p/'state';place=kit.state_path((p/'zenodo-deposit.json').resolve(),'production');kit.save_state(place,state)
 events=[];server={'published':initial_published,'gets':0};legacy_accepted=[]
 class Fake:
  def get(self,i):
   events.append({'method':'GET','id':i});server['gets']+=1
   if post_mode=='readback_failure' and server['gets']==3:raise kit.DepositError('fake failed post readback')
   dep={'id':981,'submitted':server['published'],'doi':'10.5281/zenodo.981','metadata':copy.deepcopy(meta),'files':[{'filename':f['name'],'checksum':'md5:'+f['md5'],'filesize':f['size']} for f in files]}
   if remote_mutation and server['gets']>=mutation_get:
    remote_mutation(dep)
    if legacy:
     try:legacy_accepted.append(bool(original_verify(dep,meta,files)))
     except kit.DepositError:legacy_accepted.append(False)
   return dep
  def publish(self,i):
   events.append({'method':'POST','id':i})
   if post_mode!='unconfirmed':server['published']=True
   if post_mode in ('lost','unconfirmed'):raise kit.DepositError('fake lost response')
   return {'id':i,'submitted':server['published']}
 fake=Fake();actual_run=kit.run;original_verify=kit.verify
 def invoke(args):
  d=actual_run(args,client=fake)
  if summary_mutation and args.command=='inspect':summary_mutation(d)
  return d
 kit.run=invoke
 def forbidden(*a,**kw):raise RuntimeError('No real token/network/client allowed')
 kit.token_for=forbidden;kit.ZenodoClient=forbidden;kit.doi_status=lambda doi:{'status':'not_checked_offline'}
 gate={k:hashlib.sha256((p/n).read_bytes()).hexdigest() for k,n in [('metadata_sha256','zenodo-deposit.json'),('pdf_sha256','paper.pdf'),('verification_zip_sha256','archive.zip')]}
 c.authenticate_release=lambda:copy.deepcopy(gate);c.live_preflight=lambda:events.append({'method':'READONLY_PREFLIGHT'})
 outputs=[]
 for attempt in range(2 if retry else 1):
  try:d=c.execute('publish',kit);outputs.append({'ok':True,'state':d['state'],'recovered':d.get('recovered_after_publish_error',False)})
  except Exception as e:outputs.append({'ok':False,'error':type(e).__name__+': '+str(e)})
 posts=sum(x['method']=='POST' for x in events)
 return {'case':label,'outputs':outputs,'events':events,'posts':posts,'legacy_generic_verifier_accepted_normalization':legacy_accepted,'receipt_exists':(p/'PUBLICATION_RECEIPT.json').exists(),'intent_exists':(p/'PUBLISH_INTENT.json').exists(),'fresh_inspect_exists':(p/'STAGE_INSPECT.json').exists()}
results=[]
results.append(case('exact_twice',retry=True));need(results[-1]['posts']==1 and all(x['ok'] for x in results[-1]['outputs']),'exact idempotency')
results.append(case('stale_inspect_replaced',stale=True));need(results[-1]['posts']==1 and results[-1]['outputs'][0]['ok'],'fresh ignores stale receipt')
for label,kind,mut in [('curly','curly',lambda d:d['metadata'].update(description=d['metadata']['description'].replace('\u2019',"'"))),('html_entities','plaintext',lambda d:d['metadata'].update(description='plain A &amp; B &lt; 3')),('creator_null','nullcreator',lambda d:d['metadata']['creators'][0].update(affiliation=None))]:
 for get in (1,2):
  r=case(label+'_get'+str(get),mut,get,legacy=kind);need(r['posts']==0 and not r['outputs'][0]['ok'] and r['legacy_generic_verifier_accepted_normalization']==[True],'legacy normalization failed control');results.append(r)
metadata=json.loads((A/'publication/zenodo-deposit.json').read_text())['metadata']
for field in metadata:
 for get in (1,2):
  r=case('field_'+field+'_get'+str(get),lambda d,f=field:d['metadata'].__setitem__(f,None),get);need(r['posts']==0 and not r['outputs'][0]['ok'],'metadata drift posted '+field);results.append(r)
for label,mut in [('file_size',lambda d:d['files'][0].update(filesize=0)),('file_checksum',lambda d:d['files'][0].update(checksum='md5:'+'0'*32)),('file_inventory',lambda d:d['files'].pop()),('file_duplicate',lambda d:d['files'].append(copy.deepcopy(d['files'][0]))),('record_id',lambda d:d.update(id=982)),('submitted_type',lambda d:d.update(submitted='false'))]:
 r=case(label,mut,2);need(r['posts']==0 and not r['outputs'][0]['ok'],'record/file drift posted');results.append(r)
for label,mut in [('no_exactness',lambda d:d.pop('metadata_normalizations')),('nonexact',lambda d:d.update(metadata_normalizations=['change'])),('different_id',lambda d:d.update(id=982)),('missing_files',lambda d:d.update(files=[])),('wrong_state',lambda d:d.update(state='draft')),('wrong_env',lambda d:d.update(environment='sandbox')),('wrong_title',lambda d:d.update(title='different'))]:
 r=case('summary_'+label,summary_mutation=mut);need(r['posts']==0 and not r['outputs'][0]['ok'],'summary drift posted');results.append(r)
for label,change,target in [('state_id',lambda d:d.update(id=982),'state'),('state_manifest',lambda d:d.update(manifest='/wrong'),'state'),('state_env',lambda d:d.update(environment='sandbox'),'state'),('stage_bool_id',lambda d:d.update(id=True),'stage'),('stage_bad_files',lambda d:d.update(files=[]),'stage')]:
 r=case(label,state_change=change if target=='state' else None,stage_change=change if target=='stage' else None);need(r['posts']==0 and not r['outputs'][0]['ok'],'known identity drift posted');results.append(r)
for label,kwargs,posts,oks in [('known_published',{'initial_published':True,'retry':True},0,[True,True]),('prior_unconfirmed_intent',{'prior_intent':True,'retry':True},0,[False,False]),('lost_response',{'post_mode':'lost','retry':True},1,[True,True]),('unconfirmed',{'post_mode':'unconfirmed','retry':True},1,[False,False]),('readback_failure',{'post_mode':'readback_failure','retry':True},1,[False,True])]:
 r=case(label,**kwargs);need(r['posts']==posts and [x['ok'] for x in r['outputs']]==oks,'uncertainty policy '+label);results.append(r)
report={'status':'PASS','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':len(results),'coordinator_sha256':hashlib.sha256(COORD.read_bytes()).hexdigest(),'actual_kit_sha256':hashlib.sha256(KIT.read_bytes()).hexdigest(),'results':results,'limits':'Actual coordinator execute and actual shared kit.run/verify/local_state/save_state execute with in-memory client, synthetic valid release gate and read-only preflight. No live token, client, API, POST, Git, index or tracker operation. Separate authentication tests examine the release gate. Cases include formerly accepted normalizations before inspection and between inspect/publish: all zero POST.'}
(R/'COORDINATOR_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','cases':len(results),'real_network':0}))
