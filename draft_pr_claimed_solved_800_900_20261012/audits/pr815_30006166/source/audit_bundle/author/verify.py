"""Strict, portable source-executing verifier. No assertion or bytecode-cache reliance."""
import hashlib
import json
from pathlib import Path
import stat
import sys

EXPECTED_NAMES = {
    'README.md', 'PROOF.md', 'STATUS.json', 'APPROACHES.json', 'SOURCES.json',
    'DATA_PROVENANCE.json', 'checks.py', 'EXPECTED_RESULTS.json', 'verify.py',
    'integrity_tests.py', 'INTEGRITY_RESULTS.json', 'MANIFEST.json',
}


def fail(message):
    raise RuntimeError(message)


def verify(root):
    root = Path(root)
    found = set()
    for entry in root.iterdir():
        mode = entry.lstat().st_mode
        if not stat.S_ISREG(mode):
            fail('nonregular or directory entry: ' + entry.name)
        found.add(entry.name)
    if found != EXPECTED_NAMES:
        fail('inventory mismatch')
    manifest = json.loads((root / 'MANIFEST.json').read_bytes())
    if manifest.get('schema') != 1 or manifest.get('algorithm') != 'sha256':
        fail('manifest schema')
    rows = manifest.get('files')
    if not isinstance(rows, list):
        fail('manifest entries')
    expected = EXPECTED_NAMES - {'MANIFEST.json'}
    names = [r.get('path') for r in rows]
    if len(names) != len(set(names)) or set(names) != expected:
        fail('manifest inventory')
    data = {}
    for row in rows:
        name = row['path']
        raw = (root / name).read_bytes()
        if len(raw) != row.get('bytes') or hashlib.sha256(raw).hexdigest() != row.get('sha256'):
            fail('byte/hash mismatch: ' + name)
        data[name] = raw
    status = json.loads(data['STATUS.json'])
    if (status.get('problem_id'), status.get('disposition'), status.get('approaches_used'),
        status.get('independent_review'), status.get('novelty_claimed')) != (
        30006166, 'complete_affirmative_candidate', 3, 'pending', False):
        fail('status scope drift')
    approaches = json.loads(data['APPROACHES.json'])
    if [r.get('number') for r in approaches] != [1, 2, 3]:
        fail('approach count')
    env = {'__name__': 'verified_author_source', '__file__': str(root / 'checks.py')}
    exec(compile(data['checks.py'], str(root / 'checks.py'), 'exec'), env)
    actual = env['compute']()
    encoded = (json.dumps(actual, indent=2, sort_keys=True) + '\n').encode()
    if encoded != data['EXPECTED_RESULTS.json']:
        fail('computed output does not reproduce frozen result bytes')
    return {'schema': 1, 'verified_regular_files': len(found),
            'verified_payload_hashes': len(rows), 'source_executed': 'checks.py',
            'results_sha256': hashlib.sha256(encoded).hexdigest(),
            'finite_consistency_checks_passed': True,
            'infinite_theorem_verified_by_program': False}


if __name__ == '__main__':
    try:
        result = verify(Path(__file__).resolve().parent)
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(result, indent=2, sort_keys=True))
