#!/usr/bin/env python3
"""Read-only opaque source custody. No source helper, scientific import or network."""
from pathlib import Path
import hashlib
import io
import json
import stat
import sys
import zipfile
import zlib

SOURCE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23204591/sources')
TERMINALS = {'SOURCE_READY_CLOSURE.json', 'SOURCE_READY_MANIFEST.json', 'SOURCE_READY_SEAL.json'}
CHECKS = 0


def require(value, message):
    global CHECKS
    CHECKS += 1
    if not value:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def typed(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(typed(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(typed(x, y) for x, y in zip(a, b))
    return a == b


def inside(name):
    path = Path(name)
    if not path.is_absolute():
        path = SOURCE / path
    require(path.resolve().is_relative_to(SOURCE), 'Source path escapes root')
    require(not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode), 'Not an ordinary source file')
    return path


def load(name):
    return json.loads(inside(name).read_bytes())


def metadata(info, ordinal):
    return {
        'ordinal_zero_based': ordinal, 'filename': info.filename,
        'original_filename': info.orig_filename, 'is_directory': info.is_dir(),
        'bytes': info.file_size, 'compressed_bytes': info.compress_size,
        'CRC32': format(info.CRC, '08x'), 'flags': info.flag_bits,
        'compression': info.compress_type, 'native_date_time': list(info.date_time),
        'external_attr': info.external_attr, 'internal_attr': info.internal_attr,
        'create_system': info.create_system, 'create_version': info.create_version,
        'extract_version': info.extract_version, 'header_offset': info.header_offset,
        'extra_hex': info.extra.hex(), 'comment_hex': info.comment.hex(),
    }


def main():
    require(len(sys.argv) == 1, 'Only read-only default mode is supported')
    require(digest(inside('SOURCE_READY.json').read_bytes()) ==
            'b2ecdf3cb3933244d975519bc388193eb17cbbac1cd9ef234cc8bc264e8259cb', 'READY pin differs')
    require(digest(inside('SOURCE_READY_SEAL.json').read_bytes()) ==
            'f5af12ae206e10a4660eabe81647ff085a73ab60368d1eef28f41e14b49b29bb', 'Source seal pin differs')
    manifest = load('SOURCE_READY_MANIFEST.json')
    require(set(manifest['excluded_terminal_files']) == TERMINALS, 'Wrong source terminal boundary')
    files, directories = [], []
    require(stat.S_ISDIR(SOURCE.lstat().st_mode) and not SOURCE.is_symlink(), 'Ordinary source root')
    for path in SOURCE.rglob('*'):
        mode = path.lstat().st_mode
        require(not stat.S_ISLNK(mode), 'Source namespace symlink')
        if stat.S_ISREG(mode):
            files.append(path.relative_to(SOURCE).as_posix())
        elif stat.S_ISDIR(mode):
            directories.append(path.relative_to(SOURCE).as_posix())
        else:
            raise RuntimeError('Special source namespace object')
    expected = [item['path'] for item in manifest['files']]
    require(sorted(set(files) - TERMINALS) == sorted(expected), 'Source file namespace differs')
    require(len(expected) == len(set(expected)) == 89 and len(files) == 92, 'Source file count differs')
    require(sorted(directories) == sorted(manifest['directories']) and len(directories) == 10,
            'Source directory namespace differs')
    for item in manifest['files']:
        data = inside(item['path']).read_bytes()
        require(len(data) == item['bytes'] and digest(data) == item['SHA256'], 'Source payload differs')
    for name in TERMINALS:
        inside(name)
    seal = load('SOURCE_READY_SEAL.json')
    for name, key in [('SOURCE_READY.json', 'SOURCE_READY_SHA256'),
                      ('SOURCE_READY_MANIFEST.json', 'MANIFEST_SHA256'),
                      ('SOURCE_READY_CLOSURE.json', 'CLOSURE_SHA256')]:
        require(digest(inside(name).read_bytes()) == seal[key], 'Source terminal binding differs')
    ready = load('SOURCE_READY.json')
    for asset in ready['all_native_assets_in_original_order']:
        data = inside(asset['path']).read_bytes()
        original = asset['original_api_file_object']
        algorithm, value = original['checksum'].split(':', 1)
        require(len(data) == asset['bytes'] == original['size'], 'Native asset size differs')
        require(digest(data) == asset['SHA256'] and hashlib.new(algorithm, data).hexdigest() == value,
                'Native asset checksum differs')
        require(data == inside(asset['transport_body_path']).read_bytes(), 'Native transport bytes differ')
    archive = load('ARCHIVE_CUSTODY.json')
    require(len(archive['containers']) == 2 and archive['nested_archive_count'] == 0, 'Archive extent differs')
    count, total = 0, 0
    for container in archive['containers']:
        data = inside(container['input_path']).read_bytes()
        require(digest(data) == container['input_SHA256'] and len(data) == container['input_bytes'],
                'Original archive bytes differ')
        require(container['kind'] == 'zip' and container['container_depth'] == 0, 'Actual archive family differs')
        with zipfile.ZipFile(io.BytesIO(data)) as package:
            infos = package.infolist()
            require(typed([metadata(info, i) for i, info in enumerate(infos)],
                          container['whole_original_central_directory']), 'Ordered complete central metadata differs')
            require(package.comment.hex() == container['original_archive_comment_hex'], 'ZIP comment differs')
            require(package.testzip() is None and len(infos) == len(container['members']), 'Full ZIP CRC/member count')
            for info, item in zip(infos, container['members']):
                require(info.filename == info.orig_filename == item['original_member_name'], 'Member identity differs')
                if info.is_dir():
                    continue
                require(info.file_size <= 64 * 1024 * 1024, 'Member expansion cap')
                body = package.read(info)
                require(len(body) == item['bytes'] and digest(body) == item['SHA256'], 'Member bytes differ')
                require(format(zlib.crc32(body) & 0xffffffff, '08x') == item['CRC32'], 'Member CRC differs')
                require(body == inside(item['extracted_path']).read_bytes(), 'Extracted byte equality differs')
                require(not zipfile.is_zipfile(io.BytesIO(body)) and item['nested_archive_kind'] is None,
                        'Unaccounted nested ZIP')
                count += 1
                total += len(body)
    require(count == archive['whole_regular_payload_occurrences'] == 19, 'Regular payload count differs')
    require(total == archive['expanded_bytes_all_depths'] and total <= 128 * 1024 * 1024, 'Expanded bytes differ')
    pins = []
    for name in sorted(files):
        data = inside(name).read_bytes()
        pins.append({'path': str(SOURCE / name), 'bytes': len(data), 'SHA256': digest(data)})
    print(json.dumps({'status': 'SOURCE_CUSTODY_PASS', 'checks': CHECKS,
                      'source_payload_files': 89, 'exact_source_terminal_files': sorted(TERMINALS),
                      'source_actual_files': 92, 'source_directories': sorted(directories),
                      'source_fullbyte_pins': pins, 'native_assets': 4,
                      'ZIP_regular_payloads_full_CRC_and_byte_equality': count,
                      'native_version_field_present': ready['version_field_present'],
                      'native_version_original': ready['version'],
                      'source_historical_unread_fields_unchanged': True,
                      'scientific_body_or_code_execution': False,
                      'network_requests': 0, 'filesystem_writes': 0}, indent=2))


if __name__ == '__main__':
    main()
