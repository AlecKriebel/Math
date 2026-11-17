"""One read-only finite data comparison after full personal copy/source reading."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'verification/low-exponent-supersolvability-fact-sol-20261116'
N = P / 'verification/low-exponent-supersolvability-editorial-sol-20261116'
S = P / 'papers/23331709/sources'

def need(test, message):
    if not test:
        raise RuntimeError(message)

def pin(path):
    mode = path.lstat().st_mode
    need(stat.S_ISREG(mode), 'Nonordinary file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': oct(stat.S_IMODE(mode))}

def check(expected, actual, label):
    need(all(expected[k] == actual[k] for k in ('bytes', 'SHA256', 'mode')), label)

def scan(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'Nonordinary root')
    files, dirs = {}, {}
    for path in root.rglob('*'):
        rel = path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISREG(info.st_mode):
            files[rel] = pin(path)
        else:
            need(stat.S_ISDIR(info.st_mode), 'Symlink/special node')
            dirs[rel] = oct(stat.S_IMODE(info.st_mode))
    return files, dirs

check({'bytes': 10446, 'SHA256': '6d2d89ace44b565c9a523c4beaaa375e5f66131f79c8c94b5ddf7715d746fe1b', 'mode': '0o644'}, pin(N / 'FINAL.json'), 'Writer FINAL differs')
check({'bytes': 5521, 'SHA256': '03f5e41139040d259036ae5646aad5248e622612aa6f79ec3aed9e2104835f85', 'mode': '0o644'}, pin(N / 'OWNED_MANIFEST.json'), 'Writer manifest differs')
wm = json.loads((N / 'OWNED_MANIFEST.json').read_bytes())
writer_files, writer_dirs = scan(N)
need(len(writer_files) == 22 and not writer_dirs, 'Writer extent differs')
need(set(writer_files) == {x['path'] for x in wm['files']}, 'Writer names differ')
for item in wm['files']:
    actual = writer_files[item['path']]
    need(int(actual['mode'], 8) == int(item['mode'], 8), 'Writer mode differs')
    if not item.get('terminal_control'):
        need(actual['bytes'] == item['bytes'] and actual['SHA256'] == item['sha256'], 'Writer buffer differs')
need(oct(stat.S_IMODE(N.stat().st_mode)) == '0o755', 'Writer root mode differs')
check({'bytes': 863, 'SHA256': '6bcbfcce8079f31936b2bbbcd37830d3c1fd8d5a344d9fcb1280e5db9e82ccc7', 'mode': '0o644'}, pin(O / 'INITIAL_SEAL.json'), 'Own INITIAL seal changed')
check({'bytes': 1708, 'SHA256': '85964177f686fd75c54f15c7364c37174126e8aead0437b23858f2be4a631e50', 'mode': '0o644'}, pin(O / 'INITIAL_MANIFEST.json'), 'Own INITIAL manifest changed')
im = json.loads((O / 'INITIAL_MANIFEST.json').read_bytes())
for item in im['files']:
    check(item, pin(O / item['path']), 'Own original INITIAL payload changed')
expect = json.loads((O / 'SOURCE_EXPECTATIONS.json').read_bytes())
for key in ('root_clearance', 'root_report', 'controlling_TeX', 'root_PDF_text_read'):
    item = expect[key]
    check(item, pin(Path(item['path'])), 'Source/authority input changed')
for item in expect['raw_metadata'] + expect['root_original_pages_personally_inspected']:
    check(item, pin(Path(item['path'])), 'Read input changed')
check(expect['source_manifest'], pin(S / 'SOURCE_MANIFEST.json'), 'Source manifest changed')
check(expect['source_FINAL'], pin(S / 'SOURCE_FINAL.json'), 'Source FINAL changed')
sm = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
sf, sd = scan(S)
se = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in sm['files']}
se.update({'SOURCE_MANIFEST.json': pin(S / 'SOURCE_MANIFEST.json'), 'SOURCE_FINAL.json': pin(S / 'SOURCE_FINAL.json')})
need(sf == se and len(sf) == 120 and len(sd) == 17, 'Whole source byte/mode/extent changed')
need(sd == {x['path']: x['mode'] for x in sm['directories']}, 'Source directories changed')
html = (N / 'index.html').read_text()
head = (N / 'HEAD.html').read_text().rstrip('\n')
main = (N / 'MAIN.html').read_text().rstrip('\n')
need(html.count(head) == html.count(main) == 1, 'HEAD/MAIN saved extracts differ from HTML')
need(main.startswith('<main id="main">') and main.endswith('</main>'), 'MAIN envelope differs')
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.ids, self.meta, self.links, self.anchors, self.frames = [], [], {}, [], [], []
        self.text, self.scripts = {}, []
        self.main_starts = self.main_ends = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
            self.text[a['id']] = []
        if tag == 'main': self.main_starts += 1
        if tag == 'meta': self.meta[a.get('name', a.get('property'))] = a.get('content')
        if tag == 'link': self.links.append(a)
        if tag == 'a': self.anchors.append(a)
        if tag == 'iframe': self.frames.append(a)
        if tag == 'script':
            need(a.get('type') == 'application/ld+json', 'Executable/unexpected script')
            self.scripts.append([])
        if tag not in ('meta', 'link', 'br', 'img', 'hr', 'input'):
            self.stack.append((tag, a.get('id')))
    def handle_endtag(self, tag):
        if tag == 'main': self.main_ends += 1
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
    def handle_data(self, data):
        for tag, name in self.stack:
            if name is not None: self.text[name].append(data)
        if self.stack and self.stack[-1][0] == 'script': self.scripts[-1].append(data)
page = Page()
page.feed(html)
need(page.main_starts == page.main_ends == 1 and len(page.ids) == len(set(page.ids)), 'MAIN or ids not unique')
for a in page.anchors:
    if a.get('href', '').startswith('#'):
        need(a['href'][1:] in page.ids, 'Broken internal fragment')
def norm(text):
    return ' '.join(text.replace('K_4', 'K4').replace('’', "'").split())
expected_abstract = norm((O / 'ABSTRACT_EXPECTED.txt').read_text())
raw = expect['raw_original_abstract_TeX'].replace('Toh\\u{a}neanu', 'Tohăneanu').replace('$', '')
need(norm(raw) == expected_abstract, 'Own abstract transcription differs from source')
model = json.loads((N / 'model.json').read_bytes())
schema = json.loads(''.join(page.scripts[0]))
need(len(page.scripts) == 1 and schema == model['schema'], 'Schema/model mismatch')
for actual in (''.join(page.text['original-abstract']), page.meta['DC.description'], schema['abstract'], model['abstract'], (N / 'EXPECTED_ABSTRACT.txt').read_text()):
    need(norm(actual) == expected_abstract, 'Complete abstract mismatch')
native = expect['native_metadata_exact']
need(model['title'] == schema['name'] == page.meta['citation_title'] == native['title'], 'Title mismatch')
need(schema['datePublished'] == model['publication_date'] == page.meta['DC.date'] == native['publication_date'] == '2026-10-13', 'Publication date mismatch')
need(page.meta['citation_publication_date'] == '2026/10/13' and page.meta['citation_version'] == model['native_version'] == '1.0', 'Citation date/version mismatch')
need(model['printed_numeric_version'] is None and schema['version'] == '1.0', 'Printed/native version conflation')
need(schema['identifier'] == 'https://doi.org/10.5281/zenodo.23331709' and page.meta['citation_doi'] == '10.5281/zenodo.23331709', 'DOI mismatch')
need(page.meta['citation_author'] == schema['author']['name'] == 'Alec Kriebel', 'Author mismatch')
need(page.meta['citation_author_orcid'] == '0009-0001-9320-500X', 'ORCID mismatch')
need(model['native_record_description'] == native['description'], 'Native Description not preserved accurately')
need(all(model[x] is None for x in ('canonical', 'base_url', 'production_url', 'AA', 'follow_up')), 'Private authority boundary differs')
need(model['publication_authority'] is False and page.meta['robots'] == 'noindex, nofollow', 'Private noindex/authority differs')
need(not any(x.get('rel') == 'canonical' for x in page.links), 'Private canonical installed')
need({'rel': 'stylesheet', 'href': '../research.css'} in page.links, 'Stylesheet differs')
css = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/research.css')
need(pin(css)['bytes'] == 1170 and pin(css)['SHA256'] == 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a', 'Existing stylesheet differs')
need(len(page.frames) == 1 and page.frames[0]['src'] == 'low_exponent_supersolvability.pdf#view=FitH' and page.frames[0].get('title'), 'Local titled PDF reader differs')
assets = [x['name'] for x in expect['native_asset_pins_ordered']]
need(model['native_order'] == assets == [x['contentUrl'] for x in schema['encoding']], 'Native asset/schema order differs')
block = main.split('<ol id="native-assets">', 1)[1].split('</ol>', 1)[0]
need(block.index('href="' + assets[0] + '"') < block.index('href="' + assets[1] + '"'), 'Download native order differs')
for name in assets:
    need((N / name).read_bytes() == (S / 'assets' / name).read_bytes(), 'Original asset bytes differ')
need('same complete theorem' in main and 'Ferudun’s 12 October 2026 preprint' in main and 'https://doi.org/10.5281/zenodo.23313624' in main, 'Matching work credit differs')
need('actual contributions' in main and 'unrefereed preprint' in main and 'independent human peer review' in main, 'Status/collaboration differs')
bib = (N / 'citation.bib').read_text()
need(all(x in bib for x in ('Kriebel, Alec', '10.5281/zenodo.23331709', 'version = {1.0}', 'year = {2026}', 'month = oct', 'day = {13}', 'Unrefereed preprint')), 'Bib metadata differs')
old_description = 'A relation-incidence proof that free central arrangements with nonzero exponents 1 or 2 and at most one 3 are supersolvable, with matching-work credit.'
need(page.meta['description'] == page.meta['og:description'] == model['description'] == old_description, 'Bound copy finding changed')
replacement = 'Supersolvability in characteristic zero for finite central free arrangements of distinct hyperplanes with nonzero exponents 1 or 2 and at most one 3.'
issues = [{'id': 'COPY-1', 'severity': 'NARROW_METADATA_QUALIFICATION_REQUIRED',
    'reason': 'Short search/social description omits the characteristic-zero hypothesis even though complete visible/DC/schema abstracts retain it.',
    'locations': ['index.html meta[name=description]', 'index.html meta[property=og:description]',
                  'HEAD.html same two fields', 'model.json description'],
    'actual_text': old_description, 'suggested_faithful_text': replacement,
    'MAIN_change_required': False, 'source_scientific_clearance_changed': False}]
print(json.dumps({'status': 'DATA_CUSTODY_PASS_WITH_ONE_HUMAN_COPY_FINDING', 'record': 23331709, 'row': 167,
    'writer_FINAL': writer_files['FINAL.json'], 'writer_manifest': writer_files['OWNED_MANIFEST.json'],
    'writer_all22_buffers_modes_flat_topology_authenticated': True, 'writer_file_pins': writer_files,
    'original9_INITIAL_files_unchanged': True, 'source120_files_17_dirs_unchanged': True,
    'whole_visible_DC_schema_model_abstract_equal_independent_source_transcription': True,
    'saved_HEAD_MAIN_exact_in_index': True, 'native_originals_and_order_unchanged': True,
    'identity_dates_version_rights_private_metadata_checked': True, 'local_reader_and_links_static_only': True,
    'copy_findings_from_personal_whole_context_read': issues,
    'new_science_native_producer_helper_browser_render_network_W_Git_Sheet_mutations': False}, indent=2))
