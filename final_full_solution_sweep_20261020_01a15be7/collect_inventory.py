#!/usr/bin/env python3
"""Collect a complete, cursor-paginated GitHub PR inventory without mutations."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import time
import uuid
from sweep_io import atomic_json

ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'raw'
RAW.mkdir(exist_ok=True)


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def graphql(query, variables=None):
    payload = {'query': query, 'variables': variables or {}}
    for attempt in range(5):
        r = subprocess.run(['gh', 'api', 'graphql', '--input', '-'],
                           input=json.dumps(payload), text=True, capture_output=True)
        if not r.returncode:
            break
        if not any(code in r.stderr for code in ('HTTP 502','HTTP 503','HTTP 504')) or attempt == 4:
            raise RuntimeError(r.stderr[:2000])
        print(json.dumps({'read_retry': attempt+1, 'reason': r.stderr[:200]}), flush=True)
        time.sleep(2**attempt)
    value = json.loads(r.stdout)
    if value.get('errors'):
        raise RuntimeError(json.dumps(value['errors']))
    return value


def main():
    query = '''query($cursor:String) {
      repository(owner:"AlecKriebel",name:"Math") {
        pullRequests(first:100,after:$cursor,orderBy:{field:CREATED_AT,direction:ASC}) {
          totalCount nodes { number title body state isDraft mergedAt createdAt
            updatedAt url headRefOid baseRefOid headRefName baseRefName changedFiles
            mergeCommit { oid } }
          pageInfo { hasNextPage endCursor }
        }
        defaultBranchRef { name target { oid } }
      }
      rateLimit { remaining resetAt }
    }'''
    started = now()
    stamp = started.replace(':', '').replace('-', '').split('.')[0]+'_'+uuid.uuid4().hex
    cursor = None
    seen_cursors = {None}
    prs = {}
    pages = []
    while True:
        value = graphql(query, {'cursor': cursor})
        repo = value['data']['repository']
        connection = repo['pullRequests']
        pagepath = RAW / f'inventory_{stamp}_{len(pages)+1:03d}.json'
        atomic_json(pagepath,value)
        pages.append({'path': str(pagepath.relative_to(ROOT)),
                      'sha256': hashlib.sha256(pagepath.read_bytes()).hexdigest(),
                      'reported_total': connection['totalCount'],
                      'main_sha': repo['defaultBranchRef']['target']['oid']})
        for pr in connection['nodes']:
            if prs and pr['number'] <= max(prs):
                raise RuntimeError('GraphQL ordered PR keys failed to increase strictly')
            if pr['number'] in prs:
                raise RuntimeError(f'Duplicate PR number {pr["number"]}')
            prs[pr['number']] = pr
        print(json.dumps({'inventory_page': len(pages), 'collected': len(prs),
                          'reported_total': connection['totalCount'],
                          'rate_remaining': value['data']['rateLimit']['remaining']}), flush=True)
        page = connection['pageInfo']
        if not page['hasNextPage']:
            break
        if not page['endCursor'] or page['endCursor'] in seen_cursors:
            raise RuntimeError('Pagination cursor failed to advance')
        cursor = page['endCursor']
        seen_cursors.add(cursor)
    boundary_query='''query { repository(owner:"AlecKriebel",name:"Math") {
      pullRequests(first:1,orderBy:{field:CREATED_AT,direction:DESC}) {
        totalCount nodes { number } } } }'''
    boundary_value=graphql(boundary_query)
    atomic_json(RAW/f'graphql_boundary_{stamp}.json',boundary_value)
    boundary=boundary_value['data']['repository']['pullRequests']
    highest = max(prs, default=0)
    if (not boundary['nodes'] or boundary['totalCount']!=len(prs)
            or boundary['nodes'][0]['number']!=highest):
        raise RuntimeError('Final independent GraphQL total/max disagrees with collection')
    prior_state=json.loads((ROOT/'STATE.json').read_text())
    if highest<prior_state.get('highest_observed_pr',0):
        raise RuntimeError('GraphQL capture would lower the previously observed maximum')
    ordered = [prs[n] for n in sorted(prs) if n >= 9]
    gaps = [n for n in range(9, highest+1) if n not in prs]
    if gaps:
        raise RuntimeError('GraphQL route requires individual numeric-gap investigation before promotion')
    result = {'schema_version': 1, 'started_at': started, 'completed_at': now(),
              'repository': 'AlecKriebel/Math', 'start_pr': 9,
              'highest_pr': highest, 'all_pr_count': len(prs),
              'in_scope_pr_count': len(ordered), 'numeric_gaps': gaps,
              'main_sha_at_final_page': repo['defaultBranchRef']['target']['oid'],
              'pages': pages, 'pull_requests': ordered}
    atomic_json(ROOT/'inventory.json',result)
    state = json.loads((ROOT/'STATE.json').read_text())
    state.update(highest_observed_pr=max(highest,state.get('highest_observed_pr',0)),
                 inventory_pr_count=len(ordered),inventory_timestamp=result['completed_at'],
                 completion_estimate_percent=max(2,state.get('completion_estimate_percent',0)))
    atomic_json(ROOT/'STATE.json',state)
    summary = {k:v for k,v in result.items() if k != 'pull_requests'}
    summary['state_counts'] = {s:sum(p['state']==s for p in ordered)
                               for s in ('OPEN','CLOSED','MERGED')}
    atomic_json(ROOT/'INVENTORY_RECEIPT.json',summary)
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
