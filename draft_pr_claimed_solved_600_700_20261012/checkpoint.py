#!/usr/bin/env python3
"""Publish only this shard onto remote main without touching shared files/index.

The shared checkout can remain behind remote main while other agents have dirty
files. This snapshots the dedicated shard with a temporary index on remote main,
preserves local main as an additional parent when needed, and uses a normal
(non-force) push. It never checks out, stashes, resets, or edits unrelated files.
"""
import datetime,json,os,pathlib,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT.parent
SCOPE=ROOT.name

def run(*args, env=None):
 return subprocess.check_output(['git',*args],cwd=REPO,env=env,text=True).strip()

def checkpoint(message):
 if run('branch','--show-current')!='main':raise RuntimeError('main branch required')
 run('fetch','origin','main')
 remote=run('rev-parse','refs/remotes/origin/main');local=run('rev-parse','HEAD')
 with tempfile.TemporaryDirectory(prefix='math-pr600-700-index-') as td:
  env=os.environ.copy();env['GIT_INDEX_FILE']=str(pathlib.Path(td)/'index')
  run('read-tree',remote,env=env)
  run('add','-A','--',SCOPE,env=env)
  tree=run('write-tree',env=env)
  changed=run('diff','--name-only',remote,tree)
  if not changed: return {'status':'no_change','remote_main':remote}
  if any(not x.startswith(SCOPE+'/') for x in changed.splitlines()):raise RuntimeError('scope violation')
  args=['commit-tree',tree,'-p',remote]
  if subprocess.run(['git','merge-base','--is-ancestor',local,remote],cwd=REPO).returncode!=0:args+=['-p',local]
  commit=subprocess.check_output(['git',*args],cwd=REPO,input=message+'\n',text=True).strip()
  subprocess.run(['git','push','origin',commit+':refs/heads/main'],cwd=REPO,check=True)
 return {'status':'pushed','commit':commit,'remote_parent':remote,'local_main':local,'changed_paths':changed.splitlines(),'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'shared_worktree_and_index_untouched':True}

if __name__=='__main__':
 receipt=checkpoint(sys.argv[1]);print(json.dumps(receipt,indent=2))
 (ROOT/'LATEST_PUSH_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
