#!/usr/bin/env python3
"""Standalone offline custody only. Default: verify finalized packet, read-only.

No project imports, network, subprocesses, writes or scientific calculations.
--preseal checks the already closed payload namespace before final seal binding;
it explicitly does not claim a finalized terminal seal. All failures are fatal.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import stat
import sys
import zipfile
import zlib

A = Path(__file__).resolve().parent
S = A.parents[1] / 'sources'
TERMINALS = ['CLOSURE.json', 'FINAL_MANIFEST.json', 'FINAL_SEAL.json']
CHECKS = 0


def need(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pairs(items):
    d = {}
    for k, v in items:
        if k in d:
            raise ValueError('duplicate original JSON key: ' + k)
        d[k] = v
    return d


def load(p):
    return json.loads(p.read_text(), object_pairs_hook=pairs)


def literal(x, y, label):
    need(type(x) is type(y), label + ': type')
    if type(x) is dict:
        need(list(x) == list(y), label + ': ordered keys/absence')
        for k in x:
            literal(x[k], y[k], label + '/' + k)
    elif type(x) is list:
        need(len(x) == len(y), label + ': array length')
        for i, (a, b) in enumerate(zip(x, y)):
            literal(a, b, label + '/' + str(i))
    else:
        need(x == y, label + ': scalar/null')


def namespace(root):
    need(stat.S_ISDIR(root.lstat().st_mode), str(root) + ': ordinary root')
    files, dirs = [], []
    for base, names, leaves in os.walk(root, followlinks=False):
        names.sort()
        leaves.sort()
        for n in names:
            p = Path(base) / n
            need(stat.S_ISDIR(p.lstat().st_mode), str(p) + ': no linked directory')
            dirs.append(p.relative_to(root).as_posix())
        for n in leaves:
            p = Path(base) / n
            need(stat.S_ISREG(p.lstat().st_mode), str(p) + ': ordinary file only')
            files.append(p.relative_to(root).as_posix())
    return sorted(files), sorted(dirs)


def pin(row, root=None):
    p = Path(row['path'])
    if not p.is_absolute():
        need(root is not None, 'relative binding needs exact root')
        q = PurePosixPath(row['path'])
        need(not q.is_absolute() and '..' not in q.parts, 'safe relative binding')
        p = root / p
    need(stat.S_ISREG(p.lstat().st_mode), str(p) + ': regular pin')
    b = p.read_bytes()
    need(len(b) == row['bytes'], str(p) + ': whole bytes')
    need(sha(b) == row['SHA256'], str(p) + ': whole SHA256')
    return p


def frozen(seal_name, expected):
    p = A / seal_name
    need(sha(p.read_bytes()) == expected, seal_name + ': immutable pin')
    obj = load(p)
    manifest = load(pin(obj['manifest']))
    for row in manifest['files']:
        pin(row)
    return obj


def main():
    need(sys.argv[1:] in ([], ['--preseal']), 'only default or --preseal')
    preseal = sys.argv[1:] == ['--preseal']
    files, dirs = namespace(A)
    for t in TERMINALS:
        need(t in files and '/' not in t, 'each exact root terminal already ordinary')
    manifest = load(A / 'FINAL_MANIFEST.json')
    literal(manifest['exact_root_terminals'], TERMINALS, 'terminal exclusions')
    expected = [r['path'] for r in manifest['files']]
    need(len(expected) == len(set(expected)), 'unique payload paths')
    need(sorted(expected) == sorted(set(files) - set(TERMINALS)), 'exact complete own files')
    literal(sorted(dirs), manifest['directories'], 'exact complete own directories')
    for row in manifest['files']:
        need(not Path(row['path']).is_absolute(), 'own manifest relative path')
        pin(row, A)
    frozen('INITIAL_SEAL.json', '34ee9916ed52e047272becb1f571883dc4efce486e30717bd57a383c0edc50e9')
    frozen('OWN_PROOF_CONTROL_SEAL.json', '87923ccd3c29a1efdd4616e1822632464d5011065fdd0929cfb4eed371b74135')
    source = load(A / 'SOURCE_INPUT_MANIFEST.json')
    sf, sd = namespace(S)
    expected_source = []
    for row in source['complete_source_files']:
        p = pin(row)
        expected_source.append(p.relative_to(S).as_posix())
    need(sf == sorted(expected_source) and len(sf) == 108, 'source complete108 files')
    literal(sd, source['exact_complete_source_directories'], 'source complete14 directories')
    need(len(sd) == 14, 'source directory count')
    ss = load(S / 'SOURCE_READY_SEAL.json')
    need(sha((S / 'SOURCE_READY_SEAL.json').read_bytes()) ==
         '24e7b08bda1c3561d9db2040745b2b1b8eb5b2e1f8c37be60426e831511cfb11', 'source seal pin')
    for name, key in [('SOURCE_READY.json', 'SOURCE_READY_SHA256'),
                      ('SOURCE_READY_MANIFEST.json', 'MANIFEST_SHA256'),
                      ('SOURCE_READY_CLOSURE.json', 'CLOSURE_SHA256')]:
        need(sha((S / name).read_bytes()) == ss[key], 'source terminal binding: ' + name)
    for row in load(S / 'SOURCE_READY_MANIFEST.json')['files']:
        pin(row, S)
    objects = load(A / 'LITERAL_SOURCE_OBJECTS.json')['objects']
    need(len(objects) == 50, 'all50 original JSON/native interfaces')
    for row in objects:
        literal(load(pin(row['binding'])), row['whole_original_object'], row['binding']['path'])
    core = load(A / 'CORE_BINDINGS.json')
    literal(load(pin(core['whole_root_contract_binding'])), core['whole_original_root_contract'], 'qualified core contract')
    need(len(core['actual_byreference_core_files']) == 18, '17 originals plus authorized helper')
    cp = []
    for row in core['actual_byreference_core_files']:
        p = pin(row)
        if p.name == 'checkpoint_subtree.py':
            cp.append(row)
    need(len(cp) == 1 and cp[0]['bytes'] == 6213 and cp[0]['SHA256'] ==
         '405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0', 'sole authorized405b qualification')
    handoff1 = load(A / 'RAW_PRIMARY_HANDOFF_01.json')
    literal(load(pin(handoff1['root_authority'])), handoff1['whole_root_authority'], 'whole acquisition authority')
    for r in handoff1['records']:
        pin(r['whole_original_raw_body'])
        literal(load(pin(r['legacy_metadata_container'])), r['whole_original_legacy_metadata_object'], 'whole legacy metadata')
    h2 = load(A / 'RAW_PRIMARY_HANDOFF_02.json')
    for row in h2['files']:
        pin(row)
    transports = [load(Path(r['path'])) for r in h2['files'] if r['path'].endswith('.transport.json')]
    literal(transports, h2['whole_transports'], 'whole ordered actual transport objects')
    for t in transports:
        pin({'path': str(A / t['body']), 'bytes': t['bytes'], 'SHA256': t['SHA256']})
        pin({'path': str(A / t['request']), 'bytes': t['request_bytes'], 'SHA256': t['request_SHA256']})
        need(t['body_complete'] is True and t['error'] is None, 'actual response body completeness')
    need([t['HTTP_status'] for t in transports] == [302, 403, 200, 200], 'literal actual status sequence in handoff order')
    chronological = load(A / 'ACTUAL_PRIMARY_REQUEST_SEQUENCE.json')['actual_sequence']
    for r in chronological:
        literal(load(pin(r['receipt'])), r['whole_transport'], 'chronological whole actual transport')
    literal([r['whole_transport'] for r in chronological],
            sorted(transports, key=lambda t: t['started_UTC']), 'actual chronological requests')
    custody = load(S / 'ARCHIVE_CUSTODY.json')
    need(len(custody['containers']) == 1, 'one original native ZIP container')
    occurrences = []
    for c in custody['containers']:
        pin({'path': c['input_path'], 'bytes': c['input_bytes'], 'SHA256': c['input_SHA256']})
        with zipfile.ZipFile(c['input_path']) as z:
            infos = z.infolist()
            need(len(infos) == len(c['members']) == 48, 'all48 native central-directory entries')
            seen = set()
            for ordinal, (zi, row) in enumerate(zip(infos, c['members'])):
                need(ordinal == row['ordinal_zero_based'] and zi.filename == row['original_member_name'], 'original ZIP order/name')
                q = PurePosixPath(zi.filename)
                need(not q.is_absolute() and '..' not in q.parts and '\\' not in zi.filename and not zi.is_dir(), 'safe finite regular ZIP name')
                need(zi.filename.casefold() not in seen, 'no case collision')
                seen.add(zi.filename.casefold())
                mode = zi.external_attr >> 16
                need(not stat.S_ISLNK(mode) and (stat.S_IFMT(mode) in (0, stat.S_IFREG)), 'no ZIP links/nonregulars')
                need(not (zi.flag_bits & 1), 'no encrypted payload')
                need(zi.flag_bits == row['native_flags'] and zi.external_attr == row['native_external_attr'] and
                     zi.create_system == row['native_create_system'] and list(zi.date_time) == row['native_date_time'] and
                     zi.compress_type == row['compression_method'] and zi.compress_size == row['compressed_bytes'], 'whole native ZIP metadata')
                b = z.read(zi)
                need(zi.file_size == row['bytes'] == len(b) and sha(b) == row['SHA256'], 'whole ZIP payload')
                need(format(zlib.crc32(b) & 0xffffffff, '08x') == row['CRC32'] == format(zi.CRC, '08x'), 'CRC32')
                extracted = pin({'path': row['extracted_path'], 'bytes': row['bytes'], 'SHA256': row['SHA256']})
                need(extracted.read_bytes() == b, 'whole extracted/native equality')
                occurrences.append(row)
    literal(occurrences, custody['regular_payload_occurrences'], 'whole archive occurrence list/order')
    need((S / 'assets/paper.pdf').read_bytes() ==
         (S / 'published-source/asset-001/output/pdf/paper.pdf').read_bytes(), 'archived/native PDF exact equality')
    verdict = load(A / 'VERDICT.json')
    need(verdict['publication_authority'] is False and verdict['AA'] is None and verdict['canonical_url'] is None and
         verdict['followup'] is None and verdict['root143_gate'] == 'CLOSED', 'literal private authority limits')
    if not preseal:
        seal = load(A / 'FINAL_SEAL.json')
        need(seal['status'] == 'INDEPENDENT_SCOPE_FINAL_SEALED', 'final status')
        pin(seal['manifest'])
        pin(seal['closure'])
        need(seal['payload_count'] == len(expected) and seal['actual_file_count'] == len(files) and
             seal['directory_count'] == len(dirs), 'final exact namespace counts')
        need(seal['immutable_after_seal'] is True, 'immutable final')
    print(json.dumps({'status': 'PASS', 'custody_predicates': CHECKS,
                      'phase': 'EXPLICIT_PRESEAL_NO_FINAL_SEAL_CLAIM' if preseal else 'FINAL_SEAL_BOUND',
                      'own_files': len(files), 'own_payloads': len(expected), 'own_directories': len(dirs),
                      'source_files': len(sf), 'source_directories': len(sd), 'ZIP_regular_occurrences': len(occurrences),
                      'whole_literal_source_objects': len(objects), 'qualified_core': '17 originals plus sole authorized405b',
                      'network_subprocess_writes_or_science': False, 'scientific_findings_printed': False}))


if __name__ == '__main__':
    main()
