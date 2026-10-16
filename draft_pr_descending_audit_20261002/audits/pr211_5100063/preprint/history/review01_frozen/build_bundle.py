"""Rebuild deterministic source ZIP from already prepared, explicitly selected inputs.

This is packaging, not proof checking, review clearance or publication.
No provider, Git, queue, database or private source is accessed.
"""
from pathlib import Path
import hashlib
import json
import zipfile

BASE = Path(__file__).resolve().parent
FORBIDDEN = {'private', 'private_reading', 'private_transport', '__pycache__'}


def pin(path, base):
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    return dict(path=path.relative_to(base).as_posix(), bytes=len(raw),
                sha256=hashlib.sha256(raw).hexdigest())


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    native = BASE / 'pr_update/5100063'
    # Original historical manifests are archived verbatim. Current ones bind
    # the reconciled presentation and do not reuse old review-proof bindings.
    subset = [pin(p, native) for p in sorted(native.iterdir()) if p.is_file()
              and p.name not in {'MANIFEST.json', 'PUBLICATION_MANIFEST.json', 'CURRENT_PACKET_MANIFEST.json'}]
    for name in ['MANIFEST.json', 'PUBLICATION_MANIFEST.json']:
        save(native/name, dict(scope='Current reconciled top-level presentation; original inherited bindings preserved under history/original_submission_20261015', files=subset))
    rows = [pin(p, native) for p in sorted(native.rglob('*')) if p.is_file()
            and p.name != 'CURRENT_PACKET_MANIFEST.json']
    save(native/'CURRENT_PACKET_MANIFEST.json', dict(schema='pr211-reconciled-packet-v1', self_excluded=True,
        source_head='9d7b623203b525386da3d9d91548c79e7445a11c', files=rows))
    selected = [BASE/n for n in ['manuscript.tex', 'manuscript.pdf', 'metadata.json', 'README.md', 'build_bundle.py']]
    for folder in ['verification', 'pr_update']:
        for path in sorted((BASE/folder).rglob('*')):
            if path.is_symlink() or set(path.relative_to(BASE).parts) & FORBIDDEN:
                raise ValueError('Unsafe selected payload: '+str(path))
            if path.is_file():
                selected.append(path)
    selected = sorted(set(selected))
    source = dict(schema='pr211-source-archive-sha256-v1', self_excluded=True,
        scope='Manuscript, metadata, reconciled planned native presentation and portable verification; exact original submission preserved. No third-party primary payloads.',
        files=[pin(p, BASE) for p in selected])
    save(BASE/'SOURCE_MANIFEST.json', source)
    selected.append(BASE/'SOURCE_MANIFEST.json')
    archive = BASE/'k904a-source-verification.zip'
    prefix = 'k904a_outer_focal_inverse_product/'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(selected):
            name = prefix+p.relative_to(BASE).as_posix()
            info = zipfile.ZipInfo(name, date_time=(2026,10,15,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, p.read_bytes())
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == len(selected) == len(set(z.namelist()))
        for p in selected:
            assert z.read(prefix+p.relative_to(BASE).as_posix()) == p.read_bytes()
    save(BASE/'PACKAGE_MANIFEST.json', dict(schema='pr211-submission-bundle-v1',
        source_manifest=pin(BASE/'SOURCE_MANIFEST.json',BASE),
        submission_files=[pin(BASE/'manuscript.pdf',BASE),pin(archive,BASE)],
        manuscript_source=pin(BASE/'manuscript.tex',BASE),metadata=pin(BASE/'metadata.json',BASE),
        source_archive_entries=len(selected), whole_package_review_clearance=False))
    save(BASE/'deposit.json', dict(metadata=json.loads((BASE/'metadata.json').read_text()),
        files=[dict(path='manuscript.pdf',name='k904a-outer-focal-inverse-areas.pdf'),
               dict(path=archive.name,name=archive.name)]))
    print(json.dumps(json.loads((BASE/'PACKAGE_MANIFEST.json').read_text()),indent=2))


if __name__ == '__main__':
    main()
