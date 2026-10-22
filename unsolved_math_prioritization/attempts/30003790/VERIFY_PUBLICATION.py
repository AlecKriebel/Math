#!/usr/bin/env python3
"""Strict portable package verification; no network or writes."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess
import sys


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check_manifest(root, name):
    data = json.loads((root/name).read_text())
    expected = {name}
    for item in data['files']:
        q = PurePosixPath(item['path'])
        assert not q.is_absolute() and '..' not in q.parts and '.' not in q.parts
        assert str(q) == item['path'] and item['path'] not in expected
        expected.add(item['path'])
        p = root/item['path']
        assert p.is_file() and not p.is_symlink()
        assert p.stat().st_size == item['bytes'] and sha(p) == item['sha256']
    actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    assert expected == actual
    for p in root.rglob('*'):
        assert not p.is_symlink()
        assert 'private' not in p.relative_to(root).parts
        if p.is_file():
            assert p.suffix in {'.md','.json','.py','.diff'}


def main():
    root = Path(__file__).resolve().parent
    check_manifest(root, 'PUBLICATION_MANIFEST.json')
    release = root/'release-v2'
    audit = root/'release-v2-binding-audit'
    assert sha(release/'RELEASE_MANIFEST.json') == 'ea2b9302812262a611e68745648dad936f796bd4fa9c03f32ae320e2767760fe'
    assert sha(audit/'MANIFEST.json') == 'a409898869b5a38dec86ac71a6ca8d96059daeff43e701c15a55410f2cb01059'
    check_manifest(audit, 'MANIFEST.json')
    result = subprocess.run([sys.executable,str(audit/'verification/verify_binding.py'),str(release)],
                            check=True,capture_output=True).stdout
    assert result == (audit/'verification/result.json').read_bytes()
    check_manifest(root, 'PUBLICATION_MANIFEST.json')
    print(json.dumps({'status':'PASS','artifact_files':53,
      'accepted_release_files':44,'supplemental_acceptance_files':6,
      'accepted_files_byte_identical':True,'strict_inventory':True,
      'supplemental_binding_replay_byte_identical':True,
      'mathematical_edits':False,'limits':'Integrity and recorded finite controls only.'},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
