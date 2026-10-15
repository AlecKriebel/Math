#!/usr/bin/env python3
"""Build deterministic, positive-inventory archives for the PR421 preprint."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

HERE = Path(__file__).resolve().parent
CASE = HERE.parent
FORBIDDEN = {'private', 'private_sources', 'private_cases', 'mutation_fixtures',
             '__pycache__', '.venv', 'venv', '.secrets', '.zenodo-state'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def checked(path):
    require(path.is_file() and not path.is_symlink(), 'Not a regular file: ' + str(path))
    require(path.resolve().is_relative_to(CASE), 'Outside selected case')
    require(not any(x in FORBIDDEN for x in path.relative_to(CASE).parts), 'Private path')
    require(path.suffix != '.pyc', 'Bytecode excluded')
    return path.read_bytes()


def archive(name, payloads):
    target = HERE / name
    require(len(payloads) == len(set(payloads)), 'Duplicate archive member')
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for member, data in sorted(payloads.items()):
            require(not member.startswith('/') and '..' not in Path(member).parts, 'Unsafe member')
            info = zipfile.ZipInfo(member, date_time=(2026, 10, 12, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(target) as z:
        require(z.namelist() == sorted(payloads), 'Archive member mismatch')
        require(z.testzip() is None, 'Archive CRC failure')
        for member, data in payloads.items():
            require(z.read(member) == data, 'Archive byte mismatch: ' + member)
    return {'path': name, 'bytes': target.stat().st_size,
            'sha256': digest(target.read_bytes()),
            'members': [{'path': member, 'bytes': len(data), 'sha256': digest(data)}
                        for member, data in sorted(payloads.items())]}


def main():
    source = HERE / 'source'
    source.mkdir(exist_ok=True)
    for name in ('preprint.tex', 'BIBLIOGRAPHY_POINTERS.json'):
        data = checked(CASE / 'preprint' / name)
        (source / name).write_bytes(data)
    source_payloads = {name: checked(source / name) for name in
                       ('preprint.tex', 'README.md', 'LICENSE', 'BIBLIOGRAPHY_POINTERS.json')}
    verification = CASE / 'verification'
    whitelist_data = checked(verification / 'PUBLIC_OUTPUT_WHITELIST.json')
    whitelist = json.loads(whitelist_data)
    payloads = {}
    for row in whitelist['files']:
        name = row['path']
        require(name not in payloads and name != 'PUBLIC_OUTPUT_WHITELIST.json', 'Duplicate/self record')
        require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe verification path')
        data = checked(verification / name)
        require(len(data) == row['bytes'] and digest(data) == row['sha256'],
                'Verification whitelist drift: ' + name)
        payloads[name] = data
    payloads['PUBLIC_OUTPUT_WHITELIST.json'] = whitelist_data
    actual = {p.relative_to(verification).as_posix() for p in verification.rglob('*') if p.is_file()}
    require(actual == set(payloads), 'Verification inventory drift')
    manifest = json.loads(checked(HERE / 'zenodo-deposit.json'))
    pdf = checked(CASE / 'output/pdf/preprint.pdf')
    qa = json.loads(checked(CASE / 'ROOT_PDF_VISUAL_QA.json'))
    require(qa['layout_pass'] and qa['pdf_sha256'] == digest(pdf), 'PDF QA mismatch')
    require(qa['source_sha256'] == digest(source_payloads['preprint.tex']), 'Source/PDF QA mismatch')
    built = [archive('aim_5_2_source.zip', source_payloads),
             archive('aim_5_2_verification.zip', payloads)]
    built.append({'path': '../output/pdf/preprint.pdf', 'bytes': len(pdf), 'sha256': digest(pdf)})
    require({x['path'] for x in built} == {x['path'] for x in manifest['files']}, 'Deposit inventory differs')
    record = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'positive_inventories_only': True, 'foreign_sources_included': False,
              'pdf_source_sha256': digest(source_payloads['preprint.tex']), 'files': built,
              'metadata_sha256': digest(checked(HERE / 'zenodo-deposit.json')),
              'publication_ready': False, 'pending': 'two sequential whole-package reviews'}
    (HERE / 'ARCHIVE_INVENTORY.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'archives': [{k: v for k, v in x.items() if k != 'members'} for x in built],
                      'zenodo_mutations': False}, indent=2))


if __name__ == '__main__':
    main()
