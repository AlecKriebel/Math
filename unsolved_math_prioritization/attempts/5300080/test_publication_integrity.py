#!/usr/bin/env python3
"""Disposable publication mutations; all rejection checks remain active with -O."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def demand(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    source = Path(__file__).resolve().parent
    pin = hashlib.sha256((source/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest()
    def run(root, expected=pin):
        return subprocess.run([sys.executable, '-O', '-B', str(root/'verify_publication.py'),
                               '--expected-manifest-sha256', expected, '--integrity-only'],
                              capture_output=True, text=True).returncode
    demand(run(source) == 0, 'positive baseline')
    cases = ['changed_author', 'changed_audit', 'changed_author_zip', 'changed_audit_zip',
             'missing_file', 'extra_file', 'extra_directory', 'symlink',
             'changed_manifest', 'wrong_external_pin', 'duplicate_json_key',
             'duplicate_manifest_path', 'unsafe_manifest_path', 'rehashed_scope_upgrade',
             'rehashed_archive_change', 'rehashed_expanded_change']
    outcomes = []
    with tempfile.TemporaryDirectory(prefix='henon publication mutations ') as temp:
        for case in cases:
            root = Path(temp)/case
            shutil.copytree(source, root)
            manifest = root/'PUBLICATION_MANIFEST.json'
            m = json.loads(manifest.read_text())
            expected = pin
            changes = {'changed_author': 'author/PROOF.md',
                       'changed_audit': 'independent_audit/AUDIT.md',
                       'changed_author_zip': 'archives/henon_boundary_5300080_author.zip',
                       'changed_audit_zip': 'archives/henon_boundary_5300080_independent_audit.zip',
                       'rehashed_archive_change': 'archives/henon_boundary_5300080_author.zip',
                       'rehashed_expanded_change': 'author/PROOF.md'}
            if case in changes:
                target = root/changes[case]
                target.write_bytes(target.read_bytes() + b'\n')
            elif case == 'missing_file':
                (root/'author/PROOF.md').unlink()
            elif case == 'extra_file':
                (root/'unexpected.pdf').write_bytes(b'not a source PDF')
            elif case == 'extra_directory':
                (root/'unexpected').mkdir()
            elif case == 'symlink':
                target=root/'author/PROOF.md'; target.unlink(); target.symlink_to(root/'README.md')
            elif case == 'changed_manifest':
                manifest.write_bytes(manifest.read_bytes()+b'\n')
            elif case == 'wrong_external_pin':
                expected = '0'*64
            elif case == 'duplicate_json_key':
                manifest.write_text(manifest.read_text().replace('"schema": 1', '"schema": 1, "schema": 1'))
                expected = hashlib.sha256(manifest.read_bytes()).hexdigest()
            elif case == 'duplicate_manifest_path':
                m['files'].append(m['files'][0]); manifest.write_text(json.dumps(m))
                expected = hashlib.sha256(manifest.read_bytes()).hexdigest()
            elif case == 'unsafe_manifest_path':
                m['files'][0]['path'] = '../outside'; manifest.write_text(json.dumps(m))
                expected = hashlib.sha256(manifest.read_bytes()).hexdigest()
            elif case == 'rehashed_scope_upgrade':
                target=root/'PUBLICATION_STATUS.json'; value=json.loads(target.read_text())
                value['full_target_resolved']=True; target.write_text(json.dumps(value))
            if case.startswith('rehashed_'):
                for e in m['files']:
                    data=(root/e['path']).read_bytes();e.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
                manifest.write_text(json.dumps(m));expected=hashlib.sha256(manifest.read_bytes()).hexdigest()
            demand(run(root, expected) != 0, 'accepted mutation: '+case)
            outcomes.append({'name':case,'rejected':True})
    print(json.dumps({'status':'PASS','assertions_active_under_optimization':True,
                      'positive_baseline':True,'negative_controls':outcomes},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
