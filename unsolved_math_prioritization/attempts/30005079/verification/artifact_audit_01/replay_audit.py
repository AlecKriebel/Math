"""Reproduce frozen PR888 auxiliary programs in this audit's own private scratch.
The source directory is read only by this harness. No Git mutations occur.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, ast, hashlib, json, os, shutil, subprocess, sys, time

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--python', type=Path, required=True)
a = p.parse_args()
source = a.source.resolve()
out = Path(__file__).resolve().parent
scratch = out / 'private_tmp' / 'replay_runs'
scratch.mkdir(parents=True, exist_ok=True)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def pins(root):
    return {q.relative_to(root).as_posix(): {'sha256': digest(q.read_bytes()), 'bytes': q.stat().st_size}
            for q in sorted(root.rglob('*')) if q.is_file()}

before = pins(source)
env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['TMPDIR'] = str(scratch)
receipts = []

def run(name, root, script, optimized=False, extra=()):
    command = [str(a.python.absolute()), '-B'] + (['-O'] if optimized else []) + [str(root / script), *extra]
    start = time.monotonic()
    r = subprocess.run(command, cwd=scratch, env=env, text=True, capture_output=True, timeout=300)
    item = {'name': name, 'optimized': optimized, 'exit_code': r.returncode,
            'seconds': round(time.monotonic()-start, 6), 'stdout': r.stdout,
            'stderr': r.stderr.replace(str(scratch), '<PRIVATE_TMP>')}
    receipts.append(item)
    print(name, r.returncode, item['seconds'], flush=True)
    return item

for optimized in [False, True]:
    root = scratch / ('direct_O' if optimized else 'direct_normal')
    shutil.copytree(source, root, dirs_exist_ok=True)
    authored = root / 'authored'
    authored.mkdir(exist_ok=True)
    shutil.copyfile(source / 'PROOF.md', authored / 'PROOF_CANDIDATE_v4.md')
    for script, result in [('checks/verify_construction.py','checks/CHECK_RESULTS.json'),
                           ('audits/reviewer_b/independent_checks.py','audits/reviewer_b/INDEPENDENT_CHECK_RESULTS.json')]:
        item = run(('optimized_' if optimized else 'normal_')+Path(script).stem, root, script, optimized)
        data = (root / result).read_bytes()
        item['result_sha256'] = digest(data)
        item['result_bytes'] = len(data)
        item['matches_frozen_result_bytes'] = item['exit_code'] == 0 and data == (source / result).read_bytes()

root = scratch / 'driver'
shutil.copytree(source, root, dirs_exist_ok=True)
packet_before = pins(root)
run('full_original_driver_normal', root, 'verify_publication.py')
run('full_original_driver_optimized_expected_rejection', root, 'verify_publication.py', True)
packet_after = pins(root)

# Reviewed, minimal, externally located audit hook: observe child invocations while
# executing the unchanged original driver. This is not the baseline replay above.
probe = scratch / 'trace_driver.py'
probe.write_text('import json,runpy,sys\nfrom pathlib import Path\n'
                 'events=[]\n'
                 'def observe(event,args):\n'
                 ' if event=="subprocess.Popen":\n'
                 '  events.append({"event":event,"argv":[Path(str(x)).name for x in args[1]],"python_environment_keys":sorted(k for k in (args[3] or {}) if k.startswith("PYTHON"))})\n'
                 'sys.addaudithook(observe)\n'
                 'target=sys.argv[1]; sys.argv=[target]\n'
                 'runpy.run_path(target,run_name="__main__")\n'
                 'print("CHILD_TRACE="+json.dumps(events,sort_keys=True))\n')
r = subprocess.run([str(a.python.absolute()), '-B',str(probe),str(root/'verify_publication.py')],cwd=scratch,env=env,text=True,capture_output=True,timeout=300)
receipts.append({'name':'unchanged_driver_under_audit_hook','exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr.replace(str(scratch),'<PRIVATE_TMP>')})

# Actual optimized interpreter behavior is measured on controlled source mutants.
for control in ['missing_candidate','bad_fan']:
    for optimized in [False,True]:
        root = scratch / (control + ('_O' if optimized else '_normal'))
        shutil.copytree(source,root,dirs_exist_ok=True)
        if control == 'missing_candidate':
            script = 'audits/reviewer_b/independent_checks.py'
        else:
            script = 'checks/verify_construction.py'
            q=root/script
            old=q.read_text(); new=old.replace('normals=[(1,0),(0,1),(-1,1),(0,-1)]','normals=[(2,0),(0,1),(-1,1),(0,-1)]')
            if old==new:
                raise RuntimeError('Mutant replacement failed')
            q.write_text(new)
        run(control+('_optimized' if optimized else '_normal'),root,script,optimized)

versions = subprocess.run([str(a.python.absolute()),'-B','-c','import sys,sympy,mpmath,json; print(json.dumps({"python":sys.version,"sympy":sympy.__version__,"mpmath":mpmath.__version__,"optimize":sys.flags.optimize}))'],env=env,text=True,capture_output=True,check=True)
result = {'timestamp_utc':datetime.now(timezone.utc).isoformat(),'runtime':json.loads(versions.stdout),
          'source_before':before,'source_after':pins(source),'source_unchanged':before==pins(source),
          'driver_packet_unchanged':packet_before==packet_after,'runs':receipts,
          'scope':'Observed finite auxiliary replay, child invocation, and optimize controls; no mathematical acceptance.'}
(out/'REPLAY_RECEIPTS.json').write_text(json.dumps(result,indent=2)+'\n')
