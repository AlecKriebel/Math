#!/usr/bin/env python3
"""Opaque informed editorial intake/comparison; no renderer or science execution.

Only this audit folder receives new files. Existing source/root/core and the
producer packet are read only. Cache observations are diagnostic, not immutable
cross-project requirements. Cooperative stable namespaces are assumed.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

D = Path(__file__).absolute().parent
P = D.parents[1]
E = P / 'papers/23331331/reviews/editorial'
checks = 0

def need(ok, why):
    global checks
    checks += 1
    if not ok:
        raise ValueError(why)

def read(path):
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode), 'not ordinary file ' + str(path))
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        held = os.fstat(fd)
        need((before.st_dev, before.st_ino) == (held.st_dev, held.st_ino), 'file open identity')
        parts = []
        while True:
            part = os.read(fd, 1048576)
            if not part:
                break
            parts.append(part)
        after = os.fstat(fd)
        need((held.st_size, held.st_mtime_ns, held.st_ctime_ns) == (after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'concurrent file modification')
        need((path.lstat().st_dev, path.lstat().st_ino) == (held.st_dev, held.st_ino), 'file final identity')
        body = b''.join(parts)
        need(len(body) == held.st_size, 'short read')
        return body
    finally:
        os.close(fd)

def pin(body):
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest()}

def scan(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'not ordinary root')
    files, dirs = [], []
    def visit(path):
        before = path.lstat()
        with os.scandir(path) as iterator:
            entries = sorted(iterator, key=lambda x: x.name)
        for entry in entries:
            q = path / entry.name
            rel = q.relative_to(root).as_posix()
            mode = q.lstat().st_mode
            if stat.S_ISDIR(mode):
                dirs.append(rel)
                visit(q)
            elif stat.S_ISREG(mode):
                files.append({'path': rel, **pin(read(q))})
            else:
                raise ValueError('symlink or special entry ' + str(q))
        after = path.lstat()
        need((before.st_dev, before.st_ino, before.st_mtime_ns, before.st_ctime_ns) == (after.st_dev, after.st_ino, after.st_mtime_ns, after.st_ctime_ns), 'concurrent directory modification')
    visit(root)
    return {'root': str(root), 'files': sorted(files, key=lambda x: x['path']), 'directories': sorted(dirs)}

def typed(a, b):
    need(type(a) is type(b), 'literal type difference')
    if type(a) is dict:
        need(list(a) == list(b), 'literal key order difference')
        for key in a:
            typed(a[key], b[key])
    elif type(a) is list:
        need(len(a) == len(b), 'literal list length difference')
        for x, y in zip(a, b):
            typed(x, y)
    else:
        need(a == b, 'literal value difference')

def write(relative, body):
    dest = D / relative
    need(dest.is_relative_to(D), 'outside write')
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open('xb') as stream:
        need(stream.write(body) == len(body), 'short write')
        stream.flush()
        os.fsync(stream.fileno())
    need(read(dest) == body, 'owned complete copy difference')

def write_json(relative, value):
    write(relative, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())

seal_body = read(E / 'FINAL_SEAL.json')
need(pin(seal_body) == {'bytes': 3822, 'SHA256': 'a6199b1d554dcfaae1201c2440ec0b92d97caf5c6d71fc6e24919bf781e898a5'}, 'parent forwarded seal')
seal = json.loads(seal_body)
manifest_body = read(E / 'OWNED_MANIFEST.json')
need(pin(manifest_body) == seal['OWNED_MANIFEST'], 'same-buffer producer manifest pin')
manifest = json.loads(manifest_body)
actual = scan(E)
terminals = {'FINAL_SEAL.json', 'OWNED_MANIFEST.json'}
payload = {**actual, 'files': [x for x in actual['files'] if x['path'] not in terminals]}
typed(payload, manifest)
need(len(actual['files']) == 328 and len(actual['directories']) == 8, 'producer exact extent')
need(seal['future_or_runtime_prefix_exclusions'] == [], 'no future exclusions')
need(seal['root_terminal_exclusions_exact'] == ['OWNED_MANIFEST.json', 'FINAL_SEAL.json'], 'exact terminals')
for directory in actual['directories']:
    (D / 'custody/editorial' / directory).mkdir(parents=True, exist_ok=True)
for row in actual['files']:
    body = read(E / row['path'])
    need(pin(body) == {k: row[k] for k in ['bytes', 'SHA256']}, 'producer copy-time pin')
    write(Path('custody/editorial') / row['path'], body)
source = json.loads(read(E / 'SOURCE_INPUTS.json'))
initial = json.loads(read(D / 'ORIGINAL_SOURCE_SCIENCE_ROOT_CORE_CONTRACTS.json'))
typed(source['whole_original_SOURCE_READY'], initial['whole_original_SOURCE_READY'])
typed(source['whole_root_authority'], json.loads(read(D / 'authority/root-clearance-23331331-20261115.json')))
initial_namespaces = []
for ns in initial['namespaces']:
    expected = {'root': ns['root'], 'files': [{k: row[k] for k in ['path', 'bytes', 'SHA256']} for row in ns['files']], 'directories': ns['directories']}
    typed(scan(Path(ns['root'])), expected)
    initial_namespaces.append(expected)
typed(source['namespaces'], initial_namespaces)
originals = []
for ns in initial_namespaces:
    originals.extend({'path': str(Path(ns['root']) / r['path']), 'bytes': r['bytes'], 'SHA256': r['SHA256']} for r in ns['files'])
authority_path = P / 'verification/root-clearance-23331331-20261115.json'
originals.append({'path': str(authority_path), **pin(read(authority_path))})
originals.extend(x['original'] for x in initial['qualified_core']['files'])
originals.sort(key=lambda x: x['path'])
typed([{k: row[k] for k in ['path', 'bytes', 'SHA256']} for row in source['original_files']], originals)
for row in source['original_files']:
    original = read(Path(row['path']))
    need(pin(original) == {k: row[k] for k in ['bytes', 'SHA256']}, 'original whole pin')
    need(original == read(E / row['copy']), 'whole original private blob difference')
direct_names = sorted(q.name for q in (P / 'scripts').iterdir() if q.name.endswith('.py'))
core_qualification = json.loads(read(D / 'CORE_EXTENT_QUALIFICATION.json'))
need(direct_names == core_qualification['strict_original_core_contract']['direct_script_source_names'], 'direct17 script source names')
for n in [r['path'] for r in manifest['files'] if r['path'].startswith('candidate/')]:
    leaf = Path(n).name
    need(read(E / n) == read(E / 'optimized-candidate' / leaf), 'entire normal/optimized buffer difference')
main = read(E / 'PUBLIC_MAIN.html')
need(main == read(E / 'candidate/PUBLIC_MAIN.html'), 'complete MAIN difference')
page = read(E / 'candidate/index.html')
head = read(E / 'candidate/PUBLIC_HEAD.html')
need(page.count(main) == 1 and page.count(head) == 1, 'actual page component whole identity')
for asset in source['whole_original_SOURCE_READY']['all_native_assets_in_original_order']:
    need(read(E / 'candidate' / asset['original_api_file_object']['key']) == read(Path(asset['path'])), 'unaltered native asset')
write_json('EDITORIAL_CUSTODY_CONTRACT.json', {'schema': 'independent-postinitial-editorial-finite-custody-v1', 'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'producer_full_exact_namespace': actual, 'producer_whole_manifest': manifest, 'producer_whole_seal': seal, 'whole_SOURCE_INPUTS': source, 'code_personally_read_before_any_producer_execution': json.loads(read(E / 'CURRENT_CODE_MANIFEST.json')), 'independent_initial_sources_match_originals_and_producer_whole_objects': True, 'original_core17_plus_sole405b_and_direct17names_match': True, 'cache_diagnostics_not_crossproject_immutability_requirements': True, 'all8_whole_normal_optimized_buffers_equal': True, 'candidate_MAIN_whole_unchanged': True, 'complete_original_PDF_ZIP_unchanged': True, 'special_entries_or_subtree_exclusions': [], 'scientific_or_renderer_or_fault_execution': False, 'publication_authority': False})
write_json('EDITORIAL_CUSTODY_CAPTURE_RESULT.json', {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'PASS_OPAQUE_CUSTODY_ONLY_EDITORIAL_FACT_DISPOSITION_SEPARATE', 'checks': checks, 'producer_files': len(actual['files']), 'producer_directories': len(actual['directories']), 'original_files': len(originals), 'qualified_core_source_files': 18, 'entire_CODE_bytes': 32666, 'no_defect_repair': True, 'scientific_execution': False, 'publication_authority': False})
print(json.dumps({'status': 'PASS_OPAQUE_CUSTODY_ONLY', 'checks': checks, 'producer_files': 328, 'producer_directories': 8, 'original_files': len(originals), 'editorial_fact_NO_GO_separate': True}))
