#!/usr/bin/env python3
"""Fresh public Zenodo GET acquisition and byte/topology custody only.

No mathematical text extraction, document rendering, or source execution.
The whole script must be read before first execution.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import unicodedata
import urllib.request
import zipfile

LANE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/source188189-sol-20261117')
PROJECT = LANE.parent.parent
IDS = [23203270, 23203081]
MAX_GET_BYTES = 2_000_000_000
MAX_ARCHIVE_TOTAL = 4_000_000_000


def now():
    return datetime.now(timezone.utc).isoformat()


def digest_bytes(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'md5': hashlib.md5(data).hexdigest()}


def digest_file(path):
    sha, md5, size = hashlib.sha256(), hashlib.md5(), 0
    with path.open('rb') as stream:
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            sha.update(block)
            md5.update(block)
            size += len(block)
    return {'bytes': size, 'sha256': sha.hexdigest(), 'md5': md5.hexdigest()}


def write_json(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def get(url, target):
    if not url.startswith('https://zenodo.org/'):
        raise ValueError('Unexpected acquisition origin: ' + url)
    request = urllib.request.Request(url, headers={
        'User-Agent': 'IndependentResearchSourceCustody/1.0',
        'Accept-Encoding': 'identity'})
    started = now()
    with urllib.request.urlopen(request, timeout=90) as response:
        if response.status != 200:
            raise ValueError('Unexpected response status')
        headers = list(response.headers.raw_items())
        total = 0
        with target.open('xb') as stream:
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                total += len(block)
                if total > MAX_GET_BYTES:
                    raise ValueError('Acquisition exceeds explicit byte bound')
                stream.write(block)
        receipt = {'requested_url': url, 'response_url': response.geturl(),
                   'status': response.status, 'response_headers': headers,
                   'started_utc': started, 'completed_utc': now(),
                   'object': target.name, **digest_file(target)}
    return receipt


def safe_asset_name(name):
    if not isinstance(name, str) or not name or name in ('.', '..'):
        raise ValueError('Invalid native asset name')
    if '/' in name or '\\' in name or '\x00' in name:
        raise ValueError('Native asset name is not a single safe component')
    return name


def archive_inspect_extract(archive, destination, manifest):
    destination.mkdir(mode=0o755)
    entries, seen, filesystem_prefixes = [], set(), {}
    with zipfile.ZipFile(archive) as source:
        infos = source.infolist()
        if sum(item.file_size for item in infos) > MAX_ARCHIVE_TOTAL:
            raise ValueError('Archive exceeds explicit extraction byte bound')
        # Inspect the complete archive structure before writing any member.
        for ordinal, item in enumerate(infos, 1):
            raw_name = item.orig_filename
            if raw_name != item.filename:
                raise ValueError('ZIP decoder changed the native member spelling')
            path = PurePosixPath(raw_name)
            parts = path.parts
            if (not raw_name or not parts or '\\' in raw_name or '\x00' in raw_name
                    or path.is_absolute() or '..' in parts
                    or any(part in ('', '.') for part in parts)):
                raise ValueError('Unsafe archive path: ' + repr(raw_name))
            normalized = '/'.join(parts)
            if normalized in seen:
                raise ValueError('Duplicate normalized archive member: ' + normalized)
            seen.add(normalized)
            # Reject aliases conservatively even on a case-sensitive volume.
            # Check every prefix so implicit directories cannot silently merge.
            for depth in range(1, len(parts) + 1):
                prefix = '/'.join(parts[:depth])
                alias_key = unicodedata.normalize('NFC', prefix).casefold()
                previous = filesystem_prefixes.get(alias_key)
                if previous is not None and previous != prefix:
                    raise ValueError('Case/Unicode-equivalent archive path aliases')
                filesystem_prefixes[alias_key] = prefix
            unix_mode = item.external_attr >> 16
            file_type = stat.S_IFMT(unix_mode)
            is_dir = item.is_dir()
            if is_dir and item.file_size != 0:
                raise ValueError('Nonempty directory ZIP entry cannot be represented as a directory')
            if item.flag_bits & 1:
                raise ValueError('Encrypted archive member')
            allowed = (0, stat.S_IFDIR) if is_dir else (0, stat.S_IFREG)
            if file_type not in allowed:
                raise ValueError('Link or special archive member: ' + raw_name)
            entries.append({
                'ordinal': ordinal, 'native_filename': raw_name,
                'normalized_relative_path': normalized,
                'kind': 'directory' if is_dir else 'file',
                'native_unix_mode_octal': oct(unix_mode),
                'native_permissions_octal': oct(stat.S_IMODE(unix_mode)),
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
                'native_comment_hex': item.comment.hex()})
        for item, entry in zip(infos, entries):
            out = destination.joinpath(*PurePosixPath(entry['normalized_relative_path']).parts)
            if item.is_dir():
                out.mkdir(parents=True, exist_ok=True, mode=0o755)
                entry['extracted_bytes'] = 0
            else:
                out.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
                with source.open(item, 'r') as reader, out.open('xb') as writer:
                    shutil.copyfileobj(reader, writer, length=1024 * 1024)
                actual = digest_file(out)
                if actual['bytes'] != item.file_size:
                    raise ValueError('Extracted byte length mismatch')
                entry.update({'extracted_' + k: v for k, v in actual.items()})
        # Apply modes after extraction, so a native read-only directory cannot
        # prevent safe extraction of its children. No member is ever executed.
        for item, entry in reversed(list(zip(infos, entries))):
            native_mode = item.external_attr >> 16
            permission = stat.S_IMODE(native_mode)
            if native_mode == 0:
                permission = 0o755 if item.is_dir() else 0o644
            os.chmod(destination / entry['normalized_relative_path'], permission)
        archive_comment = source.comment.hex()
    write_json(manifest, {'archive': archive.name, **digest_file(archive),
                         'archive_comment_hex': archive_comment,
                         'safety': 'all members inspected before extraction; no links, special files, encrypted entries, duplicate normalized paths, case/Unicode path aliases, nonempty directory payloads or traversal accepted',
                         'native_member_order_preserved': True,
                         'member_count': len(entries), 'members': entries})
    return entries


def tree_entries(root, excluded=()):
    entries = []
    def walk_error(error):
        raise error
    # os.walk includes dotfiles and empty directories and ignores no patterns.
    paths = [root]
    for base, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        dirs.sort()
        files.sort()
        paths.extend(Path(base) / name for name in dirs + files)
    for path in sorted(paths, key=lambda x: x.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        if rel in excluded:
            continue
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError('Unexpected symlink in acquired source tree')
        kind = 'directory' if stat.S_ISDIR(info.st_mode) else 'file'
        if kind == 'file' and not stat.S_ISREG(info.st_mode):
            raise ValueError('Unexpected special source object')
        entry = {'path': rel, 'kind': kind,
                 'mode_octal': oct(stat.S_IMODE(info.st_mode))}
        if kind == 'file':
            entry.update(digest_file(path))
        else:
            entry['empty'] = not any(path.iterdir())
        entries.append(entry)
    return entries


def acquire(record_id):
    source_root = PROJECT / 'papers' / str(record_id) / 'sources'
    if source_root.exists() or source_root.is_symlink():
        raise FileExistsError('Existing source folder is immutable: ' + str(source_root))
    source_root.parent.mkdir(parents=True, exist_ok=True)
    source_root.mkdir(mode=0o755)
    raw = source_root / 'native-metadata'
    assets = source_root / 'zenodo-files'
    archives = source_root / 'archives'
    raw.mkdir()
    assets.mkdir()
    archives.mkdir()
    started = now()
    receipts = []
    api_url = f'https://zenodo.org/api/records/{record_id}'
    receipts.append(get(api_url, raw / 'record-api.json'))
    metadata = json.loads((raw / 'record-api.json').read_bytes())
    if str(metadata.get('id')) != str(record_id):
        raise ValueError('Record identity mismatch')
    receipts.append(get(f'https://zenodo.org/records/{record_id}', raw / 'record-page.html'))
    published_files = metadata.get('files')
    if not isinstance(published_files, list) or not published_files:
        raise ValueError('Expected nonempty native ordered file list')
    file_records, archive_records = [], []
    seen_names = set()
    for ordinal, entry in enumerate(published_files, 1):
        name = safe_asset_name(entry['key'])
        if name in seen_names:
            raise ValueError('Duplicate published native filename')
        seen_names.add(name)
        url = entry.get('links', {}).get('self')
        if not url:
            raise ValueError('Missing native asset URL')
        target = assets / name
        receipt = get(url, target)
        receipts.append(receipt)
        actual = digest_file(target)
        expected_checksum = entry.get('checksum')
        if not isinstance(expected_checksum, str) or not expected_checksum.startswith('md5:'):
            raise ValueError('Unexpected native checksum algorithm')
        expected_md5_literal = expected_checksum.split(':', 1)[1]
        # Zenodo occasionally serializes a shortened leading-zero digest. Preserve
        # the exact native literal and record whether zero padding was necessary.
        if len(expected_md5_literal) > 32 or not expected_md5_literal:
            raise ValueError('Invalid native MD5 length')
        int(expected_md5_literal, 16)
        expected_md5_padded = expected_md5_literal.lower().zfill(32)
        if actual['md5'] != expected_md5_padded:
            raise ValueError('Asset MD5 mismatch: ' + name)
        if entry.get('size') != actual['bytes']:
            raise ValueError('Asset byte length mismatch: ' + name)
        item = {'ordinal': ordinal, 'native_file_entry': entry,
                'relative_path': target.relative_to(source_root).as_posix(),
                'native_md5_literal': expected_md5_literal,
                'md5_comparison_hex32': expected_md5_padded,
                'md5_left_zero_padding_count': 32 - len(expected_md5_literal),
                'integrity_matches_native_metadata': True, **actual}
        file_records.append(item)
        if name.lower().endswith('.zip'):
            folder = archives / f'{ordinal:02d}-{name}.extracted'
            manifest = archives / f'{ordinal:02d}-{name}.members.json'
            members = archive_inspect_extract(target, folder, manifest)
            archive_records.append({'published_file_ordinal': ordinal,
                'archive_relative_path': target.relative_to(source_root).as_posix(),
                'extracted_relative_path': folder.relative_to(source_root).as_posix(),
                'member_manifest_relative_path': manifest.relative_to(source_root).as_posix(),
                'member_count': len(members),
                'embedded_pdf_locations': [
                    {'archive_member_ordinal': m['ordinal'],
                     'native_filename': m['native_filename'],
                     'relative_path': (folder / m['normalized_relative_path']).relative_to(source_root).as_posix(),
                     'bytes': m['extracted_bytes'], 'sha256': m['extracted_sha256'],
                     'role': 'embedded PDF identity only; content not read or classified'}
                    for m in members if m['kind'] == 'file' and m['native_filename'].lower().endswith('.pdf')]})
    controlling = [item for item in file_records if item['native_file_entry']['key'] == 'paper.pdf']
    if len(controlling) != 1:
        raise ValueError('Expected one distinct outer controlling paper.pdf')
    md = metadata.get('metadata', {})
    identity = {'record_id': record_id, 'record_url': f'https://zenodo.org/records/{record_id}',
        'native_doi': metadata.get('doi'), 'native_doi_url': metadata.get('doi_url'),
        'native_conceptdoi': metadata.get('conceptdoi'),
        'native_conceptrecid': metadata.get('conceptrecid'),
        'native_created': metadata.get('created'), 'native_modified': metadata.get('modified'),
        'native_publication_date': md.get('publication_date'),
        'native_version_field_present': 'version' in md,
        'native_version': md.get('version'),
        'native_license': md.get('license'), 'native_access_right': md.get('access_right'),
        'native_access_right_category': md.get('access_right_category'),
        'native_rights': md.get('rights'), 'native_imprint': md.get('imprint'),
        'native_related_identifiers': md.get('related_identifiers'),
        'native_links': metadata.get('links'),
        'native_file_order': [item['key'] for item in published_files],
        'files_in_published_order': file_records,
        'archives': archive_records,
        'outer_controlling_manuscript': {
            'identity_basis': 'Published outer asset named paper.pdf; distinct from every embedded archive PDF',
            'relative_path': controlling[0]['relative_path'],
            **{k: controlling[0][k] for k in ('bytes', 'sha256', 'md5')}},
        'mathematical_content_read': False, 'native_scientific_programs_executed': False}
    write_json(raw / 'transport-receipts.json', receipts)
    write_json(source_root / 'SOURCE_METADATA.json', identity)
    write_json(source_root / 'SOURCE_LOG.json', {'started_utc': started, 'completed_utc': now(),
        'operations': ['ordinary public GET', 'native metadata identity preservation',
                       'MD5 and byte-length verification', 'safe ZIP extraction',
                       'complete byte/topology manifest construction'],
        'scientific_review': 'not started; source acquisition and custody only',
        'source_custody_completion_percent': 100})
    entries = tree_entries(source_root)
    manifest = {'schema': 'source-custody-finite-manifest-v1', 'record_id': record_id,
        'created_utc': now(), 'root': str(source_root),
        'scope': 'All source payload objects including root, every hidden/ignored/empty directory and every regular file; SOURCE_MANIFEST.json and SOURCE_FINAL.json are control files excluded from this finite payload list.',
        'excluded_control_files': ['SOURCE_MANIFEST.json', 'SOURCE_FINAL.json'],
        'entries': entries,
        'file_count': sum(e['kind'] == 'file' for e in entries),
        'directory_count': sum(e['kind'] == 'directory' for e in entries),
        'total_file_bytes': sum(e.get('bytes', 0) for e in entries)}
    manifest_path = source_root / 'SOURCE_MANIFEST.json'
    write_json(manifest_path, manifest)
    final = {'schema': 'source-custody-final-v1', 'record_id': record_id,
        'closed_utc': now(), 'status': 'source_acquisition_complete_no_scientific_review',
        'source_root': str(source_root), 'manifest': {'path': 'SOURCE_MANIFEST.json', **digest_file(manifest_path)},
        'payload_file_count': manifest['file_count'], 'payload_directory_count_including_root': manifest['directory_count'],
        'published_asset_count': len(file_records), 'archive_count': len(archive_records),
        'archive_member_count': sum(a['member_count'] for a in archive_records),
        'embedded_pdf_count': sum(len(a['embedded_pdf_locations']) for a in archive_records),
        'manifest_scope_is_finite': True,
        'no_source_mutation_after_closure': True,
        'external_pin_location': str(LANE / 'EXTERNAL_SOURCE_PINS.json'),
        'outer_controlling_manuscript': identity['outer_controlling_manuscript']}
    final_path = source_root / 'SOURCE_FINAL.json'
    write_json(final_path, final)
    # SOURCE_FINAL and SOURCE_MANIFEST are externally pinned without circularity.
    pin = {'record_id': record_id, 'source_root': str(source_root),
        'manifest': digest_file(manifest_path), 'final': digest_file(final_path),
        'payload_file_count': manifest['file_count'], 'payload_directory_count_including_root': manifest['directory_count'],
        'published_asset_count': len(file_records), 'archive_member_count': final['archive_member_count'],
        'embedded_pdf_count': final['embedded_pdf_count'],
        'outer_controlling_manuscript': identity['outer_controlling_manuscript']}
    print(json.dumps({'record_id': record_id, 'source_acquisition_complete': True,
                      'published_asset_count': len(file_records),
                      'archive_member_count': final['archive_member_count']}), flush=True)
    return pin


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--released', action='store_true')
    args = parser.parse_args()
    if not args.released or not (LANE / 'ROOT_RELEASE.txt').is_file():
        raise ValueError('Explicit root release receipt required before paper directory writes')
    if not (LANE / 'FULL_CODE_READ_RECEIPT.json').is_file():
        raise ValueError('Full current collector-code read receipt required')
    code_receipt = json.loads((LANE / 'FULL_CODE_READ_RECEIPT.json').read_text())
    if code_receipt['sha256'] != digest_file(Path(__file__))['sha256']:
        raise ValueError('Collector changed since full read receipt')
    for record_id in IDS:
        if (PROJECT / 'papers' / str(record_id) / 'sources').exists():
            raise FileExistsError('Existing sources may not be overwritten')
    pins = []
    for record_id in IDS:
        pins.append(acquire(record_id))
    write_json(LANE / 'EXTERNAL_SOURCE_PINS.json', {'closed_utc': now(),
        'collector': {'path': str(Path(__file__)), **digest_file(Path(__file__))},
        'contract': {'path': str(LANE / 'ACQUISITION_CONTRACT.json'), **digest_file(LANE / 'ACQUISITION_CONTRACT.json')},
        'records': pins})
    with (LANE / 'RESEARCH_LOG.md').open('a') as log:
        log.write(f'- {now()}: Both records acquired by public GET; exact native metadata, all published assets in order, complete safe ZIP topology, and finite payload manifests frozen. Completion estimate: 100% acquisition, pending independent custody verification. No scientific content read or scientific program run.\n')


if __name__ == '__main__':
    main()
