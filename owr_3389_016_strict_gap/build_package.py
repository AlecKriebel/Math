#!/usr/bin/env python3
"""Build deterministic publication ZIPs and optional scoped Pages deployment.

No network access, upload, release creation, or DOI minting is performed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
NAME = 'owr_3389_016_strict_gap'
STAMP = (2026, 9, 23, 0, 0, 0)
FILES = [
    'README.md', 'LICENSES.md', 'CITATION.cff', 'RESEARCH_LOG.md',
    'build_package.py', 'manuscript/paper.tex', 'output/pdf/paper.pdf',
    'audit/VERIFICATION_REPORT.md', 'audit/proof-audit.md',
    'audit/independent-derivation.md', 'audit/source-match.md',
    'audit/priority-audit-independent.md', 'audit/final-manuscript-audit.md',
    'audit/PREPRINT_REVIEW.md', 'audit/preprint-parent-checks.md',
    'verification/verify.py', 'verification/results.json', 'verification/README.md',
    'sources/README.md', 'sources/source-inventory.json',
    'site/index.html', 'site/style.css', 'zenodo/metadata.json',
    'zenodo/metadata-for-api.json', 'zenodo/UPLOAD.md',
]


def manifest(entries):
    return ''.join(f'{hashlib.sha256(data).hexdigest()}  {name}\n'
                   for name, data in sorted(entries.items())).encode()


def archive(path, entries):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo(name, STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--deploy-copy', action='store_true')
    args = parser.parse_args()
    meta = json.loads((ROOT/'zenodo/metadata.json').read_text())
    required = {'title', 'upload_type', 'publication_type', 'publication_date',
                'creators', 'description', 'access_right', 'license', 'version'}
    if not required <= meta.keys() or meta['creators'][0]['orcid'] != '0009-0001-9320-500X':
        raise ValueError('Missing metadata or incorrect author ORCID')
    if 'doi' in meta or 'prereserve_doi' in meta:
        raise ValueError('This prepared upload kit must not invent a DOI')
    (ROOT/'zenodo/metadata-for-api.json').write_text(
        json.dumps({'metadata': meta}, indent=2, ensure_ascii=False)+'\n')
    files = FILES + [p for p in ['audit/package-audit.md', 'audit/DELIVERY_CHECKS.md']
                     if (ROOT/p).is_file()]
    files += sorted(str(p.relative_to(ROOT))
                    for p in (ROOT/'audit').glob('preprint-adversarial-round*.md'))
    entries = {name:(ROOT/name).read_bytes() for name in files}
    source_checks = manifest(entries)
    (ROOT/'SOURCE_SHA256SUMS.txt').write_bytes(source_checks)
    source_entries = {**entries, 'SOURCE_SHA256SUMS.txt':source_checks}
    out = ROOT/'output'
    out.mkdir(exist_ok=True)
    source_zip = out/'source-and-verification.zip'
    archive(source_zip, {NAME+'/'+name:data for name,data in source_entries.items()})
    payload = {'paper.pdf':entries['output/pdf/paper.pdf'],
               'source-and-verification.zip':source_zip.read_bytes()}
    checks = manifest(payload)
    (ROOT/'zenodo/SHA256SUMS.txt').write_bytes(checks)
    kit = {'files/'+name:data for name,data in payload.items()}
    kit['files/SHA256SUMS.txt'] = checks
    for name in ['UPLOAD.md', 'metadata.json', 'metadata-for-api.json']:
        kit[name] = (ROOT/'zenodo'/name).read_bytes()
    kit['LICENSES.md'] = entries['LICENSES.md']
    kit_zip = out/'zenodo-upload-kit.zip'
    archive(kit_zip, kit)
    web = {**payload, 'zenodo-upload-kit.zip':kit_zip.read_bytes(),
           'index.html':entries['site/index.html'], 'style.css':entries['site/style.css'],
           'verification-report.md':entries['audit/VERIFICATION_REPORT.md'],
           'preprint-review.md':entries['audit/PREPRINT_REVIEW.md'],
           'priority-audit.md':entries['audit/priority-audit-independent.md'],
           'source-audit.md':entries['audit/source-match.md']}
    web['SHA256SUMS.txt'] = manifest(web)
    page = out/'site'
    page.mkdir(exist_ok=True)
    for name,data in web.items():
        (page/name).write_bytes(data)
    if args.deploy_copy:
        repo = ROOT.parent
        if not (repo/'.git').exists() or not (repo/'docs/index.html').is_file():
            raise RuntimeError('--deploy-copy requires original repository and docs/')
        dest = repo/'docs/papers/strict-dirichlet-gap'
        dest.mkdir(parents=True,exist_ok=True)
        for name in web:
            shutil.copy2(page/name,dest/name)
        print('Pages files:',dest)
    print('Built:',source_zip)
    print('Built:',kit_zip)
    print('Prepared metadata locally; not submitted to Zenodo.')

if __name__ == '__main__':
    main()
