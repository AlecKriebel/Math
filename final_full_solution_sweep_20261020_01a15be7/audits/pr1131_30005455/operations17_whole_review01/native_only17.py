"""Actual parser mutation-return custody after durable known facts and before checks."""
from pathlib import Path
import subprocess,sys,os,inspect
# Trusted preparation controller only: captured before full_controls blocks all
# actor process/network entry points. Only this exact own hashed child is run.
CONTROLLED_POPEN=subprocess.Popen
engine=Path(__file__).with_name('ENGINE17.py')
text=engine.read_text().replace("DEST=REVIEW/'private'/('final_phase17_'+MODE)","DEST=REVIEW/'private'/('native_only17_'+MODE)")
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
def run(w,action):
 try:return cli(w,action),None
 except Exception as exc:
  chain=[];current=exc;seen=set()
  while current is not None and id(current)not in seen:
   seen.add(id(current));chain.append({'type':type(current).__name__,'message':str(current)});current=current.__cause__ or current.__context__
  return None,{'type':type(exc).__name__,'message':str(exc),'exception_chain':chain}
for boundary in ['native_context']:
 for kind in ['create','upload','update','publish']:
  label='valid_original_'+kind+'_before_failed_'+boundary;action='publish'if kind=='publish'else'resume-stage'
  w=setup(label,'publish'if kind=='publish'else'stage');method=getattr(w.native,kind);spy={};foreign={};native_hits=[]
  def returned(*args):
   value=method(*args)
   # Identifying extra discrepancy ensures same complete original, not a
   # later correct GET, is retained even when an earlier context check fails.
   spy['body']=copy.deepcopy(value)
   if boundary=='canonical_state':
    path=c.zenodo.state_path(pub.MANIFEST.resolve(),'production')
    foreign['bytes']=(json.dumps({'manifest':str(pub.MANIFEST.resolve()),'environment':'production','id':999,'concurrent_marker':['preserve',True,1]},indent=1)+'\n').encode();path.write_bytes(foreign['bytes'])
   return value
  setattr(w.native,kind,returned)
  original_native=w.native.native_get
  if boundary=='native_context':
   def malformed(i,draft=False):
    value=original_native(i,draft);frame=inspect.currentframe().f_back
    target='upload_context_get'if kind=='upload'else kind
    if spy and frame.f_code is m.EdgeDelegate.checked_record.__code__ and frame.f_locals.get('kind')==target:
     value['parent']['id']='999';native_hits.append(copy.deepcopy(value))
    return value
   w.native.native_get=malformed
  before=(len(w.native.calls),w.appends)
  with w.installed():a,e=run(w,action)
  originals={str(q):json.loads(q.read_bytes())for q in m.PRIVATE.glob('service_original_*.json')}
  wanted=[(path,v)for path,v in originals.items()if v['kind']==kind and m.SHEET_POLICY.typed_equal(v['response'],spy.get('body'))]
  holds=[json.loads(q.read_bytes())for q in m.RUNTIME.glob('CONSUMED_RESPONSE17_HOLD_*')]
  need(e and len(wanted)==1 and holds,'Missing exact complete returned-body custody')
  refs=[v for h in holds for v in h['all_consumed_response_custody']]
  path,value=wanted[0];need(any(v['path']==path and v['pin']==c.pin(Path(path).read_bytes())for v in refs),'Returned body not bound to persistent HOLD')
  if boundary=='canonical_state':need(c.zenodo.state_path(pub.MANIFEST.resolve(),'production').read_bytes()==foreign['bytes'],'Foreign state overwritten')
  else:
   need(native_hits,'Late fresh native context boundary not hit')
   need(len(e['exception_chain'])>1,'Underlying native failure not retained in test')
  need(json.loads((m.RUNTIME/'CREATE_RETURNED_KNOWN_ID.json').read_bytes())['id']==777,'Known positive service ID lost')
  if kind=='publish':need(json.loads((m.RUNTIME/'PUBLISH_RETURNED_SERVICE_FACT.json').read_bytes())['requested_id']==777,'Publish returned fact lost')
  need(not(m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists()and not(m.RUNTIME/'LEDGER_VERIFIED.json').exists()and not list(m.RUNTIME.glob('PRIVATE_PUBLICATION_STATE_*')),'Unexpected success after rejected actual response')
  if action=='resume-stage':need(not(m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'Unexpected stage certificate')
  expected={'create':1,'upload':2,'update':4,'publish':1}[kind]
  need(len(w.native.calls)-before[0]==expected and w.appends==before[1],'Unexpected mutation count')
  child=cold(w,action)
  (w.place/'ADVERSARY_ONLY_RETURNED_BODY_SPY.json').write_text(json.dumps(spy['body'],indent=2)+'\n')
  result={'case':label,'status':'PASS','action':action,'kind':kind,'failure_boundary':boundary,'error':e,'original_file':path,'entire_returned_object_typed_equal':True,'actor_custody_pin':c.pin(Path(path).read_bytes()),'hold_references_original':True,'foreign_canonical_bytes_preserved':boundary=='canonical_state','native_context_failure_reached':bool(native_hits),'known_id':777,'native_mutations':w.native.calls,'contested_mutation_delta':expected,'appends':w.appends,'cold_reentry':child,'source_manifest_sha256':MS,'bootstrap_sha256':BS,'actual_effects':0}
  (DEST/(label+'.json')).write_text(json.dumps(result,indent=2)+'\n');RETENTION.append(result);archive_completed()
need(not model.ATTEMPTS,'Actual external escape attempted')
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_manifest_sha256':MS,'bootstrap_sha256':BS,'cases':RETENTION,'hot_parsed_invocations':len(CLI_INVOCATIONS),'cold_fresh_process_invocations':len(RETENTION),'actual_effects':0,'publication_ready':False,'child_script_sha256':CHILD_PIN,'trusted_preparation_controller_child_only':True}
(ROOT/'private/NATIVE_ONLY_RETENTION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='cases'},indent=2))
