"""Freeze allowlisted author inputs and run verifiers under real UID 1000.

Writes only this audit's private snapshot and result directory. Never changes the
author packet. Deliberate failed write probes use a disposable snapshot sentinel.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = ROOT.parent / 'greedy_spanning_tree_30001934'
SNAPSHOT = ROOT / 'private_checks/frozen_packet'
RESULTS = ROOT / 'results'


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def inventory():
    return {str(p.relative_to(AUTHOR)): digest(p) for p in AUTHOR.rglob('*') if p.is_file()}


def run():
    need(os.getuid() == 1000 and os.geteuid() == 1000, 'must run with real and effective UID 1000')
    before = inventory()
    manifest = json.loads((AUTHOR / 'PUBLIC_MANIFEST.json').read_text())
    need(not SNAPSHOT.exists(), 'snapshot already exists; do not silently replace it')
    SNAPSHOT.mkdir(parents=True)
    for row in manifest['files']:
        source = AUTHOR / row['path']
        need(digest(source) == {k: row[k] for k in ('bytes', 'sha256')}, 'author manifest mismatch: ' + row['path'])
        dest = SNAPSHOT / row['path']
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
    shutil.copyfile(AUTHOR / 'PUBLIC_MANIFEST.json', SNAPSHOT / 'PUBLIC_MANIFEST.json')
    (SNAPSHOT / 'readonly_sentinel').write_text('audit sentinel\n')
    for path in SNAPSHOT.rglob('*'):
        if path.is_file():
            path.chmod(0o444)
    for path in sorted([p for p in SNAPSHOT.rglob('*') if p.is_dir()], key=lambda p: len(p.parts), reverse=True):
        path.chmod(0o555)
    SNAPSHOT.chmod(0o555)
    snapshot_before = {str(p.relative_to(SNAPSHOT)): digest(p) for p in SNAPSHOT.rglob('*') if p.is_file()}
    probe = """import json, os
from pathlib import Path
root = Path('.')
out = {'uid': os.getuid(), 'euid': os.geteuid(), 'write_probes': []}
for p, mode in [(root/'readonly_sentinel','a'), (root/'forbidden_new_file','w')]:
    try:
        with p.open(mode) as stream: stream.write('unexpected write')
    except PermissionError as e:
        out['write_probes'].append({'target': p.name, 'denied': True, 'errno': e.errno})
    else:
        raise RuntimeError('read-only probe unexpectedly wrote')
print(json.dumps(out, sort_keys=True))
"""
    probe_result = subprocess.run([sys.executable, '-B', '-c', probe], cwd=SNAPSHOT, text=True, capture_output=True)
    need(probe_result.returncode == 0, probe_result.stderr)
    records = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GREEDY_PACKET=str(SNAPSHOT))
    for mode, switches in [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]:
        for label, script in [('author_core', SNAPSHOT/'tests/test_exact_model.py'),
                              ('author_saved_adversarial', SNAPSHOT/'tests/check_adversarial_records.py'),
                              ('independent', ROOT/'tests/independent_exact_audit.py')]:
            result = subprocess.run([sys.executable, '-B', *switches, str(script)],
                                    cwd=SNAPSHOT/'tests', env=env, text=True, capture_output=True)
            filename = f'{label}_{mode}.json'
            (RESULTS/filename).write_text(result.stdout)
            need(result.returncode == 0, f'{label} {mode}: {result.stderr}')
            parsed = json.loads(result.stdout)
            if label == 'author_core':
                need(parsed['tested_points'] == 2680 and parsed['passed'] is True, 'author core result')
            elif label == 'author_saved_adversarial':
                expected = json.loads((SNAPSHOT/'results/adversarial_exact_crosscheck.json').read_text())
                need(parsed == expected, 'saved adversarial crosscheck differs')
            else:
                need(parsed['uid'] == parsed['euid'] == 1000 and parsed['passed'] is True, 'independent result')
                need(len(parsed['mutants_rejected']) == 9, 'mutation coverage')
            records.append({'test': label, 'mode': mode, 'exit_code': result.returncode, 'output': filename,
                            'output_sha256': digest(RESULTS/filename)['sha256']})
    snapshot_after = {str(p.relative_to(SNAPSHOT)): digest(p) for p in SNAPSHOT.rglob('*') if p.is_file()}
    need(snapshot_before == snapshot_after, 'snapshot bytes changed during verification')
    need(before == inventory(), 'author packet bytes changed during verification')
    summary = {'passed': True, 'real_uid': os.getuid(), 'effective_uid': os.geteuid(),
               'readonly_probe': json.loads(probe_result.stdout),
               'author_files_unchanged': True, 'readonly_snapshot_unchanged': True,
               'manifest_files_checked': len(manifest['files']),
               'author_manifest': digest(AUTHOR/'PUBLIC_MANIFEST.json'), 'runs': records,
               'new_research_approaches': 0, 'all_graph_resolution': False}
    (RESULTS/'READONLY_VERIFICATION.json').write_text(json.dumps(summary, indent=2, sort_keys=True)+'\n')
    (ROOT/'private_checks/AUTHOR_INPUT_INVENTORY.json').write_text(json.dumps(before, indent=2, sort_keys=True)+'\n')
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == '__main__':
    run()
