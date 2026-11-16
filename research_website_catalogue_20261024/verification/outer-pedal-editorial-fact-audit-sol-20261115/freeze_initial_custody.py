#!/usr/bin/env python3
"""One-shot source/root-only opaque intake; all writes are in this owned folder.

No supplied code is imported or executed. No editorial/site/Git/Sheet/network
path is opened. Stable namespaces/cooperative writers are assumed; directory
enumeration is not an OS isolation or transactional snapshot guarantee.
"""
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import zipfile

D = Path(__file__).absolute().parent
P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
SOURCE = P / 'papers/23331331/sources'
ROOT = P / 'papers/23331331/reviews/root'
AUTHORITY = P / 'verification/root-clearance-23331331-20261115.json'
CORE_REF = P / 'verification/supported-cycle-focal-independent-code-audit-sol-20261115/ACTUAL623_QUALIFIED_CORE.json'
checks = 0

def require(test, message):
    global checks
    if not test:
        raise RuntimeError(message)
    checks += 1

def digest(body):
    return hashlib.sha256(body).hexdigest()

def read_regular(path):
    path = Path(path)
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), 'not ordinary file: ' + str(path))
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        held = os.fstat(fd)
        require((before.st_dev, before.st_ino) == (held.st_dev, held.st_ino), 'open identity: ' + str(path))
        parts = []
        while True:
            piece = os.read(fd, 1024 * 1024)
            if not piece:
                break
            parts.append(piece)
        after = os.fstat(fd)
        require((held.st_size, held.st_mtime_ns, held.st_ctime_ns) == (after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'file changed: ' + str(path))
        require((path.lstat().st_dev, path.lstat().st_ino) == (held.st_dev, held.st_ino), 'pathname identity: ' + str(path))
        body = b''.join(parts)
        require(len(body) == held.st_size, 'short read: ' + str(path))
        return body
    finally:
        os.close(fd)

def binding(path, body):
    return {'path': str(path), 'bytes': len(body), 'SHA256': digest(body)}

def write_owned(relative, body):
    dest = D / relative
    require(dest.is_relative_to(D), 'outside owned namespace')
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open('xb') as stream:
        stream.write(body)
        stream.flush()
        os.fsync(stream.fileno())
    require(read_regular(dest) == body, 'owned copy mismatch')
    return binding(dest, body)

def write_json(relative, value):
    return write_owned(relative, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())

def strict_scan(root):
    root = Path(root)
    require(stat.S_ISDIR(root.lstat().st_mode), 'not ordinary root directory')
    files, dirs = [], []
    def visit(current):
        before = current.lstat()
        require(stat.S_ISDIR(before.st_mode), 'nonordinary directory')
        with os.scandir(current) as it:
            entries = sorted(it, key=lambda e: e.name)
        for entry in entries:
            path = current / entry.name
            st = path.lstat()
            rel = path.relative_to(root).as_posix()
            if stat.S_ISDIR(st.st_mode):
                dirs.append(rel)
                visit(path)
            elif stat.S_ISREG(st.st_mode):
                body = read_regular(path)
                files.append({'path': rel, 'bytes': len(body), 'SHA256': digest(body)})
            else:
                raise RuntimeError('symlink or special entry: ' + str(path))
        after = current.lstat()
        require((before.st_dev, before.st_ino, before.st_mtime_ns, before.st_ctime_ns) == (after.st_dev, after.st_ino, after.st_mtime_ns, after.st_ctime_ns), 'directory changed: ' + str(current))
    visit(root)
    return {'root': str(root), 'files': sorted(files, key=lambda x: x['path']), 'directories': sorted(dirs)}

def typed_equal(a, b):
    require(type(a) is type(b), 'type distinction lost')
    if type(a) is dict:
        require(list(a) == list(b), 'key order distinction lost')
        for key in a:
            typed_equal(a[key], b[key])
    elif type(a) is list:
        require(len(a) == len(b), 'list length distinction lost')
        for x, y in zip(a, b):
            typed_equal(x, y)
    else:
        require(a == b, 'literal value distinction lost')

authority_body = read_regular(AUTHORITY)
require(len(authority_body) == 129113 and digest(authority_body) == '27721f2437e7a9af2a8aabcf25f18599a1c667f32d0de2d7836fdc0ca8affc16', 'root authority pin')
authority = json.loads(authority_body)
write_owned('authority/root-clearance-23331331-20261115.json', authority_body)
contract_body = read_regular(ROOT / 'ROOT_NATIVE_CUSTODY_CONTRACT_20261115.json')
require(digest(contract_body) == authority['root_custody_contract']['SHA256'], 'root contract pin')
contract = json.loads(contract_body)
originals = []
for expected in contract['namespaces']:
    observed = strict_scan(expected['root'])
    typed_equal(observed, expected)
    originals.append(observed)
originals.append(strict_scan(ROOT))
for item in originals:
    label = 'source' if item['root'] == str(SOURCE) else Path(item['root']).name
    for directory in item['directories']:
        (D / 'custody' / label / directory).mkdir(parents=True, exist_ok=True)
    for record in item['files']:
        body = read_regular(Path(item['root']) / record['path'])
        require(len(body) == record['bytes'] and digest(body) == record['SHA256'], 'copy-time original pin')
        record['owned_copy'] = write_owned(Path('custody') / label / record['path'], body)

ready_body = read_regular(SOURCE / 'SOURCE_READY.json')
ready = json.loads(ready_body)
typed_equal(ready, authority['whole_original_SOURCE_READY'])
typed_equal(ready, authority['whole_literal_scope_VERDICT']['whole_original_source_READY'])
typed_equal(ready, authority['whole_literal_adversarial_VERDICT']['whole_original_SOURCE_READY'])
apis = []
for record in ready['whole_native_API_objects']:
    body = read_regular(record['path'])
    require(len(body) == record['bytes'] and digest(body) == record['SHA256'], 'whole API pin')
    apis.append({'role': record['role'], 'original_binding': record, 'whole_literal_object': json.loads(body)})

zip_body = read_regular(ready['all_native_assets_in_original_order'][0]['path'])
payloads = []
with zipfile.ZipFile(io.BytesIO(zip_body)) as archive:
    infos = archive.infolist()
    require(len(infos) == 38, 'exact original ZIP extent')
    for info in infos:
        require(not info.is_dir() and stat.S_ISREG(info.external_attr >> 16), 'ZIP ordinary payload')
        name = Path(info.filename)
        require(not name.is_absolute() and '..' not in name.parts, 'unsafe ZIP path')
        body = archive.read(info)
        original = SOURCE / 'published-source/asset-001' / info.filename
        require(read_regular(original) == body, 'ZIP complete extracted payload identity')
        payloads.append({'ordinal_zero_based': len(payloads), 'original_name': info.filename, 'bytes': len(body), 'SHA256': digest(body), 'CRC32': format(info.CRC, '08x'), 'native_date_time': list(info.date_time), 'native_external_attr': info.external_attr, 'native_create_system': info.create_system, 'native_flags': info.flag_bits, 'compression_method': info.compress_type, 'compressed_bytes': info.compress_size})

core_ref_body = read_regular(CORE_REF)
require(len(core_ref_body) == 13162 and digest(core_ref_body) == '0f285e35daa206f53aa931946c4bcc6c5b01ae6b4b59a231a861b0a6fe11d104', 'qualified core reference pin')
write_owned('authority/PRIOR_QUALIFIED_CORE.json', core_ref_body)
core_ref = json.loads(core_ref_body)
scripts = strict_scan(P / 'scripts')
require(scripts['directories'] == [], 'unexpected scripts directory extent')
require([str(P / 'scripts' / x['path']) for x in scripts['files']] == core_ref['actual_complete_scripts_namespace'], 'complete scripts namespace drift')
core = []
for record in core_ref['files']:
    body = read_regular(record['path'])
    require(len(body) == record['bytes'] and digest(body) == record['SHA256'], 'qualified core drift')
    core.append({'original': {k: record[k] for k in ['path', 'bytes', 'SHA256']}, 'owned_copy': write_owned(Path('custody/core') / Path(record['path']).relative_to(P), body)})

root_initial_path = P / 'verification/root-science-initial-23331331-20261115.json'
root_initial_body = read_regular(root_initial_path)
require(digest(root_initial_body) == authority['root_initial_authority']['SHA256'], 'root initial authority pin')
write_owned('authority/root-science-initial-23331331-20261115.json', root_initial_body)
write_json('ORIGINAL_SOURCE_SCIENCE_ROOT_CORE_CONTRACTS.json', {'schema': 'independent-source-root-core-finite-opaque-custody-v1', 'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'authority': binding(AUTHORITY, authority_body), 'namespaces': originals, 'original_root_custody_contract_whole_literal': contract, 'whole_original_SOURCE_READY': ready, 'whole_original_native_APIs': apis, 'whole_original_ZIP_regular_payloads': payloads, 'qualified_core': {'qualification': core_ref['qualification'], 'original17_plus_sole_authorized405b_checkpoint': True, 'all18_original_unchanged_claim': False, 'complete_scripts_directories': scripts['directories'], 'complete_scripts_files': scripts['files'], 'files': core}, 'special_entries_or_subtree_exclusions': [], 'editorial_exposure': False, 'original_programmes_executed': [], 'new_scientific_result_or_proof_review_claim': False})
write_json('INITIAL_CUSTODY_CAPTURE_RESULT.json', {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'checks': checks, 'original_namespaces': [{'root': x['root'], 'files': len(x['files']), 'directories': len(x['directories'])} for x in originals], 'ZIP_regular_payloads': len(payloads), 'whole_APIs': len(apis), 'qualified_core_files': len(core), 'source_history_false_pending_null_values_preserved': True, 'editorial_exposure': False, 'website_Git_Sheet_network_or_scientific_execution': False, 'completion_percent_initial_intake': 90})
print(json.dumps({'checks': checks, 'namespaces': [{'root': x['root'], 'files': len(x['files']), 'directories': len(x['directories'])} for x in originals], 'qualified_core_files': len(core), 'editorial_exposure': False}, indent=2))
