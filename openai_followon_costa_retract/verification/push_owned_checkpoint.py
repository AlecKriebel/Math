#!/usr/bin/env python3
"""Publish only this project's snapshot to remote main, preserving shared HEAD/index.
No branches, resets, checkouts, force pushes, or shared-index writes.
"""
from pathlib import Path
import subprocess,os,tempfile,json,datetime,argparse
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent
PREFIX=ROOT.name

def run(args, *, env=None, data=None, check=True):
    return subprocess.run(['git',*args],cwd=REPO,env=env,input=data,text=True,capture_output=True,check=check)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('message');ap.add_argument('--receipt',required=True)
    a=ap.parse_args()
    if run(['branch','--show-current']).stdout.strip()!='main': raise RuntimeError('Shared branch must be main')
    parent=run(['ls-remote','origin','refs/heads/main']).stdout.split()[0]
    if run(['cat-file','-e',parent],check=False).returncode:
        run(['fetch','--no-write-fetch-head','origin',parent])
    # The temporary index is private, and starts from the current remote tree.
    with tempfile.TemporaryDirectory(dir=ROOT/'verification',prefix='checkpoint-index-') as td:
        env=dict(os.environ,GIT_INDEX_FILE=str(Path(td)/'index'))
        run(['read-tree',parent],env=env)
        run(['add','--',PREFIX],env=env)
        # Explicitly remove locally retained but ignored source copies and scratch artifacts
        # from this snapshot, including those already tracked in a prior remote tree.
        tracked=run(['ls-files','--',PREFIX],env=env).stdout.splitlines()
        ignored=[p for p in tracked if run(['check-ignore','--no-index','-q',p],env=env,check=False).returncode==0]
        if ignored: run(['rm','--cached','--ignore-unmatch','--',*ignored],env=env)
        changed=run(['diff','--cached','--name-only',parent],env=env).stdout.splitlines()
        if not changed: raise RuntimeError('No new project changes')
        if any(not p.startswith(PREFIX+'/') for p in changed): raise RuntimeError('Out of scope path')
        tree=run(['write-tree'],env=env).stdout.strip()
        commit=run(['commit-tree',tree,'-p',parent],env=env,data=a.message+'\n').stdout.strip()
        # Normal fast-forward push; a concurrent remote change makes this fail safely.
        pushed=run(['push','origin',commit+':refs/heads/main'],check=False)
        remote=run(['ls-remote','origin','refs/heads/main']).stdout.split()[0]
        receipt={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent':parent,'commit':commit,'tree':tree,'owned_paths':changed,'push_exit':pushed.returncode,'push_output':pushed.stdout+pushed.stderr,'remote_main_readback':remote,'shared_index_touched':False,'shared_head_touched':False}
        Path(a.receipt).write_text(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps(receipt,indent=2))
        if pushed.returncode: raise RuntimeError('Push rejected; reconcile remote and retry snapshot')
        if remote!=commit and run(['merge-base','--is-ancestor',commit,remote],check=False).returncode: raise RuntimeError('Push read-back does not retain commit')
if __name__=='__main__': main()
