"""Actual parser mutation-return custody after durable known facts and before checks."""
from pathlib import Path
import subprocess,sys,os,inspect
# Trusted preparation controller only: captured before full_controls blocks all
# actor process/network entry points. Only this exact own hashed child is run.
CONTROLLED_POPEN=subprocess.Popen
engine=Path(__file__).with_name('ENGINE17.py')
text=engine.read_text().replace("DEST=REVIEW/'private'/('final_phase17_'+MODE)","DEST=REVIEW/'private'/('fact_edges17_'+MODE)")
exec(compile(text,str(engine)+'[retention cohort only]','exec',dont_inherit=True,optimize=0),globals())
need((SOURCE/'SOURCE_MANIFEST.json').exists(),'Final physical freeze required')
CHILD=ROOT/'cold_reentry17.py';CHILD_PIN=sha(CHILD.read_bytes());RETENTION=[]
def cold(w,action):
 need(sha(CHILD.read_bytes())==CHILD_PIN,'Cold child changed')
 argv=[sys.executable,'-I','-S','-B',str(CHILD),str(w.place),action,MS,BS]
 child=CONTROLLED_POPEN(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate(timeout=60)
 need(child.returncode==0,'Cold child failure '+err.decode())
 result=json.loads(out);need(result['pid']!=os.getpid()and result['status']=='PASS','Not fresh successful reentry')
 return result

for boundary,kind in [('secondary_fact','create'),('secondary_fact','publish'),('combined_first','create'),('combined_first','upload'),('combined_first','update'),('combined_first','publish')]:
 label='after_fsync_'+boundary+'_'+kind;phase='publish'if kind in {'publish','get'}else'stage';action='publish'if phase=='publish'else'resume-stage'
 w=setup(label,phase);spy={};hit=[];method=getattr(w.native,kind)
 def returned(*args):
  value=method(*args)
  selected=kind!='get'or inspect.currentframe().f_back.f_code is m.EdgeDelegate.get.__code__
  if selected and not spy:spy['body']=copy.deepcopy(value)
  return value
 setattr(w.native,kind,returned);writer=c.durable;target='CREATE_RETURNED_KNOWN_ID.json'if kind=='create'else'PUBLISH_RETURNED_SERVICE_FACT.json'
 def after_fsync(path,value):
  writer(path,value)
  selected=path.name==target if boundary=='secondary_fact'else path.name.startswith('service_original_')and value.get('kind')==kind and bool(spy)
  if selected and not hit:
   before=path.read_bytes()
   with path.open('ab')as h:h.write(b'\n');h.flush();os.fsync(h.fileno())
   after=path.read_bytes();need(m.SHEET_POLICY.typed_equal(json.loads(before),json.loads(after)),'Fault changed parsed semantics')
   hit.append({'path':str(path),'before_pin':c.pin(before),'after_pin':c.pin(after),'all_IO_succeeded':True,'only_newline_added':after==before+b'\n'})
 before=(len(w.native.calls),w.appends)
 with model.patch((c,'durable',after_fsync)),w.installed():a,e=run(w,action)
 originals={str(q):json.loads(q.read_bytes())for q in m.PRIVATE.glob('service_original_*.json')}
 exact=[(path,v)for path,v in originals.items()if v['kind']==kind and m.SHEET_POLICY.typed_equal(v['response'],spy.get('body'))]
 holds=[json.loads(q.read_bytes())for q in m.RUNTIME.glob('CONSUMED_RESPONSE17_HOLD_*')]
 need(e and len(hit)==1 and len(exact)==1 and holds,'Complete original or strict rejection absent')
 path,value=exact[0];desc=next(v for h in holds for v in h['all_consumed_response_custody']if v['path']==path)
 need(holds[-1]['original_response']['path']==path and desc['durable_write_returned']is True,'First custody path lost')
 if kind!='get':need(value['known_service_fact']['kind']==kind and value['known_service_fact']['requested_or_known_id']==777,'Known outcome not combined with full original')
 if boundary=='secondary_fact':
  need(desc['expected_integrity_verified']is True and desc['pin']==c.pin(Path(path).read_bytes()),'Earlier combined original not intact/verified')
  need(json.loads((m.RUNTIME/target).read_bytes())['original_response']['path']==path,'Secondary fact not bound to first receipt')
 else:
  need(desc['expected_integrity_verified']is False and desc['pin']!=c.pin(Path(path).read_bytes()),'Altered receipt expected bytes accepted')
  if kind=='create':need(not(m.RUNTIME/'CREATE_RETURNED_KNOWN_ID.json').exists(),'Narrower known fact preceded first combined custody')
  if kind=='publish':need(not(m.RUNTIME/'PUBLISH_RETURNED_SERVICE_FACT.json').exists(),'Narrower publish fact preceded first combined custody')
 need(not(m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists()and not(m.RUNTIME/'LEDGER_VERIFIED.json').exists()and not list(m.RUNTIME.glob('PRIVATE_PUBLICATION_STATE_*')),'Rejected receipt certified or saved publication summary')
 if phase=='stage':need(not(m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'Rejected stage certified')
 expected={'create':1,'upload':2,'update':4,'publish':1,'get':0}[kind];need(len(w.native.calls)-before[0]==expected and w.appends==before[1],'Unexpected mutation/retry')
 child=cold(w,action)
 (w.place/'ADVERSARY_ONLY_RETURNED_BODY_SPY.json').write_text(json.dumps(spy['body'],indent=2)+'\n')
 result={'case':label,'status':'PASS','kind':kind,'boundary':boundary,'error':e,'post_fsync_edge':hit,'complete_original_typed_equal':True,'original_path':path,'original_descriptor':desc,'actual_retained_pin':c.pin(Path(path).read_bytes()),'full_known_fact_combined':kind!='get','native_mutations':w.native.calls,'contested_delta':expected,'appends':w.appends,'cold_reentry':child,'actual_effects':0}
 (DEST/(label+'.json')).write_text(json.dumps(result,indent=2)+'\n');RETENTION.append(result);archive_completed()
need(not model.ATTEMPTS,'Real external adapter attempted')
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_manifest_sha256':MS,'bootstrap_sha256':BS,'cases':RETENTION,'hot_parsed_invocations':len(CLI_INVOCATIONS),'cold_fresh_process_invocations':len(RETENTION),'actual_effects':0,'publication_ready':False,'child_script_sha256':CHILD_PIN}
(ROOT/'private/FACT_EDGE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='cases'},indent=2))
