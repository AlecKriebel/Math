#!/usr/bin/env python3
"""Create and byte-verify a portable source ZIP. This never verifies a theorem.

Build products, dependency caches, Git metadata and font files are excluded.
Symlinks and probable credential files fail closed. Historical nested checksum
manifests are preserved; only the root manifest is regenerated.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OMIT_DIRS = {'.lake', '.git', '__pycache__'}
OMIT_SUFFIXES = {'.pyc', '.olean', '.ilean', '.o', '.a', '.so', '.dylib', '.dll', '.wasm'}
FONT_SUFFIXES = {'.ttf', '.otf', '.woff', '.woff2', '.eot', '.ttc', '.dfont'}
CREDENTIAL_SUFFIXES = {'.pem', '.key', '.p12', '.pfx'}


def valid_name(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and '..' not in p.parts and '\\' not in name and '\n' not in name and '\r' not in name and '\x00' not in name


def selected_files(root: Path) -> list[Path]:
    result = []
    for p in sorted(root.rglob('*')):
        rel = p.relative_to(root)
        if any(part in OMIT_DIRS for part in rel.parts):
            continue
        if p.is_symlink():
            raise ValueError(f'Refusing to package a symlink: {rel}')
        if not p.is_file():
            continue
        if not valid_name(rel.as_posix()):
            raise ValueError(f'Unsafe manifest filename: {rel}')
        if p.name == '.lean-run.lock':
            raise ValueError('A verification run is active; do not package a moving report set.')
        if p.suffix.lower() in CREDENTIAL_SUFFIXES or p.name in {'.netrc', 'id_rsa', 'id_ed25519', '.env'} or p.name.startswith('.env.'):
            raise ValueError(f'Probable credential file requires manual review: {rel}')
        if p.suffix.lower() in OMIT_SUFFIXES | FONT_SUFFIXES or rel.as_posix() == 'SHA256SUMS.txt':
            continue
        result.append(p)
    return result


def parse_manifest(content: str) -> dict[str, str]:
    expected = {}
    for line in content.splitlines():
        digest, name = line.split('  ', 1)
        if not valid_name(name) or name in expected or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError(f'Invalid or duplicate manifest entry: {name!r}')
        expected[name] = digest
    return expected


def verify_zip(path: Path) -> dict:
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if len(set(names)) != len(names):
            raise ValueError('Duplicate ZIP entry.')
        if z.testzip() is not None:
            raise ValueError('ZIP CRC failure.')
        for entry in z.infolist():
            if not valid_name(entry.filename) or not entry.filename.startswith('bell_lean/'):
                raise ValueError(f'Unsafe archive entry: {entry.filename}')
            if stat.S_ISLNK(entry.external_attr >> 16):
                raise ValueError('ZIP symlink not permitted.')
        manifest = parse_manifest(z.read('bell_lean/SHA256SUMS.txt').decode())
        if set(names) != {'bell_lean/'+n for n in manifest} | {'bell_lean/SHA256SUMS.txt'}:
            raise ValueError('ZIP and root manifest differ in file membership.')
        for name, digest in manifest.items():
            if hashlib.sha256(z.read('bell_lean/'+name)).hexdigest() != digest:
                raise ValueError(f'ZIP checksum mismatch: {name}')
    return {'file_count': len(names), 'zip_crc_and_embedded_hashes_checked': True}


def make_package(root: Path, output: Path) -> dict:
    root = root.resolve(); output = output.expanduser().resolve()
    if output == root or root in output.parents:
        raise ValueError('Write the archive outside the source root.')
    paths = selected_files(root)
    payloads = {p.relative_to(root).as_posix(): p.read_bytes() for p in paths}
    checks = ''.join(hashlib.sha256(b).hexdigest()+'  '+n+'\n' for n,b in sorted(payloads.items()))
    (root/'SHA256SUMS.txt').write_text(checks)
    payloads['SHA256SUMS.txt'] = checks.encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_suffix(output.suffix+'.tmp')
    try:
        with zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for name, data in sorted(payloads.items()):
                entry = zipfile.ZipInfo('bell_lean/'+name, date_time=(2026,9,10,0,0,0))
                entry.create_system = 3
                entry.external_attr = (stat.S_IFREG | ((root/name).stat().st_mode & 0o777)) << 16
                entry.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(entry, data, compresslevel=9)
        verified = verify_zip(temp)
        for name, data in payloads.items():
            if (root/name).read_bytes() != data:
                raise ValueError(f'Source changed while packaging: {name}')
        temp.replace(output)
    finally:
        temp.unlink(missing_ok=True)
    report = {'archive': str(output), 'bytes': output.stat().st_size,
              'sha256': hashlib.sha256(output.read_bytes()).hexdigest(), **verified,
              'lean_kernel_checked_by_packaging': False,
              'note': 'Integrity of preserved bytes only; consult the separately generated verification run receipt.'}
    output.with_suffix('.receipt.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main() -> None:
    output=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'bell_lean_preflight_20260910.zip'
    print(json.dumps(make_package(ROOT,output),indent=2))

if __name__ == '__main__':
    main()
