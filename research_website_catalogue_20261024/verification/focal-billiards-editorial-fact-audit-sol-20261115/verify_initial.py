"""Pure source/root-only custody. No project imports, science, subprocess, network or writes."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import sys
import zipfile

O = Path(__file__).resolve().parent
S = O.parent.parent / 'papers/23306203/sources'
N = 0


def need(value, reason):
    global N
    N += 1
    if not value:
        raise ValueError(reason)


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
    need(type(a) is type(b), 'literal native type')
    if isinstance(a, dict):
        need(list(a) == list(b), 'whole ordered keys')
        for key in a:
            typed(a[key], b[key])
    elif isinstance(a, list):
        need(len(a) == len(b), 'whole ordered array')
        for left, right in zip(a, b):
            typed(left, right)
    else:
        need(a == b, 'whole scalar')


def main():
    need(not sys.argv[1:], 'pure default initial options')
    for row in obj(O / 'INITIAL_SEAL.json')['payloads']:
        rel = PurePosixPath(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts and str(rel) == row['path'], 'safe initial payload')
        pin(O / rel, row)
    source = obj(O / 'INITIAL_SOURCE_MANIFEST.json')
    paths = list(S.rglob('*'))
    need(S.resolve() == S and not S.is_symlink()
         and all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in paths), 'whole ordinary source namespace')
    need(sorted(p.relative_to(S).as_posix() for p in paths if p.is_file())
         == [row['path'] for row in source['files']], 'strict full source files')
    need(sorted(p.relative_to(S).as_posix() for p in paths if p.is_dir())
         == source['exact_relative_directories'], 'strict full source directories')
    need(len(source['files']) == 66, 'all66 actual source files')
    for row in source['files']:
        pin(S / row['path'], row)
    inputs = obj(O / 'INITIAL_INPUT_BINDINGS.json')
    for row in inputs['root_files']:
        pin(Path(row['path']), row)
    saved = obj(O / 'INITIAL_NATIVE_INPUTS.json')
    for row in saved['whole_source_JSON_objects']:
        typed(row['whole_object'], obj(S / row['relative_path']))
    root = obj(Path(inputs['root_clearance_path']))
    typed(root, saved['whole_root_clearance'])
    ready = obj(S / 'SOURCE_READY.json')
    typed(root['whole_original_SOURCE_READY_unchanged'], ready)
    record = obj(S / 'record.response.body')
    need(record['metadata']['description'] == saved['whole_native_deposit_description_HTML'], 'whole native description')
    need(len(re.findall('<p>', record['metadata']['description'])) == 4, 'all4 original description paragraphs')
    need([row['key'] for row in record['files']] == ['focal_product_support.zip', 'focal_product_period_criterion.pdf'], 'ZIP then PDF')
    need(record['metadata']['version'] == '1.0.0' and record['metadata']['publication_date'] == '2026-10-11', 'native edition')
    tex = read(Path(ready['controlling_TeX']['extracted_path'])).decode()
    need(len(tex.splitlines()) == 307, 'all307 TeX lines')
    need(re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S)[1]
         == saved['whole_printed_TeX_abstract'], 'distinct complete printed abstract')
    need('\\date{11 October 2026}' in tex and 'version' not in tex.lower(), 'printed date and absence of version statement')
    need(ready['embedded_PDFs'] == [] and ready['actual_standalone_TeX_assets'] == [], 'no embedded PDF or native standalone TeX')
    archive = obj(S / 'ARCHIVE_CUSTODY.json')
    need(len(archive['regular_payload_occurrences']) == 13, 'all13 regular ZIP payloads')
    with zipfile.ZipFile(S / 'assets/focal_product_support.zip') as zipped:
        infos = zipped.infolist()
        need(len(infos) == len(archive['containers'][0]['members']), 'whole ZIP member extent')
        for row in archive['regular_payload_occurrences']:
            info = infos[row['ordinal_zero_based']]
            body = zipped.read(info)
            need(info.filename == row['original_member_name'] and not info.is_dir(), 'ordered original member')
            need(body == pin(Path(row['extracted_path']), row), 'whole original member/extracted identity')
            need((f'{info.CRC:08x}', info.compress_size, info.compress_type, info.external_attr,
                  info.create_system, info.flag_bits, list(info.date_time))
                 == (row['CRC32'], row['compressed_bytes'], row['compression_method'], row['native_external_attr'],
                     row['native_create_system'], row['native_flags'], row['native_date_time']), 'whole native archive metadata')
            need(not body.startswith(b'%PDF-'), 'no hidden embedded PDF payload')
    license_body = read(S / 'published-source/asset-001/LICENSE.md').decode()
    need(license_body == saved['whole_actual_license_text'] and 'verification materials' in license_body
         and 'same terms' in license_body, 'actual broad authored support/code CC BY instrument')
    need(ready['mathematical_PDF_TeX_or_pixels_read'] is False and ready['scientific_verdict'] is None
         and ready['printed_version'] is None, 'historical unread/null fields remain literal')
    print(json.dumps({'status': 'PASS_FOCAL_BILLIARDS_SOURCE_ROOT_ONLY_INITIAL_CUSTODY', 'checks': N,
                      'source_files': 66, 'ZIP_payloads': 13, 'editorial_output_listed_or_read': False,
                      'native_version': '1.0.0', 'printed_version_observed': 'ABSENT',
                      'source_science_authoring_network_project_imports_subprocess_or_writes': False}, sort_keys=True))


if __name__ == '__main__':
    main()
