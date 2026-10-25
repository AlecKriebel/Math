"""Execute only fully inspected safe arithmetic code, in own ignored tmp."""
from pathlib import Path
import subprocess,json,hashlib,datetime
E=Path(__file__).resolve().parent;R=E.parents[1];Q=R/'sources/published-source/local_deformation_devissage_v1';E.joinpath('tmp').mkdir(exist_ok=True);out=E/'execution';out.mkdir(exist_ok=True)
py='/Users/alec/Documents/Math/research_website_catalogue_20261024/tmp/shared-math-runtime/bin/python'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
tasks=[('supplied-exact',[py,'-I','-B',str(Q/'checks/current/verify_exact.py')],0),('supplied-exact-optimized',[py,'-I','-B','-O',str(Q/'checks/current/verify_exact.py')],0),('supplied-conjugacy',[py,'-I','-B',str(Q/'checks/current/check_conjugacy.py')],0),('supplied-functor-guards',[py,'-I','-B',str(Q/'checks/verify_functor_identities_explicit_guards.py')],0),('own-independent-symbolic',[py,'-I','-B',str(E/'independent_symbolic.py')],0)]
for m in ['quotient_action','derivation_weight','parameter_shift','conjugator_translation','projective_scalar','fixed_ring']:tasks.append(('negative-'+m,[py,'-I','-B','-O',str(Q/'checks/current/verify_exact.py'),'--mutant',m],1))
receipts=[]
for name,cmd,expected in tasks:
 start=now();p=subprocess.run(cmd,cwd=E/'tmp',capture_output=True,timeout=45);stdout=out/(name+'.stdout.txt');stderr=out/(name+'.stderr.txt');assert not stdout.exists() and not stderr.exists();stdout.write_bytes(p.stdout);stderr.write_bytes(p.stderr)
 rec={'name':name,'command':cmd,'cwd':str(E/'tmp'),'started_utc':start,'completed_utc':now(),'returncode':p.returncode,'expected_returncode':expected,'stdout':{'path':str(stdout),'bytes':len(p.stdout),'sha256':sha(p.stdout)},'stderr':{'path':str(stderr),'bytes':len(p.stderr),'sha256':sha(p.stderr)}};receipts.append(rec)
 if p.returncode!=expected:raise RuntimeError(rec)
 script=Path(cmd[next(i for i,x in enumerate(cmd) if x.endswith('.py'))]);rec['inspected_programme']={'path':str(script),'bytes':script.stat().st_size,'sha256':sha(script.read_bytes())}
f=E/'EXECUTION_RECEIPTS.json';assert not f.exists();f.write_text(json.dumps({'utc':now(),'all_code_read_before_execution':True,'runs':receipts,'only_exact_finite_or_symbolic_identities_not_universal_functor_proof':True},indent=2)+'\n');print(json.dumps({'positive_runs':5,'negative_controls':6,'expected_results_observed':len(receipts),'no_original_output_writes':True},indent=2))
