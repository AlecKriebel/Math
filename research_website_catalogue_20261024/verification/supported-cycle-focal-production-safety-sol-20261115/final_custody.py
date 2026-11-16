#!/usr/bin/env python3
"""Offline read-only finite custody and independent native-byte comparison.

No project imports, network, subprocesses, live website/Git/runtime access, or
writes. All dereferenced files must be ordinary files below the fixed programme
root. Embedded historical W paths are data and are never dereferenced.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import struct
import sys

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
R = P / 'verification/supported-cycle-focal-production-safety-sol-20261115'
N = P / 'verification/supported-cycle-focal-production-preparation-sol-20261115'
TERMINALS = {'FINAL_MANIFEST.json', 'FINAL_CLOSURE.json', 'FINAL_SEAL.json'}
CHECKS = 0


def need(ok, why):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(why)


def ordinary(path):
    path = Path(path)
    need(path.is_absolute() and '..' not in path.parts, 'absolute safe path')
    need(path.is_relative_to(P), 'programme-only read boundary')
    q = P
    need(stat.S_ISDIR(q.lstat().st_mode), 'ordinary programme root')
    for part in path.relative_to(P).parts[:-1]:
        q = q / part
        need(stat.S_ISDIR(q.lstat().st_mode), 'ordinary ancestor ' + str(q))
    st = path.lstat()
    need(stat.S_ISREG(st.st_mode) and st.st_nlink == 1, 'ordinary single-link file ' + str(path))
    return path.read_bytes()


def sha(body):
    return hashlib.sha256(body).hexdigest()


def pin(spec, root=None):
    path = Path(spec['path'])
    if root is not None:
        need(not path.is_absolute() and '..' not in path.parts, 'relative pin')
        path = root / path
    body = ordinary(path)
    need(len(body) == spec['bytes'] and sha(body) == spec['SHA256'], 'pin ' + str(path))
    return body


def read(name, root=R):
    return json.loads(ordinary(root / name))


def extent(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'ordinary root')
    files, dirs = set(), set()
    for here, names, leaves in os.walk(root, followlinks=False):
        for name in names:
            q = Path(here) / name
            need(stat.S_ISDIR(q.lstat().st_mode), 'ordinary exact directory')
            dirs.add(q.relative_to(root).as_posix())
        for name in leaves:
            q = Path(here) / name
            need(stat.S_ISREG(q.lstat().st_mode) and q.lstat().st_nlink == 1, 'ordinary exact file')
            files.add(q.relative_to(root).as_posix())
    return files, dirs


def exact_manifest(root, manifest, terminals):
    entries = manifest['files']
    if isinstance(entries, dict):
        entries = [dict(v, path=k) for k, v in entries.items()]
    expected = {v['path'] for v in entries}
    need(len(expected) == len(entries), 'unique manifest files')
    files, dirs = extent(root)
    need(files == expected | terminals, 'closed files ' + str(root))
    need(dirs == set(manifest['directories']), 'closed directories ' + str(root))
    need(not expected & terminals, 'only exact root terminals excluded')
    for v in entries:
        pin(v, root)
    for name in terminals:
        need(isinstance(read(name, root), dict), 'existing JSON terminal')
    return len(files), len(dirs)


def source_pins(value):
    if isinstance(value, dict):
        if {'path', 'bytes', 'SHA256'} <= value.keys():
            pin(value)
        else:
            for v in value.values():
                source_pins(v)
    elif isinstance(value, list):
        for v in value:
            source_pins(v)


def main():
    need(len(sys.argv) == 1, 'default-only interface')
    manifest = read('FINAL_MANIFEST.json')
    need(manifest['exact_root_terminal_exclusions'] == sorted(TERMINALS), 'exact terminal names')
    need(manifest['future_subtree_or_basename_exclusions'] == [], 'no future exclusions')
    own_files, own_dirs = exact_manifest(R, manifest, TERMINALS)
    fixed = {
        'INITIAL_SEAL.json': '3b3c146a18031cd6261cb04fc8f7dc9ee47b97bc993eba34a6bcb6adf240fe88',
        'BASELINE_SEAL.json': 'af269d4782819a6be4ae9b1c41f84943b898dd3718bfb62b103d3e644eac09c4',
        'BASELINE_MANIFEST.json': '6a62db77a89f21d7db1790c71f1ffecbbf3844d7218746d599b92ee441c1b856',
        'BASELINE_CLOSURE.json': '051f0a2aba36293491ba56b04b5b886fabedc6dfbaacb35942ba43e1aa1c5ca8',
    }
    for name, digest in fixed.items():
        need(sha(ordinary(R / name)) == digest, 'immutable pre-exposure seal ' + name)
    for spec in read('INITIAL_SEAL.json')['files']:
        pin(spec)
    source_pins(read('INITIAL_INPUTS.json'))
    exact_manifest(R / 'fresh-readonly', read('BASELINE_MANIFEST.json'), set())
    need(ordinary(R / '.gitignore') == b'/fresh-readonly/\n', 'private capture ignore retained')
    bindings = read('REVIEWED_WRITER_BINDINGS.json')
    need(bindings['forwarded_FINAL_SHA256'] == '5cecd12ca60548031cd4d1cdc8426a447f3cb7c59f13368a7a95091c6a05197b', 'forwarded writer')
    need(sha(ordinary(N / 'FINAL_SEAL.json')) == bindings['forwarded_FINAL_SHA256'], 'immutable writer FINAL')
    need(sha(ordinary(N / 'OWNED_MANIFEST.json')) == '3d1bc14ffdab6f667cead4b0e04273a68480fc670ca16be7310c306099ee4e12', 'immutable writer manifest')
    files, dirs = extent(N)
    need(files == {str(Path(v['path']).relative_to(N)) for v in bindings['whole_current_writer_files']}, 'whole writer files')
    need(dirs == set(bindings['exact_writer_directories']), 'whole writer directories')
    for spec in bindings['whole_current_writer_files']:
        pin(spec)
    exact_manifest(N, read('OWNED_MANIFEST.json', N), {'FINAL_SEAL.json', 'OWNED_MANIFEST.json'})
    code = read('CURRENT_CODE_PINS.json', N)
    need(len(code) == 6 and sum(v['bytes'] for v in code.values()) == 59966, 'six full bodies')
    for name, spec in code.items():
        pin(dict(spec, path=str(N / name)))
    need(len(ordinary(N / 'NEW_CODE.diff')) == 61062 and sha(ordinary(N / 'NEW_CODE.diff')) == '86aa0404ed151797ef3a29e6b36e2eafac89944282d84df139d52da66bc3a410', 'complete current diff')
    receipt = read('MECHANISM_PURE_EXECUTION.json')
    stdout = pin(receipt['whole_stdout'])
    stderr = pin(receipt['whole_stderr'])
    need(receipt['actual_exit_code'] == 0 and not stderr, 'actual designated pure exit')
    need(stdout.decode() == receipt['literal_whole_stdout'] and stderr.decode() == receipt['literal_whole_stderr'], 'literal whole streams')
    result = json.loads(stdout)
    need(result['checks'] == 718136 and result['sealed'] is True and result['runtime_read'] is False and result['production_executed'] is False, 'bounded actual default result')
    oracle = read('SOURCE_ONLY_PRODUCTION_ORACLE.json')
    outputs = oracle['adopted_exact_ten_outputs_in_original_manifest_order']
    need(len(outputs) == 10 and sum(v['role'] == 'exclusive_new_leaf' for v in outputs) == 8, 'exact ten/eight')
    new = {}
    for spec in outputs:
        body = pin(spec['adopted_source'])
        need(body == pin(spec['paired_source']), 'paired adopted whole buffer')
        need(len(body) == spec['required_bytes'] and sha(body) == spec['required_SHA256'], 'initial authoritative buffer')
        path = spec['output_relative_to_W'].encode()
        oid = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).digest()
        new[path] = oid
    commit_oracle = read('EXACT10_COMMIT_ORACLE.json', N)
    need({v['gitpath'].encode(): bytes.fromhex(v['Git_blob_OID']) for v in commit_oracle['outputs']} == new, 'independent exact ten Git blobs')
    need(all(v['mode'] == '100644' for v in commit_oracle['outputs']), 'exact ten modes')
    raw = ordinary(R / 'fresh-readonly/native-index.before')
    need(sha(raw) == '35181f4046df6e197ba5c5c6e34c348b2b46783c0cc073a5b7f066692ba332b6', 'pre-exposure actual raw index')
    need(raw[:12] == b'DIRC' + struct.pack('>II', 2, 58563), 'native v2/count')
    need(hashlib.sha1(raw[:-20]).digest() == raw[-20:], 'whole native SHA1')
    model = read('fresh-readonly/NATIVE_INDEX_FULL_RECORDS.json')
    need(model['version'] == 2 and model['count'] == 58563 and len(model['records']) == 58563, 'full decoded model')
    offset, old = 12, {}
    for ordinal, rec in enumerate(model['records']):
        start = offset
        endname = raw.index(b'\0', start + 62)
        offset = start + ((endname + 1 - start + 7) // 8) * 8
        body = raw[start:offset]
        path = raw[start + 62:endname]
        fields = struct.unpack('>10I', body[:40])
        flags = struct.unpack('>H', body[60:62])[0]
        need(path not in old and (not old or path > next(reversed(old))), 'native unique byte order')
        need(flags & 0xf000 == 0 and flags == min(len(path), 4095), 'native ordinary stage0 flags')
        need(rec['ordinal'] == ordinal and rec['path_bytes_hex'] == path.hex() and rec['stat_fields'] == list(fields), 'native full path/stat')
        need(rec['OID_hex'] == body[40:60].hex() and rec['flags'] == flags and rec['extended_flags'] is None, 'native OID/flags')
        need(rec['padding_hex'] == raw[endname:offset].hex() and not any(raw[endname:offset]) and rec['raw_record_SHA256'] == sha(body), 'native padding/full body')
        old[path] = body
    extensions = []
    while offset < len(raw) - 20:
        sig, size = raw[offset:offset + 4], struct.unpack('>I', raw[offset + 4:offset + 8])[0]
        body = raw[offset + 8:offset + 8 + size]
        need(len(body) == size and sig == b'TREE', 'only obsolete TREE cache')
        extensions.append({'signature_hex': sig.hex(), 'bytes': size, 'SHA256': sha(body), 'whole_body_hex': body.hex()})
        offset += 8 + size
    need(offset == len(raw) - 20 and extensions == model['extensions'] and len(extensions) == 1, 'full extensions/trailer boundary')
    protected = {p: b for p, b in old.items() if p not in new}
    need(len(protected) == 58561 and len(set(old) & set(new)) == 2, 'protected58561/two replaced')
    framed = ordinary(R / 'fresh-readonly/protected-native-records.bin')
    cursor, frames = 0, []
    while cursor < len(framed):
        size = struct.unpack('>I', framed[cursor:cursor + 4])[0]
        body = framed[cursor + 4:cursor + 4 + size]
        need(size == len(body) and size >= 64, 'whole independent framed raw record')
        frames.append(body)
        cursor += 4 + size
    need(cursor == len(framed) and frames == list(protected.values()), 'pre-exposure protected full raw stream equality')
    fingerprint = sha(b'\0'.join(p + b'\t' + b.hex().encode() for p, b in protected.items()) + b'\0')
    need(fingerprint == '2a39a160e0c4a832d0afaa4159ef023f28b0ae0be03ee839d9926c370789b46c', 'exact protected fingerprint')
    planned = dict(protected)
    for path, oid in new.items():
        body = struct.pack('>10I', 0, 0, 0, 0, 0, 0, 0o100644, 0, 0, 0) + oid + struct.pack('>H', len(path)) + path + b'\0'
        body += b'\0' * (-len(body) % 8)
        planned[path] = body
    need(len(planned) == 58571, 'planned exact native count')
    planned_body = b'DIRC' + struct.pack('>II', 2, len(planned)) + b''.join(planned[p] for p in sorted(planned))
    planned_whole = planned_body + hashlib.sha1(planned_body).digest()
    proposed = sha(planned_whole)
    need(proposed == result['approved_raw_index_SHA256'] == '5f9c24f576cca18c466163a9572120f118698ead90eca728199030ba346e8244', 'independent whole proposed index')
    captured = read('fresh-readonly/FRESH_CAPTURE.json')
    aggregates = {'research/index.html', 'research/sitemap.xml'}
    need({v['public_relative_path'] for v in captured['full_public_files'] if v['public_relative_path'] in aggregates and stat.S_IMODE(v['stat']['mode']) == 0o644} == aggregates, 'actual aggregate modes0644')
    verdict = read('VERDICT.json')
    need(verdict['actual_blocking_findings'] == [] and verdict['production_execution_percent'] == 0 and verdict['AA'] is None and verdict['follow_up'] is None, 'bounded literal verdict')
    seal = read('FINAL_SEAL.json')
    sealed = seal.get('status') == 'IMMUTABLE_BOUNDED_INFORMED_PRODUCTION_SAFETY_AUDIT'
    if sealed:
        for name in ['MANIFEST', 'CLOSURE', 'REPORT', 'VERDICT', 'helper', 'helper_full_read']:
            pin(seal[name])
        need(seal['ordinary_files'] == own_files and seal['ordinary_directories'] == own_dirs, 'sealed finite extent')
    print(json.dumps({'status': 'PASS_OFFLINE_STRICT_CUSTODY_AND_INDEPENDENT_NATIVE_BYTES', 'checks': CHECKS, 'own_files': own_files, 'own_directories': own_dirs, 'writer_files': len(files), 'writer_directories': len(dirs), 'protected_raw_records': len(protected), 'planned_native_records': len(planned), 'independent_planned_index_SHA256': proposed, 'protected_fingerprint_SHA256': fingerprint, 'new_fault_campaigns': 0, 'live_W_Git_network_runtime_access': False, 'writes': False, 'production_executed': False, 'sealed': sealed}, sort_keys=True))


if __name__ == '__main__':
    main()
