#!/usr/bin/env python3
"""Reproduce frozen author/reviewer outputs without changing those inputs."""
from pathlib import Path
from fractions import Fraction
import ast,datetime,hashlib,importlib.util,json,os,subprocess,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
SRC=HERE.parent/'submitted/unsolved_math_prioritization/attempts/9700040'
rows=[]
for script,old in [('verify_exact.py','exact_receipt.json'),('independent_review/independent_checks.py','independent_review/INDEPENDENT_CHECKS.json')]:
    run=subprocess.run([sys.executable,str(SRC/script)],cwd=HERE,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,timeout=90)
    data=json.loads(run.stdout);match=run.stdout==(SRC/old).read_bytes()
    rows.append({'script':script,'returncode':run.returncode,'stderr':run.stderr.decode(),
                 'stdout_sha256':hashlib.sha256(run.stdout).hexdigest(),'stdout_bytes':len(run.stdout),
                 'matches_historical_stdout_byte_for_byte':match,'complete_json_stdout':data})
    assert run.returncode==0 and match
spec=importlib.util.spec_from_file_location('replay_target',SRC/'stationary_law.py')
target=importlib.util.module_from_spec(spec);spec.loader.exec_module(target)
old_data=rows[1]['complete_json_stdout']; xs=tuple(map(Fraction,old_data['three_thresholds']))
comparison=[]
for rs,expected in old_data['raw_coefficients'].items():
    rtuple=ast.literal_eval(rs)
    actual=target.raw_by_size(xs,rtuple,len(expected)-1)
    comparison.append({'indices':rtuple,'expected_coefficients':expected,
                       'actual_coefficients':list(map(str,actual)),'all_match':list(map(str,actual))==expected})
assert all(c['all_match'] for c in comparison)
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,
         'historical_direct_coefficient_comparison':comparison,
         'historical_direct_coefficient_match_count':sum(len(c['actual_coefficients']) for c in comparison),
         'source_mutations':False,'limits':'Finite regression controls and counts are not analytic proof.'}
(HERE/'ORIGINAL_REPLAY_RECEIPTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','all_historical_outputs_byte_identical':True,
                  'counts':[r['complete_json_stdout'].get('assertions',r['complete_json_stdout'].get('exact_assertions')) for r in rows],
                  'historical_coefficient_matches':receipt['historical_direct_coefficient_match_count']}))
