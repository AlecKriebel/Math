#!/usr/bin/env python3
"""Read-only source/root custody closure; no project imports or scientific execution."""
from pathlib import Path
import hashlib
import json
import stat
import zipfile
import html
from html.parser import HTMLParser

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

def source_closure():
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
    by_occurrence = {(row['container_id'], row['ordinal_zero_based']): row for row in flattened}
    need(len(by_occurrence) == len(flattened), 'unique occurrence identities')
    need(len(custody['regular_payload_occurrences']) == len(flattened), 'whole occurrence length')
    for row in custody['regular_payload_occurrences']:
        same(row, by_occurrence[(row['container_id'], row['ordinal_zero_based'])], 'original traversal occurrence')
    need(len(custody['containers']) == 4 and occurrence_count == 243, 'archive extent')
    a = raw(SOURCE / 'published-source/asset-001/audit/math_schur/TENSOR_CHECK_NORMAL.json')
    b = raw(SOURCE / 'published-source/asset-001/audit/math_schur/TENSOR_CHECK_OPTIMIZED.json')
    need(a == b and len(a) == 4091 and digest(a) == '4ca5921832dd43104bd351370db3694bd7c8bb498698a58fa892052bfc06ed38', 'whole saved scientific outputs; no replay')
    need(seal['current_editorial_namespace_listed_or_read'] is False, 'initial exposure record')
    return {'status': 'PASS_SOURCE_ROOT_ONLY_INITIAL', 'checks': checks, 'typed_nodes': nodes, 'source_files': len(obj(HERE / 'INITIAL_SOURCE_MANIFEST.json')['files']), 'archive_containers': 4, 'regular_occurrences': occurrence_count, 'whole_native_root_JSON_objects': len(snapshot['whole_root_source_JSON_objects']), 'editorial_access': False, 'scientific_execution': False, 'project_imports': False, 'subprocess': False, 'network': False, 'writes': False}


class Layout(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.content = []
        self.json_data = []
        self.in_json = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        self.tags.append((tag, attrs))
        if tag == 'script':
            self.in_json = attrs.get('type') == 'application/ld+json'

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_json = False

    def handle_data(self, text):
        self.content.append(text)
        if self.in_json:
            self.json_data.append(text)


def checked_pin(row):
    p = Path(row['path'])
    body = raw(p)
    need(len(body) == row['bytes'] and digest(body) == row['SHA256'], 'whole pinned file')
    return body


def main():
    source_result = source_closure()
    bindings = obj(HERE / 'EDITORIAL_BINDINGS.json')
    editorial = Path(bindings['editorial_namespace'])
    seal_bytes = checked_pin(bindings['FINAL_seal'])
    need(digest(seal_bytes) == '671d27c2cb8c1c2a3111e4f765fdeb5d7a1562fdd9fe7f57bb7960a55ac4ee4f', 'root-forwarded owner seal')
    sealed = json.loads(seal_bytes)
    manifest_bytes = checked_pin(bindings['manifest'])
    need(digest(manifest_bytes) == '900d6ae922b913dac420ee3253e3832136989316c763c472af22ab73eb8087d9', 'root-forwarded owner manifest')
    manifest = json.loads(manifest_bytes)
    terminals = ['MANIFEST.json', 'CLOSURE_RECEIPT.json', 'FINAL_SEAL.json']
    need(manifest['exact_root_terminal_controls'] == sealed['exact_root_terminal_controls'] == terminals, 'exact owner root terminals')
    need(manifest['recursive_basename_exclusions'] is False, 'no basename exclusion')
    rows = manifest['files']
    names = [x['relative_path'] for x in rows]
    need(len(names) == len(set(names)) == 334 and not set(names) & set(terminals), 'unique finite payload extent')
    for row in rows:
        rel = Path(row['relative_path'])
        need(not rel.is_absolute() and '..' not in rel.parts and str(rel) == row['relative_path'], 'safe relative path')
        b = raw(editorial / rel)
        need(len(b) == row['bytes'] and digest(b) == row['SHA256'], 'whole owner payload')
    actual = extent(editorial)
    need([x['path'] for x in actual['files']] == sorted(names + terminals), 'strict owner files; exact root exclusions')
    need(actual['directories'] == manifest['directories'] and len(actual['directories']) == 29, 'strict owner directories')
    checked_pin(sealed['closure'])
    checked_pin(sealed['manifest'])
    for row in bindings['full_current_and_historical_helpers_read']:
        checked_pin(row)
    for key in ('stdout', 'stderr'):
        checked_pin(bindings['actual_owner_pure'][key])
    need(bindings['actual_owner_pure']['exit_code'] == 0 and checked_pin(bindings['actual_owner_pure']['stderr']) == b'', 'actual owner pure success')

    protocol = obj(editorial / 'SOURCE_PROTOCOL_BINDINGS.json')
    ready = obj(SOURCE / 'SOURCE_READY.json')
    initial = obj(HERE / 'INITIAL_NATIVE_INPUTS.json')
    same(protocol['whole_original_source_ready'], ready, 'whole protocol READY')
    same(protocol['whole_literal_root_authority'], initial['whole_root_authority'], 'whole protocol root authority')
    original_objects = protocol['whole_original_source_JSON_objects']
    expected_JSON_names = [name for name in initial['whole_root_source_JSON_objects'] if name.endswith('.json')]
    need([Path(row['original']['path']).name for row in original_objects] == expected_JSON_names, 'all native dot-JSON objects in original order')
    for row in original_objects:
        p = Path(row['original']['path'])
        need(p.parent == SOURCE, 'native root-object path')
        same(json.loads(checked_pin(row['original'])), row['whole_original_object'], 'whole native protocol object')
        same(row['whole_original_object'], initial['whole_root_source_JSON_objects'][p.name], 'whole native pre-exposure baseline')
    native_api = protocol['whole_native_API_objects_in_original_role_order']
    need(len(native_api) == len(ready['whole_native_API_objects']) == 4, 'all four native roles')
    for row, expected in zip(native_api, ready['whole_native_API_objects']):
        same(row['original'], expected, 'original API role/order/pin')
        same(json.loads(checked_pin(row['original'])), row['whole_original_object'], 'whole native API body')
    for row in ready['raw_non_200_response_bodies']:
        path = Path(row['body_path'])
        need(raw(path) == raw(editorial / 'raw/source' / path.relative_to(SOURCE)), 'whole literal non-200 native body')
        same(obj(path), initial['whole_root_source_JSON_objects'][path.name], 'whole original redirect body object')
    verdicts = protocol['whole_original_scientific_verdicts']
    need(len(verdicts) == 2, 'two whole heterogeneous scientific verdicts')
    for row, key in zip(verdicts, ['whole_original_scope_verdict', 'whole_original_adversarial_verdict']):
        same(json.loads(checked_pin(row['original'])), row['whole_original_object'], 'whole scientific verdict original')
        same(row['whole_original_object'], initial['whole_root_authority'][key], 'whole root-adopted scientific verdict')
    inputs = obj(editorial / 'INPUT_BINDINGS.json')
    same(inputs['source_namespace']['directories'], obj(HERE / 'INITIAL_SOURCE_MANIFEST.json')['directories'], 'original source directories')
    for row in obj(HERE / 'INITIAL_SOURCE_MANIFEST.json')['files']:
        need(raw(SOURCE / row['path']) == raw(editorial / 'raw/source' / row['path']), 'whole source-private bytes')
    need(raw(editorial / 'raw/ROOT_REVIEW.md') == raw(Path(obj(HERE / 'INITIAL_INPUT_BINDINGS.json')['root_inputs'][0]['path'])), 'whole root proof copy')
    same(obj(editorial / 'raw/root-clearance.json'), initial['whole_root_authority'], 'whole private root authority')

    pub = obj(editorial / 'publication.json')
    sections = obj(editorial / 'public-sections.json')
    for key, value in sections.items():
        same(value, pub[key], 'actual public sections/config')
    same(pub['source_binding']['whole_original_source_ready'], ready, 'whole publication READY')
    same(pub['source_binding']['whole_native_API_objects'], native_api, 'whole publication APIs')
    same(pub['review_metadata']['whole_original_scientific_verdicts'], verdicts, 'whole publication scientific verdicts')
    same(pub['review_metadata']['root_authority']['whole_literal_object'], initial['whole_root_authority'], 'whole publication root authority')
    same(pub['source_binding']['native_asset_order'], ['source-and-verification.zip', 'paper.pdf'], 'literal native order')
    for desc in [protocol['native_description_HTML_original'], pub['source_binding']['native_deposit_description_HTML_original'], raw(editorial / 'raw/NATIVE_DESCRIPTION.html').decode()]:
        need(desc == initial['native_description_HTML'], 'whole distinct native description')
    tex_abstract = initial['printed_abstract_TeX_raw'].removeprefix('\n')
    need(raw(editorial / 'ORIGINAL_ABSTRACT.tex').decode() == tex_abstract == protocol['original_printed_abstract_TeX'], 'full original abstract source')
    for old, new in [(r'\(p\)', 'p'), (r'\(\lambda=(2p-2,1)\)', 'λ = (2p−2,1)'), (r'\(I_n(\lambda)\)', 'I_n(λ)'), (r'\(n\ge2\)', 'n≥2'), (r'\(q=1\)', 'q=1'), ('~', ' '), ("Miyachi's", 'Miyachi’s')]:
        tex_abstract = tex_abstract.replace(old, new)
    need(' '.join(tex_abstract.split()) == pub['abstract'], 'complete printed abstract only typography/math conversion')
    need(pub['version'] == pub['printed_version'] == '1.0' and pub['publication_date'] == '2026-10-16', 'edition 1.0 not 1.0.0')
    need(pub['license'] == pub['authored_package_license'] == 'CC BY 4.0' and pub['code_license'] is None, 'broad authored rights; no invented separate license')
    for key in ['follow_up', 'canonical_url', 'AA', 'native_sheet_aa_url', 'proposed_canonical_url']:
        need(pub[key] is None, 'actual null boundary')
    need(pub['production_authority'] is False and pub['root_full_copy_config_adoption_pending'] is True, 'no adoption/production invention')
    for name in ['PUBLICATION_REQUIREMENTS.json', 'SCHEMA_ADAPTER.json', 'promotion.json', 'VERDICT.json']:
        record = obj(editorial / name)
        need(record['production_authority'] is False and record['canonical_url'] is None and record['AA'] is None and record['follow_up'] is None, 'all unique no-authority interfaces')

    main_html = raw(editorial / 'PUBLIC_MAIN.html').decode()
    candidate = raw(editorial / 'candidate/index.html').decode()
    copy = raw(editorial / 'PUBLIC_COPY.md').decode()
    need(candidate.count(main_html) == 1, 'entire exact MAIN preserved')
    layout = Layout()
    layout.feed(candidate)
    ids = [a['id'] for t, a in layout.tags if 'id' in a]
    need(len(ids) == len(set(ids)), 'unique IDs')
    need(sum(t == 'main' for t, a in layout.tags) == sum(t == 'h1' for t, a in layout.tags) == sum(t == 'article' for t, a in layout.tags) == 1, 'one main/article/title')
    for tag, attrs in layout.tags:
        need(not any(k.startswith('on') for k in attrs), 'no event-handler code')
        for label in attrs.get('aria-labelledby', '').split():
            need(label in ids, 'resolvable accessible label')
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            need(attrs['href'][1:] in ids, 'resolvable page anchor')
    frames = [a for t, a in layout.tags if t == 'iframe']
    need(len(frames) == 1 and frames[0]['src'] == 'paper.pdf#view=FitH' and frames[0].get('title'), 'titled whole original PDF')
    need('href="#main-content"' in candidate and '.skip:focus' in candidate and 'a:focus-visible' in candidate, 'skip/focus access')
    scripts = [a for t, a in layout.tags if t == 'script']
    need(len(scripts) == 1 and scripts[0] == {'type': 'application/ld+json'}, 'metadata script only')
    same(json.loads(''.join(layout.json_data)), obj(editorial / 'SCHOLARLY_METADATA.json'), 'whole actual JSON-LD')
    metas = {a['name']: a.get('content') for t, a in layout.tags if t == 'meta' and 'name' in a}
    need(metas['robots'] == 'noindex,nofollow' and metas['citation_version'] == '1.0' and metas['citation_doi'] == '10.5281/zenodo.23418581', 'actual private scholarly head')
    need(not any(t == 'link' and a.get('rel') == 'canonical' for t, a in layout.tags), 'no candidate canonical')
    for key in ['plain_language', 'result', 'why_it_works', 'definitions_and_limits', 'background']:
        for paragraph in sections[key]:
            need(paragraph in copy and html.escape(paragraph) in main_html, 'full copy/config/MAIN paragraphs')
    for key in ['abstract', 'collaboration', 'ai_disclosure', 'rights_notice', 'reader_intro']:
        need(sections[key] in copy and html.escape(sections[key]) in main_html, 'full copy/status/rights/reader parity')
    for item in sections['related_resources']:
        need(item['url'] in candidate and item['url'] in copy and html.escape(item['label']) in main_html and html.escape(item['note']) in main_html, 'full actual credited reading links')
    for asset in ready['all_native_assets_in_original_order']:
        name = asset['original_api_file_object']['key']
        body = raw(Path(asset['path']))
        need(body == raw(editorial / 'candidate' / name), 'unchanged original download')
        need(hashlib.md5(body).hexdigest() == asset['original_api_file_object']['checksum'].removeprefix('md5:'), 'native original checksum')
    need(raw(editorial / 'citation.bib') == raw(editorial / 'candidate/citation.bib') == pub['prepared_bibtex'].encode(), 'complete BibTeX parity')
    history = obj(editorial / 'HISTORY.json')
    build = obj(editorial / 'BUILD_RECEIPT.json')
    need(history['checkpoint_pause']['renderer_not_run'] is True and history['checkpoint_pause']['candidate_absent'] is True, 'literal historical checkpoint state')
    need(build['exit_code'] == 0 and build['first_render_is_current_render'] is True and build['rerender_count'] == 0, 'first/current rendering history')
    need(checked_pin(build['whole_stderr']) == b'' and json.loads(checked_pin(build['whole_stdout']))['status'] == 'SOURCE_ONLY_EDITORIAL_RENDERED', 'whole actual authoring streams')
    checked_pin(history['unexecuted_pre_first_render_helper_source'])
    checked_pin(build['helper'])

    own_closed = (HERE / 'FINAL_SEAL.json').exists()
    if own_closed:
        own_seal = obj(HERE / 'FINAL_SEAL.json')
        own_manifest_bytes = raw(HERE / 'FINAL_MANIFEST.json')
        need(digest(own_manifest_bytes) == own_seal['manifest_SHA256'], 'own final manifest binding')
        own_manifest = json.loads(own_manifest_bytes)
        own_extent = extent(HERE)
        own_terminals = ['FINAL_MANIFEST.json', 'FINAL_SEAL.json']
        need(own_manifest['exact_root_terminal_exclusions'] == own_terminals, 'own exact root exclusions')
        need(own_manifest['recursive_basename_exclusions'] is False, 'own no basename hole')
        need(own_extent['directories'] == own_manifest['directories'], 'own closed directories')
        actual_payloads = [x for x in own_extent['files'] if x['path'] not in own_terminals]
        same(actual_payloads, own_manifest['files'], 'own closed whole payloads')
        need([x['path'] for x in own_extent['files']] == sorted([x['path'] for x in own_manifest['files']] + own_terminals), 'own exact finite file namespace')
    print(json.dumps({'status': 'PASS_INFORMED_EDITORIAL_FACT_CUSTODY', 'checks': checks, 'typed_nodes': nodes, 'owner_payloads': len(names), 'owner_actual_files': len(actual['files']), 'owner_directories': len(actual['directories']), 'source_files': source_result['source_files'], 'whole_original_source_JSON_objects': len(initial['whole_root_source_JSON_objects']), 'owner_protocol_dot_JSON_objects': len(original_objects), 'whole_native_API_roles': len(native_api), 'literal_non_200_JSON_bodies': len(ready['raw_non_200_response_bodies']), 'whole_scientific_verdicts': len(verdicts), 'archive_containers': 4, 'archive_occurrences': 243, 'complete_original_abstract_and_distinct_native_description': True, 'own_final_closed_namespace_checked': own_closed, 'native_or_own_science_authoring_project_imports_subprocess_network_or_writes': False}, indent=2))


if __name__ == '__main__':
    main()

