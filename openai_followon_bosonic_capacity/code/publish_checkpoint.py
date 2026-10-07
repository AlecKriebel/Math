"""Publish only this effort's owned files using an isolated index on remote main.
Never updates the shared index, HEAD, branch, worktree, or source clone.
Non-force pushes only; rejects project-path conflicts since last checkpoint.
"""
from pathlib import Path
import argparse, json, os, subprocess, tempfile, datetime
ROOT=Path(__file__).resolve().parents[2]
PROJECT=Path(__file__).resolve().parents[1]
REL=PROJECT.relative_to(ROOT).as_posix()
def run(*args, env=None, **kwargs):
    return subprocess.check_output(['git', *args], cwd=ROOT, env=env, **kwargs).decode().strip()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('message'); a=ap.parse_args()
    branch=run('branch','--show-current')
    if branch!='main': raise RuntimeError('Shared checkout must remain main')
    base=run('ls-remote','origin','refs/heads/main').split()[0]
    subprocess.run(['git','fetch','--no-write-fetch-head','origin',base],cwd=ROOT,check=True)
    last=PROJECT/'checkpoints'/'LAST_PUBLISHED.json'
    if last.exists():
        old=json.loads(last.read_text())['commit']
        changed=run('diff','--name-only',old,base,'--',REL)
        if changed: raise RuntimeError('Concurrent remote changes in owned effort: '+changed)
    with tempfile.TemporaryDirectory(dir=PROJECT/'checkpoints',prefix='index-') as tmp:
        env=os.environ.copy(); env['GIT_INDEX_FILE']=str(Path(tmp)/'index')
        run('read-tree',base,env=env)
        run('add','--',REL,env=env)
        # Never publish caches, raw third-party source downloads, or temporary indexes.
        staged_paths=run('ls-files',env=env).splitlines()
        excluded=[f for f in staged_paths if f.startswith(REL+'/') and ('/pinned_build/' in f or '/.lake/' in f or '/checkpoints/index-' in f or ('/notes/' in f and '/sources/' in f) or (f.startswith(REL+'/sources/') and f.endswith(('.pdf','.txt','.tar','.gz'))))]
        if excluded: run('rm','--cached','--ignore-unmatch','--',*excluded,env=env)
        owned=run('diff','--cached','--name-only',base,env=env).splitlines()
        if not owned: print('No new owned files'); return
        if any(not f.startswith(REL+'/') for f in owned): raise RuntimeError('Unowned path staged')
        tree=run('write-tree',env=env)
        commit=run('commit-tree',tree,'-p',base,'-m',a.message)
        subprocess.run(['git','push','origin',commit+':refs/heads/main'],cwd=ROOT,check=True)
        remote=run('ls-remote','origin','refs/heads/main').split()[0]
        if remote!=commit: raise RuntimeError('Remote advanced after push; inspect commit reachability')
        receipt={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':base,'commit':commit,'owned_paths':owned,'mode':'isolated-index non-force remote-main checkpoint','shared_checkout_untouched':True}
        last.write_text(json.dumps(receipt,indent=2)+'\n')
        (PROJECT/'checkpoints'/('push-'+commit[:12]+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps(receipt,indent=2))
if __name__=='__main__': main()
