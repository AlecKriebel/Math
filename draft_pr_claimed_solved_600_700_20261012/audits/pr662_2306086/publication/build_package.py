#!/usr/bin/env python3
"""Deterministically package the exact PR662 authored allowlist.

This builder runs in the audit working layout (publication/ beside native/ and
reviews/), not from an extracted release. It does not execute mathematical code.
The offline verifier is verify_package.py. No network, Git or cloud access.
"""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import stat
import tempfile
import zipfile

P = Path(__file__).absolute().parent
A = P.parent
OUTPUT = 'real_schlicht_verification.zip'
RECEIPT = 'PACKAGE_BUILD_RECEIPT.json'


def main():
    verifier_path = P / 'verify_package.py'
    if A.is_symlink() or P.is_symlink() or not stat.S_ISREG(verifier_path.lstat().st_mode):
        raise ValueError('linked or nonregular verifier input')
    verifier_bytes = verifier_path.read_bytes()
    # Run this exact captured verifier rather than importing cached bytecode.
    namespace = {'__file__': str(P / 'verify_package.py'), '__name__': 'package_build_checks'}
    exec(compile(verifier_bytes, str(P / 'verify_package.py'), 'exec'), namespace)
    read = namespace['read_regular']; sha = namespace['digest']; need = namespace['need']
    snapshot = namespace['json_data'](read(A, 'SCOPE_AND_SNAPSHOT.json'))
    need(namespace['inventory'](A / 'native') == set(namespace['native_bindings'](snapshot)),
         'exact original native input inventory')
    mapping = {}
    for name in namespace['PUBLICATION_FILES']:
        mapping[name] = P / ('PACKAGE_README.md' if name == 'README.md' else name)
    for name in namespace['ROOT_FILES']:
        mapping[name] = A / name
    for family, names in namespace['REVIEW_FILES'].items():
        for name in names:
            relative = 'reviews/' + family + '/' + name
            mapping[relative] = A / relative
    for name in namespace['native_bindings'](snapshot):
        mapping['native/' + name] = A / 'native' / name
    payload = {name: read(A, path.relative_to(A).as_posix()) for name, path in mapping.items()}
    need(payload['verify_package.py'] == verifier_bytes, 'verifier changed while loading')
    namespace['inspect_payload'](payload)
    entries = [{'path': name, 'bytes': len(data), 'sha256': sha(data)}
               for name, data in sorted(payload.items())]
    manifest = {'schema': 1, 'problem_id': '2306086', 'original_head': namespace['HEAD'],
                'file_count': len(entries), 'raw_third_party_fulltexts_included': False,
                'files': entries}
    payload[namespace['MANIFEST']] = (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode()
    scratch = P / 'tmp'
    need(not scratch.is_symlink(), 'linked build scratch')
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='package-build-', dir=scratch) as tmp:
        stage = Path(tmp) / 'packet'; stage.mkdir()
        for name, data in payload.items():
            path = stage / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
        namespace['verify'](stage)
        archive_path = Path(tmp) / OUTPUT
        with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9, strict_timestamps=True) as archive:
            for name, data in sorted(payload.items()):
                info = zipfile.ZipInfo(name, date_time=(2026, 10, 15, 0, 0, 0))
                info.create_system = 3; info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        data = archive_path.read_bytes()
        with zipfile.ZipFile(archive_path) as archive:
            names = archive.namelist()
            need(names == sorted(payload) and len(names) == len(set(names)), 'ZIP inventory/order')
            for name in names:
                info = archive.getinfo(name)
                need(info.date_time == (2026, 10, 15, 0, 0, 0) and
                     info.external_attr >> 16 == 0o100644 and archive.read(name) == payload[name],
                     'ZIP bytes/mode/timestamp')
        for name, path in mapping.items():
            need(read(A, path.relative_to(A).as_posix()) == payload[name],
                 'input changed during build: ' + name)
        receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'problem_id': '2306086',
                   'original_head': namespace['HEAD'], 'files': len(payload),
                   'zip_path': OUTPUT, 'zip_bytes': len(data), 'zip_sha256': sha(data),
                   'pdf_path': 'real_schlicht_preschwarzian.pdf',
                   'pdf_bytes': len(payload['real_schlicht_preschwarzian.pdf']),
                   'pdf_sha256': sha(payload['real_schlicht_preschwarzian.pdf']),
                   'manifest_sha256': sha(payload[namespace['MANIFEST']]),
                   'builder_sha256': sha(payload['build_package.py']),
                   'verifier_sha256': sha(payload['verify_package.py']),
                   'metadata_sha256': sha(payload['zenodo-deposit.json']),
                   'source_count': len(mapping), 'raw_third_party_fulltexts_included': False,
                   'replays_performed_by_builder': False,
                   'determinism': 'sorted names, fixed UTC date, Unix regular-file modes, deflate level 9; same bytes and zlib runtime reproduce ZIP'}
        receipt_temp = Path(tmp) / RECEIPT
        receipt_temp.write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
        for output in (P / OUTPUT, P / RECEIPT):
            need(not output.is_symlink() and (not output.exists() or output.is_file()), 'unsafe output')
        os.replace(archive_path, P / OUTPUT)
        os.replace(receipt_temp, P / RECEIPT)
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
