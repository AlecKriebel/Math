#!/usr/bin/env python3
"""Build deterministic archives and the dedicated GitHub Pages mirror.
Run after regenerating output/paper.pdf and verification/results.json.
No networking, repository-wide staging, releases, or Zenodo uploads.
"""
from pathlib import Path
from hashlib import sha256
from html.parser import HTMLParser
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
SITE = ROOT / 'site'
EPOCH = (2026, 9, 23, 0, 0, 0)


def digest(data):
    return sha256(data).hexdigest()


def archive(path, mapping):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(mapping.items()):
            info = zipfile.ZipInfo(name, EPOCH)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None or sorted(z.namelist()) != sorted(mapping):
            raise RuntimeError('Archive validation failed')
        for name, data in mapping.items():
            if z.read(name) != data:
                raise RuntimeError('Archive byte mismatch: ' + name)


def manifest(mapping):
    return ''.join(f'{digest(data)}  {name}\n' for name, data in sorted(mapping.items())).encode()


def main():
    required = ['README.md', 'LICENSES.md', 'CITATION.cff', 'build_package.py',
        'manuscript/paper.tex', 'output/paper.pdf', 'verification/verify.py',
        'verification/results.json', 'sources/inventory.json', 'site/index.html',
        'zenodo/metadata.json', 'zenodo/UPLOAD.md',
        'audit/adversarial-proof.md', 'audit/independent-derivation.md',
        'audit/final-review.md', 'audit/priority-independent.md',
        'audit/source-match.md', 'audit/VERIFICATION_REPORT.md',
        'audit/preprint-readiness.md']
    required += [str(p.relative_to(ROOT)) for p in sorted(
        (ROOT/'audit').glob('preprint-round-*.md'))]
    payload = {name: (ROOT/name).read_bytes() for name in required}
    metadata = json.loads(payload['zenodo/metadata.json'])
    for key in ('title', 'upload_type', 'publication_type', 'description', 'creators', 'license'):
        if not metadata.get(key):
            raise RuntimeError('Missing metadata: ' + key)
    if 'doi' in metadata or metadata['creators'][0]['orcid'] != '0009-0001-9320-500X':
        raise RuntimeError('Invalid DOI or author metadata')
    payload['SHA256SUMS'] = manifest(payload)
    source_zip = ROOT/'output/source-and-verification.zip'
    archive(source_zip, payload)
    kit = {
        'paper.pdf': (ROOT/'output/paper.pdf').read_bytes(),
        'source-and-verification.zip': source_zip.read_bytes(),
        'metadata.json': payload['zenodo/metadata.json'],
        'UPLOAD.md': payload['zenodo/UPLOAD.md'],
        'LICENSES.md': payload['LICENSES.md']}
    kit['SHA256SUMS'] = manifest(kit)
    kit_zip = ROOT/'zenodo/zenodo-upload-kit.zip'
    archive(kit_zip, kit)
    (ROOT/'zenodo/zenodo-upload-kit.zip.sha256').write_text(
        f'{digest(kit_zip.read_bytes())}  zenodo-upload-kit.zip\n')
    files = {
        'paper.pdf': ROOT/'output/paper.pdf', 'paper.tex': ROOT/'manuscript/paper.tex',
        'verify.py': ROOT/'verification/verify.py', 'results.json': ROOT/'verification/results.json',
        'source-and-verification.zip': source_zip, 'zenodo-upload-kit.zip': kit_zip,
        'zenodo-metadata.json': ROOT/'zenodo/metadata.json',
        'zenodo-upload.md': ROOT/'zenodo/UPLOAD.md',
        'verification-report.md': ROOT/'audit/VERIFICATION_REPORT.md',
        'preprint-readiness.md': ROOT/'audit/preprint-readiness.md',
        'priority-audit.md': ROOT/'audit/priority-independent.md',
        'source-match.md': ROOT/'audit/source-match.md', 'LICENSES.md': ROOT/'LICENSES.md'}
    for name, source in files.items():
        shutil.copy2(source, SITE/name)
    site_files = ['index.html', *files]
    (SITE/'SHA256SUMS').write_bytes(manifest({name:(SITE/name).read_bytes() for name in site_files}))
    site_files.append('SHA256SUMS')

    class Links(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for key, value in attrs:
                if key in ('href', 'src') and value and not value.startswith(('http:', 'https:', '#', '../../')):
                    if not (SITE/value.split('#')[0]).is_file():
                        raise RuntimeError('Broken local site link: ' + value)
    Links().feed((SITE/'index.html').read_text())
    # In an extracted source archive no repository docs directory exists.
    # In the repository, update only this paper's dedicated Pages route.
    repo_docs = ROOT.parent/'docs'
    if repo_docs.is_dir():
        mirror = repo_docs/'papers/odd-part-slow-variation'
        mirror.mkdir(parents=True, exist_ok=True)
        for name in site_files:
            shutil.copy2(SITE/name, mirror/name)
            if (SITE/name).read_bytes() != (mirror/name).read_bytes():
                raise RuntimeError('Mirror hash mismatch: ' + name)
    print(json.dumps({'status':'PASS', 'source_archive_files':len(payload),
        'upload_kit_files':len(kit), 'site_files':len(site_files),
        'source_archive_sha256':digest(source_zip.read_bytes()),
        'upload_kit_sha256':digest(kit_zip.read_bytes())}, indent=2))


if __name__ == '__main__':
    main()
