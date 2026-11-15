#!/usr/bin/env python3
"""Offline custody-only closure. Never imports or replays scientific programs.

No network, subprocess, writes or project imports. An existing final manifest
closes all ordinary files/directories except two exact root terminal files.
"""
from pathlib import Path
import base64
import hashlib
import json
import stat
import zipfile

OWN = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23203732/reviews/adversarial')
SOURCE = OWN.parent.parent / 'sources'
TERMINALS = ['MANIFEST.json', 'FINAL_SEAL.json']
checks = 0
typed_nodes = 0

def require(ok, label):
    global checks
    checks += 1
    if not ok:
        raise ValueError(label)

def body(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'ordinary input file')
    return path.read_bytes()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def load(path):
    return json.loads(body(path))

def pin(row):
    path = Path(row['path'])
    if not path.is_absolute():
        require('..' not in path.parts, 'safe owned pin')
        path = OWN / path
    raw = body(path)
    require(len(raw) == row['bytes'] and sha(raw) == row['SHA256'], 'whole pinned bytes')
    return raw

def typed(a, b):
    global typed_nodes
    typed_nodes += 1
    require(type(a) is type(b), 'literal JSON type')
    if isinstance(a, dict):
        require(list(a) == list(b), 'whole ordered keys')
        for key in a:
            typed(a[key], b[key])
    elif isinstance(a, list):
        require(len(a) == len(b), 'whole ordered array')
        for x, y in zip(a, b):
            typed(x, y)
    else:
        require(a == b, 'literal scalar/null/history')

def extent(root):
    require(stat.S_ISDIR(root.lstat().st_mode), 'ordinary directory root')
    files, directories = [], []
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            directories.append(relative)
        else:
            require(stat.S_ISREG(mode), 'no symlink or nonregular namespace member')
            raw = body(path)
            files.append({'path': relative, 'bytes': len(raw), 'SHA256': sha(raw)})
    return files, directories

def main():
    require(sha(body(SOURCE / 'SOURCE_READY.json')) == 'bd5708d6fa77da017786d34952a3d689b5b5fb2703086bc4d33a1093430ed4cb', 'root supplied READY')
    require(sha(body(SOURCE / 'SOURCE_READY_SEAL.json')) == 'cf9ffb0b5f509af974aa3e7a368c2672e000f2665aecf772a0df57f658145287', 'root supplied source seal')
    for name in ['INITIAL_SEAL.json', 'RESULTS_SEAL.json']:
        sealed = load(OWN / name)
        for row in sealed['payloads']:
            pin(row)
    require(sha(body(OWN / 'INITIAL_SEAL.json')) == '15951e6b01697725a568968507930aa574056e993139df27e344122cdee657ec', 'immutable independent initial')
    require(sha(body(OWN / 'RESULTS_SEAL.json')) == 'ca982ba0b8477aa46498a4572ffb51adc1c431034eb1eb82312561c2746d2f86', 'immutable pre-exposure proof/control results')
    original = load(OWN / 'SOURCE_OPAQUE_BINDINGS.json')
    source_files, source_dirs = extent(SOURCE)
    expected = [{'path': r['relative_path'], 'bytes': r['bytes'], 'SHA256': r['SHA256']} for r in original['files']]
    typed(source_files, expected)
    typed(source_dirs, original['directories'])
    require(len(source_files) == 101 and len(source_dirs) == 18, 'complete original source namespace')
    for row in original['files']:
        pin(row)
    whole = load(OWN / 'WHOLE_ORIGINAL_JSON.json')['whole_original_parseable_JSON_objects']
    for relative, value in whole.items():
        typed(load(SOURCE / relative), value)
    require(len(whole) == 55, 'all original parseable JSON interfaces')
    ready = load(SOURCE / 'SOURCE_READY.json')
    verdict = load(OWN / 'VERDICT.json')
    typed(verdict['whole_original_SOURCE_READY'], ready)
    require(ready['version_field_present'] is False and ready['version'] is None, 'literal absent native version')
    require(ready['printed_title_date_version_inspected'] is False and ready['printed_date'] is None and ready['printed_version'] is None, 'historical intake unread flags retained')
    record = load(SOURCE / 'record.response.body')
    require('version' not in record['metadata'] and record['metadata']['publication_date'] == '2026-10-06', 'actual native edition')
    require([a['key'] for a in record['files']] == ['paper.pdf', 'cost-betti-source-and-verification.zip'], 'whole native asset order')
    for asset in ready['all_native_assets_in_original_order']:
        raw = pin(asset)
        require(hashlib.md5(raw).hexdigest() == asset['original_api_file_object']['checksum'].removeprefix('md5:'), 'native checksum')
    require(body(SOURCE / 'assets/paper.pdf') == body(SOURCE / 'published-source/asset-002/paper.pdf'), 'complete embedded/standalone original PDF equality')
    require(len(body(SOURCE / 'published-source/asset-002/main.tex').splitlines()) == 198 and ready['selected_actual_PDF']['pages'] == 6, 'complete original manuscript extent')

    custody = load(SOURCE / 'ARCHIVE_CUSTODY.json')
    flattened = []
    for container in custody['containers']:
        raw = body(Path(container['input_path']))
        require(len(raw) == container['input_bytes'] and sha(raw) == container['input_SHA256'], 'whole original archive')
        with zipfile.ZipFile(Path(container['input_path'])) as archive:
            infos = archive.infolist()
            central = []
            for i, info in enumerate(infos):
                central.append({'ordinal_zero_based': i, 'filename': info.filename, 'original_filename': info.orig_filename, 'is_directory': info.is_dir(), 'bytes': info.file_size, 'compressed_bytes': info.compress_size, 'CRC32': f'{info.CRC:08x}', 'flags': info.flag_bits, 'compression': info.compress_type, 'native_date_time': list(info.date_time), 'external_attr': info.external_attr, 'internal_attr': info.internal_attr, 'create_system': info.create_system, 'create_version': info.create_version, 'extract_version': info.extract_version, 'header_offset': info.header_offset, 'extra_hex': info.extra.hex(), 'comment_hex': info.comment.hex()})
            typed(central, container['whole_original_central_directory'])
            require(archive.comment.hex() == container['original_archive_comment_hex'], 'native archive comment')
            for row in container['members']:
                info = infos[row['ordinal_zero_based']]
                raw = archive.read(info)
                require(not info.is_dir() and info.filename == row['original_member_name'], 'regular archive occurrence')
                require(len(raw) == row['bytes'] and sha(raw) == row['SHA256'], 'whole archive occurrence bytes')
                require(raw == body(Path(row['extracted_path'])), 'entire extracted original body')
                flattened.append(row)
    typed(flattened, custody['regular_payload_occurrences'])
    require(len(flattened) == 35 and len(custody['containers']) == 1, 'all original archive occurrences')

    package = SOURCE / 'published-source/asset-002'
    package_files, package_dirs = extent(package)
    isolated_files, isolated_dirs = extent(OWN / 'native-isolated')
    typed(isolated_files, package_files)
    typed(isolated_dirs, package_dirs)
    require(len(package_files) == 35, 'complete unchanged isolated package')
    receipt = load(OWN / 'NATIVE_REPLAY_RECEIPT.json')
    require([r['mode'] for r in receipt['runs']] == ['NORMAL', 'OPTIMIZED'], 'exact two selected native runs')
    for row in receipt['runs']:
        require(row['exit_code'] == 0 and pin(row['whole_stderr']) == b'', 'actual native exit/error stream')
        actual = pin(row['whole_stdout'])
        expected = pin(row['whole_expected'])
        require(actual == expected, 'whole native expected raw stream')
        typed(json.loads(actual), json.loads(expected))
        require(row['meaningful_assertion_verification'] is (row['mode'] == 'NORMAL'), 'O is not assertion verification')
    runtime = load(OWN / 'RUNTIME_MODE_DIAGNOSTIC.json')
    require(runtime['optimization_level'] == 0 and runtime['debug_flag'] is True and runtime['PYTHONOPTIMIZE_environment'] is None, 'ordinary-runtime diagnostic explicitly after the runs')

    handoff = load(OWN / 'RAW_HANDOFF_INDEX.json')
    require(handoff['scientific_interpretations_or_results_included'] is False, 'neutral raw-only handoff')
    for row in handoff['raw_files']:
        pin(row)
    metadata = load(OWN / 'primary/extra/openai-contents.hop0.body')
    require(base64.b64decode(metadata['content']) == body(OWN / 'primary/openai-pinned.pdf'), 'whole actual native GitHub contents body')
    upstream = load(package / 'upstream/UPSTREAM_MANIFEST.json')
    prefix = 'preprints/A-group-without-fixed-price-October-5-2026/'
    for row in upstream['files']:
        path = row['path']
        if not path.startswith(prefix):
            continue
        name = path.removeprefix(prefix)
        if name == 'unequal-costs-rank-100-amalgam.pdf':
            local = OWN / 'primary/openai-pinned.pdf'
        elif name == 'build/surgery-figure.tex':
            local = OWN / 'primary/extra-v3/openai-surgery-figure.hop0.body'
        elif name.startswith('build/'):
            local = OWN / 'primary' / name.removeprefix('build/')
        elif name == 'INPUTS.md':
            local = OWN / 'primary/INPUTS.md'
        else:
            continue
        raw = body(local)
        require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'actual pinned primary body/edition')
    require(verdict['follow_up'] is None and verdict['publication_authority'] is False, 'no follow-up/production invention')
    require(verdict['historical_firstness_or_exhaustive_novelty_certified'] is False, 'no priority inflation')
    own_closed = (OWN / 'FINAL_SEAL.json').exists()
    if own_closed:
        seal = load(OWN / 'FINAL_SEAL.json')
        manifest_bytes = body(OWN / 'MANIFEST.json')
        require(sha(manifest_bytes) == seal['MANIFEST_SHA256'], 'own final manifest pin')
        manifest = json.loads(manifest_bytes)
        require(manifest['exact_root_terminal_exclusions'] == TERMINALS and manifest['recursive_basename_exclusions'] is False, 'exact root terminals only')
        files, directories = extent(OWN)
        require(directories == manifest['directories'], 'entire exact owned directory namespace')
        typed([f for f in files if f['path'] not in TERMINALS], manifest['files'])
        actual_paths = [f['path'] for f in files]
        expected_paths = [f['path'] for f in manifest['files']] + TERMINALS
        require(len(actual_paths) == len(set(actual_paths)) and len(expected_paths) == len(set(expected_paths)), 'unique actual and expected file identities')
        require(sorted(actual_paths) == sorted(expected_paths), 'entire exact owned file namespace; Unicode lexical order on both sides')
    print(json.dumps({'status': 'PASS_OFFLINE_CUSTODY_NO_SCIENTIFIC_REPLAY', 'checks': checks, 'typed_nodes': typed_nodes, 'source_files': len(source_files), 'source_directories': len(source_dirs), 'whole_original_JSON_objects': len(whole), 'archive_containers': 1, 'regular_archive_occurrences': 35, 'isolated_unchanged_native_files': 35, 'complete_native_expected_streams': 2, 'optimized_assertions_are_verification': False, 'own_final_closed_namespace_checked': own_closed, 'scientific_programs_project_imports_subprocess_network_or_writes': False}, indent=2))

if __name__ == '__main__':
    main()
