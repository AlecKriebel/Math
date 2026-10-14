#!/usr/bin/env python3
"""Deterministic authored archive; primary downloads and private state excluded."""
import datetime
import hashlib
import json
from pathlib import Path
import stat
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    payload = {}
    def add(name, path, expected=None):
        if name in payload or not stat.S_ISREG(path.lstat().st_mode):
            raise RuntimeError('duplicate or nonregular input: ' + name)
        raw = path.read_bytes()
        if expected and (len(raw) != expected['bytes'] or digest(raw) != expected['sha256']):
            raise RuntimeError('frozen source changed: ' + name)
        payload[name] = raw
    for name in ['README.md', 'note.tex', 'metadata.json', 'CURRENT_PRIORITY.md', 'verify_package.py']:
        add(name, HERE / name)
    add('note.pdf', HERE / 'output/pdf/note.pdf')
    source = json.loads((AUDIT / 'SOURCE_MANIFEST.json').read_bytes())
    if source['original_head'] != 'c9fd5a0462d1fa98f21aa7037f7a5e061fbbee9c':
        raise RuntimeError('wrong original head')
    for row in source['files']:
        add('source/' + row['path'], AUDIT / 'source' / row['path'], row)
    for name in ['geometry_audit_01', 'trace_audit_01']:
        folder = AUDIT / name
        for path in sorted(folder.iterdir()):
            if path.is_file() and path.suffix in {'.md', '.json', '.jsonl', '.py'}:
                add(name + '/' + path.name, path)
    priority = json.loads((AUDIT / 'priority_audit_01/PUBLIC_MANIFEST.json').read_bytes())
    for row in priority['files']:
        name = row['relative_public_path']
        add('priority_audit_01/' + name, AUDIT / 'priority_audit_01' / name, row)
    add('priority_audit_01/PUBLIC_MANIFEST.json', AUDIT / 'priority_audit_01/PUBLIC_MANIFEST.json')
    root_names = ['SOURCE_MANIFEST.json', 'CLAIM_AND_SUCCESS_CRITERIA.json',
                  'ROOT_INDEPENDENT_RECONSTRUCTION.md', 'ROOT_PRIMARY_RETRIEVAL.json',
                  'ROOT_REPLAY_RESULTS.json', 'ROOT_FRESH_TRACE_REPLAY.json',
                  'ROOT_FRESH_GEOMETRY_REPLAY.json', 'ROOT_PRIORITY_RECEIPT_REPLAY.json',
                  'ROOT_CONFORMAL_PERTURBATION_PRIORITY_CHECK.md', 'ROOT_ZHAO_RETRIEVAL.json',
                  'ROOT_AJ_SOURCE_CHECK.json', 'ROOT_CLASSICAL_CYLINDER_PRIORITY_CHALLENGE.md',
                  'ROOT_PRIORITY_SEARCH_LEDGER.json', 'MORPURGO_2002_BIBLIOGRAPHIC_CHECK.json',
                  'MATHEMATICAL_ACCEPTANCE.json', 'PRIORITY_DISPOSITION.json']
    for name in root_names:
        add('root_evidence/' + name, AUDIT / name)
    index = {'schema': 'weighted-yamabe-preprint-v1', 'problem_id': 30001168,
             'original_head': source['original_head'],
             'analytic_proof_verified_by_program': False, 'priority_verified_by_program': False,
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
               'pdf_sha256': digest(payload['note.pdf']), 'original_source_files_preserved': 42,
               'downloaded_primary_content_distributed': False}
    (HERE / 'BUILD_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
