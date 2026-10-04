#!/usr/bin/env python3
"""Read-only byte custody checks; do not reproduce or infer scientific verdicts."""
import datetime
import hashlib
import json
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent
OUT = BASE / 'ROOT_completed_priority_family_readback_20261004'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def check(path, size, digest):
    p = pathlib.Path(path)
    assert p.is_file(), str(p)
    assert p.stat().st_size == size, str(p)
    assert sha(p) == digest, str(p)

def time_order(start, end):
    a = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
    b = datetime.datetime.fromisoformat(end.replace('Z', '+00:00'))
    assert a <= b

def exact():
    root = BASE / 'exact_target_priority_20261004'
    manifest = root / 'MANIFEST.json'
    d = json.loads(manifest.read_text())
    for row in d['public_files'] + d['private_files_metadata_only']:
        check(row['path'], row['bytes'], row['sha256'])
    receipts = []
    for p in sorted((root / 'receipts').glob('*.json')):
        r = json.loads(p.read_text())
        if r['kind'] == 'web_tool':
            assert r['executable_pid'] is None
            check(r['raw_private_path'], r['raw_bytes'], r['raw_sha256'])
            receipts.append({'receipt': str(p), 'kind': 'web_tool', 'pid': None})
        else:
            assert r['kind'] == 'executed_subprocess'
            assert r['subprocess_pid'] > 0 and r['recorder_pid'] > 0
            assert isinstance(r['argv'], list) and r['cwd']
            time_order(r['started_at_utc'], r['finished_at_utc'])
            for k in ['stdout', 'stderr']:
                s = r[k]
                check(s['path'], s['bytes'], s['sha256'])
            receipts.append({'receipt': str(p), 'kind': r['kind'],
                             'pid': r['subprocess_pid'], 'exit': r['returncode']})
    assert len(receipts) == d['receipt_count']
    first = json.loads((root / 'FIRST_CONCLUSION_SEAL.json').read_text())
    check(first['path'], first['bytes'], first['sha256'])
    assert first['sha256'] == '7d89628f4ebd20a4f1d7cc70c5bc13a0d40d8c6ba107ac3b4a3c5effa743d593'
    return {'manifest_path': str(manifest), 'manifest_sha256': sha(manifest),
            'public_files': len(d['public_files']),
            'private_files': len(d['private_files_metadata_only']), 'receipts': receipts}

def mechanism():
    root = BASE / 'mechanism_priority_20261004'
    manifest = root / 'MANIFEST.json'
    d = json.loads(manifest.read_text())
    for row in d['inventory']:
        check(root / row['path'], row['bytes'], row['sha256'])
    for row in d['private_copyright_artifacts_outside_repository']:
        check(row['private_path'], row['bytes'], row['sha256'])
    receipts = []
    for p in sorted((root / 'commands').glob('*/record.json')):
        r = json.loads(p.read_text())
        assert r['pid'] > 0 and r['runner_pid'] > 0
        assert isinstance(r['argv'], list) and r['cwd']
        time_order(r['started_utc'], r['ended_utc'])
        for k in ['stdout', 'stderr']:
            check(p.parent / (k + '.bin'), r[k + '_bytes'], r[k + '_sha256'])
        receipts.append({'receipt': str(p), 'pid': r['pid'], 'exit': r['exit_status']})
    assert sha(root / 'FIRST_CONCLUSION.md') == d['first_conclusion_sha256'] == '50c36c1b2b6b77aa158a1df544ab1d0eca417eb17423e8f36f1074dd1d80d5f3'
    return {'manifest_path': str(manifest), 'manifest_sha256': sha(manifest),
            'public_files': len(d['inventory']),
            'private_files': len(d['private_copyright_artifacts_outside_repository']),
            'receipts': receipts}

assert not sys.flags.optimize
OUT.mkdir(exist_ok=False)
result = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'operator_sha256': sha(pathlib.Path(__file__)),
          'scope': 'Actual completed artifact and stream custody only; no scientific replay or novel priority certificate',
          'exact_target': exact(), 'mechanism': mechanism(),
          'unknown_environment_note': 'No child environment/optimization flags inferred when receipts do not record them.',
          'verdict': 'PASS'}
(OUT / 'READBACK.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verdict': 'PASS', 'readback': str(OUT / 'READBACK.json'),
                  'families': 2, 'files': sum(result[k]['public_files'] + result[k]['private_files'] for k in ['exact_target', 'mechanism']),
                  'actual_receipts': sum(len(result[k]['receipts']) for k in ['exact_target', 'mechanism'])}, indent=2))
