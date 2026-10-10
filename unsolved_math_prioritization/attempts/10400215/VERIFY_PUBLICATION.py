"""Externally authenticate this verifier before running Python -I -S -B."""
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import zipfile

MANIFEST_PIN = 'f33f1856c07100cabb8d0ebf99c1b6fd0fc2955152fcb8392bb68e027ef6f94e'

def require(condition, message):
    if not condition:
        raise SystemExit('PUBLICATION REJECT: ' + message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result

def regular(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'nonregular file')
    return path.read_bytes()

require(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
        'Python -I -S -B is required')
require(len(sys.argv) == 2, 'supply exactly the package root')
root = Path(sys.argv[1]).absolute()
for ancestor in (root,) + tuple(root.parents):
    require(not ancestor.is_symlink(), 'symlink root or ancestor')
require(root.is_dir(), 'invalid package root')
require(Path(__file__).absolute() == root / 'VERIFY_PUBLICATION.py', 'verifier location')
manifest_bytes = regular(root / 'PUBLICATION_MANIFEST.json')
require(sha(manifest_bytes) == MANIFEST_PIN, 'manifest pin')
manifest = json.loads(manifest_bytes, object_pairs_hook=unique)
require(manifest['problem_id'] == 10400215 and manifest['rank'] == 847, 'identity')
require(manifest['status'] == 'unsolved_by_this_attempt' and
        manifest['approaches_used'] == manifest['approach_limit'] == 5, 'disposition')
files = manifest['files']
expected_files = set(files) | {'PUBLICATION_MANIFEST.json', 'VERIFY_PUBLICATION.py'}
expected_dirs = {'author', 'independent_audit'}

def authenticate():
    actual_files, actual_dirs = set(), set()
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            actual_dirs.add(name)
        else:
            require(stat.S_ISREG(mode), 'nonregular package entry')
            actual_files.add(name)
    require(actual_files == expected_files and actual_dirs == expected_dirs,
            'strict complete inventory')
    for name, meta in files.items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts,
                'unsafe manifest path')
        data = regular(root / name)
        require(len(data) == meta['bytes'] and sha(data) == meta['sha256'],
                'payload authentication')
    require(regular(root / 'PUBLICATION_MANIFEST.json') == manifest_bytes, 'manifest changed')

authenticate()
# Authenticate all archive member bytes before invoking any payload code.
for prefix, archive_suffix, directory in (
    ('AUTHOR', 'SAFE_FREEZE.zip', 'author'),
    ('INDEPENDENT_AUDIT', 'SAFE.zip', 'independent_audit'),
):
    stem = 'SHADOW_NORM_10400215_' + prefix + '_'
    inventory = json.loads(regular(root / (stem + 'EXTERNAL_MANIFEST.json')),
                           object_pairs_hook=unique)['files']
    with zipfile.ZipFile(io.BytesIO(regular(root / (stem + archive_suffix)))) as archive:
        members = archive.infolist()
        require(len(members) == len(inventory) and
                {item.filename for item in members} == set(inventory), 'ZIP inventory')
        for item in members:
            require(Path(item.filename).name == item.filename and
                    stat.S_ISREG(item.external_attr >> 16), 'ZIP member path or type')
            data = archive.read(item)
            meta = inventory[item.filename]
            require(len(data) == meta['bytes'] and sha(data) == meta['sha256'],
                    'ZIP member bytes')
            require(data == regular(root / directory / item.filename), 'extracted member bytes')

flags = ['-I', '-S', '-B'] + (['-O'] if sys.flags.optimize else [])
result = subprocess.run(
    [sys.executable, *flags, str(root / 'SHADOW_NORM_10400215_INDEPENDENT_AUDIT_VALIDATION.py'), str(root)],
    cwd=root, env={'PATH': os.environ.get('PATH', '')}, capture_output=True, timeout=180)
require(result.returncode == 0 and not result.stderr, 'independent validation failed')
require(result.stdout == regular(root / 'SHADOW_NORM_10400215_INDEPENDENT_AUDIT_VALIDATION_RECEIPT.json'),
        'independent validation receipt mismatch')
authenticate()
print(json.dumps({
    'schema': 1, 'problem_id': 10400215, 'status': 'pass',
    'queue_disposition': 'unsolved', 'approaches_used': 5, 'approach_limit': 5,
    'complete_package_files': len(expected_files), 'manifest_sha256': MANIFEST_PIN,
    'both_original_archives_and_all_members_match': True,
    'validation_receipt_sha256': sha(result.stdout),
    'independent_checks_per_acceptance': 68324, 'author_checks_per_replay': 45810,
    'positive_acceptance_replays': 4, 'author_positive_replays_per_acceptance': 4,
    'author_boundary_rejections_per_acceptance': 40, 'audit_boundary_rejections': 44,
    'scope': 'Static exact-byte and finite-algebra checks; no universal topological proof.'
}, sort_keys=True, indent=2))
