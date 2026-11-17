"""Finite data-only capture. Runs only listed ordinary read-only Git commands.

No project Git, redirect, collector, source, or scientific helper is imported or run.
All writes are restricted to this new owned directory. Run once after source review.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
from html.parser import HTMLParser

M = Path('/Users/alec/Documents/Math')
P = M / 'research_website_catalogue_20261024'
OUT = Path(__file__).resolve().parent
C = 'f98cdb2fc47f9a1c613c673bfc2255adc31546df'
D = 'docs/papers/radial-statistical-counterexample'
LEGACY = 'https://aleckriebel.github.io/Math/papers/radial-statistical-counterexample/'
TARGET = 'https://aleckriebel.com/research/radial-orthogonality-dual-conformal-flatness/'
EXPECTED_DOCS = 'e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0'

def utc():
    return datetime.now(timezone.utc).isoformat()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write(rel, data):
    dest = OUT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open('xb') as f:
        f.write(data)

def jwrite(rel, obj):
    write(rel, (json.dumps(obj, indent=2, ensure_ascii=False) + '\n').encode())

env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')
receipts = []

def git(label, *args):
    command = ['git', '-C', str(M), '-c', 'credential.helper=', *args]
    started = utc()
    result = subprocess.run(command, capture_output=True, env=env, check=False)
    write(f'raw/{label}.stdout', result.stdout)
    write(f'raw/{label}.stderr', result.stderr)
    write(f'raw/{label}.exit', (str(result.returncode) + '\n').encode())
    receipts.append({'label': label, 'argv': command, 'started_UTC': started,
                     'finished_UTC': utc(), 'exit': result.returncode,
                     'stdout_bytes': len(result.stdout), 'stdout_SHA256': digest(result.stdout),
                     'stderr_bytes': len(result.stderr), 'stderr_SHA256': digest(result.stderr)})
    if result.returncode != 0:
        raise RuntimeError(f'{label} failed; literal streams retained; no retry')
    return result.stdout

def state():
    return {'git_index_SHA256': digest((M / '.git/index').read_bytes())}

before = state()
head = git('native-refs-before', 'rev-parse', 'HEAD', 'refs/heads/main', 'refs/remotes/origin/main').decode().splitlines()
remote = git('remote-main', 'ls-remote', '--exit-code', 'https://github.com/AlecKriebel/Math.git', 'refs/heads/main').decode()
if remote.strip().split()[0] != C:
    raise RuntimeError('Remote main changed; retain capture and stop without fetching')
git('current-commit', 'cat-file', '-p', C)
docs = git('current-docs-tree', 'rev-parse', C + ':docs').decode().strip()
assert docs == EXPECTED_DOCS
tree = git('article-tree', 'ls-tree', '-r', '--full-tree', C, D).decode()
git('current-docs-exact-identity-hits', 'grep', '-n', '-i', '-e',
    'radial-statistical-counterexample', '-e', '22983519', '-e',
    'radial orthogonality', '-e', 'dual 1-conformal flatness', C, '--', 'docs')
git('current-docs-substring-candidate-paths', 'grep', '-l', '-i', '-e',
    'radial', '-e', 'statistical', C, '--', 'docs')

objects = []
for line in tree.splitlines():
    left, path = line.split('\t', 1)
    mode, kind, blob = left.split()
    assert kind == 'blob' and path.startswith(D + '/')
    data = git('article-asset-' + Path(path).name, 'cat-file', 'blob', blob)
    write('current/' + path, data)
    objects.append({'path': path, 'git_mode': mode, 'git_blob': blob,
                    'bytes': len(data), 'SHA256': digest(data),
                    'public_URL': 'https://aleckriebel.github.io/Math/' + path[len('docs/'):]})
index = git('current-docs-index', 'show', C + ':docs/index.html')
write('current/docs/index.html', index)

inputs = [
    'verification/root-clearance-22983519-20261117.json',
    'papers/22983519/reviews/root/ROOT_REVIEW.md',
    'papers/22983519/sources/SOURCE_FINAL.json',
    'papers/22983519/sources/SOURCE_MANIFEST.json',
    'papers/22983519/sources/record.response.body',
]
input_receipts = []
for rel in inputs:
    committed = git('native-' + Path(rel).name, 'show', C + ':research_website_catalogue_20261024/' + rel)
    local = (P / rel).read_bytes()
    assert committed == local
    write('inputs/' + rel, committed)
    input_receipts.append({'path': rel, 'from_commit': C, 'bytes': len(committed),
                           'SHA256': digest(committed), 'working_bytes_equal_committed': True})
record = json.loads((OUT / 'inputs/papers/22983519/sources/record.response.body').read_bytes())
native_assets = {}
comparisons = []
for name in ['SHA256SUMS.txt', 'source-and-verification.zip', 'paper.pdf']:
    native = (P / 'papers/22983519/sources/assets' / name).read_bytes()
    write('native-assets/' + name, native)
    native_assets[name] = {'bytes': len(native), 'SHA256': digest(native)}
    current = (OUT / 'current' / D / name).read_bytes()
    comparisons.append({'file': name, 'native': native_assets[name],
                        'current_SHA256': digest(current), 'byte_identical': current == native})
    assert current == native

class Identity(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta, self.canonical, self.links = {}, [], []
        self.in_title, self.in_h1 = False, False
        self.title, self.h1 = [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta':
            self.meta[a.get('name', a.get('property', ''))] = a.get('content')
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a['href'])
        if tag in ('a', 'link') and a.get('href'):
            self.links.append(a['href'])
        if tag == 'title': self.in_title = True
        if tag == 'h1': self.in_h1 = True
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        if tag == 'h1': self.in_h1 = False
    def handle_data(self, data):
        if self.in_title: self.title.append(data)
        if self.in_h1: self.h1.append(data)

html = (OUT / 'current' / D / 'index.html').read_bytes()
identity = Identity()
identity.feed(html.decode())
assert identity.meta['citation_title'] == record['metadata']['title']
assert identity.meta['citation_doi'] == record['doi']
assert identity.meta['citation_publication_date'] == record['metadata']['publication_date']
assert identity.canonical == [LEGACY]
assert any(x['identifier'] == LEGACY and x['relation'] == 'isDocumentedBy'
           for x in record['metadata']['related_identifiers'])
after_head = git('native-refs-after', 'rev-parse', 'HEAD', 'refs/heads/main', 'refs/remotes/origin/main').decode().splitlines()
after = state()
assert before == after and head == after_head
jwrite('EXECUTION.json', {'schema': 'finite-readonly-current-git-capture-v1',
       'UTC': utc(), 'git_command_receipts': receipts, 'git_state_before': before,
       'git_state_after': after, 'refs_before': head, 'refs_after': after_head,
       'native_index_and_refs_unchanged': True, 'project_helpers_executed': 0,
       'scientific_or_source_runs': 0, 'fetches': 0, 'mutating_Git_commands': 0})
jwrite('CORRESPONDENCE.json', {'schema': 'bounded-current-legacy-correspondence-v1',
       'UTC': utc(), 'row': 184, 'record': 22983519,
       'status': 'GENUINE_CURRENT_COMMITTED_ARTICLE_CORRESPONDENCE',
       'remote_main_at_capture': C, 'current_docs_tree': docs,
       'current_HTML_path': D + '/index.html', 'legacy_URL': LEGACY,
       'eventual_website_canonical': TARGET, 'target_live_or_UI_checked': False,
       'title_element': ''.join(identity.title), 'h1': ''.join(identity.h1),
       'citation_metadata': identity.meta, 'canonical': identity.canonical,
       'article_links': identity.links, 'objects': objects,
       'native_asset_comparisons': comparisons, 'input_receipts': input_receipts,
       'scientific_clearance': 'inherited; no new scientific verdict',
       'clearance_SHA256': input_receipts[0]['SHA256'],
       'clearance_commit': C,
       'locator_correction': 'a8ccbce4 is a clearance file digest prefix, not a commit',
       'redirect_executed': False,
       'redirect_condition': 'Only after the new exact target is live and independently verified; revalidate current legacy object before any change',
       'absence_or_global_priority_claim': False,
       'outside_contact_or_individual_outreach_prepared': False})
print(json.dumps({'status': 'CAPTURED', 'owned_root': str(OUT),
                  'remote_main': C, 'docs_tree': docs,
                  'article_objects': len(objects), 'native_assets_byte_identical': comparisons,
                  'clearance_SHA256': input_receipts[0]['SHA256']}, indent=2))
