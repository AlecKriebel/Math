#!/usr/bin/env python3
"""Check a closed PR97 payload or its ZIP without altering/extracting it."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

MANIFEST = 'MANIFEST.json'
MAX_BYTES = 16 * 1024 * 1024

def reject(message):
    raise ValueError(message)

def member_name(name):
    if not isinstance(name, str) or not name or '\\' in name or '\x00' in name:
        reject('Unsafe member name')
    if name.startswith('/') or re.match(r'^[A-Za-z]:', name):
        reject('Absolute member name')
    parts = name.split('/')
    if any(part in ('', '.', '..') for part in parts):
        reject('Empty, dot, or traversing member component')
    if str(PurePosixPath(name)) != name:
        reject('Noncanonical member path')
    return name

def no_ancestor_symlinks(path):
    raw = Path(path)
    if '..' in raw.parts:
        reject('Traversing root argument')
    absolute = raw.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current = current/part
        if current.is_symlink():
            reject('Symlink in root or ancestor: '+str(current))
    return absolute

def manifest_entries(data):
    decoded = json.loads(data)
    if decoded.get('schema') != 'pr97-portable-payload/v1':
        reject('Unexpected manifest schema')
    entries = decoded.get('files')
    if not isinstance(entries, list) or not entries:
        reject('Missing file inventory')
    expected = {}
    for item in entries:
        if not isinstance(item, dict) or set(item) != {'path', 'sha256', 'bytes'}:
            reject('Malformed file entry')
        name = member_name(item['path'])
        if name == MANIFEST or name in expected:
            reject('Self-reference or duplicate manifest entry')
        digest, size = item['sha256'], item['bytes']
        if not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest):
            reject('Malformed digest')
        if not isinstance(size, int) or isinstance(size, bool) or not 0 <= size <= MAX_BYTES:
            reject('Malformed size')
        expected[name] = item
    if sum(e['bytes'] for e in expected.values()) > MAX_BYTES:
        reject('Excessive declared payload')
    return expected

def check_bytes(name, data, entry):
    if len(data) != entry['bytes'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
        reject('Digest/size mismatch: '+name)

def check_root(path):
    root = no_ancestor_symlinks(path)
    if not root.is_dir():
        reject('Root is not a directory')
    actual = {}
    for parent, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            candidate = Path(parent)/name
            if candidate.is_symlink():
                reject('Payload symlink: '+str(candidate))
            if name in files:
                if not stat.S_ISREG(candidate.stat().st_mode):
                    reject('Nonregular payload entry')
                key = member_name(candidate.relative_to(root).as_posix())
                actual[key] = candidate
    if MANIFEST not in actual:
        reject('Manifest missing')
    expected = manifest_entries(actual[MANIFEST].read_bytes())
    if set(actual) != set(expected) | {MANIFEST}:
        reject('Payload closure mismatch')
    for name, entry in expected.items():
        check_bytes(name, actual[name].read_bytes(), entry)
    return len(expected)

def check_zip(path):
    archive = no_ancestor_symlinks(path)
    with zipfile.ZipFile(archive) as z:
        actual = {}
        total = 0
        for info in z.infolist():
            name = member_name(info.filename)
            if name in actual:
                reject('Duplicate ZIP member')
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode):
                reject('ZIP symlink')
            if info.is_dir() or (stat.S_IFMT(mode) not in (0, stat.S_IFREG)):
                reject('Nonregular ZIP member')
            if info.flag_bits & 1 or info.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                reject('Encrypted or unsupported ZIP entry')
            total += info.file_size
            if info.file_size > MAX_BYTES or total > MAX_BYTES:
                reject('Excessive ZIP payload')
            actual[name] = info
        if MANIFEST not in actual:
            reject('ZIP manifest missing')
        expected = manifest_entries(z.read(actual[MANIFEST]))
        if set(actual) != set(expected) | {MANIFEST}:
            reject('ZIP closure mismatch')
        for name, entry in expected.items():
            check_bytes(name, z.read(actual[name]), entry)
        return len(expected)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--root')
    choice.add_argument('--zip')
    args = parser.parse_args()
    count = check_root(args.root) if args.root else check_zip(args.zip)
    print(json.dumps({'status': 'PASS', 'payload_files': count,
                      'scope': 'Digest, size, closure and safe-path integrity only; no theorem/priority acceptance.'}))

if __name__ == '__main__':
    main()
