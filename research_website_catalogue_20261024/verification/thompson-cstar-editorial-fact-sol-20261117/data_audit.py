"""One passive identity/HTML audit; the manual copy issue is reported separately."""
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import stat

LANE = Path(__file__).resolve().parent
PROJECT = LANE.parent.parent
SOURCE = PROJECT / 'papers/23204212/sources'
WRITER = LANE.parent / 'thompson-cstar-editorial-sol-20261117'
CLEARANCE = LANE.parent / 'root-clearance-23204212-20261117.json'
REVIEW = PROJECT / 'papers/23204212/reviews/root-continuation-20261117/ROOT_REVIEW.md'
PINS = {
    SOURCE / 'SOURCE_FINAL.json': 'b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5',
    SOURCE / 'SOURCE_MANIFEST.json': 'afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be',
    WRITER / 'FINAL.json': '36c84f224773aa954a4e59a3152b2089e60c95710e88a12231931c646b1e8557',
    WRITER / 'MANIFEST.json': '4c5cb453d5fec1544e0b6556b5d858c059657f24dd547b161358f40e14314a55',
    WRITER / 'SEAL.json': 'eee46ef4f3c64b6f428538d38b64af343404fad31a152912ca926e1d7bba92d9',
    CLEARANCE: 'cf26226d4c236473c5cb75ede27c50f77e486761df16a624d39cf26abdbb797c',
    REVIEW: '71136fd6de5610566ccffa7142a2ecabac093e33bad245e06eb7a3d456d85501',
}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def file_info(path):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), str(path)
    data = path.read_bytes()
    return {'kind': 'file', 'bytes': len(data), 'sha256': digest(data),
            'md5': hashlib.md5(data).hexdigest(), 'mode_octal': oct(stat.S_IMODE(info.st_mode)),
            'mtime_ns': info.st_mtime_ns, 'empty': not data}

def inventory(root):
    entries = []
    for path in [root] + sorted(root.rglob('*')):
        relative = str(path.relative_to(root))
        info = path.lstat()
        entry = {'path': relative,
                 'hidden_component': any(p.startswith('.') for p in Path(relative).parts if p != '.')}
        if stat.S_ISDIR(info.st_mode):
            entry.update(kind='directory', mode_octal=oct(stat.S_IMODE(info.st_mode)),
                         mtime_ns=info.st_mtime_ns, empty=not any(path.iterdir()))
        else:
            entry.update(file_info(path))
        entries.append(entry)
    return entries

def guard():
    result = {}
    for label, root, files, dirs, manifest_name, exclusions in [
        ('source', SOURCE, 55, 14, 'SOURCE_MANIFEST.json', {'SOURCE_FINAL.json', 'SOURCE_MANIFEST.json'}),
        ('writer', WRITER, 27, 1, 'MANIFEST.json', set())]:
        entries = inventory(root)
        actual = {e['path']: e for e in entries}
        assert sum(e['kind'] == 'file' for e in entries) == files
        assert sum(e['kind'] == 'directory' for e in entries) - 1 == dirs
        manifest = json.loads((root / manifest_name).read_text())
        assert {e['path'] for e in manifest['entries']} | exclusions == set(actual)
        for expected in manifest['entries']:
            observed = actual[expected['path']]
            for key in ('kind', 'bytes', 'mode_octal', 'empty', 'md5', 'hidden_component'):
                if key in expected:
                    assert observed[key] == expected[key], (label, expected['path'], key)
            if 'sha256' in expected:
                assert observed['sha256'] == expected['sha256'], (label, expected['path'])
        result[label] = {'root': str(root), 'files': files, 'child_directories': dirs,
                         'manifest_exact': True, 'entries': entries}
    result['specific_inputs'] = {str(path): file_info(path) for path in PINS}
    for path, expected in PINS.items():
        assert result['specific_inputs'][str(path)]['sha256'] == expected, str(path)
    return result

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.links, self.anchors, self.iframes, self.scripts = {}, [], [], [], []
        self.script = None
        self.abstract = []
        self.in_abstract = False
        self.h1 = self.article = self.forms = self.bases = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta':
            self.meta.setdefault(a.get('name', a.get('property', '')), []).append(a.get('content'))
        if tag == 'link': self.links.append(a)
        if tag == 'a': self.anchors.append(a)
        if tag == 'iframe': self.iframes.append(a)
        if tag == 'script': self.script = {'attributes': a, 'text': ''}
        if tag == 'p' and a.get('id') == 'original-abstract': self.in_abstract = True
        self.h1 += tag == 'h1'
        self.article += tag == 'article'
        self.forms += tag == 'form'
        self.bases += tag == 'base'
    def handle_data(self, data):
        if self.in_abstract: self.abstract.append(data)
        if self.script is not None: self.script['text'] += data
    def handle_endtag(self, tag):
        if tag == 'p': self.in_abstract = False
        if tag == 'script':
            self.scripts.append(self.script)
            self.script = None

started = datetime.now(timezone.utc).isoformat()
before = guard()
(LANE / 'CUSTODY_BEFORE.json').write_text(json.dumps({'UTC': started, 'roots': before}, indent=2) + '\n')
model = json.loads((WRITER / 'MODEL.json').read_text())
final = json.loads((WRITER / 'FINAL.json').read_text())
api = json.loads((SOURCE / 'native-metadata/record-api.json').read_text())
clearance = json.loads(CLEARANCE.read_text())
assert clearance['record_id'] == '23204212' and clearance['central_defect_or_unsupported_inference'] is None
assert api['id'] == 23204212 and model['record_id'] == '23204212'
assert 'version' not in api['metadata'] and model['native_version'] is None
assert model['native_version_field_present'] is False and model['host_edition_label'] == 'v1'
assert api['metadata']['title'] == model['title']
assert api['metadata']['publication_date'] == model['native_publication_date'] == '2026-10-06'
assert api['created'] == model['native_record_created'] == '2026-10-07T05:35:37.608378+00:00'
assert api['updated'] == model['native_record_updated']
assert api['metadata']['license']['id'] == 'cc-by-4.0'
assert api['doi'] == model['doi'] == '10.5281/zenodo.23204212'
assert model['upstream_commit'] == clearance['upstream_commit'] == 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'
for field, value in final['all_null_publication_fields'].items():
    assert value is None and model[field] is None, field
assert model['publication_authority'] is final['publication_authority'] is False
assert model['private_only'] is True
html_bytes = (WRITER / 'private-page/index.html').read_bytes()
html = html_bytes.decode()
assert digest(html_bytes) == final['page_sha256'] == 'e5a368d2f5c82e10b048c21fe9e3137e503b62fa17be962e04f71bfca60eaee4'
assert digest((WRITER / 'MODEL.json').read_bytes()) == final['model_sha256']
page = Page()
page.feed(html)
page.close()
assert page.h1 == page.article == 1 and page.forms == page.bases == 0
assert page.meta['robots'] == ['noindex,nofollow']
assert page.links == [{'rel': 'stylesheet', 'href': 'research.css'}]
assert len(page.scripts) == 1 and page.scripts[0]['attributes'] == {'type': 'application/ld+json'}
schema = json.loads(page.scripts[0]['text'])
assert schema['@type'] == 'ScholarlyArticle' and schema['@context'] == 'https://schema.org'
assert schema['name'] == schema['headline'] == model['title']
assert schema['identifier'] == model['doi_url'] and schema['url'] == model['native_record_url']
assert schema['datePublished'] == model['native_publication_date']
assert schema['dateCreated'] == model['native_record_created'] and 'version' not in schema
assert schema['author']['@id'] == model['author']['orcid']
assert schema['license'] == 'https://creativecommons.org/licenses/by/4.0/'
assert model['upstream_written_proof'] in schema['citation']
for key, value in {'citation_title': model['title'], 'citation_author': 'Alec Kriebel',
                   'citation_author_orcid': model['author']['orcid'], 'citation_doi': model['doi'],
                   'citation_publication_date': '2026/10/06', 'DC.identifier': model['doi_url']}.items():
    assert page.meta[key] == [value], key
assert 'citation_version' not in page.meta
tex_path = SOURCE / 'archives/02-thompson-cstar-source.zip.extracted/main.tex'
tex = tex_path.read_text()
assert digest(tex_path.read_bytes()) == model['source_tex_sha256']
abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1).strip()
assert abstract == model['original_abstract_tex']
replacements = [('$\\Aut(F)$', 'Aut(F)'), ('$\\Comm(F)$', 'Comm(F)'), ('$F$', 'F'), ('$T$', 'T')]
assert model['abstract_rendering_replacements'] == [{'from': a, 'to': b} for a, b in replacements]
for old, new in replacements: abstract = abstract.replace(old, new)
abstract = ' '.join(abstract.split())
assert abstract == model['original_abstract_normalized'] == ''.join(page.abstract)
assert schema['abstract'] == abstract and page.meta['citation_abstract'] == [abstract]
assert digest(abstract.encode()) == model['abstract_normalized_sha256']
assert len(api['files']) == len(model['native_assets_in_original_order']) == len(schema['encoding']) == 3
names = []
for ordinal, (asset, native, encoding) in enumerate(zip(model['native_assets_in_original_order'], api['files'], schema['encoding']), 1):
    name = native['key']
    names.append(name)
    assert asset['ordinal'] == ordinal and name == asset['native_filename'] == asset['local_filename'] == encoding['name']
    original = (SOURCE / 'zenodo-files' / name).read_bytes()
    copied = (WRITER / 'private-page' / name).read_bytes()
    assert original == copied and len(original) == asset['bytes'] == native['size']
    assert digest(original) == asset['sha256']
    assert hashlib.md5(original).hexdigest() == asset['md5']
    assert native['checksum'] == 'md5:' + asset['md5']
    assert native['links']['self'] == asset['native_url'] == encoding['contentUrl']
    assert encoding['encodingFormat'] == asset['encoding_format']
    assert encoding['contentSize'] == str(len(original)) + ' bytes'
    assert any(a.get('href') == name and 'download' in a for a in page.anchors)
native_link_order = list(dict.fromkeys(a['href'] for a in page.anchors if a.get('href') in names))
assert native_link_order == names == ['thompson-cstar-verification.zip', 'thompson-cstar-source.zip', 'paper.pdf']
assert page.meta['citation_pdf_url'] == [api['files'][2]['links']['self']]
assert len(page.iframes) == 1 and page.iframes[0]['src'] == 'paper.pdf'
for anchor in page.anchors:
    href = anchor.get('href', '')
    assert not href.startswith('mailto:')
    if href and not href.startswith(('http://', 'https://', '/', '#')):
        assert '/' not in href and (WRITER / 'private-page' / href).is_file()
css = (WRITER / 'private-page/research.css').read_bytes()
assert digest(css) == 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'
bib = (WRITER / 'private-page/citation.bib').read_bytes()
assert digest(bib) == final['bib_sha256'] and 'version =' not in bib.decode()
for value in (model['title'], model['doi'], 'October 6, 2026', 'October 7, 2026'):
    assert value in bib.decode()
license_text = (SOURCE / 'archives/01-thompson-cstar-verification.zip.extracted/LICENSE_CODE.txt').read_text()
assert license_text.startswith('MIT License') and model['rights']['original_finite_check_code'] == 'MIT'
assert model['rights']['note_and_documentation'] == 'CC-BY-4.0'
for forbidden in ('31504', '31,504', '1,969', '2026-11-17', 'FINAL_REPORT', 'upstream_finite_checks.py', 'lake build'):
    assert forbidden not in html, forbidden
assert 'then takes their operator-norm closure.' in html
assert 'norm closure of the linear span' in tex
after = guard()
assert before == after, 'Protected custody changed'
ended = datetime.now(timezone.utc).isoformat()
(LANE / 'CUSTODY_AFTER.json').write_text(json.dumps({'UTC': ended, 'roots': after, 'before_after_exact': True}, indent=2) + '\n')
result = {'UTC_start': started, 'UTC_end': ended, 'status': 'PASS_DATA_IDENTITY_ONLY_COPY_ISSUE_REMAINS',
          'source55_14_writer27_1_exact': True, 'root_clearance_review_exact': True,
          'abstract_assets_metadata_schema_Bib_private_nulls_exact': True,
          'manual_copy_issue': 'Missing complex linear span in reduced-algebra definition, HTML line36',
          'full_copy_PASS': False, 'data_reader_attempts': 1,
          'scientific_source_producer_helper_execution': 0, 'network_Git_W_stage_Sheet_operations': 0}
(LANE / 'DATA_AUDIT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
