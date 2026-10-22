#!/usr/bin/env python3
"""Portable inventory/hash replay and exact diagnostics; never a proof assistant."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

FILES = {'PROOF.md', 'README.md', 'RESEARCH_LOG.md', 'STATUS.json',
         'SOURCE_VERIFICATION.json', 'PRIOR_ATTEMPT_CHECKS.json',
         'exact_checks.py', 'EXACT_CHECKS.json', 'verify_release.py'}
MANIFEST = 'MANIFEST.json'

def verify(root):
    actual = {p.name for p in root.iterdir()}
    assert actual == FILES | {MANIFEST}, 'exact file inventory mismatch'
    assert all((root / name).is_file() and not (root / name).is_symlink() for name in actual), 'files only'
    manifest = json.loads((root / MANIFEST).read_text())
    assert manifest['schema'] == 'pe-boundary-author-freeze-v1'
    assert {r['path'] for r in manifest['files']} == FILES, 'manifest inventory mismatch'
    assert len(manifest['files']) == len(FILES), 'duplicate manifest entries'
    for entry in manifest['files']:
        data = (root / entry['path']).read_bytes()
        assert len(data) == entry['bytes'], 'byte count: ' + entry['path']
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], 'hash: ' + entry['path']
    status = json.loads((root / 'STATUS.json').read_text())
    assert status['problem_id'] == '30002692'
    assert status['disposition'] == 'prior_construction_verified_for_primary_statement'
    assert status['novelty_claim'] is False
    assert status['aggregator_statement_verified'] is False
    assert status['raw_ai_problem_corpora_inspected'] is False
    assert status['substantive_approaches_used'] == 1
    assert status['independent_audit'] == 'pending'
    assert status['parent_acceptance'] == 'pending'
    output = subprocess.check_output([sys.executable, str(root / 'exact_checks.py')], cwd=root)
    assert output == (root / 'EXACT_CHECKS.json').read_bytes(), 'exact replay receipt mismatch'
    receipt = json.loads(output)
    assert receipt['result'] == 'PASS'
    return receipt['assertion_count']

def rehash(root, name):
    manifest = json.loads((root / MANIFEST).read_text())
    data = (root / name).read_bytes()
    for e in manifest['files']:
        if e['path'] == name:
            e['bytes'] = len(data)
            e['sha256'] = hashlib.sha256(data).hexdigest()
    (root / MANIFEST).write_text(json.dumps(manifest, indent=2)+'\n')

def negatives(root):
    passed = []
    cases = ['missing_proof', 'extra_pdf', 'changed_proof', 'wrong_size',
             'coherent_deleted_readme', 'coherent_novelty_upgrade', 'coherent_aggregator_upgrade']
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='pe-boundary-control-') as temp:
            copy = Path(temp) / 'packet'
            shutil.copytree(root, copy)
            if case == 'missing_proof':
                (copy / 'PROOF.md').unlink()
            elif case == 'extra_pdf':
                (copy / 'unauthorized_source.pdf').write_bytes(b'%PDF-negative-control')
            elif case == 'changed_proof':
                with (copy / 'PROOF.md').open('a') as f:
                    f.write('\nchanged\n')
            elif case == 'wrong_size':
                m = json.loads((copy / MANIFEST).read_text())
                m['files'][0]['bytes'] += 1
                (copy / MANIFEST).write_text(json.dumps(m))
            elif case == 'coherent_deleted_readme':
                (copy / 'README.md').unlink()
                m = json.loads((copy / MANIFEST).read_text())
                m['files'] = [e for e in m['files'] if e['path'] != 'README.md']
                (copy / MANIFEST).write_text(json.dumps(m))
            else:
                s = json.loads((copy / 'STATUS.json').read_text())
                s['novelty_claim' if case == 'coherent_novelty_upgrade' else 'aggregator_statement_verified'] = True
                (copy / 'STATUS.json').write_text(json.dumps(s))
                rehash(copy, 'STATUS.json')
            try:
                verify(copy)
            except (AssertionError, FileNotFoundError):
                passed.append(case)
            else:
                raise AssertionError('negative control was accepted: ' + case)
    return passed

if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    n = verify(root)
    controls = negatives(root)
    print(json.dumps({'result': 'PASS', 'frozen_files': len(FILES),
                      'exact_assertions': n, 'negative_integrity_controls': controls,
                      'scope': 'Author freeze only; independent audit and parent acceptance are not implied.'},
                     indent=2, sort_keys=True))
