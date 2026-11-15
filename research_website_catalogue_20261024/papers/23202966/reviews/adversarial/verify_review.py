"""Pure offline custody checker. Reads only; no target imports, execution or network."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
import zlib

ROOT = Path(__file__).resolve().parent
TERMINALS = ('FINAL_MANIFEST.json', 'FINAL_CLOSURE.json', 'FINAL_SEAL.json')
CHECKS = 0


def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def body(path):
    require(not path.is_symlink(), 'symlink: ' + str(path))
    require(path.is_file(), 'missing regular file: ' + str(path))
    return path.read_bytes()


def check_pin(entry, path=None):
    path = Path(entry['path']) if path is None else path
    raw = body(path)
    require(len(raw) == entry['bytes'], 'size: ' + str(path))
    require(digest(raw) == entry['SHA256'], 'hash: ' + str(path))
    return raw


def typed_equal(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(typed_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(typed_equal(x, y) for x, y in zip(a, b))
    return a == b


def namespace(root):
    files, directories = [], []
    for path in sorted(root.rglob('*')):
        require(not path.is_symlink(), 'namespace symlink: ' + str(path))
        rel = path.relative_to(root).as_posix()
        if path.is_dir():
            directories.append(rel)
        else:
            require(path.is_file(), 'nonregular: ' + str(path))
            files.append(rel)
    return sorted(files), sorted(directories)


def main():
    require(sys.argv[1:] in ([], ['--preseal']), 'unsupported arguments')
    preseal = sys.argv[1:] == ['--preseal']
    manifest = json.loads(body(ROOT / 'FINAL_MANIFEST.json'))
    require(manifest['owned_root'] == str(ROOT), 'owned root mismatch')
    require(manifest['exact_root_terminal_exclusions'] == list(TERMINALS), 'terminal exclusions')
    actual_files, actual_dirs = namespace(ROOT)
    payloads = [x for x in actual_files if x not in TERMINALS]
    require(payloads == sorted(x['path'] for x in manifest['files']), 'closed file namespace')
    require(actual_dirs == manifest['directories'], 'closed directory namespace')
    for entry in manifest['files']:
        rel = Path(entry['path'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'unsafe owned path')
        check_pin(entry, ROOT / rel)

    initial = json.loads(body(ROOT / 'INITIAL_SEAL.json'))
    for entry in initial['files']:
        check_pin(entry)
    initial_inputs = json.loads(body(ROOT / 'INITIAL_INPUTS.json'))
    require(initial_inputs['source_manifest_payloads'] == 79, 'source payload count')
    require(initial_inputs['exact_source_terminal_files'] == 3, 'source terminal count')
    require(initial_inputs['actual_source_files'] == 82, 'actual source count')
    source = Path(initial_inputs['source_READY']['path']).parent
    ready = json.loads(check_pin(initial_inputs['source_READY']))
    require(digest(body(source / 'SOURCE_READY_SEAL.json')) ==
            '9a87a851ebab2735927edb66d350168fdb9d20e738ab6a9bc2e85b7f3a93ed63', 'source seal pin')
    require(ready['native_version_whole_field'] == {'present': False, 'original_value': None},
            'absent native version distinction')
    require(ready['printed_title_date_version_inspected'] is False, 'historical printed flag changed')
    require(ready['printed_date'] is None and ready['printed_version'] is None,
            'historical printed null changed')
    source_files, source_directories = namespace(source)
    final_inputs = json.loads(body(ROOT / 'FINAL_INPUTS.json'))
    require(source_directories == final_inputs['source_directories'], 'closed source directory namespace')
    expected_source = initial_inputs['all_82_file_pins']
    require(source_files == sorted(str(Path(x['path']).relative_to(source)) for x in expected_source),
            'closed source file namespace')
    for entry in expected_source:
        check_pin(entry)
    custody = json.loads(body(ROOT / 'CUSTODY_CHECKPOINT.json'))
    members = custody['ZIP_regular_payloads_fullbyte_checked']
    with zipfile.ZipFile(source / 'assets' / 'verification.zip') as archive:
        infos = archive.infolist()
        require(len(infos) == len(members) == 28, 'regular ZIP payload count')
        for info, entry in zip(infos, members):
            require(not info.is_dir() and info.filename == entry['member'], 'ZIP member order/name')
            raw = archive.read(info)
            require(len(raw) == info.file_size == entry['bytes'], 'ZIP size')
            require((zlib.crc32(raw) & 0xffffffff) == info.CRC == int(entry['CRC32'], 16), 'ZIP CRC')
            require(digest(raw) == entry['SHA256'], 'ZIP hash')
            require(raw == body(source / 'published-source' / 'asset-004' / info.filename), 'ZIP extraction bytes')

    replay = json.loads(body(ROOT / 'NATIVE_REPLAY_RECEIPT.json'))
    require([run['mode'] for run in replay['runs']] == ['normal', 'optimized'], 'native replay run inventory')
    require(replay['unchanged_source_proven'] is True, 'unchanged native source flag')
    require(body(Path(replay['source'])) == body(Path(replay['isolated_copy'])), 'native copy equality')
    expected_bytes = body(ROOT / 'inputs' / 'native-root_compiler_check.json')
    expected = json.loads(expected_bytes)
    require(typed_equal(expected, replay['whole_expected_original']), 'whole expected object changed')
    for run in replay['runs']:
        mode = run['mode']
        out = body(ROOT / ('native-' + mode + '.stdout'))
        err = body(ROOT / ('native-' + mode + '.stderr'))
        require(run['exit_code'] == 0, 'native exit')
        require(len(out) == run['stdout_bytes'] and digest(out) == run['stdout_SHA256'], 'native stdout pin')
        require(len(err) == run['stderr_bytes'] == 0 and digest(err) == run['stderr_SHA256'], 'native stderr pin')
        require(out == expected_bytes, 'native whole expected bytes differ')
        require(typed_equal(json.loads(out), expected), 'native typed whole expected differs')
        require(run['whole_typed_expected_difference'] == [], 'native expected difference receipt')

    ledger = json.loads(body(ROOT / 'POST_INITIAL_READ_LEDGER.json'))
    for entry in ledger['entries'] + ledger['foreign_primary_bodies']:
        check_pin(entry)
    verdict = json.loads(body(ROOT / 'CUSTOM_VERDICT.json'))
    require(verdict['record_id'] == 23202966, 'record identity')
    require(verdict['follow_up'] is None, 'follow-up must remain literal null')
    require(verdict['extensive_AI_review_not_human_peer_review'] is True, 'review disclosure')
    require(verdict['formal_certification_reproduced'] is False, 'formal certification limitation')
    if not preseal:
        require(all((ROOT / x).is_file() for x in TERMINALS), 'missing exact terminal')
        seal = json.loads(body(ROOT / 'FINAL_SEAL.json'))
        require(seal['FINAL_MANIFEST_SHA256'] == digest(body(ROOT / 'FINAL_MANIFEST.json')), 'final manifest seal')
        require(seal['FINAL_CLOSURE_SHA256'] == digest(body(ROOT / 'FINAL_CLOSURE.json')), 'final closure seal')
        closure = json.loads(body(ROOT / 'FINAL_CLOSURE.json'))
        require(all(x['exit_code'] == 0 and x['stderr_bytes'] == 0 for x in closure['runs']), 'preseal closure exits')
    print(json.dumps({'status': 'PASS', 'mode': 'preseal' if preseal else 'terminal',
                      'checks': CHECKS, 'owned_payloads': len(payloads), 'owned_directories': len(actual_dirs),
                      'source_files': 82, 'ZIP_regular_payloads': 28,
                      'target_code_executed': False, 'network_requests': 0, 'writes': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
