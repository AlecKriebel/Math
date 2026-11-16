"""One finite, offline data comparison; reads only and prints a JSON receipt."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime, timezone
import hashlib
import json
import re

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/boundary-twist-editorial-fact-sol-20261116'
ED = P / 'papers/23430927/reviews/editorial'
SRC = P / 'papers/23430927/sources'
checks = []

def pin(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest()}

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

class Text(HTMLParser):
    def __init__(self, s):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.feed(s)
    def handle_data(self, s):
        self.parts.append(s)

def visible(s):
    return ''.join(Text(s).parts)

def norm(s):
    return ' '.join(s.split())

expected = {
    'FINAL.json': (1686, 'a7d23750f38ef3f18b98845102d35f1dc0caad10744277d5374213a71ff05eb1'),
    'OWNED_MANIFEST.json': (5838, '94ed67c80498476a81fbf08adb47134965e802ae6f3868e9435b3af86ab2ce4f'),
    'preview/index.html': (16210, 'c8726565c2390ff159b3ff9da42a21f95b39b826b013a5e5334ac64f3da20093'),
    'PAGE_MODEL.json': (9852, '39022c447cfdc34f0eed9935d9fcb29369bcd0b70b99fe7f09510802781fd765'),
    'preview/citation.bib': (444, '42c4d26388461d703fb656c3c83941027d55000190a396e1e283b4443308e36a'),
}
for name, (size, digest) in expected.items():
    check('handoff pin: ' + name, pin(ED / name) == {'bytes': size, 'SHA256': digest})
manifest = json.loads((ED / 'OWNED_MANIFEST.json').read_text())
entries = manifest['files']
files = sorted(str(p.relative_to(ED)) for p in ED.rglob('*') if p.is_file())
dirs = ['.'] + sorted(str(p.relative_to(ED)) for p in ED.rglob('*') if p.is_dir())
check('writer exact 37 ordinary files / 3 child directories', len(files) == 37 and len(dirs) == 4 and not any(p.is_symlink() for p in ED.rglob('*')))
check('writer finite path closure', files == sorted([e['path'] for e in entries] + ['FINAL.json', 'OWNED_MANIFEST.json']) and dirs == manifest['directories'])
for e in entries:
    check('whole writer buffer: ' + e['path'], pin(ED / e['path']) == {k: e[k] for k in ['bytes', 'SHA256']})
for name, digest in {
    'INITIAL.json': '058956234ccb621b690b10bd0f2e3fd80e1fd51cf484d2b3b682fc9c4b3b79fe',
    'INITIAL_SEAL.json': '51aeb8f46396728523906f4804f7d3779d397eb449cda2140da71e927f17b21f',
    'SOURCE_ONLY_RESULTS.json': '0399dfa0db9ede3e13d1865cb24798627267dec54a09106d5a1fd5bece366a33',
    'INFORMED_AUTHORITY_ADDENDUM.json': '79234f78ecac54a62e5fe3cb00caf9cf0a687a584509b5c0a6bfbcd09eb00592',
}.items():
    check('unchanged independent frozen control: ' + name, pin(OWN / name)['SHA256'] == digest)
record = json.loads((SRC / 'record.response.body').read_text())
model = json.loads((ED / 'PAGE_MODEL.json').read_text())
check('whole original native metadata', model['native_metadata'] == record['metadata'])
check('whole original native record files / order', model['native_record_files'] == record['files'])
check('whole original native files response', model['native_files_response'] == json.loads((SRC / 'files.response.body').read_text()))
check('native publication_date / created / version remain distinct', model['native_metadata']['publication_date'] == '2026-10-14' and model['native_created'] == record['created'] == '2026-10-17T05:23:48.570534+00:00' and model['native_metadata']['version'] == '1.0')
check('private model authority and URL gates', model['publication_authority'] is False and model['private_noindex'] is True and all(model[k] is None for k in ['canonical_url', 'base_url', 'production_url', 'AA', 'follow_up']))
page = (ED / 'preview/index.html').read_text()
main = re.search(r'<main\b[^>]*>.*?</main>', page, re.S).group()
head = re.search(r'<head>.*?</head>', page, re.S).group()
for key, fragment in [('whole_MAIN', main), ('whole_head', head), ('whole_page', page)]:
    b = fragment.encode()
    check('exact model ' + key, model[key] == {'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest()})
abstract = re.search(r'<section id="original-abstract".*?<p>(.*?)</p>', main, re.S).group(1)
source_abstract = (OWN / 'ORIGINAL_PRINTED_ABSTRACT.tex').read_text().replace('$', '').replace('\\geq', '≥').replace('\\leq', '≤').replace('--', '–')
check('full original abstract; only declared TeX/math typography conversion', norm(visible(abstract)) == norm(source_abstract))
description = re.search(r'<div id="native-description">(.*?)</div>', main, re.S).group(1)
check('complete distinct original native Description', visible(description) == record['metadata']['description'] and norm(visible(description)) != norm(visible(abstract)))
check('native original files in PDF then ZIP order', [e['key'] for e in record['files']] == ['preprint.pdf', 'verification_kit.zip'])
assets = []
for e in record['files']:
    native, copied = SRC / 'assets' / e['key'], ED / 'preview' / e['key']
    b = copied.read_bytes()
    check('native whole bytes and MD5: ' + e['key'], native.read_bytes() == b and len(b) == e['size'] and 'md5:' + hashlib.md5(b).hexdigest() == e['checksum'])
    assets.append({'name': e['key'], **pin(copied)})
ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', head, re.S).group(1))
check('structured original identity/date/version/rights', ld['name'] == record['metadata']['title'] and ld['datePublished'] == '2026-10-14' and ld['version'] == '1.0' and ld['license'] == 'https://creativecommons.org/licenses/by/4.0/' and ld['@id'] == 'https://doi.org/10.5281/zenodo.23430927')
check('structured native encoding order', [e['contentUrl'] for e in ld['encoding']] == ['preprint.pdf', 'verification_kit.zip'])
check('private head gates and direct PDF fallback', 'noindex, nofollow, noarchive' in head and '<base' not in head and 'rel="canonical"' not in head and 'preprint.pdf#view=FitH' in main and 'href="preprint.pdf" download' in main)
check('unchanged established CSS / no import', pin(ED / 'preview/research.css') == {'bytes': 1170, 'SHA256': 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'} and '@import' not in (ED / 'preview/research.css').read_text())
receipt = json.loads((ED / 'RENDER_RECEIPT.json').read_text())
check('saved render receipt binds page and CSS', all(receipt['inputs'][name] == pin(ED / name) for name in ['preview/index.html', 'preview/research.css']))
check('saved desktop/mobile receipt scope', [v['viewport'] for v in receipt['views']] == [1100, 390] and all(v['scroll'] == v['viewport'] and v['main'] == v['h1'] == 1 for v in receipt['views']) and receipt['page_errors'] == receipt['blocked_remote_page_requests'] == [])
print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'verdict': 'PASS_BOUNDED_DATA_FIDELITY', 'checks': checks, 'writer_files': len(files), 'writer_child_directories': len(dirs) - 1, 'candidate_pins': {n: pin(ED / n) for n in expected}, 'native_asset_pins_in_original_order': assets, 'scientific_native_writerhelper_render_Git_network_execution': False, 'writes': 0}, ensure_ascii=False, indent=2))
