#!/usr/bin/env python3
"""Read-only owned/public Zenodo reconciliation; never persists credentials or drafts."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib, http.client, json, sys, urllib.parse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, '/Users/alec/Documents/Math/zenodo_deposit_tool')
import zenodo

def request(path, token=None):
    conn = http.client.HTTPSConnection('zenodo.org', timeout=60)
    headers = {'Accept': 'application/json', 'User-Agent': zenodo.USER_AGENT}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    try:
        conn.request('GET', path, headers=headers)
        response = conn.getresponse()
        body = response.read(32*1024*1024)
        if response.status != 200:
            raise RuntimeError(f'Zenodo HTTP {response.status}')
        return json.loads(body), hashlib.sha256(body).hexdigest()
    finally:
        conn.close()

def main():
    token = zenodo.token_for('production')
    records, pages, unpublished_count = [], [], 0
    for page in range(1, 101):
        endpoint = f'/api/deposit/depositions?size=100&page={page}&all_versions=true'
        rows, digest = request(endpoint, token)
        assert isinstance(rows, list)
        pages.append({'endpoint': endpoint, 'count':len(rows),'response_sha256':digest})
        for raw in rows:
            if not raw.get('submitted') or raw.get('state') != 'done':
                unpublished_count += 1
                continue
            row = {k:raw[k] for k in ('id','record_id','conceptrecid','doi','metadata','submitted','state','created','modified') if k in raw}
            row['files'] = [{k:f[k] for k in ('filename','filesize','checksum') if k in f} for f in raw.get('files',[])]
            records.append(row)
        print(f'Owned page {page}: {len(rows)} entries', flush=True)
        if len(rows)<100: break
    else: raise RuntimeError('Pagination incomplete')
    del token
    assert len({r['id'] for r in records})==len(records)
    queries = ['creators.orcid:0009-0001-9320-500X','creators.name:"Kriebel, Alec"','creators.name:"Alec Kriebel"']
    def search(q):
        hits, pages = [], []
        for page in range(1, 100):
            endpoint='/api/records?'+urllib.parse.urlencode({'q':q,'all_versions':'true','size':25,'page':page})
            data,digest=request(endpoint)
            new=data['hits']['hits']; total=data['hits']['total']
            if isinstance(total,dict): total=total['value']
            pages.append({'endpoint':endpoint,'count':len(new),'total':total,'response_sha256':digest})
            hits.extend({'id':x['id'],'title':x['metadata']['title']} for x in new)
            if len(hits)>=total: break
        return {'query':q,'pages':pages,'hits':hits}
    public=list(ThreadPoolExecutor(max_workers=3).map(search,queries))
    owned_ids={str(x['id']) for x in records}
    public_ids={str(x['id']) for q in public for x in q['hits']}
    result={'retrieved_utc':datetime.now(timezone.utc).isoformat(),'source':'Read-only owned depositions and unauthenticated public author queries, all_versions=true','owned_pagination':pages,'unpublished_entries_omitted':unpublished_count,'records':records,'public_identity_queries':public,'public_identity_ids_outside_owned_published':sorted(public_ids-owned_ids),'owned_published_ids_missing_from_identity_queries':sorted(owned_ids-public_ids)}
    (HERE/'zenodo-current-public.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'published_records':len(records),'unpublished_entries_omitted':unpublished_count,'identity_union':len(public_ids),'outside_owned':result['public_identity_ids_outside_owned_published'],'missing_public_query':result['owned_published_ids_missing_from_identity_queries']}))

if __name__=='__main__': main()
