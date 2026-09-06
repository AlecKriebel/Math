#!/usr/bin/env python3
"""Verify the audit snapshot, or reconstruct it from the recorded Git commit."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.name
REPO = HERE.parent.parent
DEST = HERE / 'source_snapshot'
inventory = json.loads((HERE / 'SOURCE_INVENTORY.json').read_text())
if not DEST.exists():
    raw = subprocess.check_output(['git', 'archive', inventory['commit'], PROJECT], cwd=REPO)
    if hashlib.sha256(raw).hexdigest() != inventory['archive_sha256']:
        raise RuntimeError('Git archive does not match the recorded snapshot')
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        members = archive.getmembers()
        for item in members:
            path = Path(item.name)
            if path.is_absolute() or '..' in path.parts or path.parts[0] != PROJECT:
                raise RuntimeError('Unsafe archive member')
            if not (item.isdir() or item.isfile()):
                raise RuntimeError('Unexpected nonregular archive member')
        DEST.mkdir()
        for item in members:
            relative = Path(item.name).relative_to(PROJECT)
            target = DEST / relative
            if item.isdir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.extractfile(item).read())
                target.chmod(item.mode & 0o777)
expected = {row['path']: row['sha256'] for row in inventory['files']}
actual = {str(p.relative_to(DEST)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in DEST.rglob('*') if p.is_file()}
if actual != expected:
    raise RuntimeError('Snapshot differs from the recorded file inventory; no files repaired')
print(f'SNAPSHOT_INVENTORY_MATCH: {len(actual)} files')
