"""One independent passive audit; writes only its own fresh audit directory."""
from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
from datetime import datetime, timezone
import copy
import os
import subprocess
import hashlib
import json
import re
import stat
import struct
import zlib
import xml.etree.ElementTree as ET

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M = P.parent
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
S = P / 'verification/mink-riesz-k3-stage-sol-20261117'
A = P / 'verification/mink-riesz-k3-postpublication-sol-20261117'
T = P / 'verification/mink-riesz-k3-stage-audit-continuation-sol-20261117'
E = P / 'verification/root-mink-riesz-k3-audit-pdf-fragment-diagnosis-20261117.json'
O = P / 'verification/mink-riesz-k3-stage-audit-sol-20261117'
D = P / 'verification/root-mink-riesz-k3-audit-head-diagnosis-20261117.json'
BASE = S / 'baseline-public'
CAND = S / 'candidate-public'
PINS = {
    'FINAL.json': (12937, '2aa8bb250f77212d60903f69f64390f86a8ce7544218453b2d169c957d8e588f'),
    'OWNED_MANIFEST.json': (583387, 'cd6b884ff5efce7c5873307cdc7bf308b72c801c3ba5868660ba261dcc22c8dc'),
}
FAMILIES = [('even-minkowski', '23203081'), ('riesz-surface', '23202994'),
            ('mixed-k3-moduli', '23204176')]
CHECKS = []
DETAIL = {}

def utc():
    return datetime.now(timezone.utc).isoformat()

def require(ok, label):
    if not ok:
        raise AssertionError(label)
    CHECKS.append(label)

def write(name, value):
    path = A / name
    require(path.parent == A and not path.exists(), 'fresh own output: ' + name)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def load(path):
    return json.loads(path.read_text())

def mode(value):
    return format(int(value, 8), '04o')

def pin(path):
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), 'regular pinned file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(),
            'mode': format(stat.S_IMODE(st.st_mode), '04o')}

def relative(value):
    q = PurePosixPath(value)
    require(not q.is_absolute() and str(q) == value and '..' not in q.parts,
            'canonical relative path: ' + value)
    return value

def snap(root):
    files, dirs, seen = {}, {}, set()
    def visit(path, rel):
        st = path.lstat()
        require((st.st_dev, st.st_ino) not in seen, 'no object aliases: ' + str(path))
        seen.add((st.st_dev, st.st_ino))
        require(stat.S_ISDIR(st.st_mode), 'real directory: ' + str(path))
        children = sorted(path.iterdir(), key=lambda x: x.name)
        dirs[rel] = {'mode': format(stat.S_IMODE(st.st_mode), '04o'), 'empty': not children}
        for child in children:
            r = child.relative_to(root).as_posix()
            relative(r)
            cst = child.lstat()
            if stat.S_ISDIR(cst.st_mode):
                visit(child, r)
            else:
                require(stat.S_ISREG(cst.st_mode), 'no symlink or special object: ' + str(child))
                require((cst.st_dev, cst.st_ino) not in seen, 'no file aliases: ' + str(child))
                seen.add((cst.st_dev, cst.st_ino))
                files[r] = pin(child)
    visit(root, '.')
    return {'root': str(root), 'files': files, 'directories': dirs,
            'regular_files': len(files), 'child_directories': len(dirs) - 1}

def same_tree(a, b):
    return all(a[k] == b[k] for k in ['files', 'directories', 'regular_files', 'child_directories'])

def verify_pin(path, expected, label):
    actual = pin(path)
    expected_sha = expected.get('SHA256', expected.get('sha256'))
    expected_mode = expected.get('mode', expected.get('mode_octal'))
    if 'bytes' in expected:
        require(actual['bytes'] == expected['bytes'], label + ' bytes')
    require(expected_sha is not None and actual['SHA256'] == expected_sha, label + ' SHA256')
    if expected_mode is not None:
        require(actual['mode'] == mode(expected_mode), label + ' mode')
    md5 = expected.get('MD5', expected.get('md5'))
    if md5 is not None:
        require(hashlib.md5(path.read_bytes()).hexdigest() == md5, label + ' MD5')

def native(root):
    git = root / '.git'
    require(git.is_dir() and not git.is_symlink(), 'native .git directory ' + str(root))
    head = (git / 'HEAD').read_text()
    packed = git / 'packed-refs'
    lines = [x for x in packed.read_text().splitlines(keepends=True)
             if re.fullmatch(r'[0-9a-f]{40} refs/heads/[^\n]+\n?', x)] if packed.exists() else []
    branch = head.strip().removeprefix('ref: ')
    require(head.startswith('ref: refs/heads/'), 'native branch HEAD ' + str(root))
    loose = git / branch
    heads = {x.split()[1]: x.split()[0] for x in lines}
    resolved = loose.read_text().strip() if loose.exists() else heads[branch]
    return {'HEAD': pin(git / 'HEAD'), 'index': pin(git / 'index'), 'config': pin(git / 'config'),
            'HEAD_text': head, 'local_loose_heads': snap(git / 'refs/heads'),
            'packed_local_heads': {'file_mode': pin(packed)['mode'], 'raw_lines': lines} if packed.exists() else None,
            'resolved_native_HEAD': resolved,
            'optional_worktree_config': pin(git / 'config.worktree') if (git / 'config.worktree').exists() else None}

def protected(guard):
    return {'schema': guard['schema'],
            'roots': {r: snap(Path(r)) for r in guard['roots']},
            'controls': {r: pin(Path(r)) for r in guard['controls']},
            'public': snap(W / 'public'), 'native_M': native(M), 'native_W': native(W)}

def hidden(path):
    return any(x.startswith('.') for x in PurePosixPath(path).parts if x != '.')

def verify_stage(snapshot):
    for name, (size, sha) in PINS.items():
        require(pin(S / name) == {'bytes': size, 'SHA256': sha, 'mode': '0644'},
                'external stage terminal pin: ' + name)
    manifest = load(S / 'OWNED_MANIFEST.json')
    final = load(S / 'FINAL.json')
    require((snapshot['regular_files'], snapshot['child_directories']) == (1635, 770), 'stage 1635/770')
    require(snapshot['directories']['.']['mode'] == '0755', 'stage root 0755')
    excluded = manifest['exact_already_created_terminal_recursive_hash_exclusions']
    require(set(excluded) == {str(S / x) for x in PINS} and not manifest['other_exclusions'],
            'only exact stage terminal circular pair excluded')
    rows = manifest['payload_files']
    require(len({x['path'] for x in rows}) == len(rows), 'stage manifest unique files')
    require(set(snapshot['files']) == {x['path'] for x in rows} | set(PINS), 'whole stage file namespace')
    for row in rows:
        r = relative(row['path'])
        verify_pin(S / r, row, 'stage payload ' + r)
        require(row['hidden'] == hidden(r) and row['empty'] == (row['bytes'] == 0), 'stage hidden/empty ' + r)
    directory_rows = {x['path']: {'mode': mode(x['mode']), 'empty': x['empty']} for x in manifest['directories']}
    require(len(directory_rows) == len(manifest['directories']) and directory_rows == snapshot['directories'],
            'stage complete root-inclusive directory modes and empty topology')
    require(all(x['hidden'] == hidden(x['path']) for x in manifest['directories']), 'stage hidden directory flags')
    require(final['manifest'] == pin(S / 'OWNED_MANIFEST.json'), 'FINAL binds actual manifest')
    require(final['follow_up'] is None and final['AA'] is None and final['actual_publication_date'] is None,
            'stage no follow-up AA or publication date')
    for name, value in final['artifacts'].items():
        verify_pin(S / relative(name), value, 'FINAL artifact ' + name)
    require(Counter(x['mode'] for x in snapshot['files'].values()) ==
            Counter({'0644': 1583, '0600': 48, '0666': 4}), 'stage actual all-file mode counts')
    return final

def verify_manifest(info, snapshots):
    root = Path(info['root'])
    current = snapshots[str(root)]
    for name, key in [(info['manifest'], 'manifest_pin'), (info['terminal'], 'terminal_pin')]:
        verify_pin(root / name, info[key], 'authenticated control ' + str(root / name))
    d = load(root / info['manifest'])
    require(d.get('schema') == info['actual_schema'], 'actual manifest schema ' + str(root))
    excluded = d[info['exclusion_key']]
    require(set(excluded) == {info['manifest'], info['terminal']}, 'exact manifest terminal pair ' + str(root))
    file_rows, dir_rows = {}, {}
    for row in d[info['row_table']]:
        r = relative(row['path'])
        target = dir_rows if row.get('kind') == 'directory' else file_rows
        require(r not in target, 'manifest unique object ' + str(root / r))
        target[r] = row
    for row in d.get('directories', []):
        require(row['path'] not in dir_rows, 'distinct manifest directory table ' + str(root / row['path']))
        dir_rows[row['path']] = row
    require(set(file_rows) | set(excluded) == set(current['files']), 'manifest complete file topology ' + str(root))
    require(set(dir_rows) | {'.'} == set(current['directories']), 'manifest complete directory topology ' + str(root))
    if 'root_mode' in d:
        require(mode(d['root_mode']) == current['directories']['.']['mode'], 'manifest root mode ' + str(root))
    for r, row in dir_rows.items():
        require(mode(row.get('mode', row.get('mode_octal'))) == current['directories'][r]['mode'], 'manifest directory mode ' + str(root / r))
        if 'empty' in row:
            require(row['empty'] == current['directories'][r]['empty'], 'manifest directory emptiness ' + str(root / r))
    for r, row in file_rows.items():
        if r in excluded:
            require(mode(row.get('mode', row.get('mode_octal'))) == current['files'][r]['mode'], 'terminal mode ' + str(root / r))
            if 'bytes' in row:
                require(row['bytes'] == current['files'][r]['bytes'], 'terminal length ' + str(root / r))
        else:
            verify_pin(root / r, row, 'manifest payload ' + str(root / r))
    return {'root': str(root), 'schema': d.get('schema'), 'files': current['regular_files'],
            'child_directories': current['child_directories'], 'row_table': info['row_table'],
            'exclusion_key': info['exclusion_key'], 'terminal_pins_checked': True}

def verify_adoptions(auth, snapshots):
    for row in auth['root_adoptions']:
        verify_pin(Path(row['path']), row['pin'], 'actual root adoption')
    mink, riesz, k3 = [load(Path(x['path'])) for x in auth['root_adoptions']]
    require(mink['schema'] == 'root-even-minkowski-private-editorial-adoption-v1' and
            mink['status'] == 'ACCEPTED_PRIVATE_COPY_ONLY', 'Mink actual adoption status')
    for row in mink['finite_authentication']:
        root = P / row['root']
        current = snapshots[str(root)]
        require(set(current['files']) == {x['path'] for x in row['file_pins']}, 'Mink adoption whole file list ' + str(root))
        require((current['regular_files'], current['child_directories']) == (row['files'], row['child_directories']), 'Mink adoption counts ' + str(root))
        for f in row['file_pins']:
            verify_pin(root / f['path'], f, 'Mink adopted file ' + str(root / f['path']))
    def objects(root, table):
        current = snapshots[str(root)]
        require(len(table) == len(set(table)), 'adoption object uniqueness ' + str(root))
        require(set(table) == set(current['files']) | set(current['directories']), 'adoption full objects ' + str(root))
        for r, f in table.items():
            if f['kind'] == 'directory':
                require(mode(f['mode']) == current['directories'][r]['mode'], 'adoption directory ' + str(root / r))
            else:
                require(f['kind'] == 'file', 'adoption only ordinary objects ' + str(root / r))
                verify_pin(root / r, f, 'adopted file ' + str(root / r))
    require(riesz['schema'] == 'root-riesz-private-editorial-adoption-v1' and
            riesz['status'] == 'ACCEPTED_PRIVATE_COPY_ONLY', 'Riesz actual adoption status')
    for row in riesz['finite_authentication']:
        objects(P / row['root'], row['complete_fresh_tree'])
    objects(P / 'papers/23202994/sources', riesz['source_full_exact'])
    require('schema' not in k3 and k3['status'] == 'PRIVATE_EDITORIAL_ACCEPTED_FOR_SEPARATE_STAGING', 'K3 actual heterogeneous adoption status')
    for row in k3['authenticated']:
        require(len(row['objects']) == len({x['path'] for x in row['objects']}), 'K3 unique mixed objects')
        objects(P / row['root'], {x['path']: x for x in row['objects']})
    require(all(x['follow_up'] is None and x['AA'] is None for x in [mink, riesz, k3]), 'adoptions no follow-up or AA')

class HTML(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.data, self.elements, self.ids = [], [], []
        self.feed(text)
        self.close()
    def handle_data(self, data):
        self.data.append(data)
    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))
        if dict(attrs).get('id'):
            self.ids.append(dict(attrs)['id'])
    handle_startendtag = handle_starttag

def json_script(text):
    matches = re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', text, re.S)
    require(len(matches) == 1, 'exactly one JSON-LD script')
    return matches[0], json.loads(matches[0])

def edit(old, spans):
    cursor, parts, reverse = 0, [], []
    offset = 0
    for span in sorted(spans, key=lambda x: (x['start_byte'], x['end_byte'])):
        lo, hi = span['start_byte'], span['end_byte']
        a, b = span['old_UTF8'].encode(), span['new_UTF8'].encode()
        require(cursor <= lo <= hi <= len(old) and old[lo:hi] == a, 'closed span original bytes')
        parts.extend([old[cursor:lo], b])
        reverse.append((lo + offset, lo + offset + len(b), b, a))
        offset += len(b) - len(a)
        cursor = hi
    parts.append(old[cursor:])
    new = b''.join(parts)
    back, cursor = [], 0
    for lo, hi, a, b in reverse:
        require(new[lo:hi] == a and cursor <= lo, 'closed reverse span bytes')
        back.extend([new[cursor:lo], b])
        cursor = hi
    back.append(new[cursor:])
    require(b''.join(back) == old, 'whole original reverse reconstruction')
    return new

def span_once(old, token, replacement):
    require(old.count(token) == 1, 'unique independent HEAD token ' + token.decode()[:60])
    pos = old.index(token)
    return {'start_byte': pos, 'end_byte': pos + len(token),
            'old_UTF8': token.decode(), 'new_UTF8': replacement.decode()}

def article(family, record, activation):
    root = P / ('verification/' + family + '-editorial-sol-20261117')
    model = load(root / 'page-model.json')
    native_data = load(P / ('papers/' + record + '/sources/native-metadata/record-api.json'))
    slug = model['deployment_proposal']['slug']
    canonical = 'https://aleckriebel.com/research/' + slug + '/'
    current = CAND / ('research/' + slug)
    old = (root / 'article.html').read_bytes()
    new = (current / 'index.html').read_bytes()
    head = (root / 'head.html').read_bytes()
    require(old.count(head) == 1 and old.count((root / 'main.html').read_bytes()) == 1, 'accepted whole HEAD/MAIN assembly ' + record)
    spans = [span_once(head, b'<meta name="robots" content="noindex, nofollow">\n', b''),
             span_once(head, b'<meta name="googlebot" content="noindex, nofollow">\n', b''),
             span_once(head, b'<meta name="citation_pdf_url" content="assets/paper.pdf">',
                       ('<meta name="citation_pdf_url" content="' + canonical + 'assets/paper.pdf">').encode())]
    script_token = b'<script type="application/ld+json">'
    require(head.count(script_token) == 1, 'unique original article JSON script ' + record)
    style_token = b'<link rel="stylesheet" href="/research/research.css">\n'
    require(head.count(style_token) == 1, 'unique unchanged approved stylesheet anchor ' + record)
    pos = head.index(style_token)
    spans.append({'start_byte': pos, 'end_byte': pos, 'old_UTF8': '',
                  'new_UTF8': '<link rel="canonical" href="' + canonical + '">\n<meta property="og:url" content="' + canonical + '">\n'})
    assets = model['native_asset_order']
    require([x['name'] for x in assets] == [x['key'] for x in native_data['files']], 'native asset ordering ' + record)
    for asset, original in zip(assets, native_data['files']):
        name = asset['name']
        spans.append(span_once(head, ('"contentUrl": "assets/' + name + '"').encode(),
                               ('"contentUrl": "' + canonical + 'assets/' + name + '"').encode()))
        a = current / asset['local_path']
        verify_pin(a, asset, 'new native asset ' + record + '/' + name)
        require(a.read_bytes() == (root / asset['local_path']).read_bytes() ==
                (P / ('papers/' + record + '/sources/zenodo-files/' + name)).read_bytes(), 'whole triple native asset ' + record + '/' + name)
        require(original['checksum'] == 'md5:' + hashlib.md5(a.read_bytes()).hexdigest() and
                original['size'] == len(a.read_bytes()), 'native API asset checksum ' + record + '/' + name)
    pos = head.rindex(b'}</script>')
    spans.append({'start_byte': pos, 'end_byte': pos, 'old_UTF8': '', 'new_UTF8':
                  ', "@id": "' + canonical + '", "url": "' + canonical + '", "mainEntityOfPage": "' + canonical + '"'})
    expected_head = edit(head, spans)
    require(new == old.replace(head, expected_head), 'WHOLE article exact outside independently derived HEAD spans ' + record)
    require([{k: x[k] for k in ['start_byte', 'end_byte', 'old_UTF8', 'new_UTF8']} for x in activation['spans']] ==
            sorted(spans, key=lambda x: (x['start_byte'], x['end_byte'])), 'producer HEAD span evidence agrees with independent list ' + record)
    for tag in [b'body', b'main']:
        pattern = rb'<' + tag + rb'\b[^>]*>.*?</' + tag + rb'>'
        require(re.findall(pattern, old, re.S) == re.findall(pattern, new, re.S), 'whole ' + tag.decode() + ' exact ' + record)
    require((current / 'citation.bib').read_bytes() == (root / 'citation.bib').read_bytes(), 'whole accepted BibTeX ' + record)
    _, before = json_script(head.decode())
    _, after = json_script(new.decode())
    expected = copy.deepcopy(before)
    expected.update({'@id': canonical, 'url': canonical, 'mainEntityOfPage': canonical})
    for encoding in expected['encoding']:
        encoding['contentUrl'] = canonical + encoding['contentUrl']
    require(after == expected, 'exact complete ScholarlyArticle data allowlist ' + record)
    require(after['@context'] == 'https://schema.org' and after['@type'] == 'ScholarlyArticle' and
            after['name'] == after['headline'] == model['title'] and after['abstract'] == model['abstract'], 'scholarly title and abstract ' + record)
    require(after['datePublished'] == model['publication_date'] == native_data['metadata']['publication_date'] == '2026-10-06', 'original publication date ' + record)
    require(after['dateCreated'] == model['record_created'] == native_data['created'] and
            after['dateModified'] == model['record_updated'] == native_data['updated'], 'original creation/update timestamps ' + record)
    require(model['native_version'] == native_data['metadata'].get('version') and
            (after.get('version') == '1.0.0' if record == '23202994' else 'version' not in after and 'version' not in native_data['metadata']), 'native version distinction ' + record)
    require(after['author'] == {'@type': 'Person', 'name': 'Alec Kriebel', 'identifier': 'https://orcid.org/0009-0001-9320-500X'} and
            after['identifier'] == {'@type': 'PropertyValue', 'propertyID': 'DOI', 'value': model['doi']} and
            after['sameAs'] == model['doi_url'] and after['creativeWorkStatus'] == model['status'], 'author DOI and status metadata ' + record)
    parsed = HTML(new.decode())
    require(len(parsed.ids) == len(set(parsed.ids)), 'unique article IDs ' + record)
    meta = {x.get('name', x.get('property')): x.get('content') for tag, x in parsed.elements if tag == 'meta'}
    require('robots' not in meta and 'googlebot' not in meta and meta['og:url'] == canonical and
            meta['citation_pdf_url'] == canonical + 'assets/paper.pdf', 'robots OG absolute Scholar PDF ' + record)
    require(meta['citation_publication_date'] == meta['citation_date'] == '2026/10/06' and
            meta['DC.description'] == model['abstract'] and meta['DC.date'] == '2026-10-06', 'whole abstract and original Scholar/DC dates ' + record)
    require(meta.get('citation_version') == model['native_version'], 'citation native version ' + record)
    canonical_links = [x for tag, x in parsed.elements if tag == 'link' and x.get('rel') == 'canonical']
    require(canonical_links == [{'rel': 'canonical', 'href': canonical}], 'canonical link ' + record)
    require([x.get('href') for tag, x in parsed.elements if tag == 'link' and x.get('rel') == 'stylesheet'] == ['/research/research.css'], 'shared stylesheet link ' + record)
    for tag, attrs in parsed.elements:
        for key in ['aria-labelledby', 'aria-describedby']:
            require(all(x in parsed.ids for x in attrs.get(key, '').split()), 'local ARIA references ' + record)
        for key in ['href', 'src']:
            if key not in attrs:
                continue
            u = urlsplit(attrs[key])
            if u.scheme or u.netloc:
                if u.scheme != 'https' or u.netloc != 'aleckriebel.com':
                    continue
            target = CAND / unquote(u.path).lstrip('/') if u.path.startswith('/') else current / unquote(u.path)
            if not u.path:
                target = current / 'index.html'
            if target.is_dir():
                target = target / 'index.html'
            require(target.resolve().is_relative_to(CAND.resolve()) and target.is_file(), 'local asset/path resolves ' + record + ': ' + attrs[key])
            if u.fragment:
                if target.suffix.lower() in {'.html', '.htm'}:
                    html_bytes = target.read_bytes()
                    require(b'<html' in html_bytes[:100].lower(), 'actual HTML fragment target ' + record)
                    require(unquote(u.fragment) in HTML(html_bytes.decode('utf-8')).ids,
                            'local HTML fragment ID resolves ' + record + ': ' + attrs[key])
                elif target.suffix.lower() == '.pdf':
                    require(target.resolve() == (current / 'assets/paper.pdf').resolve(), 'correct native PDF viewer path ' + record)
                    require(unquote(u.fragment) == 'view=FitH', 'exact accepted PDF viewer parameter ' + record)
                    pdf_bytes = target.read_bytes()
                    require(pdf_bytes.startswith(b'%PDF-') and pdf_bytes ==
                            (P / ('papers/' + record + '/sources/zenodo-files/paper.pdf')).read_bytes(),
                            'whole native PDF bytes and binary header for viewer URL ' + record)
                else:
                    raise AssertionError('unsupported actual local fragment target type ' + str(target))
    require(model['follow_up'] is None and model['AA'] is None and model['actual_publication_date'] is None,
            'accepted model follow-up and publication null ' + record)
    entry = re.search(r'<p class="entry-meta">(.*?)</p>', (root / 'main.html').read_text(), re.S).group(1)
    require(entry.startswith('<a href="https://orcid.org/0009-0001-9320-500X">Alec Kriebel</a> · '), 'accepted exact author entry prefix ' + record)
    entry = entry.split('</a> · ', 1)[1]
    if record == '23203081':
        require('Zenodo display edition: v1' in entry and 'Version 1' not in entry, 'qualified Mink host-display label')
    return {'model': model, 'slug': slug, 'canonical': canonical, 'entry': entry,
            'head_spans': spans, 'article_pin': pin(current / 'index.html'), 'ids': len(parsed.ids)}

def xml_node(node):
    return {'tag': node.tag, 'attributes_in_order': list(node.attrib.items()), 'text': node.text,
            'tail': node.tail, 'children': [xml_node(x) for x in node]}

def aggregate(root):
    h = (root / 'research/index.html').read_bytes()
    x = (root / 'research/sitemap.xml').read_bytes()
    text = h.decode()
    lists = re.findall(r'<ul\b[^>]*>(.*?)</ul>', text, re.S)
    require(len(lists) == 1, 'one aggregate visible list')
    lis = re.findall(r'<li\b[^>]*>.*?</li>', lists[0], re.S)
    raw_script, schema = json_script(text)
    itemlist = schema['mainEntity']
    require(itemlist['@type'] == 'ItemList', 'actual collection ItemList schema')
    decoder = json.JSONDecoder()
    marker = re.search(r'"itemListElement"\s*:\s*\[', raw_script)
    require(marker is not None, 'actual raw JSON item array')
    pos, raw_items = marker.end(), []
    while True:
        pos += len(raw_script[pos:]) - len(raw_script[pos:].lstrip())
        if raw_script[pos] == ']':
            break
        _, end = decoder.raw_decode(raw_script, pos)
        raw_items.append(raw_script[pos:end])
        pos = end
        pos += len(raw_script[pos:]) - len(raw_script[pos:].lstrip())
        if raw_script[pos] == ',':
            pos += 1
        else:
            require(raw_script[pos] == ']', 'raw item array delimiter')
    tree = ET.fromstring(x)
    return {'html': h, 'xml': x, 'lis': lis, 'visible_data': [''.join(HTML(v).data) for v in lis],
            'raw_json': raw_items, 'typed': itemlist['itemListElement'], 'schema': schema,
            'raw_xml': re.findall(rb'<url\b[^>]*>.*?</url>', x, re.S), 'xml_tree': xml_node(tree)}

def verify_aggregates(pages):
    before, after = aggregate(BASE), aggregate(CAND)
    require((len(before['lis']), len(before['typed']), len(before['raw_xml'])) == (130, 130, 131), 'baseline complete aggregate counts')
    require((len(after['lis']), len(after['typed']), len(after['raw_xml'])) == (133, 133, 134), 'candidate complete aggregate counts')
    for k in ['lis', 'visible_data', 'raw_json', 'typed', 'raw_xml']:
        require(after[k][:len(before[k])] == before[k], 'all old whole aggregate units exact ordered prefix: ' + k)
    bt, at = before['xml_tree'], after['xml_tree']
    require({k: v for k, v in bt.items() if k != 'children'} == {k: v for k, v in at.items() if k != 'children'} and
            at['children'][:len(bt['children'])] == bt['children'], 'whole XML root and parsed old children attributes text tails order exact')
    require([x['position'] for x in after['typed']] == list(range(1, 134)), 'all old and new typed JSON positions')
    expected_lis, expected_typed, expected_xml = [], [], []
    for i, page in enumerate(pages, 131):
        model, url, slug = page['model'], page['canonical'], page['slug']
        def esc(t):
            return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;')
        li = '<li><a href="/research/' + slug + '/">' + esc(model['title']) + '</a><br><span class="entry-meta">' + page['entry'] + '</span><p>' + esc(model['meta_description']) + '</p><p><a href="/research/' + slug + '/assets/paper.pdf">PDF</a> · <a href="' + model['doi_url'] + '">Zenodo</a></p></li>'
        expected_lis.append(li)
        expected_typed.append({'@type': 'ListItem', 'position': i, 'url': url, 'name': model['title']})
        expected_xml.append(('<url><loc>' + url + '</loc><lastmod>2026-11-17</lastmod></url>').encode())
        require(len(re.findall(r'<p\b', li)) == 2, 'actual new listing two paragraphs ' + model['record_id'])
    require(after['lis'][130:] == expected_lis and after['typed'][130:] == expected_typed and
            after['raw_xml'][131:] == expected_xml, 'new aggregate units independently derived from accepted model and exact entry metadata')
    expected_schema = copy.deepcopy(before['schema'])
    expected_schema['mainEntity']['numberOfItems'] = 133
    expected_schema['mainEntity']['itemListElement'] += expected_typed
    require(after['schema'] == expected_schema, 'complete collection JSON data only count and append changes')
    index_spans = [span_once(before['html'], b'"numberOfItems": 130', b'"numberOfItems": 133')]
    item_pos = before['html'].index(before['raw_json'][-1].encode()) + len(before['raw_json'][-1].encode())
    item_append = ', ' + ', '.join(after['raw_json'][130:])
    index_spans.append({'start_byte': item_pos, 'end_byte': item_pos, 'old_UTF8': '', 'new_UTF8': item_append})
    list_pos = before['html'].index(b'</ul>')
    index_spans.append({'start_byte': list_pos, 'end_byte': list_pos, 'old_UTF8': '', 'new_UTF8': '\n'.join(expected_lis) + '\n'})
    xml_pos = before['xml'].index(b'</urlset>')
    xml_spans = [{'start_byte': xml_pos, 'end_byte': xml_pos, 'old_UTF8': '', 'new_UTF8': b'\n'.join(expected_xml).decode() + '\n'}]
    require(edit(before['html'], index_spans) == after['html'], 'independent whole index forward and reverse reconstruction')
    require(edit(before['xml'], xml_spans) == after['xml'], 'independent whole XML forward and reverse reconstruction')
    supplied = load(S / 'AGGREGATE_FIDELITY.json')
    require(edit(before['html'], supplied['index_spans']) == after['html'] and
            edit(before['xml'], supplied['XML_spans']) == after['xml'], 'supplied aggregate closed spans independently verified')
    for name, actual in [('BASELINE_AGGREGATE_UNITS.json', before), ('CANDIDATE_AGGREGATE_UNITS.json', after)]:
        saved = load(S / name)
        require(saved['index_whole_UTF8'].encode() == actual['html'] and saved['sitemap_whole_UTF8'].encode() == actual['xml'], 'stored whole aggregate buffers ' + name)
        require(saved['raw_visible_HTML_units'] == actual['lis'] and saved['raw_JSON_units'] == actual['raw_json'] and
                saved['typed_ItemList_units'] == actual['typed'] and [v.encode() for v in saved['raw_XML_units']] == actual['raw_xml'], 'stored raw/typed aggregate units ' + name)
        require(saved['visible_text_units'] == [' '.join(v.split()) for v in actual['visible_data']], 'stored visible text follows concatenated data events ' + name)
    require((S / 'ORIGINAL_RESEARCH_INDEX.html').read_bytes() == before['html'] and
            (S / 'ORIGINAL_RESEARCH_SITEMAP.xml').read_bytes() == before['xml'], 'entire original aggregate evidence')
    return {'baseline_counts': [130, 130, 131], 'candidate_counts': [133, 133, 134],
            'independent_index_span_count': len(index_spans), 'independent_XML_span_count': len(xml_spans),
            'supplied_index_span_count': len(supplied['index_spans']), 'supplied_XML_span_count': len(supplied['XML_spans']),
            'old_visible_concatenated_data_bytes': [len(v.encode()) for v in before['visible_data']],
            'XML_comparison_includes_root_children_text_tail_attribute_order': True}

COMMIT = '4cc09d6bbbad61aa11077c5002cf84a1e93b1344'
PARENT = '217d41c0a9344aed9caacee7aed31d4f23b77e47'
TREE = 'a9c5a4f3e30eb976bbe4f9c1872e14a92e22cc7e'
NEW_INDEX = {'bytes': 9062142, 'SHA256': '6b76dc0a4e7a631587aec1c081057479883573f7ff284dfc88b5adad02317179', 'mode': '0644'}
OLD_INDEX = {'bytes': 9060430, 'SHA256': '25494ed68b5d5612ae64ac01f2897c77b26024a994b66167426203d5620de4b7', 'mode': '0644'}
RUN = P / 'verification/mink-riesz-k3-runtime-sol-20261117'
ROOTEXEC = P / 'verification/mink-riesz-k3-root-execution-20261117'
OBJECTS, GIT_READS, PRIVATE_GIT_RESULTS = {}, [], []
FAILURE_ROOT = RUN / 'postpublication-audit-failure-20261117'
PACKETS = [
    ('mink-riesz-k3-stage-audit-sol-20261117', 28, 'MANIFEST.json', 1477, '3dab7883aaf53c71b8afcb49a5599fb0ead3d54d87e2c5d1a4d17919e2a37e04', 6455, 'ab248a8f6e16c18bf2e6c2fee3b6df674c2c05ca731a06cf82498c647452f945'),
    ('mink-riesz-k3-stage-audit-continuation-sol-20261117', 30, 'MANIFEST.json', 1487, '2dcda99d4e5577405d9fefceb4efdab9d3f895998dbe868d897f2f3c6660c7f6', 6911, '11f217ddb3065106e0c1b6692ba7dbe7f923d3f1999c679bbcaaa2a6f19991e2'),
    ('mink-riesz-k3-stage-audit-html-fragments-sol-20261117', 22, 'MANIFEST.json', 2315, 'f8207dd322c76addc52bafa3b5472a268f4d6924fce7ea38bdc64036bc82a4a0', 5405, '8e46e120ca55158bc9e623bb4348263591ac75d405393ff1b85e1b746092f517'),
    ('mink-riesz-k3-production-prepare-sol-20261117', 14, 'OWNED_MANIFEST.json', 11407, '9ed064c8ce6c6c226acfce9b76bfdc0d7bcc9acd179b08da5f9b310dc66113a1', 3816, '59c6c63bd49acbcb691b9c9f624ac0ee8b910483c1b1f4e665e428fdc90f0308'),
    ('mink-riesz-k3-production-static-sol-20261117', 21, 'MANIFEST.json', 2711, '0e607a93669506617a6b64c260a6b3acaa9288f6c8912d6885a41cc2cc34b9ef', 4973, '485e21dbeef6c26b03fcef7f7e3ef11b28dfb8cb6296c8295f3c331a0f9468a4'),
    ('mink-riesz-k3-production-prepare-v2-sol-20261117', 12, 'OWNED_MANIFEST.json', 8839, 'ddf44cba02ceefe26979d69abb39aa76674605b5fa629737d6b37cce2495afe7', 3343, 'bb1d3310715e55097986663b5500fd38a134c787e0e2ce507282a4c5b8f0dd02'),
    ('mink-riesz-k3-production-static-v2-sol-20261117', 20, 'MANIFEST.json', 2837, '2229e5e8d338324468aba12847510149226162aad7ca36066db5a17bcc7aae9b', 4757, 'c532aa72c645b8913804e5ca013f6aa4e8a643b90340083b61d6efe93c3779d7'),
]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def data_pin(data):
    return {'bytes': len(data), 'SHA256': digest(data)}

def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()

def packet(snapshot, row):
    name, count, manifest_name, final_size, final_sha, manifest_size, manifest_sha = row
    root = P / 'verification' / name
    require(snapshot['regular_files'] == count and snapshot['child_directories'] == 0, 'fixed frozen packet count ' + name)
    require(pin(root / 'FINAL.json') == {'bytes': final_size, 'SHA256': final_sha, 'mode': '0644'}, 'external frozen FINAL ' + name)
    require(pin(root / manifest_name) == {'bytes': manifest_size, 'SHA256': manifest_sha, 'mode': '0644'}, 'external frozen manifest ' + name)
    manifest = load(root / manifest_name)
    controls = {'FINAL.json', manifest_name}
    require(set(snapshot['files']) == {x['path'] for x in manifest['payload_files']} | controls and
            len(manifest['payload_files']) == count - 2, 'whole frozen file topology ' + name)
    require(set(manifest['exact_already_created_terminal_recursive_hash_exclusions']) in
            [controls, {str(root / x) for x in controls}] and not manifest['other_exclusions'], 'only pinned exact circular pair ' + name)
    for item in manifest['payload_files']:
        require(snapshot['files'][item['path']] == {k: item[k] for k in ['bytes', 'SHA256', 'mode']}, 'frozen payload ' + name + '/' + item['path'])
    require({x['path']: {'mode': x['mode'], 'empty': x['empty']} for x in manifest['directories']} == snapshot['directories'], 'frozen root-inclusive modes/topology ' + name)

def capture(guard, backups):
    return {'protected': protected(guard), 'stage': snap(S),
            'frozen_packets': {row[0]: snap(P / 'verification' / row[0]) for row in PACKETS},
            'retained_before_indices': {str(p): pin(p) for p in backups},
            'root_stage_adoption': pin(P / 'verification/root-mink-riesz-k3-stage-adoption-20261117.json'),
            'website_configuration': {str(W / p): pin(W / p) for p in ['.firebaserc', 'firebase.json']}}

def receipt_observation():
    require(format(stat.S_IMODE(ROOTEXEC.lstat().st_mode), '04o') == '0700' and
            format(stat.S_IMODE(RUN.lstat().st_mode), '04o') == '0700', 'root execution and runtime stay private0700')
    summaries, published = [], None
    flags = {'PREFLIGHT': '--preflight', 'INSTALL': '--install', 'VERIFY_INSTALLED': '--verify-installed', 'PUBLISH': '--publish'}
    for name, flag in flags.items():
        receipt = load(ROOTEXEC / (name + '.execution.json'))
        require(receipt['attempt'] == 1 and receipt['exit_code'] == 0, 'retained one successful mode receipt ' + name)
        require(receipt['argv'][1:] == ['-B', str(P / 'verification/mink-riesz-k3-production-prepare-v2-sol-20261117/release_three.py'), flag] and
                Path(receipt['argv'][0]).is_absolute() and Path(receipt['argv'][0]).name == 'python3.14', 'exact retained stale V2 mode argv ' + name)
        raw = (ROOTEXEC / (name + '.stdout.bin')).read_bytes()
        err = (ROOTEXEC / (name + '.stderr.bin')).read_bytes()
        require(len(raw) == receipt['stdout_bytes'] and digest(raw) == receipt['stdout_SHA256'] and
                len(err) == receipt['stderr_bytes'] == 0 and digest(err) == receipt['stderr_SHA256'], 'literal private mode streams match receipt ' + name)
        value = json.loads(raw)
        summaries.append({'mode': name, 'attempt': 1, 'exit_code': 0, 'started_UTC': receipt['started_UTC'],
                          'finished_UTC': receipt['finished_UTC'], 'receipt_pin': pin(ROOTEXEC / (name + '.execution.json')),
                          'stdout_pin': data_pin(raw), 'stderr_pin': data_pin(err), 'raw_streams_private_not_copied': True})
        if name == 'PUBLISH':
            published = value
    require(published['commit'] == COMMIT and published['parent'] == PARENT and published['tree'] == TREE and
            published['index'] == NEW_INDEX and published['delta'] == '13A2M', 'retained publication SUCCESS exact local result pins')
    publish_root = RUN / 'publish' / published['authorization_SHA256']
    install_root = Path(published['installation_SUCCESS']['path']).parent
    require(publish_root.parent == RUN / 'publish' and install_root.parent.parent == RUN and install_root.parent.name == 'install', 'exact private retained transaction roots')
    backups = [publish_root / 'native-backups/index.before', install_root / 'native-backups/index.before']
    for p in backups:
        require(pin(p) == OLD_INDEX, 'retained old raw index external pin ' + str(p))
    require(backups[0].read_bytes() == backups[1].read_bytes(), 'both independent retained old index backups identical')
    return published, summaries, backups

def objects(oids):
    pending = sorted(set(oids) - set(OBJECTS))
    if not pending:
        return
    require(all(re.fullmatch('[0-9a-f]{40}', x) for x in pending), 'literal local object requests')
    request = b''.join(x.encode() + b'\n' for x in pending)
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_OPTIONAL_LOCKS='0', GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1', GIT_TERMINAL_PROMPT='0', GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    command = ['/usr/bin/git', '--no-optional-locks', '-c', 'protocol.allow=never', '-c', 'core.hooksPath=/dev/null',
               '-c', 'core.fsmonitor=false', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false', 'cat-file', '--batch']
    result = subprocess.run(command, cwd=W, env=env, input=request, capture_output=True)
    PRIVATE_GIT_RESULTS.append((result.stdout, result.stderr, result.returncode))
    GIT_READS.append({'requested_objects': len(pending), 'request_SHA256': digest(request), 'exit_code': result.returncode,
                      'stdout_pin': data_pin(result.stdout), 'stderr_pin': data_pin(result.stderr), 'network_protocols_disabled': True})
    require(result.returncode == 0 and result.stderr == b'', 'local read-only cat-file success; streams retained only as derived hashes')
    cursor = 0
    for oid in pending:
        end = result.stdout.index(b'\n', cursor)
        header = result.stdout[cursor:end].split()
        require(len(header) == 3 and header[0] == oid.encode() and header[1] in [b'commit', b'tree', b'blob'], 'complete local object header')
        size = int(header[2])
        cursor = end + 1
        body = result.stdout[cursor:cursor + size]
        require(len(body) == size and result.stdout[cursor + size:cursor + size + 1] == b'\n' and
                hashlib.sha1(header[1] + b' ' + str(size).encode() + b'\0' + body).hexdigest() == oid, 'whole local object bytes authenticate requested OID')
        OBJECTS[oid] = (header[1], body)
        cursor += size + 1
    require(cursor == len(result.stdout), 'whole private object response consumed, never copied to public evidence')

def parsed_tree(oid):
    kind, body = OBJECTS[oid]
    require(kind == b'tree', 'actual tree object type')
    cursor, result, last = 0, [], None
    while cursor < len(body):
        space = body.index(b' ', cursor)
        zero = body.index(b'\0', space + 1)
        mode_bytes, name = body[cursor:space], body[space + 1:zero]
        require(name and b'/' not in name and name not in [b'.', b'..'] and zero + 21 <= len(body), 'complete canonical tree entry')
        directory = mode_bytes in [b'40000', b'040000']
        require(directory or mode_bytes in [b'100644', b'100755', b'120000', b'160000'], 'known actual Git tree mode')
        key = name + (b'/' if directory else b'')
        require(last is None or last < key, 'actual Git tree directory-name byte ordering')
        result.append((name, mode_bytes, body[zero + 1:zero + 21].hex(), directory))
        cursor = zero + 21
        last = key
    return result

def git_map(root):
    pending, expanded = {root}, set()
    while pending:
        objects(pending)
        children = set()
        for oid in pending:
            for name, mode_bytes, child, directory in parsed_tree(oid):
                if directory and child not in expanded and child not in pending:
                    children.add(child)
        expanded.update(pending)
        pending = children - expanded
    result = {}
    def walk(oid, prefix):
        for name, mode_bytes, child, directory in parsed_tree(oid):
            path = prefix + name
            if directory:
                walk(child, path + b'/')
            else:
                require(path not in result, 'unique complete committed leaf')
                result[path] = mode_bytes + (b' commit ' if mode_bytes == b'160000' else b' blob ') + child.encode()
    walk(root, b'')
    return result

def parse_index(raw):
    require(raw[:4] == b'DIRC' and struct.unpack('>I', raw[4:8])[0] == 2 and
            hashlib.sha1(raw[:-20]).digest() == raw[-20:], 'whole checksum-valid v2 raw index')
    count = struct.unpack('>I', raw[8:12])[0]
    cursor, records, previous = 12, {}, None
    for unused in range(count):
        start = cursor
        end = raw.index(b'\0', start + 62, len(raw) - 20)
        name = raw[start + 62:end]
        cursor = start + ((end + 1 - start + 7) // 8) * 8
        flags = struct.unpack('>H', raw[start + 60:start + 62])[0]
        require(name and (previous is None or previous < name) and not flags & 0x7000 and
                flags & 4095 == min(len(name), 4095) and not any(raw[end + 1:cursor]), 'whole raw record name/flags/NUL/padding/order')
        records[name] = (raw[start:cursor], struct.unpack('>I', raw[start + 24:start + 28])[0], raw[start + 40:start + 60])
        previous = name
    ext = raw[cursor:-20]
    require(ext[:4] == b'TREE' and struct.unpack('>I', ext[4:8])[0] == len(ext) - 8, 'sole complete TREE extension')
    return records, ext

def record_map(records):
    result = {}
    for name, (raw, mode_number, oid) in records.items():
        require(mode_number in [0o100644, 0o100755, 0o120000, 0o160000], 'native semantic mode')
        result[name] = format(mode_number, 'o').encode() + (b' commit ' if mode_number == 0o160000 else b' blob ') + oid.hex().encode()
    return result

def native_trees(records):
    root, values = {}, {}
    for path, (raw, mode_number, oid) in records.items():
        node = root
        parts = path.split(b'/')
        for part in parts[:-1]:
            require(part and (part not in node or isinstance(node[part], dict)), 'native full directory topology')
            node = node.setdefault(part, {})
        require(parts[-1] and parts[-1] not in node, 'native unique leaf topology')
        node[parts[-1]] = (format(mode_number, 'o').encode(), oid)
    def build(node, path):
        entries, count = [], 0
        for name, item in node.items():
            if isinstance(item, tuple):
                mode_bytes, oid = item
                entries.append((name, mode_bytes, oid, False))
                count += 1
            else:
                child, descendants = build(item, path + (b'/' if path else b'') + name)
                entries.append((name, b'40000', bytes.fromhex(child), True))
                count += descendants
        entries.sort(key=lambda x: x[0] + (b'/' if x[3] else b''))
        body = b''.join(mode_bytes + b' ' + name + b'\0' + oid for name, mode_bytes, oid, directory in entries)
        oid = hashlib.sha1(b'tree ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        values[path] = (count, oid, body)
        return oid, count
    build(root, b'')
    return values

def cache_check(extension, before, after):
    require(data_pin(extension) == {'bytes': 35878, 'SHA256': 'f12d2a0b795034ce5cab45ad6fa5da31b4d7ad6f4b22a5999ce27841b41350b3'}, 'whole unchanged TREE external pin')
    payload = extension[8:]
    require(data_pin(payload) == {'bytes': 35870, 'SHA256': '6078bbaef4d39e7b0418bc6ed44ad8f37d2733ec6de4a4e4ba165fe7e665bfcb'}, 'TREE payload external pin')
    cursor, paths, valid, invalid = 0, set(), [], []
    def visit(parent, first=False):
        nonlocal cursor
        end = payload.index(b'\0', cursor)
        name = payload[cursor:end]
        line = payload.index(b'\n', end + 1)
        entries, children = map(int, payload[end + 1:line].split())
        path = b'' if first else parent + (b'/' if parent else b'') + name
        require((first and name == b'') or (not first and name and b'/' not in name), 'cached TREE local component')
        require(path not in paths and path in before and path in after and entries >= -1 and children >= 0, 'cached TREE exact native path/count bounds')
        paths.add(path)
        cursor = line + 1
        if entries >= 0:
            oid = payload[cursor:cursor + 20].hex()
            cursor += 20
            require((entries, oid) == before[path][:2] == after[path][:2], 'every valid cached subtree count/OID matches both native states')
            valid.append((path, oid))
        else:
            invalid.append(path.decode())
        for unused in range(children):
            visit(path)
    visit(b'', True)
    expected_invalid = ['', 'public', 'public/research', 'public/research/binary-relation-liveness',
                        'public/research/rational-point-undecidability', 'public/research/focal-distance-period-criterion']
    require(cursor == len(payload) and len(paths) == 983 and len(valid) == 977 and sorted(invalid) == sorted(expected_invalid), 'all983 cached nodes/977 valid/exact6 invalid consumed')
    objects(oid for path, oid in valid)
    for path, oid in valid:
        require(OBJECTS[oid] == (b'tree', before[path][2]) and before[path][2] == after[path][2], 'all977 local cached tree objects equal reconstructed bytes')
    return {'whole': data_pin(extension), 'payload': data_pin(payload), 'nodes': 983, 'valid': 977, 'invalid_paths': invalid}

def map_digest(mapping):
    return digest(canonical([(name.hex(), value.decode()) for name, value in sorted(mapping.items())]))

def foreign(native_map, committed, targets):
    return {name: (native_map.get(name), committed.get(name)) for name in (set(native_map) | set(committed)) - targets
            if native_map.get(name) != committed.get(name)}

def foreign_digest(mapping):
    return digest(canonical([(name.hex(), None if a is None else a.decode(), None if b is None else b.decode())
                             for name, (a, b) in sorted(mapping.items())]))

def main():
    require(Path(__file__).resolve() == A / 'audit_local.py' and not (A / 'RESULTS.json').exists(), 'one fresh fixed local audit invocation')
    require(not os.path.lexists(FAILURE_ROOT), 'approved private nested-failure destination absent before first invocation')
    started = utc()
    publication, receipts, backups = receipt_observation()
    guard = load(S / 'GUARDS_BEFORE.json')
    candidate = snap(CAND)
    expected = copy.deepcopy(guard)
    expected['public'] = {**candidate, 'root': str(W / 'public')}
    expected['native_W']['index'] = NEW_INDEX
    expected['native_W']['resolved_native_HEAD'] = COMMIT
    expected['native_W']['local_loose_heads']['files']['master'] = {**data_pin((COMMIT + '\n').encode()), 'mode': '0644'}
    before = capture(guard, backups)
    require(before['protected'] == expected, 'whole actual postpublication native/public/source/private controls exact successor')
    write('BEFORE.json', {'UTC': started, 'snapshot': before})
    verify_stage(before['stage'])
    for row in PACKETS:
        packet(before['frozen_packets'][row[0]], row)
    require(before['root_stage_adoption'] == {'bytes': 2379, 'SHA256': '4f23be687eecdd138350a880f8630e48f570281f68507aadbc8b1b9adaf34951', 'mode': '0644'}, 'actual root private stage adoption unchanged')
    plan = load(P / 'verification/mink-riesz-k3-production-prepare-v2-sol-20261117/PLAN.json')
    require(before['website_configuration'] == {x['path']: {k: x[k] for k in ['bytes', 'SHA256', 'mode']} for x in plan['configuration_guards']}, 'whole website hosting configuration buffers unchanged')
    auth = load(S / 'INPUT_AUTHENTICATION.json')
    verify_adoptions(auth, before['protected']['roots'])
    manifests = [verify_manifest(x, before['protected']['roots']) for x in auth['actual_manifests']]
    baseline = snap(BASE)
    actual = before['protected']['public']
    require(baseline == load(S / 'BASELINE_MANIFEST.json') and candidate == load(S / 'CANDIDATE_MANIFEST.json') and same_tree(actual, candidate), 'WHOLE actual public equals complete frozen candidate bytes/modes/topology')
    targets = load(S / 'TARGETS.json')
    names = targets['Git_relative_targets']
    additions, modifications = targets['additions_public_relative'], targets['modifications_public_relative']
    require(len(names) == 15 and len(additions) == 13 and len(modifications) == 2 and
            set(candidate['files']) - set(baseline['files']) == set(additions), 'whole physical public exact13 additions15targets')
    require({r for r in baseline['files'] if actual['files'][r] != baseline['files'][r]} == set(modifications) and
            all(actual['files'][r]['mode'] == value['mode'] for r, value in baseline['files'].items()), 'all788 untouched old files and inherited0600/0666 modes exact')
    require(all(actual['directories'][r] == value for r, value in baseline['directories'].items()) and
            set(actual['directories']) - set(baseline['directories']) == set(targets['new_directories_public_relative']), 'all381 old directories/root0750 plus6 exact new dirs')
    ds = [r for r in baseline['files'] if PurePosixPath(r).name == '.DS_Store']
    require(len(ds) == 17 and all(actual['files'][r] == baseline['files'][r] for r in ds) and
            actual['files']['research/research.css'] == baseline['files']['research/research.css'], 'all17DSStore and shared CSS exact')
    pages = [article(f, r, load(S / 'HEAD_ACTIVATION.json')['pages'][i]) for i, (f, r) in enumerate(FAMILIES)]
    aggregates = verify_aggregates(pages)
    source_counts = [x for p, x in before['protected']['roots'].items() if '/papers/' in p]
    private_counts = [x for p, x in before['protected']['roots'].items() if '/verification/' in p]
    require((sum(x['regular_files'] for x in source_counts), sum(x['child_directories'] for x in source_counts)) == (133, 34) and
            (sum(x['regular_files'] for x in private_counts), sum(x['child_directories'] for x in private_counts)) == (378, 25), 'all fixed133/34 source and378/25 private input extents')
    old_raw, new_raw = backups[0].read_bytes(), (W / '.git/index').read_bytes()
    require(pin(W / '.git/index') == NEW_INDEX, 'actual complete9062142 successor raw index pin')
    old, old_ext = parse_index(old_raw)
    new, new_ext = parse_index(new_raw)
    selected = {n.encode() for n in names}
    require(len(old) == 58730 and len(new) == 58743 and set(new) == set(old) | selected and
            set(old) & selected == {('public/' + n).encode() for n in modifications}, 'actual58730to58743 native selected path extents')
    require(len(set(old) - selected) == 58728 and all(new[n][0] == row[0] for n, row in old.items() if n not in selected), 'all58728 WHOLE untouched raw records exact')
    payloads = {n: (CAND / n[7:]).read_bytes() for n in names}
    for n, raw in payloads.items():
        oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).digest()
        row = struct.pack('>10I', 0, 0, 0, 0, 0, 0, 0o100644, 0, 0, 0) + oid + struct.pack('>H', min(len(n.encode()), 4095)) + n.encode() + b'\0'
        row += b'\0' * (-len(row) % 8)
        require(new[n.encode()][0] == row, 'whole exact selected zero-stat/mode/OID/flags/name/padding ' + n)
    require(old_ext == new_ext, 'whole TREE extension exact byte preservation')
    old_trees, new_trees = native_trees(old), native_trees(new)
    cache = cache_check(new_ext, old_trees, new_trees)
    objects([COMMIT, PARENT])
    require(OBJECTS[COMMIT][0] == OBJECTS[PARENT][0] == b'commit', 'actual parent/successor commit object types')
    body = OBJECTS[COMMIT][1]
    headers, message = body.split(b'\n\n', 1)
    lines = headers.splitlines()
    require(lines[0] == ('tree ' + TREE).encode() and [x for x in lines if x.startswith(b'parent ')] == [('parent ' + PARENT).encode()], 'exact complete new commit tree and single current parent')
    require(OBJECTS[PARENT][1].split(b'\n', 1)[0] == b'tree cb7ae0adb22dc34b9c36b9d1e8efcf94f89f44e3', 'exact complete original parent tree')
    authority_raw = (RUN / 'publish' / publication['authorization_SHA256'] / 'authorization.json').read_bytes()
    require(digest(authority_raw) == publication['authorization_SHA256'], 'whole retained publication authority bound to SUCCESS hash')
    authority = json.loads(authority_raw)
    date = datetime.fromisoformat(authority['commit_date'])
    minutes = int(date.utcoffset().total_seconds()) // 60
    zone = ('+' if minutes >= 0 else '-') + format(abs(minutes) // 60, '02d') + format(abs(minutes) % 60, '02d')
    identity = (authority['author_name'] + ' <' + authority['author_email'] + '> ' + str(int(date.timestamp())) + ' ' + zone).encode()
    require(authority['author_name'] == 'Alec Kriebel' and authority['author_email'] == 'me@aleckriebel.com' and
            [x for x in lines if x.startswith(b'author ')] == [b'author ' + identity] and
            [x for x in lines if x.startswith(b'committer ')] == [b'committer ' + identity] and
            message == (plan['commit_message'] + '\n').encode(), 'actual commit identity/date/message match retained publication authority observation')
    parent_map = git_map('cb7ae0adb22dc34b9c36b9d1e8efcf94f89f44e3')
    commit_map = git_map(TREE)
    expected_commit = dict(parent_map)
    for name, raw in payloads.items():
        oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        expected_commit[name.encode()] = b'100644 blob ' + oid.encode()
    require(commit_map == expected_commit, 'COMPLETE new commit map equals COMPLETE parent map with exactly15 stage updates')
    actual_added = set(commit_map) - set(parent_map)
    actual_changed = {n for n in set(commit_map) & set(parent_map) if commit_map[n] != parent_map[n]}
    require(actual_added == {('public/' + n).encode() for n in additions} and
            actual_changed == {('public/' + n).encode() for n in modifications} and not set(parent_map) - set(commit_map), 'complete commit delta13A2M no unrelated path action')
    objects(commit_map[n.encode()].split()[-1].decode() for n in names)
    require(all(OBJECTS[commit_map[n.encode()].split()[-1].decode()] == (b'blob', raw) for n, raw in payloads.items()), 'all15 actual Git blob buffers equal exact frozen stage payloads')
    before_map, after_map = record_map(old), record_map(new)
    require(git_map(old_trees[b''][1]) == before_map and git_map(new_trees[b''][1]) == after_map, 'both COMPLETE native semantic maps match independent local Git objects')
    require(new_trees[b''][1] == publication['native_successor_semantic_tree'], 'native semantic root matches retained publication proof without assuming commit-root equality')
    foreign_before, foreign_after = foreign(before_map, parent_map, selected), foreign(after_map, commit_map, selected)
    require(foreign_before == foreign_after, 'unrelated staging exact over union of native/commit paths including staged deletions')
    after = capture(guard, backups)
    require(after == before, 'whole fixed postpublication source/private/stage/audits/native/public/config/backup custody before-after exact')
    write('AFTER.json', {'UTC': utc(), 'snapshot': after})
    detail = {'receipts_derived_only': receipts, 'private_before_index_paths': [str(x) for x in backups],
        'physical_public_files_childdirs_articles_XML': [803, 387, 133, 134], 'input_manifests': manifests,
        'article_HEAD_span_counts': [len(x['head_spans']) for x in pages], 'aggregates': aggregates,
        'index': {'before': data_pin(old_raw), 'after': data_pin(new_raw), 'before_records': len(old), 'after_records': len(new),
                  'whole_untouched_records': 58728, 'selected_exact_zero_stat_records': 15, 'TREE': cache},
        'commit': {'OID': COMMIT, 'tree': TREE, 'single_parent': PARENT, 'parent_leaves': len(parent_map), 'new_leaves': len(commit_map),
                   'parent_semantic_map_SHA256': map_digest(parent_map), 'new_semantic_map_SHA256': map_digest(commit_map),
                   'delta': '13A2M', 'all15_blobs_byte_exact': True},
        'native_semantics': {'before_tree': old_trees[b''][1], 'after_tree': new_trees[b''][1],
            'before_map_SHA256': map_digest(before_map), 'after_map_SHA256': map_digest(after_map),
            'foreign_paths': len(foreign_before), 'foreign_before_SHA256': foreign_digest(foreign_before),
            'foreign_after_SHA256': foreign_digest(foreign_after), 'staged_deletions': sum(a is None for a, b in foreign_before.values())},
        'local_Git_object_reads_derived_only': GIT_READS, 'private_raw_journals_outputs_indices_not_copied': True}
    write('DETAILS.json', detail)
    write('RESULTS.json', {'schema': 'independent-postpublication-local-audit-result-v1', 'UTC_start': started, 'UTC_end': utc(),
        'status': 'PASS_LOCAL_POSTPUBLICATION_AUDIT_ONLY', 'completion_percent_assigned_local_audit_only': 100,
        'checks_passed': len(CHECKS), 'commit': COMMIT, 'tree': TREE, 'parent': PARENT, 'index': NEW_INDEX,
        'whole_fixed_custody_before_after_exact': True, 'one_fresh_checker_invocation_only': True,
        'production_helper_or_old_audit_import_execution_AST_compile_help_test_or_retry': False,
        'network_or_repository_public_source_config_Sheet_deploy_redirect_contact_mutation': False,
        'actual_UI_live_deployment_remote_persistence_or_scientific_certificate': False,
        'follow_up': None, 'AA': None, 'future_action_authority': False})

def retain_private_failure(error):
    if not PRIVATE_GIT_RESULTS:
        return
    if os.path.lexists(FAILURE_ROOT):
        raise RuntimeError('private failure path already exists; no overwrite or retry')
    os.mkdir(FAILURE_ROOT, 0o700)
    os.chmod(FAILURE_ROOT, 0o700)
    metadata = []
    for i, (stdout, stderr, exit_code) in enumerate(PRIVATE_GIT_RESULTS):
        row = {'read': i, 'exit_code': exit_code}
        for kind, data in [('stdout', stdout), ('stderr', stderr)]:
            path = FAILURE_ROOT / (str(i).zfill(3) + '.' + kind + '.bin')
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            try:
                os.fchmod(fd, 0o600)
                cursor = 0
                while cursor < len(data):
                    written = os.write(fd, data[cursor:])
                    if written <= 0:
                        raise OSError('short private failure evidence write')
                    cursor += written
                os.fsync(fd)
            finally:
                os.close(fd)
            row[kind] = {'private_path': str(path), **data_pin(data), 'mode': '0600'}
        metadata.append(row)
    for path in [FAILURE_ROOT, RUN]:
        fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    write('NESTED_GIT_FAILURE.json', {'schema': 'approved-private-nested-object-read-failure-retention-v1',
        'error': repr(error), 'private_directory': str(FAILURE_ROOT), 'root_mode': '0700', 'streams': metadata,
        'literal_streams_not_copied_to_public_audit': True, 'automatic_retry_or_cleanup': False, 'follow_up': None})

if __name__ == '__main__':
    try:
        main()
    except BaseException as error:
        retain_private_failure(error)
        raise

