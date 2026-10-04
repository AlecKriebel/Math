#!/usr/bin/env python3
"""Validate immutable research/audit bytes and replay both exact checkers."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def check_manifest(directory, name):
    manifest = json.loads((directory / name).read_text())
    for entry in manifest['files']:
        p = directory / entry['path']
        raw = p.read_bytes()
        assert len(raw) == entry['bytes'], p
        assert hashlib.sha256(raw).hexdigest() == entry['sha256'], p
    return manifest


def main():
    public = ROOT / 'public'
    audit = ROOT / 'audit'
    author = check_manifest(public, 'FROZEN_MANIFEST.json')
    reviewer = check_manifest(audit, 'AUDIT_MANIFEST.json')
    assert author['status'] == 'unsolved'
    assert author['approaches_completed'] == 5
    assert reviewer['verdict'] == 'PASS_FOR_PARTIAL_RESULTS'
    assert reviewer['required_corrections'] == []
    assert hashlib.sha256((public/'FROZEN_MANIFEST.json').read_bytes()).hexdigest() == reviewer['frozen_manifest_sha256']
    package = check_manifest(ROOT, 'PUBLICATION_MANIFEST.json')
    expected = {e['path'] for e in package['files']} | {'PUBLICATION_MANIFEST.json'}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts}
    assert actual == expected, (actual-expected, expected-actual)
    for script, saved in [(public/'verify.py', public/'verification.json'),
                          (audit/'independent_verify.py', audit/'INDEPENDENT_RESULTS.json')]:
        replay = json.loads(subprocess.check_output([sys.executable, str(script)], cwd=ROOT))
        assert replay == json.loads(saved.read_text()), script
    assert (public/'verification.json').read_bytes() == (audit/'AUTHOR_REPLAY.json').read_bytes()
    print(json.dumps({'status':'PASS', 'files_bound':len(package['files']),
                      'author_and_independent_replays':'PASS',
                      'mathematical_status':'unsolved', 'approaches':5},indent=2))


if __name__ == '__main__':
    main()
