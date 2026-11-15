#!/usr/bin/env python3
"""Import-safe, offline, read-only closure of this review; standard library only.

Default CLI verifies the final seal too. --payload-only is the explicitly
recorded preseal closure used to create the terminal payload receipts.
No scientific programme, source helper, subprocess or network is imported/run.
"""
import hashlib
import json
from pathlib import Path
import stat
import sys
import zipfile


EXCLUDED = {
    'OWNED_MANIFEST.json', 'FINAL_SEAL.json',
    'PAYLOAD_READONLY.normal.stdout.json', 'PAYLOAD_READONLY.normal.stderr',
    'PAYLOAD_READONLY.optimized.stdout.json', 'PAYLOAD_READONLY.optimized.stderr',
    'PAYLOAD_READONLY_RECEIPT.json',
}


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check_bytes(data, row, label):
    require(len(data) == row['bytes'], 'size differs: ' + label)
    require(digest(data) == row['SHA256'], 'SHA-256 differs: ' + label)


def load_json(path):
    return json.loads(path.read_bytes())


def check_file(path, row):
    require(path.is_file() and not path.is_symlink(), 'absent/symlink: ' + str(path))
    data = path.read_bytes()
    check_bytes(data, row, str(path))
    return data


def verify_payload(root=None):
    root = Path(__file__).resolve().parent if root is None else Path(root)
    manifest = load_json(root / 'OWNED_MANIFEST.json')
    require(set(manifest['excluded_final_control_files']) == EXCLUDED,
            'manifest exclusions differ')
    owned = set()
    for row in manifest['files']:
        relative = Path(row['path'])
        require(not relative.is_absolute() and '..' not in relative.parts,
                'unsafe owned path')
        require(row['path'] not in owned, 'duplicate owned path')
        require(row['path'] not in EXCLUDED, 'manifest contains own excluded control')
        owned.add(row['path'])
        check_file(root / relative, row)
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(actual - EXCLUDED == owned, 'owned closed inventory differs')

    initial = load_json(root / 'INITIAL_SEAL.json')
    require(digest((root / 'INITIAL_MANIFEST.json').read_bytes()) ==
            initial['INITIAL_MANIFEST_SHA256'], 'early manifest differs')
    for row in load_json(root / 'INITIAL_MANIFEST.json')['files']:
        check_file(root / row['path'], row)
    require(digest((root / 'INITIAL_SEAL.json').read_bytes()) ==
            'dcaaf19b76f45a9efa7144ae948e34a610c0fc7d3248c3cea1c47b935829ad30',
            'independent early seal differs')

    source_manifest = load_json(root / 'SOURCE_NATIVE_MANIFEST.json')
    source = Path(source_manifest['source_root'])
    original_paths = set()
    for row in source_manifest['files']:
        p = Path(row['path'])
        check_file(p, row)
        original_paths.add(p.relative_to(source).as_posix())
    require({p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()}
            == original_paths, 'original source closed inventory differs')
    require(len(original_paths) == 77, 'original source file count differs')
    ready_raw = (source / 'SOURCE_READY.json').read_bytes()
    require(digest(ready_raw) ==
            '346d425ca3b35b03465fc6a3e0873b372ed2088c58ee9681354d41dad6de7576',
            'native readiness pin differs')
    require(ready_raw == (root / 'target/SOURCE_READY.original.json').read_bytes(),
            'whole raw initial readiness copy differs')
    ready = json.loads(ready_raw)
    native = load_json(root / 'FINAL_NATIVE_INPUTS.json')
    require(ready == source_manifest['whole_original_SOURCE_READY'] ==
            native['whole_original_SOURCE_READY'], 'whole native readiness differs')
    require(len(ready['whole_native_API_objects']) == 4, 'native API count differs')
    for row, saved in zip(ready['whole_native_API_objects'], native['whole_native_API_objects']):
        require(row == saved['original_identity'], 'native API identity/order differs')
        raw = check_file(Path(row['path']), row)
        require(json.loads(raw) == saved['whole_original_object'], 'whole native API differs')
    require(len(native['whole_native_API_objects']) == 4, 'saved API count differs')
    for name, field in [
        ('ALL_TRANSPORT_RECEIPTS.json', 'whole_original_transport_receipts'),
        ('NATIVE_SCHEMA_TYPES.json', 'whole_original_NATIVE_SCHEMA_TYPES'),
        ('QUEUE_BINDING.json', 'whole_original_QUEUE_BINDING'),
        ('ARCHIVE_CUSTODY.json', 'whole_original_ARCHIVE_CUSTODY'),
    ]:
        require(load_json(source / name) == native[field], 'whole native field differs: ' + name)
    require(isinstance(native['whole_original_transport_receipts'], list) and
            len(native['whole_original_transport_receipts']) == 7,
            'whole ordered native transport list differs')

    extracted = source / 'published-source/asset-001'
    package = extracted / 'supported_cycle_verification'
    archive = source / 'assets/supported-cycle-source-and-verification.zip'
    with zipfile.ZipFile(archive) as reader:
        entries = reader.infolist()
        names = set()
        regular = 0
        for item in entries:
            require(item.filename not in names, 'duplicate native ZIP member')
            names.add(item.filename)
            relative = Path(item.filename)
            require(not relative.is_absolute() and '..' not in relative.parts,
                    'unsafe native ZIP name')
            if item.is_dir():
                continue
            mode = item.external_attr >> 16
            require(not stat.S_ISLNK(mode), 'native ZIP symlink')
            data = reader.read(item)  # complete read checks stored CRC
            require(len(data) == item.file_size, 'native ZIP member size differs')
            require(data == (extracted / relative).read_bytes(),
                    'whole extracted native member differs: ' + item.filename)
            regular += 1
    require(regular == 27, 'native regular payload count differs')
    native_source_manifest = load_json(package / 'SOURCE_MANIFEST.json')
    require(native_source_manifest == native['whole_original_source_file_manifest'],
            'whole authored manifest differs')
    expected_source_members = set()
    for row in native_source_manifest['members']:
        path = package / row['path']
        check_file(path, {'bytes': row['bytes'], 'SHA256': row['sha256']})
        expected_source_members.add(row['path'])
    require({p.relative_to(package).as_posix() for p in package.rglob('*') if p.is_file()}
            == expected_source_members | {'SOURCE_MANIFEST.json'},
            'authored package closed inventory differs')
    binding = load_json(package / 'ORIGINAL_BINDING.json')
    require(binding == native['whole_original_original_binding'], 'whole original binding differs')
    require(len(binding['original_files']) == 8, 'historical original count differs')
    for row in binding['original_files']:
        check_file(package / 'original' / row['file'],
                   {'bytes': row['bytes'], 'SHA256': row['sha256']})

    expected = (package / 'verification/EXPECTED.json').read_bytes()
    require(digest(expected) ==
            '4fb31e9c781efa9341dce3469cabfb7ab3c36e38c7347f4cdf34f7501186ad97',
            'whole expected scientific result differs')
    for mode in ['normal', 'optimized', 'double-optimized']:
        require((root / ('native-' + mode + '.stdout.json')).read_bytes() == expected,
                'whole recorded native scientific output differs: ' + mode)
        require((root / ('native-' + mode + '.stderr')).read_bytes() == b'',
                'native scientific stderr nonempty: ' + mode)
    own = []
    for mode, optimization in [('normal', 0), ('optimized', 1)]:
        obj = load_json(root / ('own-cycle-final-' + mode + '.stdout.json'))
        require(obj.pop('optimization') == optimization, 'own mode field differs')
        require((root / ('own-cycle-final-' + mode + '.stderr')).read_bytes() == b'',
                'own scientific stderr nonempty')
        own.append(obj)
    require(own[0] == own[1], 'whole own semantic outputs differ')
    require(own[0]['literal_custom_status'] ==
            'INDEPENDENT_INTEGER_PREFIX_AND_EXPLICIT_CYCLE_CHAIN_DIAGNOSTICS_AGREE',
            'own literal custom diagnostic status differs')
    verdict = load_json(root / 'VERDICT.json')
    require(verdict['literal_custom_status'] ==
            'FULL_LITERAL_SUPPORTED_CYCLE_THEOREM_VALIDATED_WITH_STATED_LIMITS',
            'literal custom scientific verdict differs')
    require(verdict['followup'] is None and verdict['publication_authority'] is False,
            'scientific review authority boundary differs')
    return {
        'literal_custom_status': 'READ_ONLY_WHOLE_INPUT_AND_REVIEW_PAYLOAD_CLOSURE_CONFIRMED',
        'owned_payloads': len(owned), 'unchanged_original_source_files': len(original_paths),
        'native_API_objects_retained_whole': 4, 'native_transports_retained_whole_in_order': 7,
        'native_ZIP_regular_payloads_CRC_and_whole_bytes_checked': regular,
        'historical_authored_original_files_retained': 8,
        'native_science_modes_full_expected_bytes_checked': 3,
        'own_science_modes_whole_semantics_checked': 2,
        'imports_of_science_or_project_code': False,
        'scientific_execution_network_or_writes': False,
    }


def verify(root=None):
    root = Path(__file__).resolve().parent if root is None else Path(root)
    result = verify_payload(root)
    seal = load_json(root / 'FINAL_SEAL.json')
    require(digest((root / 'OWNED_MANIFEST.json').read_bytes()) ==
            seal['OWNED_MANIFEST_SHA256'], 'final owned manifest pin differs')
    for row in seal['terminal_payload_receipts']:
        require(row['path'] in EXCLUDED, 'unexpected terminal receipt path')
        check_file(root / row['path'], row)
    require(len(seal['terminal_payload_receipts']) == 5, 'terminal receipt count differs')
    require(seal['completion_estimate_percent_bounded_review'] == 100,
            'sealed bounded review incomplete')
    result['final_manifest_seal_and_terminal_receipt_bindings_confirmed'] = True
    return result


def main():
    require(sys.argv[1:] in [[], ['--payload-only']], 'unknown arguments')
    result = verify_payload() if sys.argv[1:] else verify()
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
