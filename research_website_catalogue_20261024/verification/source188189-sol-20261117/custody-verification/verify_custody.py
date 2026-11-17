#!/usr/bin/env python3
"""Independent metadata, byte and topology checks; no source interpretation.

This verifier imports no collector or prior helper. Its full actual code must be
printed and read before the sole initial execution. All writes stay in OWN.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import json
import stat
import unicodedata
import zipfile
import zlib

OWN = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/source188189-sol-20261117/custody-verification')
LANE = OWN.parent
PROJECT = LANE.parent.parent
RECORDS = (23203270, 23203081)
CHECKS = 0
STAGE = 'initialization'


def utc():
    return datetime.now(timezone.utc).isoformat()


def demand(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise ValueError('Custody check failed: ' + label)


def stream_pin(stream):
    h256, hmd5, crc, count = hashlib.sha256(), hashlib.md5(), 0, 0
    for block in iter(lambda: stream.read(65536), b''):
        count += len(block)
        h256.update(block)
        hmd5.update(block)
        crc = zlib.crc32(block, crc)
    return {'bytes': count, 'sha256': h256.hexdigest(),
            'md5': hmd5.hexdigest(), 'crc32': f'{crc & 0xffffffff:08x}'}


def pin_file(path):
    with path.open('rb') as stream:
        value = stream_pin(stream)
    return {key: value[key] for key in ('bytes', 'sha256', 'md5')}


def json_file(path):
    # Native API objects are used only through explicit metadata-key allowlists.
    return json.loads(path.read_bytes())


def canonical_hash(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def enumerate_tree(root):
    """Explicit lstat recursion with no suppressed traversal errors or ignores."""
    items = []
    def descend(path):
        info = path.lstat()
        relative = path.relative_to(root).as_posix()
        mode = stat.S_IMODE(info.st_mode)
        demand(not stat.S_ISLNK(info.st_mode), 'source has no symlink')
        if stat.S_ISDIR(info.st_mode):
            children = sorted(path.iterdir(), key=lambda item: item.name)
            items.append({'path': relative, 'kind': 'directory',
                          'mode_octal': oct(mode), 'empty': len(children) == 0})
            for child in children:
                descend(child)
        else:
            demand(stat.S_ISREG(info.st_mode), 'source has no special object')
            items.append({'path': relative, 'kind': 'file',
                          'mode_octal': oct(mode), **pin_file(path)})
    descend(root)
    return sorted(items, key=lambda entry: entry['path'])


def check_pin(path, declared, label):
    actual = pin_file(path)
    for key in ('bytes', 'sha256', 'md5'):
        demand(declared[key] == actual[key], label + ' ' + key)
    return actual


def permission(item):
    native = item.external_attr >> 16
    return stat.S_IMODE(native) if native else (0o755 if item.is_dir() else 0o644)


def zip_native(item, ordinal):
    raw = item.orig_filename
    demand(raw == item.filename, 'ZIP native name not sanitized')
    parts = PurePosixPath(raw).parts
    demand(bool(parts) and not PurePosixPath(raw).is_absolute(), 'ZIP path relative')
    demand('..' not in parts and '\\' not in raw and '\x00' not in raw,
           'ZIP path has no traversal or NUL')
    demand(not item.flag_bits & 1, 'ZIP is unencrypted')
    demand(not item.is_dir() or item.file_size == 0, 'ZIP directory payload empty')
    native_mode = item.external_attr >> 16
    allowed_types = (0, stat.S_IFDIR) if item.is_dir() else (0, stat.S_IFREG)
    demand(stat.S_IFMT(native_mode) in allowed_types, 'ZIP has no link or device')
    return {'ordinal': ordinal, 'native_filename': raw,
        'normalized_relative_path': '/'.join(parts),
        'kind': 'directory' if item.is_dir() else 'file',
        'native_unix_mode_octal': oct(native_mode),
        'native_permissions_octal': oct(stat.S_IMODE(native_mode)),
        'native_external_attr': item.external_attr,
        'native_internal_attr': item.internal_attr,
        'native_create_system': item.create_system,
        'native_create_version': item.create_version,
        'native_extract_version': item.extract_version,
        'native_volume': item.volume,
        'native_header_offset': item.header_offset,
        'native_date_time': list(item.date_time),
        'native_flag_bits': item.flag_bits,
        'native_compression_type': item.compress_type,
        'native_compressed_bytes': item.compress_size,
        'native_uncompressed_bytes': item.file_size,
        'native_crc32': f'{item.CRC:08x}',
        'native_extra_hex': item.extra.hex(),
        'native_comment_hex': item.comment.hex()}


def verify_archive(root, entry, archive_record):
    native_ordinal = entry['ordinal']
    filename = entry['native_file_entry']['key']
    archive_path = root / entry['relative_path']
    expected_extract = f'archives/{native_ordinal:02d}-{filename}.extracted'
    expected_manifest = f'archives/{native_ordinal:02d}-{filename}.members.json'
    demand(archive_record['published_file_ordinal'] == native_ordinal, 'archive native asset ordinal')
    demand(archive_record['archive_relative_path'] == entry['relative_path'], 'archive native path')
    demand(archive_record['extracted_relative_path'] == expected_extract, 'archive extraction locator')
    demand(archive_record['member_manifest_relative_path'] == expected_manifest, 'archive manifest locator')
    extract_root = root / expected_extract
    native_manifest = json_file(root / expected_manifest)
    demand(native_manifest['archive'] == filename, 'archive manifest source identity')
    check_pin(archive_path, native_manifest, 'archive member manifest archive pin')
    expected_tree = {'.': {'kind': 'directory', 'mode': None}}
    pdfs, hidden_members, directory_members = [], 0, 0
    seen, aliases = set(), {}
    with zipfile.ZipFile(archive_path, 'r') as archive:
        infos = archive.infolist()
        demand(len(infos) == native_manifest['member_count'] == len(native_manifest['members']), 'ZIP full member count')
        demand(archive.comment.hex() == native_manifest['archive_comment_hex'], 'ZIP archive comment')
        for ordinal, (info, declared) in enumerate(zip(infos, native_manifest['members']), 1):
            native = zip_native(info, ordinal)
            for key, value in native.items():
                demand(declared[key] == value, 'ZIP native member metadata ' + key)
            relative = native['normalized_relative_path']
            parts = PurePosixPath(relative).parts
            demand(relative not in seen, 'ZIP no duplicate normalized member')
            seen.add(relative)
            for depth in range(1, len(parts) + 1):
                prefix = '/'.join(parts[:depth])
                alias = unicodedata.normalize('NFC', prefix).casefold()
                demand(alias not in aliases or aliases[alias] == prefix, 'ZIP no prefix alias collision')
                aliases[alias] = prefix
                if depth < len(parts):
                    if prefix in expected_tree:
                        demand(expected_tree[prefix]['kind'] == 'directory', 'ZIP implicit parent is directory')
                    else:
                        expected_tree[prefix] = {'kind': 'directory', 'mode': None}
            kind = native['kind']
            if relative in expected_tree:
                demand(expected_tree[relative]['kind'] == kind, 'ZIP file-directory topology consistency')
            expected_tree[relative] = {'kind': kind, 'mode': permission(info)}
            hidden_members += any(component.startswith('.') for component in parts)
            directory_members += info.is_dir()
            # Stream every member, including empty directories, solely for digests.
            with archive.open(info, 'r') as stream:
                actual = stream_pin(stream)
            demand(actual['bytes'] == info.file_size, 'ZIP streamed uncompressed length')
            demand(actual['crc32'] == f'{info.CRC:08x}', 'ZIP independently streamed CRC32')
            output = extract_root.joinpath(*parts)
            if info.is_dir():
                demand(declared['extracted_bytes'] == 0 and output.is_dir(), 'ZIP extracted directory')
            else:
                disk = pin_file(output)
                for key in ('bytes', 'sha256', 'md5'):
                    demand(actual[key] == declared['extracted_' + key] == disk[key], 'ZIP member/disk digest agreement ' + key)
                if info.orig_filename.lower().endswith('.pdf'):
                    pdfs.append({'archive_member_ordinal': ordinal,
                        'native_filename': info.orig_filename,
                        'relative_path': output.relative_to(root).as_posix(),
                        'bytes': actual['bytes'], 'sha256': actual['sha256'],
                        'role': 'embedded PDF identity only; content not read or classified'})
    actual_tree = enumerate_tree(extract_root)
    by_path = {item['path']: item for item in actual_tree}
    demand(set(expected_tree) == set(by_path), 'ZIP exact explicit/implicit extracted namespace')
    for name, expected in expected_tree.items():
        demand(by_path[name]['kind'] == expected['kind'], 'ZIP extracted object kind')
        if expected['mode'] is not None:
            demand(by_path[name]['mode_octal'] == oct(expected['mode']), 'ZIP explicit native mode preserved')
    demand(archive_record['member_count'] == len(seen), 'archive metadata member count')
    demand(archive_record['embedded_pdf_locations'] == pdfs, 'archive embedded PDF identities')
    return {'member_count': len(seen), 'directory_member_count': directory_members,
            'hidden_member_count': hidden_members, 'embedded_pdf_count': len(pdfs),
            'extracted_file_count': sum(item['kind'] == 'file' for item in actual_tree),
            'extracted_directory_count_including_root': sum(item['kind'] == 'directory' for item in actual_tree),
            'extracted_empty_directory_count': sum(item['kind'] == 'directory' and item['empty'] for item in actual_tree)}


def verify_record(record_pin, queue_row):
    global STAGE
    record_id = record_pin['record_id']
    STAGE = 'record ' + str(record_id)
    root = PROJECT / 'papers' / str(record_id) / 'sources'
    demand(record_pin['source_root'] == str(root), 'source root identity')
    before = enumerate_tree(root)
    manifest = json_file(root / 'SOURCE_MANIFEST.json')
    final = json_file(root / 'SOURCE_FINAL.json')
    metadata = json_file(root / 'SOURCE_METADATA.json')
    check_pin(root / 'SOURCE_MANIFEST.json', record_pin['manifest'], 'external source manifest')
    check_pin(root / 'SOURCE_FINAL.json', record_pin['final'], 'external source final')
    check_pin(root / 'SOURCE_MANIFEST.json', final['manifest'], 'source final manifest')
    demand(manifest['record_id'] == final['record_id'] == metadata['record_id'] == record_id, 'control record identities')
    demand(manifest['root'] == final['source_root'] == str(root), 'control root identities')
    demand(manifest['excluded_control_files'] == ['SOURCE_MANIFEST.json', 'SOURCE_FINAL.json'], 'finite exclusion scope')
    payload = [item for item in before if item['path'] not in manifest['excluded_control_files']]
    demand(manifest['entries'] == payload, 'exact finite namespace topology modes hashes lengths and emptiness')
    files = sum(item['kind'] == 'file' for item in payload)
    directories = sum(item['kind'] == 'directory' for item in payload)
    demand(manifest['file_count'] == final['payload_file_count'] == record_pin['payload_file_count'] == files, 'finite file count')
    demand(manifest['directory_count'] == final['payload_directory_count_including_root'] == record_pin['payload_directory_count_including_root'] == directories, 'finite directory count')
    demand(manifest['total_file_bytes'] == sum(item.get('bytes', 0) for item in payload), 'finite total bytes')
    demand(final['status'] == 'source_acquisition_complete_no_scientific_review', 'source-only final status')
    demand(final['manifest_scope_is_finite'] is True, 'finite source flag')
    demand(final['external_pin_location'] == str(LANE / 'EXTERNAL_SOURCE_PINS.json'), 'external pin locator')
    api_path = root / 'native-metadata/record-api.json'
    api = json_file(api_path)
    md = api.get('metadata', {})
    demand(str(api['id']) == str(record_id), 'native API record identity')
    native_fields = {
        'native_doi': api.get('doi'), 'native_doi_url': api.get('doi_url'),
        'native_conceptdoi': api.get('conceptdoi'), 'native_conceptrecid': api.get('conceptrecid'),
        'native_created': api.get('created'), 'native_modified': api.get('modified'),
        'native_publication_date': md.get('publication_date'),
        'native_version_field_present': 'version' in md, 'native_version': md.get('version'),
        'native_license': md.get('license'), 'native_access_right': md.get('access_right'),
        'native_access_right_category': md.get('access_right_category'),
        'native_rights': md.get('rights'), 'native_imprint': md.get('imprint'),
        'native_related_identifiers': md.get('related_identifiers'), 'native_links': api.get('links')}
    for key, value in native_fields.items():
        demand(metadata[key] == value, 'native allowed metadata preservation ' + key)
    demand(api.get('doi') == queue_row['doi'], 'native DOI matches acquisition queue identity')
    demand(md.get('publication_date') == queue_row['publication_date'], 'native date matches acquisition queue')
    native_files = api['files']
    demand(metadata['native_file_order'] == [item['key'] for item in native_files], 'native asset order')
    demand(len(metadata['files_in_published_order']) == len(native_files), 'all native assets represented')
    receipts = json_file(root / 'native-metadata/transport-receipts.json')
    demand(len(receipts) == len(native_files) + 2, 'all transport receipts represented')
    demand(receipts[0]['requested_url'] == f'https://zenodo.org/api/records/{record_id}', 'API GET locator')
    demand(receipts[1]['requested_url'] == f'https://zenodo.org/records/{record_id}', 'page GET locator')
    check_pin(api_path, receipts[0], 'raw API transport object')
    check_pin(root / 'native-metadata/record-page.html', receipts[1], 'raw page transport object')
    archives, outer = [], []
    archive_cursor = 0
    for ordinal, (native, declared) in enumerate(zip(native_files, metadata['files_in_published_order']), 1):
        filename = native['key']
        demand(declared['ordinal'] == ordinal and declared['native_file_entry'] == native, 'asset full native entry order')
        relative = 'zenodo-files/' + filename
        demand(declared['relative_path'] == relative, 'native asset filename retained')
        actual = check_pin(root / relative, declared, 'published asset digest')
        literal = native['checksum'].split(':', 1)
        demand(literal[0] == 'md5' and 0 < len(literal[1]) <= 32, 'native MD5 algorithm and literal length')
        demand(declared['native_md5_literal'] == literal[1], 'native MD5 literal retained')
        padded = literal[1].lower().zfill(32)
        demand(actual['md5'] == padded == declared['md5_comparison_hex32'], 'native MD5 comparison')
        demand(declared['md5_left_zero_padding_count'] == 32 - len(literal[1]), 'native MD5 padding explicitly recorded')
        demand(actual['bytes'] == native['size'], 'native asset byte length')
        demand(declared['integrity_matches_native_metadata'] is True, 'asset integrity flag')
        receipt = receipts[ordinal + 1]
        demand(receipt['requested_url'] == native['links']['self'] and receipt['object'] == filename, 'asset native transport locator/order')
        check_pin(root / relative, receipt, 'asset transport digest')
        if filename == 'paper.pdf':
            outer.append({'identity_basis': 'Published outer asset named paper.pdf; distinct from every embedded archive PDF',
                          'relative_path': relative, **actual})
            queue_pdf = [item for item in queue_row['sources'] if item['filename'] == filename]
            demand(len(queue_pdf) == 1, 'queue outer manuscript locator')
            demand(actual['sha256'] == queue_pdf[0]['sha256'] and actual['bytes'] == queue_pdf[0]['expected_bytes'], 'outer manuscript matches initial queue pin')
        if filename.lower().endswith('.zip'):
            demand(archive_cursor < len(metadata['archives']), 'archive metadata present')
            archives.append(verify_archive(root, declared, metadata['archives'][archive_cursor]))
            archive_cursor += 1
    demand(archive_cursor == len(metadata['archives']), 'no undeclared archive metadata')
    demand(len(outer) == 1, 'unique outer controlling manuscript')
    demand(metadata['outer_controlling_manuscript'] == final['outer_controlling_manuscript'] == record_pin['outer_controlling_manuscript'] == outer[0], 'outer manuscript identity across controls')
    demand(metadata['mathematical_content_read'] is False and metadata['native_scientific_programs_executed'] is False, 'source-only acquisition declarations')
    member_count = sum(item['member_count'] for item in archives)
    embedded_count = sum(item['embedded_pdf_count'] for item in archives)
    demand(final['published_asset_count'] == record_pin['published_asset_count'] == len(native_files), 'final all-asset counts')
    demand(final['archive_count'] == len(archives), 'final archive count')
    demand(final['archive_member_count'] == record_pin['archive_member_count'] == member_count, 'final archive member count')
    demand(final['embedded_pdf_count'] == record_pin['embedded_pdf_count'] == embedded_count, 'final embedded PDF count')
    after = enumerate_tree(root)
    demand(before == after, 'complete source tree unchanged during verification')
    return {'record_id': record_id, 'status': 'PASS', 'payload_file_count': files,
            'payload_directory_count_including_root': directories,
            'full_file_count_including_controls': files + 2,
            'published_asset_count': len(native_files), 'archives': archives,
            'archive_member_count': member_count, 'embedded_pdf_count': embedded_count,
            'hidden_payload_paths': sum(any(part.startswith('.') for part in PurePosixPath(item['path']).parts if part != '.') for item in payload),
            'empty_payload_directories': sum(item['kind'] == 'directory' and item['empty'] for item in payload),
            'whole_source_tree_canonical_sha256': canonical_hash(after),
            'manifest_pin': pin_file(root / 'SOURCE_MANIFEST.json'),
            'final_pin': pin_file(root / 'SOURCE_FINAL.json'),
            'outer_controlling_manuscript': outer[0]}


def main():
    global STAGE
    started = utc()
    read_receipt = json_file(OWN / 'FULL_CODE_READ_RECEIPT.json')
    demand(read_receipt['sha256'] == pin_file(Path(__file__))['sha256'], 'verifier matches complete read receipt')
    external_path = LANE / 'EXTERNAL_SOURCE_PINS.json'
    external_before = pin_file(external_path)
    external = json_file(external_path)
    for key in ('collector', 'contract'):
        check_pin(Path(external[key]['path']), external[key], 'external ' + key + ' code/contract pin')
    demand([record['record_id'] for record in external['records']] == list(RECORDS), 'exact external record sequence')
    queue = json_file(LANE / 'QUEUE_SOURCE_METADATA.json')
    rows = {row['record_id']: row for row in queue['source_rows_as_data']}
    results = [verify_record(record, rows[record['record_id']]) for record in external['records']]
    demand(pin_file(external_path) == external_before, 'external source pins unchanged')
    STAGE = 'result closure'
    result = {'created_utc': utc(), 'started_utc': started, 'status': 'PASS',
              'scope': 'Independent source byte/native-metadata/topology custody verification only',
              'script_pin': pin_file(Path(__file__)), 'checks_passed': CHECKS,
              'external_source_pins': {'path': str(external_path), **external_before},
              'records': results, 'source_trees_unchanged': True,
              'mathematical_text_interpreted': False, 'native_source_programs_executed': False,
              'network_used': False, 'completion_percent': 100, 'follow_up': None}
    with (OWN / 'RESULT.json').open('x') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'status': 'PASS', 'checks_passed': CHECKS,
                      'records': [{'record_id': item['record_id'],
                                   'payload_files': item['payload_file_count'],
                                   'directories_including_root': item['payload_directory_count_including_root'],
                                   'archive_members': item['archive_member_count'],
                                   'embedded_pdfs': item['embedded_pdf_count']} for item in results]}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        failure = {'created_utc': utc(), 'status': 'FAIL', 'stage': STAGE,
                   'error_type': type(error).__name__, 'error': str(error),
                   'checks_reached': CHECKS, 'follow_up': 'Report first failure; no cosmetic retry or source mutation.'}
        with (OWN / 'FAILURE.json').open('x') as stream:
            json.dump(failure, stream, indent=2)
            stream.write('\n')
        raise
