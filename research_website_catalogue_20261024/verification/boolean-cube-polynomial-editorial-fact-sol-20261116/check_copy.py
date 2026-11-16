#!/usr/bin/env python3
"""Single fixed read-only row-159 data comparison; no project-code imports."""
import hashlib
import json
import re
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'verification/boolean-cube-polynomial-editorial-fact-sol-20261116'
S = P / 'papers/23443301/sources'
E = P / 'papers/23443301/reviews/editorial'

def raw(p):
    assert p.is_file() and not p.is_symlink(), str(p)
    return p.read_bytes()

def obj(p):
    return json.loads(raw(p))

def pin(p):
    b = raw(p)
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def verify(p, size, digest):
    assert pin(p) == {'bytes': size, 'sha256': digest}, str(p)

def norm(s):
    return ' '.join(s.replace('⁸', '^8').replace('’', "'").split())

verify(O / 'INITIAL_SEAL.json', 2355, '8a309ea72d333c9bfc62e65983119bf5d83296d8e74c4e762109b687130a61c6')
for f in obj(O / 'INITIAL_SEAL.json')['files']:
    verify(O / f['path'], f['bytes'], f['sha256'])
source_pins = obj(O / 'SOURCE_PINS.json')
for k in ['TeX', 'PDF', 'ZIP', 'native_record', 'native_files', 'authored_metadata', 'actual_LICENSE']:
    f = source_pins[k]
    verify(S / f['path'], f['bytes'], f['sha256'])
for f in source_pins['existing_source_rasters_personally_viewed']:
    verify(Path(source_pins['source_raster_root']) / f['path'], f['bytes'], f['sha256'])
verify(P / 'verification/root-clearance-23443301-20261116.json', 1738, '058506fb763621da4746782e2bf438b78e673c179d30c6af598d8a8fc91675f0')
verify(P / 'papers/23443301/reviews/root/ROOT_REVIEW.md', 6419, '5bc788b50a35f7eeaecb0db20174eb34e9a7c741bc4e447069bede73849bf253')
verify(E / 'FINAL.json', 7857, 'f9dd1820c53378a1816603b483360a4dc942414bcf3fbe4c913e62686b92414b')
verify(E / 'OWNED_MANIFEST.json', 6797, '491423beef048d586d4b289b3d14459730a71d6c37f47360396a53df6e0c348a')
manifest = obj(E / 'OWNED_MANIFEST.json')
expected = {f['path'] for f in manifest['files']} | {'FINAL.json', 'OWNED_MANIFEST.json'}
actual, directories = set(), set()
for p in E.rglob('*'):
    assert not p.is_symlink(), str(p)
    if p.is_file():
        actual.add(p.relative_to(E).as_posix())
    elif p.is_dir():
        directories.add(p.relative_to(E).as_posix())
    else:
        raise AssertionError(str(p))
assert actual == expected and len(actual) == 40
assert directories == {'preview', 'renders', 'source-pages'}
assert len(manifest['files']) == 38
for f in manifest['files']:
    verify(E / f['path'], f['bytes'], f['sha256'])

page = raw(E / 'preview/index.html').decode()
main = raw(E / 'MAIN.html').decode()
head = raw(E / 'HEAD.html').decode()
model, expectations = obj(E / 'PAGE_MODEL.json'), obj(E / 'EXPECTATIONS.json')
# Remove only external fragment-file trailing LF padding; preserve all HTML/content bytes.
assert page.count(main.rstrip('\n')) == page.count(head.rstrip('\n')) == 1
assert raw(E / 'citation.bib') == raw(E / 'preview/citation.bib')
for k in ['whole_MAIN', 'head', 'whole_page', 'page_model']:
    f = obj(E / 'FINAL.json')[k]
    assert pin(E / f['path']) == {'bytes': f['bytes'], 'sha256': f['sha256']}
tex = raw(S / source_pins['TeX']['path']).decode()
tex_abstract = tex.split('\\begin{abstract}\n', 1)[1].split('\\end{abstract}', 1)[0]
assert tex_abstract == raw(O / 'EXPECTED_ABSTRACT.tex').decode() == expectations['manuscript_abstract_complete_TeX']

class HTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta, self.refs, self.ids, self.canonicals = {}, [], [], []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'meta':
            self.meta[d.get('name', d.get('property'))] = d.get('content')
        if 'id' in d:
            self.ids.append(d['id'])
        for key in ['href', 'src']:
            if key in d:
                self.refs.append(d[key])
        if tag == 'link' and d.get('rel') == 'canonical':
            self.canonicals.append(d.get('href'))

h = HTML()
h.feed(page)
assert len(h.ids) == len(set(h.ids))
for ref in h.refs:
    u = urlsplit(ref)
    if u.scheme or u.netloc:
        assert u.scheme == 'https', ref
    elif u.path.startswith('/'):
        assert u.path in {'/', '/research/'}, ref
    elif u.path:
        assert u.path in {'research.css', 'citation.bib', 'polynomial-compatibility.pdf', 'polynomial-compatibility-source-and-verification.zip'}, ref
        assert (E / 'preview' / u.path).is_file()
    elif u.fragment:
        assert u.fragment in h.ids, ref
schema = json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', head).group(1))
visible = unescape(re.search(r'<p id="original-abstract">([\s\S]*?)</p>', main).group(1))
abstract = raw(O / 'EXPECTED_ABSTRACT.txt').decode()
assert norm(abstract) == norm(visible) == norm(model['abstract']) == norm(h.meta['DC.description']) == norm(schema['abstract'])
assert model['scholarly_article'] == schema
record = obj(S / 'record.response.body')
assert expectations['native_metadata_original'] == record['metadata']
assert expectations['native_record_file_objects_original_order'] == record['files']
assert expectations['native_files_endpoint_complete_original'] == obj(S / 'files-23443301.response.body')
assert expectations['actual_LICENSE_text'] == raw(S / source_pins['actual_LICENSE']['path']).decode()
assert model['full_native_Description_body_duplication'] is False
assert record['metadata']['description'] not in main
assert model['native_created'] == schema['dateCreated'] == record['created']
assert model['native_modified'] == record['modified']
assert 'is_published' not in record
assert model['printed_numeric_version'] is None and model['printed_numeric_version_present'] is False
assert model['native_version'] == schema['version'] == h.meta['citation_version'] == record['metadata']['version'] == '1.0.0'
assert model['publication_date'] == schema['datePublished'] == h.meta['DC.date'] == record['metadata']['publication_date'] == '2026-10-17'
assert h.meta['citation_publication_date'] == '2026/10/17'
title, doi = record['metadata']['title'], record['metadata']['doi']
assert model['original_title'] == schema['name'] == schema['headline'] == h.meta['citation_title'] == h.meta['DC.title'] == title
assert model['doi'] == h.meta['citation_doi'] == doi == '10.5281/zenodo.23443301'
assert schema['identifier'] == 'https://doi.org/' + doi
assert schema['author']['identifier'] == model['author']['ORCID'] == 'https://orcid.org/0009-0001-9320-500X'
assert h.meta['citation_author_orcid'] == '0009-0001-9320-500X'
assert schema['license'] == 'https://creativecommons.org/licenses/by/4.0/'
assert record['metadata']['license']['id'] == 'cc-by-4.0' and model['rights']['MIT_inference'] is False
assert model['rights']['authored_paper_code_analysis'] == 'CC BY 4.0'
assert h.meta['robots'] == model['robots'] == 'noindex,nofollow,noarchive' and h.canonicals == []
for key in ['canonical_url', 'base_url', 'production_url', 'AA', 'follow_up']:
    assert model[key] is None
assert model['private'] is True and model['publication_authority'] is False

keys = [f['key'] for f in record['files']]
assert keys == [f['name'] for f in model['native_assets']] == source_pins['native_asset_sequence']
ordered = re.search(r'<ol id="native-assets">([\s\S]*?)</ol>', main).group(1)
assert re.findall(r'<li><a href="([^"]+)" download>', ordered) == keys
for native, offered in zip(record['files'], model['native_assets']):
    b = raw(S / 'assets' / native['key'])
    assert b == raw(E / 'preview' / native['key'])
    assert len(b) == native['size'] == offered['bytes']
    assert 'md5:' + hashlib.md5(b).hexdigest() == native['checksum']
    assert hashlib.sha256(b).hexdigest() == offered['sha256']
    assert offered['original_url'] == native['links']['self']
assert h.meta['citation_pdf_url'] == 'polynomial-compatibility.pdf'
assert 'src="polynomial-compatibility.pdf#view=FitH"' in main
assert 'href="polynomial-compatibility.pdf" download' in main
bib = raw(E / 'citation.bib').decode()
for token in ['author = {Kriebel, Alec}', 'version = {1.0.0}', 'date = {2026-10-17}', 'doi = {10.5281/zenodo.23443301}', 'license = {Creative Commons Attribution 4.0 International}']:
    assert token in bib, token
assert 'title = {' + title.replace('Boolean', '{Boolean}') + '}' in bib

layout = obj(E / 'renders/LAYOUT_RECEIPT.json')
for key in ['request_failures', 'console_errors', 'page_errors', 'blocked_HTTP_requests', 'download_clicks', 'scientific_program_executions']:
    assert layout[key] == [], key
assert layout['fatal_error'] is None and layout['native_viewer_certification'] is False
assert layout['six_views_saved'] is True and len(layout['captures']) == 6
assert all(x['saved'] is True and x['error'] is None for x in layout['captures'])
assert all(x['inner_width'] == x['document_scroll_width'] for x in layout['measurements'])
assert layout['navigation_response']['status'] == 200
assert all(urlsplit(x['url']).scheme in {'file', 'chrome', 'chrome-extension'} for x in layout['requests'])
print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'PASS_DATA_ONLY_EDITORIAL_FIDELITY', 'writer_files': 40, 'writer_child_directories': sorted(directories), 'source_first_six_files_unchanged': True, 'full_abstract_visible_schema_DC_and_model_match_after_documented_typography': True, 'literal_native_metadata_files_Description_LICENSE_retained': True, 'native_assets_exact_MD5_SHA_bytes_and_ZIP_first_order': True, 'local_file_targets_present': True, 'saved_HTML_views_bound': 6, 'literal_request_console_page_blocked_HTTP_arrays': [], 'PDF_native_live_download_certification': False, 'new_render_science_native_old_helper_or_network_executions': 0, 'publication_authority': False}, indent=2))
