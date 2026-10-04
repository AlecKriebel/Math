#!/usr/bin/env python3
"""Strict recursive closure; only manifest itself and foreign primary cache omitted."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import argparse
import hashlib
import json

MANIFEST = 'artifact_manifest.json'
IGNORED_TREE = 'foreign_primary_cache'


def inventory(root):
    rows = []
    for p in sorted(root.rglob('*')):
        rel = p.relative_to(root)
        if rel.parts[0] == IGNORED_TREE:
            continue
        assert not p.is_symlink(), 'SYMLINK: '+str(rel)
        if p.is_file() and rel.as_posix() != MANIFEST:
            raw = p.read_bytes()
            rows.append({'path': rel.as_posix(), 'size': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
    return rows


def build(root):
    return {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
            'exclude_files': [MANIFEST], 'exclude_trees': [IGNORED_TREE],
            'files': inventory(root), 'scope': 'All recursively present first-party files and all executed source/streams/failures; only named foreign cache omitted'}


def verify(root, manifest):
    assert set(manifest) == {'schema', 'created_utc', 'exclude_files', 'exclude_trees', 'files', 'scope'}, 'MANIFEST_FIELDS'
    assert manifest['schema'] == 1, 'SCHEMA'
    assert manifest['exclude_files'] == [MANIFEST], 'EXCLUSION_CHEAT_FILES'
    assert manifest['exclude_trees'] == [IGNORED_TREE], 'EXCLUSION_CHEAT_TREES'
    paths = []
    for row in manifest['files']:
        assert set(row) == {'path', 'size', 'sha256'}, 'ROW_FIELDS'
        path = row['path']
        pp = PurePosixPath(path)
        assert path and not pp.is_absolute() and '..' not in pp.parts and pp.as_posix() == path, 'UNSAFE_PATH'
        assert path != MANIFEST and pp.parts[0] != IGNORED_TREE, 'EXCLUDED_PATH_IN_ROWS'
        paths.append(path)
    assert len(paths) == len(set(paths)) and paths == sorted(paths), 'DUPLICATE_OR_UNSORTED'
    actual = inventory(root)
    assert paths == [row['path'] for row in actual], 'CLOSURE_MISSING_OR_EXTRA'
    assert manifest['files'] == actual, 'HASH_OR_SIZE_MISMATCH'
    return {'verified': True, 'files': len(actual), 'excluded': [MANIFEST, IGNORED_TREE+'/'],
            'manifest_sha256': hashlib.sha256((root/MANIFEST).read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--no-digest', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.build:
        (root/MANIFEST).write_text(json.dumps(build(root), indent=2)+'\n')
    result = verify(root, json.loads((root/MANIFEST).read_text()))
    if args.no_digest:
        result.pop('manifest_sha256')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
