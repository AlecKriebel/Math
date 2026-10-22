#!/usr/bin/env python3
"""Portable integrity and exact replay for the scoped partial-result packet."""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
PINS = {
    'authored/MANIFEST.json': 'a59097544b285a4d5452cad2b8dac7d80d4f437098b123f71e04ad06242d9fa7',
    'independent_audit/AUDIT_MANIFEST.json': '5f2be175c5830e1d41f901e287c57c6d56c5d0084255519c83c3aa972624ebf1',
    'independent_audit/corrected/PARTIAL_THEOREMS.md': 'f2e0e866b9ae517ea1cdb3181546ab67f6afccd9dd604d537c64c3960984c65f',
}
FILES = set('''README.md
PUBLICATION_ACCEPTANCE.md
requirements.txt
verify_publication.py
authored/MANIFEST.json
authored/PARTIAL_THEOREMS.md
authored/README.md
authored/SLICE_GRAM_CERTIFICATES.json
authored/SOURCE_AND_READINESS.md
authored/SOURCE_MANIFEST.json
authored/VERIFICATION.json
authored/verify.py
independent_audit/AUDIT.md
independent_audit/AUDIT_MANIFEST.json
independent_audit/CORRECTION.json
independent_audit/INDEPENDENT_CHECKS.json
independent_audit/WORDING_CORRECTION.patch
independent_audit/corrected/PARTIAL_THEOREMS.md
independent_audit/independent_verify.py'''.splitlines())

def require(condition, message):
    if not condition:
        raise ValueError(message)

def pairs(items):
    out = {}
    for key, value in items:
        require(key not in out, 'duplicate JSON key: ' + key)
        out[key] = value
    return out

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def record(data):
    return {'bytes': len(data), 'sha256': digest(data),
            'git_blob_sha1': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()}

def safe_path(root, name):
    p = PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and str(p) == name,
            'unsafe/noncanonical path: ' + name)
    require('\\' not in name, 'backslash in path: ' + name)
    target = root.joinpath(*p.parts)
    require(not any(part.is_symlink() for part in [target, *target.parents] if part != root.parent),
            'symlink in path: ' + name)
    return target

def integrity(root):
    manifest = read_json(root / 'PUBLICATION_MANIFEST.json')
    require(manifest['problem_id'] == 30005481 and manifest['queue_status'] == 'unsolved'
            and manifest['turns'] == '5/5', 'wrong target/disposition')
    require(manifest['frozen_sha256'] == PINS, 'changed frozen pins')
    require(set(manifest['files']) == FILES, 'wrong manifest inventory')
    actual = set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'unexpected symlink: ' + str(p.relative_to(root)))
        if p.is_file():
            actual.add(p.relative_to(root).as_posix())
    require(actual == FILES | {'PUBLICATION_MANIFEST.json'}, 'wrong on-disk inventory')
    for name, expected in manifest['files'].items():
        raw = safe_path(root, name).read_bytes()
        require(record(raw) == expected, 'publication identity mismatch: ' + name)
    for name, sha in PINS.items():
        require(digest((root / name).read_bytes()) == sha, 'frozen pin mismatch: ' + name)
    for folder, mname in [('authored', 'MANIFEST.json'),
                          ('independent_audit', 'AUDIT_MANIFEST.json')]:
        frozen = read_json(root / folder / mname)
        require(frozen['problem_id'] == 30005481, 'wrong frozen target')
        for name, expected in frozen['files'].items():
            raw = safe_path(root / folder, name).read_bytes()
            require({'bytes': len(raw), 'sha256': digest(raw)} == expected,
                    'frozen file identity mismatch: ' + folder + '/' + name)
    original = (root / 'authored/PARTIAL_THEOREMS.md').read_bytes()
    corrected = (root / 'independent_audit/corrected/PARTIAL_THEOREMS.md').read_bytes()
    correction = read_json(root / 'independent_audit/CORRECTION.json')
    old = b'A scalar multiple of a map has the same extendability status.'
    new = b'A nonzero scalar multiple of a map has the same extendability status.'
    require(correction['old'].encode() == old and correction['new'].encode() == new,
            'changed correction language')
    require(original.count(old) == 1 and original.replace(old, new, 1) == corrected,
            'correction is not the sole authorized replacement')
    for label, raw in [('original', original), ('corrected', corrected)]:
        require(correction[label + '_bytes'] == len(raw)
                and correction[label + '_sha256'] == digest(raw), 'correction identity mismatch')
    patch = ''.join(difflib.unified_diff(original.decode().splitlines(keepends=True),
                                        corrected.decode().splitlines(keepends=True),
                                        fromfile='a/PARTIAL_THEOREMS.md',
                                        tofile='b/PARTIAL_THEOREMS.md'))
    require(patch.encode() == (root / 'independent_audit/WORDING_CORRECTION.patch').read_bytes(),
            'patch does not exactly represent the sole correction')
    return {'status': 'PASS', 'files': len(actual),
            'publication_manifest_sha256': digest((root / 'PUBLICATION_MANIFEST.json').read_bytes())}

def replay(root):
    import sympy
    import mpmath
    require(sympy.__version__ == '1.14.0' and mpmath.__version__ == '1.3.0',
            'Exact replay requires the versions in requirements.txt')
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    results = {}
    with tempfile.TemporaryDirectory(prefix='hook-replay-') as working:
        for name, script, saved, key, count in [
            ('author', 'authored/verify.py', 'authored/VERIFICATION.json', 'exact_assertions', 206),
            ('independent', 'independent_audit/independent_verify.py',
             'independent_audit/INDEPENDENT_CHECKS.json', 'independent_checks', 46),
        ]:
            run = subprocess.run([sys.executable, '-B', str(root / script)], cwd=working,
                                 env=env, capture_output=True, timeout=300, check=False)
            require(run.returncode == 0, name + ' replay failed: ' + run.stderr.decode(errors='replace'))
            require(run.stdout == (root / saved).read_bytes(), name + ' saved output differs')
            data = json.loads(run.stdout, object_pairs_hook=pairs)
            require(data[key] == count, name + ' unexpected check count')
            results[name] = {key: count, 'saved_output_byte_identical': True}
    integrity(root)
    return results

def selftest(root):
    cases = ['altered_file', 'missing_file', 'extra_file', 'symlink', 'unsafe_manifest_path',
             'rehashed_corrected_copy', 'rehashed_author_manifest', 'duplicate_json_key',
             'rehashed_patch']
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='hook-mutation-') as temporary:
            copy = Path(temporary) / 'packet'
            shutil.copytree(root, copy)
            manifest_path = copy / 'PUBLICATION_MANIFEST.json'
            manifest = read_json(manifest_path)
            def alter(name):
                p = copy / name
                p.write_bytes(p.read_bytes() + b'\n')
            if case == 'altered_file':
                alter('authored/verify.py')
            elif case == 'missing_file':
                (copy / 'authored/verify.py').unlink()
            elif case == 'extra_file':
                (copy / 'extra.txt').write_text('unexpected')
            elif case == 'symlink':
                p = copy / 'authored/verify.py'
                p.unlink()
                p.symlink_to(root / 'authored/verify.py')
            elif case == 'unsafe_manifest_path':
                manifest['files']['../escape'] = manifest['files'].pop('authored/verify.py')
            elif case == 'duplicate_json_key':
                manifest_path.write_text('{"problem_id":30005481,' + manifest_path.read_text()[1:])
            else:
                target = {'rehashed_corrected_copy': 'independent_audit/corrected/PARTIAL_THEOREMS.md',
                          'rehashed_author_manifest': 'authored/MANIFEST.json',
                          'rehashed_patch': 'independent_audit/WORDING_CORRECTION.patch'}[case]
                alter(target)
                manifest['files'][target] = record((copy / target).read_bytes())
            if case == 'unsafe_manifest_path' or case.startswith('rehashed_'):
                manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
            rejected = False
            try:
                integrity(copy)
            except (ValueError, OSError, KeyError, TypeError):
                rejected = True
            require(rejected, 'mutation not rejected: ' + case)
    return {'rejected': len(cases), 'cases': cases}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity-only', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    output = {'problem_id': 30005481, 'full_conjecture': 'unresolved',
              'weak_SOS_boundary': 'not determined', 'integrity': integrity(ROOT)}
    if not args.integrity_only:
        output['replay'] = replay(ROOT)
    if args.selftest:
        output['mutation_controls'] = selftest(ROOT)
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
