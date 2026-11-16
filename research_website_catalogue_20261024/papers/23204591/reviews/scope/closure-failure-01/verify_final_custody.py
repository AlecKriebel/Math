#!/usr/bin/env python3
"""Pure-default offline custody only: fixed source and owned namespace; no writes, network, subprocesses or science execution."""
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


def source_check():
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
    return {'status': 'SOURCE_CUSTODY_PASS', 'checks': CHECKS,
                      'source_payload_files': 89, 'exact_source_terminal_files': sorted(TERMINALS),
                      'source_actual_files': 92, 'source_directories': sorted(directories),
                      'source_fullbyte_pins': pins, 'native_assets': 4,
                      'ZIP_regular_payloads_full_CRC_and_byte_equality': count,
                      'native_version_field_present': ready['version_field_present'],
                      'native_version_original': ready['version'],
                      'source_historical_unread_fields_unchanged': True,
                      'scientific_body_or_code_execution': False,
                      'network_requests': 0, 'filesystem_writes': 0}


ROOT = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23204591/reviews/scope')
ROOT_TERMINALS = {'FINAL_MANIFEST.json', 'FINAL_CLOSURE.json', 'FINAL_SEAL.json'}


def own(name):
    path = Path(name)
    if not path.is_absolute():
        path = ROOT / path
    require(path.resolve().is_relative_to(ROOT), 'Owned path escapes namespace')
    require(not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode), 'Owned path not ordinary file')
    return path


def ownload(name):
    return json.loads(own(name).read_bytes())


def bound(item):
    require(type(item['path']) is str and type(item['bytes']) is int and type(item['SHA256']) is str,
            'Pin schema types differ')
    path = Path(item['path'])
    require(path.is_absolute(), 'Full absolute pin required')
    if path.is_relative_to(ROOT):
        path = own(path)
    elif path.is_relative_to(SOURCE):
        path = inside(path)
    else:
        raise RuntimeError('Pin outside fixed own/source boundary')
    data = path.read_bytes()
    require(len(data) == item['bytes'] and digest(data) == item['SHA256'], 'Whole pin differs: ' + str(path))
    return data


def pin_walk(value):
    if isinstance(value, dict):
        if {'path', 'bytes', 'SHA256'} <= set(value):
            bound(value)
        for child in value.values():
            pin_walk(child)
    elif isinstance(value, list):
        for child in value:
            pin_walk(child)


def seal_check(name, expected):
    data = own(name).read_bytes()
    require(digest(data) == expected, 'Immutable earlier seal differs')
    value = json.loads(data)
    for item in value['files']:
        bound(item)
    return value


def pair_headers(value):
    return type(value) is list and all(type(p) is list and len(p) == 2 and
                                     all(type(s) is str for s in p) for p in value)


def transport_check():
    count, hops = 0, 0
    statuses = []
    final_by_hash = {}
    actual_labels = []
    for path in sorted(ROOT.glob('primary-*.stdout.json')):
        value = json.loads(path.read_bytes())
        label = value['label']
        require(path.name == 'primary-' + label + '.stdout.json', 'Transport label differs')
        require(value['no_retry_or_access_bypass'] is True and
                value['scientific_body_interpreted_by_transport'] is False, 'Transport exposure fields differ')
        require(value['terminal_body_complete'] is True and value['error'] is None,
                'Transport whole-byte completion differs')
        require(own('primary-' + label + '.stderr').read_bytes() == b'', 'Transport stderr differs')
        chain = value['literal_request_chain']
        require(type(chain) is list and 1 <= len(chain) <= 8, 'Transport chain count differs')
        for i, entry in enumerate(chain):
            stored = ownload('primary/' + label + '-hop' + str(i) + '.transport.json')
            require(typed(stored, entry), 'Whole literal transport types/order differ')
            require(entry['redirect_hop'] == i and entry['method'] == 'GET', 'Request ordinal/method differs')
            require(pair_headers(entry['actual_request_headers_in_sent_order']) and
                    pair_headers(entry['response_headers_in_received_order']), 'Ordered header representation differs')
            require(entry['request_send_completed'] is True and entry['whole_response_body_complete'] is True,
                    'Actual request/body incomplete')
            require(entry['authentication_cookies_proxy_retry_or_bypass'] is False,
                    'Unexpected transport access mechanism')
            require(entry['error'] is None and entry['error_type'] is None, 'Transport exception field differs')
            body = own(entry['body']).read_bytes()
            require(len(body) == entry['bytes'] and digest(body) == entry['SHA256'], 'Raw body differs')
            request = own(entry['prepared_request_bytes_path']).read_bytes()
            require(len(request) == entry['prepared_request_bytes'] and
                    digest(request) == entry['prepared_request_SHA256'], 'Literal sent request buffer differs')
            require(request.startswith(b'GET ') and request.endswith(b'\r\n\r\n'), 'Request buffer envelope differs')
            require(type(entry['HTTP_status']) is int, 'Native HTTP status type differs')
            hops += 1
        last = chain[-1]
        require(value['terminal_body'] == last['body'] and
                value['terminal_bytes'] == last['bytes'] and
                value['terminal_SHA256'] == last['SHA256'] and
                value['terminal_HTTP_status'] == last['HTTP_status'], 'Terminal wrapper differs')
        statuses.append({'label': label, 'status': last['HTTP_status']})
        final_by_hash[last['SHA256']] = last
        actual_labels.append(label)
        count += 1
    native = ownload('primary/NATIVE_SOURCE_HASHES.json')
    require(native['upstream_commit'] == 'adc7f1241b42e322a6451854ab7e4b4c146bf78a' and
            len(native['files']) == 15, 'Native whole checksum inventory differs')
    for name, expected in native['files'].items():
        require(expected in final_by_hash, 'Native binding has no actual terminal body: ' + name)
        require(final_by_hash[expected]['HTTP_status'] == 200, 'Native body not actual HTTP200')
    shared_labels = []
    for i in range(1, 5):
        handoff = ownload('RAW_PRIMARY_HANDOFF_' + format(i, '02d') + '.json')
        pin_walk(handoff)
        for record in handoff['records']:
            require(record['actual_process_exit_code'] == 0, 'Actual acquisition process failed')
            if record.get('actual_native_pin_match') is True:
                require(record['native_expected_SHA256'] == record['whole_actual_body']['SHA256'],
                        'Handoff native pin differs')
            shared_labels.append(record['label'])
    require(len(shared_labels) == len(set(shared_labels)) == count and
            sorted(shared_labels) == actual_labels, 'Handoff coverage differs')
    require([s for s in statuses if s['status'] != 200] == [{'label': 'Calderon-DOI', 'status': 403}],
            'Literal access-failure inventory differs')
    return {'logical_requests': count, 'actual_HTTP_hops': hops,
            'literal_terminal_statuses': statuses, 'native_checksum_bindings': 15,
            'raw_handoff_records': len(shared_labels)}


def main():
    require(len(sys.argv) == 1, 'Only offline read-only default mode is supported')
    require(stat.S_ISDIR(ROOT.lstat().st_mode) and not ROOT.is_symlink(), 'Ordinary owned root required')
    files, directories = [], []
    for path in ROOT.rglob('*'):
        mode = path.lstat().st_mode
        require(not stat.S_ISLNK(mode), 'Owned namespace symlink')
        relative = path.relative_to(ROOT).as_posix()
        if stat.S_ISREG(mode):
            files.append(relative)
        elif stat.S_ISDIR(mode):
            directories.append(relative)
        else:
            raise RuntimeError('Owned namespace special object')
    manifest = ownload('FINAL_MANIFEST.json')
    require(manifest['owned_root'] == str(ROOT), 'Owned root binding differs')
    require(manifest['excluded_terminal_files'] == sorted(ROOT_TERMINALS) and
            manifest['recursive_basename_exclusions'] is False and
            manifest['future_or_unsealed_exclusions'] == [], 'Exact terminal exclusions differ')
    expected = [item['path'] for item in manifest['files']]
    require(expected == sorted(set(expected)), 'Manifest path ordering/duplicates differ')
    require(sorted(set(files) - ROOT_TERMINALS) == expected, 'Closed owned file namespace differs')
    require(manifest['directories'] == sorted(set(directories)), 'Closed owned directory namespace differs')
    require(len(files) == len(expected) + 3, 'Missing/extra exact existing terminal')
    require(len(set(s.casefold() for s in files + directories)) == len(files) + len(directories),
            'Owned case-colliding names')
    for name in ROOT_TERMINALS:
        own(name)
    for item in manifest['files']:
        require(not Path(item['path']).is_absolute() and '..' not in Path(item['path']).parts,
                'Relative manifest path escapes')
        body = own(item['path']).read_bytes()
        require(len(body) == item['bytes'] and digest(body) == item['SHA256'], 'Owned payload differs')
    source = source_check()
    require(source['checks'] > 0, 'Missing full source validation')
    initial = seal_check('INITIAL_SEAL.json',
        '69294ddb6a4f91fbb7ed85aa6e0e64412666c0d2a8ff4b550caf3f4acca53aca')
    results = seal_check('PREEXPOSURE_RESULTS_SEAL.json',
        '9a77cf6703bd40fa11f2a1704bed39645139b2f6199ec3ccd57dda078a5dfb90')
    reconstruction = seal_check('PRIMARY_RECONSTRUCTION_SEAL.json',
        'b4b1acae02b3a4d1c44f06b8a4da7047905a6bba89f97502a71487364e041523')
    require(initial['UTC'] < results['UTC'] < reconstruction['UTC'], 'Actual seal chronology differs')
    require(initial['PDF_pages_personally_read'] == 5 and
            initial['controlling_TeX_lines_personally_read'] == 329 and
            initial['fresh_own_individual_rasters_personally_viewed'] == 5, 'Initial read extent differs')
    own_receipt = ownload('OWN_CONTROL_RECEIPT.json')
    require(own_receipt['exit_code'] == 0 and own_receipt['normal_runs'] == 1 and
            own_receipt['native_program_runs'] == 0, 'Own actual control execution differs')
    for name, prefix in [('own_restriction_controls.py', 'program'),
                         ('own_restriction_controls.stdout', 'stdout'),
                         ('own_restriction_controls.stderr', 'stderr')]:
        body = own(name).read_bytes()
        require(len(body) == own_receipt[prefix + '_bytes'] and
                digest(body) == own_receipt[prefix + '_SHA256'], 'Actual own control receipt differs')
    own_output = ownload('own_restriction_controls.stdout')
    require(own_output['checks'] == 140242 and own_output['status'] == 'OWN_BOUNDED_EXACT_CONTROLS_PASS',
            'Whole retained bounded-control output differs')
    require(own_receipt['completed_UTC'] < results['UTC'], 'Own execution not before actual results seal')
    transport = transport_check()
    for path in sorted(ROOT.glob('primary-*.stdout.json')):
        require(results['UTC'] < json.loads(path.read_bytes())['started_UTC'],
                'Foreign acquisition precedes own actual results seal')
    for name in ['INITIAL_INPUTS.json', 'FINAL_INPUTS.json', 'FINAL_READ_LEDGER.json', 'OWN_FAILURE_HISTORY.json']:
        pin_walk(ownload(name))
    require(inside('SOURCE_READY.json').read_bytes() == own('inputs/SOURCE_READY.json').read_bytes(),
            'Whole READY copy differs')
    receipt = ownload('CUSTODY_HELPER_READ_RECEIPT.json')
    helper = own(__file__).read_bytes()
    require(receipt['entire_current_body_personally_read_before_execution'] is True and
            receipt['bytes'] == len(helper) and receipt['SHA256'] == digest(helper), 'Current helper read binding differs')
    verdict = ownload('CUSTOM_VERDICT.json')
    require(verdict['record_id'] == 23204591 and verdict['comparison_gate'] == 'CLOSED' and
            verdict['current_peer_root_findings_read'] is False and verdict['native_scientific_executions'] == 0,
            'Review scope/exposure fields differ')
    require(own('.gitignore').read_text() == '/primary/*.body\n/primary/*.pdf\n/primary/*.txt\n/primary-rasters/\n',
            'Private-body publication exclusions differ')
    print(json.dumps({'status': 'OFFLINE_CUSTODY_PASS', 'checks': CHECKS,
        'owned_payload_files': len(expected), 'owned_actual_files': len(files),
        'owned_directories': sorted(directories), 'owned_payload_bytes': sum(i['bytes'] for i in manifest['files']),
        'exact_existing_root_terminal_exclusions': sorted(ROOT_TERMINALS),
        'recursive_basename_exclusions': False, 'future_or_unsealed_exclusions': [],
        'source_actual_files': 92, 'source_directories': 10, 'native_assets': 4,
        'regular_ZIP_payloads_full_CRC_and_bytes': 19, 'native_version_whole_actual': '1.0.0',
        'all_original_source_fields_bytes_and_historical_unread_flags_unchanged': True,
        'early_immutable_seals_verified': 3, 'transport': transport,
        'scientific_or_native_execution': False, 'network_requests': 0, 'filesystem_writes': 0,
        'custody_does_not_certify_science': True}, indent=2))


if __name__ == '__main__':
    main()
