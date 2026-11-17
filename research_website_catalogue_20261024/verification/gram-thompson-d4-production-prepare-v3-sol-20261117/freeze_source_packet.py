#!/usr/bin/env python3
"""One administrative raw-byte/source-only freeze. Never execute release helpers."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/gram-thompson-d4-production-prepare-v3-sol-20261117'
BASE = P / 'verification/gram-thompson-d4-production-prepare-corrected-sol-20261117'
PAYLOADS = ['PLAN.diff', 'PLAN.json', 'READ_LEDGER.json', 'REPORT.md', 'RESEARCH_LOG.md',
            'SOURCE.diff', 'FIXED_INPUTS_BEFORE.json', 'FIXED_INPUTS_AFTER.json',
            'capture_fixed_inputs.py', 'freeze_source_packet.py', 'release_overlay.py']
TERMINALS = ['FINAL.json', 'MANIFEST.json', 'SEAL.json']
PINS = {
    'release_overlay.py': (115675, 'db93c08a28775a06c3925e60dac8d2732724c71ec62d2752083a56e1bf65c038'),
    'PLAN.json': (14057, 'f01b666bfd446e7ea10c1a8694bacd2d2046af1800c77ead0ecb25b620492137'),
    'SOURCE.diff': (3100, 'e81493bafafa339d0d295fe4b352593b9bb2965d61909498c5c705ec8bb84a0b'),
    'PLAN.diff': (3134, '7fa3b30df86d76d1a14dd25ca4c1b10cabc9237c5fc82bc7516223f4d7751464'),
}

def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)

def identity(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)

def read(path):
    first = path.lstat()
    require(stat.S_ISREG(first.st_mode), 'ordinary regular file required')
    require(not any(p.is_symlink() for p in (path, *path.parents)), 'no symbolic paths')
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        require(identity(first) == identity(os.fstat(descriptor)), 'same held open identity')
        blocks = []
        while True:
            block = os.read(descriptor, 1048576)
            if not block:
                break
            blocks.append(block)
        raw = b''.join(blocks)
        require(identity(first) == identity(os.fstat(descriptor)) == identity(path.lstat()), 'stable whole read')
        require(len(raw) == first.st_size, 'complete raw buffer')
        return raw
    finally:
        os.close(descriptor)

def pin(path):
    raw = read(path)
    return {'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(),
            'mode': format(stat.S_IMODE(path.lstat().st_mode), '04o')}

def write_new(name, value):
    raw = (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
    descriptor = os.open(OWN / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    try:
        os.fchmod(descriptor, 0o644)
        offset = 0
        while offset < len(raw):
            count = os.write(descriptor, raw[offset:])
            require(count > 0, 'complete terminal write')
            offset += count
        os.fsync(descriptor)
    finally:
        os.close(descriptor)

def replace_one(raw, old, new):
    require(raw.count(old) == 1, 'unique authorized raw-byte replacement')
    return raw.replace(old, new, 1)

require(Path(__file__).absolute() == OWN / 'freeze_source_packet.py', 'exact administrative sealer path')
require({p.name for p in OWN.iterdir()} == set(PAYLOADS), 'exact fresh eleven-file payload namespace')
for name in PAYLOADS:
    require(pin(OWN / name)['mode'] == '0644', 'all payloads ordinary inert 0644')
for name, (size, digest) in PINS.items():
    require(pin(OWN / name) == {'bytes': size, 'SHA256': digest, 'mode': '0644'}, 'exact personally read source/PLAN/diff pin')
old_source = read(BASE / 'release_overlay.py')
require(hashlib.sha256(old_source).hexdigest() == '0d570d53c86339222d3974c5d27abd42dd896332762b6c328d296b5079ff9583', 'frozen exact V2 source')
expected_source = replace_one(old_source, b"N=P/'verification/gram-thompson-d4-production-prepare-corrected-sol-20261117'", b"N=P/'verification/gram-thompson-d4-production-prepare-v3-sol-20261117'")
expected_source = replace_one(expected_source, b"PLAN_SHA='8268a30ba9b6a09c2b0e14886c89b29bcee67d4c5e75504818936c0241e89eae'", b"PLAN_SHA='f01b666bfd446e7ea10c1a8694bacd2d2046af1800c77ead0ecb25b620492137'")
old_block = b"""        # This ordinary main-thread Unix timer interrupts blocking urllib I/O.
        # It is not a SIGKILL/power-loss or hard-real-time scheduling guarantee.
        need(signal.getitimer(signal.ITIMER_REAL)==(0.0,0.0),'no inherited real timer to replace')
"""
new_block = b"""        # This ordinary main-thread Unix timer requires SIGALRM unblocked.
        # No uninterruptible-OS, SIGKILL/power-loss or hard-real-time guarantee.
        need(signal.getitimer(signal.ITIMER_REAL)==(0.0,0.0),'no inherited real timer to replace')
        need(callable(getattr(signal,'pthread_sigmask',None)) and hasattr(signal,'SIG_BLOCK'),'POSIX signal-mask inspection required before live GET')
        # SIG_BLOCK with an empty set inspects without changing inherited masks.
        need(signal.SIGALRM not in signal.pthread_sigmask(signal.SIG_BLOCK,set()),'live GET requires inherited SIGALRM unblocked; no mask changes')
"""
expected_source = replace_one(expected_source, old_block, new_block)
require(expected_source == read(OWN / 'release_overlay.py'), 'all other V2 source bytes unchanged')
old_plan = read(BASE / 'PLAN.json')
require(hashlib.sha256(old_plan).hexdigest() == '8268a30ba9b6a09c2b0e14886c89b29bcee67d4c5e75504818936c0241e89eae', 'frozen exact V2 PLAN')
expected_plan = replace_one(old_plan, b'production-prepare-corrected-sol-20261117', b'production-prepare-v3-sol-20261117')
expected_plan = replace_one(expected_plan, b'Each live GET is limited to expected bytes+1', b'Each live GET first requires available POSIX pthread_sigmask(SIG_BLOCK, empty set) inspection with SIGALRM unblocked, without changing the inherited mask, then is limited to expected bytes+1')
expected_plan = replace_one(expected_plan, b'No SIGKILL/power-loss or hard-real-time guarantee, UI/PDF rendering/future-persistence certificate.', b'No uninterruptible-OS, SIGKILL/power-loss or hard-real-time guarantee, UI/PDF rendering/future-persistence certificate.')
require(expected_plan == read(OWN / 'PLAN.json'), 'all other V2 PLAN bytes unchanged')
before = json.loads(read(OWN / 'FIXED_INPUTS_BEFORE.json'))
after = json.loads(read(OWN / 'FIXED_INPUTS_AFTER.json'))
require(before['entries'] == after['entries'] and after['entries_identical_to_before'] is True, 'whole bounded custody before/after equality')
expected_paths = {row['path'] for row in after['entries']}
actual_paths = set()
for root_name in after['roots']:
    root = Path(root_name)
    actual_paths.add(str(root))
    if root.is_dir():
        actual_paths.update(str(p) for p in root.rglob('*'))
require(actual_paths == expected_paths, 'same complete bounded input namespaces at freeze')
for row in after['entries']:
    path = Path(row['path'])
    info = path.lstat()
    require((info.st_dev, info.st_ino, format(stat.S_IMODE(info.st_mode), '04o'), info.st_mtime_ns, info.st_ctime_ns) == (row['device'], row['inode'], row['mode'], row['mtime_ns'], row['ctime_ns']), 'same fixed identity/mode/nanosecond timestamps at freeze')
    if row['kind'] == 'file':
        require(pin(path) == {key: row[key] for key in ('bytes', 'SHA256', 'mode')}, 'same whole fixed file at freeze')
    else:
        require(stat.S_ISDIR(info.st_mode) and row['empty'] == (not any(path.iterdir())), 'same ordinary fixed directory/empty topology at freeze')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
final = {'schema': 'inert-source-correction-v3-final-v1',
         'status': 'SOURCE_PREPARED_PENDING_INDEPENDENT_STATIC_REVIEW_AND_ROOT_FULL_READ',
         'UTC': now, 'scope': str(OWN), 'completion_percent_assigned_source_preparation': 100,
         'helper': pin(OWN / 'release_overlay.py'), 'PLAN': pin(OWN / 'PLAN.json'),
         'source_diff': pin(OWN / 'SOURCE.diff'), 'PLAN_diff': pin(OWN / 'PLAN.diff'),
         'whole_other_V2_source_and_PLAN_bytes_unchanged': True,
         'bounded_fixed_inputs_unchanged_through_freeze': True,
         'release_helper_all_mode_invocations': 0, 'release_helper_import_AST_compile_help_test': 0,
         'Git_W_designated_runtime_ignore_network_Sheet_install_deploy_actions': 0,
         'external_individual_contact': 0, 'source_preparation_only': True,
         'independent_static_review_and_root_full_actual_read_still_required': True,
         'publication_or_future_action_authority': False, 'AA': None, 'redirect': None, 'follow_up': None}
write_new('FINAL.json', final)
all_names = sorted(PAYLOADS + TERMINALS)
manifest = {'schema': 'finite-source-only-packet-manifest-v1', 'scope': str(OWN),
            'file_count': len(all_names), 'child_directory_count': 0,
            'root_mode': format(stat.S_IMODE(OWN.lstat().st_mode), '04o'),
            'terminal_content_hash_exclusions_exact': ['MANIFEST.json', 'SEAL.json'],
            'entries': [{'path': name, 'kind': 'file', **pin(OWN / name)} if name not in ('MANIFEST.json', 'SEAL.json') else
                        {'path': name, 'kind': 'file', 'mode': '0644',
                         'content_hash_exclusion': 'Acyclic terminal: actual complete external SHA256 and byte length reported to root; this marker is not a hash.'}
                        for name in all_names],
            'source_preparation_only': True, 'publication_or_future_action_authority': False}
write_new('MANIFEST.json', manifest)
seal = {'schema': 'acyclic-source-only-terminal-seal-v1', 'scope': str(OWN), 'UTC': now,
        'file_count': len(all_names), 'child_directory_count': 0, 'exact_file_names': all_names,
        'FINAL': pin(OWN / 'FINAL.json'), 'MANIFEST': pin(OWN / 'MANIFEST.json'),
        'helper': pin(OWN / 'release_overlay.py'), 'PLAN': pin(OWN / 'PLAN.json'),
        'self_hash_excluded_actual_external_pin_reported_to_root': True,
        'source_preparation_only': True, 'publication_or_future_action_authority': False}
write_new('SEAL.json', seal)
require({p.name for p in OWN.iterdir()} == set(all_names), 'exact complete final finite namespace')
for name in all_names:
    require(pin(OWN / name)['mode'] == '0644', 'final ordinary 0644 files only')
directory_fd = os.open(OWN, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
try:
    os.fsync(directory_fd)
finally:
    os.close(directory_fd)
print(json.dumps({'status': final['status'], 'files': len(all_names), 'child_directories': 0,
                  'terminal_pins': {name: pin(OWN / name) for name in TERMINALS},
                  'release_helper_invocations': 0, 'publication_or_future_action_authority': False}, sort_keys=True))
