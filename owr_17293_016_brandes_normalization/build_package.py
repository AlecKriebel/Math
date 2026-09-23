#!/usr/bin/env python3
"""Build reproducible local archives and, optionally, the repository Pages copy."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
STAMP = (2026, 9, 23, 0, 0, 0)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_zip(path, contents):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(contents.items()):
            info = zipfile.ZipInfo(name, STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)


def checksums(contents):
    return ''.join(f'{digest(data)}  {name}\n' for name, data in sorted(contents.items())).encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--deploy-docs', action='store_true')
    args = parser.parse_args()
    paper = ROOT / 'output/pdf/paper.pdf'
    if not paper.is_file():
        raise SystemExit('Compile manuscript/paper.tex into output/pdf first.')
    zenodo = ROOT / 'zenodo'
    site = ROOT / 'site'
    meta = json.loads((zenodo / 'metadata.json').read_text())
    if meta != json.loads((ROOT / '.zenodo.json').read_text()):
        raise SystemExit('Metadata copies disagree.')
    (zenodo / 'deposition-payload.json').write_text(json.dumps({'metadata': meta}, indent=2) + '\n')
    paths = [ROOT / name for name in ('README.md', 'LICENSES.md', 'CITATION.cff',
             '.gitignore', '.zenodo.json', 'build_package.py', 'research_log.md',
             'manuscript/paper.tex', 'output/pdf/paper.pdf', 'site/index.html',
             'zenodo/metadata.json', 'zenodo/UPLOAD.md', 'zenodo/deposition-payload.json')]
    paths += sorted((ROOT / 'audit').glob('*.md'))
    paths += sorted((ROOT / 'sources').glob('*.json'))
    paths += [p for p in sorted((ROOT / 'verification').rglob('*')) if p.is_file()
              and p.suffix in ('.py', '.json', '.md') and '__pycache__' not in p.parts]
    contents = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in paths}
    manifest = checksums(contents)
    (ROOT / 'SOURCE_SHA256SUMS.txt').write_bytes(manifest)
    contents['SOURCE_SHA256SUMS.txt'] = manifest
    source_zip = zenodo / 'source-and-verification.zip'
    write_zip(source_zip, contents)
    kit = {'paper.pdf': paper.read_bytes(),
           'source-and-verification.zip': source_zip.read_bytes(),
           'UPLOAD.md': (zenodo / 'UPLOAD.md').read_bytes(),
           'metadata.json': (zenodo / 'metadata.json').read_bytes(),
           '.zenodo.json': (ROOT / '.zenodo.json').read_bytes(),
           'deposition-payload.json': (zenodo / 'deposition-payload.json').read_bytes(),
           'LICENSES.md': (ROOT / 'LICENSES.md').read_bytes()}
    kit['SHA256SUMS.txt'] = checksums(kit)
    for name, data in kit.items():
        (zenodo / name).write_bytes(data)
    write_zip(zenodo / 'zenodo-upload-kit.zip', kit)
    downloads = {'paper.pdf': paper.read_bytes(),
                 'source-and-verification.zip': source_zip.read_bytes(),
                 'zenodo-upload-kit.zip': (zenodo / 'zenodo-upload-kit.zip').read_bytes(),
                 'zenodo-metadata.json': (zenodo / 'metadata.json').read_bytes(),
                 'zenodo-upload.md': (zenodo / 'UPLOAD.md').read_bytes()}
    for name, data in downloads.items():
        (site / name).write_bytes(data)
    (site / 'SHA256SUMS.txt').write_bytes(checksums(downloads))
    if args.deploy_docs:
        repo = ROOT.parent
        if not (repo / '.git').is_dir() or not (repo / 'docs').is_dir():
            raise SystemExit('--deploy-docs requires the original Math repository layout.')
        target = repo / 'docs/papers/brandes-coefficient-normalization'
        target.mkdir(parents=True, exist_ok=True)
        for name in ['index.html', 'SHA256SUMS.txt', *downloads]:
            shutil.copy2(site / name, target / name)
    print(json.dumps({'source_files': len(contents), 'paper_bytes': paper.stat().st_size,
          'source_archive_sha256': digest(source_zip.read_bytes()),
          'zenodo_kit_sha256': digest((zenodo / 'zenodo-upload-kit.zip').read_bytes()),
          'deployed_to_docs': args.deploy_docs}, indent=2))


if __name__ == '__main__':
    main()
