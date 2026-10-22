#!/usr/bin/env python3
"""Read-only, byte-bound replay of an unresolved investigation; stdlib only."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
FREEZES = [
    ('khovanov_30005185', 'AUTHOR_MANIFEST.json', 'df783c4badd6db54bf2655cb8044b0e7ac7a88b249090b6bc3716044ebdf3d70', 'KHOVANOV_30005185_SAFE_FREEZE.zip', 'c52b643a0fc86a59ca0aa6f21b12f36d92eba1dac66424d4201f27c91bd40052', 20354),
    ('khovanov_30005185_independent_audit', 'AUDIT_MANIFEST.json', 'cd7f60608ac24664bf5059cc29afd7de5b6d71975062a8657d9fb5faef427e57', 'KHOVANOV_30005185_INDEPENDENT_AUDIT_SAFE_FREEZE.zip', '00ee82fec2fbea99d55bc50221779a76076519bbd5d091424c2f36d91a1c0039', 18449),
]

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

def replay(script, *args):
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    p = subprocess.run([sys.executable, '-E', '-B', str(ROOT / script), *map(str, args)], cwd=ROOT, env=env, capture_output=True)
    require(p.returncode == 0 and not p.stderr, 'Replay failed: ' + script + '\n' + p.stderr.decode(errors='replace'))
    return json.loads(p.stdout)

def main():
    manifest = read('PUBLICATION_MANIFEST.json')
    expected = set(manifest['files']) | {'PUBLICATION_MANIFEST.json'}
    nodes = list(ROOT.rglob('*'))
    require(not any(p.is_symlink() for p in nodes), 'Symlinks are not allowed')
    require({p.relative_to(ROOT).as_posix() for p in nodes if p.is_file()} == expected, 'Publication file set differs')
    require({p.relative_to(ROOT).as_posix() for p in nodes if p.is_dir()} == {x[0] for x in FREEZES}, 'Publication directory set differs')
    for name, meta in manifest['files'].items():
        data = (ROOT / name).read_bytes()
        require(len(data) == meta['bytes'] and digest(data) == meta['sha256'], 'Publication member mismatch: ' + name)
    for folder, mn, mh, archive, zh, size in FREEZES:
        require(digest((ROOT / folder / mn).read_bytes()) == mh, 'Frozen manifest changed: ' + folder)
        zbytes = (ROOT / archive).read_bytes()
        require(len(zbytes) == size and digest(zbytes) == zh, 'Frozen archive changed: ' + folder)
        frozen = read(folder + '/' + mn)
        members = {x['path'] for x in frozen['files']} | {mn}
        require({p.name for p in (ROOT / folder).iterdir()} == members, 'Frozen member set differs')
        for meta in frozen['files']:
            data = (ROOT / folder / meta['path']).read_bytes()
            require(len(data) == meta['bytes'] and digest(data) == meta['sha256'], 'Frozen member changed: ' + meta['path'])
        with zipfile.ZipFile(ROOT / archive) as z:
            names = {folder + '/' + name for name in members}
            require(len(z.namelist()) == len(names) and set(z.namelist()) == names, 'Archive member set differs')
            for name in names:
                require(z.read(name) == (ROOT / name).read_bytes(), 'Archive member bytes differ')
    status = read('release_status.json')
    require(status['status'] == 'unsolved' and status['turns'] == '5/5', 'Current scope changed')
    for key in ['full_original_problem_solved', 'knot_counterexample_found', 'novelty_claim', 'characteristic_two_Lee_extension', 'finite_census_replay', 'ribbonness_decided_by_code', 'source_payloads_included']:
        require(status[key] is False, 'Scope flag changed: ' + key)
    audit = read('khovanov_30005185_independent_audit/AUDIT_RESULT.json')
    require(audit['verdict'] == 'PASS' and audit['mandatory_corrections'] == [] and audit['full_original_problem_solved'] is False, 'Audit scope changed')
    author = replay('khovanov_30005185/verify_manifest.py')
    require(author['status'] == 'PASS' and author['universal_problem_solved'] is False, 'Author replay changed')
    replay('khovanov_30005185_independent_audit/verify_audit_manifest.py')
    independent = replay('khovanov_30005185_independent_audit/independent_verify.py', '--author', ROOT / 'khovanov_30005185', '--zip', ROOT / 'KHOVANOV_30005185_SAFE_FREEZE.zip')
    require(independent == read('khovanov_30005185_independent_audit/INDEPENDENT_CHECKS.json'), 'Independent receipt differs')
    print(json.dumps({'publication_verified': True, 'problem_id': '30005185', 'status': 'unsolved', 'turns': '5/5', 'audit_verdict': 'PASS_SCOPED_TO_UNRESOLVED_INVESTIGATION', 'publication_file_count': len(expected), 'small_integral_torsion_free_controls': 6, 'universal_problem_solved': False, 'ribbonness_computed': False}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
