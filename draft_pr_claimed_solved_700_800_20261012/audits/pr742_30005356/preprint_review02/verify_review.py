"""Verify the closed second-review inventory and its six permitted frozen inputs."""
from pathlib import Path, PurePosixPath
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'REVIEW_MANIFEST.json').read_text())
groups = [manifest['authored_files'], manifest['permitted_frozen_inputs']]
entries = [e for group in groups for e in group]
names = [e['path'] for e in entries]
if len(names) != len(set(names)) or len(groups[1]) != 6:
    raise ValueError('Duplicate paths or wrong permitted input count')
for entry in entries:
    name = entry['path']
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name or str(p) != name or name == 'REVIEW_MANIFEST.json':
        raise ValueError('Unsafe or self path')
    path = root / name
    if not path.is_file() or path.is_symlink():
        raise ValueError('Nonregular input')
    raw = path.read_bytes()
    if len(raw) != entry['bytes'] or hashlib.sha256(raw).hexdigest() != entry['sha256']:
        raise ValueError('Fingerprint mismatch: ' + name)
actual = set()
for path in root.rglob('*'):
    if path.is_symlink():
        raise ValueError('Symlink')
    if path.is_file():
        actual.add(path.relative_to(root).as_posix())
    elif not path.is_dir():
        raise ValueError('Nonregular entry')
if actual != set(names) | {'REVIEW_MANIFEST.json'}:
    raise ValueError('Unexpected or missing review files')
expected_dirs = {parent.as_posix() for name in names for parent in PurePosixPath(name).parents
                 if parent.as_posix() != '.'}
actual_dirs = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
if actual_dirs != expected_dirs:
    raise ValueError('Unexpected or missing review directories')
if manifest['external_communications'] or manifest['remote_mutations'] or manifest['private_third_party_bodies_included']:
    raise ValueError('Research boundary violated')
print('PASS:', len(groups[0]), 'authored files and six permitted frozen inputs; closed inventory and all hashes verified')
