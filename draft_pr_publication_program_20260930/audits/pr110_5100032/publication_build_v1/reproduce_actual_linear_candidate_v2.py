from pathlib import Path
from datetime import datetime,timezone
import contextlib,hashlib,io,json,os,sys,types
A=Path(__file__).resolve().parents[1];V=A/'actual_native_candidate_adversary_20261006';O=A/'root_actual_candidate_reproduction_v2_20261006'
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(f):return {'path':str(f.relative_to(A)),**hp(f.read_bytes())}
def can(x):return (json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def need(v,m):
 if not v:raise RuntimeError(m)
O.mkdir(exist_ok=False)
(O/'START.json').write_bytes(can({'UTC':datetime.now(timezone.utc).isoformat(),'actual_root_PID':os.getpid(),'schema':'pr110-root-readonly-reproduction-start/v1'}))
def save(name,value):
 need(Path(name).name==name,'Dedicated root output')
 f=O/name;need(not f.exists(),'Unique root reproduction');f.write_bytes(can(value))
sources=[]
for filename in ['verify_linear_carryforward_actual_candidate.py','audit_linear_carryforward_actual_custody.py']:
 f=V/filename;body=f.read_bytes();sources.append(pin(f));m=types.ModuleType('root_'+filename.removesuffix('.py'));m.__file__=str(f);sys.modules[m.__name__]=m
 exec(compile(body,str(f),'exec'),m.__dict__)
 m.save=save;m.v.save=save
 out=io.StringIO()
 try:
  with contextlib.redirect_stdout(out):m.main()
 except BaseException as e:
  save('FAILURE.json',{'UTC':datetime.now(timezone.utc).isoformat(),'actual_root_PID':os.getpid(),'error_type':type(e).__name__,'error':str(e),'source_pin':pin(f),'actual_read_journal':m.v.journal,'candidate_clearance':False});raise
 (O/(filename+'.stdout.json')).write_text(out.getvalue())
 need(hp(f.read_bytes())==hp(body),'Reviewed verifier unchanged')
r={'schema':'pr110-root-actual-candidate-reproduction/v1','UTC':datetime.now(timezone.utc).isoformat(),'actual_root_PID':os.getpid(),'actual_output_reproduction_complete':True,'actual_full_body_offer_and_DIFF_application_complete':True,'actual_28_child_outer_resource_custody_complete':True,'native_assess_calls':0,'service_writes':0,'Git_mutations':0,'reviewed_verification_source_pins':sources,'output_pins':[pin(f) for f in sorted(O.iterdir()) if f.is_file()],'actual_candidate_clearance_issued':False}
save('ROOT_REPRODUCTION_COMPLETE.json',r);print(json.dumps({'actual_root_PID':os.getpid(),'completed':True,'record_pin':pin(O/'ROOT_REPRODUCTION_COMPLETE.json')}))
