"""Read-only account inventory. Credentials never enter outputs or URLs."""
import hashlib
import http.client
import json
from pathlib import Path
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'zenodo_deposit_tool'))
import zenodo

def read_account_page(token, page):
    conn = http.client.HTTPSConnection('zenodo.org', timeout=60)
    try:
        conn.request('GET', f'/api/deposit/depositions?size=100&page={page}', headers={
            'Authorization': f'Bearer {token}', 'Accept': 'application/json',
            'User-Agent': zenodo.USER_AGENT})
        response = conn.getresponse()
        body = response.read(16 * 1024 * 1024 + 1)
        result = json.loads(body)
        if response.status != 200:
            raise zenodo.DepositError(zenodo.response_error(response.status, result, body, token))
        if not isinstance(result, list):
            raise zenodo.DepositError('Unexpected inventory representation')
        return result
    finally:
        conn.close()

def main():
    token = zenodo.token_for('production')
    records = []
    for page in range(1, 101):
        batch = read_account_page(token, page)
        records.extend(batch)
        if len(batch) < 100:
            break
    else:
        raise RuntimeError('Pagination cap exceeded')
    ids = [r['id'] for r in records]
    if len(ids) != len(set(ids)):
        raise RuntimeError('Duplicate pagination IDs')
    # Keep public record data only, omitting account and API bucket details.
    public = [{k: r[k] for k in ('id', 'record_id', 'conceptrecid', 'doi',
                                'metadata', 'files', 'submitted', 'state',
                                'created', 'modified') if k in r} for r in records]
    payload = {'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'records': public}
    (HERE / 'INVENTORY.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    for r in public:
        md = r.get('metadata', {})
        print(json.dumps({'id': r['id'], 'submitted': r.get('submitted'),
             'state': r.get('state'), 'type': md.get('upload_type'),
             'subtype': md.get('publication_type'), 'version': md.get('version'),
             'title': md.get('title'), 'files': [f.get('filename') for f in r.get('files', [])]}, ensure_ascii=False))
    print(f'Inventory count: {len(public)}')

if __name__ == '__main__':
    main()
