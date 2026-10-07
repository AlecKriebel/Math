#!/usr/bin/env python3
"""Publish owned, explicitly listed paths on remote main without changing shared state."""
import argparse, hashlib, json, os, pathlib, subprocess, tempfile
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=pathlib.Path('/Users/alec/Documents/Math')
PROJECT=ROOT/'openai_followon_k3_moduli_hodge'

def git(*args, env=None, data=None):
    return subprocess.check_output(['git',*args],cwd=ROOT,env=env,input=data,text=True).strip()

def fingerprint(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None

p=argparse.ArgumentParser(); p.add_argument('--message',required=True); p.add_argument('paths',nargs='+'); args=p.parse_args()
paths=[]
for name in args.paths:
    f=(ROOT/name).resolve()
    if not f.is_relative_to(PROJECT) or not f.is_file(): raise SystemExit(f'Not an owned file: {name}')
    paths.append(f)
index=pathlib.Path(git('rev-parse','--git-path','index')); index=index if index.is_absolute() else ROOT/index
initial_index=fingerprint(index); initial_head=git('rev-parse','HEAD')
base=git('ls-remote','origin','refs/heads/main').split()[0]
subprocess.run(['git','fetch','--no-write-fetch-head','origin',base],cwd=ROOT,check=True,capture_output=True,text=True)
with tempfile.TemporaryDirectory(prefix='owned-git-',dir=PROJECT/'checks') as td:
    env=os.environ.copy(); env['GIT_INDEX_FILE']=str(pathlib.Path(td)/'index')
    git('read-tree',base,env=env)
    git('add','--',*[str(f.relative_to(ROOT)) for f in paths],env=env)
    staged=git('diff','--cached','--name-only',base,env=env).splitlines()
    if set(staged)-{str(f.relative_to(ROOT)) for f in paths}: raise SystemExit('Unexpected path staged')
    tree=git('write-tree',env=env)
    commit=git('commit-tree',tree,'-p',base,data=args.message+'\n')
    expected={str(f.relative_to(ROOT)):fingerprint(f) for f in paths}
    for rel,sha in expected.items():
        raw=subprocess.check_output(['git','show',f'{commit}:{rel}'],cwd=ROOT)
        if hashlib.sha256(raw).hexdigest()!=sha: raise SystemExit(f'Concurrent owned-file change: {rel}')
    subprocess.run(['git','push','origin',f'{commit}:refs/heads/main'],cwd=ROOT,check=True)
    remote=git('ls-remote','origin','refs/heads/main').split()[0]
    if remote!=commit:
        subprocess.run(['git','fetch','--no-write-fetch-head','origin',remote],cwd=ROOT,check=True,capture_output=True,text=True)
        subprocess.run(['git','merge-base','--is-ancestor',commit,remote],cwd=ROOT,check=True)
    if fingerprint(index)!=initial_index: raise SystemExit('Shared index changed concurrently; inspect, do not reset')
    if git('rev-parse','HEAD')!=initial_head: raise SystemExit('Shared HEAD changed concurrently; inspect, do not reset')
    receipt={'timestamp':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),'parent_remote_main':base,'commit':commit,'verified_remote_main':remote,'shared_head_preserved':initial_head,'shared_index_sha256':initial_index,'owned_files_sha256':expected,'github_commit':f'https://github.com/AlecKriebel/Math/commit/{commit}'}
    out=PROJECT/'publication'/f'checkpoint-{commit[:12]}.json';out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'receipt':str(out),'commit':commit,'remote':remote,'files':len(paths)},indent=2))
