"""Fresh passive, one-execution copy/data reader. It never imports or executes inputs."""
import datetime
import hashlib
import json
import re
import stat
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

BASE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = BASE / 'verification/pentagon-full-fifth-torsion-editorial-fact-sol-20261117'
WRITER = BASE / 'verification/pentagon-full-fifth-torsion-editorial-sol-20261117'
SOURCE = BASE / 'papers/23137834/sources'
PAGE = WRITER / 'private-page'
ROOT_REVIEW = 'papers/23137834/reviews/root-continuation-20261117/ROOT_REVIEW.md'
CLEARANCE = 'verification/root-clearance-23137834-20261117.json'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def read(path):
    a = path.lstat()
    assert stat.S_ISREG(a.st_mode) and not path.is_symlink(), str(path)
    data = path.read_bytes()
    b = path.lstat()
    stable = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    assert stable(a) == stable(b) and len(data) == a.st_size, str(path)
    return data


def pin(path):
    data = read(path)
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(),
            'MD5': hashlib.md5(data).hexdigest(), 'mode': oct(stat.S_IMODE(path.lstat().st_mode))}


def load(path):
    return json.loads(read(path))


def save(name, value):
    with (OWN / name).open('x') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def census(root):
    assert root.is_dir() and not root.is_symlink()
    files, directories = {}, {}
    for p in [root] + sorted(root.rglob('*')):
        s = p.lstat()
        assert not p.is_symlink(), str(p)
        relative = p.relative_to(root).as_posix()
        if stat.S_ISDIR(s.st_mode):
            directories[relative] = oct(stat.S_IMODE(s.st_mode))
        else:
            assert stat.S_ISREG(s.st_mode), str(p)
            files[relative] = pin(p)
    paths = set(files) | set(directories)
    return {'root': str(root), 'root_mode': directories.pop('.'), 'files': files,
            'directories': directories,
            'hidden_paths': sorted(p for p in paths if p != '.' and any(v.startswith('.') for v in p.split('/'))),
            'empty_files': sorted(p for p, v in files.items() if v['bytes'] == 0),
            'empty_directories': sorted(p for p in directories if not any(q.startswith(p + '/') for q in paths))}


def fixed_guard():
    entries = []
    for root in (SOURCE, WRITER):
        for p in [root] + sorted(root.rglob('*')):
            s = p.lstat()
            v = {'path': p.relative_to(BASE).as_posix(), 'mode': stat.S_IMODE(s.st_mode)}
            if stat.S_ISDIR(s.st_mode):
                assert not p.is_symlink()
                v['type'] = 'directory'
            else:
                v.update(type='file', **{k: w for k, w in pin(p).items() if k in ('bytes', 'SHA256')})
            entries.append(v)
    for relative in (ROOT_REVIEW, CLEARANCE):
        p = BASE / relative
        v = {'path': relative, 'type': 'file', 'mode': stat.S_IMODE(p.lstat().st_mode)}
        v.update({k: w for k, w in pin(p).items() if k in ('bytes', 'SHA256')})
        entries.append(v)
    return entries


def check_pin(actual, declared):
    assert set(declared) <= {'bytes', 'SHA256', 'MD5', 'mode'}
    assert declared.get('SHA256') is not None
    assert re.fullmatch('[0-9a-f]{64}', declared['SHA256'])
    assert all(actual[key] == value for key, value in declared.items())


baseline = load(OWN / 'BEFORE.json')
assert fixed_guard() == baseline['entries']
source = census(SOURCE)
writer = census(WRITER)
assert (len(source['files']), len(source['directories'])) == (97, 7)
assert (len(writer['files']), len(writer['directories'])) == (19, 1)
fixed_pins = {
    ROOT_REVIEW: (15716, 'acd210977221457737949db0684d2c60c289fef197b6b4dcaa26d87c8aa99599'),
    CLEARANCE: (2546, '55ea79efc35b209694e5afd51edd42ffa6994cb6ca755e83c981494b7e291951')}
for relative, expected in fixed_pins.items():
    actual = pin(BASE / relative)
    assert (actual['bytes'], actual['SHA256']) == expected
expected_controls = {
    'FINAL.json': (1972, '0c6838af4b2acf9065b89587f8701b692be78caf974b67e6e5dbb06899a713aa'),
    'FINAL_MANIFEST.json': (4483, 'e31cdbc3460f63e135e075fbb21bff87e72ae5cbbedb71ce222b822f29645584'),
    'private-page/index.html': (16374, 'da860b3ff65e8925159147f53200e5878d416dba24fbe133e8066f9b2f75604b'),
    'MODEL.json': (6831, '175c9bc64420141f5853207bb136a17507ce00920bbc6fa5f696389b0d178a87')}
for name, expected in expected_controls.items():
    assert (writer['files'][name]['bytes'], writer['files'][name]['SHA256']) == expected

sm = load(SOURCE / 'SOURCE_MANIFEST.json')
sf = load(SOURCE / 'SOURCE_FINAL.json')
assert sm['schema'] == 'opaque-native-source-manifest-v1'
assert sm['root'] == str(SOURCE) and sm['ordinary_files_including_controls'] == 97
assert sm['child_directory_count'] == 7
assert sm['root_controls_excluded_from_own_list'] == ['SOURCE_MANIFEST.json', 'SOURCE_FINAL.json']
assert sm['no_subtree_wildcard_runtime_or_future_exclusions'] is True
assert sm['all_regular_no_symlinks'] is True
assert len({row['path'] for row in sm['files']}) == len(sm['files']) == 95
assert {row['path'] for row in sm['files']} == set(source['files']) - {'SOURCE_MANIFEST.json', 'SOURCE_FINAL.json'}
for row in sm['files']:
    assert set(row) == {'path', 'bytes', 'SHA256', 'mode'}
    check_pin(source['files'][row['path']], {k: v for k, v in row.items() if k != 'path'})
assert {row['path']: row['mode'] for row in sm['directories']} == source['directories']
assert len(sm['directories']) == 7
for field in ('SOURCE_READY', 'SOURCE_MANIFEST'):
    row = sf[field]
    check_pin(source['files'][row['path']], {k: v for k, v in row.items() if k != 'path'})
assert source['files']['SOURCE_FINAL.json']['SHA256'] == '14cbf430570b90574e7c28bba911e7fe2b868c164107591b1783694c30212f80'
assert source['files']['SOURCE_MANIFEST.json']['SHA256'] == '7f2ec5e3f4d6fa358bc9dcc5af3ef5adb4ec3e3b2b8851ff831f8b4574dcd2ed'

wm = load(WRITER / 'FINAL_MANIFEST.json')
wf = load(WRITER / 'FINAL.json')
terminal = ['FINAL_MANIFEST.json', 'FINAL.json']
assert wm['root'] == str(WRITER) and wm['root_mode'] == writer['root_mode']
assert wm['file_count'] == wf['file_count'] == 19
assert wm['child_directory_count'] == wf['child_directory_count'] == 1
assert wm['directories'] == writer['directories']
assert wm['hidden_paths'] == writer['hidden_paths']
assert wm['empty_files'] == writer['empty_files']
assert wm['empty_directories'] == writer['empty_directories']
assert set(wm['payload_files']) == set(writer['files']) - set(terminal)
for name, row in wm['payload_files'].items():
    assert set(row) == {'bytes', 'SHA256', 'MD5', 'mode'}
    check_pin(writer['files'][name], row)
assert [row['path'] for row in wm['terminal_pair']] == terminal
assert wf['only_terminal_recursive_hash_exclusions'] == terminal
for row in wm['terminal_pair']:
    assert set(row) == {'path', 'bytes', 'mode', 'recursive_hash_excluded'}
    assert row['recursive_hash_excluded'] is True
    assert all(writer['files'][row['path']][key] == row[key] for key in ('bytes', 'mode'))
check_pin(writer['files']['FINAL_MANIFEST.json'], wf['manifest'])
assert wf['own_bytes'] == writer['files']['FINAL.json']['bytes'] and wf['own_mode'] == writer['files']['FINAL.json']['mode']
for field, name in [('page', 'private-page/index.html'), ('model', 'MODEL.json'), ('report', 'EDITORIAL_REPORT.md'), ('static_checks', 'STATIC_CHECKS.json')]:
    check_pin(writer['files'][name], wf[field])
assert wf['publication_authority'] is False and wf['stop'] is True

before = load(WRITER / 'CUSTODY_BEFORE.json')
after = load(WRITER / 'CUSTODY_AFTER.json')
assert before['phase'] == 'before' and after['phase'] == 'after'
assert before['source'] == after['source'] == source
assert before['fixed_inputs'] == after['fixed_inputs']
for relative in (ROOT_REVIEW, CLEARANCE):
    check_pin(pin(BASE / relative), before['fixed_inputs'][relative])
css_key = 'verification/d4-canonical-potential-editorial-v2-sol-20261117/private-page/research.css'
assert set(before['fixed_inputs']) == {ROOT_REVIEW, CLEARANCE, css_key}
assert before['fixed_inputs'][css_key] == writer['files']['private-page/research.css']
assert all(read(WRITER / name) == b'' for name in ('CUSTODY_BEFORE.stderr.txt', 'CUSTODY_AFTER.stderr.txt'))
static_checks = load(WRITER / 'STATIC_CHECKS.json')
assert json.loads(read(WRITER / 'CUSTODY_AFTER.stdout.txt')) == static_checks
assert static_checks['status'] == 'STATIC_COPY_AND_CUSTODY_CHECKS_PASSED'
assert len(read(WRITER / 'verify_private.py').splitlines()) == 103

model = load(WRITER / 'MODEL.json')
record = load(SOURCE / 'record.response.body')
metadata = record['metadata']
tex = read(SOURCE / 'published-source/container-001/tree/manuscript.tex').decode()
assert len(tex.splitlines()) == 482
assert hashlib.sha256(tex.encode()).hexdigest() == '3338be58c5c6250a826f2a2af772db5a3838dad1d45c6c4a847c62cc00b4f9df'
raw_abstract = tex.split(r'\begin{abstract}', 1)[1].split(r'\end{abstract}', 1)[0]
normalize = lambda text: ' '.join(text.split())
assert normalize(raw_abstract) == model['abstract']['source_TeX']
replacements = [
    {'from': r'$K=\Q(\sqrt5)$', 'to': 'K=Q(√5)'},
    {'from': r'$K(\sqrt{5+2\sqrt5},\zeta_5,\sqrt[5]{\lambda+\phi^5})$', 'to': 'K(√(5+2√5), ζ₅, ⁵√(λ+φ⁵))'},
    {'from': r'$\phi=(1+\sqrt5)/2$', 'to': 'φ=(1+√5)/2'}]
assert model['abstract']['literal_rendering_replacements'] == replacements
abstract = raw_abstract
for row in replacements:
    assert abstract.count(row['from']) == 1
    abstract = abstract.replace(row['from'], row['to'])
abstract = normalize(abstract)
assert abstract == model['abstract']['normalized_full_text']
assert '$' not in abstract and '\\' not in abstract
assert hashlib.sha256(abstract.encode()).hexdigest() == static_checks['abstract_normalized_SHA256']


class PageReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.ids, self.references, self.links, self.iframes = {}, [], [], [], []
        self.scripts, self.abstract, self.visible = [], [], []
        self.in_script = self.in_abstract = False
        self.headings, self.canonical, self.bases = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        self.references.extend(a.get('aria-labelledby', '').split())
        if tag == 'meta':
            key = a.get('name', a.get('property'))
            if key is not None:
                assert key not in self.meta
                self.meta[key] = a.get('content', '')
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.headings.append(tag)
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a)
        if tag == 'base':
            self.bases.append(a)
        if tag == 'iframe':
            self.iframes.append(a)
        if tag == 'script':
            assert a.get('type') == 'application/ld+json' and 'src' not in a
            self.scripts.append('')
            self.in_script = True
        if tag == 'p' and a.get('id') == 'manuscript-abstract':
            self.in_abstract = True
        for key in ('href', 'src'):
            if key in a:
                self.links.append((tag, key, a[key], a))

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False
        if tag == 'p':
            self.in_abstract = False

    def handle_data(self, value):
        if self.in_script:
            self.scripts[-1] += value
        else:
            self.visible.append(value)
        if self.in_abstract:
            self.abstract.append(value)


html = read(PAGE / 'index.html').decode()
parser = PageReader()
parser.feed(html)
parser.close()
assert len(parser.ids) == len(set(parser.ids))
assert all(reference in parser.ids for reference in parser.references)
assert parser.headings == ['h1'] + ['h2'] * 8
assert len(parser.scripts) == 1
scholar = json.loads(parser.scripts[0])
assert scholar['@type'] == 'ScholarlyArticle' and '@graph' not in scholar
assert abstract == ''.join(parser.abstract) == parser.meta['DC.description'] == parser.meta['citation_abstract'] == scholar['abstract']
assert parser.meta['robots'] == 'noindex,nofollow' and not parser.canonical and not parser.bases
assert len(parser.iframes) == 1 and parser.iframes[0]['src'] == 'pentagonal-torsion-note.pdf'
assert parser.iframes[0]['title'] and parser.iframes[0]['loading'] == 'lazy'
relative_targets, fragments, site_navigation = set(), set(), set()
for tag, key, target, attrs in parser.links:
    u = urlsplit(target)
    if not u.scheme and not u.netloc:
        if target.startswith('/'):
            site_navigation.add(target)
        elif u.path:
            assert not u.query and (PAGE / u.path).is_file()
            relative_targets.add(u.path)
        if u.fragment:
            assert not u.path and u.fragment in parser.ids
            fragments.add(u.fragment)
    if tag == 'a' and 'download' in attrs and attrs['download']:
        assert attrs['download'] == target
assert relative_targets == {'research.css', 'citation.bib', 'pentagonal-torsion-note.pdf', 'pentagonal-torsion-verification.zip'}
assert fragments == {'main'} and site_navigation == {'/', '/research/'}

assets = model['native_assets_in_original_order']
names = ['pentagonal-torsion-note.pdf', 'pentagonal-torsion-verification.zip']
assert [row['native_filename'] for row in assets] == [row['key'] for row in record['files']] == names
assert [row['name'] for row in scholar['encoding']] == names
assert wf['native_file_order'] == names
ordered_list = re.search(r'<ol>\s*(.*?)</ol>', html, re.S).group(1)
assert re.findall(r'href="([^"]+)" download=', ordered_list) == names
for index, (row, native, encoding) in enumerate(zip(assets, record['files'], scholar['encoding']), 1):
    local = pin(PAGE / row['local_filename'])
    assert row['native_order'] == index and row['local_filename'] == row['native_filename']
    assert local == pin(SOURCE / 'assets' / row['native_filename'])
    check_pin(local, {key: row[key] for key in ('bytes', 'SHA256', 'MD5')})
    assert local['bytes'] == native['size'] and 'md5:' + local['MD5'] == native['checksum']
    assert row['native_url'] == native['links']['self'] == encoding['contentUrl']
    assert encoding['contentSize'] == str(local['bytes']) + ' bytes'
    assert encoding['encodingFormat'] == row['encoding_format']
assert writer['files']['private-page/research.css']['bytes'] == 1170
assert writer['files']['private-page/research.css']['SHA256'] == 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'
assert set(writer['files']) & {f'private-page/{name}' for name in names} == {f'private-page/{name}' for name in names}
assert {name for name in writer['files'] if name.startswith('private-page/')} == {'private-page/index.html', 'private-page/citation.bib', 'private-page/research.css', *('private-page/' + n for n in names)}

assert model['title'] == metadata['title'] == parser.meta['citation_title'] == scholar['name']
assert model['DOI'] == metadata['doi'] == parser.meta['citation_doi'] == scholar['identifier']['value']
assert model['author'] == parser.meta['citation_author'] == scholar['author']['name'] == 'Alec Kriebel'
assert model['ORCID'] == parser.meta['citation_author_orcid'] == scholar['author']['sameAs'] == 'https://orcid.org/0009-0001-9320-500X'
assert model['native_version'] == metadata['version'] == parser.meta['citation_version'] == scholar['version'] == '1.0'
assert model['printed_numeric_version'] is False and model['same_current_bytes_at_creation_claim'] is False
assert model['native_publication_date'] == metadata['publication_date'] == scholar['datePublished'] == '2026-10-04'
assert parser.meta['citation_publication_date'] == parser.meta['citation_date'] == '2026/10/04'
assert model['record_created'] == record['created']
assert model['record_and_files_updated'] == record['updated'] == record['modified']
assert parser.meta['citation_pdf_url'] == assets[0]['native_url']
assert model['private_only'] is True and model['publication_authority'] is False
for field in ('actual_canonical', 'base_url', 'production_url', 'page_publication_date', 'AA', 'legacy_redirect', 'follow_up'):
    assert model[field] is None
for field in ('canonical', 'base_url', 'production_url', 'page_publication_date', 'AA', 'legacy_redirect', 'follow_up'):
    assert wf[field] is None
assert metadata['license']['id'] == 'cc-by-4.0'
assert scholar['license'] == 'https://creativecommons.org/licenses/by/4.0/'
assert model['rights']['original_note_and_authored_verification_material'] == 'CC-BY-4.0'
assert model['rights']['MIT_split'] is False
license_text = read(SOURCE / 'published-source/container-001/tree/LICENSE.txt').decode()
assert 'Original research note and author-produced verification materials' in license_text
assert 'Creative Commons Attribution4.0 International' in license_text
visible = normalize(' '.join(parser.visible))
for excluded in ('2026-11-17', 'Verdureprinted', 'printed87', 'ROOT_REVIEW', '145/203', '1364', '306424', 'formal certificate granted'):
    assert excluded not in visible
bib = read(PAGE / 'citation.bib').decode()
for literal in ('author = {Kriebel, Alec}', 'version = {1.0}', 'doi = {10.5281/zenodo.23137834}', 'Unrefereed preprint, 4 October 2026; version supplied by native record metadata'):
    assert literal in bib

end_entries = fixed_guard()
assert end_entries == baseline['entries']
save('AFTER.json', {'UTC': now(), 'guard_roots': baseline['guard_roots'],
                    'guard_fixed_files': baseline['guard_fixed_files'], 'entries': end_entries})
receipt = {'schema': 'pentagon-private-editorial-fact-passive-checks-v1', 'UTC': now(),
           'status': 'PASS_STATIC_FACT_DATA_AND_FROZEN_CUSTODY', 'execution_count': 1,
           'scientific_executions': 0, 'old_helper_executions': 0, 'protected_writes': 0,
           'source_files_child_directories': [97, 7], 'writer_files_child_directories': [19, 1],
           'complete_fixed_before_after_equal': True,
           'literal_three_replacements_and_whitespace_only': True,
           'full_visible_DC_citation_single_Scholar_abstract_equal': True,
           'abstract_SHA256': hashlib.sha256(abstract.encode()).hexdigest(),
           'native_order_names_bytes_modes_MD5_SHA256_equal': True,
           'writer_and_source_manifests_all_payload_fields_checked': True,
           'terminal_exclusions_only_exact_named_pairs_externally_pinned': True,
           'general_null_hash_acceptance': False,
           'all_relative_targets_fragment_and_aria_references_present': True,
           'site_navigation_only_static_unvalidated': sorted(site_navigation),
           'private_noindex_null_production_fields': True,
           'browser_UI_live_collision_publication_or_scientific_certificate': False,
           'page': writer['files']['private-page/index.html'], 'model': writer['files']['MODEL.json']}
save('CHECKS.json', receipt)
print(json.dumps(receipt, ensure_ascii=False))
