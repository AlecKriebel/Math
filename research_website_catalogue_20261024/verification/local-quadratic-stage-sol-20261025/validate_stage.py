"""Validate owned staging and negative controls without mutating frozen inputs."""
from pathlib import Path
import ast
import copy
import datetime
import hashlib
from html import escape, unescape
from html.parser import HTMLParser
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

O = Path(__file__).resolve().parent
R = O.parents[1]
S = O / 'public'
P = R / 'papers/23306332'
LIVE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
SLUG = 'nonunique-nearest-stable-complex-quadratics'
TARGET = S / 'research' / SLUG
C = json.loads((P / 'publication.json').read_text())
G = json.loads((P / 'promotion.json').read_text())
BASE = C['canonical_url']
CHECKER = O / 'final-content-check.stage.py'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fresh(p, content):
    with p.open('x') as stream:
        stream.write(content)


class BodyText(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.in_body = False
        self.parts = []
        self.a = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.a.append((tag, dict(attrs)))
        if tag == 'body':
            self.in_body = True
        if self.in_body and tag in ['h1', 'h2', 'p', 'li', 'br', 'header', 'section', 'footer']:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False
        if self.in_body and tag in ['h1', 'h2', 'p', 'li', 'section']:
            self.parts.append('\n')

    def handle_data(self, data):
        if self.in_body:
            self.parts.append(data)


html = (TARGET / 'index.html').read_text()
body = BodyText(html)
plaintext = '\n\n'.join(' '.join(x.split()) for x in ''.join(body.parts).split('\n') if x.strip()) + '\n'
fresh(O / 'public-copy-23306332.txt', plaintext)
sections = {}
for section_id in ['abstract', 'plain-language', 'result', 'proof', 'limits', 'status', 'collaborate']:
    part = re.search('<section id="' + section_id + '">(.*?)</section>', html, re.S).group(1)
    sections[section_id] = [unescape(x) for x in re.findall('<p>(.*?)</p>', part, re.S)]
fresh(O / 'public-sections-23306332.json', json.dumps(sections, ensure_ascii=False, indent=2) + '\n')
positive = json.loads((O / 'target-stage-check-v1.json').read_text())
assert positive['status'] == 'PASS' and len(positive['papers']['23306332']['checks']) == 76

index = (S / 'research/index.html').read_text()
old_index = (LIVE / 'research/index.html').read_text()
get_index = lambda text: json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S).group(1))['mainEntity']
old_items, items = get_index(old_index), get_index(index)
assert old_items['numberOfItems'] == len(old_items['itemListElement']) == 47
assert items['numberOfItems'] == len(items['itemListElement']) == 48
assert items['itemListElement'][:-1] == old_items['itemListElement']
assert items['itemListElement'][-1]['url'] == BASE and items['itemListElement'][-1]['name'] == C['title']
assert len({x['url'] for x in items['itemListElement']}) == 48
old_urls = [x.text for x in ET.fromstring((LIVE / 'research/sitemap.xml').read_text()).iter() if x.tag.endswith('loc')]
urls = [x.text for x in ET.fromstring((S / 'research/sitemap.xml').read_text()).iter() if x.tag.endswith('loc')]
assert len(old_urls) == 48 and len(urls) == 49 and len(set(urls)) == 49
assert set(urls) - set(old_urls) == {BASE}
assert sha(S / 'research/research.css') == sha(LIVE / 'research/research.css')
assert sha(S / 'robots.txt') == sha(LIVE / 'robots.txt')
assert sorted(x.name for x in (S / 'research').iterdir()) == sorted(['index.html', 'research.css', 'sitemap.xml', SLUG])
assert sorted(x.name for x in TARGET.iterdir()) == sorted(['index.html', 'citation.bib', C['pdf_filename'], C['supplement_filename']])
fresh(O / 'index-sitemap-checks.json', json.dumps({
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'PASS',
    'old_index_items': 47, 'staged_index_items': 48, 'all_old_index_items_unchanged': True,
    'old_sitemap_urls': 48, 'staged_sitemap_urls': 49, 'only_new_sitemap_url': BASE,
    'only_four_shared_files_and_one_new_paper_staged': True, 'css_robots_unchanged': True,
    'scope': 'Private local stage only; no live URL or browser observation.'}, indent=2) + '\n')

# Execute the same full stage checker against isolated altered copies. Every
# output path is new; the pristine stage and all original inputs remain intact.
negative = []
sentences = re.split(r'(?<=\.)\s+', C['abstract'])


def omit_sentence(number):
    replacement = ' '.join(x for i, x in enumerate(sentences) if i != number)
    return lambda folder: change_text(folder / 'research' / SLUG / 'index.html',
        '<section id="abstract"><h2>Abstract</h2><p>' + escape(C['abstract']) + '</p>',
        '<section id="abstract"><h2>Abstract</h2><p>' + escape(replacement) + '</p>')


def change_text(path, old, new):
    text = path.read_text()
    assert old in text, old
    path.write_text(text.replace(old, new, 1))


def alter_pdf(folder):
    path = folder / 'research' / SLUG / C['pdf_filename']
    path.write_bytes(path.read_bytes() + b'\n')


def alter_zip(folder):
    with zipfile.ZipFile(folder / 'research' / SLUG / C['supplement_filename'], 'a') as archive:
        archive.comment = b'owned negative control'


def remove_index_entry(folder):
    path = folder / 'research/index.html'
    text = path.read_text()
    text, count = re.subn(r'<li><a href="/research/' + SLUG + r'/">.*?</li>', '', text, count=1, flags=re.S)
    assert count == 1
    path.write_text(text)


cases = [
    ('abstract-first-omitted', omit_sentence(0), ['abstract']),
    ('abstract-middle-omitted', omit_sentence(len(sentences) // 2), ['abstract']),
    ('abstract-last-omitted', omit_sentence(len(sentences) - 1), ['abstract']),
    ('citation-doi-altered', lambda f: change_text(f / 'research' / SLUG / 'index.html',
        '<meta name="citation_doi" content="10.5281/zenodo.23306332">',
        '<meta name="citation_doi" content="10.5281/zenodo.00000000">'), ['citation_doi']),
    ('date-label-altered', lambda f: change_text(f / 'research' / SLUG / 'index.html',
        '<br>Manuscript dated <time', '<br>Published <time'), ['printed_date_and_metadata_version_distinguished']),
    ('bibtex-edition-altered', lambda f: change_text(f / 'research' / SLUG / 'citation.bib',
        C['bibtex_note'], 'Unrefereed research note, altered edition'), ['bibtex']),
    ('pdf-bytes-altered', alter_pdf, ['pdf_filename']),
    ('zip-bytes-altered', alter_zip, ['supplement_filename']),
    ('mixed-metric-caveat-omitted', lambda f: change_text(f / 'research' / SLUG / 'index.html',
        'its representing normal vector can tilt in a mixed metric.', 'its representing normal vector is omitted.'),
        ['result', 'mixed_epigraph_covector_scope']),
    ('canonical-altered', lambda f: change_text(f / 'research' / SLUG / 'index.html',
        '<link rel="canonical" href="' + BASE + '">',
        '<link rel="canonical" href="https://example.invalid/">'), ['canonical']),
    ('sitemap-entry-omitted', lambda f: change_text(f / 'research/sitemap.xml',
        '<loc>' + BASE + '</loc>', '<loc>https://example.invalid/</loc>'), ['sitemap']),
    ('index-entry-omitted', remove_index_entry, ['index_entry']),
]

for name, mutate, expected in cases:
    case = O / 'negative' / name
    case.mkdir(parents=True, exist_ok=False)
    site = case / 'public'
    shutil.copytree(S, site)
    mutate(site)
    command = ['/opt/homebrew/bin/python3', '-B', str(CHECKER), '23306332',
               '--site', str(site), '--output-dir', str(case), '--output-stem', 'check']
    run = subprocess.run(command, cwd=R, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), capture_output=True, text=True)
    fresh(case / 'stdout.json', run.stdout)
    fresh(case / 'stderr.txt', run.stderr)
    report = json.loads((case / 'check.json').read_text())
    failures = [x.split(': ', 1)[1] for x in report['issues']]
    assert run.returncode == 1 and report['status'] == 'ISSUES_FOUND'
    assert not run.stderr and set(expected).issubset(failures), (name, failures)
    negative.append({'name': name, 'rejected': True, 'expected_failed_checks': expected,
                     'actual_failed_checks': failures, 'exit_code': run.returncode})

# Authority and original-verdict mutants remain in memory. The new branch is
# extracted from the exact proposed checker so the sealed configs stay opaque
# to writes and no alternate source copy is used as public authority.
tree = ast.parse((O / 'final-content-check.proposed.py').read_text())
env = dict(Path=Path, re=re, json=json, hashlib=hashlib, unicodedata=unicodedata,
           zipfile=zipfile, unescape=unescape)
nodes = []
for node in tree.body:
    if isinstance(node, ast.FunctionDef):
        nodes.append(node)
    elif isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) and t.id.isupper() for t in node.targets):
        try:
            ast.literal_eval(node.value)
        except (ValueError, TypeError):
            continue
        nodes.append(node)
exec(compile(ast.Module(body=nodes, type_ignores=[]), '<proposed checker helpers>', 'exec'), env)
loop = next(n for n in tree.body if isinstance(n, ast.For) and isinstance(n.target, ast.Name) and n.target.id == 'rid')
branch = next(n for n in loop.body if isinstance(n, ast.If) and ast.unparse(n.test) == "rid == '23306332'")
code = compile(ast.Module(body=[branch], type_ignores=[]), '<proposed quadratic branch>', 'exec')
sys.dont_write_bytecode = True
sys.path.insert(0, str(R / 'scripts'))
from published_assets import normalized_receipt_view, asset_name
raw_receipt = json.loads((P / 'sources/receipt.json').read_text())
textpath = P / C['source_binding']['source_tex_path']
source = textpath.read_text()
a = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', source, re.S).group(1)
schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1))
article = next(x for x in schema['@graph'] if x['@type'] == 'ScholarlyArticle')
env.update(R=R, p=P, c=C, gate=G, rid='23306332', source=source, a=a,
           textpath=textpath, h=html, f=TARGET / 'index.html', base=BASE,
           raw_receipt=raw_receipt, receipt=normalized_receipt_view(raw_receipt), asset_name=asset_name,
           record_file=P / 'sources/metadata.json', record=json.loads((P / 'sources/metadata.json').read_text())['metadata'],
           frames=[x for t, x in body.a if t == 'iframe'], texts=['page'] * 6, art=article)


def evaluate(scope):
    observed = {}
    scope = dict(scope, test=lambda name, value: observed.update({name: bool(value)}))
    exec(code, scope)
    return observed


assert all(evaluate(env).values())
memory = []
for name, mutate, expected in [
    ('root-hash-forged', lambda e: e['gate'].__setitem__('root_clearance_sha256', '0' * 64), 'root_clearance_binding'),
    ('scope-mathematical-verdict-rewritten', lambda e: e['gate']['reviews']['scope']['verdict'].__setitem__('mathematical_pass', True), 'frozen_scope_chronology_preserved'),
    ('analytic-verdict-rewritten', lambda e: e['gate']['reviews']['analytic']['verdict'].__setitem__('verdict', 'PASS'), 'custom_scientific_verdicts_preserved'),
    ('metadata-hash-forged', lambda e: e['c']['source_binding'].__setitem__('metadata_sha256', '0' * 64), 'original_metadata_path_binding'),
    ('abstract-symbol-changed', lambda e: e['c'].__setitem__('abstract', e['c']['abstract'].replace('z²', 'z³', 1)), 'abstract_full_source_text'),
    ('raw-filename-schema-rewritten', lambda e: e['raw_receipt']['files'][0].__setitem__('name', e['raw_receipt']['files'][0]['filename']), 'original_receipt_schema_binding'),
]:
    altered = dict(env, c=copy.deepcopy(C), gate=copy.deepcopy(G), raw_receipt=copy.deepcopy(raw_receipt))
    mutate(altered)
    observed = evaluate(altered)
    assert observed[expected] is False
    memory.append({'name': name, 'rejected': True, 'expected_failed_check': expected})
fresh(O / 'negative-controls.json', json.dumps({'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'PASS', 'actual_staged_copy_controls': negative, 'in_memory_authority_controls': memory,
    'pristine_stage_html_unchanged': sha(TARGET / 'index.html') == positive['papers']['23306332']['hashes']['html'],
    'original_configs_and_sources_mutated': False}, ensure_ascii=False, indent=2) + '\n')

before = json.loads((O / 'inputs-before.json').read_text())
shell = json.loads((O / 'shell-inputs-before.json').read_text())
all_inputs = dict(before['files'], **shell)
changed = [name for name, x in all_inputs.items() if not Path(name).is_file()
           or Path(name).stat().st_size != x['bytes'] or sha(Path(name)) != x['sha256']]
assert not changed
live_manifest = json.loads(Path(before['live_readiness_manifest']).read_text())
live_preserved = all(Path(x['path']).stat().st_size == x['bytes'] and sha(Path(x['path'])) == x['sha256'] for x in live_manifest['files'])
assert len(live_manifest['files']) == 51 and live_preserved
editorial_seal_path = P / 'reviews/publication/EDITORIAL_SEAL.json'
editorial_seal = json.loads(editorial_seal_path.read_text())
assert all(sha(P / name) == h for name, h in editorial_seal['files'].items())
result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'completion_percent': 100,
          'status': 'PRIVATE_STAGE_CHECKS_PASS_PENDING_ROOT_RENDER_PUBLICATION_GATES',
          'target_full_content_checks': 76, 'actual_staged_negative_controls': len(negative),
          'in_memory_authority_negative_controls': len(memory), 'old_dispatches_preserved': 46,
          'index_items': 48, 'sitemap_urls': 49, 'all_old_index_items_unchanged': True,
          'live_readiness_bindings_preserved': 51, 'all_input_bindings_preserved': len(all_inputs),
          'changed_inputs': changed, 'all_13_editorial_seal_bindings_unchanged': True,
          'editorial_seal_sha256_unchanged': sha(editorial_seal_path),
          'private_stage_html_sha256': sha(TARGET / 'index.html'),
          'publication_sha256': sha(P / 'publication.json'), 'promotion_sha256': sha(P / 'promotion.json'),
          'pdf_bytes_identical_to_original': sha(TARGET / C['pdf_filename']) == sha(P / 'sources' / C['pdf_filename']),
          'zip_bytes_identical_to_original': sha(TARGET / C['supplement_filename']) == sha(P / 'sources' / C['supplement_filename']),
          'production_url_live_verified': False, 'browser_verified': False,
          'shared_or_public_site_mutated': False, 'rendered_pdf_recompiled': False}
fresh(O / 'stage-validation.json', json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False))
