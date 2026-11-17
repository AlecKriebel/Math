"""One private, data-only website stage. No subprocesses, network or project imports."""
import copy
import hashlib
import html
import json
import os
import re
import shutil
import stat
import struct
import xml.etree.ElementTree as ET
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M = P.parent
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
OWN = P / 'verification/radial-tree-stage-sol-20261117'
PUBLIC = W / 'public'
CANDIDATE = OWN / 'candidate/public'
ORIGIN = 'https://aleckriebel.com'
ADOPTIONS = [
    ('root-radial-editorial-adoption-20261117.json', 5975, '6534222701fac84e060d60b84bf54112165aa796c17af7d0bf548ef23114ca3b'),
    ('root-designed-tree-editorial-adoption-20261117.json', 15476, '76547b8593fe8bc8df5e8c0224421072fac75b464c3704eb733c7b5f3b3687f1')]
ROWS = [
    (184, 22983519, 'radial-statistical-editorial-sol-20261117', 'radial-orthogonality-dual-conformal-flatness', 'main.html'),
    (185, 23527793, 'designed-tree-editorial-sol-20261117', 'designed-tree-congestion-fragmentation', 'public-main.html')]
SOURCE_PINS = [
    (22983519, 826, '7449712c5c396fde640b7497b20f97fb174593071fce71ca80ff763a23df4954', 17481, 'e05b1df4559bac1a55fac1cfbda2a6aa6428d675e0ce7fbf708766037d425ace', 71, 14),
    (23527793, 828, 'cc7d41efdfdb532269c7579192ff839893c1a6f5a719bcc6b2eb24673102486a', 44620, '5a28bd01fb98dd9d08f746fc4bef54bb19744a1c190db03c0ffb795630ee6d84', 162, 23)]

def need(ok, message):
    if not ok:
        raise ValueError(message)

def now():
    return datetime.now(timezone.utc).isoformat()

def mode(value):
    return int(value, 8) if isinstance(value, str) else value

def data(path):
    return path.read_bytes()

def text(path):
    return data(path).decode('utf-8')

def readj(path):
    return json.loads(text(path))

def record(path):
    st = path.lstat()
    need(stat.S_ISREG(st.st_mode), 'Nonregular input: ' + str(path))
    body = data(path)
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(), 'mode': oct(stat.S_IMODE(st.st_mode))}

def pin(path, size, digest, expected_mode=0o644):
    got = record(path)
    need((got['bytes'], got['SHA256'], mode(got['mode'])) == (size, digest, mode(expected_mode)), 'Pin differs: ' + str(path))
    return got

def inventory(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'Non-directory root: ' + str(root))
    files, dirs = {}, {}
    for path in sorted(root.rglob('*'), key=lambda item: item.relative_to(root).as_posix()):
        name = path.relative_to(root).as_posix()
        need(name not in files and name not in dirs, 'Duplicate inventory name')
        st = path.lstat()
        if stat.S_ISDIR(st.st_mode):
            dirs[name] = oct(stat.S_IMODE(st.st_mode))
        else:
            files[name] = record(path)
    return {'root': str(root), 'root_mode': oct(stat.S_IMODE(root.lstat().st_mode)), 'files': files, 'directories': dirs}

def put(rel, body):
    target = OWN / rel
    need(not Path(rel).is_absolute() and '..' not in Path(rel).parts, 'Unsafe owned path')
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as handle:
        handle.write(body)
    os.chmod(target, 0o644)

def putj(rel, value):
    put(rel, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())

def manifest_auth(root, manifest, terminal_names, expected_mode=0o755, exact_files=None, exact_dirs=None):
    inv = inventory(root)
    need(mode(inv['root_mode']) == mode(manifest.get('root_mode', expected_mode)), 'Root mode differs')
    if 'root' in manifest:
        need(manifest['root'] == str(root), 'Manifest root differs')
    exclusions = manifest.get('exact_terminal_exclusions', manifest.get('exact_terminal_names', manifest.get('terminal_files_excluded')))
    need(exclusions is not None and set(exclusions) == set(terminal_names), 'Manifest terminal boundary differs')
    entries = manifest.get('payload_files', manifest.get('files'))
    need(isinstance(entries, list), 'Manifest entries absent')
    names = [entry['path'] for entry in entries]
    need(len(names) == len(set(names)), 'Duplicate manifest entry')
    need(set(inv['files']) == set(names) | set(terminal_names), 'Manifest file namespace differs')
    for entry in entries:
        actual = inv['files'][entry['path']]
        for key in ['bytes', 'SHA256']:
            need(actual[key] == entry[key], 'Manifest content differs: ' + entry['path'])
        if 'mode' in entry:
            need(mode(actual['mode']) == mode(entry['mode']), 'Manifest mode differs')
    if 'directories' in manifest:
        expected = {entry['path']: mode(entry['mode']) for entry in manifest['directories']}
        need(len(expected) == len(manifest['directories']), 'Duplicate manifest directory')
        need({key: mode(value) for key, value in inv['directories'].items()} == expected, 'Manifest directories differ')
    else:
        need(exact_dirs is not None, 'No directory boundary supplied')
    if exact_files is not None:
        need(inv['files'] == exact_files, 'Root-adopted complete files differ')
    if exact_dirs is not None:
        need({key: mode(value) for key, value in inv['directories'].items()} == {key: mode(value) for key, value in exact_dirs.items()}, 'Root-adopted directories differ')
    return inv

def controls(repo):
    git = repo / '.git'
    local = inventory(git / 'refs/heads')
    packed = [line for line in text(git / 'packed-refs').splitlines() if re.fullmatch(r'[0-9a-f]{40} refs/heads/\S+', line)]
    branches = {line.split(' ', 1)[1]: line.split(' ', 1)[0] for line in packed}
    for name in local['files']:
        branches['refs/heads/' + name] = text(git / 'refs/heads' / name).strip()
    head = text(git / 'HEAD').strip()
    need(head.startswith('ref: refs/heads/'), 'Unexpected native detached HEAD')
    return {'files': {name: record(git / name) for name in ['HEAD', 'index', 'config']}, 'HEAD': head,
            'resolved_local_HEAD': branches[head[5:]], 'local_heads': local, 'packed_local_head_lines': packed,
            'packed_refs_mode': oct(stat.S_IMODE((git / 'packed-refs').lstat().st_mode))}

def inputs():
    adopted, packets, root_pins = [], {}, {}
    for name, size, digest in ADOPTIONS:
        path = P / 'verification' / name
        root_pins[str(path)] = pin(path, size, digest)
        item = readj(path)
        adopted.append(item)
        clear = item.get('root_scientific_clearance', item.get('scientific_clearance'))
        root_pins[clear['path']] = pin(Path(clear['path']), clear['bytes'], clear['SHA256'], clear['mode'])
        for packet in item.get('packets', item.get('fresh_private_complete_authentication')):
            root = Path(packet['root'])
            need(root.parent == P / 'verification', 'Unexpected private packet root')
            for key in ['FINAL', 'manifest']:
                entry = packet[key]
                pin(Path(entry['path']), entry['bytes'], entry['SHA256'], entry['mode'])
            manifest = readj(Path(packet['manifest']['path']))
            complete = packet.get('all_actual_files')
            complete = None if complete is None else {key: {**value, 'mode': oct(mode(value['mode']))} for key, value in complete.items()}
            inv = manifest_auth(root, manifest, [Path(packet['manifest']['path']).name, 'FINAL.json'], packet.get('root_mode', 0o755), complete, packet.get('all_actual_directories'))
            if 'files' in packet:
                need((len(inv['files']), len(inv['directories'])) == (packet['files'], packet['child_directories']), 'Adopted packet extent differs')
            packets[str(root)] = inv
    sources = {}
    for recid, fsize, fhash, msize, mhash, count, dirs in SOURCE_PINS:
        root = P / 'papers' / str(recid) / 'sources'
        pin(root / 'SOURCE_FINAL.json', fsize, fhash)
        pin(root / 'SOURCE_MANIFEST.json', msize, mhash)
        inv = manifest_auth(root, readj(root / 'SOURCE_MANIFEST.json'), ['SOURCE_FINAL.json', 'SOURCE_MANIFEST.json'])
        need((len(inv['files']), len(inv['directories'])) == (count, dirs), 'Native source extent differs')
        sources[str(root)] = inv
    return {'root_pins': root_pins, 'private_packets': packets, 'native_sources': sources}

class Tags(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.tags, self.ids = [], []
        self.feed(raw)
        self.close()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])

def unique(pattern, value):
    matches = list(re.finditer(pattern, value, re.S))
    need(len(matches) == 1, 'Expected exactly one expression: ' + str(pattern))
    return matches[0]

def json_script(raw):
    hit = unique(r'<script type="application/ld\+json">(.*?)</script>', raw)
    return hit, json.loads(hit.group(1))

def strip_markup(raw):
    return ' '.join(html.unescape(re.sub('<[^>]*>', '', raw)).split())

def visible_unit(raw):
    parser = Tags(raw)
    return {'text': strip_markup(raw), 'hrefs': [attrs['href'] for tag, attrs in parser.tags if tag == 'a']}

def article_count(inv):
    return sum(len(Path(name).parts) == 3 and Path(name).parts[0] == 'research' and Path(name).parts[-1] == 'index.html' for name in inv['files'])

def page_activate(row, recid, lane, slug, main_name):
    root = P / 'verification' / lane
    model = readj(root / 'page-model.json')
    original = text(root / 'article.html')
    need(model['sheet_row'] == row and str(model['record_id']) == str(recid) and model['follow_up'] is None, 'Model identity differs')
    canonical = ORIGIN + '/research/' + slug + '/'
    need(model['deployment_proposal']['proposed_canonical_url'] == canonical, 'Proposed canonical differs')
    before_head = unique(r'<head>.*?</head>', original).group()
    main = unique(r'<main id="main">.*?</main>\n', original).group()
    need(main.encode() == data(root / main_name), 'Accepted whole MAIN differs')
    need((before_head + '\n').encode() == data(root / 'head.html'), 'Accepted whole head differs')
    script_hit, schema = json_script(before_head)
    if row == 184:
        need('@type' not in schema and [item.get('@type') for item in schema['@graph']] == ['WebPage', 'ScholarlyArticle'], 'Radial graph schema differs')
        webpage, scholarly = schema['@graph']
        need(webpage['url'] == scholarly['url'] == scholarly['mainEntityOfPage'] == canonical, 'Radial proposed URLs differ')
        need(len(scholarly['encoding']) == 3, 'Radial three-encoding contract differs')
        after_head = before_head.replace('<meta name="robots" content="noindex, nofollow">\n', '', 1)
        need(after_head != before_head, 'Radial private robots absent')
    else:
        need(schema.get('@type') == 'ScholarlyArticle' and '@graph' not in schema and len(schema['encoding']) == 2, 'Tree single-article schema differs')
        scholarly = schema
        activated = copy.deepcopy(schema)
        activated['@id'], activated['url'], activated['mainEntityOfPage'] = canonical + '#article', canonical, canonical
        for asset, encoding in zip(model['native_asset_order'], activated['encoding']):
            need(encoding['contentUrl'] == asset['local_path'], 'Tree private encoding path differs')
            encoding['contentUrl'] = canonical + asset['local_path']
        after_head = before_head[:script_hit.start(1)] + json.dumps(activated, ensure_ascii=False) + before_head[script_hit.end(1):]
        for name in ['robots', 'googlebot']:
            token = '<meta name="' + name + '" content="noindex, nofollow">\n'
            need(after_head.count(token) == 1, 'Tree private robots contract differs')
            after_head = after_head.replace(token, '', 1)
        token = '<meta name="citation_pdf_url" content="assets/congestion-fragmentation.pdf">'
        need(after_head.count(token) == 1, 'Tree citation PDF contract differs')
        after_head = after_head.replace(token, '<meta name="citation_pdf_url" content="' + canonical + 'assets/congestion-fragmentation.pdf">', 1)
        need(after_head.count('<link rel="stylesheet" href="research.css">') == 1, 'Tree stylesheet contract differs')
        after_head = after_head.replace('<link rel="stylesheet" href="research.css">', '<link rel="canonical" href="' + canonical + '">\n<link rel="stylesheet" href="/research/research.css">\n<meta property="og:url" content="' + canonical + '">', 1)
    need(scholarly['abstract'] == model['abstract'], 'Accepted schema abstract differs')
    need([encoding['encodingFormat'] for encoding in scholarly['encoding']] == [asset['format'] for asset in model['native_asset_order']], 'Native encoding order differs')
    for encoding, asset in zip(scholarly['encoding'], model['native_asset_order']):
        expected = canonical + asset['local_path'] if row == 184 else asset['local_path']
        need(encoding['contentUrl'] == expected, 'Accepted encoding URL differs')
    out = original.replace(before_head, after_head, 1)
    need(unique(r'<body>.*?</body>', out).group().encode() == unique(r'<body>.*?</body>', original).group().encode(), 'Accepted whole body changed')
    need(unique(r'<main id="main">.*?</main>\n', out).group().encode() == main.encode(), 'Accepted MAIN changed')
    prefix = 'research/' + slug + '/'
    target = CANDIDATE / prefix
    need(not target.exists(), 'Proposed article already exists')
    target.mkdir(mode=0o755)
    (target / 'assets').mkdir(mode=0o755)
    put('candidate/public/' + prefix + 'index.html', out.encode())
    shutil.copy2(root / 'citation.bib', target / 'citation.bib')
    need(data(target / 'citation.bib') == data(root / 'citation.bib'), 'Staged Bib differs')
    source = P / 'papers' / str(recid) / 'sources'
    native = readj(source / 'record.response.body')['files']
    need([entry['key'] for entry in native] == [asset['name'] for asset in model['native_asset_order']], 'Native record order differs')
    for entry, asset in zip(native, model['native_asset_order']):
        body = data(root / asset['local_path'])
        need(body == data(source / 'assets' / asset['name']), 'Accepted asset differs from native')
        need(len(body) == entry['size'] == asset['bytes'] and hashlib.sha256(body).hexdigest() == asset['SHA256'], 'Native asset identity differs')
        need('md5:' + hashlib.md5(body).hexdigest() == entry['checksum'] == asset['native_checksum'], 'Native asset MD5 differs')
        shutil.copy2(root / asset['local_path'], target / asset['local_path'])
        need(data(target / asset['local_path']) == body and mode(record(target / asset['local_path'])['mode']) == mode(asset['mode']), 'Staged original differs')
    return {'row': row, 'record': recid, 'slug': slug, 'canonical': canonical, 'model': model, 'accepted_MAIN': record(root / main_name), 'accepted_article': record(root / 'article.html'), 'activated_article': record(target / 'index.html')}

def index_parts(raw):
    hit = unique(r'(<h2>Papers</h2>\s*<ul>)(.*?)(</ul>)', raw)
    units = re.findall(r'<li(?:\s[^>]*)?>.*?</li>', hit.group(2), re.S)
    need(re.sub(r'<li(?:\s[^>]*)?>.*?</li>', '', hit.group(2), flags=re.S).strip() == '', 'Unexpected papers-list material')
    script_hit, schema = json_script(raw)
    need(schema['@type'] == 'CollectionPage' and schema['mainEntity']['@type'] == 'ItemList', 'Research index schema differs')
    script = script_hit.group(1)
    array_start = unique(r'"itemListElement"\s*:\s*\[', script).end() - 1
    decoder = json.JSONDecoder()
    typed, array_end = decoder.raw_decode(script, array_start)
    cursor, raw_items = array_start + 1, []
    while cursor < array_end - 1:
        while cursor < array_end - 1 and (script[cursor].isspace() or script[cursor] == ','):
            cursor += 1
        if cursor == array_end - 1:
            break
        item, end = decoder.raw_decode(script, cursor)
        raw_items.append(script[cursor:end])
        cursor = end
    need(typed == schema['mainEntity']['itemListElement'] and len(raw_items) == len(typed), 'Raw/typed index disagreement')
    need(len(units) == len(typed) == schema['mainEntity']['numberOfItems'], 'Visible/typed index count disagreement')
    need([item['position'] for item in typed] == list(range(1, len(typed) + 1)), 'Index positions differ')
    need(len({item['url'] for item in typed}) == len(typed), 'Duplicate typed article URL')
    visible = [visible_unit(unit) for unit in units]
    need([urljoin(ORIGIN, item['hrefs'][0]) for item in visible] == [item['url'] for item in typed], 'Visible/typed URL order disagreement')
    return {'list_hit': hit, 'units': units, 'visible': visible, 'script_hit': script_hit, 'script': script, 'schema': schema, 'typed': typed, 'raw_items': raw_items, 'array_end': array_end}

def update_index(old, pages):
    before = index_parts(old)
    need(len(before['units']) == 126, 'Baseline article count differs')
    new_items, new_rows = [], ''
    for page in pages:
        model, canonical = page['model'], page['canonical']
        need(canonical not in [item['url'] for item in before['typed']] and model['doi'] not in old, 'Duplicate new index identity')
        new_items.append({'@type': 'ListItem', 'position': 127 + len(new_items), 'url': canonical, 'name': model['title']})
        published = date.fromisoformat(model['publication_date'])
        label = str(published.day) + published.strftime(' %B %Y') + ' · Version ' + model['native_version'] + ' · ' + model['status']
        pdf = [asset['local_path'] for asset in model['native_asset_order'] if asset['format'] == 'application/pdf']
        need(len(pdf) == 1, 'One PDF required')
        base = '/research/' + page['slug'] + '/'
        new_rows += '<li><a href="' + base + '">' + html.escape(model['title']) + '</a><br><span class="entry-meta">' + html.escape(label) + '</span><p>' + html.escape(model['meta_description']) + '</p><p><a href="' + base + pdf[0] + '">PDF</a> · <a href="' + model['doi_url'] + '">Zenodo</a></p></li>\n'
    insertion = ', ' + json.dumps(new_items, ensure_ascii=False)[1:-1]
    offset = before['array_end'] - 1
    script = before['script'][:offset] + insertion + before['script'][offset:]
    script, replacements = re.subn(r'("numberOfItems"\s*:\s*)126\b', r'\g<1>128', script)
    need(replacements == 1, 'Research item count activation differs')
    hit = before['script_hit']
    out = old[:hit.start(1)] + script + old[hit.end(1):]
    list_hit = unique(r'(<h2>Papers</h2>\s*<ul>)(.*?)(</ul>)', out)
    out = out[:list_hit.end(2)] + new_rows + out[list_hit.end(2):]
    after = index_parts(out)
    need(after['units'][:126] == before['units'] and after['visible'][:126] == before['visible'] and after['typed'][:126] == before['typed'] and after['raw_items'][:126] == before['raw_items'], 'Old index units changed')
    need(len(after['units']) == 128 and after['typed'][126:] == new_items, 'New index units differ')
    restored = out.replace(new_rows, '', 1).replace(script, before['script'], 1)
    need(restored == old, 'Whole index aggregate not reversible')
    return out, {'old_visible': before['visible'], 'old_typed': before['typed'], 'old_raw_JSON_units': before['raw_items'], 'old_raw_HTML_units': before['units'], 'new_items': new_items, 'appended_HTML': new_rows, 'appended_JSON': insertion, 'whole_buffer_reversible': True}

def xml_node(node):
    return {'tag': node.tag, 'attributes': node.attrib, 'text': node.text, 'tail': node.tail, 'children': [xml_node(child) for child in node]}

def update_sitemap(old, pages):
    before = ET.fromstring(old)
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    raw_before = re.findall(r'<url>.*?</url>', old, re.S)
    need(before.tag == ns + 'urlset' and len(before) == len(raw_before) == 127, 'Sitemap baseline differs')
    locs = [node.find(ns + 'loc').text for node in before]
    need(len(locs) == len(set(locs)), 'Duplicate baseline sitemap URL')
    insertion = ''
    for page in pages:
        need(page['canonical'] not in locs, 'Duplicate new sitemap URL')
        insertion += '<url><loc>' + page['canonical'] + '</loc><lastmod>2026-11-17</lastmod></url>\n'
    need(old.count('</urlset>') == 1, 'Sitemap close differs')
    out = old.replace('</urlset>', insertion + '</urlset>', 1)
    after = ET.fromstring(out)
    need(re.findall(r'<url>.*?</url>', out, re.S)[:127] == raw_before, 'Old raw XML nodes changed')
    need([xml_node(node) for node in after][:127] == [xml_node(node) for node in before], 'Old parsed XML nodes changed')
    need(len(after) == 129 and [node.find(ns + 'loc').text for node in after][127:] == [page['canonical'] for page in pages], 'New sitemap nodes differ')
    need(out.replace(insertion, '', 1) == old, 'Whole sitemap aggregate not reversible')
    return out, {'old_raw_nodes': raw_before, 'old_parsed_nodes': [xml_node(node) for node in before], 'appended_XML': insertion, 'whole_buffer_reversible': True}

def validate_page(page):
    path = CANDIDATE / 'research' / page['slug'] / 'index.html'
    raw = text(path)
    tags = Tags(raw)
    need(len(tags.ids) == len(set(tags.ids)), 'Duplicate page identifier')
    metas = [(attrs.get('name', attrs.get('property')), attrs.get('content')) for tag, attrs in tags.tags if tag == 'meta']
    need(len(metas) == len({name for name, value in metas}), 'Duplicate metadata name')
    metas = dict(metas)
    need('robots' not in metas and 'googlebot' not in metas and 'noindex' not in raw and 'nofollow' not in raw, 'Private crawler restriction remains')
    canonical = [attrs['href'] for tag, attrs in tags.tags if tag == 'link' and attrs.get('rel') == 'canonical']
    need(canonical == [page['canonical']] and metas['og:url'] == page['canonical'], 'Activated canonical differs')
    need([attrs['href'] for tag, attrs in tags.tags if tag == 'link' and attrs.get('rel') == 'stylesheet'] == ['/research/research.css'], 'Shared stylesheet differs')
    hit, schema = json_script(raw)
    scholarly = schema['@graph'][1] if page['row'] == 184 else schema
    need(scholarly['url'] == scholarly['mainEntityOfPage'] == page['canonical'], 'Activated scholarly URL differs')
    need(scholarly['abstract'] == page['model']['abstract'], 'Activated full abstract differs')
    need([item['contentUrl'] for item in scholarly['encoding']] == [page['canonical'] + asset['local_path'] for asset in page['model']['native_asset_order']], 'Activated native encodings differ')
    pdf = [asset['local_path'] for asset in page['model']['native_asset_order'] if asset['format'] == 'application/pdf'][0]
    need(metas['citation_pdf_url'] == page['canonical'] + pdf, 'Absolute citation PDF differs')
    for tag, attrs in tags.tags:
        for key in ['href', 'src']:
            if key not in attrs:
                continue
            url = urlsplit(attrs[key])
            if url.scheme and (url.scheme != 'https' or url.netloc != 'aleckriebel.com'):
                continue
            if url.netloc and url.netloc != 'aleckriebel.com':
                continue
            if url.path:
                target = CANDIDATE / unquote(url.path.lstrip('/')) if url.path.startswith('/') else path.parent / unquote(url.path)
                need(target.resolve().is_relative_to(CANDIDATE.resolve()), 'Internal path escapes candidate')
                if target.is_dir():
                    target = target / 'index.html'
                need(target.is_file(), 'Internal candidate target missing: ' + str(target))
            elif url.fragment:
                need(url.fragment in tags.ids, 'Local fragment missing')
        for ident in attrs.get('aria-labelledby', '').split():
            need(ident in tags.ids, 'Label target missing')

def main():
    need(Path(__file__).resolve() == OWN / 'build_private.py', 'Builder location differs')
    allowed = {'RESEARCH_LOG.md', 'INTAKE_FAILURES.md', 'build_private.py', 'BUILD.stdout.txt', 'BUILD.stderr.txt'}
    need({path.name for path in OWN.iterdir()} <= allowed, 'Owned lane is not fresh')
    started = now()
    before_inputs = inputs()
    before_native = {'M': controls(M), 'W': controls(W)}
    need(before_native['M']['resolved_local_HEAD'] == 'a4ce3c37dad209339e490d18dcced6c48cf912d2', 'M checked-out main differs')
    need(before_native['M']['files']['index']['SHA256'] == '91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11', 'M native index differs')
    need(before_native['M']['files']['config']['SHA256'] == '2c083de0f0839443ce1ed062a8c1f2be83cbc30f838e5350e567a8153b7b3a47', 'M native config differs')
    need(before_native['W']['resolved_local_HEAD'] == '96f04aa5544df69daba07a9ed4d6212172e9984a', 'W master differs')
    pin(W / '.git/index', 9057886, 'e6285d49b7249ae2c88a1f624ca98c1dcf480424db272c4fe111ca91dbdafb5e')
    need(struct.unpack('>4sII', data(W / '.git/index')[:12]) == (b'DIRC', 2, 58712), 'W native index header differs')
    baseline = inventory(PUBLIC)
    need((len(baseline['files']), len(baseline['directories']), mode(baseline['root_mode']), article_count(baseline)) == (772, 373, 0o750, 126), 'Published baseline extent differs')
    need(sum(Path(name).name == '.DS_Store' for name in baseline['files']) == 17, 'Published DS_Store count differs')
    pin(PUBLIC / 'research/research.css', 1170, 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a')
    putj('GUARDS_BEFORE.json', {'inputs': before_inputs, 'native_controls': before_native, 'public': baseline})
    old_index, old_sitemap = text(PUBLIC / 'research/index.html'), text(PUBLIC / 'research/sitemap.xml')
    put('originals/research-index.html', old_index.encode())
    put('originals/research-sitemap.xml', old_sitemap.encode())
    shutil.copytree(PUBLIC, CANDIDATE, copy_function=shutil.copy2)
    pages = [page_activate(*row) for row in ROWS]
    new_index, index_evidence = update_index(old_index, pages)
    new_sitemap, sitemap_evidence = update_sitemap(old_sitemap, pages)
    (CANDIDATE / 'research/index.html').write_bytes(new_index.encode())
    (CANDIDATE / 'research/sitemap.xml').write_bytes(new_sitemap.encode())
    putj('AGGREGATE_PRESERVATION.json', {'index': index_evidence, 'sitemap': sitemap_evidence})
    for page in pages:
        validate_page(page)
    candidate = inventory(CANDIDATE)
    added = [name for name in candidate['files'] if name not in baseline['files']]
    removed = [name for name in baseline['files'] if name not in candidate['files']]
    modified = [name for name in baseline['files'] if candidate['files'].get(name) != baseline['files'][name]]
    expected_adds, expected_dirs = [], []
    for page in pages:
        prefix = 'research/' + page['slug']
        expected_adds += [prefix + '/index.html', prefix + '/citation.bib'] + [prefix + '/' + asset['local_path'] for asset in page['model']['native_asset_order']]
        expected_dirs += [prefix, prefix + '/assets']
    new_dirs = [name for name in candidate['directories'] if name not in baseline['directories']]
    need(set(added) == set(expected_adds) and len(added) == 9 and not removed, 'Production additions/deletions differ')
    need(set(modified) == {'research/index.html', 'research/sitemap.xml'}, 'Production replacement set differs')
    need(set(new_dirs) == set(expected_dirs) and len(new_dirs) == 4, 'Necessary new directory set differs')
    need(all(candidate['directories'].get(name) == value for name, value in baseline['directories'].items()) and candidate['root_mode'] == baseline['root_mode'], 'Old public directory modes/topology changed')
    need((len(candidate['files']), len(candidate['directories']), article_count(candidate)) == (781, 377, 128), 'Candidate extent differs')
    need(sum(Path(name).name == '.DS_Store' for name in candidate['files']) == 17, 'Candidate hidden DS_Store count differs')
    for name in expected_adds:
        need(mode(candidate['files'][name]['mode']) == 0o644, 'New target mode differs')
    need(all(mode(candidate['directories'][name]) == 0o755 for name in expected_dirs), 'New directory mode differs')
    after_inputs, after_native, after_public = inputs(), {'M': controls(M), 'W': controls(W)}, inventory(PUBLIC)
    need(before_inputs == after_inputs and before_native == after_native and baseline == after_public, 'Read-only input/native/public guard drift')
    putj('GUARDS_AFTER.json', {'inputs': after_inputs, 'native_controls': after_native, 'public': after_public})
    target_plan = {'row_order': [184, 185], 'A': expected_adds, 'M': ['research/index.html', 'research/sitemap.xml'], 'D': [], 'new_directories': expected_dirs, 'production_target_count': 11}
    putj('TARGETS.json', target_plan)
    putj('CANDIDATE_MANIFEST.json', candidate)
    finished = now()
    receipt = {'UTC_started': started, 'UTC_finished': finished, 'status': 'PASS_PRIVATE_STAGE_DATA_CHECKS', 'private_build_attempts': 1, 'row_order': [184, 185], 'pages': pages,
               'baseline_files': 772, 'baseline_child_directories': 373, 'candidate_files': 781, 'candidate_child_directories': 377, 'old_articles': 126, 'candidate_articles': 128, 'old_sitemap_nodes': 127, 'candidate_sitemap_nodes': 129,
               'all_126_old_visible_typed_raw_HTML_and_JSON_index_units_preserved_in_order': True, 'all_127_raw_and_parsed_XML_nodes_preserved_in_order': True, 'whole_aggregate_buffers_reversible': True,
               'all_other_old_public_bytes_modes_hidden_empty_and_directory_topology_unchanged': True, 'full_private_and_native_source_namespaces_authenticated_before_after': True, 'M_W_native_HEAD_index_config_local_loose_and_packed_heads_unchanged': True,
               'remote_tracking_refs_FETCH_HEAD_and_nonlocal_packed_lines_not_confused_with_native_main': True, 'accepted_whole_MAIN_and_body_byte_exact': True, 'native_assets_and_Bibs_byte_exact': True, 'schema_specific_activation_only': True,
               'scientific_and_copy_clearance_inherited': True, 'new_scientific_copy_or_rendered_live_certificate': False, 'W_Git_network_install_deploy_Sheet_AA_redirect_release_or_outreach_action': False, 'follow_up': None}
    putj('BUILD_RECEIPT.json', receipt)
    report = '# Private radial/tree website stage\n\nPASS for private-stage data preparation only. The candidate preserves the accepted complete MAIN/body/abstract/math/rights/collaboration and original assets/BibTeX for rows 184 then 185. The radial WebPage+ScholarlyArticle graph and three checksum→ZIP→PDF encodings are retained; only its private robots tag is removed. The tree single ScholarlyArticle retains its ZIP→PDF order while canonical/page identifiers, OG URL, absolute scholarly asset/PDF URLs and the existing shared stylesheet are activated. No public copy or scientific verdict is changed.\n\nBaseline W master96f04aa5544df69daba07a9ed4d6212172e9984a, native index v2/58712, public772 files/373 child directories and root0750 are preserved. Candidate public781 files/377 child directories contains128 articles and129 sitemap nodes. Exact11 production targets comprise9 additions and2 aggregate replacements, with4 necessary new directories. Every old126 visible/typed/raw index unit and127 raw/parsed XML nodes remains in order; complete aggregate buffers are reversible. Every other old public byte, mode, hidden/ignored/empty file and directory is unchanged. Seventeen DS_Store files remain exact.\n\nGUARDS_BEFORE/AFTER authenticate full accepted private/source packets and unchanged native M/W HEAD/index/config plus local loose/packed heads. Remote-tracking/FETCH_HEAD/nonlocal packed metadata is outside that native-main guard, as root directed. The new bounded builder was saved and personally read in full before its sole private build; no archived helper/source/scientific program or helper mode/import/test ran. All literal intake failures remain in INTAKE_FAILURES.md. No website/Git/network/install/deploy/tracker/AA/redirect/release action or outreach occurred. No child agents were used.\n\nThe private candidate requires independent implementation audit and root adoption. Rendered desktop/mobile/PDF-reader behavior, external/live downloads and actual publication remain unverified here. The radial legacy redirect is deferred until the actual replacement is live and verified; no redirect authority is supplied. Both follow-ups remain null.\n'
    put('REPORT.md', report.encode())
    need(data(OWN / 'BUILD.stdout.txt') == b'' and data(OWN / 'BUILD.stderr.txt') == b'', 'Build stream is not empty')
    with (OWN / 'RESEARCH_LOG.md').open('a', encoding='utf-8') as handle:
        handle.write('\n- ' + finished + ' — 100% complete toward the assigned private-stage preparation. One personally read new bounded builder completed all data checks; exact candidate781/377,128 articles/129 sitemap nodes,11 targets9A2M/4 new directories, accepted body/MAIN/assets/Bibs preserved. Full private/source/public/native guards passed before/after;126 old index units and127 XML nodes remain ordered and aggregate buffers reverse exactly. No scientific/copy/render/live or publication certificate is implied. Finite manifest/FINAL freeze follows; no later writes.\n')
    own_inv = inventory(OWN)
    manifest = {'schema': 'finite-private-stage-owned-manifest-v1', 'UTC': finished, 'root': str(OWN), 'root_mode': own_inv['root_mode'],
                'files': [{'path': name, **value} for name, value in own_inv['files'].items()], 'directories': [{'path': name, 'mode': value} for name, value in own_inv['directories'].items()],
                'exact_terminal_exclusions': ['OWNED_MANIFEST.json', 'FINAL.json'], 'all_hidden_ignored_empty_files_and_modes_included': True, 'no_future_or_subtree_exclusions': True}
    putj('OWNED_MANIFEST.json', manifest)
    final = {'schema': 'private-two-page-stage-final-v1', 'UTC': finished, 'status': 'FROZEN_PRIVATE_STAGE_READY_FOR_INDEPENDENT_IMPLEMENTATION_AUDIT', 'completion_percent_private_stage': 100,
             'manifest': {'path': 'OWNED_MANIFEST.json', **record(OWN / 'OWNED_MANIFEST.json')}, 'receipt': {'path': 'BUILD_RECEIPT.json', **record(OWN / 'BUILD_RECEIPT.json')},
             'candidate_manifest': {'path': 'CANDIDATE_MANIFEST.json', **record(OWN / 'CANDIDATE_MANIFEST.json')}, 'target_plan': target_plan,
             'candidate_root': str(CANDIDATE), 'candidate_files': 781, 'candidate_child_directories': 377, 'candidate_articles': 128, 'candidate_sitemap_nodes': 129,
             'source_and_private_packets_unchanged': True, 'M_W_native_and_W_public_unchanged': True, 'accepted_MAIN_body_assets_Bibs_exact': True, 'full_aggregate_preservation_and_reversibility': True,
             'scientific_copy_clearance_inherited': True, 'new_scientific_copy_or_rendered_live_certificate': False, 'actual_publication_date': None, 'AA': None, 'publication_authority': False, 'follow_up': None,
             'W_Git_network_install_deploy_Sheet_redirect_release_or_outreach_action': False, 'child_agents': 0, 'ordinary_private_stage_builds': 1, 'retained_intake_read_failures': 2,
             'extent': {'regular_files': len(own_inv['files']) + 2, 'child_directories': len(own_inv['directories']), 'root_mode': own_inv['root_mode'], 'all_paths': sorted(list(own_inv['files']) + ['OWNED_MANIFEST.json', 'FINAL.json'])},
             'terminal_self_hash_excluded': True, 'all_handles_terminal_at_return': True, 'quiescent_after_freeze': True}
    putj('FINAL.json', final)

main()
