#!/usr/bin/env python3
"""Read-only packet and immutable native payload integrity verification."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

HERE = Path(__file__).resolve().parent
SOURCES = HERE.parents[1] / 'sources'


def check(value, name):
    if not value:
        raise RuntimeError(name)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest_path = HERE / 'ARTIFACT_MANIFEST.json'
manifest = json.loads(manifest_path.read_text())
seen = {}
for entry in manifest['files']:
    name = entry['relative_path']
    parts = PurePosixPath(name)
    check(not parts.is_absolute() and '..' not in parts.parts and name not in seen,
          'unsafe or duplicate manifest member')
    seen[name] = entry
actual = set()
for p in HERE.rglob('*'):
    check(not p.is_symlink(), 'packet symlink')
    if p.is_file():
        actual.add(p.relative_to(HERE).as_posix())
check(actual == set(seen) | {'ARTIFACT_MANIFEST.json','FINAL_SEAL.json'},
      'unexpected or missing packet file')
for name, entry in seen.items():
    path = HERE / name
    check(path.stat().st_size == entry['bytes'] and sha(path) == entry['sha256'],
          'packet bytes/hash mismatch: ' + name)
seal_path = HERE / 'FINAL_SEAL.json'
seal = json.loads(seal_path.read_text())
check(sha(manifest_path) == seal['artifact_manifest_sha256'], 'manifest seal mismatch')
for name, field in [('INITIAL_RECONSTRUCTION.md','initial_reconstruction_sha256'),
                    ('REPORT.md','report_sha256'),('VERDICT.json','verdict_sha256'),
                    ('DERIVATIONS.md','derivations_sha256')]:
    check(sha(HERE / name) == seal[field], field + ' mismatch')
for name, field in [('SOURCE_READY.json','source_ready_sha256'),
                    ('regular_zas_bianchi_defect.pdf','published_pdf_sha256'),
                    ('published-source/manuscript.tex','controlling_tex_sha256'),
                    ('regular_zas_bianchi_verification_v1.zip','native_archive_sha256')]:
    check(sha(SOURCES / name) == seal[field], field + ' mismatch')
count = 0
with zipfile.ZipFile(SOURCES / 'regular_zas_bianchi_verification_v1.zip') as archive:
    for member in archive.infolist():
        if not member.is_dir():
            check((SOURCES / 'published-source' / member.filename).read_bytes()
                  == archive.read(member), 'native payload changed: ' + member.filename)
            count += 1
check(count == 181, 'native payload count differs')
print(json.dumps({'status':'PASS','packet_files_verified':len(seen),
                  'native_archive_payloads_verified':count,
                  'artifact_manifest_sha256':sha(manifest_path),
                  'final_seal_sha256':sha(seal_path),
                  'scope':'Integrity only. Mathematical evidence is in the derivations and independent verifier.'},
                 indent=2,sort_keys=True))
