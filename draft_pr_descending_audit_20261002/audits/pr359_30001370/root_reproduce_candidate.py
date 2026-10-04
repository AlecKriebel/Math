#!/usr/bin/env python3
"""Root full-byte custody and native replay of the immutable candidate.

No Git, network, source substitution or installation. Complete native streams
are preserved in a newly created private run; original and execution copies
are checked before and after. Finite checks do not replace the analytic proof.
"""
from pathlib import Path
from datetime import datetime, timezone
import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys

A = Path(__file__).resolve().parent
R = A.parents[2]
S = A / 'snapshot'
P = S / 'problems/30001370_basin_boundaries'
RUN = A / 'root_replay_private' / 'candidate_001'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def utc():
    return datetime.now(timezone.utc).isoformat()

def state(folder):
    return {str(p.relative_to(folder)): (len(p.read_bytes()), sha(p.read_bytes()))
            for p in sorted(folder.rglob('*')) if p.is_file()}

def main():
    assert not RUN.exists(), 'Preserve previous native run; use a new path.'
    RUN.mkdir(parents=True)
    original = state(S)
    m = json.loads((A / 'snapshot_manifest.json').read_text())
    assert len(m['files']) == 38
    assert set(original) == {x['path'] for x in m['files']}
    for x in m['files']:
        b = (S / x['path']).read_bytes()
        assert (len(b), sha(b)) == (x['bytes'], x['sha256'])
        assert not (S / x['path']).is_symlink()
        assert x['mode'] == '100644'
        assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == x['git_blob_sha']
    declarations = 0
    for rel in ['TURN_1_MANIFEST.json','TURN_2_MANIFEST.json','TURN_3_MANIFEST.json',
                'FINAL_AUTHOR_MANIFEST.json','review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
        f = P / rel
        j = json.loads(f.read_text())
        for x in j['files']:
            q = f.parent / x['path']
            assert q.resolve().is_relative_to(P.resolve())
            b = q.read_bytes()
            assert (len(b), sha(b)) == (x['bytes'], x['sha256'])
            declarations += 1
    assert declarations == 86
    for t in (2,3):
        j = json.loads((P / f'TURN_{t}_MANIFEST.json').read_text())
        assert j['previous_manifest_sha256'] == sha((P / f'TURN_{t-1}_MANIFEST.json').read_bytes())
    rm = json.loads((P / 'review/REVIEW_MANIFEST.json').read_text())
    assert rm['author_manifest_sha256'] == sha((P / 'FINAL_AUTHOR_MANIFEST.json').read_bytes())
    historical = json.loads((P / 'review/REMOTE_BINDING.json').read_text())
    pub = json.loads((P / 'PUBLICATION_MANIFEST.json').read_text())
    assert pub['author_head'] == historical['commit'] == 'be4730c4f09b4fe5cc82bbedb8cb154894124dfd'
    assert pub['fresh_main_parent'] == m['base']
    for x in historical['files']:
        b = (P / x['name']).read_bytes()
        assert len(b) == x['size']
        assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == x['sha']
    assert len(historical['files']) == 25
    copy = RUN / 'execution_copy'
    shutil.copytree(P, copy)
    before = state(copy)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    executions = []
    programs = [(f'check_turn_{t}.py', f'TURN_{t}_CHECKS.json') for t in (1,2,3)]
    programs += [('review/check_independent.py','review/INDEPENDENT_CHECKS.json'), ('verify_packet.py',None)]
    for k, (program, expected) in enumerate(programs):
        argv = [sys.executable, '-B', str(copy / program)]
        started = utc()
        p = subprocess.run(argv, cwd=copy, env=env, capture_output=True)
        ended = utc()
        stem = f'replay_{k:02d}'
        (RUN / (stem + '.stdout')).write_bytes(p.stdout)
        (RUN / (stem + '.stderr')).write_bytes(p.stderr)
        rec = {'argv':argv, 'cwd':str(copy),'started_utc':started,'completed_utc':ended,
               'exit_code':p.returncode,
               'stdout':{'path':stem+'.stdout','bytes':len(p.stdout),'sha256':sha(p.stdout)},
               'stderr':{'path':stem+'.stderr','bytes':len(p.stderr),'sha256':sha(p.stderr)},
               'original_stdout_receipt':expected,
               'whole_stdout_byte_exact':p.stdout == (P / expected).read_bytes() if expected else None}
        (RUN / (stem + '.execution.json')).write_text(json.dumps(rec,indent=2)+'\n')
        executions.append(rec)
        assert p.returncode == 0 and not p.stderr, rec
        if expected:
            assert rec['whole_stdout_byte_exact'], rec
        else:
            wrapper = json.loads(p.stdout)
            assert wrapper['status'] == 'PASS'
    assert before == state(copy), 'Execution changed frozen copy.'
    assert original == state(S), 'Original frozen snapshot changed.'
    receipt = {'utc':utc(),'status':'PASS_COMPLETE_CANDIDATE_REPLAY',
               'head':m['head'],'base':m['base'],'frozen_files':38,
               'nested_declarations':declarations,'historical_remote_entries':25,
               'predecessor_edges':2,'native_runs':executions,
               'source_wrapper_scope':'Original default public-only mode; source hashes explicitly not checked. Ancillary ESI payload unavailable; no substitution.',
               'candidate_and_execution_copy_unchanged':True,
               'scope':'Byte bindings and exact finite reproductions only; analytic theorem audited separately.'}
    (A / 'ROOT_CANDIDATE_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'native_runs':5,'exact_saved_stdout':4,
                      'nested_declarations':86,'snapshot_unchanged':True},indent=2))

if __name__ == '__main__':
    main()
