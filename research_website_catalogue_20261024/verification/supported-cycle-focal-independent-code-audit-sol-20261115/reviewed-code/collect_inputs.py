"""New source-only byte intake. No source helper imports/execution or live website/Git access."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = Path(__file__).resolve().parent
ROOT_PINS = {'23578142': '97d56a98f09193fc57734f494f049e4223df5a0ec99ebd50865ad181cba80af5',
             '23306203': '8d1bf740eaa8b686ef953a9ba83603459e27229be854ded0156a3a523162dc95'}


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def sha(body):
    return hashlib.sha256(body).hexdigest()


def read(path):
    need(path.is_relative_to(P) and '.git' not in path.parts
         and stat.S_ISREG(path.lstat().st_mode) and path.resolve() == path, 'ordinary permitted source input')
    return path.read_bytes()


def extent(root):
    need(stat.S_ISDIR(root.lstat().st_mode) and root.resolve() == root, 'real ordinary root')
    files, directories = [], []
    def walk(directory):
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path); mode = entry.stat(follow_symlinks=False).st_mode
                name = path.relative_to(root).as_posix()
                if stat.S_ISDIR(mode):
                    directories.append(name); walk(path)
                else:
                    need(stat.S_ISREG(mode), 'no source symlinks or specials')
                    files.append(name)
    walk(root)
    return sorted(files), sorted(directories)


def typed(value):
    if isinstance(value, dict):
        return ['dict', [[k, typed(v)] for k, v in value.items()]]
    if isinstance(value, list):
        return ['list', [typed(v) for v in value]]
    return [type(value).__name__, value]


def main():
    need(not (O / 'SOURCE_INPUTS.json').exists(), 'write-once source-only intake')
    (O / 'blobs').mkdir()
    rows, namespaces, copies = {}, [], []
    def freeze(path, expected=None):
        body = read(path)
        if expected:
            need(len(body) == expected['bytes'] and sha(body) == expected['SHA256'], 'whole adopted source pin')
        key = sha(body); destination = O / 'blobs' / key
        if not destination.exists():
            destination.write_bytes(body)
        need(read(destination) == body, 'whole retained input bytes')
        rows[str(path)] = {'path': str(path), 'bytes': len(body), 'SHA256': key, 'blob': 'blobs/' + key}
        return body
    for rid, expected_root in ROOT_PINS.items():
        root_path = P / ('verification/root-editorial-' + rid + '-20261115.json')
        root_body = freeze(root_path); need(sha(root_body) == expected_root, 'actual adopted root copy/config receipt')
        root = json.loads(root_body)
        need(root['root_full_copy_config_code_adopted'] is True and root['private_stage_preparation_authorized'] is True
             and root['production_installation_authorized'] is False, 'stage permission only, never install authority')
        editorial = P / 'papers' / rid / 'reviews/editorial'
        seal_descriptor = root['owner_final_seal'] if rid == '23578142' else root['editorial_final_seal']
        seal_body = freeze(editorial / 'SEAL.json', seal_descriptor); seal = json.loads(seal_body)
        manifest_body = freeze(editorial / 'MANIFEST.json', seal['manifest']); manifest = json.loads(manifest_body)
        files, directories = extent(editorial)
        need(files == sorted(list(manifest['payloads']) + ['MANIFEST.json', 'SEAL.json'])
             and directories == manifest['directories'], 'complete closed editorial namespace')
        for name, descriptor in manifest['payloads'].items():
            freeze(editorial / name, descriptor)
        namespaces.append({'kind': 'editorial', 'record_id': rid, 'path': str(editorial),
                           'files': files, 'directories': directories})
        publication = json.loads(read(editorial / 'publication.json'))
        source = P / 'papers' / rid / 'sources'
        ready_body = freeze(source / 'SOURCE_READY.json'); ready = json.loads(ready_body)
        need(typed(ready) == typed(publication['source_binding']['whole_original_source_ready']),
             'whole original SOURCE_READY types/key/list order/null/absence preserved')
        source_seal = json.loads(freeze(source / 'SOURCE_READY_SEAL.json'))
        need(sha(ready_body) == source_seal['SOURCE_READY_SHA256'], 'original source READY whole bytes')
        source_manifest_body = freeze(source / 'SOURCE_READY_MANIFEST.json')
        need(sha(source_manifest_body) == source_seal['MANIFEST_SHA256'], 'original source manifest pin')
        source_manifest = json.loads(source_manifest_body)
        files, directories = extent(source)
        need(files == sorted([r['path'] for r in source_manifest['files']] + source_manifest['excluded_terminal_files']),
             'whole native source ordinary file namespace')
        for descriptor in source_manifest['files']:
            freeze(source / descriptor['path'], descriptor)
        for name in source_manifest['excluded_terminal_files']:
            freeze(source / name)
        need(sha(read(source / 'SOURCE_READY_CLOSURE.json')) == source_seal['CLOSURE_SHA256'], 'literal source closure')
        namespaces.append({'kind': 'source', 'record_id': rid, 'path': str(source), 'files': files, 'directories': directories})
        authority = root['root_full_scientific_authority'] if rid == '23578142' else root['root_scientific_authority']
        freeze(Path(authority['path']), authority)
        audit_descriptor = root['independent_fact_final_seal']; audit = Path(audit_descriptor['path']).parent
        audit_seal = json.loads(freeze(audit / 'FINAL_SEAL.json', audit_descriptor))
        audit_manifest_body = freeze(audit / 'FINAL_MANIFEST.json')
        need(sha(audit_manifest_body) == audit_seal['MANIFEST_SHA256'], 'actual independent fact audit manifest')
        audit_manifest = json.loads(audit_manifest_body); files, directories = extent(audit)
        need(files == sorted([r['path'] for r in audit_manifest['files']] + audit_manifest['excluded_exact_root_terminal_files'])
             and directories == audit_manifest['directories'], 'whole closed independent fact audit namespace')
        for descriptor in audit_manifest['files']:
            freeze(audit / descriptor['path'], descriptor)
        namespaces.append({'kind': 'fact_audit', 'record_id': rid, 'path': str(audit), 'files': files, 'directories': directories})
        copies.append({'record_id': rid, 'slug': publication['slug'], 'native_original_order': ready['all_native_assets_in_original_order'],
                       'publication': rows[str(editorial / 'publication.json')], 'promotion': rows[str(editorial / 'promotion.json')],
                       'MAIN': rows[str(editorial / 'PUBLIC_MAIN.html')], 'COPY': rows[str(editorial / 'PUBLIC_COPY.md')]})
    result = {'schema': 'supported-cycle-focal-source-only-inputs-v1', 'UTC': datetime.now(timezone.utc).isoformat(),
              'status': 'PARTIAL_SOURCE_INPUTS_FROZEN_LIVE_BASELINE_GO_PENDING', 'files': list(rows.values()),
              'complete_original_namespaces': namespaces, 'records': copies,
              'all_original_raw_schemas_types_key_list_order_null_and_history_preserved': True,
              'whole_bodies_byte_frozen_not_claimed_all_scientific_bodies_semantically_reread': True,
              'website_dot_git_Git_Sheet_network_or_source_campaign_access': False,
              'production_installation_authorized': False, 'canonical_url': None, 'AA': None, 'follow_up': None}
    (O / 'SOURCE_INPUTS.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'status': result['status'], 'source_input_files': len(rows), 'namespaces':
                     [{'kind': n['kind'], 'id': n['record_id'], 'files': len(n['files']), 'directories': len(n['directories'])} for n in namespaces],
                     'distinct_blobs': len(list((O / 'blobs').iterdir())), 'website_or_Git_access': False}, indent=2))

if __name__ == '__main__':
    main()
