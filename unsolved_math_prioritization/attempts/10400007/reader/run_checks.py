#!/usr/bin/env python3
"""Isolated selected finite replay; two source-input checks are explicitly excluded."""
import ast,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
import sympy,mpmath
ROOT=Path(__file__).resolve().parent
# entry point, retained baseline, whether the checker regenerates that artifact
CHECKS=[
 ('pass1_audit/independent_checks.py','pass1_audit/INDEPENDENT_CHECK_RESULTS.json',True),
 ('pass1_configuration/check_neutral_graph_complex.py','pass1_configuration/NEUTRAL_GRAPH_CHECKS.json',True),
 ('pass1_floer/verify_algebra.py','pass1_floer/VERIFICATION.json',False),
 ('pass1_validation/verify_examples.py','pass1_validation/EXACT_CHECK_RESULTS.json',False),
 ('pass2_audit/independent_checks.py','pass2_audit/INDEPENDENT_CHECK_RESULTS.json',True),
 ('pass2_configuration/check_enriched_pairing.py','pass2_configuration/EXACT_ENRICHMENT_CHECKS.json',True),
 ('pass2_descent/verify_local_checks.py','pass2_descent/LOCAL_CHECK_RESULTS.json',True),
 ('pass2_floer/run_checks.py','pass2_floer/VERIFICATION.json',True),
 ('pass2_validation/check_floer_fibers.py','pass2_validation/FLOER_FIBERS.json',False),
 ('pass2_validation/check_su2_calibration.py','pass2_validation/SU2_CALIBRATION.json',False)]
EXTERNAL=[
 {'script':'pass2_validation/check_pd_k11n42.py','input_bytes':874,'input_sha256':'8902d73feb07f44aa1bc13a39e29e2ac0a9a2957254ab78132b99799c8e8a266','source_url':'https://katlas.org/wiki/K11n42','derived_result':'pass2_validation/K11N42_REPLAY.txt'},
 {'script':'pass2_configuration/check_higher_rank_kt.py','input_bytes':1046,'input_sha256':'d441e8606b116f7994fd9b5e6f166ff656fe9c2bfe2b0d56c7ae2c40148acd24','source_url':'https://webhomes.maths.ed.ac.uk/~v1ranick/papers/wada.pdf','derived_result':'pass2_configuration/HIGHER_RANK_KT_CHECKS.json'}]
MODES=[('normal',[]),('optimized',['-O']),('double_optimized',['-OO'])]
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def snapshot():return {p.relative_to(ROOT).as_posix():digest(p.read_bytes()) for p in ROOT.rglob('*') if p.is_file()}
def main():
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None)
 cp=subprocess.run([sys.executable,'-I','-B',str(ROOT/'verify_package.py')],capture_output=True,env=env,timeout=30)
 require(cp.returncode==0,'Initial package integrity failed: '+cp.stderr.decode())
 before=snapshot();records=[];external=[]
 with tempfile.TemporaryDirectory(prefix='jones-public-replay-') as tmp:
  for rel,baseline,writes in CHECKS:
   require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((ROOT/rel).read_text()))),'Optimization-sensitive assert in '+rel)
   expected=(ROOT/baseline).read_bytes();outputs=[]
   for mode,flags in MODES:
    work=Path(tmp)/(Path(rel).parent.name+'-'+Path(rel).stem+'-'+mode);shutil.copytree(ROOT,work)
    for p in work.rglob('*'):
     if p.is_file():p.chmod(0o644)
    cp=subprocess.run([sys.executable,'-I','-B',*flags,str(work/rel)],cwd=work,env=env,capture_output=True,timeout=240)
    require(cp.returncode==0,'Checker failed '+rel+' '+mode+': '+cp.stderr.decode())
    require(cp.stderr==b'','Unexpected stderr '+rel+' '+mode)
    if writes:require((work/baseline).read_bytes()==expected,'Regenerated baseline differs '+rel+' '+mode)
    else:require(cp.stdout==expected,'Stdout differs from retained baseline '+rel+' '+mode)
    outputs.append(cp.stdout)
    records.append({'script':rel,'script_sha256':digest((ROOT/rel).read_bytes()),'mode':mode,'baseline':baseline,'baseline_bytes':len(expected),'baseline_sha256':digest(expected),'stdout_bytes':len(cp.stdout),'stdout_sha256':digest(cp.stdout),'exact_baseline_match':True,'regenerated_artifact':writes,'returncode':0})
   require(len(set(outputs))==1,'Optimization modes disagree '+rel)
  for record in EXTERNAL:
   rel=record['script'];modes=[]
   for mode,flags in MODES:
    work=Path(tmp)/('external-'+Path(rel).stem+'-'+mode);shutil.copytree(ROOT,work)
    cp=subprocess.run([sys.executable,'-I','-B',*flags,str(work/rel)],cwd=work,env=env,capture_output=True,timeout=60)
    require(cp.returncode!=0,'External-input checker succeeded without input '+rel)
    require(b'required' in cp.stderr.lower() or b'input_json' in cp.stderr.lower(),'Missing-input failure not explicit '+rel)
    modes.append(mode)
   external.append({**record,'input_bundled':False,'mathematical_replay_performed':False,'reason':'Separately sourced fixture excluded from publication.','missing_input_rejected_in_modes':modes})
 require(before==snapshot(),'Source payload modified by replay')
 print(json.dumps({'status':'PASS','script_count':len(CHECKS),'execution_count':len(records),'modes':[m for m,_ in MODES],'optimization_sensitive_asserts':False,'source_tree_modified':False,'python_version':sys.version.split()[0],'sympy_version':sympy.__version__,'mpmath_version':mpmath.__version__,'scope':'Selected self-contained finite checks only; quantified topology relies on authored proofs and stated primary theorems. Local descent includes labeled numerical diagnostics.','checks':records,'external_input_checks':external,'external_input_mathematical_replays':0,'missing_input_rejection_invocations':6},indent=2,sort_keys=True))
if __name__=='__main__':main()
