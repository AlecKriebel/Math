#!/usr/bin/env python3
"""Read-only portable byte verification and exact checks; not a theorem prover."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
FROZEN = [
    ('author', 'DELONE_6600014_SAFE_AUDIT.zip', 15113, '2511a95f32681a85c337393c1c0ac2f7ad5525247f3e484c00d6150423c477cb', '19dd35b7bd29a784dca9730988b39f64628f52178345e87998505ec7522ba56c'),
    ('audit', 'DELONE_6600014_INDEPENDENT_AUDIT.zip', 12867, 'dbaec0657dba4e45c9985694c8e5201c4cf0cdd72b1dc3be48b4411c85214651', 'c0a36199606330ff7c806e133546a8c5334edbd0e6cc40e3333e4e4a1a07137f'),
]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

def run(script, args=(), optimized=False):
    # -E ignores PYTHONOPTIMIZE. No optimization flag is passed to author/verify.py.
    cmd = [sys.executable, '-E', '-B'] + (['-O'] if optimized else []) + [str(ROOT / script), *map(str, args)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    require(p.returncode == 0 and not p.stderr, 'Replay failed: ' + script + '\n' + p.stderr)
    result = json.loads(p.stdout)
    require(result['result'] == 'PASS', 'Replay did not pass: ' + script)
    return result

def main():
    manifest = read('PUBLICATION_MANIFEST.json')
    expected = set(manifest['files']) | {'PUBLICATION_MANIFEST.json'}
    nodes = list(ROOT.rglob('*'))
    require(not any(p.is_symlink() for p in nodes), 'Symlink in publication')
    require({p.relative_to(ROOT).as_posix() for p in nodes if p.is_file()} == expected, 'Publication file inventory mismatch')
    require({p.relative_to(ROOT).as_posix() for p in nodes if p.is_dir()} == {'author', 'audit'}, 'Publication directory inventory mismatch')
    for name, record in manifest['files'].items():
        data = (ROOT / name).read_bytes()
        require(len(data) == record['bytes'] and digest(data) == record['sha256'], 'Publication bytes mismatch: ' + name)
    for folder, archive, size, zhash, mhash in FROZEN:
        data = (ROOT / archive).read_bytes()
        require(len(data) == size and digest(data) == zhash, 'Frozen archive changed: ' + archive)
        require(digest((ROOT / folder / 'MANIFEST.json').read_bytes()) == mhash, 'Frozen manifest changed: ' + folder)
        records = read(folder + '/MANIFEST.json')['files']
        members = {r['name'] for r in records} | {'MANIFEST.json'}
        require(len(members) == len(records) + 1, 'Duplicate frozen manifest member')
        require({p.name for p in (ROOT / folder).iterdir()} == members, 'Frozen inventory changed')
        for record in records:
            b = (ROOT / folder / record['name']).read_bytes()
            require(len(b) == record['bytes'] and digest(b) == record['sha256'], 'Frozen payload changed')
        with zipfile.ZipFile(ROOT / archive) as z:
            require(len(z.namelist()) == len(members) and set(z.namelist()) == members, 'ZIP inventory changed')
            for name in members:
                require(z.read(name) == (ROOT / folder / name).read_bytes(), 'ZIP member bytes changed')
    status = read('release_status.json')
    require(status['problem_id'] == '6600014' and status['status'] == 'already_solved' and status['turns'] == '1/5', 'Classification changed')
    require(status['original_solution_credit'] == 0 and status['independent_audit'] == 'PASS', 'Credit or audit changed')
    require(status['full_published_proof_independently_audited'] is False and status['live_catalogue_recovered'] is False, 'Inspection limits changed')
    author = run('author/verify.py')
    audit = run('audit/verify_audit.py', ['--author-dir', ROOT / 'author', '--author-archive', ROOT / FROZEN[0][1]], optimized=bool(sys.flags.optimize))
    print(json.dumps({'publication_verified': True, 'problem_id': '6600014', 'status': 'already_solved', 'turns': '1/5', 'original_solution_credit': 0, 'publication_file_count': len(expected), 'author_assertions_enabled': True, 'author_checks': author['checks'], 'audit_checks': audit['computed_checks'], 'full_published_proof_independently_audited': False}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
