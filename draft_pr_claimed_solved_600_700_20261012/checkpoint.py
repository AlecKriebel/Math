#!/usr/bin/env python3
"""Publish only this shard onto remote main without touching shared files/index.

The shared checkout can remain behind remote main while other agents have dirty
files. This snapshots only the dedicated shard in a small temporary index,
preserves local main as an additional parent when needed, and uses a normal
(non-force) push. It never checks out, stashes, resets, or edits unrelated files.
"""
import argparse,datetime,hashlib,json,os,pathlib,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT.parent
SCOPE=ROOT.name

def run(*args, env=None):
 return subprocess.check_output(['git',*args],cwd=REPO,env=env,text=True).strip()

def index_identity():
 p=pathlib.Path(run('rev-parse','--git-path','index'))
 if not p.is_absolute():p=REPO/p
 return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None

def splice_scope(base, own_tree):
 # Forward every unrelated root entry byte-for-byte; Git sorts tree entries.
 entries=subprocess.check_output(['git','ls-tree','-z',base],cwd=REPO).split(b'\0')
 name=SCOPE.encode()
 kept=[entry for entry in entries if entry and entry.split(b'\t',1)[1]!=name]
 kept.append(b'040000 tree '+own_tree.encode()+b'\t'+name)
 data=b'\0'.join(kept)+b'\0'
 return subprocess.check_output(['git','mktree','-z'],cwd=REPO,input=data).decode().strip()

def checkpoint(message, *, push=True):
 if run('branch','--show-current')!='main':raise RuntimeError('main branch required')
 initial_index=index_identity()
 run('fetch','origin','main')
 remote=run('rev-parse','refs/remotes/origin/main');local=run('rev-parse','HEAD')
 with tempfile.TemporaryDirectory(prefix='math-pr600-700-index-') as td:
  env=os.environ.copy();env['GIT_INDEX_FILE']=str(pathlib.Path(td)/'index')
  run('read-tree','--empty',env=env)
  existing=subprocess.run(['git','cat-file','-e',remote+':'+SCOPE],cwd=REPO,stderr=subprocess.DEVNULL)
  if existing.returncode==0:run('read-tree','--prefix='+SCOPE+'/',remote+':'+SCOPE,env=env)
  run('add','-A','--',SCOPE,env=env)
  ignored=run('ls-files','-ci','--exclude-standard','--',SCOPE,env=env)
  if ignored:run('update-index','--force-remove','--',*ignored.splitlines(),env=env)
  scoped=run('write-tree',env=env)
  own_tree=run('rev-parse',scoped+':'+SCOPE)
  tree=splice_scope(remote,own_tree)
  changed=run('diff','--name-only',remote,tree)
  if not changed: return {'status':'no_change','remote_main':remote}
  if any(not x.startswith(SCOPE+'/') for x in changed.splitlines()):raise RuntimeError('scope violation')
  if run('rev-parse','HEAD')!=local or index_identity()!=initial_index or run('branch','--show-current')!='main':raise RuntimeError('shared checkout/index changed during preparation')
  args=['commit-tree',tree,'-p',remote]
  if subprocess.run(['git','merge-base','--is-ancestor',local,remote],cwd=REPO).returncode!=0:args+=['-p',local]
  commit=subprocess.check_output(['git',*args],cwd=REPO,input=message+'\n',text=True).strip()
  if push:subprocess.run(['git','push','origin',commit+':refs/heads/main'],cwd=REPO,check=True)
 return {'status':'pushed' if push else 'prepared_no_push','completion_estimate_percent':json.loads((ROOT/'PROGRAM_STATE.json').read_text()).get('completion_estimate_percent'),'commit':commit,'remote_parent':remote,'local_main':local,'changed_paths':changed.splitlines(),'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'shared_worktree_and_index_untouched':True,'temporary_index_scope':SCOPE}

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('message');parser.add_argument('--dry-run',action='store_true');args=parser.parse_args()
 receipt=checkpoint(args.message,push=not args.dry_run);print(json.dumps({k:v for k,v in receipt.items() if k!='changed_paths'} | {'changed_path_count':len(receipt.get('changed_paths',[]))},indent=2))
 (ROOT/('CHECKPOINT_PREPARED_RECEIPT.json' if args.dry_run else 'LATEST_PUSH_RECEIPT.json')).write_text(json.dumps(receipt,indent=2)+'\n')
