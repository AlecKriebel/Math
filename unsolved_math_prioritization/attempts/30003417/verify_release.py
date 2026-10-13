#!/usr/bin/env python3
"""Read-only portable publication checks. Not an infinite-cardinal proof checker."""
from pathlib import Path
import hashlib
import json
import stat
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
FROZEN = [
    ('author/safe_output', 'author/MEAGER_30003417_SAFE_PACKET.zip', 'author/FREEZE_RECEIPT.json', 23352, '69a2cea3fb5fcc1568d0bd538f5738d53ff7208b3b1c021d25f6b642cbdfbd4e', '2f4160f673fd31479499f3ac675221fb1048bc644ef8a529b89fdc6a9ba9150e'),
    ('audit', 'audit/MEAGER_30003417_INDEPENDENT_AUDIT.zip', 'audit/AUDIT_FREEZE.json', 22117, '7b1c0534103be80f80fc6f947090b7a4f441ffae2e7b431afbc7bac4755a4d23', '4470084687e0beca3b68dd464e422712cd72dc5e7a4ba5cfc0ac692933481fc0'),
]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

def check_status(s):
    require(s['problem_id'] == 30003417 and s['problem_number'] == 'OWR-15216-023' and s['rank'] == 735, 'Identity changed')
    require(s['status'] == 'unsolved' and s['turns'] == '5/5' and s['approaches_used'] == 5, 'Disposition changed')
    require(s['original_solution_credit'] == 0 and s['completion_estimate_new_full_resolution_percent'] == 0, 'Resolution credit changed')
    require(s['independent_audit'] == 'PASS' and s['mandatory_corrections'] == [], 'Audit changed')
    require(s['ambient_theory'] == 'ZFC' and s['dissertation_question_2_6_1_scope'] == 'inaccessible kappa only', 'Editorial scope changed')
    for key in ['universal_add_equality_proved', 'universal_cof_equality_proved', 'countermodel_constructed', 'independence_proved', 'worldwide_openness_certified', 'finite_order_assignments_are_cardinal_models', 'full_imported_forcing_proofs_independently_audited']:
        require(s[key] is False, 'Claim boundary changed: ' + key)

def run(script, args=(), optimized=False):
    # -E ignores PYTHONOPTIMIZE. The author's assertions are always enabled.
    cmd = [sys.executable, '-E', '-B'] + (['-O'] if optimized else []) + [str(ROOT / script), *map(str, args)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    require(p.returncode == 0 and not p.stderr, 'Replay failed: ' + script + '\n' + p.stderr)
    result = json.loads(p.stdout)
    require(result['status'] == 'PASS', 'Replay did not pass: ' + script)
    return result

def main():
    manifest = read('PUBLICATION_MANIFEST.json')
    expected = set(manifest['files']) | {'PUBLICATION_MANIFEST.json'}
    require(manifest['problem_id'] == 30003417, 'Manifest identity changed')
    nodes = list(ROOT.rglob('*'))
    require(not any(p.is_symlink() for p in nodes), 'Symlink in publication')
    require({p.relative_to(ROOT).as_posix() for p in nodes if p.is_file()} == expected, 'Publication file inventory mismatch')
    require({p.relative_to(ROOT).as_posix() for p in nodes if p.is_dir()} == {'author', 'author/safe_output', 'audit'}, 'Publication directory inventory mismatch')
    for name, record in manifest['files'].items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe manifest path')
        data = (ROOT / name).read_bytes()
        require(len(data) == record['bytes'] and digest(data) == record['sha256'], 'Publication bytes mismatch: ' + name)
    for folder, archive, receipt, size, zhash, mhash in FROZEN:
        data = (ROOT / archive).read_bytes()
        require(len(data) == size and digest(data) == zhash, 'Frozen archive changed: ' + archive)
        require(digest((ROOT / folder / 'MANIFEST.json').read_bytes()) == mhash, 'Frozen manifest changed: ' + folder)
        records = read(folder + '/MANIFEST.json')['files']
        members = set(records) | {'MANIFEST.json'}
        freeze = read(receipt)
        require((freeze['bytes'], freeze['sha256'], freeze['manifest_sha256']) == (size, zhash, mhash), 'Freeze receipt mismatch')
        require(set(freeze['entries']) == members and len(freeze['entries']) == len(members), 'Freeze member mismatch')
        for name, record in records.items():
            b = (ROOT / folder / name).read_bytes()
            require(len(b) == record['bytes'] and digest(b) == record['sha256'], 'Frozen member changed')
        with zipfile.ZipFile(ROOT / archive) as z:
            require(len(z.namelist()) == len(members) and set(z.namelist()) == members, 'ZIP inventory changed')
            require(z.testzip() is None, 'ZIP CRC changed')
            for info in z.infolist():
                require('/' not in info.filename and '\\' not in info.filename and not info.is_dir(), 'ZIP path changed')
                require(not stat.S_ISLNK(info.external_attr >> 16) and not info.flag_bits & 1, 'ZIP member type changed')
                require(z.read(info.filename) == (ROOT / folder / info.filename).read_bytes(), 'ZIP member bytes changed')
    check_status(read('release_status.json'))
    decision = read('audit/AUDIT_DECISION.json')
    require(decision['verdict'] == 'PASS' and decision['mandatory_corrections'] == [], 'Frozen audit mismatch')
    author = run('author/safe_output/verify_packet.py')
    audit = run('audit/verify_independently.py', ['--author-root', ROOT / 'author'], optimized=bool(sys.flags.optimize))
    require(audit['source_checks']['status'] == 'NOT_RUN', 'Portable source limits changed')
    require(audit['negative_controls']['count'] == 16 and audit['negative_controls']['all_rejected'], 'Negative controls changed')
    require(author['finite_order_logic']['admissible_order_assignments'] == 371 and audit['order_logic']['admissible_assignments'] == 1086, 'Order logic changed')
    print(json.dumps({'publication_verified': True, 'problem_id': 30003417, 'status': 'unsolved', 'turns': '5/5', 'original_solution_credit': 0, 'publication_file_count': len(expected), 'author_assertions_enabled': True, 'author_order_assignments': 371, 'independent_order_assignments': 1086, 'independent_negative_controls_rejected': 16, 'source_checks': 'NOT_RUN', 'infinite_cardinal_proofs_formally_verified': False, 'worldwide_openness_certified': False}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
