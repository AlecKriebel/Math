#!/usr/bin/env python3
"""Strict recursive inventory and byte-exact scoped-control replay (stdlib only)."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PINS = {'author': '95f814667e4dd6b68199ab9d69fc38e521b86e20ab111fa9562150fc39cb2a24',
        'audit': '0e5269fa149cc83639d6c158c73843d79e876ff5dc381b967cb7594d42a9ccc8'}

def need(ok, message):
    if not ok:
        raise SystemExit('FAIL: ' + message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read(name):
    return json.loads((ROOT / name).read_bytes())

def inventory():
    manifest = read('PUBLICATION_MANIFEST.json')
    need(manifest['problem_id'] == 20000809, 'problem identity')
    entries = manifest['files']
    expected = {'PUBLICATION_MANIFEST.json'}
    for row in entries:
        name = row['path']
        path = PurePosixPath(name)
        need(str(path) == name and not path.is_absolute() and '..' not in path.parts,
             'unsafe manifest path')
        need(name not in expected, 'duplicate manifest entry')
        expected.add(name)
    dirs = {str(p) for name in expected for p in PurePosixPath(name).parents if str(p) != '.'}
    actual_files, actual_dirs = set(), set()
    for p in ROOT.rglob('*'):
        name = p.relative_to(ROOT).as_posix()
        need(not p.is_symlink(), 'symlink: ' + name)
        if p.is_file():
            actual_files.add(name)
        elif p.is_dir():
            actual_dirs.add(name)
        else:
            need(False, 'nonregular member: ' + name)
    need(actual_files == expected, 'recursive file inventory differs')
    need(actual_dirs == dirs, 'recursive directory inventory differs')
    for row in entries:
        data = (ROOT / row['path']).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'integrity: ' + row['path'])
    for group, digest in PINS.items():
        need(sha((ROOT / group / 'MANIFEST.json').read_bytes()) == digest, 'frozen manifest pin: ' + group)
        frozen = read(group + '/MANIFEST.json')
        wanted = {'MANIFEST.json'} | {x['path'] for x in frozen['files']}
        need({p.name for p in (ROOT / group).iterdir()} == wanted, 'frozen inventory: ' + group)
        for row in frozen['files']:
            data = (ROOT / group / row['path']).read_bytes()
            need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'frozen bytes: ' + row['path'])
    return len(expected)

def main():
    need(len(sys.argv) == 1, 'no arguments supported')
    count = inventory()
    s = read('PUBLICATION_STATUS.json')
    need(s['status'] == 'unsolved' and s['turns'] == '5/5', 'status or approach budget')
    need(s['general_projective_question'] == 'unresolved_here' and s['original_target_verified_solved'] is False,
         'unsupported original-target promotion')
    need(s['novelty_established'] is False and s['mathematical_audit'] == 'PASS_SCOPED_PARTIAL', 'scope or novelty')
    audit = read('audit/audit_summary.json')
    need(audit['verdict'] == 'PASS_SCOPED_PARTIAL' and audit['required_author_corrections'] == [], 'audit verdict')
    need(audit['general_question_status'] == 'unresolved_here' and audit['approach_families_used'] == 5, 'audit scope')
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    def run(script):
        p = subprocess.run([sys.executable, '-B', str(ROOT / script)], cwd=ROOT, env=env, capture_output=True)
        need(p.returncode == 0, 'execution: ' + script + '\n' + p.stderr.decode(errors='replace'))
        return p.stdout
    run('author/verify_packet.py')
    run('audit/verify_audit.py')
    author_bytes = run('author/verify.py')
    audit_bytes = run('audit/independent_verify.py')
    need(author_bytes == (ROOT / 'author/verification.json').read_bytes(), 'author exact replay')
    need(audit_bytes == (ROOT / 'audit/independent_verification.json').read_bytes(), 'audit exact replay')
    a, b = json.loads(author_bytes), json.loads(audit_bytes)
    need(a['assertion_count'] == 116 and b['assertion_count'] == 310, 'assertion counts')
    need(len(a['negative_controls_rejected']) == 5 and len(b['negative_controls_rejected']) == 8, 'negative controls')
    need(a['affine_tangent_weights'] == b['affine_tangent_weights'], 'full tangent weight agreement')
    lifted = [{'multiplicity': x['multiplicity'], 'weight': x['weight'] + [-sum(x['weight'])]}
              for x in b['filtered_tangent_weights']]
    need(a['untruncated_homogeneous_weights'] == lifted, 'filtered tangent weight agreement after projective lift')
    print(json.dumps({'status': 'PASS', 'publication_files': count, 'problem_id': 20000809,
       'original_target_status': 'unsolved', 'turns': '5/5', 'mathematical_audit': 'PASS_SCOPED_PARTIAL',
       'author_assertions': 116, 'independent_assertions': 310,
       'author_negative_controls': 5, 'independent_negative_controls': 8,
       'cross_implementation_weights': 'MATCH', 'general_projective_question': 'unresolved_here',
       'external_source_verification': 'NOT_RUN: historical bounded retrieval and inspection metadata preserved',
       'novelty_established': False}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
