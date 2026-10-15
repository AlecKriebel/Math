#!/usr/bin/env python3
"""Verify the exact frozen PR blobs and replay actual programs in private copies.

Run from this directory with a Python interpreter containing SymPy 1.14.0.
All temporary writes stay under .cache; each job gets a fresh copy. On macOS
the actual five jobs and child jobs run with OS network access denied.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
REPO = AUDIT.parents[2]
ATTEMPT_PREFIX = 'unsolved_math_prioritization/attempts/30001232/'
EXPECTED_HEAD = '0a94b2a7e8d682af7d51a3fba7fe8df4a36f6f27'
EXPECTED_SNAPSHOT_SHA = 'b74088ad62046937bc4835f761a500d7a8f9a39ac4eb0da9e3dcb03143adb6cf'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    return {p.relative_to(root).as_posix():digest(p.read_bytes())
            for p in root.rglob('*') if p.is_file()}


def main():
    require(not sys.flags.optimize, 'Run without -O to retain the original author assertions.')
    source = AUDIT/'original'/ATTEMPT_PREFIX
    snapshot_bytes = (AUDIT/'ORIGINAL_SNAPSHOT.json').read_bytes()
    require(digest(snapshot_bytes) == EXPECTED_SNAPSHOT_SHA, 'Snapshot pin mismatch.')
    snapshot = json.loads(snapshot_bytes)
    require(snapshot['head'] == EXPECTED_HEAD, 'Unexpected PR head.')
    require(len(snapshot['files']) == 18, 'Expected eighteen exact original files.')
    expected = {}
    git_blobs = []
    for row in snapshot['files']:
        path = row['path']
        require(path.startswith(ATTEMPT_PREFIX), 'Unexpected original path.')
        relative = path[len(ATTEMPT_PREFIX):]
        local = source/relative
        data = local.read_bytes()
        require(not local.is_symlink(), 'Original symlink.')
        require(digest(data) == row['sha256'] and len(data) == row['size'], 'Original changed.')
        original_blob = subprocess.run(['git','show',EXPECTED_HEAD+':'+path],
                                       cwd=str(REPO),capture_output=True,check=True).stdout
        require(data == original_blob, 'PR Git blob mismatch: '+path)
        expected[relative] = row['sha256']
        git_blobs.append({'path':path,'sha256':digest(original_blob),'exact_local_bytes':True})
    require(inventory(source) == expected, 'Original inventory mismatch.')

    cache = HERE/'.cache'
    cache.mkdir(exist_ok=True)
    profile = '(version 1) (allow default) (deny network*)'
    runner = ['/usr/bin/sandbox-exec','-p',profile]
    require(Path(runner[0]).is_file(), 'OS network-denial runner unavailable.')
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(cache))
    probe_code = ('import socket,json; s=socket.socket();\n'
                  'try: s.connect(("127.0.0.1",9)); print("unexpected")\n'
                  'except OSError as e: print(json.dumps({"errno":e.errno}))\n')
    probe = subprocess.run(runner+[sys.executable,'-B','-c',probe_code],
                           capture_output=True,env=env,check=True)
    require(json.loads(probe.stdout)['errno'] == 1, 'Network-denial probe did not yield EPERM.')

    jobs = [('author/verify_intersections.py','author/intersection_results.json'),
            ('author/verify_formulas.py','author/formula_results.json'),
            ('audit/independent_checks.py','audit/independent_results.json'),
            ('verify_release.py',None),('test_integrity.py',None)]
    replays = []
    for script, reference in jobs:
        with tempfile.TemporaryDirectory(dir=str(cache)) as temp:
            copy = Path(temp)/'packet'
            shutil.copytree(source,copy)
            require(inventory(copy) == expected, 'Scratch copy mismatch.')
            proc = subprocess.run(runner+[sys.executable,'-B',str(copy/script)],
                                  cwd=str(copy),capture_output=True,env=env)
            require(proc.returncode == 0, script+' failed: '+proc.stderr.decode())
            require(not proc.stderr, script+' produced unexpected stderr.')
            actual = json.loads(proc.stdout)
            record = {'program':script,'exit_code':0,'stderr_empty':True,
                      'stdout_sha256':digest(proc.stdout),'network_denied_by_OS':True,
                      'frozen_inputs_before_and_after_exact':inventory(copy)==expected}
            require(record['frozen_inputs_before_and_after_exact'], 'Scratch input mutation.')
            if reference:
                expected_output = (source/reference).read_bytes()
                require(proc.stdout == expected_output, script+' stdout bytes differ.')
                record['exact_recorded_stdout'] = True
                record['reference'] = reference
                if 'results' in actual:
                    record['rows'] = len(actual['results'])
                else:
                    record['total_assertions'] = actual['total_assertions']
            elif script == 'verify_release.py':
                require(actual['status']=='PASS' and actual['strict_manifest_entries']==17
                        and actual['programs_replayed']==3,'Unexpected release result.')
                record['actual_result'] = actual
            else:
                require(actual['status']=='PASS' and actual['frozen_inputs_unchanged']
                        and len(actual['negative_controls'])==8
                        and all(x['rejected'] for x in actual['negative_controls']),
                        'Unexpected integrity controls.')
                record['actual_result'] = actual
            replays.append(record)
    require(inventory(source) == expected, 'Originals changed after replay.')
    print(json.dumps({'status':'PASS','original_count':18,'head':EXPECTED_HEAD,
                      'snapshot_sha256':digest(snapshot_bytes),'git_blob_checks':git_blobs,
                      'all_originals_unchanged':True,
                      'runtime_sympy':__import__('sympy').__version__,
                      'os_network_denial_probe_errno':json.loads(probe.stdout)['errno'],
                      'actual_top_level_jobs':5,
                      'nested_job_repetition_is_not_distinct_proof_evidence':True,
                      'replays':replays},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
