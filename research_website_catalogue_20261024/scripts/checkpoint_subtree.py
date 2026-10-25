"""Checkpoint only this programme's subtree without a repository-wide index.
All sibling root entries, the shared index, local HEAD and branch stay unchanged.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys, tempfile
PROGRAM=Path(__file__).resolve().parents[1]
REPO=PROGRAM.parent

def git(*args, env=None, data=None):
    r=subprocess.run(['git','-c','gc.auto=0',*args],cwd=REPO,env=env,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if r.returncode:
        raise RuntimeError(r.stderr.decode('utf-8','replace')[-3000:])
    return r.stdout

def value(*args, env=None):
    return git(*args,env=env).decode().strip()

def digest_file(p):
    h=hashlib.sha256()
    with p.open('rb')as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def entries(tree):
    return {r.split(b'\t',1)[1]:r for r in git('ls-tree','-z',tree).split(b'\0')if r}

branch=value('branch','--show-current');local_head=value('rev-parse','HEAD')
if branch!='main':raise RuntimeError('Expected existing main branch')
shared_index=Path(value('rev-parse','--git-path','index'))
if not shared_index.is_absolute():shared_index=REPO/shared_index
shared_sha=digest_file(shared_index)
git('fetch','origin','main');parent=value('rev-parse','origin/main')
parent_entries=entries(parent);key=PROGRAM.name.encode()
if key not in parent_entries or not parent_entries[key].startswith(b'040000 tree '):raise RuntimeError('Missing programme parent subtree')
fd,index=tempfile.mkstemp(prefix='research-catalogue-subtree-index-')
os.close(fd);os.unlink(index)
env=dict(os.environ,GIT_INDEX_FILE=index,GIT_INDEX_VERSION='4')
dry='--dry-run'in sys.argv
try:
    git('read-tree','--empty',env=env)
    git('read-tree','--prefix='+PROGRAM.name+'/',parent+':'+PROGRAM.name,env=env)
    git('add','--',PROGRAM.name+'/',env=env)
    files=value('diff','--cached','--no-renames','--name-only',parent,'--',PROGRAM.name+'/',env=env).splitlines()
    if not files:
        print('No new programme changes');raise SystemExit(0)
    if not all(p.startswith(PROGRAM.name+'/')for p in files):raise RuntimeError('Scope escape')
    git('-c','core.whitespace=-blank-at-eol,-blank-at-eof','diff','--cached','--check',parent,'--',PROGRAM.name+'/',
        ':!'+PROGRAM.name+'/papers/*/sources/published-source/**',
        ':!'+PROGRAM.name+'/papers/*/sources/related-records/*/published-source/**',
        ':!'+PROGRAM.name+'/papers/*/reviews/*/primary-imports/*.tex',
        ':!'+PROGRAM.name+'/papers/*/reviews/*/replay-work/**',
        ':!'+PROGRAM.name+'/papers/*/reviews/**/*.log',
        ':!'+PROGRAM.name+'/papers/*/reviews/**/*.stderr',
        ':!'+PROGRAM.name+'/papers/*/reviews/**/*.stdout',
        ':!'+PROGRAM.name+'/papers/*/reviews/**/*.download',
        ':!'+PROGRAM.name+'/papers/*/reviews/**/*.txt',env=env)
    isolated_root=value('write-tree',env=env)
    isolated_entries=entries(isolated_root)
    if set(isolated_entries)!={key}:raise RuntimeError('Unexpected isolated root')
    root_entries=dict(parent_entries);root_entries[key]=isolated_entries[key]
    tree=git('mktree','-z',data=b'\0'.join(root_entries.values())+b'\0').decode().strip()
    actual_entries=entries(tree)
    if actual_entries!=root_entries:raise RuntimeError('Root tree composition differs')
    if {k:v for k,v in actual_entries.items()if k!=key}!={k:v for k,v in parent_entries.items()if k!=key}:raise RuntimeError('Sibling tree modified')
    actual_files=value('diff-tree','-r','--no-commit-id','--no-renames','--name-only',parent,tree).splitlines()
    if sorted(actual_files)!=sorted(files):raise RuntimeError('Full-tree changes differ from scoped changes')
    if digest_file(shared_index)!=shared_sha or value('rev-parse','HEAD')!=local_head or value('branch','--show-current')!=branch:raise RuntimeError('Shared checkout changed')
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'parent':parent,'tree':tree,'files':len(files),'scope':PROGRAM.name,'strategy':'programme-only version4 isolated index plus exact sibling-preserving parent-root composition','temporary_index_bytes':Path(index).stat().st_size,'sibling_root_entries_preserved':len(parent_entries)-1,'shared_index_sha256_before_and_after':shared_sha,'local_branch_and_shared_index_unchanged':True,'dry_run':dry}
    if dry:
        (PROGRAM/'verification/checkpoint-subtree-dry-run-20261025.json').write_text(json.dumps(receipt,indent=2)+'\n')
    else:
        message=next((x for x in sys.argv[1:]if x!='--dry-run'),'Checkpoint Zenodo research website catalogue')
        commit=git('commit-tree',tree,'-p',parent,data=(message+'\n').encode()).decode().strip()
        git('push','origin',commit+':refs/heads/main')
        if value('ls-remote','origin','refs/heads/main').split()[0]!=commit:raise RuntimeError('Remote commit mismatch')
        if digest_file(shared_index)!=shared_sha or value('rev-parse','HEAD')!=local_head or value('branch','--show-current')!=branch:raise RuntimeError('Shared checkout changed after push')
        receipt['commit']=commit
        (PROGRAM/'verification/PUSH_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))
finally:
    for p in [Path(index),Path(index+'.lock')]:
        if p.exists():p.unlink()
