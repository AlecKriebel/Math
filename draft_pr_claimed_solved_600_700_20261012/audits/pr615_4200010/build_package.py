#!/usr/bin/env python3
"""Build an authored-only reproducible source/verification ZIP.

Whole-package release reviews remain outside the reviewed ZIP so their own
receipts do not change the bytes they review. No third-party fulltext is copied.
"""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

root = Path(__file__).resolve().parent
pub = root / 'publication'
dest = pub / 'tmp' / 'package'
if dest.exists():
    shutil.rmtree(dest)
dest.mkdir(parents=True)

def copy(src, target):
    if src.is_symlink():
        raise RuntimeError(f'Symlink rejected: {src}')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, target)

for name in ['README.md', 'manuscript.tex', 'verify_package.py']:
    copy(pub / name, dest / name)
copy(pub / 'output/pdf/manuscript.pdf', dest / 'research-note.pdf')
for src in (root / 'native').rglob('*'):
    if src.is_file():
        copy(src, dest / src.relative_to(root))
for family in ['dynamics_01', 'geometry_01', 'priority_01']:
    for src in (root / 'reviews' / family).glob('*'):
        if src.is_file() and src.suffix in {'.md', '.json', '.py'}:
            copy(src, dest / src.relative_to(root))
files = {}
for src in sorted(dest.rglob('*')):
    if src.is_file():
        files[src.relative_to(dest).as_posix()] = {
            'size': src.stat().st_size,
            'sha256': hashlib.sha256(src.read_bytes()).hexdigest(),
        }
(dest / 'PACKAGE_MANIFEST.json').write_text(json.dumps({'version': '1.0.0', 'files': files}, indent=2) + '\n')
zip_path = pub / 'hamiltonian-ugly-band-source-verification-v1.0.0.zip'
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for src in sorted(dest.rglob('*')):
        if src.is_file():
            zi = zipfile.ZipInfo(src.relative_to(dest).as_posix(), date_time=(2026, 10, 12, 12, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = (0o100644 << 16)
            archive.writestr(zi, src.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
receipt = {'zip': zip_path.name, 'size': zip_path.stat().st_size,
           'sha256': hashlib.sha256(zip_path.read_bytes()).hexdigest(),
           'content_files': len(files) + 1, 'source_fulltext_included': False}
(pub / 'PACKAGE_BUILD.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
