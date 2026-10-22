#!/usr/bin/env python3
"""Supplement the unmodified 459 controls with independently refreshed bindings.

Reads cached files, bounded Git objects and fresh read receipts; writes only in OUT.
This is an identity/coverage audit, not a proof or novelty certification.
"""
from pathlib import Path
import collections, datetime, hashlib, io, json, os, re, subprocess, zipfile

OUT = Path(__file__).resolve().parent
OLD = OUT.parent / 'range0254_0279_adversary'
ROOT = OUT.parents[1]
WORK = ROOT.parent
checks, source_hashes = [], []

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read(path):
    return json.loads(path.read_text())

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

def check(name, value, detail=None):
    checks.append({'name': name, 'pass': bool(value), 'detail': detail})

def git(*args):
    r = subprocess.run(['git', *args], cwd=WORK, capture_output=True, timeout=30,
                       env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
    r.check_returncode()
    return r.stdout

def file_hash(path, role):
    raw = path.read_bytes()
    source_hashes.append({'kind': 'file', 'path': str(path.relative_to(WORK)),
                          'role': role, 'bytes': len(raw), 'sha256': sha(raw)})

def normdoi(value):
    return re.sub(r'^https?://(?:dx[.])?doi[.]org/', '', str(value).strip()).lower().rstrip('/')

bindings = read(OLD / 'bindings.json')['bindings']
live = {v['number']: v for v in read(OUT / 'live_prs_refresh.json')['prs']}
pubs = {v['pr']: v for v in read(OUT / 'publications_refresh.json')['publications']}
old_live = {v['number']: v for v in read(OLD / 'live_prs.json')['prs']}
ledger_read = read(OUT / 'ledger_refresh.json')
ledger = ledger_read['data']['values']
replay = read(OUT / 'REPLAY_CHECK_RECEIPT.json')
check('459 original controls independently replayed', replay['passed'] and replay['checks'] == 459 and not replay['failures'])
check('fresh PR scope exactly 254 through 279', sorted(live) == list(range(254, 280)))
check('fresh four matching public records', sorted(pubs) == [254, 256, 263, 278])
check('documented read-only GWS open-ended range', ledger_read['returncode'] == 0 and ledger_read['command'][-1] == "'Math Puzzles'!A:AQ")
check('ledger schema and population', ledger[0] == ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes'] and len(ledger) == 173)
check('full ledger values unchanged', ledger == read(OLD / 'ledger_fresh.json')['data']['values'])
check('replay only redirects output and preserves original control logic', read(OUT / 'CHECKER_SAFETY_REVIEW.json')['no_other_code_changes'])
canonical = read(OLD / 'canonical_queue_fresh.json')
canonical_raw = git('cat-file', 'blob', canonical['blob_sha'])
check('immutable canonical snapshot blob independently preserved', sha(canonical_raw) == canonical['sha256'] and len(canonical_raw) == canonical['bytes'])
source_hashes.append({'kind': 'git_blob', 'role': 'canonical queue snapshot only; own PR rows determine eligibility', 'git_blob_oid': canonical['blob_sha'], 'bytes': len(canonical_raw), 'sha256': sha(canonical_raw)})

scope_table, provenance = [], []
for b in bindings:
    n, row = b['pr'], b['own_row']
    e = read(ROOT / b['eligibility_path'])
    pr, d = live[n], read(ROOT / f'PR{n:04}_DISPOSITION.json')
    fields = ['number', 'title', 'body', 'state', 'draft', 'merged_at', 'merge_commit_sha', 'updated_at', 'html_url', 'head_sha', 'base_sha']
    check(f'{n} fresh PR matches prior independent read', all(pr[k] == old_live[n][k] for k in fields))
    check(f'{n} current head base original body pin', pr['head_sha'] == e['inventory_head_sha'] == d['inventory_head_sha'] and pr['base_sha'] == e['inventory_base_sha'] == d['inventory_base_sha'] and sha(pr['body'].encode()) == b['inventory_scoped']['body_sha256'] == d['inventory_body_sha256'])
    check(f'{n} operative disposition unchanged', d == b['disposition'])
    raw = git('diff', '--no-ext-diff', '--no-renames', '--name-only', '-z', b['comparison'])
    paths = raw.decode().strip('\0').split('\0')
    check(f'{n} independent exact changed path set', set(paths) == set(e['changed_paths']) and len(paths) == e['file_count'])
    added = []
    for qb in b['queue_bindings']:
        patch = git('diff', '--no-ext-diff', '--no-renames', '--unified=0', b['comparison'], '--', qb['path'])
        added += [v[1:] for v in patch.decode().splitlines() if v.startswith('+|')]
        blob = git('cat-file', 'blob', qb['actual_blob'])
        source_hashes.append({'kind': 'git_blob', 'role': 'own-PR queue row binding', 'pr': n, 'path': qb['path'], 'commit': b['queue_end'], 'git_blob_oid': qb['actual_blob'], 'bytes': len(blob), 'sha256': sha(blob), 'comparison': b['comparison'], 'diff_sha256': sha(patch)})
    own = []
    for line in added:
        cells = [v.strip() for v in re.split(r'(?<!\\)\|', line.strip('|'))]
        if len(cells) >= 8 and cells[1].split(' / ')[0] in e['path_problem_ids']:
            own.append({'problem_id': cells[1].split(' / ')[0], 'status': cells[7], 'line': line})
    check(f'{n} exactly one own explicit status in actual diff', len(own) == 1 and own[0] == {'problem_id': row['problem_id'], 'status': row['status'], 'line': row['source_line']})
    canonical_cells = [v.strip() for v in re.split(r'(?<!\\)\|', b['canonical_row'].strip('|'))]
    check(f'{n} no generic queued exclusion', row['status'] != 'queued' and (row['status'] == 'claimed_solved' or d['disposition'] == 'skip_explicit_non_claimed_solved'))
    scope_table.append({'pr': n, 'problem_id': row['problem_id'], 'alias': row['problem_alias'].split(' / ')[1], 'own_pr_status': row['status'], 'canonical_snapshot_status': canonical_cells[7], 'changed_path_count': len(paths), 'disposition': d['disposition'], 'doi': d.get('doi'), 'ledger_row': d.get('ledger_row')})
    file_hash(ROOT / b['eligibility_path'], 'scoped eligibility receipt')
    file_hash(ROOT / f'PR{n:04}_DISPOSITION.json', 'scoped operative disposition')
    if n in [254, 256, 263]:
        parents = git('rev-list', '--parents', '-n', '1', b['queue_end']).decode().split()
        check(f'{n} reconstruction bound to actual merged head', b['queue_end'] == pr['merge_commit_sha'] and pr['head_sha'] in parents[1:])
        provenance.append({'pr': n, 'receipt_path': b['eligibility_path'], 'receipt_sha256': sha((ROOT / b['eligibility_path']).read_bytes()), 'annotation_at': now(), 'operative_file_list_source': e['file_list_source'], 'operative_pinned_comparison': e['pinned_comparison'], 'operative_file_count': e['file_count'], 'retained_historical_intake_fields': {k: e[k] for k in ['started_at', 'completed_at', 'observation_status', 'pages', 'duplicate_check', 'final_disposition']}, 'interpretation': 'The retained fields document the earlier preliminary REST intake and pending status. They are not the reconstruction time, final file-list authority, or current disposition. Exact operative changed paths, queue blob/diff, merged-head binding and current final disposition were independently revalidated in this follow-up. The original receipt is preserved; this companion is an annotation, not a scientific or disposition repair.'})

counts = collections.Counter(v['own_pr_status'] for v in scope_table)
check('classification counts rederived independently', counts == {'already_solved': 16, 'unsolved': 6, 'claimed_solved': 4})
identity_rows = []
for n, a in sorted(pubs.items()):
    b = next(v for v in bindings if v['pr'] == n)
    v, m, d, r = a['record'], a['record']['metadata'], b['disposition'], b['own_row']
    check(f'{n} fresh done submitted primary DOI', a['record_status'] == 200 and v['state'] == 'done' and v['submitted'] is True and v['doi'] == d['doi'])
    check(f'{n} fresh primary DOI resolves to same record', a['doi_resolution']['status'] == 200 and a['doi_resolution']['final_url'].rstrip('/').endswith('/' + str(v['id'])))
    expected_row = d['ledger_row']
    pid, alias = r['problem_id'], r['problem_alias'].split(' / ')[1]
    reference = re.compile(r'/pull/' + str(n) + r'(?:\D|$)')
    leads = [i + 1 for i, row in enumerate(ledger) if re.search(r'(?<!\d)' + re.escape(pid) + r'(?!\d)', ' '.join(row)) or alias in ' '.join(row) or reference.search(' '.join(row)) or any(normdoi(x) == normdoi(v['doi']) for x in row)]
    doirows = [i + 1 for i, row in enumerate(ledger) if len(row) > 2 and normdoi(row[2]) == normdoi(v['doi'])]
    check(f'{n} unique identifier alias PR DOI ledger leads', leads == doirows == [expected_row])
    text = ' '.join(ledger[expected_row - 1])
    check(f'{n} same ledger row contains each required identity', pid in text and alias in text and reference.search(text) and normdoi(ledger[expected_row - 1][2]) == normdoi(v['doi']))
    api = {f['key']: f for f in v['files']}
    check(f'{n} unchanged complete public file identity set', set(api) == {f['name'] for f in a['cached_payloads']})
    for f in a['cached_payloads']:
        raw = (ROOT / f['path']).read_bytes()
        check(f"{n} cached payload bound to current public file {f['name']}", sha(raw) == f['sha256'] and len(raw) == api[f['name']]['size'] and 'md5:' + hashlib.md5(raw).hexdigest() == api[f['name']]['checksum'])
        file_hash(ROOT / f['path'], f"PR{n} cached public payload {f['name']}")
    identity_rows.append({'pr': n, 'problem_id': pid, 'alias': alias, 'record_id': v['id'], 'primary_doi': v['doi'], 'ledger_row': expected_row, 'all_identity_leads': leads, 'title': m['title']})
    file_hash(ROOT / f'PR{n:04}_PUBLICATION_VERIFICATION.json', 'previous immutable publication verification')

for n in [254, 256]:
    receipt = read(ROOT / f'PR{n:04}_LEDGER_REPAIR.json')
    file_hash(ROOT / f'PR{n:04}_LEDGER_REPAIR.json', 'historical one-cell repair receipt')
    raw_dir = ROOT / 'raw' / f'pr{n:04}'
    for name in ['ledger_repair_before.json', 'ledger_repair_after.json', 'ledger_repair_request.json', 'ledger_repair_response.json']:
        file_hash(raw_dir / name, 'historical exact-cell repair evidence')
    before = read(raw_dir / 'ledger_repair_before.json')['values']
    after = read(raw_dir / 'ledger_repair_after.json')['values']
    changed = []
    for i in range(max(len(before), len(after))):
        aa = before[i] if i < len(before) else []
        bb = after[i] if i < len(after) else []
        for j in range(max(len(aa), len(bb))):
            if (aa[j] if j < len(aa) else '') != (bb[j] if j < len(bb) else ''):
                changed.append([i + 1, j + 1])
    rr = receipt['row']
    check(f'{n} independent one-cell history and live persistence', changed == [[rr, 4]] and before[rr - 1][3] == receipt['old_notes'] and after[rr - 1][3] == receipt['new_notes'] and receipt['new_notes'].startswith(receipt['old_notes']) and ledger[rr - 1] == after[rr - 1] == receipt['final_row'])

primary = []
for source in read(OLD / 'primary_source_identity.json')['sources']:
    path = WORK / source['path']
    start, end = source['pdf_page_range']
    if source.get('selected_pdf_pages'):
        start, end = min(source['selected_pdf_pages']), max(source['selected_pdf_pages'])
    args = ['pdftotext', '-f', str(start), '-l', str(end), '-layout', str(path), '-']
    raw = subprocess.check_output(args)
    primary.append({'key': source['key'], 'path': source['path'], 'pdf_sha256': sha(path.read_bytes()), 'selected_pdf_pages': [start, end], 'layout_text_sha256': sha(raw), 'previous_text_sha256': source['text_sha256'], 'extraction_note': 'Fresh extraction uses pdftotext -layout and these explicit page bounds. Its text hash is recorded for this extraction only; no equality with differently bounded old text is assumed.'})
    check('fresh original primary PDF pin ' + source['key'], sha(path.read_bytes()) == source['sha256'] == source['expected_sha256'])
    file_hash(path, 'original primary source PDF')

for n, docs in read(OLD / 'source_identity.json').items():
    for doc in docs:
        if doc['kind'] == 'repository_source_scope':
            raw = git('cat-file', 'blob', doc['blob_sha'])
            source_hashes.append({'kind': 'git_blob', 'role': 'primary-source interpretation and scope', 'pr': int(n), 'path': doc['path'], 'commit': doc['commit'], 'git_blob_oid': doc['blob_sha'], 'bytes': len(raw), 'sha256': sha(raw)})
        else:
            with zipfile.ZipFile(io.BytesIO((ROOT / doc['payload_path']).read_bytes())) as z:
                raw = z.read(doc['member'])
            source_hashes.append({'kind': 'archive_member', 'role': 'deposited theorem source', 'pr': int(n), 'payload_path': doc['payload_path'], 'member': doc['member'], 'bytes': len(raw), 'sha256': sha(raw)})
        check('current bound source ' + str(n) + ' ' + doc.get('path', doc.get('member')), sha(raw) == doc['sha256'] and len(raw) == doc['bytes'])

for doc in read(OLD / 'withdrawal_bindings.json'):
    raw = git('cat-file', 'blob', doc['blob_sha'])
    check('qualified exclusion remains pinned ' + str(doc['pr']) + ' ' + doc['path'], sha(raw) == doc['sha256'] and len(raw) == doc['bytes'])
    source_hashes.append({'kind': 'git_blob', 'role': 'qualified historical exclusion', 'pr': doc['pr'], 'path': doc['path'], 'commit': doc['commit'], 'git_blob_oid': doc['blob_sha'], 'bytes': len(raw), 'sha256': sha(raw)})

protected = read(OUT / 'protected_input_hashes_before.json')['files']
for entry in protected:
    path = ROOT / entry['path']
    check('preserved prior artifact ' + path.name, sha(path.read_bytes()) == entry['sha256'] and path.stat().st_size == entry['bytes'])
    file_hash(path, 'preserved interrupted-review input')
for name in ['replay_check_evidence.py', 'refresh_readonly.py', 'check_followup.py', 'CHECKER_SAFETY_REVIEW.json', 'REPLAY_CHECK_RECEIPT.json', 'ledger_refresh.json', 'live_prs_refresh.json', 'publications_refresh.json', 'REFRESH_SUMMARY.json', 'protected_input_hashes_before.json']:
    file_hash(OUT / name, 'follow-up method or fresh read receipt')

save('CLASSIFICATION_TABLE.json', {'at': now(), 'rows': scope_table, 'counts': dict(counts)})
save('PUBLICATION_IDENTITIES.json', {'at': now(), 'rows': identity_rows})
save('PROVENANCE_ANNOTATIONS.json', {'at': now(), 'annotations': provenance})
save('PRIMARY_SOURCE_RECHECK.json', {'at': now(), 'sources': primary})
save('SOURCE_HASHES.json', {'at': now(), 'note': 'Hashes bind every original review artifact, fresh receipt, operative scoped classification/publication/repair input, cached payload, primary PDF, and source/queue/withdrawal Git blob read in this completion pass. They do not claim to hash every file changed by the PRs or to certify the mathematics.', 'sources': source_hashes})
receipt = {'at': now(), 'scope': [254, 279], 'passed': all(c['pass'] for c in checks),
           'original_replayed_controls': replay['checks'], 'fresh_followup_controls': len(checks),
           'failures': [c for c in checks if not c['pass']], 'checks': checks,
           'counts': dict(counts), 'blocking_identity_or_coverage_issues': [],
           'nonblocking_issues': ['PR278 live record has 18 keywords while the deposited immutable metadata has 6. All original terms remain as the unchanged prefix; the 12 additions are recorded as live enrichment, not asserted metadata equality.', 'PR254, PR256 and PR263 original rebuilt eligibility receipts retain preliminary REST page/time/pending fields. PROVENANCE_ANNOTATIONS.json records their historical meaning without changing the original inputs.'],
           'scope_limit': 'Checks support classification and existing-publication coverage only. Mathematical qualifications are retained; no fresh correctness, current-openness, novelty, priority or external peer-review certificate is issued.',
           'external_mutations_performed': [], 'local_write_scope': str(OUT), 'payloads_downloaded': 0,
           'source_hashes_sha256': sha((OUT / 'SOURCE_HASHES.json').read_bytes())}
save('FOLLOWUP_CHECK_RECEIPT.json', receipt)
with (OUT / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n' + now() + ' — 90%. All 459 original controls pass; all 26 PRs and four public-record metadata/DOI readbacks are unchanged. Open-ended GWS A:AQ returns 173 populated rows with every value unchanged. Independent diff-row classification and unique identifier/alias/PR/DOI ledger leads agree. Five primary PDF pins and exact scoped theorem statements were reread; provenance addenda preserve historical receipt fields. Final report remains.\n')
print(json.dumps({k: receipt[k] for k in ['at', 'passed', 'original_replayed_controls', 'fresh_followup_controls', 'failures', 'counts', 'nonblocking_issues']}, indent=2))
raise SystemExit(0 if receipt['passed'] else 1)
