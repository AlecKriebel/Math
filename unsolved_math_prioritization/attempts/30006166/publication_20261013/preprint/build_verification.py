#!/usr/bin/env python3
"""Assemble an explicit authored release; exclude downloaded primary content."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import stat
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent


def digest(content):
    return hashlib.sha256(content).hexdigest()


def main():
    payload = {}
    def add(name, path):
        if name in payload:
            raise RuntimeError('duplicate release member: ' + name)
        if not stat.S_ISREG(path.lstat().st_mode):
            raise RuntimeError('nonregular input: ' + str(path))
        payload[name] = path.read_bytes()
    for name in ['README.md', 'note.tex', 'metadata.json', 'CURRENT_PRIORITY.md', 'verify_package.py']:
        add(name, HERE / name)
    add('note.pdf', HERE / 'output/pdf/note.pdf')
    source = json.loads((AUDIT / 'SOURCE_MANIFEST.json').read_bytes())
    if source['source_head'] != '5bee5139501a399da653f634147eab9433774ac7':
        raise RuntimeError('frozen head changed')
    for row in source['files']:
        path = AUDIT / row['path']
        raw = path.read_bytes()
        if len(raw) != row['bytes'] or digest(raw) != row['sha256']:
            raise RuntimeError('original source changed: ' + row['path'])
        add(row['path'], path)
    for input_folder, output_folder in [('category_audit_01', 'category'),
                                         ('slab_audit_01', 'slab'), ('priority_audit_01', 'priority')]:
        folder = AUDIT / input_folder
        for path in sorted(folder.rglob('*')):
            relative = path.relative_to(folder)
            if 'private_sources' in relative.parts or 'tmp' in relative.parts:
                continue
            if path.is_file() and path.suffix in {'.md', '.json', '.py'}:
                add('audits/' + output_folder + '/' + relative.as_posix(), path)
    names = ['SOURCE_MANIFEST.json', 'CLAIM_AND_SUCCESS_CRITERIA.json',
             'ROOT_INDEPENDENT_MATHEMATICAL_RECONSTRUCTION.md', 'ROOT_PRIMARY_RETRIEVAL.json',
             'ROOT_REPLAY_RESULTS.json', 'ROOT_FRESH_SLAB_REPLAY.json', 'ROOT_TARGET_RECORD_CHECK.json',
             'ROOT_ALMOST_FINITE_SOURCE_RETRIEVAL.json', 'ROOT_ALMOST_FINITE_PRIORITY_CHECK.md',
             'ROOT_DIMENSION_GROWTH_PRIORITY_CHECK.md', 'ROOT_PRIORITY_SEARCH_LEDGER.json',
             'MATHEMATICAL_ACCEPTANCE.json']
    for name in names:
        add('root_evidence/' + name, AUDIT / name)
    index = {'schema': 1, 'problem_id': 30006166,
             'source_head': source['source_head'],
             'infinite_theorem_verified_by_program': False,
             'files': [{'path': name, 'bytes': len(raw), 'sha256': digest(raw)}
                       for name, raw in sorted(payload.items())]}
    index_raw = (json.dumps(index, indent=2, sort_keys=True) + '\n').encode()
    payload['package_index.json'] = index_raw
    (HERE / 'package_index.json').write_bytes(index_raw)
    with zipfile.ZipFile(HERE / 'verification.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, raw in sorted(payload.items()):
            info = zipfile.ZipInfo(name, (2026, 10, 13, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, raw)
    receipt = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'members': len(payload), 'index_sha256': digest(index_raw),
               'zip_sha256': digest((HERE / 'verification.zip').read_bytes()),
               'zip_bytes': (HERE / 'verification.zip').stat().st_size,
               'pdf_sha256': digest(payload['note.pdf']),
               'original_source_files_preserved': len(source['files']),
               'downloaded_primary_content_distributed': False}
    (HERE / 'BUILD_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
