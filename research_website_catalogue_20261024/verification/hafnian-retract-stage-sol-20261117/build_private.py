"""One bounded private data build. No source/helper program or Git command runs."""
import hashlib
import html
import json
import os
import re
import shutil
import stat
import struct
import sys
import time
import traceback
import zlib
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/hafnian-retract-stage-sol-20261117'
INITIAL = P / 'verification/hafnian-retract-stage-initial-sol-20261117'
BINDINGS = P / 'verification/hafnian-retract-stage-initial-bindings-sol-20261117'
M = Path('/Users/alec/Documents/Math')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
PUBLIC = W / 'public'
BASE = OWN / 'baseline-public'
CAND = OWN / 'candidate-public'
TERMINALS = ['FINAL.json', 'OWNED_MANIFEST.json']
FAMILIES = [('hafnian', '23205294', 'nonnegative-rational-hafnians'),
            ('complex-retract', '23203270', 'complex-polynomial-retract-five-variables')]
CONTROL_PINS = {
    INITIAL / 'CONTRACT.json': 'f88a8adef0a2960ea6a3a91afa6d64f88dde8ecfe7ed8cabbbadbce562bea49c',
    BINDINGS / 'FINAL.json': '654b18de3078e4257c8fbfb033e13115220cef240fc9ef223e261e823a82273c',
    BINDINGS / 'OWNED_MANIFEST.json': '04a19fe029763b14cb7370867ad42167e8abd5283c8e989d77d81b8f63399b36',
    BINDINGS / 'INPUT_BINDINGS.json': 'c7ddeb3e335b317bba3864912807083fe4df423f0392be004de6df376c1b8a40',
    P / 'verification/root-hafnian-retract-stage-binding-adoption-20261117.json': 'ba2a73e763adf4b38fb730ce38836132e1f1b70326d9fa3a2c5bc09e2e9f578c',
    P / 'verification/root-hafnian-editorial-adoption-20261117.json': '775b1ef8b9592e55d21fcd45e4bf381f3965a27282f41277ac7ab8e9880c07dc',
    P / 'verification/root-complex-retract-editorial-adoption-20261117.json': 'ea048b2f612c2c6a7593fcd51184ad72918200dc88d2565d307dec44a8284df5'}
RULES = [
 ('verification/hafnian-editorial-sol-20261117', 'MANIFEST.json', 'FINAL.json', 'finite-private-editorial-manifest-v1', 'payload_files'),
 ('verification/hafnian-fact-sol-20261117', 'MANIFEST.json', 'FINAL.json', 'finite-private-fact-review-manifest-v1', 'payload_files'),
 ('verification/hafnian-legacy-sol-20261117', 'FINAL_MANIFEST.json', 'FINAL_SEAL.json', 'hafnian-legacy-finite-final-manifest-v1', 'entries'),
 ('verification/complex-retract-editorial-sol-20261117', 'MANIFEST.json', 'FINAL.json', 'finite-private-editorial-manifest-v1', 'payload_files'),
 ('verification/complex-retract-fact-sol-20261117', 'MANIFEST.json', 'FINAL.json', 'finite-private-fact-review-manifest-v1', 'payload_files'),
 ('verification/complex-retract-legacy-sol-20261117', 'OWNED_MANIFEST.json', 'FINAL.json', 'finite-complex-retract-legacy-correspondence-manifest-v1', 'files'),
 ('papers/23205294/sources', 'SOURCE_MANIFEST.json', 'SOURCE_FINAL.json', 'finite-source-manifest-v1', 'files'),
 ('papers/23203270/sources', 'SOURCE_MANIFEST.json', 'SOURCE_FINAL.json', 'source-custody-finite-manifest-v1', 'entries'),
 ('verification/hafnian-retract-stage-initial-sol-20261117', 'OWNED_MANIFEST.json', 'FINAL.json', 'finite-hafnian-retract-stage-INITIAL-manifest-v1', 'payload_files')]

def need(value, label):
    if not value:
        raise ValueError(label)

def utc():
    return datetime.now(timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pairs(items):
    result = {}
    for key, value in items:
        need(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result

def loads(text):
    return json.loads(text, object_pairs_hook=pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite JSON: ' + value)))

def readj(path):
    return loads(path.read_bytes().decode('utf-8'))

def mo(value):
    if type(value) is int:
        need(0 <= value <= 0o7777, 'Invalid integer mode')
        return format(value, '04o')
    need(type(value) is str and re.fullmatch(r'(?:0o[0-7]{3,4}|0[0-7]{3})', value), 'Invalid mode string')
    return format(int(value, 8), '04o')

def rel(value, root=False):
    need(type(value) is str and value != '' and '\\' not in value and '\x00' not in value, 'Invalid path')
    if value == '.' and root:
        return value
    need(not value.startswith('/') and value != '.' and all(part not in ['', '.', '..'] for part in value.split('/')) and PurePosixPath(value).as_posix() == value, 'Noncanonical path: ' + value)
    return value

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Not regular: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': sha(data), 'mode': format(stat.S_IMODE(info.st_mode), '04o')}

def inventory(root):
    info = root.lstat()
    need(stat.S_ISDIR(info.st_mode), 'Not directory: ' + str(root))
    files = {}
    dirs = {'.': {'mode': format(stat.S_IMODE(info.st_mode), '04o'), 'empty': not any(root.iterdir())}}
    for path in sorted(root.rglob('*'), key=lambda item: item.relative_to(root).as_posix()):
        name = rel(path.relative_to(root).as_posix())
        info = path.lstat()
        if stat.S_ISDIR(info.st_mode):
            dirs[name] = {'mode': format(stat.S_IMODE(info.st_mode), '04o'), 'empty': not any(path.iterdir())}
        else:
            files[name] = pin(path)
    result = {'root': str(root), 'files': files, 'directories': dirs, 'regular_files': len(files), 'child_directories': len(dirs) - 1}
    validate_snapshot(result)
    return result

def validate_snapshot(value):
    need(type(value) is dict and set(value) == {'root', 'files', 'directories', 'regular_files', 'child_directories'}, 'Snapshot schema')
    need(type(value['root']) is str and Path(value['root']).is_absolute(), 'Snapshot root')
    files, dirs = value['files'], value['directories']
    need(type(files) is dict and type(dirs) is dict and '.' in dirs and not set(files) & set(dirs), 'Snapshot domains')
    for name, row in files.items():
        rel(name)
        need(type(row) is dict and set(row) == {'bytes', 'SHA256', 'mode'}, 'File row schema')
        need(type(row['bytes']) is int and row['bytes'] >= 0 and type(row['SHA256']) is str and re.fullmatch('[0-9a-f]{64}', row['SHA256']), 'File bytes/hash')
        need(type(row['mode']) is str and re.fullmatch('0[0-7]{3}', row['mode']), 'Snapshot file mode')
    for name, row in dirs.items():
        rel(name, True)
        need(type(row) is dict and set(row) == {'mode', 'empty'} and type(row['empty']) is bool, 'Directory row schema')
        need(type(row['mode']) is str and re.fullmatch('0[0-7]{3}', row['mode']), 'Snapshot directory mode')
        expected_empty = not any(PurePosixPath(child).parent.as_posix() == name for child in list(files) + [key for key in dirs if key != '.'])
        need(row['empty'] == expected_empty, 'Directory emptiness mismatch: ' + name)
    for name in list(files) + [key for key in dirs if key != '.']:
        need(PurePosixPath(name).parent.as_posix() in dirs, 'Missing parent: ' + name)
    need(type(value['regular_files']) is int and value['regular_files'] == len(files) and type(value['child_directories']) is int and value['child_directories'] == len(dirs) - 1, 'Snapshot counts')

def equal_snapshot(left, right, root_identity=True):
    validate_snapshot(left)
    validate_snapshot(right)
    need(left['files'] == right['files'] and left['directories'] == right['directories'] and left['regular_files'] == right['regular_files'] and left['child_directories'] == right['child_directories'] and (not root_identity or left['root'] == right['root']), 'Whole snapshot differs: ' + right['root'])

def write(name, data, mode=0o644):
    rel(name)
    path = OWN / name
    need(not path.exists(), 'Owned output already exists: ' + name)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as handle:
        handle.write(data)
    os.chmod(path, mode)

def writej(name, data):
    write(name, (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode())

def native(root):
    gitdir = root / '.git'
    head = (gitdir / 'HEAD').read_text()
    need(re.fullmatch(r'ref: refs/heads/[^\n]+\n', head), 'Native HEAD shape')
    branch = head.removeprefix('ref: ').strip()
    packed = gitdir / 'packed-refs'
    raw_lines = [line for line in packed.read_text().splitlines(keepends=True) if ' refs/heads/' in line]
    need(len({line.split(' ', 1)[1].strip() for line in raw_lines}) == len(raw_lines), 'Duplicate packed local head')
    loose = gitdir / branch
    values = [line.split(' ', 1)[0] for line in raw_lines if line.split(' ', 1)[1].strip() == branch]
    resolved = loose.read_text().strip() if loose.exists() else (values[0] if len(values) == 1 else None)
    need(type(resolved) is str and re.fullmatch('[0-9a-f]{40}', resolved), 'Native head unresolved')
    return {name: pin(gitdir / name) for name in ['HEAD', 'index', 'config']} | {'HEAD_text': head, 'local_loose_heads': inventory(gitdir / 'refs/heads'), 'packed_local_heads': {'file_mode': format(stat.S_IMODE(packed.lstat().st_mode), '04o'), 'raw_lines': raw_lines}, 'resolved_native_HEAD': resolved}

def capture(binding):
    prior = binding['guards_before']
    return {'roots': {root: inventory(Path(root)) for root in prior['roots']},
            'controls': {path: pin(Path(path)) for path in prior['controls']},
            'public': inventory(PUBLIC), 'native_M': native(M), 'native_W': native(W),
            'binding_lane': inventory(BINDINGS), 'stage_control_pins': {str(path): pin(path) for path in CONTROL_PINS}}

def observe_remote():
    gitdir = M / '.git'
    result = {}
    for name in ['FETCH_HEAD', 'packed-refs']:
        path = gitdir / name
        result[name] = pin(path) if path.exists() else None
    remotes = gitdir / 'refs/remotes'
    result['loose_remote_tracking'] = inventory(remotes) if remotes.exists() else None
    result['comparison_scope'] = 'Observation only; remote/FETCH and nonlocal packed lines may advance independently of native main'
    return result

def check_manifest(root, snapshot, name, terminal, schema, rows_key, external):
    need(pin(root / name) == external['manifest'] and pin(root / terminal) == external['terminal'], 'External terminal pins differ: ' + str(root))
    value = readj(root / name)
    need(value['schema'] == schema and [key for key in ['payload_files', 'files', 'entries'] if key in value] == [rows_key], 'Manifest actual schema')
    exclusion_keys = [key for key in ['exact_terminal_exclusions', 'excluded_control_files', 'exact_already_created_terminal_recursive_hash_exclusions'] if key in value]
    need(len(exclusion_keys) == 1 and type(value[exclusion_keys[0]]) is list, 'Manifest terminal exclusion shape')
    exclusions = value[exclusion_keys[0]]
    need(len(exclusions) == 2 and len(set(exclusions)) == 2, 'Manifest terminal exclusion count/duplicate')
    expected_controls = {str(root / item) for item in [name, terminal]} if exclusion_keys[0] == 'exact_already_created_terminal_recursive_hash_exclusions' else {name, terminal}
    need(set(exclusions) == expected_controls, 'Manifest exact terminal conventions differ')
    rows = value[rows_key]
    need(type(rows) is list and type(value.get('directories', [])) is list, 'Manifest list type')
    files, dirs, controls = set(), set(), []
    for row in rows:
        need(type(row) is dict and 'path' in row, 'Manifest row type')
        name_rel = rel(row['path'], rows_key == 'entries')
        need(name_rel not in files | dirs, 'Duplicate manifest path')
        row_mode = mo(row['mode_octal'] if rows_key == 'entries' else row['mode'])
        if rows_key == 'entries' and row['kind'] == 'directory':
            need(set(row) == {'path', 'kind', 'mode_octal', 'empty'} and type(row['empty']) is bool, 'Entry directory shape')
            need(snapshot['directories'][name_rel] == {'mode': row_mode, 'empty': row['empty']}, 'Manifest directory differs')
            dirs.add(name_rel)
            continue
        need(rows_key != 'entries' or row['kind'] == 'file', 'Entry kind')
        files.add(name_rel)
        actual = snapshot['files'][name_rel]
        need(actual['mode'] == row_mode, 'Manifest file mode')
        if row.get('terminal_control') is True:
            need(root.name == 'complex-retract-legacy-sol-20261117' and name_rel in [name, terminal] and set(row) == {'path', 'mode', 'terminal_control'}, 'Unexpected mode-only terminal')
            need(actual == external['manifest' if name_rel == name else 'terminal'], 'Mode-only terminal missing external pin')
            controls.append(name_rel)
            continue
        required = {'path', 'kind', 'mode_octal', 'bytes', 'sha256', 'md5'} if rows_key == 'entries' else {'path', 'bytes', 'SHA256', 'mode'}
        allowed = required | ({'git_blob_sha1'} if rows_key == 'entries' else {'MD5'})
        need(required <= set(row) <= allowed and type(row['bytes']) is int and row['bytes'] >= 0, 'Manifest payload shape')
        digest = row['sha256'] if rows_key == 'entries' else row['SHA256']
        need(type(digest) is str and re.fullmatch('[0-9a-f]{64}', digest) and actual['bytes'] == row['bytes'] and actual['SHA256'] == digest, 'Manifest payload pin')
        data = (root / name_rel).read_bytes()
        if 'MD5' in row or 'md5' in row:
            need(hashlib.md5(data).hexdigest() == row.get('MD5', row.get('md5')), 'Manifest MD5')
        if 'git_blob_sha1' in row:
            need(hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\x00' + data).hexdigest() == row['git_blob_sha1'], 'Manifest blob SHA1')
    if rows_key != 'entries':
        need(snapshot['directories']['.']['mode'] == mo(value['root_mode']), 'Manifest root mode')
        dirs.add('.')
        for row in value['directories']:
            need(type(row) is dict and set(row) in [{'path', 'mode'}, {'path', 'mode', 'empty'}], 'Directory list row shape')
            name_rel = rel(row['path'])
            need(name_rel not in dirs | files and snapshot['directories'][name_rel]['mode'] == mo(row['mode']), 'Directory path/mode')
            if 'empty' in row:
                need(type(row['empty']) is bool and snapshot['directories'][name_rel]['empty'] == row['empty'], 'Directory emptiness')
            dirs.add(name_rel)
    need(dirs == set(snapshot['directories']), 'Manifest whole directory coverage')
    need(files == (set(snapshot['files']) if controls else set(snapshot['files']) - {name, terminal}), 'Manifest whole file coverage')
    need(not controls or set(controls) == {name, terminal}, 'Terminal row set')
    if 'counts' in value:
        need(value['counts']['payload_regular_files'] == len(files) and value['counts']['directories_including_root'] == len(dirs), 'Manifest count object')
    for key, count in [('file_count', len(files)), ('directory_count', len(dirs)), ('regular_files', snapshot['regular_files']), ('child_directories', snapshot['child_directories']), ('regular_files_after_terminal_creation', snapshot['regular_files'])]:
        if key in value:
            need(type(value[key]) is int and value[key] == count, 'Manifest count: ' + key)
    return {'root': str(root), 'schema': schema, 'manifest': pin(root / name), 'terminal': pin(root / terminal), 'whole_namespace_authenticated': True, 'mode_only_terminal_rows': controls}

class HTML(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags, self.data, self.ids = [], [], []
        self.feed(text)
        self.close()
        need(len(self.ids) == len(set(self.ids)), 'Duplicate HTML ID')
    def handle_starttag(self, tag, attrs):
        need(len([key for key, value in attrs]) == len({key for key, value in attrs}), 'Duplicate HTML attribute')
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
    def handle_data(self, data):
        self.data.append(data)

def visible(text):
    return ' '.join(''.join(HTML(text).data).split())

def only(pattern, text):
    matches = list(re.finditer(pattern, text, re.S))
    need(len(matches) == 1, 'Expected one expression: ' + str(pattern))
    return matches[0]

def scholar(head):
    match = only(r'<script type="application/ld\+json">(.*?)</script>', head)
    value = loads(match[1])
    need(type(value) is dict and value['@type'] == 'ScholarlyArticle' and '@graph' not in value, 'Article actual schema')
    return value

def json_units(text):
    match = only(r'"itemListElement"\s*:\s*\[', text)
    decoder = json.JSONDecoder(object_pairs_hook=pairs)
    pos, raw, typed = match.end(), [], []
    while True:
        while text[pos].isspace():
            pos += 1
        if text[pos] == ']':
            return raw, typed, pos
        start = pos
        value, pos = decoder.raw_decode(text, pos)
        raw.append(text[start:pos])
        typed.append(value)
        while text[pos].isspace():
            pos += 1
        need(text[pos] in ',]', 'JSON list separator')
        if text[pos] == ',':
            pos += 1
            need(text[pos:].lstrip()[0] != ']', 'JSON trailing comma')

def xml_binding_node(node):
    return {'tag': node.tag, 'attributes': dict(node.attrib), 'children': [{'tag': child.tag, 'attributes': dict(child.attrib), 'text': child.text, 'tail': child.tail} for child in node]}

def xml_full_node(node):
    return {'tag': node.tag, 'attributes': dict(node.attrib), 'text': node.text, 'tail': node.tail, 'children': [xml_full_node(child) for child in node]}

def aggregate(index_data, xml_data):
    text, xml = index_data.decode('utf-8'), xml_data.decode('utf-8')
    HTML(text)
    ul = only(r'<ul(?:\s[^>]*)?>(.*?)</ul>', text)
    units = re.findall(r'<li(?:\s[^>]*)?>.*?</li>', ul[1], re.S)
    need(re.sub(r'<li(?:\s[^>]*)?>.*?</li>', '', ul[1], flags=re.S).strip() == '', 'Unexpected HTML list content')
    schema = loads(only(r'<script type="application/ld\+json">(.*?)</script>', text)[1])
    need(type(schema) is dict and schema['@type'] == 'CollectionPage' and schema['mainEntity']['@type'] == 'ItemList', 'Index schema shape')
    raw, typed, end = json_units(text)
    need(schema['mainEntity']['itemListElement'] == typed and type(schema['mainEntity']['numberOfItems']) is int and schema['mainEntity']['numberOfItems'] == len(typed) == len(units), 'Index counts')
    routes = []
    for pos, (unit, item) in enumerate(zip(units, typed), 1):
        need(type(item) is dict and set(item) == {'@type', 'position', 'url', 'name'} and item['@type'] == 'ListItem' and type(item['position']) is int and item['position'] == pos, 'ListItem actual shape')
        tags = HTML(unit).tags
        anchors = [attrs for tag, attrs in tags if tag == 'a']
        need(anchors and type(anchors[0].get('href')) is str, 'Visible route')
        route = anchors[0]['href']
        need(item['url'] == 'https://aleckriebel.com' + route, 'Visible/typed route mismatch')
        routes.append(route)
    need(len(routes) == len(set(routes)) and len([item['url'] for item in typed]) == len(set(item['url'] for item in typed)), 'Duplicate index canonical')
    root = ET.fromstring(xml_data)
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    need(root.tag == ns + 'urlset' and all(node.tag == ns + 'url' for node in root), 'XML namespace/schema')
    raw_xml = re.findall(r'<url(?:\s[^>]*)?>.*?</url>', xml, re.S)
    locations = []
    for node in root:
        need(len(node) == 2 and node[0].tag == ns + 'loc' and node[1].tag == ns + 'lastmod' and not list(node[0]) and not list(node[1]), 'XML node schema')
        locations.append(node[0].text)
    need(len(raw_xml) == len(root) == len(locations) == len(set(locations)), 'XML count/duplicate')
    return {'index_whole_UTF8': text, 'sitemap_whole_UTF8': xml, 'raw_visible_HTML_units': units, 'visible_text_units': [visible(unit) for unit in units], 'visible_text_rule': 'concatenate HTMLParser data events, then whitespace collapse', 'raw_JSON_units': raw, 'typed_ItemList_units': typed, 'raw_XML_units': raw_xml, 'parsed_XML_units': [xml_binding_node(node) for node in root], 'XML_locations': locations, 'counts': {'visible_HTML': len(units), 'raw_JSON': len(raw), 'typed_JSON': len(typed), 'XML': len(root)}}, {'index_schema': schema, 'JSON_list_end_character': end, 'XML_tree': xml_full_node(root), 'visible_routes': routes}

def apply_spans(old, spans):
    previous = 0
    parts = []
    for span in sorted(spans, key=lambda row: row['start_byte']):
        start, end = span['start_byte'], span['end_byte']
        need(type(start) is int and type(end) is int and previous <= start <= end <= len(old), 'Overlapping edit spans')
        need(old[start:end] == span['old_UTF8'].encode(), 'Old edit span mismatch')
        parts.extend([old[previous:start], span['new_UTF8'].encode()])
        previous = end
    parts.append(old[previous:])
    result = b''.join(parts)
    offset, reversed_spans = 0, []
    for span in sorted(spans, key=lambda row: row['start_byte']):
        start = span['start_byte'] + offset
        old_part, new_part = span['old_UTF8'].encode(), span['new_UTF8'].encode()
        need(result[start:start + len(new_part)] == new_part, 'Forward replacement mismatch')
        reversed_spans.append((start, start + len(new_part), old_part))
        offset += len(new_part) - len(old_part)
    reversed_data = result
    for start, end, data in reversed(reversed_spans):
        reversed_data = reversed_data[:start] + data + reversed_data[end:]
    need(reversed_data == old, 'Whole-buffer reversal failed')
    return result

def replace_span(old, old_part, new_part, reason):
    need(old.count(old_part) == 1, 'Nonunique allowed edit: ' + reason)
    start = old.index(old_part)
    return {'start_byte': start, 'end_byte': start + len(old_part), 'old_UTF8': old_part.decode(), 'new_UTF8': new_part.decode(), 'reason': reason}

def activate(article_data, head_data, model):
    head = head_data.decode()
    need(head.startswith('<head>\n') and head.endswith('</head>\n'), 'Accepted wrapped HEAD shape')
    need(only(rb'(<head>.*?</head>\n)', article_data)[1] == head_data, 'Accepted whole HEAD differs')
    schema = scholar(head)
    canonical = model['deployment_proposal']['proposed_canonical_url']
    need(canonical == 'https://aleckriebel.com/research/' + model['deployment_proposal']['slug'] + '/' and not any(key in schema for key in ['@id', 'url', 'mainEntityOfPage']), 'Accepted canonical/identity shape')
    spans = []
    for name in ['robots', 'googlebot']:
        tag = ('<meta name="' + name + '" content="noindex, nofollow">\n').encode()
        spans.append(replace_span(head_data, tag, b'', 'remove exact private ' + name))
    spans.append(replace_span(head_data, b'<meta name="citation_pdf_url" content="assets/paper.pdf">', ('<meta name="citation_pdf_url" content="' + canonical + 'assets/paper.pdf">').encode(), 'absolute citation PDF URL'))
    for encoding in schema['encoding']:
        asset = encoding['contentUrl']
        need(asset == 'assets/' + encoding['name'], 'Encoding source path differs')
        spans.append(replace_span(head_data, ('"contentUrl": "' + asset + '"').encode(), ('"contentUrl": "' + canonical + asset + '"').encode(), 'absolute native encoding ' + encoding['name']))
    stylesheet = b'<link rel="stylesheet" href="/research/research.css">\n'
    inserted = ('<link rel="canonical" href="' + canonical + '">\n<meta property="og:url" content="' + canonical + '">\n').encode()
    need(head_data.count(stylesheet) == 1, 'Shared stylesheet shape')
    place = head_data.index(stylesheet)
    spans.append({'start_byte': place, 'end_byte': place, 'old_UTF8': '', 'new_UTF8': inserted.decode(), 'reason': 'canonical link and OG URL'})
    script = only(rb'<script type="application/ld\+json">(.*?)</script>', head_data)
    place = script.end(1) - 1
    need(head_data[place:place + 1] == b'}', 'Schema final boundary')
    addition = ', "@id": ' + json.dumps(canonical) + ', "url": ' + json.dumps(canonical) + ', "mainEntityOfPage": ' + json.dumps(canonical)
    spans.append({'start_byte': place, 'end_byte': place, 'old_UTF8': '', 'new_UTF8': addition, 'reason': 'three exact canonical string identities'})
    new_head = apply_spans(head_data, spans)
    head_match = only(rb'(<head>.*?</head>\n)', article_data)
    new_article = article_data[:head_match.start(1)] + new_head + article_data[head_match.end(1):]
    actual_schema = scholar(new_head.decode())
    expected_schema = loads(json.dumps(schema))
    expected_schema.update({'@id': canonical, 'url': canonical, 'mainEntityOfPage': canonical})
    for item in expected_schema['encoding']:
        item['contentUrl'] = canonical + item['contentUrl']
    need(actual_schema == expected_schema, 'Unauthorized schema semantic edit')
    need(only(rb'(<body>.*?</body>\n)', new_article)[1] == only(rb'(<body>.*?</body>\n)', article_data)[1], 'Whole BODY drift')
    need(new_article.replace(new_head, head_data, 1) == article_data, 'Article outside HEAD drift')
    return new_article, {'canonical': canonical, 'identity_values': {key: canonical for key in ['@id', 'url', 'mainEntityOfPage']}, 'accepted_head_SHA256': sha(head_data), 'candidate_head_SHA256': sha(new_head), 'spans': sorted(spans, key=lambda row: row['start_byte']), 'whole_HEAD_reverse_exact': True, 'whole_BODY_and_article_outside_HEAD_exact': True}

def local_checks(path, canonical, model):
    text = path.read_text()
    parsed = HTML(text)
    head = only(r'(<head>.*?</head>\n)', text)[1]
    attrs = [row for tag, row in parsed.tags if tag == 'meta']
    need(not any(row.get('name') in ['robots', 'googlebot'] for row in attrs), 'Private robot tag remains')
    need([row['href'] for tag, row in parsed.tags if tag == 'link' and row.get('rel') == 'canonical'] == [canonical], 'Canonical tag count')
    need([row['content'] for row in attrs if row.get('property') == 'og:url'] == [canonical], 'OG canonical count')
    need([row['href'] for tag, row in parsed.tags if tag == 'link' and row.get('rel') == 'stylesheet'] == ['/research/research.css'], 'Stylesheet drift')
    value = scholar(head)
    need(value['abstract'] == model['abstract'] == html.unescape(only(r'<p id="abstract-text">(.*?)</p>', text)[1]), 'Full abstract surfaces')
    need([row['content'] for row in attrs if row.get('name') == 'DC.description'] == [model['abstract']], 'DC abstract')
    need([row['content'] for row in attrs if row.get('name') == 'citation_pdf_url'] == [canonical + 'assets/paper.pdf'], 'Citation PDF destination')
    urls = [item['contentUrl'] for item in value['encoding']]
    need(len(urls) == len(set(urls)), 'Duplicate encoding URL')
    for tag, row in parsed.tags:
        for key in ['aria-labelledby', 'aria-describedby', 'aria-controls']:
            if key in row:
                need(all(ref in parsed.ids for ref in row[key].split()), 'Missing ARIA target')
        for key in ['href', 'src']:
            if key not in row:
                continue
            url = urlsplit(row[key])
            if url.scheme or url.netloc:
                if not row[key].startswith(canonical):
                    continue
                relative = row[key][len(canonical):].split('#')[0]
                target = path.parent / (unquote(relative) or 'index.html')
            elif url.path.startswith('/'):
                if url.path != '/research/research.css':
                    continue
                target = CAND / url.path.lstrip('/')
            elif url.path:
                rel(unquote(url.path))
                target = path.parent / unquote(url.path)
            else:
                target = path
            need(target.is_file(), 'Missing local destination: ' + str(target))
            if url.fragment and target == path:
                need(url.fragment in parsed.ids, 'Missing local fragment')
    for url in urls:
        need(url.startswith(canonical) and (path.parent / url.removeprefix(canonical)).is_file(), 'Encoding destination missing')
    need(any(tag == 'iframe' and row.get('src') == 'assets/paper.pdf#view=FitH' for tag, row in parsed.tags), 'PDF embed path')
    need(any(tag == 'a' and row.get('href') == 'assets/paper.pdf' and 'download' in row for tag, row in parsed.tags) and any(tag == 'a' and row.get('href') == 'assets/paper.pdf' and 'download' not in row for tag, row in parsed.tags), 'PDF open/download paths')
    return {'IDs_attributes_ARIA_fragments_local_Bib_native_PDF_paths': 'PASS', 'all_abstract_surfaces': 'PASS', 'rendered_or_live_certificate': False}

def authenticate(binding, guards):
    need(binding['schema'] == 'independent-hafnian-retract-stage-INITIAL-binding-continuation-inputs-v1' and binding['status'] == 'PASS_INPUT_BINDINGS_ONLY', 'Binding schema/status')
    old = binding['guards_before']
    need(set(old) == {'roots', 'controls', 'public', 'native_M', 'native_W'} and len(old['roots']) == 9 and len(old['controls']) == 6, 'Guard actual schema')
    for root, snapshot in old['roots'].items():
        equal_snapshot(snapshot, guards['roots'][root])
    equal_snapshot(old['public'], guards['public'])
    need(old['controls'] == guards['controls'] and old['native_M'] == guards['native_M'] and old['native_W'] == guards['native_W'], 'Root/native guard differs')
    for path, digest in CONTROL_PINS.items():
        need(guards['stage_control_pins'][str(path)]['SHA256'] == digest, 'Controlling input pin: ' + str(path))
    need(pin(BINDINGS / 'INPUT_BINDINGS.json')['bytes'] == 801813, 'Binding extent')
    contract = readj(INITIAL / 'CONTRACT.json')
    need(len(contract['criteria']) == 28 and [item['id'] for item in contract['criteria']] == ['C' + str(number).zfill(2) for number in range(1, 29)], 'Contract28 differs')
    target = readj(OWN / 'TARGETS.json')
    need(target['Git_relative_targets'] == contract['exact_Git_relative_targets'] == binding['exact_Git_relative_targets'] and target['additions_public_relative'] == binding['new_public_relative_leaves'] and target['new_directories_public_relative'] == contract['new_public_relative_directories'] == binding['new_public_relative_directories'], 'Exact target projection differs')
    need(target['Git_relative_targets'] == ['public/' + name for name in target['additions_public_relative'] + target['modifications_public_relative']] and len(set(target['Git_relative_targets'])) == 11, 'Public prefix/target duplicate')
    for name in target['additions_public_relative'] + target['new_directories_public_relative']:
        rel(name)
        need(not (PUBLIC / name).exists(), 'New target collision')
    need(guards['public']['regular_files'] == 781 and guards['public']['child_directories'] == 377 and guards['public']['directories']['.']['mode'] == '0750' and sum(Path(name).name == '.DS_Store' for name in guards['public']['files']) == 17, 'Baseline extent/mode/DSStore')
    need(sum(guards['roots'][str(P / root)]['regular_files'] for root, *_ in RULES[:6]) == 204 and sum(guards['roots'][str(P / root)]['child_directories'] for root, *_ in RULES[:6]) == 13, 'Private204/13')
    need(sum(guards['roots'][str(P / root)]['regular_files'] for root, *_ in RULES[6:8]) == 153 and sum(guards['roots'][str(P / root)]['child_directories'] for root, *_ in RULES[6:8]) == 22, 'Sources153/22')
    manifest_receipts = []
    for root, manifest, terminal, schema, rows in RULES:
        path = P / root
        manifest_receipts.append(check_manifest(path, guards['roots'][str(path)], manifest, terminal, schema, rows, binding['authenticated_finite_manifests'][str(path)]))
    binding_final = readj(BINDINGS / 'FINAL.json')
    need(binding_final['manifest']['SHA256'] == CONTROL_PINS[BINDINGS / 'OWNED_MANIFEST.json'], 'Binding FINAL manifest pin')
    own_external = {'manifest': pin(BINDINGS / 'OWNED_MANIFEST.json'), 'terminal': pin(BINDINGS / 'FINAL.json')}
    manifest_receipts.append(check_manifest(BINDINGS, guards['binding_lane'], 'OWNED_MANIFEST.json', 'FINAL.json', 'finite-hafnian-retract-stage-INITIAL-bindings-manifest-v1', 'payload_files', own_external))
    need(guards['binding_lane']['regular_files'] == 13 and guards['binding_lane']['child_directories'] == 0, 'Binding lane13/0')
    for filename, accepted in binding['adoptions'].items():
        need(readj(P / 'verification' / filename) == accepted, 'Whole adopted data differs')
    need(guards['native_M']['resolved_native_HEAD'] == 'a4ce3c37dad209339e490d18dcced6c48cf912d2' and guards['native_W']['resolved_native_HEAD'] == '7d5ac8ea5dc8d6cddee457da7a5b40042d36d344', 'Native main/master')
    index = (W / '.git/index').read_bytes()
    need(index[:4] == b'DIRC' and struct.unpack('>II', index[4:12]) == (2, 58721) and len(index) == 9059206 and hashlib.sha1(index[:-20]).digest() == index[-20:] and sha(index) == '592a25281b63a357fbe4fe2580e2c9764ba2b4836650d8751ac573ff8117c365', 'Native W index v2/count/fullchecksum')
    object_receipts = []
    for oid, kind, expected in [(guards['native_W']['resolved_native_HEAD'], 'commit', binding['native_W_commit_body'].encode()), (binding['native_W_commit_tree'], 'tree', bytes.fromhex(binding['native_W_tree_body_hex']))]:
        packed = W / '.git/objects' / oid[:2] / oid[2:]
        data = zlib.decompress(packed.read_bytes())
        header = kind.encode() + b' ' + str(len(expected)).encode() + b'\x00'
        need(data == header + expected and hashlib.sha1(data).hexdigest() == oid, 'Native loose object body/hash')
        object_receipts.append({'oid': oid, 'kind': kind, 'file': pin(packed), 'body_SHA256': sha(expected)})
    writej('INPUT_AUTHENTICATION.json', {'status': 'PASS', 'actual_finite_manifests': manifest_receipts, 'whole_root_adoptions_parsed_equal': True, 'complete_binding801813B_read_authenticated': True, 'full801813B_human_read_claim': False, 'native_index': binding['native_index'], 'native_commit_tree': object_receipts, 'contract28': True, 'source_private_INITIAL_bindings_root_public_native_guards': 'PASS'})
    return target

def build(binding, guards):
    target = authenticate(binding, guards)
    old_index = (PUBLIC / 'research/index.html').read_bytes()
    old_xml = (PUBLIC / 'research/sitemap.xml').read_bytes()
    baseline_units, baseline_extra = aggregate(old_index, old_xml)
    need(baseline_units == binding['aggregate_baseline'], 'Complete baseline aggregate buffers/units differ')
    need(baseline_units['counts'] == {'visible_HTML': 128, 'raw_JSON': 128, 'typed_JSON': 128, 'XML': 129}, 'Baseline aggregate counts')
    write('ORIGINAL_RESEARCH_INDEX.html', old_index)
    write('ORIGINAL_RESEARCH_SITEMAP.xml', old_xml)
    writej('BASELINE_AGGREGATE_UNITS.json', baseline_units)
    shutil.copytree(PUBLIC, BASE, copy_function=shutil.copy2)
    equal_snapshot(guards['public'], inventory(BASE), False)
    shutil.copytree(BASE, CAND, copy_function=shutil.copy2)
    equal_snapshot(guards['public'], inventory(CAND), False)
    writej('BASELINE_MANIFEST.json', inventory(BASE))
    head_receipts, page_receipts, new_units, new_items, canonicals = [], [], [], [], []
    for number, (family, record, slug) in enumerate(FAMILIES, 129):
        writer = P / 'verification' / (family + '-editorial-sol-20261117')
        accepted = next(item for item in binding['pages'] if item['family'] == family)
        model = readj(writer / 'page-model.json')
        need(model['record_id'] == record and model['deployment_proposal']['slug'] == slug and model['follow_up'] is None and model['scientific_clearance']['inherited'] is True and model['publication_authority'] is False, 'Accepted model identity/gates')
        need(all(model[key] is None for key in ['canonical_url', 'base_url', 'production_url', 'actual_publication_date', 'AA']), 'Accepted model actual null fields')
        article_data, head_data, main_data = [(writer / name).read_bytes() for name in ['article.html', 'head.html', 'main.html']]
        need(pin(writer / 'article.html') == accepted['article'] and pin(writer / 'head.html') == accepted['head'] and pin(writer / 'main.html') == accepted['MAIN'] and pin(writer / 'citation.bib') == accepted['Bib'], 'Accepted article fragments/Bib pins')
        need(only(rb'(<main id="main">.*?</main>\n)', article_data)[1] == main_data and scholar(head_data.decode()) == accepted['schema_object'], 'Accepted whole MAIN/schema')
        body = only(rb'(<body>.*?</body>\n)', article_data)[1]
        need(len(body) == accepted['BODY']['bytes'] and sha(body) == accepted['BODY']['SHA256'] and model['abstract'] == accepted['abstract'], 'Accepted whole BODY/abstract')
        need([item['name'] for item in model['native_asset_order']] == accepted['native_encoding_names'], 'Native encoding names/order')
        if family == 'hafnian':
            need(model['native_version'] == '1.0.0', 'Hafnian version')
        else:
            need(model['native_version'] is None and model['native_API_version_field_absent'] is True and model['native_HTML_display_version'] == 'v1' and 'version' not in scholar(head_data.decode()), 'Retract absent API version/qualified host')
        new_article, head_receipt = activate(article_data, head_data, model)
        page_root = CAND / 'research' / slug
        page_root.mkdir(mode=0o755)
        (page_root / 'assets').mkdir(mode=0o755)
        for leaf, data in [('index.html', new_article), ('citation.bib', (writer / 'citation.bib').read_bytes())]:
            with (page_root / leaf).open('xb') as handle:
                handle.write(data)
            os.chmod(page_root / leaf, 0o644)
        assets = []
        for asset in accepted['assets']:
            source = writer / asset['relative_path']
            need(pin(source) == {key: asset[key] for key in ['bytes', 'SHA256', 'mode']}, 'Accepted asset pin')
            for native_name in asset['native_source_matches']:
                need(pin(P / 'papers' / record / 'sources' / native_name) == pin(source), 'Native asset buffer/mode differs')
            shutil.copy2(source, page_root / asset['relative_path'])
            need(pin(page_root / asset['relative_path']) == pin(source), 'Candidate native asset differs')
            assets.append({'path': asset['relative_path'], **pin(source), 'MD5': hashlib.md5(source.read_bytes()).hexdigest()})
        canonical = model['deployment_proposal']['proposed_canonical_url']
        canonicals.append(canonical)
        route = model['deployment_proposal']['path']
        entry = only(r'<p class="entry-meta">(.*?)</p>', main_data.decode())[1]
        need(entry.count('</a> · ') == 1, 'Accepted entry metadata shape')
        metadata = entry.split('</a> · ', 1)[1]
        unit = '<li><a href="' + route + '">' + html.escape(model['title']) + '</a><br><span class="entry-meta">' + metadata + '</span><p>' + html.escape(model['meta_description']) + '</p><p><a href="' + route + 'assets/paper.pdf">PDF</a> · <a href="' + model['doi_url'] + '">Zenodo</a></p></li>'
        new_units.append(unit)
        new_items.append({'@type': 'ListItem', 'position': number, 'url': canonical, 'name': model['title']})
        head_receipts.append({'family': family, **head_receipt})
        page_receipts.append({'record': record, 'slug': slug, 'accepted_model': pin(writer / 'page-model.json'), 'candidate_article': pin(page_root / 'index.html'), 'Bib': pin(page_root / 'citation.bib'), 'whole_MAIN_SHA256': sha(main_data), 'whole_BODY_SHA256': sha(body), 'unchanged_native_assets': assets, 'static': local_checks(page_root / 'index.html', canonical, model), 'private_model_unchanged_and_not_copied_to_production': True})
    need(len(set(canonicals)) == 2 and not set(canonicals) & set(baseline_units['XML_locations']), 'New canonical duplicate')
    count = only(rb'"numberOfItems"\s*:\s*(128)(?=\s*[,}])', old_index)
    list_end = len(old_index.decode()[:baseline_extra['JSON_list_end_character']].encode())
    ul_end = only(rb'</ul>', old_index).start()
    index_spans = [{'start_byte': count.start(1), 'end_byte': count.end(1), 'old_UTF8': '128', 'new_UTF8': '130', 'reason': 'JSON count128to130'},
                   {'start_byte': list_end, 'end_byte': list_end, 'old_UTF8': '', 'new_UTF8': ', ' + ', '.join(json.dumps(item, ensure_ascii=False) for item in new_items), 'reason': 'append raw ListItems129and130'},
                   {'start_byte': ul_end, 'end_byte': ul_end, 'old_UTF8': '', 'new_UTF8': '\n'.join(new_units) + '\n', 'reason': 'append two whole visible li units'}]
    new_index = apply_spans(old_index, index_spans)
    xml_end = only(rb'</urlset>', old_xml).start()
    new_xml_units = ['<url><loc>' + canonical + '</loc><lastmod>2026-11-17</lastmod></url>' for canonical in canonicals]
    xml_spans = [{'start_byte': xml_end, 'end_byte': xml_end, 'old_UTF8': '', 'new_UTF8': '\n'.join(new_xml_units) + '\n', 'reason': 'append two canonical XML nodes'}]
    new_xml = apply_spans(old_xml, xml_spans)
    for relative, data in [('research/index.html', new_index), ('research/sitemap.xml', new_xml)]:
        (CAND / relative).write_bytes(data)
        os.chmod(CAND / relative, int(guards['public']['files'][relative]['mode'], 8))
    candidate_units, candidate_extra = aggregate(new_index, new_xml)
    for key in ['raw_visible_HTML_units', 'visible_text_units', 'raw_JSON_units', 'typed_ItemList_units', 'raw_XML_units', 'parsed_XML_units', 'XML_locations']:
        old_items = baseline_units[key]
        need(candidate_units[key][:len(old_items)] == old_items, 'Old whole ordered prefix differs: ' + key)
    need(candidate_units['raw_visible_HTML_units'][128:] == new_units and candidate_units['typed_ItemList_units'][128:] == new_items and candidate_units['raw_XML_units'][129:] == new_xml_units and candidate_units['XML_locations'][129:] == canonicals, 'New aggregate units differ')
    expected_index_schema = loads(json.dumps(baseline_extra['index_schema']))
    expected_index_schema['mainEntity']['numberOfItems'] = 130
    expected_index_schema['mainEntity']['itemListElement'] += new_items
    need(candidate_extra['index_schema'] == expected_index_schema and candidate_extra['XML_tree']['attributes'] == baseline_extra['XML_tree']['attributes'] and candidate_extra['XML_tree']['children'][:129] == baseline_extra['XML_tree']['children'], 'Aggregate wrapper/full XML node drift')
    need(candidate_units['counts'] == {'visible_HTML': 130, 'raw_JSON': 130, 'typed_JSON': 130, 'XML': 131}, 'Candidate aggregate counts')
    base_snapshot, candidate_snapshot = inventory(BASE), inventory(CAND)
    equal_snapshot(guards['public'], base_snapshot, False)
    additions = sorted(set(candidate_snapshot['files']) - set(base_snapshot['files']))
    deletions = sorted(set(base_snapshot['files']) - set(candidate_snapshot['files']))
    changed = sorted(name for name in base_snapshot['files'] if name in candidate_snapshot['files'] and base_snapshot['files'][name] != candidate_snapshot['files'][name])
    new_dirs = sorted(set(candidate_snapshot['directories']) - set(base_snapshot['directories']))
    need(additions == sorted(target['additions_public_relative']) and not deletions and changed == sorted(target['modifications_public_relative']) and new_dirs == sorted(target['new_directories_public_relative']), 'Exact9A2M/fourdir projection')
    need(candidate_snapshot['regular_files'] == 790 and candidate_snapshot['child_directories'] == 381, 'Candidate790/381')
    for name, row in base_snapshot['directories'].items():
        need(candidate_snapshot['directories'][name] == row, 'Old directory mode/topology/emptiness differs')
    need(all(candidate_snapshot['directories'][name] == {'mode': '0755', 'empty': False} for name in new_dirs) and all(candidate_snapshot['files'][name]['mode'] == '0644' for name in additions), 'New modes/topology')
    need(sum(Path(name).name == '.DS_Store' for name in candidate_snapshot['files']) == 17, 'DSStore custody')
    for route in candidate_extra['visible_routes'][128:]:
        need((CAND / route.lstrip('/') / 'index.html').is_file(), 'New index canonical route missing')
    writej('CANDIDATE_MANIFEST.json', candidate_snapshot)
    writej('CANDIDATE_AGGREGATE_UNITS.json', candidate_units)
    writej('HEAD_ACTIVATION.json', {'schema': 'exact-private-stage-head-activation-v1', 'pages': head_receipts, 'only_root_authorized_HEAD_spans': True, 'accepted_whole_BODY_MAIN_Bib_assets_unchanged': True})
    writej('AGGREGATE_FIDELITY.json', {'schema': 'whole-buffer-reversible-aggregate-fidelity-v1', 'baseline_index': pin(BASE / 'research/index.html'), 'candidate_index': pin(CAND / 'research/index.html'), 'baseline_XML': pin(BASE / 'research/sitemap.xml'), 'candidate_XML': pin(CAND / 'research/sitemap.xml'), 'index_spans': sorted(index_spans, key=lambda row: row['start_byte']), 'XML_spans': xml_spans, 'whole_old_buffers_saved': ['ORIGINAL_RESEARCH_INDEX.html', 'ORIGINAL_RESEARCH_SITEMAP.xml'], 'whole_byte_reversal_both': True, 'old128whole_rawHTML_visible_rawJSON_typed_and129XML_prefix_exact': True, 'old_full_XML_node_trees_attributes_text_tails_exact': True, 'new_order': ['23205294', '23203270'], 'new_visible_units': new_units, 'new_typed_units': new_items, 'new_XML_units': new_xml_units, 'no_aggregate_reserialization': True})
    projection = {'schema': 'exact-observed-private-stage-projection-v1', 'Git_relative_targets': ['public/' + name for name in target['additions_public_relative'] + target['modifications_public_relative']], 'additions_public_relative': additions, 'modifications_public_relative': changed, 'deletions': deletions, 'new_directories_public_relative': new_dirs, 'additions': 9, 'modifications': 2, 'old_untargeted_files_exact': 779, 'old_directory_modes_topology_exact': 377, 'baseline': [781, 377, 128, 129], 'candidate': [790, 381, 130, 131], 'old_and_new_DSStore_count': 17, 'pages': page_receipts, 'private_stage_authority_only': True, 'publication_authority': False}
    writej('PROJECTION.json', projection)
    return projection

def freeze(projection, execution):
    now = utc()
    with (OWN / 'RESEARCH_LOG.md').open('a') as handle:
        handle.write('\n- ' + now + ' — 100% complete toward the private staged handoff. One fully saved/read own data build exited0; literal stdout/stderr empty. Current baseline781/377 was completely cloned and authenticated; candidate790/381 has130indexunits/131XMLnodes, exactly9A2M11Gitpaths/fournewdirs. Both entire accepted BODY/MAIN/abstract/Bib and five original assets remain exact; only documented HEAD activation spans changed. All old128whole rawHTML/visible/rawJSON/typed units and129raw/parsedXML nodes remain an ordered prefix, with full-buffer reversible proofs. Both source153/22, private204/13, INITIAL14, correctedbindings13, root/nativeM/W/public guards are unchanged. Math remote/FETCH metadata is separately observed. No old helper, source/science, imports/AST/compiler/test, Git/network/W/install/production/Sheet/AA/deploy/redirect/outreach/child/otherpacket writes. Finite complete stage custody is frozen for independent implementation audit/root adoption; no live/rendered or publication authority.\n')
    write('REPORT.md', ('# Private stage result\n\nPASS for the bounded producer checks. Completion100%; independent implementation audit/root adoption remains separate. The actual candidate has790regular files/381child directories,130research entries and131sitemap nodes. Exactly9additions/2aggregate modifications/fournew directories are observed; all779other baseline files and377old directory modes/topology remain exact, including17 .DS_Store files and all hidden/ignored/empty objects.\n\nBoth accepted whole BODY/MAIN/abstracts, Bibs and five native files remain byte/mode exact. Only the recorded root-authorized HEAD spans activate canonical/OG/scholar identities and absolute PDF/encoding URLs and remove the exact private robots tags. The unchanged private models remain input data; their null actual-publication/AA/follow-up gates are not converted to publication claims. Native versions, edition qualification, rights, status and attribution are retained. Shared CSS is unchanged.\n\nThe complete old index/XML buffers and all old rawHTML/visible/rawJSON/typed/XML units are separately saved, preserved as ordered prefixes and restored by reversing the exact saved edit spans. No aggregate was regenerated or reserialized. Duplicate-aware JSON/HTML and complete snapshot/manifest schema/path/parent/mode/count validation ran before equality comparisons.\n\nComplete before/after source153/22, private204/13, INITIAL14/0, bindings13/0, root controls, native Math/W local controls and Wpublic guards match. Remote/FETCH observations are separate. One saved/read own standard-library data producer ran, with literal empty streams and exit0. No source/scientific/archived/helper/import/AST/compiler/test/Git/network/website/production/stage-sibling/Sheet/deploy/AA/redirect/child/contact/outreach activity occurred. Static results are not a rendered-reader, live-site, fresh science/copy/priority or production certificate.\n\nAll actual owned hidden/empty bytes, modes and topology are sealed. Only the exactly created FINAL.json and OWNED_MANIFEST.json terminal controls are excluded from recursive hashes; root handoff supplies their external pins. No further writes are authorized in this frozen lane.\n').encode())
    writej('BUILD_EXECUTION.json', execution)
    for name in TERMINALS:
        write(name, b'')
    snapshot = inventory(OWN)
    need(all(snapshot['files'][name]['bytes'] == 0 for name in TERMINALS), 'Terminal placeholders not empty')
    payload = {name: row for name, row in snapshot['files'].items() if name not in TERMINALS}
    manifest = {'schema': 'finite-hafnian-retract-private-stage-manifest-v1', 'UTC': now, 'root': str(OWN), 'root_mode': snapshot['directories']['.']['mode'], 'regular_files': snapshot['regular_files'], 'child_directories': snapshot['child_directories'], 'payload_files': [{'path': name, **row, 'hidden': any(part.startswith('.') for part in Path(name).parts), 'empty': row['bytes'] == 0} for name, row in payload.items()], 'directories': [{'path': name, **row, 'hidden': any(part.startswith('.') for part in Path(name).parts if part != '.')} for name, row in snapshot['directories'].items()], 'exact_already_created_terminal_recursive_hash_exclusions': [str(OWN / name) for name in TERMINALS], 'other_exclusions': [], 'all_hidden_ignored_empty_bytes_modes_topology_included': True, 'no_future_subtree_or_basename_exclusions': True, 'terminal_modes': {name: '0644' for name in TERMINALS}}
    (OWN / 'OWNED_MANIFEST.json').write_bytes((json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode())
    final = {'schema': 'private-hafnian-retract-stage-final-v1', 'UTC': now, 'status': 'PASS_PRIVATE_STAGE_FROZEN_AWAITING_INDEPENDENT_IMPLEMENTATION_AUDIT', 'completion_percent_private_stage': 100, 'root': str(OWN), 'records': ['23205294', '23203270'], 'manifest': pin(OWN / 'OWNED_MANIFEST.json'), 'extent': {'regular_files': snapshot['regular_files'], 'child_directories': snapshot['child_directories'], 'root_mode': snapshot['directories']['.']['mode']}, 'baseline': {'files': 781, 'child_directories': 377, 'root_mode': '0750', 'index_items': 128, 'XML_nodes': 129}, 'candidate': {'files': 790, 'child_directories': 381, 'root_mode': '0750', 'index_items': 130, 'XML_nodes': 131}, 'projection': {'Git_targets': 11, 'additions': 9, 'modifications': 2, 'new_directories': 4}, 'whole_old128index_and129XML_units_and_full_aggregate_reversal': True, 'whole_accepted_BODY_MAIN_abstract_Bib_native_assets_unchanged': True, 'only_authorized_HEAD_activation': True, 'source153_22_private204_13_INITIAL14_bindings13_root_native_M_W_public_guards_exact': True, 'execution': execution, 'artifacts': {name: pin(OWN / name) for name in ['PLAN.md', 'TARGETS.json', 'build_private.py', 'INPUT_AUTHENTICATION.json', 'BASELINE_MANIFEST.json', 'CANDIDATE_MANIFEST.json', 'AGGREGATE_FIDELITY.json', 'HEAD_ACTIVATION.json', 'PROJECTION.json', 'GUARDS_BEFORE.json', 'GUARDS_AFTER.json', 'REMOTE_BEFORE.json', 'REMOTE_AFTER.json', 'REPORT.md', 'READ_LEDGER.json', 'BUILD_EXECUTION.json']}, 'source_scientific_or_archived_or_old_helper_execution_import_AST_compile_test': False, 'Git_network_W_source_otherpacket_mutations_children_contact_outreach': False, 'scientific_and_copy_clearance_inherited': True, 'new_scientific_copy_priority_formal_human_rendered_live_certificate': False, 'publication_authority': False, 'AA': None, 'follow_up': None, 'exact_already_created_terminal_recursive_hash_exclusions': [str(OWN / name) for name in TERMINALS], 'terminal_external_pins_required_at_handoff': True, 'all_handles_terminal_at_return': True, 'frozen_no_further_writes': True, 'remaining_gap': 'Independent implementation audit/root adoption. Any W installation/publication requires a separately authorized later lane.'}
    (OWN / 'FINAL.json').write_bytes((json.dumps(final, ensure_ascii=False, indent=2) + '\n').encode())

def main():
    start, tick = utc(), time.monotonic()
    binding, before, projection, error = None, None, None, None
    try:
        need(not BASE.exists() and not CAND.exists() and not (OWN / 'BUILD_EXECUTION.json').exists() and not any((OWN / name).exists() for name in TERMINALS), 'Private build already attempted')
        need(pin(BINDINGS / 'INPUT_BINDINGS.json')['SHA256'] == CONTROL_PINS[BINDINGS / 'INPUT_BINDINGS.json'], 'Binding pin before parsing')
        binding = readj(BINDINGS / 'INPUT_BINDINGS.json')
        before = capture(binding)
        writej('GUARDS_BEFORE.json', before)
        writej('REMOTE_BEFORE.json', observe_remote())
        projection = build(binding, before)
    except BaseException as exc:
        error = str(exc)
        traceback.print_exc(file=sys.stderr)
    finally:
        if binding is not None:
            try:
                after = capture(binding)
                writej('GUARDS_AFTER.json', after)
                writej('REMOTE_AFTER.json', observe_remote())
                need(before is not None and after == before, 'Complete before/after guarded data differs')
            except BaseException as exc:
                error = (error + '; ' if error else '') + str(exc)
                traceback.print_exc(file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()
    execution = {'schema': 'one-private-data-build-execution-v1', 'invocations': 1, 'argv': [sys.executable, '-I', '-B', str(OWN / 'build_private.py')], 'UTC_start': start, 'UTC_end': utc(), 'elapsed_seconds': time.monotonic() - tick, 'exit_code': 1 if error else 0, 'stdout': pin(OWN / 'BUILD.stdout.txt'), 'stderr': pin(OWN / 'BUILD.stderr.txt'), 'error': error, 'retry_or_repair': False}
    if error:
        writej('BUILD_EXECUTION.json', execution)
        with (OWN / 'RESEARCH_LOG.md').open('a') as handle:
            handle.write('\n- ' + utc() + ' — Private build stopped on its first unexpected failure. Literal streams/exit/time and available before/closing guards are retained; no retry/repair/cleanup. Completion estimate60%; exact failure: ' + error + '\n')
        return 1
    try:
        freeze(projection, execution)
    except BaseException as exc:
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        writej('FREEZE_FAILURE.json', {'UTC': utc(), 'actual_process_exit': 1, 'error': str(exc), 'literal_stderr': pin(OWN / 'BUILD.stderr.txt'), 'retry_or_repair': False, 'prior_receipts_are_retained': True})
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
