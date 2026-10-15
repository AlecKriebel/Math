#!/usr/bin/env python3
"""Publish owned paths on remote main without changing shared HEAD/index/worktree."""
import os,subprocess,tempfile,json,datetime,sys
from pathlib import Path
repo=Path('/Users/alec/Documents/Math')
project=repo/'openai_followon_commuting_ergodic_hilbert'
message=sys.argv[1]
def git(*args,env=None):
 return subprocess.check_output(['git',*args],cwd=repo,env=env,text=True).strip()
assert git('branch','--show-current')=='main'
head_before=git('rev-parse','HEAD')
index_path=repo/git('rev-parse','--git-path','index')
import hashlib
index_before=hashlib.sha256(index_path.read_bytes()).hexdigest()
git('fetch','--no-tags','origin','main')
parent=git('rev-parse','FETCH_HEAD')
with tempfile.TemporaryDirectory(dir=project/'receipts',prefix='temporary_index_') as tmp:
 env=dict(os.environ,GIT_INDEX_FILE=str(Path(tmp)/'index'))
 git('read-tree',parent,env=env)
 git('add','--','openai_followon_commuting_ergodic_hilbert',env=env)
 tree=git('write-tree',env=env)
 commit=git('commit-tree',tree,'-p',parent,'-m',message)
 changed=git('diff-tree','--no-commit-id','--name-only','-r',commit).splitlines()
 assert changed and all(x.startswith('openai_followon_commuting_ergodic_hilbert/') for x in changed)
 git('push','origin',commit+':refs/heads/main')
assert git('rev-parse','HEAD')==head_before
assert hashlib.sha256(index_path.read_bytes()).hexdigest()==index_before
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':commit,'parent':parent,'changed_paths':changed,'shared_HEAD_preserved':head_before,'shared_index_sha256_preserved':index_before,'push':'confirmed'}
path=project/'receipts'/('checkpoint_'+commit[:10]+'.json')
path.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
