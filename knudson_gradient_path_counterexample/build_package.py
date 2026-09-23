#!/usr/bin/env python3
"""Build deterministic, verified source and manual-Zenodo archives.

Run from any directory with Python 3.9+. --site also copies this project's
public artifacts into the enclosing Math repository's existing docs tree.
Does not contact any service, publish a DOI, or create a GitHub release.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent
PREFIX = 'knudson-gradient-path-v1.0.1'
STAMP = (2026, 9, 23, 0, 0, 0)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sums(files):
    return ''.join(f'{sha(data)}  {name}\n' for name, data in sorted(files.items())).encode()


def archive(files):
    buffer = io.BytesIO()
    with ZipFile(buffer, 'w', compression=ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(files.items()):
            info = ZipInfo(name, STAMP)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = ZIP_DEFLATED
            z.writestr(info, data, compress_type=ZIP_DEFLATED, compresslevel=9)
    return buffer.getvalue()


def verify_outputs():
    for script, expected in [('verify.py', 'expected_output.txt'),
                             ('independent_check.py', 'independent_output.txt')]:
        result = subprocess.run([sys.executable, str(ROOT/'verification'/script)],
                                check=True, capture_output=True)
        if result.stdout != (ROOT/'verification'/expected).read_bytes():
            raise RuntimeError(f'Expected output mismatch for {script}')
    if not (ROOT/'paper/paper.pdf').read_bytes().startswith(b'%PDF-'):
        raise RuntimeError('Build the manuscript PDF first')
    meta = json.loads((ROOT/'.zenodo.json').read_text())
    wrapped = json.loads((ROOT/'zenodo/deposition.json').read_text())
    if wrapped != {'metadata': meta} or meta['version'] != '1.0.1':
        raise RuntimeError('Metadata mismatch')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', action='store_true')
    args = parser.parse_args()
    verify_outputs()
    names = [Path(n) for n in ('.gitignore', '.zenodo.json', 'README.md',
             'LICENSE.md', 'CITATION.cff', 'research_log.md', 'build_package.py',
             'paper/paper.tex', 'paper/paper.pdf', 'site/index.html',
             'zenodo/UPLOAD.md', 'zenodo/deposition.json')]
    for directory in ('audit', 'inputs', 'verification'):
        names.extend(p.relative_to(ROOT) for p in (ROOT/directory).rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts
                     and p.name != 'deployment.md' and not p.name.startswith('.'))
    files = {p.as_posix(): (ROOT/p).read_bytes() for p in sorted(names)}
    files['SHA256SUMS'] = sums(files)
    source = archive({PREFIX+'/'+n: data for n, data in files.items()})
    upload = ROOT/'zenodo/upload'
    upload.mkdir(parents=True, exist_ok=True)
    upload_files = {'paper.pdf': (ROOT/'paper/paper.pdf').read_bytes(),
                    'source-and-verification.zip': source}
    upload_files['SHA256SUMS'] = sums(upload_files)
    for name, data in upload_files.items():
        (upload/name).write_bytes(data)
    kit = {'UPLOAD.md': (ROOT/'zenodo/UPLOAD.md').read_bytes(),
           'zenodo-metadata.json': (ROOT/'.zenodo.json').read_bytes(),
           'deposition.json': (ROOT/'zenodo/deposition.json').read_bytes()}
    kit.update({'upload/'+n: data for n, data in upload_files.items()})
    kit_path = ROOT/'zenodo/zenodo-upload-kit.zip'
    kit_path.write_bytes(archive(kit))
    (ROOT/'zenodo/zenodo-upload-kit.zip.sha256').write_text(
        sha(kit_path.read_bytes())+'  zenodo-upload-kit.zip\n')
    if args.site:
        target = ROOT.parent/'docs/papers/knudson-gradient-path'
        if not (ROOT.parent/'docs/index.html').exists():
            raise RuntimeError('--site requires the existing Math repository docs tree')
        target.mkdir(parents=True, exist_ok=True)
        copy_map = {'index.html':'site/index.html', 'paper.pdf':'paper/paper.pdf',
          'paper.tex':'paper/paper.tex', 'verify.py':'verification/verify.py',
          'independent_check.py':'verification/independent_check.py',
          'verification-report.md':'audit/verification_report.md',
          'priority-audit.md':'audit/priority_independent.md',
          'zenodo-metadata.json':'.zenodo.json', 'zenodo-upload.md':'zenodo/UPLOAD.md',
          'source-and-verification.zip':'zenodo/upload/source-and-verification.zip',
          'zenodo-upload-kit.zip':'zenodo/zenodo-upload-kit.zip'}
        for dest, src in copy_map.items():
            shutil.copyfile(ROOT/src, target/dest)
        downloads = {n:(target/n).read_bytes() for n in copy_map if n != 'index.html'}
        (target/'SHA256SUMS').write_bytes(sums(downloads))
    print('Verification outputs: exact match')
    print(f'Source archive: {len(files)} files, {len(source)} bytes')
    print(f'Zenodo kit: {kit_path.stat().st_size} bytes')
    print('SHA256:', sha(kit_path.read_bytes()))
    if args.site:
        print('GitHub Pages files refreshed')


if __name__ == '__main__':
    main()
