"""Root read-only custody adoption, without repeating scientific campaigns."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,os,subprocess,sys
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parent;R=O.parent;S=R.parent/'sources'
H=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def load(f):return json.loads(f.read_bytes())
pins={'scope':('SEAL.json','c645d69ebaa1d992f48abd69066f920a72704691a0b23201783c9a358300c875'),'analytic':('FINAL_SEAL.json','607159f3f6f9f4021afaec5279610a9378a8af14f746f73bfa363b75eedc822d'),'adversarial':('FINAL_SEAL.json','c11409e89fd583567b50c72b83bd28c92932e9e9fb4ed99ff9bc447bb7ed65a9')}
for name,(filename,pin) in pins.items():need(H(R/name/filename)==pin,'exact family seal '+name)
def run(name):
    f=R/name/'verify_packet.py';args=[sys.executable,'-B',str(f)]
    result=subprocess.run(args,capture_output=True,text=True,timeout=60,env={k:v for k,v in os.environ.items() if k!='PYTHONOPTIMIZE'})
    need(result.returncode==0 and not result.stderr,'read-only packet '+name)
    return {'lane':name,'args':args,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'script_sha256':H(f)}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:runs=list(ex.map(run,['scope','adversarial']))
# The analytic packet's default verifier repeats symbolic campaigns and source
# guard functions. Its already completed receipts are authenticated here instead.
A=R/'analytic';seal=load(A/'FINAL_SEAL.json');need(H(A/'FINAL_MANIFEST.json')==seal['manifest_sha256'],'analytic manifest seal')
m=load(A/'FINAL_MANIFEST.json');names=set()
for row in m['files']:
    f=A/row['path'];need(f.resolve().is_relative_to(A.resolve()) and not f.is_symlink() and f.is_file() and f.stat().st_size==row['bytes'] and H(f)==row['sha256'],'analytic owned '+row['path']);names.add(row['path'])
actual={str(f.relative_to(A)) for f in A.rglob('*') if f.is_file() and not f.is_relative_to(A/'cache/deps') and not f.is_relative_to(A/'cache/tmp')}
need(actual==names|{'FINAL_MANIFEST.json','FINAL_SEAL.json'},'analytic exact owned set')
inputs=load(A/'INPUT_BINDINGS.json')['files']
for name,row in inputs.items():
    f=Path(name);need(f.is_file() and f.stat().st_size==row['bytes'] and H(f)==row['sha256'],'analytic external original '+name)
full=(A/'FULL_REPLAY_NORMAL.json').read_bytes();need(full==(A/'FULL_REPLAY_OPTIMIZED.json').read_bytes() and hashlib.sha256(full).hexdigest()=='8e46c0fdb6a61ca4ec1be99573e3e2aa97fa3507afb1fc64beae5f36d3503ce8','stored genuine full profiles')
receipt=json.loads(full);need(receipt['status']=='PASS' and receipt['profile']=='full' and receipt['dependencies']=={'mpmath':'1.3.0','sympy':'1.14.0'} and receipt['history_and_payloads_unchanged'] is True and receipt['finite_checks_replace_analytic_proof'] is False,'full profile scope')
need(receipt['independent_symbolic']['actual_intended_rejection_executions']==32 and receipt['explicit_guard_rejection_controls']==13,'actual stored rejections')
n=load(A/'INDEPENDENT_NORMAL.json');q=load(A/'INDEPENDENT_OPTIMIZED.json');n.pop('optimized');q.pop('optimized');need(n==q and n['exact_checks']==46 and n['false_identities_rejected']==8,'independent recorded exact controls')
need(H(S/'SOURCE_READY.json')=='aeb11ade749cbe2c6147374642fc3fed6c5d88d323dbae59340b3fb8dfbe4535','original source ready')
return_value={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ROOT_ALL3_SEALS_AND_NATIVE_CUSTODY_WITHOUT_SCIENTIFIC_REPLAY','actual_read_only_scope_and_adversarial_runs':runs,'analytic_root_direct_hash_only_closure':{'owned_files':len(names),'external_original_bindings':len(inputs),'whole_stored_full_profiles_identical':True,'full_profile_sha256':hashlib.sha256(full).hexdigest(),'whole_full_profile_original':receipt,'independent_recorded_controls':n,'default_replaying_packet_verifier_not_executed':True},'scientific_programs_or_campaigns_reexecuted':False,'original_manuscript_or_review_writes':False,'human_or_formal_mathematical_certification':False}
print(json.dumps(return_value,indent=2))
