#!/usr/bin/env python3
"""Refresh only PR254–279, the four matching public records, and ledger values.

All network methods are GET except the documented read-only GWS +read helper.
No uploaded bytes, Git writes, provider mutation commands, or package downloads.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime, hashlib, json, subprocess, urllib.request

OUT = Path(__file__).resolve().parent
OLD = OUT.parent / 'range0254_0279_adversary'

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2) + '\n')

def live_pr(n):
    args = ['gh', 'api', f'repos/AlecKriebel/Math/pulls/{n}']
    r = subprocess.run(args, capture_output=True, timeout=60)
    r.check_returncode()
    v = json.loads(r.stdout)
    return {'number': v['number'], 'title': v['title'], 'body': v['body'],
            'state': v['state'], 'draft': v['draft'], 'merged_at': v['merged_at'],
            'merge_commit_sha': v['merge_commit_sha'], 'updated_at': v['updated_at'],
            'html_url': v['html_url'], 'head_sha': v['head']['sha'],
            'base_sha': v['base']['sha'], 'api_sha256': sha(r.stdout), 'at': now()}

def get(url):
    req = urllib.request.Request(url, method='GET', headers={
        'Accept': 'application/json', 'User-Agent': 'MathIndependentCoverageReview/1.0'})
    with urllib.request.urlopen(req, timeout=40) as f:
        raw = f.read()
        return f.status, f.url, raw

def public_record(a):
    rid = a['record']['id']
    status, url, raw = get('https://zenodo.org/api/records/' + str(rid))
    v = json.loads(raw)
    ds, du, _ = get('https://doi.org/' + a['record']['doi'])
    return {'pr': a['pr'], 'at': now(), 'record_status': status,
            'record_url': url, 'record_api_sha256': sha(raw), 'record': v,
            'doi_resolution': {'status': ds, 'final_url': du},
            'payloads_downloaded': 0,
            'cached_payloads': a['payloads']}

old_prs = json.loads((OLD / 'live_prs.json').read_text())['prs']
old_pubs = json.loads((OLD / 'publications_fresh.json').read_text())['publications']
prs, pubs, errors = [], [], []
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(live_pr, n): ('pr', n) for n in range(254, 280)}
    futures.update({pool.submit(public_record, a): ('publication', a['pr']) for a in old_pubs})
    for f in as_completed(futures):
        kind, n = futures[f]
        try:
            value = f.result()
            (prs if kind == 'pr' else pubs).append(value)
        except Exception as e:
            errors.append({'kind': kind, 'pr': n, 'error': repr(e)})
save('live_prs_refresh.json', {'at': now(), 'prs': sorted(prs, key=lambda a: a['number']), 'errors': errors})
save('publications_refresh.json', {'at': now(), 'publications': sorted(pubs, key=lambda a: a['pr']), 'errors': errors})

cmd = ['gws', 'sheets', '+read', '--spreadsheet',
       '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20', '--range', "'Math Puzzles'!A:AQ"]
r = subprocess.run(cmd, capture_output=True, timeout=75)
receipt = {'at': now(), 'command': cmd, 'returncode': r.returncode,
           'stderr': r.stderr.decode(), 'stdout_sha256': sha(r.stdout)}
if r.returncode == 0:
    receipt['data'] = json.loads(r.stdout)
else:
    receipt['stdout'] = r.stdout.decode()
save('ledger_refresh.json', receipt)

old_by_n = {a['number']: a for a in old_prs}
pr_changes = [{'pr': a['number'], 'fields': [k for k, v in old_by_n[a['number']].items() if a.get(k) != v]}
              for a in prs if any(a.get(k) != v for k, v in old_by_n[a['number']].items())]
old_pubs_by_n = {a['pr']: a for a in old_pubs}
pub_changes = []
for a in pubs:
    o = old_pubs_by_n[a['pr']]['record']
    v = a['record']
    files = lambda x: sorted((f['key'], f['size'], f['checksum']) for f in x['files'])
    changes = [k for k in ['id', 'doi', 'state', 'submitted'] if v.get(k) != o.get(k)]
    changes += ['metadata.' + k for k in set(o['metadata']) | set(v['metadata'])
                if o['metadata'].get(k) != v['metadata'].get(k)]
    if files(v) != files(o):
        changes.append('files.identity')
    if changes:
        pub_changes.append({'pr': a['pr'], 'fields': sorted(changes)})
old_ledger = json.loads((OLD / 'ledger_fresh.json').read_text())['data']['values']
new_ledger = receipt.get('data', {}).get('values', [])
ledger_changes = []
for i in range(max(len(old_ledger), len(new_ledger))):
    a = old_ledger[i] if i < len(old_ledger) else []
    b = new_ledger[i] if i < len(new_ledger) else []
    for j in range(max(len(a), len(b))):
        av = a[j] if j < len(a) else ''
        bv = b[j] if j < len(b) else ''
        if av != bv:
            ledger_changes.append({'row': i + 1, 'column': j + 1})
summary = {'at': now(), 'prs_refreshed': len(prs), 'publications_refreshed': len(pubs),
           'errors': errors, 'pr_changes': pr_changes, 'publication_changes': pub_changes,
           'ledger_returncode': r.returncode, 'ledger_rows': len(new_ledger),
           'ledger_changed_cells': ledger_changes, 'payloads_downloaded': 0}
save('REFRESH_SUMMARY.json', summary)
print(json.dumps(summary, indent=2))
raise SystemExit(0 if not errors and r.returncode == 0 else 1)
