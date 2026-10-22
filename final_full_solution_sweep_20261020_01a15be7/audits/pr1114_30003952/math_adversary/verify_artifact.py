#!/usr/bin/env python3
"""Read-only externally anchored byte-custody check, not a truth certificate."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re


def fail(message):
    raise ValueError(message)


def read_json(data):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                fail('duplicate JSON key')
            out[key] = value
        return out
    return json.loads(data, object_pairs_hook=pairs,
                      parse_constant=lambda _: fail('nonfinite JSON number'))


def safe_name(name):
    if not isinstance(name, str) or not name or '\\' in name or '\x00' in name:
        fail('invalid path')
    p = PurePosixPath(name)
    if p.is_absolute() or any(x in ('', '.', '..') for x in name.split('/')):
        fail('unsafe path')
    if str(p) != name:
        fail('noncanonical path')
    return name


def payload(root, item):
    if not isinstance(item, dict) or set(item) != {'path', 'bytes', 'sha256'}:
        fail('invalid payload schema')
    name = safe_name(item['path'])
    if type(item['bytes']) is not int or item['bytes'] < 0:
        fail('invalid byte count')
    if not isinstance(item['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', item['sha256']):
        fail('invalid digest')
    p = root / name
    for ancestor in (p, *p.parents):
        if ancestor.is_symlink():
            fail('symlink input')
        if ancestor == root:
            break
    if not p.is_file() or not p.resolve().is_relative_to(root.resolve()):
        fail('missing or escaped payload')
    data = p.read_bytes()
    if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
        fail('payload identity mismatch: ' + name)
    return name


def inventory(root, exclude):
    out = set()
    for p in root.rglob('*'):
        relative = p.relative_to(root)
        if relative.parts[0] in exclude:
            continue
        if p.is_symlink():
            fail('unlisted symlink')
        if p.is_file():
            out.add(relative.as_posix())
        elif not p.is_dir():
            fail('special filesystem entry')
    return out


def records(root, rows):
    if not isinstance(rows, list):
        fail('records not list')
    names = [payload(root, item) for item in rows]
    if len(set(names)) != len(names):
        fail('duplicate payload')
    return set(names)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--expect-manifest-sha256', required=True)
    parser.add_argument('--with-private', action='store_true')
    args = parser.parse_args()
    if not re.fullmatch('[0-9a-f]{64}', args.expect_manifest_sha256):
        fail('bad external anchor')
    root = args.root.absolute()
    manifest = root / 'MANIFEST.json'
    if manifest.is_symlink():
        fail('symlink manifest')
    data = manifest.read_bytes()
    if hashlib.sha256(data).hexdigest() != args.expect_manifest_sha256:
        fail('external manifest anchor mismatch')
    m = read_json(data)
    if not isinstance(m, dict) or set(m) != {'schema', 'records', 'private_manifest'} or type(m['schema']) is not int or m['schema'] != 1:
        fail('manifest schema')
    names = records(root, m['records'])
    if 'MANIFEST.json' in names or any(x.startswith('private/') for x in names):
        fail('invalid public payload class')
    if inventory(root, {'private', '__pycache__'}) != names | {'MANIFEST.json'}:
        fail('public inventory not closed')
    private_count = None
    if args.with_private:
        private_name = payload(root, m['private_manifest'])
        if private_name != 'private/INPUT_MANIFEST.json':
            fail('private manifest locator')
        pm = read_json((root / private_name).read_bytes())
        if not isinstance(pm, dict) or set(pm) != {'schema', 'records'} or type(pm['schema']) is not int or pm['schema'] != 1:
            fail('private manifest schema')
        private_root = root / 'private'
        private_names = records(private_root, pm['records'])
        if 'INPUT_MANIFEST.json' in private_names:
            fail('private self reference')
        if inventory(private_root, set()) != private_names | {'INPUT_MANIFEST.json'}:
            fail('private inventory not closed')
        private_count = len(private_names)
    print(json.dumps({'status':'pass', 'public_payloads':len(names),
                      'private_payloads':private_count,
                      'manifest_sha256':args.expect_manifest_sha256,
                      'scope':'Externally anchored closed byte custody only; not proof, priority or publication acceptance.'},
                     sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
