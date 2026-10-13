#!/usr/bin/env python3
"""Assemble explicit authored supplement and Zenodo upload kit.

Run after final reviews. Private sources, raw extracts, logs containing fetched
documents, caches and third-party PDFs are never selected implicitly.
"""
import hashlib
import json
from pathlib import Path
import stat
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
PUBLIC = [
    'note.tex', 'README.md', 'build_package.py', 'zenodo-metadata.json',
]
# Review materials are enumerated by the root after reading their exact files.
SELECTION = HERE / 'supplement_selection.json'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def write_zip(path, members):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name, raw in sorted(members.items()):
            zi = zipfile.ZipInfo(name, (2026, 10, 12, 0, 0, 0))
            zi.create_system = 3
            zi.external_attr = (stat.S_IFREG | 0o644) << 16
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, raw)
    with zipfile.ZipFile(path) as z:
        if set(z.namelist()) != set(members):
            raise RuntimeError('archive member mismatch')
        for name, raw in members.items():
            if z.read(name) != raw:
                raise RuntimeError('archive content mismatch: ' + name)


def main():
    chosen = json.loads(SELECTION.read_text())
    members = {}
    for name in PUBLIC:
        members['preprint/' + name] = (HERE / name).read_bytes()
    for item in chosen:
        rel = item['path']
        p = AUDIT / rel
        if p.is_symlink() or '..' in Path(rel).parts or not p.is_file():
            raise RuntimeError('unsafe or missing selected file: ' + rel)
        members[item.get('archive_path', rel)] = p.read_bytes()
    manifest = {
        'format': 'annular-martin-kernel-authored-supplement-v1',
        'problem_id': 2307042,
        'source_pr': 810,
        'source_head': '5820e9784dbcfeda0acabaa435cb38cf6a4576df',
        'scope': 'Analytic proof, source, authored reviews and reproducibility support; integrity is not proof.',
        'manifest_self_reference': 'The manifest is excluded from its own inventory.',
        'files': [dict(path=n, bytes=len(b), sha256=digest(b))
                  for n, b in sorted(members.items())],
    }
    members['MANIFEST.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    write_zip(HERE / 'verification.zip', members)
    metadata = json.loads((HERE / 'zenodo-metadata.json').read_text())
    deposit = {'metadata': metadata, 'files': [
        {'path': 'output/pdf/note.pdf', 'name': 'annular-martin-kernel-note.pdf'},
        {'path': 'verification.zip', 'name': 'annular-martin-kernel-verification.zip'},
    ]}
    (HERE / 'zenodo-deposit.json').write_text(json.dumps(deposit, indent=2) + '\n')
    kit_deposit = {'metadata': metadata, 'files': [
        {'path': 'annular-martin-kernel-note.pdf'},
        {'path': 'annular-martin-kernel-verification.zip'},
    ]}
    kit = {
        'annular-martin-kernel-note.pdf': (HERE / 'output/pdf/note.pdf').read_bytes(),
        'annular-martin-kernel-verification.zip': (HERE / 'verification.zip').read_bytes(),
        'zenodo-metadata.json': (HERE / 'zenodo-metadata.json').read_bytes(),
        'zenodo-deposit.json': (json.dumps(kit_deposit, indent=2) + '\n').encode(),
    }
    write_zip(HERE / 'zenodo-upload-kit.zip', kit)
    print(json.dumps({'supplement_files': len(members), 'verification_sha256':
        digest((HERE / 'verification.zip').read_bytes()), 'kit_sha256':
        digest((HERE / 'zenodo-upload-kit.zip').read_bytes())}, indent=2))


if __name__ == '__main__':
    main()
