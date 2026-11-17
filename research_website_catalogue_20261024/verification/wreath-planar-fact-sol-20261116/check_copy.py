"""One row164 data/static comparison and finite closure; no reviewed code execution."""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
from urllib.parse import urlsplit, unquote
from datetime import datetime, timezone
import hashlib
import json
import re
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'verification/wreath-planar-fact-sol-20261116'
A = P / 'verification/wreath-planar-editorial-sol-20261116'
S = P / 'papers/23203143/sources'

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonordinary file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(),
            'mode': oct(stat.S_IMODE(info.st_mode))}

def inventory(root):
    files, dirs = {}, {}
    need(stat.S_ISDIR(root.lstat().st_mode), 'Nonordinary root')
    for path in sorted(root.rglob('*')):
        info = path.lstat()
        rel = path.relative_to(root).as_posix()
        if stat.S_ISREG(info.st_mode):
            files[rel] = pin(path)
        else:
            need(stat.S_ISDIR(info.st_mode), 'Symlink/special node')
            dirs[rel] = oct(stat.S_IMODE(info.st_mode))
    return files, dirs

def save(name, value):
    path = O / name
    need(not path.exists(), 'Refusing repeated comparison/closure: ' + name)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

need(pin(O / 'INITIAL_SEAL.json')['SHA256'] == '963f454b78c1705cd8a3d2c11fcfbdc3bb338b84eacfd08e0d80a60d847bb832', 'INITIAL seal changed')
need(pin(O / 'INITIAL_MANIFEST.sha256')['SHA256'] == '1588b7d07d3792a6cf9c1c5e55ba7770e4fea6d03014dd476b4d1fdae1169a0f', 'INITIAL manifest changed')
initial_rows = (O / 'INITIAL_MANIFEST.sha256').read_text().splitlines()
need(len(initial_rows) == 9, 'INITIAL payload extent changed')
for line in initial_rows:
    digest, name = line.split('  ', 1)
    need(pin(O / name)['SHA256'] == digest and pin(O / name)['mode'] == '0o644', 'INITIAL payload changed: ' + name)
for line in (O / 'INPUT_PINS.sha256').read_text().splitlines():
    digest, name = line.split('  ', 1)
    need(pin(Path(name))['SHA256'] == digest, 'Contract input changed: ' + name)
need(pin(A / 'FINAL.json')['SHA256'] == 'cdb1d0e19286e1ca5b8d9e54ae027238bf022018019e43588867c1a054814451', 'Writer FINAL differs')
need(pin(A / 'MANIFEST.json')['SHA256'] == '9aede975fa35a505c32be4872396ede73287e8744ae3a5f38f9a31c3a5ea6473', 'Writer MANIFEST differs')
wm = json.loads((A / 'MANIFEST.json').read_bytes())
expected_writer = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in wm['payload_files']}
need(len(expected_writer) == len(wm['payload_files']) == 21, 'Duplicate/unexpected writer payload')
expected_writer.update({x: pin(A / x) for x in ('FINAL.json', 'MANIFEST.json')})
af, ad = inventory(A)
need(af == expected_writer and len(af) == 23, 'Writer whole file bytes/modes/extent differ')
need(ad == {x['path']: x['mode'] for x in wm['directories']} == {'assets': '0o755', 'original-objects': '0o755'}, 'Writer directory topology/modes differ')
need(oct(stat.S_IMODE(A.stat().st_mode)) == wm['root_mode'] == '0o755', 'Writer root mode differs')
sf, sd = inventory(S)
baseline = {}
for line in (O / 'SOURCE_BASELINE.sha256').read_text().splitlines():
    digest, name = line.split('  ', 1)
    baseline[Path(name).relative_to(S).as_posix()] = digest
need({k: v['SHA256'] for k, v in sf.items()} == baseline and len(sf) == 121 and len(sd) == 20, 'Source baseline bytes/extent differ')
topology = {}
for line in (O / 'SOURCE_TOPOLOGY_MODES.txt').read_text().splitlines():
    mode, name = line.split(' ', 1)
    topology[name] = mode
current_topology = {str(x): format(x.lstat().st_mode, 'o') for x in [S, *S.rglob('*')]}
need(topology == current_topology and len(topology) == 142, 'Source mode/topology baseline differs')
sm = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
expected_source = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in sm['files']}
need(len(expected_source) == len(sm['files']) == 119, 'Source manifest extent differs')
expected_source.update({x: pin(S / x) for x in ('SOURCE_FINAL.json', 'SOURCE_MANIFEST.json')})
need(sf == expected_source and sd == {x['path']: x['mode'] for x in sm['directories']}, 'Source sealed custody differs')
need(oct(stat.S_IMODE(S.stat().st_mode)) == '0o755', 'Source root mode differs')
producer_guards = json.loads((A / 'SOURCE_GUARDS.json').read_bytes())
need(sf == {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in producer_guards['files']}, 'Producer source guard differs from independently observed bytes')
need(sd == {x['path']: x['mode'] for x in producer_guards['directories']}, 'Producer source guard directories differ')
record = json.loads((S / 'record.response.body').read_bytes())
native = record['metadata']
wrapper = json.loads((S / 'files-23203143.response.body').read_bytes())
model = json.loads((A / 'page-model.json').read_bytes())
need(model['title'] == native['title'] and model['native_version'] == model['printed_version'] == native['version'] == '1.0.0', 'Native title/version differs')
need(model['publication_date'] == native['publication_date'] == '2026-10-06', 'Publication date differs')
need(model['record_created'] == record['created'] and model['record_updated'] == record['updated'], 'Record date fields differ')
need(model['doi'] == native['doi'] == '10.5281/zenodo.23203143', 'DOI differs')
need(model['author']['ORCID'] == 'https://orcid.org/' + native['creators'][0]['orcid'], 'ORCID differs')
need(model['author']['affiliation'] == native['creators'][0]['affiliation'] == 'Independent researcher', 'Affiliation differs')
need(all(model[x] is None for x in ('canonical_url', 'base_url', 'production_url', 'AA', 'follow_up')) and model['publication_authority'] is False, 'Private authority differs')
need(model['robots'] == 'noindex, nofollow', 'Private indexing differs')
need(wrapper['order'] == [] and wrapper['default_preview'] is None, 'Native wrapper metadata differs')
native_names = [x['key'] for x in record['files']]
need(native_names == [x['key'] for x in wrapper['entries']] == [x['name'] for x in model['native_asset_order']] == ['preprint.pdf', 'wreath-planar-verification-v1.0.0-revised.zip'], 'Native order differs')
for source, item in zip(record['files'], model['native_asset_order']):
    data = (S / 'assets' / source['key']).read_bytes()
    need((A / item['local_path']).read_bytes() == data, 'Copied native asset differs')
    need(len(data) == source['size'] == item['bytes'] and 'md5:' + hashlib.md5(data).hexdigest() == source['checksum'] == item['native_checksum'], 'Native size/MD5 differs')
    need(item['native_url'] == source['links']['self'], 'Native content URL differs')
copy_pairs = [('record.response.body', 'record.json'), ('files-23203143.response.body', 'files.json'),
    ('published-source/container-001/tree/publication/metadata.json', 'authored-metadata.json'),
    ('published-source/container-001/tree/publication/support/LICENSES.md', 'LICENSES.md'),
    ('published-source/container-001/tree/publication/support/LICENSE_CODE.txt', 'LICENSE_CODE.txt')]
for source, dest in copy_pairs:
    need((S / source).read_bytes() == (A / 'original-objects' / dest).read_bytes(), 'Preserved original differs: ' + dest)
plain_abstract = (O / 'EXPECTED_ABSTRACT.txt').read_text().strip()
expected_abstract = plain_abstract
for before, after in [('C2 wr H', 'C₂ wr H'), ('Cohn-de Laat-Salmon', 'Cohn–de Laat–Salmon'), ('L2=2/sqrt(3)', 'L₂ = 2/√3'), ('P2=4/3', 'P₂ = 4/3')]:
    expected_abstract = expected_abstract.replace(before, after)
need(model['abstract'] == expected_abstract, 'Complete original abstract differs')

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []; self.labels = []; self.links = []; self.meta = {}; self.canonical = []; self.bases = []; self.iframes = []; self.scripts = []; self.styles = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if 'aria-labelledby' in a: self.labels += a['aria-labelledby'].split()
        if tag == 'meta' and ('name' in a or 'property' in a): self.meta[a.get('name', a.get('property'))] = a.get('content')
        if tag == 'base': self.bases.append(a)
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical.append(a)
        if tag == 'link' and a.get('rel') == 'stylesheet': self.styles.append(a.get('href'))
        if tag == 'iframe': self.iframes.append(a.get('src'))
        if tag == 'script': self.scripts.append(a.get('type'))
        for key in ('href', 'src'):
            if key in a: self.links.append(a[key])

html = (A / 'article.html').read_text()
main = (A / 'public-main.html').read_text()
head = (A / 'head.html').read_text()
need(re.search(r'<main\b.*?</main>\n?', html, re.S).group(0) == main and re.search(r'<head>.*?</head>\n?', html, re.S).group(0) == head, 'Whole head/MAIN bytes differ')
view = Inspect(); view.feed(html)
need(len(view.ids) == len(set(view.ids)) and set(view.labels) <= set(view.ids), 'ID/aria references differ')
visible_abstract = unescape(re.search(r'<p id="abstract-text">(.*?)</p>', main, re.S).group(1))
scholar = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', head, re.S).group(1))
need(visible_abstract == scholar['abstract'] == view.meta['DC.description'] == model['abstract'], 'Visible/schema/DC full abstract differs')
need(main.count('We derive two separately motivated consequences') == 1, 'Duplicate original abstract in MAIN')
need(view.meta['description'] == view.meta['og:description'] == view.meta['twitter:description'] == scholar['description'] == model['meta_description'], 'Short metadata descriptions differ')
need(view.meta['citation_title'] == native['title'] and view.meta['citation_version'] == native['version'] and view.meta['citation_doi'] == native['doi'], 'Citation identity differs')
need(view.meta['citation_publication_date'] == view.meta['citation_date'] == '2026/10/06' and scholar['datePublished'] == native['publication_date'], 'Citation/schema dates differ')
need(view.meta['robots'] == view.meta['googlebot'] == 'noindex, nofollow' and not view.canonical and not view.bases and 'og:url' not in view.meta, 'Private HTML identity differs')
need(not any(x in scholar for x in ('url', '@id', 'mainEntityOfPage')), 'Active schema production identity')
need(view.scripts == ['application/ld+json'] and view.iframes == ['assets/preprint.pdf'], 'PDF/script setup differs')
need(view.styles == ['research.css'] and pin(A / 'research.css')['SHA256'] == 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a', 'Static CSS differs')
need([x['name'] for x in scholar['encoding']] == native_names, 'Schema native order differs')
for item, encoding in zip(model['native_asset_order'], scholar['encoding']):
    need(encoding['contentUrl'] == item['local_path'] and encoding['sameAs'] == item['native_url'], 'Schema native identity differs')
need(view.links.index('assets/preprint.pdf') < view.links.index('assets/wreath-planar-verification-v1.0.0-revised.zip'), 'Visible native order differs')
for value in view.links:
    u = urlsplit(value)
    need(u.scheme in ('', 'http', 'https'), 'Unexpected active/contact scheme')
    if not u.scheme and not u.netloc:
        path = unquote(u.path)
        need(not path.startswith('/') and '..' not in Path(path).parts, 'Unconfined local destination')
        if path: need((A / path).is_file(), 'Missing local destination: ' + value)
        if u.fragment and not path: need(u.fragment in view.ids, 'Missing local fragment')
for item in model['substantive_upstream_inputs']:
    need(item['URL'] in view.links and item['source_tag'] in ('197', '090'), 'Substantive upstream input differs')
need(len(model['substantive_upstream_inputs']) == 2, 'Substantive inputs missing')
need('citation.bib' in view.links and 'download' in main and 'target="_blank"' in main, 'Open/download controls missing')
bib = (A / 'citation.bib').read_text()
need(all(x in bib for x in (native['title'], native['doi'], '1.0.0', '6 October 2026', 'Unrefereed preprint')), 'Bib identity differs')
need(not any(x in main for x in ('Original Zenodo description', 'ROOT_REVIEW', 'INITIAL_SEAL', '2,436', '102 residual', '51 finite nodes')), 'Duplicate/internal operational narrative')
need(all((O / x).read_bytes() == b'' for x in ('check.stdout.txt', 'check.stderr.txt')), 'Nonempty comparison stream before closure')
need((af, ad) == inventory(A) and (sf, sd) == inventory(S), 'Input changed during static pass')
utc = datetime.now(timezone.utc).isoformat()
save('CHECK_RECEIPT.json', {'schema': 'independent-private-copy-static-check-v1', 'UTC': utc,
    'row': 164, 'record': 23203143, 'status': 'PASS_PRIVATE_COPY_FACT_AND_STATIC_FIDELITY',
    'actual_data_static_passes': 1, 'actual_exit_on_completion': 0,
    'producer_files': [{'path': k, **v} for k, v in af.items()], 'producer_directories': ad,
    'source_files': 121, 'source_child_directories': 20,
    'source_all_bytes_modes_topology_equal_independent_INITIAL_baseline_and_sealed_manifest': True,
    'original_11_file_INITIAL_unchanged': True,
    'whole_visible_schema_DC_original_abstract_equal': True, 'head_and_MAIN_exact': True,
    'native_original_assets_order_size_MD5_SHA256_bytes_exact': True,
    'private_metadata_links_styles_Bib_identity_checked': True,
    'two_consequence_scope_credit_rights_and_status_manually_read_against_source_contract': True,
    'corrections': [], 'follow_up': None, 'new_scientific_native_producer_helper_execution': False,
    'render_browser_network_W_Git_Sheet_deploy_contact_actions': False,
    'live_reader_download_or_publication_certification': False, 'publication_authority': False})
files, dirs = inventory(O)
need(len(files) == 18 and dirs == {} and all(x['mode'] == '0o644' for x in files.values()), 'Unexpected own finite closure extent/modes')
need(oct(stat.S_IMODE(O.stat().st_mode)) == '0o755', 'Owned root mode differs')
save('OWNED_MANIFEST.json', {'schema': 'finite-copy-fact-manifest-v1', 'UTC': utc,
    'root': str(O), 'root_mode': '0o755', 'files': [{'path': k, **v} for k, v in files.items()],
    'directories': [], 'exact_terminal_exclusions': ['OWNED_MANIFEST.json', 'FINAL.json'],
    'ignored_and_empty_files_included': True, 'no_future_or_subtree_exclusions': True})
save('FINAL.json', {'schema': 'independent-private-copy-fact-final-v1', 'UTC': utc,
    'row': 164, 'record': 23203143, 'status': 'COMPLETE_FROZEN_QUIESCENT',
    'copy_fact_disposition': 'PASS', 'corrections': [], 'follow_up': None,
    'report': {'path': 'REPORT.md', **pin(O / 'REPORT.md')},
    'receipt': {'path': 'CHECK_RECEIPT.json', **pin(O / 'CHECK_RECEIPT.json')},
    'manifest': {'path': 'OWNED_MANIFEST.json', **pin(O / 'OWNED_MANIFEST.json')},
    'original_INITIAL_seal': {'path': 'INITIAL_SEAL.json', **pin(O / 'INITIAL_SEAL.json')},
    'payload_files': 18, 'actual_files': 20, 'child_directories': 0, 'completion_percent': 100,
    'new_scientific_review_or_native_execution': False, 'informed_prior_exposure_disclosed': True,
    'publication_authority': False, 'AA': None, 'postseal_owned_writes_executions_allowed': False})
