"""Independent 121/122 output contract, frozen before writer implementation.

Standard library only; no writer imports, subprocess, network or writes.
Checks whole approved main bytes and independent HTML structure/metadata/assets.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
from collections import Counter
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
import io


def need(value, label):
    if not value:
        raise ValueError(label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_blob(root, row):
    data = (root / row['blob']).read_bytes()
    need(len(data) == row['bytes'] and sha(data) == row['SHA256'], 'own raw contract blob differs')
    return data


def load_contract(root):
    return json.loads((root / 'APPROVED_CONTRACTS.json').read_bytes())


class Document(HTMLParser):
    """Strict balanced tree, retaining all text and attributes without browser repair."""
    void = {'meta', 'link', 'br', 'hr', 'img', 'input', 'source', 'wbr'}

    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.root = {'tag': '#document', 'attrs': {}, 'children': []}
        self.stack = [self.root]
        self.nodes = []
        self.doctypes = 0
        self.feed(text)
        self.close()
        need(len(self.stack) == 1, 'unclosed HTML nesting')
        need(self.doctypes == 1, 'single HTML doctype required')

    def handle_decl(self, text):
        need(text.lower() == 'doctype html' and len(self.stack) == 1, 'unexpected document declaration')
        self.doctypes += 1

    def handle_comment(self, text):
        raise ValueError('document comments outside approved contract')

    def unknown_decl(self, text):
        raise ValueError('unknown declaration')

    def handle_starttag(self, tag, attrs):
        need(len(dict(attrs)) == len(attrs), 'duplicate HTML attribute')
        attrs = dict(attrs)
        need(not ({'hidden', 'inert', 'style'} & set(attrs)), 'hidden/inert/inline-style attribute')
        need(tag not in {'template', 'noscript', 'textarea', 'xmp', 'object', 'embed', 'canvas', 'svg'},
             'inactive or outer rendering wrapper')
        parent = self.stack[-1]
        if tag == 'html': need(parent is self.root, 'html parent')
        if tag in {'head', 'body'}: need(parent['tag'] == 'html', 'head/body parent')
        if tag == 'main': need(parent['tag'] == 'body', 'main must be a direct body child')
        if parent['tag'] == 'body': need(tag in {'a', 'header', 'nav', 'main', 'footer'}, 'outer-body wrapper')
        if parent['tag'] == 'head': need(tag in {'meta', 'title', 'link', 'script', 'style'}, 'head child')
        if tag in {'meta', 'title', 'link', 'script', 'style'}: need(parent['tag'] == 'head', 'head element outside head')
        node = {'tag': tag, 'attrs': attrs, 'children': [], 'parent': parent}
        parent['children'].append(node)
        self.nodes.append(node)
        if tag not in self.void:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.void:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        need(len(self.stack) > 1 and self.stack[-1]['tag'] == tag, 'unbalanced/misnested HTML end tag: ' + tag)
        self.stack.pop()

    def handle_data(self, data):
        self.stack[-1]['children'].append(data)


def descendants(node):
    yield node
    for child in node['children']:
        if isinstance(child, dict):
            yield from descendants(child)


def text_of(node):
    return ''.join(child if isinstance(child, str) else text_of(child) for child in node['children'])


def one(nodes, tag):
    found = [n for n in nodes if n['tag'] == tag]
    need(len(found) == 1, 'single ' + tag + ' required')
    return found[0]


def main_inner(text):
    found = list(re.finditer(r'<main\b([^>]*)>([\s\S]*?)</main\s*>', text))
    need(len(found) == 1, 'single raw main required')
    return found[0].group(2)


def norm_css(text):
    return re.sub(r'\s+', '', text)


def check_page(root, record, raw, available_paths):
    pub = record['whole_original_publication']
    text = raw.decode('utf-8')
    parsed = Document(text)
    nodes = parsed.nodes
    html = one(nodes, 'html'); head = one(nodes, 'head'); body = one(nodes, 'body')
    main = one(nodes, 'main')
    need([n['tag'] for n in html['children'] if isinstance(n, dict)] == ['head', 'body'], 'ordered head/body')
    need(html['attrs'] == {'lang': 'en'} and not head['attrs'] and not body['attrs'], 'outer document attributes')
    need(all(not c.strip() for c in parsed.root['children'] if isinstance(c, str)), 'outside document text')
    need(all(not c.strip() for c in body['children'] if isinstance(c, str)), 'unapproved outer body text')
    need(main['attrs'].keys() == {'id'} and re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', main['attrs']['id']), 'main skip-id only')
    need(main_inner(text).encode() == read_blob(root, record['expected_main_inner']), 'whole approved main HTML differs')
    ids = [n['attrs']['id'] for n in nodes if 'id' in n['attrs']]
    need(len(ids) == len(set(ids)), 'duplicate document IDs')
    skip = [n for n in nodes if n['tag'] == 'a' and n['attrs'].get('href') == '#' + main['attrs']['id']]
    need(len(skip) == 1 and skip[0]['parent'] is body and 'skip' in text_of(skip[0]).lower(), 'working direct skip navigation')
    need(any(n['tag'] == 'nav' for n in nodes), 'site navigation missing')
    source_html = read_blob(root, record['source_paths']['approved_HTML']).decode()
    source_style = re.search(r'<style>([\s\S]*?)</style>', source_html).group(1)
    style = text_of(one(nodes, 'style'))
    base = norm_css(source_style); css = norm_css(style)
    need(css.count(base) == 1, 'complete approved white Arial stylesheet changed')
    extra = css.replace(base, '', 1)
    allowed_selector = re.compile(r'(?:nav|header|footer|\.site-nav|\.skip(?:-link)?)(?::(?:focus|focus-visible|hover))?(?:a(?::(?:focus|hover))?)?')
    for match in list(re.finditer(r'([^{}]+)\{([^{}]*)\}', extra)):
        need(all(allowed_selector.fullmatch(s) for s in match.group(1).split(',')), 'extra CSS reaches article or document')
        need(not re.search(r'url\(|@|visibility:hidden|display:none|opacity:0(?:;|$)', match.group(2), re.I), 'hidden or external navigation CSS')
    need(re.sub(r'[^{}]+\{[^{}]*\}', '', extra) == '', 'unparsed CSS outside approved stylesheet')
    metas = {}
    for node in [n for n in nodes if n['tag'] == 'meta']:
        a = node['attrs']; key = a.get('name', a.get('property', 'charset'))
        need(key not in metas, 'duplicate metadata key')
        metas[key] = a.get('content', a.get('charset'))
    expected = {'description': pub['description'], 'citation_title': pub['title'],
                'citation_author': pub['author'], 'citation_publication_date': pub['publication_date'].replace('-', '/'),
                'citation_version': pub['version'], 'citation_doi': pub['doi']}
    for key, value in expected.items(): need(metas.get(key) == value, 'scholarly metadata differs: ' + key)
    need(metas.get('charset', '').lower() == 'utf-8', 'Unicode document charset missing')
    need(re.sub(r'\s+', '', metas.get('viewport', '')) == 'width=device-width,initial-scale=1', 'mobile viewport differs')
    need(metas.get('robots') in {'noindex,nofollow', 'index,follow'}, 'robots policy missing or malformed')
    need(text_of(one(nodes, 'title')) == pub['seo']['title'], 'complete SEO title differs')
    proposed = pub['proposed_canonical_url']; pdf = 'assets/' + pub['pdf_filename']
    need(urljoin(proposed, metas.get('citation_pdf_url', '')) == urljoin(proposed, pdf), 'scholarly PDF target differs')
    canon = [n for n in nodes if n['tag'] == 'link' and n['attrs'].get('rel') == 'canonical']
    need(len(canon) <= 1 and all(n['attrs'].get('href') == proposed for n in canon), 'proposed canonical differs')
    need(not any(n['tag'] == 'link' and n['attrs'].get('rel') == 'stylesheet' for n in nodes), 'external stylesheet not in approved contract')
    script = one(nodes, 'script')
    need(script['attrs'] == {'type': 'application/ld+json'}, 'active script or JSON-LD attributes')
    scholarly = json.loads(text_of(script))
    original_scholarly = json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', source_html).group(1))
    for key, value in original_scholarly.items():
        if key != 'encoding': need(scholarly.get(key) == value, 'whole scholarly field differs: ' + key)
    enc = scholarly.get('encoding')
    need(isinstance(enc, list) and len(enc) == len(original_scholarly['encoding']), 'source encoding inventory/order differs')
    for saved, actual, asset in zip(original_scholarly['encoding'], enc, record['native_assets_in_original_order']):
        filename = Path(asset['binding']['path']).name
        need(set(actual) == set(saved), 'encoding schema differs')
        need(actual['@type'] == saved['@type'] and actual['encodingFormat'] == saved['encodingFormat'], 'encoding format/order differs')
        need(actual['contentUrl'] in {saved['contentUrl'], urljoin(proposed, 'assets/' + filename)}, 'encoding asset target differs')
    if 'dateModified' in scholarly:
        native = pub['source_binding']['whole_original_source_ready']
        need(scholarly['dateModified'] in {native['updated'], native['updated'][:10]}, 'modified date invented')
    for node in nodes:
        for attr in ['href', 'src']:
            if attr not in node['attrs']: continue
            value = node['attrs'][attr]; u = urlparse(value)
            need(not u.scheme or u.scheme in {'http', 'https'}, 'unsafe link scheme')
            if value.startswith('#'):
                need(value[1:] in ids, 'broken local fragment');continue
            if u.scheme and u.netloc != 'aleckriebel.com': continue
            resolved = urlparse(urljoin(proposed, value)); path = unquote(resolved.path).lstrip('/')
            if not path or path.endswith('/'): path += 'index.html'
            need(path in available_paths, 'local navigation or asset target missing: ' + path)
    if record['record_id'] == '23439582':
        visible = text_of(main)
        need('C_*' in visible and 'H_*' in visible, 'literal C_* or H_* lost')
    return {'record_id': record['record_id'], 'whole_approved_main_exact': True,
            'robots_literal': metas['robots'], 'proposed_canonical_in_HTML': bool(canon),
            'full_abstract_scholarly_metadata_and_asset_order': True}


def canonical_node(node):
    if isinstance(node, str): return node if node.strip() else ''
    return [node['tag'], sorted(node['attrs'].items()), [canonical_node(c) for c in node['children'] if not isinstance(c, str) or c.strip()]]


def index_without_new(text, new_hrefs):
    doc = Document(text)
    for node in list(doc.nodes):
        if node['tag'] == 'li' and any(n['tag'] == 'a' and n['attrs'].get('href') in new_hrefs for n in descendants(node)):
            node['parent']['children'].remove(node)
    return canonical_node(doc.root)


def check_candidate(root, candidate):
    root = Path(root); candidate = Path(candidate)
    contract = load_contract(root); baseline = json.loads((root / 'INDEPENDENT_BASELINE.json').read_bytes())
    expected_paths = {'research/index.html', 'research/sitemap.xml'}
    for record in contract['records']:
        pub = record['whole_original_publication']; prefix = 'research/' + pub['slug'] + '/'
        expected_paths.update({prefix + 'index.html', prefix + 'assets/' + pub['pdf_filename'],
                               prefix + 'assets/' + pub['supplement_filename'], prefix + 'assets/citation.bib'})
    actual = {p.relative_to(candidate).as_posix() for p in candidate.rglob('*') if p.is_file()}
    need(actual == expected_paths and len(actual) == 10, 'exact ten-output namespace differs')
    site = Path(baseline['public_root'])
    old_paths = {Path(r['path']).relative_to(site).as_posix() for r in baseline['public_files']}
    need(len(old_paths) == 585 and len(old_paths | actual) == 593, 'hypothetical public namespace count differs')
    results = []
    for record in contract['records']:
        pub = record['whole_original_publication']; prefix = 'research/' + pub['slug'] + '/'
        results.append(check_page(root, record, (candidate / prefix / 'index.html').read_bytes(), old_paths | actual))
        for asset in record['native_assets_in_original_order']:
            target = candidate / prefix / 'assets' / Path(asset['binding']['path']).name
            need(target.read_bytes() == read_blob(root, asset['binding']), 'whole original native asset differs')
            if target.suffix.lower() == '.zip':
                with zipfile.ZipFile(io.BytesIO(target.read_bytes())) as z:
                    regular = [i for i in z.infolist() if not i.is_dir()]
                    need(len(regular) == (20 if record['record_id'] == '23439582' else 61), 'whole original ZIP payload count differs')
                    for entry in regular: z.read(entry)
        need((candidate / prefix / 'assets/citation.bib').read_bytes() == read_blob(root, record['source_paths']['citation']), 'whole approved BibTeX differs')
        need(pub['canonical_url'] is None and pub['AA'] is None and pub['follow_up'] is None, 'frozen original authority boundary differs')
    new_hrefs = {'/research/' + r['whole_original_publication']['slug'] + '/' for r in contract['records']}
    old_index = read_blob(root, baseline['baseline_index']).decode()
    index = (candidate / 'research/index.html').read_text()
    need(index_without_new(index, new_hrefs) == index_without_new(old_index, set()), 'index changes beyond two complete new entries')
    hrefs = [n['attrs'].get('href') for n in Document(index).nodes if n['tag'] == 'a']
    for href in new_hrefs: need(hrefs.count(href) == 1, 'index new paper missing or duplicated')
    paper_links = [h for h in hrefs if h and re.fullmatch(r'/research/[^/]+/', h)]
    need(len(paper_links) == 87, 'research index count differs')
    for rec in contract['records']:
        pub = rec['whole_original_publication']; href = '/research/' + pub['slug'] + '/'
        li = next(n for n in Document(index).nodes if n['tag'] == 'li' and any(k['tag'] == 'a' and k['attrs'].get('href') == href for k in descendants(n)))
        visible = text_of(li)
        need(pub['title'] in visible and pub['description'] in visible and pub['publication_date_label'] in visible, 'full index title/description/date differs')
    old_xml = ET.fromstring(read_blob(root, baseline['baseline_sitemap'])); new_xml = ET.fromstring((candidate / 'research/sitemap.xml').read_bytes())
    urls = lambda x: [next(c.text for c in u if c.tag.split('}')[-1] == 'loc') for u in x]
    old_urls, new_urls = urls(old_xml), urls(new_xml)
    absolute = {'https://aleckriebel.com' + h for h in new_hrefs}
    need(len(old_urls) == 86 and len(new_urls) == 88 and len(set(new_urls)) == 88, 'research sitemap counts/uniqueness differ')
    need([u for u in new_urls if u not in absolute] == old_urls and absolute <= set(new_urls), 'sitemap old order or two additions differ')
    for u in new_xml:
        loc = next(c.text for c in u if c.tag.split('}')[-1] == 'loc')
        if loc not in absolute:
            old = next(v for v in old_xml if next(c.text for c in v if c.tag.split('}')[-1] == 'loc') == loc)
            def xml_value(node):
                return [node.tag, sorted(node.attrib.items()), (node.text or '').strip(), [xml_value(c) for c in node]]
            need(xml_value(u) == xml_value(old), 'old sitemap object changed')
        else:
            last = [c.text for c in u if c.tag.split('}')[-1] == 'lastmod']
            need(last in [[], ['2026-10-17']], 'new sitemap publication date substituted')
    return {'literal_custom_status': 'INDEPENDENT_WHOLE_BODY_NATIVE_ASSET_AND_OVERLAY_CONTRACT_CONFIRMED',
            'outputs': len(actual), 'hypothetical_public': 593, 'research_index': 87, 'research_sitemap': 88,
            'records': results, 'science_replayed': False, 'writer_code_imported': False}


if __name__ == '__main__':
    need(len(sys.argv) == 2, 'supply sealed candidate directory')
    print(json.dumps(check_candidate(Path(__file__).resolve().parent, Path(sys.argv[1])), indent=2))
