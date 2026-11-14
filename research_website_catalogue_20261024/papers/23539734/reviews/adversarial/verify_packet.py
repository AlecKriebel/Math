#!/usr/bin/env python3
"""Read-only review-packet and all-original-payload integrity check."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

ROOT = Path(__file__).resolve().parent


def ck(value, message):
    if not value:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest_path = ROOT / 'ARTIFACT_MANIFEST.json'
manifest = json.loads(manifest_path.read_text())
expected = {}
for entry in manifest['files']:
    name = entry['relative_path']
    p = PurePosixPath(name)
    ck(not p.is_absolute() and '..' not in p.parts and name not in expected,
       'unsafe or duplicate manifest path')
    expected[name] = entry
actual = set()
for p in ROOT.rglob('*'):
    ck(not p.is_symlink(), 'symlink in packet')
    if p.is_file():
        actual.add(p.relative_to(ROOT).as_posix())
ck(actual == set(expected) | {'ARTIFACT_MANIFEST.json', 'FINAL_SEAL.json'},
   'packet missing or unexpected files')
for name, entry in expected.items():
    p = ROOT / name
    ck(p.stat().st_size == entry['bytes'] and digest(p) == entry['sha256'],
       'packet content mismatch: ' + name)
seal = json.loads((ROOT / 'FINAL_SEAL.json').read_text())
ck(digest(manifest_path) == seal['artifact_manifest_sha256'], 'manifest seal mismatch')
for name, field in [('INITIAL_RECONSTRUCTION.md', 'initial_reconstruction_sha256'),
                    ('REPORT.md', 'report_sha256'), ('VERDICT.json', 'verdict_sha256')]:
    ck(digest(ROOT / name) == seal[field], field + ' mismatch')
sources = ROOT.parents[1] / 'sources'
for relative, field in [
    ('SOURCE_READY.json', 'source_ready_sha256'),
    ('fixed-birational-cycle-nonlimit.pdf', 'published_pdf_sha256'),
    ('published-source/birational-cycle-verification/paper/main.tex', 'controlling_tex_sha256'),
    ('fixed-birational-cycle-nonlimit-verification.zip', 'original_archive_sha256')]:
    ck(digest(sources / relative) == seal[field], field + ' mismatch')
payloads = 0
with zipfile.ZipFile(sources / 'fixed-birational-cycle-nonlimit-verification.zip') as archive:
    for member in archive.infolist():
        if not member.is_dir():
            payloads += 1
            ck((sources / 'published-source' / member.filename).read_bytes() == archive.read(member),
               'original payload changed: ' + member.filename)
ck(payloads == 69, 'unexpected original payload count')
print(json.dumps({'status': 'PASS', 'packet_files_verified': len(expected),
                  'original_payloads_verified': payloads,
                  'artifact_manifest_sha256': digest(manifest_path),
                  'final_seal_sha256': digest(ROOT / 'FINAL_SEAL.json'),
                  'scope': 'Integrity only; run independent_verifier.py for finite mathematics'},
                 indent=2, sort_keys=True))
