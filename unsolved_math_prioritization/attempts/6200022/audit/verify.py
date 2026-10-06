#!/usr/bin/env python3
"""Portable fail-closed integrity and replay for the separate audit package."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

FILES = {'AUDIT.md','README.md','PUBLIC_METADATA.json','CHECK_RESULTS.json',
         'VERIFY_TESTS.json','check_math.py','verify.py','test_integrity.py'}
AUTHOR_SHA = '2ed1cf89f1d8e3ea19184fa5bd14b840a2e12183b0ab4c1f0b690c9eea4f1e62'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def pairs(items):
    out = {}
    for key,value in items:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out

def load(p):
    return json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=pairs)

def main():
    need(not Path(__file__).is_symlink(), 'symlink verifier')
    root = Path(__file__).resolve().parent
    need({p.name for p in root.iterdir()} == FILES | {'MANIFEST.json'}, 'directory allowlist')
    for name in FILES | {'MANIFEST.json'}:
        p = root/name
        need(p.is_file() and not p.is_symlink(), 'regular payload required')
    m = load(root/'MANIFEST.json')
    need(set(m) == {'schema','problem_id','coverage','files'}, 'manifest keys')
    need(type(m['schema']) is int and m['schema'] == 1, 'manifest schema')
    need(m['problem_id'] == '6200022', 'manifest target')
    need(m['coverage'] == 'Every payload except MANIFEST.json.', 'coverage')
    need(type(m['files']) is dict and set(m['files']) == FILES, 'manifest allowlist')
    for name, entry in m['files'].items():
        need(type(entry) is dict and set(entry) == {'bytes','sha256'}, 'entry schema')
        need(type(entry['bytes']) is int and entry['bytes'] > 0, 'byte count type')
        need(type(entry['sha256']) is str and re.fullmatch('[0-9a-f]{64}',entry['sha256']), 'digest format')
        raw = (root/name).read_bytes()
        need(len(raw) == entry['bytes'], 'byte count mismatch')
        need(hashlib.sha256(raw).hexdigest() == entry['sha256'], 'hash mismatch')
    p = load(root/'PUBLIC_METADATA.json')
    need(p['target']['id'] == '6200022' and p['target']['problem_number'] == 'AMR-061-0022', 'semantic target')
    need(p['author_archive']['sha256'] == AUTHOR_SHA and p['author_archive']['bytes'] == 16021, 'author anchor')
    need(p['verdict']['accepted'] is True and p['verdict']['formal_certification'] is False, 'verdict scope')
    need(p['verdict']['novelty_claimed'] is False and p['verdict']['problem_21_resolved'] is False, 'scope boundary')
    need(p['record_review']['sha256'] == '14935ce8c0a28dc4f82299acb615159f9c02d1373854aaeda75f545db8efb245', 'record anchor')
    cmd = [sys.executable, '-I'] + (['-O'] if sys.flags.optimize else []) + [str(root/'check_math.py')]
    r = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd='/')
    actual = json.loads(r.stdout, object_pairs_hook=pairs)
    need(actual == load(root/'CHECK_RESULTS.json'), 'arithmetic replay mismatch')
    need(actual['status'] == 'pass' and actual['total_checks'] == 27534, 'arithmetic totals')
    print(json.dumps({'status':'pass','problem_id':'6200022','audit_checks':actual['total_checks'],
                      'optimized':bool(sys.flags.optimize),'manifest_payloads':len(FILES)},sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        sys.exit(1)
