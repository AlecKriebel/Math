"""Standalone terminal-only custody closure. No project imports or science execution.

Default requires the final seal. --preseal explicitly omits final namespace sealing.
Only Python standard-library byte/JSON/ZIP inspection is performed. No writes,
network, subprocess, imported owner helper, scientific replay or semantic controls.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile

CHECKS = 0


def require(test, label):
    global CHECKS
    CHECKS += 1
    if not test:
        raise ValueError(label)


def sha(body):
    return hashlib.sha256(body).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def same(a, b, label):
    require(type(a) is type(b), label + ': literal type')
    if isinstance(a, dict):
        require(list(a) == list(b), label + ': key order and absence')
        for k in a:
            same(a[k], b[k], label + '/' + k)
    elif isinstance(a, list):
        require(len(a) == len(b), label + ': list size')
        for i, (x, y) in enumerate(zip(a, b)):
            same(x, y, label + '/' + str(i))
    else:
        require(a == b, label + ': literal value')


def check_file(p, entry):
    require(p.is_file() and not p.is_symlink(), str(p) + ': regular file')
    b = p.read_bytes()
    require(len(b) == entry['bytes'] and sha(b) == entry['SHA256'], str(p) + ': whole bytes')
    return b


def check_wrapper(e, wrapper):
    relative = PurePosixPath(wrapper['copy'])
    require(not relative.is_absolute() and '..' not in relative.parts, 'wrapper path escape')
    b = check_file(e / str(relative), wrapper)
    same(json.loads(b), wrapper['whole_literal_object'], 'whole wrapper ' + str(relative))


def main():
    require(sys.argv[1:] in [[], ['--preseal']], 'unsupported arguments')
    preseal = sys.argv[1:] == ['--preseal']
    e = Path(__file__).resolve().parent
    require(e.name == 'editorial' and e.parent.name == 'reviews'
            and e.parents[1].name == '23392409', 'strict owner namespace')
    baseline = load(e / 'PROTECTED_INPUTS.json')
    s = Path(baseline['source_root'])
    require(s == e.parents[1] / 'sources', 'source namespace binding')
    actual_source = sorted(str(p) for p in s.rglob('*') if p.is_file())
    require(actual_source == [x['path'] for x in baseline['source_files']], 'whole source namespace unchanged')
    for entry in baseline['source_files'] + baseline['other_files']:
        check_file(Path(entry['path']), entry)
    copy_paths = {
        'ROOT_CLEARANCE.json': Path(baseline['other_files'][0]['path']),
        'ROOT_REVIEW_20261115.md': e.parent / 'root/ROOT_REVIEW_20261115.md',
        'scope-VERDICT.json': e.parent / 'scope/VERDICT.json',
        'adversarial-VERDICT.json': e.parent / 'adversarial/VERDICT.json',
        'adversarial-PRIMARY_READ_LEDGER.json': e.parent / 'adversarial/PRIMARY_READ_LEDGER.json',
        'README.md': s / 'published-source/asset-003/README.md',
        'LICENSE.txt': s / 'published-source/asset-003/LICENSE.txt'
    }
    for p in (e / 'inputs').iterdir():
        require(p.is_file() and not p.is_symlink(), 'inputs regular only')
        original = copy_paths.get(p.name, s / p.name)
        require(p.read_bytes() == original.read_bytes(), 'whole original copy: ' + p.name)
    protocol = load(e / 'SOURCE_PROTOCOL_BINDINGS.json')
    for key in ['source_ready', 'whole_ordered_transport_receipts', 'whole_native_schema_types',
                'whole_archive_custody', 'whole_original_queue_binding',
                'whole_original_native_identity_subset', 'whole_root_scientific_authority',
                'source_manifest', 'source_seal']:
        check_wrapper(e, protocol[key])
    for item in protocol['whole_native_API_objects'] + protocol['whole_original_scientific_custom_verdicts']:
        check_wrapper(e, item)
    ready = load(s / 'SOURCE_READY.json')
    authority = load(e / 'inputs/ROOT_CLEARANCE.json')
    scope = load(e / 'inputs/scope-VERDICT.json')
    adversarial = load(e / 'inputs/adversarial-VERDICT.json')
    same(authority['source_ready_whole_original'], ready, 'root full READY')
    same(adversarial['whole_original_SOURCE_READY_object'], ready, 'adversarial full READY')
    same(authority['whole_original_scientific_verdicts'][0]['whole_literal_object'], scope, 'root scope verdict')
    same(authority['whole_original_scientific_verdicts'][1]['whole_literal_object'], adversarial, 'root adversarial verdict')
    p = load(e / 'publication.json')
    promotion = load(e / 'promotion.json')
    same(p['source_binding']['whole_original_source_ready'], ready, 'publication whole READY')
    same(promotion['whole_source_binding'], p['source_binding'], 'promotion complete source binding')
    same(p['review_metadata']['root_authority'], protocol['whole_root_scientific_authority'], 'publication root authority')
    same(promotion['whole_root_scientific_authority'], protocol['whole_root_scientific_authority'], 'promotion root authority')
    same(p['review_metadata']['whole_original_custom_verdicts'], protocol['whole_original_scientific_custom_verdicts'], 'publication whole verdicts')
    same(promotion['whole_original_two_scientific_custom_verdicts'], protocol['whole_original_scientific_custom_verdicts'], 'promotion whole verdicts')
    require(promotion['scientific_status_literal_from_root'] == authority['literal_root_scientific_disposition'],
            'literal custom status, no generic PASS conversion')
    require(authority['editorial_preparation_authorized'] is True
            and authority['production_installation_authorized'] is False, 'actual editorial authority bounds')
    for key in ['rendered_public_copy_approved', 'production_integration_authorized', 'ready_to_publish',
                'installed', 'deployed', 'live_verified', 'local_http_verified', 'browser_verified',
                'native_verified', 'native_sheet_publication_verified', 'canonical_verified', 'public_page_published']:
        require(promotion[key] is False, 'ungranted authority: ' + key)
    for key in ['canonical_url', 'AA', 'native_sheet_aa_url', 'follow_up']:
        require(p[key] is None and promotion[key] is None, 'private null field: ' + key)
    record = load(s / 'record.response.body')
    latest = load(s / 'latest.response.body.redirect-01')
    versions = load(s / 'versions-page001.response.body')
    files = load(s / 'files.response.body')
    require('version' not in record['metadata'] and 'version' not in latest['metadata']
            and all('version' not in v['metadata'] for v in versions['hits']['hits']),
            'native version absence retained')
    require(ready['native_version_whole_field'] == {'present': False, 'original_value': None}
            and p['version_field_present'] is False and p['version'] is None,
            'version presence/value distinction retained')
    require(record['swh'] == {} and latest['swh'] == {} and versions['hits']['hits'][0]['swh'] is None,
            'native empty object versus null')
    require(isinstance(files['entries'], list) and files['order'] == []
            and files['default_preview'] is None, 'native list empty-order null distinctions')
    native_order = [x['key'] for x in record['files']]
    require(native_order == ['five_centers.pdf', 'five_centers.tex', 'verification-package.zip']
            and [x['key'] for x in files['entries']] == native_order
            and protocol['native_asset_order'] == native_order, 'complete original native asset order')
    for asset in ready['all_native_assets_in_original_order']:
        name = asset['original_api_file_object']['key']
        b = check_file(e / 'candidate' / name, asset)
        require(b == Path(asset['path']).read_bytes()
                and b == Path(asset['transport_body_path']).read_bytes(), 'whole native asset and transport identity')
        require('md5:' + hashlib.md5(b).hexdigest() == asset['original_api_file_object']['checksum'],
                'native checksum ' + name)
    require((e / 'candidate/citation.bib').read_bytes() == (e / 'citation.bib').read_bytes(), 'BibTeX whole identity')
    require((e / 'candidate/five_centers.pdf').read_bytes()
            == Path(ready['embedded_PDFs'][0]['extracted_path']).read_bytes(), 'embedded PDF full identity')
    require((e / 'candidate/five_centers.tex').read_bytes()
            == Path(ready['controlling_TeX']['extracted_path']).read_bytes(), 'embedded controlling TeX identity')
    seen = set()
    regular_count = 0
    with zipfile.ZipFile(e / 'candidate/verification-package.zip') as z:
        for info in z.infolist():
            path = PurePosixPath(info.filename)
            require(not path.is_absolute() and '..' not in path.parts and '\\' not in info.filename,
                    'archive member path guard')
            require(info.filename.casefold() not in seen, 'archive duplicate/case collision')
            seen.add(info.filename.casefold())
            mode = stat.S_IFMT(info.external_attr >> 16)
            if info.is_dir():
                require(mode in [0, stat.S_IFDIR], 'directory type guard')
                continue
            require(mode in [0, stat.S_IFREG], 'archive nonregular guard')
            body = z.read(info)
            require(len(body) == info.file_size, 'ZIP size and automatic CRC check')
            require(body == (s / 'published-source/asset-003' / str(path)).read_bytes(), 'whole original extracted payload')
            regular_count += 1
    require(regular_count == 64 == ready['whole_regular_payload_occurrences'], 'complete64 payloads')
    require(ready['mathematical_PDF_TeX_or_pixels_read'] is False
            and ready['printed_date'] is None and ready['printed_version'] is None,
            'original historical unread and null flags unchanged')
    owned = None
    if not preseal:
        seal = load(e / 'SEAL.json')
        manifest_bytes = check_file(e / 'MANIFEST.json', seal['manifest'])
        manifest = json.loads(manifest_bytes)
        expected = sorted(x['relative_path'] for x in manifest['files'])
        actual = sorted(str(x.relative_to(e)) for x in e.rglob('*')
                        if x.is_file() and x not in [e / 'MANIFEST.json', e / 'SEAL.json'])
        require(actual == expected, 'complete owned namespace, no omitted new files')
        for entry in manifest['files']:
            path = PurePosixPath(entry['relative_path'])
            require(not path.is_absolute() and '..' not in path.parts, 'manifest path guard')
            check_file(e / str(path), entry)
        for entry in seal['preseal_receipts']:
            check_file(e / entry['relative_path'], entry)
        require(seal['production_authority'] is False and seal['AA'] is None
                and seal['canonical_url'] is None, 'seal authority')
        owned = len(expected)
    print(json.dumps({'status': 'PASS', 'mode': 'preseal' if preseal else 'final',
                      'python': sys.version.split()[0], 'optimized': not __debug__, 'custody_checks': CHECKS,
                      'unchanged_source_files': len(baseline['source_files']),
                      'whole_original_ZIP_regular_payloads': regular_count,
                      'owned_payloads': owned, 'scientific_execution': False,
                      'project_imports_network_writes_subprocess_or_semantic_controls': False,
                      'publication_authority': False}))


if __name__ == '__main__':
    main()
