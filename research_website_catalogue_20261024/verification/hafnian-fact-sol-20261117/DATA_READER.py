"""One owned data-only fact review/seal; never imports or executes source/helper code."""
import hashlib
import html
import json
import os
import re
import stat
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/hafnian-fact-sol-20261117'
WRITER = P / 'verification/hafnian-editorial-sol-20261117'
SOURCE = P / 'papers/23205294/sources'
TEX = SOURCE / 'published-source/container-001/tree/main.tex'
PDF_TEXT = P / 'papers/23205294/reviews/scope-sol/published_pdf.txt'
CLEARANCE = P / 'verification/root-clearance-23205294-20261117.json'
ROOT_REVIEW = P / 'papers/23205294/reviews/root/ROOT_REVIEW.md'
PINS = {
    WRITER / 'FINAL.json': '7ee863a6f05e461641696eb1e89263e8082edd467a7f7ccd731ad6cd159da5d5',
    WRITER / 'MANIFEST.json': 'e9ead80b950f2406751a066d41f5514a0b6d31128052373ef4968daaa6fd0662',
    SOURCE / 'SOURCE_FINAL.json': '09da60cf7a73285d2eccac7186d563f8f1e898c5bcc0390761a8a416989064d7',
    SOURCE / 'SOURCE_MANIFEST.json': '340a82f34c9cb70a48e60c9bb7db4e1f8a0980e5ca037771c3fe7dc16c6677e7',
    CLEARANCE: '9926f66d5651c887b60e20ee689567459a21edc15f76b0b4ec390c69a624dbf7',
    ROOT_REVIEW: 'd41464f5a849fc70c5b21d52249c9924e06e091ef7339a1825736c7224f15114',
}

def readj(path):
    return json.loads(path.read_text(encoding='utf-8'))

def record(path):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError('Not a regular file: ' + str(path))
    body = path.read_bytes()
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(),
            'mode': oct(stat.S_IMODE(info.st_mode))}

def inventory(root):
    files, directories = {}, {}
    for path in sorted(root.rglob('*')):
        name, info = path.relative_to(root).as_posix(), path.lstat()
        if stat.S_ISDIR(info.st_mode):
            directories[name] = {'mode': oct(stat.S_IMODE(info.st_mode)),
                                 'empty': not any(path.iterdir())}
        else:
            files[name] = record(path)
    return {'root': str(root), 'root_mode': oct(stat.S_IMODE(root.lstat().st_mode)),
            'files': files, 'directories': directories}

def putj(name, value):
    with (OWN / name).open('x', encoding='utf-8') as handle:
        handle.write(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def mode(value):
    return oct(value) if isinstance(value, int) else value

def guard(root, manifest_name, file_key, excluded, count):
    snapshot, manifest = inventory(root), readj(root / manifest_name)
    expected = {entry['path']: {'bytes': entry['bytes'], 'SHA256': entry['SHA256'],
                              'mode': mode(entry['mode'])} for entry in manifest[file_key]}
    actual = {name: value for name, value in snapshot['files'].items() if name not in excluded}
    need(actual == expected and len(expected) == len(manifest[file_key]), str(root) + ': payload mismatch')
    dirs = {entry['path']: mode(entry['mode']) for entry in manifest['directories']}
    need({name: value['mode'] for name, value in snapshot['directories'].items()} == dirs,
         str(root) + ': directories mismatch')
    need(snapshot['root_mode'] == mode(manifest['root_mode']), str(root) + ': root mode mismatch')
    need((len(snapshot['files']), len(snapshot['directories'])) == count, str(root) + ': extent mismatch')
    return snapshot

def need(ok, label):
    if not ok:
        raise ValueError(label)

def unique(pattern, body):
    matches = re.findall(pattern, body, re.S)
    need(len(matches) == 1, 'Expected one match: ' + pattern)
    return matches[0]

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
    need(record(path)['SHA256'] == digest, 'Pin mismatch: ' + str(path))
before = {'writer': guard(WRITER, 'MANIFEST.json', 'payload_files',
                         {'MANIFEST.json', 'FINAL.json'}, (23, 1)),
          'source': guard(SOURCE, 'SOURCE_MANIFEST.json', 'files',
                         {'SOURCE_MANIFEST.json', 'SOURCE_FINAL.json'}, (56, 10)),
          'pins': {str(path.relative_to(P)): record(path) for path in PINS}}
putj('GUARDS_BEFORE.json', before)
clearance, native = readj(CLEARANCE), readj(SOURCE / 'record.response.body')
need(clearance['status'] == 'PASS_FULL_ORIGINAL_PRIVATE_EDITORIAL_PREPARATION_ALLOWED', 'Clearance status')
need(clearance['follow_up'] is None, 'Clearance followup')
tex = TEX.read_text(encoding='utf-8')
need(len(tex.splitlines()) == 165, 'Native TeX physical line count')
abstract = unique(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex)
abstract = abstract.replace('$W$', 'W').replace('$(W,1,0,0)$', '(W,1,0,0)')
abstract = abstract.replace('$4\\bits(W)-2$', '4 bits(W)−2')
need('$' not in abstract and '\\' not in abstract, 'Unexpected abstract math rendering')
abstract = ' '.join(abstract.split())
article = (WRITER / 'article.html').read_text(encoding='utf-8')
head = (WRITER / 'head.html').read_text(encoding='utf-8')
main = (WRITER / 'main.html').read_text(encoding='utf-8')
model = readj(WRITER / 'page-model.json')
bib = (WRITER / 'citation.bib').read_text(encoding='utf-8')
need(unique(r'(<head>.*?</head>\n)', article) == head, 'Saved head differs')
need(unique(r'(<main id="main">.*?</main>\n)', article) == main, 'Saved main differs')
need([len((WRITER / name).read_bytes()) for name in
      ['article.html', 'head.html', 'main.html', 'page-model.json', 'citation.bib']]
     == [23740, 6857, 16387, 7760, 470], 'Writer principal surface sizes')
tags, head_tags = Tags(article), Tags(head)
need(len(tags.ids) == len(set(tags.ids)), 'Duplicate HTML ID')
meta = {attrs.get('name', attrs.get('property')): attrs.get('content')
        for tag, attrs in tags.tags if tag == 'meta'}
schema = json.loads(unique(r'<script type="application/ld\+json">(.*?)</script>', head))
visible = html.unescape(unique(r'<p id="abstract-text">(.*?)</p>', main))
need(abstract == visible == model['abstract'] == schema['abstract'] == meta['DC.description']
     == (WRITER / 'ABSTRACT.txt').read_text().strip(), 'Full abstract surfaces differ')
metadata = native['metadata']
need(metadata['version'] == model['native_version'] == schema['version'] == meta['citation_version']
     == '1.0.0', 'Native version fidelity')
need(metadata['publication_date'] == model['publication_date'] == schema['datePublished']
     == meta['DC.date'] == '2026-10-06', 'Original date fidelity')
need(native['created'] == model['record_created'] == schema['dateCreated'], 'Creation date')
need(native['updated'] == model['record_updated'] == schema['dateModified'], 'Update date')
need(metadata['title'] == model['title'] == schema['name'] == schema['headline']
     == meta['citation_title'] == meta['DC.title'], 'Full title fidelity')
need(meta['citation_doi'] == model['doi'] == native['doi'] == '10.5281/zenodo.23205294', 'DOI')
need(meta['citation_author_orcid'] == '0009-0001-9320-500X', 'ORCID')
need(all(model[key] is None for key in
         ['canonical_url', 'base_url', 'production_url', 'actual_publication_date', 'AA', 'follow_up']),
     'Actual publication gates')
need(model['publication_authority'] is False, 'Publication authority')
need(meta['robots'] == meta['googlebot'] == 'noindex, nofollow', 'Private indexing')
need(not any(tag == 'link' and attrs.get('rel') == 'canonical' for tag, attrs in tags.tags)
     and 'url' not in schema and 'mainEntityOfPage' not in schema, 'Actual canonical supplied')
proposal = model['deployment_proposal']
need(proposal['slug'] == 'nonnegative-rational-hafnians'
     and proposal['path'] == '/research/nonnegative-rational-hafnians/'
     and proposal['proposed_canonical_url'] == 'https://aleckriebel.com' + proposal['path'],
     'Proposed canonical/slug mismatch')
order = ['source-and-verification.zip', 'README.md', 'paper.pdf']
need([item['key'] for item in native['files']] == order, 'Native asset order')
need([item['name'] for item in model['native_asset_order']] == order
     == [item['name'] for item in schema['encoding']], 'Three encoding order')
need(re.findall(r'<a href="(assets/[^\"]+)" download>',
                unique(r'<ol id="native-assets">(.*?)</ol>', main))
     == ['assets/' + name for name in order], 'Visible original asset order')
assets = []
for item, data, encoding in zip(native['files'], model['native_asset_order'], schema['encoding']):
    source, copy = SOURCE / 'assets' / item['key'], WRITER / 'assets' / item['key']
    need(source.read_bytes() == copy.read_bytes(), 'Original asset bytes: ' + item['key'])
    identity = record(source)
    need(identity == record(copy) == {key: data[key] for key in ['bytes', 'SHA256', 'mode']},
         'Original asset identity: ' + item['key'])
    need(identity['bytes'] == item['size']
         and 'md5:' + hashlib.md5(source.read_bytes()).hexdigest() == item['checksum'] == data['native_checksum'],
         'Original native MD5/size: ' + item['key'])
    need(encoding['contentUrl'] == data['local_path'] == 'assets/' + item['key']
         and encoding['contentSize'] == str(item['size']) + ' bytes'
         and encoding['encodingFormat'] == data['format']
         and encoding['sameAs'] == data['native_url'] == item['links']['self'], 'Encoding identity')
    assets.append({'name': item['key'], **identity})
paths, labels = [], []
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
                 'Unexpected file fragment')
            paths.append({'target': attrs[key], 'scope': 'local file exists'})
        elif target.fragment:
            need(target.fragment in tags.ids, 'Missing fragment')
            paths.append({'target': attrs[key], 'scope': 'fragment exists'})
    for key in ['aria-labelledby', 'aria-describedby', 'aria-controls']:
        for ident in attrs.get(key, '').split():
            need(ident in tags.ids, 'Missing ARIA target')
            labels.append({'attribute': key, 'target': ident})
need([attrs['href'] for tag, attrs in tags.tags if tag == 'link' and attrs.get('rel') == 'stylesheet']
     == ['/research/research.css'], 'Shared stylesheet')
need(not any(tag == 'style' or 'style' in attrs for tag, attrs in tags.tags), 'Local styling')
need(all(attrs.get('type') == 'application/ld+json' for tag, attrs in tags.tags if tag == 'script'),
     'Unexpected executable page script')
for token in [metadata['title'], native['doi'], 'author = {Kriebel, Alec}', 'version = {1.0.0}',
              'date = {2026-10-06}', 'Unrefereed, AI-assisted preprint']:
    need(token in bib, 'BibTeX identity token: ' + token)
pdf_text = PDF_TEXT.read_text(encoding='utf-8')
need(len([page for page in pdf_text.split('\f') if page.strip()]) == 6, 'Preserved PDF text page count')
need('Newly authored prose/data CC BY 4.0; Python code MIT' in meta['DC.rights'], 'Metadata rights split')
need(model['rights']['newly_authored_Python'] == 'MIT' and model['follow_up'] is None, 'Rights/followup')
after = {'writer': inventory(WRITER), 'source': inventory(SOURCE),
         'pins': {str(path.relative_to(P)): record(path) for path in PINS}}
need(after == before, 'Writer/source/control changed during data-only review')
putj('GUARDS_AFTER.json', after)
finished = datetime.now(timezone.utc).isoformat()
putj('DATA_CHECKS.json', {'started_UTC': started, 'completed_UTC': finished,
      'status': 'PASS_BOUNDED_PRIVATE_EDITORIAL_DATA_CHECKS', 'writer_extent': [23, 1],
      'source_extent': [56, 10], 'writer_source_clearance_pins_exact_before_after': True,
      'whole_actual_head_main_assembly_exact': True, 'complete_abstract_surfaces_exact': True,
      'native_assets_all_three_original_encodings_exact': assets, 'static_local_paths': paths,
      'ARIA_references': labels, 'native_TeX_lines': 165, 'native_PDF_text_pages_read': 6,
      'W_or_network_or_rendered_live_checks': False, 'scientific_source_helper_runs_import_AST_compile_tests': 0,
      'owned_data_only_reader_invocations': 1, 'concrete_findings': [], 'follow_up': None})
with (OWN / 'RESEARCH_LOG.md').open('x', encoding='utf-8') as handle:
    handle.write('# Private fact-review log\n\n- ' + started + ' — 80% complete: manual full-surface/native fidelity comparison completed; single saved reader fully read before execution. No concrete discrepancy found.\n- '
                 + finished + ' — 100% complete: bounded data-only checks and complete writer/source before-after guards passed. No source/helper/scientific execution or external action. Final finite freeze follows; no subsequent writes.\n')
for name in ['READER.stdout.txt', 'READER.stderr.txt']:
    need((OWN / name).read_bytes() == b'', 'Nonempty literal reader stream: ' + name)
snapshot = inventory(OWN)
manifest = {'schema': 'finite-private-fact-review-manifest-v1', 'UTC': finished, 'root': str(OWN),
            'root_mode': snapshot['root_mode'], 'payload_files': [{'path': name, **value} for name, value in snapshot['files'].items()],
            'directories': [{'path': name, **value} for name, value in snapshot['directories'].items()],
            'exact_terminal_exclusions': ['MANIFEST.json', 'FINAL.json'],
            'all_actual_hidden_ignored_empty_topology_and_modes_included': True}
putj('MANIFEST.json', manifest)
putj('FINAL.json', {'schema': 'private-fact-review-final-v1', 'UTC': finished, 'record': 23205294, 'row': 186,
      'status': 'PASS_PRIVATE_EDITORIAL_FIDELITY_FROZEN', 'completion_percent': 100,
      'manifest': {'path': 'MANIFEST.json', **record(OWN / 'MANIFEST.json')},
      'writer_FINAL_pin': PINS[WRITER / 'FINAL.json'], 'writer_MANIFEST_pin': PINS[WRITER / 'MANIFEST.json'],
      'clearance_pin': PINS[CLEARANCE], 'root_review_pin': PINS[ROOT_REVIEW],
      'writer_23files_1dir_source_56files_10dirs_preserved': True, 'concrete_findings': [],
      'new_scientific_clearance_or_action_authority': False, 'follow_up': None,
      'owned_data_only_reader_invocations': 1, 'literal_stdout_stderr_empty': True,
      'source_scientific_helper_import_AST_compile_test_execution': False,
      'W_Git_network_Sheet_deploy_AA_redirect_children_outreach_or_writer_mutation': False,
      'extent': {'regular_files': len(snapshot['files']) + 2, 'child_directories': len(snapshot['directories'])},
      'quiescent_after_freeze': True})
