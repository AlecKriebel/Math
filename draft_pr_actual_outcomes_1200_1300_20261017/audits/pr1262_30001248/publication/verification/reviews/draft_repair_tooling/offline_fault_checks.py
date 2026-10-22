#!/usr/bin/env python3
"""Actual same-ID repair helper and shared kit with completely mocked network.
Synthetic final gates/frozen identities are local fixture data, not clearance.
"""
from pathlib import Path
import copy,datetime,hashlib,importlib.util,json,subprocess,sys,tempfile,types
F=Path(__file__).resolve().parent;A=F.parents[1];PROGRAM=A.parents[1];OPERATIVE=PROGRAM/'publication_coordinators/repair_pr1262_draft.py';COORD=PROGRAM/'publication_coordinators/pr1262.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def load(p):
 spec=importlib.util.spec_from_file_location('repair_fixture_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def need(v,m):
 if not v:raise RuntimeError(m)
def rejected(fn,label,errors):
 try:fn()
 except errors:return label
 raise RuntimeError('Unexpected invalid-fixture acceptance '+label)
def fixture(folder):
 folder.mkdir(parents=True);p=folder/'publication';p.mkdir();r=load(OPERATIVE);r.A=folder;r.P=p;c=load(COORD);c.A=folder;c.P=p;kit=c.load_exact_kit();kit.STATE_DIR=folder/'kit-state';events=[]
 metadata={'title':'Sharp modulus range for triangle counts in dense random graphs','upload_type':'publication','publication_type':'preprint','description':'<p>Synthetic fixture n&gt;=3 only; no actual clearance.</p>','creators':[{'name':'Fixture author','affiliation':None}],'access_right':'open','license':'cc-by-4.0','version':'1.0','publication_date':'2026-10-17','keywords':['synthetic fixture'],'related_identifiers':[]}
 (p/r.PDF).write_bytes(b'SYNTHETIC UNCHANGED PDF');(p/r.ZIP).write_bytes(b'SYNTHETIC NEW REVIEWED ZIP');oldzip=b'SYNTHETIC OLD ZIP';save(p/'zenodo-deposit.json',{'metadata':metadata,'files':[{'path':r.PDF},{'path':r.ZIP}]});save(p/'STAGE_INTENT.json',{'synthetic_original_stage_intent':True});meta,new=kit.load_manifest(p/'zenodo-deposit.json');old=[]
 for n,data,fileid in [(r.PDF,(p/r.PDF).read_bytes(),'76184f77-18cf-40e4-a26e-c979f92920e8'),(r.ZIP,oldzip,'8e031f38-cdba-4cad-ad1c-fd3ef8f3d641')]:old.append({'name':n,'size':len(data),'md5':hashlib.md5(data).hexdigest(),'sha256':hashlib.sha256(data).hexdigest(),'id':fileid})
 baseline={'schema':'math-pr1262-draft-repair-baseline-v1','pr':1262,'problem_id':30001248,'id':r.KNOWN,'submitted':False,'environment':'production','bucket':'https://zenodo.org/api/files/f166189b-fbba-4eb5-8860-fa5f988bdcac','stage_intent_sha256':sha(p/'STAGE_INTENT.json'),'new_metadata_sha256':sha(p/'zenodo-deposit.json'),'protected_name':r.PDF,'replacement_name':r.ZIP,'files':old};save(folder/'DRAFT_REPAIR_BASELINE.json',baseline)
 freeze=folder/'INPUT_FREEZE.json';save(freeze,{'files':[{'path':str(q),'bytes':q.stat().st_size,'sha256':sha(q)} for q in [OPERATIVE,folder/'DRAFT_REPAIR_BASELINE.json']],'external_readonly_inputs':[]});gate={'latest_review':{'status':'CLEAN','input_freeze':'../INPUT_FREEZE.json','input_freeze_sha256':sha(freeze)},'synthetic_fixture_only':True};save(p/'FINAL_REVIEW_GATE.json',gate)
 def auth():
  events.append('mock full release authentication');return read_gate()
 def read_gate():return json.loads((p/'FINAL_REVIEW_GATE.json').read_text())
 c.authenticate_release=auth;c.live_preflight=lambda:events.append('mock live original PR/tracker preflight');r.coordinator=lambda:c
 place,_=kit.local_state((p/'zenodo-deposit.json').resolve(),'production');kit.save_state(place,{'manifest':str((p/'zenodo-deposit.json').resolve()),'environment':'production','id':r.KNOWN})
 remote={'id':r.KNOWN,'submitted':False,'metadata':copy.deepcopy(meta),'links':{'bucket':baseline['bucket']},'files':[{'filename':e['name'],'filesize':e['size'],'checksum':e['md5'],'id':e['id']} for e in old]};state={'mode':None,'after_delete_field':None,'lose_read':False,'failed_get_once':False};newentry=next(e for e in new if e['name']==r.ZIP)
 class Client(kit.ZenodoClient):
  def __init__(self):super().__init__('production','synthetic-never-transmitted-token')
  def request(self,method,url,payload=None,file=None,accept='application/json'):
   if method=='GET':
    events.append('GET')
    if state['lose_read']:state['lose_read']=False;raise kit.DepositError('Synthetic lost GET')
    return copy.deepcopy(remote)
   if method=='DELETE':
    events.append('DELETE');need(url=='https://zenodo.org/api/deposit/depositions/'+str(r.KNOWN)+'/files/'+old[1]['id'],'Wrong DELETE URL');need(payload is None and file is None,'Unexpected DELETE body')
    if state['mode']=='delete_failed':raise kit.DepositError('Synthetic delete rejected')
    remote['files']=[e for e in remote['files'] if e['filename']!=r.ZIP]
    if state['after_delete_field']:
     field=state['after_delete_field'];remote['metadata'][field]=corrupt(meta[field])
    if state['mode']=='lost_delete_GET':state['lose_read']=True
    if state['mode'] in {'delete_204','lost_delete_GET'}:raise kit.DepositError('Unexpected or incomplete Zenodo JSON response; operation outcome is unconfirmed. Inspect the saved draft/account before retrying')
    return {'synthetic_deleted':True}
   if method=='PUT':
    events.append('PUT');need(url==baseline['bucket']+'/'+r.ZIP and file==p/r.ZIP and payload is None,'PUT is not exact new ZIP to same bucket')
    if state['mode']=='upload_not_accepted':raise kit.DepositError('Synthetic lost upload before acceptance')
    remote['files'].append({'filename':r.ZIP,'filesize':newentry['size'],'checksum':'md5:'+newentry['md5'],'id':'11520f81-19a5-4096-a690-5c0acbfcf324'})
    if state['mode']=='lost_upload_GET':state['lose_read']=True
    if state['mode'] in {'lost_upload','lost_upload_GET'}:raise kit.DepositError('Synthetic upload response lost')
    return {'synthetic_uploaded':True}
   raise RuntimeError('Forbidden accidental network method '+method+' '+url)
 client=Client();return types.SimpleNamespace(r=r,c=c,kit=kit,p=p,a=folder,meta=meta,new=new,old=old,b=baseline,remote=remote,state=state,events=events,client=client,errors=(RuntimeError,ValueError,kit.DepositError,FileNotFoundError))
def corrupt(x):
 if isinstance(x,list):return [] if x else [{'unexpected':'corruption'}]
 return 'CORRUPTED'
def call(f,action='replace'):return f.r.execute(action,kit=f.kit,client=f.client)
def no_mutations(f):need(not any(e in {'DELETE','PUT'} for e in f.events),'Invalid fixture mutated network')
def run_case(folder,mode):
 f=fixture(folder);f.state['mode']=mode
 if mode in {'lost_delete_GET','lost_upload_GET'}:
  rejected(lambda:call(f),mode,f.errors);before=f.events[:];result=call(f);need(result['status']==('ready_to_publish' if mode=='lost_upload_GET' else 'recovery_required'),'Readonly recovery state differs');need(f.events.count('DELETE')==before.count('DELETE') and f.events.count('PUT')==before.count('PUT'),'Uncertain outcome repeated mutation')
 elif mode in {'delete_failed','upload_not_accepted'}:
  if mode=='delete_failed':rejected(lambda:call(f),mode,f.errors)
  else:need(call(f)['status']=='recovery_required','Failed upload did not require recovery')
  before=f.events[:];need(call(f)['status']=='recovery_required','Unresolved attempt was not read-only');need(f.events.count('DELETE')==1 and f.events.count('PUT')==(0 if mode=='delete_failed' else 1),'Uncertain attempt mutated twice')
 else:
  result=call(f);need(result['status']=='ready_to_publish','Successful repair missing stage');need(f.events.count('DELETE')==1 and f.events.count('PUT')==1,'Successful repair wrong mutation count');call(f);call(f,'inspect');need(f.events.count('DELETE')==1 and f.events.count('PUT')==1,'Repeated repair retried mutation');f.c.validate_summary(json.loads((f.p/'STAGE_RECEIPT.json').read_text()),f.kit,f.r.KNOWN,'ready_to_publish')
 need(f.remote['submitted'] is False,'Repair published');need(sha(f.p/'STAGE_INTENT.json')==f.b['stage_intent_sha256'],'Original stage intent changed');return {'mode':mode,'DELETE_count':f.events.count('DELETE'),'PUT_count':f.events.count('PUT'),'no_forbidden_actions':True,'original_intent_unchanged':True}
def actual_204_contract():
 c=load(COORD);kit=c.load_exact_kit();events=[]
 class Response:
  status=204
  def read(self,n):return b''
 class Conn:
  def __init__(self,*a,**k):pass
  def putrequest(self,m,t):events.append((m,t))
  def putheader(self,*a):pass
  def endheaders(self):pass
  def getresponse(self):return Response()
  def close(self):pass
 kit.http.client=types.SimpleNamespace(HTTPSConnection=Conn,HTTPException=Exception)
 client=kit.ZenodoClient('production','synthetic-secret-never-sent');rejected(lambda:client.request('DELETE','https://zenodo.org/api/deposit/depositions/23443230/files/8e031f38-cdba-4cad-ad1c-fd3ef8f3d641'),'actual_shared_request_204_empty_rejected',(kit.DepositError,));return {'actual_shared_ZenodoClient_request_exercised':True,'documented_204_empty_body_triggers_expected_kit_DepositError':True,'network_connection_mocked':True}
def worker():
 initial=sha(OPERATIVE);before_inputs={n:sha(A/n) for n in ['DRAFT_REPAIR_BASELINE.json','publication/STAGE_INTENT.json']};rejected_fields=[];faults=[]
 with tempfile.TemporaryDirectory(prefix='draft-repair-offline-',dir=F/'_local') as tmp:
  root=Path(tmp)
  for stage in ['before_DELETE','before_PUT']:
   for field in sorted(load(OPERATIVE).FIELDS):
    f=fixture(root/(stage+'_'+field))
    if stage=='before_DELETE':f.remote['metadata'][field]=corrupt(f.meta[field])
    else:f.state['after_delete_field']=field
    rejected(lambda:call(f),stage+'_'+field,f.errors);need(f.events.count('PUT')==0 and f.events.count('DELETE')==(0 if stage=='before_DELETE' else 1),'Metadata fault crossed forbidden mutation boundary');rejected_fields.append(stage+'_'+field)
  for label in ['wrong_id','submitted_true','submitted_nonbool','wrong_old_ZIP_md5','wrong_old_ZIP_size','wrong_old_ZIP_UUID','wrong_PDF_md5','wrong_PDF_size','wrong_PDF_UUID','missing_oldZIP','extra_file','duplicate_filename','bucket_url','bucket_other_valid','local_PDF_drift','local_ZIP_not_amended','kit_wrong_id','missing_helper_freeze','missing_baseline_freeze','helper_freeze_hash','baseline_freeze_hash','live_preflight_failure','original_stage_intent_drift','existing_upload_without_repair','existing_repair_intent_wrong_identity','preexisting_publish_intent']:
   f=fixture(root/label);b=f.b
   if label=='wrong_id':f.remote['id']=23443231
   elif label=='submitted_true':f.remote['submitted']=True
   elif label=='submitted_nonbool':f.remote['submitted']=0
   elif label.startswith('wrong_old_ZIP_'):f.remote['files'][1][{'md5':'checksum','size':'filesize','UUID':'id'}[label.removeprefix('wrong_old_ZIP_')]]='bad'
   elif label.startswith('wrong_PDF_'):f.remote['files'][0][{'md5':'checksum','size':'filesize','UUID':'id'}[label.removeprefix('wrong_PDF_')]]='bad'
   elif label=='missing_oldZIP':f.remote['files'].pop()
   elif label=='extra_file':f.remote['files'].append({'filename':'foreign','filesize':1,'checksum':'0'*32,'id':'11520f81-19a5-4096-a690-5c0acbfcf324'})
   elif label=='duplicate_filename':f.remote['files'].append(copy.deepcopy(f.remote['files'][1]))
   elif label=='bucket_url':f.remote['links']['bucket']='https://evil.invalid/api/files/f166189b-fbba-4eb5-8860-fa5f988bdcac'
   elif label=='bucket_other_valid':f.remote['links']['bucket']='https://zenodo.org/api/files/11520f81-19a5-4096-a690-5c0acbfcf324'
   elif label=='local_PDF_drift':(f.p/f.r.PDF).write_bytes(b'CHANGED')
   elif label=='local_ZIP_not_amended':
    (f.p/f.r.ZIP).write_bytes(b'SYNTHETIC OLD ZIP')
   elif label=='kit_wrong_id':place,_=f.kit.local_state((f.p/'zenodo-deposit.json').resolve(),'production');state=json.loads(place.read_text());state['id']=23443231;save(place,state)
   elif label in {'missing_helper_freeze','missing_baseline_freeze','helper_freeze_hash','baseline_freeze_hash'}:
    q=f.a/'INPUT_FREEZE.json';x=json.loads(q.read_text());index=0 if 'helper' in label else 1
    if label.startswith('missing'):x['files'].pop(index)
    else:x['files'][index]['sha256']='0'*64
    save(q,x);g=json.loads((f.p/'FINAL_REVIEW_GATE.json').read_text());g['latest_review']['input_freeze_sha256']=sha(q);save(f.p/'FINAL_REVIEW_GATE.json',g)
   elif label=='live_preflight_failure':f.c.live_preflight=lambda:(_ for _ in ()).throw(RuntimeError('Synthetic original PR/body/tracker change'))
   elif label=='original_stage_intent_drift':save(f.p/'STAGE_INTENT.json',{'changed':True})
   elif label=='existing_upload_without_repair':save(f.p/'DRAFT_REPAIR_UPLOAD_INTENT.json',{})
   elif label=='existing_repair_intent_wrong_identity':save(f.p/'DRAFT_REPAIR_INTENT.json',{})
   elif label=='preexisting_publish_intent':save(f.p/'PUBLISH_INTENT.json',{})
   faults.append(rejected(lambda:call(f),label,f.errors));no_mutations(f)
  cases=[run_case(root/('case_'+mode),mode) for mode in ['normal','delete_204','lost_upload','lost_delete_GET','lost_upload_GET','delete_failed','upload_not_accepted']]
  # Exact prior intent causes GET-only reconciliation even if old files remain.
  f=fixture(root/'existing_intent');g,b,meta,new=f.r.authenticate(f.c,f.kit);save(f.p/'DRAFT_REPAIR_INTENT.json',f.r.intent_identity(g,b,new));need(call(f)['status']=='recovery_required','Existing intent not readonly');no_mutations(f)
  # Exclusive file creation itself fails closed; no overwrites accepted.
  q=root/'exclusive.json';f.r.exclusive(q,{'one':1});faults.append(rejected(lambda:f.r.exclusive(q,{'two':2}),'exclusive_intent_refuses_overwrite',f.errors));need(json.loads(q.read_text())=={'one':1},'Exclusive intent overwritten')
 need(sha(OPERATIVE)==initial,'Actual operative helper changed during tests');need(before_inputs=={n:sha(A/n) for n in before_inputs},'Actual baseline/stage intent changed')
 return {'status':'PASS','all11_metadata_fields_rejected_before_each_DELETE_and_PUT':rejected_fields,'negative_controls':faults,'same_ID_scenarios':cases,'existing_intent_always_GET_only':True,'actual_shared_204_empty_response_contract':actual_204_contract(),'actual_baseline_and_original_stage_intent_unchanged':True,'actual_operative_helper_sha256':initial,'scope':'Synthetic current full-release authentication and live-PR preflight stubs; helper-specific actual frozen-input guards and actual strict coordinator/kit/client methods executed with mocked transport. No real final gate, network/token, account/Git/PR mutation or clearance.'}
def main():
 if '--worker' in sys.argv:print(json.dumps(worker(),sort_keys=True));return
 runs=[]
 for flags in [[],['-O'],['-OO']]:
  r=subprocess.run([sys.executable,'-B',*flags,str(Path(__file__).resolve()),'--worker'],capture_output=True,text=True)
  if r.returncode:raise RuntimeError(r.stderr)
  runs.append({'flags':flags,'result':json.loads(r.stdout)})
 need(all(x['result']==runs[0]['result'] for x in runs),'Optimization-dependent repair guards');out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','all3_modes_identical':True,'runs':runs};save(F/'OFFLINE_FAULT_RECEIPT.json',out);print(json.dumps({'status':'PASS','all3_modes_identical':True,'receipt_sha256':sha(F/'OFFLINE_FAULT_RECEIPT.json')},indent=2))
if __name__=='__main__':main()
