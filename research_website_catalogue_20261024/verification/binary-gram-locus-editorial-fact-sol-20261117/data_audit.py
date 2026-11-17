"""Single passive HTML/data audit with complete protected before/after custody."""
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import stat

LANE = Path(__file__).resolve().parent
PROJECT = LANE.parent.parent
SOURCE = PROJECT / 'papers/23318851/sources'
WRITER = LANE.parent / 'binary-gram-locus-editorial-sol-20261117'
CLEARANCE = LANE.parent / 'root-clearance-23318851-20261117.json'
REVIEW = PROJECT / 'papers/23318851/reviews/root-continuation-20261117/ROOT_REVIEW.md'
PINS = {
    SOURCE / 'SOURCE_FINAL.json': 'c61fb0473f0954877ab5af49e7b6139732eb4afab7cfab3377864a91dd98b317',
    SOURCE / 'SOURCE_MANIFEST.json': 'ed5c217040b7a0d72df7de7ef1d5cbce9bc516ab32c1f20ed6466ef153a6bac8',
    WRITER / 'FINAL.json': '53e6b898026ba2d566bca1226e8c851406c5f15cb7eb5ad1aefb63ff0fac9234',
    WRITER / 'FINAL_MANIFEST.json': 'd422a994ca62dd9c9ee35ba1067841065afd42e99b6763c4c93674be2a3e942c',
    CLEARANCE: 'ef479bc20bdcd8d789736abd17b9999184fee354b3a15d41bc53a6c872b807d9',
    REVIEW: 'd6d6efca566214ccb39080bd7160c3437ede74c026150bc74e149d6878867d5f',
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def one_file(path):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), str(path)
    data = path.read_bytes()
    return {'kind': 'file', 'bytes': len(data), 'SHA256': sha(data),
            'md5': hashlib.md5(data).hexdigest(), 'mode': oct(stat.S_IMODE(info.st_mode)),
            'mtime_ns': info.st_mtime_ns, 'empty': not data}

def tree(root):
    entries = []
    for path in [root] + sorted(root.rglob('*')):
        relative = str(path.relative_to(root))
        info = path.lstat()
        entry = {'path': relative, 'hidden': any(p.startswith('.') for p in Path(relative).parts if p != '.')}
        if stat.S_ISDIR(info.st_mode):
            entry.update(kind='directory', mode=oct(stat.S_IMODE(info.st_mode)),
                         mtime_ns=info.st_mtime_ns, empty=not any(path.iterdir()))
        else:
            entry.update(one_file(path))
        entries.append(entry)
    return entries

def guard():
    result = {}
    for label, root, count, dirs, manifest_name, exclusions in [
        ('source', SOURCE, 95, 16, 'SOURCE_MANIFEST.json', {'SOURCE_FINAL.json', 'SOURCE_MANIFEST.json'}),
        ('writer', WRITER, 21, 1, 'FINAL_MANIFEST.json', set())]:
        entries = tree(root)
        actual = {e['path']: e for e in entries}
        assert sum(e['kind'] == 'file' for e in entries) == count
        assert sum(e['kind'] == 'directory' for e in entries) - 1 == dirs
        manifest = json.loads((root / manifest_name).read_text())
        assert {e['path'] for e in manifest['entries']} | exclusions == set(actual)
        for expected in manifest['entries']:
            observed = actual[expected['path']]
            for key in ('kind', 'empty', 'bytes', 'md5', 'hidden'):
                if key in expected:
                    assert observed[key] == expected[key], (label, expected['path'], key)
            if 'mode_octal' in expected:
                assert observed['mode'] == expected['mode_octal']
            if 'mode' in expected:
                assert observed['mode'] == expected['mode']
            digest = expected.get('SHA256', expected.get('sha256'))
            if digest and digest != 'EXCLUDED_TERMINAL_RECURSIVE_HASH':
                assert observed['SHA256'] == digest, (label, expected['path'])
        result[label] = {'root': str(root), 'files': count, 'child_directories': dirs,
                         'manifest_exact': True, 'entries': entries}
    result['specific_inputs'] = {str(path): one_file(path) for path in PINS}
    for path, digest in PINS.items():
        assert result['specific_inputs'][str(path)]['SHA256'] == digest, str(path)
    return result

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = {}
        self.links = []
        self.anchors = []
        self.iframes = []
        self.scripts = []
        self.current_script = None
        self.in_abstract = False
        self.abstract = []
        self.h1 = 0
        self.article = 0
        self.forms = 0
        self.bases = 0
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'meta':
            self.meta.setdefault(attributes.get('name', attributes.get('property', '')), []).append(attributes.get('content'))
        if tag == 'link':
            self.links.append(attributes)
        if tag == 'a':
            self.anchors.append(attributes)
        if tag == 'iframe':
            self.iframes.append(attributes)
        if tag == 'script':
            self.current_script = {'attrs': attributes, 'text': ''}
        if tag == 'p' and attributes.get('id') == 'manuscript-abstract':
            self.in_abstract = True
        self.h1 += tag == 'h1'
        self.article += tag == 'article'
        self.forms += tag == 'form'
        self.bases += tag == 'base'
    def handle_data(self, data):
        if self.in_abstract:
            self.abstract.append(data)
        if self.current_script is not None:
            self.current_script['text'] += data
    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_abstract = False
        if tag == 'script':
            self.scripts.append(self.current_script)
            self.current_script = None

started = datetime.now(timezone.utc).isoformat()
before = guard()
(LANE / 'CUSTODY_BEFORE.json').write_text(json.dumps({'UTC': started, 'roots': before}, indent=2) + '\n')
model = json.loads((WRITER / 'MODEL.json').read_text())
final = json.loads((WRITER / 'FINAL.json').read_text())
api = json.loads((SOURCE / 'native-metadata/record-api.json').read_text())
clearance = json.loads(CLEARANCE.read_text())
assert clearance['record_id'] == '23318851' and clearance['central_defect_or_unsupported_inference'] is None
assert api['id'] == 23318851 and api['metadata']['version'] == model['native_version'] == '1.0.0'
assert api['metadata']['publication_date'] == model['native_publication_date'] == '2026-10-12'
assert api['metadata']['title'] == model['title']
assert api['metadata']['license']['id'] == 'cc-by-4.0'
assert model['DOI'] == api['doi'] == '10.5281/zenodo.23318851'
assert api['metadata']['creators'][0]['orcid'] == '0009-0001-9320-500X'
for field in ('actual_canonical', 'base_url', 'production_url', 'page_publication_date', 'AA', 'legacy_redirect', 'follow_up'):
    assert model[field] is None and final[field] is None, field
assert model['publication_authority'] is final['publication_authority'] is False
assert model['private_only'] is final['private_only'] is True
assert model['SEO']['canonical'] is None
page_bytes = (WRITER / 'private-page/index.html').read_bytes()
assert sha(page_bytes) == final['page_SHA256'] == '53e6593171f35b50514c9b1797901775a2272afc09fe0f07819c5465129feedc'
assert sha((WRITER / 'MODEL.json').read_bytes()) == final['model_SHA256']
page = Page()
page.feed(page_bytes.decode())
page.close()
assert page.h1 == page.article == 1 and page.forms == page.bases == 0
assert page.meta['robots'] == ['noindex, nofollow']
assert not any(link.get('rel') == 'canonical' for link in page.links)
assert page.links == [{'rel': 'stylesheet', 'href': 'research.css'}]
assert len(page.scripts) == 1 and page.scripts[0]['attrs'] == {'type': 'application/ld+json'}
schema = json.loads(page.scripts[0]['text'])
assert schema == model['SEO']['structured_data']
assert schema['@type'] == 'ScholarlyArticle' and schema['datePublished'] == '2026-10-12'
assert schema['url'] == 'https://doi.org/10.5281/zenodo.23318851'
assert schema['version'] == '1.0.0'
for key, value in {'citation_title': model['title'], 'citation_author': 'Alec Kriebel',
                   'citation_author_orcid': 'https://orcid.org/0009-0001-9320-500X',
                   'citation_doi': model['DOI'], 'citation_version': '1.0.0',
                   'citation_publication_date': '2026/10/12'}.items():
    assert page.meta[key] == [value], key
tex = (SOURCE / 'archives/02-gram_locus_support.zip.extracted/gram_locus_note.tex').read_text()
abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1).strip()
assert abstract == model['abstract']['source_tex']
replacements = [(r'\(n\geq3\)', 'n ≥ 3'), (r'\(n\geq4\)', 'n ≥ 4'), (r'\(n\)', 'n')]
assert model['abstract']['literal_rendering_replacements'] == [{'from': a, 'to': b} for a, b in replacements]
for old, new in replacements:
    abstract = abstract.replace(old, new)
abstract = ' '.join(abstract.split())
assert abstract == model['abstract']['normalized_full_text'] == ''.join(page.abstract)
assert schema['abstract'] == abstract and page.meta['citation_abstract'] == [abstract]
assert sha(abstract.encode()) == model['abstract']['normalized_SHA256'] == '27ecfabdbe77f251d26a2ba92e72227a09494b36493e21cc1928a809f412b9db'
assert len(api['files']) == len(model['native_assets_in_original_order']) == len(schema['encoding']) == 2
for number, (asset, native, encoding) in enumerate(zip(model['native_assets_in_original_order'], api['files'], schema['encoding']), 1):
    name = native['key']
    assert name == asset['native_filename'] == asset['local_filename'] == encoding['name']
    assert number == asset['native_order']
    original = (SOURCE / 'zenodo-files' / name).read_bytes()
    copied = (WRITER / 'private-page' / name).read_bytes()
    assert original == copied and len(original) == native['size'] == asset['bytes']
    assert sha(original) == asset['SHA256']
    assert 'md5:' + hashlib.md5(original).hexdigest() == native['checksum']
    assert encoding['contentUrl'] == asset['native_content_url'] == native['links']['self']
    assert encoding['contentSize'] == str(len(original)) + ' bytes'
    assert any(a.get('href') == name and a.get('download') == name for a in page.anchors)
assert page.meta['citation_pdf_url'] == [api['files'][0]['links']['self']]
assert len(page.iframes) == 1 and page.iframes[0]['src'] == 'gram_locus_note.pdf'
assert page.iframes[0]['title'].startswith(model['title'])
for anchor in page.anchors:
    href = anchor.get('href', '')
    assert not href.startswith('mailto:')
    if href and not href.startswith(('http://', 'https://', '/', '#')):
        assert '/' not in href and (WRITER / 'private-page' / href).is_file(), href
css = (WRITER / 'private-page/research.css').read_bytes()
assert sha(css) == model['stylesheet']['SHA256'] == final['CSS_SHA256'] == 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'
bib = (WRITER / 'private-page/citation.bib').read_text()
for value in (model['title'], model['DOI'], 'version = {1.0.0}', 'year = {2026}', 'license = {CC-BY-4.0}'):
    assert value in bib
for forbidden in ('46,274', '46274', '2026-11-17', 'GHZ', '11-factor', 'build_private.py', 'FINAL_MANIFEST'):
    assert forbidden not in page_bytes.decode(), forbidden
after = guard()
assert before == after, 'Protected namespace changed'
ended = datetime.now(timezone.utc).isoformat()
(LANE / 'CUSTODY_AFTER.json').write_text(json.dumps({'UTC': ended, 'roots': after, 'before_after_exact': True}, indent=2) + '\n')
result = {'UTC_start': started, 'UTC_end': ended, 'status': 'PASS_DATA_ONLY',
          'source_files_dirs': [95, 16], 'writer_files_dirs': [21, 1],
          'source_writer_bytes_modes_hidden_empty_topology_exact': True,
          'full_abstract_exact': True, 'native_assets_byte_identical_in_original_order': True,
          'metadata_schema_model_bib_identity_exact': True, 'private_authority_fields_null': True,
          'CSS_matches_supplied_shared_pin': True, 'W_access': False,
          'scientific_source_execution': 0, 'producer_helper_execution': 0, 'network_Git_Sheet_operations': 0,
          'data_reader_attempts': 1, 'manual_scientific_statement_map': 'FACT_REPORT.md'}
(LANE / 'DATA_AUDIT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
