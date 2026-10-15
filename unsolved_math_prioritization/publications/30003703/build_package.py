#!/usr/bin/env python3
"""Build the deterministic PR681 archive from captured, validated bytes.

Works in the audit publication/ layout or an extracted package. No network,
Git, cloud access or mathematical code execution. Exact replays are provided by
verify_package.py. The build receipt is outside the archive to avoid circularity.
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
OUTPUT = 'satoh_filtration_verification.zip'
RECEIPT = 'PACKAGE_BUILD_RECEIPT.json'
STAMP = (2026, 10, 15, 0, 0, 0)


def main():
    verifier_path = P / 'verify_package.py'
    if A.is_symlink() or P.is_symlink() or not stat.S_ISREG(verifier_path.lstat().st_mode):
        raise ValueError('linked or nonregular verifier input')
    verifier_bytes = verifier_path.read_bytes()
    # Compile the captured source, without importing mutable cached bytecode.
    ns = {'__file__': str(verifier_path), '__name__': 'captured_package_build_checks'}
    exec(compile(verifier_bytes, str(verifier_path), 'exec'), ns)
    read, sha, need = ns['read_regular'], ns['digest'], ns['need']
    extracted = (P / ns['MANIFEST']).exists()
    if extracted:
        # Existing outputs belong outside the extracted input tree. This keeps
        # its exact allowlist intact and permits a byte-for-byte rebuild.
        ns['verify'](P)
        origin = P
        snapshot = ns['json_data'](read(origin, 'SCOPE_AND_SNAPSHOT.json'))
        mapping = {name: origin / name for name in ns['allowed_names'](snapshot)}
        output_dir = P.parent
    else:
        origin = A
        snapshot = ns['json_data'](read(A, 'SCOPE_AND_SNAPSHOT.json'))
        need(ns['inventory'](A / 'native') == set(ns['native_bindings'](snapshot)),
             'exact original native input inventory')
        mapping = {name: P / ('PACKAGE_README.md' if name == 'README.md' else name)
                   for name in ns['PUBLICATION_FILES']}
        mapping.update({name: A / name for name in ns['ROOT_FILES']})
        for family, names in ns['REVIEW_FILES'].items():
            for name in names:
                member = 'reviews/' + family + '/' + name
                mapping[member] = A / member
        for name in ns['native_bindings'](snapshot):
            mapping['native/' + name] = A / 'native' / name
        output_dir = P
    need(not output_dir.is_symlink() and output_dir.is_dir(), 'unsafe output directory')

    def capture():
        for name in ns['native_bindings'](snapshot):
            need(stat.S_IMODE((origin / 'native' / name).lstat().st_mode) == 0o644,
                 'native filesystem mode: ' + name)
        return {name: read(origin, path.relative_to(origin).as_posix())
                for name, path in mapping.items()}

    payload = capture()
    need(payload['verify_package.py'] == verifier_bytes, 'verifier changed while loading')
    ns['inspect_payload'](payload)
    rows = [{'path': name, 'bytes': len(data), 'sha256': sha(data)}
            for name, data in sorted(payload.items())]
    manifest = {'schema': 1, 'problem_id': ns['PROBLEM'], 'original_head': ns['HEAD'],
                'file_count': len(rows), 'raw_third_party_fulltexts_included': False,
                'files': rows}
    payload[ns['MANIFEST']] = ns['json_bytes'](manifest)
    with tempfile.TemporaryDirectory(prefix='satoh-package-build-', dir=output_dir.parent) as tmp:
        stage = Path(tmp) / 'packet'; stage.mkdir()
        for name, data in payload.items():
            path = stage / name; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data); path.chmod(0o644)
        verified = ns['verify'](stage)
        archive_path = Path(tmp) / OUTPUT
        with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9, strict_timestamps=True) as archive:
            for name, data in sorted(payload.items()):
                info = zipfile.ZipInfo(name, date_time=STAMP)
                info.create_system = 3; info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        data = archive_path.read_bytes()
        with zipfile.ZipFile(archive_path) as archive:
            names = archive.namelist()
            need(names == sorted(payload) and len(names) == len(set(names)), 'ZIP inventory/order')
            for name in names:
                info = archive.getinfo(name)
                need(info.date_time == STAMP and info.create_system == 3 and
                     info.external_attr >> 16 == 0o100644 and
                     info.compress_type == zipfile.ZIP_DEFLATED and not info.is_dir() and
                     archive.read(name) == payload[name], 'ZIP bytes/mode/timestamp/compression')
        need(capture() == {name: content for name, content in payload.items()
                           if name != ns['MANIFEST']}, 'input changed during build')
        if extracted:
            need(ns['verify'](origin) == verified, 'extracted input changed during build')
        else:
            need(ns['inventory'](A / 'native') == set(ns['native_bindings'](snapshot)),
                 'native inventory changed during build')
        receipt = {
            'utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
            'problem_id': ns['PROBLEM'], 'original_head': ns['HEAD'],
            'files': len(payload), 'source_count': len(mapping), 'native_files': 23,
            'zip_path': OUTPUT, 'zip_bytes': len(data), 'zip_sha256': sha(data),
            'pdf_path': 'satoh_filtration_counterexamples.pdf',
            'pdf_bytes': len(payload['satoh_filtration_counterexamples.pdf']),
            'pdf_sha256': sha(payload['satoh_filtration_counterexamples.pdf']),
            'manifest_sha256': sha(payload[ns['MANIFEST']]),
            'builder_sha256': sha(payload['build_package.py']),
            'verifier_sha256': sha(payload['verify_package.py']),
            'metadata_sha256': sha(payload['zenodo-deposit.json']),
            'raw_third_party_fulltexts_included': False,
            'replays_performed_by_builder': False,
            'captured_inputs_verified_before_and_after': True,
            'native_byte_mode_and_git_blob_bindings_verified': True,
            'manifest_self_excluded': True,
            'determinism': 'sorted names; fixed 2026-10-15 00:00:00 ZIP time; Unix regular 100644; deflate level 9; same input bytes and zlib runtime reproduce ZIP',
        }
        receipt_path = Path(tmp) / RECEIPT
        receipt_path.write_bytes(ns['json_bytes'](receipt))
        for output in (output_dir / OUTPUT, output_dir / RECEIPT):
            need(not output.is_symlink() and (not output.exists() or stat.S_ISREG(output.lstat().st_mode)),
                 'unsafe output')
        os.replace(archive_path, output_dir / OUTPUT)
        os.replace(receipt_path, output_dir / RECEIPT)
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
