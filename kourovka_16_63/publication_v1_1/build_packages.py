#!/usr/bin/env python3
"""Build the focused v1.1.0 source archive and manual Zenodo upload kit.
Run from this repository; no network access. Does not publish to Zenodo.
"""
from pathlib import Path
import hashlib
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT.parent / 'docs' / 'papers' / 'kourovka-16-63'
KIT = ROOT / 'publication_v1_1' / 'upload-kit'
VERSION = '1.1.0'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def selected(path):
    rel = path.relative_to(ROOT)
    if not path.is_file() or path.name in {'.DS_Store', 'SHA256SUMS'}:
        return False
    if '__pycache__' in rel.parts or path.suffix == '.pyc':
        return False
    excluded = ('build/', 'audit/computation_work/', 'audit/pdf_preview/',
                'publication_v1_1/upload-kit/', 'publication_v1_1/post_deployment/')
    if any(rel.as_posix().startswith(prefix) for prefix in excluded):
        return False
    if rel.as_posix() in {'audit/kourovka_source.pdf', 'audit/kourovka_source.txt'}:
        return False
    if rel.parts[0] == 'report' and path.suffix in {'.log', '.aux', '.out', '.toc'}:
        return False
    return True


def make_zip(path, entries):
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(entries):
            info = zipfile.ZipInfo(name, (2026, 9, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None


def main():
    PAGE.mkdir(parents=True, exist_ok=True)
    selected_files = sorted(p for p in ROOT.rglob('*') if selected(p))
    manifest = ''.join(f'{digest(p.read_bytes())}  {p.relative_to(ROOT).as_posix()}\n'
                       for p in selected_files)
    (ROOT / 'SHA256SUMS').write_text(manifest)
    selected_files.append(ROOT / 'SHA256SUMS')
    source = PAGE / 'source-and-certificates.zip'
    make_zip(source, [('kourovka_16_63/' + p.relative_to(ROOT).as_posix(), p.read_bytes())
                      for p in selected_files])
    paper = ROOT / 'report' / 'kourovka_16_63.pdf'
    shutil.copyfile(paper, PAGE / 'paper.pdf')
    uploads = KIT / 'UPLOAD_THESE_FILES'
    uploads.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(paper, uploads / f'kourovka_16_63_v{VERSION}.pdf')
    shutil.copyfile(source, uploads / f'kourovka_16_63_v{VERSION}_source-and-certificates.zip')
    for p in (ROOT / 'publication_v1_1' / 'zenodo').iterdir():
        if p.is_file():
            shutil.copyfile(p, KIT / p.name)
    (KIT / 'UPLOAD_SHA256SUMS.txt').write_text(''.join(
        f'{digest(p.read_bytes())}  UPLOAD_THESE_FILES/{p.name}\n'
        for p in sorted(uploads.iterdir())))
    kit_zip = PAGE / 'zenodo-upload-kit.zip'
    make_zip(kit_zip, [(p.relative_to(KIT).as_posix(), p.read_bytes())
                       for p in KIT.rglob('*') if p.is_file()])
    with zipfile.ZipFile(source) as z:
        for line in manifest.splitlines():
            expected, name = line.split(maxsplit=1)
            assert digest(z.read('kourovka_16_63/' + name)) == expected
        assert z.read('kourovka_16_63/report/kourovka_16_63.pdf') == paper.read_bytes()
    for p in (PAGE / 'paper.pdf', source, kit_zip):
        print(f'{digest(p.read_bytes())}  {p.name}  ({p.stat().st_size} bytes)')
    print(f'Source package: {len(selected_files)} files; all manifest entries verified.')


if __name__ == '__main__':
    main()
