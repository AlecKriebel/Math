"""Narrow read-only site-pilot release check; write evidence only in this folder."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256, md5
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urljoin, unquote
from urllib.request import urlopen
from zipfile import ZipFile
import json
import re
import xml.etree.ElementTree as ET

SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
PILOT = Path('/Users/alec/Documents/Math/research_website_pilot_20261024')
OUT = Path(__file__).parent
BASE = 'http://127.0.0.1:8765'
PAGES = ['/research/', '/research/free-spanning-forest-degree/']

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.links = []
        self.ids = []
        self.schema = []
        self._json = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.elements.append((tag, a))
        if 'id' in a:
            self.ids.append(a['id'])
        for key in ('href', 'src'):
            if key in a:
                self.links.append((tag, key, a[key]))
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self._json = ''

    def handle_endtag(self, tag):
        if tag == 'script' and self._json is not None:
            self.schema.append(json.loads(self._json))
            self._json = None

    def handle_data(self, data):
        if self._json is not None:
            self._json += data

def local_file(path):
    f = SITE / unquote(path).lstrip('/')
    return f / 'index.html' if f.is_dir() else f

def parse_file(path):
    p = Page()
    p.feed(local_file(path).read_text())
    return p

def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': sha256(data).hexdigest(), 'md5': md5(data).hexdigest()}

report = {'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'scope': 'Static HTML, all local page links/anchors, local HTTP content, frozen downloads, metadata', 'pages': {}, 'http': {}, 'artifacts': {}, 'failures': []}
urls = set(PAGES)

for path in PAGES:
    parsed = parse_file(path)
    duplicates = [key for key, count in Counter(parsed.ids).items() if count > 1]
    el = parsed.elements
    expected_canonical = 'https://aleckriebel.com' + path
    canonical = [a.get('href') for tag, a in el if tag == 'link' and a.get('rel') == 'canonical']
    og_url = [a.get('content') for tag, a in el if tag == 'meta' and a.get('property') == 'og:url']
    missing = []
    checked = []
    for tag, key, href in parsed.links:
        u = urlsplit(urljoin(BASE + path, href))
        if u.netloc != urlsplit(BASE).netloc:
            continue
        urls.add(u.path)
        f = local_file(u.path)
        ok = f.is_file()
        fragment_ok = True
        if ok and u.fragment:
            fragment_ok = (f.suffix == '.pdf' and u.fragment == 'view=FitH') or (f.suffix == '.html' and unquote(u.fragment) in parse_file(u.path).ids)
        checked.append({'reference': href, 'path': u.path, 'exists': ok, 'fragment_valid': fragment_ok})
        if not ok or not fragment_ok:
            missing.append(href)
    headings = [int(tag[1]) for tag, a in el if re.fullmatch('h[1-6]', tag)]
    skipped_headings = [(a, b) for a, b in zip(headings, headings[1:]) if b > a + 1]
    aria_missing = [value for tag, a in el for attr in ('aria-labelledby', 'aria-describedby') for value in a.get(attr, '').split() if value not in parsed.ids]
    generic_labels = [a for tag, a in el if tag in ('div', 'span') and 'aria-label' in a and not a.get('role')]
    record = {
        'identity': digest(local_file(path)), 'canonical': canonical,
        'og_url': og_url, 'canonical_consistent': canonical == [expected_canonical] and og_url == [expected_canonical],
        'language': [a.get('lang') for tag, a in el if tag == 'html'],
        'main_count': sum(tag == 'main' for tag, a in el), 'h1_count': headings.count(1),
        'duplicate_ids': duplicates, 'missing_local_references': missing,
        'skipped_heading_levels': skipped_headings, 'unresolved_aria_references': aria_missing,
        'unnamed_navigation': [a for tag, a in el if tag == 'nav' and not (a.get('aria-label') or a.get('aria-labelledby'))],
        'images_without_alt': [a for tag, a in el if tag == 'img' and 'alt' not in a],
        'aria_labels_on_generic_elements': generic_labels,
        'metadata': {a.get('name') or a.get('property'): a.get('content') for tag, a in el if tag == 'meta' and (a.get('name') or a.get('property'))},
        'schema': parsed.schema, 'checked_local_references': checked,
    }
    report['pages'][path] = record
    for key in ('duplicate_ids', 'missing_local_references', 'skipped_heading_levels', 'unresolved_aria_references', 'unnamed_navigation', 'images_without_alt'):
        if record[key]: report['failures'].append(f'{path}: {key}: {record[key]}')
    if not record['canonical_consistent'] or record['main_count'] != 1 or record['h1_count'] != 1:
        report['failures'].append(f'{path}: canonical or main/h1 structure mismatch')

css_path = '/research/research.css'
for href in re.findall(r'url\([\'"]?([^\)\'\"]+)', local_file(css_path).read_text()):
    urls.add(urlsplit(urljoin(BASE + css_path, href)).path)
urls.update(['/research/sitemap.xml', '/robots.txt'])

for path in sorted(urls):
    try:
        with urlopen(BASE + path, timeout=10) as r:
            data = r.read()
            record = {'status': r.status, 'content_type': r.headers.get('Content-Type'), 'bytes': len(data), 'matches_local_file': data == local_file(path).read_bytes()}
        if record['status'] != 200 or not record['matches_local_file']:
            report['failures'].append(f'{path}: HTTP content mismatch')
    except Exception as error:
        record = {'error': str(error)}
        report['failures'].append(f'{path}: HTTP {error}')
    report['http'][path] = record

paper_path = SITE / 'research/free-spanning-forest-degree'
for name in ('graph-square-forest-degree.pdf', 'graph-square-forest-degree-source-and-verification.zip'):
    ident = digest(paper_path / name)
    ident['matches_fresh_source_download'] = (paper_path / name).read_bytes() == (PILOT / 'sources' / name).read_bytes()
    report['artifacts'][name] = ident
    if not ident['matches_fresh_source_download']:
        report['failures'].append(name + ': published-source mismatch')

with ZipFile(paper_path / 'graph-square-forest-degree-source-and-verification.zip') as archive:
    report['artifacts']['zip_crc_error'] = archive.testzip()
    report['artifacts']['embedded_pdf_matches_download'] = archive.read('paper.pdf') == (paper_path / 'graph-square-forest-degree.pdf').read_bytes()
    report['artifacts']['certificate_sha256'] = sha256(archive.read('square_flow_certificate.json.gz')).hexdigest()
    report['artifacts']['source_metadata'] = json.loads(archive.read('zenodo-metadata.json'))

ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
tree = ET.parse(SITE / 'research/sitemap.xml')
report['sitemap'] = [{child.tag.split('}')[-1]: child.text for child in item} for item in tree.findall('s:url', ns)]
report['sitemap_matches_canonicals'] = {r['loc'] for r in report['sitemap']} == {'https://aleckriebel.com' + p for p in PAGES}
report['passed'] = not report['failures']
(OUT / 'static-results.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'passed': report['passed'], 'failures': report['failures'], 'http_paths_checked': len(report['http']), 'artifact_checks': report['artifacts'], 'sitemap': report['sitemap']}, indent=2))
