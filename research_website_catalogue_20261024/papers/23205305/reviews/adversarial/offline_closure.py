#!/usr/bin/env python3
"""Read-only local custody verification. No target import, execution, network or writes.

The only exclusions are three exact root terminal files, all of which must
already exist as ordinary files. Every other file and every directory is
closed by FINAL_MANIFEST.json. Terminal receipts are bound by FINAL_SEAL.json
after their construction; this checker does not recursively hash its own seal.
Ignored third-party caches remain part of this strict local namespace.
"""
from pathlib import Path
import hashlib
import json
import stat
import sys
import zipfile
import zlib

ROOT = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23205305/reviews/adversarial')
SOURCE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23205305/sources')
TERMINALS = frozenset(('FINAL_MANIFEST.json', 'FINAL_CLOSURE.json', 'FINAL_SEAL.json'))
CHECKS = 0


def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def typed(value):
    if isinstance(value, dict):
        return ('dict', tuple((key, typed(item)) for key, item in value.items()))
    if isinstance(value, list):
        return ('list', tuple(typed(item) for item in value))
    return (type(value).__name__, value)


def inside(base, relative):
    require(isinstance(relative, str), 'Path is not a string')
    path = Path(relative)
    require(not path.is_absolute() and bool(path.parts), 'Expected nonempty relative path')
    require(all(part not in ('.', '..') for part in path.parts), 'Unsafe path component')
    return base / path


def absolute_inside(base, name):
    path = Path(name)
    require(path.is_absolute(), 'Expected absolute pinned path')
    relative = path.relative_to(base)
    return inside(base, str(relative))


def ordinary_file(path):
    mode = path.lstat().st_mode
    require(stat.S_ISREG(mode) and not stat.S_ISLNK(mode), 'Not an ordinary file: ' + str(path))


def pin(path, expected_bytes, expected_sha):
    ordinary_file(path)
    data = path.read_bytes()
    require(len(data) == expected_bytes, 'Byte count differs: ' + str(path))
    require(sha(data) == expected_sha, 'SHA256 differs: ' + str(path))
    return data


def namespace(base):
    require(stat.S_ISDIR(base.lstat().st_mode), 'Namespace root is not a directory')
    files, directories = [], []
    for path in sorted(base.rglob('*')):
        mode = path.lstat().st_mode
        relative = path.relative_to(base).as_posix()
        require(not stat.S_ISLNK(mode), 'Symlink in closed namespace: ' + relative)
        if stat.S_ISDIR(mode):
            directories.append(relative)
        elif stat.S_ISREG(mode):
            files.append(relative)
        else:
            raise RuntimeError('Special object in namespace: ' + relative)
    return files, directories


def read_json(path):
    return json.loads(path.read_bytes())


def member_metadata(info):
    return {
        'filename': info.filename,
        'file_size': info.file_size,
        'compress_size': info.compress_size,
        'CRC32': format(info.CRC, '08x'),
        'flag_bits': info.flag_bits,
        'compress_type': info.compress_type,
        'date_time': list(info.date_time),
        'external_attr': info.external_attr,
        'internal_attr': info.internal_attr,
        'create_system': info.create_system,
        'create_version': info.create_version,
        'extract_version': info.extract_version,
        'header_offset': info.header_offset,
        'extra_hex': info.extra.hex(),
        'comment_hex': info.comment.hex(),
        'is_directory': info.is_dir(),
    }


def main():
    require(len(sys.argv) == 1, 'No mutation or other mode is supported')
    require(Path(__file__).absolute().parent == ROOT, 'Helper outside its exact owned root')
    for name in sorted(TERMINALS):
        ordinary_file(ROOT / name)
    manifest = read_json(ROOT / 'FINAL_MANIFEST.json')
    require(manifest['exact_root_terminal_exclusions'] == sorted(TERMINALS), 'Wrong terminal exclusions')
    actual_files, actual_directories = namespace(ROOT)
    actual_payloads = sorted(set(actual_files) - TERMINALS)
    expected_payloads = [item['path'] for item in manifest['owned_payloads']]
    require(expected_payloads == sorted(expected_payloads), 'Payload manifest order differs')
    require(len(set(expected_payloads)) == len(expected_payloads), 'Duplicate payload path')
    require(actual_payloads == expected_payloads, 'Owned file namespace is not closed')
    require(actual_directories == manifest['owned_directories'], 'Owned directory namespace is not closed')
    for item in manifest['owned_payloads']:
        require(item['path'] not in TERMINALS, 'Terminal in payload manifest')
        pin(inside(ROOT, item['path']), item['bytes'], item['SHA256'])

    custody = read_json(ROOT / 'CUSTODY_CHECKPOINT.json')
    source_files, source_directories = namespace(SOURCE)
    expected_source = []
    for item in custody['source_fullbyte_pins']:
        path = absolute_inside(SOURCE, item['path'])
        expected_source.append(path.relative_to(SOURCE).as_posix())
        pin(path, item['bytes'], item['SHA256'])
    require(source_files == sorted(expected_source), 'Original source file namespace changed')
    require(source_directories == custody['source_directories'], 'Original source directory namespace changed')
    require(len(source_files) == 126, 'Source count is not 123 payloads plus 3 terminals')
    require(sha((SOURCE / 'SOURCE_READY.json').read_bytes()) ==
            'd5e1575052e0db802b6d8ff47309660b50213d91594856eb4df141943bf0db91', 'SOURCE_READY pin differs')
    require(sha((SOURCE / 'SOURCE_READY_SEAL.json').read_bytes()) ==
            '6540b1c94839ae033e0747843452bd6c33d29c3734680332c8cbc119e79fdcc8', 'Source seal pin differs')

    zip_count = 0
    for archive in custody['whole_ZIP_central_directory_and_comments']:
        archive_path = SOURCE / 'assets' / archive['name']
        with zipfile.ZipFile(archive_path) as package:
            require(package.comment.hex() == archive['archive_comment_hex'], 'ZIP comment changed')
            observed = [member_metadata(info) for info in package.infolist()]
            require(typed(observed) == typed(archive['whole_central_directory_in_original_order']),
                    'Whole ordered ZIP central directory changed')
            require(package.testzip() is None, 'ZIP full CRC failure')
            expected = [item for item in custody['all_regular_ZIP_payloads']
                        if item['container'] == archive['name']]
            require([info.filename for info in package.infolist() if not info.is_dir()] ==
                    [item['member'] for item in expected], 'ZIP regular member order changed')
            for item in expected:
                data = package.read(item['member'])
                require(len(data) == item['bytes'], 'ZIP payload size changed')
                require(format(zlib.crc32(data) & 0xffffffff, '08x') == item['CRC32'], 'ZIP payload CRC changed')
                require(sha(data) == item['SHA256'], 'ZIP payload SHA changed')
                extracted = absolute_inside(SOURCE, item['extracted_path'])
                ordinary_file(extracted)
                require(data == extracted.read_bytes(), 'ZIP/extracted full bytes differ')
                zip_count += 1
    require(zip_count == 61, 'Wrong number of regular ZIP payloads')

    immutable = (
        ('INITIAL_SEAL.json', 'c81c8253895dc3ecd06af4e0b760821e9f743240f714845139533f457c895eb8'),
        ('PREEXPOSURE_RESULTS_SEAL.json', 'a4faf99f6b3d23ac62194d63bf78cc5109556de9bbaecdb6cc054ec23a7f700d'),
    )
    for name, digest in immutable:
        data = (ROOT / name).read_bytes()
        require(sha(data) == digest, 'Immutable early seal changed')
        for item in json.loads(data)['files']:
            pin(absolute_inside(ROOT, item['path']), item['bytes'], item['SHA256'])

    replay = ROOT / 'native-replay'
    original = SOURCE / 'published-source/asset-002/verification/check_two_converse_programs.py'
    require(original.read_bytes() == (replay / original.name).read_bytes(), 'Selected native buffer differs')
    expected = read_json(replay / 'expected-whole.json')
    receipt = read_json(replay / 'REPLAY_RECEIPT.json')
    require([run['label'] for run in receipt['runs']] == ['normal', 'optimized'], 'Replay chronology differs')
    for run in receipt['runs']:
        require(run['returncode'] == 0 and type(run['returncode']) is int, 'Native replay exit failure')
        stdout = pin(replay / (run['label'] + '.stdout'), run['stdout_bytes'], run['stdout_sha256'])
        stderr = pin(replay / (run['label'] + '.stderr'), run['stderr_bytes'], run['stderr_sha256'])
        require(stderr == b'', 'Native replay stderr is nonempty')
        require(typed(json.loads(stdout)) == typed(expected), 'Whole typed replay expectation differs')
        require(typed(run['actual_whole_json']) == typed(expected), 'Receipt whole result differs')
        require(typed(run['expected_whole_json']) == typed(expected), 'Receipt whole expectation differs')
    require((replay / 'normal.stdout').read_bytes() == (replay / 'optimized.stdout').read_bytes(),
            'Native normal/O literal stdout differs')

    transport_count = 0
    for path in sorted((ROOT / 'primary').glob('*.transport.json')):
        data = read_json(path)
        body = data.get('body')
        if body is not None:
            require(isinstance(body, str) and Path(body).parts[0] == 'primary', 'Unexpected raw body binding')
            pin(inside(ROOT, body), data['bytes'], data['SHA256'])
        else:
            require(isinstance(data.get('error'), str), 'Bodyless transport lacks literal error')
        for key in ('actual_request_headers_in_sent_order', 'response_headers_in_received_order'):
            if key in data and data[key] is not None:
                require(isinstance(data[key], list), 'Header order/type changed')
                require(all(isinstance(pair, list) and len(pair) == 2 for pair in data[key]),
                        'Header pair shape changed')
        transport_count += 1

    print(json.dumps({
        'result': 'PASS',
        'checks': CHECKS,
        'owned_payload_files': len(expected_payloads),
        'owned_directories': len(actual_directories),
        'exact_root_terminal_files': sorted(TERMINALS),
        'source_files_unchanged': len(source_files),
        'regular_ZIP_payloads_full_CRC_bytes_checked': zip_count,
        'raw_transport_receipts_checked': transport_count,
        'selected_native_normal_O_whole_typed_expected': True,
        'all_original_metadata_preserved_by_wholebyte_pins': True,
        'mode': 'read-only offline custody; no science execution',
        'terminal_seal_binding': 'FINAL_SEAL.json separately binds manifest and literal closure receipts',
    }, sort_keys=True))


if __name__ == '__main__':
    main()
