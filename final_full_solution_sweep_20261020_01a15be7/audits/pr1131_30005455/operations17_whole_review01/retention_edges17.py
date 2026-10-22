"""Actual parser mutation-return custody after durable known facts and before checks."""
from pathlib import Path
import subprocess,sys,os,inspect
# Trusted preparation controller only: captured before full_controls blocks all
# actor process/network entry points. Only this exact own hashed child is run.
CONTROLLED_POPEN=subprocess.Popen
engine=Path(__file__).with_name('ENGINE17.py')
text=engine.read_text().replace("DEST=REVIEW/'private'/('final_phase17_'+MODE)","DEST=REVIEW/'private'/('retention_edges17_'+MODE)")
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

for boundary,kind in [('checked_source','create'),('approval','publish')]:
 label='original_'+kind+'_before_failed_'+boundary;action='publish'if kind=='publish'else'resume-stage'
 w=setup(label,'publish'if kind=='publish'else'stage');method=getattr(w.native,kind);spy={};changed={}
 def after_return(*args):
  value=method(*args);spy['body']=copy.deepcopy(value)
  if boundary=='checked_source':
   path=m.CONTEXT['source_root']/'sheet17.py';changed['path']=str(path);changed['bytes']=path.read_bytes()+b'\n# post-effect inert source drift\n';path.write_bytes(changed['bytes'])
  else:
   path=w.ad_path;v=json.loads(path.read_bytes());v['publication_ready']=False;changed['path']=str(path);changed['bytes']=(json.dumps(v,indent=1)+'\n').encode();path.write_bytes(changed['bytes'])
  return value
 setattr(w.native,kind,after_return);before=len(w.native.calls)
 with w.installed():a,e=run(w,action)
 originals={str(q):json.loads(q.read_bytes())for q in m.PRIVATE.glob('service_original_*.json')}
 exact=[p for p,v in originals.items()if v['kind']==kind and m.SHEET_POLICY.typed_equal(v['response'],spy.get('body'))]
 holds=[json.loads(q.read_bytes())for q in m.RUNTIME.glob('CONSUMED_RESPONSE17_HOLD_*')]
 need(e and len(exact)==1 and holds,'Post-effect source/approval lost original custody')
 need(any(v['path']==exact[0]and v['pin']==c.pin(Path(exact[0]).read_bytes())for h in holds for v in h['all_consumed_response_custody']),'Original HOLD reference missing')
 need(Path(changed['path']).read_bytes()==changed['bytes'],'Inert competing source/approval overwritten')
 need(json.loads((m.RUNTIME/'CREATE_RETURNED_KNOWN_ID.json').read_bytes())['id']==777,'Known id lost')
 need(len(w.native.calls)-before==1 and not(m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists()and not list(m.RUNTIME.glob('PRIVATE_PUBLICATION_STATE_*')),'Unexpected continuation/certificate')
 if kind=='create':need(not(m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'Stage certificate')
 child=cold(w,action)
 (w.place/'ADVERSARY_ONLY_RETURNED_BODY_SPY.json').write_text(json.dumps(spy['body'],indent=2)+'\n')
 v={'case':label,'status':'PASS','kind':kind,'failure_boundary':boundary,'error':e,'entire_returned_object_typed_equal':True,'actor_custody_pin':c.pin(Path(exact[0]).read_bytes()),'native_mutations':w.native.calls,'appends':w.appends,'cold_reentry':child,'actual_effects':0}
 (DEST/(label+'.json')).write_text(json.dumps(v,indent=2)+'\n');RETENTION.append(v);archive_completed()
need(not model.ATTEMPTS,'External escape')
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_manifest_sha256':MS,'bootstrap_sha256':BS,'cases':RETENTION,'hot_parsed_invocations':len(CLI_INVOCATIONS),'cold_fresh_process_invocations':len(RETENTION),'actual_effects':0,'publication_ready':False,'child_script_sha256':CHILD_PIN}
(ROOT/'private/RETENTION_LOCAL_EDGE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='cases'},indent=2))
