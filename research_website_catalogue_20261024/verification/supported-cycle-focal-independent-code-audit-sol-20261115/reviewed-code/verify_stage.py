"""Pure owned source custody. No project imports, original/live reads, network, subprocess or writes."""
from pathlib import Path
import hashlib
import json
import os
import re
import struct
import xml.etree.ElementTree as ET
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


def parse_index(raw, targets):
    need(raw[:4] == b'DIRC' and len(raw) >= 32, 'whole native index')
    version, count = struct.unpack('>II', raw[4:12])
    need(version == 2 and hashlib.sha1(raw[:-20]).digest() == raw[-20:], 'native v2 and checksum')
    offset = 12; entries = []; protected = []
    for _ in range(count):
        start = offset
        need(offset + 62 < len(raw) - 20, 'whole native header')
        flags = struct.unpack('>H', raw[offset + 60:offset + 62])[0]
        end = raw.find(b'\0', offset + 62, len(raw) - 20)
        need(end >= 0 and flags & 0xF000 == 0, 'stage0 ordinary native flags')
        path = raw[offset + 62:end]
        offset = start + ((end + 1 - start + 7) // 8) * 8
        need(path and flags & 0xFFF == min(len(path), 0xFFF)
             and raw[end:offset] == b'\0' * (offset - end), 'native path/padding')
        mode = struct.unpack('>I', raw[start + 24:start + 28])[0]
        oid = raw[start + 40:start + 60].hex()
        need(mode in [0o100644, 0o100755, 0o120000, 0o160000], 'native mode')
        record = raw[start:offset]; entries.append((path, record, mode, oid))
        if path not in targets:
            protected.append((path, record))
    paths = [e[0] for e in entries]
    need(paths == sorted(set(paths)), 'complete unique native path order')
    extensions = []
    while offset < len(raw) - 20:
        need(offset + 8 <= len(raw) - 20, 'whole extension header')
        key = raw[offset:offset + 4]; length = struct.unpack('>I', raw[offset + 4:offset + 8])[0]; offset += 8
        need(key == b'TREE' and offset + length <= len(raw) - 20, 'only supported TREE extension')
        extensions.append({'name': 'TREE', 'bytes': length, 'SHA256': sha(raw[offset:offset + length])}); offset += length
    need(offset == len(raw) - 20 and len(extensions) <= 1, 'whole native extension extent')
    records = b'\0'.join(path + b'\t' + record.hex().encode() for path, record in protected) + b'\0'
    return entries, {'version': version, 'records': count, 'protected_records': len(protected),
                     'protected_native_raw_records_SHA256': sha(records), 'extensions': extensions}



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


def closed_namespace(root, files, directories, terminals=()):
    actual_files, actual_dirs = extent(root)
    need(len(files) == len(set(files)) and actual_files == sorted(set(files) | set(terminals)),
         'exact ordinary files and exact root terminals only')
    need(directories == sorted(set(directories)) and actual_dirs == directories,
         'exact declared directories including legitimate empty inputs')
    return actual_files, actual_dirs


def baseline_fences():
    seal = obj(O / 'BASELINE_CACHE_SEAL.json')
    body = read(O / 'WEBSITE_BASELINE.json')
    need(sha(body) == seal['WEBSITE_BASELINE_SHA256'], 'whole fresh623 baseline cache seal')
    need(sha(read(O / 'ACTUAL_BASELINE_GO.json')) == seal['root_GO_SHA256'] ==
         '0d7371f227e608c79d7f79135cb78cecd2fee4e190c7952bebb3afa7c0c639c2', 'actual separate root GO')
    baseline = json.loads(body)
    go = obj(O / 'ACTUAL_BASELINE_GO.json')
    need(baseline['Git']['HEAD'] == baseline['Git']['master'] == go['actualWebsiteHEAD']
         and baseline['Git']['tree'] == go['actualWebsiteTree']
         and baseline['Git']['index_SHA256'] == go['actualIndexSHA256']
         and baseline['Git']['actual_remote_advertisement'].split() == [go['actualWebsiteHEAD'], 'refs/heads/master'],
         'actual root623 HEAD/master/tree/index/remote identities')
    closed_namespace(O / 'baseline-blobs', seal['exact_baseline_blob_names'], seal['baseline_blob_directories'])
    for row in baseline['files']:
        pin(O / row['blob'], row)
    need(baseline['baseline_counts'] == [623,94,95] and baseline['proposed_counts'] == [631,96,97]
         and len(baseline['public_namespace']) == 623 and baseline['unrelated_public_paths'] == 621,
         'actual623 interface, never614 as623')
    raw = read(O / baseline['full_raw_index'])
    need(sha(raw) == baseline['Git']['index_SHA256'] == seal['raw_index_SHA256'], 'whole captured native index')
    requirements = obj(O / 'ADAPTER_REQUIREMENTS.json')
    targets = {('public/' + name).encode() for name in requirements['eight_article_root_leaves'] + requirements['only_aggregate_paths']}
    entries, native = parse_index(raw, targets)
    same(native, baseline['native_index'])
    need(native['records'] == 58563 and native['protected_records'] == 58561, 'fresh actual native record counts')
    for receipt in baseline['actual_readonly_Git_receipts']:
        for stream in ['stdout', 'stderr']:
            body = read(O / receipt[stream])
            need(len(body) == receipt[stream + '_bytes'] and sha(body) == receipt[stream + '_SHA256'], 'whole literal Git transport stream')
        need(receipt['exit'] == 0, 'actual read-only Git exit')
    return baseline


def index_card(publication):
    import html
    e = html.escape
    prefix = '/research/' + publication['slug'] + '/'
    return ('      <li><a href="' + prefix + '">' + e(publication['title']) + '</a><br><span class="entry-meta">'
            + e(publication['publication_date_label']) + ' · ' + e(publication['status']) + '</span><p>'
            + e(publication['description']) + '</p><p><a href="' + prefix + publication['pdf_filename']
            + '">PDF</a> · <a href="https://doi.org/' + publication['doi'] + '">Zenodo</a></p></li>\n').encode()


def output_fences(inputs, baseline):
    rows = {r['path']:r for r in inputs['files']}
    def cached(path):
        return pin(O / rows[str(path)]['blob'], rows[str(path)])
    publications = [json.loads(cached(P / 'papers' / r['record_id'] / 'reviews/editorial/publication.json')) for r in inputs['records']]
    paths = sorted(obj(O / 'ADAPTER_REQUIREMENTS.json')['eight_article_root_leaves'] + ['research/index.html','research/sitemap.xml'])
    directories = sorted({'research'} | {'research/' + p['slug'] for p in publications})
    for candidate in ['candidate-a','candidate-b']:
        root = O / candidate / 'public'
        closed_namespace(root, paths, directories)
        for publication, item in zip(publications, inputs['records']):
            editorial = P / 'papers' / item['record_id'] / 'reviews/editorial'
            prefix = root / 'research' / publication['slug']
            main = cached(editorial / 'PUBLIC_MAIN.html'); page = read(prefix / 'index.html')
            need(page.count(main) == 1 and page.count(b'<main ') == 1, 'entire approved MAIN exact; zero transforms')
            need(b'noindex' not in page and publication['proposed_canonical_url'].encode() in page,
                 'proposed public metadata only; no actual canonical AA transition')
            graph = json.loads(re.findall(rb'<script type="application/ld\+json">(.*?)</script>',page,re.S)[0])
            original = json.loads(cached(editorial / 'SCHOLARLY_METADATA.json'))
            need(graph.pop('mainEntityOfPage') == {'@type':'WebPage','@id':publication['proposed_canonical_url']}, 'future page identity')
            need(graph['url'] == publication['proposed_canonical_url'], 'approved slug only')
            graph['url'] = original['url']; same(graph, original)
            need(read(prefix / 'citation.bib') == cached(editorial / 'citation.bib'), 'whole original Bib')
            for asset in publication['native_assets_in_original_order']:
                need(read(prefix / asset['original_api_file_object']['key']) == cached(Path(asset['path'])), 'whole original native asset')
        old_index_row = next(r for r in baseline['files'] if r['path'].endswith('/public/research/index.html'))
        old_index = pin(O / old_index_row['blob'], old_index_row)
        new_index = read(root / 'research/index.html')
        pattern = rb'<script type="application/ld\+json">\s*(.*?)\s*</script>'
        old_graph_raw = re.findall(pattern,old_index,re.S)[0]; new_graph_raw = re.findall(pattern,new_index,re.S)[0]
        old_graph = json.loads(old_graph_raw); new_graph = json.loads(new_graph_raw)
        old_list = old_graph['mainEntity']; new_list = new_graph['mainEntity']
        need(new_list['numberOfItems'] == len(new_list['itemListElement']) == 96, 'actual candidate96 graph')
        same(new_list['itemListElement'][:94],old_list['itemListElement'])
        same(new_list['itemListElement'][94:], [{'@type':'ListItem','position':95+i,'url':p['proposed_canonical_url'],'name':p['title']} for i,p in enumerate(publications)])
        restored = new_index.replace(new_graph_raw,old_graph_raw,1)
        for publication in publications:
            card = index_card(publication); need(restored.count(card) == 1, 'one exact new public card')
            restored = restored.replace(card,b'',1)
        need(restored == old_index, 'whole old index bytes outside new graph/cards unchanged')
        old_xml_row = next(r for r in baseline['files'] if r['path'].endswith('/public/research/sitemap.xml'))
        old_xml = pin(O / old_xml_row['blob'],old_xml_row); new_xml = read(root / 'research/sitemap.xml')
        old_tree = ET.fromstring(old_xml); new_tree = ET.fromstring(new_xml)
        need(len(old_tree) == 95 and len(new_tree) == 97, 'actual candidate97 sitemap')
        for old,new in zip(old_tree,list(new_tree)[:95]):
            need(not (old.tail or '').strip() and not (new.tail or '').strip()
                 and ET.tostring(old).rstrip() == ET.tostring(new).rstrip(),
                 'all original95 sitemap URL contents unchanged; only sibling whitespace tails differ')
        restored_xml = new_xml
        for publication in publications:
            line = ('  <url><loc>' + publication['proposed_canonical_url'] + '</loc><lastmod>2026-11-15</lastmod></url>\n').encode()
            need(restored_xml.count(line) == 1, 'one exact new sitemap entry'); restored_xml = restored_xml.replace(line,b'',1)
        need(restored_xml == old_xml, 'whole old sitemap bytes unchanged')
    for name in paths:
        need(read(O / 'candidate-a/public' / name) == read(O / 'candidate-b/public' / name), 'whole normal optimized ten-buffer equality')
    need(len(set(baseline['public_namespace']) | set(paths)) == 631, 'virtual public union631')
    return paths


def main():
    need(sys.argv[1:] in [[], ['--preseal']], 'bounded pure custody options')
    inputs = source_fences()
    baseline = baseline_fences() if (O / 'WEBSITE_BASELINE.json').exists() else None
    paths = output_fences(inputs,baseline) if baseline and (O / 'candidate-a').exists() and (O / 'candidate-b').exists() else None
    if (O / 'OWNED_MANIFEST.json').exists():
        need(paths is not None, 'FINAL or preseal requires complete paired exact10 outputs')
        need(obj(O / 'POST_AUTHORING_GUARD.json')['status'] ==
             'PASS_ALL_ACTUAL_SOURCE_WEBSITE_CONFIG_CORE_RAW_INDEX_HEAD_MASTER_REMOTE_UNCHANGED',
             'actual final live read-only guard receipt required')
        need(obj(O / 'NAMESPACE_CONTROLS.stdout.json')['status'] == 'PASS_NEW_FINITE_NAMESPACE_CONTROLS',
             'actual new bounded namespace controls required')
        for row in obj(O / 'CURRENT_CODE_MANIFEST.json')['files']:
            pin(O / row['path'], row)
        manifest_body = read(O / 'OWNED_MANIFEST.json'); manifest = json.loads(manifest_body)
        terminals = {'OWNED_MANIFEST.json'} if sys.argv[1:] == ['--preseal'] else {'OWNED_MANIFEST.json','FINAL_SEAL.json'}
        closed_namespace(O,list(manifest['payloads']),manifest['directories'],terminals)
        for name,row in manifest['payloads'].items(): pin(O / name,row)
        if sys.argv[1:] != ['--preseal']:
            seal = obj(O / 'FINAL_SEAL.json')
            need(sha(manifest_body) == seal['manifest']['SHA256'], 'final immutable owner manifest')
    print(json.dumps({'status': 'PASS_PRIVATE_EXACT10_STAGE_CUSTODY' if paths else 'PASS_PARTIAL_SOURCE_CUSTODY',
                      'checks':CHECKS,'whole_typed_nodes':TYPED_NODES,'whole_literal_wrappers':WRAPPERS,
                      'source_input_files':819,'initial_source_blobs':578,'actual_held_baseline':[623,94,95] if baseline else None,
                      'proposed_counts':[631,96,97] if paths else None,'paired_output_buffers':len(paths) if paths else None,
                      'whole_approved_MAIN_transforms':0,'fresh_protected_native_records':58561 if baseline else None,
                      'network_subprocess_project_imports_source_science_live_reads_or_writes':False,
                      'production_authority':False,'canonical_url':None,'AA':None,'follow_up':None},sort_keys=True))

if __name__ == '__main__':
    main()
