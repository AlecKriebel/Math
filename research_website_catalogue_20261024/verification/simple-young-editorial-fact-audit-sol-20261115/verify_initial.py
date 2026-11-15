#!/usr/bin/env python3
"""Read-only source/root custody closure; no project imports or scientific execution."""
from pathlib import Path
import hashlib
import json
import stat
import zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
SOURCE = BASE / 'papers/23418581/sources'
checks = 0
nodes = 0

def need(value, message):
    global checks
    checks += 1
    if not value:
        raise RuntimeError(message)

def raw(path):
    need(stat.S_ISREG(path.lstat().st_mode), 'nonregular input: ' + str(path))
    return path.read_bytes()

def digest(body):
    return hashlib.sha256(body).hexdigest()

def obj(path):
    return json.loads(raw(path))

def same(a, b, label):
    global nodes
    nodes += 1
    need(type(a) is type(b), 'type: ' + label)
    if isinstance(a, dict):
        need(list(a) == list(b), 'ordered keys: ' + label)
        for k in a:
            same(a[k], b[k], label + '/' + k)
    elif isinstance(a, list):
        need(len(a) == len(b), 'list length: ' + label)
        for i, (x, y) in enumerate(zip(a, b)):
            same(x, y, label + '/' + str(i))
    else:
        need(a == b, 'value: ' + label)

def extent(root):
    files, dirs = [], []
    for p in sorted(root.rglob('*')):
        mode = p.lstat().st_mode
        rel = p.relative_to(root).as_posix()
        if stat.S_ISDIR(mode):
            dirs.append(rel)
        else:
            need(stat.S_ISREG(mode), 'nonregular extent: ' + str(p))
            b = raw(p)
            files.append({'path': rel, 'bytes': len(b), 'SHA256': digest(b)})
    return {'files': files, 'directories': dirs}

def main():
    seal = obj(HERE / 'INITIAL_SEAL.json')
    for row in seal['payloads']:
        b = raw(HERE / row['path'])
        need(len(b) == row['bytes'] and digest(b) == row['SHA256'], 'initial payload ' + row['path'])
    same(extent(SOURCE), obj(HERE / 'INITIAL_SOURCE_MANIFEST.json'), 'source extent')
    pins = obj(HERE / 'INITIAL_INPUT_BINDINGS.json')
    for row in pins['root_inputs']:
        b = raw(Path(row['path']))
        need(len(b) == row['bytes'] and digest(b) == row['SHA256'], 'root input')
    snapshot = obj(HERE / 'INITIAL_NATIVE_INPUTS.json')
    for rel, value in snapshot['whole_root_source_JSON_objects'].items():
        same(obj(SOURCE / rel), value, 'native/' + rel)
    authority = obj(Path(pins['root_inputs'][1]['path']))
    same(authority, snapshot['whole_root_authority'], 'root authority')
    ready = obj(SOURCE / 'SOURCE_READY.json')
    same(ready, authority['source_native_ready_whole_unchanged'], 'root original READY')
    same(ready, authority['whole_original_adversarial_verdict']['whole_original_SOURCE_READY'], 'adversarial original READY')
    record = obj(SOURCE / 'record.response.body')
    need(record['metadata']['description'] == snapshot['native_description_HTML'], 'whole native description')
    need(record['metadata']['version'] == '1.0' and record['metadata']['publication_date'] == '2026-10-16', 'edition')
    need([x['key'] for x in record['files']] == ['source-and-verification.zip', 'paper.pdf'], 'asset order')
    need(record['metadata']['license'] == {'id': 'cc-by-4.0'}, 'native rights')
    tex = raw(SOURCE / 'published-source/asset-001/paper.tex').decode()
    need(tex.split('\\begin{abstract}', 1)[1].split('\\end{abstract}', 1)[0] == snapshot['printed_abstract_TeX_raw'], 'full printed abstract')
    need(raw(SOURCE / 'published-source/asset-001/LICENSE.txt').decode() == snapshot['authored_license_literal'], 'license text')
    need(len(tex.splitlines()) == 279 and ready['selected_actual_PDF']['pages'] == 4, 'paper extent')
    need(ready['embedded_PDFs'] == [] and ready['actual_standalone_TeX_assets'] == [], 'native reader shape')
    custody = obj(SOURCE / 'ARCHIVE_CUSTODY.json')
    occurrence_count = 0
    flattened = []
    for container in custody['containers']:
        path = Path(container['input_path'])
        b = raw(path)
        need(len(b) == container['input_bytes'] and digest(b) == container['input_SHA256'], 'archive bytes')
        with zipfile.ZipFile(path) as z:
            infos = z.infolist()
            need(z.comment.hex() == container['original_archive_comment_hex'], 'archive comment')
            central = []
            for i, info in enumerate(infos):
                central.append({'ordinal_zero_based': i, 'filename': info.filename, 'original_filename': info.orig_filename, 'is_directory': info.is_dir(), 'bytes': info.file_size, 'compressed_bytes': info.compress_size, 'CRC32': f'{info.CRC:08x}', 'flags': info.flag_bits, 'compression': info.compress_type, 'native_date_time': list(info.date_time), 'external_attr': info.external_attr, 'internal_attr': info.internal_attr, 'create_system': info.create_system, 'create_version': info.create_version, 'extract_version': info.extract_version, 'header_offset': info.header_offset, 'extra_hex': info.extra.hex(), 'comment_hex': info.comment.hex()})
            same(central, container['whole_original_central_directory'], 'central directory')
            for row in container['members']:
                info = infos[row['ordinal_zero_based']]
                body = z.read(info)
                need(not info.is_dir() and info.filename == row['original_member_name'], 'regular occurrence identity')
                need(len(body) == row['bytes'] and digest(body) == row['SHA256'], 'occurrence bytes')
                need(body == raw(Path(row['extracted_path'])), 'whole extracted body')
                flattened.append(row)
                occurrence_count += 1
    same(flattened, custody['regular_payload_occurrences'], 'whole occurrence stream')
    need(len(custody['containers']) == 4 and occurrence_count == 243, 'archive extent')
    a = raw(SOURCE / 'published-source/asset-001/audit/math_schur/TENSOR_CHECK_NORMAL.json')
    b = raw(SOURCE / 'published-source/asset-001/audit/math_schur/TENSOR_CHECK_OPTIMIZED.json')
    need(a == b and len(a) == 4091 and digest(a) == '4ca5921832dd43104bd351370db3694bd7c8bb498698a58fa892052bfc06ed38', 'whole saved scientific outputs; no replay')
    need(seal['current_editorial_namespace_listed_or_read'] is False, 'initial exposure record')
    print(json.dumps({'status': 'PASS_SOURCE_ROOT_ONLY_INITIAL', 'checks': checks, 'typed_nodes': nodes, 'source_files': len(obj(HERE / 'INITIAL_SOURCE_MANIFEST.json')['files']), 'archive_containers': 4, 'regular_occurrences': occurrence_count, 'whole_native_root_JSON_objects': len(snapshot['whole_root_source_JSON_objects']), 'editorial_access': False, 'scientific_execution': False, 'project_imports': False, 'subprocess': False, 'network': False, 'writes': False}, indent=2))

if __name__ == '__main__':
    main()
