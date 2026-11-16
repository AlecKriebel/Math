#!/usr/bin/env python3
"""One fixed, read-only row-155 copy comparison. No imports of project code."""
import hashlib
import json
import re
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'verification/outer-focal-inverse-editorial-fact-sol-20261116'
E = P / 'papers/23394004/reviews/editorial'
S = P / 'papers/23394004/sources'

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

def text(s):
    return ' '.join(unescape(re.sub(r'<[^>]*>', '', s)).split())

initial = obj(O / 'INITIAL_SEAL.json')
verify(O / 'INITIAL_SEAL.json', 1904, '15b5434cd9c0288382a340130739b8bdc168b7a4d1e7aa999832d21d115f3305')
for f in initial['files']:
    verify(O / f['path'], f['bytes'], f['SHA256'])
sources = obj(O / 'SOURCE_PINS.json')
for k in ['PDF', 'ZIP', 'TeX', 'native_record', 'authored_metadata']:
    f = sources[k]
    verify(S / f['path'], f['bytes'], f['SHA256'])
for f in sources['source_rasters_personally_viewed']:
    verify(Path(sources['clean_root_source_raster_root']) / f['path'], f['bytes'], f['SHA256'])

authorities = [
    ('verification/root-clearance-23394004-20261116.json', 1627, 'c3819ef78fa9fb2fc585d072d3a0822cfa91792711bd67e3ee748c5fb97dc4bf'),
    ('papers/23394004/reviews/root/ROOT_REVIEW.md', 5802, '2e1c30e4fcd90a1342d0aac43e0c6f5ac693839212238e52bc909593233a44a0'),
]
for path, size, digest in authorities:
    verify(P / path, size, digest)
verify(E / 'FINAL.json', 4402, 'a1dd96475d5a68e8912ca55b4d2c755dea3e3a27eccf89fd620b5a3da31cd86e')
verify(E / 'OWNED_MANIFEST.json', 5069, '6465ccb32eb8971a10638dda2e0cb276c2568ac80a6afcc38051351f3e60fc87')
manifest = obj(E / 'OWNED_MANIFEST.json')
expected = {f['path'] for f in manifest['files']} | {'OWNED_MANIFEST.json', 'FINAL.json'}
actual = set()
directories = set()
for p in E.rglob('*'):
    assert not p.is_symlink(), str(p)
    if p.is_file():
        actual.add(p.relative_to(E).as_posix())
    elif p.is_dir():
        directories.add(p.relative_to(E).as_posix())
    else:
        raise AssertionError(str(p))
assert actual == expected and len(actual) == 32
assert directories == {'preview', 'renders'}
assert len(manifest['files']) == 30
for f in manifest['files']:
    verify(E / f['path'], f['bytes'], f['sha256'])

page = raw(E / 'preview/index.html').decode()
main = raw(E / 'MAIN.html').decode()
model = obj(E / 'PAGE_MODEL.json')
assert re.search(r'<main\b[\s\S]*?</main>', page).group(0) == main
for key, name in [('whole_page', 'preview/index.html'), ('whole_MAIN', 'MAIN.html'), ('BibTeX', 'preview/citation.bib'), ('stylesheet', 'preview/research.css')]:
    assert pin(E / name) == model[key]
head = re.search(r'<head>[\s\S]*?</head>', page).group(0)
assert len(head.encode()) == model['whole_head']['bytes']
assert hashlib.sha256(head.encode()).hexdigest() == model['whole_head']['sha256']

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
        for k in ['href', 'src']:
            if k in d:
                self.refs.append(d[k])
        if tag == 'link' and d.get('rel') == 'canonical':
            self.canonicals.append(d.get('href'))

h = HTML()
h.feed(page)
assert len(h.ids) == len(set(h.ids))
for ref in h.refs:
    u = urlsplit(ref)
    if u.scheme or u.netloc:
        assert u.scheme in {'https'}, ref
    elif u.path.startswith('/'):
        assert u.path in {'/', '/research/'}, ref
    elif u.path:
        assert u.path in {'research.css', 'citation.bib', 'k904a-source-verification.zip', 'k904a-outer-focal-inverse-areas.pdf'}, ref
        assert (E / 'preview' / u.path).is_file()
    elif u.fragment:
        assert u.fragment in h.ids, ref

abstract = raw(O / 'EXPECTED_ABSTRACT.txt').decode().strip()
visible = re.search(r'<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)</p>', main).group(1)
schema = json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', head).group(1))
assert text(visible) == abstract == h.meta['DC.description'] == schema['abstract'] == model['abstract'] == model['abstract_tex']
record = obj(S / 'record.response.body')
authored = obj(S / sources['authored_metadata']['path'])
assert model['native_metadata_original'] == record['metadata']
assert model['native_record_files'] == record['files']
assert model['native_files_response'] == obj(S / 'files-23394004.response.body')
assert model['authored_metadata_original'] == authored
assert model['native_description_original'] == record['metadata']['description'] == authored['description']
assert model['visible_duplicate_description'] is False
assert record['metadata']['description'] not in main
assert model['native_is_published_field'] == 'ABSENT' and 'is_published' not in record
assert model['native_created'] == record['created'] == sources['created']
assert sources['modified'] == record['modified']
assert model['native_version'] == h.meta['citation_version'] == schema['version'] == record['metadata']['version'] == authored['version'] == '1.0'
assert model['printed_version'] is None and model['printed_date'] == '15 October 2026'
title = record['metadata']['title']
assert schema['name'] == schema['headline'] == h.meta['citation_title'] == h.meta['DC.title'] == model['title'] == title
assert text(re.search(r'<h1>(.*?)</h1>', main).group(1)) == title
assert schema['datePublished'] == record['metadata']['publication_date'] == authored['publication_date'] == '2026-10-15'
assert h.meta['citation_date'] == h.meta['citation_publication_date'] == '2026/10/15'
assert h.meta['citation_doi'] == record['metadata']['doi'] == '10.5281/zenodo.23394004'
assert schema['identifier']['value'] == h.meta['citation_doi']
assert schema['license'] == 'https://creativecommons.org/licenses/by/4.0/'
assert record['metadata']['license']['id'] == authored['license'] == 'cc-by-4.0'
assert model['rights']['separate_LICENSE_present'] is False and model['rights']['no_invented_MIT_split'] is True
assert schema['creativeWorkStatus'] == 'Unrefereed preprint'
assert h.meta['citation_author_orcid'] == schema['author']['identifier'] == 'https://orcid.org/0009-0001-9320-500X'
assert h.meta['robots'] == 'noindex, nofollow, noarchive' and h.canonicals == []
for k in ['canonical_url', 'base_url', 'production_url', 'AA', 'follow_up']:
    assert model[k] is None
assert model['publication_authority'] is False

keys = [f['key'] for f in record['files']]
assert keys == model['native_asset_order'] == sources['native_original_asset_order']
ordered = re.search(r'<ol id="native-downloads">([\s\S]*?)</ol>', main).group(1)
assert re.findall(r'<li><a href="([^"]+)" download>', ordered) == keys
assert [f['name'] for f in schema['encoding']] == keys
for f, enc in zip(record['files'], schema['encoding']):
    source_bytes, preview_bytes = raw(S / 'assets' / f['key']), raw(E / 'preview' / f['key'])
    assert source_bytes == preview_bytes and len(source_bytes) == f['size']
    assert 'md5:' + hashlib.md5(source_bytes).hexdigest() == f['checksum']
    assert enc['contentUrl'] == f['key'] and enc['sameAs'] == f['links']['self']
    assert enc['contentSize'] == str(f['size']) + ' bytes'
pdf = 'k904a-outer-focal-inverse-areas.pdf'
assert h.meta['citation_pdf_url'] == pdf
assert 'src="' + pdf + '#view=FitH"' in main
assert 'href="' + pdf + '" download' in main and 'href="' + pdf + '" target="_blank"' in main
bib = raw(E / 'preview/citation.bib').decode()
for field, value in [('author', 'Kriebel, Alec'), ('title', title), ('year', '2026'), ('day', '15'), ('version', '1.0'), ('doi', record['metadata']['doi']), ('license', 'CC-BY-4.0')]:
    assert re.search(r'\b' + field + r'\s*=\s*\{' + re.escape(value) + r'\}', bib), field

render = obj(E / 'RENDER_RECEIPT.json')
d = render['diagnostics']
assert render['explicit_render_invocations'] == 1 and render['failure'] is None
assert len(d['nonlocal_page_routes_aborted']) == len(d['console_errors']) == len(d['failed_requests']) == 12
assert all(u.startswith('chrome://resources/') for u in d['nonlocal_page_routes_aborted'])
assert all(e == 'Failed to load resource: net::ERR_FAILED' for e in d['console_errors'])
assert all(f['error'] == 'net::ERR_FAILED' and f['url'].startswith('chrome://resources/') for f in d['failed_requests'])
assert d['page_errors'] == [] and render['actual_embedded_PDF_display_certified'] is False
assert len(render['captures']) == 6
for capture in render['captures']:
    verify(E / capture['path'], capture['bytes'], capture['sha256'])
assert all(x['viewport'] == x['scroll'] for x in render['layouts'])
print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'PASS_DATA_ONLY_COPY_FIDELITY', 'writer_files': 32, 'writer_directories': sorted(directories), 'initial_five_files_unchanged': True, 'native_and_authored_metadata_exact': True, 'full_abstract_visible_schema_DC_exact': True, 'native_assets_exact_MD5_SHA_and_order': True, 'local_file_references_present': True, 'saved_views_bound': 6, 'literal_Chrome_resource_failures': 12, 'embedded_PDF_display_certified': False, 'new_render_scientific_native_or_network_executions': 0, 'publication_authority': False}, indent=2))
