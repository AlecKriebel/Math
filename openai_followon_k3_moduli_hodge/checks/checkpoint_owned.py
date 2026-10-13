#!/usr/bin/env python3
"""Publish explicit owned paths on remote main, preserving shared index and HEAD.
Only index this project's subtree, so a large shared repository needs no
second full-tree index. Reattach the subtree to the unchanged remote root.
"""
import argparse, hashlib, json, os, pathlib, subprocess, tempfile
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=pathlib.Path('/Users/alec/Documents/Math')
PROJECT=ROOT/'openai_followon_k3_moduli_hodge'

def git(*args, env=None, data=None, cwd=ROOT):
    return subprocess.check_output(['git',*args],cwd=cwd,env=env,input=data,text=True).strip()

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
root_entries=subprocess.check_output(['git','ls-tree','-z',base],cwd=ROOT).split(b'\0')
project_name=PROJECT.name.encode()
old_subtree=None
for entry in root_entries:
    if not entry: continue
    header,name=entry.split(b'\t',1)
    if name==project_name:
        mode,kind,oid=header.split()
        if mode!=b'040000' or kind!=b'tree': raise SystemExit('Project remote path is not a tree')
        old_subtree=oid.decode()
with tempfile.TemporaryDirectory(prefix='owned-git-',dir=PROJECT/'checks') as td:
    env=os.environ.copy(); env['GIT_INDEX_FILE']=str(pathlib.Path(td)/'index')
    env['GIT_WORK_TREE']=str(PROJECT); env['GIT_DIR']=git('rev-parse','--absolute-git-dir')
    git('read-tree',old_subtree,env=env,cwd=PROJECT) if old_subtree else git('read-tree','--empty',env=env,cwd=PROJECT)
    relatives=[str(f.relative_to(PROJECT)) for f in paths]
    git('add','--',*relatives,env=env,cwd=PROJECT)
    diff_args=['diff','--cached','--name-only']+([old_subtree] if old_subtree else [])
    staged=git(*diff_args,env=env,cwd=PROJECT).splitlines()
    if set(staged)-set(relatives): raise SystemExit('Unexpected path staged')
    subtree=git('write-tree',env=env,cwd=PROJECT)
    new_entries=[]
    for entry in root_entries:
        if not entry: continue
        header,name=entry.split(b'\t',1)
        if name==project_name: entry=b'040000 tree '+subtree.encode()+b'\t'+name
        new_entries.append(entry)
    if old_subtree is None: new_entries.append(b'040000 tree '+subtree.encode()+b'\t'+project_name)
    root_data=b'\0'.join(new_entries)+b'\0'
    tree=subprocess.check_output(['git','mktree','-z'],cwd=ROOT,input=root_data).decode().strip()
    # Independently ensure every root entry outside this project is unchanged.
    def outside(raw):
        return {entry.split(b'\t',1)[1]:entry.split(b'\t',1)[0] for entry in raw if entry and entry.split(b'\t',1)[1]!=project_name}
    actual_entries=subprocess.check_output(['git','ls-tree','-z',tree],cwd=ROOT).split(b'\0')
    if outside(actual_entries)!=outside(root_entries): raise SystemExit('Unrelated remote tree changed')
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
    receipt={'timestamp':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),'parent_remote_main':base,'commit':commit,'verified_remote_main':remote,'shared_head_preserved':initial_head,'shared_index_sha256':initial_index,'unrelated_remote_root_entries_preserved':True,'index_scope':'owned project subtree','owned_files_sha256':expected,'github_commit':f'https://github.com/AlecKriebel/Math/commit/{commit}'}
    out=PROJECT/'publication'/f'checkpoint-{commit[:12]}.json';out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'receipt':str(out),'commit':commit,'remote':remote,'files':len(paths)},indent=2))
