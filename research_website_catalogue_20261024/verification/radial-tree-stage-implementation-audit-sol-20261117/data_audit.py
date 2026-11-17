"""One bounded local-data audit; no project imports, execution, Git or network."""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, urljoin
import copy
import hashlib
import html
import json
import os
import re
import stat
import struct
import traceback

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = P / 'verification/radial-tree-stage-sol-20261117'
C = S / 'candidate/public'
I = P / 'verification/radial-tree-stage-audit-sol-20261117'
O = P / 'verification/radial-tree-stage-implementation-audit-sol-20261117'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
CHECKS, EVIDENCE = [], {}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def check(name, ok, detail=None):
    CHECKS.append({'check': name, 'PASS': bool(ok), 'details': detail})
    need(ok, name)

def pairs(items):
    result = {}
    for key, value in items:
        need(key not in result, 'Duplicate JSON object key: ' + key)
        result[key] = value
    return result

def parse(raw):
    return json.loads(raw, object_pairs_hook=pairs)

def readj(path):
    return parse(path.read_bytes())

def readt(path):
    return path.read_bytes().decode('utf-8')

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def mode(value):
    need(type(value) in (str, int), 'Explicit mode type')
    return format(int(value, 8) if isinstance(value, str) else value, '04o')

def rel(name):
    need(type(name) is str and name and '\\' not in name, 'Relative path string')
    q = Path(name)
    need(not q.is_absolute() and q.as_posix() == name and not ({'.', '..'} & set(q.parts)), 'Canonical relative path')
    return name

def row(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Ordinary regular input: ' + str(path))
    raw = path.read_bytes()
    last = path.lstat()
    need((info.st_dev, info.st_ino, info.st_size, info.st_mode, info.st_mtime_ns, info.st_ctime_ns) == (last.st_dev, last.st_ino, last.st_size, last.st_mode, last.st_mtime_ns, last.st_ctime_ns), 'Stable file read')
    return {'bytes': len(raw), 'SHA256': digest(raw), 'mode': mode(stat.S_IMODE(info.st_mode))}

def file_rows(entries):
    result = {}
    for entry in entries:
        need(set(entry) == {'path', 'bytes', 'SHA256', 'mode'}, 'Complete exact file-row schema')
        name = rel(entry['path'])
        need(name not in result and type(entry['bytes']) is int and entry['bytes'] >= 0, 'Unique file path/integer size')
        need(re.fullmatch('[0-9a-f]{64}', entry['SHA256']) is not None, 'SHA256 encoding')
        result[name] = {'bytes': entry['bytes'], 'SHA256': entry['SHA256'], 'mode': mode(entry['mode'])}
    return result

def dir_rows(entries):
    result = {}
    for entry in entries:
        need(set(entry) == {'path', 'mode'}, 'Exact directory-row schema')
        name = rel(entry['path'])
        need(name not in result, 'Unique directory path')
        result[name] = mode(entry['mode'])
    return result

def normalized(snapshot):
    keys = {'root', 'root_mode', 'files', 'directories'}
    need(set(snapshot) in (keys, keys | {'regular_files', 'child_directories'}), 'Actual snapshot schema')
    need(Path(snapshot['root']).is_absolute(), 'Absolute snapshot root')
    if type(snapshot['files']) is list:
        files, dirs = file_rows(snapshot['files']), dir_rows(snapshot['directories'])
    else:
        need(type(snapshot['files']) is dict and type(snapshot['directories']) is dict, 'Actual mapped inventory')
        files = file_rows([{'path': name, **value} for name, value in snapshot['files'].items()])
        dirs = dir_rows([{'path': name, 'mode': value} for name, value in snapshot['directories'].items()])
    need(not (set(files) & set(dirs)), 'No file/directory path collision')
    if 'regular_files' in snapshot:
        need(type(snapshot['regular_files']) is int and type(snapshot['child_directories']) is int, 'Integer snapshot counts')
        need((len(files), len(dirs)) == (snapshot['regular_files'], snapshot['child_directories']), 'Snapshot counts exact')
    return {'root': snapshot['root'], 'root_mode': mode(snapshot['root_mode']), 'files': files, 'directories': dirs}

def census(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'Ordinary census root')
    files, dirs = [], []
    for parent, childdirs, childfiles in os.walk(root, followlinks=False):
        parent = Path(parent)
        for name in childdirs:
            q = parent / name
            need(stat.S_ISDIR(q.lstat().st_mode), 'No symbolic/special directory')
            dirs.append({'path': q.relative_to(root).as_posix(), 'mode': mode(stat.S_IMODE(q.lstat().st_mode))})
        for name in childfiles:
            q = parent / name
            files.append({'path': q.relative_to(root).as_posix(), **row(q)})
    return normalized({'root': str(root), 'root_mode': mode(stat.S_IMODE(root.lstat().st_mode)), 'files': files, 'directories': dirs, 'regular_files': len(files), 'child_directories': len(dirs)})

def octal_inventory(inv):
    return {'root': inv['root'], 'root_mode': oct(int(inv['root_mode'], 8)), 'files': {k: {**v, 'mode': oct(int(v['mode'], 8))} for k, v in inv['files'].items()}, 'directories': {k: oct(int(v, 8)) for k, v in inv['directories'].items()}}

def native(repo):
    g = repo / '.git'
    local = octal_inventory(census(g / 'refs/heads'))
    packed = [line for line in (g / 'packed-refs').read_text().splitlines() if re.fullmatch(r'[0-9a-f]{40} refs/heads/\S+', line)]
    branches = {line.split(' ', 1)[1]: line.split(' ', 1)[0] for line in packed}
    for name in local['files']:
        branches['refs/heads/' + name] = (g / 'refs/heads' / name).read_text().strip()
    head = (g / 'HEAD').read_text().strip()
    need(head.startswith('ref: refs/heads/'), 'Native attached local head')
    files = {}
    for name in ['HEAD', 'index', 'config']:
        item = row(g / name)
        files[name] = {**item, 'mode': oct(int(item['mode'], 8))}
    return {'files': files, 'HEAD': head, 'resolved_local_HEAD': branches[head[5:]], 'local_heads': local, 'packed_local_head_lines': packed, 'packed_refs_mode': oct(stat.S_IMODE((g / 'packed-refs').lstat().st_mode))}

def section(pattern, raw):
    hits = list(re.finditer(pattern, raw, re.S))
    need(len(hits) == 1, 'Exactly one section: ' + pattern)
    return hits[0]

class Tags(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.tags, self.ids = [], []
        self.feed(raw)
        self.close()
    def handle_starttag(self, tag, attrs):
        need(len(attrs) == len({key for key, value in attrs}), 'No duplicate HTML attribute')
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])

def script(raw):
    hit = section(r'<script type="application/ld\+json">(.*?)</script>', raw)
    return hit, parse(hit.group(1))

def index(raw, number):
    hit = section(r'<h2>Papers</h2>\s*<ul>(.*?)</ul>', raw)
    units = list(re.finditer(r'<li(?:\s[^>]*)?>.*?</li>', hit.group(1), re.S))
    need(re.sub(r'<li(?:\s[^>]*)?>.*?</li>', '', hit.group(1), flags=re.S).strip() == '', 'Only complete visible list units')
    sh, schema = script(raw)
    need(schema['@type'] == 'CollectionPage' and schema['mainEntity']['@type'] == 'ItemList', 'Actual typed ItemList')
    items = schema['mainEntity']['itemListElement']
    need(type(schema['mainEntity']['numberOfItems']) is int and len(items) == len(units) == schema['mainEntity']['numberOfItems'] == number, 'Exact typed/visible integer count')
    need([x['position'] for x in items] == list(range(1, number + 1)) and all(type(x['position']) is int for x in items), 'Ordered integer positions')
    need(len({x['url'] for x in items}) == number, 'No duplicate article URL')
    urls = [urljoin('https://aleckriebel.com', next(attrs['href'] for tag, attrs in Tags(m.group()).tags if tag == 'a')) for m in units]
    need(urls == [x['url'] for x in items], 'Visible/typed URL sequence exact')
    body = sh.group(1)
    start = section(r'"itemListElement"\s*:\s*\[', body).end() - 1
    decoder = json.JSONDecoder(object_pairs_hook=pairs)
    parsed, end = decoder.raw_decode(body, start)
    raw_units, pos = [], start + 1
    for item in parsed:
        while body[pos].isspace() or body[pos] == ',':
            pos += 1
        value, finish = decoder.raw_decode(body, pos)
        need(value == item, 'Raw JSON unit interpretation')
        raw_units.append(body[pos:finish])
        pos = finish
    return {'list': hit, 'HTML': [m.group() for m in units], 'script': sh, 'schema': schema, 'items': items, 'raw_JSON': raw_units, 'close': end - 1}

def xml_value(node):
    return {'tag': node.tag, 'attrib': node.attrib, 'text': node.text, 'tail': node.tail, 'children': [xml_value(c) for c in node]}

def audit():
    initial = census(I)
    need((len(initial['files']), len(initial['directories'])) == (5, 0), 'Frozen INITIAL exact5/0')
    need(row(I / 'INITIAL_SEAL.json')['SHA256'] == 'cad30b746a75ae567fe55e35af18d283f0cff256125698fc89621efde3105910', 'Actual INITIAL seal pin')
    seal, bindings, contract = readj(I / 'INITIAL_SEAL.json'), readj(I / 'INPUT_BINDINGS.json'), readj(I / 'CONTRACT.json')
    for key in ['manifest', 'contract', 'input_bindings', 'log']:
        expected = seal[key]
        need(row(I / expected['path']) == {k: expected[k] for k in ['bytes', 'SHA256', 'mode']}, 'INITIAL payload pin')
    check('C01_C26_INITIAL_independence_and_exact_immutable5', seal['new_producer_file_or_directory_opened'] is False and seal['children_spawned'] is False)
    stage = census(S)
    check('whole_stage804_380', (len(stage['files']), len(stage['directories']), stage['root_mode']) == (804, 380, '0755'))
    for name, size, sha in [('FINAL.json', 72852, '481f6ea4801fd64d722ae5efd62b8bb9269673b6539c2675edb1d815f59a03be'), ('OWNED_MANIFEST.json', 228980, '3b631660dfdba93a8c44bfcfc125225325ee65735c4e42890de2502fa5d3907f'), ('build_private_v2.py', 38992, 'b32021f13319cf13968cc97d1ef525a93a4febe59769b8f53ae14db8c253d8a3')]:
        need(row(S / name) == {'bytes': size, 'SHA256': sha, 'mode': '0644'}, 'Root-pinned producer control: ' + name)
    final, manifest = readj(S / 'FINAL.json'), readj(S / 'OWNED_MANIFEST.json')
    payload = file_rows(manifest['files'])
    need(set(manifest['exact_terminal_exclusions']) == {'FINAL.json', 'OWNED_MANIFEST.json'}, 'Exact terminal exclusions only')
    need(manifest['no_future_or_subtree_exclusions'] is True and manifest['root'] == str(S), 'Finite manifest root/boundary')
    payload.update({name: row(S / name) for name in ['FINAL.json', 'OWNED_MANIFEST.json']})
    check('C04_stage_manifest_every_payload_terminal_mode_topology', stage['files'] == payload and stage['directories'] == dir_rows(manifest['directories']) and stage['root_mode'] == mode(manifest['root_mode']))
    need(final['extent']['all_paths'] == sorted(stage['files']), 'FINAL full finite path list')
    for key in ['manifest', 'receipt', 'candidate_manifest']:
        expected = final[key]
        need(row(S / expected['path']) == {k: (mode(expected[k]) if k == 'mode' else expected[k]) for k in ['bytes', 'SHA256', 'mode']}, 'FINAL nested whole pin')
    before, after = readj(S / 'GUARDS_BEFORE_V2.json'), readj(S / 'GUARDS_AFTER_V2.json')
    check('captured_before_after_whole_guards_equal', before == after and (S / 'GUARDS_BEFORE_V2.json').read_bytes() == (S / 'GUARDS_AFTER_V2.json').read_bytes())
    need(set(before) == {'inputs', 'native_controls', 'public', 'retained_first_attempt'}, 'Actual guard schema')
    frozen, sources = {}, {}
    for family, key, target in [('private_inputs', 'private_packets', frozen), ('source_inputs', 'native_sources', sources)]:
        for packet in bindings[family]:
            expected = normalized(packet['snapshot'])
            current = census(Path(expected['root']))
            need(current == expected == normalized(before['inputs'][key][expected['root']]), 'Whole immutable namespace and initial/source guards: ' + expected['root'])
            target[expected['root']] = current
    check('C02_C03_private186_16_sources233_37_complete_unchanged', (sum(len(x['files']) for x in frozen.values()), sum(len(x['directories']) for x in frozen.values()), sum(len(x['files']) for x in sources.values()), sum(len(x['directories']) for x in sources.values())) == (186, 16, 233, 37))
    source_json = []
    for source in bindings['source_inputs']:
        root = Path(source['snapshot']['root'])
        for name in ['SOURCE_FINAL.json', 'SOURCE_MANIFEST.json', 'record.response.body', 'files-' + str(source['record']) + '.response.body']:
            need((root / name).is_file(), 'Controlling source JSON exists')
            readj(root / name)
            source_json.append(str(root / name))
    check('C16_controlling_native_source_JSON_duplicate_keys_rejected', len(source_json) == 8)
    for name, expected in before['inputs']['root_pins'].items():
        need(row(Path(name)) == {k: (mode(expected[k]) if k == 'mode' else expected[k]) for k in ['bytes', 'SHA256', 'mode']}, 'Actual root adoption/clearance pin')
    public, candidate = census(W / 'public'), census(C)
    need(public == normalized(before['public']), 'Whole current W public equals captured guard')
    need(candidate == normalized(readj(S / 'CANDIDATE_MANIFEST.json')), 'Whole current candidate equals validated manifest')
    check('C06_C07_complete_normalized_namespaces772_373_to781_377', (len(public['files']), len(public['directories']), public['root_mode'], len(candidate['files']), len(candidate['directories']), candidate['root_mode']) == (772, 373, '0750', 781, 377, '0750'))
    current_native = {'M': native(P.parent), 'W': native(W)}
    check('C08_whole_current_M_W_native_controls_unchanged', current_native == before['native_controls'])
    need(current_native['M']['resolved_local_HEAD'] == 'a4ce3c37dad209339e490d18dcced6c48cf912d2' and current_native['M']['files']['index']['SHA256'] == '91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11', 'Actual native Math checkpoint, not remote')
    raw_index = (W / '.git/index').read_bytes()
    need(len(raw_index) == 9057886 and digest(raw_index) == 'e6285d49b7249ae2c88a1f624ca98c1dcf480424db272c4fe111ca91dbdafb5e' and struct.unpack('>4sII', raw_index[:12]) == (b'DIRC', 2, 58712) and hashlib.sha1(raw_index[:-20]).digest() == raw_index[-20:], 'Whole checksum-valid exact W index')
    need(current_native['W']['resolved_local_HEAD'] == '96f04aa5544df69daba07a9ed4d6212172e9984a', 'Actual W master')
    targets = readj(S / 'TARGETS.json')
    check('C05_actual_public_relative_plan_exact_Git_projection', {'public/' + rel(x) for x in targets['A'] + targets['M']} == set(contract['expected_exact_projection']['paths']) and (len(targets['A']), len(targets['M']), len(set(targets['A'] + targets['M'])), targets['production_target_count'], targets['D']) == (9, 2, 11, 11, []))
    need(set(targets['new_directories']) == set(contract['expected_exact_projection']['new_directories']) and len(targets['new_directories']) == 4, 'Exact unique four-directory projection')
    need(final['target_plan'] == targets and targets['row_order'] == [184, 185], 'Exact final target plan/order')
    added = set(candidate['files']) - set(public['files'])
    modified = {name for name in public['files'] if candidate['files'].get(name) != public['files'][name]}
    check('all770_untargeted_files373_dir_modes17_DSStore_exact', added == set(targets['A']) and modified == set(targets['M']) and set(candidate['files']) == set(public['files']) | added and all(candidate['directories'].get(k) == v for k, v in public['directories'].items()) and set(candidate['directories']) - set(public['directories']) == set(targets['new_directories']) and sum(Path(x).name == '.DS_Store' for x in candidate['files']) == sum(Path(x).name == '.DS_Store' for x in public['files']) == 17)
    need(all(candidate['files'][x]['mode'] == '0644' for x in targets['A']) and all(candidate['directories'][x] == '0755' for x in targets['new_directories']), 'Exact new modes')
    pre = readj(S / 'PRE_V2_WORKBENCH.json')
    bench = normalized(pre['inventory'])
    need(len(pre['all9_new_leaves_absent']) == len(set(pre['all9_new_leaves_absent'])) == 9 and len(pre['all4_new_directories_absent']) == len(set(pre['all4_new_directories_absent'])) == 4, 'Unique exact historical absence rows')
    check('pre_v2_retained_baseline_and_exact9leaf4dir_absence_proof', all(bench[k] == public[k] for k in ['root_mode', 'files', 'directories']) and set(pre['all9_new_leaves_absent']) == set(targets['A']) and set(pre['all4_new_directories_absent']) == set(targets['new_directories']) and pre['exact772files373dirs_baseline_authenticated'] is True)
    failure, receipt = readj(S / 'FAILURE_1.json'), readj(S / 'BUILD_RECEIPT.json')
    need(len(receipt['pages']) == 2 and [x['record'] for x in receipt['pages']] == [22983519, 23527793], 'Exactly two receipt pages in native row order')
    for name, expected in receipt['first_attempt_evidence'].items():
        need(row(S / name) == {k: (mode(expected[k]) if k == 'mode' else expected[k]) for k in ['bytes', 'SHA256', 'mode']}, 'All retained first-attempt evidence exact')
    check('literal_build1_0_failure_and_zero_streams_retained', failure['exit'] == receipt['first_attempt_exit'] == 1 and receipt['private_build_attempts'] == 2 and receipt['v2_build_attempts'] == 1 and failure['first_builder_rerun'] is False and len((S / 'BUILD.stderr.txt').read_bytes()) == 1028 and 'ValueError: Accepted whole head differs' in (S / 'BUILD.stderr.txt').read_text() and all((S / name).read_bytes() == b'' for name in ['BUILD.stdout.txt', 'BUILD_V2.stdout.txt', 'BUILD_V2.stderr.txt']))
    page_evidence = []
    for accepted, returned in zip(bindings['writer_specific_bindings'], receipt['pages']):
        recid, canonical, slug = accepted['record'], accepted['canonical'], accepted['slug']
        writer = Path(accepted['article']['path']).parent
        old, new = readt(writer / 'article.html'), readt(C / 'research' / slug / 'index.html')
        old_tags = Tags(old)
        need(len(old_tags.ids) == len(set(old_tags.ids)), 'Original accepted HTML identifiers unique')
        model = readj(writer / 'page-model.json')
        need(returned['model'] == model and returned['record'] == recid, 'Receipt actual accepted model')
        oh, nh = section(r'<head>.*?</head>', old), section(r'<head>.*?</head>', new)
        need(old[:oh.start()] == new[:nh.start()] and old[oh.end():] == new[nh.end():], 'Whole document outside activated HEAD byte-exact')
        need(section(r'<main id="main">.*?</main>\n', new).group().encode() == Path(accepted['MAIN']['path']).read_bytes(), 'Entire accepted MAIN exact')
        osh, oschema = script(oh.group())
        nsh, nschema = script(nh.group())
        if recid == 22983519:
            need(new == old.replace('<meta name="robots" content="noindex, nofollow">\n', '', 1) and oschema == nschema, 'Radial only private robots removal')
            need([x['@type'] for x in nschema['@graph']] == ['WebPage', 'ScholarlyArticle'], 'Radial actual graph order')
            scholarly = nschema['@graph'][1]
        else:
            expected_schema = copy.deepcopy(oschema)
            expected_schema.update({'@id': canonical + '#article', 'url': canonical, 'mainEntityOfPage': canonical})
            for asset, item in zip(model['native_asset_order'], expected_schema['encoding']):
                item['contentUrl'] = canonical + asset['local_path']
            need(nschema == expected_schema, 'Tree complete typed schema differs only by authorized URLs')
            outside = oh.group()[:osh.start(1)] + '<JSON>' + oh.group()[osh.end(1):]
            for name in ['robots', 'googlebot']:
                outside = outside.replace('<meta name="' + name + '" content="noindex, nofollow">\n', '', 1)
            outside = outside.replace('content="assets/congestion-fragmentation.pdf"', 'content="' + canonical + 'assets/congestion-fragmentation.pdf"', 1)
            outside = outside.replace('<link rel="stylesheet" href="research.css">', '<link rel="canonical" href="' + canonical + '">\n<link rel="stylesheet" href="/research/research.css">\n<meta property="og:url" content="' + canonical + '">', 1)
            need(outside == nh.group()[:nsh.start(1)] + '<JSON>' + nh.group()[nsh.end(1):], 'Tree all non-JSON head bytes authorized only')
            scholarly = nschema
        tags = Tags(new)
        need(len(tags.ids) == len(set(tags.ids)), 'Unique HTML ids')
        metadata = [(a.get('name', a.get('property')).lower(), a['content']) for tag, a in tags.tags if tag == 'meta' and ('name' in a or 'property' in a)]
        need(len(metadata) == len({k for k, v in metadata}), 'Unique metadata identity')
        metadata = dict(metadata)
        need(not ({'robots', 'googlebot'} & set(metadata)), 'No private crawler gate remains')
        need([a['href'] for tag, a in tags.tags if tag == 'link' and a.get('rel') == 'canonical'] == [canonical], 'Exactly one activated canonical')
        need([a['href'] for tag, a in tags.tags if tag == 'link' and a.get('rel') == 'stylesheet'] == ['/research/research.css'], 'Existing shared stylesheet only')
        need(scholarly['url'] == scholarly['mainEntityOfPage'] == metadata['og:url'] == canonical, 'All activated scholarly identity URLs')
        need(scholarly['abstract'] == model['abstract'] and scholarly['datePublished'] == model['publication_date'] and scholarly['version'] == model['native_version'], 'Accepted full abstract/date/version')
        abstract_id = 'original-abstract' if recid == 22983519 else 'abstract-text'
        visible = section(r'<p id="' + abstract_id + r'">(.*?)</p>', new).group(1)
        need(html.unescape(visible) == model['abstract'], 'Whole visible abstract exact')
        if recid == 23527793:
            need(metadata['dc.description'] == model['abstract'], 'Tree complete DC abstract exact')
        need([x['contentUrl'] for x in scholarly['encoding']] == [canonical + a['local_path'] for a in model['native_asset_order']], 'Native all3/all2 encoding order')
        pdf = next(a['local_path'] for a in model['native_asset_order'] if a['format'] == 'application/pdf')
        need(metadata['citation_pdf_url'] == canonical + pdf, 'Exact absolute citation PDF URL')
        for asset in model['native_asset_order']:
            raw = (C / 'research' / slug / asset['local_path']).read_bytes()
            need(raw == (writer / asset['local_path']).read_bytes() == (P / 'papers' / str(recid) / 'sources/assets' / asset['name']).read_bytes(), 'All native asset buffers identical')
            need(len(raw) == asset['bytes'] and digest(raw) == asset['SHA256'] and 'md5:' + hashlib.md5(raw).hexdigest() == asset['native_checksum'], 'Native size/SHA256/MD5')
        need((C / 'research' / slug / 'citation.bib').read_bytes() == (writer / 'citation.bib').read_bytes(), 'Whole original Bib exact')
        for tag, attrs in tags.tags:
            for ident in attrs.get('aria-labelledby', '').split():
                need(ident in tags.ids, 'ARIA target exists')
            for key in ['href', 'src']:
                if key not in attrs:
                    continue
                u = urlsplit(attrs[key])
                if (u.scheme and u.scheme != 'https') or (u.netloc and u.netloc != 'aleckriebel.com'):
                    continue
                if u.path:
                    target = C / unquote(u.path.lstrip('/')) if u.path.startswith('/') else C / 'research' / slug / unquote(u.path)
                    need(target.resolve().is_relative_to(C.resolve()), 'No escaping internal URL')
                    need((target / 'index.html').is_file() if target.is_dir() else target.is_file(), 'Every internal target exists')
                elif u.fragment:
                    need(u.fragment in tags.ids, 'Local fragment exists')
        page_evidence.append({'record': recid, 'activated': row(C / 'research' / slug / 'index.html'), 'whole_MAIN': row(Path(accepted['MAIN']['path'])), 'schema_and_head_changes_whitelisted': True, 'body_assets_Bib_abstract_rights_AI_collaboration_unchanged': True})
    check('C09_to_C16_C21_both_actual_page_heads_bodies_assets_Bibs_links', len(page_evidence) == 2, page_evidence)
    old_index = readt(S / 'originals/research-index.html')
    new_index = readt(C / 'research/index.html')
    Tags(old_index)
    Tags(new_index)
    need(old_index.encode() == (W / 'public/research/index.html').read_bytes(), 'Complete original/current index')
    old, new = index(old_index, 126), index(new_index, 128)
    expected_new = [{'@type': 'ListItem', 'position': 127 + i, 'url': x['canonical'], 'name': readj(Path(x['model']['path']))['title']} for i, x in enumerate(bindings['writer_specific_bindings'])]
    need(new['HTML'][:126] == old['HTML'] and new['raw_JSON'][:126] == old['raw_JSON'] and new['items'][:126] == old['items'] and new['items'][126:] == expected_new, 'All old126 raw/typed/visible prefix, exact two append rows')
    ol, nl = old['list'], new['list']
    need(nl.group(1).startswith(ol.group(1)), 'Entire visible list body is an exact prefix')
    appended_html = nl.group(1)[len(ol.group(1)):]
    without_visible = new_index[:nl.start(1)] + ol.group(1) + new_index[nl.end(1):]
    oscript, nscript = old['script'].group(1), new['script'].group(1)
    restored_script = nscript[:old['close']] + nscript[new['close']:]
    restored_script, changes = re.subn(r'("numberOfItems"\s*:\s*)128(?!\d)', r'\g<1>126', restored_script)
    need(changes == 1 and restored_script == oscript, 'Complete raw JSON reversal')
    fresh_hit = script(without_visible)[0]
    restored_index = without_visible[:fresh_hit.start(1)] + restored_script + without_visible[fresh_hit.end(1):]
    check('C17_C18_C19_all126_prefixes_and_whole_index_reversal', restored_index.encode() == old_index.encode())
    aggregate = readj(S / 'AGGREGATE_PRESERVATION.json')
    need(aggregate['index']['old_raw_HTML_units'] == old['HTML'] and aggregate['index']['old_raw_JSON_units'] == old['raw_JSON'] and aggregate['index']['old_typed'] == old['items'] and aggregate['index']['new_items'] == expected_new and aggregate['index']['appended_HTML'] == appended_html, 'Actual full index evidence agrees independent extraction')
    old_xml, new_xml = (S / 'originals/research-sitemap.xml').read_bytes(), (C / 'research/sitemap.xml').read_bytes()
    need(old_xml == (W / 'public/research/sitemap.xml').read_bytes(), 'Whole original/current XML')
    import xml.etree.ElementTree as ET
    ot, nt = ET.fromstring(old_xml), ET.fromstring(new_xml)
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    oraw, nraw = list(re.finditer(rb'<url>.*?</url>', old_xml, re.S)), list(re.finditer(rb'<url>.*?</url>', new_xml, re.S))
    need(ot.tag == nt.tag == ns + 'urlset' and len(ot) == len(oraw) == 127 and len(nt) == len(nraw) == 129, 'Actual namespace-aware sitemap counts')
    need([x.group() for x in nraw[:127]] == [x.group() for x in oraw] and [xml_value(x) for x in list(nt)[:127]] == [xml_value(x) for x in ot], 'All127 complete raw/parsed XML prefix')
    locs = [x.find(ns + 'loc').text for x in nt]
    need(len(locs) == len(set(locs)) == 129 and locs[127:] == [x['canonical'] for x in bindings['writer_specific_bindings']], 'Exact unique two new canonical XML locs')
    close = new_xml.index(b'</urlset>')
    restored_xml = new_xml[:nraw[127].start()] + new_xml[close:]
    check('C20_all127_raw_parsed_prefix_and_whole_XML_reversal', restored_xml == old_xml)
    first = readj(S / 'GUARDS_BEFORE.json')
    check('first_and_v2_common_input_native_public_guards_exact', all(first[k] == before[k] for k in ['inputs', 'native_controls', 'public']))
    EVIDENCE.update({'INITIAL': initial, 'stage804': stage, 'candidate781': candidate, 'current_public772': public, 'private186': frozen, 'source233': sources, 'native_controls': current_native, 'pages': page_evidence, 'target_plan_namespace': 'Paths relative to candidate/public; prefix public/ exactly once for Git-relative projection.', 'target_plan': targets, 'literal_build_history': [1, 0], 'first_failure': failure, 'pre_v2_workbench_pin': row(S / 'PRE_V2_WORKBENCH.json'), 'aggregate_reversal': {'old126_raw_HTML': old['HTML'], 'old126_raw_JSON': old['raw_JSON'], 'old126_typed': old['items'], 'new_two_items': expected_new, 'old_index_SHA256': digest(old_index.encode()), 'restored_index_SHA256': digest(restored_index.encode()), 'old_XML_SHA256': digest(old_xml), 'restored_XML_SHA256': digest(restored_xml)}})
    check('complete_protected_namespaces_still_exact_after_own_data_read', census(S) == stage and census(C) == candidate and census(W / 'public') == public and census(I) == initial and native(P.parent) == current_native['M'] and native(W) == current_native['W'] and all(census(Path(root)) == value for root, value in {**frozen, **sources}.items()))

try:
    audit()
    result = {'schema': 'independent-radial-tree-stage-data-result-v1', 'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'PASS', 'checks': CHECKS, 'failed_checks': 0, 'evidence': EVIDENCE, 'own_data_auditor_invocations': 1, 'producer_source_program_Git_network_execution': False, 'production_authority': False, 'new_scientific_copy_or_live_certificate': False}
    print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as error:
    print(json.dumps({'schema': 'independent-radial-tree-stage-data-result-v1', 'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'CORRECTIONS_REQUIRED', 'error': repr(error), 'traceback': traceback.format_exc(), 'checks': CHECKS, 'evidence': EVIDENCE, 'own_data_auditor_invocations': 1, 'automatic_retry': False, 'production_authority': False}, indent=2, ensure_ascii=False))
    raise
