"""Finite offline comparison of the fixed two-page stage; stdout only."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
from datetime import datetime, timezone
import hashlib, json, os, re, subprocess
import xml.etree.ElementTree as ET

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'verification/coefficient-boundary-stage-audit-sol-20261116'
S = P / 'verification/coefficient-boundary-private-stage-sol-20261116'
B = json.loads((O / 'BASELINE.json').read_text())
C = json.loads((O / 'APPROVED_CONTRACTS.json').read_text())
W = Path(B['website_root'])
checks = []

def pin(f):
    h = hashlib.sha256()
    with f.open('rb') as stream:
        while block := stream.read(1048576): h.update(block)
    return {'bytes': f.stat().st_size, 'SHA256': h.hexdigest(), 'mode': oct(f.stat().st_mode & 0o777)}

def check(name, ok):
    if not ok: raise AssertionError(name)
    checks.append(name)

class Parsed(HTMLParser):
    def __init__(self, s):
        super().__init__(convert_charrefs=True)
        self.tags, self.text = [], []
        self.feed(s)
    def handle_starttag(self, tag, attrs): self.tags.append((tag, dict(attrs)))
    def handle_data(self, s): self.text.append(s)

def visible(s): return ''.join(Parsed(s).text)
def fragment(s, tag): return re.search(r'<' + tag + r'\b[^>]*>.*?</' + tag + '>', s, re.S).group()
def script(s): return re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1)
def lis(s): return re.findall(r'<li\b[^>]*>.*?</li>', fragment(s, 'ul'), re.S)
def simplepin(f): return {k: v for k, v in pin(f).items() if k != 'mode'}
def node_content(e): return ET.tostring(ET.fromstring(ET.tostring(e)))

check('actual handed FINAL pin', simplepin(S / 'FINAL.json') == {'bytes': 5067, 'SHA256': '6662f23e66ccfeb55f9aba6d1872a70876817f725b8b6125af2f60c9202ac47b'})
F = json.loads((S / 'FINAL.json').read_text())
check('actual handed manifest pin', pin(S / 'MANIFEST.json') == {k: F['manifest'][k] for k in ['bytes', 'SHA256', 'mode']})
manifest = json.loads((S / 'MANIFEST.json').read_text())
packet_files = sorted(str(f.relative_to(S)) for f in S.rglob('*') if f.is_file())
packet_dirs = sorted(str(f.relative_to(S)) for f in S.rglob('*') if f.is_dir())
check('writer exact 22 files / 5 child directories', packet_files == sorted([e['path'] for e in manifest['payload_pins']] + ['FINAL.json', 'MANIFEST.json']) and packet_dirs == manifest['directories'] and len(packet_files) == 22 and not any(f.is_symlink() for f in S.rglob('*')))
for e in manifest['payload_pins']:
    check('whole stage buffer: ' + e['path'], pin(S / e['path']) == {k: e[k] for k in ['bytes', 'SHA256', 'mode']})
initial = json.loads((O / 'INITIAL.json').read_text())
candidate = S / 'candidate'
paths = sorted(str(f.relative_to(candidate)) for f in candidate.rglob('*') if f.is_file())
check('exact fixed 10 candidate paths / 4 child directories', paths == initial['fixed_candidate_paths'] == F['exact_paths'] and len([f for f in candidate.rglob('*') if f.is_dir()]) == 4)
for e in F['candidate_pins']:
    check('FINAL candidate pin: ' + e['path'], simplepin(candidate / e['path']) == {k: e[k] for k in ['bytes', 'SHA256']})
all_local_links = []
headers, footers = [], []
for c in C:
    rid = str(c['record_id']); rel = 'public' + c['slug']; url = 'https://aleckriebel.com' + c['slug']
    approved = Path(c['approved_page']['path']).read_text()
    page = (candidate / rel / 'index.html').read_text(); main = fragment(page, 'main'); head = fragment(page, 'head')
    check(rid + ' approved whole MAIN unchanged', main == fragment(approved, 'main') and {'bytes': len(main.encode()), 'SHA256': hashlib.sha256(main.encode()).hexdigest()} == c['approved_MAIN'])
    check(rid + ' exact original BibTeX', (candidate / rel / 'citation.bib').read_bytes() == Path(c['approved_Bib']['path']).read_bytes())
    check(rid + ' original full title / single MAIN and h1', visible(fragment(main, 'h1')) == c['native_title'] and len(re.findall(r'<main\b', page)) == len(re.findall(r'<h1\b', main)) == 1)
    parsed = Parsed(page); meta = {a.get('name', a.get('property')): a.get('content') for t, a in parsed.tags if t == 'meta'}
    check(rid + ' citation identity/date/version/author', meta['citation_title'] == c['native_title'] and meta['citation_doi'] == c['native_metadata']['doi'] and meta['citation_publication_date'] == c['native_metadata']['publication_date'].replace('-', '/') and meta['citation_version'] == c['native_metadata']['version'] and meta['citation_author'] == 'Alec Kriebel' and meta['citation_author_orcid'] == 'https://orcid.org/0009-0001-9320-500X')
    pdf = next(a['native_object']['key'] for a in c['assets_in_native_order'] if a['native_object']['key'].endswith('.pdf'))
    check(rid + ' canonical/OG/PDF/shared CSS/no base or import', [a['href'] for t, a in parsed.tags if t == 'link' and a.get('rel') == 'canonical'] == [url] and meta['og:url'] == url and meta['citation_pdf_url'] == url + pdf and [a['href'] for t, a in parsed.tags if t == 'link' and a.get('rel') == 'stylesheet'] == ['/research/research.css'] and '<base' not in head and '@import' not in page)
    graph = json.loads(script(page))['@graph']; article = next(x for x in graph if x['@type'] == 'ScholarlyArticle'); webpage = next(x for x in graph if x['@type'] == 'WebPage')
    check(rid + ' full abstract in JSONLD and Dublin Core', article['abstract'] == meta['DC.description'] == visible(c['original_abstract_HTML']))
    check(rid + ' structured identity/date/rights/graph', article['name'] == c['native_title'] and article['datePublished'] == c['native_metadata']['publication_date'] and article['version'] == c['native_metadata']['version'] and article['license'] == 'https://creativecommons.org/licenses/by/4.0/' and article['url'] == webpage['url'] == url and article['mainEntityOfPage']['@id'] == webpage['@id'] and webpage['mainEntity']['@id'] == article['@id'])
    check(rid + ' native asset encoding order and original URLs', [e['name'] for e in article['encoding']] == [a['native_object']['key'] for a in c['assets_in_native_order']] and all(e['contentUrl'] == url + a['native_object']['key'] and e['sameAs'] == a['native_object']['links']['self'] for e, a in zip(article['encoding'], c['assets_in_native_order'])))
    for a in c['assets_in_native_order']:
        n = a['native_object']; b = (candidate / a['target']).read_bytes()
        check(rid + ' whole original asset / native MD5: ' + n['key'], b == Path(a['source_pin']['path']).read_bytes() and len(b) == n['size'] and 'md5:' + hashlib.md5(b).hexdigest() == n['checksum'])
    description_id = 'record-description' if rid == '22982894' else 'native-description'
    description = re.search(r'<div id="' + description_id + r'">(.*?)</div>', main, re.S).group(1)
    check(rid + ' complete distinct native Description', visible(description) == visible(c['native_metadata']['description']) and visible(description) != article['abstract'])
    check(rid + ' local PDF embed and open/download fallback', pdf + '#view=FitH' in main and 'href="' + pdf + '" download' in main)
    headers.append(fragment(page, 'header')); footers.append(fragment(page, 'footer'))
    all_local_links.append((url, page))
check('shared article header/footer across both new pages', headers[0] == headers[1] and footers[0] == footers[1])
index = (candidate / 'public/research/index.html').read_text(); oldindex = (O / 'baseline-research-index.html').read_text()
newlis = lis(index); oldlis = B['visible_old_li_HTML']; listing = json.loads(script(index))['mainEntity']; oldlisting = B['old_ItemList']
check('all 105 old visible entries exact and ordered / total107', newlis[:105] == oldlis and len(newlis) == 107)
check('all 105 old JSONLD entries exact and ordered / total107', listing['itemListElement'][:105] == oldlisting['itemListElement'] and listing['numberOfItems'] == len(listing['itemListElement']) == 107)
for c, li, item in zip(C, newlis[105:], listing['itemListElement'][105:]):
    anchors = [a for t, a in Parsed(li).tags if t == 'a']; label = visible(re.search(r'<a\b[^>]*>(.*?)</a>', li, re.S).group(1))
    check(str(c['record_id']) + ' new index full native title and stable URL', label == item['name'] == c['native_title'] and anchors[0]['href'] == c['slug'] and item['url'] == 'https://aleckriebel.com' + c['slug'])
restored = index.replace(script(index), script(oldindex), 1)
for li in newlis[105:]: restored = restored.replace('      ' + li + '\n', '', 1)
check('whole old research index restored exactly after two additions removed', restored == oldindex)
sitemap = ET.fromstring((candidate / 'public/research/sitemap.xml').read_bytes()); oldmap = ET.fromstring((O / 'baseline-research-sitemap.xml').read_bytes())
check('all 106 old sitemap URL node contents exact and ordered / total108; external tail whitespace excluded', [node_content(e) for e in sitemap[:106]] == [node_content(e) for e in oldmap] and len(sitemap) == 108)
locs = [e.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text for e in sitemap]
check('new sitemap exact stable URLs without duplicates', locs[106:] == ['https://aleckriebel.com' + c['slug'] for c in C] and len(locs) == len(set(locs)))
all_local_links.append(('https://aleckriebel.com/research/', index))
link_count = 0
for base, page in all_local_links:
    for tag, attrs in Parsed(page).tags:
        for key in ['href', 'src']:
            if key not in attrs: continue
            target = urlsplit(urljoin(base, attrs[key]))
            if target.scheme not in ['http', 'https'] or target.netloc != 'aleckriebel.com': continue
            rel = 'public' + unquote(target.path); choices = [rel] if not target.path.endswith('/') else [rel + 'index.html', rel + 'index.php']
            resolved = next((f for r in choices for f in [candidate / r, W / r] if f.is_file()), None)
            check('projected local link: ' + base + ' -> ' + attrs[key], resolved is not None)
            if target.fragment and resolved.suffix == '.html': check('HTML fragment: ' + target.fragment, target.fragment in [a['id'] for t, a in Parsed(resolved.read_text()).tags if 'id' in a])
            link_count += 1
current = [{'path': str(f.relative_to(W / 'public')), **pin(f)} for f in sorted((W / 'public').rglob('*')) if f.is_file()]
check('whole actual W674 files and modes remain exact baseline', current == B['whole_public_files'] and sorted(str(f.relative_to(W / 'public')) for f in (W / 'public').rglob('*') if f.is_dir()) == B['public_directories'])
for name, root in [('W', W), ('Math', Path(B['Math_root']))]:
    b = B['Git_read_only'][name]
    check(name + ' raw shared index and HEAD file unchanged', pin(root / '.git/index') == {k: b['index'][k] for k in ['bytes', 'SHA256', 'mode']} and pin(root / '.git/HEAD') == {k: b['HEAD_file'][k] for k in ['bytes', 'SHA256', 'mode']})
    r = subprocess.run(['git', '--no-optional-locks', 'rev-parse', 'HEAD', 'HEAD^{tree}'], cwd=root, env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}, capture_output=True, text=True)
    check(name + ' read-only HEAD/tree unchanged', r.returncode == 0 and r.stderr == '' and r.stdout == b['HEAD_read']['stdout'])
for e in B['unchanged_controls']: check('unchanged site control: ' + e['path'], pin(Path(e['path'])) == {k: e[k] for k in ['bytes', 'SHA256', 'mode']})
check('projected exact 682/107/108 and eight new leaves', len(current) + len([p for p in paths if not (W / p).exists()]) == 682 and len([p for p in paths if not (W / p).exists()]) == 8 and F['publication_authority'] is False and F['AA'] is F['follow_up'] is None)
print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'verdict': 'PASS_FIXED_TWO_PAGE_PRIVATE_STAGE_DATA_FIDELITY', 'checks': checks, 'candidate_pins': F['candidate_pins'], 'stage_FINAL': pin(S / 'FINAL.json'), 'stage_manifest': pin(S / 'MANIFEST.json'), 'baseline_counts': B['counts'], 'projected_counts': [682, 107, 108], 'local_references_resolved': link_count, 'writer_helper_browser_renderer_native_science_network_executed': False, 'writes': 0}, ensure_ascii=False, indent=2))
