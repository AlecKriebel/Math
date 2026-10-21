#!/usr/bin/env python3
"""Exhaustive REST inventory; numeric tail is discovered, never hardcoded."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import time
import uuid
from sweep_io import atomic_json

ROOT = Path(__file__).resolve().parent
RAW = ROOT/'raw'


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def api(endpoint):
    for attempt in range(5):
        p = subprocess.run(['gh','api',endpoint],text=True,capture_output=True)
        if not p.returncode:
            return json.loads(p.stdout)
        if not any(s in p.stderr for s in ('HTTP 502','HTTP 503','HTTP 504')) or attempt==4:
            raise RuntimeError(p.stderr[:1000])
        time.sleep(2**attempt)


def main():
    RAW.mkdir(exist_ok=True)
    started=now()
    stamp=started.replace(':','').replace('-','').split('.')[0]+'_'+uuid.uuid4().hex
    nodes={}
    pages=[]
    page=1
    while True:
        endpoint=f'repos/AlecKriebel/Math/pulls?state=all&sort=created&direction=asc&per_page=100&page={page}'
        data=api(endpoint)
        path=RAW/f'rest_inventory_{stamp}_{page:03d}.json'
        atomic_json(path,data)
        pages.append({'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'count':len(data)})
        for p in data:
            n=p['number']
            if nodes and n<=max(nodes):
                raise RuntimeError('REST creation-order keys failed to increase strictly')
            if n in nodes:
                raise RuntimeError(f'duplicate PR {n} across pages')
            nodes[n]={
                'number':n,'title':p['title'],'body':p['body'] or '',
                'state':'MERGED' if p.get('merged_at') else p['state'].upper(),
                'isDraft':p.get('draft',False),'mergedAt':p.get('merged_at'),
                'createdAt':p['created_at'],'updatedAt':p['updated_at'],
                'url':p['html_url'],'headRefOid':p['head']['sha'],
                'baseRefOid':p['base']['sha'],'headRefName':p['head']['ref'],
                'baseRefName':p['base']['ref'],
                'mergeCommit':{'oid':p['merge_commit_sha']} if p.get('merged_at') and p.get('merge_commit_sha') else None,
                'changedFiles':p.get('changed_files')}
        print(json.dumps({'rest_inventory_page':page,'collected':len(nodes),'page_count':len(data)}),flush=True)
        if not data:
            break
        page+=1
    latest=api('repos/AlecKriebel/Math/pulls?state=all&sort=created&direction=desc&per_page=1')
    latestpath=RAW/f'rest_boundary_{stamp}.json'
    atomic_json(latestpath,{'observed_at':now(),'response':latest})
    highest=max(nodes,default=0)
    if not latest or latest[0]['number']!=highest:
        raise RuntimeError('Newest-PR response did not match the collected maximum; extend or investigate inventory')
    query='query { repository(owner:"AlecKriebel",name:"Math") { pullRequests(first:1,orderBy:{field:CREATED_AT,direction:DESC}) { totalCount nodes { number } } } }'
    p=subprocess.run(['gh','api','graphql','--input','-'],input=json.dumps({'query':query}),capture_output=True,text=True)
    if p.returncode:
        raise RuntimeError('Independent total/max query failed: '+p.stderr[:1000])
    independent=json.loads(p.stdout)
    independentpath=RAW/f'independent_boundary_{stamp}.json'
    atomic_json(independentpath,{'observed_at':now(),'response':independent})
    boundary=independent['data']['repository']['pullRequests']
    if boundary['totalCount']!=len(nodes) or not boundary['nodes'] or boundary['nodes'][0]['number']!=highest:
        raise RuntimeError('Independent total/max disagrees; extend or investigate inventory')
    branch=api('repos/AlecKriebel/Math/git/ref/heads/main')
    branchpath=RAW/f'main_boundary_{stamp}.json'
    atomic_json(branchpath,{'observed_at':now(),'response':branch})
    gaps=[n for n in range(9,highest+1) if n not in nodes]
    gap_evidence=[]
    for n in gaps:
        issue=api(f'repos/AlecKriebel/Math/issues/{n}')
        if 'pull_request' in issue:
            raise RuntimeError(f'PR {n} missing from supposedly complete inventory')
        gap_evidence.append({'number':n,'kind':'issue_not_pull_request','url':issue['html_url']})
    ordered=[nodes[n] for n in sorted(nodes) if n>=9]
    result={'schema_version':1,'collector':'GitHub REST with empty terminal page and newest-PR recheck',
            'started_at':started,'completed_at':now(),'repository':'AlecKriebel/Math',
            'start_pr':9,'highest_pr':highest,'all_pr_count':len(nodes),
            'in_scope_pr_count':len(ordered),'numeric_gaps':gaps,'gap_evidence':gap_evidence,
            'boundary_receipts':[str(p.relative_to(ROOT)) for p in (latestpath,independentpath,branchpath)],
            'independent_total':boundary['totalCount'],
            'main_sha_at_final_page':branch['object']['sha'],'pages':pages,'pull_requests':ordered}
    known_max=0
    for path,key in ((ROOT/'STATE.json','highest_observed_pr'),(ROOT/'rest_inventory.json','highest_pr')):
        if path.exists():
            known_max=max(known_max,json.loads(path.read_text()).get(key,0))
    if highest<known_max:
        raise RuntimeError('REST capture would lower a previously recorded maximum; prior inventory preserved')
    atomic_json(ROOT/'rest_inventory.json',result)
    summary={k:v for k,v in result.items() if k not in ('pull_requests','pages')}
    summary['state_counts']={s:sum(p['state']==s for p in ordered) for s in ('OPEN','CLOSED','MERGED')}
    atomic_json(ROOT/'REST_INVENTORY_RECEIPT.json',summary)
    print(json.dumps(summary),flush=True)


if __name__=='__main__':
    main()
