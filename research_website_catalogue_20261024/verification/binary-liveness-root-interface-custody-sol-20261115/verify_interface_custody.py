#!/usr/bin/env python3
"""Offline read-only custody/interface checks, not mathematical verification.

Reads this packet and explicitly pinned original source/peer/core/two root files.
It is NOT owned-only. No project imports, execution, extraction, subprocess,
network, package installation, cache/Git/Sheet/site access or file writes.
"""
import argparse
import binascii
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import zipfile

D = Path(__file__).absolute().parent
CONTRACT_SHA256 = '4eb68ad6c374865a5fe22a87413a89e8377806f904ccf2475c34e180b48cc38e'
checks = 0
typed_nodes = 0
allowed = {}

def need(ok, why):
    global checks
    checks += 1
    if not ok:
        raise ValueError(why)

def pin(body):
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest()}

def read(path):
    path = Path(path)
    need(path.is_absolute() and '..' not in path.parts, 'noncanonical input path')
    need(path.is_relative_to(D) or str(path) in allowed, 'unpinned foreign input')
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode), 'not ordinary file ' + str(path))
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        held = os.fstat(fd)
        need((held.st_dev, held.st_ino) == (before.st_dev, before.st_ino), 'open identity')
        pieces = []
        while True:
            piece = os.read(fd, 1048576)
            if not piece:
                break
            pieces.append(piece)
        after = os.fstat(fd)
        need((held.st_size, held.st_mtime_ns, held.st_ctime_ns) == (after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'held file changed')
        final = path.lstat()
        need((final.st_dev, final.st_ino) == (held.st_dev, held.st_ino), 'final pathname identity')
        body = b''.join(pieces)
        need(len(body) == held.st_size, 'short read')
        if str(path) in allowed:
            need(pin(body) == allowed[str(path)], 'whole pinned input changed ' + str(path))
        return body
    finally:
        os.close(fd)

def obj(path):
    # Authenticate and parse exactly this same held-file buffer.
    return json.loads(read(path))

def typed(a, b, pointer='$'):
    global typed_nodes
    typed_nodes += 1
    need(type(a) is type(b), 'type ' + pointer)
    if type(a) is dict:
        need(list(a) == list(b), 'keys/order ' + pointer)
        for key in a:
            typed(a[key], b[key], pointer + '/' + key)
    elif type(a) is list:
        need(len(a) == len(b), 'length ' + pointer)
        for i, (x, y) in enumerate(zip(a, b)):
            typed(x, y, pointer + '/' + str(i))
    else:
        need(a == b, 'literal ' + pointer)

def scan(root, expected=None):
    need(stat.S_ISDIR(root.lstat().st_mode), 'not ordinary directory root')
    file_names = None if expected is None else {x['path'] for x in expected['files']}
    dir_names = None if expected is None else set(expected['directories'])
    files, directories = [], []
    def visit(path):
        before = path.lstat()
        with os.scandir(path) as iterator:
            entries = sorted(iterator, key=lambda x: x.name)
        for entry in entries:
            q = path / entry.name
            rel = q.relative_to(root).as_posix()
            mode = q.lstat().st_mode
            if stat.S_ISDIR(mode):
                need(dir_names is None or rel in dir_names, 'unlisted directory ' + rel)
                directories.append(rel)
                visit(q)
            elif stat.S_ISREG(mode):
                need(file_names is None or rel in file_names, 'unlisted file ' + rel)
                files.append({'path': rel, **pin(read(q))})
            else:
                raise ValueError('symlink/FIFO/special entry ' + rel)
        after = path.lstat()
        need((before.st_dev, before.st_ino, before.st_mtime_ns, before.st_ctime_ns) == (after.st_dev, after.st_ino, after.st_mtime_ns, after.st_ctime_ns), 'directory changed')
    visit(root)
    result = {'root': str(root), 'files': sorted(files, key=lambda x: x['path']), 'directories': sorted(directories)}
    if expected is not None:
        typed(result, expected)
    return result

def ready_embeddings(value, ready):
    found = 0
    if type(value) is dict:
        if {'selected_actual_PDF', 'all_native_assets_in_original_order', 'whole_native_API_objects'} <= set(value):
            typed(value, ready)
            return 1
        for child in value.values():
            found += ready_embeddings(child, ready)
    elif type(value) is list:
        for child in value:
            found += ready_embeddings(child, ready)
    return found

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preseal', action='store_true', help='original-input closure only; no final owned-namespace assertion')
    args = parser.parse_args()
    cb = read(D / 'INPUT_CONTRACT.json')
    need(hashlib.sha256(cb).hexdigest() == CONTRACT_SHA256, 'fixed contract pin')
    contract = json.loads(cb)
    for ns in contract['complete_immutable_namespaces']:
        for row in ns['files']:
            allowed[str(Path(ns['root']) / row['path'])] = {k: row[k] for k in ['bytes', 'SHA256']}
    for row in contract['immutable_root_files_only'] + contract['qualified_core_sources'] + [contract['qualified_core_reference']]:
        allowed[row['path']] = {k: row[k] for k in ['bytes', 'SHA256']}
    for ns in contract['complete_immutable_namespaces']:
        scan(Path(ns['root']), ns)
    for path in allowed:
        read(Path(path))
    source, scope, adv = [Path(ns['root']) for ns in contract['complete_immutable_namespaces']]
    need([(len(ns['files']), len(ns['directories'])) for ns in contract['complete_immutable_namespaces']] == [(82, 9), (272, 45), (133, 21)], 'exact original extents')
    schemas = contract['original_terminal_schemas']
    for root, mf, key, terms in [(source, 'SOURCE_READY_MANIFEST.json', 'path', schemas['source']), (scope, 'MANIFEST.json', 'relative_path', schemas['scope']), (adv, 'FINAL_MANIFEST.json', 'path', schemas['adversarial'])]:
        manifest = obj(root / mf)
        actual = next(ns for ns in contract['complete_immutable_namespaces'] if ns['root'] == str(root))
        listed = sorted([{'path': r[key], 'bytes': r['bytes'], 'SHA256': r['SHA256']} for r in manifest['files']], key=lambda r: r['path'])
        typed(listed, [r for r in actual['files'] if r['path'] not in set(terms)])
        need(set(terms) <= {r['path'] for r in actual['files']}, 'upstream exact terminals')
        terminal_key = 'excluded_terminal_files' if root == source else ('exact_root_terminal_controls' if root == scope else 'exact_root_terminal_exclusions')
        typed(manifest[terminal_key], terms)
        if root != source:
            typed(sorted(manifest['directories']), actual['directories'])
    need(pin(read(source / 'SOURCE_READY_MANIFEST.json'))['SHA256'] == obj(source / 'SOURCE_READY_SEAL.json')['MANIFEST_SHA256'], 'original source manifest/seal')
    need(pin(read(scope / 'MANIFEST.json')) == {k: obj(scope / 'FINAL_SEAL.json')['manifest'][k] for k in ['bytes', 'SHA256']}, 'original scope manifest/seal')
    need(pin(read(adv / 'FINAL_MANIFEST.json'))['SHA256'] == obj(adv / 'FINAL_SEAL.json')['FINAL_MANIFEST_SHA256'], 'original adversarial manifest/seal')
    ready = obj(source / 'SOURCE_READY.json')
    need(pin(read(source / 'SOURCE_READY.json'))['SHA256'] == obj(source / 'SOURCE_READY_SEAL.json')['SOURCE_READY_SHA256'], 'READY seal')
    source_jsons, all_jsons = 0, 0
    for ns in contract['complete_immutable_namespaces']:
        for row in ns['files']:
            if row['path'].endswith('.json'):
                obj(Path(ns['root']) / row['path'])
                all_jsons += 1
                source_jsons += ns['root'] == str(source)
    binding = obj(scope / 'ORIGINAL_SOURCE_BINDING.json')
    need(len(binding['files']) == 82, 'whole scope source-copy count')
    for row in binding['files']:
        need(read(Path(row['original']['path'])) == read(Path(row['exact_private_copy']['path'])), 'scope whole original source copy')
    typed(sorted(binding['original_directories']), contract['complete_immutable_namespaces'][0]['directories'])
    iface = obj(scope / 'SOURCE_INTERFACE.json')
    interface_rows = iface['all_original_JSON_objects_and_native_API_objects_in_input_order']
    for row in interface_rows:
        original = obj(Path(row['original']['path']))
        typed(original, row['whole_original_object'])
        typed(original, obj(Path(row['exact_private_copy']['path'])))
    for row in contract['complete_immutable_namespaces'][2]['files']:
        p = Path(row['path'])
        if len(p.parts) == 2 and p.parts[0] == 'inputs' and str(source / p.name) in allowed:
            need(read(source / p.name) == read(adv / p), 'adversarial whole original input copy')
    verdict_embeddings = []
    for row in contract['whole_original_verdicts']:
        value = obj(Path(row['binding']['path']))
        typed(value, row['whole_literal_object'])
        verdict_embeddings.append(ready_embeddings(value, ready))
    # No embedding is invented if either heterogeneous peer verdict omits READY.
    for api in ready['whole_native_API_objects']:
        obj(Path(api['path']))
    for ordinal, asset in enumerate(ready['all_native_assets_in_original_order']):
        body = read(Path(asset['path']))
        need(asset['ordinal_zero_based'] == ordinal, 'native asset order')
        need(pin(body) == {k: asset[k] for k in ['bytes', 'SHA256']}, 'complete native asset')
        need(body == read(Path(asset['transport_body_path'])), 'native transport/asset complete bytes')
        need('md5:' + hashlib.md5(body).hexdigest() == asset['original_api_file_object']['checksum'], 'original native checksum')
    archive_custody = obj(source / 'ARCHIVE_CUSTODY.json')
    zip_asset = next(a for a in ready['all_native_assets_in_original_order'] if a['original_api_file_object']['key'] == 'verification.zip')
    occurrences = archive_custody['regular_payload_occurrences']
    with zipfile.ZipFile(io.BytesIO(read(Path(zip_asset['path'])))) as archive:
        infos = archive.infolist()
        need(len(infos) == len(occurrences) == 28, '28 exact ZIP central-directory occurrences')
        seen = set()
        for ordinal, (info, occurrence) in enumerate(zip(infos, occurrences)):
            name = Path(info.filename)
            need(not name.is_absolute() and '..' not in name.parts and '\\' not in info.filename, 'safe ZIP name')
            need(info.filename.casefold() not in seen, 'duplicate/case-colliding ZIP name')
            seen.add(info.filename.casefold())
            need(not info.is_dir() and stat.S_ISREG(info.external_attr >> 16), 'ordinary ZIP member')
            body = archive.read(info)  # Full member read verifies the ZIP CRC; no extraction.
            need(len(body) == info.file_size and (binascii.crc32(body) & 0xffffffff) == info.CRC, 'ZIP complete size/CRC')
            need(info.filename == occurrence['original_member_name'] and ordinal == occurrence['ordinal_zero_based'], 'ZIP original order/name')
            need(pin(body) == {k: occurrence[k] for k in ['bytes', 'SHA256']}, 'ZIP member whole hash')
            need(format(info.CRC, '08x') == occurrence['CRC32'], 'original ZIP CRC field')
            need(info.compress_size == occurrence['compressed_bytes'] and info.compress_type == occurrence['compression_method'], 'ZIP compression metadata')
            need(info.external_attr == occurrence['native_external_attr'] and info.create_system == occurrence['native_create_system'] and info.flag_bits == occurrence['native_flags'] and list(info.date_time) == occurrence['native_date_time'], 'whole ZIP native member metadata')
            need(body == read(Path(occurrence['extracted_path'])), 'existing extracted member whole identity')
    buffers = contract['full_original_expected_and_actual_buffers']
    expected = buffers[0]['whole_literal_object']
    for row in buffers:
        body = read(Path(row['binding']['path']))
        need(body == row['whole_buffer_UTF8'].encode('utf-8') and len(body) == 398, 'entire original 398B buffer')
        typed(json.loads(body), row['whole_literal_object'])
        typed(json.loads(body), expected)
    replay = obj(adv / 'NATIVE_REPLAY_RECEIPT.json')
    typed(replay['whole_expected_original'], expected)
    for run in replay['runs']:
        typed(run['whole_typed_actual_result'], expected)
        need(run['whole_typed_expected_difference'] == [] and run['exit_code'] == 0 and run['stdout_bytes'] == 398 and run['stderr_bytes'] == 0, 'original saved replay declaration')
        need(run['stdout_SHA256'] == pin(read(adv / 'native-normal.stdout'))['SHA256'] and run['stderr_SHA256'] == pin(b'')['SHA256'], 'saved replay whole stream pins')
    need(read(adv / 'native-normal.stdout') == read(adv / 'native-optimized.stdout'), 'whole saved normal/O output agreement')
    need(read(adv / 'native-normal.stderr') == read(adv / 'native-optimized.stderr') == b'', 'whole saved empty stderr')
    selected = contract['selected_native_code']
    need(read(Path(selected[0]['path'])) == read(Path(selected[1]['path'])), 'native selected checker full source/copy')
    need(selected[0]['SHA256'] == selected[1]['SHA256'] == '013a096ca48a8a8123d6f28adf32b6e6d517ef7bd9d125450e6950ee772b49d0', 'selected checker pin')
    need(replay['source_SHA256'] == replay['copy_SHA256'] == selected[0]['SHA256'], 'saved selected-source declaration')
    clean = obj(source / 'published-source/asset-004/receipts/clean_reproduction.json')
    typed(clean['runs'][0]['result'], expected)
    need(clean['runs'][0]['sha256'] == selected[0]['SHA256'], 'historical selected-checker declaration')
    authority = obj(Path(contract['immutable_root_files_only'][1]['path']))
    typed(authority['reconstruction'], contract['immutable_root_files_only'][0])
    # References to moving root rasters/primary files are data only; never follow.
    if not args.preseal:
        seal = obj(D / 'FINAL_SEAL.json')
        mb = read(D / 'FINAL_MANIFEST.json')
        need(pin(mb) == seal['manifest'], 'same-buffer owned manifest')
        manifest = json.loads(mb)
        current = scan(D)
        terms = {'FINAL_MANIFEST.json', 'FINAL_SEAL.json'}
        need(terms <= {r['path'] for r in current['files']}, 'exact own root terminals')
        current['files'] = [r for r in current['files'] if r['path'] not in terms]
        typed(current['files'], manifest['files'])
        typed(current['directories'], manifest['directories'])
        need(manifest['exact_root_terminal_exclusions'] == sorted(terms) and manifest['subtree_or_future_exclusions'] == [], 'no future carveouts')
        need(seal['scientific_disposition'] is None and seal['root_adoption'] is False and seal['publication_authority'] is False and seal['AA'] is None, 'no delegated authority')
    print(json.dumps({'status': 'CUSTODY_AND_SAVED_INTERFACE_MATCH_ONLY', 'strict_final_owned_namespace': not args.preseal, 'checks': checks, 'typed_nodes': typed_nodes, 'original_namespaces': [[82, 9], [272, 45], [133, 21]], 'original_JSON_bodies_parsed': all_jsons, 'source_JSON_bodies': source_jsons, 'whole_scope_interface_rows': len(interface_rows), 'READY_embeddings_in_source_scope_adversarial_verdicts': verdict_embeddings, 'native_assets': 4, 'ZIP_regular_occurrences_fullbyte_CRC_checked_without_extraction': 28, 'saved_398B_buffers': len(buffers), 'root_files_only': 2, 'qualified_core_sources': 18, 'reads_pinned_original_inputs': True, 'owned_only_claim': False, 'scientific_or_native_program_execution': False, 'scientific_disposition': None, 'root_adoption': False, 'publication_authority': False, 'AA': None}, sort_keys=True))

if __name__ == '__main__':
    main()
