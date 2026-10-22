#!/usr/bin/env python3
"""PR280 fresh read-only full-ledger/account/head evidence; private raw custody."""
import argparse
import json
import re
import subprocess
import uuid
from urllib.parse import urlencode, urlparse
from ops_binding import *


def read_command(arguments):
    run = subprocess.run(arguments, cwd=REPO, capture_output=True, text=True)
    if run.returncode:
        raise RuntimeError('Read-only provider command failed: ' + run.stderr[:700])
    return json.loads(run.stdout)


def account_search(client, query):
    url = client.base + '/api/user/records?' + urlencode({'q': query, 'size': 25})
    seen, found, total, pages = set(), {}, None, 0
    while url:
        if url in seen or urlparse(url).scheme != 'https' or urlparse(url).netloc != urlparse(client.base).netloc:
            raise RuntimeError('Account pagination loop or unexpected destination')
        seen.add(url)
        response = client.request('GET', url)
        hits = response['hits']
        count = hits.get('total')
        if isinstance(count, dict):
            if count.get('relation') != 'eq':
                raise RuntimeError('Inexact account total')
            count = count.get('value')
        if type(count) is not int or count < 0 or (total is not None and total != count):
            raise RuntimeError('Account total absent/changed')
        total = count
        if not isinstance(hits.get('hits'), list):
            raise RuntimeError('Unexpected account record inventory')
        for record in hits['hits']:
            identifier = int(record['id'])
            if identifier <= 0 or identifier in found:
                raise RuntimeError('Invalid or repeated account record')
            identity_projection(record)
            found[identifier] = record
        pages += 1
        url = response.get('links', {}).get('next')
    if len(found) != total:
        raise RuntimeError('Incomplete authenticated account enumeration')
    return {'query': query, 'total': total, 'pages': pages, 'records': list(found.values())}


def validate_pr(pr, expected_head, phase):
    if (not re.fullmatch('[0-9a-f]{40}', expected_head)
            or pr.get('number') != 280 or pr['head']['sha'] != expected_head
            or pr['base']['ref'] != 'main' or pr['base']['repo']['full_name'] != 'AlecKriebel/Math'
            or pr['head']['repo']['full_name'] != 'AlecKriebel/Math'):
        raise RuntimeError('Live PR head/base/destination changed')
    if phase == 'before_integration':
        if pr['state'] != 'open' or pr.get('merged') is not False:
            raise RuntimeError('PR is not the exact open unmerged candidate')
    elif pr.get('merged') is not True or pr['state'] != 'closed':
        raise RuntimeError('Publication/ledger require an already merged PR')


def gather(phase, expected_head, expected_deposit_id=None):
    verify_destination()
    metadata, uploads = manifest()
    start, operation = stamp(), uuid.uuid4().hex
    raw = PRIVATE / ('prepublication_' + operation)
    raw.mkdir(parents=True)
    sheet = read_command(['gws','sheets','spreadsheets','values','get','--params',json.dumps({
        'spreadsheetId': SHEET, 'range': "'Math Puzzles'!A:AQ", 'valueRenderOption':'FORMATTED_VALUE'})])
    atomic_json(raw/'ledger.json', sheet)
    rows = schema_rows(sheet)
    baseline = ledger_baseline(json.loads((ROOT/'raw/pr0280/ledger_live.json').read_text()))
    changed = [i+1 for i in range(max(len(rows),len(baseline)))
               if (rows[i] if i<len(rows) else None) != (baseline[i] if i<len(baseline) else None)]
    ledger_matches = [{'row':i,'values':r} for i,r in enumerate(rows,1)
                      if PATTERN.search(' '.join(r)) or (expected_deposit_id is not None
                      and target_in_row(r,expected_deposit_id))]
    client = zenodo.ZenodoClient('production', zenodo.token_for('production'))
    positive = account_search(client, 'Fibonacci')
    if 23174283 not in {int(r['id']) for r in positive['records']}:
        raise RuntimeError('Authenticated account known-record positive control failed')
    keyword = account_search(client, '"30000156" OR "OWR-768-006" OR "birational" OR "Vivaldi" OR "cycle distribution"')
    full = account_search(client, '')
    for n,v in [('account_positive_control',positive),('account_keyword',keyword),('account_complete',full)]:
        atomic_json(raw/(n+'.json'),v)
    checksums = {u['md5'] for u in uploads}
    targets = {int(r['id']):r for r in keyword['records']}
    for record in full['records']:
        projection = identity_projection(record)
        if (PATTERN.search(json.dumps(projection,ensure_ascii=False)) or any(
                str(f.get('checksum','')).lower().removeprefix('md5:') in checksums
                for f in record['files'])):
            targets[int(record['id'])] = record
    all_ids = {int(r['id']) for r in full['records']}
    if not set(targets).issubset(all_ids):
        raise RuntimeError('Keyword records missing from whole account; retry read-only collection')
    if expected_deposit_id is not None and expected_deposit_id not in targets:
        raise RuntimeError('Exact expected draft/record absent from complete model/file comparison')
    identity_ids=(record_identity_ids(next(r for r in full['records'] if int(r['id'])==expected_deposit_id),expected_deposit_id)
                  if expected_deposit_id is not None else [])
    ledger_matches=[{'row':i,'values':r} for i,r in enumerate(rows,1) if PATTERN.search(' '.join(r))
                    or (expected_deposit_id is not None and target_in_row(r,expected_deposit_id,identity_ids))]
    pr = read_command(['gh','api','--hostname','github.com','repos/AlecKriebel/Math/pulls/280'])
    main = read_command(['gh','api','--hostname','github.com','repos/AlecKriebel/Math/git/ref/heads/main'])
    atomic_json(raw/'pr.json',pr)
    validate_pr(pr,expected_head,phase)
    states = []
    for p in (REPO/'.zenodo-state').glob('*.json'):
        value = json.loads(p.read_text())
        if PATTERN.search(json.dumps(value,ensure_ascii=False)):
            states.append({'path':p.relative_to(REPO).as_posix(),'sha256':sha(p.read_bytes()),
                           'deposit_id':value.get('id',value.get('deposit_id'))})
    receipt = {'started_utc':start,'completed_utc':stamp(),'operation':operation,'phase':phase,
        'read_only':True,'expected_identity_record_ids':identity_ids,'expected_pr_head':expected_head,'expected_deposit_id':expected_deposit_id,
        'release_manifest_sha256':RELEASE_SHA,'release_files':release()['files'],
        'ledger_rows':len(rows),'ledger_sha256':digest(rows),'ledger_matches':ledger_matches,
        'ledger_changed_rows_since_initial_candidate_check':changed,
        'account_complete_total':full['total'],'account_complete_pages':full['pages'],
        'account_complete_sha256':sha((raw/'account_complete.json').read_bytes()),
        'account_positive_control':'PASS_23174283','account_targets':sorted(targets),
        'unexpected_account_matches':[{'id':i} for i in targets if i!=expected_deposit_id],
        'local_deposit_state_matches':states,'live_pr':{'state':pr['state'],'merged':pr['merged'],
        'draft':pr['draft'],'head':pr['head']['sha']},'live_main':main['object']['sha'],
        'raw_receipts':str(raw),'receipt':str(raw/'gate.json'),
        'scope':'Fresh read-only observations; leads require root exact identity reconciliation; no scientific clearance or cross-service lock.'}
    atomic_json(raw/'gate.json',receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',required=True,choices=['before_integration','before_stage','before_publish','before_ledger'])
    parser.add_argument('--expected-pr-head',required=True)
    parser.add_argument('--expected-deposit-id',type=int)
    args=parser.parse_args()
    gate=gather(args.phase,args.expected_pr_head,args.expected_deposit_id)
    print(json.dumps({'private_receipt':gate['receipt'],'phase':args.phase,'read_only':True,
                      'account_complete_total':gate['account_complete_total'],'ledger_rows':gate['ledger_rows']},indent=2))


if __name__=='__main__':
    main()
