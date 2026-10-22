"""Actual parser mutation-return custody after durable known facts and before checks."""
from pathlib import Path
import subprocess,sys,os,inspect,http.client
# Trusted preparation controller only: captured before full_controls blocks all
# actor process/network entry points. Only this exact own hashed child is run.
CONTROLLED_POPEN=subprocess.Popen
engine=Path(__file__).with_name('BASELINE16_ENGINE17.py')
text=engine.read_text().replace("DEST=REVIEW/'private'/('final_phase17_'+MODE)","DEST=REVIEW/'private'/('baseline16_unicode17_'+MODE)")
exec(compile(text,str(engine)+'[retention cohort only]','exec',dont_inherit=True,optimize=0),globals())
need((SOURCE/'SOURCE_MANIFEST.json').exists(),'Final physical freeze required')
CHILD=ROOT/'cold_baseline16_reentry17.py';CHILD_PIN=sha(CHILD.read_bytes());RETENTION=[]
def cold(w,action):
 need(sha(CHILD.read_bytes())==CHILD_PIN,'Cold child changed')
 argv=[sys.executable,'-I','-S','-B',str(CHILD),str(w.place),action,MS,BS]
 child=CONTROLLED_POPEN(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate(timeout=60)
 need(child.returncode==0,'Cold child failure '+err.decode())
 result=json.loads(out);need(result['pid']!=os.getpid()and result['status']=='PASS','Not fresh successful reentry')
 return result

SDK_CLIENT=c.zenodo.ZenodoClient;UTF=[]
def sdk_parse(raw,kind,metadata):
 exchanges=[]
 class Transport:
  def __init__(self,*a,**k):pass
  def putrequest(self,method,target):exchanges.append({'method':method,'target':target})
  def putheader(self,key,value):
   if key=='Authorization':need(value=='Bearer OFFLINE_SENTINEL_NO_CREDENTIAL','Not inert token')
  def endheaders(self):pass
  def send(self,data):pass
  def getresponse(self):return types.SimpleNamespace(status=200,read=lambda maximum:raw)
  def close(self):pass
 with model.patch((http.client,'HTTPSConnection',Transport)):
  client=SDK_CLIENT('production','OFFLINE_SENTINEL_NO_CREDENTIAL');value=client.create(metadata)if kind=='create'else client.publish(777)
 need(len(exchanges)==1 and exchanges[0]['method']=='POST','SDK parser bypassed')
 return value,exchanges
for tag,suffix in [('high',chr(0xd800))]:
 for kind in ['create','publish']:
  label='held16_unicode_'+tag+'_'+kind;action='publish'if kind=='publish'else'resume-stage';w=setup(label,'publish'if kind=='publish'else'stage');method=getattr(w.native,kind);spy={};steps=[];writes=[];writer=c.durable
  def returned(*args):
   value=method(*args);value['title']='Contrary original parser text '+suffix
   raw=json.dumps(value,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode('ascii');parsed,ex=sdk_parse(raw,kind,w.native.metadata);steps.extend(ex);spy.update(body=copy.deepcopy(parsed),wire=raw);return parsed
  setattr(w.native,kind,returned)
  def tracked(path,value):
   if path.name.startswith('service_original_')and value.get('kind')==kind:writes.append(str(path))
   return writer(path,value)
  before=len(w.native.calls)
  with model.patch((c,'durable',tracked)),w.installed():a,e=run(w,action)
  # Full independent inputs are durable BEFORE adjudication/cold replay.
  for name,body in [('ADVERSARY_ONLY_RETURNED_BODY_SPY.json',(json.dumps(spy['body'],ensure_ascii=True,sort_keys=True,indent=2)+'\n').encode('ascii')),('INERT_SDK_RESPONSE_ASCII.json',spy['wire'])]:
   with(w.place/name).open('xb')as f:f.write(body);f.flush();os.fsync(f.fileno())
  holds=[json.loads(q.read_bytes())for q in m.RUNTIME.glob('CONSUMED_RESPONSE16_HOLD_*')]
  originals=[(q,json.loads(q.read_bytes()))for q in m.PRIVATE.glob('service_original_*.json')]
  exact=[(q,v)for q,v in originals if v['kind']==kind and m.SHEET_POLICY.typed_equal(v['response'],spy['body'])]
  need(e and e['type']=='ConsumedResponseError'and holds and not exact and not writes,'Frozen16 Unicode failure not reproduced')
  need(any(h['exception_type']=='UnicodeEncodeError'for h in holds),'Expected pre-writer UnicodeEncodeError not reached')
  need(holds and all(h['known_id']==777 for h in holds),'Known777 lost from durable HOLD')
  need(len(w.native.calls)-before==1 and not(m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists()and not list(m.RUNTIME.glob('PRIVATE_PUBLICATION_STATE_*')),'False16success/retry')
  if kind=='create':need(not(m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'Frozen16 contrary title certified')
  child=cold(w,action)
  result={'case':label,'status':'EXPECTED_OLD16_HOLD_REPRODUCED','kind':kind,'string_class':tag,'error':e,'HOLD_exception_types':[h['exception_type']for h in holds],'SDK_exchanges':steps,'wire_pin':c.pin(spy['wire']),'SDK_parser_accepted_complete_original':True,'original_writer_attempts':len(writes),'complete_typed_original_lost':True,'known777_preserved':True,'native_mutations':w.native.calls,'appends':w.appends,'cold_reentry':child,'actual_effects':0}
  (DEST/(label+'.json')).write_text(json.dumps(result,ensure_ascii=True,indent=2)+'\n');UTF.append(result);archive_completed()
need(not model.ATTEMPTS,'Actual external attempt')
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_manifest_sha256':MS,'bootstrap_sha256':BS,'cases':UTF,'hot_parsed_invocations':len(CLI_INVOCATIONS),'cold_reentries':len(UTF),'actual_effects':0,'publication_ready':False,'SDK_sha256':sha((c.REPO/'zenodo_deposit_tool/zenodo.py').read_bytes())}
(ROOT/'private/BASELINE16_UNICODE_RESULTS.json').write_text(json.dumps(out,ensure_ascii=True,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='cases'},indent=2))
