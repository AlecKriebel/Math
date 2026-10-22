#!/usr/bin/env python3
"""Authenticate this audit and, optionally, the exact accepted author packet."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fail(message):
    raise SystemExit('FAIL: ' + message)


def verify_inventory(root, expected_hash, label):
    manifest_path = root / 'MANIFEST.json'
    raw = manifest_path.read_bytes()
    if digest(raw) != expected_hash:
        fail(label + ' manifest does not match the independently supplied hash')
    manifest = json.loads(raw)
    expected = set(manifest['files'])
    actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    if actual != expected | {'MANIFEST.json'}:
        fail(label + ' inventory differs from the frozen manifest')
    for name, record in manifest['files'].items():
        path = Path(name)
        if path.is_absolute() or '..' in path.parts:
            fail(label + ' manifest contains an unsafe path')
        data = (root / path).read_bytes()
        if len(data) != record['bytes'] or digest(data) != record['sha256']:
            fail(label + ' file mismatch: ' + name)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-manifest', required=True)
    parser.add_argument('--author-dir', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = verify_inventory(root, args.expected_manifest, 'audit')
    acceptance = json.loads((root / 'ACCEPTANCE.json').read_text())
    binding = acceptance['accepted_author_packet']
    if binding != manifest['accepted_author_packet']:
        fail('acceptance and audit manifest bind different author packets')
    proof = binding['proof']
    if args.author_dir:
        author = args.author_dir.resolve()
        verify_inventory(author, binding['manifest']['sha256'], 'author')
        for name, record in [('MANIFEST.json', binding['manifest']), ('PROOF.md', proof)]:
            raw = (author / name).read_bytes()
            if len(raw) != record['bytes'] or digest(raw) != record['sha256']:
                fail('author binding mismatch: ' + name)
    print(json.dumps({
        'status': 'PASS',
        'audit_files': len(manifest['files']),
        'audit_manifest_sha256': args.expected_manifest,
        'accepted_author_manifest_sha256': binding['manifest']['sha256'],
        'accepted_proof_sha256': proof['sha256'],
        'author_packet_verified': bool(args.author_dir),
        'meaning': 'Byte integrity and scope binding only; mathematical acceptance is in FULL_REPORT.md.'
    }, indent=2))


if __name__ == '__main__':
    main()
