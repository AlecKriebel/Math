"""Prefreeze exact candidate buffers, no physical final source manifest yet."""
from pathlib import Path
import json,hashlib,datetime,copy,os
ROOT=Path(__file__).resolve().parent;S=ROOT/'source'
if(S/'SOURCE_MANIFEST.json').exists():raise RuntimeError('Candidate only before sole freeze')
def digest(b):return hashlib.sha256(b).hexdigest()
CANDIDATE=(json.dumps({q.name:{'bytes':len(q.read_bytes()),'sha256':digest(q.read_bytes())}for q in sorted(S.iterdir())},sort_keys=True,indent=2)+'\n').encode()
saved=ROOT/'private/candidate_inputs16_02';saved.mkdir()
for q in S.iterdir():(saved/q.name).write_bytes(q.read_bytes())
(saved/'SOURCE_MANIFEST.json').write_bytes(CANDIDATE)
outside_read=Path.read_bytes
def candidate_read(path):return CANDIDATE if path==S/'SOURCE_MANIFEST.json'else outside_read(path)
Path.read_bytes=candidate_read
engine=ROOT/'ENGINE17.py';text=engine.read_text().replace("DEST=REVIEW/'private'/('final_phase17_'+MODE)","DEST=REVIEW/'private'/('candidate17_02_'+MODE)")
needle='    for p in SOURCE.iterdir():(src/p.name).write_bytes(p.read_bytes())';text=text.replace(needle,needle+"\n    (src/'SOURCE_MANIFEST.json').write_bytes(CANDIDATE)")
exec(compile(text,str(engine)+'[candidate MF/destination only]','exec',dont_inherit=True,optimize=0),globals())
RESULT=[]
def done(label,w,v):
 v={'case':label,'native':w.native.calls,'appends':w.appends,'actual_effects':0,**v}
 (DEST/(label+'.json')).write_text(json.dumps(v,indent=2)+'\n');RESULT.append(v);archive_completed()
w=setup('candidate_full_positive');actions=[]
with w.installed():
 for action in ['resume-stage','publish','verify-public','ledger']:
  a,e=run(w,action);actions.append([action,a,e]);need(e is None,'Candidate positive '+str(e))
done(w.place.name,w,{'actions':actions,'status':'PASS'})
for boundary in ['secondary_fact','combined_first_receipt']:
 w=setup('candidate_create_'+boundary);spy={};hit=[];method=w.native.create
 def returned(md):v=method(md);spy['body']=copy.deepcopy(v);return v
 w.native.create=returned;writer=c.durable
 def after_fsync(path,value):
  writer(path,value)
  selected=path.name=='CREATE_RETURNED_KNOWN_ID.json'if boundary=='secondary_fact'else path.name.startswith('service_original_')and value.get('kind')=='create'
  if selected:
   with path.open('ab')as h:h.write(b'\n');h.flush();os.fsync(h.fileno())
   hit.append(str(path))
 with model.patch((c,'durable',after_fsync)),w.installed():a,e=run(w,'resume-stage')
 originals=[(q,json.loads(q.read_bytes()))for q in m.PRIVATE.glob('service_original_*.json')]
 exact=[(q,v)for q,v in originals if v['kind']=='create'and m.SHEET_POLICY.typed_equal(v['response'],spy.get('body'))]
 holds=[json.loads(q.read_bytes())for q in m.RUNTIME.glob('CONSUMED_RESPONSE17_HOLD_*')]
 need(e and hit and len(exact)==1 and holds,'Candidate lost body/HOLD')
 q,v=exact[0];need(v['known_service_fact']['returned_positive_id']==777 and holds[-1]['original_response']['path']==str(q),'Combined known fact or pointer lost')
 need(len(w.native.calls)==1 and not(m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'Unexpected continuation')
 if boundary=='combined_first_receipt':need(holds[-1]['original_response']['expected_integrity_verified']is False,'Altered first receipt verified')
 done(w.place.name,w,{'status':'PASS','error':e,'boundary':boundary,'complete_original_and_known_fact_retained':True})
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_manifest_sha256':MS,'candidate_bootstrap_sha256':BS,'cases':RESULT,'parsed_invocations':len(CLI_INVOCATIONS),'virtual_initial_manifest_only':True,'actual_effects':0,'publication_ready':False}
(ROOT/'private/CANDIDATE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='cases'},indent=2))
