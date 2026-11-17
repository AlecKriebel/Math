"""Single owned data-only fact reader/seal. No source imports, subprocesses or network."""
import hashlib
import html
import json
import re
import stat
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/complex-retract-fact-sol-20261117'
WRITER = P / 'verification/complex-retract-editorial-sol-20261117'
SOURCE = P / 'papers/23203270/sources'
TEX = SOURCE / 'archives/01-source-and-verification.zip.extracted/main.tex'
PDF_TEXT = P / 'papers/23203270/reviews/root/original-pdf.txt'
CLEARANCE = P / 'verification/root-clearance-23203270-20261117.json'
ROOT_REVIEW = P / 'papers/23203270/reviews/root-continuation-20261117/ROOT_REVIEW.md'
PINS = {
    WRITER / 'FINAL.json': '37e5c1e3417fa8b572ac04a0084cc055ec9dce65404146c0841606892e4683f4',
    WRITER / 'MANIFEST.json': 'fd18a77e709ea1dfa14265987810358181fda72db696ac1df60198ff98e31726',
    SOURCE / 'SOURCE_FINAL.json': '2fec24204f44586d98bd88fbe26a1519e7b55b4abe221275475b1cbf2a7bc62e',
    SOURCE / 'SOURCE_MANIFEST.json': '4d41d1b02c1f436a7a0fd8f6249515aa69eced4658527a1c56f3fec20c86a704',
    CLEARANCE: '7b7096d4fcdf0260f849140e95a97c26e5a1fac8e999bd4d86bbe0b505a93774',
    ROOT_REVIEW: '3a8c154c15491194fc85df87faabe47a4ed65e2d644f4c02b6cf27749a093300',
}

def need(ok, label):
    if not ok:
        raise ValueError(label)

def readj(path):
    return json.loads(path.read_text(encoding='utf-8'))

def record(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Not regular: ' + str(path))
    body = path.read_bytes()
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(),
            'MD5': hashlib.md5(body).hexdigest(), 'mode': oct(stat.S_IMODE(info.st_mode))}

def inventory(root):
    files, dirs = {}, {}
    for path in sorted(root.rglob('*')):
        info, name = path.lstat(), path.relative_to(root).as_posix()
        if stat.S_ISDIR(info.st_mode):
            dirs[name] = {'mode': oct(stat.S_IMODE(info.st_mode)), 'empty': not any(path.iterdir())}
        else:
            files[name] = record(path)
    return {'root': str(root), 'root_mode': oct(stat.S_IMODE(root.lstat().st_mode)),
            'root_empty': not any(root.iterdir()), 'files': files, 'directories': dirs}

def putj(name, value):
    with (OWN / name).open('x', encoding='utf-8') as handle:
        handle.write(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def unique(pattern, body):
    found = re.findall(pattern, body, re.S)
    need(len(found) == 1, 'Unique expression missing: ' + pattern)
    return found[0]

class Tags(HTMLParser):
    def __init__(self, body):
        super().__init__(convert_charrefs=True)
        self.tags, self.ids = [], []
        self.feed(body)
        self.close()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])

started = datetime.now(timezone.utc).isoformat()
need(Path(__file__).resolve() == OWN / 'DATA_READER.py', 'Unexpected reader location')
for path, digest in PINS.items():
    need(record(path)['SHA256'] == digest, 'Pin differs: ' + str(path))
writer_before, source_before = inventory(WRITER), inventory(SOURCE)
wm, sm = readj(WRITER / 'MANIFEST.json'), readj(SOURCE / 'SOURCE_MANIFEST.json')
expected_wfiles = {item['path']: {key: item[key] for key in ['bytes', 'SHA256', 'MD5', 'mode']}
                   for item in wm['payload_files']}
need({name: value for name, value in writer_before['files'].items()
      if name not in {'MANIFEST.json', 'FINAL.json'}} == expected_wfiles, 'Writer payload differs')
need(writer_before['directories'] == {item['path']: {'mode': item['mode'], 'empty': item['empty']}
                                    for item in wm['directories']}, 'Writer dirs differ')
need(writer_before['root_mode'] == wm['root_mode'] == '0o755', 'Writer root mode')
need((len(writer_before['files']), len(writer_before['directories'])) == (22, 1), 'Writer extent')
expected_sfiles = {item['path']: {'bytes': item['bytes'], 'SHA256': item['sha256'],
                   'MD5': item['md5'], 'mode': item['mode_octal']}
                   for item in sm['entries'] if item['kind'] == 'file'}
expected_sdirs = {item['path']: {'mode': item['mode_octal'], 'empty': item['empty']}
                  for item in sm['entries'] if item['kind'] == 'directory'}
need({name: value for name, value in source_before['files'].items()
      if name not in {'SOURCE_MANIFEST.json', 'SOURCE_FINAL.json'}} == expected_sfiles,
     'Source payload differs')
need(source_before['directories'] == {name: value for name, value in expected_sdirs.items() if name != '.'},
     'Source directories differ')
need({'mode': source_before['root_mode'], 'empty': source_before['root_empty']} == expected_sdirs['.'],
     'Source root differs')
need((len(source_before['files']), len(source_before['directories'])) == (97, 12), 'Source extent')
before = {'writer': writer_before, 'source': source_before,
          'pins': {str(path.relative_to(P)): record(path) for path in PINS}}
putj('GUARDS_BEFORE.json', before)
clearance = readj(CLEARANCE)
need(clearance['status'] == 'PASS_FULL_ORIGINAL_PRIVATE_EDITORIAL_PREPARATION_ALLOWED'
     and clearance['follow_up'] is None, 'Clearance scope')
native = readj(SOURCE / 'native-metadata/record-api.json')
metadata = native['metadata']
model = readj(WRITER / 'page-model.json')
article, head, main, bib = [(WRITER / name).read_text(encoding='utf-8') for name in
                          ['article.html', 'head.html', 'main.html', 'citation.bib']]
need([len((WRITER / name).read_bytes()) for name in
      ['article.html', 'head.html', 'main.html', 'page-model.json', 'citation.bib']]
     == [23202, 6419, 16287, 6615, 463], 'Surface sizes')
need(unique(r'(<head>.*?</head>\n)', article) == head, 'Whole saved head differs')
need(unique(r'(<main id="main">.*?</main>\n)', article) == main, 'Whole saved main differs')
tex = TEX.read_text(encoding='utf-8')
need(len(tex.splitlines()) == 362, 'Native physical TeX lines')
abstract = ' '.join(unique(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex).split())
need('\\' not in abstract and '$' not in abstract, 'Unexpected abstract TeX')
tags = Tags(article)
need(len(tags.ids) == len(set(tags.ids)), 'Duplicate HTML ID')
meta = {attrs.get('name', attrs.get('property')): attrs.get('content')
        for tag, attrs in tags.tags if tag == 'meta'}
schema = json.loads(unique(r'<script type="application/ld\+json">(.*?)</script>', head))
visible = html.unescape(unique(r'<p id="abstract-text">(.*?)</p>', main))
need(abstract == visible == model['abstract'] == schema['abstract'] == meta['DC.description']
     == (WRITER / 'ABSTRACT.txt').read_text().strip(), 'Complete abstract surfaces')
need('version' not in metadata and model['native_version'] is None
     and model['native_API_version_field_absent'] is True, 'Native absent-version scope')
need('version' not in schema and 'citation_version' not in meta
     and not re.search(r'(?m)^\s*version\s*=', bib), 'Invented author version')
need(model['native_HTML_display_version'] == 'v1'
     and b'Version v1</span>' in (SOURCE / 'native-metadata/record-page.html').read_bytes(), 'Host label')
need('Zenodo display edition' in main and 'Zenodo displays edition v1' in bib
     and 'no author version field in API metadata' in bib, 'Unqualified host edition')
need(metadata['publication_date'] == model['publication_date'] == schema['datePublished']
     == meta['DC.date'] == '2026-10-06', 'Original date')
need(native['created'] == model['record_created'] == schema['dateCreated'], 'Creation date')
need(native['updated'] == model['record_updated'] == schema['dateModified'], 'Update date')
need(metadata['title'] == model['title'] == schema['name'] == schema['headline']
     == meta['citation_title'] == meta['DC.title'], 'Title identity')
need(native['doi'] == model['doi'] == meta['citation_doi'] == '10.5281/zenodo.23203270', 'DOI')
need(meta['citation_author_orcid'] == '0009-0001-9320-500X', 'ORCID')
need(all(model[key] is None for key in
         ['canonical_url', 'base_url', 'production_url', 'actual_publication_date', 'AA', 'follow_up'])
     and model['publication_authority'] is False, 'Actual private fields')
need(meta['robots'] == meta['googlebot'] == 'noindex, nofollow', 'Private noindex')
need(not any(tag == 'link' and attrs.get('rel') == 'canonical' for tag, attrs in tags.tags)
     and 'url' not in schema and 'mainEntityOfPage' not in schema, 'Actual page canonical')
proposal = model['deployment_proposal']
need(proposal['slug'] == 'complex-polynomial-retract-five-variables'
     and proposal['path'] == '/research/complex-polynomial-retract-five-variables/'
     and proposal['proposed_canonical_url'] == 'https://aleckriebel.com' + proposal['path'], 'Proposal identity')
order = ['source-and-verification.zip', 'paper.pdf']
need([item['key'] for item in native['files']] == order
     == [item['name'] for item in model['native_asset_order']]
     == [item['name'] for item in schema['encoding']], 'Native two-asset order')
need(re.findall(r'<a href="(assets/[^\"]+)" download>',
                unique(r'<ol id="native-assets">(.*?)</ol>', main))
     == ['assets/' + name for name in order], 'Visible native order')
assets = []
for item, data, encoding in zip(native['files'], model['native_asset_order'], schema['encoding']):
    source, copy = SOURCE / 'zenodo-files' / item['key'], WRITER / 'assets' / item['key']
    value = record(source)
    need(source.read_bytes() == copy.read_bytes() and value == record(copy)
         == {key: data[key] for key in ['bytes', 'SHA256', 'MD5', 'mode']}, 'Copied asset identity')
    need(value['bytes'] == item['size'] and 'md5:' + value['MD5'] == item['checksum'] == data['native_checksum'],
         'Native asset size/checksum')
    need(encoding['contentUrl'] == data['local_path'] == 'assets/' + item['key']
         and encoding['contentSize'] == str(item['size']) + ' bytes'
         and encoding['encodingFormat'] == data['format']
         and encoding['sameAs'] == data['native_url'] == item['links']['self'], 'Encoding identity')
    assets.append({'name': item['key'], **value})
paths, aria = [], []
for tag, attrs in tags.tags:
    for key in ['href', 'src']:
        if key not in attrs:
            continue
        target = urlsplit(attrs[key])
        if target.scheme or target.netloc:
            continue
        if target.path.startswith('/'):
            need(target.path == '/research/research.css', 'Unexpected site-root path')
            paths.append({'target': attrs[key], 'scope': 'expected shared stylesheet; no W/live access'})
        elif target.path:
            path = WRITER / unquote(target.path)
            need(path.resolve().is_relative_to(WRITER.resolve()) and path.is_file(), 'Missing/escaping local file')
            need(not target.fragment or (target.path.endswith('.pdf') and target.fragment == 'view=FitH'),
                 'Unexpected local-file fragment')
            paths.append({'target': attrs[key], 'scope': 'existing local file'})
        elif target.fragment:
            need(target.fragment in tags.ids, 'Missing fragment')
            paths.append({'target': attrs[key], 'scope': 'existing HTML ID'})
    for key in ['aria-labelledby', 'aria-describedby', 'aria-controls']:
        for ident in attrs.get(key, '').split():
            need(ident in tags.ids, 'Missing ARIA reference')
            aria.append({'attribute': key, 'target': ident})
need([attrs['href'] for tag, attrs in tags.tags if tag == 'link' and attrs.get('rel') == 'stylesheet']
     == ['/research/research.css'], 'Shared stylesheet only')
need(not any(tag == 'style' or 'style' in attrs for tag, attrs in tags.tags), 'Added local styling')
need(all(attrs.get('type') == 'application/ld+json' for tag, attrs in tags.tags if tag == 'script'),
     'Unexpected executable page script')
for token in [metadata['title'], native['doi'], 'author = {Kriebel, Alec}', 'date = {2026-10-06}',
              'Unrefereed, AI-assisted preprint']:
    need(token in bib, 'Bib identity: ' + token)
need('Apache' in main and 'Apache 2.0' in meta['DC.rights'] and 'MIT' not in main + head + bib,
     'Rights exception/MIT substitution')
need(model['rights']['original_note_and_original_verification_package'] == 'CC BY 4.0'
     and 'Apache' in model['rights']['bundled_OpenAI_Lean_and_adapted_configuration_audit_harness'], 'Rights model')
need(len([page for page in PDF_TEXT.read_text().split('\f') if page.strip()]) == 6, 'Native PDF text pages')
after = {'writer': inventory(WRITER), 'source': inventory(SOURCE),
         'pins': {str(path.relative_to(P)): record(path) for path in PINS}}
need(after == before, 'Writer/source/control drift')
putj('GUARDS_AFTER.json', after)
finished = datetime.now(timezone.utc).isoformat()
putj('DATA_CHECKS.json', {'started_UTC': started, 'completed_UTC': finished,
      'status': 'PASS_BOUNDED_PRIVATE_EDITORIAL_DATA_CHECKS', 'writer_extent': [22, 1], 'source_extent': [97, 12],
      'full_namespace_pins_before_after_exact': True, 'whole_saved_head_main_exact': True,
      'full_abstract_visible_DC_schema_model_exact': True, 'two_native_assets_and_encodings': assets,
      'native_version': None, 'API_version_absent_host_label_qualified': True,
      'rights_CCBY4_Apache2_exception_no_MIT': True, 'static_paths': paths, 'ARIA_references': aria,
      'native_TeX_lines': 362, 'native_PDF_text_pages_read': 6, 'W_network_rendered_live_checks': False,
      'own_data_reader_invocations': 1, 'source_scientific_helper_import_AST_compile_test_runs': 0,
      'concrete_findings': [], 'follow_up': None})
with (OWN / 'RESEARCH_LOG.md').open('x', encoding='utf-8') as handle:
    handle.write('# Private fact-review log\n\n- ' + started
                 + ' — 80% complete: full manual editorial/native comparison complete; saved data-only reader fully read before its sole invocation. No concrete defect identified.\n- '
                 + finished + ' — 100% complete: full writer/source before-after guards, assets, abstract and static metadata/paths passed. No scientific/source/helper execution or outside action. Final finite freeze follows.\n')
for name in ['READER.stdout.txt', 'READER.stderr.txt']:
    need((OWN / name).read_bytes() == b'', 'Nonempty literal reader stream')
snapshot = inventory(OWN)
putj('MANIFEST.json', {'schema': 'finite-private-fact-review-manifest-v1', 'UTC': finished,
      'root': str(OWN), 'root_mode': snapshot['root_mode'], 'root_empty': snapshot['root_empty'],
      'payload_files': [{'path': name, **value} for name, value in snapshot['files'].items()],
      'directories': [{'path': name, **value} for name, value in snapshot['directories'].items()],
      'exact_terminal_exclusions': ['MANIFEST.json', 'FINAL.json'],
      'all_actual_hidden_ignored_empty_objects_and_modes_included': True})
putj('FINAL.json', {'schema': 'private-fact-review-final-v1', 'UTC': finished, 'record': 23203270, 'row': 188,
      'status': 'PASS_PRIVATE_EDITORIAL_FIDELITY_FROZEN', 'completion_percent': 100,
      'manifest': {'path': 'MANIFEST.json', **record(OWN / 'MANIFEST.json')},
      'writer_FINAL_pin': PINS[WRITER / 'FINAL.json'], 'writer_MANIFEST_pin': PINS[WRITER / 'MANIFEST.json'],
      'clearance_pin': PINS[CLEARANCE], 'root_review_pin': PINS[ROOT_REVIEW],
      'writer22files1dir_source97files12dirs_preserved': True, 'concrete_findings': [],
      'new_scientific_clearance_or_action_authority': False, 'follow_up': None,
      'own_saved_fully_read_data_reader_invocations': 1, 'literal_stdout_stderr_empty': True,
      'source_scientific_helper_import_AST_compile_test_execution': False,
      'W_Git_network_Sheet_deploy_AA_redirect_children_contact_outreach_or_writer_otherpacket_mutation': False,
      'extent': {'regular_files': len(snapshot['files']) + 2, 'child_directories': len(snapshot['directories'])},
      'quiescent_after_freeze': True})
