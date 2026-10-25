"""Redirect the verified group-paper article, preserving the shared Git checkout."""
from pathlib import Path
from datetime import datetime, timezone
from html import escape
import hashlib, json, os, re, subprocess, tempfile

PROGRAM = Path(__file__).resolve().parents[1]
REPO = PROGRAM.parent
PUBLIC = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
rid = '22770864'
paper = PROGRAM/'papers'/rid
content = json.loads((paper/'publication.json').read_text())
assert json.loads((paper/'promotion.json').read_text())['status'] == 'PASS'
receipt = json.loads((PROGRAM/'verification/live-22770864-22729537.json').read_text())
page_path = 'research/'+content['slug']+'/index.html'
live = next(x for x in receipt['checks'] if x['path'] == page_path)
assert receipt['passed'] and live['passed']
assert live['actual_sha256'] == hashlib.sha256((PUBLIC/page_path).read_bytes()).hexdigest()
destination = live['url']
assert destination == 'https://aleckriebel.com/research/'+content['slug']+'/'
old_base = 'https://aleckriebel.github.io/Math/papers/kourovka-16-63/'
leaf = 'docs/papers/kourovka-16-63/index.html'
paths = [leaf, 'docs/index.html', 'docs/sitemap.xml']

def git(*args, env=None):
    return subprocess.check_output(['git','-c','gc.auto=0',*args],cwd=REPO,env=env)

assert git('branch','--show-current').strip() == b'main'
git('fetch','origin','main')
parent = git('rev-parse','origin/main').decode().strip()
before = {}
for path in paths:
    original = (REPO/path).read_bytes()
    assert original == git('show',parent+':'+path), 'Unrelated local/remote change: '+path
    before[path] = original
assert content['doi'].encode() in before[leaf]
if b'http-equiv="refresh"' in before[leaf] and destination.encode() in before[leaf]:
    print('Verified group redirect already present')
    raise SystemExit(0)

h = escape
redirect = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paper moved | Alec Kriebel</title>
<meta http-equiv="refresh" content="0; url={h(destination)}">
<link rel="canonical" href="{h(destination)}">
</head><body>
<h1>Paper moved</h1>
<p><a href="{h(destination)}">{h(content['title'])}</a> is now on AlecKriebel.com.</p>
</body></html>
'''
index = before['docs/index.html'].decode()
index = index.replace('href="./papers/kourovka-16-63/"','href="'+destination+'"')
index = index.replace('href="./papers/kourovka-16-63/paper.pdf"','href="'+destination+content['pdf_filename']+'"')
sitemap, removed = re.subn(r'  <url>\s*<loc>'+re.escape(old_base)+r'</loc>.*?</url>\n','',before['docs/sitemap.xml'].decode(),flags=re.S)
assert removed == 1
after = {leaf:redirect.encode(),'docs/index.html':index.encode(),'docs/sitemap.xml':sitemap.encode()}
assert all(after[p] != before[p] for p in paths)
for path,data in after.items(): (REPO/path).write_bytes(data)
fd,index_path = tempfile.mkstemp(prefix='research-redirect-index-')
os.close(fd); os.unlink(index_path)
env = dict(os.environ, GIT_INDEX_FILE=index_path)
try:
    git('read-tree',parent,env=env)
    git('add','--',*paths,env=env)
    assert set(git('diff','--cached','--name-only',parent,env=env).decode().splitlines()) == set(paths)
    git('diff','--cached','--check',parent,'--',*paths,env=env)
    tree = git('write-tree',env=env).decode().strip()
    commit = subprocess.check_output(['git','-c','gc.auto=0','commit-tree',tree,'-p',parent],input=b'Redirect verified group paper to its canonical research page\n',cwd=REPO,env=env).decode().strip()
    git('push','origin',commit+':refs/heads/main')
finally:
    if os.path.exists(index_path): os.unlink(index_path)
result = {'utc':datetime.now(timezone.utc).isoformat(),'record_id':rid,'commit':commit,'parent':parent,'source':old_base,'destination':destination,'paths':paths,'before_sha256':{p:hashlib.sha256(v).hexdigest() for p,v in before.items()},'after_sha256':{p:hashlib.sha256(v).hexdigest() for p,v in after.items()},'shared_index_and_local_branch_untouched':True,'live_redirect_verification':'pending GitHub Pages build'}
(PROGRAM/'redirects/group-redirect.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
