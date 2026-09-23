#!/usr/bin/env python3
"""Build deterministic public archives and copy only this project's Pages assets.

Standard library only. No network, Git changes, or Zenodo publication.
"""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
STAMP = (2026, 9, 23, 0, 0, 0)


def archive(path, files):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    required = ['paper/main.pdf', 'audit/final_manuscript_review.md', 'audit/priority_review.md',
                'verification/results_exact.json', 'verification/results_numeric.json']
    for item in required:
        if not (ROOT / item).is_file():
            raise SystemExit(f'Missing required artifact: {item}')
    payload = {}
    for name in ['README.md', 'LICENSE.md', 'CITATION.cff', 'build_release.py']:
        payload[name] = (ROOT / name).read_bytes()
    for folder, allowed in [('paper', {'.tex', '.pdf'}), ('audit', {'.md', '.json'}),
                            ('verification', {'.md', '.py', '.json'}), ('research', {'.md'}),
                            ('site', {'.html'}), ('zenodo', {'.md', '.txt', '.json'})]:
        for path in sorted((ROOT / folder).iterdir()):
            if path.is_file() and path.suffix in allowed and path.name != 'SHA256SUMS.txt':
                payload[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    payload['MANIFEST.sha256'] = ''.join(f'{digest(data)}  {name}\n' for name, data in sorted(payload.items())).encode()
    out = ROOT / 'zenodo'
    repro = out / 'reproducibility.zip'
    archive(repro, payload)
    kit_files = {'paper.pdf': (ROOT / 'paper/main.pdf').read_bytes(),
                 'reproducibility.zip': repro.read_bytes(),
                 'metadata.json': (out / 'metadata.json').read_bytes(),
                 'COPY_PASTE.txt': (out / 'COPY_PASTE.txt').read_bytes(),
                 'UPLOAD.md': (out / 'UPLOAD.md').read_bytes()}
    kit_files['SHA256SUMS.txt'] = ''.join(f'{digest(data)}  {name}\n' for name, data in sorted(kit_files.items())).encode()
    version = json.loads((out / 'metadata.json').read_text())['version']
    kit = out / f'gromov-unitary-retraction-v{version}-zenodo-upload.zip'
    archive(kit, kit_files)
    (out / 'SHA256SUMS.txt').write_text(f'{digest(repro.read_bytes())}  reproducibility.zip\n{digest(kit.read_bytes())}  {kit.name}\n')
    # Only publish to this repository if its Pages root is present. This also
    # lets readers build the archives in a standalone extracted package.
    pages_root = ROOT.parent / 'docs'
    if pages_root.is_dir():
        site = pages_root / 'papers/gromov-unitary-lipschitz'
        site.mkdir(parents=True, exist_ok=True)
        sources = {'index.html': ROOT / 'site/index.html', 'paper.pdf': ROOT / 'paper/main.pdf',
                   'reproducibility.zip': repro, 'zenodo-upload.zip': kit,
                   'zenodo-metadata.json': out / 'metadata.json'}
        for name, source in sources.items():
            shutil.copyfile(source, site / name)
        (site / 'SHA256SUMS.txt').write_text(''.join(f'{digest((site / name).read_bytes())}  {name}\n' for name in sorted(sources)))
    print(json.dumps({'reproducibility_bytes': repro.stat().st_size, 'upload_kit_bytes': kit.stat().st_size,
                      'archived_files': len(payload), 'reproducibility_sha256': digest(repro.read_bytes()),
                      'upload_kit_sha256': digest(kit.read_bytes())}, indent=2))

if __name__ == '__main__':
    main()
