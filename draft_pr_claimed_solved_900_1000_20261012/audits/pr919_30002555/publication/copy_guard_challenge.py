#!/usr/bin/env python3
"""Corrupt a disposable checker copy and require rejection before execution."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

HARNESS = r'''
import importlib.util,json,sys
from pathlib import Path
root=Path(sys.argv[1]);pin=sys.argv[2];work=Path(sys.argv[3]);marker=Path(sys.argv[4])
spec=importlib.util.spec_from_file_location('copy_boundary_verifier',root/'verify_package.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.validate(root,pin)
original=m.shutil.copytree
def tampered_copy(source,destination,*args,**kwargs):
    result=original(source,destination,*args,**kwargs)
    if Path(destination).name=='package':
        (Path(destination)/'run_checked.py').write_text(
            'from pathlib import Path\nPath('+repr(str(marker))+').write_text("UNSAFE_EXECUTION")\n')
    return result
m.shutil.copytree=tampered_copy
caught=''
try:m.worker(root,pin,work)
except Exception as error:caught=str(error)
if marker.exists() or 'Payload fingerprint mismatch: run_checked.py' not in caught:
    raise RuntimeError('Copy executed or was not authenticated before execution: '+caught)
m.validate(root,pin)
print(json.dumps({'status':'PASS','copy_rejected_before_execution':True,
                  'marker_created':False,'worker_optimization':sys.flags.optimize,
                  'worker_isolated':sys.flags.isolated}))
'''
LAUNCHER = r'''
import os,subprocess,sys
env=dict(os.environ)
for name in ('PYTHONOPTIMIZE','PYTHONPATH','PYTHONHOME'):env.pop(name,None)
proc=subprocess.run([sys.executable,'-I','-B',*sys.argv[1:]],env=env)
raise SystemExit(proc.returncode)
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bundle', type=Path, required=True)
    ap.add_argument('--expected-manifest', required=True)
    ap.add_argument('--python', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--workdir', type=Path)
    args = ap.parse_args()
    root = args.bundle.absolute()
    if hashlib.sha256((root/'PACKAGE_MANIFEST.json').read_bytes()).hexdigest() != args.expected_manifest:
        raise RuntimeError('External package anchor mismatch')
    temporary = (args.workdir or root.parent/('.'+root.name+'-copy-challenge-work')).absolute()
    output = args.output.absolute()
    if temporary == root or root in temporary.parents or root in output.parents:
        raise RuntimeError('Test work and output must lie outside the closed package')
    temporary.mkdir(parents=True, exist_ok=True)
    if temporary.is_symlink():
        raise RuntimeError('Symlinked test work directory')
    rows = []
    with tempfile.TemporaryDirectory(dir=temporary) as td:
        temp = Path(td)
        harness = temp/'harness.py'
        harness.write_text(HARNESS)
        launcher = temp/'launcher.py'
        launcher.write_text(LAUNCHER)
        for mode, flags, optimize in [('normal', [], None), ('O', ['-O'], None),
                                      ('OO', ['-OO'], None), ('env2', [], '2')]:
            work = temp/mode
            work.mkdir()
            marker = work/'must_not_execute.txt'
            env = dict(os.environ, TMPDIR=str(work), PYTHONDONTWRITEBYTECODE='1')
            env.pop('PYTHONOPTIMIZE', None)
            if optimize is not None:
                env['PYTHONOPTIMIZE'] = optimize
            result = subprocess.run([str(args.python), *flags, str(launcher), str(harness),
                        str(root), args.expected_manifest, str(work), str(marker)],
                        env=env, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                raise RuntimeError(mode+' copy authentication failed: '+result.stderr)
            observed = json.loads(result.stdout)
            if observed['status'] != 'PASS' or observed['worker_optimization'] != 0 or observed['worker_isolated'] != 1:
                raise RuntimeError('Unexpected copy-control execution state')
            rows.append({'outer_mode': mode, **observed})
    receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
               'package_manifest_sha256': args.expected_manifest, 'tampered_copy_runs': len(rows),
               'all_copies_rejected_before_execution': True, 'original_bundle_unchanged': True,
               'rows': rows, 'scope': 'Controlled post-copy corruption; no mathematical or security certification beyond this tested boundary.'}
    output.write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
