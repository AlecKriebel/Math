#!/usr/bin/env python3
"""Build strict, deterministic source and upload kits with identical metadata."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
STAMP = (2026, 10, 1, 0, 0, 0)


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def archive(path, members):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(members.items()):
            p = PurePosixPath(name)
            assert not p.is_absolute() and '..' not in p.parts
            info = zipfile.ZipInfo(name, date_time=STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        assert sorted(z.namelist()) == sorted(members)
        for name, data in members.items():
            assert z.read(name) == data, name


def main():
    deposit = json.loads((ROOT / 'zenodo-deposit.json').read_text())
    assert set(deposit) == {'metadata', 'files'}
    assert deposit['files'] == [
        {'path': 'output/paper.pdf', 'name': 'paper.pdf'},
        {'path': 'output/source-and-verification.zip',
         'name': 'source-and-verification.zip'},
    ]
    pdf = (ROOT / 'output/paper.pdf').read_bytes()
    assert pdf.startswith(b'%PDF-') and len(pdf) > 10000
    names = json.loads((ROOT / 'public-files.json').read_text())['files']
    assert len(names) == len(set(names))
    members = {}
    for name in names:
        p = PurePosixPath(name)
        assert not p.is_absolute() and '..' not in p.parts
        assert not any(part.startswith('.') for part in p.parts)
        assert not any(part in {'tmp', 'output', '__pycache__', 'documents'}
                       for part in p.parts)
        path = ROOT / name
        assert path.is_file() and not path.is_symlink(), name
        assert path.resolve().is_relative_to(ROOT), name
        assert path.suffix in {'.tex', '.py', '.md', '.json', '.txt'}, name
        members[name] = path.read_bytes()
    api_metadata = encode({'metadata': deposit['metadata']})
    members['api-metadata.json'] = api_metadata
    members['PACKAGE_MANIFEST.json'] = encode({
        'format': 'sha256-file-inventory-v1',
        'paper_pdf': {'name': 'paper.pdf', 'sha256': sha(pdf), 'bytes': len(pdf)},
        'files': {name: {'sha256': sha(data), 'bytes': len(data)}
                  for name, data in sorted(members.items())},
        'exclusions': ['foreign full texts', 'raw publisher and tool responses',
                       'credentials', 'environments', 'scratch',
                       'publication receipts', 'fresh review working folders'],
        'review_binding': 'Separate fresh full reviews bind this exact manuscript '
                          'and archive; reports are preserved in the repository '
                          'program so their inclusion cannot create a hash cycle.',
    })
    out = ROOT / 'output'
    archive(out / 'source-and-verification.zip', members)
    files = {'paper.pdf': pdf,
             'source-and-verification.zip': (out / 'source-and-verification.zip').read_bytes()}
    sums = ''.join(sha(data) + '  ' + name + '\n'
                   for name, data in sorted(files.items())).encode()
    kit = dict(files)
    kit.update({
        'api-metadata.json': api_metadata,
        'zenodo-deposit.json': encode({
            'metadata': deposit['metadata'],
            'files': [{'path': name, 'name': name} for name in files]}),
        'SHA256SUMS': sums,
        'UPLOAD.md': (
            '# Zenodo upload kit\n\nUpload paper.pdf and source-and-verification.zip '
            'with the exact metadata in api-metadata.json. Check SHA256SUMS. '
            'The repository manifest is the canonical live-deposit input; this '
            'offline convenience must never create another deposit once staging '
            'has begun. Fresh complete review reports and publication/DOI '
            'receipts are recorded separately in the repository program. '
            'The source archive inventories every member and binds the PDF.\n').encode(),
    })
    archive(out / 'zenodo-upload-kit.zip', kit)
    (out / 'api-metadata.json').write_bytes(api_metadata)
    (out / 'SHA256SUMS').write_bytes(sums)
    report = {'state': 'built_and_verified_locally',
              'source_members': len(members),
              'metadata_sha256': sha(api_metadata),
              'deposited_files': {name: {'sha256': sha(data), 'bytes': len(data)}
                                  for name, data in sorted(files.items())},
              'kit_sha256': sha((out / 'zenodo-upload-kit.zip').read_bytes())}
    (out / 'package-build.json').write_bytes(encode(report))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
