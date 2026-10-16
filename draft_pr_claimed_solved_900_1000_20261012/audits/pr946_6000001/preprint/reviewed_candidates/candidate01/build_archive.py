#!/usr/bin/env python3
"""Build/check the explicitly allowlisted PR946 source and verification archive.

This is a transport check, not a proof checker. The extracted package has its
own pinned verifier. No external application or publication action is used.
"""
import sys
if not (sys.flags.isolated or getattr(sys.flags, 'safe_path', False)):
    raise SystemExit('Use python -I -B so source-directory files cannot shadow the standard library')
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVE = 'global_hessian_verification.zip'
MANIFEST = 'ARCHIVE_MANIFEST.json'
EXTRAS = (
    'research_note.tex', 'research_note.pdf', 'README.md',
    'zenodo-deposit.json', 'PR_DESCRIPTION.md', 'AUTHORING_NOTES.md', 'build_archive.py',
    'PACKAGE_REPLAY_normal.json', 'PACKAGE_REPLAY_O.json',
    'PACKAGE_REPLAY_OO.json', 'PACKAGE_REPLAY_env2.json',
)
MAX_FILE = 32 * 1024 * 1024
MAX_TOTAL = 96 * 1024 * 1024


def digest(data):
    return hashlib.sha256(data).hexdigest()


def name_checked(name):
    if (type(name) is not str or not name or '\\' in name or
            '\x00' in name or '\n' in name or '\t' in name or
            PurePosixPath(name).as_posix() != name or
            any(p in ('', '.', '..') for p in name.split('/')) or
            PurePosixPath(name).is_absolute()):
        raise ValueError('Noncanonical member name')
    return name


def regular_bytes(name, cap=MAX_FILE):
    name_checked(name)
    cur = ROOT
    for part in name.split('/')[:-1]:
        cur = cur / part
        if not stat.S_ISDIR(cur.lstat().st_mode):
            raise ValueError('Non-directory or symlink ancestor: ' + name)
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    fd = os.open(ROOT / name, flags)
    try:
        mode = os.fstat(fd).st_mode
        if not stat.S_ISREG(mode) or stat.S_IMODE(mode) != 0o644:
            raise ValueError('Expected regular0644 file: ' + name)
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            data = stream.read(cap + 1)
        if len(data) > cap:
            raise ValueError('Oversized file: ' + name)
        return data
    finally:
        os.close(fd)


def fingerprint(data):
    return {'bytes': len(data), 'sha256': digest(data)}


def collect(package_pin):
    raw = regular_bytes('package/PACKAGE_MANIFEST.json')
    if digest(raw) != package_pin:
        raise ValueError('Package manifest external pin mismatch')
    package = json.loads(raw)
    if package.get('schema') != 'pr946-closed-verification-package-v1':
        raise ValueError('Package schema')
    files = package['files']
    if type(files) is not dict or not files:
        raise ValueError('Missing package file map')
    expected = set(files) | {'PACKAGE_MANIFEST.json'}
    actual = set()
    for base, dirs, names in os.walk(ROOT / 'package', followlinks=False):
        for name in dirs:
            if not stat.S_ISDIR((Path(base) / name).lstat().st_mode):
                raise ValueError('Non-directory package entry')
        for name in names:
            actual.add((Path(base) / name).relative_to(ROOT / 'package').as_posix())
    if actual != expected:
        raise ValueError('Package file inventory mismatch')
    result = {'package/PACKAGE_MANIFEST.json': raw}
    for name, pin in files.items():
        name_checked(name)
        data = regular_bytes('package/' + name)
        if (type(pin) is not dict or type(pin.get('bytes')) is not int or
                pin['bytes'] != len(data) or pin.get('sha256') != digest(data) or
                pin.get('mode') != '0644'):
            raise ValueError('Package payload mismatch: ' + name)
        result['package/' + name] = data
    for name in EXTRAS:
        result[name] = regular_bytes(name)
    if not result['research_note.pdf'].startswith(b'%PDF-'):
        raise ValueError('Paper is not a PDF')
    if sum(map(len, result.values())) > MAX_TOTAL:
        raise ValueError('Archive expanded size cap exceeded')
    return result


def check_archive(payloads, manifest_bytes):
    archive_bytes = regular_bytes(ARCHIVE, MAX_TOTAL)
    expected = dict(payloads)
    expected[MANIFEST] = manifest_bytes
    with zipfile.ZipFile(io.BytesIO(archive_bytes), 'r') as archive:
        entries = archive.infolist()
        if len(entries) != len(expected) or {x.filename for x in entries} != set(expected):
            raise ValueError('Archive inventory/duplicate mismatch')
        for info in entries:
            name_checked(info.filename)
            data = expected[info.filename]
            if (info.create_system != 3 or info.external_attr >> 16 != 0o100644 or
                    info.is_dir() or info.flag_bits & 1 or info.file_size != len(data) or
                    info.file_size > MAX_FILE):
                raise ValueError('Archive member mode/size/encryption mismatch')
            with archive.open(info, 'r') as source:
                extracted = source.read(len(data) + 1)
            if extracted != data:
                raise ValueError('Archive member bytes mismatch')
    return {'status': 'PASS', 'pr': 946, 'problem_id': '6000001',
            'archive_sha256': digest(archive_bytes),
            'archive_manifest_sha256': digest(manifest_bytes),
            'archive_members': len(expected),
            'expanded_payload_bytes': sum(map(len, expected.values())),
            'original_byte_identity': 'Package payloads match externally pinned closed inventory',
            'scope': 'Exact transport only; universal proof and source priority separate'}


def main():
    if not __debug__:
        raise SystemExit('Use nonoptimized Python for the archive builder/checker')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--package-manifest-sha256', required=True)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    if len(args.package_manifest_sha256) != 64 or any(
            x not in '0123456789abcdef' for x in args.package_manifest_sha256):
        raise ValueError('Invalid external package pin')
    payloads = collect(args.package_manifest_sha256)
    manifest_bytes = (json.dumps({'schema': 'pr946-outer-archive-v1',
                                'files': {n: fingerprint(b) for n, b in sorted(payloads.items())}},
                               indent=2) + '\n').encode('utf-8')
    if args.check:
        if regular_bytes(MANIFEST) != manifest_bytes:
            raise ValueError('Outer manifest differs from current frozen inputs')
    else:
        if (ROOT / ARCHIVE).exists() or (ROOT / MANIFEST).exists():
            raise ValueError('Preserve the existing candidate before rebuilding')
        (ROOT / MANIFEST).write_bytes(manifest_bytes)
        with zipfile.ZipFile(ROOT / ARCHIVE, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, data in sorted({**payloads, MANIFEST: manifest_bytes}.items()):
                info = zipfile.ZipInfo(name, date_time=(2026, 10, 15, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, data)
        os.chmod(ROOT / ARCHIVE, 0o644)
        os.chmod(ROOT / MANIFEST, 0o644)
    print(json.dumps(check_archive(payloads, manifest_bytes), indent=2))


if __name__ == '__main__':
    main()
