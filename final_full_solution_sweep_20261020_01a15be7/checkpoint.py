#!/usr/bin/env python3
"""Publish only this sweep's explicit checkpoint paths onto live main.

Uses a private index and Git plumbing; never checks out, stages in the shared
index, resets, stashes, cleans, creates a branch, or force-pushes. A concurrent
main advance causes a normal push rejection and a safe retry from the new main.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import uuid
from urllib.parse import urlparse
from sweep_io import atomic_json

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent
PRIVATE=ROOT/'private'
NAMES=['.gitignore','README.md','RESEARCH_LOG.md','STATE.json',
       'collect_inventory.py','collect_rest_inventory.py',
       'collect_eligibility_evidence.py','checkpoint.py','sweep_io.py',
       'rest_inventory.json','REST_INVENTORY_RECEIPT.json',
       'PR0009_PENDING.json','PR0009_DISPOSITION.json',
       'PR0009_PUBLICATION_LEAD_VERIFICATION.json','dispositions.jsonl',
       'CLASSIFICATION_POLICY.md','INCIDENT_RECOVERY.json','advance_clear_exclusions.py',
       'reviews/early_classification_adversary/REVIEW.md',
       'reviews/early_classification_adversary/check_results.json',
       'reviews/early_classification_adversary/GWS_GENERATION_INCIDENT.json',
       'audits/pr0097_10300055/SOURCE_SNAPSHOT.json',
       'audits/pr0097_10300055/CORRECTED_SNAPSHOT.json',
       'audits/pr0097_10300055/DUPLICATE_CHECK.json',
       'audits/pr0097_10300055/ROOT_ORIGINAL_REPRODUCTION.json',
       'audits/pr0097_10300055/ROOT_CORRECTED_REPRODUCTION.json',
       'audits/pr0097_10300055/reviews/math_audit/REVIEW.md',
       'audits/pr0097_10300055/reviews/math_audit/independent_falsification.py',
       'audits/pr0097_10300055/reviews/priority_audit/REVIEW.md',
       'audits/pr0097_10300055/reviews/priority_audit/VERDICT.json']
DESTINATION='https://github.com/AlecKriebel/Math.git'
TRANSPORT_REMOTE='origin'
TRANSPORT=['git','-c','remote.'+TRANSPORT_REMOTE+'.url='+DESTINATION,
           '-c','remote.'+TRANSPORT_REMOTE+'.pushurl='+DESTINATION]


def run(args,*,env=None,input=None,check=True):
    p=subprocess.run(args,cwd=REPO,env=env,input=input,capture_output=True)
    if check and p.returncode:
        raise RuntimeError(p.stderr.decode(errors='replace')[:2000])
    return p


def live_main():
    p=run(['gh','api','repos/AlecKriebel/Math/git/ref/heads/main'])
    return json.loads(p.stdout)['object']['sha']


def verify_destination():
    urls=run(TRANSPORT+['remote','get-url','--push','--all',TRANSPORT_REMOTE]).stdout.decode().splitlines()
    fetch_urls=run(TRANSPORT+['remote','get-url','--all',TRANSPORT_REMOTE]).stdout.decode().splitlines()
    def intended(url):
        if url.startswith('git@github.com:'):
            return url[len('git@github.com:'):].removesuffix('.git').lower()=='aleckriebel/math'
        parsed=urlparse(url)
        return (parsed.scheme=='https' and parsed.hostname=='github.com'
                and not parsed.username and not parsed.password and not parsed.query
                and not parsed.fragment and parsed.path.rstrip('/').removesuffix('.git').lower()=='/aleckriebel/math')
    if len(urls)!=1 or not fetch_urls or not all(intended(url) for url in urls+fetch_urls):
        raise RuntimeError('Effective push destination does not match the intended repository; no push attempted')
    return urls[0]


def ensure_commit(sha):
    p=run(['git','cat-file','-e',sha+'^{commit}'],check=False)
    if p.returncode:
        verify_destination()
        run(TRANSPORT+['fetch','--no-tags','--no-write-fetch-head',TRANSPORT_REMOTE,sha])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--message',default='Checkpoint exhaustive final-sweep inventory and ledger-access blocker')
    args=parser.parse_args()
    destination=verify_destination()
    selected=[]
    # Named per-PR receipts are authored only in this dedicated effort folder.
    # This is a filename whitelist, not a shared-worktree git add or broad glob.
    receipt_names=sorted(p.name for p in ROOT.iterdir()
                         if re.fullmatch(r'PR\d{4}_(?:DISPOSITION|PUBLICATION_VERIFICATION)\.json',p.name))
    for name in dict.fromkeys(NAMES+receipt_names):
        path=ROOT/name
        relative=Path(name)
        parts=[ROOT.joinpath(*relative.parts[:n]) for n in range(1,len(relative.parts)+1)]
        if (relative.is_absolute() or '..' in relative.parts
                or any(part.is_symlink() for part in parts)
                or not path.is_file() or not path.resolve().is_relative_to(ROOT.resolve())):
            raise RuntimeError(f'Unsafe or absent checkpoint path: {name}')
        selected.append((str(path.relative_to(REPO)),path.read_bytes()))
    parent=live_main()
    receipt={'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),
             'remote_main_parent':parent,'execute':args.execute,
             'files':[{'path':p,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for p,b in selected],
             'completion_estimate_percent':json.loads((ROOT/'STATE.json').read_text())['completion_estimate_percent'],
             'mechanism':'private Git index; commit-tree on fresh live main; ordinary non-force push; shared index/worktree untouched'}
    if not args.execute:
        print(json.dumps(receipt,indent=2))
        return
    PRIVATE.mkdir(exist_ok=True)
    index=PRIVATE/f'checkpoint-index-{uuid.uuid4().hex}'
    env=os.environ.copy()
    env['GIT_INDEX_FILE']=str(index)
    try:
        for attempt in range(3):
            parent=live_main()
            ensure_commit(parent)
            run(['git','read-tree',parent],env=env)
            for path,content in selected:
                blob=run(['git','hash-object','-w','--stdin'],input=content).stdout.decode().strip()
                run(['git','update-index','--add','--cacheinfo','100644,'+blob+','+path],env=env)
            tree=run(['git','write-tree'],env=env).stdout.decode().strip()
            parent_tree=run(['git','rev-parse',parent+'^{tree}']).stdout.decode().strip()
            if tree==parent_tree:
                receipt.update(status='already_recorded',commit=parent)
                break
            commit=run(['git','commit-tree',tree,'-p',parent],input=(args.message+'\n').encode()).stdout.decode().strip()
            changed=run(['git','diff-tree','--no-commit-id','--name-only','-r',commit]).stdout.decode().splitlines()
            allowed={p for p,_ in selected}
            if not set(changed)<=allowed:
                raise RuntimeError('Commit unexpectedly modifies unowned paths')
            if verify_destination()!=destination:
                raise RuntimeError('Push destination changed during checkpoint; no push attempted')
            push=run(TRANSPORT+['push',TRANSPORT_REMOTE,commit+':refs/heads/main'],check=False)
            if push.returncode:
                error=push.stderr.decode(errors='replace')
                if attempt<2 and ('non-fast-forward' in error or 'fetch first' in error):
                    continue
                raise RuntimeError(error[:2000])
            after=live_main()
            ensure_commit(after)
            ancestry=run(['git','merge-base','--is-ancestor',commit,after],check=False)
            if ancestry.returncode:
                raise RuntimeError('Pushed commit ancestry could not be verified on live main')
            receipt.update(status='pushed_and_verified',commit=commit,
                           remote_main_parent=parent,live_main_after_push=after,
                           changed_paths=changed)
            break
        atomic_json(ROOT/'LATEST_CHECKPOINT_RECEIPT.json',receipt)
        print(json.dumps(receipt,indent=2))
    finally:
        index.unlink(missing_ok=True)
        Path(str(index)+'.lock').unlink(missing_ok=True)


if __name__=='__main__':
    main()
