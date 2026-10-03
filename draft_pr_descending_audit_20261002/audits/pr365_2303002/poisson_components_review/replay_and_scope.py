"""Reproducible read-only candidate checks with private lossless captures.

Run from this review directory. Only its private/ and receipts/ files are
written. Git/index/refs and candidate snapshot are never changed.
"""
from pathlib import Path
import datetime, gzip, hashlib, json, os, re, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
REPO=Path('/Users/alec/Documents/Math')
SNAPSHOT=AUDIT/'snapshot'
TARGET='unsolved_math_prioritization/attempts/2303002'
HEAD='4245f1af53840a07f43c05c928c4783bc6c3a467'
BASE='efd29c05204703acca9a0860812f54b94fae54b1'
PRIVATE=ROOT/'private'
RECEIPTS=ROOT/'receipts'
ENV=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
records=[]

def sha(b): return hashlib.sha256(b).hexdigest()
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def capture(name, cmd, cwd=REPO, expected=None):
    start=utc()
    r=subprocess.run(cmd,cwd=cwd,env=ENV,capture_output=True)
    rec={'name':name,'started_utc':start,'completed_utc':utc(),
         'command':list(map(str,cmd)),'cwd':str(cwd),'exit':r.returncode,'streams':{}}
    for stream,b in [('stdout',r.stdout),('stderr',r.stderr)]:
        z=gzip.compress(b,compresslevel=9,mtime=0)
        path=PRIVATE/(name+'.'+stream+'.gz');path.write_bytes(z)
        rec['streams'][stream]={'path':str(path.relative_to(ROOT)),
           'logical_bytes':len(b),'logical_sha256':sha(b),
           'stored_bytes':len(z),'stored_sha256':sha(z)}
    if expected is not None:
        rec['whole_stdout_equals_expected']=r.stdout==expected
        rec['expected_bytes']=len(expected);rec['expected_sha256']=sha(expected)
    records.append(rec)
    (RECEIPTS/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
    if r.returncode!=0: raise AssertionError((name,'nonzero exit',r.returncode))
    if expected is not None and r.stdout!=expected:
        raise AssertionError((name,'whole stdout mismatch'))
    return r.stdout

def git(*args): return ['git','-c','core.fsmonitor=false',*args]

PRIVATE.mkdir(exist_ok=True);RECEIPTS.mkdir(exist_ok=True)
manifest=json.loads((AUDIT/'snapshot_manifest.json').read_text())
assert manifest['head']==HEAD and manifest['base']==BASE
assert len(manifest['files'])==19
frozen={f['path']:f for f in manifest['files']}
target_files={p:f for p,f in frozen.items() if p.startswith(TARGET+'/')}
assert len(target_files)==18
assert set(frozen)-set(target_files)=={'unsolved_math_prioritization/QUEUE.md'}
scope=[]
for p,f in frozen.items():
    b=(SNAPSHOT/p).read_bytes()
    assert len(b)==f['bytes'] and sha(b)==f['sha256'] and blob(b)==f['git_blob_sha']
    scope.append({'path':p,'bytes':len(b),'sha256':sha(b),'git_blob_sha':blob(b)})
branch=capture('branch',git('rev-parse','--abbrev-ref','HEAD')).decode().strip()
assert branch=='main',branch
remote=capture('remote',git('remote','get-url','origin')).decode().strip()
match=re.search(r'github\.com[:/]([^/]+/[^/]+?)(?:\.git)?$',remote)
assert match,remote
repository=match.group(1)
tree=capture('head_scope_tree',git('ls-tree','-rz',HEAD,'--',TARGET,'unsolved_math_prioritization/QUEUE.md'))
tree_rows={}
for entry in tree.split(b'\0'):
    if not entry: continue
    prefix,path=entry.split(b'\t',1);mode,typ,oid=prefix.decode().split()
    tree_rows[path.decode()]={'mode':mode,'type':typ,'git_blob_sha':oid}
assert set(tree_rows)==set(frozen)
for p in frozen:
    assert tree_rows[p]=={'mode':'100644','type':'blob','git_blob_sha':frozen[p]['git_blob_sha']}
delta=capture('head_base_delta',git('diff-tree','--no-commit-id','--name-status','-r',BASE,HEAD)).decode().splitlines()
delta_rows={line.split('\t',1)[1]:line.split('\t',1)[0] for line in delta}
assert set(delta_rows)==set(frozen)
assert delta_rows['unsolved_math_prioritization/QUEUE.md']=='M'
assert all(delta_rows[p]=='A' for p in target_files)
capture('base_ancestor',git('merge-base','--is-ancestor',BASE,HEAD))
history=capture('head_history',git('log','--format=fuller','--name-status',BASE+'..'+HEAD))
parents=capture('head_parents',git('show','-s','--format=%P',HEAD)).decode().split()
assert parents==[BASE,'a3ac55761d2301fbfe30e07a266da4a039cbfaba']
author_commit=parents[1]
capture('author_ancestor',git('merge-base','--is-ancestor',author_commit,HEAD))
author_tree=capture('author_tree',git('ls-tree','-rz',author_commit,'--',TARGET))
author_paths=[]
for entry in author_tree.split(b'\0'):
    if not entry: continue
    prefix,path=entry.split(b'\t',1);mode,typ,oid=prefix.decode().split()
    p=path.decode();assert p in target_files
    assert mode=='100644' and typ=='blob' and oid==target_files[p]['git_blob_sha']
    author_paths.append(p)
assert len(author_paths)==10
for i,p in enumerate(author_paths):
    assert capture('author_blob_'+str(i),git('show',author_commit+':'+p))==(SNAPSHOT/p).read_bytes()
for p in frozen:
    b=capture('head_blob_'+str(len(scope)),git('show',HEAD+':'+p))
    # Unique name overwritten below is avoided by using records length.
    assert b==(SNAPSHOT/p).read_bytes()
    scope.append({'verified_head_blob':p,'sha256':sha(b)})
queue_base=capture('queue_base',git('show',BASE+':unsolved_math_prioritization/QUEUE.md'))
queue_head=(SNAPSHOT/'unsolved_math_prioritization/QUEUE.md').read_bytes()
old=queue_base.decode().splitlines();new=queue_head.decode().splitlines()
assert len(old)==len(new)
differences=[{'line':i+1,'before':a,'after':b} for i,(a,b) in enumerate(zip(old,new)) if a!=b]
assert len(differences)==1
d=differences[0]
assert '2303002' in d['before'] and '2303002' in d['after']
before=d['before'].split('|');after=d['after'].split('|')
changed=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b]
assert len(changed)==1 and 'already_solved' in after[changed[0]]
assert '0/5' in d['before'] and '0/5' in d['after']
api_pr=json.loads(capture('api_pr',['gh','api','repos/'+repository+'/pulls/365']))
assert api_pr['head']['sha']==HEAD and api_pr['base']['sha']==BASE
assert api_pr['changed_files']==19 and api_pr['draft'] is True
api_files=json.loads(capture('api_files',['gh','api','repos/'+repository+'/pulls/365/files?per_page=100']))
assert len(api_files)==19 and {f['filename'] for f in api_files}==set(frozen)
for f in api_files:
    assert f['sha']==frozen[f['filename']]['git_blob_sha']
    assert f['status']==frozen[f['filename']]['status']

private_target=PRIVATE/'candidate'
private_target.mkdir(exist_ok=True)
for p in target_files:
    relative=Path(p).relative_to(TARGET);dest=private_target/relative
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((SNAPSHOT/p).read_bytes())
    assert dest.read_bytes()==(SNAPSHOT/p).read_bytes()
nested=[]
for name in ['FINAL_FROZEN_MANIFEST.json','PUBLICATION_MANIFEST.json']:
    doc=json.loads((private_target/name).read_text())
    for f in doc['files']:
        b=(private_target/f['path']).read_bytes()
        assert len(b)==f['bytes'] and sha(b)==f['sha256']
        nested.append({'manifest':name,'path':f['path'],'sha256':sha(b)})
pub=json.loads((private_target/'PUBLICATION_MANIFEST.json').read_text())
assert pub['author_manifest_sha256']==sha((private_target/'FINAL_FROZEN_MANIFEST.json').read_bytes())
assert pub['review_manifest_sha256']==sha((private_target/'final_review/REVIEW_MANIFEST.json').read_bytes())
for path,digest in json.loads((private_target/'final_review/REVIEW_MANIFEST.json').read_text()).items():
    assert sha((private_target/'final_review'/path).read_bytes())==digest
sources=PRIVATE/'sources';sources.mkdir(exist_ok=True)
for name in ['hayman_lingham_2018','carleson_1976']:
    (sources/(name+'.pdf')).write_bytes(gzip.decompress((PRIVATE/(name+'.pdf.gz')).read_bytes()))
capture('author_controls',[sys.executable,str(private_target/'verify_source_alignment.py')],cwd=private_target,
        expected=(private_target/'SOURCE_CHECKS.json').read_bytes())
expected_review=(private_target/'final_review/INDEPENDENT_CHECKS.json').read_bytes()
capture('review_math_only',[sys.executable,str(private_target/'final_review/run_portable.py'),'--math-only'],
        cwd=private_target,expected=expected_review.replace(b'1667',b'1665'))
capture('review_sources',[sys.executable,str(private_target/'final_review/run_portable.py'),'--sources',str(sources)],
        cwd=private_target,expected=expected_review)
controls=capture('poisson_controls',[sys.executable,str(ROOT/'check_poisson_controls.py')],cwd=ROOT)
for p in target_files:
    assert (private_target/Path(p).relative_to(TARGET)).read_bytes()==(SNAPSHOT/p).read_bytes()
for p,f in frozen.items():
    assert sha((SNAPSHOT/p).read_bytes())==f['sha256']
for p in sources.glob('*.pdf'):p.unlink()
report={'completed_utc':utc(),'head':HEAD,'base':BASE,'branch':branch,'repository':repository,
    'scope_files':19,'target_files':18,'snapshot_all_exact':True,'head_scope_tree':tree_rows,
    'changes':delta_rows,'queue_only_change':differences,'nested_checks':nested,
    'api_draft':api_pr['draft'],'api_state':api_pr['state'],'api_files_exact':True,
    'author_wip_commit':author_commit,'author_files_unchanged':author_paths,
    'whole_receipt_matches':3,'new_controls':json.loads(controls),
    'writes_only_review_subtree':True,'candidate_snapshot_unchanged_after':True}
(RECEIPTS/'execution_scope.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','scope_files':19,'target_files':18,
    'whole_receipt_matches':3,'new_exact_controls':report['new_controls']['exact_assertions'],
    'negative_controls_rejected':len(report['new_controls']['rejected_false_claims'])},indent=2))
