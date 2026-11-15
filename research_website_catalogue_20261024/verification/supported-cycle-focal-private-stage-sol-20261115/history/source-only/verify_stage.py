"""Pure owned source custody. No project imports, original/live reads, network, subprocess or writes."""
from pathlib import Path
import hashlib
import json
import os
import stat
import sys

O = Path(__file__).resolve().parent
P = O.parent.parent
CHECKS = 0
TYPED_NODES = 0
WRAPPERS = 0


def need(ok, label):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise RuntimeError(label)


def read(path):
    path = Path(path)
    need(O in path.parents and '.git' not in path.parts
         and stat.S_ISREG(path.lstat().st_mode) and path.resolve() == path, 'ordinary owned input only')
    return path.read_bytes()


def sha(body):
    return hashlib.sha256(body).hexdigest()


def obj(path):
    return json.loads(read(path))


def pin(path, row):
    body = read(path)
    need(len(body) == row['bytes'] and sha(body) == row['SHA256'], 'whole owned buffer pin')
    return body


def extent(root):
    need(stat.S_ISDIR(root.lstat().st_mode) and root.resolve() == root, 'real ordinary owned directory')
    files, directories = [], []
    def walk(directory):
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path); mode = entry.stat(follow_symlinks=False).st_mode
                name = path.relative_to(root).as_posix()
                if stat.S_ISDIR(mode):
                    directories.append(name); walk(path)
                else:
                    need(stat.S_ISREG(mode), 'reject namespace links and special entries')
                    files.append(name)
    walk(root)
    return sorted(files), sorted(directories)


def same(a, b):
    global TYPED_NODES
    TYPED_NODES += 1
    need(type(a) is type(b), 'whole object exact scalar/container types')
    if isinstance(a, dict):
        need(list(a) == list(b), 'exact original key order and absent/present fields')
        for key in a:
            same(a[key], b[key])
    elif isinstance(a, list):
        need(len(a) == len(b), 'exact original ordered list length')
        for x, y in zip(a, b):
            same(x, y)
    else:
        need(a == b, 'exact original scalar or null')


def source_fences():
    initial = obj(O / 'INITIAL_SOURCE_SEAL.json')
    need(sha(read(O / 'SOURCE_INPUTS.json')) == initial['SOURCE_INPUTS_SHA256']
         and sha(read(O / 'INITIAL_EXPECTATIONS.json')) == initial['INITIAL_EXPECTATIONS_SHA256']
         and sha(read(O / 'INITIAL_READ_LEDGER.json')) == initial['INITIAL_READ_LEDGER_SHA256'], 'immutable substantive source initial')
    files, directories = extent(O / 'blobs')
    need(files == initial['exact_blob_names'] and directories == initial['blob_directories'], 'exact closed ignored input blobs')
    inputs = obj(O / 'SOURCE_INPUTS.json')
    need(len(inputs['files']) == initial['source_original_files'] == 819 and len(files) == 578,
         'complete initial819 whole input buffers/578 distinct blobs')
    rows = {row['path']: row for row in inputs['files']}
    need(len(rows) == len(inputs['files']), 'unique original input descriptors')
    for row in rows.values():
        pin(O / row['blob'], row)
    def cached(original):
        return pin(O / rows[str(original)]['blob'], rows[str(original)])
    def parsed(original):
        return json.loads(cached(original))
    def wrappers(value, editorial):
        global WRAPPERS
        if isinstance(value, dict):
            if 'whole_literal_object' in value and 'copy' in value:
                original = editorial / value['copy']
                body = cached(original)
                need(len(body) == value['bytes'] and sha(body) == value['SHA256'], 'complete literal wrapper body')
                same(value['whole_literal_object'], json.loads(body))
                WRAPPERS += 1
            for item in value.values():
                wrappers(item, editorial)
        elif isinstance(value, list):
            for item in value:
                wrappers(item, editorial)
    for rid in ['23578142', '23306203']:
        editorial = P / 'papers' / rid / 'reviews/editorial'
        source = P / 'papers' / rid / 'sources'
        publication = parsed(editorial / 'publication.json')
        promotion = parsed(editorial / 'promotion.json')
        root = parsed(P / ('verification/root-editorial-' + rid + '-20261115.json'))
        ready = parsed(source / 'SOURCE_READY.json')
        need(root['root_full_copy_config_code_adopted'] is True and root['private_stage_preparation_authorized'] is True
             and root['production_installation_authorized'] is False, 'actual root stage-only adoption')
        same(ready, publication['source_binding']['whole_original_source_ready'])
        same(publication['source_binding'], promotion['whole_source_binding'])
        wrappers(publication, editorial); wrappers(promotion, editorial)
        protocol = parsed(editorial / 'SOURCE_PROTOCOL_BINDINGS.json')
        wrappers(protocol, editorial)
        native = [parsed(Path(row['path'])) for row in ready['whole_native_API_objects']]
        need([r['role'] for r in ready['whole_native_API_objects']] == ['record', 'latest', 'versions-page001', 'files'],
             'original four native API roles/order')
        same(native[0], native[1])
        need(native[0]['swh'] == {} and native[2]['hits']['hits'][0]['swh'] is None
             and native[3]['order'] == [] and native[3]['default_preview'] is None
             and type(native[3]['entries']) is list, 'native empty/null/key/list distinctions')
        same(native[0]['files'], [r['original_api_file_object'] for r in ready['all_native_assets_in_original_order']])
        same(native[3]['entries'], [r['whole_original_native_files_entry'] for r in ready['all_native_assets_in_original_order']])
        for asset in ready['all_native_assets_in_original_order']:
            body = cached(Path(asset['path']))
            need(len(body) == asset['bytes'] and sha(body) == asset['SHA256'], 'unchanged native asset entire buffer')
        need(cached(editorial / 'citation.bib') == publication['prepared_bibtex'].encode(), 'whole approved Bib')
        main = cached(editorial / 'PUBLIC_MAIN.html')
        candidate = cached(editorial / 'candidate/index.html')
        need(candidate.count(main) == 1 and main.startswith(b'<main id="main">')
             and b'#view=FitH' in main, 'entire adopted MAIN and original reader')
        protected = parsed(editorial / 'PROTECTED_INPUTS.json')
        checkpoint = next(row for row in protected['files'] if row['path'].endswith('/scripts/checkpoint_subtree.py'))
        need(len(protected['core_files']) == 18 and checkpoint['SHA256'] ==
             '405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0',
             'qualified17original plus authorized405b')
        for descriptor in protected['files']:
            body = cached(editorial / descriptor['copy'])
            need(len(body) == descriptor['bytes'] and sha(body) == descriptor['SHA256'], 'complete original retained source/core contract')
        audit_root = Path(root['independent_fact_final_seal']['path']).parent
        same(root['whole_original_independent_fact_findings'], parsed(audit_root / 'FINDINGS.json'))
        if rid == '23306203':
            same(publication['source_binding']['whole_native_record'], native[0])
            same(publication['source_binding']['whole_original_support_metadata'],
                 parsed(source / 'published-source/asset-001/metadata.json'))
            need(publication['printed_version_field_present'] is False and publication['printed_version'] is None
                 and publication['version'] == '1.0.0' and publication['code_license'] == 'CC BY 4.0', 'native versus printed edition and broad rights')
            need(cached(editorial / 'NATIVE_DEPOSIT_DESCRIPTION.html').decode() == publication['native_deposit_description_html'],
                 'whole separate four-paragraph native description')
        else:
            need(publication['mixed_ZIP_encoding_blanket_license_omitted'] is True and publication['code_license'] == 'MIT',
                 'CCBY prose/PDF and MIT code; mixed archive no blanket license')
        need(publication['canonical_url'] is None and publication['AA'] is None and publication['follow_up'] is None,
             'original canonical/AA/follow-up remain literal null')
    return inputs


def main():
    need(sys.argv[1:] == [], 'default pure source custody only')
    source_fences()
    print(json.dumps({'status': 'PASS_PARTIAL_SOURCE_CUSTODY_BASELINE_GO_PENDING', 'checks': CHECKS,
                      'whole_typed_nodes': TYPED_NODES, 'whole_literal_wrappers': WRAPPERS,
                      'source_input_files': 819, 'ignored_whole_blobs': 578,
                      'website_dot_git_original_source_network_subprocess_project_imports_science_or_writes': False,
                      'live_baseline_observed': False, 'final_stage_ready': False,
                      'production_authority': False, 'canonical_url': None, 'AA': None, 'follow_up': None}, sort_keys=True))

if __name__ == '__main__':
    main()
