"""Private data-only assembly; no source programs, native science, render or network."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import datetime
import hashlib
import json
import os
import re
import stat

R = Path(__file__).resolve().parent
P = R.parents[1]
S = P / 'papers/23527793/sources'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
TEX = S / 'published-source/container-001/tree/congestion-fragmentation-verification/paper/main.tex'
LICENSE = TEX.parents[1] / 'LICENSE.txt'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def pin(path, relative=None):
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), 'not a regular file: ' + str(path))
    data = path.read_bytes()
    return {'path': path.relative_to(relative).as_posix() if relative else str(path),
            'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(),
            'mode': oct(stat.S_IMODE(st.st_mode))}

def inventory(root):
    files, directories = [], []
    for path in sorted(root.rglob('*')):
        mode = path.lstat().st_mode
        if stat.S_ISREG(mode):
            files.append(pin(path, root))
        elif stat.S_ISDIR(mode):
            directories.append({'path': path.relative_to(root).as_posix(),
                                'mode': oct(stat.S_IMODE(mode))})
        else:
            raise RuntimeError('unexpected topology: ' + str(path))
    return files, directories

def normalized(entry):
    return dict(entry, mode=oct(entry['mode']) if isinstance(entry['mode'], int) else entry['mode'])

def create(name, value):
    with (R / name).open('xb') as stream:
        stream.write(value.encode('utf-8') if isinstance(value, str) else value)

def create_json(name, value):
    create(name, json.dumps(value, ensure_ascii=False, indent=2) + '\n')

clearance = P / 'verification/root-clearance-23527793-20261117.json'
review = P / 'papers/23527793/reviews/root/ROOT_REVIEW.md'
require(pin(clearance)['bytes'] == 2092 and pin(clearance)['SHA256'] == '6fde779a24c6270f69429828a804784bb9f996c11683df47d7bd117ce0bb42c3', 'clearance differs')
require(pin(review)['bytes'] == 14961 and pin(review)['SHA256'] == '3effd8e3f8681e7cfc075f60d2ccd502e87a76116e50b310a1e2acb6bd2cb0a3', 'root report differs')
c = json.loads(clearance.read_text())
require(c['status'] == 'PASS_FULL_ORIGINAL_PRIVATE_EDITORIAL_PREPARATION_ALLOWED' and c['W_install_Git_push_deploy_Sheet_AA_redirect_authority'] is False and c['follow_up'] is None, 'clearance scope differs')
sf, sd = inventory(S)
sm = json.loads((S / 'SOURCE_MANIFEST.json').read_text())
require(pin(S / 'SOURCE_MANIFEST.json')['SHA256'] == '5a28bd01fb98dd9d08f746fc4bef54bb19744a1c190db03c0ffb795630ee6d84', 'source manifest differs')
source_payload = [q for q in sf if q['path'] not in sm['exact_terminal_exclusions']]
require(source_payload == [normalized(q) for q in sm['files']] and sd == [normalized(q) for q in sm['directories']], 'source payload identity or topology differs')
require(len(sf) == 162 and len(sd) == 23 and oct(stat.S_IMODE(S.lstat().st_mode)) == oct(sm['root_mode']), 'source extent differs')
record = json.loads((S / 'record.response.body').read_text())
native_files = json.loads((S / 'files-23527793.response.body').read_text())
n = record['metadata']
m = json.loads((R / 'page-model.json').read_text())
for key in ('title', 'doi', 'publication_date'):
    require(m[key] == n[key], 'native model identity differs: ' + key)
require(m['native_version'] == m['printed_version'] == n['version'] == '1.0', 'version differs')
require(m['record_created'] == record['created'] and m['record_updated'] == record['updated'], 'native record dates differ')
require(m['author']['ORCID'].endswith(n['creators'][0]['orcid']) and n['license']['id'] == 'cc-by-4.0', 'author or rights differ')
require(' '.join(LICENSE.read_text().split()) == m['rights']['actual_LICENSE_txt'], 'actual LICENSE differs')
require(all(m[key] is None for key in ('canonical_url', 'base_url', 'production_url', 'actual_publication_date', 'AA', 'follow_up')) and m['publication_authority'] is False, 'private model gate differs')
tex = TEX.read_text()
abstract = re.search(r'\\begin\{abstract\}\s*(.*?)\s*\\end\{abstract\}', tex, re.S).group(1)
abstract = ' '.join(abstract.replace(r'\(k^2\)', 'k²').replace(r'\(16\sqrt{\log k/k}\)', '16√(log k/k)').split())
require(abstract == m['abstract'], 'complete manuscript abstract differs')
require(r'\date{21 October 2026\quad (version 1.0; unrefereed preprint)}' in tex, 'printed date/version/status differs')
require([q['name'] for q in m['native_asset_order']] == [q['key'] for q in record['files']] == [q['key'] for q in native_files['entries']], 'native returned asset order differs')
target = W / 'public/research' / m['deployment_proposal']['slug']
require(not os.path.lexists(target), 'proposed public slug already exists')
css = W / 'public/research/research.css'
reference_inputs = [css, W / 'public/research/free-spanning-forest-degree/index.html', W / 'public/research/low-exponent-supersolvability/index.html']
reference_pins = [pin(path) for path in reference_inputs]
for name in ('article.html', 'head.html', 'research.css', 'assets', 'SOURCE_GUARDS.json', 'STATIC_CHECK.json', 'REPORT.md', 'MANIFEST.json', 'FINAL.json'):
    require(not os.path.lexists(R / name), 'owned output already exists: ' + name)
(R / 'assets').mkdir()
copies = []
for entry, original in zip(m['native_asset_order'], record['files']):
    source = S / 'assets' / entry['name']
    data = source.read_bytes()
    require(len(data) == entry['bytes'] == original['size'], 'native asset size differs')
    require('md5:' + hashlib.md5(data).hexdigest() == entry['native_checksum'] == original['checksum'], 'native asset MD5 differs')
    require(hashlib.sha256(data).hexdigest() == entry['SHA256'], 'native asset SHA differs')
    require(oct(stat.S_IMODE(source.lstat().st_mode)) == entry['mode'], 'native mode differs')
    create(entry['local_path'], data)
    (R / entry['local_path']).chmod(stat.S_IMODE(source.lstat().st_mode))
    require(pin(source)['bytes'] == pin(R / entry['local_path'])['bytes'] and pin(source)['SHA256'] == pin(R / entry['local_path'])['SHA256'] and pin(source)['mode'] == pin(R / entry['local_path'])['mode'], 'private asset differs')
    copies.append({'source': pin(source, S), 'private_copy': pin(R / entry['local_path'], R), 'native_url': entry['native_url']})
create('research.css', css.read_bytes())
(R / 'research.css').chmod(stat.S_IMODE(css.lstat().st_mode))

def meta(key, value, prop=False):
    return '<meta ' + ('property' if prop else 'name') + '="' + escape(key, quote=True) + '" content="' + escape(value, quote=True) + '">'

sch = {
    '@context': 'https://schema.org', '@type': 'ScholarlyArticle', 'name': m['title'],
    'headline': m['title'], 'description': m['meta_description'], 'abstract': abstract,
    'author': {'@type': 'Person', 'name': m['author']['name'], 'identifier': m['author']['ORCID'],
               'affiliation': {'@type': 'Organization', 'name': m['author']['affiliation']}},
    'datePublished': m['publication_date'], 'dateCreated': m['record_created'], 'version': m['native_version'],
    'creativeWorkStatus': m['status'], 'inLanguage': 'en', 'isAccessibleForFree': True,
    'identifier': {'@type': 'PropertyValue', 'propertyID': 'DOI', 'value': m['doi']},
    'sameAs': m['doi_url'], 'license': 'https://creativecommons.org/licenses/by/4.0/',
    'keywords': n['keywords'],
    'encoding': [{'@type': 'MediaObject', 'name': q['name'], 'contentUrl': q['local_path'],
                  'encodingFormat': q['format'], 'contentSize': str(q['bytes']) + ' bytes',
                  'sameAs': q['native_url']} for q in m['native_asset_order']]
}
fields = [
    ('description', m['meta_description']), ('author', m['author']['name']),
    ('robots', m['robots']), ('googlebot', m['robots']),
    ('citation_title', m['title']), ('citation_author', 'Kriebel, Alec'),
    ('citation_author_orcid', '0009-0001-9320-500X'),
    ('citation_publication_date', m['publication_date'].replace('-', '/')),
    ('citation_date', m['publication_date'].replace('-', '/')), ('citation_version', m['native_version']),
    ('citation_doi', m['doi']), ('citation_language', 'en'), ('citation_pdf_url', m['native_asset_order'][1]['local_path']),
    ('DC.title', m['title']), ('DC.creator', m['author']['name']), ('DC.date', m['publication_date']),
    ('DC.description', abstract), ('DC.identifier', 'doi:' + m['doi']), ('DC.type', 'Text'), ('DC.language', 'en'),
    ('DC.rights', 'CC BY 4.0 for authored manuscript and supplement; third-party rights retained'),
    ('twitter:card', 'summary'), ('twitter:title', m['title']), ('twitter:description', m['meta_description'])
]
head = '<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>' + escape(m['seo_title']) + '</title>\n'
head += '\n'.join(meta(key, value) for key, value in fields) + '\n'
head += '\n'.join(meta(key, value, True) for key, value in [('og:type', 'article'), ('og:title', m['title']), ('og:description', m['meta_description']), ('og:site_name', 'Alec Kriebel'), ('article:published_time', m['publication_date'])]) + '\n'
head += '<link rel="stylesheet" href="research.css">\n<script type="application/ld+json">' + json.dumps(sch, ensure_ascii=False) + '</script>\n</head>\n'
create('head.html', head)
main = (R / 'public-main.html').read_text()
before = '<!doctype html>\n<html lang="en">\n' + head + '<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header><p class="site-title"><a href="https://aleckriebel.com/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="https://aleckriebel.com/">Home</a> · <a href="https://aleckriebel.com/research/">Research</a></nav></header>\n'
after = '<footer><p><a href="https://aleckriebel.com/research/">Research index</a> · <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></p></footer>\n</body>\n</html>\n'
create('article.html', before + main + after)

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []; self.links = []; self.meta = {}; self.abstract = []
        self.capture = None; self.iframe = []; self.canonical = []; self.bases = []; self.scripts = []
    def handle_starttag(self, tag, attrs):
        q = dict(attrs)
        if 'id' in q: self.ids.append(q['id'])
        if q.get('id') == 'abstract-text': self.capture = tag
        if tag == 'meta': self.meta[q.get('name', q.get('property'))] = q.get('content')
        if tag == 'iframe': self.iframe.append(q.get('src'))
        if tag == 'link' and q.get('rel') == 'canonical': self.canonical.append(q.get('href'))
        if tag == 'base': self.bases.append(q)
        if tag == 'script': self.scripts.append(q.get('type'))
        for key in ('href', 'src'):
            if key in q: self.links.append(q[key])
    def handle_endtag(self, tag):
        if tag == self.capture: self.capture = None
    def handle_data(self, data):
        if self.capture: self.abstract.append(data)

html = (R / 'article.html').read_text(); v = Inspect(); v.feed(html)
require(len(v.ids) == len(set(v.ids)), 'duplicate HTML ids')
require(' '.join(''.join(v.abstract).split()) == abstract == v.meta['DC.description'] == sch['abstract'], 'abstract differs among visible/DC/schema/model')
require(v.meta['citation_title'] == n['title'] and v.meta['citation_version'] == n['version'] and v.meta['citation_doi'] == n['doi'], 'scholarly citation identity differs')
require(v.meta['robots'] == v.meta['googlebot'] == 'noindex, nofollow' and not v.canonical and not v.bases and 'og:url' not in v.meta, 'private head gate differs')
require(not any(key in sch for key in ('url', '@id', 'mainEntityOfPage')), 'active production schema identity')
require(v.iframe == [m['native_asset_order'][1]['local_path'] + '#view=FitH'] and v.scripts == ['application/ld+json'], 'reader/script setup differs')
require(re.search(r'<main\b.*?</main>\n?', html, re.S).group(0) == main and re.search(r'<head>.*?</head>\n?', html, re.S).group(0) == head, 'whole MAIN/head assembly differs')
for link in v.links:
    u = urlsplit(link)
    if not u.scheme and not u.netloc:
        path = unquote(u.path)
        require(not path.startswith('/') and '..' not in Path(path).parts, 'unexpected local link: ' + link)
        if path: require((R / path).is_file(), 'missing local link: ' + link)
        elif u.fragment: require(u.fragment in v.ids, 'missing local fragment: ' + link)
require(v.links.index(m['native_asset_order'][0]['local_path']) < v.links.index(m['native_asset_order'][1]['local_path']), 'visible native order differs')
require(all(q['native_url'] in v.links for q in m['native_asset_order']), 'native original links absent')
for forbidden in ('ROOT_REVIEW', 'INITIAL_SEAL', 'NumPy', '534', '687', '3972', 'MIT', '32 retained controls', '52 literature searches', '16 primary source bodies'):
    require(forbidden not in main, 'unexpected public audit or rights text: ' + forbidden)
bib = (R / 'citation.bib').read_text()
require(all(value in bib for value in (n['title'], n['doi'], '{1.0}', '{2026-10-21}', '21 October 2026')), 'Bib identity differs')
require([pin(path) for path in reference_inputs] == reference_pins and pin(css)['SHA256'] == pin(R / 'research.css')['SHA256'], 'reference/CSS drift')
require(not os.path.lexists(target), 'proposed public slug appeared')
af, ad = inventory(S)
require(af == sf and ad == sd and oct(stat.S_IMODE(S.lstat().st_mode)) == oct(sm['root_mode']), 'source drift during data-only assembly')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
create_json('SOURCE_GUARDS.json', {
    'UTC': now, 'source_root': str(S), 'root_mode': oct(sm['root_mode']), 'files': sf, 'directories': sd,
    'source162files23dirs_unchanged_before_after': True, 'asset_copies': copies,
    'actual_clearance': pin(clearance, P), 'actual_root_report': pin(review, P),
    'complete_native_metadata': pin(S / 'record.response.body', P), 'native_files_returned_order': pin(S / 'files-23527793.response.body', P),
    'controlling_manuscript': pin(TEX, P), 'actual_license': pin(LICENSE, P),
    'reference_files_unchanged': reference_pins, 'private_css_copy': pin(R / 'research.css', R),
    'proposed_slug_absent_before_after': str(target)
})
create_json('STATIC_CHECK.json', {
    'UTC': now, 'status': 'PASS_PRIVATE_DATA_AND_COPY_CONSISTENCY_ONLY', 'ordinary_passes': 1,
    'full_native_manuscript_abstract_visible_DC_schema_model_equal': True, 'whole_MAIN_head_exact': True,
    'native_asset_order_filenames_bytes_checksums_modes_exact': True, 'native_metadata_dates_versions_rights_retained': True,
    'private_noindex_null_actual_canonical_base_production_publication_AA': True,
    'shared_white_Arial_CSS_exact': True, 'local_links_and_ids_valid': True,
    'source_files': len(sf), 'source_directories': len(sd),
    'no_native_scientific_archived_helper_build_network_Git_W_Sheet_deploy_execution': True,
    'scientific_clearance_inherited_not_new_independent_review': True,
    'full_numerical_replay_newly_reproduced_claimed': False, 'follow_up': None,
    'reader_limit': 'No current browser/article render, iframe display, live link/download or deployment certification'
})
create('REPORT.md', '# Private editorial handoff — row 185 / 23527793\n\nREADY for independent copy-fidelity review. Actual root clearance and complete ROOT_REVIEW, full native metadata/files, complete controlling manuscript/abstract and actual LICENSE.txt were read. Scientific clearance is inherited; this task is private editorial preparation, not a new scientific family.\n\nThe complete original manuscript abstract is present consistently in visible HTML, DC.description, ScholarlyArticle.abstract and the private model. The only rendering changes are whitespace and the two TeX math expressions to plain Unicode. The full all-time/every-optimizer joint event retains its explicit finite failure bound and binary-size/delta condition; fixed-time throughput and marginal/component limits, the critical-time exclusions and eventual coupling statement are included. Sparse tree/dense traffic, growing capacities, fixed topology, quenched Exp(1) rates, quadratic time variance and realized-slope normalization remain explicit. The sufficient width is not described as exact critical scaling.\n\nAldous, classical flow/concentration, transportation antecedents, HOT and nearest percolation models receive credit. The final 1993 Karp–Motwani–Nisan edition gap and unresolved historical priority remain explicit. No uniquely right model/global firstness claim or follow-up is added. Collaboration is passive and tied to actual contributions. Extensive AI involvement and unrefereed status are stated concisely. Public copy omits internal verification timelines, counts, dependency failures and logs; it does not claim a new successful full replay. The inherited record is that both family main replay attempts stopped at missing NumPy before components, while one distinct exact rational root control passed.\n\nOriginal version 1.0 / 21 October 2026 / ORCID and actual CC BY 4.0 authored-manuscript/supplement rights are preserved. Exact native originals are ZIP then PDF, with unchanged bytes, filenames and modes, local direct downloads and native links; the unchanged five-page PDF is embedded locally. No MIT split is invented. Complete native Description stays in its existing source object and is not substituted for the manuscript abstract.\n\nOne bounded, fully read own data-only assembly/static pass checked actual clearance pins, the full 162-file/23-directory source before/after, native originals/order/rights/date/version, whole head/MAIN assembly, scholarly abstract equality, local links/ids, private null/noindex gates and unchanged shared CSS/reference articles. No source/scientific/archived-helper/build program, network, Git, W mutation, Sheet, deploy, browser/display or outreach action occurred. Proposed canonical is confined to the model; actual publication, canonical/base/production URL and AA are null. Separate stage activation and live verification remain necessary. No current article desktop/mobile or iframe/PDF display certification is claimed.\n')
with (R / 'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n- ' + now + ' — 90% private editorial preparation. Own data-only assembly/static pass passed; actual clearance and whole source bytes/modes/topology unchanged, exact ZIP/PDF copies and all abstract/metadata/private gates checked. Assembled head/article now require whole-file reading before final freeze. No current browser/display or publication claim.\n')
