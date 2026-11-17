"""Data-only static editorial audit; reads immutable inputs, writes only its own receipt."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import datetime
import hashlib
import json
import re
import stat
import zipfile

BASE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = BASE / 'verification/radial-statistical-fact-sol-20261117'
WRITER = BASE / 'verification/radial-statistical-editorial-sol-20261117'
SOURCE = BASE / 'papers/22983519/sources'
NATIVE = SOURCE / 'published-source/container-001/tree/radial_statistical_counterexample'
ROOT = BASE / 'papers/22983519/reviews/root'
checks = []

def check(name, predicate, detail=None):
    entry = {'name': name, 'pass': bool(predicate)}
    if detail is not None:
        entry['detail'] = detail
    checks.append(entry)

def fingerprint(path, relative_to=None):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError('Not a regular file: ' + str(path))
    data = path.read_bytes()
    return {'path': str(path.relative_to(relative_to)) if relative_to else str(path),
            'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(),
            'mode': oct(stat.S_IMODE(info.st_mode))}

def same_pin(path, expected):
    observed = fingerprint(path)
    return all(observed[key] == expected[key] for key in ('bytes', 'SHA256', 'mode'))

def load(path):
    return json.loads(path.read_text())

class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.ids = []
        self.text_by_id = {}
        self.meta = {}
        self.links = []
        self.anchors = []
        self.iframes = []
        self.scripts = []
        self.current_script = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        ident = attrs.get('id')
        if ident is not None:
            self.ids.append(ident)
            self.text_by_id[ident] = ''
        if tag == 'meta':
            self.meta[attrs.get('name', attrs.get('property'))] = attrs.get('content')
        if tag == 'link':
            self.links.append(attrs)
        if tag == 'a':
            self.anchors.append(attrs)
        if tag == 'iframe':
            self.iframes.append(attrs)
        if tag == 'script':
            self.current_script = {'attrs': attrs, 'text': ''}
            self.scripts.append(self.current_script)
        if tag not in {'meta', 'link', 'br', 'hr', 'img', 'input', 'wbr'}:
            self.stack.append((tag, ident))

    def handle_endtag(self, tag):
        if tag == 'script':
            self.current_script = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        if self.current_script is not None:
            self.current_script['text'] += data
        for _, ident in self.stack:
            if ident is not None:
                self.text_by_id[ident] += data

clearance_path = BASE / 'verification/root-clearance-22983519-20261117.json'
check('supplied root clearance exact pin', same_pin(clearance_path, {
    'bytes': 2783, 'SHA256': 'a8ccbce4c81911c984e8ad31796d164083f4c72f4cb60ebb4db05ba3426ed7ae', 'mode': '0o644'}))
clearance = load(clearance_path)
check('full root review pin', same_pin(BASE / clearance['root_review']['path'], clearance['root_review']))
check('root full claim and null follow-up', clearance['full_every_center_all_n_at_least3_and_nonselfdual_nowhere_zero_cubic_claim'] is True and clearance['follow_up'] is None)
check('supplied writer FINAL exact pin', same_pin(WRITER / 'FINAL.json', {
    'bytes': 3695, 'SHA256': '3103f93b8543570b951aa1ad176a95f89b7b54ebf2107eda2efd0e86570701ab', 'mode': '0o644'}))
check('supplied writer manifest exact pin', same_pin(WRITER / 'OWNED_MANIFEST.json', {
    'bytes': 3042, 'SHA256': 'fbef9cc61fc0a1bd02120907f438163e4dbd6a15f41c079c7f1290079206390e', 'mode': '0o644'}))
manifest = load(WRITER / 'OWNED_MANIFEST.json')
final = load(WRITER / 'FINAL.json')
observed_files = []
observed_dirs = []
special = []
for path in sorted(WRITER.rglob('*')):
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        observed_files.append(fingerprint(path, WRITER))
    elif stat.S_ISDIR(mode):
        observed_dirs.append({'path': str(path.relative_to(WRITER)), 'mode': oct(stat.S_IMODE(mode))})
    else:
        special.append(str(path.relative_to(WRITER)))
expected_names = {entry['path'] for entry in manifest['payload_files']} | set(manifest['exact_terminal_names'])
check('complete tree including hidden ignored empty files and exact topology',
      len(observed_files) == 16 and len(observed_dirs) == 1 and not special
      and {entry['path'] for entry in observed_files} == expected_names
      and observed_dirs == manifest['directories'],
      {'files': len(observed_files), 'directories': len(observed_dirs), 'special_entries': special,
       'empty_files': [entry['path'] for entry in observed_files if entry['bytes'] == 0]})
for entry in manifest['payload_files']:
    check('writer manifest payload: ' + entry['path'], same_pin(WRITER / entry['path'], entry))
check('FINAL pins manifest', same_pin(WRITER / final['manifest']['path'], final['manifest']))
for entry in final['key_files'].values():
    check('FINAL key pin: ' + entry['path'], same_pin(WRITER / entry['path'], entry))
inputs = load(WRITER / 'INPUTS.json')
for entry in inputs['inputs']:
    check('writer inherited input pin: ' + entry['path'], same_pin(BASE / entry['path'], entry))
record = load(SOURCE / 'record.response.body')
native_files = load(SOURCE / 'files-22983519.response.body')['entries']
model = load(WRITER / 'page-model.json')
article = (WRITER / 'article.html').read_text()
head = (WRITER / 'head.html').read_text()
main = (WRITER / 'main.html').read_text()
bib = (WRITER / 'citation.bib').read_text()
doc = Document(article)
graph = json.loads(next(s['text'] for s in doc.scripts if s['attrs'].get('type') == 'application/ld+json'))['@graph']
scholarly = next(item for item in graph if item.get('@type') == 'ScholarlyArticle')
tex = (NATIVE / 'manuscript/paper.tex').read_text()
abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1)
abstract = abstract.replace(r'\emph{Open Problems in Affine Differential Geometry and Related Topics}',
                            'Open Problems in Affine Differential Geometry and Related Topics')
abstract = abstract.replace(r'$S^2(1)\times\R$', 'S²(1) × ℝ').replace(r'$1$', '1').replace('Levi--Civita', 'Levi–Civita')
abstract = ' '.join(abstract.split())
check('complete abstract exact disclosed TeX rendering in every payload',
      abstract == (WRITER / 'ABSTRACT.txt').read_text().strip() == model['abstract'] == scholarly['abstract'] == doc.text_by_id['original-abstract'])
check('head fragment exactly embedded in actual article', '<head>\n' + head + '</head>' in article)
check('main fragment exactly embedded in actual article', main in article and article.count(main) == 1)
check('one H1 and one main, no duplicate IDs', article.count('<h1 ') == 1 and article.count('<main ') == 1 and len(doc.ids) == len(set(doc.ids)))
check('all local fragments exist', all(a['href'][1:] in doc.ids for a in doc.anchors if a.get('href', '').startswith('#')))
check('all relative file links resolve', all((WRITER / urlsplit(a['href']).path).is_file() for a in doc.anchors if a.get('href') and not urlsplit(a['href']).scheme and not a['href'].startswith(('#', '/'))))
metadata = record['metadata']
check('record identity title version original date author ORCID in model',
      model['title'] == metadata['title'] and model['doi'] == metadata['doi']
      and model['native_version'] == model['printed_version'] == metadata['version'] == '1.0.1'
      and model['publication_date'] == metadata['publication_date'] == '2026-09-26'
      and model['author']['ORCID'].endswith(metadata['creators'][0]['orcid']))
check('native full Description retained verbatim privately', model['native_description_html'] == metadata['description'])
check('original creation and later record/file updates separately retained',
      model['record_created'] == record['created'] and model['record_updated'] == record['updated']
      and model['current_file_updates'] == [{'name': item['key'], 'updated': item['updated']} for item in native_files]
      and model['current_files_not_asserted_identical_to_initial_upload'] is True)
eventual = model['deployment_proposal']['proposed_canonical_url']
check('private actual URLs and AA null, no publication authority', all(model[key] is None for key in ('canonical_url', 'base_url', 'production_url', 'AA')) and model['publication_authority'] is False and final['canonical_url'] is None and final['AA'] is None)
check('private robots retained in head model and final', doc.meta['robots'] == model['robots'] == final['robots'] == 'noindex, nofollow')
check('eventual canonical URLs internally consistent', next(link['href'] for link in doc.links if link.get('rel') == 'canonical') == doc.meta['og:url'] == scholarly['url'] == final['eventual_canonical'] == eventual)
check('citation metadata exact identity and date',
      doc.meta['citation_title'] == model['title'] and doc.meta['citation_doi'] == model['doi']
      and doc.meta['citation_author'] == 'Kriebel, Alec' and doc.meta['citation_author_orcid'] == metadata['creators'][0]['orcid']
      and doc.meta['citation_version'] == '1.0.1' and doc.meta['citation_publication_date'] == '2026/09/26')
check('scholarly identity original date version and status', scholarly['name'] == model['title'] and scholarly['datePublished'] == '2026-09-26' and scholarly['dateModified'] == '2026-10-10' and scholarly['version'] == '1.0.1' and scholarly['creativeWorkStatus'] == model['status'])
check('PDF embed direct-open download and citation paths agree',
      len(doc.iframes) == 1 and doc.iframes[0]['src'] == 'assets/paper.pdf#view=FitH'
      and any(a.get('href') == 'assets/paper.pdf' and 'download' in a for a in doc.anchors)
      and any(a.get('href') == 'assets/paper.pdf' and 'download' not in a for a in doc.anchors)
      and doc.meta['citation_pdf_url'] == eventual + 'assets/paper.pdf')
check('native three-asset order model and visible HTML',
      [item['name'] for item in model['native_asset_order']] == [item['key'] for item in record['files']] == [item['key'] for item in native_files]
      and [a['href'] for a in Document(main[main.index('<ol id="native-assets">'):main.index('</ol>')]).anchors if 'download' in a] == [item['local_path'] for item in model['native_asset_order']])
for native, item in zip(native_files, model['native_asset_order']):
    local = WRITER / item['local_path']
    data = local.read_bytes()
    check('native asset exact bytes MD5 SHA256 mode and URL: ' + native['key'],
          data == (SOURCE / 'assets' / native['key']).read_bytes()
          and len(data) == native['size'] == item['bytes']
          and 'md5:' + hashlib.md5(data).hexdigest() == native['checksum'] == item['native_checksum']
          and hashlib.sha256(data).hexdigest() == item['SHA256']
          and oct(stat.S_IMODE(local.stat().st_mode)) == item['mode'] == '0o644'
          and item['native_url'] == native['links']['content'])
for line in (WRITER / 'assets/SHA256SUMS.txt').read_text().splitlines():
    digest, filename = line.split(maxsplit=1)
    check('native SHA256SUMS: ' + filename, hashlib.sha256((WRITER / 'assets' / filename).read_bytes()).hexdigest() == digest)
with zipfile.ZipFile(WRITER / 'assets/source-and-verification.zip') as archive:
    pdfs = [name for name in archive.namelist() if name.lower().endswith('.pdf')]
    check('ZIP contains only author manuscript PDF', pdfs == ['radial_statistical_counterexample/output/pdf/paper.pdf'], pdfs)
check('BibTeX exact paper identity date version DOI', all(fragment in bib for fragment in (
    'author = {Kriebel, Alec}', 'title = {Radial orthogonality does not imply dual {1}-conformal flatness}',
    'year = {2026}', 'month = sep', 'day = {26}', 'version = {1.0.1}',
    'doi = {10.5281/zenodo.22983519}', 'url = {https://doi.org/10.5281/zenodo.22983519}')))
check('follow-up null in root model FINAL', clearance['follow_up'] is None and model['follow_up'] is None and final['follow_up'] is None)
check('public prose has no internal review receipts or dated audit narrative', not any(marker in main for marker in ('ROOT_REVIEW', 'ROOT_FINAL', 'PASS_FULL', 'EDITORIAL_CHECKS', '2026-11-17', '37 bounded', 'completion_percent')))
result = {'schema': 'independent-data-only-editorial-audit-v1',
          'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'status': 'PASS' if all(item['pass'] for item in checks) else 'FAIL',
          'checks_total': len(checks), 'checks_passed': sum(item['pass'] for item in checks),
          'checks': checks, 'writer_files': observed_files, 'writer_directories': observed_dirs,
          'writer_before_FINAL': fingerprint(WRITER / 'FINAL.json'),
          'writer_before_manifest': fingerprint(WRITER / 'OWNED_MANIFEST.json'),
          'source_clearance': fingerprint(clearance_path),
          'scientific_execution_count': 0, 'network_requests': 0,
          'live_or_visual_certification': False}
(OWN / 'DATA_AUDIT.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'status': result['status'], 'checks': result['checks_total'], 'passed': result['checks_passed'],
                  'failed': [entry['name'] for entry in checks if not entry['pass']]}))
