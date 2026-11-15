"""Install only the ten root-adopted sealed public files; preserve other work."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, tempfile

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
S = P / 'verification/cellularization-tree-private-stage-sol-20261115'
O = Path(__file__).resolve().parent
BASE = '178d87e643aafaf45dad9a6a5ea9fad496729db5'

def need(ok, why):
    if not ok: raise RuntimeError(why)
def now(): return datetime.now(timezone.utc).isoformat()
def obj(f): return json.loads(f.read_bytes())
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*args, env=None, data=None):
    r = subprocess.run(['git', '-c', 'gc.auto=0', *args], cwd=W, env=env,
                       input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode: raise RuntimeError((r.stdout+r.stderr).decode('utf-8','replace')[-2000:])
    return r.stdout
def save(name, value):
    (O/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
def bound(f, row):
    need(f.is_file() and not f.is_symlink(), 'regular '+str(f))
    raw=f.read_bytes(); need(len(raw)==row['bytes'] and sha(raw)==row['SHA256'], 'byte binding '+str(f))
    return raw

need(not (O/'installation.json').exists(), 'Existing installation receipt: inspect, do not repeat')
need(sha((P/'verification/root-cellularization-tree-stage-adoption-20261115.json').read_bytes()) ==
     '1ab9723e9163b2037fda00e2eaa85962497e08fff8e6cea4fae3e1bce388112b', 'exact root adoption')
need(sha((S/'FINAL_SEAL.json').read_bytes()) ==
     '93f0f4409c29185d4947b6050a15db3da82beb674dc6dfb5eef1d4bfcd084a34', 'writer final seal')
audit=P/'verification/cellularization-tree-independent-code-audit-sol-20261115'
need(sha((audit/'FINAL_SEAL.json').read_bytes()) ==
     'baea5b13b919e3026a90a91d071b084077b6e599d0febfcb2c34de7a68b86173', 'independent final seal')
need(git('branch','--show-current').decode().strip()=='master' and
     git('rev-parse','HEAD').decode().strip()==BASE, 'existing website master/HEAD')
need(git('ls-remote','origin','refs/heads/master').decode().split()[0]==BASE, 'remote master baseline')
base=obj(S/'FRESH_BASELINE.json'); public=W/'public'
need(len(base['public_files'])==585, '585 baseline')
need({str(f.relative_to(public)) for f in public.rglob('*') if f.is_file()} ==
     {r['path'] for r in base['public_files']}, 'whole old public namespace')
for row in base['public_files']: bound(public/row['path'],row)
for row in base['site_configurations']: bound(Path(row['path']),row)
rows=obj(S/'OVERLAY_MANIFEST.json')['files'];need(len(rows)==10, 'ten exact overlay paths')
copies=[];target=set()
for row in rows:
    rel=Path(row['public_relative_path'])
    need(not rel.is_absolute() and '..' not in rel.parts and rel.as_posix().startswith('research/'), 'safe public relative path')
    need(rel.as_posix() not in target, 'unique destination'); target.add(rel.as_posix())
    raw=bound(S/row['path'],row);need(raw==bound(S/'candidate-b/public'/rel,row),'paired byte equality')
    if row['action']=='add_new_leaf':need(not (public/rel).exists(),'new leaf absent')
    else:need(row['action']=='replace_aggregate_only' and rel.as_posix() in
              {'research/index.html','research/sitemap.xml'},'only two aggregate replacements')
    copies.append(dict(row,source=str(S/row['path']),destination=str(public/rel)))
need(sum(x['action']=='add_new_leaf' for x in rows)==8,'eight new leaves')
gitpaths=['public/'+x for x in sorted(target)]
def protected_index():
    records=git('ls-files','--stage','-z').split(b'\0')
    records=[x for x in records if x and x.split(b'\t',1)[1].decode() not in gitpaths]
    return len(records),sha(b'\0'.join(records)+b'\0')
protected=protected_index()
idx=Path(git('rev-parse','--git-path','index').decode().strip())
if not idx.is_absolute():idx=W/idx
index_sha=sha(idx.read_bytes())
save('pre-installation.json',{'UTC':now(),'parent':BASE,'copies':copies,
     'public_baseline':base['public_files'],'protected_index_records':protected[0],
     'protected_index_records_SHA256':protected[1],'shared_index_SHA256_before':index_sha,
     'only_ten_target_index_records_may_change':True})
for row in copies:
    dest=Path(row['destination']);dest.parent.mkdir(parents=True,exist_ok=True)
    fd,temp=tempfile.mkstemp(prefix='.research-install-',dir=dest.parent)
    with os.fdopen(fd,'wb')as f:f.write(Path(row['source']).read_bytes())
    os.replace(temp,dest);bound(dest,row)
need({str(f.relative_to(public)) for f in public.rglob('*') if f.is_file()} ==
     {r['path'] for r in base['public_files']}|target,'exact593 union')
for row in base['public_files']:
    if row['path'] not in target:bound(public/row['path'],row)
need(len(list(f for f in public.rglob('*') if f.is_file()))==593,'593 installed public files')
need(sha(idx.read_bytes())==index_sha and protected_index()==protected,'shared index unchanged during copies')
fd,tempindex=tempfile.mkstemp(prefix='cellularization-tree-git-index-');os.close(fd);os.unlink(tempindex)
env=dict(os.environ,GIT_INDEX_FILE=tempindex,GIT_INDEX_VERSION='4')
try:
    git('read-tree',BASE,env=env);git('add','--',*gitpaths,env=env)
    changed=git('diff','--cached','--name-only',BASE,env=env).decode().splitlines()
    need(sorted(changed)==gitpaths,'exact ten-path staged commit')
    git('diff','--cached','--check',BASE,'--',*gitpaths,env=env)
    tree=git('write-tree',env=env).decode().strip()
    commit=git('commit-tree',tree,'-p',BASE,data=b'Publish cellularization and eleven-vertex tree research pages\n').decode().strip()
    need(sorted(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines())==gitpaths,
         'complete commit exact ten paths')
    need(git('rev-parse','HEAD').decode().strip()==BASE and sha(idx.read_bytes())==index_sha,
         'no concurrent checkout/index change')
    git('add','--',*gitpaths)
    need(protected_index()==protected,'all unrelated staged records unchanged')
    git('update-ref','refs/heads/master',commit,BASE)
    git('push','origin',commit+':refs/heads/master')
    need(git('ls-remote','origin','refs/heads/master').decode().split()[0]==commit,'remote actual commit')
    need(git('rev-parse','HEAD').decode().strip()==commit and protected_index()==protected,'final local/index preservation')
    for row in copies:bound(Path(row['destination']),row)
    receipt={'UTC':now(),'status':'PASS_EXACT10_INSTALL_COMMIT_PUSH','parent':BASE,'commit':commit,
             'tree':tree,'exact_committed_paths':gitpaths,'copies':copies,'public_files':593,
             'index_entries':87,'sitemap_locations':88,'unrelated_public_files_unchanged':583,
             'protected_index_records':protected[0],'protected_index_records_SHA256':protected[1],
             'unrelated_index_records_unchanged':True,'site_configurations_unchanged':True,
             'no_source_or_core_or_paper_config_edits':True,'deployed':False,'live_verified':False,
             'browser_verified':False,'native_sheet_publication_verified':False,'canonical_url':None,'AA':None}
    save('installation.json',receipt)
    print(json.dumps({k:v for k,v in receipt.items() if k not in ['copies','exact_committed_paths']},indent=2))
finally:
    for f in [Path(tempindex),Path(tempindex+'.lock')]:
        if f.exists():f.unlink()
