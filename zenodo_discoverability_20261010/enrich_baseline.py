"""Read-only preservation of native file display and per-file access settings."""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from baseline import PacedClient
import zenodo

HERE = Path(__file__).resolve().parent

def enrich(path, client):
    baseline = json.loads(path.read_text())
    if 'native_files' in baseline:
        return baseline['id'], 'already bound'
    record = client.native_get(baseline['id'])
    for key in ('metadata','pids','access','custom_fields'):
        if record[key] != baseline['native'][key]:
            raise RuntimeError(f'Native {key} baseline drift for {baseline["id"]}')
    for key, value in {'id':record['id'],'pids':record['pids'],
                       'parent_id':record['parent']['id'],'parent_pids':record['parent']['pids'],
                       'versions':record['versions']}.items():
        if value != baseline['identity'][key]:
            raise RuntimeError(f'Identity {key} baseline drift')
    files = sorted([{'name':name,'md5':entry['checksum'].removeprefix('md5:'),'size':entry['size']}
                    for name,entry in record['files']['entries'].items()],key=lambda r:r['name'])
    if files != baseline['files']:
        raise RuntimeError('Native file content differs from original deposited checksum inventory')
    baseline['native_files'] = record['files']
    path.write_text(json.dumps(baseline,indent=2,ensure_ascii=False)+'\n')
    return baseline['id'], 'native file settings bound'

if __name__ == '__main__':
    client = PacedClient('production',zenodo.token_for('production'))
    failures = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(enrich,p,client):p for p in (HERE/'receipts').glob('*/before.json')}
        for future in as_completed(futures):
            try:
                record_id,status=future.result()
                print(record_id,status,flush=True)
            except Exception as exc:
                failures.append({'path':str(futures[future]),'error':str(exc)})
                print('Read-only error:',str(exc),flush=True)
    (HERE/'BASELINE_ENRICHMENT_ERRORS.json').write_text(json.dumps(failures,indent=2)+'\n')
    if failures:
        raise SystemExit(1)
