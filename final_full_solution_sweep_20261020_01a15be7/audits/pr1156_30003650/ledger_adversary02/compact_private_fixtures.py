#!/usr/bin/env python3
"""Deduplicate and verify only this audit's completed private fixture trees."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import zipfile

D = Path(__file__).resolve().parent
PRIVATE = D / 'private'
TREES = ['fixtures', 'fixtures_final']


def require(value, reason):
    if not value: raise RuntimeError(reason)


def main():
    destination = PRIVATE / 'completed_fixture_content_store.zip'
    temporary = PRIVATE / 'completed_fixture_content_store.partial.zip'
    require(not destination.exists() and not temporary.exists(), 'Do not replace an existing archive')
    files, directories, blobs = [], [], {}
    total = 0
    for tree in TREES:
        top = PRIVATE / tree
        require(top.is_dir() and not top.is_symlink(), 'Missing or unsafe owned fixture tree')
        for path in [top, *sorted(top.rglob('*'))]:
            require(not path.is_symlink(), 'Unexpected symlink')
            info = path.stat()
            entry = {'path': path.relative_to(PRIVATE).as_posix(), 'mode': stat.S_IMODE(info.st_mode), 'mtime_ns': info.st_mtime_ns}
            if path.is_dir(): directories.append(entry); continue
            require(path.is_file(), 'Unexpected special file')
            payload = path.read_bytes()
            digest = hashlib.sha256(payload).hexdigest()
            entry.update(bytes=len(payload), sha256=digest)
            files.append(entry)
            blobs.setdefault(digest, path)
            total += len(payload)
    manifest = {'schema': 1, 'trees': TREES, 'files': files, 'directories': directories,
                'blob_key': 'blobs/<sha256>', 'source_files': len(files), 'source_bytes': total,
                'unique_content_blobs': len(blobs), 'mapping_scope': 'Every original file path, exact bytes/SHA256, permission mode and mtime; every directory path/mode/mtime.'}
    manifest_bytes = (json.dumps(manifest, indent=2) + '\n').encode()
    with zipfile.ZipFile(temporary, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        archive.writestr('MANIFEST.json', manifest_bytes)
        for digest, path in sorted(blobs.items()): archive.writestr('blobs/' + digest, path.read_bytes())
    with zipfile.ZipFile(temporary) as archive:
        require(archive.testzip() is None, 'Archive CRC check failed')
        require(archive.read('MANIFEST.json') == manifest_bytes, 'Manifest readback mismatch')
        require(set(archive.namelist()) == {'MANIFEST.json'} | {'blobs/' + digest for digest in blobs}, 'Archive member inventory mismatch')
        decoded = {digest: archive.read('blobs/' + digest) for digest in blobs}
        require(all(hashlib.sha256(body).hexdigest() == digest for digest, body in decoded.items()), 'Content blob SHA mismatch')
        for entry in files:
            path = PRIVATE / entry['path']
            require(path.read_bytes() == decoded[entry['sha256']] and len(decoded[entry['sha256']]) == entry['bytes'], 'Original/archive file bytes mismatch')
            require(stat.S_IMODE(path.stat().st_mode) == entry['mode'] and path.stat().st_mtime_ns == entry['mtime_ns'], 'Original file mode/time changed')
        for entry in directories:
            path = PRIVATE / entry['path']
            require(path.is_dir() and stat.S_IMODE(path.stat().st_mode) == entry['mode'] and path.stat().st_mtime_ns == entry['mtime_ns'], 'Original directory mode/time changed')
    os.replace(temporary, destination)
    receipt = {'at': dt.datetime.now(dt.timezone.utc).isoformat(), 'archive': 'private/' + destination.name,
               'archive_bytes': destination.stat().st_size, 'archive_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
               'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(), 'files': len(files), 'directories': len(directories),
               'source_bytes': total, 'unique_content_blobs': len(blobs),
               'all_path_byte_sha_mode_and_mtime_mappings_verified': True, 'full_crc_and_closed_member_inventory_verified': True,
               'completed_owned_fixture_trees_removed_after_verification': TREES, 'other_folders_touched': False}
    for tree in TREES: shutil.rmtree(PRIVATE / tree)
    (D / 'FIXTURE_ARCHIVE_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__': main()
