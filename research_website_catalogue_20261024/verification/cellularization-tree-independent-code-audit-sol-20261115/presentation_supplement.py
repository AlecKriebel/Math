"""Exact root-approved shared-template supplement; original oracle stays sealed.

Imports only this audit's pre-exposure oracle and standard library. No writer
imports, source programme, subprocess, network or writes. Actual new head is
checked separately before normalizing it for the original whole-main oracle.
"""
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import copy
import json
import re
import sys
import zipfile
import io
import independent_contract as first

BUILD_DATE = '2026-11-15'


def literal(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def same(a, b):
    first.need(type(a) is type(b) and literal(a) == literal(b), 'typed/ordered whole object differs')


def page(root, record, raw, available, baseline):
    text = raw.decode(); pub = record['whole_original_publication']; url = pub['proposed_canonical_url']
    doc = first.Document(text); nodes = doc.nodes
    first.need(not any(n['tag'] == 'style' for n in nodes), 'unapproved inline stylesheet')
    for n in nodes:
        first.need(not any(k.startswith('on') or k in {'aria-hidden', 'srcdoc'} for k in n['attrs']), 'hiding/event/rawtext attribute')
    metas = {}
    for n in [v for v in nodes if v['tag'] == 'meta']:
        a = n['attrs']; key = a.get('name', a.get('property', 'charset'))
        first.need(key not in metas, 'duplicate actual head metadata')
        metas[key] = a.get('content', a.get('charset'))
    source_html = first.read_blob(root, record['source_paths']['approved_HTML']).decode()
    source_head = re.search(r'<head>[\s\S]*?</head>', source_html).group()
    source_nodes = first.Document(source_html).nodes
    expected_meta = {}
    for n in [v for v in source_nodes if v['tag'] == 'meta']:
        a = n['attrs']; expected_meta[a.get('name', a.get('property', 'charset'))] = a.get('content', a.get('charset'))
    expected_meta.update({'viewport': 'width=device-width, initial-scale=1', 'robots': 'index,follow',
        'author': pub['author'], 'citation_author_orcid': pub['orcid'], 'citation_language': 'en',
        'citation_pdf_url': urljoin(url, 'assets/' + pub['pdf_filename']), 'twitter:card': 'summary',
        'og:type': 'article', 'og:title': pub['title'], 'og:description': pub['description'],
        'og:url': url, 'og:site_name': 'Alec Kriebel'})
    first.need(metas == expected_meta, 'complete actual shared-template head metadata differs')
    first.need(first.text_of(first.one(nodes, 'title')) == pub['seo']['title'], 'actual full SEO title differs')
    links = [n['attrs'] for n in nodes if n['tag'] == 'link']
    first.need(links == [{'rel': 'canonical', 'href': url}, {'rel': 'icon', 'href': '/favicon.ico'},
                         {'rel': 'stylesheet', 'href': '/research/research.css'}], 'only exact approved canonical/favicon/shared stylesheet')
    public = Path(baseline['public_root']); by_rel = {Path(r['path']).relative_to(public).as_posix(): r for r in baseline['public_files']}
    for rel in ['research/research.css', 'favicon.ico']:
        row = by_rel[rel]; data = (public / rel).read_bytes()
        first.need(first.sha(data) == row['SHA256'] and len(data) == row['bytes'], 'installed presentation asset drift')
    script = first.one(nodes, 'script')
    first.need(script['attrs'] == {'type': 'application/ld+json'}, 'actual script must be inert JSON-LD')
    graph = json.loads(first.text_of(script)); original = json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', source_html).group(1))
    article = {k: v for k, v in original.items() if k != '@context'}
    article.update({'@id': url + '#article', 'url': url})
    article['encoding'] = []
    for asset, old_encoding in zip(record['native_assets_in_original_order'], original['encoding']):
        name = Path(asset['binding']['path']).name
        article['encoding'].append({'@type': old_encoding['@type'], 'encodingFormat': old_encoding['encodingFormat'],
            'contentUrl': urljoin(url, 'assets/' + name), 'sameAs': old_encoding['contentUrl'], 'license': pub['license_url']})
    webpage = {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': pub['title'],
        'dateModified': BUILD_DATE, 'mainEntity': {'@id': url + '#article'}}
    first.need(graph == {'@context': original['@context'], '@graph': [webpage, article]},
               'exact WebPage/ScholarlyArticle graph, original date/abstract/version/order differs')
    # Preserve the actual body while the already separately checked actual head
    # is replaced only in memory by the original head. No public output changes.
    actual_head = re.search(r'<head>[\s\S]*?</head>', text).group()
    virtual = text.replace(actual_head, source_head, 1)
    original_result = first.check_page(root, record, virtual.encode(), available)
    body = first.one(nodes, 'body'); main = first.one(nodes, 'main')
    def outside(n):
        if n is main: return ''
        return ''.join(c if isinstance(c, str) else outside(c) for c in n['children'])
    norm = lambda s: re.sub(r'\s+', ' ', s).strip()
    names = [Path(a['binding']['path']).name for a in record['native_assets_in_original_order']]
    expected_outside = 'Skip to content Alec Kriebel Research | Blog | ORCID Original Zenodo files: ' + ' · '.join(names) + ' Research home © 2013–2026 Kriebel LLC.'
    first.need(norm(outside(body)) == expected_outside, 'visible wrapper gains/loses unapproved text')
    expected_outer_hrefs = ['#main', '/', '/research/', '/blog/', pub['orcid']] + [a['whole_original_asset_identity']['original_api_file_object']['links']['self'] for a in record['native_assets_in_original_order']] + ['/research/']
    def inside_main(n):
        while n.get('parent'):
            if n is main: return True
            n = n['parent']
        return False
    outer_anchors = [n['attrs'].get('href') for n in nodes if n['tag'] == 'a' and not inside_main(n)]
    first.need(outer_anchors == expected_outer_hrefs, 'exact outer navigation/native source order differs')
    return {'record_id': record['record_id'], 'whole_preexposure_main_oracle_confirmed': original_result['whole_approved_main_exact'],
            'literal_actual_robots': metas['robots'], 'proposed_HTML_canonical_only': url,
            'source_publication_date': article['datePublished'], 'webpage_modified': BUILD_DATE,
            'exact_installed_CSS_and_favicon': True, 'shared_template_supplement_only': True}


class Spanned(first.Document):
    def __init__(self, text):
        self.source = text; self.offsets = []; total = 0
        for line in text.splitlines(keepends=True): self.offsets.append(total); total += len(line)
        super().__init__(text)

    def at(self):
        line, col = self.getpos(); return self.offsets[line - 1] + col

    def handle_starttag(self, tag, attrs):
        start = self.at(); super().handle_starttag(tag, attrs); self.nodes[-1]['begin'] = start

    def handle_endtag(self, tag):
        node = self.stack[-1]; end = self.source.index('>', self.at()) + 1
        super().handle_endtag(tag); node['end'] = end


def index(root, raw, records, baseline):
    text = raw.decode(); old = first.read_blob(root, baseline['baseline_index']).decode()
    pattern = r'<script type="application/ld\+json">([\s\S]*?)</script>'
    old_m = list(re.finditer(pattern, old)); new_m = list(re.finditer(pattern, text))
    first.need(len(old_m) == len(new_m) == 1, 'single old/new collection JSON-LD')
    original = json.loads(old_m[0].group(1)); actual = json.loads(new_m[0].group(1)); expected = copy.deepcopy(original)
    collection = expected['mainEntity']; first.need(collection['numberOfItems'] == len(collection['itemListElement']) == 85, 'old collection85')
    for i, record in enumerate(records):
        pub = record['whole_original_publication']
        collection['itemListElement'].append({'@type': 'ListItem', 'position': 86 + i, 'url': pub['proposed_canonical_url'], 'name': pub['title']})
    collection['numberOfItems'] = 87
    same(actual, expected)
    doc = Spanned(text); spans = []
    for record in records:
        pub = record['whole_original_publication']; href = '/research/' + pub['slug'] + '/'
        found = [n for n in doc.nodes if n['tag'] == 'li' and any(v['tag'] == 'a' and v['attrs'].get('href') == href for v in first.descendants(n))]
        first.need(len(found) == 1, 'single complete new index object')
        n = found[0]; first.need(not n['attrs'], 'no hidden new row attributes')
        visible = first.text_of(n)
        first.need(all(v in visible for v in [pub['title'], pub['description'], pub['publication_date_label'], 'Unrefereed preprint']), 'full new index text/date/status')
        anchors = [v for v in first.descendants(n) if v['tag'] == 'a']
        first.need([v['attrs'].get('href') for v in anchors] == [href, href + 'assets/' + pub['pdf_filename'], 'https://doi.org/' + pub['doi']], 'new row page/PDF/DOI targets')
        start, end = n['begin'], n['end']; line = text.rfind('\n', 0, start) + 1
        first.need(not text[line:start].strip(), 'new entry starts on its own line')
        start = line
        first.need(text[end:end + 1] == '\n', 'single complete new row newline')
        spans.append((start, end + 1))
    # First restore the JSON substring, then erase only the independently located
    # complete new lines; positions are adjusted by doing removals right-to-left.
    modifications = spans + [(new_m[0].start(1), new_m[0].end(1), old_m[0].group(1))]
    restored = text
    for item in sorted(modifications, key=lambda x: x[0], reverse=True):
        restored = restored[:item[0]] + (item[2] if len(item) == 3 else '') + restored[item[1]:]
    first.need(restored.encode() == old.encode(), 'every old index byte/85 typed objects must recover exactly')
    return {'old_index_bytes_exactly_recovered': True, 'old_typed_ItemList_objects': 85, 'new_complete_entries': 2, 'total': 87}


def sitemap(root, raw, records, baseline):
    text = raw.decode(); old = first.read_blob(root, baseline['baseline_sitemap']).decode(); restored = text
    for record in records:
        url = record['whole_original_publication']['proposed_canonical_url']
        expression = r'(?m)^[ \t]*<url><loc>' + re.escape(url) + r'</loc><lastmod>' + BUILD_DATE + r'</lastmod></url>\n'
        matches = list(re.finditer(expression, restored)); first.need(len(matches) == 1, 'one exact build-dated new sitemap node')
        restored = restored[:matches[0].start()] + restored[matches[0].end():]
    first.need(restored.encode() == old.encode(), 'every old sitemap byte must recover exactly')
    root_xml = first.ET.fromstring(raw); locs = [u.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text for u in root_xml]
    first.need(len(locs) == len(set(locs)) == 88, 'sitemap88 complete unique URLs')
    return {'old_sitemap_bytes_exactly_recovered': True, 'old_locations': 86, 'new_build_dated_nodes': 2, 'total': 88}


def check(root, candidate):
    root = Path(root); candidate = Path(candidate); contracts = first.load_contract(root)
    baseline = json.loads((root / 'INDEPENDENT_BASELINE.json').read_bytes()); records = contracts['records']
    paths = {'research/index.html', 'research/sitemap.xml'}
    for r in records:
        p = r['whole_original_publication']; prefix = 'research/' + p['slug'] + '/'
        paths |= {prefix + 'index.html', prefix + 'assets/' + p['pdf_filename'], prefix + 'assets/' + p['supplement_filename'], prefix + 'assets/citation.bib'}
    actual = {p.relative_to(candidate).as_posix() for p in candidate.rglob('*') if p.is_file()}
    first.need(actual == paths and len(actual) == 10, 'exact ten-output overlay fence')
    first.need(not any(p.is_symlink() for p in candidate.rglob('*')), 'no candidate symlinks')
    public = Path(baseline['public_root']); oldpaths = {Path(r['path']).relative_to(public).as_posix() for r in baseline['public_files']}
    first.need(len(oldpaths) == 585 and oldpaths & paths == {'research/index.html', 'research/sitemap.xml'} and len(oldpaths | paths) == 593, '585-to593 namespace, only2 existing overlays')
    results = []
    for r in records:
        p = r['whole_original_publication']; prefix = 'research/' + p['slug'] + '/'
        results.append(page(root, r, (candidate / prefix / 'index.html').read_bytes(), oldpaths | paths, baseline))
        for a in r['native_assets_in_original_order']:
            target = candidate / prefix / 'assets' / Path(a['binding']['path']).name
            first.need(target.read_bytes() == first.read_blob(root, a['binding']), 'complete native PDF/ZIP differs')
            if target.suffix.lower() == '.zip':
                with zipfile.ZipFile(io.BytesIO(target.read_bytes())) as z:
                    entries = [i for i in z.infolist() if not i.is_dir()]
                    first.need(len(entries) == (20 if r['record_id'] == '23439582' else 61), 'complete archive regular member count')
                    for e in entries: z.read(e)
        first.need((candidate / prefix / 'assets/citation.bib').read_bytes() == first.read_blob(root, r['source_paths']['citation']), 'whole approved BibTeX differs')
    return {'literal_custom_status': 'EXACT_ROOT_APPROVED_PRESENTATION_SUPPLEMENT_AND_ORIGINAL_INDEPENDENT_BODY_ASSET_CONTRACT_CONFIRMED',
        'records': results, 'outputs': 10, 'hypothetical_public': 593,
        'index': index(root, (candidate / 'research/index.html').read_bytes(), records, baseline),
        'sitemap': sitemap(root, (candidate / 'research/sitemap.xml').read_bytes(), records, baseline),
        'writer_code_imported': False, 'science_replayed': False, 'files_written_by_checker': False}


if __name__ == '__main__':
    first.need(len(sys.argv) == 2, 'supply immutable candidate directory')
    print(json.dumps(check(Path(__file__).resolve().parent, Path(sys.argv[1])), indent=2))
