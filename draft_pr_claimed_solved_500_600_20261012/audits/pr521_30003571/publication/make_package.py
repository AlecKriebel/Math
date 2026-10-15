#!/usr/bin/env python3
"""Build an explicit authored-source archive; downloaded source papers are excluded."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

PUB = Path(__file__).resolve().parent
AUDIT = PUB.parent
PROGRAM = AUDIT.parent.parent
ORIGINAL = AUDIT / 'original/unsolved_math_prioritization/attempts/30003571'


def main():
    required = [AUDIT / 'reviews/flow01/INDEPENDENT_FLOW_REVIEW.md',
                AUDIT / 'reviews/geometry01/REPORT.md',
                AUDIT / 'reviews/source01/SOURCE_AUDIT.md']
    for p in required:
        if not p.is_file():
            raise RuntimeError(f'Required review is absent: {p}')
    scratch = PROGRAM / 'tmp'
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='package-build-', dir=scratch) as tmp:
        root = Path(tmp) / 'positivity-loss-30003571'
        root.mkdir()
        shutil.copytree(ORIGINAL, root / 'original')
        for name in ['positivity_loss.tex', 'README.md', 'CORRECTIONS.md']:
            (root / 'paper').mkdir(exist_ok=True)
            shutil.copyfile(PUB / name, root / 'paper' / name)
        for name in ['run_all.py', 'requirements.txt']:
            shutil.copyfile(PUB / name, root / name)
        # Only authored review formats are allowed. Copyrighted papers and
        # full extracted text are intentionally ineligible, even if adjacent.
        for folder in sorted((AUDIT / 'reviews').iterdir()):
            if not folder.is_dir():
                continue
            # Complete-package reviews refer to a frozen ZIP, so keep their
            # reports beside it in the public repository, outside that ZIP.
            # This avoids a self-referential review/hash cycle.
            if folder.name.startswith('package'):
                continue
            for p in sorted(folder.rglob('*')):
                if any(part in {'sources', 'records', '__pycache__'} for part in p.relative_to(folder).parts):
                    continue
                if p.is_file() and p.suffix in {'.md', '.py', '.json'}:
                    dest = root / 'reviews' / folder.name / p.relative_to(folder)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(p, dest)
        shutil.copytree(AUDIT / 'root_reproduction', root / 'root_reproduction')
        for name in ['PRIMARY_SOURCE_RECEIPT.json', 'ROOT_MATH_ASSESSMENT.md']:
            shutil.copyfile(AUDIT / name, root / name)
        items = {}
        for p in sorted(root.rglob('*')):
            if p.is_file():
                data = p.read_bytes()
                items[str(p.relative_to(root))] = {'bytes': len(data),
                    'sha256': hashlib.sha256(data).hexdigest()}
        manifest = {'version': '1.0', 'problem_id': 30003571, 'pr': 521,
                    'original_head': '91385a9ba0d445a2fae4629cd60b70026584e24b',
                    'paper_pdf_sha256': hashlib.sha256((PUB / 'positivity_loss.pdf').read_bytes()).hexdigest(),
                    'files': items,
                    'manifest_hash_convention': 'Manifest excludes itself; outer ZIP and PDF hashes are independently recorded.'}
        (root / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
        archive = PUB / 'verification_package.zip'
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for p in sorted(root.rglob('*')):
                if not p.is_file():
                    continue
                info = zipfile.ZipInfo(str(p.relative_to(root.parent)), date_time=(2026, 10, 12, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                z.writestr(info, p.read_bytes())
        shutil.copyfile(root / 'MANIFEST.json', PUB / 'PACKAGE_MANIFEST.json')
        print(json.dumps({'archive': str(archive), 'files': len(items) + 1,
                          'bytes': archive.stat().st_size,
                          'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
                          'paper_pdf_sha256': manifest['paper_pdf_sha256']}))


if __name__ == '__main__':
    main()
