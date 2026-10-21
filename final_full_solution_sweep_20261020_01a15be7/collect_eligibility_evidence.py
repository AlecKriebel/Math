#!/usr/bin/env python3
"""Collect changed-file and QUEUE-patch evidence in increasing PR order.

This is preparatory evidence collection, not a completed publication duplicate
check, full-solution classification, mathematical audit, or disposition.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
from sweep_io import atomic_json
from checkpoint import ensure_commit

ROOT=Path(__file__).resolve().parent
RAW=ROOT/'raw'/'eligibility'
OUT=ROOT/'eligibility'
QUEUE_PATHS={'QUEUE.md','unsolved_math_prioritization/QUEUE.md'}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def api(endpoint):
    for attempt in range(5):
        p=subprocess.run(['gh','api',endpoint],capture_output=True,text=True)
        if not p.returncode:
            return json.loads(p.stdout)
        if not any(s in p.stderr for s in ('HTTP 502','HTTP 503','HTTP 504')) or attempt==4:
            raise RuntimeError(p.stderr[:1000])
        time.sleep(2**attempt)


def queue_row(line):
    cells=[c.strip() for c in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
    if len(cells)<9 or not cells[0].isdigit():
        return None
    return {'rank':int(cells[0]),'problem_id':cells[1].split('/')[0].strip(),
            'problem_alias':cells[1],'problem_title':cells[2],
            'status':cells[7],'turns':cells[8],'source_line':line}


def main():
    if OUT.is_symlink() or RAW.is_symlink() or not OUT.resolve().is_relative_to(ROOT.resolve()) or not RAW.resolve().is_relative_to(ROOT.resolve()):
        raise RuntimeError('Evidence directories must be ordinary directories inside this program')
    RAW.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(exist_ok=True)
    inventory=json.loads((ROOT/'rest_inventory.json').read_text())
    summary=[]
    for pr in inventory['pull_requests']:
        n=pr['number']
        path=OUT/f'pr{n:04d}.json'
        if path.exists():
            old=json.loads(path.read_text())
            if (old.get('inventory_head_sha')==pr['headRefOid']
                    and old.get('inventory_base_sha')==pr['baseRefOid']
                    and old.get('collection_schema')==2):
                summary.append(old)
                continue
        started=now()
        files=[]
        pages=[]
        page=1
        source='live REST file-list endpoint; not commit-bound'
        while True:
            data=api(f'repos/AlecKriebel/Math/pulls/{n}/files?per_page=100&page={page}')
            wire=json.dumps(data,sort_keys=True,separators=(',',':')).encode()
            pages.append({'page':page,'count':len(data),'decoded_response_sha256':hashlib.sha256(wire).hexdigest()})
            files.extend(data)
            if len(data)<100:
                break
            if len(files)>=100:
                if pr['state']=='MERGED' and pr.get('mergeCommit'):
                    revision=pr['mergeCommit']['oid']
                    ensure_commit(revision)
                    comparison=revision+'^1..'+revision
                    source='complete pinned merged-commit first-parent diff; large live file-list endpoint bypassed'
                else:
                    ensure_commit(pr['baseRefOid'])
                    ensure_commit(pr['headRefOid'])
                    comparison=pr['baseRefOid']+'...'+pr['headRefOid']
                    source='complete pinned git merge-base diff; large live file-list endpoint bypassed'
                p=subprocess.run(['git','diff','--no-ext-diff','--no-renames','--name-status','-z',comparison],capture_output=True,check=True)
                tokens=p.stdout.decode().split('\0')
                files=[]
                for index in range(0,len(tokens)-1,2):
                    change,changed_path=tokens[index:index+2]
                    f={'filename':changed_path,'sha':None,'status':{'A':'added','D':'removed','M':'modified'}.get(change,change),'additions':None,'deletions':None}
                    if changed_path in QUEUE_PATHS:
                        patch=subprocess.run(['git','diff','--no-ext-diff','--no-renames','--unified=3',comparison,'--',changed_path],capture_output=True,check=True)
                        f['patch']=patch.stdout.decode()
                        reference=(revision+'^1' if change=='D' else revision) if pr['state']=='MERGED' and pr.get('mergeCommit') else (pr['baseRefOid'] if change=='D' else pr['headRefOid'])
                        blob=subprocess.run(['git','rev-parse',reference+':'+changed_path],capture_output=True,text=True,check=True)
                        f['sha']=blob.stdout.strip()
                    files.append(f)
                break
            page+=1
        rows=[]
        queues=[]
        for f in files:
            if f['filename'] in QUEUE_PATHS:
                patch=f.get('patch')
                queues.append({'path':f['filename'],'sha':f['sha'],'patch_present':patch is not None,'patch':patch})
                for line in (patch or '').splitlines():
                    if line.startswith('+') and not line.startswith('+++'):
                        row=queue_row(line[1:])
                        if row:
                            row['queue_path']=f['filename']
                            rows.append(row)
        ids=sorted(set(m for f in files for m in re.findall(r'(?:attempts|problems)/(\d+)(?:/|_)',f['filename'])))
        value={'pr':n,'collection_schema':2,'inventory_head_sha':pr['headRefOid'],
               'inventory_base_sha':pr['baseRefOid'],'inventory_state':pr['state'],'file_list_source':source,
               'pinned_comparison':comparison if source.startswith('complete pinned') else None,
               'started_at':started,'completed_at':now(),
               'observation_status':'preliminary_live_file_list; exact head binding must be rechecked before final disposition',
               'file_count':len(files),'pages':pages,
               'changed_paths':[f['filename'] for f in files],
               'files':[{'filename':f['filename'],'sha':f['sha'],'status':f['status'],
                         'additions':f['additions'],'deletions':f['deletions']} for f in files],
               'queue_changes':queues,'added_queue_rows':rows,'path_problem_ids':ids,
               'duplicate_check':'pending_live_gws','final_disposition':'pending'}
        if OUT.is_symlink() or not OUT.resolve().is_relative_to(ROOT.resolve()) or path.resolve().parent != OUT.resolve():
            raise RuntimeError('Eligibility receipt escaped its dedicated output directory')
        atomic_json(path,value)
        summary.append(value)
        if n%25==0 or n==inventory['highest_pr']:
            progress={'captured_at':now(),'last_pr_collected':n,'prs_collected':len(summary),
                      'inventory_highest':inventory['highest_pr'],'candidate_processing_cursor':9,
                      'live_ledger_verified':False}
            atomic_json(ROOT/'ELIGIBILITY_COLLECTION_PROGRESS.json',progress)
            print(json.dumps(progress),flush=True)
    receipt={'completed_at':now(),'count':len(summary),'first_pr':summary[0]['pr'] if summary else None,
             'last_pr':summary[-1]['pr'] if summary else None,
             'queue_modified':sum(bool(s['queue_changes']) for s in summary),
             'no_added_queue_row':sum(not s['added_queue_rows'] for s in summary),
             'claimed_solved_in_any_added_queue_row':[s['pr'] for s in summary if any(r['status']=='claimed_solved' for r in s['added_queue_rows'])],
             'warning':'Structural collection only. No completed live duplicate check, mathematical verification, priority audit, or final disposition is asserted.'}
    atomic_json(ROOT/'ELIGIBILITY_COLLECTION_RECEIPT.json',receipt)
    print(json.dumps(receipt),flush=True)


if __name__=='__main__':
    main()
