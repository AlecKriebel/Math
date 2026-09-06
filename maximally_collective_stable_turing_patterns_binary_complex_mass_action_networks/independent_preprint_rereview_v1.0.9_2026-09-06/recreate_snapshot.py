#!/usr/bin/env python3
"""Recreate only this audit's ignored snapshot from the immutable local Git tree."""
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import tarfile
import tempfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PROJECT = HERE.parent.name
inventory = json.loads((HERE / 'SOURCE_INVENTORY.json').read_text())
target = HERE / 'source_snapshot'
if target.exists():
    raise SystemExit('source_snapshot already exists; no files changed. Use check_audit_evidence.py to verify it.')
archive = subprocess.check_output(['git', 'archive', inventory['commit'], PROJECT], cwd=REPO)
if hashlib.sha256(archive).hexdigest() != inventory['archive_sha256']:
    raise RuntimeError('Archive digest mismatch')
expected = {r['path']: r for r in inventory['files']}
with tempfile.TemporaryDirectory(prefix='referee_snapshot_') as temporary:
    work = Path(temporary) / 'source'
    work.mkdir()
    seen = set()
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        for member in tar:
            parts = PurePosixPath(member.name).parts
            if not parts or parts[0] != PROJECT or '..' in parts:
                raise RuntimeError('Unexpected archive path')
            if member.isdir():
                continue
            if not member.isfile():
                raise RuntimeError('Unexpected non-regular archive entry')
            relative = str(PurePosixPath(*parts[1:]))
            row = expected[relative]
            data = tar.extractfile(member).read()
            if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
                raise RuntimeError('File digest mismatch: '+relative)
            destination = work / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            destination.chmod(member.mode)
            seen.add(relative)
    if seen != set(expected):
        raise RuntimeError('Archive file set mismatch')
    # Atomic rename on the same filesystem where available; copy fallback
    # preserves permissions if the temporary directory is on another volume.
    import shutil
    shutil.move(str(work), str(target))
print('IMMUTABLE_SOURCE_SNAPSHOT_RECREATED', len(expected))
