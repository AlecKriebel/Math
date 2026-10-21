#!/usr/bin/env python3
"""Read-only verification of the frozen PR421–490 review's observed evidence.
This verifies recorded bytes, Git path/row bindings and archive integrity only.
It does not certify proof correctness, historical priority, global live state,
or arbitrary provider/cache/manifest schemas.
"""
from pathlib import Path, PurePosixPath
import hashlib, json, os, subprocess, zipfile

P = Path(__file__).resolve().parent
ROOT = P.parents[2]
def need(ok, message):
    if not ok:
        raise RuntimeError(message)
def read(name): return json.loads((P/name).read_text())
def git(*args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1')
    return subprocess.run(['git', '--no-optional-locks', *args], cwd=ROOT,
                          env=env, capture_output=True, check=True).stdout

def main():
    inputs = read('INPUT_MANIFEST.json')
    for item in inputs:
        b = (P/item['snapshot']).read_bytes()
        need(len(b) == item['bytes'] and hashlib.sha256(b).hexdigest() == item['sha256'],
             'Frozen input mismatch: '+item['snapshot'])
    inv = {x['number']: x for x in read('inputs/rest_inventory.json')['pull_requests']}
    checks = read('pinned_scope_checks.json')
    need([x['pr'] for x in checks] == list(range(421,491)), 'Numeric range incomplete')
    for x in checks:
        n = x['pr']; pr = inv[n]
        need(x['head'] == pr['headRefOid'] and x['base'] == pr['baseRefOid'], 'Pinned identity mismatch')
        b = git('diff', '--no-ext-diff', '--no-renames', '--name-only', '-z', x['comparison'])
        need(b == (P/f'pinned/pr{n:04}/paths.nul').read_bytes(), 'Actual path receipt mismatch')
        paths = b.decode().rstrip('\0').split('\0') if b else []
        cache = read(f'inputs/eligibility/pr{n:04}.json')
        need(len(paths) == len(set(paths)) == cache['file_count'] and set(paths) == set(cache['changed_paths']),
             'Path set/cache mismatch')
        patches = b''
        for q in sorted(set(paths) & {'QUEUE.md','unsolved_math_prioritization/QUEUE.md'}):
            patches += git('diff', '--no-ext-diff', '--no-renames', '--unified=0', x['comparison'], '--', q)
        need(patches == (P/f'pinned/pr{n:04}/QUEUE.patch').read_bytes(), 'Actual queue receipt mismatch')
        actual = [line[1:] for line in patches.decode().splitlines() if line.startswith('+|')]
        need(actual == [r['source_line'] for r in cache['added_queue_rows']], 'Actual added row mismatch')
        need(len(actual) == 1, 'Own-row uniqueness mismatch')
        row = [cell.strip() for cell in actual[0].split('|')[1:-1]]
        disp = read(f'inputs/PR{n:04}_DISPOSITION.json')
        need(row[1].split('/')[0].strip() in disp['problem_ids'], 'Own problem ID mismatch')
        need(row[7] == ('claimed_solved' if n in {421,464,468} else disp['current_classification']), 'Status mismatch')
    need(read('live_metadata_differences.json') == [], 'Fresh metadata difference recorded')
    ledger = read('ledger_fresh.json')['values']
    for n, row, doi, pid in [(421,66,'23328912','20001515'), (464,65,'23320818','30004807'),
                              (468,62,'23310484','30000689')]:
        whole = ' '.join(ledger[row-1])
        need(pid in whole and ('/pull/'+str(n)) in whole and doi in ledger[row-1][2], 'Whole ledger identity mismatch')
        record = read(f'publication_pr{n:04}/record_fresh.json')
        need(record['status'] == 'published' and record['submitted'] is True and record['state'] == 'done', 'Record not published')
        for f in record['files']:
            b = (P/f'publication_pr{n:04}'/f['key']).read_bytes()
            need(len(b) == f['size'] and 'md5:'+hashlib.md5(b).hexdigest() == f['checksum'], 'Provider payload mismatch')
    payloads = 0
    for n, name, mf in [(421,'aim_5_2_verification.zip','MANIFEST.json'),
                         (464,'regular_zas_bianchi_verification_v1.zip','SHA256SUMS.json'),
                         (468,'missing_faces_verification_v1.zip','SHA256SUMS.json')]:
        with zipfile.ZipFile(P/f'publication_pr{n:04}'/name) as z:
            names = z.namelist()
            need(len(names) == len(set(names)) and z.testzip() is None, 'ZIP duplicate/CRC mismatch')
            need(all(not q.startswith('/') and '..' not in PurePosixPath(q).parts and '\\' not in q for q in names), 'Unsafe ZIP path')
            need(not any((i.external_attr >> 16) & 0o170000 == 0o120000 for i in z.infolist()), 'ZIP symlink')
            m = json.loads(z.read(mf))['files']
            items = m if isinstance(m,list) else [dict(v,path=k) for k,v in m.items()]
            need(len(items) == len({i['path'] for i in items}), 'Duplicate manifest path')
            for i in items:
                b = z.read(i['path'])
                need(len(b) == i['bytes'] and hashlib.sha256(b).hexdigest() == i['sha256'], 'Manifest payload mismatch')
                payloads += 1
    need(payloads == 269, 'Manifest total mismatch')
    print(json.dumps({'status':'PASS_OBSERVATIONAL_EVIDENCE','prs':70,'explicit_non_claimed_statuses':67,
                      'published_identity_matches':3,'manifest_payloads':payloads,
                      'scope':'Recorded input integrity and pinned scope/publication evidence only; no fresh mathematical or priority audit.'},indent=2))
if __name__ == '__main__': main()
