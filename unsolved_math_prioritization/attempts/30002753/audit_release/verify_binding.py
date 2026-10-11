#!/usr/bin/env python3
"""Bind the audit to the original frozen packet without extracting or changing it."""
from pathlib import Path
import hashlib
import json
import sys
import tarfile

EXPECTED_MANIFEST = 'dbc674b5e74de6e98a077b3eb5fd6a5b38e6566a89c6b629f54d7d8c0db9b31e'
EXPECTED_ARCHIVE = '051c82bb55cc5cd3a967b128db8c560065000ec5db81753cdb78016ef2e3755c'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def run(directory):
    base = Path(directory)
    safe = base/'safe_release'
    archive = base/'transpositions_30002753_safe.tar.gz'
    manifest_bytes = (safe/'MANIFEST.json').read_bytes()
    archive_bytes = archive.read_bytes()
    assert digest(manifest_bytes) == EXPECTED_MANIFEST
    assert len(archive_bytes) == 18329 and digest(archive_bytes) == EXPECTED_ARCHIVE
    manifest = json.loads(manifest_bytes)
    names = ['MANIFEST.json'] + [row['path'] for row in manifest['files']]
    assert len(names) == 10 and len(set(names)) == 10
    assert sorted(x.name for x in safe.iterdir()) == sorted(names)
    inventory = []
    for name in names:
        path = safe/name
        assert Path(name).name == name and path.is_file() and not path.is_symlink()
        data = path.read_bytes()
        if name != 'MANIFEST.json':
            record = next(row for row in manifest['files'] if row['path'] == name)
            assert len(data) == record['bytes'] and digest(data) == record['sha256']
        inventory.append({'path':name,'bytes':len(data),'sha256':digest(data)})
    with tarfile.open(archive, 'r:gz') as stream:
        members = stream.getmembers()
        assert len(members) == len(names)
        assert set(x.name for x in members) == {'safe_release/'+name for name in names}
        for member in members:
            assert member.isfile() and not member.issym() and not member.islnk()
            assert stream.extractfile(member).read() == (safe/Path(member.name).name).read_bytes()
    # Negative controls are in memory only.
    proof = (safe/'PROOF.md').read_bytes()
    expected = next(row for row in inventory if row['path'] == 'PROOF.md')
    changed = bytes([proof[0]^1])+proof[1:]
    assert digest(changed) != expected['sha256']
    assert len(proof[:-1]) != expected['bytes']
    assert digest(manifest_bytes+b' ') != EXPECTED_MANIFEST
    assert digest(archive_bytes[:-1]) != EXPECTED_ARCHIVE
    return {'status':'passed','frozen_manifest_sha256':EXPECTED_MANIFEST,
            'frozen_archive_sha256':EXPECTED_ARCHIVE,'frozen_archive_bytes':18329,
            'exact_safe_file_count':len(names),'inventory':sorted(inventory,key=lambda x:x['path']),
            'archive_matches_directory_byte_for_byte':True,
            'unexpected_files_links_or_path_traversal':False,
            'negative_controls':['one-bit proof mutation rejected','proof truncation rejected',
                                 'manifest alteration rejected','archive truncation rejected'],
            'frozen_inputs_changed':False}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python3 verify_binding.py DIRECTORY_CONTAINING_ORIGINAL_SAFE_RELEASE')
    print(json.dumps(run(sys.argv[1]),indent=2,sort_keys=True))
