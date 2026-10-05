#!/usr/bin/env python3
"""Integrity and exact finite tail checks for the second quasiconical audit.

This is not a PDE solver, proof assistant, or analytic theorem certificate.
No input is edited or copied into the package.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile


EXPECTED = {
    'author': (16490, '2d15c0f1f7b094c92bafb6d2fed6d3b212c597adf9043c9f49c737a6f082e09e'),
    'first_audit': (45053, '64bf89900a083fbc41176efd9766fde3a64397a5850207ce8e190eebbcdae6ea'),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def safe_relative(name):
    p = PurePosixPath(name)
    return not p.is_absolute() and '..' not in p.parts and str(p) == name


def validate_manifest(manifest, read):
    rows = manifest['files']
    names = [row['path'] for row in rows]
    require(len(names) == len(set(names)), 'duplicate manifest paths')
    for row in rows:
        require(safe_relative(row['path']), 'unsafe member path')
        data = read(row['path'])
        require(len(data) == row['bytes'], 'member byte count: '+row['path'])
        require(sha(data) == row['sha256'], 'member hash: '+row['path'])
    return set(names)


def archive_check(path, key):
    data = path.read_bytes()
    size, digest = EXPECTED[key]
    require(len(data) == size, key+' archive bytes')
    require(sha(data) == digest, key+' archive hash')
    with zipfile.ZipFile(path) as z:
        require(z.testzip() is None, key+' archive CRC')
        names = z.namelist()
        require(len(names) == len(set(names)), key+' duplicate ZIP members')
        require(all(safe_relative(n) for n in names), key+' unsafe ZIP members')
        manifest = json.loads(z.read('MANIFEST.json'))
        expected_names = validate_manifest(manifest, z.read) | {'MANIFEST.json'}
        require(set(names) == expected_names, key+' exact member set')
        payload = {name: z.read(name) for name in names}
    return payload, {'bytes': size, 'sha256': digest, 'members': len(payload),
                     'manifest_and_crc_match': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-zip', type=Path)
    parser.add_argument('--first-audit-zip', type=Path)
    parser.add_argument('--inputs-only', action='store_true',
                        help='Skip package manifest verification during initial freezing.')
    args = parser.parse_args()
    require(bool(args.author_zip) == bool(args.first_audit_zip),
            'supply both frozen archives or neither')
    result = {'status': 'PASS', 'scope': 'Integrity and exact finite arithmetic only'}
    if not args.inputs_only:
        root = Path(__file__).resolve().parent
        manifest = json.loads((root/'MANIFEST.json').read_bytes())
        names = validate_manifest(manifest, lambda n: (root/n).read_bytes())
        actual = {p.name for p in root.iterdir() if p.is_file()}
        require(actual == names | {'MANIFEST.json'}, 'exact package file set')
        result['package'] = {'manifest_matches': True, 'payload_files': len(names)}
    if args.author_zip:
        author, author_meta = archive_check(args.author_zip, 'author')
        first, first_meta = archive_check(args.first_audit_zip, 'first_audit')
        for name, data in author.items():
            require(first['author/'+name] == data, 'embedded author identity: '+name)
        require(sha(author['PROOF.md']) ==
                '5d1bab0b62ac5f78c69b0d82babd0b79fa4944097470fa760fdb3c485e362a20',
                'frozen proof hash')
        result['inputs'] = {'author': author_meta, 'first_audit': first_meta,
                            'embedded_author_identical': True,
                            'frozen_proof_hash_matches': True}
    tests = 0
    for n in range(1, 129):
        tail = Fraction(1, 2**(n+1))
        require(tail < 1, 'rank threshold')
        require(Fraction(1, 2**n)+tail == 3*tail, 'birth plus tail')
        tests += 2
        for m in range(n+1, n+17):
            partial = sum(Fraction(1, 2**(j+2)) for j in range(n, m))
            remainder = Fraction(1, 2**(m+1))
            require(partial+remainder == tail, 'finite sum plus remainder')
            tests += 1
    result['exact_tail_checks'] = tests
    result['not_certified'] = ['Infinite-dimensional analytic theorem',
                               'Numerical aperture choices', 'Historical priority']
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
