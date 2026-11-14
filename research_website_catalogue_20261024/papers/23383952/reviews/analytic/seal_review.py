"""Seal only this analytic review; no source builder/finalizer is invoked."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
O=Path(__file__).resolve().parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def bnd(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
if (O/'MANIFEST.json').exists() or (O/'SEAL.json').exists():raise RuntimeError('own final seal already exists')
cmd=[sys.executable,'-B',str(O/'verify_review.py'),'--preseal'];start=now();r=subprocess.run(cmd,capture_output=True,timeout=60)
(O/'READONLY_PRESEAL.stdout').write_bytes(r.stdout);(O/'READONLY_PRESEAL.stderr').write_bytes(r.stderr)
write(O/'READONLY_PRESEAL.execution.json',{'started_utc':start,'finished_utc':now(),'command':cmd,'exit_code':r.returncode,'stderr_bytes':len(r.stderr),'arithmetic_or_source_programs_replayed':False})
if r.returncode!=0 or r.stderr or json.loads(r.stdout)['status']!='PASS':raise RuntimeError('actual read-only verification failure retained')
files=sorted([p for p in O.rglob('*') if p.is_file()],key=lambda p:str(p.relative_to(O)))
m={'utc':now(),'record_id':23383952,'role':'analytic','payload_files':len(files),'files':[{'relative_path':str(p.relative_to(O)),**bnd(p)} for p in files],'excludes_only':['MANIFEST.json','SEAL.json']};write(O/'MANIFEST.json',m)
s={'utc':now(),'record_id':23383952,'role':'analytic','assessment':'FULL_ORIGINAL_FINITE_THEOREM_AND_ATTAINMENT_SUPPORTED','manifest':bnd(O/'MANIFEST.json'),'payload_files':len(files),'report':bnd(O/'REPORT.md'),'custom_verdict':bnd(O/'VERDICT.json'),'initial_seal':bnd(O/'INITIAL_SEAL.json'),'proof_validation':bnd(O/'PROOF_VALIDATION.md'),'read_only_verifier':bnd(O/'verify_review.py'),'protected_original_and_prior_stage_bindings':914,'source_repair':False,'promotion_authority':False,'priority_or_openness_certified':False,'follow_up':None,'completion_percent_for_this_analytic_lane':100,'overall203_complete':False};write(O/'SEAL.json',s)
print(json.dumps({'utc':s['utc'],'manifest':bnd(O/'MANIFEST.json'),'seal':bnd(O/'SEAL.json'),'payload_files':len(files),'report':s['report'],'verdict':s['custom_verdict']}))
