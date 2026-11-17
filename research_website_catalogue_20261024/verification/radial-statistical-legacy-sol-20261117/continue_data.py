"""One bounded continuation after the preserved manifest-scope assertion failure.

Reads earlier captured current objects and native data; never imports or reruns
the earlier helper. Only new Git commands are explicitly read-only plumbing.
"""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import json
import os
import subprocess

M = Path('/Users/alec/Documents/Math')
P = M / 'research_website_catalogue_20261024'
O = Path(__file__).resolve().parent
C = 'f98cdb2fc47f9a1c613c673bfc2255adc31546df'
D = 'docs/papers/radial-statistical-counterexample'
LEGACY = 'https://aleckriebel.github.io/Math/papers/radial-statistical-counterexample/'
TARGET = 'https://aleckriebel.com/research/radial-orthogonality-dual-conformal-flatness/'

def utc(): return datetime.now(timezone.utc).isoformat()
def sha(data): return hashlib.sha256(data).hexdigest()
def put(path, data):
    target = O / path
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as f: f.write(data)
def jout(path, obj): put(path, (json.dumps(obj, indent=2, ensure_ascii=False) + '\n').encode())

env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')
receipts = []
def git(label, *args):
    argv = ['git', '-C', str(M), '-c', 'credential.helper=', *args]
    start = utc()
    r = subprocess.run(argv, capture_output=True, check=False, env=env)
    for ext, data in [('stdout', r.stdout), ('stderr', r.stderr), ('exit', (str(r.returncode)+'\n').encode())]:
        put('raw/' + label + '.' + ext, data)
    receipts.append({'argv': argv, 'label': label, 'started_UTC': start,
                     'finished_UTC': utc(), 'exit': r.returncode,
                     'stdout_bytes': len(r.stdout), 'stdout_SHA256': sha(r.stdout),
                     'stderr_bytes': len(r.stderr), 'stderr_SHA256': sha(r.stderr)})
    if r.returncode != 0: raise RuntimeError(label + ' failed; no retry')
    return r.stdout

index_before = sha((M/'.git/index').read_bytes())
refs_before = git('continuation-refs-before', 'rev-parse', 'HEAD', 'refs/heads/main', 'refs/remotes/origin/main')
assert refs_before == (O/'raw/native-refs-before.stdout').read_bytes()
remote = (O/'raw/remote-main.stdout').read_text()
assert remote.strip().split() == [C, 'refs/heads/main']
docs_tree = (O/'raw/current-docs-tree.stdout').read_text().strip()
assert docs_tree == 'e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0'

objects = []
for line in (O/'raw/article-tree.stdout').read_text().splitlines():
    left, path = line.split('\t')
    mode, kind, blob = left.split()
    data = (O/'current'/path).read_bytes()
    assert kind == 'blob'
    # Verify Git blob identity without invoking Git or source code.
    assert hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest() == blob
    objects.append({'path': path, 'git_mode': mode, 'git_blob': blob,
                    'bytes': len(data), 'SHA256': sha(data),
                    'public_URL': 'https://aleckriebel.github.io/Math/' + path[len('docs/'):]})

inputs = []
for path in sorted((O/'inputs').rglob('*')):
    if path.is_file():
        rel = path.relative_to(O/'inputs').as_posix()
        data = path.read_bytes()
        assert data == (P/rel).read_bytes()
        inputs.append({'path': rel, 'from_commit': C, 'bytes': len(data), 'SHA256': sha(data),
                       'working_bytes_equal_captured_committed': True})
record = json.loads((O/'inputs/papers/22983519/sources/record.response.body').read_bytes())
clearance = json.loads((O/'inputs/verification/root-clearance-22983519-20261117.json').read_bytes())
source_manifest = json.loads((O/'inputs/papers/22983519/sources/SOURCE_MANIFEST.json').read_bytes())
manifest_entries = {x['path']: x for x in source_manifest['files']}
comparisons = []
for name in ['SHA256SUMS.txt', 'source-and-verification.zip', 'paper.pdf']:
    native = (P/'papers/22983519/sources/assets'/name).read_bytes()
    dest = O/'native-assets'/name
    if dest.exists(): assert dest.read_bytes() == native
    else: put('native-assets/'+name, native)
    native_entry = manifest_entries['assets/'+name]
    assert sha(native) == native_entry['SHA256'] and len(native) == native_entry['bytes']
    current = (O/'current'/D/name).read_bytes()
    native_md5 = next(x['checksum'] for x in record['files'] if x['key'] == name)
    assert native_md5 == 'md5:' + hashlib.md5(native).hexdigest()
    same = native == current
    comparisons.append({'file': name, 'native_bytes': len(native), 'native_SHA256': sha(native),
                        'native_md5_verified': native_md5, 'current_bytes': len(current),
                        'current_SHA256': sha(current), 'byte_identical': same,
                        'interpretation': 'Different checksum scopes; expected inequality' if name == 'SHA256SUMS.txt' else 'Exact deposited substantive asset'})
    if name != 'SHA256SUMS.txt': assert same

checksum_checks = []
for which, path in [('site', O/'current'/D/'SHA256SUMS.txt'), ('native', O/'native-assets/SHA256SUMS.txt')]:
    for line in path.read_text().splitlines():
        expected, name = line.split(None, 1)
        root = O/'current'/D if which == 'site' else O/'native-assets'
        actual = sha((root/name).read_bytes())
        checksum_checks.append({'scope': which, 'file': name, 'expected': expected,
                                'actual': actual, 'matches': actual == expected})
assert all(x['matches'] for x in checksum_checks)

class Identity(HTMLParser):
    def __init__(self):
        super().__init__(); self.meta={}; self.canonical=[]; self.links=[]
        self.title=[]; self.h1=[]; self.structured=[]
        self.t=False; self.h=False; self.j=False; self.jbuf=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='meta': self.meta[a.get('name',a.get('property',''))]=a.get('content')
        if tag=='link' and a.get('rel')=='canonical': self.canonical.append(a['href'])
        if tag in ('a','link') and a.get('href'): self.links.append(a['href'])
        if tag=='title': self.t=True
        if tag=='h1': self.h=True
        if tag=='script' and a.get('type')=='application/ld+json': self.j=True; self.jbuf=[]
    def handle_endtag(self, tag):
        if tag=='title': self.t=False
        if tag=='h1': self.h=False
        if tag=='script' and self.j:
            self.structured.append(json.loads(''.join(self.jbuf))); self.j=False
    def handle_data(self, data):
        if self.t: self.title.append(data)
        if self.h: self.h1.append(data)
        if self.j: self.jbuf.append(data)

identity=Identity(); identity.feed((O/'current'/D/'index.html').read_text())
assert identity.meta['citation_title'] == record['metadata']['title'] == clearance['title']
assert identity.meta['citation_doi'] == record['doi']
assert identity.meta['citation_publication_date'] == record['metadata']['publication_date']
assert identity.canonical == [LEGACY]
article = next(x for x in identity.structured if x.get('@type')=='ScholarlyArticle')
assert article['version'] == record['metadata']['version'] == '1.0.1'
assert article['headline'] == record['metadata']['title']
assert article['encoding']['contentUrl'] == identity.meta['citation_pdf_url'] == LEGACY+'paper.pdf'
assert any(x['identifier']==LEGACY and x['relation']=='isDocumentedBy' for x in record['metadata']['related_identifiers'])

ramsey = git('collision-ramsey-HTML', 'show', C+':docs/research/ramsey-number-5-5/index.html')
put('collisions/ramsey-index.html', ramsey)
ramsey_id=Identity(); ramsey_id.feed(ramsey.decode())
assert ramsey_id.meta.get('citation_doi') != record['doi']
git('collision-ramsey-substring', 'grep', '-n', '-i', '-e', 'radial', '-e', 'statistical', C, '--', 'docs/research/ramsey-number-5-5/index.html')
git('collision-fps-substring', 'grep', '-n', '-i', '-e', 'radial', '-e', 'statistical', C, '--', 'docs/papers/fps-equality/preprint-round2.md', 'docs/papers/fps-equality/verify.py')
refs_after = git('continuation-refs-after', 'rev-parse', 'HEAD', 'refs/heads/main', 'refs/remotes/origin/main')
index_after = sha((M/'.git/index').read_bytes())
assert refs_before == refs_after and index_before == index_after

exact_hits = (O/'raw/current-docs-exact-identity-hits.stdout').read_text()
assert all(line.startswith(C+':docs/') for line in exact_hits.splitlines())
candidate_paths = [line.split(':',1)[1] for line in (O/'raw/current-docs-substring-candidate-paths.stdout').read_text().splitlines()]
classifications = []
for path in candidate_paths:
    if path == D+'/index.html': kind='Genuine corresponding article'
    elif path.startswith(D+'/'): kind='Corresponding article supporting asset; not an HTML article redirect candidate'
    elif path == 'docs/index.html': kind='Research index entry for the article; not the corresponding standalone article'
    elif path == 'docs/sitemap.xml': kind='Sitemap locator; not an article'
    elif path.startswith('docs/research/ramsey-number-5-5/'):
        kind='Different HTML article; lexical statistical-methods hit, different identity'
    elif path.endswith('.zip'): kind='Binary ZIP lexical hit; filename/content substring does not establish HTML article correspondence'
    else: kind='Different project note/code lexical hit; not an HTML article'
    classifications.append({'path':path, 'classification':kind})

raw_inventory=[]
for path in sorted((O/'raw').iterdir()):
    data=path.read_bytes()
    raw_inventory.append({'path':path.relative_to(O).as_posix(),'bytes':len(data),'SHA256':sha(data)})
jout('EXECUTION.json', {'schema':'finite-readonly-capture-continuation-v1','UTC':utc(),
      'original_capture_exit':1,'original_capture_failure':'Incorrect checksum-manifest byte-equality assertion',
      'original_capture_reexecuted':False,'first_run_command_times':'Not persisted before abort; raw command streams retained',
      'continuation_receipts':receipts,'raw_inventory':raw_inventory,
      'native_index_SHA256_before_continuation':index_before,'native_index_SHA256_after_continuation':index_after,
      'native_index_unchanged_during_continuation':True,
      'refs_equal_original_capture_and_continuation_before_after':True,
      'native_refs':refs_after.decode().splitlines(),
      'mutating_Git_commands':0,'fetches':0,'source_or_scientific_runs':0,
      'other_project_helpers_executed':0,'own_data_capture_helper_runs':2,
      'outside_contact_or_individual_outreach_prepared':False})
jout('CORRESPONDENCE.json', {'schema':'bounded-current-legacy-correspondence-v1','UTC':utc(),
      'row':184,'record':22983519,'status':'GENUINE_CURRENT_COMMITTED_ARTICLE_CORRESPONDENCE',
      'remote_main_at_capture':C,'current_docs_tree':docs_tree,'current_HTML_path':D+'/index.html',
      'legacy_URL':LEGACY,'eventual_website_canonical':TARGET,'target_live_or_UI_checked':False,
      'title_element':''.join(identity.title),'h1':''.join(identity.h1),'citation_metadata':identity.meta,
      'canonical':identity.canonical,'scholarly_article':article,'objects':objects,
      'native_asset_comparisons':comparisons,'checksum_checks':checksum_checks,
      'input_receipts':inputs,'candidate_classifications':classifications,
      'different_HTML_article':{'path':'docs/research/ramsey-number-5-5/index.html',
                                'title':''.join(ramsey_id.title),'h1':''.join(ramsey_id.h1),
                                'citation_doi':ramsey_id.meta.get('citation_doi')},
      'clearance_SHA256':sha((O/'inputs/verification/root-clearance-22983519-20261117.json').read_bytes()),
      'clearance_commit':C,'locator_correction':'a8ccbce4 is the clearance file SHA-256 prefix, not a Git revision',
      'scientific_clearance':'inherited; no new scientific verdict',
      'redirect_executed':False,
      'redirect_condition':'Only after exact new target is live and verified; revalidate current article object immediately before a separately authorized change',
      'global_historical_absence_or_priority_claim':False,'outside_contact_or_individual_outreach_prepared':False})
print(json.dumps({'status':'CONTINUATION_COMPLETE','objects':len(objects),'native_asset_comparisons':comparisons,
                  'checksum_checks_passed':len(checksum_checks),'native_index_SHA256':index_after,
                  'HTML':next(x for x in objects if x['path'].endswith('/index.html'))},indent=2))
