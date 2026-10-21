#!/usr/bin/env python3
"""Disk-light checkpoint of this effort's explicit paths; no shared Git writes.

GitHub's tree overlay preserves every unselected path. A non-fast-forward ref
update is rejected and rebuilt on the new live main; force is always false.
No token, raw ledger, private runtime or scientific download is uploaded.
"""
import argparse
import base64
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
from checkpoint import NAMES, ROOT, REPO, verify_destination
from sweep_io import atomic_json

API='repos/AlecKriebel/Math/'


def api(endpoint,method='GET',body=None):
    command=['gh','api','--hostname','github.com',API+endpoint,'--method',method]
    data=None
    if body is not None:
        command+=['--input','-']
        data=json.dumps(body,ensure_ascii=False).encode()
    result=subprocess.run(command,input=data,capture_output=True,cwd=REPO)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace')[:1500])
    return json.loads(result.stdout)


def tree_map(sha,recursive=False):
    result=api('git/trees/'+sha+('?recursive=1' if recursive else ''))
    if result.get('truncated'):raise RuntimeError('Tree listing truncated')
    return {entry['path']:entry for entry in result['tree']}


def blob_sha(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def overlay_entry(folder,name,data):
    """Represent frozen bytes exactly; verify binary blob identity before use."""
    entry={'path':folder+'/'+name,'mode':'100644','type':'blob'}
    try:
        entry['content']=data.decode('utf-8')
    except UnicodeDecodeError:
        uploaded=api('git/blobs','POST',{'encoding':'base64',
                     'content':base64.b64encode(data).decode('ascii')})
        if uploaded.get('sha')!=blob_sha(data):
            raise RuntimeError('Uploaded binary blob identity mismatch: '+name)
        entry['sha']=uploaded['sha']
    return entry


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--message',required=True)
    args=parser.parse_args()
    verify_destination()
    extras=['remote_checkpoint.py',
            'reviews/inventory_adversary_02/REMOTE_CHECKPOINT_REVIEW.md',
            'reviews/pr0248_ledger_repair_adversary/REVIEW.md',
            'reviews/pr0248_ledger_repair_adversary/VERIFICATION.json']
    receipts=[p.name for p in ROOT.iterdir()
              if re.fullmatch(r'PR\d{4}_(?:DISPOSITION|PUBLICATION_VERIFICATION|LEDGER_REPAIR|LEDGER_REPAIR_PROPOSAL)\.json',p.name)]
    selected={}
    for name in dict.fromkeys(NAMES+extras+sorted(receipts)):
        relative=Path(name)
        path=ROOT/relative
        if (relative.is_absolute() or '..' in relative.parts or
                any(ROOT.joinpath(*relative.parts[:i]).is_symlink()
                    for i in range(1,len(relative.parts)+1)) or
                not path.is_file() or not path.resolve().is_relative_to(ROOT.resolve())):
            raise RuntimeError('Unsafe or absent checkpoint path: '+name)
        before=path.stat()
        content=path.read_bytes()
        after=path.stat()
        if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
            raise RuntimeError('Checkpoint input changed during read: '+name)
        selected[name]=content
    state=json.loads(selected['STATE.json'])
    journal=[json.loads(line) for line in selected['dispositions.jsonl'].decode().splitlines()]
    if [row['pr'] for row in journal]!=list(range(9,state['next_pr'])):
        raise RuntimeError('Checkpoint cursor/journal are not a contiguous snapshot')
    if state['last_completely_processed_pr']!=state['next_pr']-1:
        raise RuntimeError('Checkpoint cursor mismatch')
    hashes={name:blob_sha(content) for name,content in selected.items()}
    folder=ROOT.name
    for attempt in range(3):
        parent=api('git/ref/heads/main')['object']['sha']
        parent_commit=api('git/commits/'+parent)
        base_tree=parent_commit['tree']['sha']
        original_root=tree_map(base_tree)
        old_folder=original_root.get(folder)
        original=tree_map(old_folder['sha'],True) if old_folder else {}
        changed={name:data for name,data in selected.items()
                 if original.get(name,{}).get('sha')!=hashes[name]}
        receipt={'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),
                 'remote_main_parent':parent,'completion_estimate_percent':state['completion_estimate_percent'],
                 'last_completely_processed_pr':state['last_completely_processed_pr'],
                 'changed_paths':[folder+'/'+name for name in changed],
                 'files':[{'path':folder+'/'+name,'bytes':len(data),
                           'sha256':hashlib.sha256(data).hexdigest(),'git_blob':hashes[name]}
                          for name,data in selected.items()],
                 'mechanism':'GitHub tree overlay on fresh main; every unselected tree entry verified unchanged; non-forced fast-forward ref update; no local index/branch writes'}
        if not args.execute:
            print(json.dumps(receipt,indent=2));return
        if not changed:
            receipt.update(status='already_recorded',commit=parent)
            break
        entries=[overlay_entry(folder,name,data) for name,data in changed.items()]
        created=api('git/trees','POST',{'base_tree':base_tree,'tree':entries})
        new_root=tree_map(created['sha'])
        signature=lambda v:(v['mode'],v['type'],v['sha'])
        if {k:signature(v) for k,v in new_root.items() if k!=folder}!={k:signature(v) for k,v in original_root.items() if k!=folder}:
            raise RuntimeError('Unrelated root entry changed')
        actual=tree_map(new_root[folder]['sha'],True)
        # Intermediate directory tree SHAs change by design; all leaf entries
        # must equal the base tree overlaid by exactly the selected changed files.
        expected={k:(v['mode'],v['type'],v['sha']) for k,v in original.items() if v['type']!='tree'}
        expected.update({name:('100644','blob',hashes[name]) for name in changed})
        observed={k:(v['mode'],v['type'],v['sha']) for k,v in actual.items() if v['type']!='tree'}
        if expected!=observed:raise RuntimeError('Created tree differs outside exact checkpoint overlay')
        commit=api('git/commits','POST',{'message':args.message,'tree':created['sha'],'parents':[parent]})
        if [p['sha'] for p in commit['parents']]!=[parent] or commit['tree']['sha']!=created['sha']:
            raise RuntimeError('Commit binding mismatch')
        verify_destination()
        if api('git/ref/heads/main')['object']['sha']!=parent:
            continue
        try:
            api('git/refs/heads/main','PATCH',{'sha':commit['sha'],'force':False})
        except RuntimeError:
            if api('git/ref/heads/main')['object']['sha']!=parent:continue
            raise
        after=api('git/ref/heads/main')['object']['sha']
        relation=api('compare/'+commit['sha']+'...'+after)
        if relation['status'] not in {'identical','ahead'}:
            raise RuntimeError('Checkpoint ancestry not verified on live main')
        receipt.update(status='pushed_and_verified',commit=commit['sha'],
                       live_main_after_push=after)
        break
    else:raise RuntimeError('Main advanced three times; no unsafe ref update attempted')
    # The stdout receipt survives a local ENOSPC after successful remote save.
    print(json.dumps(receipt,indent=2),flush=True)
    atomic_json(ROOT/'LATEST_CHECKPOINT_RECEIPT.json',receipt)


if __name__=='__main__':main()
