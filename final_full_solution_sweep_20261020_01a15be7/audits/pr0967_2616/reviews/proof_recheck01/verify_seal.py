#!/usr/bin/env python3
"""Read-only verification of a detached, externally anchored evidence manifest."""
import argparse
import hashlib
import json
from pathlib import Path


def need(ok, msg):
    if not ok:
        raise RuntimeError(msg)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--expected-manifest-sha256', required=True)
    args = ap.parse_args()
    root = args.root.resolve()
    expected = args.expected_manifest_sha256
    need(len(expected) == 64 and all(c in '0123456789abcdef' for c in expected), 'digest syntax')
    raw = (root/'EVIDENCE_MANIFEST.json').read_bytes()
    need(sha(raw) == expected, 'external manifest digest mismatch')
    manifest = json.loads(raw)
    need(manifest['schema'] == 1 and manifest['problem_id'] == 2616, 'manifest identity')
    need((root/'SEAL.sha256').read_text() == expected+'  EVIDENCE_MANIFEST.json\n', 'detached seal mismatch')
    all_paths = list(root.rglob('*'))
    need(not any(p.is_symlink() for p in all_paths), 'symlink in sealed evidence')
    actual_files = {str(p.relative_to(root)) for p in all_paths if p.is_file()}
    rows = manifest['files']
    named = [row['path'] for row in rows]
    need(len(named) == len(set(named)), 'duplicate manifest file')
    need(actual_files == set(named) | {'EVIDENCE_MANIFEST.json', 'SEAL.sha256'}, 'file-set mismatch')
    actual_dirs = sorted(str(p.relative_to(root)) for p in all_paths if p.is_dir())
    need(actual_dirs == manifest['directories'], 'directory-set mismatch')
    for row in rows:
        rel = Path(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts and str(rel) == row['path'], 'unsafe manifest path')
        body = (root/rel).read_bytes()
        need(len(body) == row['bytes'] and sha(body) == row['sha256'], 'body mismatch: '+row['path'])
    print(json.dumps({'status':'PASS','manifest_sha256':expected,'verified_files':len(rows),
                      'verified_directories':len(actual_dirs),'private_evidence_included':True,
                      'writes_performed':False},sort_keys=True))


if __name__ == '__main__':
    main()
