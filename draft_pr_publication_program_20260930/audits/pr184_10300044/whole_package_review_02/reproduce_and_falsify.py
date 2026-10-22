#!/usr/bin/env python3
"""Fresh executions of pinned extracted controls; no package writes.

Runs reuse existing interpreters. Environment independence is NOT claimed.
Mutation working copies are private and excluded from the public allowlist.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime, hashlib, json, subprocess, sys

ROOT = Path(__file__).resolve().parent
A = ROOT.parent
EXTRACTED = ROOT / 'private' / 'extracted_zip'
STDLIB = Path('/opt/homebrew/opt/python@3.14/bin/python3.14')
SYMPY = A / 'gv_algebra_reproduction_adversary/private/control_env/bin/python'
CONTROLS = EXTRACTED / 'controls'
RECEIPTS = ROOT / 'receipts'
RECEIPTS.mkdir(exist_ok=True)
MUTATIONS = ROOT / 'private' / 'mutations'
MUTATIONS.mkdir(exist_ok=True)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

jobs = []
names = ['verify_forms.py', 'independent_symbolic_checks.py',
         'independent_integrable_controls.py', 'finite_sampling_counterexample.py']
for name in names:
    for optimized in (False, True):
        jobs.append((name.removesuffix('.py') + ('_optimized' if optimized else '_ordinary'),
                     CONTROLS/name, name == 'independent_symbolic_checks.py', optimized, 0))

changes = {
 'verify_forms.py': {
   'false_guard': ('    if not b:', '    b = False\n    if not b:'),
   'wrong_GV_sign': ('density=add(mul(qz,der(pz,2)),scale(mul(pz,der(qz,2)),-1))',
                     'density=scale(add(mul(qz,der(pz,2)),scale(mul(pz,der(qz,2)),-1)),-1)'),
   'missing_compression_jacobian': ('scale(subz(density,a,l),1/l)', 'subz(density,a,l)'),
 },
 'independent_symbolic_checks.py': {
   'false_guard': ('    if not value:', '    value = False\n    if not value:'),
   'wrong_GV_sign': ('G=s.diff(q,z)*s.diff(p,z,2)-s.diff(p,z)*s.diff(q,z,2)',
                     'G=-(s.diff(q,z)*s.diff(p,z,2)-s.diff(p,z)*s.diff(q,z,2))'),
   'missing_compression_jacobian': ('g.subs(sub)/length', 'g.subs(sub)'),
 },
 'independent_integrable_controls.py': {
   'false_guard': (' if not b:', ' b = False\n if not b:'),
   'wrong_GV_sign': ('rho=(-6*zv**2', 'rho=-(-6*zv**2'),
   'missing_compression_jacobian': ('==rho/ell)', '==rho)'),
 },
 'finite_sampling_counterexample.py': {
   'wrong_unsampled_value': ('negative!=Q(-62,63)', 'negative!=Q(0)'),
   'false_grid_guard': ('if min(values)<=0:', 'if True:'),
 },
}
mutation_inventory = []
for name, variants in changes.items():
    source = (CONTROLS/name).read_text()
    for tag,(old,new) in variants.items():
        if old not in source:
            raise RuntimeError('Mutation target absent: '+name+' '+tag)
        target = MUTATIONS / (name.removesuffix('.py')+'__'+tag+'.py')
        target.write_text(source.replace(old,new))
        mutation_inventory.append({'path':str(target.relative_to(ROOT)), 'source':name,
                                   'tag':tag, 'sha256':digest(target),
                                   'replacement_count':source.count(old)})
        for optimized in (False,True):
            jobs.append((target.stem+('_optimized' if optimized else '_ordinary'),
                         target,name=='independent_symbolic_checks.py',optimized,1))

def run(job):
    tag,path,symbolic,optimized,expected = job
    interpreter = SYMPY if symbolic else STDLIB
    flags = ['-E','-B','-P'] if symbolic else ['-E','-S','-B','-P']
    if optimized:flags.append('-O')
    cmd = [str(interpreter),*flags,str(path)]
    started = datetime.datetime.now(datetime.timezone.utc)
    result = subprocess.run(cmd,cwd=path.parent,capture_output=True,text=True,timeout=240)
    ended = datetime.datetime.now(datetime.timezone.utc)
    (RECEIPTS/(tag+'.stdout.txt')).write_text(result.stdout)
    (RECEIPTS/(tag+'.stderr.txt')).write_text(result.stderr)
    record={'tag':tag,'UTC_started':started.isoformat(),'UTC_finished':ended.isoformat(),
      'elapsed_seconds':(ended-started).total_seconds(),'command':cmd,
      'script_sha256':digest(path),'returncode':result.returncode,
      'expected_exit_status':expected,'accepted':result.returncode==expected,
      'stdout_sha256':hashlib.sha256(result.stdout.encode()).hexdigest(),
      'stderr_sha256':hashlib.sha256(result.stderr.encode()).hexdigest()}
    (RECEIPTS/(tag+'.json')).write_text(json.dumps(record,indent=2)+'\n')
    return record

with ThreadPoolExecutor(max_workers=3) as pool:
    records=list(pool.map(run,jobs))
summary={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'scope':'Fresh execution of actual archive bytes, in reused interpreters; no independent environment claim.',
  'baseline_runs':8,'negative_runs':len(records)-8,'all_expected_exit_statuses':all(r['accepted'] for r in records),
  'mutations':mutation_inventory,'runs':records}
(ROOT/'FRESH_EXECUTION.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ('runs','mutations')},indent=2))
if not summary['all_expected_exit_statuses']:
    for r in records:
        if not r['accepted']:print('FAILED EXPECTATION',r['tag'],r['returncode'])
    raise SystemExit(1)
