#!/usr/bin/env python3
"""Private 11-payload assembly. Default reads only; --build writes only this folder."""
from pathlib import Path
from datetime import date
from html import escape, unescape
from html.parser import HTMLParser
from urllib.parse import urlsplit
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import xml.etree.ElementTree as ET

E = Path(__file__).resolve().parent
P = E.parent.parent
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
C = E / 'candidate'
ENV = {**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}
INITIAL_SHA = 'bc4856e04569d5b7de28bacdff46b03d1e1a3b84ceed6f562400931d6ab38a7f'

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def hp(b):
    return {'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest()}

def pin(f, base):
    s = f.lstat()
    need(stat.S_ISREG(s.st_mode) and not f.is_symlink(), 'Regular leaf: ' + str(f))
    return {'path': str(f.relative_to(base)), **hp(f.read_bytes()), 'mode': oct(stat.S_IMODE(s.st_mode))}

def git(repo, *args):
    return subprocess.check_output(['git', '--no-optional-locks', '-C', str(repo), *args], env=ENV)

def gitstate(repo):
    index = repo / '.git/index'
    raw = git(repo, 'ls-files', '--stage', '-z')
    return {'HEAD': git(repo, 'rev-parse', 'HEAD').decode().strip(),
            'tree': git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip(),
            'branch': git(repo, 'branch', '--show-current').decode().strip(),
            'index': {**hp(index.read_bytes()), 'mode': oct(stat.S_IMODE(index.stat().st_mode)),
                      'records': len(raw.split(b'\0')) - 1, 'raw_records_SHA256': hashlib.sha256(raw).hexdigest()}}

def load_inputs():
    b = (E / 'INITIAL.json').read_bytes()
    need(hp(b) == {'bytes': 2864, 'SHA256': INITIAL_SHA}, 'Fixed INITIAL')
    initial = json.loads(b)
    for name in ['BASELINE', 'BUILD_INPUTS']:
        item = initial[name]
        need(pin(E / item['path'], E) == item, 'Fixed ' + name)
    return json.loads((E / 'BASELINE.json').read_text()), json.loads((E / 'BUILD_INPUTS.json').read_text())

def guards(baseline, inputs):
    need(gitstate(W) == baseline['W'] and gitstate(P.parent) == baseline['Math'], 'Unchanged W/Math HEAD, tree and shared indices')
    leaves = sorted(f for f in (W / 'public').rglob('*') if f.is_file())
    dirs = sorted(str(f.relative_to(W)) for f in (W / 'public').rglob('*') if f.is_dir())
    need(not any(f.is_symlink() for f in (W / 'public').rglob('*')), 'No public symlinks')
    need([pin(f, W) for f in leaves] == baseline['public_file_pins'] and dirs == baseline['public_directories'], 'Complete public namespace/bytes unchanged')
    for item in inputs['source_guards']:
        need(pin(P / item['path'], P) == item, 'Frozen source guard: ' + item['path'])
    for page in inputs['pages']:
        adoption = json.loads((P / page['adoption']['path']).read_text())
        need(adoption['production_install_Git_deploy_or_tracker_authority'] is False and adoption['follow_up'] is None, 'Private adopted authority only')
        need(adoption['whole_MAIN'] == page['whole_MAIN'] and adoption['native_assets_in_order'] == page['native_assets_in_order'], 'Adopted MAIN/native contract')
        need(not (W / 'public/research' / page['slug']).exists(), 'New public slug absent')

def fragments(text, tag):
    return re.findall(r'<' + tag + r'\b[^>]*>[\s\S]*?</' + tag + '>', text)

def script(text):
    matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
    need(len(matches) == 1, 'One scholarly/index JSON-LD block')
    return matches[0]

def typed_parts(raw):
    start = raw.index('[', raw.index('"itemListElement"'))
    decoder = json.JSONDecoder()
    items, end = decoder.raw_decode(raw, start)
    close = end - 1
    cursor = start + 1
    spans = []
    for _ in items:
        while raw[cursor].isspace() or raw[cursor] == ',':
            cursor += 1
        _, stop = decoder.raw_decode(raw, cursor)
        spans.append(raw[cursor:stop])
        cursor = stop
    return close, spans

def public_page(page):
    source = (P / page['editorial_folder'] / 'preview/index.html').read_text()
    oldhead = fragments(source, 'head')[0]
    main = fragments(source, 'main')[0]
    need(hp(main.encode()) == page['whole_MAIN'], 'Whole adopted MAIN before composition')
    pdf = next(x['name'] for x in page['native_assets_in_order'] if x['name'].endswith('.pdf'))
    head = oldhead.replace('content="noindex, nofollow, noarchive"', 'content="index, follow, max-image-preview:large"')
    head = re.sub(r'<meta name="editorial-status"[^>]*>\n', '', head)
    head = head.replace('name="citation_pdf_url" content="' + pdf + '"', 'name="citation_pdf_url" content="' + page['canonical'] + pdf + '"')
    oldschema = script(head)
    schema = json.loads(oldschema)
    schema.update({'@id': page['canonical'] + '#article', 'url': page['canonical'],
                   'mainEntityOfPage': {'@type': 'WebPage', '@id': page['canonical']}})
    for encoding in schema['encoding']:
        encoding['contentUrl'] = page['canonical'] + encoding['name']
    need(schema['abstract'] == page['full_abstract'], 'Full adopted abstract')
    head = head.replace(oldschema, json.dumps(schema, ensure_ascii=False))
    additions = '<link rel="canonical" href="' + page['canonical'] + '">\n<link rel="icon" href="/favicon.ico">\n'
    additions += '<meta property="og:url" content="' + page['canonical'] + '">\n<meta property="og:site_name" content="Alec Kriebel">\n'
    head = head.replace('<link rel="stylesheet" href="research.css">', additions + '<link rel="stylesheet" href="/research/research.css">')
    result = source.replace(oldhead, head, 1)
    need(fragments(result, 'main')[0] == main, 'No adopted MAIN byte changes')
    return result.encode()

def aggregates(inputs):
    old = (W / 'public/research/index.html').read_text()
    raw = script(old)
    entity = json.loads(raw)['mainEntity']
    need(entity['numberOfItems'] == 109 and len(entity['itemListElement']) == 109, '109 original typed entries')
    close, _ = typed_parts(raw)
    added = []
    visible = []
    for position, page in enumerate(inputs['pages'], 110):
        added.append({'@type': 'ListItem', 'position': position, 'url': page['canonical'], 'name': page['title']})
        day = date.fromisoformat(page['date'])
        displayed = str(day.day) + ' ' + day.strftime('%B %Y')
        local = '/research/' + page['slug'] + '/'
        pdf = next(x['name'] for x in page['native_assets_in_order'] if x['name'].endswith('.pdf'))
        visible.append('      <li><a href="' + local + '">' + escape(page['title']) + '</a><br><span class="entry-meta">' + displayed + ' · Unrefereed preprint</span><p>' + escape(page['meta_description']) + '</p><p><a href="' + local + pdf + '">PDF</a> · <a href="https://doi.org/10.5281/zenodo.' + str(page['record_id']) + '">Zenodo</a></p></li>\n')
    newraw = raw[:close] + ', ' + ', '.join(json.dumps(x, ensure_ascii=False) for x in added) + raw[close:]
    need(newraw.count('"numberOfItems": 109') == 1, 'One original count field')
    newraw = newraw.replace('"numberOfItems": 109', '"numberOfItems": 111', 1)
    index = old.replace(raw, newraw, 1)
    need(index.count('    </ul>') == 1, 'One visible research list')
    index = index.replace('    </ul>', ''.join(visible) + '    </ul>', 1)
    oldmap = (W / 'public/research/sitemap.xml').read_text()
    need(oldmap.count('</urlset>') == 1, 'One sitemap root')
    nodes = ''.join('  <url><loc>' + p['canonical'] + '</loc><lastmod>' + inputs['build_date'] + '</lastmod></url>\n' for p in inputs['pages'])
    sitemap = oldmap.replace('</urlset>', nodes + '</urlset>', 1)
    return {'public/research/index.html': index.encode(), 'public/research/sitemap.xml': sitemap.encode()}

def payloads(inputs):
    result = aggregates(inputs)
    for page in inputs['pages']:
        folder = 'public/research/' + page['slug'] + '/'
        result[folder + 'index.html'] = public_page(page)
        for name in ['citation.bib'] + [x['name'] for x in page['native_assets_in_order']]:
            result[folder + name] = (P / page['editorial_folder'] / 'preview' / name).read_bytes()
    need(sorted(result) == inputs['candidate_exact_paths'] and len(result) == 11, 'Exactly 9 new leaves plus 2 aggregates')
    return result

class Tags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

def verify(inputs, expected):
    need(C.is_dir() and not any(f.is_symlink() for f in C.rglob('*')), 'Finite regular candidate')
    actual = sorted(str(f.relative_to(C)) for f in C.rglob('*') if f.is_file())
    dirs = sorted(str(f.relative_to(C)) for f in C.rglob('*') if f.is_dir())
    expected_dirs = sorted(['public', 'public/research'] + ['public/research/' + p['slug'] for p in inputs['pages']])
    need(actual == inputs['candidate_exact_paths'] and dirs == expected_dirs, 'Exact candidate 11 files / 4 child directories')
    for name, b in expected.items():
        need((C / name).read_bytes() == b, 'Exact deterministic candidate: ' + name)
    for page in inputs['pages']:
        name = 'public/research/' + page['slug'] + '/index.html'
        html = (C / name).read_text()
        main = fragments(html, 'main')[0]
        head = fragments(html, 'head')[0]
        schema = json.loads(script(head))
        tags = Tags(); tags.feed(html)
        metas = {a.get('name', a.get('property')): a.get('content') for t, a in tags.tags if t == 'meta'}
        links = [a for t, a in tags.tags if t == 'link']
        need(hp(main.encode()) == page['whole_MAIN'], 'Adopted whole MAIN')
        abstract = re.search(r'<section id="original-abstract"[\s\S]*?<p>(.*?)</p>', main, re.S).group(1)
        need(unescape(abstract) == page['full_abstract'] == metas['DC.description'] == schema['abstract'], 'Full abstract visible/ScholarlyArticle/DC')
        need(schema['url'] == page['canonical'] == metas['og:url'] and schema['mainEntityOfPage']['@id'] == page['canonical'], 'Production canonical/schema/OG')
        need([a['href'] for a in links if a.get('rel') == 'canonical'] == [page['canonical']], 'Unique canonical')
        need(metas['robots'] == 'index, follow, max-image-preview:large' and 'editorial-status' not in metas and 'noindex' not in head and '<base' not in head, 'Indexable public wrapper')
        need(metas['citation_title'] == page['title'] == schema['name'] and metas['citation_version'] == page['version'], 'Native title and attributed version')
        pdf = next(x['name'] for x in page['native_assets_in_order'] if x['name'].endswith('.pdf'))
        need(metas['citation_pdf_url'] == page['canonical'] + pdf, 'Absolute local scholarly PDF citation')
        need([x['contentUrl'] for x in schema['encoding']] == [page['canonical'] + x['name'] for x in page['native_assets_in_order']], 'Absolute native-order schema assets')
        need(not re.search(r'Original Zenodo description|ROOT_REVIEW|root-clearance|2026-11-16', main), 'No private audit narrative or duplicate Description')
        ids = [a['id'] for _, a in tags.tags if 'id' in a]
        need(len(ids) == len(set(ids)), 'Unique page IDs')
        for tag, attrs in tags.tags:
            for key in ['href', 'src']:
                if key not in attrs:
                    continue
                target = attrs[key]
                split = urlsplit(target)
                if split.scheme and (split.scheme != 'https' or split.netloc != 'aleckriebel.com'):
                    continue
                if target.startswith('#'):
                    need(target[1:] in ids, 'Local page fragment')
                    continue
                rel = split.path
                need('..' not in rel.split('/'), 'No path traversal')
                rel = 'public' + rel if rel.startswith('/') else 'public/research/' + page['slug'] + '/' + rel
                if rel.endswith('/'):
                    rel += 'index.html'
                need((C / rel).is_file() or (W / rel).is_file(), 'Overlay local link: ' + target)
        for asset in page['native_assets_in_order']:
            b = (C / 'public/research' / page['slug'] / asset['name']).read_bytes()
            need(hp(b) == {k: asset[k] for k in ['bytes', 'SHA256']}, 'Exact native asset pin')
    oldindex = (W / 'public/research/index.html').read_text()
    newindex = (C / 'public/research/index.html').read_text()
    oldvisible, newvisible = fragments(oldindex, 'li'), fragments(newindex, 'li')
    oldraw, newraw = script(oldindex), script(newindex)
    oldtyped = json.loads(oldraw)['mainEntity']['itemListElement']
    entity = json.loads(newraw)['mainEntity']; newtyped = entity['itemListElement']
    need(len(oldvisible) == 109 and len(newvisible) == 111 and oldvisible == newvisible[:109], 'All 109 complete old visible items byte-preserved')
    need(oldtyped == newtyped[:109] and typed_parts(oldraw)[1] == typed_parts(newraw)[1][:109], 'All 109 entire old typed item values/raw bytes preserved')
    need(entity['numberOfItems'] == 111 and [x['position'] for x in newtyped] == list(range(1, 112)), '111 sequential typed entries')
    need(len({x['url'] for x in newtyped}) == 111, 'Unique typed URLs')
    for item, visible, page in zip(newtyped[-2:], newvisible[-2:], inputs['pages']):
        title = unescape(re.search(r'<a href="[^"]+">(.*?)</a>', visible, re.S).group(1))
        need(item['name'] == title == page['title'] and item['url'] == page['canonical'], 'Full native titles in new visible/typed entries')
    oldmap = (W / 'public/research/sitemap.xml').read_text()
    newmap = (C / 'public/research/sitemap.xml').read_text()
    oldnodes, newnodes = fragments(oldmap, 'url'), fragments(newmap, 'url')
    need(len(oldnodes) == 110 and len(newnodes) == 112 and oldnodes == newnodes[:110], 'All 110 complete old XML nodes byte-preserved')
    locs = [node.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text for node in ET.fromstring(newmap)]
    need(len(set(locs)) == 112 and all(item['url'] in locs for item in newtyped), 'Sitemap unique and index coverage complete')
    return {'status': 'PASS_PRIVATE_PUBLIC_COPY_STAGE', 'candidate_pins': [pin(C / n, C) for n in actual],
            'candidate_files': 11, 'candidate_child_directories': dirs, 'new_leaves': 9, 'aggregate_replacements': 2,
            'old_visible_and_typed_items_preserved': 109, 'old_entire_sitemap_nodes_preserved': 110,
            'projected_counts': [699, 111, 112], 'projected_native_index_records': 58639, 'protected_native_raw_records': 58628,
            'whole_MAINs_unchanged': True, 'native_assets_and_Bibs_unchanged': True, 'full_abstracts_visible_JSONLD_DC': True,
            'shared_CSS_favicon_current_public_and_sources_unchanged': True, 'W_and_Math_HEAD_tree_indices_unchanged': True,
            'render_or_science_or_network_execution': False, 'inherited_reader_limits': [p['reader_limit'] for p in inputs['pages']],
            'production_install_Git_deploy_or_tracker_authority': False}

def main():
    need(sys.argv[1:] in [[], ['--build']], 'Only read-only default or explicit --build supported')
    baseline, inputs = load_inputs()
    guards(baseline, inputs)
    expected = payloads(inputs)
    if sys.argv[1:] == ['--build']:
        need(not C.exists(), 'Exclusive new private candidate')
        C.mkdir()
        for name, b in sorted(expected.items()):
            target = C / name
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as stream:
                stream.write(b)
    result = verify(inputs, expected)
    guards(baseline, inputs)
    result['mode'] = 'private-build' if sys.argv[1:] else 'read-only-verify'
    result['candidate_writes'] = 11 if sys.argv[1:] else 0
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
