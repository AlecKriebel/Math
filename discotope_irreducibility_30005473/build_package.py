#!/usr/bin/env python3
"""Build and verify the two deposited files and matching offline upload kit.

Python 3 standard library. Run only after paper.tex has been compiled to
output/pdf/paper.pdf and the mathematical/priority/review artifacts are final.
Publication receipts, credentials, third-party PDFs, and environments are excluded.
"""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
STAMP = (2026, 9, 30, 0, 0, 0)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def archive(path, contents):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(contents.items()):
            assert not name.startswith('/') and '..' not in Path(name).parts
            info = zipfile.ZipInfo(name, date_time=STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(contents)
        for name, data in contents.items():
            assert z.read(name) == data, name


def main():
    deposit = json.loads((ROOT / 'zenodo-deposit.json').read_text())
    assert set(deposit) == {'metadata', 'files'}
    assert deposit['files'] == [
        {'path': 'output/pdf/paper.pdf', 'name': 'paper.pdf'},
        {'path': 'output/source-and-verification.zip',
         'name': 'source-and-verification.zip'},
    ]
    metadata = {'metadata': deposit['metadata']}
    pdf = (ROOT / 'output/pdf/paper.pdf').read_bytes()
    assert pdf.startswith(b'%PDF-') and len(pdf) > 10000
    items = {}
    root_names = ['paper.tex', 'README.md', 'LICENSES.md',
                  'build_package.py', 'zenodo-deposit.json']
    for name in root_names:
        items[name] = (ROOT / name).read_bytes()
    # Whitelist original author artifacts and documentary evidence. Publisher
    # downloads and extracted third-party full texts are not redistributed.
    for folder in ['verification', 'reviews', 'priority']:
        for path in sorted((ROOT / folder).rglob('*')):
            if not path.is_file() or path.is_symlink():
                continue
            relative = path.relative_to(ROOT)
            if any(part.startswith('.') for part in relative.parts):
                continue
            if any(part in {'__pycache__', 'tmp', 'documents'}
                   for part in relative.parts):
                continue
            allowed = {'.md', '.json', '.py', '.tex', '.jsonl'}
            if folder == 'verification':
                allowed |= {'.txt', '.pdf'}
            if path.suffix not in allowed:
                continue
            items[relative.as_posix()] = path.read_bytes()
    items['api-metadata.json'] = encode(metadata)
    # Build evidence can bind the PDF without including another copy in sources.
    inventory = {
        'format': 'sha256-file-inventory-v1',
        'paper_pdf': {'name': 'paper.pdf', 'sha256': sha(pdf), 'size': len(pdf)},
        'files': {name: {'sha256': sha(data), 'size': len(data)}
                  for name, data in sorted(items.items())},
        'exclusions': ['publication receipts', 'credentials', 'environments',
                       'third-party source PDFs and full-text extracts', 'scratch'],
    }
    items['PACKAGE_MANIFEST.json'] = encode(inventory)
    out = ROOT / 'output'
    out.mkdir(exist_ok=True)
    inner = out / 'source-and-verification.zip'
    archive(inner, items)
    files = {'paper.pdf': pdf, 'source-and-verification.zip': inner.read_bytes()}
    checksum_lines = ''.join(f'{sha(data)}  {name}\n'
                             for name, data in sorted(files.items()))
    kit = dict(files)
    kit['api-metadata.json'] = encode(metadata)
    kit['zenodo-deposit.json'] = encode({
        'metadata': deposit['metadata'],
        'files': [{'path': name, 'name': name} for name in files],
    })
    kit['SHA256SUMS'] = checksum_lines.encode()
    kit['UPLOAD.md'] = (
        '# Zenodo upload kit\n\n'
        'Upload only paper.pdf and source-and-verification.zip. '
        'Use the metadata object in api-metadata.json exactly. '
        'The root repository manifest is the canonical live-deposit path; '
        'the kit manifest is an offline convenience and must not create a '
        'second deposit after staging has begun.\n\n'
        'Check SHA256SUMS before uploading. The source archive includes its '
        'own inventory and binds this PDF. It contains source, pinned exact '
        'checks, source provenance, priority evidence, and AI adversarial '
        'reviews. Review status and AI disclosure are explicit in the paper '
        'and metadata. DOI and publication receipts are recorded separately '
        'after publication.\n'
    ).encode()
    archive(out / 'zenodo-upload-kit.zip', kit)
    (out / 'api-metadata.json').write_bytes(encode(metadata))
    (out / 'SHA256SUMS').write_text(checksum_lines)
    report = {
        'state': 'built_and_verified_locally',
        'metadata_sha256': sha(encode(metadata)),
        'source_members': len(items),
        'deposited_files': {name: {'sha256': sha(data), 'size': len(data)}
                            for name, data in sorted(files.items())},
        'kit_sha256': sha((out / 'zenodo-upload-kit.zip').read_bytes()),
    }
    (out / 'package-build.json').write_bytes(encode(report))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
