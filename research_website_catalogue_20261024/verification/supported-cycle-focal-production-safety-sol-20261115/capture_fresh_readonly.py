"""New bounded fresh read-only capture; explicit root GO required.

Default does not inspect W. Explicit capture reads W and immutable adopted
references, invokes only the listed local read-only Git commands, and writes
exclusive new receipts below this own folder. No network or W/Git mutation,
renderer, scientific/native/archive/control execution or project imports.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import stat
import struct
import subprocess
import sys
import traceback

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
R = P / 'verification/supported-cycle-focal-production-safety-sol-20261115'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
I = P / 'verification/supported-cycle-focal-v2-integration-audit-sol-20261115'
INITIAL = '3b3c146a18031cd6261cb04fc8f7dc9ee47b97bc993eba34a6bcb6adf240fe88'
CHECKS = 0
OUT = R / 'fresh-readonly'
CREATED_THIS_ATTEMPT = False


def need(ok, why):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise RuntimeError(why)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def metadata(info):
    return {'mode': info.st_mode, 'device': info.st_dev, 'inode': info.st_ino,
            'links': info.st_nlink, 'uid': info.st_uid, 'gid': info.st_gid,
            'size': info.st_size, 'mtime_ns': info.st_mtime_ns, 'ctime_ns': info.st_ctime_ns}


def ordinary_read(path, root):
    need(path.is_absolute() and path.is_relative_to(root), 'Fixed input root')
    need(path.resolve() == path, 'No symlink in input ancestry')
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode), 'Ordinary input file')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        opened = os.fstat(fd)
        need(metadata(before) == metadata(opened), 'Stable held input identity')
        parts = []
        while True:
            part = os.read(fd, 1024 * 1024)
            if not part:
                break
            parts.append(part)
        data = b''.join(parts)
        after = os.fstat(fd)
        need(metadata(opened) == metadata(after) == metadata(path.lstat()), 'Stable input while read')
        need(len(data) == opened.st_size, 'Full input body')
        return data, {'path': str(path), 'bytes': len(data), 'SHA256': sha(data),
                      'stat': metadata(opened), 'observed_atime_ns_before': opened.st_atime_ns,
                      'observed_atime_ns_after': after.st_atime_ns}
    finally:
        os.close(fd)


def reference(path, item):
    data, _ = ordinary_read(path, P)
    need(len(data) == item['bytes'] and sha(data) == item['SHA256'], 'Immutable reference pin')
    return data


def new(path, data):
    need(path.is_relative_to(OUT) and path.parent.resolve() == path.parent, 'Own fresh output only')
    with path.open('xb') as stream:
        need(stream.write(data) == len(data), 'Exclusive complete own receipt write')
    return {'path': str(path), 'bytes': len(data), 'SHA256': sha(data)}


def js(path, value):
    return new(path, (json.dumps(value, indent=2, ensure_ascii=True) + '\n').encode())


def public_extent():
    root = W / 'public'
    need(root.resolve() == root and stat.S_ISDIR(root.lstat().st_mode), 'Ordinary exact public root')
    files, directories = [], []

    def walk(parent):
        for entry in os.scandir(parent):
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISDIR(info.st_mode):
                need(path.resolve() == path, 'Ordinary public directory ancestry')
                directories.append({'path': relative, 'stat': metadata(info)})
                walk(path)
            else:
                need(stat.S_ISREG(info.st_mode), 'No public symlink or special object')
                body, item = ordinary_read(path, W)
                item['public_relative_path'] = relative
                files.append(item)

    walk(root)
    return sorted(files, key=lambda r: r['public_relative_path']), sorted(directories, key=lambda r: r['path'])


def fence(files, directories):
    return ([{k: v for k, v in item.items() if not k.startswith('observed_atime')}
             for item in files], directories)


def native_index(data, target_paths):
    need(data[:4] == b'DIRC' and hashlib.sha1(data[:-20]).digest() == data[-20:],
         'Complete native SHA1 index header/checksum')
    version, count = struct.unpack('>II', data[4:12])
    need(version in (2, 3), 'Only reviewed native version2/3 index layout')
    offset = 12
    records, protected, tuples = [], [], []
    for ordinal in range(count):
        start = offset
        need(offset + 62 <= len(data) - 20, 'Native entry fixed header bounds')
        values = struct.unpack('>10I', data[offset:offset + 40])
        oid = data[offset + 40:offset + 60]
        flags = struct.unpack('>H', data[offset + 60:offset + 62])[0]
        offset += 62
        extended = None
        if flags & 0x4000:
            need(version == 3 and offset + 2 <= len(data) - 20, 'Native extended flags')
            extended = struct.unpack('>H', data[offset:offset + 2])[0]
            offset += 2
        end = data.index(b'\0', offset, len(data) - 20)
        path = data[offset:end]
        need((flags & 0xfff) == min(len(path), 0xfff), 'Native filename byte length bits')
        offset = start + ((end - start + 1 + 7) // 8) * 8
        need(offset <= len(data) - 20 and not any(data[end:offset]), 'Exact native NUL/alignment padding')
        raw = data[start:offset]
        stage = (flags >> 12) & 3
        name = path.decode('utf-8', errors='surrogateescape')
        tuples.append(('%o %s %d\t' % (values[6], oid.hex(), stage)).encode() + path + b'\0')
        record = {'ordinal': ordinal, 'path_bytes_hex': path.hex(), 'stat_fields': list(values),
                  'OID_hex': oid.hex(), 'flags': flags, 'extended_flags': extended,
                  'padding_hex': data[end:offset].hex(), 'raw_record_SHA256': sha(raw)}
        records.append(record)
        if name not in target_paths:
            protected.append(struct.pack('>I', len(raw)) + raw)
    extensions = []
    while offset < len(data) - 20:
        need(offset + 8 <= len(data) - 20, 'Native extension header bounds')
        signature = data[offset:offset + 4]
        size = struct.unpack('>I', data[offset + 4:offset + 8])[0]
        offset += 8
        need(offset + size <= len(data) - 20, 'Whole native extension bounds')
        body = data[offset:offset + size]
        extensions.append({'signature_hex': signature.hex(), 'bytes': size,
                           'SHA256': sha(body), 'whole_body_hex': body.hex()})
        offset += size
    need(offset == len(data) - 20, 'Whole native index extent')
    return {'version': version, 'count': count, 'records': records, 'extensions': extensions,
            'checksum_hex': data[-20:].hex()}, b''.join(protected), b''.join(tuples)


def git_commands():
    return [['rev-parse', '--show-toplevel'], ['rev-parse', '--show-object-format'],
            ['symbolic-ref', 'HEAD'], ['rev-parse', 'HEAD'],
            ['rev-parse', 'refs/heads/master'], ['rev-parse', 'HEAD^{tree}'],
            ['ls-files', '--stage', '-z'],
            ['diff', '--cached', '--no-ext-diff', '--no-textconv', '--name-status', '-z',
             '0880af3e389248dbcd098ac275a880d93e09ea99'],
            ['diff', '--cached', '--no-ext-diff', '--no-textconv', '--name-only', '--diff-filter=D', '-z',
             '0880af3e389248dbcd098ac275a880d93e09ea99']]


def local_git(arguments, ordinal):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update({'GIT_OPTIONAL_LOCKS': '0', 'GIT_TERMINAL_PROMPT': '0',
                'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null',
                'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_ATTR_NOSYSTEM': '1'})
    command = ['/usr/bin/git', '-c', 'maintenance.auto=false', '-c', 'gc.auto=0',
               '-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false'] + arguments
    start = now()
    process = subprocess.run(command, cwd=W, env=env, capture_output=True, timeout=60)
    out = new(OUT / ('git-%02d.stdout' % ordinal), process.stdout)
    err = new(OUT / ('git-%02d.stderr' % ordinal), process.stderr)
    receipt = {'started_UTC': start, 'completed_UTC': now(), 'command': command,
               'exit_code': process.returncode, 'whole_stdout': out, 'whole_stderr': err,
               'no_network_command': True, 'optional_locks_hooks_fsmonitor_maintenance_disabled': True}
    js(OUT / ('git-%02d.receipt.json' % ordinal), receipt)
    need(process.returncode == 0 and not process.stderr, 'Actual bounded local Git command')
    return process.stdout


def capture(go_path, go_sha):
    global CREATED_THIS_ATTEMPT
    need(go_path.parent == P / 'verification' and go_path.name.startswith('root-'), 'Root GO reference boundary')
    go_data, _ = ordinary_read(go_path, P)
    need(sha(go_data) == go_sha, 'Exact root-forwarded GO bytes')
    go = json.loads(go_data)
    helper, _ = ordinary_read(Path(__file__).absolute(), P)
    initial, _ = ordinary_read(R / 'INITIAL_SEAL.json', P)
    need(sha(initial) == INITIAL, 'Source-only immutable INITIAL')
    need(go['authority'] == 'root' and go['INITIAL_SEAL_SHA256'] == INITIAL and
         go['capture_helper_SHA256'] == sha(helper) and go['authorized_readonly_capture'] is True and
         go['website_root'] == str(W) and go['network'] is False and
         go['production_authority'] is False, 'Explicit exact-code read-only root GO')
    need(not OUT.exists(), 'Fresh own capture folder only; no overwrite')
    OUT.mkdir()
    CREATED_THIS_ATTEMPT = True
    js(OUT / 'GO_REFERENCE.json', {'path': str(go_path), 'bytes': len(go_data), 'SHA256': go_sha,
                                 'whole_original_GO': go})
    oracle = json.loads(ordinary_read(R / 'SOURCE_ONLY_PRODUCTION_ORACLE.json', P)[0])
    source_inputs = json.loads(ordinary_read(R / 'INITIAL_INPUTS.json', P)[0])
    reference(Path(source_inputs['root_adoption']['path']), source_inputs['root_adoption'])
    for item in source_inputs['whole_root_adopted_outputs']:
        reference(Path(item['path']), item)
    for item in source_inputs['publication_contracts']:
        reference(Path(item['path']), item)
    for item in source_inputs['old_baseline_reference_metadata']:
        reference(Path(item['path']), item)
    historical_guard = json.loads(reference(Path(source_inputs['old_writer_pre_guard_by_reference']['path']),
                                            source_inputs['old_writer_pre_guard_by_reference']))
    protected_source = [{'path': path, **item} for path, item in
                        historical_guard['protected_source_science_core_whole_bindings'].items()]
    need(len(protected_source) == 558, 'Bounded original source/science/core reference count')
    for item in protected_source:
        reference(Path(item['path']), item)
    qualified = json.loads(ordinary_read(I / 'ACTUAL623_QUALIFIED_CORE.json', P)[0])
    need(qualified['original17_plus_sole_authorized405b_checkpoint'] is True and
         qualified['all18_original_unchanged_claim'] is False and len(qualified['files']) == 18,
         'Qualified17original plus separate405b core; no global cache obligation')
    for item in qualified['files']:
        reference(Path(item['path']), item)
    old_base = json.loads(ordinary_read(I / 'ACTUAL623_PUBLIC_BASELINE.json', P)[0])
    need(W.resolve() == W and stat.S_ISDIR(W.lstat().st_mode) and
         (W / '.git').resolve() == W / '.git' and stat.S_ISDIR((W / '.git').lstat().st_mode),
         'Exact ordinary W and Git control directory')
    need(not (W / '.git/index.lock').exists(), 'No concurrent index lock')
    controls = oracle['historical_six_site_config_expected_pins'] + oracle['historical_Git_control_expected_pins']
    before_controls = []
    for item in controls:
        body, current = ordinary_read(Path(item['path']), W)
        need(len(body) == item['bytes'] and sha(body) == item['SHA256'], 'Fresh config/control matches source oracle')
        before_controls.append(current)
    index_before, index_observation = ordinary_read(W / '.git/index', W)
    need(sha(index_before) == '35181f4046df6e197ba5c5c6e34c348b2b46783c0cc073a5b7f066692ba332b6',
         'Fresh complete raw index matches immutable historical source')
    new(OUT / 'native-index.before', index_before)
    target_paths = {item['output_relative_to_W'] for item in oracle['adopted_exact_ten_outputs_in_original_manifest_order']}
    decoded, protected, tuples = native_index(index_before, target_paths)
    need(decoded['count'] == 58563 and len(decoded['records']) == 58563, 'Full fresh native record count')
    need(sum(1 for r in decoded['records'] if bytes.fromhex(r['path_bytes_hex']).decode('utf-8', errors='surrogateescape')
             not in target_paths) == 58561, 'Full fresh protected record count')
    js(OUT / 'NATIVE_INDEX_FULL_RECORDS.json', decoded)
    new(OUT / 'protected-native-records.bin', protected)
    new(OUT / 'stage-tuples.z', tuples)
    files, dirs = public_extent()
    expected = {item['public_relative_path']: item for item in old_base['public_files']}
    need([item['public_relative_path'] for item in files] == sorted(expected) and
         [item['path'] for item in dirs] == old_base['public_directories'], 'Full fresh623/public directory namespace')
    for item in files:
        old = expected[item['public_relative_path']]
        need(item['bytes'] == old['bytes'] and item['SHA256'] == old['SHA256'], 'All623 fresh bodies unchanged')
    for item in oracle['adopted_exact_ten_outputs_in_original_manifest_order']:
        target = W / item['output_relative_to_W']
        if item['role'] == 'exclusive_new_leaf':
            need(not target.exists() and not target.is_symlink(), 'All eight future leaves absent')
        else:
            need(target.lstat().st_nlink == 1, 'Aggregate target not hard-linked')
    outputs = [local_git(arguments, i + 1) for i, arguments in enumerate(git_commands())]
    need(outputs[0].decode().strip() == str(W) and outputs[1] == b'sha1\n' and
         outputs[2] == b'refs/heads/master\n', 'Actual local repository identity')
    need(outputs[3] == outputs[4] == b'0880af3e389248dbcd098ac275a880d93e09ea99\n' and
         outputs[5] == b'41a222e824f23b5efc0acd4f5a92ea50c4572cfa\n', 'Actual fresh local HEAD/master/tree')
    need(outputs[6] == tuples and outputs[8] == b'', 'Native tuple identity and zero actual cached deletions')
    local_final = local_git(['rev-parse', 'HEAD', 'refs/heads/master', 'HEAD^{tree}'], 10)
    need(local_final == outputs[3] + outputs[4] + outputs[5], 'Final local identity fence')
    after_files, after_dirs = public_extent()
    need(fence(files, dirs) == fence(after_files, after_dirs), 'Complete public body/stat/mode/directory before-after fence')
    for item in before_controls:
        _, after = ordinary_read(Path(item['path']), W)
        need({k: v for k, v in item.items() if not k.startswith('observed_atime')} ==
             {k: v for k, v in after.items() if not k.startswith('observed_atime')}, 'Whole config/control fence')
    index_after, after_index_stat = ordinary_read(W / '.git/index', W)
    need(index_after == index_before and index_observation['stat'] == after_index_stat['stat'] and
         not (W / '.git/index.lock').exists(), 'Whole raw index/stat unchanged by capture')
    for item in protected_source:
        reference(Path(item['path']), item)
    for item in qualified['files']:
        reference(Path(item['path']), item)
    result = {'UTC': now(), 'status': 'FRESH_LOCAL_READONLY_CAPTURE_PASS', 'checks': CHECKS,
              'source_only_INITIAL_SHA256': INITIAL, 'root_GO_SHA256': go_sha,
              'capture_helper_SHA256': sha(helper), 'website_root': str(W),
              'full_public_files': files, 'full_public_directories': dirs,
              'all623_configs_controls_before_after_unchanged': True, 'controls': before_controls,
              'whole_native_index_stat': index_observation, 'native_records': 58563,
              'protected_complete_raw_records': 58561, 'staged_deletions': 0,
              'actual_local_readonly_Git_commands': 10, 'fresh_remote_network_query': False,
              'historical_remote_advertisement_not_relabelled_fresh': True,
              'source_science_core_reference_fences': 558,
              'qualified17original_plus_separate405b_core_reference_fences': True,
              'network_or_W_Git_mutations': False, 'production_authority': False,
              'canonical_url': None, 'AA': None, 'follow_up': None,
              'stable_cooperative_filesystem_not_atomic_global_snapshot': True}
    js(OUT / 'FRESH_CAPTURE.json', result)
    print(json.dumps({'status': result['status'], 'checks': CHECKS, 'public_files': len(files),
                      'public_directories': len(dirs), 'native_records': 58563,
                      'protected_records': 58561, 'local_Git_commands': 10,
                      'network_or_W_Git_mutations': False, 'production_authority': False}, indent=2))


def main():
    if len(sys.argv) == 1:
        print(json.dumps({'status': 'NO_ACTION_ROOT_GO_REQUIRED', 'W_inspection': False,
                          'Git_commands': 0, 'network': False, 'filesystem_writes': False}))
        return
    need(len(sys.argv) == 4 and sys.argv[1] == '--capture', 'Only explicit bounded root-GO capture')
    capture(Path(sys.argv[2]), sys.argv[3])


if __name__ == '__main__':
    try:
        main()
    except Exception:
        if CREATED_THIS_ATTEMPT and OUT.exists() and OUT.is_dir() and OUT.resolve() == OUT:
            path = OUT / 'ACTUAL_FAILURE.txt'
            if not path.exists():
                with path.open('x') as stream:
                    stream.write(traceback.format_exc())
        raise
