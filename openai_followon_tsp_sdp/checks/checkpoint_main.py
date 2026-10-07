#!/usr/bin/env python3
"""Publish this effort's tree onto remote main without changing shared HEAD/index."""
import argparse,datetime,hashlib,json,os,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent

def run(args,env=None):
    return subprocess.run(['git','-c','gc.auto=0',*args],cwd=REPO,env=env,text=True,capture_output=True,check=True).stdout.strip()

def main():
    p=argparse.ArgumentParser();p.add_argument('message');p.add_argument('--receipt',required=True);args=p.parse_args()
    before_head=run(['rev-parse','HEAD']);index=REPO/'.git/index'
    before_index=hashlib.sha256(index.read_bytes()).hexdigest() if index.exists() else None
    attempts=[]
    for attempt in range(4):
        base=run(['ls-remote','origin','refs/heads/main']).split()[0]
        run(['fetch','--no-tags','origin',base])
        tmp=ROOT/f'.git-checkpoint-index-{os.getpid()}'
        env=os.environ.copy();env['GIT_INDEX_FILE']=str(tmp)
        try:
            # Build a small project-only tree and retain every other remote entry.
            run(['read-tree','--empty'],env)
            run(['add','--',ROOT.name],env)
            scoped=run(['write-tree'],env)
            project_entry=subprocess.check_output(['git','ls-tree','-z',scoped,'--',ROOT.name],cwd=REPO)
            assert project_entry and project_entry.count(b'\0')==1
            entries=subprocess.check_output(['git','ls-tree','-z',base+'^{tree}'],cwd=REPO).split(b'\0')
            owned_name=ROOT.name.encode()
            retained=[entry for entry in entries if entry and entry.split(b'\t',1)[1]!=owned_name]
            tree=subprocess.check_output(['git','mktree','-z'],cwd=REPO,input=b'\0'.join(retained)+b'\0'+project_entry).decode().strip()
            commit=run(['commit-tree',tree,'-p',base,'-m',args.message],env)
            changed=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','-z',base,commit],cwd=REPO).split(b'\0')
            assert all(not name or name.startswith(owned_name+b'/') for name in changed)
            push=subprocess.run(['git','push','origin',f'{commit}:refs/heads/main'],cwd=REPO,text=True,capture_output=True)
            attempts.append({'base':base,'commit':commit,'returncode':push.returncode,'output':push.stdout+push.stderr})
            if push.returncode==0:break
            if not any(x in push.stderr for x in ['fetch first','non-fast-forward','failed to push']):raise RuntimeError(push.stderr)
        finally:
            tmp.unlink(missing_ok=True);Path(str(tmp)+'.lock').unlink(missing_ok=True)
    else:raise RuntimeError('Concurrent updates prevented four non-force pushes')
    remote=run(['ls-remote','origin','refs/heads/main']).split()[0]
    run(['fetch','--no-tags','origin',remote])
    contained=subprocess.run(['git','merge-base','--is-ancestor',commit,remote],cwd=REPO).returncode==0
    after_head=run(['rev-parse','HEAD']);after_index=hashlib.sha256(index.read_bytes()).hexdigest() if index.exists() else None
    result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'published_commit':commit,'remote_main':remote,'commit_is_remote_ancestor':contained,'shared_HEAD_before':before_head,'shared_HEAD_after':after_head,'shared_index_sha256_before':before_index,'shared_index_sha256_after':after_index,'attempts':attempts}
    (ROOT/args.receipt).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert contained,'Pushed commit no longer belongs to remote main'
    assert before_head==after_head,'Shared HEAD changed during publication; investigate independent concurrent operation'
    # Index hash is observational: concurrent researchers may legitimately change their own index.

if __name__=='__main__':main()
