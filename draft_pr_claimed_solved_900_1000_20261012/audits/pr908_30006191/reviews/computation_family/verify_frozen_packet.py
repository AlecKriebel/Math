#!/usr/bin/env python3
"""Portable stdlib, closed-allowlist verifier for the authenticated PR908 packet.

The trust anchor is an externally authenticated Git head and PACKAGE hash,
embedded here. SHA-256 hashes are consistency fingerprints, not signatures.
Run against packet itself, a standalone original_packet, or original/fullprefix.
No source inputs are opened and no Python assert is used.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys

HEAD = 'a35667b1bb0bafed69916709997a4684223ecc93'
PACKAGE = '828280cc131c38e1f651b48b655dff177f880ba3505bba54e049510d81827795'
PROOF = '2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350'
PREFIX = ('unsolved_math_prioritization', 'attempts', '30006191', 'bounded_region_v2')
# These pins must agree with the independently supplied, authenticated package.
NESTED = {'author/AUTHOR_MANIFEST.json': 'd6a0862cbf2f6500cc5fd7ee2239e0e8a2c5864c9d09a6cd9a13b1b4f99176ef',
          'audit_a/AUDIT_MANIFEST.json': '75c4fdb635d14131759bc47d779c95079c719373d7f9305a649f9f60bf26bfc4',
          'audit_b/AUDIT_MANIFEST.json': '180bee30c70c810f8f92984fd4604ba7fdc25201ff2e579ed99f686935b1a6fd'}
EXPECTED_FILES = frozenset({
    'PACKAGE_MANIFEST.json', 'PUBLICATION_VERIFICATION.json', 'README.md', 'verify_package.py',
    'author/AUTHOR_MANIFEST.json', 'author/BOUNDED_REGION_PROOF.md', 'author/CHECK_RESULTS.json',
    'author/README.md', 'author/RESEARCH_LOG.md', 'author/SOURCE_MANIFEST.json', 'author/verify.py',
    'audit_a/ACCEPTANCE.json', 'audit_a/AUDIT_MANIFEST.json', 'audit_a/AUTHOR_REPLAY.json',
    'audit_a/INDEPENDENT_AUDIT.md', 'audit_a/INDEPENDENT_CHECK_RESULTS.json',
    'audit_a/INDEPENDENT_SUMMARY.json', 'audit_a/INTEGRITY_TAMPER_TESTS.json', 'audit_a/independent_checks.py',
    'audit_b/AUDIT_MANIFEST.json', 'audit_b/AUDIT_REPORT.md', 'audit_b/AUTHOR_RESULTS.json',
    'audit_b/INDEPENDENT_RESULTS.json', 'audit_b/INPUT_FINGERPRINTS.json',
    'audit_b/SOURCE_INSPECTION.json', 'audit_b/independent_checks.py'})
EXPECTED_DIRS = frozenset({'author', 'audit_a', 'audit_b'})


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strict_json(data, label):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key in ' + label)
            result[key] = value
        return result
    def invalid_constant(value):
        raise ValueError('nonfinite JSON constant in ' + label + ': ' + value)
    return json.loads(data.decode('utf-8'), object_pairs_hook=pairs, parse_constant=invalid_constant)


def plain_path(path, directory=False):
    info = path.lstat()
    require(stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode),
            'nonregular ' + ('directory' if directory else 'file') + ': ' + str(path))
    return info


def regular_read(path):
    # lstat rejects FIFOs/sockets/symlinks before opening. O_NONBLOCK prevents a
    # raced FIFO from blocking; O_NOFOLLOW prevents a raced final symlink.
    before = plain_path(path)
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    descriptor = os.open(path, flags)
    try:
        during = os.fstat(descriptor)
        require(stat.S_ISREG(during.st_mode), 'raced nonregular file: ' + str(path))
        require((before.st_dev, before.st_ino) == (during.st_dev, during.st_ino), 'raced identity: ' + str(path))
        with os.fdopen(descriptor, 'rb', closefd=False) as handle:
            data = handle.read()
        after = path.lstat()
        require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
                (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), 'raced bytes: ' + str(path))
        return data
    finally:
        os.close(descriptor)


def fingerprint(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def validate_record(name, record):
    require(type(name) is str and name != '', 'invalid manifest key')
    relative = PurePosixPath(name)
    require(not relative.is_absolute() and str(relative) == name and '..' not in relative.parts
            and '\\' not in name, 'unsafe or noncanonical manifest path: ' + name)
    require(type(record) is dict and set(record) == {'bytes', 'sha256'}, 'invalid fingerprint record: ' + name)
    require(type(record['bytes']) is int and record['bytes'] >= 0, 'invalid byte count: ' + name)
    digest = record['sha256']
    require(type(digest) is str and len(digest) == 64 and all(c in '0123456789abcdef' for c in digest),
            'invalid SHA-256: ' + name)


def select_root(raw):
    require('..' not in Path(raw).parts, 'parent traversal in supplied root')
    root = Path(raw).absolute()
    # Check each supplied absolute path component before following it.
    current = Path(root.anchor)
    for part in root.parts[1:]:
        current = current / part
        plain_path(current, directory=True)
    if (root / 'PACKAGE_MANIFEST.json').exists() or (root / 'PACKAGE_MANIFEST.json').is_symlink():
        return root, 'direct_packet'
    options = [(root / 'original_packet', 'standalone_original_packet'),
               (root.joinpath(*PREFIX), 'full_prefix'),
               (root / 'original').joinpath(*PREFIX)]
    options[-1] = (options[-1], 'audit_original_full_prefix')
    selected = []
    for candidate, layout in options:
        if candidate.exists() or candidate.is_symlink():
            selected.append((candidate, layout))
    require(len(selected) == 1, 'missing or ambiguous packet layout')
    candidate, layout = selected[0]
    for relative_component in candidate.relative_to(root).parts:
        root = root / relative_component
        plain_path(root, directory=True)
    return candidate, layout


def inventory(root):
    files, directories = set(), set()
    def visit(folder):
        plain_path(folder, directory=True)
        for child in folder.iterdir():
            mode = child.lstat().st_mode
            rel = child.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                directories.add(rel)
                require(rel in EXPECTED_DIRS, 'unexpected package directory: ' + rel)
                visit(child)
            else:
                require(stat.S_ISREG(mode), 'special entry or symlink rejected: ' + rel)
                files.add(rel)
    visit(root)
    require(files == EXPECTED_FILES, 'closed file allowlist mismatch: ' + repr(sorted(files ^ EXPECTED_FILES)))
    require(directories == EXPECTED_DIRS, 'closed directory allowlist mismatch')
    return files


def verify(root_arg, expected_head=HEAD, expected_package=PACKAGE, expected_proof=PROOF):
    require(expected_head == HEAD, 'external HEAD anchor mismatch')
    require(expected_package == PACKAGE, 'external PACKAGE anchor mismatch')
    require(expected_proof == PROOF, 'external proof anchor mismatch')
    root, layout = select_root(root_arg)
    inventory(root)
    # External fixed anchor is checked before trusting any manifest fields.
    package_data = regular_read(root / 'PACKAGE_MANIFEST.json')
    require(fingerprint(package_data)['sha256'] == PACKAGE, 'authenticated PACKAGE fingerprint mismatch')
    package = strict_json(package_data, 'PACKAGE_MANIFEST.json')
    require(type(package) is dict and set(package) == {'problem_id', 'revision', 'self_excluded', 'files'}, 'invalid package schema')
    require(type(package['problem_id']) is int and package['problem_id'] == 30006191, 'invalid problem id')
    require(type(package['revision']) is int and package['revision'] == 2, 'invalid revision')
    require(package['self_excluded'] == 'PACKAGE_MANIFEST.json', 'invalid package self exclusion')
    require(type(package['files']) is dict and set(package['files']) == EXPECTED_FILES - {'PACKAGE_MANIFEST.json'}, 'invalid manifest file allowlist')
    records = {'PACKAGE_MANIFEST.json': fingerprint(package_data)}
    for name, expected in package['files'].items():
        validate_record(name, expected)
        actual = fingerprint(regular_read(root / name))
        require(actual == expected, 'frozen bytes mismatch: ' + name)
        records[name] = actual
    require(records['author/BOUNDED_REGION_PROOF.md'] == {'bytes': 12771, 'sha256': PROOF}, 'external proof fingerprint mismatch')
    nested_results = {}
    for relative, pinned_digest in NESTED.items():
        require(records[relative]['sha256'] == pinned_digest, 'nested external pin mismatch: ' + relative)
        nested = strict_json(regular_read(root / relative), relative)
        folder, filename = relative.split('/')
        require(type(nested) is dict and type(nested.get('files')) is dict, 'invalid nested manifest schema: ' + relative)
        require(nested.get('self_excluded') == filename, 'invalid nested self exclusion: ' + relative)
        require(type(nested.get('problem_id')) is int and nested['problem_id'] == 30006191, 'invalid nested problem id')
        expected_names = {name.split('/')[1] for name in EXPECTED_FILES if name.startswith(folder + '/')}
        require(set(nested['files']) | {filename} == expected_names, 'nested allowlist mismatch: ' + relative)
        for name, expected in nested['files'].items():
            validate_record(name, expected)
            require('/' not in name, 'nested path outside flat folder')
            require(records[folder + '/' + name] == expected, 'nested fingerprint mismatch: ' + relative + '/' + name)
        nested_results[relative] = {'status': 'PASS', 'checked_file_count': len(nested['files']), 'sha256': pinned_digest}
    inventory(root)
    return {'status': 'PASS', 'layout': layout, 'file_count': len(records),
            'authenticated_external_head': HEAD, 'package_sha256': PACKAGE, 'proof_sha256': PROOF,
            'nested_manifest_checks': nested_results, 'files': dict(sorted(records.items())),
            'source_bytes_verified': False,
            'trust_boundary': 'The supplied external head/package/proof pins must be authenticated independently. Hashes are fingerprints, not signatures. This is a byte/inventory verifier, not a proof validator. Concurrent ancestor-directory renaming is outside the threat model; final-entry races are guarded.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--expected-head', default=HEAD)
    parser.add_argument('--expected-package', default=PACKAGE)
    parser.add_argument('--expected-proof', default=PROOF)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        result = verify(args.root, args.expected_head, args.expected_package, args.expected_proof)
    except (ValueError, OSError, TypeError, KeyError, json.JSONDecodeError) as error:
        print(json.dumps({'status': 'REJECT', 'error': str(error)}, sort_keys=True))
        return 1
    encoded = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(encoded)
    print(encoded, end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
