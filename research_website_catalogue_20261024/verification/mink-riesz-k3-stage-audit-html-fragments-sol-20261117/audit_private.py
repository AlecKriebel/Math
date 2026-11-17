"""One independent passive audit; writes only its own fresh audit directory."""
from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
from datetime import datetime, timezone
import copy
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
A = P / 'verification/mink-riesz-k3-stage-audit-html-fragments-sol-20261117'
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

def verify_prior_failed(snapshot):
    expected = {'FINAL.json': (1477, '3dab7883aaf53c71b8afcb49a5599fb0ead3d54d87e2c5d1a4d17919e2a37e04'),
                'MANIFEST.json': (6455, 'ab248a8f6e16c18bf2e6c2fee3b6df674c2c05ca731a06cf82498c647452f945')}
    for name, (size, sha) in expected.items():
        require(pin(O / name) == {'bytes': size, 'SHA256': sha, 'mode': '0644'}, 'prior failed audit external terminal pin ' + name)
    manifest = load(O / 'MANIFEST.json')
    terminal = load(O / 'FINAL.json')
    require((snapshot['regular_files'], snapshot['child_directories']) == (28, 0), 'prior failed finite namespace28/0')
    require(set(snapshot['files']) == {r['path'] for r in manifest['payload_files']} | set(expected), 'prior failed complete file topology')
    require(manifest['exact_already_created_terminal_recursive_hash_exclusions'] == ['MANIFEST.json', 'FINAL.json'] and
            not manifest['other_exclusions'], 'prior failed only exact circular terminal pair')
    for row in manifest['payload_files']:
        verify_pin(O / relative(row['path']), row, 'prior failed preserved payload ' + row['path'])
    require({r['path']: {'mode': r['mode'], 'empty': r['empty']} for r in manifest['directories']} == snapshot['directories'],
            'prior failed root-inclusive mode and empty topology')
    require(terminal['manifest'] == pin(O / 'MANIFEST.json') and terminal['original_audit_exit'] == 1 and
            terminal['completion_percent_assigned_original_audit_only'] == 60 and terminal['no_PASS_retroclaim'],
            'prior failed original exit1/incomplete60 remains literal')
    require(pin(O / 'audit_private.py') == {'bytes': 41491, 'SHA256': '39fe5f73831676dca34930af27c4e1dc6315556e1f2cbedbbe2317a4353a34d8', 'mode': '0644'},
            'original failed592line reader immutable never imported or rerun')
    require(pin(D) == {'bytes': 2877, 'SHA256': '7a3a3f3d4768b754511ac739ef297d26c15c8e6d94d8ed1d21c009a8550ebb6d', 'mode': '0644'},
            'root independent diagnosis external pin')

def verify_second_failed(snapshot):
    expected = {'FINAL.json': (1487, '2dcda99d4e5577405d9fefceb4efdab9d3f895998dbe868d897f2f3c6660c7f6'),
                'MANIFEST.json': (6911, '11f217ddb3065106e0c1b6692ba7dbe7f923d3f1999c679bbcaaa2a6f19991e2')}
    for name, (size, sha) in expected.items():
        require(pin(T / name) == {'bytes': size, 'SHA256': sha, 'mode': '0644'}, 'second failed audit external terminal pin ' + name)
    manifest = load(T / 'MANIFEST.json')
    terminal = load(T / 'FINAL.json')
    require((snapshot['regular_files'], snapshot['child_directories']) == (30, 0), 'second failed finite namespace30/0')
    require(set(snapshot['files']) == {r['path'] for r in manifest['payload_files']} | set(expected), 'second failed complete file topology')
    require(manifest['exact_already_created_terminal_recursive_hash_exclusions'] == ['MANIFEST.json', 'FINAL.json'] and
            not manifest['other_exclusions'], 'second failed only exact circular terminal pair')
    for row in manifest['payload_files']:
        verify_pin(T / relative(row['path']), row, 'second failed preserved payload ' + row['path'])
    require({r['path']: {'mode': r['mode'], 'empty': r['empty']} for r in manifest['directories']} == snapshot['directories'],
            'second failed root-inclusive mode and empty topology')
    require(terminal['manifest'] == pin(T / 'MANIFEST.json') and terminal['original_audit_exit'] == 1 and
            terminal['completion_percent_assigned_original_audit_only'] == 60 and terminal['no_PASS_retroclaim'],
            'second failed original exit1/incomplete60 remains literal')
    require(pin(T / 'audit_private.py') == {'bytes': 44562, 'SHA256': '1923a70e3eb716920f96b12facbae4fa0b12337eac320da650fd558f4c7d88fb', 'mode': '0644'},
            'second failed629line reader immutable never imported or rerun')
    require(pin(E) == {'bytes': 2165, 'SHA256': '700257c3ce91aa281fe730fdd5a360763fef974dfbb10e95512f9fd32063f49a', 'mode': '0644'},
            'root PDF fragment type diagnosis external pin')

def main():
    require(Path(__file__).resolve() == A / 'audit_private.py', 'fixed own reader path')
    require(not (A / 'RESULTS.json').exists(), 'single audit invocation fresh result')
    started = utc()
    guard = load(S / 'GUARDS_BEFORE.json')
    stage_before = snap(S)
    before = protected(guard)
    prior_failed_before = snap(O)
    verify_prior_failed(prior_failed_before)
    diagnosis_before = pin(D)
    second_failed_before = snap(T)
    verify_second_failed(second_failed_before)
    pdf_diagnosis_before = pin(E)
    write('BEFORE.json', {'UTC': started, 'stage': stage_before, 'protected': before,
                          'prior_failed': prior_failed_before, 'root_diagnosis': diagnosis_before,
                          'second_failed': second_failed_before, 'pdf_diagnosis': pdf_diagnosis_before})
    final = verify_stage(stage_before)
    require((S / 'GUARDS_BEFORE.json').read_bytes() == (S / 'GUARDS_AFTER.json').read_bytes(), 'literal successful build guard bytes identical')
    require(before == guard, 'all actual protected trees/native controls match authenticated build guard')
    require(before['native_M']['resolved_native_HEAD'] == 'a4ce3c37dad209339e490d18dcced6c48cf912d2' and
            before['native_M']['index']['SHA256'] == '91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11', 'native Math main and raw index fixed pins')
    require(before['native_W']['resolved_native_HEAD'] == '217d41c0a9344aed9caacee7aed31d4f23b77e47' and
            before['native_W']['index'] == {'bytes': 9060430, 'SHA256': '25494ed68b5d5612ae64ac01f2897c77b26024a994b66167426203d5620de4b7', 'mode': '0644'}, 'native website master and raw index fixed pins')
    index = (W / '.git/index').read_bytes()
    require(index[:4] == b'DIRC' and struct.unpack('>II', index[4:12]) == (2, 58730) and
            hashlib.sha1(index[:-20]).digest() == index[-20:], 'website native index v2 count and checksum')
    oid = before['native_W']['resolved_native_HEAD']
    raw = zlib.decompress((W / '.git/objects' / oid[:2] / oid[2:]).read_bytes())
    require(hashlib.sha1(raw).hexdigest() == oid and raw.split(b'\0', 1)[0].startswith(b'commit '), 'existing loose native commit object authentication')
    tree = re.search(rb'^tree ([0-9a-f]{40})\n', raw.split(b'\0', 1)[1]).group(1).decode()
    require(tree == 'cb7ae0adb22dc34b9c36b9d1e8efcf94f89f44e3', 'native website commit exact tree')
    auth = load(S / 'INPUT_AUTHENTICATION.json')
    verify_adoptions(auth, before['roots'])
    DETAIL['input_manifests'] = [verify_manifest(x, before['roots']) for x in auth['actual_manifests']]
    sources = [v for r, v in before['roots'].items() if '/papers/' in r]
    private = [v for r, v in before['roots'].items() if '/verification/' in r]
    require((sum(x['regular_files'] for x in sources), sum(x['child_directories'] for x in sources)) == (133, 34), 'all source input 133/34')
    require((sum(x['regular_files'] for x in private), sum(x['child_directories'] for x in private)) == (378, 25), 'all private input 378/25')
    base, cand = snap(BASE), snap(CAND)
    require(base == load(S / 'BASELINE_MANIFEST.json') and cand == load(S / 'CANDIDATE_MANIFEST.json'), 'full actual baseline/candidate manifests exact')
    require(same_tree(base, before['public']), 'complete baseline is actual website public tree')
    require((base['regular_files'], base['child_directories'], cand['regular_files'], cand['child_directories']) == (790, 381, 803, 387), 'whole public/candidate counts')
    require(base['directories']['.']['mode'] == cand['directories']['.']['mode'] == '0750', 'both public-copy root modes0750')
    activation = load(S / 'HEAD_ACTIVATION.json')['pages']
    pages = [article(f, r, activation[i]) for i, (f, r) in enumerate(FAMILIES)]
    expected_add = [f'research/{p["slug"]}/{x}' for p in pages for x in p['model']['deployment_proposal']['future_payloads']]
    expected_mod = ['research/index.html', 'research/sitemap.xml']
    expected_dirs = [x for p in pages for x in ['research/' + p['slug'], 'research/' + p['slug'] + '/assets']]
    added = set(cand['files']) - set(base['files'])
    deleted = set(base['files']) - set(cand['files'])
    changed = {r for r in base['files'] if cand['files'].get(r) != base['files'][r]}
    require(added == set(expected_add) and changed == set(expected_mod) and not deleted, 'full candidate exact13 additions2 modifications no deletions')
    require(set(cand['directories']) - set(base['directories']) == set(expected_dirs) and
            all(cand['directories'][r] == v for r, v in base['directories'].items()), 'six added directories all381 inherited modes/topology exact')
    require(all(cand['files'][r]['mode'] == v['mode'] for r, v in base['files'].items()) and
            all(cand['files'][r]['mode'] == '0644' for r in added), 'all inherited file modes0600/0666 preserved only13 new0644')
    require(Counter(x['mode'] for x in base['files'].values()) == Counter({'0644': 764, '0600': 24, '0666': 2}), 'actual baseline inherited mode counts')
    require(sum(cand['files'][r] == base['files'][r] for r in base['files']) == 788 and
            cand['files']['research/research.css'] == base['files']['research/research.css'], 'all788 untouched files and shared CSS exact')
    ds = [r for r in base['files'] if PurePosixPath(r).name == '.DS_Store']
    require(len(ds) == 17 and all(cand['files'][r] == base['files'][r] for r in ds), 'all17 DS_Store exact')
    targets = load(S / 'TARGETS.json')
    require(targets['append_order'] == [r for _, r in FAMILIES] and targets['additions_public_relative'] == expected_add and
            targets['modifications_public_relative'] == expected_mod and targets['new_directories_public_relative'] == expected_dirs and
            targets['Git_relative_targets'] == ['public/' + r for r in expected_add + expected_mod], 'actual TARGETS exact model-derived order and public prefix once')
    DETAIL['aggregates'] = verify_aggregates(pages)
    DETAIL['articles'] = [{k: v for k, v in p.items() if k != 'model'} for p in pages]
    DETAIL['projection'] = {'A': sorted(added), 'M': sorted(changed), 'Git_paths': targets['Git_relative_targets'], 'new_directories': expected_dirs}
    for name, key, count in [('SEAL_ATTEMPT_V1.input-metadata.json', 'snapshot', 1616),
                             ('SEAL_V2_GUARDS_BEFORE.json', 'snapshot', 1628),
                             ('SEAL_V2_GUARDS_AFTER.json', 'protected_preexisting_snapshot', 1628)]:
        original = load(S / name)[key]
        require(original['regular_files'] == count and original['child_directories'] == 770 and
                all(stage_before['files'][r] == v for r, v in original['files'].items()) and
                original['directories'] == stage_before['directories'], 'all preexisting stage bytes/modes/topology unchanged: ' + name)
    execution = load(S / 'BUILD_EXECUTION.json')
    first = load(S / 'SEAL_ATTEMPT_V1.execution.json')
    v2 = load(S / 'SEAL_V2_EXECUTION.json')
    require(execution['invocations'] == 1 and execution['exit_code'] == 0 and
            first['mapped_failure_status'] == 1 and first['native_process_exit_code'] is None and
            v2['invocations'] == 1 and v2['exit_code_at_normal_completion'] == 0, 'retained distinct builder0 first administrative1 separate metadata0')
    require((S / 'BUILD.stdout.txt').read_bytes() == (S / 'BUILD.stderr.txt').read_bytes() == b'' and
            (S / 'SEAL_V2.stdout.txt').read_bytes() == (S / 'SEAL_V2.stderr.txt').read_bytes() == b'' and
            b'Error: filepin' in (S / 'SEAL_ATTEMPT_V1.stderr.txt').read_bytes(), 'literal producer/metadata streams retained')
    require(pin(S / 'build_private.py') == {'bytes': 36119, 'SHA256': '571d593b18f9d74584a18787f4b8da9118fcd1de8d71e500ca8a87a5745acc56', 'mode': '0644'} and
            len((S / 'build_private.py').read_bytes().splitlines()) == 435, 'frozen producer file bytes/lines only never executed or parsed as code')
    after = protected(guard)
    stage_after = snap(S)
    prior_failed_after = snap(O)
    diagnosis_after = pin(D)
    second_failed_after = snap(T)
    pdf_diagnosis_after = pin(E)
    require(after == before and stage_after == stage_before and prior_failed_after == prior_failed_before and
            diagnosis_after == diagnosis_before and second_failed_after == second_failed_before and
            pdf_diagnosis_after == pdf_diagnosis_before, 'audit whole protected boundary stage both failed lanes and both diagnoses before/after exact')
    write('AFTER.json', {'UTC': utc(), 'stage': stage_after, 'protected': after,
                         'prior_failed': prior_failed_after, 'root_diagnosis': diagnosis_after,
                         'second_failed': second_failed_after, 'pdf_diagnosis': pdf_diagnosis_after})
    write('DETAILS.json', DETAIL)
    write('RESULTS.json', {'schema': 'independent-private-mink-riesz-k3-stage-audit-result-v1',
                           'UTC_start': started, 'UTC_end': utc(), 'status': 'PASS_TYPED_FRAGMENT_PRIVATE_STAGE_AUDIT_ONLY',
                           'completion_percent_assigned_audit_only': 100, 'checks_passed': len(CHECKS),
                           'checks': list(CHECKS), 'follow_up': None, 'AA': None, 'actual_publication_date': None,
                           'future_action_authority': False, 'actual_UI_render_live_or_production_certificate': False,
                           'source_science_or_producer_execution': False, 'network_Git_writes_deploy_Sheet_redirect_outreach': False})
    report = ('Separate typed-fragment private stage audit PASS. Both earlier audits remain frozen exit 1 each, incomplete 60%; '
              'this distinct reader uses the approved unchanged stylesheet insertion anchor and checks IDs only on actual HTML targets. '
              'PDF viewer parameters bind to the native PDF path, complete bytes and binary header; no embedded display certificate. '
              'Completion 100% applies only to this assigned continuation audit; '
              'follow_up null and no later action authority.\n\n'
              'The externally pinned 1635-file/770-child-directory stage and entire 790-file website baseline / '
              '803-file candidate pass whole-tree bytes, actual inherited modes, hidden/empty topology, '
              '13 additions / 2 modifications / 15 Git paths with public/ once, six added directories, 788 untouched files, 381 old '
              'directory modes, shared CSS and 17 DS_Store checks. Actual old modes 764x0644 + 24x0600 + 2x0666 '
              'are preserved in each copy; only 13 new payloads require 0644.\n\n'
              'All three actual root adoption formats and all 12 source/private manifests pass, including '
              'externally bound circular terminal pairs. Whole accepted articles match outside independently '
              'derived 8/7/7 HEAD spans; complete BODY/MAIN, abstracts, BibTeX and seven native assets are exact. '
              'Canonical/OG/absolute Scholar PDF and native encoding URLs are valid; exact scholarly data, '
              'original 6 October dates and native version distinctions remain faithful. Rights, AI disclosure '
              'and passive collaboration remain within byte-identical accepted content.\n\n'
              'All 130 old whole HTML units, concatenated HTMLParser data-event bytes, raw/typed JSON units '
              'and positions, 131 whole XML units and complete parsed root/children including text/tails/'
              'attribute order remain exact prefixes. New listings retain their two-paragraph form. '
              'Independent 3 index + 1 XML closed edit proofs reconstruct both complete buffers forward and backward; '
              'sitemap lastmod 2026-11-17 is file-update metadata only.\n\n'
              'Protected native Math a4ce/index91b10 and website217d/treecb7ae0/index25494 controls, '
              'whole website public tree, 133 source files/34 summed child directories, 378 private files/25 summed child directories, '
              'root adoption/clearance buffers and whole stage remain exact before/after. The retained '
              'history remains builder 0, first administrative seal 1 and distinct passive metadata v2 zero; '
              'this audit does not independently observe past process execution beyond authenticated receipts.\n\n'
              'One fresh passive reader was saved and personally read before one invocation. No producer, '
              'scientific program or publication helper was imported, executed, AST-parsed, compiled or help-run. '
              'The checks are local/static; no actual UI, rendering, live, production, new scientific/copy, '
              'AA or publication certificate is issued. No Git write, network, deployment, website/source/'
              'other-packet mutation, Sheet action, redirect or external contact occurred.\n')
    require(not (A / 'REPORT.md').exists(), 'fresh final audit report')
    (A / 'REPORT.md').write_text(report)
    with (A / 'RESEARCH_LOG.md').open('a') as log:
        log.write('\n' + utc() + ' — Verified checkpoint, estimated 100% of assigned private audit complete. '
                  'All finite checks passed. Literal execution receipt and final own manifest remain '
                  'administrative closure. follow_up null; no later action authority.\n')

if __name__ == '__main__':
    main()
