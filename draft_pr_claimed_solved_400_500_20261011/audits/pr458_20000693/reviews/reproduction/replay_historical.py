#!/usr/bin/env python3
"""Isolated normal/optimized reproduction. No frozen-source writes."""
import ast, concurrent.futures, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CASE=ROOT.parents[1]
FROZEN=CASE/'source_snapshot/unsolved_math_prioritization/attempts/20000693'
PRIVATE=ROOT/'private_cases/historical'
PRIVATE.mkdir(parents=True,exist_ok=True)
JOBS=[('author', 'author/verify.py', 'verification.json', 'author/verification.json', False),
      ('reviewer', 'review/reviewer_checks.py', 'REVIEWER_CHECKS.json', 'review/REVIEWER_CHECKS.json', False),
      ('publication', 'verify_publication.py', None, None, False),
      ('publication_replay', 'verify_publication.py', None, None, True)]
def run(job, optimized):
    label, script, output, expected, replay=job
    destination=PRIVATE/(label+('_optimized' if optimized else '_normal'))
    if destination.exists(): shutil.rmtree(destination)
    destination.mkdir(parents=True)
    if label.startswith('publication'):
        packet=destination/'packet'
        shutil.copytree(FROZEN,packet)
        copied=packet/script
    else:
        copied=destination/Path(script).name
        shutil.copyfile(FROZEN/script,copied)
    env=os.environ.copy()
    env.pop('PYTHONOPTIMIZE',None)
    if optimized: env['PYTHONOPTIMIZE']='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    command=[sys.executable,str(copied)] + (['--replay'] if replay else [])
    result=subprocess.run(command,cwd=destination,capture_output=True,env=env,timeout=240)
    record={'label':label,'mode':'optimized' if optimized else 'normal','inherited_PYTHONOPTIMIZE':env.get('PYTHONOPTIMIZE'),
      'returncode':result.returncode,'stdout_bytes':len(result.stdout),'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),
      'stderr':result.stderr.decode(errors='replace'),'command_switch_minus_O':False}
    if result.returncode==0:
        record['report']=json.loads(result.stdout)
        if output:
            generated=(destination/output).read_bytes(); frozen=(FROZEN/expected).read_bytes()
            record['generated_bytes']=len(generated); record['generated_sha256']=hashlib.sha256(generated).hexdigest()
            record['generated_exactly_frozen']=generated==frozen; record['stdout_exactly_frozen']=result.stdout==frozen
    else: record['stdout']=result.stdout.decode(errors='replace')
    return record
jobs=[(j,o) for j in JOBS for o in (False,True)]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records=list(pool.map(lambda x: run(*x),jobs))
assertions={}
for name in ('author/verify.py','review/author_verify.py','review/reviewer_checks.py','verify_publication.py'):
    tree=ast.parse((FROZEN/name).read_text()); assertions[name]=sum(isinstance(n,ast.Assert) for n in ast.walk(tree))
report={'reviewer':'/root/pr458_reproduction','pr':458,'problem_id':'20000693','frozen_head':'87a39f7b4e5ef81aacf98464f86586cc95684d7f',
 'python_version':sys.version,'assert_nodes_disabled_by_optimization':assertions,'records':records,
 'all_baselines_exit_zero':all(x['returncode']==0 for x in records),'all_author_reviewer_outputs_exactly_frozen':all(x.get('generated_exactly_frozen',True) and x.get('stdout_exactly_frozen',True) for x in records)}
(ROOT/'HISTORICAL_REPLAYS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='records'},indent=2))
for r in records:print(r['label'],r['mode'],r['returncode'],r['stdout_sha256'])
