#!/usr/bin/env python3
"""Offline frozen-input integrity verification; no mathematical proof certificate."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    def no_constant(value):
        raise RuntimeError('Nonfinite JSON: ' + value)
    def no_duplicates(pairs):
        out = {}
        for key, value in pairs:
            require(key not in out, 'Duplicate JSON key')
            out[key] = value
        return out
    return json.loads(path.read_text(), object_pairs_hook=no_duplicates,
                      parse_constant=no_constant)


def safe_file(root, relative):
    p = Path(relative)
    require(not p.is_absolute() and '..' not in p.parts and p.parts,
            'Unsafe relative path')
    for index in range(1, len(p.parts) + 1):
        require(not root.joinpath(*p.parts[:index]).is_symlink(), 'Symlink')
    result = root / p
    require(result.is_file(), 'Missing file: ' + str(p))
    return result


def verify_map(root, entries):
    require(type(entries) is list, 'Bad manifest entry list')
    seen = set()
    for item in entries:
        name = item['path']
        require(name not in seen, 'Repeated manifest path')
        seen.add(name)
        raw = safe_file(root, name).read_bytes()
        require(type(item['bytes']) is int and item['bytes'] == len(raw),
                'Byte count mismatch: ' + name)
        require(item['sha256'] == digest(raw), 'SHA mismatch: ' + name)
    return seen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expect-public-sha256', required=True)
    parser.add_argument('--with-private', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest_path = safe_file(root, 'OUTPUT_MANIFEST.json')
    require(digest(manifest_path.read_bytes()) == args.expect_public_sha256,
            'Externally anchored public manifest differs')
    manifest = load(manifest_path)
    public_names = verify_map(root, manifest['files'])
    actual_public = {p.name for p in root.iterdir() if p.is_file()}
    require(actual_public == public_names | {'OUTPUT_MANIFEST.json'},
            'Public file closure differs')
    require({p.name for p in root.iterdir() if p.is_dir()} <= {'private'},
            'Unexpected directory')
    check = load(root / 'CHECK.json')
    require(check['pr'] == 1114 and
            check['head'] == 'e1a11feef98ed0fde22375c983e30b72b268d265',
            'Wrong claim binding')
    require(check['verdict'] == 'prior_published_standard_consequence' and
            check['new_resolution_publication_eligible'] is False and
            check['formal_proof_certificate'] is False and
            check['global_firstness_established'] is False,
            'Verdict/scope mismatch')
    private_entries = load(root / 'PRIVATE_EVIDENCE_MANIFEST.json')['files']
    if args.with_private:
        expected = verify_map(root, private_entries)
        actual = set()
        for p in (root / 'private').rglob('*'):
            require(not p.is_symlink(), 'Private symlink')
            if p.is_file():
                actual.add(p.relative_to(root).as_posix())
        require(actual == expected, 'Private file closure differs')
        pins = load(root / 'private/head_bindings.json')
        require(pins['head'] == check['head'] and len(pins['files']) == 8 and
                pins['no_QUEUE_diff'] is True, 'Wrong actual PR input inventory')
        for item in pins['files']:
            raw = safe_file(root, item['retained']).read_bytes()
            require(len(raw) == item['bytes'] and digest(raw) == item['sha256'],
                    'Pinned PR bytes differ')
            git_sha = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
            require(git_sha == item['git_blob'], 'Pinned Git blob differs')
        scope = load(root / 'private/submitted_STATUS.json')
        require(scope['full_resolution'] is True and scope['novelty_claim'] is False,
                'Submitted scope changed')
        require(load(root / 'private/parent_PR1114_PUBLICATION_LEADS.json')['matches'] == [],
                'Parent narrow duplicate context differs')
        fetches = load(root / 'private/source_fetches.json')
        require(len(fetches) == 5 and all(x.get('status') == 200 for x in fetches),
                'Fresh direct source fetch missing')
        for source in fetches:
            raw = safe_file(root, source['path']).read_bytes()
            require(len(raw) == source['bytes'] and digest(raw) == source['sha256'],
                    'Direct source bytes mismatch')
        hkm = load(root / 'private/hkm_fetch.json')
        require(hkm['status'] == 200 and hkm['sha256'] ==
                digest((root / 'private/hkm_published.pdf').read_bytes()),
                'Publisher correspondence source differs')
    result = {
        'status': 'pass', 'pr': 1114, 'public_payload_files': len(public_names),
        'private_payload_files': len(private_entries) if args.with_private else None,
        'with_private': args.with_private,
        'verdict': check['verdict'],
        'certificate_scope': 'Frozen artifact integrity and exact scope binding only; not a formal proof or worldwide priority certificate',
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
