"""Read-only public/native baseline for every in-scope paper."""
import json
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import threading
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'zenodo_deposit_tool'))
import zenodo
import metadata_updates as updates

class PacedClient(zenodo.ZenodoClient):
    """Keep authenticated requests comfortably below the minute quota."""
    _lock = threading.Lock()
    _next = 0.0

    def request(self, *args, **kwargs):
        with self._lock:
            delay = self._next - time.monotonic()
            if delay > 0:
                time.sleep(delay)
            type(self)._next = time.monotonic() + 0.85
        return super().request(*args, **kwargs)

def identity(native, versions):
    hits = versions['hits']['hits']
    total = versions['hits']['total']
    if isinstance(total, dict):
        total = total['value']
    if total != len(hits):
        raise RuntimeError('Version pagination not fully covered')
    return {'id': native['id'], 'pids': native['pids'],
            'parent_id': native['parent']['id'], 'parent_pids': native['parent']['pids'],
            'versions': native['versions'], 'version_ids': sorted(str(r['id']) for r in hits),
            'version_count': total}

def snapshot(client, record_id):
    record = client.get(record_id)
    native = client.native_get(record_id)
    versions = client.request('GET', client.base + f'/api/records/{record_id}/versions?size=100',
                              accept='application/vnd.inveniordm.v1+json')
    compatible = True
    issue = None
    ns = {k: native[k] for k in ('metadata', 'custom_fields', 'access', 'pids')}
    try:
        updates.require_legacy_coverage(ns)
    except zenodo.DepositError as exc:
        compatible = False
        issue = str(exc)
    return {'retrieved_utc': datetime.now(timezone.utc).isoformat(),
            'id': record_id, 'submitted': record['submitted'], 'state': record['state'],
            'conceptrecid': record.get('conceptrecid'), 'doi': updates.record_doi(record),
            'metadata': record['metadata'], 'files': updates.file_snapshot(record),
            'native': ns, 'native_files': native['files'], 'identity': identity(native, versions),
            'legacy_compatible': compatible, 'issue': issue}

def main():
    catalog = json.loads((HERE / 'SOURCE_CATALOG.json').read_text())
    inventory = {r['id']: r for r in json.loads((HERE / 'INVENTORY.json').read_text())['records']}
    ids = [r['id'] for r in catalog if r['status'] == 'paper']
    client = PacedClient('production', zenodo.token_for('production'))
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        pending = []
        for record_id in ids:
            saved = HERE / 'receipts' / str(record_id) / 'before.json'
            if saved.exists():
                snap = json.loads(saved.read_text())
                results.append({'id': record_id, 'compatible': snap['legacy_compatible'],
                                'state': snap['state'], 'version_count': snap['identity']['version_count'],
                                'issue': snap['issue']})
            else:
                pending.append(record_id)
        futures = {pool.submit(snapshot, client, record_id): record_id for record_id in pending}
        for future in as_completed(futures):
            record_id = futures[future]
            snap = future.result()
            old = inventory[record_id]
            if snap['metadata'] != old['metadata'] or snap['files'] != updates.file_snapshot(old):
                raise RuntimeError(f'Inventory drift for {record_id}')
            dest = HERE / 'receipts' / str(record_id)
            dest.mkdir(parents=True, exist_ok=True)
            (dest / 'before.json').write_text(json.dumps(snap, indent=2, ensure_ascii=False) + '\n')
            results.append({'id': record_id, 'compatible': snap['legacy_compatible'],
                            'state': snap['state'], 'version_count': snap['identity']['version_count'],
                            'issue': snap['issue']})
            print(f"Baseline {record_id}: compatible={snap['legacy_compatible']} versions={snap['identity']['version_count']}", flush=True)
    (HERE / 'BASELINE_REPORT.json').write_text(json.dumps(sorted(results, key=lambda r:r['id']), indent=2) + '\n')

if __name__ == '__main__':
    main()
