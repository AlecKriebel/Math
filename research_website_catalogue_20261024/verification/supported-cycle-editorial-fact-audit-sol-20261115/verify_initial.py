"""Offline source/root-only custody. No project imports, subprocess, network or writes."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys
import zipfile

O = Path(__file__).resolve().parent
S = O.parent.parent / 'papers/23578142/sources'
COUNT = 0


def need(value, why):
    global COUNT
    COUNT += 1
    if not value:
        raise ValueError(why)


def read(path):
    need(path.is_file() and not path.is_symlink() and path.resolve() == path, 'real regular input')
    return path.read_bytes()


def obj(path):
    return json.loads(read(path))


def pin(path, row):
    body = read(path)
    need(len(body) == row['bytes'] and hashlib.sha256(body).hexdigest() == row['SHA256'], 'whole-byte pin')
    return body


def typed(a, b):
    need(type(a) is type(b), 'exact native type')
    if isinstance(a, dict):
        need(list(a) == list(b), 'whole ordered object keys')
        for key in a:
            typed(a[key], b[key])
    elif isinstance(a, list):
        need(len(a) == len(b), 'whole ordered array')
        for left, right in zip(a, b):
            typed(left, right)
    else:
        need(a == b, 'whole scalar')


def main():
    need(not sys.argv[1:], 'default pure initial options')
    seal = obj(O / 'INITIAL_SEAL.json')
    for row in seal['payloads']:
        rel = PurePosixPath(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts and str(rel) == row['path'], 'safe initial path')
        pin(O / rel, row)
    inventory = obj(O / 'INITIAL_SOURCE_MANIFEST.json')
    entries = list(S.rglob('*'))
    need(not S.is_symlink() and S.resolve() == S
         and all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in entries), 'whole regular source namespace')
    need(sorted(p.relative_to(S).as_posix() for p in entries if p.is_file())
         == [r['path'] for r in inventory['files']], 'whole closed source77 extent')
    need(sorted(p.relative_to(S).as_posix() for p in entries if p.is_dir())
         == inventory['exact_relative_directories'], 'whole source directories')
    need(len(inventory['files']) == 77, 'source77 distinct files')
    for row in inventory['files']:
        pin(S / row['path'], row)
    bindings = obj(O / 'INITIAL_INPUT_BINDINGS.json')
    for row in bindings['root_files']:
        pin(Path(row['path']), row)
    saved = obj(O / 'INITIAL_NATIVE_INPUTS.json')
    for item in saved['whole_source_JSON_objects']:
        typed(item['whole_object'], obj(S / item['relative_path']))
    clearance = obj(Path(bindings['root_clearance_path']))
    typed(saved['whole_root_clearance'], clearance)
    typed(clearance['source_native_ready_whole_unchanged'], obj(S / 'SOURCE_READY.json'))
    native = obj(S / 'record.response.body')
    need(native['metadata']['description'] == saved['native_abstract_HTML'], 'entire exact native abstract')
    need([item['key'] for item in native['files']] == ['supported-cycle-source-and-verification.zip',
                                                     'supported-cycle-bound.pdf'], 'original ZIP/PDF order')
    need(native['metadata']['version'] == '1.0.0' and native['metadata']['publication_date'] == '2026-10-22', 'edition')
    archive = obj(S / 'ARCHIVE_CUSTODY.json')
    occurrences = archive['regular_payload_occurrences']
    need(len(occurrences) == 27, 'whole27 archive occurrences')
    with zipfile.ZipFile(S / 'assets/supported-cycle-source-and-verification.zip') as zipped:
        infos = zipped.infolist()
        need(len(infos) == len(archive['containers'][0]['members']), 'complete ZIP member extent')
        for row in occurrences:
            info = infos[row['ordinal_zero_based']]
            need(info.filename == row['original_member_name'] and not info.is_dir(), 'whole ordered ZIP name')
            body = zipped.read(info)
            need(len(body) == row['bytes'] and hashlib.sha256(body).hexdigest() == row['SHA256'], 'whole ZIP payload')
            need(body == read(Path(row['extracted_path'])), 'actual original extracted bytes')
            need((f'{info.CRC:08x}', info.compress_size, info.compress_type, info.external_attr,
                  info.create_system, info.flag_bits, list(info.date_time))
                 == (row['CRC32'], row['compressed_bytes'], row['compression_method'], row['native_external_attr'],
                     row['native_create_system'], row['native_flags'], row['native_date_time']), 'whole ZIP native metadata')
    ready = obj(S / 'SOURCE_READY.json')
    need(len(read(Path(ready['controlling_TeX']['extracted_path'])).splitlines()) == 391, 'actual391 TeX lines')
    need(read(Path(ready['embedded_PDFs'][0]['extracted_path'])) == read(Path(ready['selected_actual_PDF']['path'])), 'whole embedded/standalone PDF identity')
    need(ready['mathematical_PDF_TeX_or_pixels_read'] is False
         and ready['scientific_verdict'] is None and ready['publication_authority'] is False, 'historical fields unchanged')
    print(json.dumps({'status': 'PASS_SOURCE_ROOT_ONLY_INITIAL_CUSTODY', 'checks': COUNT,
                      'source_files': 77, 'ZIP_payloads': 27, 'editorial_output_read': False,
                      'source_scientific_or_historical_execution': False,
                      'network_subprocess_project_imports_or_writes': False}, sort_keys=True))


if __name__ == '__main__':
    main()
