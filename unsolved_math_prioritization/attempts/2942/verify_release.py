#!/usr/bin/env python3
"""Offline immutable bindings and finite controls; not a topology proof."""
from pathlib import Path
from hashlib import sha256
import io
import json
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVES = {
    'AUTHOR_SAFE.zip': (24247, '6b4de8ccb793e9284547a7beee11b2f203cb7f5edfb0eb9c22d2cd873e06825e', 'author', 10),
    'INDEPENDENT_AUDIT_SAFE.zip': (23023, '60b44afb8702f93b114dcb8b091204c18b8a98f982b03265bc0f2575535617d9', 'audit', 8),
}
ANCHORS = {
    'author/AUTHOR_MANIFEST.json': '66298016e916da48b988c46affdfc3dc3636a9d80888e21f0e03b10d72eb94fa',
    'author/PROOF.md': '889b365034795f4cc3c53d229fd44e653bcac9f5af9946eb61955e831a03581f',
    'audit/AUDIT_MANIFEST.json': '5ee1efe7a901eda43a73b2b6c01f10f1e7322bf8ad1e4f46034359ceaaa219b0',
    'audit/AUDIT.md': 'f61454c2f01b89f8978d19abf22806d125d5d9af97c23658c6a67f3476e11c2a',
    'audit/AUDIT_BINDING.json': '1b4eefdf83b468ee9147dd964f2ba3ad6f3ac57d13bdb371f9c814cf93e7fd46',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def record_matches(data, entry):
    return len(data) == entry['bytes'] and sha256(data).hexdigest() == entry['sha256']


def check_manifest(folder, name):
    manifest = json.loads((folder/name).read_text())
    seen = set()
    for entry in manifest['files']:
        relative = entry['name']
        p = Path(relative)
        require(not p.is_absolute() and '..' not in p.parts and relative not in seen, 'Unsafe/duplicate manifest entry')
        seen.add(relative)
        target = folder/p
        require(not target.is_symlink() and target.is_file(), 'Missing or unsafe file: '+relative)
        require(record_matches(target.read_bytes(), entry), 'Manifest mismatch: '+relative)
    actual = {str(p.relative_to(folder)) for p in folder.rglob('*') if p.is_file()}
    require(actual == seen | {name}, 'File inventory mismatch: '+name)
    return manifest


def main():
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(), 'Symlink not allowed')
    release = check_manifest(ROOT, 'RELEASE_MANIFEST.json')
    for relative, expected in ANCHORS.items():
        require(sha256((ROOT/relative).read_bytes()).hexdigest() == expected, 'Immutable anchor mismatch: '+relative)
    for archive, (size, digest, folder, count) in ARCHIVES.items():
        data = (ROOT/archive).read_bytes()
        require(len(data) == size and sha256(data).hexdigest() == digest, 'Immutable archive mismatch: '+archive)
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            names = z.namelist()
            require(len(names) == count and len(set(names)) == count, 'Archive inventory mismatch')
            require(all(Path(n).name == n for n in names), 'Unsafe archive member')
            require(set(names) == {p.name for p in (ROOT/folder).iterdir() if p.is_file()}, 'Extracted inventory mismatch')
            for name in names:
                require(z.read(name) == (ROOT/folder/name).read_bytes(), 'Archive member mismatch: '+name)
    author = check_manifest(ROOT/'author', 'AUTHOR_MANIFEST.json')
    audit = check_manifest(ROOT/'audit', 'AUDIT_MANIFEST.json')
    binding = json.loads((ROOT/'audit/AUDIT_BINDING.json').read_text())
    require(binding['author_archive']['sha256'] == ARCHIVES['AUTHOR_SAFE.zip'][1], 'Author archive audit binding mismatch')
    require(binding['author_manifest_sha256'] == ANCHORS['author/AUTHOR_MANIFEST.json'], 'Author manifest audit binding mismatch')
    require(len(binding['author_files']) == 10, 'Wrong author binding count')
    for entry in binding['author_files']:
        require(record_matches((ROOT/'author'/entry['name']).read_bytes(), entry), 'Audit author binding mismatch')
    status = json.loads((ROOT/'RELEASE_STATUS.json').read_text())
    require(status['problem_id'] == 2942 and status['rank'] == 694, 'Wrong target')
    require(status['disposition'] == 'unsolved' and status['turns'] == '5/5' and status['target_resolved'] is False, 'Wrong disposition')
    require(status['independent_audit_verdict'] == binding['verdict'] == audit['verdict'] == 'PASS_FOR_UNSOLVED_5_OF_5', 'Wrong audit verdict')
    require(binding['required_author_corrections'] == status['required_author_corrections'] == [], 'Unexpected author correction')
    jobs = [
        ('author/verify_packet.py', [], 'audit/AUTHOR_REPLAY_RESULT.json', 'finite_controls', 6378),
        ('author/verify_controls.py', [], 'author/CONTROL_RESULTS.json', 'checks', 6378),
        ('audit/independent_controls.py', [], 'audit/INDEPENDENT_CONTROL_RESULTS.json', 'checks', 13618),
        ('audit/negative_controls.py', [str(ROOT/'AUTHOR_SAFE.zip')], 'audit/NEGATIVE_CONTROL_RESULTS.json', 'rejected_cases', 39),
    ]
    with tempfile.TemporaryDirectory(prefix='lasagna2942-replay-') as temporary:
        for script, args, saved, key, expected in jobs:
            for flags in ([], ['-O']):
                output = subprocess.check_output([sys.executable, '-B']+flags+[str(ROOT/script)]+args, cwd=temporary)
                require(output == (ROOT/saved).read_bytes(), 'Replay output mismatch: '+script)
                require(json.loads(output)[key] == expected, 'Unexpected control count')
    print(json.dumps({
        'status': 'PASS_IMMUTABLE_BINDINGS_AND_FINITE_REPLAY',
        'problem_id': 2942, 'disposition': 'unsolved', 'turns': '5/5',
        'release_files': len(release['files'])+1,
        'frozen_author_files': len(author['files'])+1,
        'frozen_audit_files': len(audit['files'])+1,
        'author_controls': 6378, 'independent_controls': 13618, 'negative_controls': 39,
        'normal_and_optimized_outputs_byte_identical': True,
        'scope': 'Integrity and finite algebra only; not a topology proof, human peer review, novelty determination or GitHub CI result.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
