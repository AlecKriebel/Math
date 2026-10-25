"""Redirect exact old articles after root has accepted their live browser evidence.

Uses a separate Git index and a commit based on fresh origin/main, preserving
the user's shared local index, branch, and unrelated research changes.
"""
from pathlib import Path
from datetime import datetime, timezone
from html import escape
import argparse, hashlib, json, os, re, subprocess, tempfile

PROGRAM = Path(__file__).resolve().parents[1]
REPO = PROGRAM.parent
PUBLIC = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
CONFIG = {
    '21699161': ('minimum-bell-setting-complexity', 'paper.pdf'),
    '22089551': ('bimolecular-positive-recurrence', 'paper-v1.2.4.pdf'),
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('record_ids', nargs='+', choices=CONFIG)
args = parser.parse_args()
assert len(set(args.record_ids)) == len(args.record_ids)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*argv, env=None):
    return subprocess.check_output(['git', '-c', 'gc.auto=0', *argv], cwd=REPO, env=env)

display = json.loads((PROGRAM/'verification/browser-root-disposition.json').read_text())
accepted = {}
for rid in args.record_ids:
    paper = PROGRAM/'papers'/rid
    content = json.loads((paper/'publication.json').read_text())
    promotion = json.loads((paper/'promotion.json').read_text())
    proof = display['papers'][rid]
    assert promotion['status'] == proof['status'] == 'PASS'
    assert proof['html_sha256'] == sha((PUBLIC/'research'/content['slug']/'index.html').read_bytes())
    assert proof['pdf_sha256'] == promotion['pdf_sha256'] == sha((PUBLIC/'research'/content['slug']/content['pdf_filename']).read_bytes())
    assert (PROGRAM/proof['browser_receipt']).is_file()
    live = json.loads((PROGRAM/proof['live_receipt']).read_text())
    page = next(x for x in live['checks'] if x['path'] == 'research/'+content['slug']+'/index.html')
    assert live['passed'] and page['passed'] and page['actual_sha256'] == proof['html_sha256']
    assert page['url'] == 'https://aleckriebel.com/research/'+content['slug']+'/'
    accepted[rid] = (content, page['url'])

assert git('branch', '--show-current').strip() == b'main'
git('fetch', 'origin', 'main')
parent = git('rev-parse', 'origin/main').decode().strip()
paths = ['docs/index.html', 'docs/sitemap.xml'] + ['docs/papers/'+CONFIG[rid][0]+'/index.html' for rid in args.record_ids]
before = {}
for path in paths:
    original = (REPO/path).read_bytes()
    assert original == git('show', parent+':'+path), 'Unrelated local/remote change: '+path
    before[path] = original
after = dict(before)
index = before['docs/index.html'].decode()
sitemap = before['docs/sitemap.xml'].decode()
redirects = []
for rid, (content, destination) in accepted.items():
    old_slug, old_pdf = CONFIG[rid]
    leaf = 'docs/papers/'+old_slug+'/index.html'
    old_base = 'https://aleckriebel.github.io/Math/papers/'+old_slug+'/'
    old_pdf_bytes = git('show', parent+':docs/papers/'+old_slug+'/'+old_pdf)
    assert sha(old_pdf_bytes) == json.loads((PROGRAM/'papers'/rid/'promotion.json').read_text())['pdf_sha256'], 'Not the exact reviewed manuscript'
    assert content['title'] in before[leaf].decode(), 'Old article title mismatch'
    assert 'http-equiv="refresh"' not in before[leaf].decode(), 'Already redirected; inspect receipt first'
    h = escape
    after[leaf] = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paper moved | Alec Kriebel</title>
<meta http-equiv="refresh" content="0; url={h(destination)}">
<link rel="canonical" href="{h(destination)}">
</head><body>
<h1>Paper moved</h1>
<p><a href="{h(destination)}">{h(content['title'])}</a> is now on AlecKriebel.com.</p>
</body></html>
'''.encode()
    old_index = index
    index = index.replace('href="./papers/'+old_slug+'/"', 'href="'+destination+'"')
    index = index.replace('href="./papers/'+old_slug+'/'+old_pdf+'"', 'href="'+destination+content['pdf_filename']+'"')
    assert index != old_index, 'Old index contains no corresponding article or PDF link'
    sitemap, removed = re.subn(r'  <url>\s*<loc>'+re.escape(old_base)+r'</loc>.*?</url>\n', '', sitemap, flags=re.S)
    assert removed == 1, 'Old sitemap correspondence mismatch'
    redirects.append({'record_id': rid, 'source': old_base, 'destination': destination, 'article': leaf})
after['docs/index.html'] = index.encode()
after['docs/sitemap.xml'] = sitemap.encode()
assert all(after[path] != before[path] for path in paths)
for path, data in after.items():
    (REPO/path).write_bytes(data)
fd, index_path = tempfile.mkstemp(prefix='research-verified-redirect-index-')
os.close(fd)
os.unlink(index_path)
env = dict(os.environ, GIT_INDEX_FILE=index_path)
try:
    git('read-tree', parent, env=env)
    git('add', '--', *paths, env=env)
    assert set(git('diff', '--cached', '--name-only', parent, env=env).decode().splitlines()) == set(paths)
    git('diff', '--cached', '--check', parent, '--', *paths, env=env)
    tree = git('write-tree', env=env).decode().strip()
    commit = subprocess.check_output(['git', '-c', 'gc.auto=0', 'commit-tree', tree, '-p', parent], input=b'Redirect verified Bell and reaction-network articles to canonical research pages\n', cwd=REPO, env=env).decode().strip()
    git('push', 'origin', commit+':refs/heads/main')
finally:
    if os.path.exists(index_path):
        os.unlink(index_path)
result = {'utc': datetime.now(timezone.utc).isoformat(), 'commit': commit, 'parent': parent, 'redirects': redirects, 'paths': paths, 'before_sha256': {p: sha(v) for p,v in before.items()}, 'after_sha256': {p: sha(v) for p,v in after.items()}, 'shared_index_and_local_branch_untouched': True, 'live_redirect_verification': 'pending GitHub Pages build'}
(PROGRAM/'redirects/verified-article-redirects.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result))
