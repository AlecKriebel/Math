#!/usr/bin/env python3
"""Run own guards and one actual historical wrong-ratio probe in private copies."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,subprocess,json,hashlib,os,ast,sys
root=Path(__file__).resolve().parent
case=root.parent.parent
parser=argparse.ArgumentParser()
parser.add_argument('--historical-python',default=str(case/'reviews/reproduction/venv/bin/python'))
args=parser.parse_args()
records=[]
for mode in [0,1]:
    env=os.environ.copy();env['PYTHONOPTIMIZE']=str(mode)
    run=subprocess.run([sys.executable,str(root/'verify_whole.py')],capture_output=True,env=env)
    if run.returncode:raise RuntimeError(run.stderr.decode())
    (root/('CHECKS_OPTIMIZED.json' if mode else 'CHECKS_NORMAL.json')).write_bytes(run.stdout)
    for name in ['sharp_full_equality','dropped_deletion','wrong_deletion_sign','independent_prime_phases','ignored_finite_ratio','modulus_grouping','conjugate_grouping','wrong_barnes','extra_gamma']:
        r=subprocess.run([sys.executable,str(root/'verify_whole.py'),'--mutant',name],capture_output=True,env=env)
        if r.returncode!=1 or r.stdout:raise RuntimeError('invalid mutant accepted '+name)
        records.append({'mode':mode,'mutant':name,'exit_code':r.returncode,'stdout_bytes':len(r.stdout),'last_error':r.stderr.decode().splitlines()[-1]})
source=case/'source_snapshot/unsolved_math_prioritization/attempts/20000693/author/verify.py'
orig=source.read_text()
needle='==s.Rational(1,6);checks+=1'
if orig.count(needle)!=1:raise RuntimeError('author mutation anchor changed')
mutated=orig.replace(needle,'==s.Rational(1,7);checks+=1')
historical=[]
for mode in [0,1]:
    loc=root/'private_cases'/('historical_'+str(mode));loc.mkdir(parents=True,exist_ok=True)
    script=loc/'author_invalid_ratio.py';script.write_text(mutated)
    generated=loc/'verification.json'
    if generated.exists():generated.unlink()
    env=os.environ.copy();env['PYTHONOPTIMIZE']=str(mode)
    r=subprocess.run([args.historical_python,str(script)],cwd=loc,capture_output=True,env=env)
    report=generated.read_bytes() if generated.exists() else None
    frozen=source.with_name('verification.json').read_bytes()
    historical.append({'mode':mode,'mechanism':'wrong deletion ratio1/7 instead of1/6','exit_code':r.returncode,'stdout_bytes':len(r.stdout),'generated_report_exists':report is not None,'generated_report_equals_original_PASS':report==frozen,'stdout_equals_original_PASS':r.stdout==frozen,'last_error':r.stderr.decode().splitlines()[-1] if r.stderr else None})
    if (mode==0 and (r.returncode!=1 or r.stdout)) or (mode==1 and (r.returncode!=0 or report!=frozen or r.stdout!=frozen)):raise RuntimeError('historical negative unexpected result')
checks=json.loads((root/'CHECKS_NORMAL.json').read_text())
normal=(root/'CHECKS_NORMAL.json').read_bytes();opt=(root/'CHECKS_OPTIMIZED.json').read_bytes()
if normal!=opt:raise RuntimeError('fresh positive bytes disagree')
result={'captured_at_utc':datetime.now(timezone.utc).isoformat(),'fresh_normal_optimized_byte_identical':True,'positive_sha256':hashlib.sha256(normal).hexdigest(),'fresh_guards_per_mode':checks['guards'],'fresh_negative_subprocesses':records,'historical_wrong_ratio_runs':historical,'author_assert_nodes':sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(orig))),'fresh_guard_assert_nodes':sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((root/'verify_whole.py').read_text()))),'own_probe_not_a_source_repair':True}
(root/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','fresh_guards_per_mode':checks['guards'],'fresh_mutant_rejections':len(records),'historical_wrong_ratio_falsePASS_under_optimization':True,'fresh_output_sha256':result['positive_sha256']},indent=2))
