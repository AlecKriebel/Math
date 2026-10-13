#!/usr/bin/env python3
"""Offline inventory, byte-integrity, metadata, and local-link checks.

This program does not prove mathematics, authenticate outside sources, verify
external web links, or supply a trusted signature. It performs explicit checks
under both ordinary Python and python -O. Python 3.9+; standard library only.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit


def fail(message):
    raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def relative_path(value):
    if not isinstance(value, str) or not value or '\\' in value:
        fail('Invalid manifest path')
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or '.' in path.parts or str(path) != value:
        fail('Unsafe or noncanonical manifest path: ' + value)
    return path


def verify(root, expected_manifest):
    if root.is_symlink() or not root.is_dir():
        fail('Reader root must be a real directory')
    root = root.resolve()
    manifest_file = root / 'MANIFEST.json'
    if manifest_file.is_symlink() or not manifest_file.is_file():
        fail('Missing regular MANIFEST.json')
    manifest_bytes = manifest_file.read_bytes()
    manifest_hash = sha(manifest_bytes)
    if expected_manifest is not None:
        if re.fullmatch(r'[0-9a-f]{64}', expected_manifest) is None:
            fail('Expected manifest hash must be 64 lowercase hex characters')
        if manifest_hash != expected_manifest:
            fail('Manifest hash differs from independently supplied expected value')
    manifest = read_json(manifest_file)
    if manifest.get('schema_version') != 1 or manifest.get('problem_id') != 30003527:
        fail('Wrong manifest schema or target')
    if manifest.get('self_excluded') != 'MANIFEST.json':
        fail('Manifest must explicitly exclude only its own bytes')
    records = manifest.get('files')
    if not isinstance(records, list) or not records:
        fail('Missing nonempty file inventory')
    listed = set()
    total = 0
    for record in records:
        if not isinstance(record, dict) or set(record) != {'path', 'bytes', 'sha256'}:
            fail('Malformed manifest record')
        name = record['path']
        relative_path(name)
        if name == 'MANIFEST.json' or name in listed:
            fail('Duplicate or self-referential inventory record: ' + name)
        if type(record['bytes']) is not int or record['bytes'] < 0:
            fail('Invalid byte count: ' + name)
        if not isinstance(record['sha256'], str) or re.fullmatch(r'[0-9a-f]{64}', record['sha256']) is None:
            fail('Invalid digest: ' + name)
        listed.add(name)
        file = root / name
        if file.is_symlink() or not file.is_file():
            fail('Missing regular file: ' + name)
        if root not in file.resolve().parents:
            fail('File escapes reader root: ' + name)
        data = file.read_bytes()
        if len(data) != record['bytes']:
            fail('Byte count mismatch: ' + name)
        if sha(data) != record['sha256']:
            fail('SHA-256 mismatch: ' + name)
        data.decode('utf-8')
        if file.suffix not in {'.md', '.json', '.py', '.patch'}:
            fail('Unexpected file type in reader: ' + name)
        total += len(data)
    actual = set()
    for file in root.rglob('*'):
        if file.is_symlink():
            fail('Symlink in reader: ' + file.relative_to(root).as_posix())
        if file.is_file():
            actual.add(file.relative_to(root).as_posix())
        elif not file.is_dir():
            fail('Unexpected nonregular filesystem entry: ' + file.relative_to(root).as_posix())
    if actual != listed | {'MANIFEST.json'}:
        fail('Exact inventory mismatch: missing=' + repr(sorted(listed - actual)) +
             '; unexpected=' + repr(sorted(actual - listed - {'MANIFEST.json'})))
    required = {'README.md', 'PROOF_INDEX.md', 'SOURCES.md', 'CORRECTIONS.md',
                'DISPOSITION.json', 'SOURCE_METADATA.json', 'ARTIFACT_PROVENANCE.json',
                'INTEGRITY.md', 'verify_reader.py',
                'proofs/ONE_DIMENSIONAL_ISOLATED_MOVABILITY_V2.md',
                'audits/DIMENSION_ONE_ACCEPTANCE.md',
                'audits/LEFT_CONTINUITY_ACCEPTANCE.md',
                'corrections/EMPTY_ENTRY_CORRECTION.patch'}
    if not required <= listed:
        fail('Missing required reader files: ' + repr(sorted(required - listed)))
    if any(PurePosixPath(name).name == 'ONE_DIMENSIONAL_ISOLATED_MOVABILITY.md' for name in listed):
        fail('Superseded uncorrected proof must not appear as a current public proof')
    disposition = read_json(root / 'DISPOSITION.json')
    expected = {'problem_id': 30003527, 'queue_row': 1767,
                'full_target_disposition': 'UNSOLVED', 'new_shared_substantive_passes': 5,
                'lifetime_substantive_count': 'unknown', 'continuation_search_budget': 'exhausted',
                'general_affirmative_proof_obtained': False,
                'all_enlargements_counterexample_obtained': False,
                'novelty_claim': False, 'worldwide_openness_certificate': False}
    for key, value in expected.items():
        if disposition.get(key) != value:
            fail('Wrong disposition value: ' + key)
    for name, digest in {
        'proofs/ONE_DIMENSIONAL_ISOLATED_MOVABILITY_V2.md': '5a325bc382d9094bd50e13b8a17fbdf8151b31e56dc58e3e32af9355f8a0ca1c',
        'audits/DIMENSION_ONE_ACCEPTANCE.md': '24df75398dda97da9038ee94bf33495fb8eb1efd7d257002130e6fff58d3da0a',
        'audits/LEFT_CONTINUITY_ACCEPTANCE.md': '9f4afc390b18e8b0e3a2f61e8826218442912ac883f78d7bd2e8f42afd076ed1',
        'corrections/EMPTY_ENTRY_CORRECTION.patch': '91ad5980bd093fccf4d0466e2a45963712308d2d9d39b64543cb6d49b1ded9b4'
    }.items():
        if sha((root / name).read_bytes()) != digest:
            fail('Pinned authored version mismatch: ' + name)
    provenance = read_json(root / 'ARTIFACT_PROVENANCE.json')
    seen = set()
    for record in provenance['files']:
        name = record['public_path']
        relative_path(name)
        if name in seen or name not in listed:
            fail('Duplicate or unlisted provenance file: ' + name)
        seen.add(name)
        data = (root / name).read_bytes()
        if len(data) != record['public_bytes'] or sha(data) != record['public_sha256']:
            fail('Provenance/public byte mismatch: ' + name)
        if record['transformation'] == 'byte-for-byte':
            if record['source_sha256'] != record['public_sha256'] or record['source_bytes'] != record['public_bytes']:
                fail('Invalid byte-for-byte provenance claim: ' + name)
    expected_authored = {name for name in listed if name.startswith(('proofs/', 'audits/', 'corrections/'))}
    if seen != expected_authored:
        fail('Authored provenance inventory is incomplete')
    if len([name for name in listed if name.startswith('proofs/')]) != 16:
        fail('Expected sixteen complete proof artifacts')
    if len([name for name in listed if name.startswith('audits/')]) != 11:
        fail('Expected eleven independent audit artifacts')
    local_links = 0
    for name in listed:
        file = root / name
        if file.suffix not in {'.md', '.json'}:
            continue
        text = file.read_text(encoding='utf-8')
        if file.suffix == '.md':
            for link in re.findall(r'(?<![\w])\[[^\]\n]+\]\(([^\s)]+)\)', text):
                split = urlsplit(link)
                if split.scheme or split.netloc or not split.path:
                    continue
                target = (file.parent / unquote(split.path)).resolve()
                if root not in target.parents or not target.is_file():
                    fail('Broken or escaping local link in ' + name + ': ' + link)
                local_links += 1
    sources = read_json(root / 'SOURCE_METADATA.json')['sources']
    for source in sources:
        if source.get('body_included') is not False:
            fail('Source-body inclusion flag must be false')
        if not source.get('public_url', '').startswith('https://'):
            fail('Source metadata needs a public HTTPS URL')
    print('PASS: {} inventoried files, {} bytes excluding manifest, {} local links.'.format(len(listed), total, local_links))
    print('Manifest SHA-256: ' + manifest_hash)
    print('Expected manifest hash externally pinned: ' + ('yes' if expected_manifest else 'no'))
    print('Byte integrity and recorded scope checked. Mathematical correctness was NOT verified by this program.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--expected-manifest-sha256')
    args = parser.parse_args()
    try:
        verify(args.root, args.expected_manifest_sha256)
    except (ValueError, OSError, UnicodeError, KeyError, TypeError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
