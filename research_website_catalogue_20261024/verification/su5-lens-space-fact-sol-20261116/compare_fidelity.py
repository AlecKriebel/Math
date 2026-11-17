#!/usr/bin/env python3
"""Bounded data-only fact comparison. Reads fixed inputs; writes only stdout."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/su5-lens-space-fact-sol-20261116'
WRITER = P / 'verification/su5-lens-space-editorial-sol-20261116'
SOURCE = P / 'papers/23174156/sources'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def snapshot(root):
    files, directories, special = [], [], []
    for path in sorted(root.rglob('*')):
        mode = path.lstat().st_mode
        rel = path.relative_to(root).as_posix()
        if stat.S_ISREG(mode):
            body = path.read_bytes()
            files.append({'path': rel, 'bytes': len(body), 'SHA256': digest(body),
                          'mode': oct(stat.S_IMODE(mode))})
        elif stat.S_ISDIR(mode):
            directories.append({'path': rel, 'mode': oct(stat.S_IMODE(mode))})
        else:
            special.append(rel)
    return {'root_mode': oct(stat.S_IMODE(root.lstat().st_mode)),
            'files': files, 'directories': directories, 'special': special}

checks = []
def check(name, ok):
    checks.append({'name': name, 'pass': bool(ok)})

baseline = json.loads((OWN / 'SOURCE_CUSTODY.json').read_text())
source = snapshot(SOURCE)
check('source all bytes modes and topology unchanged', not source['special'] and
      all(source[k] == baseline[k] for k in ('root_mode', 'files', 'directories')))
seal_bytes = (OWN / 'INITIAL_SEAL.json').read_bytes()
seal = json.loads(seal_bytes)
check('original INITIAL seal pinned', digest(seal_bytes) ==
      '07725b1fc6c46ee89c068b19881c955a3e737c4f8e2f7662d9a638620bf8d730')
own_rows = {row['path']: row for row in snapshot(OWN)['files']}
check('all five immutable INITIAL payloads unchanged',
      all(own_rows.get(row['path']) == row for row in seal['payloads']))

writer = snapshot(WRITER)
writer_rows = {row['path']: row for row in writer['files']}
check('writer handed-off FINAL exact', writer_rows['FINAL.json']['SHA256'] ==
      '9e7bd6f255dc72c2d06e5bd1826aed57deca6bed88e22e4b4054725ab5848a04')
check('writer handed-off manifest exact', writer_rows['OWNED_MANIFEST.json']['SHA256'] ==
      '67719684db10797f5156a079d285a9756ffdd74073e3aefb8de985be3ce05886')
manifest = json.loads((WRITER / 'OWNED_MANIFEST.json').read_text())
check('writer exact 26-flat regular inventory', not writer['special'] and
      len(writer_rows) == 26 and not writer['directories'] and writer['root_mode'] == '0o755' and
      sorted(writer_rows) == sorted(row['path'] for row in manifest['files']))
for row in manifest['files']:
    actual = writer_rows[row['path']]
    fields_ok = int(actual['mode'], 8) == int(row['mode'], 8)
    if not row.get('terminal_control'):
        fields_ok = fields_ok and actual['bytes'] == row['bytes'] and actual['SHA256'] == row['sha256']
    check('writer manifest ' + row['path'], fields_ok)

record = json.loads((SOURCE / 'record.response.body').read_text())
order = [entry['key'] for entry in record['files']]
for entry in record['files']:
    name = entry['key']
    raw = (WRITER / name).read_bytes()
    check('native unchanged bytes and MD5 ' + name,
          raw == (SOURCE / 'assets' / name).read_bytes() and len(raw) == entry['size'] and
          'md5:' + hashlib.md5(raw).hexdigest() == entry['checksum'])

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.ids, self.links, self.iframes = {}, [], [], []
        self.abstract, self.jsonld, self.native_order = '', '', []
        self.in_abstract = self.in_schema = self.in_assets = False
        self.main_open = self.main_close = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'main':
            self.main_open += 1
            check('main semantic id', attrs.get('id') == 'main')
        if tag == 'meta':
            self.meta[attrs.get('name', attrs.get('property'))] = attrs.get('content')
        if tag == 'link':
            self.links.append(attrs)
        if tag == 'iframe':
            self.iframes.append(attrs)
        if attrs.get('id') == 'original-abstract':
            self.in_abstract = True
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.in_schema = True
        if tag == 'ol' and attrs.get('id') == 'native-assets':
            self.in_assets = True
        if tag == 'a' and self.in_assets and attrs.get('href') in order:
            self.native_order.append(attrs['href'])
    def handle_endtag(self, tag):
        if tag == 'main': self.main_close += 1
        if tag == 'p': self.in_abstract = False
        if tag == 'script': self.in_schema = False
        if tag == 'ol': self.in_assets = False
    def handle_data(self, text):
        if self.in_abstract: self.abstract += text
        if self.in_schema: self.jsonld += text

model = json.loads((WRITER / 'model.json').read_text())
html = (WRITER / 'index.html').read_text()
page = Page()
page.feed(html)
schema = json.loads(page.jsonld)
source_abstract = json.loads((OWN / 'SOURCE_PINS.json').read_text())['actual_abstract_LaTeX_complete']
for before, after in [('Reshetikhin--Turaev', 'Reshetikhin–Turaev'),
                      (r'\Z', 'ℤ'), (r'\wt', 'τ̂'), ('S^3', 'S³'),
                      (r'\sqrt5', '√5'), ('$', '')]:
    source_abstract = source_abstract.replace(before, after)
source_abstract = ' '.join(source_abstract.split())
check('whole source abstract body DC schema model and saved text equal',
      page.abstract == page.meta.get('DC.description') == schema['abstract'] == model['abstract'] ==
      (WRITER / 'EXPECTED_ABSTRACT.txt').read_text().strip() == source_abstract)
check('distinct native Description literal', model['native_record_description'] == record['metadata']['description'])
check('native order visible model and schema', page.native_order == order == model['native_order'] ==
      [entry['contentUrl'] for entry in schema['encoding']])
check('HEAD and whole MAIN exact in whole HTML', all(html.count((WRITER / name).read_text().rstrip('\n')) == 1
      for name in ('HEAD.html', 'MAIN.html')))
check('unique ids and single semantic main', len(page.ids) == len(set(page.ids)) and
      page.main_open == page.main_close == 1)
check('schema identical to model schema', schema == model['scholarly_schema'])
check('native dates identity version and rights', model['title'] == record['metadata']['title'] and
      model['record_created'] == schema['dateCreated'] == record['created'] and
      model['record_modified'] == schema['dateModified'] == record['modified'] and
      model['publication_date'] == schema['datePublished'] == record['metadata']['publication_date'] and
      model['native_version'] == schema['version'] == record['metadata']['version'] and
      model['printed_numeric_version'] is None and
      schema['identifier'] == record['doi_url'] and
      schema['license'] == 'https://creativecommons.org/licenses/by/4.0/')
check('private noindex no production canonical authority or followup',
      page.meta.get('robots') == 'noindex, nofollow' and
      not any(link.get('rel') == 'canonical' for link in page.links) and
      all(model[key] is None for key in ('canonical', 'base_url', 'production_url', 'AA', 'follow_up', 'webpage_publication_date')) and
      model['publication_authority'] is False and model['private_noindex'] is True)
check('titled PDF FitH and shared stylesheet reference only', len(page.iframes) == 1 and
      page.iframes[0].get('src') == 'pr95_note.pdf#view=FitH' and bool(page.iframes[0].get('title')) and
      {'rel': 'stylesheet', 'href': '../research.css'} in page.links)
check('writer byte mode topology unchanged across comparison', snapshot(WRITER) == writer)

result = {'status': 'PASS' if all(row['pass'] for row in checks) else 'NO_GO',
          'checks': checks, 'source_extent': {'files': len(source['files']), 'child_directories': len(source['directories'])},
          'writer_extent': {'files': len(writer['files']), 'child_directories': len(writer['directories'])},
          'writer_pins': writer['files'], 'writer_root_mode': writer['root_mode'],
          'ordinary_data_only_invocations': 1, 'scientific_native_browser_render_network_executions': 0,
          'writes_by_this_program': 0, 'visual_CSS_PDF_live_download_certification': False}
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['status'] == 'PASS' else 1)
