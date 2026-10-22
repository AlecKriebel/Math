"""Portable independent audit verifier; finite diagnostics are not theorem verification."""
import hashlib
import json
from pathlib import Path
import stat
import sys

AUTHOR_NAMES = {'APPROACHES.json', 'DATA_PROVENANCE.json', 'EXPECTED_RESULTS.json',
                'INTEGRITY_RESULTS.json', 'MANIFEST.json', 'PROOF.md', 'README.md',
                'SOURCES.json', 'STATUS.json', 'checks.py', 'integrity_tests.py', 'verify.py'}
AUDIT_NAMES = {'ACCEPTANCE.json', 'CORPUS_VERIFICATION.json', 'SOURCE_VERIFICATION.json',
               'REPORT.md', 'README.md', 'independent_checks.py', 'INDEPENDENT_RESULTS.json',
               'AUTHOR_REPLAY.json', 'PACKAGE_REPLAY.json', 'INTEGRITY_RESULTS.json',
               'verify.py', 'integrity_tests.py'}
EXPECTED = {'author/' + n for n in AUTHOR_NAMES} | {'audit/' + n for n in AUDIT_NAMES}
MANIFEST_PIN = 'c9c1b418218bbb6f831908733d4b8a27d819cdd3abbb72a142d3f57aea3ab171'
PROOF_PIN = '74c727c159d7af1ec7be50c3766356f43a07171f3787a629627d2fce9bfe3a57'


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def encoded(obj):
    return (json.dumps(obj, indent=2, sort_keys=True) + '\n').encode()


def inventory(root):
    found = set()
    def visit(folder):
        for p in folder.iterdir():
            rel = p.relative_to(root).as_posix()
            mode = p.lstat().st_mode
            if stat.S_ISDIR(mode):
                require(rel in {'author', 'audit'}, 'unexpected directory: ' + rel)
                visit(p)
            else:
                require(stat.S_ISREG(mode), 'nonregular file: ' + rel)
                found.add(rel)
    visit(root)
    require(found == EXPECTED | {'MANIFEST.json'}, 'exact package inventory')
    return found


def verify(root):
    root = Path(root)
    found = inventory(root)
    manifest = json.loads((root / 'MANIFEST.json').read_bytes())
    require(manifest.get('schema') == 1 and manifest.get('algorithm') == 'sha256', 'manifest schema')
    rows = manifest.get('files')
    require(isinstance(rows, list), 'manifest rows')
    names = [r.get('path') for r in rows]
    require(len(names) == len(set(names)) and set(names) == EXPECTED, 'manifest inventory')
    raw = {}
    for row in rows:
        name = row['path']
        data = (root / name).read_bytes()
        require(len(data) == row.get('bytes') and hashlib.sha256(data).hexdigest() == row.get('sha256'), 'payload binding: ' + name)
        raw[name] = data
    require(hashlib.sha256(raw['author/MANIFEST.json']).hexdigest() == MANIFEST_PIN, 'immutable author manifest')
    require(hashlib.sha256(raw['author/PROOF.md']).hexdigest() == PROOF_PIN, 'immutable author proof')
    status = json.loads(raw['audit/ACCEPTANCE.json'])
    require(status.get('problem_id') == 30006166 and status.get('verdict') == 'accept_complete_affirmative_candidate', 'acceptance identity')
    for field in ['human_peer_review', 'formal_verification', 'novelty_certified', 'unrestricted_borel_action_problem_claimed_solved']:
        require(status.get(field) is False, 'acceptance scope: ' + field)
    env = {'__name__': 'audited_author_verifier', '__file__': str(root / 'author/verify.py')}
    exec(compile(raw['author/verify.py'], env['__file__'], 'exec'), env)
    author = env['verify'](root / 'author')
    require(author.get('infinite_theorem_verified_by_program') is False, 'author verification scope')
    env = {'__name__': 'independent_source_checks', '__file__': str(root / 'audit/independent_checks.py')}
    exec(compile(raw['audit/independent_checks.py'], env['__file__'], 'exec'), env)
    result = env['compute']()
    require(encoded(result) == raw['audit/INDEPENDENT_RESULTS.json'], 'independent recomputation')
    require(result.get('all_diagnostics_passed') is True and result.get('infinite_theorem_verified_by_program') is False, 'independent diagnostic scope')
    return {'schema': 1, 'verified_regular_files': len(found), 'verified_payload_hashes': len(rows),
            'author_manifest_pin_matched': True, 'author_proof_pin_matched': True,
            'author_finite_checks_passed': True, 'independent_finite_checks_passed': True,
            'independent_counted_diagnostics': sum(result['counts'].values()),
            'independent_results_sha256': hashlib.sha256(encoded(result)).hexdigest(),
            'infinite_theorem_verified_by_program': False}


if __name__ == '__main__':
    try:
        print(json.dumps(verify(Path(__file__).resolve().parents[1]), indent=2, sort_keys=True))
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
