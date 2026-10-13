#!/usr/bin/env python3
"""Build a deterministic archive from explicit authored-only inputs."""
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile

PUB = Path(__file__).resolve().parent
AUDIT = PUB.parent


def main():
    files = {}

    def add(name, path):
        data = path.read_bytes()
        if name in files:
            raise RuntimeError(f'Duplicate member: {name}')
        files[name] = data

    for name in ('README.md', 'requirements.txt', 'run_all.py', 'CORRECTIONS.md',
                 'BUILD.json', 'PDF_QA.json', 'ambient_independence.tex'):
        add(name, PUB / name)
    add('metadata.json', PUB / 'zenodo-deposit.json')
    old = AUDIT / 'original/unsolved_math_prioritization/attempts/30001182'
    for p in sorted(old.rglob('*')):
        if p.is_file() and p.suffix in ('.md', '.json', '.py'):
            add('original/' + p.relative_to(old).as_posix(), p)
    for family in ('operator01', 'extension01', 'source01'):
        folder = AUDIT / 'reviews' / family
        for p in sorted(folder.iterdir()):
            if p.is_file() and (p.suffix in ('.md', '.json', '.py')
                                or p.name == '.gitignore'):
                add('reviews/' + family + '/' + p.name, p)
    for p in sorted((AUDIT / 'root_reproduction').iterdir()):
        if p.is_file() and p.suffix in ('.md', '.json', '.py'):
            add('root_reproduction/' + p.name, p)
    add('SOURCE_DOWNLOADS.json', AUDIT / 'root_sources/SOURCES.json')
    for family in ('operator01', 'extension01', 'source01'):
        base = 'reviews/' + family + '/'
        seal = json.loads(files[base + 'MANIFEST.json'])
        for item in seal['files']:
            name = base + item['path']
            if name not in files:
                raise RuntimeError(f'Nested sealed payload omitted: {name}')
            data = files[name]
            if (len(data) != item.get('bytes', item.get('size'))
                    or hashlib.sha256(data).hexdigest() != item['sha256']):
                raise RuntimeError(f'Nested sealed payload inconsistent: {name}')
    manifest = {
        'problem_id': 30001182, 'pr': 533,
        'head': '135911efff1ad14314f0506b0d5f158ba986426f',
        'files': {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                  for name, data in sorted(files.items())},
        'limits': 'Integrity is not a signature; proofs, scope and bounded priority '
                  'limits are essential. Source full texts and account material excluded.',
    }
    files['MANIFEST.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    with tempfile.NamedTemporaryFile(dir=PUB, suffix='.zip', delete=False) as tmp:
        temporary = Path(tmp.name)
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for name, data in sorted(files.items()):
                item = zipfile.ZipInfo('ambient_independence_verification/' + name,
                                       date_time=(2026, 10, 12, 12, 0, 0))
                item.compress_type = zipfile.ZIP_DEFLATED
                item.external_attr = 0o100644 << 16
                z.writestr(item, data)
        temporary.replace(PUB / 'verification_package.zip')
    finally:
        temporary.unlink(missing_ok=True)
    (PUB / 'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    record = {
        'zip_sha256': hashlib.sha256((PUB / 'verification_package.zip').read_bytes()).hexdigest(),
        'zip_bytes': (PUB / 'verification_package.zip').stat().st_size,
        'archive_members': len(files), 'payload_files': len(manifest['files']),
        'pdf_sha256': hashlib.sha256((PUB / 'ambient_independence.pdf').read_bytes()).hexdigest(),
        'source_builder_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (PUB / 'PACKAGE_BUILD.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
