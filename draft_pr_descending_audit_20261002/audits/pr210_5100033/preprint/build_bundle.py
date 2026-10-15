"""Deterministically seal the prepared local submission; no publication or external calls.

Whole-manuscript reviews and actual release receipts are recorded alongside the
case, outside this dated source ZIP, so a review can bind the exact final ZIP
without a self-referential archive containing its own approval/hash.
"""
from pathlib import Path
import hashlib
import json
import zipfile

BASE = Path(__file__).resolve().parent
FORBIDDEN = {'private', 'private_reading', 'private_transport', 'private_upstream', '__pycache__'}


def pin(path, base):
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    return dict(path=path.relative_to(base).as_posix(), bytes=len(raw),
                sha256=hashlib.sha256(raw).hexdigest())


def save(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def main():
    native = BASE / 'pr_update/5100033'
    top = [pin(p, native) for p in sorted(native.iterdir()) if p.is_file()
           and p.name not in {'MANIFEST.json', 'PUBLICATION_MANIFEST.json', 'CURRENT_PACKET_MANIFEST.json'}]
    for name in ['MANIFEST.json', 'PUBLICATION_MANIFEST.json']:
        save(native/name, dict(scope='Current reconciled top-level presentation; original inherited bindings preserved under history/original_submission_20261015', files=top))
    rows = [pin(p, native) for p in sorted(native.rglob('*')) if p.is_file()
            and p.name != 'CURRENT_PACKET_MANIFEST.json']
    save(native/'CURRENT_PACKET_MANIFEST.json', dict(schema='pr210-reconciled-packet-v1', self_excluded=True,
        source_head='2180d64b648b81ac660a792f7823d0b715f9cf12', files=rows))
    selected = [BASE/n for n in ['manuscript.tex', 'manuscript.pdf', 'metadata.json', 'README.md',
                                'build_bundle.py', 'prepare_native_presentation.py',
                                'NATIVE_RELEASE_PLAN.json', 'RENDER_QA.json', 'apply_review01_fixes.py', 'resume_review01_fixes.py', 'REVIEW01_RESOLUTION.json']]
    for folder in ['verification', 'pr_update']:
        for path in sorted((BASE/folder).rglob('*')):
            if path.is_symlink() or set(path.relative_to(BASE).parts) & FORBIDDEN:
                raise ValueError('Unsafe selected payload: '+str(path))
            if path.is_file():
                selected.append(path)
    selected = sorted(set(selected))
    source = dict(schema='pr210-source-archive-sha256-v1', self_excluded=True,
        scope='Dated prepublication manuscript, metadata, reconciled planned native presentation and portable verification. No third-party primary texts. Required whole-manuscript reviews and final actual release receipts remain alongside the case in the repository audit, outside this source ZIP.',
        files=[pin(p, BASE) for p in selected])
    save(BASE/'SOURCE_MANIFEST.json', source)
    selected.append(BASE/'SOURCE_MANIFEST.json')
    archive = BASE/'k605a-source-verification.zip'
    prefix = 'k605a_outer_focal_pedal_product/'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(selected):
            info = zipfile.ZipInfo(prefix+p.relative_to(BASE).as_posix(), date_time=(2026,10,15,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, p.read_bytes())
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == len(selected) == len(set(z.namelist()))
        for p in selected:
            assert z.read(prefix+p.relative_to(BASE).as_posix()) == p.read_bytes()
    save(BASE/'PACKAGE_MANIFEST.json', dict(schema='pr210-submission-bundle-v1',
        source_manifest=pin(BASE/'SOURCE_MANIFEST.json',BASE),
        submission_files=[pin(BASE/'manuscript.pdf',BASE),pin(archive,BASE)],
        manuscript_source=pin(BASE/'manuscript.tex',BASE), metadata=pin(BASE/'metadata.json',BASE),
        source_archive_entries=len(selected),
        clearance_record_role='This binds prepublication bytes only. Version-bound whole-manuscript reports and later FINAL_CLEARANCE.json/actual release receipts are outside this ZIP; no self-certification.'))
    save(BASE/'deposit.json', dict(metadata=json.loads((BASE/'metadata.json').read_text()),
        files=[dict(path='manuscript.pdf',name='k605a-outer-focal-pedal-areas.pdf'),
               dict(path=archive.name,name=archive.name)]))
    print(json.dumps(json.loads((BASE/'PACKAGE_MANIFEST.json').read_text()),indent=2))


if __name__ == '__main__':
    main()
