#!/usr/bin/env python3
"""Verify the authored seal and, when present, its private evidence hashes."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'SAFE_AUTHORED_MANIFEST.json').read_text())
for row in manifest['authored_files']:
 p=ROOT/row['path']
 assert p.is_file() and not p.is_symlink(),row['path']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],row['path']
 assert p.stat().st_size==row['bytes'],row['path']
 assert not row['path'].startswith(('private_reading/','private_transport/')),row['path']
for row in manifest['private_evidence_hashes']:
 p=ROOT/row['path']
 if p.exists():
  assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],row['path']
subject=Path(manifest['subject']['candidate_path'])
if subject.exists():
 assert hashlib.sha256(subject.read_bytes()).hexdigest()==manifest['subject']['candidate_sha256']
print('PASS: authored files, subject, and available private evidence match the seal.')
