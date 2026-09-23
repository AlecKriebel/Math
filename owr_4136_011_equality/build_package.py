#!/usr/bin/env python3
"""Build checked paper downloads and a manual Zenodo kit; never upload anything."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.name
STAMP = (2026, 9, 23, 0, 0, 0)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(paths, target, base):
    target.write_text(''.join(digest(p) + '  ' + p.relative_to(base).as_posix() + '\n'
                              for p in sorted(paths)))


def archive(paths, target, base, prefix=''):
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(paths):
            info = zipfile.ZipInfo(prefix + p.relative_to(base).as_posix(), STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, p.read_bytes())
    with zipfile.ZipFile(target) as z:
        if z.testzip() is not None:
            raise RuntimeError('Corrupt generated archive')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compile', action='store_true', help='Compile paper with Tectonic')
    parser.add_argument('--publish-site', action='store_true', help='Copy assets into local docs/ tree')
    args = parser.parse_args()
    (ROOT/'output/build').mkdir(parents=True, exist_ok=True)
    (ROOT/'output/pdf').mkdir(parents=True, exist_ok=True)
    if args.compile:
        subprocess.run(['tectonic', '--keep-logs', '--outdir', str(ROOT/'output/build'),
                        str(ROOT/'manuscript/paper.tex')], check=True)
        shutil.copy2(ROOT/'output/build/paper.pdf', ROOT/'output/pdf/paper.pdf')
    pdf = ROOT/'output/pdf/paper.pdf'
    if not pdf.is_file():
        raise RuntimeError('Missing PDF; run with --compile')
    normal = subprocess.check_output([sys.executable, str(ROOT/'verification/verify.py')])
    optimized = subprocess.check_output([sys.executable, '-O', str(ROOT/'verification/verify.py')])
    if normal != optimized:
        raise RuntimeError('Verifier differs under optimization')
    result = json.loads(normal)
    if result['status'] != 'passed' or result['checks'] != 298 or len(result['cases']) != 18:
        raise RuntimeError('Unexpected verifier result; review package claims')
    (ROOT/'output/verification.json').write_bytes(normal)
    metadata = json.loads((ROOT/'zenodo/metadata.json').read_text())
    if metadata != json.loads((ROOT/'.zenodo.json').read_text()):
        raise RuntimeError('Metadata copies differ')
    if {'metadata': metadata} != json.loads((ROOT/'zenodo/deposition.json').read_text()):
        raise RuntimeError('REST metadata wrapper differs')
    # Explicit allowlist prevents redistribution of third-party reading copies,
    # temporary renderings, credentials, or previously generated archives.
    selected = [ROOT/p for p in [
        'README.md', 'LICENSE.md', 'CITATION.cff', '.zenodo.json', '.gitignore',
        'RESEARCH_LOG.md', 'build_package.py', 'manuscript/paper.tex',
        'verification/verify.py', 'verification/README.md', 'output/verification.json',
        'output/pdf/paper.pdf', 'site/index.html', 'sources/README.md',
        'zenodo/metadata.json', 'zenodo/deposition.json', 'zenodo/UPLOAD.md']]
    selected += sorted((ROOT/'audit').glob('*.md'))
    selected += sorted((ROOT/'audit').glob('*.json'))
    for p in selected:
        if not p.is_file():
            raise RuntimeError('Missing package file: '+str(p))
    manifest(selected, ROOT/'SOURCE_SHA256SUMS', ROOT)
    selected.append(ROOT/'SOURCE_SHA256SUMS')
    source_zip = ROOT/'output/source-and-verification.zip'
    archive(selected, source_zip, ROOT, PROJECT+'/')
    upload = ROOT/'zenodo/upload'
    upload.mkdir(exist_ok=True)
    shutil.copy2(pdf, upload/'paper.pdf')
    shutil.copy2(source_zip, upload/'source-and-verification.zip')
    manifest([upload/'paper.pdf', upload/'source-and-verification.zip'], upload/'SHA256SUMS', upload)
    kit_files = [ROOT/'zenodo'/p for p in [
        'UPLOAD.md', 'metadata.json', 'deposition.json', 'upload/paper.pdf',
        'upload/source-and-verification.zip', 'upload/SHA256SUMS']]
    kit = ROOT/'zenodo/zenodo-upload-kit.zip'
    archive(kit_files, kit, ROOT/'zenodo')
    manifest([kit], ROOT/'zenodo/zenodo-upload-kit.zip.sha256', ROOT/'zenodo')
    if args.publish_site:
        repo = ROOT.parent
        if not (repo/'docs/index.html').is_file():
            raise RuntimeError('--publish-site requires the Math repository checkout')
        site = repo/'docs/papers/fps-equality'
        site.mkdir(parents=True, exist_ok=True)
        copies = {
            'index.html': ROOT/'site/index.html', 'paper.pdf': pdf,
            'paper.tex': ROOT/'manuscript/paper.tex', 'verify.py': ROOT/'verification/verify.py',
            'verification-report.md': ROOT/'audit/VERIFICATION_REPORT.md',
            'independent-proof.md': ROOT/'audit/independent-proof.md',
            'priority-audit.md': ROOT/'audit/priority-independent.md',
            'source-match.md': ROOT/'audit/source-match.md',
            'source-and-verification.zip': source_zip,
            'zenodo-upload-kit.zip': kit, 'zenodo-metadata.json': ROOT/'zenodo/metadata.json',
            'zenodo-upload.md': ROOT/'zenodo/UPLOAD.md'}
        for name, path in copies.items():
            shutil.copy2(path, site/name)
        manifest([site/name for name in copies], site/'SHA256SUMS', site)
    print(json.dumps({'status':'passed','checks':result['checks'],'cases':len(result['cases']),
                      'source_archive':str(source_zip),'zenodo_kit':str(kit),
                      'source_sha256':digest(source_zip),'zenodo_sha256':digest(kit)}, indent=2))


if __name__ == '__main__':
    main()
