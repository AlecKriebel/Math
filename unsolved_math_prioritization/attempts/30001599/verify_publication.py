#!/usr/bin/env python3
"""Strict publication binding and portable replay; Python standard library only."""
import argparse
import copy
import hashlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
AUTHOR = 'fat_points_30001599/safe/'
AUDIT = 'fat_points_30001599_independent_audit/safe/'
ARCHIVE = 'fat_points_30001599/FAT_POINTS_30001599_SAFE_FROZEN.zip'
PINS = {
    AUTHOR+'MANIFEST.json': '675d0e15df109374d34bea061bb54ffc23e70fa87b344f9a2b3fc57acd40dc51',
    AUDIT+'MANIFEST.json': '6479531a723ea29c5267c0b3a425a83d96982dc25bb80862f371377b91fcc640',
    AUDIT+'AUDIT.md': 'ec2cf7fdc5ac33b0758e0b4f6fb00cb9c40a974b833c5fbf9e6925ab2ac20835',
    ARCHIVE: '23445c65f62d9f1d06c140ec12378aac0ce6f2539303eeadf9e5ce7851e9c526',
}
MANIFEST = 'PUBLICATION_MANIFEST.json'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def verify(blobs, expected):
    require(MANIFEST in blobs and sha(blobs[MANIFEST]) == expected, 'publication manifest hash')
    manifest = json.loads(blobs[MANIFEST])
    require(manifest['target_id'] == '30001599' and manifest['status'] == 'unsolved'
            and manifest['turns_used'] == 5 and manifest['turns_limit'] == 5
            and manifest['full_resolution'] is False, 'publication target')
    records = manifest['files']
    paths = [r['file'] for r in records]
    require(len(paths) == len(set(paths)), 'duplicate manifest path')
    require(set(blobs) == set(paths) | {MANIFEST}, 'exact publication file set')
    for rec in records:
        p = rec['file']
        require(not Path(p).is_absolute() and '..' not in Path(p).parts, 'unsafe path')
        require(len(blobs[p]) == rec['bytes'] and sha(blobs[p]) == rec['sha256'], 'publication bytes: '+p)
    for p, digest in PINS.items():
        require(sha(blobs[p]) == digest, 'frozen pin: '+p)
    for prefix in (AUTHOR, AUDIT):
        sub = json.loads(blobs[prefix+'MANIFEST.json'])
        names = [r['file'] for r in sub['files']]
        require(len(names) == len(set(names)), 'duplicate frozen record')
        require({p[len(prefix):] for p in blobs if p.startswith(prefix)} == set(names)|{'MANIFEST.json'}, 'frozen exact set')
        for rec in sub['files']:
            data = blobs[prefix+rec['file']]
            require(len(data) == rec['bytes'] and sha(data) == rec['sha256'], 'frozen manifest bytes')
    binding = json.loads(blobs[AUDIT+'BINDING.json'])
    require(binding['target']['id'] == '30001599' and binding['target']['rank'] == 697
            and binding['target']['attempts_used'] == 5
            and binding['target']['full_resolution'] is False
            and binding['verdict'] == 'PASS_as_unsolved_5_of_5_with_scoped_partials', 'audit target')
    require(binding['target'] == json.loads(blobs[AUDIT+'results.json'])['target'], 'audit result target')
    originals = binding['original_files']
    require(len(originals) == 8 and {r['file'] for r in originals} ==
            {p[len(AUTHOR):] for p in blobs if p.startswith(AUTHOR)}, 'audit original file set')
    for rec in originals:
        data = blobs[AUTHOR+rec['file']]
        require(sha(data) == rec['sha256'] and len(data) == rec['bytes'], 'audit original bytes')
    for key in ('audit_code', 'audit_report', 'audit_results'):
        rec = binding[key]
        require(sha(blobs[AUDIT+rec['file']]) == rec['sha256'], key)
    require(sha(blobs[ARCHIVE]) == binding['original_archive']['sha256']
            and len(blobs[ARCHIVE]) == binding['original_archive']['bytes'], 'archive binding')
    with zipfile.ZipFile(io.BytesIO(blobs[ARCHIVE])) as z:
        names = z.namelist()
        require(len(names) == 8 and len(names) == len(set(names))
                and set(names) == {r['file'] for r in originals}, 'archive exact set')
        require(all(z.read(p) == blobs[AUTHOR+p] for p in names), 'archive contents')
    return manifest

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-manifest-sha256', required=True)
    args = parser.parse_args()
    expected = args.expected_manifest_sha256
    require(len(expected) == 64 and all(x in '0123456789abcdef' for x in expected), 'invalid expected hash')
    require(not any(p.is_symlink() for p in HERE.rglob('*')), 'symlinks not accepted')
    blobs = {p.relative_to(HERE).as_posix(): p.read_bytes() for p in HERE.rglob('*') if p.is_file()}
    manifest = verify(blobs, expected)
    rejected = []
    mutants = []
    for p in (AUTHOR+'PROOFS.md', AUDIT+'AUDIT.md', AUDIT+'BINDING.json',
              AUDIT+'results.json', AUTHOR+'MANIFEST.json', AUDIT+'MANIFEST.json',
              ARCHIVE, 'README.md', 'verify_publication.py', MANIFEST):
        mutant = dict(blobs); mutant[p] += b'\n'; mutants.append(('changed '+p, mutant, expected))
    mutant = dict(blobs); del mutant[AUTHOR+'PROOFS.md']; mutants.append(('missing file', mutant, expected))
    mutant = dict(blobs); mutant['unreviewed.txt'] = b'x'; mutants.append(('extra file', mutant, expected))
    mutants.append(('wrong trusted hash', blobs, '0'*64))
    for label, mutant, pin in mutants:
        try:
            verify(mutant, pin)
        except (ValueError, KeyError, json.JSONDecodeError, zipfile.BadZipFile):
            rejected.append(label)
        else:
            raise AssertionError('corruption accepted: '+label)
    with tempfile.TemporaryDirectory(prefix='fat-point-portable-') as td:
        root = Path(td)/'relocated-package'
        for p, data in blobs.items():
            dest = root/p; dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(data)
        script = root/AUDIT/'independent_checks.py'
        ns = {'__name__': 'portable_audit', '__file__': str(script)}
        exec(compile(script.read_bytes(), str(script), 'exec'), ns)
        ns['main']()
        require((root/AUDIT/'results.json').read_bytes() == blobs[AUDIT+'results.json'], 'audit replay differs')
        for p, data in blobs.items():
            require((root/p).read_bytes() == data, 'relocated bytes differ: '+p)
    require(blobs == {p.relative_to(HERE).as_posix(): p.read_bytes() for p in HERE.rglob('*') if p.is_file()}, 'published inputs changed')
    result = json.loads(blobs[AUDIT+'results.json'])
    print(json.dumps({'target_id': '30001599', 'status': 'unsolved', 'turns': '5/5',
          'publication_manifest_sha256': expected, 'files_verified': len(blobs),
          'publication_corruptions_rejected': len(rejected),
          'audit_counts': result['counts'], 'audit_replay_exact': True,
          'author_replay_exact': result['author_control_replay_matches'],
          'original_bytes_unchanged': True, 'universal_result_proved': False}, sort_keys=True))

if __name__ == '__main__':
    main()
