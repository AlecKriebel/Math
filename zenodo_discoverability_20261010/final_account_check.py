"""Read-only final account coverage, intended metadata and exclusion check."""
import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'zenodo_deposit_tool'))
import zenodo
import metadata_updates as metadata

def main():
    approvals = json.loads((HERE/'APPROVED_PROPOSALS.json').read_text())['records']
    catalog = json.loads((HERE/'SOURCE_CATALOG.json').read_text())
    if {r['id'] for r in approvals} != {r['id'] for r in catalog if r['status']=='paper'}:
        raise RuntimeError('Approved paper set differs from final scope')
    for row in approvals:
        if not (HERE/'receipts'/str(row['id'])/'after.json').exists():
            raise RuntimeError('All paper publications must finish before final account check')
    original = {r['id']:r for r in json.loads((HERE/'INVENTORY.json').read_text())['records']}
    scope = json.loads((HERE/'reviews/ALL_VERSIONS_SCOPE_EVIDENCE.json').read_text())
    for row in scope['new_since_inventory_or_previous_versions']:
        if row['id'] in original and original[row['id']] != row:
            raise RuntimeError('Conflicting additional original record baseline')
        original.setdefault(row['id'],row)
    # Same read-only endpoint as inventory, with all prior versions included.
    token = zenodo.token_for('production')
    import http.client
    conn = http.client.HTTPSConnection('zenodo.org', timeout=60)
    try:
        conn.request('GET', '/api/deposit/depositions?size=100&page=1&all_versions=true', headers={
            'Authorization':f'Bearer {token}', 'Accept':'application/json', 'User-Agent':zenodo.USER_AGENT})
        response = conn.getresponse()
        body = response.read(16*1024*1024+1)
        data = json.loads(body)
        if response.status != 200:
            raise zenodo.DepositError(zenodo.response_error(response.status,data,body,token))
        if not isinstance(data,list) or len(data)>=100:
            raise RuntimeError('Unexpected final inventory shape or unhandled pagination')
    finally:
        conn.close()
    current = {r['id']:r for r in data}
    if len(current)!=len(data) or set(current)!=set(original) or set(current)!=set(r['id'] for r in catalog):
        raise RuntimeError('Owned record IDs changed or final scope is incomplete')
    excluded=[]
    for row in catalog:
        rid=row['id']; now=current[rid]
        if row['status']=='paper':
            after=json.loads((HERE/'receipts'/str(rid)/'after.json').read_text())
            if (now['state']!='done' or not now['submitted'] or now['metadata']!=after['metadata'] or
                metadata.file_snapshot(now)!=after['files'] or metadata.record_doi(now)!=after['doi'] or
                now.get('conceptrecid')!=after['conceptrecid']):
                raise RuntimeError(f'Final owned listing differs from verified publication {rid}')
        else:
            old=original[rid]
            if (now['metadata']!=old['metadata'] or metadata.file_snapshot(now)!=metadata.file_snapshot(old) or
                any(now.get(k)!=old.get(k) for k in ('submitted','state','conceptrecid','doi'))):
                raise RuntimeError(f'Excluded record changed {rid}')
            excluded.append(rid)
    result={'utc':datetime.now(timezone.utc).isoformat(),'method':'GET',
            'path':'/api/deposit/depositions?size=100&page=1&all_versions=true',
            'owned_record_count':len(current),'paper_count':len(approvals),'excluded_count':len(excluded),
            'same_owned_record_ids':True,'all_papers_published_match_verified_receipts':True,
            'all_excluded_metadata_files_dois_states_unchanged':True,'excluded_ids':sorted(excluded)}
    bound = ['APPROVED_PROPOSALS.json','SOURCE_CATALOG.json','INVENTORY.json',
             'reviews/ALL_VERSIONS_SCOPE_EVIDENCE.json','final_account_check.py']
    result['input_sha256']={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in bound}
    result['after_receipt_sha256']={str(r['id']):hashlib.sha256(
        (HERE/'receipts'/str(r['id'])/'after.json').read_bytes()).hexdigest() for r in approvals}
    result['authenticated_response_sha256']=hashlib.sha256(body).hexdigest()
    (HERE/'ACCOUNT_FINAL_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
