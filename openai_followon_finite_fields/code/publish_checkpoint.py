#!/usr/bin/env python3
"""Push only an explicit owned-file list atop current remote main without touching shared index or checkout."""
import argparse, datetime, hashlib, json, os, pathlib, subprocess, tempfile
ROOT=pathlib.Path(__file__).resolve().parents[2]
PROJECT='openai_followon_finite_fields'
def run(args, env=None):
    return subprocess.check_output(['git',*args],cwd=ROOT,env=env,text=True).strip()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--message',required=True);ap.add_argument('--receipt',required=True);ap.add_argument('files',nargs='+');a=ap.parse_args()
    if run(['branch','--show-current'])!='main':raise SystemExit('Shared checkout is not on main; refusing.')
    files=[]
    for x in a.files:
        p=pathlib.PurePosixPath(x)
        if p.is_absolute() or '..' in p.parts or p.parts[0]!=PROJECT:raise SystemExit('Only explicit owned project files allowed')
        if not (ROOT/p).is_file():raise SystemExit('Not a regular existing file: '+x)
        files.append(x)
    before_head=run(['rev-parse','HEAD'])
    shared_index=pathlib.Path(run(['rev-parse','--git-path','index']))
    if not shared_index.is_absolute():shared_index=ROOT/shared_index
    before_index=hashlib.sha256(shared_index.read_bytes()).hexdigest()
    hashes={x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in files}
    for attempt in range(4):
        remote=run(['ls-remote','origin','refs/heads/main']).split()[0]
        subprocess.run(['git','fetch','--no-tags','--no-write-fetch-head','origin',remote],cwd=ROOT,check=True,capture_output=True,text=True)
        with tempfile.TemporaryDirectory(prefix='private_index_',dir=ROOT/PROJECT/'receipts') as tmp:
            env=os.environ.copy();env['GIT_INDEX_FILE']=str(pathlib.Path(tmp)/'index')
            run(['read-tree',remote],env);run(['add','--',*files],env)
            tree=run(['write-tree'],env)
            if tree==run(['rev-parse',remote+'^{tree}']):raise SystemExit('No owned changes to publish')
            staged=run(['diff-tree','--no-commit-id','--name-only','-r',remote,tree])
            if set(staged.splitlines())-set(files):raise SystemExit('Unexpected path in tree diff')
            commit=run(['commit-tree',tree,'-p',remote,'-m',a.message],env)
        result=subprocess.run(['git','push','origin',commit+':refs/heads/main'],cwd=ROOT,capture_output=True,text=True)
        if result.returncode==0:
            observed=run(['ls-remote','origin','refs/heads/main']).split()[0]
            ancestor=subprocess.run(['git','merge-base','--is-ancestor',commit,observed],cwd=ROOT,capture_output=True)
            if observed!=commit and ancestor.returncode!=0:raise SystemExit('Remote receipt does not prove commit presence')
            after_index=hashlib.sha256(shared_index.read_bytes()).hexdigest()
            receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent':remote,'commit':commit,'remote_main_observed':observed,'files':hashes,'shared_head_before':before_head,'shared_head_after':run(['rev-parse','HEAD']),'shared_index_sha256_before':before_index,'shared_index_sha256_after':after_index,'shared_index_unchanged_during_window':before_index==after_index,'push_output':result.stdout+result.stderr}
            (ROOT/a.receipt).write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2));return
        if 'fetch first' not in result.stderr and 'non-fast-forward' not in result.stderr and 'failed to update ref' not in result.stderr:raise SystemExit(result.stderr)
    raise SystemExit('Remote main moved repeatedly; no force push attempted')
if __name__=='__main__':main()
